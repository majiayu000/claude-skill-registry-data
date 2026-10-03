---
name: simplify-code
description: "Sequential 3-lens cleanup of recent code changes."
allowed-tools:
  - bash
  - read_file
  - str_replace
  - write_file
enabled: true
related-skills: [requesting-code-review, test-driven-development, plan]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); inspired by Claude Code /simplify
---

# Simplify Code — Sequential Review & Cleanup

Review your recent code changes with three focused lenses, aggregate findings,
and apply the fixes worth applying.

**Core principle:** Three narrow reviews beat one broad review. Each one deeply
searches the codebase for a single class of problem — reuse, quality,
efficiency — without diluting attention across all three.

> **Poirot note:** The original skill runs 3 reviewers in parallel via
> subagent delegation. Poirot has no subagents, so this version runs the 3
> lenses **sequentially** in the same context. The methodology is identical;
> only the concurrency is lost.

## When to Use

Trigger this skill when the user says any of:

- "simplify" / "simplify my changes" / "simplify these changes"
- "review my code" / "review my recent changes" / "clean up my changes"

Optional modifiers the user may add — honor them:

- **Focus:** "simplify focus on efficiency" → run only the efficiency lens.
  Recognized focuses: `reuse`, `quality`, `efficiency`.
- **Dry run:** "simplify but don't change anything" / "just report" → run the
  three lenses, present findings, apply NOTHING. Ask before applying.
- **Scope:** "simplify the last commit" / "simplify staged" / "simplify
  src/foo.py" → narrow the diff source accordingly.

Do NOT auto-run this after every edit. Invoke it only when the user asks.

## The Process

### Phase 1 — Identify the changes

Capture the diff to review. Pick the source by what the user asked for:

```bash
# 1. Default: uncommitted working-tree changes (tracked files)
git diff

# 2. If that's empty, include staged changes
git diff HEAD

# 3. Scoped variants:
git diff --staged                 # "staged changes"
git diff HEAD~1                    # "the last commit"
git diff main...HEAD              # "this branch" / "my PR"
git diff -- src/foo.py            # specific file(s)
```

If `git diff` and `git diff HEAD` are both empty, fall back to files the user
explicitly named or recently edited in this session. If you can't find any
changed code, say so and stop.

Capture the full diff text. Note its size: if >2000 changed lines, warn the
user and offer to scope down before proceeding.

### Phase 2 — Run three lenses (sequentially)

Each lens gets the **complete diff** (not fragments — cross-file issues hide in
the gaps) plus the repo path so it can search the wider codebase via `bash`
(`grep`) and `read_file`.

For each lens:
- Search the existing codebase for evidence (don't reason from the diff alone).
- **Apply Chesterton's Fence:** before flagging anything for removal, run
  `git blame` on the line to understand why it exists. If you can't determine
  the original purpose, mark it `confidence: low`.
- Report findings as structured output:
  ```
  file:line → problem → suggested fix | confidence: high/medium/low | risk: SAFE/CAREFUL/RISKY
  ```
  - **SAFE** = proven not to affect behavior (unused imports, commented-out
    code, pass-through wrappers). Auto-apply these.
  - **CAREFUL** = improves without changing semantics (rename local variable,
    flatten nested ternary, extract helper). Apply with test verification.
  - **RISKY** = may change behavior or breaks public contracts. Flag for
    human review — do NOT auto-apply.
- Skip nits and style-only churn.

Run these three lenses (skip any the user's focus excludes):

**Lens 1 — Code Reuse**
> Review this diff for code that duplicates functionality already in the
> codebase. Search utility modules, shared helpers, and adjacent files (use
> `bash` grep) for existing functions, constants, or patterns the new code
> could call instead of reimplementing. Flag: new functions that duplicate
> existing ones; hand-rolled logic that an existing utility already does. For
> each, name the existing thing to use and where it lives.

**Lens 2 — Code Quality**
> Review this diff for quality problems. Look for: redundant state; parameter
> sprawl; copy-paste-with-variation; leaky abstractions; stringly-typed code
> (raw strings where a constant/enum exists); AI-generated slop patterns
> (extra comments restating obvious code, unnecessary defensive null-checks,
> `as any` casts). For each, give the concrete refactor.

**Lens 3 — Efficiency**
> Review this diff for efficiency problems. Look for: unnecessary work
> (redundant computation, repeated file reads, N+1 access); missed concurrency;
> hot-path bloat; TOCTOU anti-patterns; memory issues (unbounded growth,
> missing cleanup); overly broad reads; silent failures (empty catch blocks,
> `except: pass`). For each, give the concrete fix and why it's faster/safer.

### Phase 3 — Aggregate and apply

1. **Merge** the findings into one list, deduping where lenses overlap.
2. **Discard false positives** — you have the most context; drop weak or wrong
   suggestions silently.
3. **Resolve conflicts.** Default resolution order:
   **correctness > the user's stated focus > readability/reuse > micro-perf.**
   Don't apply a perf "fix" that hurts clarity unless the path is genuinely hot.
4. **Apply in risk-tier order:**
   - **SAFE first** (auto-apply): unused imports, commented-out code,
     pass-through wrappers. Run tests after.
   - **CAREFUL next** (apply with verification, one file at a time): rename
     locals, flatten ternaries, extract helpers, consolidate dupes. Run tests
     after each file. Revert any that break.
   - **RISKY last** (flag for review — do NOT auto-apply): N+1 restructuring,
     public API changes, concurrency fixes. Present each with risk description
     and test coverage status.
   If the user opted for a dry run, present all three tiers and apply nothing.
5. **Verify** you didn't break anything: run the project's targeted tests for
   the touched files, and re-run any linter/type check the repo uses. If a fix
   breaks a test, revert that one fix and report it.
6. **Summarize** what you changed: a short list of applied fixes grouped by
   lens and risk tier, plus any findings you deliberately skipped and why.

## Pitfalls

- **Give the WHOLE diff to each lens.** Splitting the diff defeats the design —
  cross-file duplication and N+1s only show up with the full picture.
- **Lenses search, they don't guess.** A reuse finding with no pointer to the
  existing utility is noise. Require `file:line` evidence; drop findings that
  lack it.
- **Apply ≠ rewrite.** This is cleanup of the user's recent changes, not a
  license to refactor the whole module. Keep edits scoped to what the diff
  touched plus the minimal surrounding change a fix requires.
- **Respect project conventions.** If the repo has `AGENTS.md` / `CLAUDE.md`
  or a linter config, fold those rules into the lens prompts so suggestions
  match house style.
- **Large diffs blow context.** If the diff is huge, scope it down before
  reviewing — a 5000-line diff may truncate.
- **Over-trusting dead code tools.** `knip`, `ts-prune`, `depcheck` flag
  exports that ARE used dynamically. Always grep for the symbol name before
  removing — a clean tool report is not proof.
- **Renaming without checking public contracts.** Export names, API route
  paths, DB column names, config keys are contracts. Tag public-contract
  changes as RISKY; never auto-rename them.
- **Removing "unnecessary" error handling.** An empty catch block might be
  intentional. Flag it, don't remove it; let the human decide.

## Related

Use `requesting-code-review` for the pre-commit security/quality gate.
This skill is the standalone *after-the-fact* cleanup pass.
