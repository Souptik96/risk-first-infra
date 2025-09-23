import os, json, time, hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
from pathlib import Path
from ledger import write_evidence
OPA_URL = os.getenv("OPA_URL","http://localhost:8181")
TOXIC_WORDS = {"idiot","stupid","hate","kill"}
class GuardReq(BaseModel):
    text: str
    meta: Dict[str, Any] = {}
app = FastAPI(title="Content Guard (Pro)", version="0.2.0")

def read_health():
    try: return json.loads(Path("state/health.json").read_text())
    except Exception: return {"overall":"fail"}

def is_toxic(text: str) -> bool:
    t = text.lower(); return any(w in t for w in TOXIC_WORDS)

@app.post("/check")
def check(req: GuardReq):
    health = read_health()
    if health.get("overall") != "pass":
        raise HTTPException(412, detail={"reason":"policy_block","health":health})
    toxic = is_toxic(req.text)
    decision = "block" if toxic else "allow"
    write_evidence({
        "trace_id": hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:16],
        "service": "content-guard",
        "model": {"name":"regex_rules","version":"0.0.2"},
        "data": {"contract":"content_events_v1"},
        "checks": health,
        "inputs": {"len": len(req.text)},
        "output": {"toxic": toxic, "decision": decision},
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })
    return {"toxic": toxic, "decision": decision}

@app.get("/business")
def business(vertical: str = "content_moderation"):
    from business.impact import load_vertical, roi_summary
    v = load_vertical(vertical)
    return {"vertical": vertical, "kpis": v.get("kpis", {}), "roi": roi_summary(vertical)}
