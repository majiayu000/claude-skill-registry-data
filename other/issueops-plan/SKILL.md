---
name: issueops-plan
description: Prepare the plan, reviews, and canonical worktree for an IssueOps cycle, then hand off through Herdr when available, otherwise continue in the current session. Use when "issueops next" reports plan.architecture, plan.write, plan.review, or plan.handoff, or when the user says "아키텍처 정해줘", "계획 세워줘", "계획 검토해줘", "구현 인계".
---

# IssueOps Plan

이 스킬의 일은 **아키텍처를 먼저 정하고, 그 위에 구현할 수 있는 계약을 만들어 구현 세션에 넘기는 것**이다. 구현은
하지 않는다. 워크트리를 먼저 준비하고, 환경별 자동 세션 인계로 구현에 넘긴다.

- 전체 흐름과 단계 판별: [`issueops`](../issueops/SKILL.md)
- 계획 작성: [`implementation-planning`](../implementation-planning/SKILL.md)
- 적대 리뷰(아키텍처 문서와 계획): [`issueops-review`](../issueops-review/SKILL.md)
- 게이트 원장: [`gates-ledger`](../gates-ledger/SKILL.md)
- 프로젝트 문서 갱신 절차: [`project-docs-update`](../project-docs-update/SKILL.md)
- 다음 단계: [`issueops-implement`](../issueops-implement/SKILL.md)

## 이 스킬이 맞는지 확인

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

`stage.key`가 `plan.architecture`, `plan.write`, `plan.review`, `plan.handoff` 중 하나면 이
스킬이다. 네 값은 이 스킬 안의 어느 절부터 시작할지를 말한다. 순서는 이 표기 그대로이고,
아키텍처가 승인되기 전에는 계획 단계로 넘어가지 못한다. 계획이 먼저 스테이징돼 있어도
`next`는 `plan.architecture`를 돌려준다. `prepare`면
[`issueops-prepare`](../issueops-prepare/SKILL.md)가 먼저다.

## 어디에서 실행하는가

이 단계는 **source checkout의 준비 세션**이 수행한다. 워크트리는 아직 없다. 워크트리를
만드는 것은 이 단계 끝의 `execution prepare`다. 준비한 뒤 환경별 자동 세션 인계를 적용한다.

그래서 아키텍처 문서와 계획 파일은 **source checkout 밖의 임시 파일**에 쓰고 `artifact stage`로
올린다. source checkout 안에 만들면 그 파일이 커밋 대상이 되고, 워크트리가 생긴 뒤에는
두 곳에 같은 문서가 존재한다.

`git worktree add`를 실행하지 않는다.

## 프로젝트 문서 확인

아키텍처를 쓰기 **전에** 이 변경을 제약하는 운영 문서를 읽는다. 아키텍처와 계획을 다 쓰고 나서
읽으면 이미 내려진 결정을 되돌리게 된다.

```bash
# MCP: project_docs_route에 이슈 제목과 구현 범위를 넣어 읽을 문서를 고른다.
# MCP를 쓸 수 없으면 같은 라우터를 CLI로 실행한다.
issueops project route-docs --repo "$SOURCE_ROOT" --task "<이슈 제목과 구현 범위>" --json
# MCP: project_docs_read로 각 문서의 현재 내용과 SHA를 읽는다.
```

route 결과는 아래 목록에 **더하는** 후보이고 목록을 대신하지 않는다. route가 무엇을 돌려주든
다음 여섯 문서는 직접 열고, 색인이 이 변경의 모듈을 가리키면 그 모듈 파일도 연다:
`CONSTITUTION.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `CAUTIONS.md`, `ADR.md`, `TESTING.md`.

읽은 결과는 계획의 `## 적용되는 결정과 주의사항` 절에(아키텍처 문서에도 해당하는 제약은 그 문서의 관련 절에) 위 여섯 문서와 route가 더한 문서마다
**한 줄씩** 적는다. 적용되는 항목이 있으면 규칙이 실제로 적힌 파일의 경로(색인이 모듈로 넘기는
규칙이면 색인이 아니라 그 모듈 경로), 항목 제목, 그 파일에서 그대로 옮긴 문장, 이 계획에 미치는
제약 한 문장을 쓰고, 열어서 대조했지만 해당 항목이 없으면 그 문서 경로와 "대조했으나 없음"을 쓴다.
route가 더한 문서를 열지 않기로 했으면 "열지 않음: <이 변경과 무관한 이유>"로 쓴다. "대조했으나 없음"은
실제로 연 문서에만 쓴다. 여섯 문서는 "열지 않음"을 쓸 수 없고, 한 줄이라도 빠지면 읽지 않은 것이다.
읽지 않은 것과 읽었는데 없는 것은 다르다.

