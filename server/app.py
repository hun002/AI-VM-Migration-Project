import csv 
import os 
import joblib
# 브라우저(HTML/JS)와 Flask 서버가 서로 다른 주소에서 통신할 때
# 발생하는 CORS 문제를 해결하기 위한 라이브러리
from flask_cors import CORS
from datetime import datetime
from flask import Flask, request
# migration.py에서 Migration 판단 함수와 결과 데이터를 가져옴
from migration import migration_process, migration_result
# 꼭 서버 경로에서 실행할 것.(AI모델 경로 때문에)
app = Flask(__name__)
# Flask 애플리케이션 생성

CORS(app)
# 웹 브라우저에서 Flask API에 접근할 수 있도록 CORS 허용
# 예) localhost:5500에서 192.168.45.184:5000 API 접근 가능
CSV_FILE = "../data/vm_status.csv" # 서버 상태 데이터를 저장할 CSV 파일 경로
model = joblib.load("model.pkl") # 학습 완료된 AI 모델 불러오기
vm_status = {} # 현재 VM들의 최신 상태 데이터를 저장하는 딕셔너리

# VM 상태 데이터를 CSV 파일에 저장하는 함수
def save_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    # CSV 파일이 이미 존재하는지 확인
    with open(CSV_FILE, "a", newline="") as f:
    # 기존 데이터 뒤에 새로운 데이터를 추가하는 방식으로 파일 열기
        writer = csv.writer(f) # CSV 데이터를 작성하기 위한 writer 생성
        # 파일이 처음 생성되는 경우 컬럼명을 먼저 추가(이전 csv를 지워도 작동 가능)
        if not file_exists:
            writer.writerow(
                [
                    "timestamp", # 데이터 기록 시간
                    "server",    # VM 이름
                    "cpu",       # CPU 사용량
                    "memory",    # Memory 사용량
                    "disk",      # Disk 사용량
                    "network",   # Network 사용량
                    "label",     # 실제 상태 라벨
                    "ai_prediction" # AI 모델 예측 결과
                ]
            )
        # 현재 VM 상태 데이터를 한 행으로 저장
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

# 클라이언트 VM에서 상태 데이터를 전달받는 API
# POST 방식으로 JSON 데이터를 받음
@app.route("/receive", methods=["POST"])
def receive():
    # 요청 body에 포함된 JSON 데이터를 Python dictionary 형태로 변환
    data = request.json
    # AI 모델을 이용하여 현재 VM 상태 예측
    prediction = model.predict(
        [[
            data["cpu"], #입력값들
            data["memory"],
            data["disk"],
            data["network"]
        ]]
    )

    # numpy 타입 결과를 Python int 타입으로 변환
    # JSON 변환 및 저장을 위해 필요
    data["ai_prediction"] = int(prediction[0])
    # 최신 VM 상태 갱신/같은 이름의 VM이면 기존 데이터를 최신 데이터로 덮어씀
    vm_status[data["server"]] = data
    # CSV 파일에 현재 상태 저장
    save_csv(data)
    migration_process(vm_status)
     # AI 판단 결과를 기반으로 Migration 필요 여부 판단
    return {  # 클라이언트에게 처리 완료 응답 반환
        "status": "success"
    }


# 웹 대시보드에서 현재 VM 상태를 요청하는 API
# JavaScript fetch()에서 GET 요청으로 호출
@app.route("/vms")
def get_vms():
    # dictionary 형태로 저장된 VM 데이터를 JSON 형태로 변환하여 반환
    return {
        "vms": list(vm_status.values())
    }
# Migration 결과를 제공하는 API
@app.route("/migration")
def get_migration():

    return migration_result

# 버튼을 통해 특정 VM에 강제로 과부하 상황을 발생시키는 API
@app.route("/overload", methods=["POST"])
def overload():
    # JavaScript에서 전달한 JSON 데이터 받기
    data = request.json
    # 과부하를 발생시킬 VM 이름 추출
    server = data["server"] 

    # print("버튼 요청:", server)
    # print("현재 VM:", vm_status.keys())
    
    # 해당 VM이 현재 관리 중인 VM이면 AI Prediction 값을 1로 변경하여 Migration 대상 처리
    if server in vm_status:
        vm_status[server]["ai_prediction"] = 1
        # 변경된 상태를 기준으로 Migration 실행
        migration_process(vm_status)
      
    return {
        "status":"overload",
        "server":server
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# Flask 서버 실행
# 모든 네트워크 인터페이스에서 접근 가능하도록 설정