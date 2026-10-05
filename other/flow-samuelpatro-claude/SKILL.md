---
name: flow
description: >-
  Verify a code change end-to-end in the current worktree: identify what
  changed, run the relevant tests, get the app running, drive a browser over
  the affected areas, and report a verdict with screenshots. Generic across
  project types (Laravel/Herd, Node/bun, frontend, CLI, library). Use when the
  user wants to verify/QA/smoke-test a change, check that a PR or branch works,
  validate uncommitted work, or says "/flow", "verify this change", "does this
  PR work", "test and click through this". Optional target: PR number/URL,
  branch/ref, or worktree path; default is the current working changes.
---

# Flow

Verify a change end-to-end and report whether it actually works: **change set →
tests → app running → browser → verdict.**

**Read-only on the repository.** No checkout/switch/stash/reset/pull, no new
worktrees, no commits or PRs — flow observes the current worktree and reports.
A target argument only locates the change set and context (e.g. PR acceptance
criteria). If the target isn't what's checked out, say so, verify what's
actually there, and let the user decide. The only `cd` allowed is into an
existing worktree path passed as the target.

## 1. Resolve the change set

- No argument → working changes: `git status --short` + `git diff HEAD`.
- PR number/URL → `gh pr view <n> --json title,body,headRefName,files,comments`
  and `gh pr diff <n>`. Use the PR body for acceptance criteria; flag it if the
  head branch isn't the current checkout.
- Branch/ref → `git diff <ref>...HEAD`.
- Worktree path → `cd` into it and use its working changes.

## 2. Understand what changed

Read the diff first: classify the files (backend, frontend, config,
migrations, tests, infra), identify the **affected surfaces** — the routes,
pages, endpoints, or commands a user reaches the change through (these drive
the browser step) — and extract acceptance criteria if the source has them;
without criteria you'll smoke-test. Non-UI changes (library, CLI, pure
backend) are verified by tests and direct command runs, not a browser.

## 3. Run the relevant tests

Use the project's own runner and commands. Scope to the change when scoping is
reliable, full suite otherwise. Failing tests don't stop the flow — continue
and surface them prominently in the verdict.

## 4. Get the app running

Reuse what's already serving (Herd site, running dev server) — never a second
server for the same code. Otherwise use the project's **run** skill or
documented dev command. Capture the base URL; if nothing can serve a UI, go to
the verdict with tests and CLI checks as the evidence.

## 5. Drive the browser

Use the **agent-browser** skill. This step is mandatory whenever the diff
touches anything the browser executes or renders — templates, JS/TS, CSS,
build config, assets — or backend that shapes those pages, even when the
running server serves different code: get the target served read-only (e.g.
`git archive` into a scratch dir, dev-serve on a free port or another loopback
address family, remap the hostname with Chrome's `--host-resolver-rules`) and
state in the report how the pages were served.

Walk each acceptance criterion; without criteria, smoke-test each affected
surface — the obvious interactions, console errors, failed requests. Stay
scoped to what the diff touched, not a full-site audit.

Every exercised surface needs **both DOM and visual evidence**: DOM/network
assertions (element state, response statuses, console, no stuck loaders) prove
behavior but are blind to rendering; a screenshot you actually view catches
broken layout, overlapping popups, missing images. DOM-only verification is
⚠️, not ✅. A screenshot saved but never viewed counts as not taken.

## 6. Report a verdict

Icons, used consistently: ✅ pass · ❌ broken, blocks the change · ⚠️ caveat or
partially verified · ⏭️ not applicable.

1. **Verdict line** — `✅ Looks good` / `⚠️ Works with caveats` /
   `❌ Issues found`. Be a critic: any ❌ forbids an overall ✅.
2. **Target** — what was verified and the checkout it ran against; flag any
   mismatch.
3. **Status table** — `Check | Status | Notes`, one row per check, one per
   acceptance criterion when they exist:

   ```
   | Check              | Status | Notes                                 |
   | ------------------ | :----: | ------------------------------------- |
   | Unit tests         |   ✅   | 497 passed / 31 files                 |
   | Login page renders |   ✅   | no console errors, screenshot clean   |
   | Cashflow (live)    |   ⚠️   | auth-gated, no backend under vite dev |
   ```

4. **Change summary** — a few lines: what the diff does, surfaces touched.
5. **Detail** — failing test output verbatim, per-surface browser results with
   screenshots, exact reproduction for any ❌.
6. **Nitpicks & follow-ups** — non-blocking issues, each with `file:line` when
   known and why it's low-priority. Write "None spotted." rather than omitting
   the section.

Every ❌ and ⚠️ in the table must be explained in Detail or Nitpicks.
