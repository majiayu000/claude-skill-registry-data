---
name: issueops
description: Route an issue-driven work cycle across its ten user-facing stages. Run "issueops next" to decide which stage a cycle is in, hand the work to that stage's skill, and hold the invariants every stage shares. Use when the user asks to start, resume, or continue an issue cycle, when the current stage is unclear, or when they say "이슈옵스", "이슈 작업 시작", "이어서 진행".
---

# IssueOps

IssueOps는 이슈, 브랜치, 계획, 실행 lease, 검증 증거, PR/MR을 durable record
하나로 묶는다. 이 스킬은 **라우터**다. 단계의 일은 단계 스킬이 하고, 이 파일은
어느 단계인지 정하는 방법과 모든 단계가 공유하는 불변식만 소유한다.

이 본문은 복사·단독 주입 때도 적용되는 actor 계약이다. 단계 스킬은 설치되어 있으면
사용하되, 없으면 아래 계약과 CLI가 반환한 `next_command`로 진행한다. 명령·필수 입력을
확인할 수 없으면 그 지점만 보고하고 멈춘다. evaluator 자료나 sibling 설치를 요구하지 않는다.
참고 링크는 cwd가 아니라 symlink를 해소한 이 파일 위치에서 찾는다.

## 먼저 실행

```bash
issueops next --json
```

읽기 전용이며 record·로컬 관측만 쓴다(fetch/provider 호출 없음).

1. 사용자나 현재 대화가 지정한 lifecycle ID가 있으면 처음부터
   `issueops next --id "$ISSUEOPS_ID" --json`을 실행한다. 없을 때만 자동 선택한다.
   `selected.id` 또는 `start` 결과의 ID를 이후 명령·인계·압축 요약에 유지한다.
2. `stage.key`를 아래 `## 단계 표`로 바꾸고 해당 스킬을 실행한다. 단계가 끝나면 같은
   ID로 `next`를 다시 읽고 다음 단계로 이어간다. 단계 선택 메뉴를 반복해서 묻지 않는다.
3. `next_command_kind=template`의 값은 record·whoami·계획·저장소에서 채운다.
   명령의 placeholder나 `--confirm` 자체는 사용자 질문 사유가 아니다.

- `ambiguous`라도 대화에 지정된 ID가 있으면 그 ID로 다시 읽는다. ID가 없고 후보를
  구별할 근거도 없을 때만 고르게 한다. 다른 사이클을 임의로 선택하거나 정리하지 않는다.
- `none`이면 요청 범위에 맞게 이슈 단계로 들어간다. 본문 초안이나 상태 조회만 요청했으면
  그 결과만 제공한다. 사용자가 새 사이클을 요청하면 기존 후보와 별개로 시작한다.
- `blocked.*`는 아래 중단 규칙을 따른다. 다른 holder의 작업을 대신하거나 상태를 우회하지 않는다.

## 환경별 자동 세션 인계

**브랜치·canonical worktree 준비 후, 구현 진입 전**에 실행 세션을 자동 결정한다.
세션 선택 메뉴는 묻지 않는다. 전체 사이클은 draft PR/MR 발행·execution complete에서,
이슈 작성·계획만 요청했거나 더 좁은 종료점을 정했으면 그 범위에서 끝낸다.

- `issueops-plan`이 워크트리를 먼저 준비한다. 준비한 뒤 Herdr를 확인한다. 준비 세션이
  Herdr 세션이고 실행 중인 서버·호환성·현재 native host 실행 가능 여부가 확인되면 같은
  worktree의 새 Herdr 세션으로 인계한다. Herdr를 쓸 수 없으면 현재 세션에서 이어가거나,
  사용자가 직접 연 두 번째 터미널에서 수동 인계한다.
  바이너리 설치 여부만으로 ready라고 판단하지 않는다.
