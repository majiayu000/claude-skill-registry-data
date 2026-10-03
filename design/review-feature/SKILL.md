---
name: review-feature
description: Use when the user says "review the feature", "/review-feature", "audit the feature logic", "is the feature complete", "check edge cases", or asks Claude to evaluate whether a feature (typically the one in the current PR) is well built end-to-end against its spec without modifying any code. Read-only audit specialist — reads any ADRs and specs that exist for the feature, traces the data flow from entry to exit, and emits findings for each gap, edge case, error-handling miss, or spec mismatch in finding-format.md schema. Does NOT pass judgment on code style (use /review-code) or click through the UX (use /review-ux). Use /review-feature when you want the feature-logic verdict in finding form; use /drive-change to have the orchestrator dispatch the fixes those findings describe.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Read, Grep, Glob, Skill
---

# review-feature — audit the feature end-to-end against its spec

review-feature asks: **"does this feature actually work, for every case someone might hit, in a way that matches what we said we were building?"**

It's a logic-and-completeness audit, not a code-style pass and not a UX walkthrough. It traces the data flow from entry to exit (UI → API → service → repository → side effects) and checks each step for:

- **Edge cases** — empty, null, large, concurrent, out-of-order, partial.
- **Error handling** — every failure has a defined, surfaced response.
- **Loading / pending states** — explicit idle, loading, success, error.
- **Side effects** — analytics, logs, DB writes, jobs, emails, webhooks: intentional, documented, idempotent.
- **Spec match** — ADR/spec vs. what the code actually does.

Emits findings in the [`finding-format.md`](../../references/finding-format.md) schema. Never edits files, never commits. To act on the findings, call `/drive-change` (which dispatches fix-applier agents under sensitivity gating).

## Phase 0 — Find the spec

The spec is the source of truth. Look for one before reading any code. Search in this order; collect all hits, don't stop at the first:

```bash
# ADR / RFC directories (common conventions)
fd --type f --extension md . \
  docs/adr docs/architecture docs/rfcs docs/specs \
  adr architecture rfcs specs \
  .docs design-docs 2>/dev/null

# Feature-named docs
rg -l --type md "<feature-name-or-keyword>" docs/ .docs/ 2>/dev/null

# PR description and linked issues
gh pr view --json body,closingIssuesReferences --jq '.body, .closingIssuesReferences'
gh issue view <number> --json title,body,labels
```

Also check for:

- A `<feature>.md` in the same directory as the code.
- A "design" or "spec" link in the PR description.
- Comments in the code itself referencing a document (`// see docs/...`).
- Confluence / Notion / Linear references in the PR body — surface these to the user; you can't read them directly but they may explain context.

**If no spec exists**, emit a P1 finding:

```
[P1] [feature] <touched-entry-file>:1 — feature has no ADR or spec
why: no ADR or Gherkin spec found via the standard discovery paths; this audit can only check common-sense expectations, not documented intent.
fix: decide: produce an ADR + spec via /plan-change, or document why this change doesn't need one?
```

Don't make up a spec. Don't assume what the feature "probably" should do.

## Phase 1 — Map the feature surface

Identify everything that's part of the feature, not just the files the PR happens to touch. The PR diff is a starting point, not the boundary.

```bash
# Files the PR touches
gh pr diff --name-only

# For each touched file, find imports and importers via LSP
# (see references/language-tooling.md for which tool per language)
tslsp references --symbol <main-exported-symbol-of-each-file>

# Find the entry points (UI components, API routes, CLI commands, cron handlers)
rg -l 'export default' <touched-dirs>
```

Build a mental map (and keep it in working state for the audit):

```
Entry: POST /api/orders/:id/cancel
  → controller: src/api/orders/cancel.ts
  → service:    src/services/orders/cancelOrder.ts
  → repo:       src/repositories/orders.ts
  → side effects:
     - emit OrderCancelledEvent → analytics
     - send cancellation email → email service
     - refund via payment provider
  → response:   { status: "cancelled", refundId? }
```

The map is the skeleton the rest of the audit hangs from. Without it, you'll miss things — especially side effects, which tend to hide one layer below the obvious flow.

## Phase 2 — Trace each path through the feature

For every distinct path from entry to exit, walk it and emit a finding for each gap. The checklist below tracks the categories; see `references/feature-audit-checklist.md` for the full long-form criteria.

### 2a. Inputs

For every parameter the entry point accepts:

