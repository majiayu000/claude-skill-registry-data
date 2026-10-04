---
name: tdd-feature
description: 간결한 plan을 사용자와 합의한 뒤, feature(use case) 하나를 RGB(Red→Green→Blue) 사이클로 끝까지 자율 구현하는 오케스트레이터. 문제 정의·기능 분해·완료조건(programmer test) 합의까지는 사용자와 피드백을 주고받고(인터랙티브), 합의 후 구현은 그 feature의 모든 test에 대해 Red 전체→Green 전체→Blue 전체 3-phase로 피드백 없이 끝까지 진행하고, feature(use case) 전체를 phase마다 하나씩 최대 3개 커밋(reviewable-commits Why-body 포함)으로 남긴다(자율). superpowers의 장황한 spec/plan 대신 개발에 맞는 간결 포맷을 쓴다. "기능을 TDD로 끝까지 구현", "plan 합의하고 자율 구현", "feature 단위 RGB", "use case TDD로 짜줘", "/tdd-feature" 요청 시 반드시 사용. 후속 "이어서", "다음 feature", "재개", "다시 진행"도 처리. 단, 단일 test의 step-wise(매 단계 피드백) RGB는 /tdd-rgb, plan 문서만 작성하고 끝낼 때는 /tdd-plan이 적합.
argument-hint: "[feature/use case 설명 또는 plan-doc-path]"
---

# tdd-feature — 간결 Plan → Feature 단위 자율 RGB

하나의 feature(use case)를, 간결한 plan을 사용자와 합의한 뒤 RGB 사이클로 **끝까지 자율** 구현하는 오케스트레이터입니다. 기존 `tdd-red`/`tdd-green`/`tdd-blue` 에이전트를 재사용합니다.

## GOAL

- **성공 = 하나의 feature가 ① 간결 plan 합의 ② 모든 programmer test가 RGB로 구현·통과 ③ feature(use case) 전체가 reviewable-commits 표준(Why-body)을 갖춘 3-phase 커밋(test:/feat:/refactor:)으로 남음**
- **Phase A (인터랙티브)**: 문제·기능 분해·완료조건을 사용자와 합의
- **Phase B (자율)**: 합의된 **단일 feature**를 피드백 없이 끝까지 구현
- 향후 리뷰어가 커밋 메시지만으로 그 feature에서 내린 결정의 의도(Why)·맥락을 재구성할 수 있음

## CONSTRAINTS

### Hard Rules

#### 1. WIP = 1 (한 번에 하나의 feature)

- **한 실행에서 feature(use case) 하나만 구현한다.** plan에 feature가 2개 이상이면, 이번에 구현할 **하나를 선택**하고 나머지는 수정하지 않는다.
- 선택한 feature 완료 후 종료한다. 남은 feature는 "이어서 다시 호출" 또는 "다른 세션에서" 진행하도록 안내한다.
- 한 번에 하나에 집중해야 맥락·품질이 유지되고 슬라이스 단위로 동작을 검증할 수 있다(Walking Skeleton → 슬라이스 정교화).

#### 2. 자율성 경계 = Phase 경계

- **Phase A(plan)는 인터랙티브** — 각 단계마다 사용자 합의를 받고 다음으로 간다.
- **Phase B(구현)는 자율** — plan이 합의되면 그 feature의 모든 test에 대해 R→G→B를 **피드백 요청 없이 끝까지** 실행한다.
- 경계를 넘지 않는다: plan 미합의 상태로 구현 진입 금지, 합의 후 구현 중 불필요한 중단·재확인 금지. (이 점이 `/tdd-rgb`와의 근본 차이 — tdd-rgb는 기어가 정한 검토 지점마다 피드백을 받는다.)

#### 2a. 기어(Gears) 위치 — Phase B = high 기어

이 스킬은 `--gear` 옵션을 받지 않는다. **Phase B의 자율 진행 자체가 feature 범위의
high 기어**이기 때문이다. 따라서 tdd-rgb의 high 기어 안전장치를 동일하게 적용한다
(자율성만 가져오고 안전망을 제외하는 것은 허용되지 않는다):

- **시작 전 폭발 반경(blast radius) 점검** — 인증/인가, 결제·금액 계산, 데이터 삭제·변경, 외부 API
  호출, 동시성에 해당하면 Phase B 진입 전에 경고하고 "`/tdd-rgb --gear=low|mid`로
  단계별 검토"를 권한다. 결정은 사용자