- 결정은 `decision add`에 `current|new-session|hold`, 런처·실측 상태, 원래 요청과 대화 근거,
  ID·issue·branch·worktree·계획·generation·승인 범위·종료점으로 기록하고 `status`로 확인한다.
  인계 전 새 dispatch를 멈추고 writer와 자손의 실제 종료를 확인한다. 인계 자료에는 목적·비목표,
  source/worktree, base/full HEAD·diff, 계획 경로/digest, 검증 입력·명령·시각·환경·실패,
  미완료 작업·결과 위치, lifecycle 상태, exact 인수/조회 명령과 자료 digest를 남긴다.
  secret·이전 claim token은 제외한다. release/status로 해제를 확인한 뒤 같은 worktree에
  현재 native host의 새 세션 하나만 연다. 수신자는 HEAD·계획/자료 digest와 최신 지시를 대조하고
  자기 actor로 인수하며, stale 근거만 재확인한다. 이전 callback은 쓰기나 pass 근거가 아니다.
  자동 분기를 다시 적용하지 않는다.
- 런처를 설치하거나 서버를 시작하지 않는다. 호출 전후 `trace handoff-delivery`로 실측
  identity·generation·prompt/material digest와 receipt를 기록한다. 입력 접수, native turn,
  claim은 별개 증거다. 모호한 launch를 재전송하거나 다른 런처/current로 우회하지 않는다.
  Claude/Codex는 설치 CLI가 지원하는 permission bypass 플래그로 연다. 전달을 확인하면
  기존 세션은 종료하며 구현 완료를 기다리지 않는다. 세부 recipe는
  [session-choice.md](references/session-choice.md)에 있다.
- 자동 분기는 실행 위치만 정한다. 원래 요청의 승인 범위·종료점을 그대로 유지하며,
  구현만 요청한 작업에 commit·push·PR/MR 발행 권한을 추가하지 않는다.
  phase·claim·`--approved`도 승인 근거가 아니다.
- 현재 세션 진행·새 세션·보류를 명시한 최신 사용자 지시는 자동 분기보다 우선한다.
  보류는 lease를 해제하고 준비 상태를 보존한다. 기존 worktree는
  세션 인계를 이유로 바꾸거나 다시 만들지 않는다.

단계 스킬과 함께 쓰는 계획·검증·Git 스킬도 이 승인 범위와 종료점을 따른다.
하위 스킬의 일반적인 "계속할까요" 절차를 추가 확인 지점으로 만들지 않는다.

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

## 단계별 협업

단계 라우팅은 아래 표 하나를 쓴다. 필요한 협업만 로드한다:
1단계는 `implementation-planning` 인터뷰·`web-research`, 3단계는 계획·`issueops-review`·
`database-design`·`algorithm-optimization`·`prompt-engineering`, 4단계는 `issueops-debugging`·
`verified-execution`·`ui-ux-craft`·`sync-base`, 5단계는 `code-quality-metrics`·`verified-execution`,
6단계는 `project-docs-update`, 7단계는 `database-design`·`verified-execution`·`aside-web-qa`,
8단계의 history 수술은 `git-operations`다. 공용 협업은 `gates-ledger`(3·4·5·7),
`issueops-review`(3·7), `issueops-remote-write`(1·9·10·동기화), `explain`(사용자 보고)이다.
낡은 본문은 `issueops-sync-issue`/`issueops-sync-pr`로 관리 블록을 보존해 갱신한다.
탈출은 `issueops-abandon`이다. Issue와 PR/MR 생성 스킬을 동시에 읽지 않는다.

## 세션 경계

1·2단계는 worktree 없이 source 준비 세션에서, 3단계도 같은 세션에서 수행한다.
3단계 `execution prepare`가 worktree·lease를 만들고 위 인계를 적용한다.
4단계부터 선택한 세션이 canonical worktree에서 수행한다. current는 기존 lease를 유지하고
새 세션은 release 확인 후 인수한다. 새 세션은 `replace --preview`와 반환된 `--reseed` 명령,
`claim --claim-current-token`으로 이어지는 인수 체인이 유일한 인계 경로다.
host 간 재개·인수도 `next_command`의 generation·quiescence 검증 체인을 따른다.

