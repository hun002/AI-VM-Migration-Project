# AI-VM-Migration-Project

📁프로젝트 소개
서버 상태 데이터를 기반으로 과부하를 예측하고, VM-Migration 여부 및 대상 서버를 선정하는 클라우드 환경 최적화 시스템을 구현한 프로젝트입니다. 또한 결과를 웹 대시보드로 시각화했습니다. <br>

⌛개발 기간
2026년 07월 12일 ~ 2026년 07월 13일(2일)<br>

🖥️개발 환경
개발 플랫폼: Windows 11, Ubuntu<br>
개발 툴: Visual Studio Code, Oracle VirtualBox, Github Desktop<br>
웹 서버: 로컬<br>

👾기술 스택<br>
언어: Python,HTML,CSS,JS<br>
기타: Github<br>

🦴시스템 전체 구조도<br>

<img width="451" height="537" alt="image" src="https://github.com/user-attachments/assets/3ff5b69d-f46b-4207-a551-9bb26a2be34a" />


🔍주요 기능<br>

- 가상 환경 데이터 수집<br>
각 VM의 CPU, 메모리 등 시스템 상태 데이터 수집

- 양방향 데이터 전송<br>
Flask API를 활용해 서버 간 상태 데이터 송수신

- 과부하 예측<br>
수집 데이터를 기반으로 Random Forest 머신러닝 모델을 학습하고 서버 과부하 상태 예측

- VM-Migration 판단<br>
예측 결과를 기반으로 Migration 필요 여부 결정

- App-Aware 알고리즘 기반 대상 서버 선정<br>
서버 자원 상태와 네트워크 의존성을 고려하여 최적 Migration 대상 선정

- 웹 대시보드<br>
VM 상태, Migration 결과, 네트워크 의존성 그래프 시각화<br>

🦿프로젝트 시연 영상<br>

https://github.com/user-attachments/assets/8899f8ea-0d3c-44de-b769-9a9e3d85e133



* App-aware 알고리즘 참고 논문 링크<br>
https://scholar.google.com/citations?view_op=view_citation&hl=ko&user=M7edePUAAAAJ&citation_for_view=M7edePUAAAAJ:KlAtU1dfN6UC