이 절은 두 곳으로 흘러간다. 아키텍처 검토의 `--risk`에 그 제약이 들어가고,
`issueops-review`의 리뷰 프롬프트에 이 절이 들어가 리뷰어가 "무시된 결정"을
공격한다.

## 아키텍처 작성과 스테이징

계획보다 먼저 **아키텍처 문서**를 쓴다. 문서는 구현 순서가 아니라 구조와 경계에 대한 결정을
담는다. 저장 위치는 `$(mktemp -d)/architecture.md`처럼 source checkout 밖이다. 다음 다섯 절이
반드시 있고, 절마다 본문이 비어 있지 않아야 한다.

| 절 | 내용 |
|---|---|
| `## 요구사항과 규모` | 기능 요구사항과 비기능 요구사항(부하, 지연, 가용성), 필요할 때의 규모 추정 |
| `## 데이터와 API 계약` | 엔터티, 저장 위치, CLI·MCP·record 계약 |
| `## 구조와 흐름` | 구성 요소와 읽기·쓰기 경로. 재사용하는 기존 코드의 `파일:라인`을 함께 적는다 |
| `## 병목과 장애` | 단일 장애점, 의존성 실패, 대체 경로 |
| `## 절충점과 기각한 대안` | 선택한 방식, 기각한 대안, 기각한 이유 |

변경과 관계없는 절에는 "해당 없음: <근거>"를 쓴다. 근거 없이 비워 둔 절은 `architecture review`가
`architecture is missing required sections: <제목>`으로 거부한다. 제목은 `## ` 깊이로 정확히
써야 하고, `### ` 아래에 쓴 내용은 그 절의 본문으로 센다.

```bash
issueops artifact stage --id "$ISSUEOPS_ID" --name architecture --file "$TMP_ARCHITECTURE" --json
```

스테이징한 문서는 `artifact unstage --name architecture`로 내리거나 같은 이름으로 다시 올려
교체한다. 승인한 뒤 문서를 고치면 승인이 `architecture_review_stale`이 되므로 다시 검토한다.

## 아키텍처 검토

[`issueops-review`](../issueops-review/SKILL.md)를 `--target architecture`로 호출한다. 리뷰어는 빈
컨텍스트의 서브에이전트이고 [`architecture-review`](../architecture-review/SKILL.md)의 아키텍처
렌즈를 적용한다. 루프 절차는 그 스킬이 소유한다. `pass` 판정일 때만 승인을 기록한다.

```bash
issueops architecture review --id "$ISSUEOPS_ID" \
  --problem-summary "<문제>" --proposed-architecture "<아키텍처 결정>" --refactor-plan "<리팩터 계획>" \
  --alternative "<기각한 대안과 이유>" --risk "<위 문서 확인에서 온 제약>" \
  --verification "아키텍처 검토로 대안과 위험을 확인했다" \
  --reviewer-context subagent --approved $RECORD_ACTOR_FLAGS --json

issueops record-routing --id "$ISSUEOPS_ID" --phase plan --skill implementation-planning \
  $RECORD_ACTOR_FLAGS --json
```

- 승인은 스테이징한 아키텍처 문서의 sha256에 묶인다. 문서가 없거나 필수 절이 비면 기록이
  거부된다.
- `--verification`에는 "아키텍처"와 "검토"가 함께 들어가야 한다(영어면 "architecture"와
  "review"). 그 두 단어가 없으면 `architecture_review_evidence`가 통과하지 않는다.
