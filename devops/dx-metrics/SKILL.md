---
name: dx-metrics
description: "개발자 생산성 측정 — DORA, SPACE, DevEx, DX Core 4 프레임워크 비교와 메트릭 수집 구조. Use when 팀 생산성·배포 빈도·리드타임을 측정하거나 어떤 DX 지표 프레임워크를 쓸지 정할 때."
---

# Developer Experience Metrics 가이드

DORA, SPACE, DevEx, DX Core 4 프레임워크를 활용한 개발자 생산성 측정

## Quick Reference (결정 트리)

```
측정 목적?
    │
    ├─ 딜리버리 성능 ────────> DORA Metrics
    │       │
    │       └─ 배포 빈도, Lead Time, 실패율, MTTR
    │
    ├─ 개발자 경험 전체 ────> SPACE Framework
    │       │
    │       └─ 만족도, 성과, 활동, 협업, 효율성
    │
    ├─ 마찰점 개선 ─────────> DevEx Framework
    │       │
    │       └─ Flow State, Cognitive Load, Feedback Loops
    │
    └─ 비즈니스 임팩트 ────> DX Core 4
            │
            └─ Speed, Effectiveness, Quality, Business Impact
```

---

## CRITICAL: 프레임워크 비교

```
┌─────────────────────────────────────────────────────────────────┐
│              Developer Productivity Frameworks                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DORA (2014)          SPACE (2021)         DevEx (2023)         │
│  ───────────          ────────────         ───────────          │
│  딜리버리 파이프라인    전체 개발 경험        개발자 관점          │
│  4 Key Metrics        5 Dimensions         3 Core Dimensions    │
│  정량적               정량+정성             정성 중심            │
│                                                                  │
│                    DX Core 4 (2024)                              │
│                    ───────────────                               │
│                    통합 프레임워크                                │
│                    Speed + Effectiveness                         │
│                    Quality + Business Impact                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 프레임워크 | 초점 | 데이터 소스 | 적합한 상황 |
|------------|------|-------------|-------------|
| **DORA** | 딜리버리 속도/안정성 | CI/CD 시스템 | 파이프라인 최적화 |
| **SPACE** | 전체 개발자 경험 | 설문 + 시스템 | 팀 건강 모니터링 |
| **DevEx** | 개발자 마찰점 | 설문 + 관찰 | 병목 지점 개선 |
| **DX Core 4** | 비즈니스 임팩트 | 통합 | 경영진 보고, ROI 증명 |

---

## DORA Metrics

### 4 Key Metrics

| 메트릭 | 정의 | Elite 기준 | 측정 방법 |
|--------|------|------------|-----------|
| **Deployment Frequency** | 프로덕션 배포 빈도 | 하루 여러 번 | CI/CD 로그 |
| **Lead Time for Changes** | 커밋 → 프로덕션 시간 | < 1시간 | Git + Deploy 시간 |
| **Change Failure Rate** | 배포 후 실패 비율 | < 5% | Incident 데이터 |
| **MTTR** | 장애 복구 시간 | < 1시간 | Incident 데이터 |

### 성과 수준 분류

```
Performance Level        Deploy Freq    Lead Time    CFR      MTTR
─────────────────────────────────────────────────────────────────
Elite                    Multiple/day   < 1 hour     < 5%     < 1 hour
High                     Daily-Weekly   1 day-1 week < 10%    < 1 day
Medium                   Weekly-Monthly 1-6 months   10-15%   1 day-1 week
Low                      < Monthly      > 6 months   > 15%    > 1 week
```

### DORA 수집 구현 (GitHub Actions)

```yaml
# .github/workflows/dora-metrics.yaml
name: DORA Metrics Collection

on:
  deployment:
  workflow_run:
    workflows: ["Deploy"]
    types: [completed]

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Calculate Lead Time
        id: lead-time
        run: |
          # 마지막 커밋 시간
          COMMIT_TIME=$(git log -1 --format=%ct)
          DEPLOY_TIME=$(date +%s)
          LEAD_TIME=$((DEPLOY_TIME - COMMIT_TIME))
          echo "lead_time_seconds=$LEAD_TIME" >> $GITHUB_OUTPUT
          echo "lead_time_hours=$((LEAD_TIME / 3600))" >> $GITHUB_OUTPUT

      - name: Send to Metrics Backend
        run: |
          curl -X POST "${{ secrets.METRICS_ENDPOINT }}/dora" \
            -H "Content-Type: application/json" \
            -d '{
              "metric": "deployment",
              "repository": "${{ github.repository }}",
              "sha": "${{ github.sha }}",
              "lead_time_seconds": ${{ steps.lead-time.outputs.lead_time_seconds }},
              "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
            }'
