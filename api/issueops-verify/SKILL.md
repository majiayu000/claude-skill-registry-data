---
name: issueops-verify
description: Use when "issueops next" reports the verify stage, or when the user asks to verify a sealed IssueOps implementation before publication.
---

# IssueOps Verify

이 스킬의 일은 **봉인된 변경이 정말 통과하는지 확인하고 그 판정을 기록하는 것**이다.
파일은 하나도 바꾸지 않는다. 고칠 것이 나오면 앞 단계로 돌아간다.

- 전체 흐름과 단계 판별: [`issueops`](../issueops/SKILL.md)
- 게이트 원장: [`gates-ledger`](../gates-ledger/SKILL.md)
- 적대 리뷰: [`issueops-review`](../issueops-review/SKILL.md)
- 이전 단계: [`issueops-docs`](../issueops-docs/SKILL.md)
- 커밋: [`atomic-commit-push`](../atomic-commit-push/SKILL.md)

## 이 스킬이 맞는지 확인

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

`stage.key`가 `verify`면 이 스킬이다. `clean`이나 `docs`면 봉인이나 문서 반영이
아직이므로 그 단계로 돌아간다.

## 파일을 만지지 않는다

change fingerprint는 `git diff <base>..HEAD`와 `git status`가 가리키는 **모든 경로의
내용 해시**다. untracked 파일도 들어간다. 그래서 이 단계에서 파일을 하나라도 바꾸면
정리 단계의 봉인과 문서 단계의 판정이 동시에 stale이 된다.

이 단계의 명령은 전부 읽기이거나 record 기록이다. record 기록은 durable state를 바꾸지만
워크트리 파일을 바꾸지 않으므로 fingerprint에 영향이 없다.

검증이 실패해 코드를 고쳐야 하면 4단계로 돌아가 구현·정리·재봉인·문서 반영을 다시
밟는다. `next`가 `clean`으로 되돌리는 것이 그 신호다.

## 프로젝트 문서 확인

실행할 검증을 고르기 **전에** 저장소가 요구하는 검증 기준을 읽는다. 무엇이 필수 명령인지는
이 문서들이 정하고, 게이트 원장은 그중 이번 변경에 해당하는 부분만 담는다.

- `.issueops/TESTING.md`: 필수 검증 배터리와 "검증됨"이라고 말할 수 있는 기준
- `.issueops/AGENT_WORKFLOW.md`: 검증에서 완료 보고까지의 흐름
- endpoint·DTO·OpenAPI가 바뀌었으면 `.issueops/OPEN_API_SPEC.md`
- 같은 검증이 반복해서 실패하면 `.issueops/CAUTIONS.md`

report의 검증 절에는 따른 문서 경로와 그 문서가 요구한 명령을 짝지어 적는다. 문서가
요구했지만 실행하지 않은 명령은 사유와 함께 `Not Run`으로 적는다.

## 0 재사용을 확인하고 필요한 작업을 병렬 실행한다

봉인된 fingerprint와 1절의 증거 재사용 조건을 먼저 확인한다. 아래 작업 중 유효한
증거가 없는 필수 작업만 고르고, 입력과 실행 환경을 공유해 서로 영향을 주지 않는
작업을 **같은 fingerprint에 대해 동시에** 시작한다. 같은 DB나 브라우저 상태를 쓰는
검증은 순서대로 실행한다. 리뷰어에게는 기존 검증 증거와 아직 실행 중인 항목을 구분해
전달하고, 추가 결과가 판정에 영향을 주면 기록 전에 그 결과로 delta 리뷰를 받는다.

1. 게이트 원장과 저장소 검증 배터리(1절). `gates check`는 `--write` 없이 실행한다.
   `--write`는 4·5단계가 소유한다.