- **시작 커밋 해시 기록** — Phase B 시작 시 HEAD를 plan 문서에 남긴다(적대적 리뷰 diff 기준점)
- **완료 보고 전 적대적 리뷰** — `../tdd-rgb/references/adversarial-review.md`의 절차를
  그대로 실행. green 스위트 + 적대적 리뷰 통과가 이 스킬의 Definition of Done
- **후퇴·놀라움 발생 시** — 자율을 중단하고 사용자에게 돌아가는 것이 다운시프트에 해당한다
  (tdd-rgb의 다운시프트 신호와 동일: revert, 예상 밖 실패 반복, 최소 구현 초과)

**low·mid 기어가 필요하면 이 스킬이 아니라 `/tdd-rgb --gear=low|mid`를 쓴다** — 낯선
도메인, 학습 목적, 설계 확신 부족은 자율 구현의 전제(작동하는 이론 보유)를 만족하지 않는다.

#### 3. use case 내 3-phase 커밋 (high 기어의 커밋 단위)

- **feature(use case) 하나 = 최대 3개 커밋.** 테스트 단위가 아니라 **phase 단위**로 나눈다
  — 그 feature의 모든 test에 대한 Red 변경을 한 커밋(`test:`)에, Green 변경을 한 커밋
  (`feat:`)에, Blue 변경을 한 커밋(`refactor:`, tidying이 불필요하면 생략)에 담는다.
  테스트마다 나누지 않고, feature 전체를 진행해 한 phase씩 끝낸다: 모든 test의 Red를 다
  쓴 뒤 → 모든 test의 Green을 채우고 → 마지막에 Blue를 한 번 적용한다.
- 따라서 **R/G/B 에이전트는 커밋하지 않는다** — `git add`까지만 수행하고(커밋 보류), 각
  phase가 feature의 모든 test에 대해 끝날 때마다 이 오케스트레이터가 커밋한다.
- **use case 경계를 넘겨 합치지 않는다** — 두 feature를 같은 phase 커밋에 담으면 "이
  phase가 이 feature에 대해 무엇을 했는가"라는 리뷰 단위가 성립하지 않는다. Hard Rule 1(WIP=1)이
  이 경계를 자동으로 보장한다.
- **제약**: test 단위 revert는 불가능하다(되돌림 단위는 phase). phase 단위 되돌림
  (구현만, 또는 tidying만)은 가능하다. 확신이 부족하면 `/tdd-rgb --gear=low|mid`로
  간다 (정본: `../tdd-rgb/SKILL.md`의 "진행 표기 규칙").

#### 4. Reviewable 커밋 (mental model을 커밋에 기록한다)

- 모든 커밋은 **`docs/reviewable-commits.md`(없으면 `${CLAUDE_PLUGIN_ROOT}/references/reviewable-commits.md`) 표준**을 단일 출처로 따른다.
- 이 스킬·에이전트는 subject·body 형식을 재기술하지 않고 경로로 참조만 한다(배포 시 표준 전문은 README의 "커밋 표준" 섹션 참조).
- 단, 길이는 플러그인 `../../references/commit-style.md`의 간결성 규칙(제목 + 핵심 bullet 2~4줄)이 우선한다.
- 이 스킬 고유사항만 여기 명시: 커밋이 phase마다 하나이므로 subject의 type 접두사는
  그 phase 그대로(`test:`/`feat:`/`refactor:`)이고, 무엇을 했는지가 아니라 **그 phase가
  이 use case에 대해 무엇을 보장·구현·정리했는지**를 적는다.
- ADR성 결정(되돌리기 어려운 설계 선택)도 **커밋 본문에 내장**한다 (별도 ADR 문서를 만들지 않는다).

#### 5. TDD 핵심 규칙 (tdd-rgb 계승)

- Three Laws of TDD: 실패 테스트 없이 production code 금지 / 실패를 보일 만큼만 테스트 작성 / 통과시킬 만큼만 구현.
- 한 번에 하나의 failing test. 실패 테스트가 있으면 새 테스트 추가 금지.
- TEST SHOULD FAIL WHEN YOU ADD IT — 모델 코드 수정 없이 통과하는 테스트는 추가하지 않는다.
- 허락 없이 테스트 삭제 금지.