- `--reviewer-context`는 `subagent` 또는 `inline`이며 감사 필드다. 하네스는 자기신고를 검증할 수
  없으므로 `inline`도 기록되지만, 저자 세션이 직접 검토한 기록은 리뷰가 아니라 규칙 위반이다.
  독립 서브에이전트가 돌려준 판정만 `subagent`로 기록한다.
- `--refactor-plan`, `--alternative`, `--risk`는 각각 하나 이상 필요하고, open question은
  0이어야 승인된다. 열린 질문이 남았으면 그것을 먼저 닫는다.
- `revise`면 문서를 고쳐 다시 스테이징하고 다시 검토한다. `stop`이면 승인을 기록하지 않고
  이슈 본문의 사실 변경을 `feedback add --classification contract_change`로 남긴 뒤 이슈를
  동기화한다.

## 계획 작성과 스테이징

승인된 아키텍처가 있어야 이 절로 넘어온다. [`implementation-planning`](../implementation-planning/SKILL.md)을
호출해 계획을 쓴다. 계획은 아키텍처에서 내린 결정을 실행 순서로 풀어 쓴다. 쓰다가 아키텍처를
바꿔야 하면 계획을 멈추고 `plan.architecture`로 돌아가 문서를 고치고 다시 검토한다.
저장 위치는 `$(mktemp -d)/plan.md`처럼 source checkout 밖이다.

계획에는 다음 네 절이 반드시 있다.

| 절 | 내용 |
|---|---|
| `## 적용되는 결정과 주의사항` | 위 문서 확인의 결과 |
| `## 재사용하는 기존 구현` | plan-prep의 코드베이스 조사에서 찾은 심볼·패키지·테스트 헬퍼와 재사용 방식. 새로 만드는 것이 있으면 기존 것으로 왜 안 되는지 |
| `## 성능 영향` | hot path 여부, 복잡도 변화, 측정 계획. 알고리즘 선택이 걸리면 [`algorithm-optimization`](../algorithm-optimization/SKILL.md) |
| `## 하위 호환성과 side effect` | CLI JSON·MCP schema·golden·record schema·provider body 계약, 기존 데이터, 롤백 경로. 마이그레이션·엔티티·인덱스·쿼리가 걸리면 [`database-design`](../database-design/SKILL.md)으로 정규화 판단·인덱스 계획·예상 row 수를 먼저 정하고 그 값을 여기 적는다. 7단계의 실측이 이 값과 대조된다 |

계획이 **LLM에게 주는 프롬프트 본문**을 바꾸면(서브에이전트·리뷰어 프롬프트,
`.issueops/prompt-engineering/`의 문서, SKILL 안의 프롬프트 템플릿 블록)
[`prompt-engineering`](../prompt-engineering/SKILL.md)으로 측정 가능한 출력 기준을 정해
`## 하위 호환성과 side effect` 절에 적는다: 무엇이 나오면 그 프롬프트가 실패한 것이고,
어떤 산출물로 확인하는가. 메인 에이전트가 읽는 절차 산문 변경은 해당 없다.

이 네 절은 형식이 아니라 판단이다. "재사용할 것이 없다"는 결론도 근거와 함께 적으면
유효하고, 근거 없이 비워 두면 리뷰가 그것을 공격한다. 절 제목 자체는 4단계의
`issueops link-plan`이 검사한다. 네 제목 중 하나라도 없는 계획은
`plan is missing required sections`로 연결이 거부되므로, 제목을 바꾸거나 합치지 않는다.

계획에 lifecycle ID, 사용자 요청 범위, 브랜치·worktree 준비 뒤의 환경별 자동 세션 인계,
승인된 종료점을 적어 인계받는 세션도 같은 경계를 알게 한다. 자동 인계는 사용자 요청 범위를
넓히지 않는다. 이미 읽은 plan-prep 조사와 문서는 변경이나
새 질문이 없으면 재사용한다. 작업 규모에 맞춰 필요한 검증 명령을 정하고, 같은 명령을
게이트와 별도 검증 목록에 중복 등록하지 않는다.

### 사실 주장 확인

계획이 **기존 동작에 대해 단언하는 문장**은 스테이징 전에 명령으로 확인하고
`파일:라인`을 인용한다. 확인하지 않은 단언은 계획에 쓰지 않는다.

