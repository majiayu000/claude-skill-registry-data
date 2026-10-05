---
name: setup-hooks
description: >
  위험한 shell 명령을 막는 안전 훅을 Claude Code와 Codex 설정에 설치하거나 제거하는 스킬.
  파괴적 git 명령 auto-stash, force push 차단, rg --replace 차단을 포함한다.
  "hooks 설치", "guard 설치", "setup hooks", "install hooks", "훅 설정",
  "codex hook 설치", "hooks 제거", "guard 제거", "uninstall hooks", "훅 삭제",
  "rg -r 막아줘", "위험한 명령 차단" 등에서 트리거.
---

# setup-hooks

이 플러그인에 포함된 shell 명령 안전 훅을 사용자의 CLI 도구 설정에 등록하거나 제거한다.

설치 요청을 받으면 대상 에이전트를 먼저 확인한다. 사용자가 `Codex`, `codex hook`, `~/.codex`를 언급하면 Claude Code 설정을 건드리지 말고 Codex 전용 절차를 수행한다.

## 스크립트 구성

| 파일 | 역할 |
|------|------|
| `shell_lex.py` | 셸 인용·heredoc 인식 렉서. 아래가 import하며 단독 실행하지 않는다 |
| `guard_rules.py` | 명령 분류 로직과 rg 플래그 집합. 세 훅이 import하며 단독 실행하지 않는다 |
| `guard-commands.py` | Claude Code용 훅. rewrite + deny 정책 |
| `guard-commands-codex.py` | Codex용 훅. deny 전용 정책 |
| `auto-backup.sh` | rewrite된 명령이 원 명령 앞에서 호출하는 백업 단계. 훅으로 등록하지 않는다 |
| `rg-replace-flag-fix.py` | Claude Code용 훅. `rg -rn` 형태 short-flag 클러스터를 rewrite로 교정 |
| `install-codex-hook.sh` | Codex `hooks.json` 등록/해제 |
| `test-guard-rules.py` | 두 guard 훅 계약 테스트. `python3 test-guard-rules.py` |
| `test-auto-backup.sh` | `auto-backup.sh` 계약 테스트. `bash test-auto-backup.sh` |
| `test-rg-replace-flag-fix.py` | `rg-replace-flag-fix.py` 계약 테스트. `python3 test-rg-replace-flag-fix.py` |

```
${CLAUDE_PLUGIN_ROOT}/skills/setup-hooks/scripts/guard-commands.py
${CLAUDE_PLUGIN_ROOT}/skills/setup-hooks/scripts/rg-replace-flag-fix.py
~/.agents/skills/setup-hooks/scripts/guard-commands-codex.py
```

세 훅은 모두 같은 디렉토리의 `shell_lex.py`와 `guard_rules.py`를 import하고, rewrite된 명령은 `auto-backup.sh`를 절대경로로 호출한다. 파일은 항상 함께 배치한다 — import가 실패하면 훅은 조용히 통과하므로 아무것도 지키지 않는다.

## 판정 방식

`shell_lex.py`가 명령 문자열을 셸이 실제로 실행할 명령 단위로 나눈 뒤, **각 세그먼트의 command word와 서브커맨드가 실제로 무엇인지**로 판정한다. 부분 문자열 매칭이 아니다. 따라서 `echo 'git clean -fd'`나 `git commit -m "git clean 버그 수정"`처럼 위험 명령을 **언급만** 하는 경우는 통과한다.

세그먼트 분리는 인용을 인식한다. `|`, `;`, `&`, 개행이 구분자가 되는 것은 **인용 밖에 있을 때뿐**이고, heredoc 본문은 명령이 아니라 stdin 데이터이므로 아예 판정 대상이 아니다. 이것이 계약의 핵심이다 — 구분자가 인용을 무시하면 실행되지 않을 가짜 세그먼트가 만들어지고, `git commit -m "fix; git reset --hard 제거"` 같은 무해한 커밋이 파괴적 명령으로 판정된다. 그 오탐은 deny보다 나쁘다. rewrite 경로에 걸리면 auto-backup이 실제로 실행되어 working tree가 조작되기 때문이다.

