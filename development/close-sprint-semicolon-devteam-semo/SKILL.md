---
name: close-sprint
description: |
  Sprint(Iteration) 종료 및 회고 정리. Use when (1) Sprint 마감,
  (2) 회고 작성, (3) /SEMO:sprint close 커맨드.
tools: [Bash, Read, Write]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: close-sprint 호출` 메시지를 첫 줄에 출력하세요.

# close-sprint Skill

> Sprint(Iteration) 종료 처리 및 회고 생성

## Purpose

Sprint를 종료하고 회고를 정리하며, 미완료 Task를 다음 Iteration으로 이관합니다.

## Workflow

```
Sprint 종료 요청
    ↓
1. Iteration의 완료/미완료 Task 집계
2. Velocity 계산
3. 회고 요약 생성
4. Sprint Issue에 회고 추가
5. 미완료 Task → 다음 Iteration 이관
6. sprint-current 라벨 제거
```

## Quick Start

```yaml
iteration_title: "11월 4/4"
next_iteration: "12월 1/4"
retrospective:
  good: ["API 개발 순조로움"]
  improve: ["테스트 커버리지 부족"]
```

## Output

```markdown
✅ Sprint "11월 4/4" 종료 완료

**완료**: 8/10 Task (80%)
**Velocity**: 24pt
**미완료 이관**: 2 Task → 12월 1/4
```

## References

- [API Calls](references/api-calls.md)
- [Retrospective Template](references/retrospective.md)
