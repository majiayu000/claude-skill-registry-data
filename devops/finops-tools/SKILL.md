---
name: finops-tools
description: "FinOps 도구 비교와 설치 — OpenCost, Kubecost, Infracost 설정, KEDA+Karpenter 통합. Use when Kubernetes 비용 도구를 고르고 설치하거나 오토스케일링과 묶을 때. 고급 자동화는 finops-tools-advanced."
---

# FinOps Tools 가이드

Kubecost, OpenCost, Infracost 비교 및 설정, KEDA+Karpenter 통합

## Quick Reference (결정 트리)

```
FinOps 도구 선택?
    │
    ├─ Kubernetes 비용 가시성
    │       │
    │       ├─ 무료, 기본 기능 ────────> OpenCost
    │       ├─ 정확한 가격, RI/Spot ───> Kubecost
    │       └─ 엔터프라이즈 기능 ──────> Kubecost Enterprise
    │
    ├─ IaC 비용 예측
    │       │
    │       └─ PR 단계 비용 검토 ──────> Infracost
    │
    └─ 자동 최적화
            │
            ├─ 이벤트 기반 스케일링 ───> KEDA
            ├─ 노드 최적화 + Spot ────> Karpenter
            └─ 조합 (권장) ──────────> KEDA + Karpenter
```

---

## CRITICAL: 도구 비교

### Kubernetes 비용 도구

| 기능 | OpenCost | Kubecost Free | Kubecost Enterprise |
|------|----------|---------------|---------------------|
| **가격** | 무료 | 무료 | $199+/클러스터/월 |
| **CNCF** | Incubating | 기반 | 기반 |
| **네임스페이스 비용** | ✅ | ✅ | ✅ |
| **워크로드 비용** | ✅ | ✅ | ✅ |
| **할인 반영 (RI/Spot)** | ❌ | ✅ | ✅ |
| **클라우드 통합** | 기본 | AWS/GCP/Azure | 완전 통합 |
| **다중 클러스터** | 수동 | 15일 보존 | 무제한 |
| **알림** | ❌ | 기본 | 고급 |
| **SSO/RBAC** | ❌ | ❌ | ✅ |

### IaC 비용 도구

| 기능 | Infracost | env0 | Spacelift |
|------|-----------|------|-----------|
| **가격** | 무료 Tier | 유료 | 유료 |
| **Terraform** | ✅ | ✅ | ✅ |
| **OpenTofu** | ✅ | ✅ | ✅ |
| **Pulumi** | ✅ | ❌ | ✅ |
| **PR 코멘트** | ✅ | ✅ | ✅ |
| **정책 엔진** | OPA | 내장 | 내장 |
| **예측 정확도** | 높음 | 높음 | 높음 |

---

## OpenCost 설치 및 설정

### Helm 설치

```bash
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm install opencost opencost/opencost \
  --namespace opencost \
  --create-namespace \
  --set prometheus.enabled=false \
  --set externalPrometheus.url="http://prometheus-server.monitoring:80" \
  --set ui.enabled=true
```

### 기본 설정

```yaml
# opencost-values.yaml
opencost:
  exporter:
    # 클라우드 가격 설정
    cloudProviderApiKey: ""  # 빈 값 = 기본 가격 사용

    # AWS 설정
    aws:
      spotInstance:
        enabled: true
        dataRegion: ap-northeast-2

  # Prometheus 연동
  prometheus:
    internal:
      enabled: false
    external:
      enabled: true
      url: "http://prometheus-server.monitoring:80"

  # UI 활성화
  ui:
    enabled: true
    service:
      type: ClusterIP

# 네임스페이스별 비용 쿼리
# GET /allocation/compute?window=7d&aggregate=namespace
```

### PromQL 쿼리 (OpenCost)

```promql
# 네임스페이스별 일일 비용
sum(
  node_cpu_hourly_cost
  * on(node) group_left()
  sum(rate(container_cpu_usage_seconds_total{namespace!=""}[1h])) by (node, namespace)
) by (namespace) * 24

# Pod별 비용 (CPU + Memory)
sum(
  (
    rate(container_cpu_usage_seconds_total[1h])
    * on(node) group_left()
    node_cpu_hourly_cost
  ) + (
    container_memory_working_set_bytes / 1024 / 1024 / 1024
    * on(node) group_left()
    node_ram_hourly_cost
  )
) by (namespace, pod)
```

---

