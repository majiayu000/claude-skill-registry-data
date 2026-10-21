---
name: issueops-implement
description: Run the implement stage of a linked IssueOps cycle with a generation-fenced execution lease, canonical-worktree TDD, a gate ledger for the RED and GREEN evidence, and delegated child cycles. Enter through link-plan, the compatibility review, and the ledger; exit by moving the cycle to ai-slop-clean. Use when "issueops next" reports implement.enter or implement, or when the user says "구현 시작", "구현 이어서 해줘", "이슈 구현해줘", "child로 나눠서 구현해줘".
---

# IssueOps Implement

**implement 단계 하나**를 맡는다. 승인된 plan을 canonical worktree에서 lease를 지키며
TDD로 구현하고 증거와 함께 ai-slop-clean으로 넘긴다. 승인된 종료점 전에는 완료로 끊지 않는다.

본문만 주입하거나 이 스킬만 복사해도 아래 계약을 적용한다. sibling 스킬은 설치되어
있을 때 협업에 쓰며, 없으면 이 본문과 CLI의 exact `next_command`로 진행한다.
필수 입력·명령을 확인할 수 없으면 그 지점을 보고하고 멈추며 evaluator 자료를 요구하지 않는다.
선택적 [실패 예시](references/implementation-examples.md)는 symlink를 해소한 이 파일 기준이다.

진행 순서: 시작 게이트 → lease·worktree 확인 → 직접 TDD 또는 child 위임 →
focused verification → 워크트리 안 report 초안 → `ai-slop-clean`.

## 시작 게이트

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

`stage.key`가 `implement.enter`나 `implement`면 이 스킬이다.
선택한 ID는 인계·압축 뒤에도 유지한다. `blocked.*`는 우회하지 않는다.
ID가 없고 후보를 구별할 근거가 없을 때만 사용자에게 선택을 묻는다.

- `claim`이면 `next_command`가 돌려주는 `execution claim --claim-current-token` 명령을
  정확히 한 번 실행하고 `next`를 다시 돌린다. released는 `replace --preview`, revoking은
  `replace --finalize-preview`로 시작하는 회복 체인을 따른다.
- `plan.*`이면 [`issueops-plan`](../issueops-plan/SKILL.md)이, `clean`이면
  [`issueops-slop-clean`](../issueops-slop-clean/SKILL.md)이 맞다.
- `none`이면 사이클이 아직 없다. [`issueops-create-issue`](../issueops-create-issue/SKILL.md)로
  시작한다. 상태만 보고하고 "진행 방향은 사용자 결정"으로 멈추는 것은 게이트 통과가
  아니라 라우팅 누락이다.

편집 대상을 실측한다.
```bash
issueops execution whoami --json
git -C "$WORKTREE" rev-parse --abbrev-ref HEAD
git -C "$WORKTREE" status --porcelain
```

holder/generation 불일치는 아래 회복 표를 따른다. branch·HEAD 불일치나 무관한 dirty 변경은 stop이다.

진입 전에 인계 결정 기록과 원래 요청의 승인 범위·종료점을 `status`로 대조한다.
새 세션은 이전 holder의 release 확인 후 자기 lease로 인수하며, 이미 인계받았으면
재인계하지 않는다. 보류·phase·claim·`--approved`는 구현이나 publication 승인이 아니다.
준비 세션은 같은 worktree에서 Herdr를 먼저 확인한다. 준비 세션이 Herdr 세션이고 실행 중인
서버·호환성·현재 native host 실행 가능 여부가 확인되면 Herdr로 인계한다. Herdr를 쓸 수
없으면 현재 세션에서 이어가거나, 사용자가 직접 연 두 번째 터미널에서 수동으로 인계한다.
설치만으로 ready라 판단하거나 실행 방식 메뉴를 묻지 않는다. 최신 명시적 current/new-session/hold가 우선한다.
인계 시 아래 writer 종료 규칙을 지키고 ID·generation·경로·요청/대화 근거·승인 범위·종료점,
목적/비목표·base/full HEAD·diff·계획 digest·검증 입력/명령/시각/환경/실패·미완료 결과 위치·
exact resume/조회 명령·자료 digest를 남긴다. secret/token은 제외한다. release/status로
해제를 확인한 뒤 현재 native host의 세션 하나만 열고 수신을 확인하면 기존 세션은 끝낸다.
런처 설치·worktree 재생성·모호한 launch 재시도는 금지한다. 세부 recipe가 있으면
[`session-choice.md`](../issueops/references/session-choice.md)를 사용한다.
인계문이 있으면 현재 HEAD, 계획 digest, 인계 자료 digest를 현재 worktree와 대조한다.
stale하거나 누락된 근거는 필요한 범위만 다시 확인한다. 서로 다른 host의 session ID는
이식 가능한 identity가 아니다. 인계 자료와 status를 검증한 뒤 claim 복구 체인을 따른다.