2. 스키마 실측(2절). 변경 집합에 스키마 파일이 있을 때만 활성화된다.
3. 구현 리뷰 서브에이전트(3절).
4. 화면 QA(`next`의 `review.frontend`가 true일 때만).
   [`aside-web-qa`](../aside-web-qa/SKILL.md)에 네 입력을 이렇게 매핑한다.
   TARGET=계획이나 이슈 본문의 로컬 실행 절차가 준 URL, SCOPE=변경 집합의 frontend 경로,
   REQUIREMENTS=intent 문서와 이슈의 성공 기준, `gates.md`, INTENT=4단계 report의 `## UI 판단` 절.
   넷 중 하나라도 없으면 지어내지 말고 QA를 `Not Run`으로 report에 사유와 함께 적는다.
   보고서 출력 경로는 ignored 영역 `.issueops/issues/<n>/review/`나 워크트리 밖으로
   고정한다 — 워크트리 안 미추적 파일은 fingerprint에 들어가 봉인을 깬다. 제품을 바꾸는
   시나리오는 그 스킬의 allowed mutations·cleanup 계약 안으로 한정하고 정리 영수증을
   report에 적는다. `aside-functional-qa`·`aside-visual-qa`를 직접 부르지 않는다.

- **결과를 모두 모은 뒤 판정을 기록한다.** 배터리가 실패하거나 필수 스키마·QA 증거가
  빠졌으면 먼저 도착한 리뷰 `pass`를 기록하지 않는다. 실패 출력과 리뷰 지적은 수정에
  쓸 근거로 보존하고 4단계로 돌아간다. 수정으로 fingerprint가 바뀌면 이전 판정을
  재사용하지 않는다. `Not Run`이 성공 기준 검증을 누락했다면 readiness의 blocker다.
- 이 동시 실행의 전제는 정리 단계가 관련 검증을 이미 통과시켰다는 것이다. 배터리
  실패가 드물지 않으면 병렬화가 아니라 5단계를 먼저 고친다.
  검증 명령의 실패 기록으로 판단한다. `issueops review-metrics --repo "$WORKTREE"
  --json`의 revise 비율은 계획 리뷰 판정 비율이며 배터리 실패율이 아니다.
- 이 fan-out은 `SUB_AGENT_PATTERNS.md`의 기대 이득 `parallel_speed`에 해당한다.
  그 slug와 실제로 절약한 벽시계 시간을 verified-execution report에 적는다.
- 정리(5단계)·문서 반영(6단계)과는 동시에 실행하지 않는다. 그 둘은 파일을 쓰므로
  봉인을 바꾼다.

## 1 검증 증거 확인과 필요한 재검증

게이트 원장을 읽기 전에 봉인 intent 문서(`<artifact_dir>/intent.md`, 없으면
`status --json`의 `.intent`)의 성공 기준과 비목표를 읽는다. 원장의 G 항목과 이슈의 완료
기준이 그 성공 기준을 모두 덮는지 대조하고, 덮지 않는 성공 기준은 report의 `## 의도 대조`
절에 적어 4절의 readiness 판정에서 blocker로 다룬다. 봉인 뒤 intent가
다시 기록됐으면 `status --json`의 `.intent`가 최신이다.

원장은 눈으로 읽지 않는다. 체크박스와 EVIDENCE 줄은 주장이고, 원장의 실제 상태는 파서가 읽은 값이다.
먼저 `issueops gates status --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --json`을
실행해 게이트마다 `state`와 `has_check`를 본다. `met`이 아니거나 `has_check`가 false인 게이트는 `[x]`여도
미충족이다. met인 게이트도 그 CHECK가 성공 기준의 동작을 실제로 관찰하는지 본다. 관계없는 기존 테스트나
EXPECT 없는 빌드는 그 게이트의 증거가 아니다.

현재 fingerprint에 대한 성공 기록이 있고 명령·입력·의존성·환경이 같으며 외부 상태의
유효기간도 지나지 않았으면 그 결과를 재사용한다. 단계가 바뀌었다는 이유만으로 같은
명령을 다시 실행하지 않는다. 하나라도 확인할 수 없거나 저장소가 새 실행을 요구하면
다시 실행한다. fingerprint 변경·실패·새 검증 항목은 재검증 사유다.

