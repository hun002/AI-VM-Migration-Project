async function loadVMData(){

    const response = await fetch(
        "http://192.168.45.184:5000/vms"
    );

    const data = await response.json();

    const vms = Object.values(data);

    renderVMs(
        vms.map(vm => ({
            name: vm.server,

            status:
                vm.ai_prediction === 1
                ? "critical"
                : "running",

            cpu: vm.cpu,
            memory: vm.memory,
            disk: vm.disk,
            network: vm.network,

            prediction:
                vm.ai_prediction === 1
                ? "Migration Recommended"
                : "Stable"
        }))
    );
}


function level(pct) {

    if (pct >= 85)
        return "crit";

    if (pct >= 70)
        return "warn";

    return "";
}


function metric(label, value) {

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

    </div>`;
}


function renderVMs(vms) {

    document.getElementById("vm-cards").innerHTML =

    vms.map((vm) => `

      <div class="vm-card">


        <div class="vm-card-head">

          <span class="vm-name">
            ${vm.name}
          </span>


          <span class="badge badge-${vm.status}">
            ${vm.status}
          </span>

        </div>


        ${metric("CPU", vm.cpu)}

        ${metric("Memory", vm.memory)}

        ${metric("Disk", vm.disk)}

        ${metric("Network", vm.network)}



        <div class="ai-predict">

          <span class="label">
            AI Prediction:
          </span>


          <span class="value">
            ${vm.prediction}
          </span>


        </div>


      </div>


    `).join("");

}



async function loadMigration(){

    const response = await fetch(
        "http://192.168.45.184:5000/migration"
    );


    const data = await response.json();


    renderMigration(data);

}



function renderMigration(m){


    const box =
    document.getElementById(
        "migration-result"
    );


    if(!m.source){

        box.innerHTML = `

        <div class="mig-row">

            <span class="label">
                Migration 여부
            </span>


            <span class="value">

                <span class="badge badge-running">
                    NO
                </span>

            </span>


        </div>

        `;

        return;

    }



    box.innerHTML = `


    <div class="mig-flow">


        <span class="mig-node">

            <span class="role">
                Source VM
            </span>

            ${m.source}

        </span>



        <span class="arrow">
            →
        </span>



        <span class="mig-node">

            <span class="role">
                Target VM
            </span>

            ${m.target}

        </span>


    </div>



    <div class="mig-row">

        <span class="label">
            Source VM
        </span>


        <span class="value">
            ${m.source}
        </span>


    </div>



    <div class="mig-row">

        <span class="label">
            Target VM
        </span>


        <span class="value">
            ${m.target}
        </span>


    </div>



    <div class="mig-row">

        <span class="label">
            Migration 여부
        </span>


        <span class="value">

            <span class="badge badge-running">
                YES
            </span>

        </span>


    </div>


    `;

}



function tick(){

    const now = new Date();


    const p = (n)=>
        String(n).padStart(2,"0");


    document.getElementById("clock").textContent =

    `${p(now.getHours())}:${p(now.getMinutes())}:${p(now.getSeconds())}`;

}



// VM 데이터 실행

loadVMData();


setInterval(
    loadVMData,
    3000
);



// Migration 데이터 실행

loadMigration();


setInterval(
    loadMigration,
    3000
);



// Clock

tick();


setInterval(
    tick,
    1000
);