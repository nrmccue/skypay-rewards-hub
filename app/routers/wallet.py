from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import time

router = APIRouter()

# In-memory demo users
USERS: Dict[str, dict] = {
    "u_alex": {"user_id": "u_alex", "name": "Alex Johnson", "tier": "gold", "points": 8200, "history": [], "travel_credits": []},
    "u_bailey": {"user_id": "u_bailey", "name": "Bailey Kim", "tier": "silver", "points": 1200, "history": [], "travel_credits": []},
}

class RedeemRequest(BaseModel):
    points: int

@router.get("/{user_id}")
def get_wallet(user_id: str):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(404, "user not found")
    return user

@router.post("/{user_id}/redeem")
def redeem_points(user_id: str, req: RedeemRequest):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(404, "user not found")
    if req.points <= 0 or req.points > user["points"]:
        raise HTTPException(400, "invalid or insufficient points")
    user["points"] -= req.points
    value_usd = round(req.points * 0.012, 2)
    user["history"].append({"ts": int(time.time()), "type": "redeem", "points": req.points, "value_usd": value_usd})
    return {"user_id": user_id, "redeemed_points": req.points, "value_usd": value_usd, "balance": user["points"]}