토큰은 인용을 제거한 상태로 비교하므로 `git push "--force"`처럼 인용된 플래그도 실제로 git이 받는 대로 판정된다. command word는 basename으로 본다 — `/usr/bin/git`은 `git`이다.

## 동작 요약

### Claude Code

파괴적이지만 복구 가능한 명령은 차단하지 않고 rewrite한다. 원 명령 앞에 `bash <scripts>/auto-backup.sh '<label>' && `를 붙이는 형태다. 백업 스크립트가 `git stash push --include-untracked`로 백업을 만든 뒤 working tree를 즉시 원복하므로, 원래 명령은 진짜 dirty state에 그대로 실행되어 사용자 의도가 보존되고 stash entry는 복구 지점으로 남는다. stash로 되돌릴 수 없는 것만 deny한다.

`;`가 아니라 `&&`인 것이 계약의 절반이다. working tree를 되돌리지 못했으면 스크립트가 non-zero로 끝나 원 명령이 실행되지 않는다. 백업만 남고 tree는 비워진 채 파괴적 명령이 도는 경로가 없다.

| 명령 | 동작 |
|------|------|
| `git clean` | auto-backup 후 실행 |
| `git clean -n` / `--dry-run` / `-i` | 통과 (실제 삭제 없음) |
| `git reset --hard` | auto-backup 후 실행 |
| `git restore .` / `git restore <file>` | auto-backup 후 실행 |
| `git restore --staged <file>` / `-S <file>` | 통과 (index만 갱신) |
| `git restore --staged --worktree <file>` / `-SW` | auto-backup 후 실행 |
| `git checkout .` / `git checkout -- <file>` | auto-backup 후 실행 |
| `git checkout <ref> <path>` (`--` 없음) | auto-backup 후 실행 |
| `git checkout -f <branch>` / `--force` | auto-backup 후 실행 |
| `git checkout <branch>` (DWIM) | 통과 (git이 dirty 충돌 시 거부) |
| `git checkout -b <new> <start>` | 통과 (파일을 건드리지 않음) |
| `git push --force` / `-f` | deny |
| `git push --force-with-lease` / `--force-if-includes` | 허용 |
| `rg -r <값>` / `--replace <값>` | deny |
| `rg -rn` / `-rl` / `-rln` 등 클러스터 | `-r` 제거 후 실행 (`rg-replace-flag-fix.py`) |
| `rg -o -r '$1' ...` | 허용 (캡처 그룹 추출) |

복구: `git stash list` → `git stash apply stash@{N}` (백업이 필요할 때만).

`auto-backup.sh`의 판정:

| 상황 | 동작 |
|------|------|
| git repo 밖 | 백업 없이 exit 0. 원 명령 실행 |
| clean tree | 백업 없이 exit 0. 원 명령 실행 |
| dirty tree, 원복 성공 | 백업 생성 + tree 원복 + stderr 한 줄 + exit 0 |
| dirty tree, `--index` 원복만 실패 | tree는 원복. staged/unstaged 구분 손실을 경고하고 exit 0 |
| dirty tree, 원복 실패 | stash 유지 + 복구 안내 + exit 1. 원 명령 미실행 |

백업 stash 메시지는 `auto-backup [<worktree>] before <label> <stamp>` 형태다. `refs/stash`는 repo 전역이라 worktree가 여럿이면 branch 이름만으로는 어느 tree의 백업인지 구분되지 않는다.

retention: 백업이 성공할 때마다 `auto-backup ` 표식을 가진 stash 중 **최근 10개를 제외하고 7일이 지난 것**을 지운다. 사람이 직접 만든 stash는 표식이 없어 대상이 아니다. 파라미터는 `auto-backup.sh` 상단 `KEEP_RECENT`, `PRUNE_AFTER_DAYS`.

