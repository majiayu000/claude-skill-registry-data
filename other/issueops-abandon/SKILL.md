---
name: issueops-abandon
description: Leave an IssueOps cycle safely from any stage. Pause by releasing the execution lease so another session or host can resume it, or abandon the cycle by closing its draft PR or MR, closing the issue, deleting the remote branch, and removing the worktree, local branch, and record through one fingerprinted cleanup abandon. Use when the user says "중단", "탈출", "이슈옵스 정리", "일시 중단", "abandon the cycle", or when "issueops next" reports an abandon exit.
---

# IssueOps Abandon

이 스킬의 일은 **사이클에서 안전하게 빠져나오는 것**이다. 잠시 멈추는 것과 완전히
버리는 것은 다른 일이므로 다른 경로를 쓴다. 머지된 사이클의 정리는 이 스킬이 아니다.

- 전체 흐름과 단계 판별: [`issueops`](../issueops/SKILL.md)
- 머지 뒤 정리: [`issueops-cleanup`](../issueops-cleanup/SKILL.md)
- WIP 커밋·푸시: [`atomic-commit-push`](../atomic-commit-push/SKILL.md)

## 이 스킬이 맞는지 확인

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

어느 stage에서든 들어올 수 있다. 읽어야 하는 것은 두 곳이다.

- `exits.pause_command`가 있으면 이 세션이 홀더다. 일시 중단이 가능하다.
- `exits.abandon_command`는 항상 있다. 폐기의 첫 명령이다.
- `lease.status`와 `lease.holder_is_self`가 어느 경로를 쓸 수 있는지 결정한다.

머지된 아티팩트를 가진 사이클이면 폐기가 게이트에서 막힌다. 그때는
[`issueops-cleanup`](../issueops-cleanup/SKILL.md)이 맞다.

## 두 경로

| 경로 | 조건 | 남는 것 |
|---|---|---|
| 일시 중단(pause) | 이 세션이 홀더다 | record, 워크트리, 브랜치, 원격이 모두 남는다. 다른 세션이나 다른 호스트가 이어받는다 |
| 폐기(abandon) | 어느 단계든 | record, 워크트리, 로컬 브랜치가 사라진다. 원격 효과는 고른 것만 일어난다 |

재개와 인수는 이 스킬의 명령이 아니다. 아래 절이 그 이유를 설명한다.

## 일시 중단

```bash
issueops execution status --id "$ISSUEOPS_ID" --json   # generation 확인
# WIP 처리: atomic-commit-push로 커밋·푸시하거나, 사용자가 명시하면 변경을 버린다.
cd "$WORKTREE" && issueops execution release --id "$ISSUEOPS_ID" \
  --generation "$GENERATION" $ACTOR_FLAGS --json
```

cwd가 canonical worktree와 **정확히** 같아야 한다. 다른 디렉터리에서 실행하면 홀더
확인이 실패한다. 커밋하지 않은 변경은 release가 지우지 않으므로, 무엇을 할지 먼저
정한다. 커밋·푸시하지 않고 release하면 다음 세션이 그 변경을 그대로 물려받는다.

## 재개·인수는 라우터가 안내한다

절차를 여기 복사하지 않는다. `issueops next`와 `execution status`가 렌더한
`next_command` 체인을 그대로 따르며, 그 체인의 각 행은 라우터
[`issueops`](../issueops/SKILL.md)의 `## 단계 표`가 소유한다.

- 사용자의 "그 세션은 껐다"는 quiescence 증거가 아니다. 인수는 관측된 상태 위에서만
  진행하며, 각 단계가 돌려준 명령만 실행한다.
- 호스트가 달라도 명령은 같다. `issueops execution whoami --json`의
  `claim_actor_flags`를 그대로 쓴다.
- 체인의 시작만 적어 둔다. 홀더가 죽었으면 `issueops execution replace
  --id "$ISSUEOPS_ID" --expected-generation "$GENERATION" --preview`이고, 그 다음부터는
  직전 명령이 돌려준 `next_command`만 실행한다. 중간 명령을 여기서 외워 쓰지 않는다.

홀더가 죽은 사이클을 폐기하려면 먼저 그 체인을 완주해 lease를 released나 self active로
만든다. 살아 있는 홀더를 가진 사이클은 폐기 게이트가 막는다.

## 프로젝트 문서 확인

