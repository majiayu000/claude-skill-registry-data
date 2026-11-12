---
name: sre-sli-slo
description: "SRE 신뢰성 목표 — SLI 유형별 정의, SLO 설정, SLA 구분, error budget 정책, burn rate 알림, Grafana 대시보드. Use when 서비스의 가용성·지연 목표를 숫자로 정하고 error budget 으로 운영할 때."
---

# SRE: SLI/SLO/SLA 정의 가이드

서비스 신뢰성 목표 설정 및 에러 버짓 관리

## Quick Reference (결정 트리)

```
서비스 유형?
    │
    ├─ API 서비스 ────> Availability + Latency SLO
    │
    ├─ 배치 작업 ─────> Freshness + Correctness SLO
    │
    ├─ 스트리밍 ─────> Throughput + Latency SLO
    │
    └─ 프론트엔드 ───> Availability + LCP/FID SLO

SLO 수준?
    ├─ 99% ──────> 월 7.3시간 다운타임 허용 (내부 서비스)
    ├─ 99.9% ────> 월 43분 다운타임 허용 (일반 서비스)
    ├─ 99.95% ───> 월 22분 다운타임 허용 (중요 서비스)
    └─ 99.99% ───> 월 4.3분 다운타임 허용 (핵심 서비스)
```

---

## CRITICAL: SLI/SLO/SLA 개념

| 개념 | 정의 | 예시 |
|------|------|------|
| **SLI** (Indicator) | 측정 가능한 지표 | 성공 요청 비율, p99 응답시간 |
| **SLO** (Objective) | 목표 수준 | "99.9% 요청이 성공해야 함" |
| **SLA** (Agreement) | 고객과의 계약 | "SLO 미달 시 크레딧 제공" |

```
SLI (측정) → SLO (목표) → SLA (계약)
   ↓            ↓           ↓
 메트릭      내부 목표     외부 약속
```

**핵심 원칙**: SLO는 SLA보다 엄격하게 설정 (버퍼 확보)

---

## SLI 유형별 정의

### 1. Availability (가용성)

```promql
# 성공 요청 비율
sum(rate(http_requests_total{status!~"5.."}[30d]))
/
sum(rate(http_requests_total[30d]))
```

**측정 방식**:
| 방식 | 장점 | 단점 |
|------|------|------|
| 서버 메트릭 | 구현 쉬움 | 클라이언트 에러 누락 |
| 합성 모니터링 | 사용자 관점 | 커버리지 제한 |
| 실제 사용자 측정 (RUM) | 정확함 | 구현 복잡 |

### 2. Latency (지연시간)

```promql
# p99 응답시간 500ms 이하 비율
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[30d]))
/
sum(rate(http_request_duration_seconds_count[30d]))
```

**권장 기준**:
| 서비스 유형 | p50 | p99 |
|------------|-----|-----|
| API (동기) | 100ms | 500ms |
| 웹 페이지 | 500ms | 2s |
| 배치 작업 | - | SLA 정의 |

### 3. Quality (품질)

```promql
# 정상 응답 비율 (비즈니스 로직 성공)
sum(rate(business_operation_total{result="success"}[30d]))
/
sum(rate(business_operation_total[30d]))
```

### 4. Freshness (데이터 신선도)

```promql
# 데이터가 10분 이내로 업데이트된 비율
sum(time() - data_last_updated_timestamp < 600) / count(data_last_updated_timestamp)
```

---

## SLO 설정 가이드

### CRITICAL: SLO 수준별 다운타임

| SLO | 연간 다운타임 | 월간 다운타임 | 적합한 서비스 |
|-----|-------------|--------------|--------------|
| 99% | 3.65일 | 7.3시간 | 내부 도구, 배치 |
| 99.5% | 1.83일 | 3.6시간 | 일반 내부 서비스 |
| 99.9% | 8.76시간 | 43분 | 일반 프로덕션 |
| 99.95% | 4.38시간 | 22분 | 중요 서비스 |
| 99.99% | 52.6분 | 4.3분 | 핵심 인프라 |

### SLO 정의 템플릿

