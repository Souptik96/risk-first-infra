from pydantic import BaseModel
from typing import Dict, Any

class ScoreReq(BaseModel):
    keys: Dict[str, Any]
    meta: Dict[str, Any] = {}
