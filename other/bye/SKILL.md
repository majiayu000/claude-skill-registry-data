---
name: bye
description: 지금 대화 중인 Claude Code 세션 프로세스(와 그 MCP 서버 자식들)만 종료한다. VSCode 확장엔 /exit 가 없어 세션이 백그라운드에 쌓이며 메모리를 먹는 문제의 우회. 사용자가 "/bye", "이 세션 죽여", "세션 끝내" 라고 하면 사용. 다른 세션은 건드리지 않는다.
allowed-tools:
  - Bash
---

# /bye

Bash 로 아래 한 줄만 실행한다. 다른 도구·설명·확인 질문 없이 바로 실행한다.

```bash
bash ~/.claude/skills/bye/bye.sh
```

스크립트가 자기 조상 중 첫 번째 `claude` 프로세스와 그 하위 트리(MCP 서버 등)를 종료하므로 이 대화는 여기서 끝난다. 도구 결과가 돌아오지 않는 것이 정상이다.
