---
name: adr-retrospective
description: "Accepted ADR 사후 검토 — 6/12개월 재평가 트리거, 예측 vs 실측 비교, Superseded·Deprecated 판단, decision log 누적 분석. Use when 이미 채택한 ADR이 지금도 옳은지 재평가하거나 결정 회고를 할 때."
license: MIT
---

# ADR Retrospective — 결정 사후 검토

ADR을 **언제·어떻게 다시 검토할지** 표준화한다. 작성 흐름은 `dx/rfc-adr.md`가 cover. 이 skill은 Accepted ADR의 **수명 관리** + **누적 패턴 분석** + **Superseded 트리거**에 집중한다.

> 핵심 질문: "이 결정이 6개월 후에도 옳은가?" "이 결정의 비용이 예측 범위 안인가?" "같은 카테고리에서 같은 실수를 반복하는가?"

## When to Use

- Accepted ADR의 6개월/12개월 정기 재평가
- 인시던트·SEV1 사고가 ADR 결정과 연관됐을 때 즉시 재평가
- Provider 약관/가격 변경, 새 기술 GA 등 외부 변동 시
- ADR을 Superseded 처리할지 결정해야 할 때
- 분기/연간 회고에서 decision log 누적 분석
- 기술 부채 레지스터에 "예전 ADR" 항목이 누적될 때
- Tech Radar 재배치 (Adopt → Hold) 시 관련 ADR 추적
- 회사 전체 architecture review (외부 컨설팅, 인수합병 due diligence)

**관련 skill (cross-link)**:
- `dx/rfc-adr.md` — ADR/RFC 작성 워크플로우 (Proposed → Accepted)
- `dx/engineering-strategy.md` — Tech Radar, Build vs Buy, 부채 레지스터
- `operations/incident-postmortem.md` — 인시던트 → ADR 재평가 트리거
- `dx/spec-driven-development.md` — 스펙 변경이 ADR 가정을 깨뜨릴 때
- `dx/quarterly-review.md` — 분기 회고에서 decision metrics 활용

---

## 재평가 트리거 결정 트리

```
재평가 시작 트리거?
    │
    ├─ 시간 기반 (정기) ──────────> Lifecycle review
    │       │
    │       ├─ 6개월: Tier-1 (인프라/DB/Auth/결제)
    │       │   - 가정 변경 여부, 가격, 약관, 대안 모니터링
    │       │
    │       └─ 12개월: Tier-2 (라이브러리/툴체인/내부 패턴)
    │           - 채택률, 학습 곡선, deprecation 신호
    │
    ├─ 이벤트 기반 (트리거) ──────> Event review
    │       │
    │       ├─ SEV1/SEV2 인시던트가 ADR 결정과 연관됨
    │       ├─ Provider 가격 30% 이상 변동 또는 약관 변경
    │       ├─ 새 ADR이 기존 ADR과 충돌 가능성
    │       ├─ 트래픽/사용자 10배 이상 증가 (가정 깨짐)
    │       └─ 새 기술이 Tech Radar Adopt 진입
    │
    ├─ 패턴 기반 (회고) ──────────> Decision log analysis
    │       │
    │       ├─ Same-category supersede ≥ 2 (반복 실수)
    │       ├─ Avg lifespan < 6개월 (성급한 결정)
    │       └─ Hit rate < 60% (예측 실패율 높음)
    │
    └─ 조직 변경 ─────────────────> Strategic review
            │
            ├─ 인수합병 due diligence
            ├─ 핵심 엔지니어 퇴사 (decision context 유실)
            └─ 외부 컨설팅 architecture review
```

---

## 사후 검토 매트릭스 (Tier × Trigger)

| Tier | 정기 주기 | 이벤트 트리거 | 검토 주체 | 결과물 |
|---|---|---|---|---|
| **Tier 1** (인프라/DB/Auth/PG) | 6개월 | SEV1, 가격 30%+ 변동 | tech-lead + 도메인 owner | New ADR 또는 Deprecation note |
| **Tier 2** (프레임워크/라이브러리) | 12개월 | 새 major version, deprecated | 도메인 owner | Tech Radar 재배치 |
| **Tier 3** (내부 패턴/컨벤션) | ad-hoc | 대규모 리팩토링 시 | 작성자 + 영향받는 팀 | Rule 또는 Skill 갱신 |

---

## 6단계 재평가 워크플로우

