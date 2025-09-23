import json
from pathlib import Path

def combine_latest(n=20):
    chain=Path("ledger_data/evidence.jsonl")
    if not chain.exists():
        print("No evidence yet."); return
    lines=chain.read_text().strip().splitlines()[-n:]
    packets=[json.loads(x) for x in lines]
    Path("docs/evidence_snapshot.json").write_text(json.dumps(packets, indent=2))
    print(f"Wrote docs/evidence_snapshot.json ({len(packets)} packets).")

if __name__=="__main__": combine_latest()
