---
name: cmux-help
description: >
  cmux CLI 사용 가이드이자 전용 cmux 스킬로 가는 진입점.
  안정적인 모델·함정만 정적으로 담고
  커맨드 카탈로그·옵션은 라이브 출력에 위임한다.
  "cmux 사용법", "cmux 명령어", "cmux help", "cmux 옵션",
  "cmux 세션", "cmux split", "cmux 브라우저 열기",
  "cmux send", "cmux read-screen", "cmux workspace",
  "cmux ssh", "cmux 마크다운", "cmux notify", "cmux 설정",
  "cmux shortcut", "cmux 단축키", "cmux dock", "cmux sidebar",
  "cmux agent hooks", "cmux pane", "cmux surface", "cmux 탭"
  등에서 트리거.
---

# cmux CLI

cmux 앱을 Unix socket으로 제어하는 CLI. tmux와 유사하지만 macOS 네이티브 앱 기반이며 브라우저·마크다운 뷰어를 내장한다.

이 스킬은 **자주 안 바뀌는 모델과 함정만 정적으로** 담는다. 커맨드 목록·옵션 시그니처는 라이브 출력으로 위임한다 — drift 방지.

## 라이브 조회 (먼저 실행)

커맨드 syntax나 옵션이 필요하면 추측하지 말고 다음을 먼저 호출한다.

```bash
cmux --help                  # 전체 커맨드 목록
cmux <subcommand> --help     # 가능한 경우
cmux docs                    # 토픽 인덱스 (사용 가능한 topic 목록 확인)
cmux docs <topic>            # 해당 topic의 web URL과 curl 가능한 raw skill 경로 출력
cmux capabilities            # 런타임 기능 플래그
cmux ping                    # 소켓 도달 확인
cmux identify --json         # 현재 위치 (workspace/surface)
cmux tree --all              # 전체 토폴로지
```

`cmux docs <topic>`은 항상 최신 업스트림 raw URL을 안내한다 (`raw.githubusercontent.com/manaflow-ai/cmux/main/skills/...`). 정적 문서가 stale하면 그쪽을 fetch.

## 전용 스킬로 라우팅 (fallback 체인)

cmux는 영역별 공식 스킬(`cmux-browser`, `cmux-settings`, `cmux-customization`, `cmux-keyboard-shortcuts`, `cmux-workspace`, `cmux-diagnostics`, `cmux-markdown`)을 제공한다. 이 `cmux-help`는 그 진입점이며, 깊은 작업은 이름이 대응되는 전용 스킬로 위임한다 (browser → `cmux-browser`, settings → `cmux-settings` …).

전용 스킬이 미설치라도 끊기지 않도록 다음 fallback 체인을 따른다.

1. 전용 스킬이 설치돼 있으면 invoke.
2. 없으면 `cmux docs`로 토픽 인덱스를 조회한 뒤, 해당 `cmux docs <topic>`이 안내하는 raw `SKILL.md` URL을 fetch — 전용 스킬과 동일 내용에 도달한다.
3. 그래도 막히면 `cmux <command> --help`.

②·③은 cmux 런타임이 항상 제공하므로 스킬 미설치와 무관하게 동작한다. 토픽으로 덮이지 않는 영역(diagnostics, markdown 등)은 ②를 건너뛰고 ③으로 간다.

사용자가 설치를 요청하면 전체 설치는 `npx skills add manaflow-ai/cmux -g -y`, 개별 설치는 `--skill <name>`을 붙여 수행한다.

## 핵심 개념 (안정)

### 4계층

```
Window (macOS 윈도우)
  └─ Workspace  (사이드바 항목 — tmux의 session)
       └─ Pane  (분할 영역 — tmux의 pane)
            └─ Surface  (pane 안의 탭 — terminal / browser / markdown)
```

tmux와 가장 다른 점: **Surface**. 한 pane 안에 여러 surface가 탭으로 공존하며 terminal·browser·markdown이 혼재 가능.

### Handle 형식

| 형식 | 예시 | 비고 |
|------|------|------|
| short ref | `workspace:2`, `surface:7` | 출력 기본 |
| UUID | `550e8400-...` | 고유, 장황 |
| index | `2` | 숫자만 |

- `--id-format uuids|both`로 출력 형식 변경
- `tab-action`은 `tab:<n>` 형식도 수용

### 환경변수

cmux 터미널 안에서 자동 설정. 대부분 커맨드의 기본값. **cmux 밖**에서 호출하면 명시 필요.

