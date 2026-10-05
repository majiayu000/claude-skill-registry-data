---
name: session-log
description: >
  Claude Code Stop 이벤트마다 마지막 user/assistant 교환을 세션당 1개 markdown
  파일에 기계적으로 append하는 훅을 설치하거나 제거하는 스킬. LLM 호출 없이
  jq 추출만 하므로 토큰 비용이 없고, transcript 만료 후에도 읽을 수 있는
  세션 원료 로그를 남긴다. "세션 로그 훅 설치", "stop 로그 설치",
  "세션 자동 기록", "대화 자동 기록해줘", "세션 로그 제거", "session log 설치",
  "install session log hook", "uninstall session log" 등에서 트리거.
---

# session-log

Claude Code의 `Stop` 훅으로 세션 대화를 자동 기록한다. 매 응답 종료 시점에 transcript에서 마지막 user prompt와 assistant 최종 텍스트를 뽑아 세션당 1개 `.md` 파일에 append한다.

`session-history`(정제된 의사결정 요약, 수동 트리거)와 보완 관계다. 이 스킬의 로그는 자동·무비용·crash-safe한 원료이고, 나중에 요약이 필요하면 이 파일을 소재로 삼는다.

## 스크립트 구성

| 파일 | 역할 |
|------|------|
| `scripts/stop-session-log.sh` | Stop 훅 본체. stdin JSON에서 transcript 경로를 받아 jq로 추출·append |

## 기록 위치와 포맷

- 기본 경로: `~/.agents/session-logs/{project}/{YYYY-MM-DD}-{session_id 앞 8자}.md`
- 루트는 에이전트 중립이다. Codex 등 다른 에이전트용 세션 로그 훅을 만들 때도 같은 루트에 쓰고, 파일 헤더의 `agent:` 필드로 출처를 구분한다
- `{project}`는 훅 입력 `cwd`의 실제 디렉토리 이름 (`pwd -P` 기준)
- 환경변수 `AGENT_SESSION_LOG_DIR`로 루트 재정의 가능
- 파일 헤더에 agent, 전체 session_id, cwd를 기록하고, 엔트리는 `## HH:MM` + user prompt(blockquote) + assistant 텍스트 + `<!-- stop:UUID -->` 마커 순서

## 추출 규칙

- user: sidechain(subagent), meta, compaction 요약, tool_result 전용 라인을 제외한 마지막 실제 prompt. 4000자 초과분은 절단
- assistant: text 블록을 가진 마지막 assistant 라인의 text 블록 전체. 절단 없음
- 같은 assistant UUID가 이미 파일에 있으면 skip (Stop 재발화 대비)

## 설치 절차

Claude Code 대상으로 "세션 로그 훅 설치해줘"라고 요청하면:

1. `npx skills add ./ -g --skill session-log` 또는 사용자가 지정한 설치 명령으로 스킬을 설치한다.
2. 설치된 `stop-session-log.sh`의 절대 경로를 확인한다.
3. `~/.claude/settings.json`의 `hooks.Stop`에 등록한다. 이미 같은 파일명이 command에 포함된 항목이 있으면 skip한다.

```jsonc
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/stop-session-log.sh",
            "statusMessage": "Appending session log..."
          }
        ]
      }
    ]
  }
}
```

ref: https://code.claude.com/docs/en/hooks

## 제거 절차

`hooks.Stop`에서 `stop-session-log.sh`가 포함된 항목만 제거한다. 해당 entry의 hooks 배열이 비면 entry 자체를 제거한다. 이미 쌓인 로그 파일은 사용자 소유이므로 건드리지 않는다.

## Gotchas

- settings.json은 세션 시작 시 로드된다. 설치/제거 후 새 세션부터 적용.
- `jq`가 없거나 stdin이 JSON이 아니면 조용히 exit 0 한다. 로깅 실패가 세션을 방해하는 것이 기록 누락보다 나쁘다.
- Stop은 세션 종료가 아니라 **매 응답 종료마다** 발동한다. 이 스킬은 그 특성을 이용해 crash-safe 증분 기록을 만든다. 세션 종료 1회 기록이 필요하면 `SessionEnd`가 맞지만 터미널 강제 종료 시 발동이 보장되지 않는다.
- `claude --resume`은 새 session_id를 만들 수 있다. 그 경우 새 파일로 이어지며, 파일 헤더의 cwd·날짜로 연결을 추적한다.
- 자정을 넘긴 세션은 파일명 날짜(생성일)와 엔트리 시각이 어긋날 수 있다. 파일 탐색은 session_id 기준이므로 파일이 쪼개지지는 않는다.
- 마지막 user prompt가 슬래시 커맨드면 `<command-name>` XML 원문이 그대로 기록된다. 원료 로그이므로 교정하지 않는다.