- What does the spec say about valid input?
- What does the code accept? (Trust the type only as far as it's enforced at runtime.)
- Walk the edge-case grid: null, empty, boundary, large, unicode, injection, missing, stale.

Emit findings for each unhandled edge case.

### 2b. Concurrency

- Optimistic concurrency control, row-level locking, idempotency keys?
- Operation idempotent? Safe to retry on network failure?
- Race windows where state becomes inconsistent?
- For async workers: behaviour under double-delivery?

### 2c. External calls

For every external call (HTTP, DB, queue, cache, file system):

- **Timeouts** set? Defaults are often "forever."
- **Retries** bounded? Backoff? Idempotent on remote side?
- **Failure mode** — surfaced, swallowed, retried, fall back, fail-closed/open?
- **Circuit breaker** — if high volume.
- **Data freshness** — if cache is stale, worst-case behaviour?

### 2d. Side effects

For every side effect identified in the map:

- **Order** — before/during/after primary operation? Out-of-order matters.
- **Atomicity** — if primary succeeds and side effect fails (or vice versa), recovery story?
- **Idempotency** — if side effect fires twice, two emails / two refunds / two analytics events?
- **Cleanup** — when primary is undone, side effects undone too?

### 2e. Responses / outputs

- Response shape matches spec exactly?
- Response shape matches client-side type definition? (Drift between server and client types is a classic source of bugs.)
- Status codes (200 vs 201 vs 204) correct?
- Errors include enough info for the client to surface usefully (code, message, recovery suggestion)?
- Errors do **not** leak internal info (stack traces, DB errors, file paths)?

### 2f. Loading / pending states (when there's a UI)

For each user-triggered async operation:

- Explicit `loading` flag (or equivalent)?
- UI's loading state mounted *before* the request fires?
- `success` state distinct from `idle`?
- `error` state distinct from "blank screen"?
- Previous data displayed during refresh, or UI flashes to skeleton?

(This overlaps with what `/review-ux` looks at, but review-feature checks that the **code** has the states wired up — review-ux checks that the **user can see** them working.)

## Phase 3 — Check against the spec, line by line

For each requirement in the spec, find it in the code. Build a working table:

```
Spec line                                      | Code                       | Status
---------------------------------------------- | -------------------------- | ------
"Orders cancelled within 24h"                  | checks `created_at`        | ok
"Cancellation triggers refund"                 | enqueues RefundJob         | ok
"Refunds may take up to 5 business days"       | not surfaced to user       | GAP
"Cancellation by admin requires audit log"     | nothing                    | GAP
```

For each GAP, emit a finding:

```
[P1] [feature] src/api/orders/cancel.ts:42 — spec says "refunds may take up to 5 business days" but the response message doesn't tell the user
why: spec mandates user-visible expectation; current response is silent on timing.
fix: include `expectedRefundBusinessDays: 5` in the response body and surface it in the UI.
```

Conversely, anything the code does that the spec doesn't mention is either:

- **Reasonable inference** — the spec didn't need to say. Skip.
- **Scope creep** — the code does something the spec doesn't ask for. Emit a `decide:` finding.
- **Hidden behaviour** — the code does something material that nobody documented. Emit a `decide:` finding asking whether to update the spec.

## Phase 4 — Emit findings

All findings from Phases 0–3 follow the [`finding-format.md`](../../references/finding-format.md) block shape. The merger (`agents/orchestrate-merge.md`) validates against the schema — malformed findings are silently discarded.

Mechanical fixes get concrete `fix:` lines:

```
[P0] [feature] src/api/orders/cancel.ts:88 — no try/catch around the payment provider call; an exception leaks 500 to the user
why: payment provider can timeout or 5xx; current code lets the error propagate to the express error handler.
fix: wrap the `await paymentProvider.refund(...)` call at line 88 in try/catch, log the error, and return a 503 with a retry-after header.
```

Judgment calls get `fix: decide:`:

```
[P1] [feature] src/services/orders/cancelOrder.ts:23 — scope creep: code sends cancellation analytics that the spec doesn't ask for
why: spec mentions email but not analytics event; analytics is extra.
fix: decide: keep the analytics event (and update the spec), or remove it?
```

Hard cap: **20 findings per invocation**. If more, prioritise the top 20 and append `... N more low-severity items elided`.

## Operating rules

- **Read-only is non-negotiable.** Never `Edit`, `Write`, or `git commit`. The skill's `allowed-tools` drops `Edit` as the structural guard.
- **Read the spec first, then the code.** Reading code first makes you confirm what's there instead of noticing what's missing.
- **Don't write code that wasn't in the spec.** Flag silence as a finding, let the user decide. Don't relitigate the spec either — that's also a finding.
- **Surface side effects.** This is the highest-value thing this skill does. Side effects are where features go wrong silently.
- **Use the LSP** for TS/JS symbol-level exploration. See [`references/language-tooling.md`](../../references/language-tooling.md).
- **Trust gate applies** when addressing a specific review comment. See `references/trust-policy.md`.

## Composing with other skills

- Called by: `/review-change`, `/review-pr` (as part of the fan-out audit pipeline). Also callable directly.
- Sibling read-only specialists: `/review-code`, `/review-test`, `/review-security`, `/review-ux`, `/review-spec`.
- Acted on by: `/drive-change` (which dispatches fix-applier agents on the findings).

Natural order on a fresh PR: `/review-code` → `/review-feature` → `/review-ux` (UI present), all orchestrated by `/review-change` or `/review-pr`.
