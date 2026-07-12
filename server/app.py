from flask import Flask, request

app = Flask(__name__)

@app.route("/receive", methods=["POST"])
def receive():
    data = request.json

    print("받은 VM 데이터")
    print(data)

    return {
        "status": "success"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)