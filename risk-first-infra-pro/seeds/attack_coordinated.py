import pandas as pd, uuid, random, time, json
from pathlib import Path

def simulate():
    rows=[]
    base_users=[f"a_to_{i}" for i in range(1,80)]
    for u in base_users:
        for _ in range(random.randint(5,15)):
            rows.append({"txn_id": str(uuid.uuid4()),"user_id": u,"amount": round(random.uniform(1, 12),2),"currency": random.choice(["USD","INR","EUR"]),"ts": int(time.time())})
        for _ in range(random.randint(1,3)):
            rows.append({"txn_id": str(uuid.uuid4()),"user_id": u,"amount": round(random.uniform(800, 4000),2),"currency": random.choice(["USD","INR","EUR"]),"ts": int(time.time())})
    cur=pd.read_csv("data/transactions.csv")
    df=pd.concat([cur, pd.DataFrame(rows)], ignore_index=True)
    df.to_csv("data/transactions.csv", index=False)
    Path("state/privacy.json").write_text(json.dumps({"privacy_status":"fail","reason":"PII anomaly"}, indent=2))
    print("Attack simulated: privacy fail.")

if __name__=="__main__": simulate()
