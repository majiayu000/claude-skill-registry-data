---
name: smoke-test
description: "Goal-driven smoke test for the feature just implemented. Drives a browser (UI) or hits the running service (backend), both, when full-stack. Tests every behaviour acceptance criteria define plus exploratory edges, catches console errors / network failures / a11y issues / contract violations / auth leaks / missing observability, fixes every gap or bug it finds, then re-runs until clean. Captures the successful trajectory as a permanent test before declaring done. Use after implementation and after figma-matcher (when UI), before /flagrare:wrap-up. Triggers when the user says 'smoke test', 'does this actually work', 'test the feature', 'validate this', 'launch the app and test', 'make sure nothing is broken', or finishes implementing a feature."
---

# Smoke Test

A goal-driven validation pass for the feature you just implemented. The pass ends only when every scenario, both acceptance-criteria-defined and exploratory, passes against a real running instance, every gap or bug found has been fixed, and the working trajectory has been captured as a permanent test.

The word "smoke" is doing real work here: this is not a full regression suite. It is the shortest path that exercises the new behaviour end-to-end against a real running system. If it can't be done in under ten minutes, the scope is wrong, split the feature, not the test.

---

## Why this exists

Implementation finishing and the feature working are two different events that teams routinely conflate. Tests pass, types check, lint is clean, and the feature is still broken in production because nobody opened the actual app or hit the actual endpoint. Static checks measure code, not behaviour. This skill closes that gap.

There is a second reason. The model that writes the implementation also writes its own test discipline. Without an external loop that exercises the running system, defects that live between units, exactly the defects integration tests are supposed to catch but rarely do completely, ship straight to review.

---

## Step 1: Set the goal explicitly

Before any action, state the goal in one sentence. The goal owns this entire flow; the agent does not exit until the goal is met.

> **Goal:** validate that [feature name / ticket key] works end-to-end against a running instance. Every acceptance criterion passes, every exploratory edge passes, every gap or bug found is fixed before exit, and the successful trajectory is captured as a permanent test.

Surface the goal back to the user in plain prose so they can correct scope before the loop starts.

---

## Step 2: Detect the domain

Inspect the staged diff (`git diff --staged --name-only`) and the recent context (intake brief if present, last few commits if not) to pick the domain.

| Signal | Domain |
|---|---|
| Diff touches `.tsx`/`.jsx`/`.vue`/`.svelte`/`.css`/`.scss`/component dirs, no backend handlers | `ui` |
| Diff touches API handlers / controllers / route files / DB migrations / worker code, no frontend files | `backend` |
| Diff touches both | `both` |
| Ambiguous | ask via `AskUserQuestion` with the three options |

Load the matching reference file(s):

- `ui` → read `references/ui.md`
- `backend` → read `references/backend.md`
- `both` → read both. The priority order interleaves: do P0-P1 of each domain in parallel, then P2 of each, and so on, so a broken backend doesn't block UI validation and vice versa.

Skip the skill entirely when the diff is purely process / config / docs and no user-observable behaviour changed, say so explicitly rather than running an empty loop.

---

## Step 3: Derive scenarios from acceptance criteria + diff

This is the part where AI assistance pays off most. Draft the scenario list once, then freeze it as something the loop executes deterministically.

Gather inputs:

- Acceptance criteria, from the intake brief (`## Acceptance Criteria` section), the ticket, the PR description, or directly from the user
- The diff, what the feature actually changed, not just what the ticket asked for (implementations often go beyond or under the spec)
- Skip-conditions, anything the user explicitly deferred ("error handling out of scope for this PR" stays out)

Emit a structured scenario list. Each scenario has:

- An ID (`S1`, `S2`, …)
- A priority tier (P0-P4, domain-specific; see the reference files)
- A one-line behaviour description, phrased as what the user / caller observes
- A pass condition that's objectively verifiable

Show the list to the user via `AskUserQuestion` with options to **Run all (Recommended)** / **Edit scope first** / **Cancel**. Don't start driving the browser or hitting the API before scope is confirmed, a smoke test against a wrong scope is just noise.

---

## Step 4: Run the priority loop

Walk the scenarios in priority order, lowest tier first (P0 catches dead-on-arrival, P4 is nice-to-have). The reference files define each tier in detail; this section describes the loop, not the content.

For each scenario:

1. Execute it (drive the browser / hit the endpoint, see reference for tooling).
2. Capture the outcome and the *evidence*: a screenshot, the network log, the response body, the spans emitted, the console output. Evidence is what makes the fix-and-retest loop possible.
3. Record: `pass`, `fail`, or `blocked` (depends on a prior scenario failing).

If P0 fails, stop the cascade, fix P0 first, then restart from P0. P0 is "did the feature even load?", if not, everything else is noise. P1 onwards can collect failures and triage them together.

**No retries on flake.** A scenario that passes on second attempt without an intervening change is a defect, not a config setting. Investigate. Race conditions, hydration timing, and connection-pool warmup all hide behind retries.