## 공통 불변식

각 독립 단계의 본문에도 실행에 필요한 최소 계약을 유지한다.

**(a) 단계 판별.** 모든 단계 스킬은 선택한 ID의 `issueops next --id "$ISSUEOPS_ID" --json`으로 시작하고
`stage.key`가 자기 단계인지 확인한다. 아니면 표가 지목하는 스킬로 안내한다. `blocked.*`
면 중단한다. phase를 추정하지 않는다.

**(b) actor 플래그.** `issueops execution whoami --json`이 돌려주는
`record_actor_flags`와 `claim_actor_flags`를 그대로 쓴다. 손으로 조립하지 않는다.

**(c) lease fencing.** durable mutation(phase 전이, record 기록, artifact stage) 전마다
exact lifecycle ID·generation·native actor·canonical cwd를 현재 record와 대조한다.
record 기록은 `RECORD_ACTOR_FLAGS`, lease 전이와 publication은 `ACTOR_FLAGS`를 쓴다.
두 축약의 정의는 `issueops --help`의 legend가 소유한다. 불일치는 stop이다. 사용자의
"그 세션은 내가 껐어"는 quiescence 증거가 아니다. 모호한 결과는 재실행하지 않고 reconcile한다.
lease 전의 준비 기록은 source checkout의 native actor로, 구현은 active holder의 canonical cwd로 한다.

**(d) 편집 대상 확인.** 편집 배치마다 셸 프롬프트를 믿지 말고 실측한다.

```bash
pwd
git branch --show-current
git rev-parse HEAD
test "$PWD" = "$EXPECTED_WORKTREE"
git -C "$SOURCE_CHECKOUT" status --short
git status --short
```

patch·edit·생성 도구의 루트를 `$EXPECTED_WORKTREE`로 둔다. 도구가 다른 체크아웃에
썼으면 멈추고, 자기 변경만 canonical worktree로 옮긴 뒤 두 status를 다시 확인한다.
worker 프롬프트에는 exact lifecycle ID, generation, branch, worktree, 허용 경로,
수락 기준, 중단 규칙을 넣는다.

**(e) 코드베이스 존중.** 새로 만들기보다 기존 구현의 확장과 재사용을 먼저 본다. 계약
표면의 하위 호환성, 성능 영향, 파일·원격·상태의 side effect를 세 곳에서 명시한다:
계획의 필수 절 세 개(`## 재사용하는 기존 구현`, `## 성능 영향`,
`## 하위 호환성과 side effect`), 구현 루프의 네 규칙, 리뷰의 네 렌즈. 근거는
`AGENTS.md` §2 Simplicity First와 §3 Surgical Changes다.

## Core contract

durable phase는 `problem`, `grill`, `plan`, `compatibility-review`, `implement`,
`ai-slop-clean`, `feedback`, `pr`, `done`이다. `issue`는 linkage, `cleanup`은 done 뒤 후처리다.
한 cycle은 exact ID·canonical worktree·generation-fenced holder·linked Issue·검증된 PR/MR을 갖는다.
CLI `issueops ... --json`/MCP `issueops_execution`이 state를 소유하고 `execution complete`만
done을 기록한다. hook은 SessionStart의 project-doc context만 제공한다. Issue 생성·편집·
테스트·대기·branch/worktree 준비·publication·reply·merge·cleanup을 hook에 맡기지 않는다.

## 단계 표

`stage.key`를 스킬과 label로 바꾸는 유일한 표다. CLI는 이 표를 모른다.

