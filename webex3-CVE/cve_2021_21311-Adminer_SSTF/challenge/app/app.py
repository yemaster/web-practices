from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "HEAD", "PUT", "DELETE"])
def flag():
    return "flag{test_flag}", 400