---

## Step 5: Fix-and-retest

For every `fail`, fix it before exit. Not "log it for later." Not "tracked in the PR description." Fixed.

Loop:

1. Pick the highest-priority failure.
2. Diagnose using the evidence captured in Step 4 (and for UI failures, Chrome DevTools MCP for the deeper console/network/perf view, see `references/ui.md`).
3. Apply the fix at the lowest reasonable layer (style fix in CSS, not a JS workaround; validation in the schema, not the controller).
4. Re-run that scenario. If it now passes, re-run any scenarios that were `blocked` by it.
5. Repeat until every scenario is `pass`.

The loop ends only when the scenario list is all green. If a fix takes the work out of scope (a defect not caused by this PR), surface it to the user via `AskUserQuestion`: **Fix in scope** / **Defer with a follow-up ticket** / **Block this PR until resolved**. The user owns the call; the skill must not silently defer.

---

## Step 6: Capture the trajectory as a permanent test

A successful smoke pass is wasted unless the next person can re-run it without re-driving the browser by hand. Before declaring the goal met, convert the trajectory into a runnable test:

- **UI**: capture as a Playwright spec via the MCP server's codegen (see `references/ui.md`). One file per feature, named for the feature. Use `getByRole` / `getByLabel` selectors, never CSS classes or XPaths. Include the same scenarios at the same priorities; the spec becomes the regression test.
- **Backend**: capture as a test file in the project's existing test framework (pytest / vitest / jest / cargo test / go test, match what the repo already uses). Include schema assertions, auth matrix cases, error-shape assertions, and observability spans (see `references/backend.md`).

If the project already has a smoke-test suite, add to it. If not, create the suite in the conventional location (`tests/smoke/`, `e2e/`, or the framework's default).

This step exists because a smoke test that only the agent can run is a regression that will land within weeks. Codifying it makes the next person's work cheaper, not just yours.

---

## Step 7: Confirm the goal is met

Once every scenario passes and the trajectory is captured, surface the final state to the user via `AskUserQuestion`:

- **Goal met, proceed to `/flagrare:wrap-up`** (Recommended): the feature works end-to-end, every gap was closed, the regression test landed.
- **Goal met, stop here**: same as above, user wants to do something else next.
- **Adjust scope and re-run**: the user wants to expand or shrink scenarios.

Never declare done by prose. The button-prompt is the audit trail.

---

## Anti-patterns

- **Don't run the loop without a goal statement.** "I'll just check a few things" is how a smoke test becomes performance theatre. Step 1 exists to make the exit condition explicit.
- **Don't accept "mostly works."** Either every scenario passes or the loop is not done. There is no partial credit. If a scenario can't be validated this round, that's a fix-or-defer decision the user owns, not a silent skip.
- **Don't retry to mask flake.** A scenario that passes only on the second run is a defect. Investigate the timing / state / cleanup gap instead of adding retries.
- **Don't end with a prose question.** Step 7 uses `AskUserQuestion`. Same UX contract as plan-mode's accept tool: a button, not a typing prompt.
- **Don't skip the capture step.** A trajectory that isn't codified will need to be re-driven by hand the next time someone touches this feature. That is the regression bug already happening, you just haven't met it yet.
- **Don't depend on external skills.** flagrare skills are self-contained. Use MCP tools (Playwright MCP, Chrome DevTools MCP) directly when present; degrade gracefully when not (ask the user to run the test pass themselves and report results).
- **Don't blur smoke and full regression.** Ten-minute budget. If the loop is taking longer, the scope is wrong, split the feature, not the test.

---

## Flow position

```
[implementation]
     ↓
/flagrare:figma-matcher       (only when UI; verify visual against Figma)
     ↓
/flagrare:smoke-test          (this skill, behavioural validation against a running instance)
     ↓
/flagrare:wrap-up             (static quality: tests, lint, types, /flagrare:implementation-review)
     ↓
/flagrare:staleness-audit
     ↓
git commit
     ↓
/flagrare:open-pr
     ↓
/flagrare:release-check
```

When the feature is backend-only, skip the figma-matcher step and start at smoke-test. When it's UI-only, smoke-test runs without the backend branch of the priority loop. Full-stack features run both branches interleaved (see Step 2).

---

## References

- `references/ui.md`, UI priority order (P0 preconditions, P1 acceptance criteria, P2 cross-cutting quality gates, P3 exploratory, P4 nice-to-have), Playwright MCP + Chrome DevTools MCP split, axe + keyboard walk
- `references/backend.md`, backend priority order (reachability → happy path → contract → auth matrix → error shape → boundaries → idempotency → observability → edges → latency), RFC 9457 Problem Details, observability-driven testing, 403/404 tenant-leak check
- `docs/research/2026-05-23-ui-smoke-test-best-practices.md`, sourced findings the UI reference is built on
- `docs/research/2026-05-23-backend-smoke-test-best-practices.md`, sourced findings the backend reference is built on
