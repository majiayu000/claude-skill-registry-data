---
name: product-thinking
description: "프로덕트 사고 프레임워크 — RICE 스코어링, MoSCoW, Shape Up, JTBD, Story Mapping, MVP 정의, A/B 테스트 기초. Use when 기능 우선순위를 정하거나 MVP 범위·로드맵을 결정할 때."
---

# Product Thinking 가이드

RICE, MoSCoW, Shape Up, JTBD, Story Mapping 기반 프로덕트 사고

## Quick Reference (결정 트리)

```
우선순위 결정 방법?
    │
    ├─ 정량적 비교 필요 ──────> RICE Scoring
    │       │
    │       └─ Score = (Reach × Impact × Confidence) ÷ Effort
    │
    ├─ 빠른 분류 필요 ────────> MoSCoW
    │       │
    │       └─ Must / Should / Could / Won't
    │
    ├─ 프로젝트 사이클 관리 ──> Shape Up
    │       │
    │       └─ Shaping → Betting → Building → Cooldown
    │
    ├─ 사용자 근본 니즈 ──────> JTBD (Jobs To Be Done)
    │       │
    │       └─ When [situation], I want to [motivation], so I can [outcome]
    │
    └─ 릴리스 범위 정의 ──────> Story Mapping
            │
            └─ Backbone → Walking Skeleton → Release Slices
```

---

## RICE Scoring

### 공식

```
RICE Score = (Reach × Impact × Confidence) ÷ Effort
```

### 각 항목 정의

| 항목 | 정의 | 단위 | 예시 |
|------|------|------|------|
| **Reach** | 분기당 영향받는 사용자/이벤트 수 | 명/건 | 10,000명/분기 |
| **Impact** | 개인당 영향도 | 스케일 | 3 = massive |
| **Confidence** | 추정 신뢰도 | 퍼센트 | 80% = high |
| **Effort** | 소요 공수 | person-months | 2 person-months |

### Impact 스케일

```
3.0  Massive    — 전환율/만족도 대폭 향상
2.0  High       — 상당한 개선
1.0  Medium     — 눈에 띄는 개선
0.5  Low        — 미미한 개선
0.25 Minimal    — 거의 변화 없음
```

### Confidence 기준

| 수준 | 퍼센트 | 근거 |
|------|--------|------|
| High | 100% | 데이터 기반 추정, A/B 테스트 결과 있음 |
| Medium | 80% | 유사 사례 참고, 정성 리서치 기반 |
| Low | 50% | 직감, 데이터 부족, 불확실성 높음 |

### RICE 실전 예시

```
┌────────────────────────┬───────┬────────┬──────┬────────┬───────┐
│ Feature                │ Reach │ Impact │ Conf │ Effort │ RICE  │
├────────────────────────┼───────┼────────┼──────┼────────┼───────┤
│ 검색 자동완성          │ 8,000 │ 2.0    │ 80%  │ 3      │ 4,267 │
│ 결제 수단 추가 (카카오)│ 5,000 │ 3.0    │ 100% │ 2      │ 7,500 │
│ 다크 모드              │ 3,000 │ 0.5    │ 80%  │ 1      │ 1,200 │
│ 추천 알고리즘 개선     │ 10,000│ 2.0    │ 50%  │ 5      │ 2,000 │
│ 관리자 대시보드 개편   │ 200   │ 3.0    │ 80%  │ 4      │   120 │
└────────────────────────┴───────┴────────┴──────┴────────┴───────┘

우선순위: 결제 수단 > 검색 자동완성 > 추천 알고리즘 > 다크 모드 > 대시보드
```

### RICE 사용 시 주의사항

```
RICE는 의사결정 "보조" 도구이지, 유일한 기준이 아니다

추가 고려 사항:
  - 전략적 정렬: OKR/비전과 일치하는가?
  - 의존성: 다른 피처의 선행 조건인가?
  - 기술 부채: 지금 안 하면 나중에 비용이 더 커지는가?
  - 시장 타이밍: 경쟁사 대응이 급한가?

Score가 낮아도 전략적 이유로 우선할 수 있다
Score가 높아도 전략에 안 맞으면 보류할 수 있다
```

---

## MoSCoW 프레임워크

### 4가지 분류

| 분류 | 정의 | 비율 가이드 |
|------|------|------------|
| **Must Have** | 없으면 릴리스 불가, 법적/비즈니스 필수 | 60% 이하 |
| **Should Have** | 중요하지만 우회 방법 존재 | 20% |
| **Could Have** | 있으면 좋지만 없어도 무방 | 20% |
| **Won't Have** | 이번에는 하지 않음 (미래 고려) | 명시적 기록 |