대상은 계획이 "현재 이렇게 되어 있다"고 말하는 모든 것이다. 자주 틀리는 것들:

- 데이터가 어디에 저장되고 무엇을 키로 재사용되는가. "저장 데이터는 그대로"는
  저장 지점과 조회 키를 둘 다 읽기 전에는 쓸 수 없는 문장이다.
- 대상 spec이 내가 고치려는 서비스를 mock하는가. mock하면 그 안에 넣은 변경은
  그 spec으로 관측되지 않으므로 성공 기준을 검증할 수 없다.
- 재시도 횟수·타임아웃·상수의 실제 값과 그 곱. 최악 지연은 곱으로 계산한다. 대기나 재시도가
  제한 시간이 있는 경로(hook, 요청 처리, CI job) 안에서 돌면 그 경로의 설정 파일에서 바깥
  제한 시간을 찾아 최악 지연과 비교한다. 이슈나 사용자가 제안한 대기 시간을 평가할 때도 같다.
- 이 동작을 소비하는 호출부가 몇 곳인가. 센 것이 아니라 찾은 것을 적는다.
- 근거로 드는 ADR·선례가 실제로 그 주장을 뒷받침하는가. 제목이 아니라 본문을 읽는다.

이것은 리뷰어의 일이 아니라 저자의 일이다. 확인은 몇 분이지만 틀린 단언 하나는 리뷰
라운드 하나와 계획 전면 개정을 부른다. 적대 리뷰는 저자가 못 보는 설계 결함을 잡으라고
있는 것이지, 저자가 읽지 않은 코드를 대신 읽으라고 있는 것이 아니다.

확인할 수 없는 것은 단언하지 말고 미확인 가정으로 적는다. 그러면 리뷰어가 그 가정을
판별할 최소 확인을 요청할 수 있다.

```bash
issueops artifact stage --id "$ISSUEOPS_ID" --name plan --file "$TMP_PLAN" --json
```

`artifact stage`는 actor 플래그를 받지 않는다. `--id`, `--name`, `--file`, `--json`뿐이다.
잘못 올렸으면 `issueops artifact unstage --id "$ISSUEOPS_ID" --name plan --json`으로
내린다.

`link-plan`은 여기서 하지 않는다. 워크트리가 없어 `plan_in_worktree`를 만족할 수 없다.
prepare가 스테이징한 계획을 워크트리 안에 materialize하고, 4단계가 그것을 링크한다.

## 게이트 원장

계획의 수용 기준을 [`gates-ledger`](../gates-ledger/SKILL.md)의 형식대로 `G1..Gn`
(CHECK/EXPECT)으로 계획 안에 적어 둔다. 게이트마다 `gates init`에 그대로 넘길 한 줄 spec
(`- G1: <결과> | CHECK: <명령> | EXPECT: <기대>`)으로 쓴다. 원장 **파일**은 워크트리 안에 있어야 하므로
여기서 만들지 않는다. 4단계가 파일을 만들고 `--write`로 EVIDENCE를 채우며, 5단계가
정리 뒤 다시 채우고, 7단계는 증거 유효성을 확인해 읽거나 필요한 검사를 재실행한다.

게이트 중 적어도 하나는 이슈의 완료 조건, 곧 보고된 실패가 사라진 최종 상태를 직접 관측한다.
고치는 의존성을 fake로 바꾼 unit 테스트나 호출 순서만 확인하는 테스트는 그 게이트를 대신하지 못한다.
그 관측이 smoke 명령(실제 명령을 실행한 뒤 상태를 읽어 비교)이면 구현 단계나 측정 계획에만 적지 말고
게이트의 CHECK로 쓴다. 테스트로 관측하면 그 테스트가 무엇을 실제로 실행하고 무엇을 비교하는지 게이트
결과 칸에 적는다.

스테이징 전에 계획의 게이트를 실행 없이 검사한다. `problems`가 남은 계획은 스테이징하지 않는다.

```bash
issueops gates lint --plan "$TMP_PLAN" --cwd "$SOURCE_ROOT" --json
```

## 검토 루프

