---
name: tmux
description: >
  tmux를 통해 Claude Bash 도구 바깥의 프로세스와 상호작용하는 스킬.
  send-keys로 명령 전달, capture-pane으로 출력 읽기.
  SSH 원격 서버, 로컬 dev 서버 로그, 다른 Claude/Codex 인스턴스,
  장시간 빌드/테스트 등 다양한 시나리오에 대응.
  "서버 확인해줘", "ssh로 ~해줘", "원격에서 실행", "배포해줘",
  "서버 로그 확인", "dev 서버 로그 봐줘", "다른 터미널에서 실행해줘",
  "빌드 돌려놓고 결과 확인", "codex한테 시켜줘", "pane 확인",
  "tmux 세션 만들어", "로그 모니터링", "백그라운드에서 실행",
  "run on remote", "deploy to server", "check the server",
  "check dev server logs", "run in another terminal",
  "send to codex", "monitor logs"
  등에서 트리거.
---

# tmux

Claude Bash 도구는 로컬·동기 전용이다. tmux send-keys/capture-pane을 통해 다른 프로세스(SSH, dev 서버, 에이전트, 빌드)와 상호작용한다.

## 언제 tmux를 쓰는가

| 상황 | tmux? | 이유 |
|------|-------|------|
| SSH 원격 작업 | O | Bash 도구로 직접 불가 |
| dev 서버 (`pnpm dev`) | O | 장기 실행, 로그 모니터링 |
| 다른 Claude/Codex 인스턴스 | O | 에이전트 오케스트레이션 |
| 파일 워처, 테스트 워처 | O | 백그라운드 프로세스 |
| 10초 미만 단발 명령 | X | Bash 도구로 직접 실행 |
| stdout를 대화에 바로 써야 할 때 | X | capture-pane 경유하면 비효율 |

## 워크플로우

### 1. 세션/pane 탐색

기존 환경부터 확인한다. 새로 만들기 전에 재사용할 대상을 찾는다.

```bash
tmux list-sessions -F '#{session_name}: #{session_windows} windows'
tmux list-panes -t <session> -F '#{pane_index}: #{pane_current_command} (#{pane_width}x#{pane_height})'
```

재사용 판단: `pane_current_command`가 목적과 일치하면 재사용. 아니면 새 window 추가.

### 2. 세션 생성 (멱등)

`has-session`으로 존재 여부를 먼저 확인한다. 하나의 프로젝트 = 하나의 세션, 여러 프로세스 = 여러 window.

```bash
SESSION=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" || basename "$PWD")

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n main
fi
```

**inline command anti-pattern** — `new-session`에 명령을 직접 넘기면 shell init(PATH, direnv 등)을 우회한다. 반드시 `send-keys`로 실행:

```bash
# WRONG: tmux new-session -d -s work 'pnpm dev'
# RIGHT:
tmux new-session -d -s work -n dev
tmux send-keys -t work:dev 'pnpm dev' Enter
```

window 추가도 멱등하게:
```bash
if ! tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^logs$"; then
  tmux new-window -t "$SESSION" -n logs
  tmux send-keys -t "$SESSION:logs" 'tail -f app.log' Enter
fi
```

세션 생성 후 사용자에게 모니터 명령을 안내한다:
```
세션을 직접 보려면:
  tmux attach -t <session>
```

### 3. 접속/ready 확인

용도에 따라 분기:

**SSH**: 프롬프트 패턴 출현 polling.
```bash
for i in $(seq 1 10); do
  tmux capture-pane -t work -p -J | grep -qE '^\s*[\$#>]\s*$' && break
  sleep 1
done
```

**dev 서버**: ready 시그널 polling.
```bash
for i in $(seq 1 15); do
  tmux capture-pane -t work:dev -p -J | grep -q 'ready in\|listening on\|compiled' && break
  sleep 1
done
```

**에이전트**: 프롬프트(`❯`, `$`) 대기 후 상호작용.

### 4. 명령 실행

**기본 패턴:**
```bash
tmux send-keys -t <target> -l -- '<command>'
sleep 0.1
tmux send-keys -t <target> Enter
# 결과 필요 시 polling 또는 최소 대기 후 capture
sleep 1
tmux capture-pane -t <target> -p -J
```

핵심 플래그:
- **`-l`** (literal): 키 이름 해석을 방지. `Enter`라는 문자열을 보내야 할 때 필수.
- text와 `Enter`를 분리 전송하면 TUI에서 paste/multiline 엣지케이스를 피한다.

### 5. 긴 작업 polling

완료 마커 패턴:
```bash
tmux send-keys -t work -l -- 'long-command; echo __DONE__'
tmux send-keys -t work Enter
for i in $(seq 1 30); do
  tmux capture-pane -t work -p -J -S -50 | grep -q '__DONE__' && break
  sleep 2
done
```