#### 6. 기존 에이전트 재사용

- `tdd-red`/`tdd-green`/`tdd-blue` 에이전트(모델 `sonnet`)를 Agent 도구로 위임한다. **새 에이전트를 만들지 않는다.**
- 커밋 표준은 에이전트도 위임 prompt도 **소유하지 않는다** — 양쪽 모두 `reviewable-commits.md`를 경로로 참조(cite)할 뿐이다. 위임 prompt는 형식을 다시 적지 않고 단계(R/G/B)·자율 지시·**커밋 보류 지시**만 전달한다(아래 OUTPUT FORMAT 참조).
- 커밋은 에이전트가 아니라 이 오케스트레이터가 수행하므로, 각 에이전트가 반환한 변경 요약을 모아 두었다가 use case 커밋의 body 재료로 쓴다.

### 배움 반영 게이트 (Spec Anchored)

구현 중 앵커 문서(규칙·예제)와 어긋나는 배움을 발견하면 코드보다 앵커를 먼저
갱신하고 같은 커밋에 담는다. 규칙이 바뀌는 배움만 사용자에게 질문한다.
절차·기준은 `../../references/anchor-update.md`가 정본.

### Principles

#### 간결 우선 (anti-verbose)

superpowers·tdd-plan의 장황함을 제거한다. plan은 **합의에 꼭 필요한 것**만 담는다.

- **남길 것**: 문제(무엇을·왜), feature별 스토리 한 줄·핵심 규칙, programmer test 목록.
- **버릴 것**: 요구사항 작성 원칙(완전성/명확성/일관성)의 메타설명, INVEST 점검 서술, Gherkin `Rule:`/`Examples` 정식 서식(핵심 예시는 test 목록 항목으로 흡수), 별도 경계조건 섹션.

#### Programmer Test (완료 조건의 정의)

- 완료 조건 = Kent Beck의 programmer test. **FIRST**(Fast, Isolated, Repeatable=Deterministic, Self-validating, Timely) + **Test Desiderata**를 만족하고, **동작(behavior)에 coupled / 구조(structure)에 decoupled**.
- 작성 순서: degenerate(null·empty·0·경계) → interesting → general. (상세 기준은 `tdd-plan`·`tdd-rgb` 스킬 참조.)
- 기능의 external behavior를 실행 가능한 명세(Cucumber `.feature`)로 구축해 주 검증층으로 쓸 때는 `cucumber-acceptance` 스킬 참조 — 그 경우 `.feature`가 programmer test 계층이 되고, JUnit은 구현 세부사항과 결합되는 unit test로 세밀한 분기만 보조한다(programmer test가 좁혀지는 것이 아니라 별개 계층이 나뉘는 것).
- 요구사항 형식 선택 기준(0층 도메인 규칙 / User Story / Gherkin / 조건부 Use Case)은 `tdd-plan` 스킬이 단일 출처다 — 완료 조건을 Gherkin 핵심 예시로 쓰면 이후 `.feature`로 재작성 없이 이관된다.

## OUTPUT FORMAT

### 호출

```
/tdd-feature [feature 설명 또는 plan-doc-path]
```

- 인자로 feature 설명을 주면 Phase A의 문제 정의 출발점으로 쓴다.
- 기존 plan 문서 경로를 주면, 그 문서를 읽어 합의 상태를 파악하고 적절한 Phase로 진입한다(후속 "이어서"/"재개").

### 진입 판단 (Phase 0)

1. 인자로 plan 문서 경로가 주어졌거나 작업 디렉토리에 plan 문서가 있으면 읽는다.
2. 상태에 따라 분기:
   - plan 없음 / 미합의 → **Phase A부터**
   - plan 합의됨 + 미구현 test 존재 → **Phase B로** (해당 feature 자율 구현)
   - 한 feature 완료 + 남은 feature 존재 → 사용자에게 다음 feature 선택 요청 (WIP=1)

---

### Phase A: 간결 Plan (인터랙티브)

#### 간결 plan 포맷

