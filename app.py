from flask import Flask, render_template, request
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# -------------------------------
# Knowledge base (Physics + Maths)
# -------------------------------

answers = {
    # ---------- PHYSICS ----------
    "ohm": {
        "keywords": ["ohm", "ओम", "ওহম", "ಓಂ"],
        "en": "Ohm’s Law states that voltage is directly proportional to current (V = IR).",
        "hi": "ओम का नियम कहता है कि वोल्टेज धारा के समानुपाती होता है (V = IR)।",
        "bn": "ওহমের সূত্র অনুযায়ী ভোল্টেজ কারেন্টের সমানুপাতিক (V = IR)।",
        "kn": "ಓಮ್‌ನ ನಿಯಮವು ವೋಲ್ಟೇಜ್ ವಿದ್ಯುತ್ ಪ್ರವಾಹಕ್ಕೆ ಅನುಪಾತವಾಗಿರುತ್ತದೆ (V = IR)."
    },

    "newton": {
        "keywords": ["newton", "न्यूटन", "নিউটন", "ನ್ಯೂಟನ್"],
        "en": "Newton’s First Law states that a body remains at rest or in motion unless acted upon by an external force.",
        "hi": "न्यूटन का पहला नियम कहता है कि कोई वस्तु स्थिर या गतिशील रहती है जब तक उस पर बाहरी बल न लगे।",
        "bn": "নিউটনের প্রথম সূত্র অনুযায়ী বাহ্যিক বল না থাকলে বস্তু স্থির বা গতিশীল থাকে।",
        "kn": "ನ್ಯೂಟನ್‌ನ ಮೊದಲ ನಿಯಮವು ಹೊರಗಿನ ಬಲವಿಲ್ಲದೆ ವಸ್ತು ಸ್ಥಿರವಾಗಿರುತ್ತದೆ ಎಂದು ಹೇಳುತ್ತದೆ."
    },

    "kinetic": {
        "keywords": ["kinetic", "गतिज", "গতিশক্তি", "ಚಲನಾ"],
        "en": "Kinetic energy is the energy possessed by a body due to its motion.",
        "hi": "गतिज ऊर्जा वह ऊर्जा है जो वस्तु की गति के कारण होती है।",
        "bn": "গতিশক্তি হলো বস্তুর গতির কারণে সৃষ্ট শক্তি।",
        "kn": "ಚಲನಾ ಶಕ್ತಿ ವಸ್ತುವಿನ ಚಲನೆಯಿಂದ ಉಂಟಾಗುತ್ತದೆ."
    },

    "gravity": {
        "keywords": ["gravity", "गुरुत्वाकर्षण", "মাধ্যাকর্ষণ", "ಗುರುತ್ವ"],
        "en": "Gravity is the force that attracts objects towards the Earth.",
        "hi": "गुरुत्वाकर्षण वह बल है जो वस्तुओं को पृथ्वी की ओर खींचता है।",
        "bn": "মাধ্যাকর্ষণ বস্তুগুলোকে পৃথিবীর দিকে আকর্ষণ করে।",
        "kn": "ಗುರುತ್ವಾಕರ್ಷಣವು ವಸ್ತುಗಳನ್ನು ಭೂಮಿಯತ್ತ ಆಕರ್ಷಿಸುತ್ತದೆ."
    },

    # ---------- MATHEMATICS ----------
    "pythagoras": {
        "keywords": ["pythagoras", "पाइथागोरस", "পিথাগোরাস","ಪೈಥಾಗೋರಸ್"],
        "en": "In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides.",
        "hi": "समकोण त्रिभुज में कर्ण का वर्ग अन्य दो भुजाओं के वर्गों के योग के बराबर होता है।",
        "bn": "সমকোণী ত্রিভুজে অতিভুজের বর্গ অপর দুই বাহুর বর্গের যোগফলের সমান।",
        "kn": "ಸಮಕೋಣ ತ್ರಿಭುಜದಲ್ಲಿ ಹೈಪೋಟೆನ್ಯೂಸ್‌ನ ವರ್ಗವು ಉಳಿದ ಎರಡು ಬದಿಗಳ ವರ್ಗಗಳ ಮೊತ್ತಕ್ಕೆ ಸಮಾನ."
    },

    "quadratic": {
        "keywords": ["quadratic", "द्विघात", "দ্বিঘাত","ದ್ವಿಘಾತ"],
        "en": "A quadratic equation is of the form ax² + bx + c = 0.",
        "hi": "द्विघात समीकरण का रूप ax² + bx + c = 0 होता है।",
        "bn": "দ্বিঘাত সমীকরণের রূপ ax² + bx + c = 0।",
        "kn": "ದ್ವಿಘಾತ ಸಮೀಕರಣದ ರೂಪ ax² + bx + c = 0."
    },

    "derivative": {
        "keywords": ["derivative", "अवकलन", "অন্তরকলন", "ಅವಕಲನ"],
        "en": "A derivative represents the rate of change of a function.",
        "hi": "अवकलन किसी फलन के परिवर्तन की दर को दर्शाता है।",
        "bn": "অন্তরকলন একটি ফাংশনের পরিবর্তনের হার নির্দেশ করে।",
        "kn": "ಅವಕಲನವು ಕಾರ್ಯದ ಬದಲಾವಣೆಯ ವೇಗವನ್ನು ಸೂಚಿಸುತ್ತದೆ."
    },

    "integration": {
        "keywords": ["integration", "समाकलन", "সমাকলন", "ಸಮಾಕಲನ"],
        "en": "Integration is the process of finding the area under a curve.",
        "hi": "समाकलन वक्र के नीचे के क्षेत्रफल को ज्ञात करने की प्रक्रिया है।",
        "bn": "সমাকলন হলো বক্ররেখার নিচের ক্ষেত্রফল নির্ণয়।",
        "kn": "ಸಮಾಕಲನವು ವಕ್ರರೇಖೆಯ ಅಡಗಿನ ಪ್ರದೇಶವನ್ನು ಕಂಡುಹಿಡಿಯುವ ಪ್ರಕ್ರಿಯೆ."
    }
}

