---
name: tdd-plan
description: TDD Planning (Spec Anchored) - 얇은 앵커 문서(규칙 + 예제 검산표 + 미확정)를 에이전트 1회 + 사용자 리뷰 1회로 작성. --full로 3단계 풀 플로우(도메인 규칙→예시→테스트 목록). "TDD 계획 문서", "앵커 문서 작성", "테스트 목록 뽑아줘", "plan 세우고 TDD", "/tdd-plan" 요청 시 사용. 단, 요구사항 원천 문서를 먼저 만드는 것은 /tdd-plan-input, plan 합의 후 자율 구현까지는 /tdd-feature가 적합. /tdd-plan [plan-doc-path] [--full]로 호출.
argument-hint: "[plan-doc-path] [--full]"
allowed-tools: Write, Edit, Read, Bash(git add:*), Bash(git commit:*), Bash(git status:*)
---

# TDD Planning Skill (Spec Anchored)

얇은 앵커를 만들고, 구현 기간 동안 갱신 대상으로 유지한다. 앵커 = 규칙(한 줄씩) +
예제 검산표(값의 정본) + 미확정. 시나리오의 실행되는 정본은 `.feature`다
(`/cucumber-acceptance`) — 앵커 문서에 Gherkin 사본을 두지 않는다.

구현 중 배움은 `../../references/anchor-update.md`의 게이트로 앵커에 먼저
반영된다 — plan은 변경 가능함이 최우선 원칙이다.

## GOAL

- **성공 = 템플릿 문서의 앵커 섹션(규칙·예제·미확정)이 채워지고 사용자 리뷰 1회를
  통과하며, (web-app) E-1 인수 셋업·E-2 Walking Skeleton으로 이어짐**
- 승인 왕복은 기본 1회 — 앵커 초안 리뷰. 미확정 항목 질문은 그 리뷰에 함께 담는다
- CancelOrder급 도메인에서 앵커 문서 100줄 이하

## 기본 플로우 (경량)

1. **`tdd-anchor-drafter` 에이전트 1회 호출** — plan-input 문서(있으면)·템플릿 문서
   경로를 전달. 규칙·예제 검산표·미확정을 문서에 채우고 `.feature`용 Gherkin 초안을
   반환받는다
2. **사용자 리뷰 1회** — 앵커 내용 + Gherkin 초안 + 미확정 질문을 한 번에 제시.
   수정 요청이면 에이전트 재호출 또는 메인이 직접 반영
3. **커밋** — `git add [변경 파일]` (git add -A 금지) →
   `git commit -m "docs: 앵커 작성 - [기능명]"` → 체크박스 갱신
4. **(web-app) E-1: 인수 테스트 셋업** — 리뷰에서 승인된 Gherkin 초안 전문을
   `/cucumber-acceptance` 위임 prompt에 포함해 전달한다(앵커 문서에 사본을 두지
   않으므로 대화에만 있는 전문을 그대로 넘긴다). `.feature` 생성 후 앵커 문서
   `## 미확정` 위나 문서 상단에 `.feature 경로: <경로>` 한 줄을 추가한다(사본이
   아니라 포인터). 리뷰 승인과 E-1 사이에 세션이 끊기면 Gherkin이 대화에만
   남으므로, 승인 직후 지체 없이 E-1을 실행한다
5. **(web-app) E-2: Walking Skeleton** — `tdd-skeleton-builder` 위임 (아래 참조)
6. **다음 단계 안내** — 기어에 맞는 `/tdd-rgb` 또는 `/tdd-feature` 호출 안내.
   구현 중 배움 반영 규약은 `../../references/anchor-update.md`가 정본

### 경량 모드에 없는 것

- Unit test 목록 단계 — Gherkin이 포함하지 못하는 세밀 분기는 구현 중 발견 시
  앵커 `## 규칙`에 한 줄 추가로 대체 (배움 반영 게이트)
- critic 검증 — 사용자 리뷰 1회가 그 역할
- 단계별 승인 왕복 — 리뷰는 1회다

## --full 플로우

high-stakes(인증·결제·데이터 삭제·외부 API·동시성 등 폭발 반경(blast radius) 큰 도메인)·대형·
다팀 작업에서 사용자가 명시적으로 선택한다. 절차는
`references/full-plan.md`가 정본 — tdd-domain-modeler → tdd-example-designer →
tdd-test-list → tdd-plan-critic, 단계별 승인.

## CONSTRAINTS

