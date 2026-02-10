---
name: ln-510-quality-coordinator
description: "Coordinates code quality checks: ln-511 code quality, ln-512 agent review, ln-513 regression. Single-pass, returns results to ln-500."
---

# Quality Coordinator

Single-pass coordinator for code quality checks. Invokes workers and returns aggregated results to ln-500.

## Purpose & Scope
- Invoke ln-511-code-quality-checker (which invokes ln-512 agent-reviewer internally)
- Run Criteria Validation (Story dependencies, AC-Task Coverage, DB Creation Principle)
- Run linters from tech_stack.md
- Invoke ln-513-regression-checker
- Return aggregated quality results to ln-500-story-quality-gate
- **No verdict determination** — ln-500 decides final Gate verdict

## When to Use
- **Invoked by ln-500-story-quality-gate** Phase 2
- All implementation tasks in Story status = Done

## Workflow

### Phase 1: Discovery

1) Auto-discover team/config from `docs/tasks/kanban_board.md`
2) Load Story + task metadata from Linear (no full descriptions)

**Input:** Story ID from ln-500-story-quality-gate

### Phase 2: Code Quality (delegate to ln-511)

1) **Invoke ln-511-code-quality-checker** via Skill tool
   - ln-511 runs code metrics, MCP Ref validation (OPT/BP/PERF), static analysis
   - ln-511 internally invokes ln-512-agent-reviewer for external agent reviews
2) **If ln-511 returns ISSUES_FOUND** -> aggregate issues, continue (ln-500 decides action)

**Invocation:**
```
Skill(skill: "ln-511-code-quality-checker", args: "{storyId}")
```

### Phase 3: Criteria Validation

**MANDATORY READ:** Load `references/criteria_validation.md`

| Check | Description | Fail Action |
|-------|-------------|-------------|
| #1 Story Dependencies | No forward deps within Epic | [DEP-] issue |
| #2 AC-Task Coverage | STRONG/WEAK/MISSING scoring | [COV-]/[BUG-] issue |
| #3 DB Creation Principle | Schema scope matches Story | [DB-] issue |

### Phase 4: Linters

1) Read `docs/project/tech_stack.md` for linter commands
2) Run all configured linters (eslint, ruff, mypy, etc.)
3) **If linters fail** -> aggregate issues, continue

### Phase 5: Regression Tests (delegate to ln-513)

1) **Invoke ln-513-regression-checker** via Skill tool
   - Runs full test suite, reports PASS/FAIL
2) **If regression FAIL** -> aggregate issues, continue

**Invocation:**
```
Skill(skill: "ln-513-regression-checker", args: "{storyId}")
```

### Phase 6: Return Results

Return aggregated results to ln-500:

```yaml
quality_check: PASS | CONCERNS | ISSUES_FOUND
code_quality_score: {0-100}
criteria_validation: PASS | FAIL
linters: PASS | FAIL
regression: PASS | FAIL
issues:
  - {id: "SEC-001", severity: high, finding: "...", source: "ln-511"}
  - {id: "DEP-001", severity: medium, finding: "...", source: "criteria"}
  - {id: "LINT-001", severity: low, finding: "...", source: "linters"}
```

**TodoWrite format (mandatory):**
```
- Invoke ln-511-code-quality-checker (in_progress)
- Criteria Validation (Story deps, AC coverage, DB schema) (pending)
- Run linters from tech_stack.md (pending)
- Invoke ln-513-regression-checker (pending)
- Return results to ln-500 (pending)
```

## Worker Invocation (MANDATORY)

| Step | Worker | Context |
|------|--------|---------|
| Code Quality | ln-511-code-quality-checker | Shared (Skill tool) — delegates agent review to ln-512 |
| Regression | ln-513-regression-checker | Shared (Skill tool) |

**All workers:** Invoke via Skill tool — workers see coordinator context. ln-512 is invoked by ln-511 internally.

**Anti-Patterns:**
- Running mypy, ruff, pytest directly instead of invoking ln-511/ln-513
- Marking steps as completed without invoking the actual skill
- Determining final verdict (that's ln-500's responsibility)

## Critical Rules
- Return all results to ln-500; do NOT determine verdict
- Single source of truth: rely on Linear metadata for tasks
- Language preservation in comments (EN/RU)
- Do not create tasks or change statuses; ln-500 decides next actions

## Definition of Done
- ln-511 invoked, code quality score returned
- Criteria Validation completed (3 checks)
- Linters executed
- ln-513 invoked, regression results returned
- Aggregated results returned to ln-500

## Reference Files
- Criteria Validation: `references/criteria_validation.md`
- Gate levels: `references/gate_levels.md`
- Workers: `../ln-511-code-quality-checker/SKILL.md`, `../ln-512-agent-reviewer/SKILL.md`, `../ln-513-regression-checker/SKILL.md`
- Caller: `../ln-500-story-quality-gate/SKILL.md`
- Test planning (separate coordinator): `../ln-520-test-planner/SKILL.md`
- Tech stack/linters: `docs/project/tech_stack.md`

---
**Version:** 7.0.0 (BREAKING: Simplified to single-pass quality coordinator. Pass 2 test verification moved to ln-500.)
**Last Updated:** 2026-02-09
