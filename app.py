from flask import Flask, request
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

    text = text.lower()

    numbers = re.findall(r'\d+', text)

    if numbers:
        return numbers[0]

    words = {
        "zero":0,
        "one":1,
        "two":2,
        "three":3,
        "four":4,
        "five":5,
        "six":6,
        "seven":7,
        "eight":8,
        "nine":9,
        "ten":10,
        "eleven":11,
        "twelve":12,
        "thirteen":13,
        "fourteen":14,
        "fifteen":15,
        "sixteen":16,
        "seventeen":17,
        "eighteen":18,
        "nineteen":19,
        "twenty":20
    }

    for word, value in words.items():
        if word in text:
            return str(value)

    return "NONE"



@app.route("/upload", methods=["POST"])
def upload():

    wav = request.data

    print("Received:", len(wav), "bytes")


    if len(wav)==0:
        return "NONE"


    with open("received.wav","wb") as f:
        f.write(wav)


    print("Sending to Groq...")


    audio_file = open(
        "received.wav",
        "rb"
    )


    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        response_format="text"
    )


    print("Recognized:")
    print(transcription)


    result = extract_number(transcription)


    print("Returning:", result)


    return result



if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )