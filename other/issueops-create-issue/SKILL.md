---
name: issueops-create-issue
description: Confirm and create the IssueOps issue that a cycle contracts on. Interview the user only on blocking ambiguity, survey the codebase and background sources into plan-prep evidence, record the intent contract, domain review, split decision, and plan prep, then publish a readable Korean issue through the shared remote write protocol and link it. Use at the start of a cycle, when "issueops next" reports stage none or issue, or when the user says "이슈 만들어줘", "이슈부터 시작하자", "child task 만들어줘".
---

# IssueOps Create Issue

**1단계 하나**를 맡는다. 할 일을 확정해 기록하고 팀이 보는 이슈로 만든다.
브랜치·계획·구현은 다음 단계다.

본문은 단독 주입·복사에도 적용된다. sibling 스킬은 설치되어 있을 때 활용하며 없으면
아래 계약과 CLI의 exact `next_command`로 진행한다. evaluator나 sibling 설치는 요구하지 않는다.
선택적 [작성 예시와 배경](references/issue-writing.md)은 symlink를 해소한 이 파일 기준이다.
초안/상태만 요청했으면 그 결과에서 끝낸다. 원격 생성 권한을 추정하지 않는다.

`execution whoami --json`의 `record_actor_flags`를 `$RECORD_ACTOR_FLAGS`,
`claim_actor_flags`를 `$ACTOR_FLAGS`로 그대로 쓴다. durable 기록 직전 exact ID·native actor·
source cwd를 대조하고, execution이 있으면 generation·holder·canonical cwd도 확인한다.
다른 holder나 불일치는 stop이다. lease 전 준비에 가짜 generation을 만들지 않는다.
`feedback add`와 `status`는 유효 root alias다. 이 단계가 인증된 feedback 기록을 맡는다.
`skill-bench`는 미구현이고 `quality inspect`는 semantic skill runner가 아니다.

## 이 스킬이 맞는지 확인

```bash
# ID가 있으면 --id "$ISSUEOPS_ID"를 붙인다. 새 사이클 선택에만 자동 판정을 쓴다.
issueops next --json
```

`none|issue`면 진행한다. 명시적인 새 사이클 요청은 다른 기존 stage/사이클과 무관하게
허용한다. 그 밖에는 `next`가 지목한 단계로 간다. `blocked.*`를 우회하지 않는다.

`start`는 **source checkout**에서만 실행한다. worktree를 record의 repo로 만들지 않는다.

`next`가 기존 사이클을 선택했지만 사용자가 별도의 새 사이클을 명시적으로 요청했다면
첫 명령에 `--new`를 붙인다. `--new`는 `--branch`와 함께 쓸 수 없고, 실행할 때마다
새 lifecycle ID를 만든다. 성공 응답의 ID를 이후 명령에 계속 사용한다. 응답을 받았는지
불분명하면 `issueops list --repo "$SOURCE_ROOT" --json`으로 먼저 확인하고, 같은 명령을
바로 다시 실행하지 않는다.

## 입력 세 가지

세 입력의 조사 출처를 plan-prep evidence 문자열로 남긴다.

1. **사용자가 준 정보.** 원문을 그대로 intent contract의 `--raw-request`에 넣는다.
   요약해서 넣으면 나중에 해석이 맞았는지 대조할 원본이 사라진다.
   사용자가 HWP·PDF·DOCX 기획서나 화면 캡처를 줬으면
   요구사항·모순·누락을 원문·표·화면·작은 글씨까지 확인해 먼저 추출한다. 설치된
   `requirements-analysis`를 활용한다. 원문 요청은 그대로 `--raw-request`에 넣고, 추출한 제약은
   `intent record --constraint`에, 모순과 누락은 `--ambiguity`에 넣는다. 문서를 요약해
   `--raw-request`를 대체하지 않는다.
2. **코드베이스 조사.** `.codegraph/`가 있으면 `codegraph explore "<질문>"`으로 관련
   심볼과 호출 경로를 찾고, 없으면 `rg`로 찾는다. 만진 심볼·파일·호출 경로를 evidence
   문자열로 만든다(`--codebase-survey-evidence`). 운영 문서는 `project_docs_route`에 요청
   요약을 넣어 고른다. 이미 내려진 결정(`.issueops/ADR.md`와 `adr/` 기록)과 반복 실수
   (`.issueops/CAUTIONS.md`와 `cautions/` 기록) 중 이 요청에 걸리는 항목은 문서 경로와 항목
   제목을 `--decisions-evidence`에 적는다. 걸리는 항목이 없으면 대조한 문서 목록을 적는다.
   `project_docs_route`는 요청과 단어가 두 개 이상 겹치는 기록만 고르므로, 요청이 새로 들이는 핵심 단어(새
   플래그·명령 이름, 동작을 가리키는 영어 단어)는 따로 `.issueops/adr/`와 `.issueops/cautions/`에서 Grep한다.
   걸린 기록은 열어서 그 문장이 이 요청의 범위나 방식을 정하는지 판정한다. 정하면 위 evidence와 이슈 본문의
   범위·비목표에 옮긴다. 걸렸는데 열어 보지 않고 "해당 없음"으로 적지 않는다.
   모든 변경에 걸리는 원칙(`.issueops/CONSTITUTION.md`)도 연다. 요청한 동작이 원칙에 걸리면(예: 반복·재시도·
   감시 루프의 상한과 종료 경로, secret 처리, 권한 경계) 그 원칙을 성공 기준이나 제약으로 이슈 본문에
   옮기거나, 지키는 방법이 갈리면 blocking 질문으로 묻는다.