### 적용 방법

```
MoSCoW 분류 프로세스:

1. 전체 요구사항 나열
2. 각 항목에 대해 질문:
   "이것 없이 릴리스할 수 있는가?"
   ├─ No  → Must Have
   └─ Yes → "이것이 없으면 사용자 불만이 큰가?"
            ├─ Yes → Should Have
            └─ No  → "리소스가 남으면 하고 싶은가?"
                     ├─ Yes → Could Have
                     └─ No  → Won't Have

3. Must Have가 60%를 초과하면 재분류
   - "정말 필수인가?" 재검토
   - Must → Should 강등 후보 식별
```

### MoSCoW 실전 예시

```markdown
## Release 2.0 MoSCoW

### Must Have (55%)
- [ ] 소셜 로그인 (카카오, 네이버)
- [ ] 결제 프로세스 리뉴얼
- [ ] 개인정보 처리방침 업데이트 (법적 요건)

### Should Have (25%)
- [ ] 주문 내역 필터링/검색
- [ ] 푸시 알림 설정 세분화
- [ ] 배송 추적 실시간 업데이트

### Could Have (15%)
- [ ] 다크 모드
- [ ] 위시리스트 공유 기능

### Won't Have (this release)
- [ ] AI 챗봇 상담 — 다음 분기 검토
- [ ] 다국어 지원 — Q3 로드맵
```

---

## Shape Up (Basecamp)

### 전체 사이클

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐
│   Shaping    │─>│   Betting    │─>│  Building    │─>│ Cooldown │
│   (2주)      │  │   Table      │  │  (6주)       │  │ (2주)    │
│              │  │   (1일)      │  │              │  │          │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────┘
      │                 │                 │               │
      ▼                 ▼                 ▼               ▼
  문제 정의         프로젝트 선정      팀 자율 구현     버그 수정
  솔루션 스케치     Appetite 확인     Hill Chart 추적   기술 부채
  Breadboard       선택/탈락 결정    Circuit Breaker   탐색/학습
```

### 핵심 개념

**Appetite (식욕)**

```
Appetite = 이 문제에 "투자할 의향이 있는 시간"

Small Batch:  2주 (1~2명)
Big Batch:    6주 (2~3명)

Appetite ≠ Estimate
  Estimate: "이 기능은 4주 걸립니다" (바텀업)
  Appetite: "이 문제에 6주까지 투자합니다" (탑다운)

Appetite가 Scope를 결정한다:
  - 6주 안에 들어가도록 Scope 조정
  - 안 들어가면 Scope 축소 또는 포기
```

**Breadboarding**

```
핵심 흐름만 표현하는 저충실도 설계:

장소(Place)          어포던스(Affordance)     연결(Connection)
──────────          ──────────────          ────────────
[주문 페이지]        (수량 선택)              → [장바구니]
                    (배송지 입력)
[장바구니]           (쿠폰 적용)              → [결제 페이지]
                    (주문하기 버튼)
[결제 페이지]        (결제 수단 선택)          → [주문 완료]
                    (결제하기 버튼)

UI 디자인이 아닌 워크플로우에 집중
```

**Betting Table**

```
참석자: CEO, CTO, Product Lead, Design Lead

안건: Shaped된 Pitch들을 검토
  Pitch 1: 검색 개선 (6주 appetite)  → 채택
  Pitch 2: 알림 시스템 (6주 appetite) → 채택
  Pitch 3: 관리자 도구 (2주 appetite) → 채택
  Pitch 4: 추천 엔진 (6주 appetite)  → 탈락 (다음 사이클)

원칙:
  - 미완성 프로젝트 자동 연장 없음 (Circuit Breaker)
  - 매 사이클 fresh start
  - "아니오"도 건강한 결정
```

**Hill Chart**

```
진행 상황을 "언덕" 메타포로 추적:

        /\
       /  \
      /    \
     /      \
    /        \
───/──────────\───
  Uphill      Downhill
  (불확실성    (실행,
   해소 중)    확신 있음)

  ● 결제 리뉴얼        → Downhill 80% (거의 완료)
  ● 검색 자동완성      → Uphill 60% (기술 조사 중)
  ● 알림 시스템        → Uphill 30% (시작 단계)