### 인계 관찰과 writer 종료

외부 launcher로 인계할 때는 다음을 본문 계약으로 적용한다.

- build, golden, generator, formatter, fixture와 분류 불명 작업은 명령·cwd·출력 위치로
  공유 상태를 바꾸지 않는다는 점을 입증하기 전까지 writer다. 공유 상태 밖의 immutable
  입력만 읽는 독립 reader만 계속 실행할 수 있다. 소유자·핸들·입력 리비전·쓰기 범위·결과
  위치를 열거하고, writer와 자손의 실제 종료 및 대기 writer 0을 관찰한 뒤에만 release한다.
- 제출 전에 event/state subscription을 등록하고 staging observation을 성공적으로 기록한다.
  staging 기록이 실패하면 외부 launch를 실행하지 않는다. idle prompt나 launcher의 `done`은
  수신 증거가 아니다. 모호한 결과는 재제출하지 말고 기존 attempt를 reconcile한다.
- `issueops trace handoff-delivery --input "$OBSERVATION_JSON" --json`의 observation에는
  `schema_version: 1`, `attempt_id`, `lineage_id`, `lifecycle_id`, `prompt_sha256`,
  `material_sha256`, `request.durable_id`, `expected_owner_host`, `source_generation`,
  `created_at`, `updated_at`, `receipt`를 포함한다. `launcher`에는 name/version/path/runtime_id/
  machine_id/server_id, `target`에는 terminal_id/pane_id를 실제 관찰값으로 기록한다.
- 최초 `created_at`, `updated_at`, `call_staged.observed_at`은 같은 RFC3339Nano 시각이다.
  `call_staged`는 observed와 evidence `external_call_staged`; input_accepted,
  native_turn_observed, owner_claimed, ambiguous는 not_observed에서 시작한다.
  최초 durable_id는 비우고 native launcher가 반환한 실제 ID만 채운다.
- 이후에도 같은 attempt/lineage/created_at을 유지하고 native receipt 및 processIncarnation을
  보존한다. receiver의 PID·시작 시각·executable을 실제 process 관찰과 대조한다.
  owner-claim 증거를 수동으로 만들지 않는다. 늦은 결과는 격리하고 release 뒤의 과거
  callback을 source 수정이나 pass 기록에 사용하지 않는다.
- receipt 뒤에는 같은 producer를 다시 호출해 두 번째 observation을 기록하고,
  `observation.receipt.location`과 digest를 읽어 실제 audit frame을 확인한다.
  `target.process_incarnation` 및 `target.process`의 pid/started_at/executable을 실제
  receiver 조회값으로 채운다. PID·시작 시각·executable이 claim holder의 `session_process`와
  모두 맞아야 owner claim과 연결한다. staged 시점에 아직 없는 process를 추측하지 않으며,
  PID reuse-safe 상관관계를 확인할 수 없으면 입력 수락 증거만 남긴다.
- 첫 호출에는 retry ID를 넣지 않는다. 입력 수락의 evidence는 `launcher_receipt`, 실제
  native host의 새 turn만 `native_receipt`다. timeout/응답 유실은 ambiguous의 timeout/
  accepted_response_lost로 기록하고 자동 재전송하지 않는다. Herdr의 pane run/agent prompt
  성공은 `launcher_accepted` 입력 증거일 뿐이며 agent_prompt_stalled/herdr_wait_state는
  ambiguous이지 native turn이 아니다. owner_claimed는 current generation·expected host·
  단일 manual lineage·입력 수락·session_process 일치를 확인한 claim handler만 기록한다.

### base가 앞서 나갔는지 본다

구현 `next`는 readiness 경고를 주지 않는다. **claim 뒤 active(self)**에서 직접 관측한다.
claimable은 `released_completion_authority`로 거부되므로 재개 세션도 claim부터 끝낸다.