```yaml
# slo-definition.yaml
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: order-service
spec:
  service: "order-service"
  labels:
    team: "backend"
    tier: "critical"
  slos:
    - name: "availability"
      objective: 99.9  # 목표 99.9%
      description: "주문 API 가용성"
      sli:
        events:
          errorQuery: sum(rate(http_requests_total{service="order",status=~"5.."}[{{.window}}]))
          totalQuery: sum(rate(http_requests_total{service="order"}[{{.window}}]))
      alerting:
        pageAlert:
          labels:
            severity: critical
        ticketAlert:
          labels:
            severity: warning

    - name: "latency"
      objective: 99.0
      description: "주문 API p99 응답시간 500ms 이하"
      sli:
        events:
          errorQuery: |
            sum(rate(http_request_duration_seconds_count{service="order"}[{{.window}}]))
            -
            sum(rate(http_request_duration_seconds_bucket{service="order",le="0.5"}[{{.window}}]))
          totalQuery: sum(rate(http_request_duration_seconds_count{service="order"}[{{.window}}]))
```

---

## 에러 버짓 (Error Budget)

### 개념

```
에러 버짓 = 100% - SLO 목표

예: SLO 99.9% → 에러 버짓 0.1%
   월간 요청 1억 건 → 허용 실패 10만 건
```

### 에러 버짓 계산

```promql
# 30일 에러 버짓 소진율
(
  1 - (
    sum(rate(http_requests_total{status!~"5.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))
  )
) / (1 - 0.999)  # SLO 99.9%
```

### 에러 버짓 정책

| 버짓 소진율 | 상태 | 액션 |
|------------|------|------|
| < 50% | 🟢 여유 | 기능 개발 진행 |
| 50-80% | 🟡 주의 | 신규 배포 신중히 |
| 80-100% | 🟠 경고 | 안정화 작업 우선 |
| > 100% | 🔴 초과 | 배포 동결, 복구 집중 |

```yaml
# 에러 버짓 기반 배포 정책
error_budget_policy:
  thresholds:
    - consumed: 50
      actions:
        - notify_team
    - consumed: 80
      actions:
        - require_approval
        - increase_canary_time
    - consumed: 100
      actions:
        - freeze_deployments
        - incident_review_required
```

---

## 알림 설정

### CRITICAL: 다중 윈도우 알림

단일 윈도우 알림은 너무 민감하거나 둔감함. **다중 윈도우** 사용 권장.

```yaml
# Prometheus AlertManager Rules
groups:
  - name: slo-alerts
    rules:
      # 빠른 소진 알림 (1시간 내 5% 소진)
      - alert: ErrorBudgetFastBurn
        expr: |
          (
            slo:sli_error:ratio_rate1h{service="order"} > (14.4 * 0.001)
            and
            slo:sli_error:ratio_rate5m{service="order"} > (14.4 * 0.001)
          )
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "주문 서비스 에러 버짓 급속 소진 중"
          description: "1시간 내 에러 버짓 5% 이상 소진 예상"

      # 느린 소진 알림 (6시간 내 5% 소진)
      - alert: ErrorBudgetSlowBurn
        expr: |
          (
            slo:sli_error:ratio_rate6h{service="order"} > (6 * 0.001)
            and
            slo:sli_error:ratio_rate30m{service="order"} > (6 * 0.001)
          )
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "주문 서비스 에러 버짓 서서히 소진 중"
```

### Burn Rate 참조표

| 윈도우 | Burn Rate | 의미 |
|--------|-----------|------|
| 1시간 | 14.4x | 1시간 내 5% 소진 |
| 6시간 | 6x | 6시간 내 5% 소진 |
| 1일 | 3x | 1일 내 10% 소진 |
| 3일 | 1x | 3일 내 10% 소진 |

---

## Grafana 대시보드

### SLO 대시보드 패널

```json
{
  "panels": [
    {
      "title": "SLO Status",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])) * 100",
        "legendFormat": "Current SLI"
      }],
      "thresholds": {
        "steps": [
          {"color": "red", "value": 99.0},
          {"color": "yellow", "value": 99.5},
          {"color": "green", "value": 99.9}
        ]
      }
    },
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "targets": [{
        "expr": "1 - (slo:error_budget:ratio{service=\"order\"})",
        "legendFormat": "Remaining"
      }],
      "max": 100,
      "thresholds": {
        "steps": [
          {"color": "red", "value": 0},
          {"color": "yellow", "value": 20},
          {"color": "green", "value": 50}
        ]
      }
    },
    {
      "title": "Error Budget Burn Rate (30d)",
      "type": "timeseries",
      "targets": [{
        "expr": "slo:sli_error:ratio_rate1h{service=\"order\"} / 0.001",
        "legendFormat": "1h burn rate"
      }]
    }
  ]
}
```

