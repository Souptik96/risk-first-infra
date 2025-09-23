import pandas as pd, numpy as np, uuid, random, time
from pathlib import Path
Path("data").mkdir(exist_ok=True, parents=True)

def gen(n=5000, ref=False):
    rows=[]
    for _ in range(n):
        rows.append({"txn_id": str(uuid.uuid4()),"user_id": f"user_{random.randint(1,300)}","amount": round(max(0, np.random.lognormal(3.0, 0.6)), 2),"currency": random.choice(["USD","INR","EUR"]),"ts": int(time.time())})
    df = pd.DataFrame(rows)
    out = "data/ref_transactions.csv" if ref else "data/transactions.csv"
    df.to_csv(out, index=False)
    print("Wrote", out)

if __name__ == "__main__":
    gen(20000, ref=True)
    gen(5000, ref=False)
