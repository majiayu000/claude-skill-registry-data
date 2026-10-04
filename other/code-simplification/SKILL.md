---
name: code-simplification
description: >
  Simplify application code for clarity without changing behavior — refactor after
  tests pass, reduce nesting and duplication, match project conventions. Load when
  refactoring for readability, cleaning up after a feature ships, or when code review
  flags complexity. Also triggers on "simplify this code", "code simplification",
  "make this easier to read", "reduce complexity", "refactor for clarity". Not for
  compress/split/prune-skill (skill-library files). Pairs with technical-debt-audit.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: addyosmani/agent-skills code-simplification + simplify-ignore hook (MIT)
  resources:
    references:
      - simplification-patterns.md
      - simplify-ignore.md
      - examples.md
---

# Code Simplification

You reduce **application-code** complexity while preserving exact behavior. Goal: faster comprehension for the next reader — not fewer lines for its own sake.

## Hard Rules

Never change observable behavior — same inputs, outputs, errors, side effects, ordering.
Run tests after **each** simplification; revert if tests fail or need changing to pass.
Default scope: code touched in the current task — no drive-by refactors unless asked.
Separate refactoring commits from feature/bugfix commits.
Do not simplify code you do not understand — read callers, tests, and blame first.
>500 lines touched → prefer codemods/AST tools over manual edits.
Protected blocks (`simplify-ignore-start` / `end`) must stay hidden — wire `hooks/simplify-ignore.sh` in Claude Code or read `references/simplify-ignore.md`.

---

## Workflow

### Step 0 — Optional: protect hot paths (Claude Code)

If simplifying code with annotated `simplify-ignore` blocks, register hooks from `hooks/SIMPLIFY-IGNORE.md` before reads/edits. Crash recovery: `echo '{}' | bash hooks/simplify-ignore.sh`.

### Step 1 — Understand (Chesterton's Fence)

Before changing anything, answer:

- What is this code's responsibility? Who calls it?
- What edge cases and error paths exist?
- Do tests define expected behavior?
- Why might it look this way? (performance, platform, history)

If you cannot answer, read more context — do not simplify yet.

### Step 2 — Identify opportunities

Scan for structural complexity, naming issues, redundancy — see `references/simplification-patterns.md` for the signal table.

### Step 3 — Apply incrementally

For each change: edit → run test suite → commit or continue.
One simplification per commit when possible.

### Step 4 — Verify the whole

- Is the result genuinely easier to understand?
- Consistent with project conventions (AGENTS.md, neighboring files)?
- Diff reviewable with no unrelated changes?
- If "simplified" code is harder to read, revert.

---

## When NOT to use

- Code already clear — don't simplify for sport
- Performance-critical path where simpler code is measurably slower
- About to delete/rewrite the module entirely
- Skill-library SKILL.md files — use `compress-skill` / `split-skill` instead

---

## Gotchas

- Simplification that requires test changes usually changed behavior.
- Inlining a well-named helper hurts readability.
- Fewer lines ≠ simpler (nested ternaries prove this).
- Mixed refactor + feature PRs are hard to review and revert.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It works, don't touch it" | Hard-to-read working code is expensive on every future fix. |
| "Fewer lines is always simpler" | Comprehension speed matters, not line count. |
| "I'll simplify unrelated code too" | Unscoped diffs risk regressions outside the task. |
| "Types make it self-documenting" | Types show structure; names show intent. |
| "Refactor while adding the feature" | Split PRs — mixed changes hide bugs. |

---

## Output Format

```markdown
## Code simplification — [scope]

Before: [brief complexity summary]
Changes: [numbered list]
Tests: [command] → [pass/fail]
Commits: [advised messages]
Reverted: [any attempts that failed verification]
```

---

## Examples

<examples>
  <example>
    <input>This handler has four levels of nesting after the feature landed; tests pass.</input>
    <output>
Read tests + callers. Extract guard clauses (one commit, tests green). Rename `data` → `orderPayload` (second commit). Stop — out of scope for unrelated modules.
    </output>
  </example>
</examples>

---

## Verification

- [ ] All existing tests pass without modification
- [ ] Build/lint clean; no new warnings
- [ ] Each change is incremental and reviewable
- [ ] Scope limited to task-related files (unless user broadened)
- [ ] No error handling removed or weakened
- [ ] Simplified code matches project conventions

---

## Red Flags

- Simplification required test changes that alter behavior
- Well-named helper inlined for fewer lines only
- Nested ternaries introduced to reduce line count
- Refactor bundled unrelated behavior changes
## Reference Files

- **`references/simplification-patterns.md`**: Pattern signal table — read at Step 2.
- **`references/simplify-ignore.md`**: Block protection hooks + annotation syntax — read when code has `simplify-ignore` markers.
- **`hooks/SIMPLIFY-IGNORE.md`**: Full setup, examples, limitations (repo root).

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Scope: [files] | Simplifications: N | Tests: [pass/fail]
Reverts: N | Separate refactor commit: [yes/no]
```