```bash
# 위 조건을 만족하면 기존 EVIDENCE를 읽는다. status는 CHECK를 실행하지 않는다.
issueops gates status --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --json

# 새 실행이 필요하면 CHECK를 실행하되 원장은 바꾸지 않는다.
issueops gates check --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --json

# 게이트 CHECK에서 이미 실행한 명령은 중복 실행하지 않는다.
# 저장소의 필수 검증 중 아직 유효한 성공 증거가 없는 명령만 실행한다.
issueops verify-work --json -- "$VERIFY_COMMAND"
```

위 명령은 모두 순서대로 실행하는 목록이 아니다. 재사용할 때는 원래 명령·결과·시점과
현재 입력이 같다는 근거를 보고한다. 실행하지 않은 명령을 새 PASS로 기록하거나 stale
판정을 덮어쓰지 않는다. 필수 리뷰·readiness·lease 검사는 그대로 수행한다.

이 issueops 저장소의 self-verify 배터리를 실행할 때는 먼저
`issueops status --id "$ISSUEOPS_ID" --json`을 읽고, 해당 사이클의
`branch_prepare.base_sha`를 `BASE_SHA`로 사용한다. 커밋 후 worktree가 깨끗해도
기준을 전달한다. base가 없으면 검증을 중단하고 준비 기록을 확인하며, 무기준 실행이나
다른 사이클·origin/main 추론으로 우회하지 않는다.

```bash
./bin/issueops self-verify --base-ref "$BASE_SHA" --seed=100 --target-score=95 --llm-eval=false --json
```

MCP를 사용하면 같은 값을 `self_verify`의 `base_ref`에 전달한다. risk QA 결과의
`scope.base_sha`와 `scope.head_sha`를 실제 준비 기준과 HEAD에 대조하고, scope 오류가
없으며 요구된 vet/race 명령이 실행됐는지 확인한다. 범위는 기준 tree부터 관측 HEAD
tree까지의 변경과 staged·unstaged·untracked 경로의 합집합이다.

- endpoint·DTO·OpenAPI가 바뀌었으면 `.issueops/OPEN_API_SPEC.md` 게이트를 적용하고
  `issueops api-doc check --json`을 실행한다. 대상 저장소에
  `npm run swagger:check` 같은 wrapper가 있으면 그것을 먼저 실행한다.
- `verify-work`는 실행한 명령과 결과를 evidence로 남긴다. 실행하지 않은 검증을 pass로
  적지 않는다.
- report의 검증 절은 명령마다 한 행을 쓴다:
  `| 요구한 문서 경로 | 그 문서의 해당 문장 인용 | 명령 | 결과 또는 Not Run 사유 |`.
  문서가 요구하지 않았지만 실행한 명령은 문서 칸에 `게이트 원장`이나 `스킬`처럼 실제 출처를 적는다.
- 미충족 게이트가 남으면 여기서 멈추고 4단계로 돌아간다. 원장을 고쳐 통과시키지 않는다.

## 2 스키마 실측과 기록

변경 집합에 마이그레이션·엔티티·`.sql`·`schema.prisma` 파일이 있을 때만 활성화된다.
없으면 이 게이트는 뜨지 않는다.

활성화되면 추정이 아니라 **실제 데이터베이스 관찰값**을 요구한다. 대상 테이블의 기존
인덱스 현황과 row 수, 그리고 그 값을 어디서 봤는지다. 조회는 [`database-design`](../database-design/SKILL.md)
또는 DB MCP 서버로 한다.

커넥션을 소모하는 대형 스캔을 던지지 않는다. `COUNT(*)` 전수 대신 카탈로그의 추정 row
수(`pg_class.reltuples`, `information_schema`, `SHOW INDEX`)를 쓰고 필요하면 `LIMIT`을
건다. 운영 DB에서 무거운 쿼리 하나가 커넥션 풀을 마르게 한다.