#### Act-Assert 동일 추상화 수준 규칙

- 테스트에서 act와 assert는 같은 추상화 수준에서 이루어져야 함
- 한 테스트 내에서 서로 다른 추상화 레벨 혼합 금지
- api를 호출하여 행동을 수행하고, 같은 api 레벨에서 결과를 검증
- 예: post로 생성하고 get으로 검증하는 방식 — 단, **그 post가 실제 인수 조건일 때만**이다.
  시나리오가 요구하지 않는 쓰기 API를 검증 편의를 위해 만들지 않는다(단계 E-2의
  "인수 조건에 없는 API를 지어내지(invent) 않는다" 참조). 이때는 given을 Repository 시드로 두고
  읽기 경로만 같은 레벨에서 검증한다

#### 조용한 실패 — 관찰된 정상 상태는 의도된 설정을 보증하지 않는다

**눈에 보이는 정상 신호(로그가 나온다 · 테스트가 통과한다 · 문제가 안 생긴다)를
"설정이 맞다"의 증거로 오독**하는 사례 4건:

| 신호 | 오독 | 사실 |
|---|---|---|
| SQL 로그가 나온다 | p6spy 설정이 맞다 | 키를 틀려도 기본값으로 로그는 나온다 (단계 E-2) |
| 테스트가 통과한다 | 그 검증이 일어났다 | 트랜잭션·어노테이션 위치 때문에 검증이 공허할 수 있다 (5단계 계약 테스트) |
| 설정 항목이 없다 | 그 기능은 꺼져 있다 | `open-in-view`의 부재는 off가 아니라 on이다 (영속성 경계) |
| 그 파일이 커밋된 적 없다 | 커밋이 차단되어 있다 | 우연히 안 들어갔을 뿐, 규칙이 없으면 언제든 들어간다 (승인 산물) |

**공통 처방**: 정상으로 보이는 상태를 근거로 삼지 말고, **틀렸을 때 무엇이 달라지는지를
확인한다.** 로그는 출력 유무가 아니라 형태 차이로, 테스트는 보호 장치를 제거한 실패
주입으로, 설정은 명시 여부로, 규칙은 파일 존재가 아니라 규칙 자체의 존재로 판정한다.

#### 도구는 최초로 필요해진 시점에 추가한다

관측·검증 도구(p6spy, approvaltests 등)를 초기 셋업에 미리 넣지 않는다. 세 가지 이유:

1. **thinnest 원칙과 충돌** — Walking Skeleton은 "실제 기능의 가장 얇은 슬라이스"인데,
   쓰지도 않을 관측 인프라를 추가하면 얇지 않다. skeleton이 검증해야 할 인프라
   변수를 늘리는 일이다
2. **의존성마다 비용** — p6spy는 Spring Boot 메이저 버전에 의존하고, 어긋나면 자동
   설정이 **조용히** 적용되지 않는다(단계 E-2). 안 쓰는 도구의 함정까지 관리할 이유가 없다
3. **도입 커밋에 Why가 남는다** — 필요해진 시점에 넣으면 "무엇 때문에 필요했나"가
   커밋에 기록된다. 초기 셋업에 일괄 포함되면 나중 사람은 알 수 없다

**트리거를 언제 관찰 가능하게 써야 하는가** — 실패가 즉시 감지되는지로 갈린다:

| | 없을 때 | 알아차리는가 | 그래서 |
|---|---|---|---|
| OSIV를 끄지 않음 | 경계 밖 지연 로딩이 조용히 성공하고 그 위에 코드가 누적된다 | **아니오** | **미룰 수 없다 — 항상 명시** |
| p6spy 없음 | 바인딩 값을 봐야 하는 순간 `?`만 보인다 | **예, 그 자리에서 감지된다** | 미뤄도 된다 — 주관적 트리거로 충분 |

**감지되지 않는 실패는 미룰 수 없고, 즉시 감지되는 실패는 미뤄도 된다.**

트리거 예:

- **approvaltests** — 첫 다중 값 검증(코드에서 관찰 가능)
- **p6spy** — ① `JdbcTemplate`·native query 등 **JPA를 거치지 않는 데이터 접근 경로가
  처음 등장할 때**(`show-sql`은 이 경로를 아예 못 본다 — 코드 리뷰로 탐지되는 신호)
  ② 바인딩된 파라미터 **값**이 원인 후보인 디버깅을 시작할 때(주관적이어도 안전)

