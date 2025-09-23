import json, os, time, hashlib
from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd
import httpx
from req import ScoreReq
from model import predict as model_predict
from ledger import write_evidence
OPA_URL = os.getenv("OPA_URL","http://localhost:8181")
app = FastAPI(title="RiskOps Score (Pro)", version="0.2.0")

def read_health():
    try: return json.loads(Path("state/health.json").read_text())
    except Exception: return {"overall": "fail"}

def policy_guard(meta):
    health = read_health()
    payload = {"input": {"health": health, "meta": meta}}
    try:
        r = httpx.post(f"{OPA_URL}/v1/data/guard/allow", json=payload, timeout=2.0)
        allowed = r.json().get("result", False)
        if not allowed:
            reason = httpx.post(f"{OPA_URL}/v1/data/guard/reason", json=payload, timeout=2.0).json().get("result", "blocked")
            return False, reason
        return True, "ok"
    except Exception as e:
        return False, f"OPA error: {e}"

def get_features(keys):
    p = Path("features/features.parquet")
    if not p.exists(): return {"amt_norm": 0.0, "user_txn_rate": 0.0}
    df = pd.read_parquet(p)
    import hashlib as _h
    uid = str(keys.get("user_id","anon"))
    tok = "tok_" + _h.sha256(uid.encode()).hexdigest()[:12]
    row = df[df["user_id_token"] == tok]
    if row.empty: return {"amt_norm": 0.0, "user_txn_rate": 0.0}
    r = row.iloc[0]
    return {"amt_norm": float(r["amt_norm"]), "user_txn_rate": float(r["user_txn_rate"])}

@app.post("/score")
def score(req: ScoreReq):
    allow, reason = policy_guard(req.meta)
    if not allow:
        raise HTTPException(412, detail={"reason":"policy_block", "why": reason, "health": read_health()})
    feats = get_features(req.keys)
    yhat = model_predict(feats)
    decision = "flag" if yhat>0.8 else "allow"
    write_evidence({
        "trace_id": hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:16],
        "service": "riskops-score",
        "model": {"name":"heuristic_v0","version":"0.0.2"},
        "data": {"contract":"transactions_v3","schema_hash":"demo"},
        "checks": read_health(),
        "inputs": {"features": feats},
        "output": {"score": yhat, "decision": decision},
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })
    return {"score": yhat, "decision": decision}

@app.get("/business")
def business(vertical: str = "fraud_detection"):
    from business.impact import load_vertical, roi_summary
    v = load_vertical(vertical)
    return {"vertical": vertical, "kpis": v.get("kpis", {}), "roi": roi_summary(vertical)}
