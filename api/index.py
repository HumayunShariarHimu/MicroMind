from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class BioAnalysisData(BaseModel):
    baseline_jitter: float
    current_jitter: float
    brow_dist: float
    eye_ratio: float
    mouth_tension: float
    pulse_val: float
    mode: str # 'mouse', 'camera', 'heartbeat'
    is_triggered: bool

@app.post("/api/analyze")
async def analyze(data: BioAnalysisData):
    # সাইকোলজিক্যাল থ্রেশহোল্ড (Based on FACS research)
    score = 0
    feedback = ""
    
    # ১. মাইক্রো-এক্সপ্রেশন বিশ্লেষণ (Ekman's Theory)
    if data.brow_dist < 0.15: # ভ্রু কুঁচকানো (চাপ বা রাগ)
        score += 25
        feedback += "Cognitive Load detected. "
    if data.eye_ratio < 0.1: # ঘনঘন পলক বা চোখ সরু করা (সন্দেহ)
        score += 20
        feedback += "Possible avoidance behavior. "
    if data.mouth_tension > 0.4: # ঠোঁটে চাপ (তথ্য গোপন)
        score += 20
        feedback += "Speech suppression signs. "

    # ২. হার্টবিট এবং বায়ো-রিদম (PPG analysis)
    # উচ্চ ফ্রিকোয়েন্সি পালস মানে 'Fight or Flight' মোড
    pulse_impact = min(data.pulse_val * 10, 35)
    score += pulse_impact

    # ৩. মাউস ট্রেমর (Subconscious tremors)
    jitter_factor = abs(data.current_jitter - data.baseline_jitter)
    score += min(jitter_factor * 12, 30)

    if data.is_triggered: score *= 1.3 # প্রশ্ন করার মুহূর্তে সেনসিটিভিটি বৃদ্ধি
    score = min(score, 100)

    # সাইকোলজিক্যাল ভার্ডিক্ট (Psychological Research Based)
    if score > 80:
        verdict = "HIGH DECEPTION / PANIC"
        mind_state = "অবচেতন মন আত্মরক্ষামূলক অবস্থানে (Defensive Mode)। উত্তরের সত্যতা প্রশ্নবিদ্ধ।"
    elif score > 50:
        verdict = "COGNITIVE CONFLICT"
        mind_state = "মস্তিষ্ক তথ্য প্রসেস করতে হিমশিম খাচ্ছে। ব্যক্তি অস্বস্তিতে বা দ্বিধায় আছেন।"
    else:
        verdict = "NEUTRAL / COHERENT"
        mind_state = "মন শান্ত এবং ভাবনার সাথে উত্তরের সামঞ্জস্য রয়েছে (Cognitive Coherence)।"

    return {
        "score": round(score, 2),
        "verdict": verdict,
        "mind_state": mind_state,
        "scientific_feedback": feedback,
        "mode_active": data.mode
    }