이 규칙은 **새로 넣을 때의 시점**을 정한다. 이미 들어가 있는 도구를 제거하라는 뜻이
아니다 — 제거는 별도 판단이다.

## Web App 추가 단계

> 다음 단계들은 TDD 유형이 `web-app`일 때만 진행합니다.

#### 단계 E-1: 인수 테스트 셋업 (.feature + Runner) — `/cucumber-acceptance` 위임

리뷰에서 승인된 Gherkin 초안을 `.feature` + Runner로 실행 가능하게 만든다. 이 계층이 external
behavior의 주 검증층이므로 별도 High Level Test(JUnit)를 두지 않는다 — 같은 검증이 두
계층에 중복되면 안 된다. 미구현 시나리오는 `@pending`으로 실행에서 제외하고, 각 Green이
자기 시나리오의 태그를 **같은 커밋에서** 해제한다(일괄 활성화 단계는 없다).

`/cucumber-acceptance`를 호출한다 — 그 스킬이 대상을 파악한 뒤 `tdd-acceptance-builder`
에이전트에 실제 구축(Four Layer 셋업 + 커밋)을 위임한다. 세부(Four Layer 구조, Approvals
배치, DSL 개선 목표, 탈출구)는 그 스킬과 `references/web-app-acceptance.md`가 정본이므로
여기서 재기술하지 않는다.

---

#### 단계 E-2: Walking Skeleton 구현 — `tdd-skeleton-builder` 위임

실제 HTTP → 실제 앱 → **실제 DB(docker MySQL)**를 관통(end-to-end)하는 가장 얇은 슬라이스를 세운다.
real(실행 경로가 진짜인가)과 thinnest(기능이 얇은가)는 다른 축이다 — DB를 in-memory로
대체하면 real 위반이고, 합산·할인 같은 비즈니스 규칙이 들어가면 thinnest 위반이다.

**`tdd-skeleton-builder` 에이전트에 위임한다** — 승인된 앵커 문서 경로(어떤 HTTP 요청이
인수 조건인지 판단 근거) + E-1에서 `tdd-acceptance-builder`가 확정한 Target Design을
전달한다. 이 단계에서 함께 확정되는 불변 규칙(에이전트가 판단·적용하는 것 — 미루면 우회가
누적된 뒤에 되돌려야 한다):

- `spring.jpa.open-in-view: false`를 **명시**한다. 항목이 아예 없으면 Spring Boot 기본값
  `true`가 적용된다 — **부재는 off가 아니라 on이다**(위 "조용한 실패" 참조).
  OSIV는 도입 시점을 판단할 항목이 아니라 JPA를 쓰는 순간부터 off다
- 트랜잭션 경계는 Controller에 둔다(이 단계 한정, 조회는 `@Transactional(readOnly = true)`).
  경계만을 위해 서비스 계층을 새로 만들지 않는다
- 연관관계는 LAZY를 유지한다 — 예외가 발생하는 지점마다 EAGER로 바꾸는 것은 우회이고, 목록 조회가
  생기는 순간 N+1이 된다. 필요한 지점에서 fetch join·`@EntityGraph`로 명시적으로 로딩한다
- Controller 반환 타입은 엔티티가 아니라 DTO다 — OSIV를 끈 상태에서 엔티티를 반환하면
  JSON 직렬화가 트랜잭션 **밖**에서 일어난다. 이 실패는 테스트에 안 보인다(클래스 레벨
  `@Transactional` 안에서 직렬화가 끝나므로 테스트는 초록색, 실서버만 500)

세부(profile 구조, Docker Compose 설정, SQL 로깅과 p6spy 도입 시점, 영속성 경계의
근거·명시적 `save()` 가드와 적용 순서·계약 테스트)는 에이전트가
`references/web-app-skeleton.md`·`references/web-app-persistence.md`를 정본으로 참조한다.
완료 후 에이전트가 확정한 영속성 경계 결정을 보고받아 이후 RGB 사이클에 전달한다.

## FAILURE CONDITIONS

- 앵커 문서에 산문 계층(정본 선언·INVEST·제외 근거)이나 Gherkin 사본을 씀
- 경량 모드에서 3 에이전트(domain-modeler·example-designer·test-list) 또는
  critic을 호출함
- 사용자가 --full을 선택하지 않았는데 unit test 목록 단계를 진행함
- 승인 왕복이 리뷰 1회 + 미확정 질문을 초과함 (사용자가 수정을 요청한 경우 제외)
