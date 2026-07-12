from flask import Flask, request, send_file

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "ESP Voice Server Running!"


@app.route("/upload", methods=["POST"])
def upload():

    # Receive raw WAV bytes from ESP8266
    wav = request.data

    print("Received", len(wav), "bytes")

    if len(wav) == 0:
        return "No audio received", 400

    # Save WAV file
    with open("received.wav", "wb") as f:
        f.write(wav)

    print("WAV saved successfully")

    return "UPLOAD OK"


@app.route("/download", methods=["GET"])
def download():

    return send_file(
        "received.wav",
        mimetype="audio/wav",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)