```
1. Trigger 감지 → 2. 컨텍스트 재구성 → 3. 가정 검증
                                            │
                                            ▼
6. 결과 기록 ← 5. 결정 (Accept/Supersede/Deprecate) ← 4. 트레이드오프 실측
```

### 1. Trigger 감지

각 Tier별 reminder 자동화 (예시):

```bash
# 6개월 지난 Tier-1 ADR 자동 알림 (cron)
find docs/adr -name "*.md" -mtime +180 \
    | xargs grep -l "Tier: 1" \
    | xargs -I{} echo "::review-due:: {}"
```

또는 ADR frontmatter에 `review_due: 2026-09-01` 필드 추가.

### 2. 컨텍스트 재구성

원본 ADR을 다시 읽되 **현재 시점 가정**으로 비교한다:

| 항목 | 결정 시점 | 현재 시점 | 변화 |
|---|---|---|---|
| 트래픽 | 10K MAU | 1M MAU | 100x |
| 팀 크기 | 5명 | 25명 | 5x |
| Provider 가격 | $0.05/req | $0.07/req | +40% |
| 대안 (B) 성숙도 | Beta | GA + 채택 사례 | Adopt |

### 3. 가정 검증 (예측 vs 실측)

ADR 작성 시 명시한 **Predicted outcomes**가 있으면 실측과 비교. 없으면 이번 회고에서 retrospective metric을 정의:

```yaml
# ADR-0042 sample retrospective metrics
predicted:
  cost_monthly_max: $500
  p95_latency_max: 200ms
  team_onboarding_days: 3
actual_after_6m:
  cost_monthly: $1,200      # 2.4x — 가정 깨짐
  p95_latency: 180ms        # OK
  team_onboarding_days: 7   # 2.3x — 가정 깨짐
verdict: Reconsider — cost가 예측 2x 초과
```

### 4. 트레이드오프 실측

원본 ADR의 "Cons" / "Risks" 섹션을 실제 발생 여부로 표시:

| 원본 Risk | 실제 발생? | 영향도 | 비고 |
|---|---|---|---|
| Vendor lock-in | ✅ | 높음 | Provider 약관 변경 시 협상력 없음 |
| 학습 곡선 | ⚠️ 부분 | 중간 | 신입 onboarding 7일 (예측 3일) |
| 가격 상승 | ✅ | 높음 | 6개월 만에 +40% |
| 운영 복잡도 | ❌ | — | 자동화로 흡수됨 |

### 5. 결정: Accept / Supersede / Deprecate

```
결정 매트릭스:

         가정 변경 적음     가정 변경 큼
실측 OK     Accept              Adjust (보충 ADR)
실측 NG     Supersede           Replace + Migration
```

- **Accept (Re-confirmed)**: 원본 ADR 유효, `last_reviewed: YYYY-MM-DD` 추가
- **Adjust**: 보충 ADR로 가정 갱신 (예: ADR-0042-amendment.md)
- **Supersede**: 새 ADR 작성, 원본 상태 `Superseded by ADR-NNNN`로 이동
- **Deprecate**: 원본 결정 무효화, 대체 결정 없음 (단순 제거)
- **Replace + Migration**: 새 ADR + `docs/migration/NNNN-...md`

### 6. 결과 기록

원본 ADR 끝에 **Review history** 섹션 추가 (Accepted ADR도 review log는 append 가능):

```markdown
## Review History

### 2026-04-15 — 6-month review
- **Trigger**: Lifecycle (Tier-1)
- **Verdict**: Adjust
- **Findings**: 비용 예측 $500 vs 실측 $1,200 (2.4x). 트래픽 100x로 가정 깨짐.
- **Action**: ADR-0042-amendment.md 작성, FinOps tagging 강화
- **Reviewer**: @tech-lead, @platform-team
```

---

## Decision Log 누적 분석

ADR을 단일 파일이 아닌 **데이터셋**으로 보고 패턴을 찾는다.

### 메타데이터 추출 (모든 ADR frontmatter 필요)

```yaml
# docs/adr/0042-stripe-vs-toss.md
---
id: 0042
title: "Stripe vs TossPayments 선택"
date: 2026-01-15
tier: 1
category: payment
status: Accepted
review_due: 2026-07-15
predicted_lifespan_months: 24
superseded_by: null
last_reviewed: null
---
```

### 분석 쿼리 예시