```bash
issueops execution sync-base --id "$ISSUEOPS_ID" --preview $ACTOR_FLAGS --json
```

- `merge_needed`가 false면 그대로 진행한다.
- true이고 `conflict_files`가 비었으면 `--apply --confirm --fingerprint <preview의 값> $ACTOR_FLAGS`로
  반영한다. **이 apply는 지금, 즉 봉인이 하나도 없는 4단계 진입에서만 한다.** 반영하면
  변경 집합이 봉인된 `BranchPrepare.BaseSHA` 기준으로 잡히므로 base가 바꾼 파일이 이
  사이클의 diff·티어·리뷰 대상에 들어온다. 그 사실을 계획의
  `## 하위 호환성과 side effect` 절에 적는다. 이미 추적 중인 미커밋 변경이 있으면
  `worktree_clean`으로 거부되므로 변경이 없는 이 시점에 한다.
- `conflict_files`가 있으면 계획의 영향 범위를 다시 보고 사용자에게 알린다.
- rebase하지 않는다. 봉인된 base identity와 기존 증거를 보존한다.

## 진입 절차

`implement.enter`면 아래 순서를 지킨다.

```bash
# prepare가 스테이징한 계획을 워크트리에 풀어 두고 plan_path를 채웠으면 생략한다.
# 계획에 3단계의 네 필수 절(## 적용되는 결정과 주의사항, ## 재사용하는 기존 구현,
# ## 성능 영향, ## 하위 호환성과 side effect)이 없으면 연결이 거부된다.
issueops link-plan --id "$ISSUEOPS_ID" --plan-path "$WORKTREE_PLAN" \
  $RECORD_ACTOR_FLAGS --json

issueops compatibility review --id "$ISSUEOPS_ID" \
  --backward-compatibility "<기존 호출자에게 무엇이 그대로인가>" \
  --side-effect "<파일·원격·상태에 남는 변화>" --rollback-plan "<되돌리는 방법>" \
  --verification "<무엇으로 확인하는가>" --approved $RECORD_ACTOR_FLAGS --json

# 계획의 수용 기준을 게이트 원장 파일로 만든다(gates-ledger).
issueops gates init --file "$WORKTREE/.issueops/issues/$ISSUE/gates.md" --scope "$ISSUE" \
  --gate "G1: <결과> | CHECK: <명령> | EXPECT: <문자열>" --json

issueops phase --id "$ISSUEOPS_ID" --to implement $RECORD_ACTOR_FLAGS --json
```

blocker가 하나라도 있으면 compatibility review는 승인되지 않는다. blocker를 먼저 없앤다.

compatibility review를 기록하기 전에 계획이 고치거나 재사용한다고 적은 코드를 열어, 계획이 현재 동작에
대해 단언한 것(어디에 무엇이 있고 누가 호출하는가)이 맞는지 확인한다. 계획대로 구현하면 문서 규칙(레이어
경계, 컨벤션)이나 실제 코드와 충돌하거나 계획의 전제가 코드와 다르면 구현하지 않는다. 충돌마다 계획 위치와
근거(문서 규칙 원문, 확인한 `파일:줄`)를 `--blocker`로 적어 `--approved` 없이 compatibility review를
기록한다. 기록은 다음 세션도 보는 상태로 남는다. 그다음 [`issueops-plan`](../issueops-plan/SKILL.md)의
검토 루프로 돌려보내 계획을 고치고 새 리뷰를 받는다. 이 단계에서 계획을 직접 다시 쓰거나 충돌을 우회하는
다른 설계로 구현하지 않는다.

blocker 근거는 기록 직전에 한 번 더 확인한다. `파일:줄`은 Read 도구나 `grep -n`처럼 줄 번호를 찍는 출력에서
그대로 옮긴다. `sed -n`·`cat`처럼 번호 없는 출력에서 세어 적지 않는다(한 줄씩 어긋나기 쉽다).
"없다"·"아무도 호출하지 않는다"는 Glob 한 번이 0건이라는 이유로 쓰지 않는다. 상위 디렉터리를 읽거나 Grep으로
다시 찾은 뒤에 쓰고, `_test.go`에서만 나온 호출은 production 의존으로 세지 않는다. 계획이 무언가가 아직 없거나
중복 구현됐다고 전제하면 두 가지를 각각 `파일:줄`로 적는다. 하나는 그 코드가 이미 있는지이고, 다른 하나는
진입점(CLI·MCP·hook 등)이 이미 그 코드를 거치는지다.

