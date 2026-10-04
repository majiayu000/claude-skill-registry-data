---
name: tdd-rgb
description: TDD RGB(Red→Green→Blue) 사이클 진행 — 테스트 목록의 한 항목씩 tdd-red·tdd-green·tdd-blue 에이전트에 순차 위임하고 기어(low/mid/high)로 검토 밀도를 조절. "RGB 사이클 돌려", "다음 테스트 진행", "TDD 사이클 계속", "red-green-blue", "/tdd-rgb" 요청 시 사용. 단, feature 하나를 plan 합의 후 끝까지 자율 구현하는 것은 /tdd-feature, 계획 문서만 작성하는 것은 /tdd-plan이 적합. /tdd-rgb [plan-doc-path] [--gear=low|mid|high]로 호출.
argument-hint: "[plan-doc-path] [--gear=low|mid|high]"
---

# TDD RGB 사이클 Skill

Red → Green → Blue 사이클을 조율하여 테스트 목록의 각 항목을 순차적으로 구현합니다.

## GOAL

- **성공 = 테스트 목록의 모든 항목이 `- [x]`로 완료되고, 모든 테스트가 통과하며, 작업 내역이 마크다운에 반영됨**
- 모든 테스트 케이스가 `- [x]`로 완료됨
- 모든 테스트가 통과함
- 작업 내역이 마크다운 파일에 반영됨
- (Web App의 경우) 모든 `.feature` 시나리오의 `@pending` 해제·green, JPA Repository 완성, DSL 개선까지 완료
- 검토 지점의 밀도는 기어(low/mid/high)가 정한다 — 아래 "기어(Gears)" 섹션 참조

## CONSTRAINTS

### Hard Rules

#### Three Laws of TDD

1. "Write NO production code except to pass a failing test."
2. "Write only ENOUGH of a test to demonstrate a failure."
3. "Write only ENOUGH production code to pass the test."

#### TDD 핵심 규칙

- don't write code without a failing test.
- only write the code necessary to get the test to pass (little golf game).
- never delete tests without express permission.
- 테스트를 추가할 때는 반드시 한번에 하나씩 추가. 실패하는 테스트가 있을 때는 절대 새로운 테스트를 추가할 수 없음.

#### 마이크로 사이클

각 단계는 **2-3분 이내** 작업으로 빠른 피드백을 받습니다.

- 복잡한 목표를 작은, 집중된, 검증 가능한 단계로 분해하여 순차적으로 실행
- **low·mid 기어**: 각 R/G/B 에이전트가 작업 완료 후 자체적으로 커밋을 수행 (커밋 → 피드백 → 다음 단계)
- **high 기어**: 에이전트는 커밋을 보류하고(stage까지만), 오케스트레이터가 use case 전체를
  Red 전체→Green 전체→Blue 전체 3단계로 진행하며 각 단계 종료 시 한 번씩 커밋한다
  (아래 "진행 표기 규칙"의 기어별 커밋 단위)

#### 피드백 규칙

- **기어가 정의하는 검토 지점에서 반드시 사용자 피드백을 요청하고 대기** ("기어(Gears)" 섹션의 검토 지점 표 참조)
- 검토 지점에서는 사용자가 명시적으로 다음 단계로 진행을 결정해야만 진행
- 검토 지점이 아닌 phase 경계(mid/high 기어)에서는 대기 없이 다음 phase로 진행한다. 커밋은
  기어별 커밋 단위를 따른다 — low는 phase마다, mid는 사이클마다, high는 use case 내
  3-phase(전체 Red·전체 Green·전체 Blue)마다
- 피드백 요청 형식: "이 [구현/테스트/설계]에 대한 피드백을 주시겠어요? 특히 [집중해야 할 부분]에 대해서요."

### 기어(Gears) — 검토 밀도 조절

Kent Beck의 "driving in gears": 이론에 대한 확신(confidence)이 검토 지점의 밀도를 정한다.
**기어는 검토 지점의 밀도를 바꾸고, 그에 맞춰 커밋 단위도 바뀐다** — TDD 3법칙, 한 번에
테스트 하나, 테스트 삭제 금지는 모든 기어에서 동일하지만, 커밋 단위는 low=phase(테스트마다
R/G/B 각각), mid=사이클(테스트마다 RGB 하나), high=use case 내 3-phase(use case 전체의
Red 한 번·Green 한 번·Blue 한 번)다.

