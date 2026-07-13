migration_result = {
    "source": "-",
    "target": "-",
    "migrate": False
}
# VM 간 애플리케이션 의존 관계를 나타내는 의존성 그래프
# Edge의 값은 VM 간 통신량을 의미하는 가중치로 사용함.(실제 측정값X / 0~1 사이의 임의 값으로 설정)
# 값이 클수록 두 VM 간의 의존성이 높다고 가정.
dependency_graph = { 
    "VM1": {"VM2": 0.8, "VM3": 0.3},
    "VM2": {"VM1": 0.8, "VM3": 0.5},
    "VM3": {"VM1": 0.3, "VM2": 0.5}
}
# VM 간 논리적 네트워크 거리를 나타내는 테이블
# 실제 네트워크 토폴로지는 구성하기 어렵기 때문에 논리적 거리 값을 임의로 설정.
network_distance = {
    "VM1": {"VM2": 0.2, "VM3": 0.7},
    "VM2": {"VM1": 0.2, "VM3": 0.5},
    "VM3": {"VM1": 0.7, "VM2": 0.5}
}

# Migration 필요 여부 판단
def check_migration_needed(vm_status):
    for vm, data in vm_status.items(): #vm_status 딕셔너리의 key, value를 vm, data에 하나씩 넣어 반복
        if data.get("ai_prediction") == 1: #만약 data 딕셔너리의 ai_prediction 값이 1이면 Migration 필요
            print(f"{vm}: Migration 필요")
            return vm #Migration이 필요한 서버를 반환

    print("Migration 필요 없음") #Migration이 필요 없는 경우 메시지 출력

    return None #None 반환


# 후보 서버 선정
def select_candidate_servers(vm_status, overloaded_vm):
    candidates = [] #후보 서버를 저장할 리스트

    for vm, data in vm_status.items(): # vm_status 딕셔너리의 key, value를 vm, data에 하나씩 넣어 반복
        # vm이 과부하 VM이면 아래 조건문을 건너뛰고 다음 반복으로 넘어감
        if vm == overloaded_vm: #만약 과부하 서버와 vm이 같으면 아래 코드를 건너뛰고 다음 반복으로 넘어감
            continue

        cpu = data["cpu"] 
        memory = data["memory"]

        #data 에서 각 자원 값을 가져와 아래 조건에 맞으면 리스트에 추가
        # 자원 여유 조건
        if cpu < 80 and memory < 80:
            candidates.append(vm)

    return candidates #후보 서버 리스트 반환


# 네트워크 거리 계산 
def calculate_network_distance(
        source_vm,
        target_vm
):
    return network_distance[source_vm].get(
        target_vm,
        0
    ) #source_vm과 target_vm 간 논리적 네트워크 거리 반환


# 통신량 계산
def calculate_communication_cost(
        source_vm,
        target_vm
):
    return dependency_graph[source_vm].get(
        target_vm,
        0
    ) #두 VM 간 통신 관계를 나타내는 의존성 그래프의 가중치를 통신량으로 가정하여 사용.


# App-aware Cost 함수Function
def calculate_cost(overloaded_vm,target_vm):
    distance = calculate_network_distance(
        overloaded_vm,
        target_vm
    )

    #네트워크 거리 및 통신량 계산
    communication = calculate_communication_cost(
        overloaded_vm,
        target_vm
    )

    # 통신량과 네트워크 거리를 곱하여 Cost 계산
    # Cost가 낮을수록 Migration 이후 애플리케이션의 영향이 적다고 판단한다.
    cost = communication * distance

    return cost


# 최적 Migration 서버 선택
def select_best_target(
        overloaded_vm,
        candidates
):
    if len(candidates) == 0: #후보 서버가 없으면 Migration 불가능
        print(
            "Migration 가능한 서버가 없습니다."
        )
        return None #None 반환

    costs = {} #비용 저장용 딕셔너리

    for server in candidates: #후보 서버들을 server에 하나씩 넣어 반복
        cost = calculate_cost( #아래 매개변수들을 calculate_cost로 보냄
            overloaded_vm,
            server
        )

        costs[server] = cost #계산된 비용을 costs 딕셔너리에 저장

    print("\n후보 서버 Cost") 

    for server, cost in costs.items(): #costs` 딕셔너리의 key, value를 server, cost에 하나씩 넣어 반복`
        print(f"{server} : {cost:.2f}") #서버 별 비용 출력

    best_server = min(  #costs 딕셔너리에서 가장 작은 비용을 가진 서버를 best_server에 저장
        costs,
        key=costs.get
    )

    return best_server #best_server 반환


# 전체 Migration 과정
def migration_process(vm_status):
    overloaded_vm = check_migration_needed( #Migration이 필요한 서버를 확인하고
        vm_status                           #있다면 overloaded_vm에 저장
    )

    # Migration이 필요한 서버가 없다면 그대로 종료/migration_result 초기화
    if overloaded_vm is None:
        migration_result["source"] = "-"
        migration_result["target"] = "-"
        migration_result["migrate"] = False
        return

    candidates = select_candidate_servers( #두 매개변수를 select_candidate_servers로 보내
        vm_status,                         #서버 자원이 충분한 서버를 후보로 선정
        overloaded_vm
    )

    print("후보 서버:",candidates) #후보 서버들 출력

    target = select_best_target( #두 매개변수들을 모두 select_best_target로 보내 최적의 Migration 대상 서버를 선정
        overloaded_vm,
        candidates
    )
    # Migration 대상 서버가 없다면 그대로 종료/migration_result 초기화
    if target is None:
        migration_result["source"] = overloaded_vm
        migration_result["target"] = "-"
        migration_result["migrate"] = False
        return


    migration_result["source"] = overloaded_vm
    migration_result["target"] = target
    migration_result["migrate"] = True

    print(
        f"{overloaded_vm} → {target} Migration 선택"
    )

        