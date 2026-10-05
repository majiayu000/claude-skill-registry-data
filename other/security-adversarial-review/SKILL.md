---
name: "security-adversarial-review"
description: "Actively try to break a running, isolated instance of the application with malformed input, boundary conditions, and deliberate misuse, and report any runtime issue found with exact reproduction steps. Refuses to run against anything but a loopback target. Trigger phrases: adversarial review, penetration test, try to break the app, fuzz the app, red team the running app."
argument-hint: "<target-url> (must be a loopback address, e.g. http://localhost:PORT — an already-running Aspire dashboard/service URL)"
user-invocable: true
---

## Instructions

Contract: `specs/008-adversarial-security-review/contracts/skill-commands.md` (`/security-adversarial-review`).
Requirements satisfied: FR-005, FR-006, FR-007, FR-010, FR-011, SC-004.

### 1. Read trigger-mode config (FR-011)

Read `specs/008-adversarial-security-review/review-config.json` and check `adversarialReview.trigger`. Today the only valid value is `"on-demand"` — proceed for a manual invocation.

### 2. Enforce the loopback guard BEFORE anything else (FR-006, SC-004)

```bash
.specify/scripts/bash/security-assert-loopback.sh "<target-url>"
```

**If this exits non-zero, stop immediately.** Show the user the error and do not proceed to any further step — do not enumerate endpoints, do not start a run, do not attempt any scenario. This check must happen before any scenario executes, not after.

If `$ARGUMENTS` has no target URL at all, ask the user for one rather than guessing a default — do not assume `http://localhost:<some port>` on their behalf.

### 3. Confirm the target is actually up, then enumerate endpoints

Tell the user this capability requires an already-running local AppHost (`dotnet run --project src/eShop.AppHost`) — this skill does not start it. Enumerate reachable service endpoints by querying the Aspire dashboard at `<target-url>` (or, if the dashboard API isn't conveniently queryable, cross-reference the known service topology in `src/eShop.AppHost/Program.cs`: `basket-api`, `catalog-api`, `ordering-api`, `identity-api`, `webhooks-api`, `order-processor`, `payment-processor`, `webapp`, `webhooksclient`, `mobile-bff`) and confirm each one actually responds before including it in scope.

### 4. Start a run

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  start-run --capabilities adversarial --scope full --trigger manual
```

Capture `RUN_ID`.

### 5. Generate and execute scenarios (judgment call — this is the Agent-invocation step)

Use the `Agent` tool to attempt a range of malformed, boundary, and deliberately-misusing interactions against the enumerated endpoints — e.g., malformed JSON bodies, boundary-value quantities/prices, cross-buyer data access attempts (accessing another buyer's basket/order by guessing/incrementing an ID), sequence misuse (skipping steps in a checkout flow), and resource-exhaustion probes. Per spec.md Assumptions, state-changing and intentionally-malicious actions are permitted here (this is the one capability allowed to do that) — but only against this loopback target, never anything else.

**For every single scenario attempted — whether or not it produced an issue —** record it:

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  add-scenario --run-id "$RUN_ID" \
  --description "<what was attempted>" --target-service "<service>" \
  --outcome no-issue
```

If a scenario reveals a crash, unhandled error, authorization bypass, or data-integrity problem: first persist it as a Finding, then record the scenario with `--outcome finding`:

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  upsert-finding --run-id "$RUN_ID" --source adversarial \
  --title "<title>" --description "<what happened>" --severity "<critical|high|medium|low>" \
  --evidence "<exact sequence of requests/actions needed to reproduce this>"
# capture the returned finding id as FINDING_ID, then:
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  add-scenario --run-id "$RUN_ID" \
  --description "<what was attempted>" --target-service "<service>" \
  --outcome finding --finding-id "$FINDING_ID"
```

**Evidence must be reproducible** (Acceptance Scenario 2, User Story 3) — the exact request sequence, not a vague description.

### 6. Handle a crash mid-run (Edge Case §4)

If a previously-reachable service stops responding partway through — a crash — do not try to keep going as if nothing happened:

1. Persist the crash itself as a `critical` Finding (as in step 5), with evidence describing the exact scenario that preceded it.
2. Mark the run as failed:

   ```bash
   .specify/scripts/bash/security-findings-store.sh \
     --findings-dir specs/008-adversarial-security-review/findings \
     mark-failed --run-id "$RUN_ID"
   ```
3. Skip step 7's `--full true` finalize (see below) — a run that didn't complete has no basis to claim it reconfirmed (or safely auto-resolve) every prior finding.
4. Everything already recorded via `add-scenario`/`upsert-finding` before the crash is already persisted — do not discard it.

### 7. Finalize and report

If the run completed normally (no crash):

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  finalize-run --run-id "$RUN_ID" --full true
```

If it crashed (step 6), skip this finalize call entirely — the run's `failedPartway: true` flag from `mark-failed` is the correct terminal state; don't also try to resolve/full-finalize it.

```bash
.specify/scripts/bash/security-report-render.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  --out specs/008-adversarial-security-review/findings/report.md

.specify/scripts/bash/security-report-render.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  --capability adversarial --snapshot-date "$(date -u +%Y%m%d)" \
  --out "specs/008-adversarial-security-review/findings/$(date -u +%Y%m%d)-adversarial-review.md"
```

The dated file is a git-tracked, point-in-time snapshot of just this capability's findings and attempted scenarios for today (re-running later the same day overwrites today's file, a new day gets a new file); `report.md` remains the always-current cross-capability view. Write the dated snapshot even for a crashed/`failedPartway` run — it's still real, valuable signal.

Show the user the `## Adversarial Review` section. If zero findings, the report will list every scenario attempted (Acceptance Scenario 4) — show that, don't just say "nothing found."

### 8. Independence check (FR-010)

If asked to demonstrate FR-010, confirm this capability produces a complete, correct report using only `findings.json`/`runs.json` entries with `source`/`capabilities` of `adversarial` — no dependency on `code` or `dependency` findings existing.

## User Input

```text
$ARGUMENTS
```