**revert 단위는 커밋 단위와 같다**: low·mid는 테스트 단위로 되돌리고, high는 use case
내 phase 단위(전체 구현 또는 tidying만)로 되돌린다. high에서는 테스트 하나만 골라
되돌릴 수 없다.

#### 기어별 검토 지점

| 기어 | 검토 지점(사용자 피드백 대기) | 이해 채널(사용자가 코드를 이해하는 방법) | 대응 상황 |
|---|---|---|---|
| **low** (기본) | Red 후 · Green 후 · Blue 후 | 편집 하나하나 직접 읽기, 리팩터링도 직접 지시 (이해 체화) | 이론에 확신 없음, 낯선 도메인·기술, 학습 목적 |
| **mid** | 테스트 1개의 R→G→B 사이클 완료 후 1회 | 사이클 경계의 diff 검토 + tidying 방향 지목·승인 (실행은 위임하되 판단은 유지) | 유사 문제 경험 있음, 작동하는 이론을 빠르게 확보할 것으로 기대 |
| **high** | 전체 테스트 목록 완료 + 적대적 리뷰 통과 후 최종 1회 | 행동 명세(테스트 목록·Gherkin)로 이해 + 최종 검토에서 대표 슬라이스 하나를 골라 표본 정독 | 이론이 상용구(boilerplate) 수준으로 명확 |

#### 기어 운용 — 호출 형식·전환 신호·폭발 반경(blast radius)·기어 기록

시작 시·사이클 경계 점검 시 이 스킬 디렉터리의 `references/gears.md`(정본)를
`Read`로 읽는다:

- Step 1 시작 시 — 기어 결정, 폭발 반경(blast radius) 점검, 기어 기록 형식
- 사이클 완료 시 — 업/다운시프트 신호 점검
- `/tdd-feature`와의 경계가 궁금할 때

기억할 최소한: **기어는 검토 밀도를 정하고, 폭발 반경(blast radius)은 틀렸을 때의 비용을 정한다 —
다른 축이다.** 그래서 폭발 반경(blast radius) high-stakes(인증·인가, 결제·금액 계산, 데이터 삭제·변경,
외부 API, 동시성)가 감지되면 기어 권장과 별개로 **적대적 리뷰 1회가 기어와 무관하게**
실행되고, 그 diff 기준점이 될 HEAD 해시를 진행 기록에 남겨야 한다.

#### 진행 표기 규칙 (기어 무관 — 정본)

**체크박스는 커밋과 동기화된다: 표기는 그 커밋과 같은 커밋에 들어가고, 그 커밋에 담긴
만큼만 표기한다.** 기어마다 커밋
단위가 달라서 결과가 달라 보일 뿐이다.

| 기어 | 커밋 단위 | 그래서 표기 |
|---|---|---|
| low | R / G / B 각각 별도 커밋 | 각 커밋에서 그 단계를 표기 |
| mid | 테스트 1개의 RGB가 한 커밋 | 그 커밋에서 R·G·B를 한 번에 표기 |
| high | **use case 전체를 3단계로 나눠 커밋: 전체 Red→`test:`, 전체 Green→`feat:`, 전체 Blue→`refactor:`** | Green 커밋에서 use case의 모든 테스트를 한 번에 `[x]`로 표기 |