```markdown
# {작업명}

## 문제
- 무엇을: {사용자가 무엇을 하려는가}
- 왜: {이것이 왜 필요한가 / 무엇을 해결하나}

## Features
### F1: {use case 이름}
스토리: As a {역할}, I want {원하는 것}, so that {가치}   ← 한 줄 압축. so that이 비면 작업 지시다
규칙: {핵심 비즈니스 규칙 1~3줄}
완료 조건 (programmer tests):
- [ ] {가장 단순한 degenerate case}
- [ ] {경계 case}
- [ ] {일반 case}

### F2: ...   ← 있으면 나열만, 구현은 한 번에 하나(WIP=1)

## 진행 기록
Phase B 시작 커밋: {F1: abc1234}   ← Phase B 진입 시 feature마다 HEAD 해시 기록 (적대적 리뷰 diff 기준점)
```

#### 진행 단계

각 단계 완료 후 **사용자 피드백을 받고**, 명시적 승인이 있을 때만 다음으로 간다.

1. **문제 정의** — 무엇을/왜를 1~2문단으로. 모호하면 질문한다.
2. **feature 분해** — 실행 가능한 use case 단위로 나눈다. 이번에 구현할 **feature 하나를 선택**한다(WIP=1).
3. **완료 조건 합의** — 선택한 feature의 programmer test 목록을 degenerate→general로 작성하고 합의한다.
4. **plan 문서화 + 커밋** — 위 포맷으로 마크다운 작성(경로는 사용자 지정, 없으면 제안). `git add <plan>` 후 `docs: {작업명} plan 합의` 커밋.

#### 합의 게이트 (Phase A → B 전환점)

- plan(특히 선택 feature의 test 목록)이 합의되고, 사용자가 **명시적으로 구현 시작을 승인**해야 Phase B로 진입한다.
- 이 게이트가 인터랙티브↔자율의 경계다. 승인 전에는 production code를 한 줄도 쓰지 않는다.

---

### Phase B: Feature 단위 자율 RGB (합의 후)

**진입 직전 (high 기어 안전장치, Hard Rule 2a)**: ① 폭발 반경(blast radius) 점검 — 해당하면 경고하고
`/tdd-rgb --gear=low|mid` 대안을 제시한 뒤 사용자 결정을 기다린다. ② 현재 HEAD 해시를
plan 문서의 `## 진행 기록` 섹션에 `Phase B 시작 커밋: {feature: 해시}` 형식으로 기록한다
(위 plan 포맷 참조 — 적대적 리뷰가 이 값을 diff 기준점으로 읽는다).

선택된 feature의 구현 목록(web-app은 `.feature`의 `@pending` 시나리오 목록, general은
앵커 문서 `## 예제 (검산표)` 표의 미구현 행 — Cucumber 없이 구현하기로 선택했다면 앵커
예제 검산표를 구현 목록으로 사용한다. `--full`로 작성한 경우 그 unit test 목록)를 위에서
아래로 순회한다. **테스트 단위로 R→G→B를 반복하지 않는다** — feature 전체를 phase 단위로 진행한다: 모든 test에 대해 Red를 다 마친 뒤, 모든 test에 대해 Green을 채우고, 마지막에 Blue를 feature 범위로 한 번 적용한다. **단계·test 사이에 사용자 피드백을 요청하지 않는다.**

협력 객체가 다수 관여하는 feature에서도 phase를 끝까지 마친 뒤 실행·확인한다. 그래야
phase 경계가 실제 리뷰 단위(이 phase가 feature 전체에 대해 무엇을 했는가)로 남는다.

#### feature의 3-phase

1. **Red 전체** — feature의 미완료 test(`- [ ]`) 각각에 대해 `tdd-red`를 순차 위임한다.
   각 위임은 그 test 하나의 실패 테스트만 작성, **커밋 보류**(`git add`까지). 모든 test를
   다 쓴 뒤 스위트를 실행해 신규 test 수만큼 의도한 실패인지 확인한다.
2. **커밋 1 (`test:`)** — `git add` 누락분 확인 후 커밋. subject
   `test(<범위>): <feature 이름> — 실패 테스트 작성`. 체크박스는 아직 `- [ ]`로 남긴다
   (아래 "Feature 완료 처리"의 커밋 절차 참조).
3. **Green 전체** — 같은 순서로 `tdd-green`을 순차 위임한다. 위임 prompt에 "**최대한
   절차적으로**"를 명시한다 — 추출·일반화 없이 통과만 시킨다(정리는 Blue phase가
   담당). **커밋 보류**. 전체 완료 후 스위트 전부 green을 확인한다.