```

### Prometheus DORA 메트릭

```yaml
# prometheus-rules.yaml
groups:
  - name: dora-metrics
    rules:
      # 배포 빈도 (일간)
      - record: dora:deployment_frequency:daily
        expr: |
          sum(increase(deployments_total[24h])) by (service)

      # Lead Time (평균)
      - record: dora:lead_time:avg
        expr: |
          avg(deployment_lead_time_seconds) by (service)

      # 변경 실패율
      - record: dora:change_failure_rate
        expr: |
          sum(rate(deployment_failures_total[7d])) by (service)
          /
          sum(rate(deployments_total[7d])) by (service)

      # MTTR
      - record: dora:mttr:avg
        expr: |
          avg(incident_resolution_time_seconds) by (service)
```

### Grafana 대시보드 패널

```json
{
  "panels": [
    {
      "title": "Deployment Frequency (Daily)",
      "type": "stat",
      "targets": [{
        "expr": "sum(dora:deployment_frequency:daily)"
      }],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 1, "color": "yellow"},
              {"value": 7, "color": "green"}
            ]
          }
        }
      }
    },
    {
      "title": "Lead Time Trend",
      "type": "timeseries",
      "targets": [{
        "expr": "dora:lead_time:avg / 3600",
        "legendFormat": "Hours"
      }]
    },
    {
      "title": "Change Failure Rate",
      "type": "gauge",
      "targets": [{
        "expr": "dora:change_failure_rate * 100"
      }],
      "fieldConfig": {
        "defaults": {
          "max": 100,
          "thresholds": {
            "steps": [
              {"value": 0, "color": "green"},
              {"value": 5, "color": "yellow"},
              {"value": 15, "color": "red"}
            ]
          }
        }
      }
    }
  ]
}
```

---

## SPACE Framework

### 5 Dimensions

| Dimension | 측정 내용 | 예시 메트릭 |
|-----------|----------|-------------|
| **S**atisfaction | 만족도, 웰빙 | eNPS, 번아웃 지수 |
| **P**erformance | 성과, 결과물 | 코드 리뷰 품질, 버그 탈출율 |
| **A**ctivity | 활동량 | 커밋 수, PR 수, 코드 라인 |
| **C**ommunication | 협업, 소통 | 리뷰 응답 시간, 미팅 시간 |
| **E**fficiency | 효율성, 흐름 | 방해 없는 시간, 컨텍스트 스위칭 |

### CRITICAL: Activity Metrics 주의사항

```
⚠️  Activity 메트릭 단독 사용 금지

잘못된 사용:
  - 커밋 수로 개발자 평가
  - 코드 라인 수로 생산성 측정
  - PR 수로 순위 매기기

올바른 사용:
  - 다른 Dimension과 함께 맥락적으로 해석
  - 팀 수준에서 트렌드 파악
  - 개인 비교가 아닌 시스템 병목 발견
```

### SPACE 설문 예시

```yaml
# space-survey.yaml
survey:
  frequency: bi-weekly
  questions:
    # Satisfaction
    - id: satisfaction_recommend
      type: scale_1_10
      text: "팀의 개발 환경을 동료에게 추천하시겠습니까?"

    - id: satisfaction_burnout
      type: scale_1_5
      text: "지난 2주간 번아웃을 느낀 정도는?"

    # Performance
    - id: performance_quality
      type: scale_1_5
      text: "최근 배포한 코드의 품질에 만족하십니까?"

    # Activity (시스템에서 자동 수집)

    # Communication
    - id: communication_review
      type: scale_1_5
      text: "코드 리뷰를 통해 유용한 피드백을 받고 있습니까?"

    - id: communication_meetings
      type: hours
      text: "주간 미팅에 소요되는 시간은?"

    # Efficiency
    - id: efficiency_flow
      type: hours
      text: "방해 없이 집중할 수 있는 시간(Deep Work)은 하루 몇 시간?"

    - id: efficiency_tools
      type: scale_1_5
      text: "개발 도구가 생산성을 돕고 있습니까?"
