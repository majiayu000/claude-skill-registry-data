---
name: finops
description: "클라우드 비용 최적화 기본 — FinOps 프레임워크, 비용 가시성, right-sizing, Spot Instance, 예약 인스턴스·Savings Plan, 미사용 리소스 정리. Use when 클라우드 청구서를 줄일 방법을 찾는 첫 단계일 때. 세부는 finops-* skill."
---

# FinOps 가이드

클라우드 비용 최적화, Right-sizing, Spot Instance 활용

## Quick Reference (결정 트리)

```
비용 최적화 영역?
    │
    ├─ 컴퓨팅 ──────────────> Right-sizing + Spot Instance
    │       │
    │       ├─ 예측 가능 워크로드 ──> Reserved Instance / Savings Plan
    │       ├─ 유연한 워크로드 ────> Spot Instance (70-90% 절감)
    │       └─ 가변 워크로드 ─────> On-Demand + Autoscaling
    │
    ├─ Kubernetes ─────────> Resource Requests 최적화
    │       │
    │       ├─ VPA 추천 분석
    │       └─ Kubecost 모니터링
    │
    └─ 스토리지/네트워크 ──> 불필요한 리소스 정리
```

---

## CRITICAL: FinOps 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                    FinOps Lifecycle                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Inform ──────────> Optimize ──────────> Operate           │
│      │                   │                    │              │
│   비용 가시성         비용 절감           지속적 관리         │
│   할당 & 태깅        Right-sizing         정책 & 거버넌스    │
│   예산 설정          Spot 활용            자동화             │
│                      예약 구매                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### FinOps 원칙

| 원칙 | 설명 |
|------|------|
| **팀이 비용 소유** | 엔지니어링 팀이 자신의 비용 책임 |
| **비즈니스 가치 기반** | 절감이 아닌 가치 최적화 |
| **협업** | 엔지니어링 + 재무 + 경영 협력 |
| **적시 의사결정** | 실시간 데이터로 빠른 결정 |
| **지속적 개선** | 반복적 최적화 프로세스 |

---

## 비용 가시성 (Inform)

### Kubecost 설치

```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="<token>"
```

### 비용 할당 라벨링

```yaml
# 모든 리소스에 비용 추적 라벨 필수
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  labels:
    # 비용 할당 라벨
    app.kubernetes.io/name: order-service
    team: backend
    environment: production
    cost-center: e-commerce
spec:
  template:
    metadata:
      labels:
        app.kubernetes.io/name: order-service
        team: backend
        environment: production
        cost-center: e-commerce
```

### Kyverno 라벨 강제 정책

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-cost-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-labels
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "team, environment, cost-center 라벨이 필요합니다"
        pattern:
          metadata:
            labels:
              team: "?*"
              environment: "?*"
              cost-center: "?*"
```

### 비용 메트릭 (Prometheus)

```promql
# 네임스페이스별 일일 비용
sum(
  container_memory_working_set_bytes{namespace!=""}
  * on(node) group_left()
  node_ram_hourly_cost
) by (namespace) * 24

# 팀별 월간 비용
sum(
  kubecost_cluster_daily_cost
  * on(namespace) group_left(team)
  kube_namespace_labels{label_team!=""}
) by (label_team) * 30

# 유휴 리소스 비용
sum(kubecost_cluster_daily_cost{type="idle"}) * 30
```

---

## Right-sizing

### VPA 추천 분석

```yaml
# VPA Off 모드로 추천만 받기
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: order-service-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  updatePolicy:
    updateMode: "Off"  # 추천만, 자동 적용 안함
```

```bash
# VPA 추천값 확인
kubectl describe vpa order-service-vpa

# 추천값 예시
# Recommendation:
#   Container Recommendations:
#     Container Name: order-service
#     Lower Bound:    Cpu: 25m, Memory: 128Mi
#     Target:         Cpu: 50m, Memory: 256Mi
#     Upper Bound:    Cpu: 100m, Memory: 512Mi
```

### Right-sizing 적용

```yaml
# VPA 추천 기반 리소스 설정
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
        - name: order-service
          resources:
            requests:
              cpu: 50m       # VPA Target 기반
              memory: 256Mi
            limits:
              cpu: 200m      # Upper Bound + 버퍼
              memory: 512Mi
```

### CRITICAL: 리소스 낭비 지표

```promql
# CPU 낭비율 (requests - 실제 사용)
sum(
  kube_pod_container_resource_requests{resource="cpu"}
  -
  rate(container_cpu_usage_seconds_total[5m])
) by (namespace, pod) / sum(kube_pod_container_resource_requests{resource="cpu"}) by (namespace, pod)

# 메모리 낭비율
sum(
  kube_pod_container_resource_requests{resource="memory"}
  -
  container_memory_working_set_bytes
) by (namespace, pod) / sum(kube_pod_container_resource_requests{resource="memory"}) by (namespace, pod)
```

---

## Spot Instance 활용

### Karpenter Spot 설정

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: spot-pool
spec:
  template:
    spec:
      requirements:
        # Spot 인스턴스 사용
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["medium", "large", "xlarge", "2xlarge"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: 500
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
---
# On-Demand 풀 (중요 워크로드용)
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: on-demand-pool
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
      taints:
        - key: critical
          value: "true"
          effect: NoSchedule
```

### Spot 워크로드 배치

```yaml
# Spot 노드에 배치할 워크로드
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  template:
    spec:
      # Spot 노드 선호
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: karpenter.sh/capacity-type
                    operator: In
                    values: ["spot"]
      # Spot 중단 대비
      terminationGracePeriodSeconds: 120
      containers:
        - name: processor
          image: batch-processor:latest
---
# 중요 워크로드는 On-Demand
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  template:
    spec:
      tolerations:
        - key: critical
          operator: Equal
          value: "true"
          effect: NoSchedule
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: karpenter.sh/capacity-type
                    operator: In
                    values: ["on-demand"]
```

