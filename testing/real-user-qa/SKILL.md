---
name: real-user-qa
description: Use when asked to "QA this", "is this ready to ship?", "test it like a user", "bug hunt", "sign off this build/phase", or before declaring a web app / feature shippable — a real-user QA pass that files severity-ranked bug reports and returns a binary ship verdict. Not for visual/CRO polish (frontend-audit) or fixing an already-reported UI bug (ui-fix-observe-first).
---

# real-user-qa

Simulate a careful, mildly unforgiving customer who has never read the source code. Drive the live app from URLs, clicks, and form fills — not from the API layer or code inspection — file every failure as a structured bug, and end with a binary verdict. Adapted from rayfernando's running-bug-review-board (Apache 2.0), retooled for our stack.

**Why this exists:** engineers test what they wrote; it works. Real users hit stale state across flows, mobile overflow, copy that lies, 404s mid-onboarding, races between auth and routing. The happy path is what was already tested — everything else is your job.

## Three hats per pass

- **PM** — does the build deliver the user-visible promise in the spec/phase doc? A missing promise is a product gap, flagged in the run report, not a bug.
- **QA** — execute every scenario as a real user; capture evidence; Pass / Fail / Blocked.
- **Engineer** — note invalidated assumptions (docs say server-driven, UI shows client orchestration; fields in UI absent from spec). Finding doc–reality gaps is the point; never edit the docs to match buggy behavior.

Do NOT fix product code during the pass unless explicitly asked. Test, document, file, hand off.

Two references carry the tactical depth — load them at the step that needs them:
- [references/driving-and-accounts.md](references/driving-and-accounts.md) — human-like driving (attach to real Chrome, fresh-ref discipline, recovery protocol), hygiene cooldowns/rate limits, per-provider test-account fixtures (Clerk OTP, Stripe cards, emulator ports).
- [references/scenarios-and-verdict.md](references/scenarios-and-verdict.md) — environment gate, scenario ID taxonomy + pain-point seed checklist, bug lifecycle (reproduce-twice, Impact/Risk-to-fix, dedup heuristics), strict verdict/gate rules, resume protocol, parallel sharding, gh-CLI tracker sync.

## Workflow

0. **Environment gate** — build/typecheck must pass first. Failure is a BLOCKER, not a bug; don't start scenarios on a broken build.
1. **Discover** — read spec/README/phase doc for the promise and what was just built; re-test open bugs and prior-pass regressions FIRST (regressions are the highest-value finds); list entry points a real new user touches. No docs at all? Derive candidate scenarios from the landing page and visible routes, state them as assumptions, and ask the user to confirm the core promise before planning — don't invent the product.
2. **Plan** — write a scenario list with IDs, steps, and expected results before driving anything. No plan = ad-hoc clicking that misses coverage. If scenarios need a signed-in state and no test account is documented, ask the user for one before guessing at credentials or seeding data.
3. **Drive** — our tool ladder: chrome-devtools MCP (CDP; DOM-first, real signed-in Chrome, console/network inspection) → Claude-in-Chrome extension → Playwright. One browser tab/profile per agent; never share a tab across parallel agents (auth throttling, session bleed).
4. **Viewports** — test mobile 375×812, tablet 768×1024, desktop 1280×800 (or the spec's breakpoints). Lead with the product's primary; overflow and tap-target bugs hide at the breakpoint you skip.
5. **File bugs immediately on FAIL** — not at end of pass. Destination: `docs/qa/bug-reports/BUG-NNN-<slug>.md` in the target repo (adopt the repo's existing QA/issue layout instead if one exists; use the session scratchpad only if the user doesn't want QA files committed). Each bug: title, severity, steps to reproduce, actual vs expected, evidence (screenshot/snapshot at the moment of failure + console errors verbatim + server row when relevant), suspect area if obvious.
6. **Verdict** — merge results and close with the verdict block.

## Severity

| Level | Definition | Effect |
|---|---|---|
| **P0** | Blocks core flow; data loss; auth bypass; security | Cannot ship; halt the pass until triaged |
| **P1** | Feature broken or wrong; workaround exists | Blocks sign-off |
| **P2** | Cosmetic, edge case, a11y, console noise | Defer to polish |

Torn between P0 and P1? Pick P0 if a user can land in a non-recoverable state or lose data.

## Verdict (required closing block — the last thing in the report)

> **Ready? YES** — all scenarios pass with evidence on the current build, no open P0/P1.
> **Ready? NO** — open P0/P1 listed + unrun scenarios + paste-ready handoff (branch/commit, open bugs, remaining scenario IDs, test accounts, known gotchas) so a fresh session needn't rediscover state.

A pass where every scenario came back BLOCKED (infra, no product bug) is still **NO** — nothing was verified. Gate-flip and resume rules: [references/scenarios-and-verdict.md](references/scenarios-and-verdict.md).

## Session hygiene

Stale localStorage/cookies/reused test emails silently poison fresh-user flows. Fresh profile or cleared storage per fresh-user scenario; suffix test emails per run (`+run3`); never reuse a previously-failed test email without changing the suffix.

## Never

- Mark PASS from code inspection — users experience the app, not the source.
- Sign off without evidence per scenario.
- Test only the happy path.
- Trust prior PASS marks on a fresh build without re-running.
- Rename specs/docs to match buggy behavior.
- File a bug without steps to reproduce — it's not actionable.

## When the pass reveals work bigger than QA

A promised feature with no code path, a schema diverging from spec across scenarios, or a P0 blocking everything remaining → stop testing, surface the finding, let the user decide. Continuing burns time on a foundation that needs replacing.

## Siblings

- `frontend-audit` — read-only visual/CRO/a11y report; run it for design quality, this skill for functional ship-readiness.
- `ui-fix-observe-first` — the fix loop AFTER a bug from this pass is assigned.
- `verify-the-claim-not-the-label` / `subagent-verification-workflow` — if QA shards were delegated to subagents, their PASS claims are hypotheses; spot-check evidence before merging into the verdict.
- `authoring-dynamic-workflows` — a large multi-surface pass can run as a workflow fan-out (one shard per surface/viewport, manifest-as-coverage-gate, verify tier per shard).
