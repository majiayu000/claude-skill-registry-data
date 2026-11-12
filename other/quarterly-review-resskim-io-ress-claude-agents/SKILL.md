---
name: quarterly-review
description: "분기 엔지니어링 회고 — DORA 4 metrics 추이, SLO 달성률, 인시던트 패턴, ADR hit rate, FinOps·MRR cohort, 회고 미팅 진행, 1페이지 보고서. Use when 지난 분기 성과를 데이터로 회고하고 다음 분기로 인계할 때."
license: MIT
---

# Quarterly Review — 분기 엔지니어링 회고

**지난 분기 결과를 데이터로 회고하고 다음 분기로 인계**한다. 다음 분기 계획·OKR 수립은 `dx/engineering-strategy.md`. 이 skill은 회고 facilitation + 정량 지표 산출 + lessons-to-action 흐름에 집중.

> 핵심 질문: "OKR을 달성했나? 못했다면 왜?" "DORA 추이가 개선됐나?" "사고 패턴에서 시스템적 문제가 보이나?" "예산 vs 실측 차이는?"

## When to Use

- 분기말 (3·6·9·12월) 엔지니어링 회고 facilitation
- 한국 회계연도 결산 (1·4·7·10월 첫 주) 데이터 정리
- 연간 회고 (Q4 → 다음 해 Q1 전환)
- All-hands 또는 board reporting용 메트릭 패키지 작성
- Tech debt register 분기 갱신
- ADR 회고 결과 통합 (`dx/adr-retrospective.md`)
- 인시던트 누적 패턴 분석 (operations/incident-postmortem.md 데이터)
- DORA 메트릭이 처음 도입된 후 첫 분기

**관련 skill (cross-link)**:
- `dx/engineering-strategy.md` — Tech Radar, OKR, Now/Next/Later (다음 분기 계획)
- `dx/adr-retrospective.md` — ADR hit rate / lifespan (회고 인풋)
- `operations/incident-postmortem.md` — 인시던트 카운트 / 카테고리 / RCA
- `sre/sli-slo-design.md` — SLO 달성률 산출 (해당 skill 있는 경우)
- `sre/finops-ai.md` — Unit Economics, FinOps 추이
- `business/subscription-billing-metrics.md` — MRR Movement, Cohort SQL (재사용)
- `observability/observability-cost.md` — 관측 스택 비용 추이

---

## 분기 회고 사이클 (12주)

```
W1 (분기 시작)            W12 (분기 끝)
   │                          │
   ├─ 다음 분기 계획 (W12 직후) ─┐
   │                            ▼
   ├─ Mid-quarter 체크 (W6)   회고 데이터 수집 (W11)
   │                            │
   └─ 매주 DORA 메트릭 모니터    회고 미팅 (W12 마지막 주)
                                 │
                                 ▼
                              회고 보고서 + lessons → 다음 분기 OKR
```

| 시점 | 작업 |
|---|---|
| 매주 | DORA 4 metrics 자동 수집, SLO burn rate 모니터 |
| W6 (mid-quarter) | OKR 진행률 점검, course correction |
| W11 | 데이터 수집 1주 전 작업 (incident dump, ADR review) |
| W12 마지막 주 | 회고 미팅 (2시간), 보고서 작성 |
| W12+1 | 다음 분기 OKR 수립 (`engineering-strategy.md`) |

---

## 데이터 수집 체크리스트 (회고 1주 전)

| 영역 | 데이터 | 출처 |
|---|---|---|
| **DORA** | Lead time / Deploy freq / Change failure / MTTR | CI/CD logs, 인시던트 DB |
| **SLO** | 각 서비스 SLO 달성률, error budget 소진 | Prometheus / SLO 대시보드 |
| **인시던트** | SEV별 카운트, MTTR, repeating, RCA 카테고리 | postmortem corpus |
| **ADR** | 신규/Superseded 수, review hit rate, overdue | docs/adr/ frontmatter |
| **FinOps** | 비용 vs 예산, unit economics ($/request, $/MAU) | 클라우드 빌링, FinOps 대시보드 |
| **Business** | MRR Movement, Cohort retention, ARR 추이 | subscription-billing-metrics SQL |
| **Tech debt** | 부채 register 변화 (추가/해소) | engineering-strategy register |
| **People** | 신입 onboarding 일수, 팀 NPS, 퇴사율 | HR + 회고 설문 |

---

## DORA 4 Metrics 산출

### 1. Deployment Frequency

```sql
-- 분기 동안 production deploy 횟수 / 영업일
SELECT DATE_TRUNC('week', deployed_at) AS week,
       COUNT(*) AS deploys,
       COUNT(*) / 5.0 AS deploys_per_workday
FROM deployments
WHERE environment = 'production'
  AND deployed_at >= NOW() - INTERVAL '90 days'
GROUP BY 1
ORDER BY 1;
```