### Codex

Codex 훅은 shell command rewrite를 하지 않는다. 현재 Codex 훅 출력에서 `updatedInput` rewrite는 신뢰하지 않는다. 따라서 위 표에서 rewrite에 해당하는 명령은 모두 deny하고, agent에게 `auto-backup.sh`를 먼저 실행한 뒤 재시도하라고 안내한다. 안내는 stash 파이프라인을 직접 적지 않고 스크립트를 가리킨다 — 손으로 쓴 `git stash push && git stash apply`는 clean tree에서 무관한 stash를 되살린다. `-rn` 클러스터도 rewrite 대신 deny하며, `-r`을 빼고 재시도하라는 교정을 함께 전달한다. 통과/허용 항목은 Claude Code와 동일하다.

## rg -r을 다루는 방식

`-r`은 recursive 플래그가 아니라 `--replace`이고 값을 소비한다. rg는 기본이 재귀 검색이라 recursive 플래그 자체가 없다. 여기서 성격이 다른 두 함정이 나온다.

| 함정 | 예 | 결과 | 처방 |
|------|-----|------|------|
| short-flag 클러스터 | `rg -rn foo .` | `-r`이 `n`을 replacement로 먹어 모든 매치가 `n`으로 출력 | 의도가 명확하므로 `-r`을 떼고 실행 |
| 공백 분리 / long form | `rg -r 'foo' src/` | `foo`가 replacement, `src/`가 **패턴** | 의도를 추측할 수 없으므로 deny |

두 번째는 rewrite가 원리적으로 불가능하다. `-r 'foo'`만 떼면 `rg src/`가 되어 여전히 틀린 검색이고, 진짜 의도인 `rg 'foo' src/`로 복원하려면 어느 인자가 패턴인지 추측해야 한다. 추측이 필요하면 막고 사람이 다시 쓰게 하는 편이 맞다.

`--replace`가 파일을 수정한다고 착각하는 경우도 같은 룰에 걸린다. rg는 어떤 플래그로도 파일을 수정하지 않고 출력 라인만 치환한다.

세 경우 모두 exit 0으로 끝나고 그럴듯한 출력을 내므로 실패로 드러나지 않는다. 반면 `-o`와 함께 쓰는 캡처 그룹 추출(`rg -o -r '$1' ...`)은 의도가 명확하므로 허용한다.

클러스터 교정은 `rg-replace-flag-fix.py`가 담당하고 `guard-commands.py`는 관여하지 않는다. guard가 먼저 deny하면 교정 기회가 사라지기 때문이다. 두 훅의 등록 순서는 무관하다. 대신 "무엇이 클러스터인가"는 `guard_rules.py`의 `RG_BOOL_FLAGS` 하나로 판정한다 — 양쪽이 따로 정의하면 guard가 교정을 기대하고 통과시킨 클러스터를 교정 훅이 그대로 두는 구멍이 생긴다. Codex는 rewrite를 쓰지 않으므로 `guard-commands-codex.py`가 클러스터도 deny한다.

교정 범위는 **인용 밖 토큰뿐이다**. 따옴표 안 텍스트와 heredoc 본문은 플래그가 아니라 데이터라서, 건드리면 명령의 동작이 아니라 명령이 남기는 내용이 바뀐다 — `echo "rg -rn 쓰지 마세요" >> notes.md`가 반대 뜻을 파일에 기록하고, 피해가 검색 한 번이 아니라 파일에 남는다. 탐지는 `shell_lex.py`가 인용 구간을 지운 사본에서 하고 치환은 원본에 적용해 두 위치가 어긋나지 않게 한다. 계약 테스트는 `python3 test-rg-replace-flag-fix.py`.

## 프로토콜

### Claude Code

- **입력**: `{ "tool_input": { "command": "..." } }`
- **출력**: rewrite 시 `updatedInput`, 차단 시 `permissionDecision: "deny"`, 해당 없으면 exit 0 (빈 출력)

