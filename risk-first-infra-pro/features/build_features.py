import pandas as pd
from pathlib import Path

def build_features(txn_path="data/transactions_tokenized.csv", out_path="features/features.parquet"):
    Path("features").mkdir(exist_ok=True, parents=True)
    df = pd.read_csv(txn_path)
    amt_norm = (df["amount"] - df["amount"].mean()) / (df["amount"].std() + 1e-6)
    df["amt_norm"] = amt_norm
    df["user_txn_rate"] = df.groupby("user_id_token")["txn_id"].transform("count").astype(float)
    df[["user_id_token","amt_norm","user_txn_rate"]].to_parquet(out_path, index=False)
    print("Wrote features →", out_path)

if __name__ == "__main__": build_features()