3. **배경지식과 웹 조사.** 외부 API의 의미나 계약이 걸릴 때만
   출처를 직접 조사하고(설치된 `web-research` 활용) 그 결과를
   `--web-research-evidence`에 넣는다. 조사하지 않았으면 waive하지 말고 왜 필요 없는지를
   evidence로 쓴다. 관련 이슈는 `--related-score-ref`로 남긴다.

원격 이슈를 쓰기 전에 `.issueops/AGENT_WORKFLOW.md`의 Start·Work 절을 읽는다. Work 절이
가리키는 `.issueops/VCS.md`가 있으면 provider recipe와 CLI 대체 경로를 거기서 확인한다.

## 질문 규칙

모호함을 세 갈래로 나눠 원장처럼 관리한다.

| 분류 | 뜻 | 처리 |
|---|---|---|
| `resolved` | 조사로 답이 나왔다 | 이슈 본문의 근거 절에 답과 출처를 쓴다 |
| `deferred` | 지금 몰라도 구현 방향이 바뀌지 않는다 | 이슈 본문 "열린 결정" 절에 남긴다 |
| `blocking` | 답에 따라 다른 것을 만들게 된다 | 사용자에게 묻는다 |

- **blocking만 묻는다.** 조사로 답할 수 있는 것은 먼저 조사한다.
- 한 번에 한 질문만 한다. 선택지가 있으면 번호로 제시하고 추천안을 먼저 둔다.
- 답을 받으면 그 답이 무엇을 바꾸는지 한 문장으로 되돌려 확인한다.
- 다음을 확인할 때까지 이슈를 만들지 않는다: 사용자에게 보이는 문제와 지금 중요한
  이유, 테스트와 실제 표면으로 검증 가능한 성공 기준, 비목표와 범위 경계, 근거가 필요한
  도메인 용어, 필요한 파일·API·명령·런타임 표면, 구현을 실질적으로 바꿀 열린 결정.

blocking 질문이 둘 이상이거나 답에 따라 만들 것이 갈리면 드래프트를 먼저 만들고,
한 번에 한 질문만 하며 매 답변 뒤 남은 모호함을 확인한다. 설치된 `implementation-planning`의
인터뷰를 활용한다. 드래프트의 `Requirements (confirmed)` 절이 intent contract
`--interpreted-intent`의 원문이 된다. 확정 뒤 드래프트는 지운다 — 이슈 본문이 유일한
계약이다.

## 기록 순서

아래 기록 순서를 지킨다. 항목이 비면 grill 진입이 거부된다.

```bash
issueops start --repo "$SOURCE_ROOT" --json      # ISSUEOPS_ID를 받는다
# 기존 사이클과 별도의 새 사이클을 요청한 경우에만 위 명령에 --new를 붙인다.

issueops intent record --id "$ISSUEOPS_ID" \
  --raw-request "<사용자 원문>" --interpreted-intent "<해석>" \
  --success-criteria "<검증 가능한 기준>" --intent-class trivial|standard \
  $RECORD_ACTOR_FLAGS --json

issueops domain-review record --id "$ISSUEOPS_ID" \
  --model-fit "<도메인 모델과 이 변경의 관계>" $RECORD_ACTOR_FLAGS --json

# 분할하지 않는 경우: 그 근거를 결정으로 남긴다.
issueops decision add --id "$ISSUEOPS_ID" --kind scope \
  --title "no split" --body "<한 owner·한 리뷰로 끝나는 근거>" $RECORD_ACTOR_FLAGS --json
# 분할하는 경우: remote create-child로 child를 만든다(아래 Parent와 child).

# 관련 이슈·라벨 점수는 plan-prep보다 먼저 만든다. 그 요약이 --related-score-ref다.
issueops remote score --input "$SCORE_INPUT" --judge none --json > "$SCORE_FILE"
# 선택하거나 거절한 라벨과 threshold는 본문이 아니라 record에 남긴다.
issueops decision add --id "$ISSUEOPS_ID" --kind review --title "라벨 판단" \
  --body "<threshold, 선택한 라벨, 거절한 라벨, override 여부>" $RECORD_ACTOR_FLAGS --json

issueops plan-prep record --id "$ISSUEOPS_ID" \
  --decisions-evidence "<...>" --related-score-ref "<score 결과의 선택·거절 후보와 threshold 요약>" \
  --web-research-evidence "<...>" --codebase-survey-evidence "<...>" \
  $RECORD_ACTOR_FLAGS --json

issueops phase --id "$ISSUEOPS_ID" --to grill $RECORD_ACTOR_FLAGS --json
```