**1. Same-category supersede frequency** (반복 실수 감지):
```bash
# payment 카테고리에서 6개월 안에 supersede된 ADR
grep -l "category: payment" docs/adr/*.md \
    | xargs grep -lE "superseded_by: ADR" \
    | xargs grep -B2 "date:" \
    | awk '/date:/{...}'  # 의사코드
```

**2. Hit rate** (예측 적중률):
```sql
-- review log를 DB로 export 시
SELECT category, COUNT(*) AS total,
       SUM(CASE WHEN verdict='Accept' THEN 1 ELSE 0 END) AS hits,
       ROUND(100.0 * SUM(CASE WHEN verdict='Accept' THEN 1 ELSE 0 END) / COUNT(*), 1) AS hit_rate_pct
FROM adr_reviews
WHERE reviewed_at >= NOW() - INTERVAL '12 months'
GROUP BY category
ORDER BY hit_rate_pct ASC;
```

**3. Avg lifespan** (성급한 결정 감지):
```sql
SELECT category,
       AVG(EXTRACT(EPOCH FROM (superseded_at - decided_at)) / 86400) AS avg_lifespan_days
FROM adr
WHERE status = 'Superseded'
GROUP BY category
HAVING AVG(...) < 180;  -- 6개월 미만 supersede 빈번한 카테고리
```

### 회고 알람 룰

| 신호 | 임계값 | 행동 |
|---|---|---|
| Hit rate | < 60% / 12개월 | 카테고리별 ADR 작성 가이드 보강 |
| Avg lifespan (Tier-1) | < 9개월 | RFC 단계 강제 (성급한 결정 차단) |
| Same-category supersede | ≥ 2 / 12개월 | 도메인 expert agent 컨설트 의무화 |
| Review overdue | > 30일 | tech-lead 에스컬레이션 |

---

## Superseded vs Deprecated 결정 흐름

```
Accepted ADR을 무효화해야 한다.
    │
    ├─ 대체 결정 있음? ──Yes─> Supersede + 새 ADR 작성
    │   │                       └─ 원본: status=Superseded by ADR-NNNN
    │   │                       └─ 새: 원본을 "Replaces ADR-MMMM"로 명시
    │   │
    │   └─No─> Deprecate (대체 없음)
    │           └─ 원본: status=Deprecated, reason 명시
    │           └─ 마이그레이션 필요 시 docs/migration 별도 작성
    │
    └─ 마이그레이션 영향 큰가?
        └─Yes─> Migration plan 필수 (docs/migration/NNNN-...md)
                downtime, rollback, data migration 명시
```

**Accepted ADR은 immutable** — 본문 수정 금지. Review history 섹션 append만 허용.
Superseded 처리도 status 필드만 변경, 본문은 유지 (역사적 기록).

---

## 한국 시장 결정의 특수 재평가

한국 PG/Auth/PIPA 결정은 **외부 변수가 빠르게 움직여서** 6개월 미만 재평가 필요.

| 결정 카테고리 | 재평가 트리거 (한국 특화) |
|---|---|
| **PG (TossPayments/PortOne/KG이니시스)** | 약관 변경, 수수료 조정, 정기결제 빌링키 정책, PG 라이센스 박탈 사고 |
| **본인인증** | 통신사 정책 변경, NICE/KCB 가격, 통신사 독과점 행정처분 |
| **PIPA/위치정보법** | 법 개정 (2026-07 이미지 차단 의무 등), 개보위 가이드라인 업데이트 |
| **Cloud (네이버/KT)** | 망내 latency 변화, 망사용료 분쟁, 정부망 접속 의무 |
| **카카오/네이버 OAuth** | 정책 변경, 친구목록 권한 축소, B2B 라이선스 가격 |

> 한국 결정은 **frontmatter `review_due`를 글로벌 결정의 절반(3개월)으로** 설정 권장.

자세한 법령 추적은 `/security:kr-location-info-act`, `/security:data-subject-rights` 참조.

---

## ADR 본문 추가 섹션 (Retrospective-ready ADR)

기존 ADR 템플릿(`dx/documentation-templates.md` ADR section)에 다음을 추가하면 사후 검토가 쉬워진다:

