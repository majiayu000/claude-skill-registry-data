---
name: statusline
description: >
  Claude Code 터미널 하단에 디렉토리, git branch, 모델명, context 사용량,
  rate limit, 변경 라인 수를 표시하는 2줄 statusline 스크립트를 설치한다.
  "statusline 설치", "statusline 설정", "스테이터스라인 설치",
  "상태바 설치", "install statusline", "setup statusline"
  등에서 트리거.
---

# Statusline 설치

2줄 statusline 스크립트를 설치한다.

- 라인1: 디렉토리명 + git branch + worktree + 모델명
- 라인2: context % + rate limit + lines changed

## 설치 절차

1. `${CLAUDE_PLUGIN_ROOT}/skills/statusline/statusline-command.sh`를 `~/.claude/statusline-command.sh`에 복사
2. `chmod +x ~/.claude/statusline-command.sh`
3. `~/.claude/settings.json`에 아래 설정 병합 (기존 설정 유지):

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline-command.sh"
  }
}
```

4. 설치 완료 메시지 출력: "statusline 설치 완료. 다음 응답부터 적용됩니다."

## 주의

- `settings.json`에 기존 `statusLine` 설정이 있으면 덮어쓰기 전에 사용자에게 확인
- `settings.json`의 다른 설정은 절대 변경하지 않음
- jq 의존성 필요 — 없으면 안내