[`issueops-review`](../issueops-review/SKILL.md)를 `--target plan`으로 호출한다. 루프
절차는 그 스킬이 소유하므로 여기 복사하지 않는다. 이 단계가 알아야 하는 것은 셋이다.

- **입력**: 스테이징한 계획 전체. 위 `## 적용되는 결정과 주의사항` 절과 승인된 아키텍처 문서 전문이 함께 간다.
- **종료 조건**: `pass` 판정이 finding 하나 이상과 함께 기록됐다.
- **stop 판정**: 이 단계가 되돌린다.

```bash
issueops regress --id "$ISSUEOPS_ID" --reason "<리뷰 결론>" $RECORD_ACTOR_FLAGS --json
```

`regress`는 사이클을 grill로 되돌리고 아키텍처 승인도 지운다. 다시 조사하고 이슈 본문을 갱신한 뒤
`phase --to plan`으로 올라와 계획을 다시 쓴다. 판정은 계획 파일의 sha256에 묶이므로,
판정 뒤 계획을 고치면 `devils_advocate_review_stale`이 되어 인계가 막힌다. 고쳤으면
다시 검토한다.

검토가 이슈 본문의 사실(완료 기준, 범위, 원인 설명, 작업 구조)을 틀렸다고 판정하면
계획만 고치고 끝내지 않는다. 그 사실을 계약 변경으로 기록한다. 기록이 남으면 기존
게이트 `contract_feedback_issue_update`가 PR 준비를 막고, `sync-issue`로 본문을 고친 뒤
`feedback mark-issue-updated`를 기록해야 풀린다.

```bash
issueops feedback add --id "$ISSUEOPS_ID" --source plan-review --classification contract_change \
  --body "<이슈 본문에서 바뀐 사실>" $RECORD_ACTOR_FLAGS --json
```

## 인계

사용자 요청이 계획 작성·검토까지라면 여기서 계획과 검토 결과를 보고하고 종료한다.
아래 `execution prepare`, lease 발급, 새 세션 실행이나 구현 진입은 하지 않는다.
이 경우 아래 인계 후 검증 항목도 적용하지 않는다.

```bash
issueops execution whoami --json   # ACTOR_FLAGS 원문
issueops execution prepare --id "$ISSUEOPS_ID" $ACTOR_FLAGS --json        # preview
# preview가 보여 준 workspace root·branch·base를 확인한 뒤, 같은 요청에 --confirm만 더해 실행한다.
```

`--confirm`은 같은 세션에 lease를 부여하고 계획을 materialize한다. 반환된
workspace root, branch, 계획을 확인한 뒤
[`issueops`](../issueops/SKILL.md)의 **환경별 자동 세션 인계**를 적용한다.

[session-choice.md](../issueops/references/session-choice.md)에 따라 준비 세션이 Herdr 세션이면
Herdr의 서버·호환성·현재 native host 실행 가능 여부를 확인하고, 사용 가능하면 아래와 같은
release·새 세션 인계 절차를 적용한다.
현재 holder가 결정 기록, 인계 자료 봉인, writer 정리를 마친 뒤 release하고
같은 worktree에 새 세션 하나를 띄운다. 이때 새 쓰기 작업과 하위 작업 dispatch를 중지하고,
소유자, 실행 핸들, 입력 리비전, 쓰기 범위, 결과 위치, 읽기 작업인지 쓰기 작업인지의 분류,
대기 중인 writer가 0이라는 재확인, 자손 프로세스가 실제로 종료됐다는 관측, 늦게 도착한
결과는 격리했다는 기록을 인계 자료와 release 이전 증거로 남긴다.
새 세션은 자기 native actor로 `execution replace --id ID --expected-generation N --preview`를
실행하고, 반환된 `--reseed` 명령을 거쳐 `claim --claim-current-token`으로 lease를 넘겨받는다.
Herdr를 쓸 수 없으면 lease를 유지하고 현재 세션에서 구현으로 이어가거나, 사용자가 직접 연
두 번째 터미널에서 같은 인수 체인으로 수동 인계한다. Herdr는 기존 worktree를 열 뿐
재생성하지 않는다. 진행 방식을 묻지 않는다. 명시적인 보류·범위 제한은 우선한다.

## 의존성과 로컬 설정

