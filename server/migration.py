import math
#의존성 그래프
dependency_graph = { #서버 간 논리적 거리를 임의로 지정함.
    "VM1": {"VM2": 0.8, "VM3": 0.3},
    "VM2": {"VM1": 0.8, "VM3": 0.5},
    "VM3": {"VM1": 0.3, "VM2": 0.5}
}
# Migration 필요 여부 판단
def check_migration_needed(vm_status):
    for vm, data in vm_status.items():
        if data.get("ai_prediction") == 1:
            print(f"{vm}: Migration 필요")
            return vm

    print("Migration 필요 없음")

    return None

# 후보 서버 선정
def select_candidate_servers(vm_status, overloaded_vm):
    candidates = []

    for vm, data in vm_status.items():
        # 과부하 VM 제외
        if vm == overloaded_vm:
            continue

        cpu = data["cpu"]
        memory = data["memory"]

        # 자원 여유 조건
        if cpu < 80 and memory < 80:
            candidates.append(vm)

    return candidates

# 네트워크 거리 계산
def calculate_network_distance(
        source_vm,
        target_vm
):
    dependency = dependency_graph[source_vm].get(
        target_vm,
        0
    )
    # 의존성이 높을수록 거리 비용 감소
    distance = 1 - dependency

    return distance

# 통신량 비용 계산

def calculate_communication_cost(
        vm_status,
        target_vm
):
    return vm_status[target_vm]["network"]

# App-aware Cost Function

def calculate_cost(
        overloaded_vm,
        target_vm,
        vm_status
):
    network_distance = calculate_network_distance(
        overloaded_vm,
        target_vm
    )
    communication = calculate_communication_cost(
        vm_status,
        target_vm
    )
    # Cost 함수
    cost = (
        communication * 0.5
        +
        network_distance * 0.5
    )
    return cost

# 최적 Migration 대상 선택

def select_best_target(
        overloaded_vm,
        candidates,
        vm_status
):
    if len(candidates) == 0:
        print(
            "Migration 가능한 서버가 없습니다."
        )
        return None

    costs = {}

    for server in candidates:
        cost = calculate_cost(
            overloaded_vm,
            server,
            vm_status
        )

        costs[server] = cost

    print("\n후보 서버 Cost")

    for server, cost in costs.items():
        print(
            server,
            ":",
            cost
        )
    best_server = min(
        costs,
        key=costs.get
    )
    return best_server

# 전체 Migration 과정
def migration_process(vm_status):
    overloaded_vm = check_migration_needed(
        vm_status
    )
    # Migration 필요 없음
    if overloaded_vm is None:
        return

    candidates = select_candidate_servers(
        vm_status,
        overloaded_vm
    )

    print(
        "후보 서버:",
        candidates
    )

    target = select_best_target(
        overloaded_vm,
        candidates,
        vm_status
    )

    if target:

        print(
            f"{overloaded_vm} → {target} Migration 선택"
        )


