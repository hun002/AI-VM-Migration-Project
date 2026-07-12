import csv 
import os 
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

CSV_FILE = "data/vm_status.csv"
vm_status = {}

def save_csv(data):

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "server",
                    "cpu",
                    "memory",
                    "disk",
                    "network",
                    "label"
                ]
            )

        writer.writerow(
            [
                datetime.now(),
                data["server"],
                data["cpu"],
                data["memory"],
                data["disk"],
                data["network"],
                data["label"]
            ]
        )

@app.route("/receive", methods=["POST"])
def receive():

    data = request.json

    print("받은 VM 데이터")
    print(data)

    vm_status[data["server"]] = data

    save_csv(data)

    return {
        "status": "success"
    }

@app.route("/vms")
def get_vms():

    return vm_status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)