워크트리가 생긴 뒤의 규칙이지만 계획에 함께 적는다.

의존성은 canonical worktree 안에서 저장소가 문서화한 설치 명령으로 준비한다. 크게
생성되는 의존성 디렉터리를 재사용하려면 패키지 매니저·lockfile·런타임·플랫폼·네이티브
모듈 상태가 모두 같은지 확인한 뒤에만 한다. 생성된 의존성 디렉터리나 심볼릭 링크를
커밋하지 않는다.

`.env`, `.env.local`, `.mcp.json`, `dbhub.toml` 같은 로컬 전용 설정은 작업에 필요하고,
원본이 ignore돼 있고, 어떤 secret도 프롬프트·로그·테스트·이슈 본문·PR/MR 본문에 들어가지
않을 때만 링크한다. 추적되는 파일, ignore되지 않은 파일, 설명되지 않은 자격 증명 파일은
링크하기 전에 멈춘다.

## 나쁜 예

| 나쁜 행동 | 왜 나쁜가 | 대신 할 일 |
|---|---|---|
| source checkout 안에 계획 파일을 만든다 | 커밋 대상이 되고 워크트리 생성 뒤 계획이 두 곳에 존재한다 | 임시 디렉터리에 쓰고 `artifact stage` |
| `git worktree add`를 실행한다 | `execution prepare`가 만드는 worktree와 경로·브랜치가 충돌한다 | `execution prepare`가 만들게 둔다 |
| 세션 인계를 위해 worktree를 재생성한다 | lease와 브랜치 identity가 새 worktree와 어긋난다 | 준비한 같은 worktree에서 환경별 자동 세션 인계를 적용한다 |
| 기존 동작에 대한 단언을 확인 없이 계획에 쓴다 | 저자가 몇 분이면 읽을 코드를 리뷰어가 읽게 되고, 틀린 단언 하나가 리뷰 라운드와 전면 개정을 부른다 | 스테이징 전에 명령으로 확인하고 `파일:라인`을 인용한다 |
| 아키텍처 없이 계획부터 쓴다 | 결정이 계획 전체에 퍼진 뒤에야 구조 결함이 드러나 계획을 다시 쓴다 | 아키텍처를 먼저 스테이징하고 승인받는다 |
| 승인한 아키텍처를 고치고 재검토를 생략한다 | `architecture_review_stale`로 계획 단계에 못 들어가거나, 검토되지 않은 구조가 계획에 들어간다 | 다시 스테이징하고 새 승인을 기록한다 |
| 리뷰 없이 `--verdict pass`나 `--approved`를 기록한다 | 게이트 연극이다 | `issueops-review`로 실제 리뷰를 돌린다 |
| revise 판정을 `--waive`로 닫는다 | 지적이 반영되지 않은 채 구현으로 간다 | 계획을 고치고 다시 검토한다 |
| 판정 뒤 계획을 고치고 재검토를 생략한다 | stale 판정으로 인계가 막히거나, 검토되지 않은 계획이 구현된다 | 다시 검토해 새 판정을 기록한다 |
| staged plan 없이 인계한다 | prepare가 워크트리에 materialize할 계획이 없다 | `artifact stage`를 먼저 한다 |
| 새 세션에 인계했는데 이 세션이 계속 구현한다 | 두 세션이 같은 워크트리를 쓴다 | Herdr 인계 전달을 확인하면 여기서 멈춘다 |

## 검증

- `issueops status --id "$ISSUEOPS_ID" --json`의 `architecture_review.approved`가
  true이고 `reviewed_architecture_digest`가 현재 아키텍처 문서의 sha256과 같으며, `devils_advocate_review.verdict`가 `pass`이며 그 digest가 현재 계획과 같다.
- `issueops next --id "$ISSUEOPS_ID" --json`의 `stage.key`가 `plan.handoff`
  이거나, 인계 뒤라면 `claim` 또는 `implement.enter`다.
- `git -C "$SOURCE_ROOT" status --short`에 계획 파일이 없다.
- 인계 뒤 `execution prepare` 결과의 `workspace.root`가 실제로 존재하고 그 브랜치가
  record의 브랜치와 같다.
