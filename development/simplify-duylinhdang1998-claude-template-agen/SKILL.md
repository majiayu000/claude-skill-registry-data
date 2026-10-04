---
name: simplify
description: "Review recently changed code for simplification, dead code, over-engineering, duplication, and low-value abstractions — then fix what you find. Use immediately after implementing a feature/fix, after merging a branch, when code feels bloated, when the user says 'simplify', 'clean this up', 'tidy', 'refactor the mess', 'dọn dẹp code', or as the second stage of the /go verification loop. Focuses on net-negative diffs: prefer deleting over adding. Never changes public behavior, APIs, or test expectations. Not a full refactor — a focused cleanup pass on what just changed."
---
# /simplify — Focused Cleanup Pass

You are reviewing **code that just changed** (not the whole codebase) and removing every line, abstraction, or indirection that does not pay for itself. The goal is a **net-negative diff** — fewer lines, lower cyclomatic complexity, clearer intent — without changing public behavior.

## 🎯 Prime Rule — Delete First, Then Refactor

> The cheapest, fastest, most correct line of code is the one you don't write.

Before proposing any replacement, ask: **"Can this just be deleted?"** If yes, delete it. Only if the answer is no do you consider rewriting.

## 🚫 Hard Boundaries — Do NOT

1. **Do not change public API** (exported functions, types, route signatures, CLI flags, DB schema). If simplifying *requires* an API change, **stop and ask the user first**.
2. **Do not modify test expectations.** Tests describe the contract. Change the code to satisfy the tests, never the reverse.
3. **Do not touch code outside the current change's blast radius** unless it is directly entangled. Do not freelance a cleanup of unrelated files.
4. **Do not reformat** (whitespace, import ordering, quote style). That is the formatter's job, not yours.
5. **Do not "simplify" by adding new dependencies, frameworks, or abstractions.** Removing an abstraction is simplification; adding one with a friendlier name is not.
6. **Do not silence errors** to reduce code. If a try/catch exists because something can actually fail, it stays.

If any proposed simplification would break one of the above, discard it.

## 📋 Workflow

Follow these steps in order.

### Step 1 — Define the Blast Radius

Determine which files to review. In priority order:

1. **Staged + unstaged changes** (`git status`, `git diff`, `git diff --staged`) — the primary target.
2. **Files touched in the last commit** (`git diff HEAD~1 HEAD --name-only`) — if nothing is staged.
3. **Files passed explicitly by the user or caller** (e.g., `/go` passes the list of files it verified).
4. **Nothing else.** Do not wander the repo.

Output the blast radius as a list. If it is empty, stop and say "nothing changed — nothing to simplify."

### Step 2 — Read the Diff, Not the File

For each file in the blast radius, read the **diff** first (`git diff <file>`), then read surrounding context only for lines the diff touched. This keeps the review focused on what's new, not a general code audit.

### Step 3 — Run the 8 Simplification Lenses

For every changed hunk, walk through these lenses in order. Note concrete findings (file:line → issue → proposed action).

| # | Lens | Question |
|---|---|---|
| 1 | **Dead code** | Is this branch/function/import reachable? Is it referenced anywhere? Remove unused imports, unreachable branches, commented-out code, TODOs that are actually DONE. |
| 2 | **Redundant abstraction** | Does this wrapper/helper/class add information, or does it just rename the underlying call? A one-line wrapper used once is almost always net-negative. |
| 3 | **Duplication** | Is the same shape repeated 2+ times in the diff? Extract only if the duplicates will actually co-evolve (avoid premature DRY — incidental duplication is fine). |
| 4 | **Over-parameterization** | Does this function take a flag/option that is only ever passed one value? Inline the value. Does it have dead parameters? Remove. |
| 5 | **Speculative generality** | Is there a base class, interface, or plugin seam with only one implementation? Collapse to the concrete class. |
| 6 | **Nesting depth** | More than 3 levels of if/for nesting? Invert guards (`if (!x) return`), early-return, or extract. |
| 7 | **Comment-as-apology** | Is a comment explaining *why the code is confusing*? Fix the code so the comment is unnecessary. Keep comments that explain *why*, not *what*. |
| 8 | **Boolean-chain / null-dance** | Long `&&`/`||` chains, repeated `x && x.y && x.y.z`, defensive `if (x !== undefined && x !== null)`? Use optional chaining, destructuring, or restructure the data so the chain isn't needed. |

### Step 4 — Propose Edits as a Diff Plan

Before editing, list every proposed change in this format:

```
<file>:<line>  <lens #> — <one-line rationale>
  BEFORE: <short snippet or summary>
  AFTER:  <short snippet or "DELETE">
  Net:    <lines removed> / <lines added>
```

**Target: total net lines MUST be negative.** If your plan has more additions than deletions, you are not simplifying — stop and reconsider.

### Step 5 — Apply Edits

Apply the plan with `Edit`. After each file:

1. Re-read the file to confirm no dangling references.
2. If tests exist for the file, note them — they will be run in Step 6.

### Step 6 — Verify Behavior Is Unchanged

This is non-negotiable. Before declaring success:

1. **Type check** — run the project's type checker (`tsc --noEmit`, `mypy`, `cargo check`, `go vet`, etc. — detect from the project).
2. **Lint** — run the project's linter. Do not auto-fix style; fail loudly if your simplification introduced lint errors.
3. **Tests** — run the test suite scoped to the affected files if possible, full suite otherwise.
4. **If a /go verification script exists or was just run** — re-run it.

If any of these fail, **revert the change that caused the failure** and note it in the report. A simplification that breaks behavior is not a simplification.

### Step 7 — Report

Output a single report with this shape:

```
🧹 Simplify Report
  Blast radius : <N files>
  Findings     : <N>
  Applied      : <N>
  Skipped      : <N>  (reason each)
  Net lines    : -<X>  (deletions − additions; MUST be ≤ 0)
  Type check   : PASS / FAIL
  Lint         : PASS / FAIL
  Tests        : PASS / FAIL / NOT RUN (<why>)
  API changed  : NO   (if YES → you violated a boundary; revert)

Next step: <one of: "ship", "re-run /go", "review skipped findings with user">
```

## 🔁 When Called By `/go`

If the caller is `/go`, you will receive the verified file list explicitly. Use that as your blast radius (skip Step 1's discovery). Report back in the same format — `/go` will compose it into its own final report.

## ❌ When NOT to Run `/simplify`

- **On a branch you did not change** — there's no diff to review.
- **On generated code** (protobufs, OpenAPI clients, migration files) — those are owned by their generator.
- **Mid-feature** when the code is intentionally scaffolded and will be filled in next. Ask the user first.
- **Immediately before a release freeze** — simplification can introduce regressions; run it after the release, not before.

## 🧭 Philosophy — Why This Exists

Claude tends to produce slightly too much code: extra helpers, defensive guards, speculative flags, explanatory comments for confusing structure. A dedicated cleanup pass — run *after* the feature works, *before* the diff is committed — catches this drift. Over many iterations it compounds: the codebase stays lean instead of slowly bloating.

This is not a style pass. Style is the formatter's job. This is a **structural** pass: removing what does not earn its keep.
