---
name: finops-showback
description: "팀별 비용 가시화 — Showback·Chargeback 구현, Kubecost 대시보드, AWS CUR 기반 배분, Prophet 비용 예측. Use when 팀·서비스별 클라우드 비용을 보여 주거나 부서에 청구하는 체계를 만들 때."
---

# FinOps: Showback & Chargeback 가이드

팀별 비용 가시화, Kubecost 대시보드, AWS CUR 기반 Chargeback

## Quick Reference

```
비용 할당 방식?
    │
    ├─ Showback ────────> 비용 인식 (청구 없음)
    │       │
    │       └─ Kubecost + Grafana 대시보드
    │
    └─ Chargeback ──────> 실제 비용 청구
            │
            └─ AWS CUR + Athena + 자동 리포트
```

---

## Showback 구현

### Kubecost 고급 설정

```yaml
# kubecost-values.yaml
kubecostModel:
  # 실제 클라우드 가격 연동
  cloudIntegrationEnabled: true

# AWS 가격 통합
cloudCost:
  enabled: true
  aws:
    enabled: true
    athenaQueryEnabled: true
    athenaBucketName: "s3://aws-cur-reports"
    athenaRegion: "ap-northeast-2"
    athenaDatabase: "athenacurcfn_cost_report"
    athenaTable: "cost_report"

# 사용자 정의 비용 할당
customCostAllocation:
  enabled: true
  # 네임스페이스 → 팀 매핑
  teamMappings:
    - namespace: "order-*"
      team: "commerce"
    - namespace: "user-*"
      team: "platform"
    - namespace: "infra-*"
      team: "sre"
```

### Showback 대시보드 (PromQL)

```promql
# 팀별 일일 비용 (CPU + Memory + Storage)
sum(
  (
    # CPU 비용
    sum(rate(container_cpu_usage_seconds_total{namespace!~"kube-system|istio-system"}[1h])) by (namespace)
    * on() group_left()
    scalar(kubecost_cpu_hourly_cost) * 24
  )
  +
  (
    # Memory 비용
    sum(container_memory_working_set_bytes{namespace!~"kube-system|istio-system"}) by (namespace)
    / 1024 / 1024 / 1024
    * on() group_left()
    scalar(kubecost_memory_hourly_cost) * 24
  )
  * on(namespace) group_left(team)
  kube_namespace_labels
) by (label_team)

# 팀별 월간 비용 추정
sum(
  kubecost_cluster_daily_cost{type!="idle"}
  * on(namespace) group_left(team)
  kube_namespace_labels
) by (label_team) * 30

# 환경별 비용 분포
sum(
  kubecost_cluster_daily_cost
  * on(namespace) group_left(environment)
  kube_namespace_labels
) by (label_environment) * 30

# 서비스별 비용 (세분화)
sum(
  kubecost_container_cost_daily
  * on(namespace, pod) group_left(service)
  kube_pod_labels
) by (label_service) * 30
```

### Grafana 대시보드 JSON

```json
{
  "title": "FinOps Showback Dashboard",
  "panels": [
    {
      "title": "팀별 월간 비용 (예상)",
      "type": "piechart",
      "targets": [{
        "expr": "sum(kubecost_cluster_daily_cost * on(namespace) group_left(team) kube_namespace_labels) by (label_team) * 30"
      }]
    },
    {
      "title": "환경별 비용 추이",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(kubecost_cluster_daily_cost * on(namespace) group_left(environment) kube_namespace_labels) by (label_environment)",
        "legendFormat": "{{label_environment}}"
      }]
    },
    {
      "title": "비용 Top 10 서비스",
      "type": "bargauge",
      "targets": [{
        "expr": "topk(10, sum(kubecost_container_cost_daily * on(namespace, pod) group_left(service) kube_pod_labels) by (label_service) * 30)"
      }]
    }
  ]
}
```

---

## Chargeback 구현

### AWS CUR (Cost and Usage Report) 설정

```hcl
# aws-cur.tf
resource "aws_cur_report_definition" "cost_report" {
  report_name                = "cost-report"
  time_unit                  = "HOURLY"
  format                     = "Parquet"
  compression                = "Parquet"
  additional_schema_elements = ["RESOURCES", "SPLIT_COST_ALLOCATION_DATA"]
  s3_bucket                  = aws_s3_bucket.cur_bucket.id
  s3_prefix                  = "cur"
  s3_region                  = "ap-northeast-2"
  additional_artifacts       = ["ATHENA"]
  refresh_closed_reports     = true
  report_versioning          = "OVERWRITE_REPORT"
}

resource "aws_s3_bucket" "cur_bucket" {
  bucket = "${var.company}-aws-cur-reports"
}

# Athena 데이터베이스 자동 생성 (AWS가 관리)
```

