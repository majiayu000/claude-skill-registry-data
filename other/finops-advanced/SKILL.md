---
name: finops-advanced
description: "FinOps 거버넌스 — 성숙도 모델, 태그 기반 비용 할당, 비용 이상 탐지, 안티패턴. Use when 조직 단위로 비용 태그 체계와 이상 탐지를 세우고 성숙도를 끌어올릴 때. 기본 절감 기법은 finops."
---

# FinOps Advanced 가이드

태그 기반 비용 할당, FinOps 성숙도 모델, 기업 비용 거버넌스

## Quick Reference (결정 트리)

```
비용 거버넌스 유형?
    │
    ├─ Showback ──────────> 비용 가시성 (인식만)
    │       │
    │       └─ Kubecost + PromQL + Grafana
    │
    ├─ Chargeback ────────> 실제 비용 청구
    │       │
    │       └─ AWS CUR + Athena + QuickSight
    │
    └─ FinOps 자동화 ──────> 이상 탐지 + 자동 대응
            │
            ├─ 비용 이상 탐지 → ML 기반 알림
            ├─ Infracost PR → IaC 비용 예측
            └─ 유휴 리소스 정리 → 자동화 스크립트
```

---

## CRITICAL: FinOps 성숙도 모델

```
┌─────────────────────────────────────────────────────────────────┐
│                    FinOps Maturity Model                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 1: Crawl          Level 2: Walk          Level 3: Run    │
│  ──────────────          ─────────────          ────────────    │
│  - 비용 가시성            - Showback 구현       - Chargeback     │
│  - 태그 정책 수립         - 팀별 대시보드       - 자동 최적화     │
│  - 기본 알림              - 예산 관리           - ML 비용 예측    │
│                          - Right-sizing         - IaC 비용 통합  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 핵심 지표: Unit Economics (서비스/기능당 비용)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**FinOps 원칙 (심화)**:
| 원칙 | Level 1 | Level 3 |
|------|---------|---------|
| **비용 인식** | 월별 리포트 | 실시간 대시보드 |
| **할당** | 부서별 | 기능/서비스별 |
| **최적화** | 수동 조정 | 자동화 + 예측 |
| **거버넌스** | 가이드라인 | 정책 자동 적용 |

---

## 태그 기반 비용 할당

### CRITICAL: 필수 태그 정책

```yaml
# 필수 태그 (모든 리소스)
required_tags:
  - team           # 담당 팀
  - environment    # dev/staging/prod
  - cost-center    # 비용 귀속 부서
  - service        # 서비스명
  - owner          # 담당자 이메일

# 선택 태그
optional_tags:
  - project        # 프로젝트명
  - feature        # 기능 식별
  - expiry-date    # 만료일 (개발/테스트)
```

### Kyverno 필수 라벨 정책

```yaml
# enforce-cost-labels.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: enforce-cost-labels
  annotations:
    policies.kyverno.io/title: Enforce Cost Labels
    policies.kyverno.io/category: FinOps
    policies.kyverno.io/severity: high
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: require-finops-labels
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
                - DaemonSet
      validate:
        message: >-
          FinOps 필수 라벨이 누락되었습니다: team, environment, cost-center, service.
          예시: team=backend, environment=prod, cost-center=platform, service=order-api
        pattern:
          metadata:
            labels:
              team: "?*"
              environment: "dev | staging | prod"
              cost-center: "?*"
              service: "?*"

    - name: require-owner-annotation
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "owner 어노테이션이 필요합니다 (이메일 형식)"
        pattern:
          metadata:
            annotations:
              owner: "*@*.*"
```

### AWS 태그 정책 (Terraform)

```hcl
# aws-tag-policy.tf
resource "aws_organizations_policy" "cost_tags" {
  name        = "cost-allocation-tags"
  description = "Required tags for cost allocation"
  type        = "TAG_POLICY"

  content = jsonencode({
    tags = {
      team = {
        tag_key = {
          @@assign = "team"
        }
        enforced_for = {
          @@assign = [
            "ec2:instance",
            "ec2:volume",
            "rds:db",
            "eks:cluster",
            "s3:bucket"
          ]
        }
      }
      environment = {
        tag_key = {
          @@assign = "environment"
        }
        tag_value = {
          @@assign = ["dev", "staging", "prod"]
        }
      }
      cost-center = {
        tag_key = {
          @@assign = "cost-center"
        }
      }
    }
  })
}

# 모든 리소스에 기본 태그 적용
locals {
  default_tags = {
    team         = var.team
    environment  = var.environment
    cost-center  = var.cost_center
    service      = var.service_name
    managed-by   = "terraform"
  }
}

provider "aws" {
  default_tags {
    tags = local.default_tags
  }
}
```

---

## 비용 이상 탐지

### Prometheus 알림 규칙

```yaml
# finops-alerts.yaml
groups:
  - name: finops-anomaly
    rules:
      # 일일 비용 급증 (전일 대비 30% 이상)
      - alert: DailyCostSpike
        expr: |
          (
            sum(kubecost_cluster_daily_cost)
            -
            sum(kubecost_cluster_daily_cost offset 1d)
          )
          /
          sum(kubecost_cluster_daily_cost offset 1d)
          > 0.3
        for: 30m
        labels:
          severity: warning
          category: finops
        annotations:
          summary: "클러스터 일일 비용이 30% 이상 증가"
          description: |
            현재 비용: {{ $value | humanize }}% 증가
            비용 검토가 필요합니다.

      # 팀별 예산 초과
      - alert: TeamBudgetExceeded
        expr: |
          sum(
            kubecost_cluster_daily_cost
            * on(namespace) group_left(team)
            kube_namespace_labels
          ) by (label_team) * 30 > 10000
        for: 1h
        labels:
          severity: warning
          category: finops
        annotations:
          summary: "팀 {{ $labels.label_team }} 월간 예산 초과 예상"
          description: "예상 비용: ${{ $value | humanize }}"

      # 유휴 리소스 비율 과다
      - alert: HighIdleCost
        expr: |
          sum(kubecost_cluster_daily_cost{type="idle"})
          /
          sum(kubecost_cluster_daily_cost)
          > 0.3
        for: 2h
        labels:
          severity: warning
          category: finops
        annotations:
          summary: "유휴 리소스 비용이 30%를 초과"
          description: "Right-sizing 검토가 필요합니다."
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 태그 없는 리소스 | Chargeback 불가 | Kyverno 강제 정책 |
| Showback만 구현 | 책임 소재 불명확 | Chargeback 도입 |
| 월간 리포트만 | 이상 탐지 지연 | 실시간 알림 구축 |
| IaC 비용 미검토 | 예상치 못한 비용 | Infracost PR 통합 |
| 수동 정리 | 좀비 리소스 누적 | 자동 정리 CronJob |
| 과도한 자동 삭제 | 서비스 장애 위험 | 리포트 → 승인 → 삭제 |

---

## 체크리스트

### 태그 정책
- [ ] 필수 태그 정의 (team, environment, cost-center)
- [ ] Kyverno 라벨 강제 정책
- [ ] AWS Organizations 태그 정책
- [ ] 태그 준수율 대시보드

### 모니터링
- [ ] 비용 이상 탐지 알림
- [ ] 팀별 예산 알림
- [ ] 유휴 리소스 알림

**관련 skill**: `/sre:finops-showback` (Showback/Chargeback), `/sre:finops-automation` (자동화), `/sre:finops`, `/k8s:k8s-autoscaling`