```

---

## DevEx Framework

### 3 Core Dimensions

```
┌─────────────────────────────────────────────────────────────────┐
│                    DevEx Framework                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Flow State              Cognitive Load         Feedback Loops   │
│  ──────────              ──────────────         ──────────────   │
│  몰입 상태 유지           정신적 부담 최소화      빠른 피드백       │
│                                                                  │
│  측정:                   측정:                   측정:            │
│  - 방해 없는 시간         - 도구 복잡도           - 빌드 시간       │
│  - 컨텍스트 스위칭        - 문서 찾기 시간        - 테스트 시간     │
│  - 몰입 빈도             - 온보딩 기간           - 리뷰 대기 시간   │
│                                                                  │
│  개선:                   개선:                   개선:            │
│  - 미팅 프리 시간         - Golden Paths         - CI 최적화       │
│  - 알림 최소화           - 셀프서비스 플랫폼     - 자동화 리뷰     │
│  - 비동기 소통           - 표준화               - 로컬 개발 환경   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### DevEx 개선 우선순위

| 순위 | 영역 | 임팩트 | 구현 난이도 |
|------|------|--------|-------------|
| 1 | 빌드/테스트 시간 단축 | 매우 높음 | 중간 |
| 2 | 로컬 개발 환경 개선 | 높음 | 낮음 |
| 3 | 문서화 및 검색성 | 높음 | 낮음 |
| 4 | 코드 리뷰 프로세스 | 중간 | 낮음 |
| 5 | 온보딩 자동화 | 중간 | 중간 |

### Feedback Loop 측정

```promql
# 빌드 시간
histogram_quantile(0.95,
  sum(rate(ci_build_duration_seconds_bucket[7d])) by (le, pipeline)
)

# PR 리뷰 대기 시간
avg(pull_request_review_wait_seconds) by (repository)

# 테스트 실행 시간
histogram_quantile(0.95,
  sum(rate(test_execution_duration_seconds_bucket[7d])) by (le, suite)
)

# 배포 대기 시간 (PR 머지 → 프로덕션)
avg(deployment_wait_time_seconds) by (service)
```

---

## DX Core 4 (통합 프레임워크)

### 4 Dimensions

```
┌─────────────────────────────────────────────────────────────────┐
│                      DX Core 4                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐          ┌─────────────────┐               │
│  │     Speed       │          │  Effectiveness  │               │
│  │   ───────────   │          │  ─────────────  │               │
│  │ DORA Delivery + │          │ Developer       │               │
│  │ Perceived Speed │          │ Experience Index│               │
│  └─────────────────┘          └─────────────────┘               │
│                                                                  │
│  ┌─────────────────┐          ┌─────────────────┐               │
│  │    Quality      │          │ Business Impact │               │
│  │   ──────────    │          │ ───────────────  │               │
│  │ DORA Stability +│          │ ROI, Revenue    │               │
│  │ Code Quality    │          │ Enabled         │               │
│  └─────────────────┘          └─────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 메트릭 매핑

| Dimension | 정량 메트릭 | 정성 메트릭 |
|-----------|-------------|-------------|
| **Speed** | Deploy Freq, Lead Time | "빠르게 배포할 수 있다" |
| **Effectiveness** | DXI Score, Flow Time | "효율적으로 일할 수 있다" |
| **Quality** | CFR, MTTR, Bug Escape Rate | "품질에 자신감이 있다" |
| **Business Impact** | Feature Cycle Time, Revenue | "비즈니스 가치를 전달한다" |

### DXI (Developer Experience Index) 계산

```python
# dxi_calculator.py
def calculate_dxi(metrics: dict) -> float:
    """
    DXI = (Deep Work + Local Iteration + Release Process + Confidence) / 4

    각 항목 0-100 점수
    """
    weights = {
        'deep_work': 0.25,           # 방해 없는 집중 시간
        'local_iteration': 0.25,     # 로컬 개발 속도
        'release_process': 0.25,     # 릴리스 프로세스 효율
        'confidence': 0.25           # 변경에 대한 자신감
    }

    dxi = sum(
        metrics.get(key, 0) * weight
        for key, weight in weights.items()
    )

    return round(dxi, 1)