## Kubecost 설치 및 설정

### Helm 설치

```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="${KUBECOST_TOKEN}" \
  --set prometheus.server.global.external_labels.cluster_id="prod-cluster"
```

### AWS 통합 설정

```yaml
# kubecost-values.yaml
kubecostModel:
  # 실제 클라우드 가격 연동
  cloudIntegrationEnabled: true

# AWS 가격 통합 (Athena CUR)
cloudCost:
  enabled: true
  aws:
    enabled: true
    athenaQueryEnabled: true
    athenaBucketName: "s3://my-company-aws-cur"
    athenaRegion: "ap-northeast-2"
    athenaDatabase: "athenacurcfn_cost_report"
    athenaTable: "cost_report"
    athenaProjectID: "123456789012"

# Spot 가격 반영
kubecostModel:
  spotCPU: "0.03"
  spotRAM: "0.004"

# 다중 클러스터 (Enterprise)
federatedETL:
  enabled: true
  primaryCluster: true

# SAML SSO (Enterprise)
saml:
  enabled: true
  secretName: kubecost-saml
  idpMetadataURL: "https://login.microsoftonline.com/..."
```

### Kubecost API 활용

```bash
# 네임스페이스별 비용 (지난 7일)
curl -s "http://kubecost.kubecost:9090/model/allocation?window=7d&aggregate=namespace" | jq '.data[0]'

# 팀별 비용 (라벨 기반)
curl -s "http://kubecost.kubecost:9090/model/allocation?window=30d&aggregate=label:team"

# 비용 예측
curl -s "http://kubecost.kubecost:9090/model/prediction?window=30d&aggregate=namespace"

# 비용 효율성 점수
curl -s "http://kubecost.kubecost:9090/model/savings?window=7d"
```

### CRITICAL: Kubecost 권장 대시보드 쿼리

```promql
# 팀별 월간 비용
sum(
  kubecost_cluster_daily_cost
  * on(namespace) group_left(team)
  kube_namespace_labels
) by (label_team) * 30

# 환경별 비용 분포
sum(kubecost_cluster_daily_cost * on(namespace) group_left(env) kube_namespace_labels) by (label_env)

# 유휴 비용 비율
sum(kubecost_cluster_daily_cost{type="idle"})
/
sum(kubecost_cluster_daily_cost)

# Right-sizing 절감 가능 금액
sum(kubecost_savings_memory_total + kubecost_savings_cpu_total)
```

---

## Infracost 설정

### 설치

```bash
# CLI 설치
brew install infracost

# API 키 설정
infracost auth login
# 또는
export INFRACOST_API_KEY="ico-xxx"

# 초기 설정
infracost configure get api_key
```

### GitHub Actions 통합

```yaml
# .github/workflows/infracost.yaml
name: Infracost PR Comment

on:
  pull_request:
    paths:
      - 'terraform/**'
      - '**/*.tf'

jobs:
  infracost:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    env:
      TF_ROOT: terraform/

    steps:
      - uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      # 기준선 (base) 비용
      - name: Checkout base branch
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.ref }}
          path: base

      - name: Generate Infracost baseline
        run: |
          infracost breakdown --path=base/${{ env.TF_ROOT }} \
            --format=json \
            --out-file=/tmp/infracost-base.json

      # PR 브랜치 비용
      - name: Checkout PR branch
        uses: actions/checkout@v4
        with:
          path: pr

      - name: Generate Infracost PR cost
        run: |
          infracost breakdown --path=pr/${{ env.TF_ROOT }} \
            --format=json \
            --out-file=/tmp/infracost-pr.json

      # 비교 및 코멘트
      - name: Generate diff
        run: |
          infracost diff \
            --path=/tmp/infracost-pr.json \
            --compare-to=/tmp/infracost-base.json \
            --format=json \
            --out-file=/tmp/infracost-diff.json

      - name: Post PR comment
        run: |
          infracost comment github \
            --path=/tmp/infracost-diff.json \
            --repo=${{ github.repository }} \
            --pull-request=${{ github.event.pull_request.number }} \
            --github-token=${{ secrets.GITHUB_TOKEN }} \
            --behavior=update

      # 비용 임계값 검사
      - name: Check cost threshold
        run: |
          DIFF=$(cat /tmp/infracost-diff.json | jq '.diffTotalMonthlyCost | tonumber')
          if (( $(echo "$DIFF > 500" | bc -l) )); then
            echo "::error::Monthly cost increase exceeds $500 threshold"
            exit 1
          fi
```

