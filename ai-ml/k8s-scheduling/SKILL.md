---
name: k8s-scheduling
description: "파드 배치 기본 — nodeSelector, Node Affinity, Pod Affinity/Anti-Affinity, Taint & Toleration 비교. Use when 특정 노드에 파드를 두거나 떼어 놓는 규칙을 작성할 때."
---

# Kubernetes Scheduling 가이드

Node Affinity, Pod Affinity/Anti-Affinity, Taint & Toleration

## Quick Reference (결정 트리)

```
스케줄링 목적?
    │
    ├─ 특정 노드에 배치 ─────────> Node Affinity + nodeSelector
    │       │
    │       ├─ 필수 조건 ────> requiredDuringScheduling
    │       └─ 선호 조건 ────> preferredDuringScheduling
    │
    ├─ 특정 노드 회피 ──────────> Taint + Toleration
    │
    ├─ Pod 간 같이/따로 배치 ───> Pod Affinity/Anti-Affinity
    │       │
    │       ├─ 같은 노드/존 ──> Pod Affinity
    │       └─ 다른 노드/존 ──> Pod Anti-Affinity (HA)
    │
    └─ 리소스 기반 배치 ────────> Resource Requests
```

---

## CRITICAL: 스케줄링 개념 비교

| 기능 | 대상 | 방향 | 용도 |
|------|------|------|------|
| **nodeSelector** | Node | 끌어당김 | 단순 노드 선택 |
| **Node Affinity** | Node | 끌어당김 | 고급 노드 선택 |
| **Taint/Toleration** | Node | 밀어냄 | 노드 격리/전용화 |
| **Pod Affinity** | Pod | 끌어당김 | Pod 공존 |
| **Pod Anti-Affinity** | Pod | 밀어냄 | Pod 분산 (HA) |

```
┌─────────────────────────────────────────────────────────────┐
│                    Scheduling Flow                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pod 생성 요청                                               │
│       │                                                      │
│       ▼                                                      │
│  Filtering (노드 필터링)                                     │
│  ├─ Taint/Toleration 체크                                   │
│  ├─ Node Affinity required 체크                             │
│  └─ 리소스 체크                                              │
│       │                                                      │
│       ▼                                                      │
│  Scoring (노드 점수화)                                       │
│  ├─ Node Affinity preferred 점수                            │
│  ├─ Pod Affinity/Anti-Affinity 점수                         │
│  └─ 리소스 균형 점수                                         │
│       │                                                      │
│       ▼                                                      │
│  최고 점수 노드에 배치                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Node Selector (기본)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  nodeSelector:
    disktype: ssd
    environment: production
  containers:
    - name: my-container
      image: myapp:latest
```

**장점**: 단순함
**단점**: 필수 조건만 가능, OR 연산 불가

---

## Node Affinity

### 유형

| 유형 | 스케줄링 시 | 실행 중 | 용도 |
|------|------------|---------|------|
| **requiredDuringSchedulingIgnoredDuringExecution** | 필수 | 무시 | 반드시 필요한 조건 |
| **preferredDuringSchedulingIgnoredDuringExecution** | 선호 | 무시 | 가능하면 적용 |

### Required (필수)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              # GPU 노드에만 배치
              - key: gpu-type
                operator: In
                values:
                  - nvidia-a100
                  - nvidia-v100
              # 프로덕션 환경
              - key: environment
                operator: In
                values:
                  - production
  containers:
    - name: ml-training
      image: ml-training:latest
      resources:
        limits:
          nvidia.com/gpu: 1
```

### Preferred (선호)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        # 가중치 100: SSD 노드 선호
        - weight: 100
          preference:
            matchExpressions:
              - key: disktype
                operator: In
                values:
                  - ssd
        # 가중치 50: ap-northeast-2a 선호
        - weight: 50
          preference:
            matchExpressions:
              - key: topology.kubernetes.io/zone
                operator: In
                values:
                  - ap-northeast-2a
  containers:
    - name: web
      image: web:latest
```

### Operator 종류

| Operator | 의미 | 예시 |
|----------|------|------|
| **In** | 값 중 하나 | `values: [a, b]` |
| **NotIn** | 값이 아닌 것 | `values: [c, d]` |
| **Exists** | 키가 존재 | (values 불필요) |
| **DoesNotExist** | 키가 없음 | (values 불필요) |
| **Gt** | 값보다 큼 | `values: ["100"]` |
| **Lt** | 값보다 작음 | `values: ["50"]` |

