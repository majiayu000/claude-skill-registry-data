---
name: issueops-remote-write
description: Apply the shared IssueOps remote write protocol to any governed "issueops remote ..." mutation. Write the body from the render-template skeleton and the readable-body guide, polish it with fluent-korean, read the readability report in the preview, confirm the identical request, read the artifact back, and reconcile instead of retrying when the result is ambiguous. Use before creating or editing issues, child tasks, PR or MR bodies, comments, or review replies inside an IssueOps cycle, or when the user says "원격에 써줘", "이슈 본문 올려줘", "PR 본문 갱신".
---

# IssueOps Remote Write

이 스킬의 일은 **원격에 무언가를 쓰기 전후에 지켜야 하는 절차 하나**다. 무엇을
쓸지는 각 단계 스킬이 정하고, 어떻게 안전하게 쓰는지는 여기가 소유한다.

- 이슈 생성: [`issueops-create-issue`](../issueops-create-issue/SKILL.md)
- PR/MR 생성: [`issueops-create-pr`](../issueops-create-pr/SKILL.md)
- 본문 동기화: [`issueops-sync-issue`](../issueops-sync-issue/SKILL.md), [`issueops-sync-pr`](../issueops-sync-pr/SKILL.md)
- 한국어 문체: [`fluent-korean`](../fluent-korean/SKILL.md)
- 본문 작성 지침: [`references/readable-body.md`](references/readable-body.md)

## 여덟 규칙

1. **본문은 `render-template` 골격에서 시작한다.** 절 목록을 기억이나 다른 문서에서
   복사하지 않는다. 절 구성의 원본은 `issueops remote render-template`이다.
2. **본문은 `fluent-korean`을 거친다.** 초안을 그대로 원격에 쓰지 않는다. 이 호출은
   권고가 아니라 write의 선행 조건이다.
3. **preview를 먼저 실행하고 가독성 보고서를 읽는다.** `--confirm` 없는 같은 명령이
   무엇이 쓰일지와 `readability` 판정을 보여 준다. critical이 있으면 confirm이 거부되므로
   본문을 고친 뒤 preview부터 다시 실행한다. warning은 고치거나, 남겨 두는 이유를 한
   줄로 적는다.
4. **confirm은 preview와 완전히 같은 요청에만 붙인다.** 본문이 바뀌면 preview부터 다시
   실행한다. `--confirm`은 CLI의 실행 확정 플래그다. 승인된 작업 범위 안에서는 에이전트가
   preview를 검토하고 실행하며 매번 사람에게 재승인받지 않는다. 사용자가 특정 본문을
   그대로 승인했거나 수정이 범위를 바꾸면 변경된 내용에 대한 승인이 필요하다.
5. **쓴 뒤 읽는다.** provider가 조용히 무시한 write를 성공으로 보고하지 않으려면
   readback이 필요하다.
6. **결과가 불명확하면 재호출하지 않고 reconcile한다.** timeout이나 전송 실패는 "쓰이지
   않았다"는 뜻이 아니다. 다시 만들면 중복 아티팩트가 생긴다.
7. **secret 원문을 남기지 않는다.** 로그·명령 출력·환경값을 붙일 때는 토큰과 자격
   증명을 지운 뒤 붙인다. 원격 본문은 지워도 이력에 남는다.
8. **label과 concrete assignee 없이 쓰지 않는다.** 스코어 결과의 threshold 이상 label만
   적용하고, assignee는 실제 사용자 이름이어야 한다. `@me`는 사용자 이름이 아니다.

## 절차

```bash
# 1. 골격 받기. 종류와 템플릿에 맞는 필수 절이 순서대로 나온다.
issueops remote render-template --kind issue --template implementation_task \
  --provider "$PROVIDER" --title "$TITLE" --json

# 2. 작성. references/readable-body.md의 구조·용어 변환표를 따라 골격을 채운다.
# 3. 본문 초안에 fluent-korean 스킬을 호출해 다듬는다(Skill 도구).
# 4. 독자 검토(권장). 맥락 없는 subagent에게 제목과 본문만 주고 네 질문에 답하게 한다.
#    모델은 reader-check 역할이다.
issueops model resolve --host "$HOST" --role reader-check --json   # .model, .effort, .argv

# 5. preview. 응답의 readability.critical이 비어 있어야 confirm이 통과한다.
issueops remote <verb> --id "$ISSUEOPS_ID" ... --body-file "$BODY_FILE" --json

# 6. 동일 요청 + --confirm. create-issue는 --template을 반드시 넘긴다.
issueops remote <verb> --id "$ISSUEOPS_ID" ... --body-file "$BODY_FILE" --confirm --json

# 7. readback
issueops remote verify-artifact --id "$ISSUEOPS_ID" --provider "$PROVIDER" \
  --kind pr --url "$URL" --target-branch "$BASE" --label "$LABEL" --assignee "$ASSIGNEE" \
  $RECORD_ACTOR_FLAGS --json   # PR/MR. record를 쓰므로 lease holder의 actor 플래그가 필요하다
# issue·child·본문 갱신은 해당 명령의 응답 readback 필드(hierarchy_verified, url, body sha)를 확인한다.

# 8. 결과가 불명확하면 재호출하지 않는다.
issueops remote reconcile-issue --id "$ISSUEOPS_ID" --json                          # issue create
issueops execution reconcile --id "$ISSUEOPS_ID" --preview $ACTOR_FLAGS --json      # PR/MR create
```

