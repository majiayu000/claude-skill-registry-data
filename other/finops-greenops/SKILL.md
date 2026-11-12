---
name: finops-greenops
description: "GreenOps — 클라우드 탄소 발자국 측정, 저탄소 리전 선택, ARM 인스턴스 전환, 오프피크 스케줄링, SCI(Software Carbon Intensity). Use when 비용 절감과 함께 탄소 배출을 측정·줄이려 할 때."
---

# GreenOps 가이드

클라우드 탄소 발자국 측정, 지속가능성 최적화, FinOps + GreenOps 통합

## Quick Reference (결정 트리)

```
GreenOps 목표?
    │
    ├─ 탄소 발자국 측정 ────────> Cloud Carbon Footprint
    │       │
    │       └─ 클라우드별 도구 ──> AWS/GCP/Azure 내장 도구
    │
    ├─ 지속가능성 최적화
    │       │
    │       ├─ 저탄소 리전 ──────> Region 선택 가이드
    │       ├─ ARM 인스턴스 ────> Graviton / T2A 전환
    │       └─ 오프피크 스케줄링 > 재생 에너지 시간대 활용
    │
    └─ 리포팅/거버넌스 ────────> ESG 대시보드
```

---

## CRITICAL: GreenOps 개요

### FinOps + GreenOps 시너지

```
┌─────────────────────────────────────────────────────────────────┐
│                    GreenOps = FinOps + Sustainability           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   FinOps                          GreenOps                       │
│   ──────                          ────────                       │
│   비용 최적화         ──────>     탄소 최적화                      │
│   Right-sizing        ──────>     에너지 효율                     │
│   유휴 리소스 제거    ──────>     탄소 낭비 제거                    │
│   Spot Instance       ──────>     가변 수요 + 재생 에너지           │
│                                                                  │
│   ┌────────────────────────────────────────────────────────┐    │
│   │ 핵심 통찰: 비용 최적화 = 탄소 최적화 (대부분의 경우)    │    │
│   └────────────────────────────────────────────────────────┘    │
│                                                                  │
│   예외: 저탄소 리전이 더 비쌀 수 있음 (trade-off 필요)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 핵심 지표

| 지표 | 정의 | 목표 |
|------|------|------|
| **CO2e** | 이산화탄소 환산 배출량 | 감소 추세 |
| **PUE** | Power Usage Effectiveness | < 1.5 |
| **CUE** | Carbon Usage Effectiveness | < 0.5 kg/kWh |
| **REF** | Renewable Energy Factor | > 80% |
| **SCI** | Software Carbon Intensity | 감소 추세 |

---

## 탄소 발자국 측정

### Cloud Carbon Footprint (오픈소스)

```bash
# Docker로 실행
docker pull cloudcarbonfootprint/api
docker pull cloudcarbonfootprint/client

# docker-compose.yaml
version: '3'
services:
  api:
    image: cloudcarbonfootprint/api
    ports:
      - "4000:4000"
    environment:
      - AWS_USE_BILLING_DATA=true
      - AWS_ATHENA_DB_NAME=ccf
      - AWS_ATHENA_REGION=ap-northeast-2
      - GCP_USE_BILLING_DATA=true
      - GCP_BIG_QUERY_TABLE=carbon-data
  client:
    image: cloudcarbonfootprint/client
    ports:
      - "3000:80"
    depends_on:
      - api
```

### AWS Carbon Footprint Tool

```bash
# AWS CLI로 탄소 발자국 조회
aws sustainability get-carbon-footprint-summary \
  --start-date 2026-01-01 \
  --end-date 2026-01-31

# CloudWatch 대시보드 쿼리
# 네임스페이스: AWS/CarbonFootprint
# 메트릭: EstimatedTotalEmissions
```

### GCP Carbon Footprint

```sql
-- BigQuery 탄소 데이터 조회
SELECT
  usage_month,
  service.description AS service,
  location.location AS region,
  carbon_footprint_total_kgCO2e.location_based AS co2e_kg,
  carbon_footprint_total_kgCO2e.market_based AS co2e_market_kg
FROM
  `project.dataset.carbon_footprint`
