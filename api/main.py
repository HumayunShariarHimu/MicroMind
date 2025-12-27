from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class BioAnalysisData(BaseModel):
    baseline_jitter: float
    current_jitter: float
    brow_dist: float
    eye_ratio: float
    pulse_val: float
    is_triggered: bool

@app.post("/api/analyze")
async def analyze(data: BioAnalysisData):
    # স্কোরিং লজিক
    stress_score = 0
    
    # ১. হার্টবিট/পালস ইনটেনসিটি বিশ্লেষণ (৩০%)
    pulse_stress = min(data.pulse_val * 8, 30)
    
    # ২. মাইক্রো-ট্রেমর বা পেশির কাঁপুনি (৩৫%)
    jitter_diff = abs(data.current_jitter - data.baseline_jitter)
    vibration_score = min(jitter_diff * 15, 35)
    
    # ৩. কপাল ও চোখের স্থিরতা (৩৫%)
    facial_score = 0
    if data.brow_dist < 0.18: facial_score += 17.5
    if data.eye_ratio < 0.12: facial_score += 17.5

    total = pulse_stress + vibration_score + facial_score
    if data.is_triggered: total *= 1.2
    total = min(total, 100)

    verdict = "শান্ত ও স্বাভাবিক"
    if total > 75: verdict = "উচ্চ মানসিক চাপ / মিথ্যা বলার সম্ভাবনা"
    elif total > 45: verdict = "চিন্তিত বা অবচেতন প্রতিক্রিয়া"

    return {
        "score": round(total, 2),
        "verdict": verdict,
        "pulse_status": "অস্থির" if pulse_stress > 20 else "স্বাভাবিক"
    }