다음은 원격 write다. 초안을 보여 주고 요청에 발행이 포함되어 있으면 아래 publication
절차로 재승인 없이 진행한다. 승인받은 특정 원문이나 범위를 바꿨으면 먼저 확인받는다.

`remote create-issue` 뒤 `status --json`에 `issue_url`이 없을 때만
`issueops link-issue --id "$ISSUEOPS_ID" --issue-url "$ISSUE_URL" $RECORD_ACTOR_FLAGS --json`을 실행한다.

이슈만 요청했으면 다음 세 줄로 완료 보고한다. 전체 작업 요청이면 진행 상황으로 알린 뒤
같은 ID로 `issueops-prepare`를 실행한다. worktree 준비 후 환경별 자동 세션 인계를 적용한다.

```text
ISSUEOPS_ID: <id>
issue: <url>
다음 단계: issueops-prepare
```

## 먼저 고르는 것

| 요청 | 사용할 형식 | 분리 기준 |
|---|---|---|
| 결함·회귀 | `bug` | 재현 절차와 기대/실제 동작을 숫자 목록으로 쓴다 |
| 사용자 기능 | `feature` | 사용자 가치와 완료 조건을 짧은 checklist로 쓴다 |
| 구조·정책 결정 | `proposal` | 대안 비교가 핵심이면 표와 결정 근거를 쓴다 |
| 바로 실행할 작업 | `implementation_task` | 근거·범위·검증을 중심으로 쓴다 |
| parent의 독립 작업 | `child_task` | scope·의존성·wave를 metadata 표로 쓴다 |

**결론은 요약, 근거는 배경, 명령은 검증 절**에 둔다. 다이어그램은 흐름·상태·경계를
문장보다 빨리 이해할 때만 쓴다.

## Parent와 child

기본은 `no split`이다. 한 owner의 검토 가능한 변경이면 아래 근거를 parent에 남긴다.

```text
Large Issue Breakdown Gate: no split
- 독립적인 acceptance와 rollback 경계가 없다.
- 한 owner와 한 MR로 검토할 수 있다.
- 이번 범위는 <파일/모듈> 안에 머문다.
```

다음 중 하나가 있을 때만 split한다.

- 한 Issue에 두면 독립된 delivery·rollback·review가 숨겨진다.
- 사용자가 병렬 ownership 또는 assignee 분리를 명시했다.

| 항목 | 규칙 |
|---|---|
| 실행 class | `[p]` 기본. `[s]`는 이름 있는 hard dependency가 있을 때만 |
| `[p]` | prerequisite `none`, 독립 검증, 보통 wave 1 |
| `[s]` | 선행 child URL/산출물과 순서를 반드시 명시 |
| 생성 | ordinary sibling이 아닌 `remote create-child` |
| parent 기록 | `## 하위 Task` 아래 URL·scope·wave·prerequisite를 본문에 기록 |

닫힌 parent를 재사용하지 않는다. parent body를 안전하게 갱신할 IssueOps 경계가 없으면
raw `gh`/`glab`로 우회하지 말고 중지한다. 댓글만 남기는 것은 완료가 아니다.
GitHub 관련 이슈는 body cross-reference, GitLab은 native linked item이다.
child는 양쪽 모두 native hierarchy를 확인하며 sibling/body 목록으로 대체하지 않는다.
`[p]`/`[s]`, prerequisite, wave는 child 제목·본문·parent 하위 Task 절에 모두 남긴다.

## 읽기 좋은 body

절 구성은 `issueops remote render-template`이 출력하는 골격을 따른다. 사람이 읽을
문제·범위/비목표·완료 기준·실행 가능한 검증 명령과 기대 결과를 채운다.

```bash
issueops remote render-template --kind issue --template "$TEMPLATE" \
  --provider "$PROVIDER" --title "$TITLE" --json
```

로그는 secret을 제거한 짧은 code block으로만 붙인다. 긴 로그 전체나
스크린샷 대신 재현에 필요한 줄과 파일·명령을 적는다. 해시, 커밋 SHA 전문,
라벨 점수, plan 원문·repo-local plan 경로·`Plan Link`·`TBD`는 본문에 넣지 않는다.
plan-prep 네 항목은 waive로 채우지 않는다. 조사 결과나 불필요한 이유를 evidence로 쓴다.

