from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ESP Voice Server Running!"

@app.route("/upload", methods=["POST"])
def upload():

    wav = request.data

    with open("received.wav", "wb") as f:
        f.write(wav)

    print("Received", len(wav), "bytes")

    return "UPLOAD OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)