---
name: maintaining-agents-md
description: Maintains AGENTS.md, AGENT_LEARNINGS.md, AGENT_REQUESTS.md, and CONTRIBUTING.md governance files in sync with codebase changes. Use when updating governance files, during sprint reviews, or after structural changes.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [audit|sync|promote|full]
  allowed-tools: Read, Grep, Glob, Edit
  stability: stable
  content-hash: sha256:7aed6247ed8472ddf5d9d0387f039e54b3bd51c5a57f924464f625808fe75661
---

# Maintain Agent Governance Files

**Scope**: $ARGUMENTS

Keeps agent governance files synchronized with codebase state. Detects stale
references, missing updates, and promotion candidates.

## Governance Files

| File | Authority | Purpose |
|------|-----------|---------|
| `AGENTS.md` | Behavioral | Rules, role boundaries, compliance requirements |
| `CONTRIBUTING.md` | Technical | Workflows, commands, coding standards |
| `AGENT_LEARNINGS.md` | Knowledge | Accumulated patterns and solutions |
| `AGENT_REQUESTS.md` | Escalation | Active blockers requiring human input |

## When to Use

- After PRs that change project structure, commands, or patterns
- At sprint start/end for governance health check
- When promoting patterns from `AGENT_LEARNINGS.md` to `.claude/rules/`
- After `make validate` pipeline or Makefile changes
- When adding/removing skills or plugins

## Modes

### `audit` (default)

Scan governance files for staleness and inconsistencies.

**Checks:**

1. **Stale paths**: Grep governance files for `src/`, `docs/`, `tests/` paths.
   Verify each path still exists.
2. **Stale commands**: Parse `CONTRIBUTING.md` command reference table. Verify
   each `make` recipe exists in `Makefile`.
3. **Missing learnings**: Check recent git log for patterns not yet in
   `AGENT_LEARNINGS.md`. If `ralph/docs/LEARNINGS.md` exists, check it too.
4. **Resolved requests**: Check `AGENT_REQUESTS.md` entries — flag any whose
   referenced files/issues no longer exist.
5. **Role boundary drift**: Verify AGENTS.md role definitions match current
   `.claude/skills/` inventory.

**Output**: Findings table with file, line, issue type, description.

### `sync`

Fix staleness found by audit. For each finding:

1. Propose the specific edit
2. Apply on user approval
3. Follow priority order: AGENTS.md > CONTRIBUTING.md > AGENT_LEARNINGS.md > AGENT_REQUESTS.md

### `promote`

Evaluate `AGENT_LEARNINGS.md` entries for promotion per the criteria in
`.claude/rules/compound-learning.md` (3rd occurrence → rule, recurring → skill).

**Procedure:**

1. Read `AGENT_LEARNINGS.md` entries
2. Grep codebase for each pattern's problem statement
3. If pattern appears in 3+ locations or has been referenced in 3+ commits,
   recommend promotion to `.claude/rules/`
4. Draft the rule file content for user approval

### `full`

Run all three modes in sequence: audit → sync → promote.

## Maintenance Priority Order

When multiple files need updates, follow this order to prevent hierarchy
conflicts:

1. **AGENTS.md** — behavioral rules first (highest impact)
2. **CONTRIBUTING.md** — technical standards second
3. **AGENT_LEARNINGS.md** — patterns third (high-value, low-risk)
4. **AGENT_REQUESTS.md** — escalations last (time-sensitive, not structural)

## References

- `.claude/rules/compound-learning.md` — promotion path
- CONTRIBUTING.md "Documentation Hierarchy" — authority structure
- AGENTS.md "Decision Framework" — anti-redundancy rules
