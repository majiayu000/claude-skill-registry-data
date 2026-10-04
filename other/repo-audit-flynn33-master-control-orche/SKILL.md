---
name: repo-audit
description: Audit MCOS repository state before implementing a phase. Use before edits in every phase.
disable-model-invocation: true
---

# Repo Audit Skill

Use this before editing.

1. Read the active phase file.
2. Read `handoff/realignment/manifest.json`.
3. Inspect all phase `readFirst` paths.
4. Identify old contracts that conflict with the phase objective.
5. Produce a file-by-file edit plan.
6. Identify tests and validation commands before editing.
7. Do not edit until the plan is explicit.

Output:

```markdown
## Phase audit summary
- Phase:
- Existing contracts found:
- Conflicts:
- Files to edit:
- Tests to update/add:
- Validation commands:
- Risks:
```
