---
name: check-team-codex
description: Validate code against Team Codex standards. Use when (1) before creating commits, (2) during verification phase, (3) quality gate enforcement.
tools: [Bash, Read, Grep]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: check-team-codex 호출 - {검증 대상}` 시스템 메시지를 첫 줄에 출력하세요.

# Check Team Codex Skill

@./../_shared/quality-gates.md
@./../_shared/nextjs-commands.md

> 코드를 Semicolon 팀 표준에 맞게 자동 검증

## 규칙 참조 (SoT)

> **모든 Team Codex 규칙은 semo-core/TEAM_RULES.md에서 관리됩니다.**

```bash
# 로컬 참조
.claude/semo-core/TEAM_RULES.md

# 원격 참조
gh api repos/semicolon-devteam/semo-core/contents/TEAM_RULES.md --jq '.content' | base64 -d
```

**참조 섹션**:
- `2. Code Quality (Team Codex)` - 검증 항목, 금지 사항, Severity Levels
- `6. Quality Gates` - Pre-commit, Pre-PR 검증

## Quick Start

```bash
# Pre-commit 필수 체크
npm run lint && npx tsc --noEmit

# Debug 코드 확인
grep -r "console\.log\|debugger" src/ --exclude-dir=node_modules

# any 타입 확인
grep -r ":\s*any\|as any" src/
```

## When to Use

- Before creating commits
- During verification phase
- After implementation completion
- Quality gates in v0.4.x CODE phase

## Severity Levels

| Level | 항목 | 조치 |
|-------|------|------|
| 🔴 CRITICAL | ESLint/TS 에러, hook 우회, 아키텍처 위반 | PR 차단 |
| 🟡 WARNING | Debug 코드, any 타입, TODO 주석 | 수정 권장 |
| 🟢 INFO | 스타일 제안, 성능 힌트 | 선택적 |

## Related Skills

- `verify` - 종합 검증에서 사용
- `implement` - v0.4.x CODE phase에서 사용
- `git-workflow` - 커밋 전 품질 검사

## References

- [Check Items](references/check-items.md) - Detailed check items
- [Output Format](references/output-format.md) - Report format
