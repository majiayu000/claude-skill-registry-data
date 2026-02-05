---
name: audit-semo
description: 전체 SEMO 패키지 통합 품질 감사. Use when (1) 전체 패키지 품질 점검, (2) Agent/Skill/Command 표준 준수 검토, (3) 비효율적 구조 탐지, (4) 정기 감사 수행.
tools: [Bash, Read, Grep, Glob]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: audit-semo 호출 - {감사 범위}` 시스템 메시지를 첫 줄에 출력하세요.

# audit-semo Skill

> 전체 SEMO 패키지 Agent/Skill/Command 통합 품질 감사

## Purpose

모든 SEMO 패키지를 일괄 검토하여 표준 위반, 비효율적 구조, 품질 문제를 탐지합니다.

| 감사 대상 | 검토 내용 |
|----------|----------|
| **Agent** | Frontmatter, PROACTIVELY 패턴, model 필드, 라인 수 |
| **Skill** | Frontmatter, 시스템 메시지, Progressive Disclosure |
| **Command** | 파일 존재, CLAUDE.md 연동 |

## Quick Start

```bash
# 1. 전체 패키지 스캔
for pkg in semo-meta semo-next semo-backend semo-po semo-qa semo-core semo-pm; do
  echo "=== $pkg ==="
  ls -la $pkg/agents/ 2>/dev/null
  ls -la $pkg/skills/ 2>/dev/null
done

# 2. Agent 감사 (Frontmatter 4필드)
grep -rL "model:" semo-*/agents/*/*.md

# 3. Skill 감사 (100 lines 초과)
wc -l semo-*/skills/*/SKILL.md | awk '$1 > 100'

# 4. PROACTIVELY 패턴 누락
grep -rL "PROACTIVELY\|Use when" semo-*/agents/*/*.md
```

## 감사 체크리스트

### Agent 검증

| 항목 | 기준 | 심각도 |
|------|------|--------|
| **Frontmatter 4필드** | name, description, tools, model | 🔴 Critical |
| **PROACTIVELY 패턴** | description에 "PROACTIVELY use when" | 🔴 Critical |
| **model 필드** | opus/sonnet/haiku/inherit 중 하나 | 🔴 Critical |
| **라인 수** | 200 lines 이하 | 🟡 Important |
| **references/** | 200+ lines 시 분리 | 🟢 Nice-to-have |

### Skill 검증

| 항목 | 기준 | 심각도 |
|------|------|--------|
| **Frontmatter 3필드** | name, description, tools | 🔴 Critical |
| **시스템 메시지** | Frontmatter 직후 blockquote | 🔴 Critical |
| **"Use when" 패턴** | description에 포함 | 🟡 Important |
| **라인 수** | 100 lines 이하 | 🟡 Important |
| **references/** | 100+ lines 시 분리 | 🟢 Nice-to-have |

### Command 검증

| 항목 | 기준 | 심각도 |
|------|------|--------|
| **파일 존재** | commands/{name}.md 존재 | 🔴 Critical |
| **Frontmatter** | name, description 필수 | 🔴 Critical |
| **CLAUDE.md 연동** | commands 테이블에 등록 | 🟡 Important |

## Output Format

```markdown
[SEMO] Skill: audit-semo 완료

## 📊 SEMO 통합 감사 결과

**감사 일시**: {날짜}
**감사 범위**: 전체 SEMO 패키지 (7개)

### 📈 요약

| 패키지 | Agent | Skill | Command | 문제 |
|--------|-------|-------|---------|------|
| semo-meta | 5 ✅ | 6 ✅ | 2 ✅ | 0 |
| semo-next | 3 ⚠️ | 8 ✅ | 1 ✅ | 2 |
| ... | ... | ... | ... | ... |

**총 문제**: 🔴 Critical {n}건, 🟡 Important {n}건, 🟢 Nice-to-have {n}건

### 🔴 Critical 문제 (즉시 수정 필요)

#### semo-next/agents/example-agent
- **문제**: model 필드 누락
- **위치**: `semo-next/agents/example-agent/example-agent.md:1-10`
- **수정**: Frontmatter에 `model: sonnet` 추가

### 🟡 Important 문제 (권장 수정)

#### semo-po/skills/some-skill
- **문제**: SKILL.md 150 lines (100 lines 초과)
- **권장**: references/ 분리

### 📋 권장 조치

1. Critical 문제 우선 수정
2. agent-manager/skill-manager로 수정 작업 위임
3. package-validator로 수정 후 재검증
```

## SEMO Message

```markdown
[SEMO] Skill: audit-semo 호출 - {범위}

[SEMO] Audit: Agent 검사 중... ({n}개)
[SEMO] Audit: Skill 검사 중... ({n}개)
[SEMO] Audit: Command 검사 중... ({n}개)

[SEMO] Skill: audit-semo 완료 (🔴 {n}건, 🟡 {n}건, 🟢 {n}건)
```

## Related

- [agent-manager Agent](../../agents/agent-manager/agent-manager.md) - Agent 수정 위임
- [skill-manager Agent](../../agents/skill-manager/skill-manager.md) - Skill 수정 위임
- [package-validator Skill](../package-validator/SKILL.md) - 단일 패키지 구조 검증

## References

- [Audit Checklist](references/audit-checklist.md) - 상세 검증 기준
- [Scan Commands](references/scan-commands.md) - 패키지별 스캔 명령어
- [Fix Guide](references/fix-guide.md) - 문제 유형별 수정 가이드