## Canonical publication

1. 현재 provider 이슈·label 후보를 조사한다. 일치하는 이슈가 있으면 중복 생성 대신
   연결/갱신한다. score의 기본 threshold는 0.70(더 강한 repo/user 값 우선)이며 선택된
   label·관련 이슈만 적용한다. 없는 label도 선택된 것만 먼저 만든다. 미선택 label을
   적용하려면 근거 있는 override를 decision/feedback에 기록한다. 무라벨 발행은 하지 않는다.
2. deterministic score 뒤 semantic 판단이 필요하면 `remote score --judge prompt`를
   fresh 독립 read-only agent에게 주고 결과 JSON을 `--judge file --judge-file`로 검증한다.
   독립 agent가 없거나 비활성화했으면 deterministic 결과를 쓰고 그 선택을 기록한다.
3. 한국어 본문을 다듬는다. `fluent-korean`이 있으면 호출하고, 없으면 명확한 주어·완성된
   문장·검증 가능한 결과·불필요한 수식 제거를 직접 검토한다. secret을 제거하고 실제
   assignee를 확인한다(`@me` 금지). 설치된 `issueops-remote-write`를 활용할 수 있다.
4. body file을 읽고 preview의 `readability`를 확인한다. critical은 수정 후 재preview,
   warning은 수정하거나 이유를 기록한다. preview와 동일한 요청에만 `--confirm`을 붙인다.
5. URL·상태·본문 hash·label·assignee·hierarchy와 `status.body_syncs` baseline을 readback한다.
   모호한 issue 생성은 `remote reconcile-issue --id ID --json`으로 확인하며 재생성하지 않는다.
   raw provider CLI/MCP 쓰기로 우회하지 않는다. 둘 이상의 artifact면 중단한다.

```bash
issueops remote create-issue --id "$ISSUEOPS_ID" --provider "$PROVIDER" \
  --title "$TITLE" --template "$TEMPLATE" --body-file "$BODY_FILE" \
  --label "$LABEL" --assignee "$ASSIGNEE" $ACTOR_FLAGS --json
```

child는 parent URL이 record에 연결되고 umbrella branch gate가 통과한 뒤 만든다.

```bash
issueops remote create-child --id "$ISSUEOPS_ID" --title "$CHILD_TITLE" \
  --template child_task --body-file "$CHILD_BODY" \
  --label "$LABEL" --assignee "$ASSIGNEE" $ACTOR_FLAGS --json
```

같은 본문으로 의도적인 새 child를 만들려면 ID를 한 번 생성해 저장하고 최초 요청과
재시도에 같은 값을 `--operation-id`로 넘긴다.

무ID 재시도는 완료 뒤에도 최초 implicit child를 반환한다. 같은 본문의 explicit 새
child가 생겨도 이 결합은 유지된다. 미해결 operation은 새 ID로도 생성하지 않으며,
오류 응답의 known URL·operation ID·recovery command를 보존한다.
`remote reconcile-child --id ID --operation-id OPERATION`의 preview에서 제목·본문
digest·type·계층·metadata를 확인한 뒤 같은 요청에 `--confirm`을 붙인다. 현재
execution holder만 confirm할 수 있고, generation이 바뀐 작업은 자동 replay 대신
명시적 reconcile로 복구한다. 복구는 기존 child를 조회·연결하며 생성하지 않는다.

child 본문의 요약에는 parent 링크와 이 child가 맡는 부분을, 선행 조건과 병합 조건
절에는 `[p]`/`[s]`, prerequisite, wave, 병합 조건을 쓴다. confirmed child 결과의
`hierarchy_verified`, type, URL, labels, assignee와 parent body readback을
확인한다.

## 품질·성능 게이트

- 품질: preview의 `readability.critical` 0, warning 처리 기록, 원격 write 전
  한국어 검토(설치된 `fluent-korean` 호출), 라벨 판단 decision 기록, secret redaction,
  hierarchy/label/assignee readback.
- 성능: issue 단계에서만 이 스킬을 로드한다. PR/MR reference를 함께
  중복 로드하지 않는다. 변경 전후 byte 수와 focused 검증 시간을 기록하되
  측정 없는 성능 개선을 주장하지 않는다.
- 검증:
```bash
python3 scripts/validate-skill.py skills/issueops-create-issue
python3 scripts/verify-skill-shell.py skills/issueops-create-issue
wc -c skills/issueops-create-issue/SKILL.md
```

provider, project authority, owner, body, label/assignee, hierarchy, 또는
durable intent가 모호하면 쓰지 않는다.