### Codex

- **입력**: `PreToolUse` JSON의 `tool_name`, `tool_input.command`
- **출력**: 차단 시 `hookSpecificOutput.permissionDecision: "deny"`와 non-empty `permissionDecisionReason`
- **제약**: `permissionDecision: "allow" | "ask"`, `updatedInput`, `additionalContext`는 사용하지 않는다.

## 설치 가이드

### Claude Code (`~/.claude/settings.json`)

`hooks.PreToolUse` 배열에 Bash matcher로 등록한다. 이미 Bash matcher가 있으면 해당 `hooks` 배열에 추가한다.

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          // ... 기존 훅들 ...
          {
            "type": "command",
            "command": "python3 /absolute/path/to/guard-commands.py",
            "statusMessage": "Guarding risky shell commands..."
          },
          {
            "type": "command",
            "command": "python3 /absolute/path/to/rg-replace-flag-fix.py",
            "statusMessage": "Repairing rg flag clusters..."
          }
        ]
      }
    ]
  }
}
```

ref: https://code.claude.com/docs/en/hooks

### Codex (`~/.codex/hooks.json`)

`npx skills add ./`는 스킬 파일을 설치/동기화하는 단계이고, hook 등록은 별도 설정 파일 변경이다. Codex hook 설치 요청까지 받은 경우 다음 순서로 끝까지 수행한다.

1. `npx skills add ./ -g --skill setup-hooks --agent '*' -y` 또는 사용자가 지정한 `npx skills` 설치 명령으로 최신 `setup-hooks`를 설치한다.
2. 설치된 스킬 경로의 등록 스크립트를 실행한다.

```bash
bash ~/.agents/skills/setup-hooks/scripts/install-codex-hook.sh install
```

제거:

```bash
bash ~/.agents/skills/setup-hooks/scripts/install-codex-hook.sh remove
```

이 스크립트는 구 이름(`guard-commands-codex.sh`, `guard-untracked-codex.sh`)으로 등록된 handler도 함께 제거하므로 중복 등록이 생기지 않는다.

### 다른 CLI 도구

동일한 stdin/stdout JSON 프로토콜을 지원하는 도구라면 해당 도구의 pre-execution hook에 `python3 /path/to/guard-commands.py`를 등록한다. 도구별 설정 문서를 참조.

## 설치/제거 절차

Claude Code 대상으로 "훅 설치해줘" 또는 "훅 제거해줘"라고 요청하면:

1. **설치 시**: `~/.claude/settings.json`을 읽고, `hooks.PreToolUse`에 `guard-commands.py`와 `rg-replace-flag-fix.py` 항목이 없으면 추가한다. 기존 Bash matcher가 있으면 그 `hooks` 배열에 append한다.
2. **구 이름 정리**: command에 `guard-commands.sh` 또는 `guard-untracked.sh`가 포함된 항목이 있으면 함께 제거한다. 남겨두면 훅이 이중 등록되어 stash가 두 번 생기고, 삭제된 스크립트를 가리키는 항목은 매 Bash 호출마다 에러를 낸다.
3. **제거 시**: Bash matcher에서 두 항목만 제거한다. Bash matcher의 hooks가 비면 matcher 자체를 제거한다.
4. 설정 변경 후 Claude Code 재시작 필요.

이미 해당 파일명이 command에 포함되어 있으면 skip한다.

Codex 대상으로 "codex hook 설치해줘"라고 요청하면:

1. `~/.codex/hooks.json`이 있는지 확인한다.
2. `install-codex-hook.sh install`을 실행한다.
3. `jq`로 `~/.codex/hooks.json`을 파싱하고 `guard-commands-codex.py` handler가 하나만 있는지 확인한다.
4. 설정 변경 후 Codex 재시작 필요.

## Gotchas

- settings.json은 세션 시작 시 로드된다. 설치/제거 후 반드시 재시작.
- 판정은 세그먼트의 command word 기준이므로 `bash -c "git clean -fd"`, `$(git clean -fd)`, `xargs git clean` 형태는 통과한다. 이 훅은 실수 방지 장치이지 sandbox가 아니다.
- heredoc 본문도 같은 이유로 통과한다. `bash <<EOF`로 넘긴 파괴적 명령은 걸리지 않는다. 본문을 명령으로 읽으면 `cat > notes.md <<EOF` 같은 문서 작성이 파괴적 명령으로 판정되는 쪽이 훨씬 흔하고, 그 오탐은 문서를 쓰려던 명령 앞에 stash를 실행한다.
- stdin이 JSON이 아니거나 sibling 모듈을 import할 수 없으면 훅은 조용히 exit 0 한다. 훅이 매 Bash 호출마다 에러를 내는 것이 차단 실패보다 나쁘다. 세 훅 모두 `python3`를 요구하고, `jq`는 더 이상 훅 실행에 필요하지 않다(`install-codex-hook.sh`는 여전히 사용).
- `rg -rn` 클러스터 교정은 Claude Code 전용이다. Codex는 rewrite를 지원하지 않아 같은 입력을 deny하고 교정 방법만 안내한다.
- 판정 로직을 고치면 `python3 test-guard-rules.py`를 돌린다. 두 훅을 subprocess로 실행해 Claude Code의 rewrite/deny/pass와 Codex의 deny/pass를 함께 확인하므로, 정책 분기까지 회귀 판정 범위에 들어간다.
- stdin은 판정보다 먼저 읽는다. 읽기 전에 빠져나가면 호출자 쪽 write가 EPIPE로 실패한다.
- `git checkout <ref> <path>`는 `--` 없이도 파일을 덮어쓴다. DWIM branch 전환과의 구분은 operand 개수이고, `-b`/`-B`/`--orphan`이 있으면 두 번째 operand는 start point이므로 통과한다.
- `git push --force`는 stash로 보호할 수 없어 deny한다. `--force-with-lease`는 토큰 단위 비교라 `--force` 룰에 걸리지 않지만, 둘을 함께 쓰면 `--force`가 우선하므로 deny된다.
- `git stash push`는 clean tree에서 아무것도 저장하지 않고도 exit 0이다. 그래서 `auto-backup.sh`는 exit code가 아니라 `refs/stash` before/after 비교로 백업 생성 여부를 판정한다. exit code로 판정하면 뒤따르는 `git stash apply`가 stack 맨 위의 **무관한 stash**를 clean tree에 쏟아 conflict marker와 unmerged index를 남긴다. 아무것도 파괴할 것이 없던 명령이 tree를 깨뜨리는 경로다.
- `cd a && cd b && git clean` 같은 체인은 cd 전체가 backup 앞에 유지된다. 그렇지 않으면 stash가 엉뚱한 레포에 생긴다. 변수 대입이나 개행이 섞인 명령은 cd 인식에 실패할 수 있고, 그때 백업은 원 명령과 다른 레포에서 돌아 그 tree를 원복한 뒤 stash 하나를 남긴다. stderr 한 줄이 그 사실을 드러내고 retention이 정리한다.
- 백업을 만들었을 때 `auto-backup.sh`는 stderr에 한 줄을 남긴다. 이 출력을 지우면 엉뚱한 레포에 생긴 백업이 조용히 쌓인다.
- `git stash drop`은 그보다 큰 index를 한 칸씩 당긴다. retention이 높은 index부터 지우는 이유이고, 낮은 쪽부터 지우면 두 번째 drop이 엉뚱한 stash를 지운다.
- Codex 훅은 side effect를 만들지 않는다. PreToolUse 단계에서 훅이 직접 `git stash`를 실행하면 실제 원명령이 취소되어도 stash가 남으므로, Codex에서는 차단과 안내만 수행한다.