| stage.key | 스킬 | label |
|---|---|---|
| `none`, `issue` | `issueops-create-issue` | 이슈 확정·생성 |
| `prepare` | `issueops-prepare` | 브랜치 준비 |
| `plan.architecture`, `plan.write`, `plan.review`, `plan.handoff` | `issueops-plan` | 문서 확인·아키텍처·계획·검토·인계 |
| `claim` | 스킬 없음. `next_command`가 돌려주는 체인(claimable이면 `claim --claim-current-token`, released이면 `replace --preview`, revoking이면 `replace --finalize-preview`)을 lease가 active(self)가 될 때까지 따라간 뒤 `next`를 다시 실행한다 | 현재 index의 label |
| `implement.enter`, `implement` | `issueops-implement` | 구현 |
| `clean` | `issueops-slop-clean` | AI slop 정리 |
| `docs` | `issueops-docs` | 프로젝트 문서 반영 |
| `verify` | `issueops-verify` | 검증 |
| `commit-push` | `atomic-commit-push` | 커밋·푸시 |
| `pr.create` | `issueops-create-pr` | PR/MR 발행·완료 |
| `pr.complete` | `issueops-complete` | PR/MR 발행·완료 |
| `done` | 머지 전이면 `issueops-merge`, 머지 뒤면 `issueops-cleanup`. 구분은 `issueops remote merge-pr --id ID --json`의 `already_merged`로 한다 | 머지·정리 |
| `takeover` | 스킬 없음. `next_command`를 실행하고 결과가 돌려주는 `next_command`를 따라간다. 죽은 홀더 인수는 `issueops-abandon`이 설명한다 | 현재 index의 label |
| `blocked.pending`, `blocked.holder_live` | 없음. `next_command`로 상태를 다시 읽는다 | 현재 index의 label |
| `blocked.root_conflict` | 충돌 사이클을 `issueops-cleanup`(머지됨) 또는 `issueops-abandon`(미머지)으로 먼저 정리한다 | 현재 index의 label |
| `unknown`, `invalid` | 없음. `next_command`로 record를 읽고 `warnings`의 missing 키를 사용자에게 보여 준다 | 현재 index의 label |
| `ambiguous` | 사용자에게 `candidates` 중 ID 선택 또는 새 사이클 시작을 요청 | 없음 |

`missing`의 해소 명령은 CLI의 `next_command`가 소유한다.

## 구현·검증 규칙

본문만으로 실행해도 evidence schema를 생략하지 않는다. domain 검토에는 invariant,
exact mechanism, equivalent behavior, source 근거를 분리해 적는다. 구현 전 환경 표에는
Environment / Repo-config evidence / Runtime evidence / Failure path / Remediation order를
채운다. feedback은 classification, verification, thread reply와 resolution을 추적한다.
완료 기록에는 diff, verification, labels, children, draft URL, thread status, cleanup,
follow-ups를 남겨 사람이 검사할 수 있게 한다.

domain 계약은 구현 전에 issue 또는 plan의 evidence 절에 기록한다. exact mechanism이
없다는 사실과 다른 경로가 같은 invariant를 보장하는지는 별개로 판정한다. end-to-end
동작까지 미확인·반박된 것이 아니면 단순한 mechanism 부재를 기능 부재로 단정하지 않는다.
endpoint/controller/DTO/schema/OpenAPI 또는 public error 동작이 바뀌면 계획과 PR/MR
초안에 변경 endpoint(또는 계약 변경 없음), usecase/error mapping의 도달 가능한 public
error, 대상 repo의 static/API-doc review 결과와 관련 검증 명령을 기록한다. 해당 명령이
없으면 부재와 가장 가까운 static/review 검사를 명시하고 무관한 legacy 부채와 구분한다.

live matrix에서는 source diff와 실제 DB/config/env/pod/log 증거를 분리하고 비슷해 보이는
failure path를 한 원인으로 합치지 않는다. local-only 관측과 same-network/in-workload
관측을 구분하며, 실제 runtime 확인 가능 여부와 여러 수정의 순서를 기록한다.
feedback classification은 contract_change/defect/question/noise/valid_review/stale_review/
rollout_evidence_missing/environment_debt, resolution은 unresolved/fixed/resolved/obsolete/
split to follow-up으로 남긴다. 검증된 feedback만 적용하고 수용 기준·non-goals·검증·labels·
링크·구현 범위가 바뀌면 계속 진행하기 전에 remote issue body를 갱신한다.