**high의 커밋 단위는 use case 내 3-phase다** — use case에 속한 모든 테스트의 Red
변경을 한 커밋(`test:`)에, Green 변경을 한 커밋(`feat:`)에, Blue 변경을 한 커밋
(`refactor:`, tidying이 불필요하면 생략)에 담는다. 테스트 단위가 아니라 **phase
단위**로 묶는다 — "이 use case가 무엇을 보장하는가"(Red) → "어떻게 최소 구현으로
통과시켰는가"(Green) → "구조를 어떻게 정리했는가"(Blue)가 각각 하나의 리뷰 단위가
된다. 에이전트는 커밋하지 않고 `git add`까지만 수행하며(커밋 보류), 오케스트레이터가
각 phase가 use case의 모든 테스트에 대해 끝날 때마다 커밋한다. body에는 그 phase에서
그 use case 전체에 걸쳐 내린 결정들을 `docs/reviewable-commits.md` 표준대로 담되,
길이는 `../../references/commit-style.md`의 간결성 규칙(제목 + 핵심 bullet 2~4줄)을 따른다.
실행 절차는 "use case 완료 시" 섹션 참조.

이 규칙은 "Red 커밋에 테스트 파일과 문서 갱신을 같은 커밋에"(`tdd-red`)의 일반형이다.
표기가 커밋과 불일치하는 순간 진행 기록이 실제와 어긋난다(드리프트).

**단, 완료 판정에 그대로 쓰지 않는다.** 현재 포맷은 테스트당 체크박스가 하나라 R/G/B를
구분해 적을 자리가 없다 — low 기어에서는 Red 커밋이 그 하나를 채우므로, **마지막
테스트가 Red만 된 상태에서도 "모두 `[x]`"가 성립한다.** high 기어도 같은 간극이
생긴다 — **use case 전체의 Red 커밋(`test:`) 시점에는 모든 테스트가 아직 실패 상태이므로
체크박스는 전부 `[ ]`로 남는다.** Green 커밋(`feat:`) 시점에 비로소 전부 `[x]`로
일괄 갱신한다. 완료는 체크박스가 아니라 **전체 스위트 green**으로 판정한다(mid는
한 커밋에 G·B가 함께 담기므로 이 간극이 없다).

### 배움 반영 게이트 (Spec Anchored)

구현 중 앵커 문서(규칙·예제)와 어긋나는 배움을 발견하면 코드보다 앵커를 먼저
갱신하고 같은 커밋에 담는다. 규칙이 바뀌는 배움만 사용자에게 질문한다.
절차·기준은 `../../references/anchor-update.md`가 정본.

### Principles

#### 설계의 두 축과 Test Desiderata