```bash
issueops schema-evidence record --id "$ISSUEOPS_ID" \
  --measurement "orders: 8.4M rows(reltuples), idx_orders_user_id 없음" \
  --source "mcp db-bc-prod execute_sql_bc_prod_market" \
  $RECORD_ACTOR_FLAGS --json
```

- measurement와 source는 짝이다. 출처 없는 수치는 추정과 구분되지 않는다.
- 관찰이 불가능하면 `--waive --waiver-rationale "<근거>"`로 남긴다. rationale 없는
  waive는 게이트를 열지 않는다.
- 실측 결과가 구현을 바꿔야 한다면 그것은 이 단계가 아니라 4단계의 일이다. row 수가
  크면 인덱스 생성 전략, 마이그레이션 잠금 시간, 백필 배치 크기가 달라진다.

## 3 구현 리뷰

[`issueops-review`](../issueops-review/SKILL.md) 스킬 파일을 열고, 대상 `diff`로 그 `## 실행` 절을 따른다.
`--target diff`는 CLI 명령이 아니라 그 스킬의 대상 구분이다(`issueops review` 명령은 없다). 리뷰는 이 세션이
지금 delegation 도구로 띄우는 빈 컨텍스트 서브에이전트이며, 명령 파일에 적어 두고 끝내지 않는다. 띄울 수
없으면 판정 없이 그 사실과 이유를 보고한다. 판정은 서브에이전트가 돌려준 결과로만
`issueops implementation-review record`에 기록한다. 루프 절차는 그 스킬이 소유한다. 이 단계가 아는 것은 여섯이다.

- 리뷰어에게 diff와 **계획을 함께** 준다. 무엇을 하기로 했는지 모르는 리뷰어는 구현이
  계획에서 벗어났는지 판정할 수 없다.
- `pass`만 통과한다. `revise`면 지적을 고쳐야 하므로 4단계로 돌아간다. 이 단계에서
  고치면 fingerprint가 바뀌어 앞 판정이 전부 stale이 된다.
- 모드에 따른 면제는 없다. execution이 있는 사이클은 전부 이 게이트의 대상이다.
- **계획 리뷰가 남긴 주장을 함께 준다.** `issueops status --id "$ISSUEOPS_ID" --json`의
  `devils_advocate_review.findings`와 `history`의 finding을 "검증할 주장 목록"으로
  프롬프트에 넣는다. 리뷰어는 diff 전체를 탐색하기 전에 그 주장이 실제로 지켜졌는지
  확인한다. 계획 리뷰에서 살아남은 위험이 구현에서 되살아났는지가 가장 싸게 잡히는 결함이다.
- **코드베이스 존중 렌즈는 `next.review.lenses`만 적용한다.** `issueops next --id "$ISSUEOPS_ID" --json`이
  돌려주는 티어와 렌즈를 프롬프트에 넣고 그 목록만 검토하게 한다. `docs-only` 티어는
  side effect 렌즈 하나다.
- **`review.frontend`가 true면 UI 렌즈를 더한다.** diff 리뷰 프롬프트의 "검증할 주장
  목록"에 4단계 report의 `## UI 판단` 절을 넣고, 렌즈 목록에 접근성·반응형 상태·모션
  감소 세 항목을 덧붙인다. 이 셋이 [`ui-ux-craft`](../ui-ux-craft/SKILL.md)가 소유한
  판단이며, frontend 사이클의 리뷰 finding에 이 렌즈 언급이 하나도 없으면 프롬프트가
  실패한 것이다.

`next.review.tier`가 `schema-auth`이고 `git -C "$WORKTREE" diff --stat "$BASE_SHA"`의
변경 줄 수가 500을 넘을 때만 렌즈 네 개를 서브에이전트 넷으로 나눈다. 합치는 규칙은
"필수 결함이 하나라도 있으면 `revise`"다. 그 밖의 티어에서는 나누지 않는다 — 조정
비용이 절약한 시간을 넘는다. 이 분할 조건은 이 문장이 단독으로 소유하며 코드에는 없다.