WHERE
  usage_month >= '2026-01'
ORDER BY
  co2e_kg DESC
LIMIT 20;
```

### Azure Emissions Dashboard

```bash
# Azure CLI로 지속가능성 데이터 조회
az carbon query \
  --scope "/subscriptions/{subscription-id}" \
  --start-date 2026-01-01 \
  --end-date 2026-01-31
```

---

## 저탄소 리전 선택

### CRITICAL: 리전별 탄소 강도

| 클라우드 | 저탄소 리전 | 탄소 강도 (gCO2/kWh) | 재생에너지 % |
|----------|------------|---------------------|--------------|
| **AWS** | eu-north-1 (스톡홀름) | ~20 | ~100% |
| | eu-west-1 (아일랜드) | ~300 | ~85% |
| | us-west-2 (오레곤) | ~100 | ~90% |
| **GCP** | europe-north1 (핀란드) | ~130 | ~100% |
| | us-central1 (아이오와) | ~400 | ~95% |
| **Azure** | swedencentral | ~20 | ~100% |
| | norwayeast | ~30 | ~100% |

### 리전 선택 가이드

```yaml
# 리전 선택 우선순위
region_selection:
  # 1. 지연 시간 요구사항 확인
  latency_requirement:
    critical: true
    max_latency_ms: 50

  # 2. 저탄소 리전 후보 (지연 시간 허용 범위 내)
  low_carbon_regions:
    aws:
      - eu-north-1     # 스웨덴, 매우 낮은 탄소
      - eu-west-1      # 아일랜드, 낮은 탄소
      - us-west-2      # 오레곤, 낮은 탄소
    gcp:
      - europe-north1  # 핀란드
      - us-central1    # 아이오와
    azure:
      - swedencentral
      - norwayeast

  # 3. 비용-탄소 트레이드오프
  tradeoff_rules:
    # 탄소 10% 감소를 위해 비용 5% 증가까지 허용
    max_cost_premium_for_carbon: 5%
```

### Terraform 예시

```hcl
# 저탄소 리전 우선 선택
variable "preferred_regions" {
  default = {
    aws   = ["eu-north-1", "eu-west-1", "us-west-2"]
    gcp   = ["europe-north1", "us-central1"]
    azure = ["swedencentral", "norwayeast"]
  }
}

# 워크로드별 리전 선택
locals {
  # 배치 작업: 저탄소 리전 강제
  batch_region = var.preferred_regions["aws"][0]

  # 사용자 대면: 지연 시간 우선, 저탄소 차선
  user_facing_region = var.user_region_override != "" ? var.user_region_override : var.preferred_regions["aws"][1]
}
```

---

## ARM 인스턴스 전환

### AWS Graviton

```yaml
# Graviton 장점
# - 동일 성능 대비 40% 적은 에너지
# - 20% 저렴한 가격
# - 동일 성능 (대부분 워크로드)

# Karpenter NodePool - Graviton 우선
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: graviton-preferred
spec:
  template:
    spec:
      requirements:
        # ARM 아키텍처 우선
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64", "amd64"]  # arm64 먼저 시도
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values:
            - c7g    # Graviton3 Compute
            - m7g    # Graviton3 General
            - r7g    # Graviton3 Memory
            - c6g    # Graviton2 Compute
            - m6g    # Graviton2 General
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
```

### 멀티 아키텍처 이미지

```dockerfile
# Dockerfile.multiarch
FROM --platform=$BUILDPLATFORM golang:1.22 AS builder
ARG TARGETOS TARGETARCH

WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .

FROM gcr.io/distroless/static:nonroot
COPY --from=builder /app/server /server
ENTRYPOINT ["/server"]
```

```bash
# 멀티 아키텍처 빌드 및 푸시
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myregistry/myapp:latest \
  --push .
```

### GCP T2A (ARM)

```yaml
# GKE Node Pool - T2A
apiVersion: container.google.com/v1beta1
kind: NodePool
metadata:
  name: t2a-pool
spec:
  config:
    machineType: t2a-standard-4  # ARM 기반
    diskSizeGb: 100
    imageType: COS_CONTAINERD
  management:
    autoRepair: true
    autoUpgrade: true