폐기는 record·워크트리·로컬 브랜치를 지우고, 고른 원격 효과는 되돌릴 수 없다. preview
전에 `.issueops/CAUTIONS.md` 색인을 읽고, `project_docs_route`(MCP를 쓸 수 없으면
`issueops project route-docs --repo "$PWD" --task "<작업 요약>" --json`)에 "미머지 사이클 폐기와
원격 브랜치 정리" 같은 작업 요약을 넣어 폐기·잔여물·원격 브랜치에 관한 `cautions/` 기록을
고른다. 원격 정리 선택지를 물을 때 해당 주의사항을 문서 경로와 함께 적는다.

## 폐기

원격 효과를 먼저 정한 뒤(아래 `## 원격 정리 선택지`) 사용자가 고른 것만 플래그로
넣는다. 아래 `$REMOTE_FLAGS`는 답을 받은 뒤에 채운다. 예를 들어 PR만 닫고 이슈와 브랜치는
남기기로 했으면 `--close-pr` 하나다. 답을 받기 전에 세 플래그를 모두 넣은 명령을 적어 두지 않는다.

```bash
REMOTE_FLAGS="<고른 것만: --close-pr / --close-issue / --delete-remote-branch>"
issueops cleanup abandon --id "$ISSUEOPS_ID" --reason "$REASON" \
  $REMOTE_FLAGS --preview --json

# preview의 remote_effects, worktree, branch, fingerprint를 사용자에게 확인한 뒤
# 돌려준 next_command 그대로 실행한다.
issueops cleanup abandon --id "$ISSUEOPS_ID" --reason "$REASON" \
  $REMOTE_FLAGS --apply --confirm --fingerprint "$FP" --json
```

apply는 원격 효과를 record 삭제보다 **먼저** 실행한다. record가 사라진 뒤에는 `--id`
기반 명령이 아무것도 할 수 없으므로, 원격 정리를 나중으로 미룰 수 없다.

`--reason`에는 셸이 활성 문자로 읽는 것을 넣지 않는다. 따옴표, 백틱, `$`, `\`, `|`,
`&`, `;`, `<`, `>`, `(`, `)`, `*`, `?`, `~`가 들어가면 lease 가드가 명령을 거부한다.
사실만 간결하게 쓴다.

### 게이트와 해소

| missing | 뜻 | 해소 |
|---|---|---|
| `reason_required` | 사유가 없거나 금지 문자가 들어 있다 | 사실 문장으로 다시 쓴다 |
| `lease_terminal` | 살아 있는 writer가 있다(active·revoking) | 홀더면 release, 아니면 라우터의 인수 체인을 완주한다 |
| `worktree_clean` | 커밋하지 않은 변경이 있다 | 아래 `## dirty 워크트리 선택지` |
| `requester_occupies_worktree` | 지우려는 워크트리 **안에서** 폐기를 실행했다 | source checkout으로 나온 뒤 다시 실행한다 |
| `remote_artifact_unmerged` | 아티팩트가 머지됐거나 미머지를 관측하지 못했다 | 머지됐으면 `issueops-cleanup`이 맞다. 관측 실패면 provider 접근을 고친다 |
| `no_children` | 해소되지 않은 child가 남았다 | 각 child를 accept·reject·drop으로 끝낸다 |
| `worktree_identity_conflict`·`local_branch_head`·`branch_checked_out_elsewhere` | 잔여물이 record가 말하는 것과 다르다 | 무엇이 다른지 확인하고 사람이 판단한다. 지워서 맞추지 않는다 |
| `local_residue_execution` | record가 링크하지 않은 워크트리·브랜치가 있다 | 그 잔여물의 주인을 먼저 확인한다 |
| `pending_intent_safe` | 외부 작업 결과가 모호하다 | `execution reconcile --preview`로 정확히 하나를 확인한다 |

### execution 없이 끝난 사이클

`execution prepare`를 거치지 않고 provider에서 머지·종료된 사이클은 `Execution`도
`remote_artifact`도 없다. `cleanup finish`는 아티팩트를 검증할 수 없고 `cleanup orphan`은
record가 없기를 요구하므로, 이 사이클의 출구는 폐기뿐이다. record가 링크한 워크트리나
브랜치(`link-worktree`·`branch prepare`가 남긴 `worktree_path`)는 record 소유 잔여물로
인정되지만 canonical 경로·브랜치 일치·HEAD·clean 검사는 그대로 통과해야 한다. record가
링크한 적 없는 잔여물은 `local_residue_execution`으로 계속 막힌다. 폐기는 완료 증거를
이슈에 쓰지 않는다. provider의 MR·이슈가 그대로 증거로 남으므로 `--reason`을 사실대로
적는다.

