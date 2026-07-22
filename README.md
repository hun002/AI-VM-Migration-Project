# AI-VM-Migration-Project

📁프로젝트 소개
서버 스스로 자신의 과부하 상태를 체크하고 VM-Migration여부를 정해 VM-Miaration 대상 서버를 선정하는 시스템을 대시보드를 통해 보여주는 웹 사이트입니다.

⌛개발 기간
2026년 07월 12일 ~ 2026년 07월 13일(2일)

🖥️개발 환경
개발 플랫폼: Window11, Ubuntu
개발 툴: Visual Studio Code, Oracle VirtualBox, Github Desktop
웹 서버: 로컬

👩🏻‍🔧기술 스택
프론트엔드: HTML/CSS/JS
API: Flask

기타 등: 깃허브, Python

🦴시스템 전체 구조도

<img width="451" height="537" alt="image" src="https://github.com/user-attachments/assets/3ff5b69d-f46b-4207-a551-9bb26a2be34a" />

🔍주요 기능

- 가상 환경 데이터 수집
각 VM의 CPU, 메모리 등 시스템 상태 데이터 수집

- 양방향 데이터 전송
Flask API를 활용해 서버 간 상태 데이터 송수신

- 과부하 예측
수집 데이터를 기반으로 머신러닝 모델을 학습하고 서버 과부하 상태 예측

- VM-Migration 판단
예측 결과를 기반으로 Migration 필요 여부 결정

- App-Aware 알고리즘 기반 대상 서버 선정
서버 자원 상태와 네트워크 의존성을 고려하여 최적 Migration 대상 선정

- 웹 대시보드
VM 상태, Migration 결과, 네트워크 의존성 그래프 시각화

🦿웹 대시보드 구현 영상

https://github.com/user-attachments/assets/8899f8ea-0d3c-44de-b769-9a9e3d85e133



* App-aware 알고리즘에 대한 학술자료 링크
https://scholar.google.com/citations?view_op=view_citation&hl=ko&user=M7edePUAAAAJ&citation_for_view=M7edePUAAAAJ:KlAtU1dfN6UC
