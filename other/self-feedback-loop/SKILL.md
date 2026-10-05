---
name: self-feedback-loop
description: >
  구현 결과를 plan 기준으로 반복 검토하여 품질을 끌어올리는
  review-fix-verify-commit 루프. material finding 소진까지 반복한다.
  "self-feedback loop 돌려", "피드백 루프 시작", "review fix commit 반복",
  "구현 결과 검토하고 수정해", "코드 리뷰하고 고치고 커밋까지",
  "adversarial review and fix", "review and fix", "리뷰하고 고쳐",
  "review loop 돌려", "셀프 리뷰하고 수정해", "리뷰 루프", "피드백 루프",
  "코드 점검하고 수정해줘" 등 실행 의도가 명확할 때 트리거.
  단순 "review", "검토", "구현 검토해줘", "self-review" 같은 read-only
  요청만으로는 트리거하지 않는다.
---

# Self-Feedback Loop

구현 결과를 plan 기준으로 반복 검토하여 품질을 끌어올리는 review-fix-verify-commit 루프.

## 모드 선언

이 스킬이 활성되면 아래 모드로 전환한다:

- **plan-bounded fix 세션이다.** review-fix-verify-commit 루프를 돌리되, 새 기능 추가, 범위 확장, 설계 재논의를 하지 않는다.
- **plan이 기준이다.** plan에 없는 개선은 자동 수정하지 않는다. plan이나 AGENTS.md에 out-of-scope로 명시된 항목을 미구현이라고 finding 처리하지 않는다.
- **surgical fix만 한다.** 수정은 finding에 직접 대응하는 범위로 한정한다. 인접 코드 정리, unrelated refactor, 스타일 통일 금지.
- **단, 시야는 닫지 않는다.** plan 밖 개선 여지, design smell, 범위 밖 위험은 fix 대상이 아니지만 **Notes**로 누적해 Final에서 한 번에 보고한다.
- **read-only 요청이면 중단한다.** 사용자 요청이 단순 `review`/`검토`/`확인`이면 이 루프를 실행하지 말고, 수정·커밋 없는 read-only review로 전환한다.

## 시작 절차

### 1. 프로젝트 컨텍스트 수집

아래 파일을 찾아 읽는다 (없으면 건너뜀):

- `AGENTS.md` (프로젝트 root) — 코딩 가이드라인, out-of-scope 정의
- `docs/plans/` 하위 최신 plan 파일 — 구현 목표와 체크리스트
- `README.md` — 프로젝트 개요
- operator/feature guide가 있으면 함께 읽는다

### 2. 현재 상태 파악

```bash
git status
git diff --stat
git log --oneline -5
```

변경된 파일 목록에서 구현 파일과 테스트 파일을 식별한다.

### 3. plan 대조

plan의 각 chunk/task와 현재 구현을 대조한다. 체크박스가 체크되어 있는데 실제로 구현이 안 된 항목, 또는 구현은 되어 있는데 체크 안 된 항목을 찾는다.

## 루프 구조

```
review → findings 정리 → fix → targeted verify → commit
  ↑                                                 |
  └─────────── material finding 있으면 반복 ─────────┘
```

### Review

첫 cycle은 **다중 페르소나 dispatch**, 이후 cycle은 **narrow follow-up** 모드로 동작한다. 단, 시작 전에 현재 환경에서 subagent/Agent 도구를 사용할 수 있는지 확인한다.

#### Pass A: 다중 페르소나 dispatch (첫 cycle만)

subagent/Agent 도구를 사용할 수 있으면 `general-purpose` 서브에이전트를 페르소나별로 **병렬 dispatch**한다. 같은 머리로 모든 시각을 동시에 유지하지 않기 위함이다.

subagent/Agent 도구가 없으면 **local fallback**으로 진행한다:

1. 기본 3종(`correctness`, `scope-guardian`, `adversarial`)만 본 세션에서 순차 적용한다.
2. `security`는 변경이 외부 입력, secret, auth, trust boundary에 닿을 때만 추가한다.
3. `coherence`는 docs/guide drift나 기존 패턴 변경이 보일 때만 추가한다.
4. cycle 출력에 `Fallback: local persona review`를 명시한다.

**기본 페르소나 5종** (모든 프로젝트):