## dirty 워크트리 선택지

폐기는 깨끗한 워크트리를 요구한다. 커밋하지 않은 변경이 있으면 사용자에게 번호로
묻는다.

1. **WIP를 커밋·푸시한 뒤 폐기한다.** 작업이 원격 브랜치에 남으므로 나중에 되찾을 수
   있다. 원격 브랜치를 지우기로 했다면 이 선택은 의미가 없으므로 함께 확인한다.
2. **변경을 버리고 폐기한다.** 되돌릴 수 없으므로 무엇을 버리는지(`git status --short`
   전체)를 보여 주고 별도 확인을 받는다.
3. **일시 중단으로 바꾼다.** 지금 결정하지 않고 lease만 놓는다.

## 원격 정리 선택지

preview 전에 번호로 묻는다. 고른 것만 플래그로 넣는다. 묻지 않고 전부 켜지 않는다.
질문 끝에 `주의사항:` 줄을 붙여 `## 프로젝트 문서 확인`에서 고른 항목을 "문서 경로: 해당 문장
인용"으로 적는다. 해당 항목이 없으면 대조한 문서 경로 목록과 "해당 없음"을 적는다.

1. **draft PR/MR을 닫는다**(`--close-pr`). 아티팩트가 있을 때만 의미가 있다.
2. **이슈를 닫는다**(`--close-issue`) 또는 열어 둔다. 다시 시작할 예정이면 열어 둔다.
   닫을 때는 `not planned`로 닫힌다.
3. **원격 브랜치를 삭제한다**(`--delete-remote-branch`) 또는 유지한다. 삭제는 관측한
   OID에 대한 lease로 실행되므로, 그 사이에 누가 push했으면 거부된다.

`issueops remote close-issue`와 `issueops cleanup
remote-branch`는 여기서 쓰지 않는다. 두 명령 모두 머지 증적을 요구하므로 미머지
사이클에서는 각각 아티팩트 검증 실패와 `phase_done` 미충족으로 막힌다(2026-09-04 실측).

## 나쁜 예

| 나쁜 행동 | 왜 나쁜가 | 대신 할 일 |
|---|---|---|
| 홀더가 살아 있는데 폐기 | 다른 세션이 쓰는 워크트리를 지운다 | 홀더 세션에서 release하거나 인수 체인을 완주한다 |
| `gh pr close`·`glab mr close`로 직접 닫기 | pending intent가 없어 모호한 결과를 회복할 수 없다 | `--close-pr` 플래그로 같은 일을 하게 한다 |
| 워크트리를 `rm -rf`로 지우기 | git 등록이 남아 다음 prepare가 깨진다 | apply가 `git worktree remove`로 지우게 한다 |
| `--reason`에 셸 문자 넣기 | lease 가드가 명령을 거부한다 | 사실 문장으로 다시 쓴다 |
| 머지된 사이클을 폐기로 정리 | 완료 증거가 이슈에 반영되지 않는다 | `issueops-cleanup`의 reflect → finish |
| record 삭제 뒤 원격 정리 시도 | `--id` 명령이 동작하지 않는다 | 폐기 플래그로 같은 실행 안에서 끝낸다 |

## 검증

- 일시 중단: `issueops execution status --id "$ISSUEOPS_ID" --json`의
  `lease.status`가 `released`이고 holder가 없다. 워크트리와 record는 그대로 있다.
- 폐기: `issueops status --id "$ISSUEOPS_ID" --json`이 record 없음을
  돌려준다. `git worktree list`에 그 경로가 없고 `git show-ref --verify
  refs/heads/<branch>`가 실패한다.
- 원격 효과를 골랐다면 apply 결과의 `remote_effects`, `pr_closed`, `issue_closed`,
  `remote_branch_deleted`가 고른 것과 일치하는지 확인한다.
- 부분 실패로 멈췄으면 record가 남아 있고 `cleanup_abandon_failure.step`이 어디서
  멈췄는지 말한다. 그 지점부터 다시 preview한다.
