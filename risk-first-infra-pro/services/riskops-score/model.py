def predict(feats: dict) -> float:
    score = 0.5 + 0.4*abs(feats.get("amt_norm",0.0)) + 0.1*(feats.get("user_txn_rate",0.0) > 3)
    return max(0.0, min(1.0, score))
