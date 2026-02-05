---
name: governance
description: Engineering standards and code governance enforcement. Triggers during code review discussions, PR descriptions, commit preparation, and when discussing code quality. Ensures compliance with standards.md and runs audit checks. Trigger phrases include "code review", "review this", "commit", "standards", "compliance", "code quality", "best practices", "before I merge".
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Governance Skill

Enforces engineering standards and code quality policies during development.

> **Standards Document**: [docs/architecture/standards.md](../../../docs/architecture/standards.md)
> **Governance Documentation**: [docs/governance/](../../../docs/governance/)
> **Audit Script**: `npm run audit:standards`

---

## Quick Start (First-Time Setup)

### 1. Run Setup Check

```bash
# Comprehensive governance setup verification
node .claude/skills/governance/scripts/governance-check.mjs
```

This checks CLAUDE.md, standards.md, audit script, ADRs, and pre-commit hooks with actionable fix instructions.

### 2. Understand the Two-Document Model

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| **CLAUDE.md** | AI operational context (commands, URLs, quick-ref) | Frequent |
| **standards.md** | Engineering policy (authoritative) | Infrequent |

**Rule**: CLAUDE.md defers to standards.md for authoritative definitions.

### 3. Common Operations

```bash
# Check standards compliance
npm run audit:standards

# Typecheck before commit
npm run typecheck && npm run lint && npm run test

# View pre-commit checklist
cat docs/architecture/standards.md | grep -A20 "Pre-Commit Checklist"
```

---

## When This Skill Activates

### During Code Review

When reviewing code or discussing PRs, automatically check:

1. **File length compliance** (max 500 lines per file)
2. **Naming conventions** match project standards
3. **Test coverage** exists for new code
4. **No forbidden patterns** (`any` types, hardcoded secrets)

### Before Commits

When helping prepare commits, remind about:

1. **Pre-commit checklist** (typecheck, lint, test)
2. **Standards audit** (`npm run audit:standards`)
3. **Commit message format** (conventional commits)

---

## Core Standards Quick Reference

> **Full reference**: [docs/architecture/standards.md](../../../docs/architecture/standards.md)

### Code Quality (§1)

| Standard | Requirement | Check |
|----------|-------------|-------|
| TypeScript | Strict mode enabled | `npm run typecheck` |
| No `any` types | Use `unknown` for external data | Audit script |
| Max file length | 500 lines | Audit script |
| JSDoc | Required for public APIs | Audit script |

### Naming Conventions (§1.2)

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `Button.tsx`, `UserCard.astro` |
| Utilities | camelCase | `userService.ts` |
| Variables | camelCase | `getUserById()` |
| Constants | SCREAMING_SNAKE | `const MAX_RETRIES = 3` |
| DB columns | snake_case | `user_id`, `created_at` |
| CSS classes | kebab-case | `nav-sidebar` |

### Testing (§2)

| Layer | Target | Framework (example) |
|-------|--------|---------------------|
| Unit tests | 90-100% | Vitest, Jest, pytest |
| API routes | 90-100% | Testing framework + supertest |
| E2E critical paths | 100% | Playwright, Cypress |

### Workflow (§3)

- **Branching**: `feature/`, `fix/`, `chore/`, `docs/` prefixes
- **Commits**: `<type>(scope): <description>`
- **Review**: All code requires approval before merge

---

## Compliance Check

Run the standards audit before committing:

```bash
npm run audit:standards
```

This checks:
- TypeScript strict mode
- No `any` types in source
- File length limits (500 lines)
- JSDoc on exported functions
- Test files exist
- Feature flags module exists
- CLAUDE.md exists
- ADR directory exists
- Pre-commit hooks configured

### Handling Failures

| Failure | Resolution |
|---------|------------|
| File too long | Split into modules (document decision in ADR if significant) |
| Missing JSDoc | Add documentation to exported functions |
| `any` type found | Replace with proper type or `unknown` |
| Missing tests | Add test coverage for new code |

---

## Anti-Patterns vs Correct Patterns

### Code Quality