## 프로젝트 문서 확인

코드를 고치기 **전에** 이 변경을 제약하는 운영 문서를 읽는다. 계획의
`## 적용되는 결정과 주의사항`은 계획 시점의 대조 결과라서, 구현 중 새로 닿는 모듈의 규칙은
여기서 다시 확인해야 한다.

- `.issueops/CONVENTIONS.md`: 코드 작성 규칙과 레이어 경계
- `.issueops/TESTING.md`: RED 테스트 설계와 필수 검증 명령
- `.issueops/CAUTIONS.md`: 색인과 변경 모듈의 반복 실수
- 새 패키지·컴포넌트를 추가하거나 책임을 옮기면 `.issueops/ARCHITECTURE.md`
- endpoint·DTO·OpenAPI를 바꾸면 `.issueops/OPEN_API_SPEC.md`

구현에 적용한 문서 규칙은 verified-execution report의 `## 적용한 문서 규칙` 절에 규칙마다
`| 문서 경로 | 해당 문장 인용 | 이 구현에서 바뀐 결정 |` 한 행으로 적는다. 게이트 원장 EVIDENCE는
`gates check --write`가 명령 출력으로 채우므로 여기에 쓰지 않는다. 읽었지만 적용할 규칙이 없으면
그 절에 대조한 문서 목록을 적는다.

## 구현 루프

- behavior change는 focused failing test에서 시작한다:
  RED→GREEN→SURFACE→CLEAN. RED에서 새 테스트가 곧바로 통과하면 버그 이해가
  틀린 것이므로 수정에 착수하지 않고 보고한다.
- 크기·시간과 무관하게 canonical worktree에서만 수정한다. source checkout 구현은 금지다.
- focused 검증 명령·결과를 그대로 기록한다. 실행하지 않은 검증은 `pass`가 아니다.
- `phase --to implement`와 `phase --to ai-slop-clean`은 `.issueops/issues/<n>/`에 구현 자료의
  추적 사본(plan.md, intent.md, spec.md, plan-review.md)을 쓰고 응답 `tracked_materials`에
  경로를 보고한다. 사본은 변경 집합에 들어가므로 구현 진입 뒤 첫 커밋에 포함한다.
- commit·push는 승인된 종료점에 포함되어 있으면 [`atomic-commit-push`](../atomic-commit-push/SKILL.md)로
  이어간다. 원래 요청에서 허용된 issue branch의 publication을 다시 묻지 않는다.
- API/DTO/OpenAPI 변경은 `.issueops/OPEN_API_SPEC.md` gate를 적용한다.
  해당 문서가 없는 대상도 변경 endpoint·public error 계약을 조사하고, 제공되는 static check와
  agent review 결과를 기록한다. 관련 없는 legacy 부채로 실패시키지 않는다.
- RED/GREEN 증거는 [`gates-ledger`](../gates-ledger/SKILL.md)로
  `.issueops/issues/<n>/gates.md`에 `gates check --write`로 채운다.
- 코드를 바꾸기 직전에 그 변경을 정한 문서 규칙을 `## 적용한 문서 규칙` 절에 한 행 추가한다.

계획과 코드베이스를 존중하는 네 규칙:

1. **재사용을 먼저 본다.** 기존 함수·패키지·테스트 헬퍼를 확장하는 쪽이 새 파일·새
   추상화보다 앞선다. 계획의 `## 재사용하는 기존 구현`에 없는 새 추상화는 만들지 않는다.
2. **계약 표면은 이슈와 계획이 명시한 것만 바꾼다.** CLI JSON, MCP schema, golden,
   record schema, provider body 계약이 여기 해당한다. 하위 호환이 깨지는 변경은 계획에
   적힌 것만 한다.
3. **hot path를 건드리면 전후를 측정한다.** 측정값을 evidence로 남긴다. 측정 없이
   성능이 나아졌다고 적지 않는다.
4. **side effect를 목록으로 적는다.** 파일·원격·durable state에 남는 변화를 verified-execution
   report에 적는다.

