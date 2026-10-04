---
name: code-simplify
description: Simplify DegenExus code while preserving source-of-truth behavior and test evidence.
disable-model-invocation: true
argument-hint: "[target files or behavior]"
---

# Code Simplify Workflow

Canonical `/code-simplify` workflow. Use this skill instead of keeping simplification prose in `.claude/commands/code-simplify.md`.

## Sources of Truth

- Routing contract: `.claude/rules/synergy-contract.yml`
- Evidence schema: `.claude/rules/evidence-schema.yml`
- Review rubric: `.claude/skills/code-reviewer/SKILL.md`
- FSV doctrine: `.claude/skills/fsv-verify/SKILL.md`

## Workflow

1. Identify the target code and source-of-truth behavior.
2. Read callers, tests, edge cases, and relevant invariants before editing.
3. Prefer deletion, guard clauses, extracted helpers, descriptive names, and removal of dead code after proof.
4. Apply one simplification at a time.
5. After each meaningful change, run targeted tests and compare behavior against source-of-truth expectations.
6. Run `python -m compileall -q src/` for runtime changes.
7. If behavior changes unexpectedly, revert that simplification and investigate before continuing.

## Output

Emit `.claude/rules/evidence-schema.yml` fields with behavior-preservation proof, source-of-truth comparisons, commands run, edge cases, and memory-update status.