provider CLI(`gh`, `glab`)와 provider MCP 도구(GitHub MCP, glab MCP)는 사이클 안에서
원격에 쓰는 데 쓰지 않는다. 직접 쓰면 가독성 검사를 건너뛰고, pending intent가 기록되지
않아 모호한 결과를 회복할 방법도 사라진다.

## 가독성 검사

`create-issue`, `create-child`, `create-pr`, `sync-issue`, `sync-pr`은 본문 계약과
가독성 검사를 항상 실행한다. 스크립트를 따로 돌리지 않는다.

| 명령 | preview | `--confirm` |
|---|---|---|
| `create-issue`, `create-child`, `create-pr` | `readability`에 판정을 담는다 | critical이 있으면 원격 호출 전에 거부한다. `create-issue`는 `--template`이 없으면 거부한다 |
| `sync-issue`, `sync-pr` | 제안 본문은 `readability`, 원격의 현재 본문은 `live_readability`(warning만)에 담는다 | 제안 본문에 critical이 있으면 원격을 읽기 전에 거부한다 |

- critical은 한국어 비율, 요약 절, 필수 절, 코드 밖 64자리 hex다. 판정 기준과
  warning 목록은 작성 지침에 있다.
- `sync-*`에 `--template`이 없으면 제안 본문의 절 제목으로 템플릿을 추론한다.
- 본문 품질 규칙(완성된 문장, 단정 회피 금지, 검증 가능한 완료 기준 등)은
  [`references/readable-body.md`](references/readable-body.md)가 소유한다.

원격 issue 본문에는 repo-local plan 경로를 넣지 않는다. plan과 구현 자료는
`.issueops/issues/<n>/`에 두고, 본문은 사람이 흐름을 파악하는 데 필요한 내용만 담는다.

## body-of-record

원격 issue 본문이 IssueOps 범위의 SSOT다. 사용자 피드백, 리뷰 피드백, QA, CI 증거,
에이전트 분석이 문제 정의·수락 기준·비목표·검증·구현 범위·관련 이슈 링크·label 중
하나라도 바꾸면 계속하기 전에 본문을 갱신한다. 스레드 댓글은 논의를 남길 뿐 계약이
아니다.

```bash
# 본문 갱신은 issueops-sync-issue가 소유한다. 갱신한 뒤 그 접합점을 기록한다.
issueops feedback mark-issue-updated --id "$ISSUEOPS_ID" $RECORD_ACTOR_FLAGS --json
```

이 기록 전까지 `issueops pr-readiness --strict`는 `contract_feedback_issue_update`로
막힌 채 남는다. 그것이 의도다 — 계약이 바뀌었는데 팀이 보는 이슈가 그대로면, 진행
상태를 이슈로 공유한다는 전제가 깨진다.

## 나쁜 예

- raw `gh`·`glab`로 본문을 고친다. pending intent가 없으니 모호한 결과를 회복할 수 없다.
- preview 없이 `--confirm`을 붙인다.
- preview 뒤 본문을 고치고 preview를 다시 하지 않는다. 검토한 요청과 다른 것이 쓰인다.
- timeout 뒤 create를 다시 실행한다. 중복 이슈나 중복 PR이 생기고, 그것을 정리하는 일이
  원래 작업보다 커진다.
- 실패 로그를 그대로 붙인다. 토큰과 자격 증명이 원격 이력에 영구히 남는다.
- `fluent-korean` 호출을 생략한다. 가독성 검사는 자연스러운 문장인지 판정하지 않으므로
  통과하고, 팀은 AI가 쓴 본문을 읽는다.
- provider MCP 도구로 본문을 게시한다. 가독성 검사와 intent 기록을 모두 건너뛴다.
- preview의 warning을 읽지 않고 confirm한다. warning마다 고치거나 남기는 이유를 적는다.
- label과 assignee 없이 쓴다. 아무도 그 아티팩트를 자기 것으로 보지 않는다.

## 검증

- write 뒤 readback 응답의 URL·상태·본문 해시가 방금 쓴 것과 같은지 확인한다.
- `issueops status --id "$ISSUEOPS_ID" --json`의 `body_syncs`에 이번 write의
  baseline이 남았는지 확인한다.
- 모호한 결과를 만났다면 reconcile 결과가 정확히 하나의 아티팩트를 지목했는지 확인한다.
  둘 이상이면 사람이 판단할 때까지 멈춘다.