ready/done을 보고하기 전에 actual diff, source/target branch, remote issue/PR/MR body의
최신성, issue label의 복사 또는 명시적 교체, single-commit 정책 또는 다중 commit 사유,
branch divergence와 clean worktree, cleanup 상태 또는 번호 붙인 선택지를 확인한다.
최종 보고와 remote write 전에 위 증거를 담은 inspectable draft completion record를 만든다.
테스트 성공만으로 remote 갱신·thread reply·merge readiness·cleanup 완료를 대신하지 않는다.

- behavior change는 focused failing test에서 시작해
  `RED→GREEN→SURFACE→CLEAN` 순서로 검증한다.
- 작업은 canonical worktree에서만 한다. source checkout에 구현하지 않는다.
- API/DTO/OpenAPI 변경은 `.issueops/OPEN_API_SPEC.md` gate를 적용한다.
- live runtime, review reply, completion hygiene가 요청 범위라면 테스트 통과만으로
  완료를 선언하지 않는다.
- ai-slop-clean은 실제 diff가 생긴 뒤 실행하고, cleanup 후 관련 검증을 다시
  실행한다.
- publication 전에 구현 diff를 project docs와 양방향으로 대조한다. CONSTITUTION·
  CONVENTIONS·ARCHITECTURE를 어겼으면 구현을 고치고, CAUTIONS에 남길 재발 함정이나
  ADR에 남길 결정이 생겼으면 문서를 먼저 고친 뒤 기록한다. 남길 것이 없으면 실제로
  읽은 문서 경로(`--reviewed-doc`)와 확인 근거를 함께 `no-change`로 기록한다.
- 변경 집합에 마이그레이션·엔티티·SQL 스키마 파일이 있으면 실제 데이터베이스에서
  인덱스 현황과 카탈로그 추정 row 수를 관찰해 관찰값과 출처를 기록한다. 전수 스캔하지 않는다.
  관찰 불가면 근거 있는 waive로 남긴다. 문서·스키마 증거 뒤 구현 리뷰를 기록하고,
  변경 집합이 바뀌면 봉인을 재검증한다.
- Git staging/push는 `atomic-commit-push`, 고급 history 작업은 `git-operations`가
  소유한다. 원래 요청에서 승인된 issue branch의 commit·push는 다시 묻지 않는다.
- destructive cleanup은 exact target과 fingerprint를 preview한 뒤 별도 사용자
  승인을 받는다.

## 원격 쓰기

`issueops-remote-write`가 설치되어 있으면 사용한다. 단독 실행에도 다음 순서를 지킨다:
render-template 골격 → 한국어 다듬기(`fluent-korean`이 있으면 호출, 없으면 완성된 문장·
명확한 주어·검증 가능한 결과·불필요한 수식 제거를 직접 검토) → secret 제거 →
threshold로 선택한 label·실제 assignee(`@me` 금지) → preview의 readability 확인 →
같은 요청에만 confirm → URL·상태·본문·metadata readback. critical은 수정 후 재preview하고,
warning은 수정하거나 이유를 기록한다. 승인된 원문/범위가 바뀌면 사용자에게 확인한다.
raw provider 쓰기로 우회하지 않는다. 모호한 write는 reconcile하며 중복 생성하지 않는다.
계약 변경 feedback은 소유 단계가 인증된 actor로 기록하고 이슈 본문을 먼저 갱신한 뒤
`feedback mark-issue-updated`를 기록한다. 댓글은 계약이 아니다.
`issueops feedback add`와 `issueops status`는 유효한 root alias다. `quality inspect`는
semantic skill runner가 아니며 `issueops skill-bench`는 구현되지 않았다.

## Reference map

