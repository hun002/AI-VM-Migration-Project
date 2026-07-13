// Flask 서버 주소/모든 API 요청은 이 주소를 기준으로 보냄
const SERVER = "http://192.168.45.184:5000";

// VM 상태 데이터 가져오기
// async: 서버 응답을 기다리는 비동기 함수
async function loadVMData(){
    // Flask의 /vms API에 GET 요청 전송
    // fetch()는 JavaScript에서 서버와 통신하기 위한 함수이다.
    // 기본 요청 방식은 GET이므로, 아래 코드는 GET /vms 요청과 동일함
    const response = await fetch(
        `${SERVER}/vms`
    );
    // 서버에서 받은 HTTP 응답 데이터를 JSON으로 변환
    const data = await response.json();
    // 받은 VM 데이터를 화면에 출력하는 함수 호출
    renderVMs(
        data.vms
    );

}
// Migration 결과 가져오기
async function loadMigration(){
    // Flask의 /migration API 호출
    const response = await fetch(
        `${SERVER}/migration`
    );
    // JSON 데이터를 JavaScript 객체로 변환
    const data = await response.json();
    // Migration 결과 화면 출력
    renderMigration(
        data
    );

}

// 자원 사용량 상태 표시 결정 함수
// CPU, Memory 등의 사용량에 따라 progress bar 색상을 결정
// 85 이상 -> 위험(red)
// 70 이상 -> 경고(yellow)
// 그 이하 -> 정상
function level(value){
    // 자원 사용량이 85 이상이면
    // 위험 상태 클래스 반환
    if(value >= 85)
        return "crit";
    // 70 이상이면
    // 경고 상태 클래스 반환
    if(value >= 70)
        return "warn";
    // 정상 상태
    return "";
}

// VM 자원 사용량 UI 생성 함수
// 하나의 자원(CPU, Memory 등)을 HTML 코드 형태로 생성
function metric(label,value){
    return `
    <div class="metric">
        <div class="metric-top">
            <span class="label">
                ${label}
            </span>

            <span class="value">
                ${value}%
            </span>
        </div>

        <div class="bar">
            <div 
            class="bar-fill ${level(value)}"
            style="width:${value}%">
            </div>
        </div>
    </div>
    `;
}

// VM 카드 화면 출력
function renderVMs(vms){
    // id가 vm-cards인 HTML 영역 선택
    // 이후 innerHTML을 변경하여 화면 내용을 수정
    document.getElementById(
        "vm-cards"
    ).innerHTML =

    // map() 배열의 데이터를 하나씩 꺼내서 새로운 배열로 변환하는 JavaScript 함수
    // 여기서는 VM 데이터 배열 -> HTML 카드 배열로 변환
    vms.map(vm => `
    <div class="vm-card">
        <div class="vm-card-head">
            <!-- VM 이름 출력 -->
            <span class="vm-name">
                ${vm.server}
            </span>

            <!-- AI 판단 결과에 따라 상태 표시 -->
            <span class="
            badge 
            badge-${
                vm.ai_prediction === 1
                ? "critical"
                : "running"
            }">
                ${
                vm.ai_prediction === 1
                ? "critical"
                : "running"
                }
            </span>
        </div>
        <!-- VM 자원 상태 출력 -->
        ${metric("CPU", vm.cpu)}
        ${metric("Memory", vm.memory)}
        ${metric("Disk", vm.disk)}
        ${metric("Network", vm.network)}

        <!-- AI Migration 판단 결과 -->
        <div class="ai-predict">
            <span class="label">
                AI Prediction:
            </span>

            <span class="value">
                ${
                vm.ai_prediction === 1
                ? "Migration Recommended"
                : "Stable"
                }
            </span>
        </div>

        <!-- 해당 VM 과부하 테스트 버튼 -->
        <button
        class="vm-overload-btn"
        data-vm="${vm.server}">
            ${vm.server} 과부하 생성
        </button>
    </div>
    `)
    // map() 결과는 배열이므로 join("")을 이용해 하나의 문자열 HTML로 변환
    .join("");
    // 생성된 버튼들에게 클릭 이벤트 추가
    addOverloadButtonEvent();
}
// 과부하 버튼 이벤트 연결

function addOverloadButtonEvent(){
    // 모든 과부하 버튼 선택
    // querySelectorAll: 조건에 맞는 HTML 요소들을 모두 가져옴
    const buttons = document.querySelectorAll(
        ".vm-overload-btn"
    );

    // 각각의 버튼에 이벤트 추가
    buttons.forEach(button => {
        // 버튼 클릭 시 실행될 함수 등록
        button.onclick = async function(){
            // data-vm 속성값 가져오기
            const vmName =
            this.dataset.vm;

            // Flask /overload API 호출
            // VM 상태를 변경해야 하기 때문에 POST 사용
            await fetch(
                `${SERVER}/overload`,
                {
                    method:"POST",
                    headers:{
                        // JSON 형식 데이터 전달
                        "Content-Type":
                        "application/json"
                    },
                    // JavaScript 객체를 JSON 문자열로 변환
                    // Flask request.json으로 받을 수 있음
                    body:JSON.stringify({
                        server:vmName
                    })
                }
            );
            // 사용자에게 테스트 실행 알림
            alert(
                `${vmName} 과부하 발생`
            );
            // 변경된 상태를 다시 불러와 화면 갱신
            loadVMData();
            loadMigration();
        };
    });
}
// Migration 결과 화면 출력
function renderMigration(m){
    // Migration 결과를 출력할 HTML 영역
    const area =
    document.getElementById(
        "migration-result"
    );

    // Migration이 실행되지 않은 경우
    if(
        !m ||
        m.migrate === false
    ){
        area.innerHTML =
        "Migration 없음";
        return; 
    }

    // Migration 발생 시 결과 출력
    area.innerHTML = `
    <div class="mig-flow">

        ${m.source}
        →
        ${m.target}


    </div>
    <br>
    <div>
        Source VM :
        ${m.source}
    </div>

    <div>
        Target VM :
        ${m.target}
    </div>

    <div>
        Migration :
        ${m.migrate}
    </div>
    `;
}

// 초기 데이터 로딩
// 페이지가 처음 열릴 때 VM 상태와 Migration 결과 표시
loadVMData();
loadMigration();

// 주기적 데이터 갱신
// 3000ms = 3초/3초마다 Flask API를 호출하여 최신 상태 반영
setInterval(
    loadVMData,
    3000
);
setInterval(
    loadMigration,
    3000
);