| Anti-Pattern | Correct Pattern | Why |
|--------------|-----------------|-----|
| ❌ `any` type | ✅ `unknown` for external data | Type safety at runtime boundaries |
| ❌ 600+ line files | ✅ Split at 500 lines | Maintainability, easier review |
| ❌ `console.log` in production | ✅ Proper logging or remove | Security, performance |
| ❌ Hardcoded secrets | ✅ Environment variables | Security best practice |

### Documentation

| Anti-Pattern | Correct Pattern | Why |
|--------------|-----------------|-----|
| ❌ Duplicating policy in CLAUDE.md | ✅ Cross-reference standards.md | Single source of truth |
| ❌ No JSDoc on public functions | ✅ JSDoc with @param, @returns | API discoverability |
| ❌ Inline comments explaining "what" | ✅ Comments explaining "why" | Code should be self-documenting |

### Workflow

| Anti-Pattern | Correct Pattern | Why |
|--------------|-----------------|-----|
| ❌ Committing directly to main | ✅ Feature branches with PR | Code review, CI checks |
| ❌ `git push --force` to main | ✅ Never force-push protected branches | History integrity |
| ❌ Skipping audit:standards | ✅ Run before every commit | Catch issues early |
| ❌ Merge without review | ✅ Require approval | Quality gate |

### Testing

| Anti-Pattern | Correct Pattern | Why |
|--------------|-----------------|-----|
| ❌ Tests after code | ✅ TDD or tests alongside | Better design, coverage |
| ❌ Mocking internal modules | ✅ Mock only external services | Test real behavior |
| ❌ Ignoring flaky tests | ✅ Fix or quarantine immediately | CI reliability |

---

## Pre-Commit Checklist

Before every commit:

```
[ ] npm run typecheck     # TypeScript compiles
[ ] npm run lint          # Linter passes
[ ] npm run test          # Tests pass
[ ] npm run audit:standards  # Standards compliance
[ ] No console.log statements (use proper logging)
[ ] No hardcoded secrets
[ ] Meaningful commit message
```

---

## PR Review Checklist

When reviewing or preparing PRs:

| Category | Criteria |
|----------|----------|
| Correctness | Does it work? Edge cases handled? |
| Security | No secrets, injection vulnerabilities, or auth bypasses |
| Performance | No N+1 queries, unnecessary re-renders, or memory leaks |
| Style | Matches project conventions, readable, maintainable |
| Testing | Tests exist for new functionality |
| Scope | No unrelated changes, minimal footprint |

### PR Description Template

```markdown
## Summary
[What this PR does in 1-2 sentences]

## Ticket
[PROJECT-XXX](link)

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Tested in deploy preview
- [ ] Edge cases considered

## Screenshots (if UI changes)
[Before/After screenshots]
```

---

## Two-Document Model

This project uses a two-document governance model:

| Document | Purpose | Location |
|----------|---------|----------|
| **CLAUDE.md** | AI operational quick-reference | Project root |
| **standards.md** | Engineering policy (authoritative) | docs/architecture/ |

- CLAUDE.md is optimized for **token efficiency** — concise commands and context
- standards.md is optimized for **human comprehension** — rationale and justifications

**Rule**: CLAUDE.md defers to standards.md for authoritative definitions using section references (§1.3).

---

## Using This Skill in Other Projects

To replicate this governance model:

1. **Copy the skill**:
   ```bash
   cp -r .claude/skills/governance /path/to/new-project/.claude/skills/
   ```

2. **Copy governance docs**:
   ```bash
   cp -r docs/governance /path/to/new-project/docs/
   ```

3. **Create standards.md** using the template at [docs/governance/guardrails-template.md](../../../docs/governance/guardrails-template.md)

4. **Create audit script** using [scripts/audit-standards.mjs](../../../scripts/audit-standards.mjs) as a starting point

5. **Add npm script**:
   ```json
   "audit:standards": "node scripts/audit-standards.mjs"
   ```

6. **Update CLAUDE.md** to cross-reference standards.md

---

## Related Documents

- [Engineering Standards](../../../docs/architecture/standards.md) — Authoritative policy
- [Guardrails Instructions](../../../docs/governance/guardrails-instructions.md) — How the model works
- [Guardrails Template](../../../docs/governance/guardrails-template.md) — For new projects
- [ADR Index](../../../docs/adr/index.md) — Architecture decisions

---

*Last updated: December 2025*
*Project-level governance enforcement for Claude Code*