**Elite tier**: 일 1회 이상 / **High**: 주 1회 이상 / **Medium**: 월 1회 이상 / **Low**: 월 1회 미만

### 2. Lead Time for Changes (commit → production)

```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY lead_time_minutes) AS p50_min,
       PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY lead_time_minutes) AS p90_min
FROM (
    SELECT EXTRACT(EPOCH FROM (d.deployed_at - c.committed_at)) / 60 AS lead_time_minutes
    FROM deployments d
    JOIN commits c ON d.commit_sha = c.sha
    WHERE d.environment = 'production'
      AND d.deployed_at >= NOW() - INTERVAL '90 days'
) t;
```

**Elite**: 1시간 미만 / **High**: 1일 미만 / **Medium**: 1주 미만 / **Low**: 1개월 이상

### 3. Change Failure Rate

```
실패한 deploy (rollback / hotfix 트리거) / 전체 deploy
```

```sql
SELECT
    100.0 * SUM(CASE WHEN failed THEN 1 ELSE 0 END) / COUNT(*) AS cfr_pct
FROM deployments
WHERE deployed_at >= NOW() - INTERVAL '90 days';
```

**Elite/High**: 5% 미만 / **Medium**: 10% 미만 / **Low**: 15% 이상

### 4. MTTR (Mean Time to Restore)

```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (
           ORDER BY EXTRACT(EPOCH FROM (resolved_at - detected_at)) / 60
       ) AS p50_minutes
FROM incidents
WHERE detected_at >= NOW() - INTERVAL '90 days'
  AND severity IN ('SEV1', 'SEV2');
```

**Elite**: 1시간 미만 / **High**: 1일 미만 / **Medium**: 1주 미만 / **Low**: 1주 이상

### 분기 추이 비교 (Trend)

```
분기      Deploy/주   Lead time p50   CFR     MTTR
2025 Q4   3.2         2.5h           7.1%    1.8h
2026 Q1   5.8 (+81%)  1.4h (-44%)    4.2%    1.1h   ✅ Tier up: High → Elite
```

---

## SLO 달성률 산출

### 분기 단위 error budget 소진

```promql
# 99.9% SLO, 90일 = 90 * 24 * 60 = 129,600분 → budget 129.6분
# 실제 down time이 budget 안인지

(
  sum_over_time(
    (1 - sli:availability:ratio)[90d:1m]
  )
)
/
(0.001 * 90 * 24 * 60)  # 0.1% of 90일
```

| 서비스 | SLO 목표 | 실측 | Error budget 소진 | Verdict |
|---|---|---|---|---|
| api-gateway | 99.9% | 99.92% | 78% | OK |
| auth | 99.95% | 99.91% | 152% | ❌ Exceeded — 다음 분기 안정화 우선 |
| payment | 99.99% | 99.99% | 24% | OK + 여유 |

Error budget 초과 시 다음 분기 feature 작업 동결 정책 (Google SRE 권장).

---

## 인시던트 패턴 분석

```sql
-- 분기 동안 인시던트 RCA 카테고리 분포
SELECT rca_category, COUNT(*) AS count,
       AVG(EXTRACT(EPOCH FROM (resolved_at - detected_at)) / 60) AS avg_mttr_min,
       SUM(CASE WHEN severity='SEV1' THEN 1 ELSE 0 END) AS sev1_count
FROM incidents
WHERE detected_at >= NOW() - INTERVAL '90 days'
GROUP BY rca_category
ORDER BY count DESC;
```

### 패턴 신호

| 신호 | 임계값 | 행동 |
|---|---|---|
| Same RCA category ≥ 3건 | 시스템적 문제 | 다음 분기 OKR에 reliability 항목 |
| SEV1 ≥ 2건 | 중대 사고 누적 | 임원 보고 + 외부 컨설팅 검토 |
| Repeating incident ≥ 2건 | 근본 원인 미해결 | 해당 카테고리 expert agent 컨설트 |
| MTTR 분기 대비 50% 증가 | 운영 역량 저하 | runbook + on-call 훈련 강화 |
| Action item completion < 70% | postmortem 흐지부지 | tech-lead 에스컬레이션 |

자세한 회고 절차는 `/sre:incident-postmortem` §Action Item 추적 참조.

---

## FinOps 추이 + Unit Economics

```
지표              Q4 2025      Q1 2026      변화
월 클라우드 비용   $48,000      $62,000      +29%
MAU                120K         180K         +50%
$ / MAU            $0.40        $0.34        -15% ✅ 효율성 개선
$ / request        $0.0021      $0.0018      -14% ✅
관측 스택 비용     $4,200       $6,800       +62% ❌ 매출 대비 빠름
DB 비용 비중       38%          41%          +3pp
```

