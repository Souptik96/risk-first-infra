import json, yaml
from pathlib import Path

def load_vertical(name: str):
    cfg = yaml.safe_load(Path("business/impact.yaml").read_text())
    vert = cfg["verticals"].get(name)
    if not vert: raise ValueError(f"Unknown vertical: {name}")
    return vert

def roi_summary(vertical: str):
    if vertical == "fraud_detection": invest, annual_return = 150_000, 1_800_000
    elif vertical == "content_moderation": invest, annual_return = 120_000, int(45_000*12*0.8)
    else: invest, annual_return = 180_000, 650_000
    roi_pct = (annual_return - invest) / invest * 100
    return {"vertical": vertical, "investment_usd": invest, "annual_return_usd": int(annual_return), "roi_pct": round(roi_pct, 2)}

if __name__ == "__main__":
    for v in ["fraud_detection","content_moderation","supply_chain_risk"]:
        print(json.dumps(roi_summary(v)))