**phase마다 다른 설계를 한다**: Red = 인터페이스 설계("이 행위가 외부에서 어떻게
호출되어야 하는가"), Green = 설계 없음·오직 동작, Blue = 구현 설계("내부적으로 어떻게
구현할 것인가"). 이 셋을 섞지 않는 것이 사이클을 도는 이유다.

**테스트 품질의 기준**: "Tests should be coupled to the **behavior** of code and
decoupled from the **structure** of code."

Kent Beck 인용 원문, phase별 상세, Test Desiderata 12가지 속성 전체 표는 이 스킬
디렉터리의 `references/test-design-principles.md`가 정본이다 — 처음 이해할 때, 또는
phase 구분이 흐려졌다고 느낄 때 `Read`로 읽는다. (`tdd-plan`이 참조하는 정본이기도 하다.)

---

#### Mocking 가이드라인

판단에 바로 쓰는 규칙만 둔다. 근거·인용·안티패턴 전체 목록·테스트 더블 분류는
이 스킬 디렉터리의 `references/mocking-guide.md`를 `Read`로 읽는다.

**무엇을 대체하는가 — 역할(role)이지 객체가 아니다.**

| 대체해도 되는 것 | 대체하면 안 되는 것 |
|---|---|
| 다른 application service | 내부 구현(리팩토링으로 생긴 협력자) |
| driven port(경계 인터페이스) | adapter — port를 대체하지 adapter를 대체하지 않는다 |
| 아직 구현 안 된 API 경계(설계 목적) | 소유하지 않은 타입(3rd party) — 얇은 추상화로 감싼다 |
| 생성 비용이 크거나 공유되는 자원 | 데이터 객체(Entity·Value Object) — 실제 객체를 쓴다 |

**무엇으로 대체하는가 — Fake를 먼저 고려한다.** stubbing(when) 대신 `save()`,
verify 대신 `findAll()`로 실제 결과를 검증한다. 영속성 계층에서 특히 그렇다.
Mock은 상호작용 검증이 요구사항일 때만 쓴다.

**경계 객체 자체는 모킹하지 않고 통합 테스트한다.** UserService를 테스트할 때
UserRepository를 대체하고, UserRepositoryImpl은 실제 DB로 테스트한다.

**단위(unit)는 동작(behavior)의 단위다.** 격리 대상은 SUT가 아니라 테스트다
("the unit of isolation is the test not the thing under test"). 테스트끼리
격리되어 있다면 단위 테스트가 DB나 파일시스템과 통신해도 된다.

**아래가 보이면 설계 신호다 — 테스트가 아니라 대상을 고친다.**

- mock이 mock을 반환한다 / mock이 너무 많다 → code smell
- static 메서드를 모킹해야 한다 → 그건 static이 아니어야 한다
- stub한 메서드를 verify한다 / 호출 횟수를 검증한다 → CQS 위반 의심
- 클래스 격리를 위해 모든 의존성을 mock으로 채운다 → 단위 개념 오해

**모킹 자체를 줄이는 설계**: 복잡한 로직을 순수 함수로 분리하면 stubbing·verify가
사라진다 (`segregate-functional-core` 스킬 참조).

## OUTPUT FORMAT

### 실행 흐름

#### Step 1: 현재 상태 확인

1. 구현 목록 확인 — web-app은 `.feature`의 `@pending` 시나리오 목록(각 Green이 자기
   시나리오 태그를 해제하는 이중 루프), general은 앵커 문서 `## 예제 (검산표)` 표의
   미구현 행(Degenerate→General로 이미 정렬됨)이 원천이다. 구현 중 발견되는 필요한 동작은
   발견 즉시 목록에 추가한다(`../../references/anchor-update.md`의 "테스트 목록 갱신")
   (`--full`로 작성한 경우 `../tdd-plan/references/full-plan.md`의 unit test 목록이 그 원천)
2. 첫 미완성 테스트(`- [ ]`) 식별
3. 현재 테스트 실행 상태 확인
4. **기어 결정**: `--gear` 파라미터 > 템플릿 문서의 기어 기록 > 기본 low 순으로 결정.
   `references/gears.md`를 `Read`로 읽어 폭발 반경(blast radius) 점검을 수행하고, high-stakes 영역이면 두 처방을 함께
   출력한다 — 한 단 낮은 기어 **권장**(사용자 결정)과 완료 시 적대적 리뷰 1회 **실행**
   (기어 무관). 경고를 출력한 경우 사용자의 기어 확정 응답을 기다린 뒤 진행한다.
   **적대적 리뷰가 예정되면**(high 기어이거나 폭발 반경(blast radius) high-stakes) 현재 HEAD 해시를
   진행 기록에 남긴다 — 리뷰 diff 기준점이다.
   `--gear`로 명시 지정되었거나 문서의 기존 기록과 다를 때만 진행 기록을 갱신 —
   `--gear` 미지정 + 기록 없음이면 low로 동작하되 문서는 변경하지 않는다(하위 호환).

#### Step 2: RGB 사이클 실행

**low·mid 기어**: 각 미완성 테스트(`- [ ]`)에 대해 아래 Red→Green→Blue 사이클을 반복한다.

**high 기어**: 테스트 단위로 사이클을 반복하지 않는다. use case에 속한 모든 테스트에
대해 Red를 전부 마친 뒤, 전부에 대해 Green을 마치고, 마지막에 Blue를 use case 범위로
한 번 수행한다 — 아래 Red/Green/Blue 단계 설명은 각 phase 내부에서 에이전트에게
위임하는 방식을 다루고, 전체 순서와 커밋 지점은 "use case 완료 시" 섹션(3-phase 실행
순서)이 정본이다.

##### Red 단계
- **tdd-red agent**에 위임
- 실패하는 테스트 작성 — Test Desiderata 준수
  (12가지 속성 전체는 `references/test-design-principles.md`)
- 테스트 추가 후 구현 방향을 즉시 결정할 수 없으면 Getting Stuck으로 간주 —
  tdd-green의 "Getting Stuck 복구 경로"(더 단순한 테스트로 후퇴 우선)를 따른다.
  후퇴 결정은 Red/Green 경계를 넘으므로 오케스트레이터가 인지하고 조율한다.
  후퇴가 발생하면 진행 기록에 남긴다(특히 mid/high 기어 자율 진행 중에는
  사용자가 최종 검토에서 볼 수 있도록)
- approved.txt 파일 생성 (필요 시)
- **low·mid**: 에이전트 내에서 `test:` 접두사로 커밋 수행 / **high**: 커밋 보류(`git add`까지만)
- **검토 지점이면 사용자 피드백 대기** (low: 매 phase 후 / mid·high: 대기 없이 다음 phase)

##### Green 단계
- **tdd-green agent**에 위임
- 최소 구현으로 테스트 통과 (Little Golf Game)
- TPP (Transformation Priority Premise) 적용
- Make-it-Work 전략 (Obvious / Fake it / Triangulation)
- 테스트가 성공하면 javadoc comment의 테스트 항목에 완료 표시('X')
- **low·mid**: 에이전트 내에서 `feat:` 접두사로 커밋 수행 / **high**: 커밋 보류(`git add`까지만)
- **검토 지점이면 사용자 피드백 대기** (low: 매 phase 후 / mid·high: 대기 없이 다음 phase)

##### Blue 단계
- **tdd-blue agent**에 위임
- Tidying Process — Composed Method 지향 리팩토링. 단계 목록과 순서는
  `../../agents/references/tidying-process.md`가 유일한 정본이다(여기서 재나열하지 않는다).
  Domain Logic 이동(다른 클래스로 옮기는 분리)은 Blue 범위 밖 — `/system-wide-refactoring` 전담.
- 변경이 있는 경우 **low·mid**는 에이전트 내에서 `refactor:` 접두사로 커밋 수행 /
  **high**는 커밋 보류(`git add`까지만)
- **검토 지점이면 사용자 피드백 대기** (low: 매 phase 후 / mid·high: 대기 없이 다음 phase)

##### 사이클 완료 시 (low·mid 기어 — 테스트 1개의 R→G→B 종료)

- **테스트 목록 갱신 확인** (다음 Red 전) — 세 에이전트 보고의 `목록 추가:` 필드를
  모은다. 자율 추가 항목은 문서에 행이 있는지 확인하고, 규칙이 바뀌는 항목은 사용자에게
  질문한 뒤 반영한다. 필드가 없는 보고는 그 에이전트에 재확인한다. 다음 Red는 갱신된
  목록에서 Degenerate→General 순서로 고른다
- **mid 기어**: 여기가 검토 지점 — 사이클 요약(테스트·구현·리팩토링)과 사이클 diff를 함께
  제시하고 사용자 피드백 대기. tidying 방향 지시(추가 리팩터링 지목)를 받으면 반영 후 재보고
- **기어 전환 점검** (low·mid): `references/gears.md`의 업/다운시프트 신호를 점검하고,
  감지 시 전환을 제안 — 전환을 제안한 경우 사용자 응답을 기다린 뒤 진행한다(제안만
  출력하고 지나가지 않는다). 사용자가 수락하면 템플릿 문서의 기어 기록을 갱신하고
  다음 사이클부터 새 기어 적용
- **폭발 반경(blast radius)이 사이클 도중 처음 감지되면**(그 영역에 이제야 진입) 두 처방을 그때
  적용하고, diff 기준점은 **이 작업의 첫 커밋의 부모**를 남긴다 — 감지 시점 HEAD를
  남기면 리뷰 diff가 그 이전 구현을 포함하지 못한다("리뷰 diff가 전체 구현을 포함해야 한다").
  이미 기록된 기준점이 있으면 갱신하지 않는다

##### use case 완료 시 (high 기어 전용 — 3-phase 실행 순서 + 커밋 지점)

high 기어는 use case를 테스트 단위가 아니라 **phase 단위(Red 전체→Green 전체→Blue 전체)**로
진행한다. 협력 객체가 다수 관여하는 use case에서도 phase를 끝까지 마친 뒤 실행한다.

1. **Red 전체** — use case의 미완성 테스트(`- [ ]`) 각각에 대해 `tdd-red`를 순차 위임한다.
   각 위임은 그 테스트 하나의 실패 테스트만 작성하고 **커밋 보류**(`git add`까지만). 모든
   테스트를 다 쓴 뒤 스위트를 실행해 신규 테스트 수만큼 의도한 실패인지 확인한다.
2. **커밋 1 (`test:`)** — `git add` 누락분 확인 후 커밋. subject
   `test(<범위>): <use case 이름> — 실패 테스트 작성`. body에는 이 use case가 검증하려는
   행동들과 테스트를 그 순서로 고른 근거(Gherkin·도메인 규칙과의 대응)를 담는다. 진행
   기록 체크박스는 아직 갱신하지 않는다 — 전부 `[ ]`로 남는다(아직 실패 상태이므로).
3. **Green 전체** — 같은 순서로 `tdd-green`을 순차 위임한다. 위임 prompt에 "**최대한
   절차적으로**"를 명시한다 — 이 phase는 추출·일반화를 하지 않고 통과만 시킨다(tdd-green의
   평소 최소 구현 원칙에 이 제약을 추가하는 것 — 정리는 Blue phase에서 한 번에 한다).
   커밋 보류. 전체 완료 후 스위트 전부 green을 확인한다.
