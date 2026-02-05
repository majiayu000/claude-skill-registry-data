---
name: remote-bridge
description: |
  Remote 요청 브릿지 스킬. Use when (1) 원격 상태 확인,
  (2) 대기 중인 요청 조회, (3) 수동 권한 승인/거부.
tools: [Bash, Read, mcp]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: remote-bridge 호출` 시스템 메시지를 첫 줄에 출력하세요.

# remote-bridge Skill

> 원격 제어 요청과 로컬 Claude Code 세션 간의 브릿지

## Purpose

모바일 PWA와 Claude Code 세션 간의 통신을 관리합니다:
- 대기 중인 원격 요청 조회
- 수동 권한 승인/거부
- 원격 연결 상태 확인

## 트리거

- "원격 상태 확인"
- "pending 요청 확인"
- "원격 요청 목록"

## Workflow

### 1. 대기 중인 요청 조회

```bash
# MCP 도구로 DB 조회
mcp__semo-integrations__supabase_query(
  table: "remote_requests",
  filter: "status.eq.pending",
  select: "id,type,message,created_at"
)
```

### 2. 요청 상태 업데이트

```bash
# 승인
mcp__semo-integrations__remote_respond(
  request_id: "{id}",
  response: "approve",
  message: "승인됨"
)

# 거부
mcp__semo-integrations__remote_respond(
  request_id: "{id}",
  response: "deny",
  message: "거부됨"
)
```

## 출력 예시

```markdown
[SEMO] Skill: remote-bridge 호출

## 원격 요청 현황

| ID | 유형 | 메시지 | 생성 시간 |
|----|------|--------|----------|
| abc123 | permission | Bash 실행 권한 요청 | 2분 전 |
| def456 | user_question | 테스트 환경 선택 | 5분 전 |

**대기 중**: 2건
```

## Error Handling

### DB 연결 실패

```markdown
⚠️ Remote DB 연결 실패

SEMO_DB_PASSWORD 환경 변수를 확인하세요.
```

### 요청 없음

```markdown
✅ 대기 중인 원격 요청이 없습니다.
```

## SEMO Message Format

```markdown
[SEMO] Skill: remote-bridge 호출

[SEMO] Skill: remote-bridge 완료 - {N}건 조회됨
```

## References

- [semo-hooks](../../../semo-hooks/)
- [Orchestrator](../../agents/orchestrator/orchestrator.md)