`next.review.frontend`가 true면 기존 디자인 시스템과 컴포넌트 출처·접근성·반응형·
모션 감소를 확인하고 실제 화면을 검증한다. 설치된 `ui-ux-craft`를 활용하며, 확인 결과는
report의 **`## UI 판단`**에 적는다. 이는 7단계 브라우저 QA의 INTENT이므로 비우지 않는다.
schema 변경은 실제 인덱스·카탈로그 추정 row 수와 출처를 기록한다. 운영 DB 전수
`SELECT COUNT(*)`는 금지하며 관찰 불가면 waive 근거를 남긴다.

같은 focused test가 **두 번** GREEN에 실패하면 세 번째를 추측으로 시도하지 않는다.
[`issueops-debugging`](../issueops-debugging/SKILL.md)으로 실패 명령을 그대로 재현하고
원인을 격리한 뒤 최소 수정을 넣는다. 이 카운터는 [`verified-execution`](../verified-execution/SKILL.md)의
"같은 기준 3회 실패 → 목표 종료"와 **같은 카운터**이며, 세 번째 실패가 그 종료다. 그때는
4단계를 멈추고 진단과 시도한 수정을 보고한다. 진단 결과는 verified-execution report의
실패 항목에 적는다.

## Lease fencing

`execution whoami --json`의 `record_actor_flags`를 `$RECORD_ACTOR_FLAGS`로,
`claim_actor_flags`를 `$ACTOR_FLAGS`로 그대로 쓴다. 손으로 조합하지 않는다.
durable mutation(phase·record·artifact) 직전 exact ID·generation·native actor·canonical cwd를
record와 대조한다. record 기록은 전자, lease 전이·publication은 후자다.
편집 배치마다 pwd·branch·HEAD·source/canonical status를 실측하고 도구 루트를 canonical로 둔다.
잘못된 root에 썼으면 멈추고 자기 변경만 옮긴 뒤 양쪽 status를 확인한다.
불일치나 다른 holder는 stop이다. 사용자의 구두 확인은 quiescence 증거가 아니다.
인증된 feedback 기록도 이 단계가 소유한다(`issueops feedback add`/`status`는 유효 alias).
계약 feedback은 이슈 본문을 먼저 갱신하고 `feedback mark-issue-updated`를 기록한다.
원격 쓰기는 preview → 동일 요청 confirm → readback이며 모호하면 reconcile한다.
원래 승인 범위 밖 commit·push·publication·merge·cleanup은 하지 않는다.
명령 존재는 usage 카탈로그/소스로 확인한다. `skill-bench`는 미구현이며
`quality inspect`는 semantic skill runner가 아니다.

## 회복은 next_command 체인만

lease 부재·다른 holder·모호한 mutation은 아래에서 시작해 반환된 exact `next_command`만 따른다.

| 상황 | 첫 명령 |
|---|---|
| 방향을 모르겠다 | `execution status --id ID --json` |
| holder 교체·회수가 필요하다 | `execution replace --id ID --preview`의 generation·inventory·quiescence 검증 체인 |
| provisioning·publication 결과가 모호하다 | `execution reconcile --id ID --preview` 후 `--confirm` |

- `--revoke`·`--finalize`·`--reseed`·fingerprint는 preview가 준 값만 쓴다.
- 회복의 종착은 `claim`이다.
- 모호한 prepare/create는 흔적이 안 보여도 반복하지 않는다. reconcile이 처분한다.
- legacy도 CLI가 반환한 체인을 따른다. 추가 설명은 [`execution.md`](../issueops/references/execution.md)에 있다.

## Child 위임

원격 parent/child 분리는 [`issueops-create-issue`](../issueops-create-issue/SKILL.md)가
소유한다. 실행 중 만드는 delegated child cycle은 그것과 별개다.

세 조건이 모두 참일 때만 위임한다: parent가 implement phase다, architecture·compatibility·
devil's-advocate 리뷰가 approved 또는 waive다, plan이 sub-agent pattern·scope·acceptance·
verification·fallback·tradeoff·기대 이득을 기록한다.

```bash
issueops child start --parent "$ISSUEOPS_ID" \
  --branch "$CHILD_BRANCH" --title "$TITLE" \
  --scope "$SCOPE" --acceptance "$CRITERION" \
  --host claude --session-id "$SESSION_ID" --cwd "$WORKER_PATH" --json
issueops child status --parent "$ISSUEOPS_ID" \
  --host claude --session-id "$SESSION_ID" --cwd "$WORKER_PATH" --json
```