에이전트/인터랙티브 프로세스는 마커 불가 — 셸 프롬프트 복귀로 완료 판단. 줄 시작 앵커 기반(`^\s*(❯|\$)\s*$`)으로 검사하거나, `pane_current_command`가 셸(bash/zsh)인지 확인하는 방식을 사용한다.

### 6. 출력 읽기

```bash
# 현재 화면 (줄바꿈 정리)
tmux capture-pane -t <target> -p -J

# 스크롤백 포함 (최근 200줄)
tmux capture-pane -t <target> -p -J -S -200

# 전체 스크롤백
tmux capture-pane -t <target> -p -J -S -

# 패턴 필터링
tmux capture-pane -t <target> -p -J -S -500 | grep 'ERROR\|WARN'
```

- **`-J`**: 줄바꿈(wrapped line) 아티팩트를 제거. 항상 붙인다.
- 출력이 길면 필터링한다. 전체 스크롤백을 컨텍스트에 넣지 말 것.

### 7. 다중 프로세스 관리

하나의 세션 안에서 window로 분리:
```bash
tmux new-window -t "$SESSION" -n server
tmux new-window -t "$SESSION" -n tests
tmux new-window -t "$SESSION" -n logs
```

전체 상태 확인:
```bash
tmux list-windows -t "$SESSION" -F '#{window_name}: #{pane_current_command}'
```

### 8. 에이전트 오케스트레이션

여러 Claude/Codex를 병렬로 실행:
```bash
for i in 1 2 3; do
  tmux new-window -t "$SESSION" -n "agent-$i"
  tmux send-keys -t "$SESSION:agent-$i" -l -- "cd /path/to/worktree-$i && claude 'Fix bug $i'"
  tmux send-keys -t "$SESSION:agent-$i" Enter
done
```

완료 감지 — 셸 프롬프트 복귀 확인:
```bash
for w in agent-1 agent-2 agent-3; do
  if tmux capture-pane -p -t "$SESSION:$w" -S -3 | grep -qE '^\s*(❯|\$)\s*$'; then
    echo "$w: DONE"
  else
    echo "$w: running..."
  fi
done
```

병렬 작업 시 git worktree로 브랜치 충돌을 방지한다.

멀티라인 프롬프트를 실행 중인 에이전트에 전송:
```bash
cat << 'EOF' | tmux load-buffer -
멀티라인 프롬프트 내용
EOF
tmux paste-buffer -t "$SESSION:agent-1"
tmux send-keys -t "$SESSION:agent-1" Enter
```

`send-keys`의 줄바꿈은 Enter로 변환되어 TUI가 즉시 제출한다. `paste-buffer`는 bracketed paste로 전달되므로 줄바꿈이 보존된다.

## Gotchas

- **capture-pane 빈 결과**: pane 크기가 0이거나 세션이 종료된 상태. `list-panes`로 존재 여부부터 확인.
- **send-keys 직후 capture 누락**: send-keys와 capture-pane 사이에 대기 필요. 단발 명령은 `sleep 1`, 네트워크/장시간 명령은 polling 패턴 사용.
- **SSH 호스트 키 / 비밀번호 프롬프트**: 자동으로 응답하지 말 것. 사용자에게 알리고 직접 입력하게 한다. sudo 비밀번호도 동일.
- **ANSI 이스케이프 오염**: 컬러 출력이 많으면 capture가 지저분하다. `| sed 's/\x1b\[[0-9;]*m//g'`로 정리하거나 `--no-color` 플래그.
- **기존 세션/pane 파괴 금지**: `kill-session`, `kill-server`는 사용자 확인 없이 실행하지 말 것. 다른 Claude 인스턴스나 사용자가 쓰고 있을 수 있다.
- **비-텍스트 TUI** (vim, htop): `send-keys`로 제어하지 말 것. 비대화형 대안 사용 (`cat`, `ps aux`).
- **텍스트 입력 TUI** (Claude Code, Codex 등): 단발 명령은 `send-keys` OK. 멀티라인은 `send-keys`의 줄바꿈이 Enter(=제출)로 변환되어 한 줄로 붙는다. `load-buffer` + `paste-buffer` 사용.
- **Python REPL**: `PYTHON_BASIC_REPL=1` 환경변수를 설정해야 한다. 기본 Python REPL은 readline/fancy prompt가 send-keys 흐름을 깨뜨린다.
- **tmux 미설치/미실행**: `tmux list-sessions`가 실패하면 tmux가 없거나 서버가 안 떠있는 것. 사용자에게 안내.
- **new-session에 inline command 금지**: shell init(PATH, direnv, nvm 등)을 우회한다. 반드시 세션 생성 후 `send-keys`로 실행.