- `correctness` — 로직 결함, 누락된 edge case, 계약 불일치, happy-path-only 테스트
- `scope-guardian` — plan 체크리스트 vs 실제 코드 정합성, out-of-scope 침범, finding/Notes 분류
- `security` — 미검증 입력, secret 노출, 권한 우회, 신뢰 경계
- `adversarial` — "이 코드를 어떻게 깨뜨릴까" 시각. race, 동시성, 비정상 입력, 부분 실패
- `coherence` — 기존 스타일/네이밍/구조와의 일관성, docs·guide drift

**프로젝트별 페르소나** (CLAUDE.md / AGENTS.md / package 매니페스트에서 신호 감지 시 추가):

- `performance` — 핫패스, N+1, blocking I/O, allocation
- `framework-specific` — Rails / Next.js / React Native / Swift 등 프레임워크 footgun

각 페르소나 프롬프트는 `references/personas.md` 참조. 서브에이전트는 SKILL.md를 재로드하지 않으므로 프롬프트는 stateless·self-contained로 전달.

각 페르소나의 출력 포맷 (구조화된 JSON-ish):

```
[<severity-hint>] <파일:라인> — <문제> | 기대: <기대 동작>
```

`severity-hint`는 참고 신호다. 페르소나는 severity를 확정하지 말고 finding 후보와 hint만 반환한다. 최종 severity 분류는 Pass B에서 본 스킬이 일괄 수행.

#### Pass B: merge & dedup

페르소나별 raw finding을 한 곳에 모은 뒤:

1. **dedup** — 같은 파일:라인 ±3 윈도우에서 같은 증상을 가리키는 finding은 1개로 병합. 페르소나 라벨은 `(correctness+adversarial)` 형태로 유지.
2. **severity 분류** — `Findings 정리` 표 기준으로 critical/high/medium/low 부여.
3. **Notes 추출** — finding 형태이지만 plan 범위 밖이거나 "~하면 좋겠다" 수준은 Notes로 이동.

페르소나 간 충돌 (예: `security`는 fix 권고, `scope-guardian`은 범위 밖이라 Notes 권고)은 *scope-guardian 우선* — 범위 밖이면 Notes로 가고, 위험도가 보이면 Notes에 위험도를 명시.

#### Pass A (narrow): 후속 cycle

2회차 이후 cycle은 **이전 cycle finding의 fix 결과만** 좁게 review한다. 페르소나 dispatch 없이 본 스킬이 직접 수행:

1. 이전 cycle의 각 finding이 의도대로 해결됐는가
2. fix가 새 finding(regression 또는 인접 결함)을 만들었는가
3. plan 체크리스트 상태가 fix로 변했는가 (체크 갱신)

전체 페르소나 재dispatch는 다음 조건에서만:
- 범위가 크게 확장된 fix가 있었다
- 페르소나 한 종류가 1회차에서 0 finding을 반환했고, 실제로는 누락이 의심된다

### Findings 정리

severity 순으로 정리한다:

| Severity | 기준 | 예시 |
|----------|------|------|
| **critical** | 런타임 에러, 데이터 손실, 보안 결함 | race condition, 미검증 입력 |
| **high** | 기능 오동작, 계약 불일치 | async contract 위반, 잘못된 상태 전이 |
| **medium** | edge case 누락, 불완전한 테스트 | 중복 처리 미흡, 경계값 미검증 |
| **low** | docs 불일치, 사소한 불일관성 | 가이드 문구와 코드 동작 차이 |

각 finding은 **파일:라인 + 구체적 문제 + 기대 동작**으로 기술한다. "~하면 좋겠다" 수준의 모호한 제안은 finding이 아니다 — **Notes로 기록한다.**

### Notes (개선/범위 밖)

아래는 finding이 아니라 Notes로 누적한다. **자동 수정하지 않고**, Final 출력에 한 번에 모아 보고한다.

- plan 범위 밖이지만 변경 코드 인접에서 발견한 개선 여지
- design smell, 구조적 어색함, 후속 plan 후보
- "~하면 좋겠다" 수준의 제안
- doc drift 중 즉시 깨지지 않는 것
- out-of-scope이지만 위험도가 보이는 항목

형식: `파일:라인 — 한 줄 메모 (왜 지금 안 고치는지)`

cycle 진행 중 발견하면 메모만 해두고 cycle 출력에는 적지 않는다. Final에서 합쳐 보고.

