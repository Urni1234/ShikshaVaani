from flask import Flask, render_template, request
from gtts import gTTS
import requests
import os
import uuid

app = Flask(__name__)


# -------------------------------
# Main solve function (language-aware)
# -------------------------------
def solve_doubt(question, lang):

    url = "https://api.asi1.ai/v1/chat/completions"

    lang_names = {
        "en": "English",
        "hi": "Hindi",
        "bn": "Bengali",
        "kn": "Kannada",
        "pa": "Punjabi",
        "gu" : "Gujarati",
        "ta":"Tamil",
        "te":"Telugu"
    }

    language_name = lang_names.get(lang, "English")

    headers = {
        "Authorization": f"Bearer {os.getenv('ASI_ONE_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
    "model": "asi1",
    "messages": [
        {
            "role": "system",
            "content": f"You are a helpful  tutor. Reply clearly in {language_name}. Do NOT use markdown symbols like ##, **, or bullet points. Use simple plain text only."
        },
        {
            "role": "user",
            "content": question
        }
    ]
}

    try:
        response = requests.post(url, headers=headers, json=body)
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"
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
            "kannada": ("kn", "kn"),
            "punjabi": ("pa","pa"),
            "gujarati":("gu","gu"),
            "tamil":("ta","ta"),
            "telugu":("te","te")

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
