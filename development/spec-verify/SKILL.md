---
name: spec-verify
description: >
  Verify a completed feature spec by driving the real running app — not just lint/typecheck/build
  — and checking off every acceptance criterion from its specs/{feature}/ folder one by one. Use
  this after /spec-implement finishes a spec, when the user says "test this end to end",
  "verify this feature actually works", "did we actually build this right", or "/spec-verify",
  and before /spec-ship or opening a PR. This is the spec-aware sibling of the generic /verify and
  /run skills — /verify checks an arbitrary diff's runtime behavior and /run just launches the
  app, but this skill specifically reads a spec's requirements.md and task files, builds a master
  checklist of acceptance criteria, and reports pass/fail per criterion with real evidence
  (screenshots, API responses, DB state) instead of a vague "looks good." Always invoke this when
  a specs/{feature}/ folder exists and its implementation just finished, even if the user only
  says "does this work" or "test it."
license: MIT
---

# Verify Feature

Close the loop that `spec-create` → `spec-implement` leaves open: passing lint, typecheck, and
build proves the code compiles, not that the feature does what the spec says it does. This skill
reads a spec's acceptance criteria and checks each one against the actual running application —
clicking through the UI, calling the real API routes, or inspecting real database state produced
by the real code path. It produces a report the user can trust before shipping.

## When there's no spec folder

If the user asks to verify a feature that wasn't built through `spec-create`, don't refuse —
interview them briefly for what was built and what "working" means (the golden path, the edge
cases they care about), then skip to [Step 3](#step-3-prepare-the-environment) treating their
answers as the criteria list. The spec-driven path below is the common case, not the only one.

## Step 1: Locate the spec

1. If the user named a feature, use `specs/{feature}/`.
2. Otherwise look for a `specs/*/README.md` whose Task Status section is fully checked (all
   tasks `- [x]`) but has no `verification-report.md` sibling yet — that's the most recently
   completed, not-yet-verified feature.
3. If `spec-implement` hasn't finished all batches yet (some tasks still `- [ ]`), tell the user
   and ask whether to verify what's done so far or wait for the rest — verifying half a feature
   can produce confusing false failures for criteria that depend on an unbuilt task.

## Step 2: Build the master criteria checklist

Read `requirements.md`'s **Acceptance Criteria** section (feature-level, the whole thing working
end-to-end) and every `tasks/task-*.md`'s own **Acceptance Criteria** section (task-level). Merge
them into one ordered list, each item tagged with its source (`requirements` or the task
filename).

Split the merged list into two kinds, because they're verified completely differently:

- **Static criteria** — things like "`npm run check` passes" or "`npx next build` succeeds."
  `spec-implement`'s review gate already ran these during the build. Re-run them once quickly
  to confirm nothing regressed since (uncommitted fix-ups, a rebase, etc.), but don't treat this
  as the interesting part of verification.
- **Behavioral criteria** — anything that describes what a user, an API caller, or a scheduled
  job actually observes ("a FREE user sees a Renew button," "the cron doesn't double-send,"
  "removing a member revokes their access on next request"). These are why this skill exists —
  they require driving the real app, not reading the diff.

## Step 3: Prepare the environment

Check whether the dev server is already running (e.g. `curl -sf http://localhost:3000` or the
port your project's dev script uses) before starting a new one — a stray second instance just
causes confusing port conflicts. If nothing responds, start `npm run dev` in the background and
poll until it's ready.

Look at what the behavioral criteria actually need before reaching for tools:

- **UI-observable** (a button appears, a page shows a value, a flow completes) → browser
  automation. Use whatever browser-automation capability your host provides — a browser MCP
  server (Playwright, Puppeteer, etc.), a built-in browser tool, or a browser extension — and
  enable/load it per your host's own convention if it isn't active by default. Take a screenshot
  as evidence for each criterion you check this way.
- **API-only** (no UI surface, e.g. a webhook or a cron route) → call the real route. For
  session-gated routes, log in through the actual UI once (or reuse a session cookie from a
  browser step) rather than fabricating auth state. For routes gated by a bearer secret (like a
  cron's `CRON_SECRET`), call them directly with `curl`.
  Note: if your browser tool can read console/network logs, that's useful when a criterion is
  best confirmed by watching what the frontend actually sent/received rather than clicking
  through screenshots.
- **DB-state-only** (a column got stamped correctly, a row was scoped the way it should be) →
  drive the real write path first (through the UI or API — never insert the expected state
  directly, that verifies nothing), then read the resulting row back via Prisma or `psql` to
  confirm it. This mirrors how you'd sanity-check a migration: trust the app's own code path to
  produce the state, and only use direct DB reads for the *assertion*, never the *setup*.
- **Timing-dependent** (a reminder email fires N days before expiry, idempotency across cron
  runs) → don't wait real days. Insert or edit the relevant date field in the test data so it
  already sits at the boundary the criterion describes, then invoke the real code path (call the
  cron route, run the actual query) and observe what happens. You're still exercising the real
  logic — you're just moving the clock via input data instead of a `sleep`.

Create whatever throwaway test data (a second test user, a lapsed subscription row, etc.) each
criterion needs. Note everything you create — you'll remove it in Step 5.

## Step 4: Verify each criterion

Work through the checklist in order. For each one, record:

- **Verdict**: PASS, FAIL, or SKIPPED (with a reason — e.g. "requires a live payment gateway
  webhook, not reproducible locally").
- **Evidence**: a screenshot path, the exact `curl` command and response, or the DB query and
  the row it returned. Evidence is what makes the report trustworthy instead of another
  unverified claim — write down enough that someone who wasn't watching could confirm it.
- **For a FAIL**: the concrete scenario that breaks it (exact input/state → actual vs expected
  output), not just "doesn't work." This is what turns a failure into something fixable.

Don't stop at the first failure — finish the checklist so the report reflects the feature's real
state, not just the first thing that went wrong.

## Step 5: Clean up

Remove every test user, record, or row you created in Step 3/4 so the dev database is left the
way you found it. Never delete data that predates this run — if you're not certain something is
yours, leave it. If you started the dev server yourself in Step 3, it's fine to leave it running
(the user likely wants it for their own follow-up testing) — just say so in the report.

## Step 6: Report

Write `specs/{feature}/verification-report.md` — see `references/report-template.md` for the
exact structure (a summary line, then a table of criterion → source → verdict → evidence, then a
"Failures" section with full repro detail for anything that didn't pass).

Update `specs/{feature}/README.md` with a short **Verification** section linking to the report
and stating the overall status (all pass / N of M pass).

Then tell the user directly:

```
Verified {feature}: {X}/{Y} criteria passed.

{If all pass:} Ready to ship.
{If failures:} {N} failing — see specs/{feature}/verification-report.md for exact repro steps.
Options: loop back to /spec-implement to fix, or fix manually.
```

This skill only verifies and reports — it does not fix failures itself. Mixing "test" and "fix"
in one pass makes it too easy to quietly patch a failure without recording that it happened;
keeping them separate means the report is always an honest snapshot of what was actually true
when you ran it.
