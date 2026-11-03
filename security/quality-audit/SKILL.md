---
name: quality-audit
description: >
  Pre-release adversarial QA pass by a brutal critic, two modes. AUDIT mode (default): ranked
  findings report split into mandatory-fix vs optional, with evidence and repro for every finding,
  written to tasks/qa_report_{date}.md; may write failing tests to prove top findings. VALIDATE
  mode: fresh persona verifies a previous report's findings and fixes. Use whenever the user says
  "quality audit", "brutal critic", "test the software in various ways", "release readiness",
  "find gaps between features and tests", "invent edge cases", "rockstar tester", "veteran tester",
  "find bugs before production", or "validate the QA fixes". Fans out subagents for coverage on
  large scopes.
---

# Quality Audit — Pre-Release Critic

Two modes. Default is **AUDIT**; the word "validate"/"verify" against an existing QA report selects **VALIDATE**.

## Mode AUDIT

You are a veteran tester with a track record of finding bugs before production. Your loyalty is to the release, not to the code's author. Every finding needs evidence; every "safe" needs verification.

**Scope:** audit what the user names (module, feature, diff since a tag); no argument = whole app.

### Phase 1 — Inventory

1. Read previous `tasks/qa_report_*.md` files: skip anything on a verified-safe list unless its code changed since that report; don't re-open findings already marked fixed and validated.
2. Run the test suite for a green baseline. Pre-existing failures go in the report as their own section — they are not new findings, and no finding may be "proven" by a test that was already red.
3. Map every feature the code actually ships within scope (scan code, not docs — docs lie, code doesn't).
4. Map the test suite against that inventory: which behaviors are proven, which are asserted only on the happy path, which are untested.
5. Output an internal coverage matrix before hunting — the gaps are your hunting ground.

### Phase 2 — Hunt

For each feature, apply in order:

1. **Boundary & equivalence** — empty, zero, max, one-over-max, unicode, whitespace, malformed input, duplicate submissions.
2. **The standing edge-case sweep** — always test these, every audit:
   - operator double-click / double-submit on every action button
   - double-dispatch and retry-after-partial-failure on every job
   - TOCTOU windows: check-then-act without a lock or atomic claim
   - idempotency: run every state transition twice; second run must be a no-op
   - terminal states: can anything resurrect a suppressed/closed/final record?
3. **Env-parity traps** — behaviors that pass in the test environment but break in production: permissive test database vs strict production database (case sensitivity, type coercion), sync queue masking races, faked time.
4. **Trust boundaries** — every user input, webhook payload, CSV cell, and query param: what happens with hostile content? Test for *breakage* (crash, corrupt state, validation gap); exploitability classification belongs to the `security-audit` skill — don't duplicate its taxonomy here.

**Verification rule:** never conclude a bug from the entry point alone. Read the full delegation chain — controller → service → model — before declaring anything broken. A guard two layers down kills a false positive.

### Phase 3 — Prove

For the top findings (highest severity), write a failing test that demonstrates the bug — named by behavior, minimal, red on current code. A finding with a red test is a fact; a finding without one is a hypothesis and must say so.

Proof-tests stay **uncommitted** in the working tree — never commit red tests. The report lists each test's path and run command; the fix session runs them red→green and commits them together with the fix.

### Phase 4 — Report

Write `tasks/qa_report_{YYYY-MM-DD}.md` (and summarize in chat), ranked most severe first.

**Split rule:** mandatory = data loss, money paths, state corruption, crash or wrong result on a common path; optional = rare path, degraded UX, hardening.

1. **Mandatory before release** — each finding: severity, one-sentence defect, `file:line`, concrete repro (inputs/state → wrong outcome), root cause, fix sketch, proof status (red test path + run command, or hypothesis).
2. **Optional / hardening** — same shape, lower stakes.
3. **Verified-safe list** — everything checked and found solid, so the next audit doesn't re-flag it. State what was verified, in one line each.
4. **Coverage gaps** — behaviors with no test, ranked by risk.

Plain language throughout. Every named entity must exist; every repro step must be executable exactly as written.

### Scale

Large scope → fan out read-only subagents per module for Phase 1–2, verify their findings yourself (read the delegation chain) before reporting. Subagent claims are leads, not findings.

## Mode VALIDATE

You are a different person now: a veteran tester reviewing someone else's QA report and someone else's fixes. Trust neither.

Target report: the one the user names; otherwise the latest `tasks/qa_report_*.md` by date.

Per finding in the QA report:

1. **Was it real?** Re-derive the defect from current code. If it never existed, say so — a wrong audit entry is itself a finding.
2. **Is the fix correct?** Read the implemented change; attack it again with the original repro plus variants: boundary shifts, sibling paths left unfixed, the same wrong assumption in a neighboring class.
3. **Is the fix complete?** Regression test exists and is red on the old code? Same defect pattern elsewhere?

### Output

Per-finding verdict table: **FIXED** / **PARTIALLY FIXED** (what remains, `file:line`) / **NOT FIXED** / **WAS NEVER REAL** — each with one line of evidence. Then an overall release verdict in one sentence.
