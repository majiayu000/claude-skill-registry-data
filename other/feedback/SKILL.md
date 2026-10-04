---
name: feedback
description: Use when implementation, review, security, scalability, or incident work reveals that an upstream .forge/ artifact is wrong, when a contract is missing an operation, when an ADR is being contradicted by a current need, when security recommends architecture changes, or when the user says "we discovered the spec is wrong".
---

# Feedback (reverse cascade)

## Overview

Capture a finding from any downstream stage into a structured `.forge/feedback/<timestamp>-<source>.md` entry that targets one upstream artifact. The entry stays as `status: PENDING` until the upstream skill re-runs and addresses it. `forge-sync` flags the target artifact as **FEEDBACK_PENDING** until the entry is resolved.

This is the only sanctioned reverse-cascade primitive. The forward chain (`prd → arch → tasks → code`) flows one direction; backward propagation happens through these entries, not by directly editing upstream artifacts mid-stream.

## When to Use

- During `/build` you discover the relevant contract is missing an operation or has the wrong shape
- During `/review` you find an architectural flaw that wasn't visible at design time
- During `/secure` or `/scale` you produce a recommendation that implies architecture changes (add a WAF, change a data store, add a gateway)
- During an incident you discover an error path the error-handling spec didn't cover
- After a sprint, you realize ≥3 tasks split mid-flight — the plan needs an update before the next sprint

## When NOT to Use