4. **self-check (Green 커밋 전)** — 커밋할 diff가 이미 추출된 private 메서드·이름 붙은
   중간 변수를 여럿 갖고 있다면(Composed Method 형태), "Blue가 정리할 게 없다"로 넘기지
   말고 **Green 위임 자체를 의심한다** — `tdd-green`에 실제로 위임했는지, 참조 구현이나
   최종 형태를 그대로 옮겨 쓰지 않았는지 확인한다. 참조 구현을 참고하더라도 3단계 지시
   ("최대한 절차적으로")를 지켜 인위적으로 절차적인 형태로 만든 뒤 커밋한다 — 그래야
   Blue 단계가 실제로 할 일이 생기고 refactor: 커밋이 의미를 갖는다.
5. **커밋 2 (`feat:`)** — `git add` 후 커밋. subject `feat(<범위>): <use case 이름>`.
   body에는 왜 이 구현을 택했는지·배제한 접근을 결정별로 담는다. **진행 기록의 그 use
   case에 속한 모든 체크박스를 `[x]`로 갱신해 같은 커밋에 담는다.**
6. **Blue 전체** — `tdd-blue`에 이 use case 범위 전체(커밋 2 이후 변경된 파일 목록)로
   위임한다. Composed Method 지향 Tidying Process를 적용. 커밋 보류. 적용 후에도 스위트
   green 유지를 확인한다.
