import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

CSV_FILE = "../data/vm_status.csv"
data = pd.read_csv(CSV_FILE)

print("데이터 개수:")
print(len(data))
print("\nLabel 분포:")
print(data["label"].value_counts())

# 입력 데이터
X = data[
    [
        "cpu",
        "memory",
        "disk",
        "network"
    ]
]

# 정답 데이터(label)
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(
    X_train,
    y_train
)
# 예측
prediction = model.predict(X_test)
# 정확도 출력
accuracy = accuracy_score(
    y_test,
    prediction
)

print("\n모델 정확도:")
print(accuracy)
# 임의의 VM 상태 예측 테스트
test_data = pd.DataFrame(
    [
        {
            "cpu": 95,
            "memory": 60,
            "disk": 23,
            "network": 200000
        }
    ]
)
result = model.predict(test_data)
if result[0] == 1:
    print("예측 결과: 과부하 상태")
else:
    print("예측 결과: 정상 상태")