- The fix is fully contained inside the current stage (don't escalate every implementation detail)
- You have permission to edit the upstream artifact directly and want to do so — then just edit it; `forge-sync` will flag downstream as STALE
- The finding is a question, not a recommended change — discuss with the user first; file the entry once a recommendation crystallizes
- The target artifact doesn't exist (`.forge/security.md` not yet generated) — run the source skill instead

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll just edit the contract inline" | Then the chain has no record of WHY it changed. Future readers see a contract that contradicts the PRD with no explanation. |
| "Filing a feedback entry is overhead — I'll fix it later" | "Later" means the finding is forgotten by the time the upstream skill re-runs. The entry is the memory. |
| "The upstream skill will figure it out when it re-runs" | The upstream skill regenerates from its inputs, not from the downstream's discovery. Without a feedback entry, the regenerated artifact has the same flaw. |
| "This is too small for a feedback entry" | Three small findings ignored = one big surprise at /ship. |
| "I'll just tell the user verbally" | Verbal findings evaporate. The entry survives session boundaries. |

## Red Flags

- Editing `.forge/contracts/<X>.md` directly during `/build` instead of filing a feedback entry
- A sprint ends with no `.forge/feedback/` entries despite ≥3 tasks having `notes` populated
- `forge-sync` reports `FEEDBACK_PENDING` on artifacts that are about to be re-generated, but the regenerating skill doesn't read `.forge/feedback/`
- A `.forge/feedback/*.md` file exists with `status: PENDING` for more than two sprints — either resolve it or mark it `DEFERRED` with a reason

## Core Process

### Step 1: Identify source, target, and finding

- **Source stage:** which skill or activity discovered the issue (`build`, `review`, `secure`, `scale`, `incident`, `manual`)
- **Source context:** task ID, commit, PR, incident ID, or "manual" if ad-hoc
- **Target artifact:** which `.forge/` file needs revision. Must exist on disk. If multiple files need revision, file separate entries.
- **Finding:** what was discovered (1-3 sentences, specific)
- **Recommended change:** what should change in the target artifact (specific enough that re-running the source skill can apply it)

### Step 2: Decide severity

Choose one:
- **NEEDS_REVIEW** — finding requires a human decision; auto-cascade not safe (e.g., "add WAF" — the human decides whether to absorb the change in architecture or defer)
- **FEEDBACK_PENDING** — recommended change is mechanical; the upstream skill can apply it on re-run (e.g., "add `refund` endpoint to PaymentService contract")

Both states block `/ship`. Only `NEEDS_REVIEW` blocks `/build` if it touches the in-flight task's contract.

### Step 3: Write the entry

Path: `.forge/feedback/<ISO8601-UTC-with-dashes>-<source>.md` — e.g., `.forge/feedback/2026-05-14T103000Z-build.md`.

```markdown
<!-- forge:meta
generated_by: feedback
generated_at: 2026-05-14T10:30:00Z
depends_on: [.forge/contracts/payment-service.md]
generated_from:
  .forge/contracts/payment-service.md: <target's content_hash AT filing time>
content_hash: <first 8 chars of sha256 over this entry's body>
-->

# Feedback: <short title>

- **Source stage:** build (incremental-implementation, task T-042)
- **Source context:** commit pending; branch task/T-042-refund-flow
- **Target artifact:** .forge/contracts/payment-service.md
- **Severity:** FEEDBACK_PENDING
- **Status:** PENDING
- **Filed at:** 2026-05-14T10:30:00Z
- **Resolved at:** —

## Finding

While implementing the refund flow, the PaymentService contract has no `refund(transactionId, amount)` operation. The PRD's "User can refund failed transactions within 30 days" story can't be satisfied without it.

## Recommended change

Add to `Provides` in `.forge/contracts/payment-service.md`:

  refund(input: RefundInput): RefundOutput | RefundError

with:
- `RefundInput = { transactionId: string, amount?: number, idempotencyKey: string }`
- `RefundOutput = { refundId, refundedAt, amount }`
- `RefundError` cases: `TransactionNotFound`, `RefundWindowExpired`, `AlreadyRefunded`, `PartialRefundNotAllowed`

Idempotency-Key required per `api-design.md` mutation policy.

## Cascade

- Re-run `/architect` (or edit the contract directly) to address this entry.
- After contract update, re-run `/plan` if the refund story needs new tasks beyond T-042.
- `forge-sync` will mark this entry `RESOLVED` once the target artifact's `generated_at` advances past this entry's `generated_at` AND the recommended operation appears in the target.
```

`depends_on` is the target_artifact (single-element list) — that's what `forge-sync` reads to identify what's being annotated.

### Step 4: Confirm with user

Print the entry path and a one-line summary:

> Filed `.forge/feedback/2026-05-14T103000Z-build.md` — target `.forge/contracts/payment-service.md`, severity FEEDBACK_PENDING. Run `/sync` to see chain impact.

Do not modify the target artifact in this skill. The skill is write-only into `.forge/feedback/`.

### Step 5: Tracking resolution

The feedback skill itself does not resolve entries. Resolution happens when the targeted upstream skill re-runs:

1. The upstream skill (e.g., `architecture-and-contracts`) reads all `.forge/feedback/*.md` entries where `target_artifact` matches an output it owns AND `status: PENDING`.
2. It addresses each in its regeneration.
3. After writing, it updates each addressed entry: `status: RESOLVED`, `resolved_at: <now UTC>`, `resolved_by: <commit or "manual">`.
4. `forge-sync` confirms the resolution by checking that the target artifact's content reflects the recommended change.

Entries can also be marked `DEFERRED` (with a reason in the body) when the team decides not to act — the entry stays in the directory as historical record.

## Verification

- [ ] `.forge/feedback/<timestamp>-<source>.md` written
- [ ] Filename timestamp is UTC with Z; format `YYYY-MM-DDTHHMMSSZ-<source>.md`
- [ ] `forge:meta` header has `depends_on: [<single target artifact path>]`
- [ ] Severity is one of `FEEDBACK_PENDING` or `NEEDS_REVIEW`
- [ ] Status is `PENDING` at filing time
- [ ] Recommended change is specific (operation name, type names, error cases — not "make it better")
- [ ] Cascade section names which upstream skill should re-run
- [ ] No upstream artifact was directly edited by this skill