```markdown
## Predicted Outcomes

향후 6/12개월 후 검증할 예측 (정량):

| 지표 | 6개월 목표 | 12개월 목표 | 측정 방법 |
|---|---|---|---|
| 월 비용 | < $500 | < $700 | FinOps 대시보드 |
| p95 latency | < 200ms | < 180ms | Grafana SLO |
| 팀 onboarding | < 3일 | < 2일 | 신입 회고 설문 |

## Review Schedule

- **Tier**: 1
- **Next review**: 2026-07-15 (6개월)
- **Reviewer**: @tech-lead, @payment-owner
- **Auto-trigger**: SEV1, 비용 30% 초과, Provider 약관 변경
```

이 섹션이 있어야 사후 검토에서 "예측 vs 실측" 비교가 가능하다. 없으면 retrospective는 인상비평으로 끝남.

---

## 안티패턴

| 안티패턴 | 왜 나쁜가 | 대신 |
|---|---|---|
| Accepted ADR 본문 직접 수정 | 결정의 역사적 기록 파괴, audit 불가 | 새 ADR(Supersede) 또는 Review history append |
| 재평가 일정 없는 ADR | "쓰고 잊는" 결정 — 부채 누적 | frontmatter `review_due` 필수 |
| Predicted outcomes 없는 ADR | 사후 검증 불가, 인상비평 회고 | 정량 목표 3개 이상 명시 |
| Same-category supersede 무시 | 같은 실수 반복 | 알람 룰에 카운터 |
| 인시던트 후 ADR 재평가 안 함 | 사고-결정 연결 끊김 | 인시던트 RCA에 "관련 ADR" 필드 의무 |
| 모든 ADR을 같은 주기로 검토 | Tier-1과 Tier-3에 같은 비용 | Tier별 차등 |
| Decision log를 git commit history로만 추적 | 카테고리/Tier 분류 불가 | frontmatter 메타데이터 + 별도 export |
| Superseded 시 마이그레이션 무시 | 코드는 옛 결정 따라감 | docs/migration 의무 |
| 외부 변수 (가격/약관) 모니터링 안 함 | 트리거 놓침 | Provider별 Slack 알림 채널 |
| 회고 결과 공유 안 함 | 조직 학습 부재 | engineering all-hands 또는 RFC 형태 공유 |
| 한국 결정에 글로벌 주기 적용 | 외부 변동 빠름 | review_due를 절반으로 |
| Hit rate를 사람 평가에 사용 | 보수적 결정 유발 | 시스템 지표로만, 개인 평가 X |

---

## ADR 작성 가이드 보강 (rfc-adr.md 연계)

`dx/rfc-adr.md` ADR 템플릿에 retrospective-ready 섹션 추가 권장. 다음 PR에서 다음 항목을 반영:

1. frontmatter에 `tier`, `review_due`, `predicted_lifespan_months` 필드
2. "Predicted Outcomes" 섹션 의무화
3. "Review Schedule" 섹션 의무화
4. Accepted 후 본문 수정 금지 규칙 명시
5. Review history append 형식 표준화

---

## Quick Start (10분 안에 ADR 회고 1건)

```
1. 6개월 이상 된 Tier-1 ADR 1개 선택
2. ADR을 다시 읽고, 결정 시점 가정을 표로 작성
3. 현재 시점 가정과 비교 (트래픽/비용/팀 크기/Provider 변동)
4. 원본 Risks 섹션을 "실제 발생 여부"로 채점
5. 결정: Accept / Adjust / Supersede / Deprecate
6. ADR에 Review history 섹션 append, status 필드 갱신
7. 결정이 Supersede면 새 ADR 작성, Migration 영향 평가
```

---

## 다음 단계 (After Adoption)

- 분기 회고에 "decision metrics" 섹션 추가 (`dx/quarterly-review.md` 참조)
- ADR frontmatter에 메타데이터 자동 추출 스크립트 (`scripts/adr-stats.sh`)
- Decision log를 `docs/adr/index.md`에 자동 생성 (table 형식, status별 그룹)
- Tech Radar (`dx/engineering-strategy.md`)와 ADR 간 양방향 링크
- 인시던트 포스트모템 (`operations/incident-postmortem.md`)에 "관련 ADR" 필드 의무화

---

## 관련 자원

- Michael Nygard, "Documenting Architecture Decisions" (2011) — ADR 원조
- ThoughtWorks Technology Radar — 분기별 기술 평가 리듬
- AWS Builders' Library, "Architectural patterns" — 결정 lifecycle
- log4brains — ADR 정적 사이트 생성기 (rfc-adr.md 참조)
- Spotify "Squad health check" — 정기 self-assessment 리듬