### 회고 알람 룰

- **$ / MAU 증가** → unit economics 악화. 비용 최적화 우선
- **관측 비용 / 매출 ratio > 5%** → cardinality 관리 필요 (`observability/observability-cost.md`)
- **컴포넌트별 비용 비중 5pp 이상 변화** → 원인 추적 (예: DB scale up, egress spike)

자세한 비용 분석은 `/sre:finops-ai`, 관측 비용은 `/observability:observability-cost` 참조.

---

## MRR / Cohort 추이 (B2C/B2B SaaS)

`business/subscription-billing-metrics.md`의 SQL을 분기 단위로 실행:

```sql
-- MRR Movement (분기)
SELECT DATE_TRUNC('quarter', event_date) AS qtr,
       SUM(CASE WHEN movement='new' THEN delta_mrr ELSE 0 END) AS new_mrr,
       SUM(CASE WHEN movement='expansion' THEN delta_mrr ELSE 0 END) AS expansion_mrr,
       SUM(CASE WHEN movement='contraction' THEN delta_mrr ELSE 0 END) AS contraction_mrr,
       SUM(CASE WHEN movement='churn' THEN delta_mrr ELSE 0 END) AS churn_mrr,
       SUM(delta_mrr) AS net_new_mrr
FROM mrr_movements
WHERE event_date >= NOW() - INTERVAL '12 months'
GROUP BY 1
ORDER BY 1;
```

| 지표 | Q1 | Q2 | 추이 |
|---|---|---|---|
| Net new MRR | $12K | $18K | +50% |
| Voluntary churn rate | 3.2% | 2.8% | -0.4pp ✅ |
| Involuntary churn (결제 실패) | 1.8% | 0.9% | -0.9pp ✅ Smart Retries 도입 효과 |
| Expansion MRR | $4K | $9K | +125% ✅ Seat 추가 |
| Cohort 6m retention | 78% | 82% | +4pp |

---

## ADR Hit Rate (decision quality)

`dx/adr-retrospective.md`의 분석 결과를 분기 회고에 통합:

```
이번 분기 ADR 회고 결과:
- 신규 ADR: 12건
- Re-confirmed: 8/10 (80% hit rate, 6개월 review)
- Superseded: 2건 (모두 payment 카테고리 — ⚠️ 반복 패턴)
- Deprecated: 1건
- Overdue review: 3건 (다음 분기 우선)

⚠️ Action: payment 카테고리 ADR 작성 시 RFC 단계 강제 (성급한 결정 차단)
```

---

## 회고 미팅 facilitation (2시간)

### Agenda

```
[10분] Opening + 분기 highlight 1줄
[20분] 데이터 리뷰 (DORA, SLO, 인시던트, FinOps)
[30분] Went well / Didn't go well / Surprises
        - 각자 5분 silent 작성 (Mural/Miro)
        - dot voting (top 5)
[20분] Top 5 항목 deep dive
[30분] Lessons → Action items (다음 분기 OKR 후보)
[10분] Action item 우선순위 + owner 지정 + Closing
```

### 안티패턴 (회고 자체)

| 안티패턴 | 왜 나쁜가 | 대신 |
|---|---|---|
| 데이터 없이 회고 | 인상비평, 큰 목소리만 들림 | W11에 데이터 dump 의무 |
| Blameful 회고 | 침묵, 진실 은폐 | Etsy "Just Culture" 5 questions |
| Action item 없는 회고 | 학습 → 행동 단절 | 미팅 끝에 owner+기한 명시 |
| Action item 70% 미만 완료 | 회고 신뢰도 붕괴 | 다음 분기 OKR로 승격 |
| 동일 안건 반복 등장 | 시스템적 문제 무시 | 3분기 연속 등장 시 임원 보고 |
| Squad-level과 Eng-level 같이 진행 | 디테일 묻힘 | 별도 미팅, 데이터만 공유 |
| 4시간+ 미팅 | 집중력 붕괴 | 2시간 시간박스, 데이터는 비동기로 |
| 회고록 내부 비공개 | 조직 학습 부재 | 1주 안에 회사 전체 공유 (민감 정보 redact) |

---

## 한국 시장 분기 회고 특수성

### 회계연도 + 트래픽 패턴

