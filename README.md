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
가상 환경 데이터 수집: 각 VM의 시스템 상태를 수집하는 기능
양방향 데이터 전송: Flask API를 통해 각 서버들이 데이터를 보내고 받는 기능
과부하 예측: 임의로 랜덤 과부하를 발생시킨 데이터를 Csv로 저장하고 그 데이터를 기반으로 AI를 기계학습시켜 서버의 과부하를 예측하는 기능
VM-Migration 판단: AI예측 결과를 바탕으로한 VM_Migration여부 판단 기능
App-Aware 알고리즘을 통한 서버 선정: 각 서버의 자원 상태를 확인해 후보 서버를 선정후 그속에서 비용, 통신량등을 고려해 최종 서버를 선정하는 기능
웹 대시보드: 각 VM의 상태를 나타내는 카드 및 Migration결과, 네트워크 의존성 그래프를 실시간으로 나타내는 페이지 표시 기능
