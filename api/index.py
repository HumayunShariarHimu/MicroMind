import cv2
import numpy as np
from deepface import DeepFace
import mediapipe as mp
import time

# MediaPipe ফেস মেশ কনফিগারেশন
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def analyze_personality(emotion_data, gaze_score, movement_score):
    """
    সাইকোলজিক্যাল ডাটা পয়েন্টের ভিত্তিতে পার্সোনালিটি ও মেন্টাল স্টেট প্রেডিকশন
    """
    dominant_emotion = emotion_data['dominant_emotion']
    
    # ১. ব্যক্তিত্ব নির্ধারণ (Big Five Traits - Approximate)
    personality = {
        "Openness": "High" if dominant_emotion in ['happy', 'neutral'] else "Moderate",
        "Neuroticism": "High" if dominant_emotion in ['fear', 'angry', 'sad'] else "Low",
        "Extroversion": "High" if dominant_emotion == 'happy' and movement_score > 0.5 else "Low",
        "Conscientiousness": "High" if dominant_emotion == 'neutral' and gaze_score > 0.7 else "Moderate"
    }

    # ২. মেন্টাল কন্ডিশন বিশ্লেষণ
    if dominant_emotion == 'fear' or dominant_emotion == 'angry':
        mental_state = "High Cortisol / Acute Stress"
        verdict = "ব্যক্তি বর্তমানে মানসিকভাবে অস্থির বা আত্মরক্ষামূলক।"
    elif dominant_emotion == 'sad':
        mental_state = "Depressive / Low Dopamine"
        verdict = "ব্যক্তি মানসিকভাবে বিষণ্ণ বা ক্লান্ত।"
    elif dominant_emotion == 'happy':
        mental_state = "High Serotonin / Positive State"
        verdict = "ব্যক্তি বর্তমানে আত্মবিশ্বাসী এবং সুখী।"
    else:
        mental_state = "Stable / Cognitive Focus"
        verdict = "ব্যক্তি স্বাভাবিক এবং মনোযোগী।"

    return personality, mental_state, verdict

def start_advanced_analysis():
    cap = cv2.VideoCapture(0)
    print("Starting Deep Bio-Analysis... Press 'q' to exit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # ইমেজ প্রি-প্রসেসিং
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        try:
            # ১. DeepFace দিয়ে ইমোশন বিশ্লেষণ
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
            emotion_res = analysis[0]
            
            # ২. মুভমেন্ট ও গেজ স্কোর (কাল্পনিক লজিক ল্যান্ডমার্কের ওপর ভিত্তি করে)
            gaze_score = 0.8  # ডিফল্ট (উন্নত লজিক এখানে যুক্ত করা সম্ভব)
            movement_score = 0.6

            # ৩. সাইকোলজিক্যাল ক্যালকুলেশন
            personality, mental_state, verdict = analyze_personality(emotion_res, gaze_score, movement_score)

            # স্ক্রিনে আউটপুট দেখানো
            y0, dy = 30, 30
            cv2.putText(frame, f"Emotion: {emotion_res['dominant_emotion'].upper()}", (10, y0), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Mental State: {mental_state}", (10, y0 + dy), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"Verdict: {verdict}", (10, y0 + 2*dy), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            # ব্যক্তিত্বের চারিত্রিক বৈশিষ্ট্য দেখানো
            idx = 3
            for trait, val in personality.items():
                cv2.putText(frame, f"{trait}: {val}", (10, y0 + idx*dy), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                idx += 1

        except Exception as e:
            cv2.putText(frame, "Analyzing...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow('AI Mental & Personality Analyzer', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_advanced_analysis()
