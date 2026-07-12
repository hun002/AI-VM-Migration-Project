import pandas as pd
import joblib
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

joblib.dump(
    model,
    "model.pkl"
)

print("모델 저장 완료")