# -------------------------------
# Main solve function (language-aware)
# -------------------------------
def solve_doubt(question, lang):
    q = question.lower()
    for item in answers.values():
        for kw in item["keywords"]:
            if kw.lower() in q:
                return item.get(lang, item["en"])

    fallback = {
        "en": "Sorry, I don't know this answer yet.",
        "hi": "क्षमा करें, मुझे अभी इसका उत्तर नहीं पता।",
        "bn": "দুঃখিত, আমি এখনও এই প্রশ্নের উত্তর জানি না।",
        "kn": "ಕ್ಷಮಿಸಿ, ನನಗೆ ಈ ಪ್ರಶ್ನೆಯ ಉತ್ತರ ಇನ್ನೂ ತಿಳಿದಿಲ್ಲ."
    }
    return fallback.get(lang, fallback["en"])

# -------------------------------
# Flask routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    audio_file = None
    language = "english"

    if request.method == "POST":
        question = request.form["question"]
        language = request.form["language"]

        lang_map = {
            "english": ("en", "en"),
            "hindi": ("hi", "hi"),
            "bengali": ("bn", "bn"),
            "kannada": ("kn", "kn")
        }

        dict_lang, tts_lang = lang_map.get(language, ("en", "en"))
        answer = solve_doubt(question, dict_lang)
 # --------- CREATE AUDIO ----------
        os.makedirs("static/audio", exist_ok=True)
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("static/audio", filename)

        tts = gTTS(text=answer, lang=tts_lang, slow=False)
        tts.save(filepath)

        audio_file = f"/static/audio/{filename}"

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        audio_file=audio_file,
        language=language
    )
# -------------------------------
# Run app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