4. **self-check (Green 커밋 전)** — 커밋할 diff가 이미 추출된 private 메서드·이름 붙은
   중간 변수를 여럿 갖고 있다면(Composed Method 형태), "Blue가 정리할 게 없다"로 판단하지
   말고 **Green 위임 자체를 의심한다** — 참조 구현이나 최종 형태를 그대로 옮겨 쓰지
   않았는지 확인하고, 인위적으로 절차적인 형태로 다시 만들어 커밋한다.
5. **커밋 2 (`feat:`)** — `git add` 후 커밋. subject `feat(<범위>): <feature 이름>`.
   feature의 모든 test 체크박스를 `- [x]`로 갱신해 **같은 커밋에** 담는다.
6. **Blue 전체** — `tdd-blue`에 이 feature 범위 전체(커밋 2 이후 변경 파일 목록)로
   위임한다. Local Tidying Process. **커밋 보류**. 적용 후에도 스위트 green 유지를
   확인한다.
7. **커밋 3 (`refactor:`)** — 변경이 있으면 `git add` 후 커밋. 변경이 없으면(이미
   깔끔하면) 생략한다.
8. **추가 항목 pass** — 1·3·6의 에이전트 보고에서 `목록 추가:` 항목을 모은다. 규칙이 바뀌는
   항목은 사용자에게 질문해 확정한다(Phase B에서 유일하게 허용되는 중간 질문). 확정된 추가
   행이 있으면 그 행만 대상으로 1~7을 한 번 더 실행한다(커밋 최대 3개 추가, subject에
   "추가 항목" 명시). 추가가 없을 때까지 반복한다. 절차는
   `../../references/anchor-update.md`의 "테스트 목록 갱신"이 정본

각 phase 내부(1, 3, 6)에서 test마다 에이전트가 반환한 변경 요약(무엇을·왜 그렇게
했는가)을 보관한다 — 그 phase 커밋 body의 재료다. 작업 내역은 plan 문서에 1~3줄
기록한다(코드 제외).

커밋 절차의 세부(진행 기록 표기 시점·body 구성)는 아래 "Feature 완료 처리" 참조.

> **Getting Stuck 후퇴 수신**: Green 단계에서 tdd-green이 "Getting Stuck 복구 경로"
> 1단계(simpler test로 후퇴)를 보고하면, 오케스트레이터가 원 테스트를 `@Disabled`
> 처리하고 simpler test를 목록 앞에 삽입한 뒤 자율 진행을 계속한다. 후퇴 발생은
> plan 문서 작업 내역에 남긴다 — 사용자 중단 없이 처리하되 최종 검토에서 보이게.

#### 에이전트 위임 prompt 템플릿

각 에이전트 호출 시 Agent 도구의 `subagent_type`에 `tdd-red`/`tdd-green`/`tdd-blue`를 지정하고, prompt에 **대상 test + 자율 지시 + 커밋 보류 지시**만 전달한다:

```
[자율 모드 / 커밋 보류 / feature: {F이름} / phase: {Red|Green|Blue} 전체 / test: "{test 설명}"]

{Red|Green|Blue} 단계를 수행하세요.

- **커밋 보류**: `git add`까지만 하고 커밋하지 마세요. 이 feature는 phase 단위(전체
  Red→전체 Green→전체 Blue)로 최대 3번 커밋되며, 커밋은 오케스트레이터가 수행합니다.
- (Green 단계에만) **최대한 절차적으로 구현하세요** — 추출·일반화하지 마세요. 정리는
  모든 test의 Green이 끝난 뒤 Blue phase에서 한 번에 합니다.
- 대신 변경 요약을 반환하세요 — 무엇을 바꿨는지, **왜 그렇게 했는지(버린 대안 포함)**.
  이 요약이 그 phase 커밋 body의 재료가 됩니다.
- 목록에 없는 필요한 동작을 발견하면 목록에 추가(기존 규칙의 새 예시)하거나 보고(새
  규칙)하고, 완료 보고에 `목록 추가: [항목 | 없음]`을 반드시 적으세요.
- 이 단계는 자율 실행입니다. 작업 후 사용자 피드백을 기다리지 마세요.
```

#### phase 커밋 body에 담을 Why

