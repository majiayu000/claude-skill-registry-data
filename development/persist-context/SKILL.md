---
name: persist-context
description: |
  SEMO 세션 간 컨텍스트 영속화 (공통 Skill). Use when (1) 아키텍처 결정 사항 저장,
  (2) 팀 선호도 기록, (3) 자주 참조하는 파일 캐싱, (4) 세션 간 맥락 유지.
tools: [Read, Write, Bash, Glob]
model: inherit
---

> **시스템 메시지**: `[SEMO] Skill: persist-context 호출 - {action}`

# persist-context Skill

> 세션 간 컨텍스트 영속화를 위한 장기 메모리 시스템 (SEMO Core 공통 Skill)

## Purpose

Claude Code의 "기억 상실(Amnesia)" 문제를 해결합니다:
- 세션 간 아키텍처 결정 사항 유지
- 팀 선호도 및 규칙 기록
- 자주 참조하는 파일/패턴 캐싱
- 프로젝트별 맥락 저장

## Memory Storage

```text
.claude/memory/
├── decisions.json      # 아키텍처 결정 사항
├── preferences.json    # 팀/사용자 선호도
├── cache/              # 자주 참조하는 패턴 캐시
└── context/            # 프로젝트별 맥락
```

## Actions

### 1. save - 메모리 저장

```markdown
skill:memory save decision "api-pattern" "모든 API 응답은 JSON Envelope 패턴 사용"
```

### 2. load - 메모리 로드

```markdown
skill:memory load decision
skill:memory load decision "api-pattern"
```

### 3. sync - 세션 시작 시 자동 로드

세션 시작 시 자동 호출:
1. decisions.json 로드 → 아키텍처 결정 복원
2. preferences.json 로드 → 선호도 복원
3. context/{project}.json 로드 → 프로젝트 맥락 복원

## Integration

### MCP 연동 (권장)

Memory MCP 서버가 설치된 경우 자동으로 MCP를 우선 사용합니다.

| 순위 | 저장소 | 조건 | 장점 |
|------|--------|------|------|
| 1 | Memory MCP | MCP 서버 활성화 시 | 강력한 영속화, 크로스 프로젝트 공유 |
| 2 | .claude/memory/ | MCP 없을 때 | 프로젝트별 독립 관리, 설정 불필요 |

## References

- [Memory Schema](references/memory-schema.md) - 메모리 스키마 상세
- [MCP Integration](references/mcp-integration.md) - MCP 서버 연동