```

**Circuit Breaker**

```
6주 타임박스 내 완료 못 하면:
  - 자동 연장 없음
  - 프로젝트 중단
  - 다음 Betting Table에서 재평가

이유:
  - 끝없는 프로젝트 방지
  - Shaping이 부족했음을 의미
  - 재-Shape 후 다시 Pitch 가능
```

---

## JTBD (Jobs To Be Done)

### Job Statement 구조

```
When [상황/트리거],
I want to [동기/행동],
so I can [기대 결과/가치].
```

### 3가지 Job 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **Functional** | 실용적 과업 달성 | "파일을 빠르게 공유하고 싶다" |
| **Emotional** | 감정적 충족 | "전문적으로 보이고 싶다" |
| **Social** | 사회적 인식 | "팀에서 신뢰받고 싶다" |

### JTBD 실전 예시

```markdown
## 전자상거래 — 주요 Jobs

### Job 1: 빠른 재구매
When 자주 사는 상품이 떨어졌을 때,
I want to 이전 주문을 빠르게 반복하고 싶다,
so I can 시간 낭비 없이 필요한 것을 받을 수 있다.

→ Feature: 원클릭 재주문, 정기 배송

### Job 2: 선물 고르기
When 친구 생일이 다가올 때,
I want to 상대방 취향에 맞는 선물을 고르고 싶다,
so I can 센스 있는 사람이라는 인상을 줄 수 있다. (Emotional + Social)

→ Feature: 선물 추천, 선물 포장 옵션, 메시지 카드

### Job 3: 가격 비교
When 고가 상품을 구매하려 할 때,
I want to 여러 판매자의 가격을 비교하고 싶다,
so I can 합리적인 가격에 구매할 수 있다.

→ Feature: 가격 비교, 가격 알림, 최저가 히스토리
```

### JTBD 인터뷰 가이드

```
Switch Interview (전환 인터뷰):
  "이전에 어떤 솔루션을 사용했나요?"
  "왜 바꾸게 되었나요?"
  "바꾸기 전 고민은 무엇이었나요?"
  "바꾼 후 기대와 다른 점은?"

4 Forces Framework:
  Push: 현재 솔루션의 불만 (전환 촉진)
  Pull: 새 솔루션의 매력 (전환 촉진)
  Habit: 현재 솔루션 관성 (전환 저항)
  Anxiety: 새 솔루션 불안 (전환 저항)

  전환 = (Push + Pull) > (Habit + Anxiety)
```

---

## Story Mapping (Jeff Patton)

### 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    User Activity (활동)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 상품 검색 │  │ 장바구니  │  │ 결제     │  │ 배송 확인 │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│       │              │             │              │          │
│  ─────┼──────────────┼─────────────┼──────────────┼───── ← Backbone
│       │              │             │              │          │
│  ┌────┴────┐   ┌─────┴────┐  ┌────┴────┐   ┌────┴────┐    │
│  │키워드   │   │상품 추가 │  │결제수단 │   │주문상태 │    │  Release 1
│  │검색     │   │          │  │선택     │   │조회     │    │  (Walking
│  ├─────────┤   ├──────────┤  ├─────────┤   ├─────────┤    │  Skeleton)
│  │카테고리 │   │수량 변경 │  │쿠폰    │   │배송추적 │    │  ──────
│  │필터     │   │          │  │적용     │   │         │    │  Release 2
│  ├─────────┤   ├──────────┤  ├─────────┤   ├─────────┤    │  ──────
│  │자동완성 │   │위시리스트│  │할부선택 │   │배송알림 │    │  Release 3
│  │         │   │이동      │  │         │   │         │    │
│  └─────────┘   └──────────┘  └─────────┘   └─────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 개념

**Backbone (등뼈)**
- 사용자 활동의 큰 흐름을 좌→우로 배열
- 시간 순서 또는 사용 빈도 기준

**Walking Skeleton (걸어다니는 뼈대)**
- 전체 흐름을 end-to-end로 관통하는 최소 기능 세트
- Release 1 = Walking Skeleton

**Release Slices (릴리스 슬라이스)**
- Backbone 아래 세로로 스토리 배열 (우선순위 높→낮)
- 수평 라인으로 릴리스 경계 표시

### Story Mapping 워크숍 진행법

```
준비 (30분 전):
  - 큰 벽면 또는 디지털 보드 (Miro, FigJam)
  - 포스트잇 3색: 활동(파랑), 스토리(노랑), 릴리스(빨강)