```

---

## 오프피크 스케줄링

### CRITICAL: 재생 에너지 시간대 활용

```
재생 에너지 가용성 (일반적 패턴)
─────────────────────────────────
태양광: 오전 10시 ~ 오후 4시 (피크)
풍력: 야간 ~ 새벽 (지역별 상이)

권장: 배치 작업을 재생 에너지 풍부 시간대에 스케줄링
```

### Kubernetes CronJob 스케줄링

```yaml
# 야간/오프피크 시간대 배치 작업
apiVersion: batch/v1
kind: CronJob
metadata:
  name: data-processing
  labels:
    greenops.io/schedule-type: off-peak
spec:
  # UTC 기준: 한국 새벽 2시 = UTC 17:00 (전일)
  # 유럽 저탄소 리전 기준: 야간 재생 에너지 활용
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          nodeSelector:
            # Spot + 저탄소 노드 선호
            karpenter.sh/capacity-type: spot
          tolerations:
            - key: greenops.io/low-carbon
              operator: Exists
          containers:
            - name: processor
              image: data-processor:latest
              resources:
                requests:
                  cpu: "4"
                  memory: "8Gi"
          restartPolicy: OnFailure
```

### KEDA + 시간 기반 스케일링

```yaml
# 재생 에너지 풍부 시간대에 확장
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: green-batch-processor
spec:
  scaleTargetRef:
    name: batch-processor
  minReplicaCount: 0
  maxReplicaCount: 100
  triggers:
    # 시간 기반: 야간에만 활성화
    - type: cron
      metadata:
        timezone: UTC
        start: "0 18 * * *"   # UTC 18:00 (한국 새벽 3시)
        end: "0 6 * * *"      # UTC 06:00 (한국 오후 3시)
        desiredReplicas: "50"
    # SQS 큐 기반 (주간에는 최소 유지)
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.../batch-queue
        queueLength: "10"
```

---

## SCI (Software Carbon Intensity)

### SCI 공식

```
SCI = ((E × I) + M) / R

E = 에너지 소비 (kWh)
I = 탄소 강도 (gCO2/kWh)
M = 내재 탄소 (하드웨어 제조/폐기)
R = 기능 단위 (트랜잭션, 사용자 등)
```

### SCI 측정 구현

```promql
# SCI 계산용 메트릭

# 에너지 소비 추정 (CPU 기반)
energy_kwh = sum(
  rate(container_cpu_usage_seconds_total[1h])
  * 0.0001  # kWh 변환 계수 (인스턴스별 조정 필요)
)

# 탄소 강도 (리전별 상수)
carbon_intensity_gco2_kwh = 400  # ap-northeast-2 기준

# 기능 단위당 탄소
sci_per_request = (energy_kwh * carbon_intensity_gco2_kwh) / rate(http_requests_total[1h])
```

### Grafana 대시보드 패널

```json
{
  "title": "Software Carbon Intensity (SCI)",
  "panels": [
    {
      "title": "SCI per 1000 Requests (gCO2e)",
      "type": "stat",
      "targets": [{
        "expr": "(sum(rate(container_cpu_usage_seconds_total{namespace=\"api\"}[1h])) * 0.0001 * 400) / (sum(rate(http_requests_total{namespace=\"api\"}[1h])) / 1000)"
      }],
      "thresholds": {
        "steps": [
          {"color": "green", "value": 0},
          {"color": "yellow", "value": 10},
          {"color": "red", "value": 50}
        ]
      }
    },
    {
      "title": "Daily Carbon Emissions (kgCO2e)",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(rate(container_cpu_usage_seconds_total[1h])) * 0.0001 * 400 * 24 / 1000"
      }]
    },
    {
      "title": "Carbon by Service",
      "type": "piechart",
      "targets": [{
        "expr": "sum(rate(container_cpu_usage_seconds_total[24h]) * 0.0001 * 400) by (namespace)"
      }]
    }
  ]
}
```

---

## ESG 리포팅

### 자동 리포트 생성

```python
# greenops_report.py
import boto3
from datetime import datetime, timedelta
import pandas as pd