본문으로 라우팅·권한·증거·중단을 판단하고 필요한 recipe만 `references/`에서 읽는다:
`remote-issue.md`(provider 계층), `evidence-contract.md`(domain/API/live/completion),
`execution.md`(lease/claim/recovery/publication), `session-choice.md`(세션 인계),
`orchestration.md`(child), `cleanup-state.md`(머지 후 정리),
`review-feedback.md`(thread; 봇은 `review-agent-feedback`, 사람 리뷰는 `pr-review`).

## Stop conditions

다음 조건이면 해당 phase나 remote write를 실행하지 않는다. 승인 범위 안에서 조사·수정·
재검증으로 해소할 수 있으면 에이전트가 해소하고 같은 ID로 `next`를 다시 읽는다.
stale 판정이나 테스트 실패 자체를 사용자에게 진행 여부를 물을 이유로 삼지 않는다.

- provider, credentials, project, Issue owner가 모호하다. target branch는
  본문의 Execution ownership에 있는 base 선택 순서로 해소하고 질문 사유로 삼지 않는다.
  [`issueops-prepare`](../issueops-prepare/SKILL.md)는 추가 설명이며 필수 dependency가 아니다.
- intent·success criteria·domain term 해석이 구현을 바꿀 만큼 갈린다.
- architecture open question, compatibility blocker, stale review(`architecture_review_stale` 포함)가 남아 있다.
- branch/worktree/plan/generation/actor가 current record와 맞지 않는다.
- strict PR readiness가 Issue, branch link, plan, worktree, upstream,
  ai-slop-clean, project-doc 반영 판정, 스키마 실측 근거, contract feedback를
  누락했다고 보고한다.
- label·assignee·한국어 body·target branch·live readback이 검증되지 않았다.
- merge evidence 없이 cleanup을 요청한다.

조사·문서·관례로 답할 수 있으면 진행하고 근거를 보고한다. 질문은 해소되지 않는 요구사항,
승인 범위 변경, 필요한 권한/자격 증명, 자동 복구 불가 충돌에 한정하며 결정과 근거를 적는다.
동일 blocker가 두 번의 복구 뒤에도 남으면 명령·원인을 보고하고 중단한다.
다른 holder를 무한 polling하거나 모호한 원격 mutation을 반복하지 않는다.

## IssueOps benchmark artifact contract

Benchmark 응답에는 의도나 계획만 쓰지 말고 다음 labeled evidence를 넣는다.

```text
Durable state record: <IssueOps id, phase, readiness gates, state path/tool output>
Phase routing: <problem -> grill -> issue -> plan -> compatibility-review -> implement -> ai-slop-clean -> feedback -> pr -> cleanup>
Flow evidence: <Issue, plan, TDD, sub-agent decision, feedback, PR/MR artifacts>
Hook boundary: <what hooks may suggest and what only the main agent/CLI owns>
Cleanup/readiness evidence: <strict readiness, merge/cleanup status, remaining choices>
```

semantic judge는 artifact 작성자가 아닌 fresh-context host agent가 맡는다.
deterministic pass를 먼저 실행하고, JSON-only judge map을 `--judge file`로
strict-decode한다. 외부 judge는 read-only이며 workspace나 remote를 수정하지
않는다.

## Execution ownership

base 선택은 사용자 명시 branch → issue가 지정한 integration branch → 프로젝트 관례 →
관찰한 최근 merge target → repository default 순서다. 선택한 근거와 정확한 base SHA를
보고한다. release flow를 벗어나는 base는 사용자가 명시적으로 그 base를 요청한 경우에만
선택하고 그 예외를 보고한다. 그렇지 않으면 관찰한 release 관례를 따른다.
형제 prepare 스킬이 없어도 이 순서를 적용한다.

active holder만 canonical worktree에서 구현·검증·publication·`execution complete`를 수행한다.
complete는 done과 lease 해제만 기록한다. merge·resource 삭제는 별도 승인 단계다.