| 변수 | 기본 대상 |
|------|-----------|
| `CMUX_WORKSPACE_ID` | `--workspace` |
| `CMUX_SURFACE_ID` | `--surface` |
| `CMUX_TAB_ID` | `--tab` |
| `CMUX_SOCKET_PATH` | 소켓 경로 오버라이드 |

### 글로벌 옵션

- `--json` — 자동화 시 필수, ref 파싱 안정
- `--id-format <refs|uuids|both>`
- `--socket <path>`, `--password <value>`

소켓 인증 우선순위: `--password` > `CMUX_SOCKET_PASSWORD` > Settings 저장값.

## 자주 틀리는 함정 (안정)

- **send + send-key 분리**: `cmux send 'cmd'`만으로는 실행 안 됨. 반드시 `cmux send-key Enter` 별도 호출. 가장 흔한 실수.
- **read-screen 타이밍**: send 직후엔 이전 화면을 반환할 수 있다. `sleep` 또는 완료 패턴(`✓`, `PASS`, prompt 복귀) polling.
- **snapshot ref 수명**: `browser snapshot --interactive`의 `e1`/`e2`/...는 DOM 변경(navigation, Ajax) 시 stale. 액션 뒤 반드시 re-snapshot.
- **WKWebView 제약**: cmux 브라우저는 viewport emulation·network interception·trace recording 미지원. CDP 기반 도구(Playwright 등)와 다름.
- **소켓 미연결**: cmux 앱이 꺼져 있으면 모든 커맨드 실패. `cmux ping`으로 사전 확인.
- **cmux 바깥에서 실행**: 일반 터미널에서는 `CMUX_*` env가 비어 있으니 `--workspace`/`--surface` 명시 필요.
- **new-workspace --command**: shell init(PATH, direnv 등) 전에 실행될 수 있음. 복잡한 초기화는 `send` + `send-key`로 분리.
- **browser open vs goto**: surface 지정 없는 `open`은 새 browser split/surface 생성. 기존 surface 이동은 `goto|navigate`를 선호한다. 현재 CLI는 surface를 지정한 `open`을 navigate처럼 처리할 수 있으므로 실제 동작은 `cmux browser --help`로 확인한다.

## 핵심 워크플로우 (안정)

### 명령 실행 + 결과 읽기

```bash
cmux send --surface surface:3 'pnpm test'
cmux send-key --surface surface:3 Enter
sleep 2
cmux read-screen --surface surface:3 --lines 50
```

긴 결과는 `--scrollback`/`--lines`로 범위 조절.

### 병렬 workspace 세팅

```bash
cmux new-workspace --name "server" --cwd ~/project --command "pnpm dev"
cmux new-workspace --name "test"   --cwd ~/project --command "pnpm test --watch"
cmux new-workspace --name "agent"  --cwd ~/project
```

### 브라우저 자동화 루프

```bash
cmux --json browser open https://example.com
# 반환된 surface ref 기억 (예: surface:7)
cmux browser surface:7 wait --load-state complete --timeout-ms 15000
cmux browser surface:7 snapshot --interactive
cmux browser surface:7 fill e1 "query"
cmux --json browser surface:7 click e2 --snapshot-after
# DOM 변경 후 반드시 re-snapshot
cmux browser surface:7 snapshot --interactive
```

세부 옵션(cookies, storage, dialog, download, frame 등)은 `cmux browser --help` 또는 `cmux docs browser`.

### plan 실시간 표시

```bash
cmux markdown /tmp/plan.md
# 이후 파일 수정 시 뷰어 자동 갱신
```

## tmux와의 차이 (안정)

- session → **workspace**
- `send-keys 'cmd' Enter` → `send 'cmd'` + `send-key Enter` (Enter 분리)
- `split-window -h/-v` → `new-split <left|right|up|down>` (방향 이름)
- pane 안에 **surface 탭** 개념 추가 (terminal/browser/markdown 혼재)
- cmux 고유: 디렉토리 인자(`cmux <path>`), 내장 브라우저, 마크다운 뷰어

tmux 호환 커맨드(capture-pane, resize-pane, pipe-pane, wait-for, swap-pane, break-pane, join-pane, find-window, next/previous/last-window, set-buffer/paste-buffer, set-hook 등)도 다수 제공. 정확한 옵션은 `cmux <command> --help` 또는 `cmux docs api`.
