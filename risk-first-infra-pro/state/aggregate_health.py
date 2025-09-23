import json
from pathlib import Path

def read_json(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return {}

def aggregate():
    quality = read_json("state/quality.json")
    drift = read_json("state/drift.json")
    privacy = read_json("state/privacy.json")
    overall = "pass"
    for key, src in [("quality_status",quality), ("drift_status",drift), ("privacy_status",privacy)]:
        if src.get(key) != "pass": overall = "fail"
    out = {"overall": overall, "quality_status": quality.get("quality_status","unknown"), "drift_status": drift.get("drift_status","unknown"), "privacy_status": privacy.get("privacy_status","unknown"), "policy_status": "pass" if overall=="pass" else "fail"}
    Path("state/health.json").write_text(json.dumps(out, indent=2))
    print("Health:", out)

if __name__ == "__main__": aggregate()
