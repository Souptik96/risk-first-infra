import pandas as pd, random, time
from pathlib import Path
Path("data").mkdir(exist_ok=True, parents=True)

def gen(n=2000):
    base=["Hello world","I love this!","This is stupid","You idiot","Have a nice day"]
    rows=[{"event_id": f"e_{i}","user_id": f"user_{random.randint(1,300)}","text": random.choice(base),"ts": int(time.time())} for i in range(n)]
    pd.DataFrame(rows).to_csv("data/content.csv", index=False)
    print("Wrote data/content.csv")

if __name__ == "__main__": gen()
