import json, hashlib
from pathlib import Path
LEDGER_DIR = Path("ledger_data"); LEDGER_DIR.mkdir(exist_ok=True, parents=True)
CHAIN_FILE = LEDGER_DIR / "evidence.jsonl"
HEAD_FILE = LEDGER_DIR / "head.sha"

def _head(): return HEAD_FILE.read_text().strip() if HEAD_FILE.exists() else ""

def _write_head(h): HEAD_FILE.write_text(h)

def write_evidence(packet: dict):
    prev = _head()
    body = json.dumps(packet, sort_keys=True)
    new_hash = hashlib.sha256((prev + body).encode()).hexdigest()
    packet["_prev"] = prev
    packet["_hash"] = new_hash
    with open(CHAIN_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(packet) + "\n")
    _write_head(new_hash)
    print("Ledger append:", new_hash[:12])