---

## 도구: Sloth

SLO → Prometheus Rules 자동 생성

### 설치

```bash
# Helm
helm repo add sloth https://slok.github.io/sloth
helm install sloth sloth/sloth
```

### Sloth SLO 정의

```yaml
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: api-gateway
spec:
  service: "api-gateway"
  slos:
    - name: "requests-availability"
      objective: 99.9
      sli:
        events:
          errorQuery: sum(rate(nginx_http_requests_total{status=~"5.."}[{{.window}}]))
          totalQuery: sum(rate(nginx_http_requests_total[{{.window}}]))
      alerting:
        name: ApiGatewayHighErrorRate
        pageAlert:
          labels:
            severity: critical
            team: platform
```

생성되는 Recording Rules:
```yaml
# 자동 생성됨
- record: slo:sli_error:ratio_rate5m
- record: slo:sli_error:ratio_rate30m
- record: slo:sli_error:ratio_rate1h
- record: slo:sli_error:ratio_rate6h
- record: slo:error_budget:ratio
```

---

## 서비스별 SLO 예시

### API 서비스

```yaml
slos:
  - name: availability
    objective: 99.9
    sli: "성공 응답 비율 (non-5xx)"

  - name: latency-p99
    objective: 99.0
    sli: "p99 응답시간 500ms 이하"
```

### 결제 서비스 (Critical)

```yaml
slos:
  - name: availability
    objective: 99.99
    sli: "결제 성공 비율"

  - name: latency-p99
    objective: 99.5
    sli: "p99 응답시간 1s 이하"

  - name: correctness
    objective: 99.999
    sli: "정확한 금액 처리 비율"
```

### 데이터 파이프라인

```yaml
slos:
  - name: freshness
    objective: 99.0
    sli: "데이터가 5분 이내 처리된 비율"

  - name: completeness
    objective: 99.9
    sli: "데이터 손실 없이 처리된 비율"
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| SLO = SLA | 버퍼 없음 | SLO를 더 엄격하게 |
| 100% SLO | 달성 불가, 혁신 억제 | 현실적 목표 (99.9%) |
| 지표 없는 SLO | 측정 불가 | SLI 먼저 정의 |
| 단일 윈도우 알림 | 노이즈 많음 | 다중 윈도우 사용 |
| 모든 서비스 동일 SLO | 비용 낭비 | 중요도별 차등 |
| 에러 버짓 무시 | SLO 형식화 | 정책에 반영 |

---

## 구현 단계

### Phase 1: SLI 정의 (1-2주)
- [ ] 핵심 서비스 식별
- [ ] 서비스별 SLI 메트릭 정의
- [ ] Prometheus 메트릭 수집 확인

### Phase 2: SLO 설정 (1주)
- [ ] 서비스별 SLO 목표 설정
- [ ] Sloth 또는 Recording Rules 설정
- [ ] 에러 버짓 대시보드 생성

### Phase 3: 알림 & 정책 (1주)
- [ ] 다중 윈도우 알림 설정
- [ ] 에러 버짓 정책 문서화
- [ ] 팀 교육

### Phase 4: 운영 (지속)
- [ ] 주간 SLO 리뷰
- [ ] 분기별 SLO 재검토
- [ ] 에러 버짓 기반 배포 관리

---

## 체크리스트

### SLI
- [ ] 측정 가능한 메트릭 정의
- [ ] Prometheus 쿼리 작성
- [ ] Recording Rules 설정

### SLO
- [ ] 현실적 목표 설정 (100% X)
- [ ] SLA보다 엄격하게
- [ ] 문서화

### 에러 버짓
- [ ] 계산 방식 정의
- [ ] 대시보드 구성
- [ ] 소진 정책 수립

### 알림
- [ ] 다중 윈도우 알림
- [ ] Burn rate 기반
- [ ] 적절한 severity

**관련 skill**: `/observability:observability`, `/observability:monitoring-metrics`, `/observability:monitoring-grafana`, `/observability:monitoring-troubleshoot`
