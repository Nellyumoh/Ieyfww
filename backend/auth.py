from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase_client import supabase
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
otp_log = {}
OTP_MAX_PER_HOUR = 3

class SendOTPReq(BaseModel):
    phone: str

class VerifyOTPReq(BaseModel):
    phone: str
    token: str

def _rate_limit_ok(phone: str) -> bool:
    now = datetime.now(timezone.utc)
    history = [t for t in otp_log.get(phone, []) if now - t < timedelta(hours=1)]
    otp_log[phone] = history
    return len(history) < OTP_MAX_PER_HOUR

@router.post("/send-otp")
def send_otp(req: SendOTPReq):
    if not _rate_limit_ok(req.phone):
        raise HTTPException(429, "Too many OTP requests. Try again in an hour.")
    try:
        supabase.auth.sign_in_with_otp({"phone": req.phone})
    except Exception as e:
        raise HTTPException(400, f"OTP send failed: {e}")
    otp_log.setdefault(req.phone, []).append(datetime.now(timezone.utc))
    return {"ok": True, "message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(req: VerifyOTPReq):
    try:
        res = supabase.auth.verify_otp({"phone": req.phone, "token": req.token, "type": "sms"})
    except Exception as e:
        raise HTTPException(401, f"Invalid OTP: {e}")
    if not res.session:
        raise HTTPException(401, "No session returned")
    return {"access_token": res.session.access_token, "user_id": res.user.id}