7. **커밋 3 (`refactor:`)** — 변경이 있으면 `git add` 후 커밋. subject
   `refactor(<범위>): <use case 이름> — tidying`. body에는 tidying이 무엇을 드러냈는지.
   **변경이 없으면(이미 깔끔하면) 커밋 3은 생략한다.**
8. **추가 항목 pass** — 1·3·6의 에이전트 보고에서 `목록 추가:` 항목을 모은다. 규칙이 바뀌는
   항목은 사용자에게 질문해 확정한다. 확정된 추가 행이 있으면 그 행만 대상으로 1~7을 한 번
   더 실행한다(커밋 최대 3개 추가, subject에 "추가 항목" 명시). 추가가 없을 때까지 반복한다

각 phase 내부(1, 3, 6)에서 테스트 사이 대기·피드백 요청은 없다. phase 경계에서도
대기하지 않는다 — 검토 지점은 여전히 "전체 테스트 목록 완료 + 적대적 리뷰 통과
후" 1회뿐이다.

**use case 경계를 넘겨 합치지 않는다** — 두 use case를 같은 phase 커밋에 담으면 "이
phase가 이 use case에 대해 무엇을 했는가"라는 리뷰 단위가 성립하지 않는다. 이것이 high 기어가
지키는 커밋 경계다.