### CRITICAL: Spot 적합 워크로드

| 적합 | 부적합 |
|------|--------|
| 배치 처리 | 결제 서비스 |
| CI/CD 러너 | 데이터베이스 |
| 개발/테스트 환경 | 스테이트풀 워크로드 |
| 데이터 분석 | 실시간 트랜잭션 |
| ML 학습 | 단일 인스턴스 서비스 |

### Spot 중단 처리

```yaml
# Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: batch-processor-pdb
spec:
  minAvailable: 50%
  selector:
    matchLabels:
      app: batch-processor
```

```go
// Spot 중단 신호 처리 (2분 전 알림)
func handleSpotInterruption() {
    // AWS IMDSv2에서 중단 알림 확인
    resp, err := http.Get(
        "http://169.254.169.254/latest/meta-data/spot/instance-action")
    if err == nil && resp.StatusCode == 200 {
        // Graceful shutdown 시작
        log.Info("Spot interruption notice received, starting graceful shutdown")
        gracefulShutdown()
    }
}
```

---

## 예약 인스턴스 & Savings Plan

### 구매 전략

| 유형 | 할인율 | 유연성 | 적합 상황 |
|------|--------|--------|----------|
| **Reserved Instance** | 최대 72% | 낮음 | 고정 워크로드 |
| **Savings Plan** | 최대 66% | 높음 | 가변 워크로드 |
| **Spot** | 최대 90% | 매우 높음 | 중단 허용 |

### 권장 비율

```
┌─────────────────────────────────────────────────────────────┐
│              Compute Mix Strategy                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ███████████████████████████░░░░░░░░░░░░                    │
│  └─ Savings Plan (50-60%) ─┘└─ Spot (30%) ─┘└ OD (10-20%)   │
│                                                              │
│  기준:                                                       │
│  - 베이스라인 사용량 → Savings Plan                          │
│  - 배치/개발 워크로드 → Spot                                 │
│  - 예측 불가/중요 → On-Demand                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 불필요한 리소스 정리

### 정리 대상 식별

```bash
# 사용하지 않는 PVC
kubectl get pvc --all-namespaces -o json | jq '.items[] | select(.status.phase == "Released") | .metadata.name'

# 오래된 ReplicaSet (replicas=0)
kubectl get rs --all-namespaces -o json | jq '.items[] | select(.spec.replicas == 0) | .metadata.name'

# 미사용 ConfigMap/Secret
# (주의: 실제 사용 여부 확인 필요)
```

### 자동 정리 정책

```yaml
# TTL Controller로 완료된 Job 자동 삭제
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job
spec:
  ttlSecondsAfterFinished: 3600  # 1시간 후 삭제
  template:
    spec:
      containers:
        - name: job
          image: batch:latest
      restartPolicy: Never
```

### 스토리지 최적화

```yaml
# 적절한 스토리지 클래스 선택
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3  # gp2보다 저렴
  resources:
    requests:
      storage: 100Gi
```

---

## 비용 알림

### 예산 초과 알림

```yaml
# Prometheus Alert
groups:
  - name: cost-alerts
    rules:
      - alert: NamespaceCostHigh
        expr: |
          sum(kubecost_namespace_daily_cost{namespace!~"kube-system|istio-system"}) by (namespace) > 100
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "네임스페이스 {{ $labels.namespace }} 일일 비용이 $100 초과"

      - alert: ClusterCostSpike
        expr: |
          (sum(kubecost_cluster_daily_cost) - sum(kubecost_cluster_daily_cost offset 1d))
          / sum(kubecost_cluster_daily_cost offset 1d) > 0.2
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "클러스터 비용이 전일 대비 20% 이상 증가"
```

### 팀별 비용 리포트

```promql
# 팀별 월간 비용 추정
sum(
  kubecost_cluster_daily_cost
  * on(namespace) group_left(team)
  kube_namespace_labels
) by (label_team) * 30
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 라벨 없는 리소스 | 비용 추적 불가 | 라벨 정책 강제 |
| 과도한 requests | 리소스 낭비 | VPA 추천 활용 |
| Spot만 사용 | 서비스 불안정 | 혼합 전략 |
| 모든 워크로드 Reserved | 유연성 부족 | Savings Plan 활용 |
| 비용 모니터링 없음 | 낭비 인식 불가 | Kubecost 설치 |
| 정리 없는 리소스 | 좀비 리소스 | 자동 정리 정책 |

---

## 체크리스트

### Inform (가시성)
- [ ] Kubecost 설치
- [ ] 비용 할당 라벨 정책
- [ ] 팀별/환경별 대시보드
- [ ] 예산 알림 설정

### Optimize (최적화)
- [ ] VPA 추천 분석
- [ ] Right-sizing 적용
- [ ] Spot Instance 활용
- [ ] Savings Plan 구매

### Operate (운영)
- [ ] 정기 비용 리뷰 (주간/월간)
- [ ] 불필요 리소스 정리
- [ ] 자동화 정책 적용

**관련 skill**: `/k8s:k8s-autoscaling`, `/k8s:k8s-scheduling`, `/observability:monitoring-metrics`

> **AI 워크로드 비용 관리**: LLM API 토큰 비용, GPU 인스턴스 최적화, Model Routing,
> Shift-Left FinOps for AI는 `finops-ai.md` 참조.
> 2026 기준 GPU 워크로드가 클라우드 비용의 18%를 차지하며 98% 팀이 AI 비용을 관리 중.
