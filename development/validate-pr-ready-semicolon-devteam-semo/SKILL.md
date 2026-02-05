---
name: validate-pr-ready
description: Execute Phase 5 comprehensive verification before PR. Use when (1) implementation is complete, (2) before creating Pull Request, (3) user requests quality check, (4) pre-commit validation needed, (5) Constitution compliance verification required.
tools: [Bash, Read, Grep, GitHub CLI]
location: project
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: validate-pr-ready 호출 - {검증 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# validate-pr-ready Skill

@./../_shared/quality-gates.md
@./../_shared/ddd-patterns.md
@./../_shared/browser-testing.md

**Purpose**: Multi-layered quality verification before PR submission with integrated spec analysis

## Quick Start

### When to Use

- Implementation is complete
- Before creating Pull Request
- User requests quality check
- Pre-commit validation needed

### What It Does

Executes **6-layer verification** with integrated spec analysis:

| Layer | Name | Checks |
|-------|------|--------|
| 1 | Spec Compliance | spec.md ↔ plan.md ↔ tasks.md ↔ code alignment |
| 2 | Team Codex | Commits, ESLint, TypeScript, debug code, 'any' types |
| 3 | DDD Architecture | 4-layer structure, SSR rules, imports |
| 4 | Supabase Patterns | Server client, RPC naming, type assertions |
| 5 | Test Coverage | npm test, coverage thresholds (80%/80%/70%) |
| 5.5 | Browser Testing | Optional: UI/UX validation via MCP |
| 6 | Constitution | All 9 principles validation |

## Usage

```javascript
// Full verification (recommended before PR)
skill: verify();

// Quick check (skip tests)
skill: verify({ quick: true });

// Spec-only verification
skill: verify({ layers: ["spec"] });

// Code-only verification (skip spec)
skill: verify({ layers: ["code", "tests", "constitution"] });

// Full verification with browser testing
skill: verify({ browserTest: true });

// Browser testing with specific MCP
skill: verify({ browserTest: true, mcp: "playwright" });
```

## Severity Levels

| Level | Meaning | PR Impact |
|-------|---------|-----------|
| 🔴 Critical | Test failures, TS errors, Constitution violations | **Blocks PR** |
| 🟡 Warning | Debug code, 'any' types, low coverage | Should fix |
| 🟢 Suggestion | Performance, accessibility improvements | Nice to have |

## Related

- [Verification Layers Detail](references/verification-layers.md) - Layer-specific checks
- [Output Format](references/output-format.md) - Report format
- [Severity Guide](references/severity-guide.md) - Issue classification

## Related Skills

- `spec` - SDD Phase 1-3
- `implement` - ADD Phase 4
- `check-team-codex` - Team Codex validation
- `validate-architecture` - DDD architecture validation
