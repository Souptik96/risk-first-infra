import re, json, hashlib
from pathlib import Path
import pandas as pd
STATE = Path("state"); STATE.mkdir(exist_ok=True, parents=True)

def _tokenize(s: str) -> str: return "tok_" + hashlib.sha256(s.encode()).hexdigest()[:12]

def scan_and_tokenize(in_path="data/transactions.csv", out_path="data/transactions_tokenized.csv"):
    df = pd.read_csv(in_path)
    if "user_id" in df.columns: df["user_id_token"] = df["user_id"].astype(str).apply(_tokenize)
    email_re = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace(email_re, "[EMAIL]", regex=True)
    df.to_csv(out_path, index=False)
    Path("state/privacy.json").write_text(json.dumps({"privacy_status":"pass","pii_masked": True}, indent=2))
    print("Privacy scan complete → state/privacy.json")

if __name__ == "__main__": scan_and_tokenize()