**기어가 use case 도중 바뀌면**: high→다운시프트 시 그때까지 stage된 변경을 진행 중이던
phase 기준으로 그 자리에서 한 번 커밋하고(불완전한 use case임을 body에 명시) 낮은 기어의
커밋 단위로 이어간다. →high 업시프트는 이미 커밋된 phase를 그대로 두고, 그 시점 이후
phase부터 3-phase 커밋으로 모은다.

#### Step 3: 완료 처리
- 체크박스 확인 (`- [x]`) — 표기는 각 커밋에서 이미 끝났어야 한다("진행 표기 규칙"
  참조). 아직 `- [ ]`인데 대응 커밋이 있으면 그 커밋에서 누락된 것이므로 여기서 채우고,
  왜 불일치했는지 확인한다
- **완료 판정은 체크박스만으로 하지 않는다** — low 기어에서는 마지막 테스트가 Red만
  된 상태에서도 "모두 `[x]`"가 성립한다. 전체 스위트 green을 함께 확인한다
- **high 기어면 미커밋 변경이 없는지 확인한다** — `git status`가 깨끗해야 한다. 남아 있으면
  마지막 phase(test:/feat:/refactor:)의 커밋이 누락된 것이므로 여기서 커밋한다
- 작업 내역을 마크다운 파일에 반영
- **완료 판정 전 대응 점검 (모든 기어)** — 미구현 행 0개(사이클 중 추가 행 포함) +
  `## 규칙` 모든 번호가 테스트 1개 이상과 대응하는지 확인한다. 대응 없는 규칙은 미구현
  행으로 추가하고 Step 2로 돌아간다. 정본은 `../../references/anchor-update.md`의
  "완료 판정 전 대응 점검"
- **진행 기록 대조 (모든 기어)** — 전체 완료 시, 체크된 항목과 실제 테스트 코드를
  한 번 대조한다. 체크 안 된 항목을 검증하는 테스트가 이미 있거나, 체크됐는데 대응
  테스트가 없으면 그 자리에서 바로잡는다. 1차 방어는 Red 커밋의 원자성이지만
  (`tdd-red`의 "테스트 파일과 체크박스 갱신을 같은 커밋에"), 리팩터링 중 테스트가
  이동·통합되면서도 어긋나므로 완료 시점에 한 번 더 대조한다. **드리프트는 기어와
  무관하게 발생하므로 이 대조는 low·mid·high 모두에서 수행한다**
- **Web App이면** 추가 단계(인수 테스트 완료 확인·JPA Repository 완성·DSL 개선)를
  수행한다 — `references/web-app-finish.md`
- **high 기어였거나 폭발 반경(blast radius) high-stakes였다면**: 최종 사용자 검토 **전에** 적대적
  리뷰를 실행한다 — `references/adversarial-review.md`. Web App이면 위 추가 단계를
  마친 뒤에 실행한다(리뷰 diff가 전체 구현을 포함해야 하기 때문). green 스위트 +
  적대적 리뷰 통과가 이 경우의 Definition of Done. high 기어라면 최종 검토 보고에
  표본 정독 대상으로 대표 슬라이스 하나(가장 복잡했거나 후퇴가 있었던 것)를 추천해 함께 제시
- **하드닝 제안 (실행 아님, 모든 기어)**: 최종 검토 보고 마지막에
  `references/hardening-gate.md`를 `Read`로 읽어 그 규칙대로 제안 블록을 추가한다 —
  CRAP·DRY(빠름, 변경 파일 한정)와 mutation(느림, 파일 1개)을 사용자가 복사해 실행할
  수 있는 명령으로. 블록 안의 순서는 비용순이 아니라 **파이프라인순**이다 —
  ①CRAP·DRY(정리할 곳 찾기) → ②`/system-wide-refactoring`(정리) → ③mutation(정리된
  코드에). ②가 뮤턴트 지점을 바꾸므로 ③이 마지막이다. 적용 조건(Java·src/main 변경 존재, CRAP·mutation은
  추가로 Maven 필요) 미충족 시 생략 사실만 한 줄 보고. **자동 실행 금지.**