def generate_greenops_report(start_date, end_date):
    """월간 GreenOps 리포트 생성"""

    # 1. 탄소 발자국 데이터 수집
    sustainability = boto3.client('sustainability')
    carbon_data = sustainability.get_carbon_footprint_summary(
        startDate=start_date,
        endDate=end_date
    )

    # 2. 비용 데이터 수집
    ce = boto3.client('ce')
    cost_data = ce.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    # 3. 효율성 계산
    total_co2e = carbon_data['totalEmissions']['value']
    total_cost = float(cost_data['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

    carbon_efficiency = total_cost / total_co2e  # $/kgCO2e

    # 4. 리포트 생성
    report = {
        'period': f"{start_date} ~ {end_date}",
        'total_co2e_kg': total_co2e,
        'total_cost_usd': total_cost,
        'carbon_efficiency': carbon_efficiency,
        'recommendations': generate_recommendations(carbon_data)
    }

    return report

def generate_recommendations(carbon_data):
    """개선 권장 사항 생성"""
    recommendations = []

    # 고탄소 리전 사용 시
    high_carbon_regions = ['ap-northeast-1', 'ap-southeast-1']
    for region in carbon_data.get('byRegion', []):
        if region['region'] in high_carbon_regions:
            recommendations.append(
                f"리전 {region['region']}의 워크로드를 저탄소 리전으로 이전 검토"
            )

    return recommendations
```

### 대시보드 템플릿

```markdown
## 월간 GreenOps 리포트 - [YYYY-MM]

### 요약

| 지표 | 이번 달 | 전월 | 변화 |
|------|---------|------|------|
| 총 탄소 배출 (kgCO2e) | XXX | XXX | -X% |
| 비용 ($) | XXX | XXX | -X% |
| 탄소 효율 ($/kgCO2e) | XXX | XXX | +X% |
| 재생에너지 비율 | XX% | XX% | +X% |

### 서비스별 탄소 배출

| 서비스 | 탄소 (kgCO2e) | 비율 | 권장 조치 |
|--------|--------------|------|----------|
| API Gateway | XXX | XX% | ARM 전환 |
| Data Pipeline | XXX | XX% | 오프피크 스케줄링 |
| ML Training | XXX | XX% | Spot + 저탄소 리전 |

### 개선 조치 추적

| 조치 | 상태 | 예상 절감 |
|------|------|----------|
| Graviton 전환 | 진행 중 | -40% 에너지 |
| eu-north-1 마이그레이션 | 계획됨 | -80% 탄소 |
| 배치 작업 오프피크 이동 | 완료 | -15% 탄소 |
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 탄소 측정 안 함 | 최적화 불가 | CCF 또는 클라우드 내장 도구 |
| 고탄소 리전만 사용 | 불필요한 배출 | 저탄소 리전 검토 |
| x86만 고집 | 에너지 비효율 | ARM (Graviton/T2A) 전환 |
| 24/7 배치 실행 | 고탄소 시간대 사용 | 오프피크 스케줄링 |
| 비용만 추적 | ESG 미준수 | 탄소 KPI 추가 |

---

## 체크리스트

### 측정
- [ ] Cloud Carbon Footprint 또는 클라우드 내장 도구 설정
- [ ] 서비스별 탄소 배출 추적
- [ ] SCI 메트릭 정의 및 측정

### 최적화
- [ ] 저탄소 리전 식별 및 마이그레이션 계획
- [ ] ARM 인스턴스 (Graviton/T2A) 전환
- [ ] 배치 작업 오프피크 스케줄링
- [ ] 유휴 리소스 제거 (FinOps + GreenOps)

### 리포팅
- [ ] 월간 GreenOps 리포트 자동화
- [ ] ESG 대시보드 구축
- [ ] 팀별 탄소 할당 (Showback)

**관련 agent**: `finops-advisor`, `cost-analyzer`
**관련 skill**: `/sre:finops`, `/sre:finops-tools`

---

## Sources

- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/)
- [AWS Customer Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/)
- [GCP Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Green Software Foundation - SCI](https://greensoftware.foundation/articles/software-carbon-intensity-sci-specification)
- [FinOps + GreenOps Integration](https://www.finops.org/)
