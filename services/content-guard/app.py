from fastapi import FastAPI
from business.impact import load_vertical, roi_summary
app = FastAPI()
@app.get('/business')
def business(vertical: str = 'fraud_detection'):
    v = load_vertical(vertical)
    return {'vertical': vertical, 'kpis': v.get('kpis', {}), 'roi': roi_summary(vertical)}
