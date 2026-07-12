from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ESP Voice Server Running!"

@app.route("/upload", methods=["POST"])
def upload():

    if "audio" not in request.files:
        return "No audio received", 400

    audio = request.files["audio"]

    audio.save("received.wav")

    print("Received:", audio.filename)

    return "UPLOAD OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)