- **세션 프로파일 안내 (전체 완료 시, 모든 기어)**: 하드닝 제안 다음 줄에
  "`/tdd-profile` — 이 세션의 단계·에이전트별 시간·토큰과 model/effort 조정안" 한 줄을
  추가한다. 실행은 사용자가 한다(transcript 사후 분석이라 세션이 끝난 뒤가 정확하다)
- 다음 테스트 안내 또는 전체 완료

---

### 작업 내역 기록 형식

각 테스트를 구현할 때마다 템플릿 문서에 작업 내역을 남긴다 (Step 2의 사이클과 함께 수행):

- 각 테스트에 대한 작업 내역을 `### n.x` 레벨로 추가
- multiline git commit message 수준으로 작성
- "gutter test 추가"처럼 제목을 작성하고, 빈칸 넣고, 주목할 내용 2~3줄
- code는 markdown 파일에 추가하지 않음

---

### 조건부 절차 — references

아래 절차는 조건이 맞을 때만 실행되므로 본문에 두지 않는다. 해당 시점에 `Read`로 읽는다.

| 절차 | 언제 | 정본 |
|---|---|---|
| **적대적 리뷰** | high 기어 **또는** 폭발 반경(blast radius) high-stakes. 전체 green 후, 최종 사용자 검토 **전** | `references/adversarial-review.md` |
| **Web App 추가 단계** | Web App이고 모든 테스트 완료 후 (인수 테스트 확인·JPA Repository 완성·DSL 개선) | `references/web-app-finish.md` |
| **하드닝 제안 (실행 아님)** | 전체 완료 처리(Step 3) 시, 최종 검토 보고 마지막 (모든 기어) | `references/hardening-gate.md` |

둘 다 해당하면 **Web App 추가 단계를 먼저** 마친 뒤 적대적 리뷰를 실행한다 — 리뷰
diff가 전체 구현을 포함해야 하기 때문이다.

`references/adversarial-review.md`는 `tdd-feature`가 그대로 참조하는 정본이기도 하다.

## FAILURE CONDITIONS

### 단계별 검증 체크리스트

#### 1. 테스트 작성 후 확인

- [ ] 테스트가 명확한 하나의 동작만 검증하는가?
- [ ] 테스트 이름이 검증하려는 내용을 명확하게 설명하는가?
- [ ] approved.txt 파일이 필요한 경우 작성되었는가?
- [ ] 테스트가 실행되고 예상대로 실패하는가?

#### 2. 구현 후 확인

- [ ] 테스트를 통과하는 가장 단순한 구현인가?
- [ ] make-it-work-strategy, TPP 규칙의 단계를 적절히 적용했는가?
- [ ] 불필요한 코드가 없는가?
- [ ] 모든 테스트가 통과하는가?

#### 3. 리팩토링 후 확인

- [ ] 중복이 제거되었는가?
- [ ] 코드가 더 명확해졌는가?
- [ ] 모든 테스트가 여전히 통과하는가?

#### 4. 전체 과정 후 확인

- [ ] 작업 내역이 마크다운 파일에 반영되었는가?
- [ ] 다음 단계 진행을 위한 피드백을 요청했는가?
- [ ] (모든 기어) 진행 기록의 체크박스와 실제 테스트가 일치하는가?
- [ ] (모든 기어) 사이클 중 발견한 필요한 동작이 목록에 추가되었고, 모든 규칙이 테스트와 대응하는가?
- [ ] (high 기어 **또는** 폭발 반경(blast radius) high-stakes) 적대적 리뷰를 실행하고 결과를 보고했는가?
- [ ] (high 기어 **또는** 폭발 반경(blast radius) high-stakes) 시작 커밋 해시가 진행 기록에 있는가?
- [ ] (high 기어) 커밋이 test:/feat:/refactor: 3-phase(tidying 불필요 시 2-phase)로 남았고,
  `git status`에 미커밋 변경이 없는가?
- [ ] (모든 기어) 하드닝 제안 블록을 최종 검토 보고에 붙였는가(적용 조건 미충족 시
  생략 사유 한 줄)? 하드닝 도구를 **자동 실행하지 않았는가**?
- [ ] 앵커와 어긋난 코드 변경을 앵커 갱신 없이(또는 다른 커밋으로) 커밋하지 않았는가?
