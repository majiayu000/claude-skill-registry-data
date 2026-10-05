---
name: spec-review
description: |
  "/spec-review", "spec review", "스펙 리뷰", "문서 리뷰",
  "설계 문서 수정", "requirements 수정", "요구사항 수정",
  "design.md 수정해줘", "requirements.md 변경", "plan 수정"
  Gate 밖에서 v2 파이프라인 문서(requirements.md / plan.json / design.md) 동기화 수정.
  specify/blueprint 세션 없이도 문서 기반 피드백을 반영하고 관련 파일을 동기화한다.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /spec-review — Gate 밖 문서 동기화 리뷰 (v2)

specify/blueprint 승인 게이트 밖에서도 **문서 기반 피드백 → 파일 수정 → 관련 파일 동기화**를 수행한다.

---

## v2 파이프라인 아티팩트 구조

```
<spec_dir>/
├── requirements.md   ← /specify 산출물. 요구사항 SSoT. 직접 편집 가능 (마크다운).
├── plan.json         ← /blueprint 산출물. 태스크/verify/contracts 상태. CLI로만 수정.
├── contracts.md      ← /blueprint 산출물. cross-module 인터페이스 + 불변식.
└── design.md         ← /blueprint Phase 4.5 산출물. 아키텍처 문서 (human-only).
```

**수정 원칙:**
- `requirements.md` → **직접 Edit** (마크다운 SSoT, CLI 불필요)
- `plan.json` → **`sr-harness-cli plan merge`** 만 사용 (직접 편집 금지)
- `contracts.md` → **직접 Edit** (마크다운)
- `design.md` → **직접 Edit** (human-only, /execute가 읽지 않음)

---

## 왜 필요한가

```
blueprint 승인 게이트 내:
  "R-T1.2 수정해줘" → requirements.md 수정 → design.md 재렌더링 → ✅

게이트 밖 (다른 세션, 일반 대화):
  "design.md §4 수정해줘" → design.md만 수정 → ❌ requirements.md 미반영
```

/spec-review는 **언제든지** 파이프라인과 동일한 동기화를 제공한다.

---

## 실행 흐름

### Step 1: spec_dir 로드

```
1. .sr-harness/specs/ 디렉토리에서 spec 목록 확인
2. spec이 1개 → 자동 로드
3. spec이 2개+ → 사용자에게 선택 질문
```

```
AskUserQuestion(
  question: "리뷰할 spec을 선택해주세요.",
  options: [
    { label: "wheel-controller-uart-refactor", description: "requirements.md + plan.json 있음" },
    { label: "narrow-corridor-navigation", description: "requirements.md만 있음 (blueprint 미실행)" }
  ]
)
```

### Step 2: 현재 상태 표시

```
Spec: wheel-controller-uart-refactor
Pipeline stage: blueprint 완료 (requirements + plan + design 있음)

Documents:
  ✅ requirements.md  — R-B1~R-B3, R-U1~R-U2, R-T1~R-T4 (18 sub-reqs)
  ✅ plan.json        — 11 tasks, 2 journeys, 18 verify entries
  ✅ contracts.md     — 3 interfaces, 2 invariants
  ✅ design.md        — 9 sections
  ❌ plan.json        — 없음 (blueprint 미실행)
```

### Step 3: 피드백 수신 루프

사용자의 자연어 피드백을 받아 처리한다.

```
사용자 피드백 수신
    ↓
피드백 유형 분류:
  ├── Sub-requirement 수정   → "R-T1.2의 then을 변경해줘"
  ├── Sub-requirement 추가   → "R-B2에 인증 실패 케이스 추가"
  ├── Sub-requirement 삭제   → "R-U1.3 삭제해줘"
  ├── Parent req 수정        → "R-T1 behavior 문구 변경"
  ├── contracts 수정         → "invariant 추가해줘"
  ├── design.md 섹션 수정    → "§4의 시퀀스가 틀렸다"
  ├── plan.json task 수정    → "T3 action 문구 변경"
  └── 전반적 보완 요청        → "에러 핸들링이 전체적으로 부족하다"
    ↓
파일 수정 (아래 규칙 적용)
    ↓
영향 범위 분석 → 관련 파일 동기화
    ↓
갱신된 내용 제시
    ↓
[Continue / Done]
```

### Step 4: 파일 수정 규칙

