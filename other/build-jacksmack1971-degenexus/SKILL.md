---
name: build
description: Incrementally implement DegenExus changes with tests, FSV source-of-truth proof, and runtime verification.
disable-model-invocation: true
argument-hint: "[task or issue scope]"
---

# Build Workflow

Canonical `/build` workflow. Use this skill instead of keeping implementation prose in `.claude/commands/build.md`.

## Sources of Truth

- Routing contract: `.claude/rules/synergy-contract.yml`
- Evidence schema: `.claude/rules/evidence-schema.yml`
- Test ownership: `.claude/agents/test-engineer.md`
- FSV doctrine: `.claude/skills/fsv-verify/SKILL.md`

## Workflow

1. Read acceptance criteria and identify the source of truth before editing.
2. Load relevant code, tests, and project conventions.
3. Write a failing Prove-It or feature test when behavior changes.
4. Implement the minimum change to satisfy the test.
5. Reread the source of truth and compare the expected delta with the observed delta.
6. Run targeted tests, then broader tests when feasible.
7. Run `python -m compileall -q src/` for runtime changes.
8. Commit with a scoped conventional-style subject when the change is ready.

If verification fails repeatedly, halt and request read-only root-cause analysis from `fdd-investigator` before more edits.

## Output

Emit `.claude/rules/evidence-schema.yml` fields with failing-test evidence where applicable, passing-test evidence, FSV PRE/POST/DIFF, edge cases, and memory-update status.
