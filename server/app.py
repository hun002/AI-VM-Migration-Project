import csv 
import os 
import joblib
from datetime import datetime
from flask import Flask, request
from migration import migration_process

app = Flask(__name__)

CSV_FILE = "data/vm_status.csv"
model = joblib.load("model.pkl")
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
                    "label",
                    "ai_prediction"
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
                data["label"],
                data["ai_prediction"]
            ]
        )

@app.route("/receive", methods=["POST"])
def receive():

    data = request.json

    prediction = model.predict(
        [[
            data["cpu"],
            data["memory"],
            data["disk"],
            data["network"]
        ]]
    )

    data["ai_prediction"] = int(prediction[0])

    vm_status[data["server"]] = data

    save_csv(data)
    migration_process(vm_status)
    
    return {
        "status": "success"
    }

@app.route("/vms")
def get_vms():

    return vm_status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)