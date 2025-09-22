import yaml, json
from pathlib import Path
def load_vertical(name): return yaml.safe_load(Path('business/impact.yaml').read_text())['verticals'][name]
def roi_summary(v='fraud_detection'):
    if v=='fraud_detection': inv, ret = 150000, 1800000
    elif v=='content_moderation': inv, ret = 120000, 45000*12*0.8
    else: inv, ret = 180000, 650000
    return {'vertical': v, 'investment_usd': inv, 'annual_return_usd': int(ret), 'roi_pct': round((ret-inv)/inv*100,2)}
if __name__ == '__main__':
    for v in ['fraud_detection','content_moderation','supply_chain_risk']:
        print(json.dumps(roi_summary(v)))