import json
from pathlib import Path
import pandas as pd
Path("state").mkdir(exist_ok=True, parents=True)

def run_quality(in_path="data/transactions.csv"):
    df = pd.read_csv(in_path)
    issues = []
    if df["txn_id"].isna().any(): issues.append("null_txn_id")
    if (df["amount"] < 0).any(): issues.append("neg_amount")
    if "currency" in df.columns and (~df["currency"].isin(["USD","INR","EUR"]).astype(bool)).any(): issues.append("bad_currency_enum")
    status = "pass" if not issues else "fail"
    Path("state/quality.json").write_text(json.dumps({"quality_status": status, "issues": issues}, indent=2))
    print("Quality:", {"quality_status": status, "issues": issues})

if __name__ == "__main__": run_quality()