phase마다 커밋 하나이므로 그 phase가 feature 전체에 걸쳐 무엇을 했는지를 **테스트별로
나열하지 말고 결정별로** 적는다:

| phase | body에 담을 Why |
|------|-----------|
| Red (`test:`) | 이 동작(인수조건)들이 왜 중요한가, 왜 이 순서로 골랐나 |
| Green (`feat:`) | 왜 이 구현을 택했나 (다른 접근을 배제한 이유) |
| Blue (`refactor:`) | tidying이 무엇을 드러냈나 (이 구조가 의도를 더 잘 드러내는 이유) |

#### Feature 완료 처리

- feature의 모든 test가 `- [x]`이고 전체 테스트가 통과하면 구현 완료.
  **체크박스만으로 판정하지 않는다** — 전체 스위트 green을 함께 확인한다. Red phase
  커밋 시점에는 모든 test가 아직 실패 상태이므로 체크박스는 전부 `- [ ]`로 남아 있는
  것이 정상이다 — Green phase 커밋에서 일괄 `- [x]`로 갱신한다.
- **진행 기록 대조**: Green phase 커밋 직후, 체크된 항목과 실제 테스트 코드를 맞춰
  본다. 체크 안 된 항목을 덮는 테스트가 이미 있거나, 체크됐는데 대응 테스트가 없으면
  그 자리에서 바로잡는다(자율 진행은 중간 검토가 없어 드리프트가 누적된다).
- **완료 판정 전 대응 점검**: 미구현 행 0개(추가 항목 pass 포함) + `## 규칙` 모든 번호가
  테스트 1개 이상과 대응하는지 확인한다. 대응 없는 규칙은 미구현 행으로 추가하고 추가
  항목 pass로 처리한다. 정본은 `../../references/anchor-update.md`의 "완료 판정 전 대응 점검"
- **3-phase 커밋** (각 phase가 feature의 모든 test에 대해 끝날 때마다 수행 — 위
  "feature의 3-phase" 1~6단계와 동일 절차의 커밋 부분만 재정리):
  1. **커밋 1 (`test:`)** — Red 전체 완료 후. `git status`로 누락분 확인 후 `git add`,
     커밋. subject `test(<범위>): <feature 이름> — 실패 테스트 작성`
  2. **커밋 2 (`feat:`)** — Green 전체 완료 + 스위트 green 확인 후. `git add`, 커밋.
     subject `feat(<범위>): <feature 이름>`. 체크박스 갱신을 같은 커밋에 담는다
  3. **커밋 3 (`refactor:`)** — Blue 적용 + 스위트 green 재확인 후. 변경이 있으면
     `git add`, 커밋. 변경 없으면 생략
  - 각 커밋 body는 `reviewable-commits.md` 표준 + 위 "phase 커밋 body에 담을 Why"의
    해당 행
  - 한글 메시지는 임시 파일 + `git commit -F` (`-m "한글"` 금지 — 깨짐)
- **적대적 리뷰 (필수)**: 완료 보고 **전에** 실행한다 — 시작 커밋 해시부터 HEAD까지의
  diff를 대상으로, `../tdd-rgb/references/adversarial-review.md`(리뷰어 선택·내장
  프롬프트·심각도 처리)를 `Read`로 읽어 그대로 따른다. green 스위트 + 적대적 리뷰
  통과가 Definition of Done. 리뷰에서 수정이 발생하면 **그 수정이 속한 phase의 커밋에**
  `--amend`로 합친다 — 이미 커밋된 다른 phase는 수정하지 않는다.
- **완료 보고**: 구현된 test 목록, 3-phase 커밋 해시(test:/feat:/refactor:, 생략된
  phase가 있으면 명시), 통과 상태, 적대적 리뷰 결과를 요약한다. 표본 정독용으로
  대표 test 하나(가장 복잡했거나 후퇴가 있었던 것)를 추천해 함께 제시한다.