### Fix

- finding 하나당 하나의 수정 단위. 여러 finding을 한 번에 고쳐도 되지만, 각 수정이 어떤 finding에 대응하는지 추적 가능해야 한다.
- 수정 중 새로운 문제를 발견하면 현재 fix를 완료하고, 다음 cycle의 finding으로 기록한다.

### Verify

수정 범위에 맞는 targeted test를 실행한다. 프로젝트의 test runner를 사용한다 (시작 전 `package.json`, `Makefile`, `Gemfile` 등에서 test 명령을 확인).

### Commit

targeted verification이 green일 때만 커밋한다. 메시지는 해당 cycle의 수정 의도를 드러낸다:
```
fix(scope): 구체적 수정 내용
```

## 종료 조건

- **연속 2회 리뷰에서 material finding(critical/high/medium)이 없으면 종료한다.**
- 최소 1회 review는 반드시 수행한다. finding이 없으면 review만으로 cycle 완료를 인정한다.
- 종료 전 가능하면 **full test suite**를 실행한다. 환경 제약(대형 repo, 느린 CI, 부분 checkout)으로 불가하면 변경 범위에 해당하는 test suite로 대체하고, 그 사실을 Final 출력에 명시한다.
- low severity만 남은 경우 한 번에 모아서 수정하고 종료해도 된다.
- **Notes는 종료를 막지 않는다.** 누적량이 많아도 보고만 하고 끝낸다.

## 출력 포맷

각 cycle과 최종 결과를 아래 형식으로 보고한다. 상세 템플릿은 `references/output-format.md` 참조.

```
## Cycle N
- Findings: (severity별 목록)
- Fixes: (파일:라인 단위)
- Verification: (실행 명령 + 결과)
- Commit: (hash + 메시지)

## Final
- Full verification: (명령 + 결과)
- Residual risks: (있으면)
- Notes: (cycle 동안 누적된 개선/범위 밖 항목. 없으면 "없음")
```

## Gotchas

- **Scope creep의 가장 흔한 형태**: "이 finding을 고치려면 관련 테스트도 업데이트해야 하고, 그러면 test helper도..." — finding의 직접 수정 범위를 넘어가면 멈추고 다음 cycle finding으로 분리한다.
- **Targeted test만 돌리다가 final에서 깨지는 패턴**: 수정이 3개 파일 이상에 걸치면 targeted 대신 관련 test suite 전체를 돌리는 게 안전하다.
- **첫 리뷰에서 finding 0개**: plan과 코드를 실제로 라인 단위로 대조했는지 자문한다. finding이 정말 없으면 무리하게 만들지 말되, diff/tests/docs/plan status를 한 번 더 확인한 후에 결론 내린다.
- **Finding severity 과대평가**: cosmetic 이슈를 medium으로 올리면 수정 시간을 낭비한다. "이걸 안 고치면 사용자가 영향을 받는가?"로 판단.
- **Fix 도중 새 버그 도입**: 수정 후 targeted verify를 건너뛰고 싶은 유혹이 있다. 반드시 verify를 거친다 — 1줄 수정이라도.
- **Out-of-scope 오판**: plan에 명시적으로 제외된 항목(auth, UI redesign 등)을 "발견"하고 고치려 하면 review session의 목적을 벗어난다. 시작 시 out-of-scope 목록을 메모하고 매 finding마다 대조한다. 위험도가 보이면 fix 대신 **Notes에 기록**한다.
- **커밋 단위가 너무 크거나 작음**: 1 finding = 1 commit이 아니다. 한 cycle의 모든 fix를 하나의 커밋으로 묶되, 성격이 완전히 다른 fix(예: 로직 수정 + docs 수정)는 분리한다.
- **페르소나 추가의 함정**: 페르소나는 *서로 다른 사각지대*를 보기 위한 것이다. 비슷한 시각의 페르소나를 늘리면 dedup 부담만 커지고 finding 다양성은 오르지 않는다. 5종으로 시작하고, 프로젝트 신호가 있을 때만 1–2종 추가한다.
- **페르소나 결과를 그대로 finding으로 채택 금지**: dispatch 결과는 *후보 finding*이다. Pass B의 merge·severity 분류·Notes 분리를 거치지 않고 바로 fix로 가면 false positive에 시간을 낭비한다.