#### requirements.md 수정 (직접 Edit)

v2 requirements.md 포맷:
```markdown
## R-B1: <parent title>

#### R-B1.1: <sub title>
- given: <precondition>
- when: <trigger>
- then: <expected outcome>
```

수정 유형별 처리:
| 피드백 | 처리 |
|---|---|
| sub-req GWT 수정 | `#### R-X<n>.Y:` 해당 블록 Edit |
| sub-req 추가 | 부모 req 아래 새 `#### R-X<n>.Y:` 블록 추가 |
| sub-req 삭제 | 해당 블록 삭제, 이후 번호 재정렬 |
| parent behavior 수정 | `## R-X<n>:` 줄 + behavior 라인 Edit |

#### plan.json 수정 (CLI 경유)

```bash
cat > /tmp/sr-plan-patch.json << 'EOF'
{"tasks": [{"id": "T3", "action": "새로운 action 문구"}]}
EOF
sr-harness-cli plan merge <spec_dir> --patch --json "$(cat /tmp/sr-plan-patch.json)"
```

task status 변경은 `sr-harness-cli plan task <spec_dir> --status T3=done` 사용.

#### contracts.md / design.md 수정 (직접 Edit)

마크다운 파일이므로 해당 섹션을 직접 Edit. 전체 재작성 금지 — 수정된 섹션만.

### Step 5: 영향 범위 분석 + 동기화

수정된 파일에 따라 연쇄 동기화:

| 수정 대상 | 동기화 필요 파일 |
|---|---|
| `requirements.md` sub-req GWT | `design.md §4` (해당 기능 상세 섹션) |
| `requirements.md` parent req | `design.md §4`, `§3` (엔티티 영향 시) |
| `requirements.md` R-T req | `contracts.md` (인터페이스 영향 시), `design.md §2`, `§6` |
| `contracts.md` interface/invariant | `design.md §6`, `§2` |
| `plan.json` task 변경 | `design.md §5` (시퀀스 다이어그램) |

**동기화 규칙:**
1. 영향받는 문서의 **해당 섹션만** 재생성 (전체 재작성 금지)
2. 재생성 시 requirements.md ID 가시성 유지 (R-B1.1, R-T2.3 등)
3. plan.json 수정 후 반드시 `sr-harness-cli plan validate <spec_dir>` 실행

### Step 6: 결과 제시

```
## 수정 완료

### 파일 변경
- requirements.md: R-T1.2 then 항목 수정
- requirements.md: R-B2.4 추가 (인증 실패 케이스)

### 동기화
- design.md §4 R-T1 섹션 재생성
- design.md §4 R-B2 섹션에 R-B2.4 추가

[Continue reviewing / Done]
```

---

## 제약 사항

- **plan.json 직접 편집 금지** — 반드시 `sr-harness-cli plan merge/task` 경유
- **요구사항 신규 추가 시** — 해당 sub-req를 fulfill하는 task가 plan.json에 없으면 경고 표시
  ("R-B2.4가 plan.json에 coverage되지 않습니다. /blueprint를 다시 실행하거나 수동으로 task를 추가하세요.")
- **plan.json validate 실패 시** — 사용자에게 보고, 수정 제안

---

## 사용 예시

```bash
# 다음 날 design.md를 다시 읽다가 문제 발견
/spec-review
> "R-T1.2의 then에 'E-Stop 발행' 조건 추가해줘"
# → requirements.md R-T1.2 then Edit → design.md §4 R-T1 섹션 재생성

# 리뷰 미팅 후 피드백 반영
/spec-review
> "contracts.md의 wheel_cmd invariant에 timeout 조건 추가"
# → contracts.md Edit → design.md §6 재생성

# plan.json task 수정
/spec-review
> "T5 action 문구를 더 명확하게 바꿔줘"
# → sr-harness-cli plan merge --patch → design.md §5 재생성
```

---

## /specify · /blueprint 게이트와의 차이

| | 게이트 내 | /spec-review |
|--|---|---|
| 실행 시점 | specify/blueprint 세션 안 | **언제든지** |
| 세션 | 연속 세션 | 독립 세션 |
| 파일 동기화 | 자동 | 자동 |
| 다음 단계 진행 | Approve 시 | 없음 (Done만) |
| plan.json coverage 체크 | 자동 | 경고만 |