- **하드닝 제안 (실행 아님)**: 완료 보고 마지막에 `../tdd-rgb/references/hardening-gate.md`를
  `Read`로 읽어 그 규칙대로 제안 블록을 추가한다 — CRAP·DRY(빠름, 변경 파일 한정)와
  mutation(느림, 파일 1개)을 사용자가 복사해 실행할 수 있는 명령으로. 블록 안의 순서는
  비용순이 아니라 **파이프라인순**이다 — ①CRAP·DRY(정리할 곳 찾기) →
  ②`/system-wide-refactoring`(정리) → ③mutation(정리된 코드에). ②가 뮤턴트 지점을
  바꾸므로 ③이 마지막이다. 적용 조건
  (Java·src/main 변경 존재, CRAP·mutation은 추가로 Maven 필요) 미충족 시 생략 사실만
  한 줄 보고. **자동 실행 금지.**
- **세션 프로파일 안내**: 하드닝 제안 다음 줄에 "`/tdd-profile` — 이 세션의 단계·
  에이전트별 시간·토큰과 model/effort 조정안" 한 줄을 추가한다. 실행은 사용자가 한다.
- **WIP=1 안내**: plan에 다른 feature가 남아 있으면 — "feature {F} 완료. 남은 feature: {목록}. 이어서 진행하려면 `/tdd-feature {plan경로}`로 다시 호출하거나, 다른 세션에서 진행하세요." (자동으로 다음 feature를 시작하지 않는다.)

## FAILURE CONDITIONS

| 증상 | 대처 |
|------|------|
| plan 미합의 상태로 구현 진입 시도 | 중단하고 Phase A로 복귀, 합의 게이트 통과 후 재진입 |
| feature 2개 이상을 한 실행에서 구현 시도 | WIP=1 위반 — 하나로 좁히고 나머지는 다음 실행으로 |
| 커밋이 What만 담고 Why가 없음 | reviewable-commits 미달 — body에 Why·버린 대안 보강 후 amend |
| 자율 구현(Phase B) 중 매 단계 피드백 요청 | `/tdd-rgb`와 혼동 — Phase B는 feature 끝까지 자율 |
| 폭발 반경(blast radius) 점검 없이 Phase B 진입 | high 기어 안전장치 누락(Hard Rule 2a) — 점검 후 재진입, 해당 영역이면 `/tdd-rgb --gear=low\|mid` 권고 |
| 시작 커밋 해시 미기록 | 적대적 리뷰의 diff 기준점 없음 — Phase B 진입 시점 커밋을 찾아 진행 기록에 보강 |
| 하드닝 도구를 자동 실행함 | 제안만 모드 위반 — 실행을 중단하고 제안 블록으로 되돌린다 |
| 적대적 리뷰 없이 완료 보고 | Definition of Done 미달 — 리뷰 실행 후 결과를 포함해 재보고 |
| 진행 기록 체크박스와 실제 테스트 불일치 | 드리프트 — 완료 처리의 대조로 바로잡고, Green phase 커밋에 문서 갱신을 함께 담는다 |
| 에이전트가 test마다 커밋함 | 커밋 보류 지시 누락(Hard Rule 3) — `git reset --soft`로 그 phase 시작점까지 되돌려 phase 커밋 하나로 다시 만든다 |
| feature 2개가 한 phase 커밋에 담김 | use case 경계 위반 — WIP=1을 지키지 않은 결과. 커밋을 분리한다 |
| 테스트 단위로 R→G→B를 반복함(phase를 안 나눔) | Hard Rule 2a/3 위반 — high 기어의 3-phase 커밋 단위를 따르지 않은 것. 이미 커밋됐다면 phase 경계로 재구성하거나 사용자에게 보고 |
| low·mid 검토 밀도를 요구받고도 이 스킬로 진행 | 기어 불일치 — `/tdd-rgb --gear=low\|mid`로 전환 안내 |
| 추가 시점에 실패하지 않는 test | TDD 위반 — 모델 코드 수정이 필요한 failing test만 추가 |
| 요구사항 이해 불확실 | 추측 말고 "제가 이해한 것이 맞는지 확인해주세요"로 질문 (Phase A 한정) |
| 앵커와 어긋난 코드 변경을 앵커 갱신 없이(또는 다른 커밋으로) 커밋함 | 배움 반영 게이트 위반 — 앵커를 먼저 갱신하고 같은 커밋에 담아 재정리 |
| 구현 중 발견한 필요한 동작이 목록에 없음 / 대응 테스트 없는 규칙이 남은 채 완료 보고 | 테스트 목록 갱신 위반 — 미구현 행으로 추가하고 추가 항목 pass 실행 |