---

## KEDA + Karpenter 통합

### KEDA 설치

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda \
  --namespace keda \
  --create-namespace
```

### Karpenter 설치

```bash
helm repo add karpenter https://charts.karpenter.sh
helm install karpenter karpenter/karpenter \
  --namespace karpenter \
  --create-namespace \
  --set settings.clusterName="my-cluster" \
  --set settings.interruptionQueue="my-cluster" \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=1Gi
```

### CRITICAL: KEDA + Karpenter 최적화 조합

```yaml
# 1. KEDA ScaledObject (이벤트 기반 스케일링)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor
  namespace: order
spec:
  scaleTargetRef:
    name: order-processor
  minReplicaCount: 0       # 제로 스케일 가능!
  maxReplicaCount: 200
  cooldownPeriod: 60
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.ap-northeast-2.amazonaws.com/123456789/orders
        queueLength: "5"   # 5개 메시지당 1개 Pod
        awsRegion: ap-northeast-2
      authenticationRef:
        name: keda-aws-credentials
---
# 2. Karpenter NodePool (Spot 우선)
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: spot-burst
spec:
  template:
    spec:
      requirements:
        # Spot 인스턴스 사용
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"]
        # 인스턴스 타입 다양화 (Spot 가용성 증가)
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["large", "xlarge", "2xlarge"]
        # ARM 인스턴스 포함 (비용 절감)
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: 1000
    memory: 2000Gi
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s   # 빠른 통합으로 비용 절감
    budgets:
      - nodes: "10%"
---
# 3. EC2NodeClass
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: Bottlerocket
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "my-cluster"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "my-cluster"
  tags:
    team: platform
    cost-center: infrastructure
```

### 결과 예시

```
[KEDA] SQS 큐 증가 감지 (메시지 1000개)
    ↓
[KEDA] order-processor 0 → 200 replicas 스케일
    ↓
[Karpenter] 200 pending pods 감지
    ↓
[Karpenter] Spot c6g.xlarge 10대 프로비저닝 (30초)
    ↓
[처리 완료] 큐 비워짐
    ↓
[KEDA] 200 → 0 replicas 스케일다운
    ↓
[Karpenter] 30초 후 노드 통합/종료

비용 절감: On-Demand 대비 70-90%
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Kubecost 할인 미설정 | 실제 비용과 불일치 | CUR/Athena 통합 |
| OpenCost만 의존 | RI/Spot 가격 미반영 | Kubecost로 업그레이드 또는 보정 |
| Infracost 임계값 없음 | 대규모 비용 증가 PR 통과 | 정책 파일 + 검사 |
| KEDA minReplica=1 | 유휴 비용 발생 | minReplica=0 활용 |
| Karpenter 단일 인스턴스 타입 | Spot 가용성 저하 | 다양한 타입 지정 |

---

## 체크리스트

### Kubernetes 비용 도구
- [ ] OpenCost 또는 Kubecost 설치
- [ ] Prometheus 연동 확인
- [ ] 클라우드 가격 통합 (Kubecost)
- [ ] 팀별 대시보드 구축

### IaC 비용 예측
- [ ] Infracost 설치 및 API 키
- [ ] GitHub Actions 통합
- [ ] 비용 임계값 정책
- [ ] PR 자동 코멘트

### 자동 최적화
- [ ] KEDA 설치
- [ ] Karpenter 설치 및 NodePool
- [ ] Spot 인스턴스 활용
- [ ] 통합 + 제로 스케일 활성화

## Sources

- [OpenCost - CNCF](https://opencost.io/)
- [Kubecost Documentation](https://docs.kubecost.com/)
- [Infracost GitHub Actions](https://github.com/infracost/actions)
- [KEDA + Karpenter Integration](https://sufiyanpk.medium.com/simplify-autoscaling-and-cost-optimization-with-keda-and-karpenter-in-an-amazon-eks-cluster-d9058fc52a04)
- [Karpenter Best Practices](https://www.anantacloud.com/post/smarter-cost-optimization-with-karpenter-a-practical-migration-guide)

## 참조 스킬

- `/sre:finops` - FinOps 기초
- `/sre:finops-tools-advanced` - 고급 최적화 도구 (Cast AI, Kubecost 고급, 4Rs Framework)
- `/sre:finops-greenops` - GreenOps & 지속가능성