진행:
  1. Backbone 구축 (30분)
     - "사용자가 처음부터 끝까지 무엇을 하는가?"
     - 큰 활동을 좌→우 순서로 배치

  2. 스토리 채우기 (60분)
     - 각 활동 아래 구체적 스토리 나열
     - 우선순위 높은 것을 위로

  3. 릴리스 슬라이싱 (30분)
     - Walking Skeleton 라인 긋기
     - Release 2, 3 경계 설정
     - "이 릴리스로 무엇을 검증하는가?" 정의
```

---

## MVP 정의 프로토콜

### MVP 범위 결정

```
MVP ≠ 미완성 제품
MVP = 가설을 검증할 수 있는 최소 완성 제품

Step 1: 핵심 가설 정의
  "사용자는 [X] 기능이 있으면 [Y] 행동을 할 것이다"

Step 2: 검증에 필요한 최소 기능 식별
  - JTBD에서 가장 중요한 Functional Job 1~2개
  - Story Map에서 Walking Skeleton

Step 3: 성공 기준 정의 (출시 전)
  - 활성 사용자 수: N명
  - 핵심 전환율: X%
  - NPS: Y점 이상

Step 4: 타임박스 설정
  - MVP는 최대 6~8주 이내 출시
  - 넘으면 Scope 재조정
```

### MVP 체크리스트

```markdown
- [ ] 핵심 가설이 1문장으로 정의되어 있는가
- [ ] 검증 기준(성공/실패)이 수치로 정의되어 있는가
- [ ] Must Have가 5개 이하인가
- [ ] 8주 이내 출시 가능한가
- [ ] Walking Skeleton이 end-to-end를 커버하는가
- [ ] 수동 운영(Wizard of Oz)으로 대체 가능한 것은 자동화하지 않았는가
```

---

## A/B Testing 기초

### 실험 설계

```
가설: [변경]하면 [메트릭]이 [X%] 개선될 것이다

예시:
  가설: 결제 페이지 CTA 버튼을 녹색으로 변경하면
        결제 전환율이 5% 향상될 것이다

  Control (A): 현재 파란 버튼
  Variant (B): 녹색 버튼

  Primary Metric: 결제 전환율
  Guardrail Metric: 반품률 (악화되지 않아야 함)

  Sample Size: 통계적 유의성 도달에 필요한 트래픽
  Duration: 최소 1~2주 (주중/주말 패턴 포함)
```

### 의사결정 기준

| 결과 | 액션 |
|------|------|
| Primary 개선 + Guardrail 유지 | Ship (배포) |
| Primary 개선 + Guardrail 악화 | 추가 분석 필요 |
| Primary 변화 없음 | 실험 종료, 학습 기록 |
| Primary 악화 | 실험 종료, 원인 분석 |

---

## Anti-Patterns

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| RICE 점수만으로 결정 | 전략적 맥락 무시 | RICE + 전략 정렬 + 의존성 종합 |
| MVP에 Must Have 과다 | 출시 지연, MVP가 V1이 됨 | Must Have 5개 이하 제한 |
| MoSCoW 전부 Must | 우선순위가 없는 것과 같음 | Must ≤ 60% 강제 |
| JTBD 없이 Feature 나열 | "왜" 없이 "무엇"만 | Job → Feature 매핑 |
| Shape Up Appetite 무시 | 끝없는 프로젝트 | Circuit Breaker 적용 |
| Story Map 없이 백로그 | 전체 흐름 파악 불가 | 분기마다 Story Mapping |
| A/B Test 없이 출시 | 효과 검증 불가 | 핵심 변경은 실험 필수 |
| 감으로 우선순위 결정 | 편향, 정치적 결정 | 프레임워크 기반 합의 |

---

## Sources

- Intercom, "RICE: Simple prioritization for product managers"
- Dai Clegg, "Case Method Fast-Track: A RAD Approach" (1994) — MoSCoW 원전
- Ryan Singer, "Shape Up" (Basecamp, 2019): https://basecamp.com/shapeup
- Clayton Christensen, "Competing Against Luck" (2016) — JTBD
- Jeff Patton, "User Story Mapping" (2014)
- Eric Ries, "The Lean Startup" (2011) — MVP
- Teresa Torres, "Continuous Discovery Habits" (2021)
- Marty Cagan, "Inspired" (2017) — Product Discovery

**관련 skill**: `/dx:engineering-strategy`, `/dx:rfc-adr`, `/dx:dx-metrics`, `/dx:team-topologies`
