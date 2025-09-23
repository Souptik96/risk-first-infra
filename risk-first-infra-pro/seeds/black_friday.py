import pandas as pd, numpy as np, time, json
from pathlib import Path

def simulate():
    cur=pd.read_csv("data/transactions.csv")
    surge=cur.sample(len(cur), replace=True).copy()
    surge["amount"]=surge["amount"]*np.random.lognormal(0.3,0.5,size=len(surge))
    surge["ts"]=int(time.time())
    df=pd.concat([cur,surge],ignore_index=True)
    df.to_csv("data/transactions.csv",index=False)
    Path("state/drift.json").write_text(json.dumps({"drift_status":"fail","psi_amount":0.35}, indent=2))
    print("Black Friday simulated: drift fail.")

if __name__=="__main__": simulate()