- verdict는 `accept`·`reject`·`drop` 셋뿐이다. child scope를 고치는 amend 명령은
  없으므로 찾거나 발명하지 않는다.
- child의 branch·worktree·lease는 child cycle 자신의 `branch prepare`와
  `execution prepare`가 소유한다. worktree provisioning은 `execution prepare`
  몫이며, legacy `worktree prepare` 계열 명령은 v1 카탈로그에서 제거되었다.
  parent가 child worktree를 직접 만들지 않는다.
- child가 scope drift를 보고하면 child를 조용히 넓히지 않는다. 사용자가
  승인해도 경로는 두 가지뿐이다: 새 scope를 **새 child**로 분리하거나, plan을
  개정하고 plan hash에 묶인 리뷰 freshness를 다시 확인한다.
- 인계 준비나 최신 사용자 취소·범위 축소 뒤에는 새 쓰기 작업과 하위 작업 dispatch를
  중지한다. 이 스킬이 시작한 child나 worker는 인계 자료에 소유자, 실행 핸들, 입력 리비전,
  쓰기 범위, 결과 위치, 읽기 작업인지 쓰기 작업인지의 분류를 남기고, writer와 자손
  프로세스가 실제로 종료됐는지 확인한다. 사용자의 최신 취소나 범위 변경이 우선하며,
  이전 세션의 callback이나 결과는 source 변경이나 pass 기록의 근거가 될 수 없다.
- accept 전 rubric: 위임한 scope·expected worktree 준수, acceptance별 증거,
  선언한 검증 명령의 실행 결과, 무관한 diff·secret·stale scaffold 없음. 하나라도
  모호하면 accept하지 않는다.
- parent는 child record를 대신 수정하지 않는다. prompt에는 parent/child ID·generation·
  branch·canonical path·허용 scope·수락 기준·검증·중단 규칙을 넣고, child가 pwd·Git root·
  branch·HEAD·native process receipt·whoami를 확인한 뒤 쓰게 한다.
  출력은 변경 파일 요약, 검증 명령/결과, blocker/scope drift다. 새 migration·remote write·
  미계획 검증·parent 결정도 scope drift다. parent는 증거를 직접 검증한 뒤 accept/reject/drop을
  기록한다. 고칠 수 있는 미완료는 reject, 범위를 제거하거나 대체할 때만 사유를 적고 drop한다.
  Omo durable child는 canonical worktree에 cwd가 결속된 native team을 사용한다.
  prompt의 `cd`나 worktree 결속 없는 task로 대체하지 않는다. team 실행 불가면 사유를 보고하고
  같은 worktree의 독립 native `omo -p`로 같은 identity 게이트를 확인한다.

## 종료 게이트

1. focused verification 증거가 명령·결과로 남아 있고, 위임한 child가 전부 accepted
   또는 dropped다. `child_incomplete`·`child_unvalidated`가 남으면 전이가 거부된다.
2. verified-execution report 초안을 워크트리 **안**에 쓴다. 경로는
   워크트리 내부 상대 경로로 기록한다. 최종 확정은 5단계 정리가 한다.
3. `issueops phase --id ID --to ai-slop-clean $RECORD_ACTOR_FLAGS --json`
   으로 전이한다. 다음은 [`issueops-slop-clean`](../issueops-slop-clean/SKILL.md)이다.
4. 이 단계에서는 커밋·푸시나 ai-slop-clean·구현 리뷰 기록을 하지 않는다. 정리·문서·검증이
   먼저이고 커밋은 8단계다. 승인된 종료점까지 같은 ID의 `next`로 이어간다.

`execution complete`는 pr phase의 검증된 remote artifact URL·final head·report가 있어야 한다.
"구현 완료"는 여기서 phase 전이이며 complete 호출이 아니다.

## 검증

```bash
python3 scripts/validate-skill.py skills/issueops-implement
python3 scripts/verify-skill-shell.py skills/issueops-implement
wc -c skills/issueops-implement/SKILL.md
```

시작 게이트·lease·child verdict·리뷰 게이트·종료 게이트 중 하나라도 모호하면
durable mutation을 하지 않고 현재 상태와 막힌 지점을 보고한다.