---

## Taint & Toleration

### Taint 적용

```bash
# Taint 추가
kubectl taint nodes node1 dedicated=gpu:NoSchedule
kubectl taint nodes node1 maintenance=true:NoExecute

# Taint 제거
kubectl taint nodes node1 dedicated=gpu:NoSchedule-

# Taint 확인
kubectl describe node node1 | grep -A5 Taints
```

### Taint Effect

| Effect | 동작 |
|--------|------|
| **NoSchedule** | 새 Pod 스케줄링 금지 |
| **PreferNoSchedule** | 가능하면 스케줄링 안함 |
| **NoExecute** | 기존 Pod도 퇴거 |

### Toleration 설정

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-workload
spec:
  tolerations:
    # 정확히 일치하는 toleration
    - key: "dedicated"
      operator: "Equal"
      value: "gpu"
      effect: "NoSchedule"

    # 키만 일치 (모든 값 허용)
    - key: "gpu-type"
      operator: "Exists"
      effect: "NoSchedule"

    # NoExecute에 시간 제한
    - key: "node.kubernetes.io/not-ready"
      operator: "Exists"
      effect: "NoExecute"
      tolerationSeconds: 300  # 5분 후 퇴거

  containers:
    - name: gpu-app
      image: gpu-app:latest
```

### CRITICAL: GPU 노드 전용화

```bash
# 1. GPU 노드에 Taint 추가
kubectl taint nodes gpu-node-1 nvidia.com/gpu=true:NoSchedule

# 2. GPU 노드에 Label 추가
kubectl label nodes gpu-node-1 gpu-type=nvidia-a100
```

```yaml
# GPU 워크로드 Pod
apiVersion: v1
kind: Pod
spec:
  # Toleration: Taint 허용
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"

  # Node Affinity: GPU 노드 선택
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: gpu-type
                operator: In
                values:
                  - nvidia-a100

  containers:
    - name: ml
      image: ml-training:latest
      resources:
        limits:
          nvidia.com/gpu: 1
```

---

## Pod Affinity / Anti-Affinity

### Pod Affinity (같이 배치)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cache
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: cache
    spec:
      affinity:
        podAffinity:
          # 필수: web Pod와 같은 노드
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - web
              topologyKey: kubernetes.io/hostname
      containers:
        - name: redis
          image: redis:7
```

### Pod Anti-Affinity (따로 배치) - HA

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: web
    spec:
      affinity:
        podAntiAffinity:
          # 필수: 같은 앱은 다른 노드에
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - web
              topologyKey: kubernetes.io/hostname

          # 선호: 가능하면 다른 AZ에
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - web
                topologyKey: topology.kubernetes.io/zone
      containers:
        - name: web
          image: web:latest
```

### TopologyKey 종류

| TopologyKey | 분산 범위 |
|-------------|----------|
| `kubernetes.io/hostname` | 노드 |
| `topology.kubernetes.io/zone` | AZ (가용 영역) |
| `topology.kubernetes.io/region` | 리전 |
| `kubernetes.io/os` | OS 유형 |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| required만 사용 | 스케줄링 불가 상황 | preferred 혼용 |
| Anti-Affinity + 적은 노드 | 레플리카 부족 | 노드 수 확보 또는 preferred |
| Toleration만 설정 | 다른 노드에도 배치됨 | Node Affinity 함께 사용 |
| topologyKey 오타 | 무시됨 | 표준 키 사용 |

---

## 체크리스트

### Node Affinity
- [ ] required vs preferred 구분
- [ ] operator 올바른 사용
- [ ] 노드 라벨 사전 확인

### Taint/Toleration
- [ ] Taint와 함께 Node Affinity 사용
- [ ] tolerationSeconds 고려 (NoExecute)
- [ ] 시스템 Taint 처리

### Pod Affinity/Anti-Affinity
- [ ] topologyKey 적절히 설정
- [ ] HA를 위한 Anti-Affinity
- [ ] 데이터 지역성 고려

**관련 skill**: `/k8s:k8s-autoscaling`, `/k8s:k8s-security`, `/k8s:k8s-helm`

---

## 참조 스킬

- `k8s-scheduling-advanced.md` - 실전 시나리오, Topology Spread, 디버깅
- `/k8s:k8s-autoscaling` - 오토스케일링
- `/k8s:k8s-security` - 보안 정책
- `/k8s:k8s-helm` - Helm 차트 관리