## 4 호환성 재확인과 readiness

strict readiness `warnings`의 `base_advanced`는 차단이 아니다. 이 단계에서는
`issueops execution sync-base --id "$ISSUEOPS_ID" --preview $ACTOR_FLAGS --json`으로 충돌
유무만 확인해 report에 적고 **apply하지 않는다.** apply는 봉인된 변경 집합에 base의
파일을 끌어들여 fingerprint를 바꾸고, 정리·구현 리뷰·문서 반영 판정이 한꺼번에 stale이
되어 5단계부터 다시 밟게 만든다. 머지는 PR 병합 시점에 provider가 한다. 충돌이 있으면 그
사실을 PR 본문의 위험 절에 적는다.

구현된 diff가 계획 시점의 compatibility review와 다르면 durable 판정을 최신으로 맞춘다.
1절의 `## 의도 대조`에 미충족 항목이 있으면 approved로 기록하지 않는다.

```bash
issueops compatibility review --id "$ISSUEOPS_ID" \
  --backward-compatibility "<실제 diff 기준>" --side-effect "<실제 diff 기준>" \
  --rollback-plan "<실제 되돌리는 방법>" --verification "<이 단계에서 실행한 검증>" \
  --approved $RECORD_ACTOR_FLAGS --json

issueops pr-readiness --id "$ISSUEOPS_ID" --strict --json
```

strict readiness의 `missing`이 `worktree_clean`, `upstream`, `upstream_fetch`,
`upstream_synced`의 부분집합이면 남은 일은 커밋과 푸시뿐이다. 그 밖의 키가 남으면
`next`가 가리키는 단계로 돌아간다. 특히 `gates_incomplete:*`와 `*_stale`은 앞 단계로
되돌아가라는 뜻이다.

## 출구

다음은 8단계 커밋·푸시다. [`atomic-commit-push`](../atomic-commit-push/SKILL.md)로
plan.md, gates.md, verified-execution report, 문서, 구현을 커밋·푸시하고, `next`가 렌더한
`phase --to pr`를 실행한다.

## 나쁜 예

- 배터리가 실패했는데 동시에 돌던 리뷰의 `pass`를 기록한다. 그 판정은 무효인 diff에
  대한 것이다.
- 검증 단계에서 `gates check --write`를 실행한다. 원장이 바뀌어 봉인이 stale이 된다.

| 나쁜 행동 | 문제 |
|---|---|
| 이 단계에서 파일을 고친다 | 앞 두 단계의 봉인과 판정이 동시에 stale이 된다 |
| 실행하지 않은 검증을 pass로 기록한다 | 기록은 남고 검증은 없다 |
| 리뷰 없이 구현 리뷰를 pass로 기록한다 | 게이트 연극이다 |
| 운영 DB에 `SELECT COUNT(*)` 전수 스캔을 던진다 | 커넥션 풀을 마르게 한다. 카탈로그 추정치를 쓴다 |
| revise 지적을 이 단계에서 고치고 재리뷰를 생략한다 | fingerprint가 바뀌어 판정이 stale이 되거나, 검토되지 않은 수정이 게시된다 |
| 미충족 게이트를 원장 수정으로 통과시킨다 | 원장이 통과하고 결과는 검증되지 않는다 |
| 이 단계에서 커밋한다 | 커밋은 8단계다. 여기서 커밋하면 무엇을 검증한 상태인지 흐려진다 |

## 검증

- `issueops pr-readiness --id "$ISSUEOPS_ID" --strict --json`의 `missing`이
  커밋·푸시로 해소되는 키만 남았다.
- `issueops status --id "$ISSUEOPS_ID" --json`의 `implementation_review`와
  `schema_evidence`(활성화된 경우)가 현재 fingerprint에 묶여 있다.
- `git -C "$WORKTREE" status --porcelain`이 이 단계 시작 때와 같다. 달라졌으면 이 단계가
  파일을 바꾼 것이다.