| 시기 | 한국 특수 이벤트 | 회고에 반영할 점 |
|---|---|---|
| **Q1 (1-3월)** | 명절(설), 신년 결산 압박, 카드사 캐시백 | 결제 트래픽 spike, PG 수수료 정산 |
| **Q2 (4-6월)** | 개강, 청년도약계좌, 부동산 청약 | 인증 트래픽, KCB/NICE 비용 |
| **Q3 (7-9월)** | 휴가철, 추석, 정기인사 | on-call 인계, 핵심 엔지니어 부재 리스크 |
| **Q4 (10-12월)** | 수능, 블랙프라이데이, 연말 결산 | 트래픽 peak, 망내 latency, 망사용료 정산 |

### 한국 결산 압박

- 연결 결산 (1월 첫 주) — Q4 인시던트가 매출에 미친 영향 즉시 산출 의무
- 분기 단위 PG 수수료 정산, NTS(국세청) 신고 자료 — `business/subscription-billing-metrics.md` SQL 결과 export
- PIPA / 위치정보법 24h 신고 — 분기 회고에 "신고 case" 별도 섹션

### 한국 특수 메트릭

```
지표                          글로벌    한국 추가
PG 수수료 (% of GMV)          —         3.0~3.5% 추적 의무
망내 vs 망외 latency p95      —         네이버/KT 망내 < 50ms 검증
PIPA 24h 신고 발생            —         분기 신고 case 0 목표
KCB/NICE 본인인증 비용         —         건당 50~150원, MAU 비례
```

---

## 보고서 템플릿 (1 페이지)

```markdown
# 2026 Q1 Engineering Quarterly Review

## TL;DR
- ✅ DORA: High → Elite (Deploy 5.8/주, Lead 1.4h, CFR 4.2%)
- ⚠️ SLO: auth 서비스 error budget 152% 초과 — Q2 안정화 우선
- ✅ MRR Net new $18K (+50% QoQ), Involuntary churn -0.9pp
- ❌ Payment 카테고리 ADR 2건 Supersede — 반복 패턴, RFC 강제
- ✅ $ / MAU $0.34 (-15%) — 효율성 개선
- ⚠️ 관측 스택 비용 +62% — cardinality 관리 필요

## DORA Metrics (Q4 → Q1)
[테이블]

## SLO 달성률
[테이블]

## 인시던트 (총 N건, SEV1 N건, MTTR p50)
[카테고리별 차트]

## FinOps + Business
[비용/매출/Unit economics 추이]

## ADR Hit Rate
[decision metrics]

## Top 5 Lessons → Action Items (Q2 OKR 후보)
1. ... (owner: @x, 기한: ...)
```

---

## 분기 회고 → 다음 분기 OKR 인계

회고 결과 중 **Top 3 lessons는 다음 분기 OKR로 승격**한다. 흐름:

```
Q1 회고 (W12)
   │
   ▼
Top 3 lessons (예: payment ADR 반복, auth SLO 초과, 관측 비용 폭증)
   │
   ▼
Q2 OKR 후보로 변환 (engineering-strategy.md §OKR)
   │
   ▼
Now / Next / Later 재배치 (engineering-strategy.md)
   │
   ▼
Q2 W1 OKR commit
```

전환 가이드는 [`dx/engineering-strategy.md`](../engineering-strategy/SKILL.md) §Engineering OKR 참조.

---

## Quick Start (W11 데이터 수집 1시간)

```
1. CI/CD logs export → DORA 4 metrics SQL 실행
2. Prometheus → SLO 달성률 (분기 단위 burn rate)
3. Postmortem corpus → 카테고리/severity 카운트
4. ADR 디렉토리 → status별 count, hit rate, overdue
5. 클라우드 빌링 → 분기 비용, $/MAU 계산
6. subscription-billing-metrics SQL → MRR Movement, Cohort
7. 결과를 1-page 보고서 템플릿에 채움
8. 회고 미팅 1주 전 비동기 공유 (사전 검토)
```

---

## 다음 단계 (After Adoption)

- 메트릭 자동화: `scripts/quarterly-metrics.sh` (DORA + SLO + 인시던트 + ADR + FinOps export)
- 분기 보고서를 `docs/retrospective/YYYY-QN-engineering.md`에 정식 기록
- ADR retrospective와 분기 회고를 같은 사이클에 묶기 (W11에 동시 진행)
- 임원/board에 분기 보고 packet 표준화 (1-page + appendix)
- Mid-quarter (W6) 미니 회고 — course correction
- 연간 회고 (Q4 → 다음 해 Q1) — 4분기 누적 트렌드 분석

---

## 관련 자원

- Google SRE Workbook §SLO Engineering — error budget 정책
- DORA "State of DevOps" 보고서 — 4 metrics 정의 + tier 기준
- ThoughtWorks "Build Quality In" — 분기 단위 quality 회고
- Atlassian "Team playbook — Health monitor" — 정기 self-check
- Spotify "Squad health check" model — 5 axis 정성 평가