# 예시
metrics = {
    'deep_work': 65,          # 하루 4시간+ 집중 가능
    'local_iteration': 80,    # 빠른 로컬 빌드/테스트
    'release_process': 70,    # 원활한 배포 프로세스
    'confidence': 75          # 변경에 대한 높은 자신감
}

dxi = calculate_dxi(metrics)  # 72.5
# DXI 1점 개선 = 개발자당 주 13분 절약
```

### ROI 계산

```python
# finops_roi.py
def calculate_dx_roi(
    developers: int,
    avg_salary: float,
    dxi_improvement: float
) -> dict:
    """
    DXI 1점 개선 = 주당 13분 절약 (연구 기반)
    """
    minutes_saved_per_week = dxi_improvement * 13
    hours_saved_per_year = (minutes_saved_per_week * 52) / 60

    hourly_rate = avg_salary / (52 * 40)  # 연봉 → 시급
    savings_per_developer = hours_saved_per_year * hourly_rate
    total_savings = savings_per_developer * developers

    return {
        'hours_saved_per_developer': round(hours_saved_per_year, 1),
        'savings_per_developer': round(savings_per_developer, 2),
        'total_annual_savings': round(total_savings, 2),
        'dxi_improvement': dxi_improvement
    }

# 예시: 50명 개발팀, 평균 연봉 1억, DXI 5점 개선
roi = calculate_dx_roi(
    developers=50,
    avg_salary=100_000_000,
    dxi_improvement=5
)
# {
#   'hours_saved_per_developer': 56.3,
#   'savings_per_developer': 2,706,730,
#   'total_annual_savings': 135,336,500,
#   'dxi_improvement': 5
# }
```

---

## 메트릭 수집 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                  DX Metrics Collection                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  GitHub  │  │   CI/CD  │  │  Jira/   │  │ Surveys  │        │
│  │   API    │  │  Metrics │  │  Linear  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴──────┬──────┴─────────────┘               │
│                            │                                    │
│                    ┌───────▼───────┐                            │
│                    │   Collector   │                            │
│                    │   Service     │                            │
│                    └───────┬───────┘                            │
│                            │                                    │
│              ┌─────────────┼─────────────┐                      │
│              │             │             │                      │
│       ┌──────▼──────┐ ┌────▼────┐ ┌─────▼─────┐                │
│       │ TimeSeries  │ │ Analytics│ │ Alerting  │                │
│       │ (Prometheus)│ │ (BI Tool)│ │           │                │
│       └─────────────┘ └─────────┘ └───────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 권장 도구 스택

| 목적 | 도구 | 비고 |
|------|------|------|
| 메트릭 수집 | Prometheus, OpenTelemetry | 시계열 데이터 |
| 대시보드 | Grafana, Looker | 시각화 |
| 설문 | Typeform, Google Forms | 정기 수집 |
| 통합 플랫폼 | DX, LinearB, Jellyfish | 상용 솔루션 |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Activity 메트릭으로 개인 평가 | 게이밍, 신뢰 파괴 | 팀 수준 트렌드만 |
| DORA만 측정 | 개발자 경험 무시 | SPACE/DevEx 병행 |
| 너무 많은 메트릭 | 분석 마비 | Core 4 집중 |
| 경영진 보고용만 | 팀 개선 안됨 | 팀 대시보드 공유 |
| 분기 1회 측정 | 트렌드 놓침 | 실시간 + 격주 설문 |
| 벤치마크 맹신 | 맥락 무시 | 자체 베이스라인 우선 |

---

## 체크리스트

### DORA 구축
- [ ] CI/CD에서 배포 이벤트 수집
- [ ] Lead Time 자동 계산
- [ ] Incident 데이터 연동
- [ ] Grafana 대시보드 구축

### SPACE/DevEx
- [ ] 격주 설문 설계 및 자동화
- [ ] Activity 메트릭 시스템 연동
- [ ] 설문 결과 → 액션 아이템 프로세스

### DX Core 4
- [ ] DXI 계산 로직 구현
- [ ] ROI 리포트 자동화
- [ ] 경영진 대시보드 구축

### 거버넌스
- [ ] 메트릭 사용 가이드라인 문서화
- [ ] 팀별 목표 설정 (Elite 기준)
- [ ] 분기별 리뷰 프로세스

**관련 skill**: `/sre:sre-sli-slo`, `/observability:monitoring-grafana`, `/platform:platform-backstage`
