---
name: handover
description: Produce a high-detail continuation/handover file so a fresh session can resume with absolute accuracy. Use at every clean task close, when all todos are green-gated, and ALWAYS before a context compact — reserve enough context window to write it in full. Triggers on "handover", "continuation", "session close", "wrap up", "before compact", "checkpoint the session".
---

# Handover / continuation file

Produce a single Markdown file that lets a brand-new session (zero prior context)
continue THIS work with no loss of fidelity. This is Req 6 of the Kingdom operating
contract (knowledge/global/operating-contract.md).

## When to produce one (any of)

- A task or planned run closed clean and green-gated.
- All todos are complete.
- Context is getting heavy — produce it BEFORE a compact, not after. Watch the window
  and keep ~15–20% in reserve to write this file faithfully. A compact that happens
  before the handover exists is a continuity failure.
- The owner asks (`/handover`).

## Where it goes (keep the existing naming — do NOT invent a new scheme)

- **Kingdom control-plane work** (this repo, ~/kingdom):
  `docs/<project-slug-or-area>/kingdom-continuation-<ISO8601>.md`
  ISO8601 = `YYYY-MM-DDTHH-MM-SS` (hyphens, local time, matching the existing series).
- **Inside a tracked project** (~/kingdom/projects/<slug>): that project's own
  continuation location and name (e.g. `docs/<project>-continuation-<ISO8601>.md`).
- The new file SUPERSEDES the prior one — add a `supersedes:` line in the frontmatter
  and state "where this conflicts with an older note, this wins."

## Required sections (omit none; write "none" if empty)

1. **Frontmatter** — title, version (the ISO8601), supersedes, repo(s), branch, state.
2. **Git state (verify before trusting)** — current branch, last-known `main`/branch tip
   SHA, what is squash-merged vs local-only, any divergence traps. SHAs are
   "last observed" — include the exact commands to re-verify (do not assert as fact).
3. **What CLOSED this run** — merged/landed work, with the files touched.
4. **OPEN workstreams (carried forward)** — each with: current status, the decision
   pending (if any), the next concrete step, and any owner-gated blocker.
5. **Known untracked / in-flight files** — anything dirty on the tree that is expected.
6. **Verification commands** — copy-paste block to run at next session start
   (git state, gates, build) with the expected output for each.
7. **Standing rules & gotchas** — the environment/policy traps that bit this run
   (cross-reference knowledge/policies/ rather than re-deriving them).
8. **Next action** — the single first thing the next session should do.

## Method

1. Reconstruct git truth FIRST: `git log --oneline -5`, `git status -sb`,
   `git branch --show-current`, and (for projects) `git log origin/main` — never assert
   a SHA you have not just observed.
2. Pull forward the still-open items from the PRIOR continuation file (don't drop them).
3. Write the file. Stage ONLY that file (`git add <path>`; never `git add -A` on a dirty
   tree). Commit in isolation, then it is safe to `/clear` or allow compact.
4. If this is also a planned-run close, follow knowledge/policies/run-close.md
   (push Kingdom + ensure draft PR) after the file is committed.

## Token discipline (Req 1)

Dense and pointer-based. Reference file paths and policy docs instead of pasting large
bodies. The goal is total reconstructability per token, not length.
