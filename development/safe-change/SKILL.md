---
name: safe-change
description: >
  Apply one logical code change with mandatory impact mapping, git snapshot,
  verification, and automatic revert on failure. Load when the user asks for
  a safe edit, verified change, one change at a time with rollback, or
  codespine-style edit loop. Also triggers on "safe change", "edit with
  verification", "don't break the build", "revert if tests fail", or any
  non-trivial code edit where blast radius matters. Always runs
  dependency-mapping first. Pairs with incremental-implementation for
  multi-slice work; this skill is one atomic verify cycle per invocation.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: jeromeetienne/codespine, alexsarrell/synapse-farsight, agentralabs/agentic-codebase
  resources:
    references:
      - examples.md
    scripts:
      - verify.sh
---
# Safe Change

You make **one logical edit per verify cycle**: map blast radius, snapshot git state, apply the change, run `scripts/verify.sh`, keep on pass or **auto-revert on fail**. Non-negotiable.

## Hard Rules

Invoke `dependency-mapping` and attach its impact report before editing — no exceptions for non-trivial edits.
One logical change per cycle — feature + refactor = separate cycles (`pr-authoring` for commit separation).
Take a git snapshot before editing (`git stash push -u -m "safe-change snapshot"` or commit on a branch).
On verify failure: `git restore .` and `git clean -fd` (or `git stash pop` reversal) — **always revert**, never leave a broken tree.
Never skip verify because "it's a small change."
Report `behaviorVerified: false` when no test command exists.

---

## Workflow

### Step 1 — Impact gate

Run `dependency-mapping` for the target symbol/file. If risk is `high` and tests are `NONE`, confirm with user before proceeding.

### Step 2 — Snapshot

```bash
git status   # must be clean or user-approved dirty scope
git stash push -u -m "safe-change: pre-edit $(date +%s)"
# OR: git checkout -b safe-change/<slug>
```

Record `snapshot_ref` (stash ref or branch name).

### Step 3 — Apply one logical change

Edit only what the impact report scoped. No drive-by refactors.

### Step 4 — Verify

```bash
# Use the package/fixture directory — not repo root for subpath edits
bash .agents/skills/safe-change/scripts/verify.sh examples/seed/calc
```

Parse JSON stdout: `pass`, `typecheck`, `tests`, `behaviorVerified`.

### Step 5 — Keep or revert

| Result | Action |
|--------|--------|
| `pass: true` | Keep change. Emit change-run report. Advise commit via `git-workflow-and-versioning`. |
| `pass: false` | `git restore . && git clean -fd` (or stash pop to restore). Report failure with verify evidence. **Do not retry blindly** — revise plan or invoke `dynamic-routing`. |

### Step 6 — Next cycle

For multi-step work, hand off to `incremental-implementation` or repeat Steps 1–5 per slice.

---

## Gotchas

- Stash on a dirty tree may include unrelated files — scope stash paths when possible.
- `verify.sh` skipping tests is not a pass for behavior — surface `behaviorVerified: false`.
- Monorepos: pass the **package/fixture path** to `verify.sh` (e.g. `examples/seed/calc`), not `.` at repo root unless tests live there.
- Auto-revert loses the failed attempt — capture error output before restoring.

---

## Output Format

```markdown
## Safe change run — [slug]

Snapshot: [stash@ref | branch]
Impact risk: [low|medium|high] (from dependency-mapping)

Verify:
- typecheck: [pass/fail] — [cmd]
- tests: [pass/fail/skip] — [cmd]
- behaviorVerified: [true/false]

Outcome: [KEPT | REVERTED]
Evidence: [stderr/stdout excerpt on failure]

Next: [commit message suggestion | revised approach]
```

---

## Examples

Teaser: Rename export → impact medium → verify fails typecheck → auto-revert → report lists 3 TS errors at importers.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too small to verify" | Small edits cause the biggest surprise breakages. |
| "I'll fix forward" | Revert first; forward-fix compounds errors. |
| "Tests are slow" | Slow tests beat slow debugging. |
| "Impact map is overkill" | It's 2 minutes vs 2 hours of bisect. |
| "Stash is annoying" | Broken main is worse. |

## Verification

- [ ] dependency-mapping report attached
- [ ] Git snapshot taken before edit
- [ ] verify.sh run after edit
- [ ] Failed verify triggered revert

## Red Flags

- Edit applied without impact report
- Verify skipped
- Failed verify left dirty tree
- Multiple logical changes in one cycle

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 2 family)

## Impact Report

```
Safe change: [slug] | Outcome: [KEPT|REVERTED] | behaviorVerified: [bool]
Verify: typecheck=[pass/fail] tests=[pass/fail/skip]
```
