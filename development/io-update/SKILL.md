---
name: io-update
description: "Use when the user requests io update, issueops update, native skill refresh, or reinstalling the current IssueOps source checkout. Updates the binary and Codex, Claude, Omo, omp, and opencode integration without fetching source or changing Git history."
---

# IO Update

`io update`를 현재 issueops checkout의 검증 가능한 install transaction으로
실행한다. 이 스킬은 source를 원격에서 가져오지 않으며 Git history를 바꾸지 않는다.

## 의미

| 요청 | 실행 |
|---|---|
| `io update` / 하네스 업데이트 | dry-run 확인 후 `io update --json` |
| update 계획만 확인 | `io update --dry-run --json`만 실행 |
| 기존 binary 재사용 | 사용자가 명시한 경우에만 `--skip-build` |
| project-local 파일도 설치 | 사용자가 명시한 경우에만 `--project-local` |
| PATH 변경 회피 | 사용자가 명시하면 `--path-mode=skip` |
| 원격 source 갱신 | 이 스킬의 책임이 아님. `git pull`을 대신 실행하지 않는다. |

`io update`는 설치된 `io`가 가리키는 issueops checkout을 source of truth로
사용한다. 현재 작업 디렉터리가 다른 repository여도 update source는 바뀌지 않는다.

## 시작 확인

다음 세 명령을 먼저 실행한다.

```bash
command -v io
io version
io update --help
```

- `io`가 없으면 임의 경로를 추측하지 말고 설치 상태를 보고한다.
- `--dry-run`, `--json`, `--skip-build`, `--project-local`, `--path-mode` 계약을
  help에서 확인한다.
- issueops checkout이 dirty이면 update를 막지는 않는다. 다만 현재
  uncommitted byte가 build·설치된다는 사실을 실행 전에 명시한다.
- update 요청이 명시되지 않았다면 user-scope 파일을 쓰지 않는다.

## Dry-run

실제 실행과 같은 선택 flag에 `--dry-run --json`만 추가한다.

```bash
io update --dry-run --json
```

다음을 확인한다.

- top-level `ok`가 `true`다.
- `root`가 의도한 issueops checkout이다.
- `hosts`의 Codex, Claude, Omo, omp, opencode 항목이 모두 성공한다.
- 새 link와 제거될 stale link가 요청 범위에 맞다.
- dry-run은 binary와 host 설정을 변경하지 않는다.

dry-run이 실패하거나 예상하지 않은 root·project-local write를 보이면 실제 update를
실행하지 않는다.

## 실행

기본 실행은 JSON evidence를 남긴다.

```bash
io update --json
```

사용자가 선택 flag를 지정했다면 dry-run과 실제 실행에 같은 flag를 사용한다.
`--skip-build`를 build 실패 회피 수단으로 추가하지 않는다. build 실패는 source
결함으로 처리하고 실패 출력을 보존한다.

update는 다음을 하나의 transaction으로 처리한다.

1. 현재 checkout에서 `bin/issueops`를 build한다.
2. Codex, Claude, Omo, omp, opencode user-scope skill link와 MCP·lifecycle 설정을 갱신한다.
3. stale harness-owned link를 제거한다.
4. native activation receipt를 readback해 봉인한다.

## 완료 확인

update 출력에서 다음을 확인한다.

- `ok: true`
- `committed: true`
- 비어 있지 않은 `transition_id`
- 모든 `hosts[].ok: true`
- `native activation receipt sealed` message

그다음 실제 새 binary를 사용한다.

```bash
io inspect --json
io docs --json
```

`inspect`와 `docs`의 `ok`가 `true`여야 한다. 새 MCP 코드는 host가 `issueops mcp`를
다시 띄울 때(세션 재시작이나 MCP 재연결) 적용된다. 이미 열린 세션의 MCP가 옛 동작을
보이면 update 실패로 추측하지 말고 그 세션의 MCP 재연결 여부를 확인한다.

## 실패 처리

- 실패한 update를 성공으로 요약하지 않는다.
- stdout/stderr와 exit code를 보존하고 실패한 단계(build, install, activation
  readback)를 구분한다.
- 같은 명령을 맹목적으로 반복하지 않는다. 원인을 수정한 뒤 dry-run부터 다시 시작한다.
- dry-run 성공을 실제 설치 성공으로 보고하지 않는다.
- update 과정에서 `git pull`, commit, push, branch 변경을 실행하지 않는다.
- secret-like 경로나 credential 원문이 출력되면 완료 보고 전에 redaction 문제로
  처리한다.

## 완료 보고

다음만 간결하게 보고한다.

| 항목 | 근거 |
|---|---|
| source | update 출력의 `root` |
| 결과 | exit code, `ok`, `committed`, `transition_id` |
| host | Codex·Claude·Omo·omp·opencode `hosts[].ok` |
| runtime | `inspect`, `docs` readback |
| 선택 flag | `--skip-build`, `--project-local`, `--path-mode` 사용 여부 |
| 미실행 | 생략한 검증과 이유 |
