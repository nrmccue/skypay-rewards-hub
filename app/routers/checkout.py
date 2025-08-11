from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
import uuid

from .wallet import USERS

router = APIRouter()

FX = {"USD": 1.0, "EUR": 1.08, "GBP": 1.30}
POINT_VALUE_USD = 0.012
EARN_RATE = {"flight": 3.0, "ancillary": 2.0, "upgrade": 2.5}


class Item(BaseModel):
    sku: str
    name: str
    category: Literal["flight", "ancillary", "upgrade", "other"] = "other"
    price: float
    qty: int = 1


class CheckoutRequest(BaseModel):
    user_id: str
    currency: str = "USD"
    payment_method: str = "card:visa"
    use_points: bool = False
    points_to_use: int | None = None
    items: List[Item]


@router.post("/checkout")
def checkout(req: CheckoutRequest):
    user = USERS.get(req.user_id)
    if not user:
        raise HTTPException(404, "user not found")
    if req.currency not in FX:
        raise HTTPException(400, "unsupported currency")

    subtotal = round(sum(i.price * i.qty for i in req.items), 2)
    subtotal_usd = round(subtotal * FX[req.currency], 2)

    # Points usage (cap at 80% of subtotal_usd)
    points_redeemed = 0
    discount_usd = 0.0
    if req.use_points:
        max_pts = int((0.8 * subtotal_usd) / POINT_VALUE_USD)
        if req.points_to_use is None:
            points_redeemed = min(user["points"], max_pts)
        else:
            pts = max(0, int(req.points_to_use))
            points_redeemed = min(user["points"], min(pts, max_pts))
        discount_usd = round(points_redeemed * POINT_VALUE_USD, 2)
        user["points"] -= points_redeemed

    cash_due_usd = round(max(0.0, subtotal_usd - discount_usd), 2)
    payment = {
        "tx_id": f"pay_{uuid.uuid4().hex[:8]}",
        "status": "approved",
        "amount_usd": cash_due_usd,
        "method": req.payment_method,
    }

    # Earn points on cash portion only, proportional by category
    points_earned = 0
    if cash_due_usd > 0:
        for it in req.items:
            cat_amount_usd = it.price * it.qty * FX[req.currency]
            share = cat_amount_usd / subtotal_usd if subtotal_usd else 0
            earn_base = cash_due_usd * share
            rate = EARN_RATE.get(it.category, 1.0)
            points_earned += int(earn_base * rate)

    user["points"] += points_earned

    order = {
        "order_id": f"ord_{uuid.uuid4().hex[:8]}",
        "user_id": req.user_id,
        "subtotal": subtotal,
        "currency": req.currency,
        "subtotal_usd": subtotal_usd,
        "points_redeemed": points_redeemed,
        "points_earned": points_earned,
        "cash_collected_usd": cash_due_usd,
        "payment": payment,
    }
    return order
