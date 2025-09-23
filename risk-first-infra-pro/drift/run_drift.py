import json
from pathlib import Path
import pandas as pd
import numpy as np

def simple_psi(ref, cur, bins=10, eps=1e-6):
    qs = np.linspace(0, 1, bins+1)
    refq = np.quantile(ref + np.random.normal(0,1e-9, size=len(ref)), qs)
    ref_hist, _ = np.histogram(ref, bins=refq)
    cur_hist, _ = np.histogram(cur, bins=refq)
    ref_pct = ref_hist / (ref_hist.sum() + eps)
    cur_pct = cur_hist / (cur_hist.sum() + eps)
    psi = np.sum((cur_pct - ref_pct) * np.log((cur_pct + eps) / (ref_pct + eps)))
    return float(psi)

def run_drift(ref_path="data/ref_transactions.csv", cur_path="data/transactions.csv"):
    Path("state").mkdir(exist_ok=True, parents=True)
    ref = pd.read_csv(ref_path)
    cur = pd.read_csv(cur_path)
    psi = 0.0 if "amount" not in ref or "amount" not in cur else simple_psi(ref["amount"].values, cur["amount"].values, bins=10)
    status = "pass" if psi < 0.2 else "fail"
    Path("state/drift.json").write_text(json.dumps({"drift_status": status, "psi_amount": psi}, indent=2))
    print("Drift:", {"drift_status": status, "psi_amount": psi})

if __name__ == "__main__": run_drift()