### Athena 쿼리 (팀별 Chargeback)

```sql
-- 팀별 월간 비용 (EC2 + EKS + RDS)
SELECT
  resource_tags_user_team AS team,
  resource_tags_user_environment AS environment,
  DATE_FORMAT(line_item_usage_start_date, '%Y-%m') AS month,
  SUM(line_item_unblended_cost) AS total_cost,
  SUM(CASE WHEN product_product_name = 'Amazon Elastic Compute Cloud'
      THEN line_item_unblended_cost ELSE 0 END) AS ec2_cost,
  SUM(CASE WHEN product_product_name = 'Amazon Elastic Container Service for Kubernetes'
      THEN line_item_unblended_cost ELSE 0 END) AS eks_cost,
  SUM(CASE WHEN product_product_name = 'Amazon Relational Database Service'
      THEN line_item_unblended_cost ELSE 0 END) AS rds_cost
FROM
  "athenacurcfn_cost_report"."cost_report"
WHERE
  line_item_usage_start_date >= DATE_ADD('month', -1, CURRENT_DATE)
  AND resource_tags_user_team IS NOT NULL
GROUP BY
  resource_tags_user_team,
  resource_tags_user_environment,
  DATE_FORMAT(line_item_usage_start_date, '%Y-%m')
ORDER BY
  total_cost DESC;

-- 태그 없는 리소스 비용 (미할당)
SELECT
  product_product_name,
  line_item_resource_id,
  SUM(line_item_unblended_cost) AS untagged_cost
FROM
  "athenacurcfn_cost_report"."cost_report"
WHERE
  line_item_usage_start_date >= DATE_ADD('month', -1, CURRENT_DATE)
  AND resource_tags_user_team IS NULL
  AND line_item_unblended_cost > 1
GROUP BY
  product_product_name,
  line_item_resource_id
ORDER BY
  untagged_cost DESC
LIMIT 100;
```

### 자동 리포트 생성 (Lambda)

```python
# chargeback_report.py
import boto3
import pandas as pd
from datetime import datetime, timedelta

def lambda_handler(event, context):
    athena = boto3.client('athena')
    s3 = boto3.client('s3')
    ses = boto3.client('ses')

    # 팀별 비용 쿼리 실행
    query = """
    SELECT
      resource_tags_user_team AS team,
      SUM(line_item_unblended_cost) AS total_cost
    FROM "athenacurcfn_cost_report"."cost_report"
    WHERE line_item_usage_start_date >= DATE_ADD('month', -1, CURRENT_DATE)
    GROUP BY resource_tags_user_team
    """

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'athenacurcfn_cost_report'},
        ResultConfiguration={'OutputLocation': 's3://query-results/'}
    )

    # 결과 처리 및 이메일 발송
    # ... (결과 대기 및 CSV 생성 로직)

    return {'statusCode': 200}
```

---

## 비용 예측 (Prophet 기반)

```python
# cost_forecasting.py
from prophet import Prophet
import pandas as pd
from prometheus_api_client import PrometheusConnect

def forecast_cost(prometheus_url, days_ahead=30):
    prom = PrometheusConnect(url=prometheus_url)

    # 지난 90일 비용 데이터 조회
    query = 'sum(kubecost_cluster_daily_cost)'
    result = prom.custom_query_range(
        query=query,
        start_time=datetime.now() - timedelta(days=90),
        end_time=datetime.now(),
        step='1d'
    )

    # Prophet 입력 형식으로 변환
    df = pd.DataFrame({
        'ds': [r['values'][0][0] for r in result],
        'y': [float(r['values'][0][1]) for r in result]
    })

    # 예측 모델 학습
    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(df)

    # 미래 예측
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
```

---

## 체크리스트

### Showback
- [ ] Kubecost 설치 및 클라우드 연동
- [ ] 팀별/환경별 대시보드 구축
- [ ] 월간 비용 리포트 자동화

### Chargeback
- [ ] AWS CUR 설정
- [ ] Athena 쿼리 최적화
- [ ] 자동 리포트 생성 (Lambda)
- [ ] 부서별 청구 프로세스

### 예측
- [ ] 비용 예측 모델 구축
- [ ] 예산 초과 알림

**관련 skill**: `/sre:finops-advanced` (허브), `/sre:finops-automation` (자동화), `/observability:monitoring-metrics`
