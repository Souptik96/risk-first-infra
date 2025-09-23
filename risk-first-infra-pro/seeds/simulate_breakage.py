import json
from pathlib import Path
bad={"overall":"fail","quality_status":"fail","drift_status":"fail","privacy_status":"pass","policy_status":"fail"}
Path("state").mkdir(exist_ok=True, parents=True)
Path("state/health.json").write_text(json.dumps(bad, indent=2))
print("Simulated breakage → state/health.json")
