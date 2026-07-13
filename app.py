from flask import Flask, request, Response
from groq import Groq
import os
import re

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


@app.route("/", methods=["GET"])
def home():
    return "ESP Voice Server Running!"


def extract_number(text):

    text = text.lower().strip()

    print("Normalized:", text)

    # Numeric forms (80, 81, ..., 99)
    numbers = re.findall(r"\d+", text)

    for n in numbers:
        value = int(n)
        if 80 <= value <= 99:
            return str(value)

    # Spoken forms
    words = {

        "ninety nine": 99,
        "ninety eight": 98,
        "ninety seven": 97,
        "ninety six": 96,
        "ninety five": 95,
        "ninety four": 94,
        "ninety three": 93,
        "ninety two": 92,
        "ninety one": 91,
        "ninety": 90,

        "eighty nine": 89,
        "eighty eight": 88,
        "eighty seven": 87,
        "eighty six": 86,
        "eighty five": 85,
        "eighty four": 84,
        "eighty three": 83,
        "eighty two": 82,
        "eighty one": 81,
        "eighty": 80,
    }

    # Longest phrases first
    for word in sorted(words, key=len, reverse=True):
        if word in text:
            return str(words[word])

    return "NONE"


@app.route("/upload", methods=["POST"])
def upload():

    wav = request.data

    print("Received:", len(wav), "bytes")

    if len(wav) == 0:
        return "NONE"

    with open("received.wav", "wb") as f:
        f.write(wav)

    print("Sending to Groq...")

    with open("received.wav", "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="text"
        )

    print("Recognized:")
    print(transcription)

    result = extract_number(transcription)

    print("Returning:", result)

    return Response(
        result,
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )