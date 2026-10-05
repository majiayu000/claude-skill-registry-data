---
name: business-logic-abuse
description: Identify business-logic vulnerabilities that bypass intended workflows including race conditions, TOCTOU, double-spending, workflow-state bypass.
---

# Business-Logic Abuse

Business-logic vulnerabilities break the application's own rules: balances go negative, workflows skip required steps, requests replay inside an allowed window, two parallel operations both succeed when only one should. Generic scanners miss these because they depend on domain knowledge - what "valid" means for this app. This skill guides a domain-aware audit that elicits the rules from the operator, traces each rule through the code, and flags the atomicity, idempotency, and sequencing gaps where abuse lives.

## When to Use This Skill

Use this skill when:

- Auditing financial workflows (payments, refunds, ledgers, credit grants, promotional codes)
- Reviewing reservation or inventory systems (seats, slots, stock, quotas)
- Assessing privilege grants and role transitions (invitations, upgrades, approvals)
- Evaluating multi-step workflows where each step has preconditions
- Running `/run-penetration-test --depth=deep` (this skill powers the Business Logic & Advanced Attacks hunter)
- Investigating a specific incident that looks like "the system did something it should not have allowed"

Do NOT use this skill for:
- Generic vulnerability classes (XSS, SQL injection) - use `security-review` or `/run-penetration-test` standard depth.
- Stateless endpoint bugs - use `semantic-bug-detector` or unit-test coverage instead.

**Trigger phrases**: "business logic", "race condition", "TOCTOU", "time of check time of use", "double spend", "idempotency", "workflow bypass", "state machine bug", "check then act", "workflow state", "ledger integrity", "WSTG-BUSL".

## What This Skill Does

Provides a domain-aware audit procedure for business-logic flaws including:

- **Rule Elicitation**: A structured interview that surfaces high-value workflows, critical invariants, and idempotency guarantees from the operator.
- **Attack Class Coverage**: Six canonical attack classes (race conditions, TOCTOU, double-spending, workflow bypass, idempotency violations, check-sequence abuse) with indicators, example code patterns, and remediation guidance.
- **Code-Trace Procedure**: For each elicited rule, a walkthrough that maps the rule onto atomicity boundaries, state-machine transitions, and persistence guarantees.
- **Structured Output**: A findings table schema (severity, rule violated, code reference, reproduction sketch, remediation) consumable by `/run-penetration-test` reports and security reviews.

## Instructions

### Step 1: Scope and Caveat - Elicit the Rules

**You cannot audit what you do not know.** Business logic lives in the operator's head and in the product spec, not in the code. Before reading any code, ask the operator:

1. **High-value workflows**: "What are the 3-5 workflows where a bypass would cost real money, real privilege, or real trust?" Typical answers: payment capture, refund, reservation commit, role grant, promo-code redemption, withdrawal, transfer.
2. **Critical invariants**: "What statements should always be true regardless of load, concurrency, or retries?" Examples: "balance cannot go negative," "a seat is either available or held by exactly one user," "a refund cannot exceed the original charge," "a user has at most one active subscription."
3. **Idempotency guarantees**: "Which endpoints must produce the same visible result if called twice with the same inputs?" Typical: payment submission, order creation, webhook handlers.
4. **Trust boundaries**: "Which inputs come from the user vs an internal trusted source?" Prices and quantities submitted by a client are the classic vector for workflow bypass.
5. **State transitions**: "Walk me through the state machine of each high-value workflow - what are the states, and what transitions are allowed from each?"

If the operator cannot answer these, stop and request the product spec or domain owner. **This skill produces garbage on unspecified domains.** Do not guess the rules.

### Step 2: Race Conditions

**What it is**: Two requests arrive close enough in time that their combined effect breaks an invariant. Classic case: `SELECT balance; check balance >= amount; UPDATE balance - amount;` - two requests both pass the check, both succeed, balance goes negative.

**Indicators in code**:
- Read-modify-write patterns that are not wrapped in a transaction or atomic operation.
- `if (record.locked) { ... } else { record.lock(); ... }` without a database-level lock.
- Cache-then-database patterns where the cache is read first and writes do not invalidate atomically.
- Concurrent job processing that reads pending tasks without `FOR UPDATE SKIP LOCKED` or an equivalent.

**Code-trace procedure**:
1. For each invariant elicited in Step 1, locate every code path that reads or writes the state the invariant depends on.
2. For each path, identify the atomicity boundary: where does the transaction begin and end? Is the read inside the same transaction as the write? Is the write-side lock pessimistic (`FOR UPDATE`), optimistic (version column + retry), or absent?
3. Flag any boundary where two concurrent requests could both pass the check and both commit.

**Remediation**:
- Database-enforced atomicity: `SELECT ... FOR UPDATE`, unique constraints, conditional UPDATE (`WHERE balance >= amount`), optimistic concurrency with version columns.
- Application-level locks only when database locks are infeasible - and only with an external lock service (Redis Redlock, ZooKeeper) with correctly-handled lock expiry.
- Design out the race: single-writer job queues, event sourcing with per-aggregate ordering.

### Step 3: TOCTOU (Time-of-Check / Time-of-Use)

**What it is**: A resource or permission is checked at time T1 and used at time T2; between T1 and T2 the resource changes. Distinct from race conditions: TOCTOU often involves two different subjects (a file, a permission, an external resource) rather than two concurrent requests on the same row.

**Indicators in code**:
- `os.path.exists(p)` followed by `open(p)` - the file may be replaced with a symlink between the two calls.
- `if user.has_permission('admin'): ... do_admin_action()` where the permission check and the action are not in the same transaction or permission token.
- `check_not_banned(user); send_message(user);` - the ban happens between the two calls.
- External-resource availability checks (API health, disk space) followed by use.

**Remediation**:
- Fuse check and use into a single atomic operation (e.g., open-if-not-exists file modes; `INSERT ... ON CONFLICT`; permission-bearing capability tokens carried with the action).
- Replace check-then-use with use-and-handle: attempt the operation and handle failure, rather than pre-checking.

### Step 4: Double-Spending / Replay-Within-Window

**What it is**: The same financially-meaningful request succeeds twice because the server did not have an idempotency key or the key was not enforced. Includes coupon re-use, voucher re-redemption, gift-card double-charge, and transaction replay.

**Indicators in code**:
- Payment, refund, or ledger endpoints that do not accept or require an idempotency key.
- Idempotency keys that are accepted but not stored (only logged), or stored without a uniqueness constraint.
- Idempotency key TTLs shorter than the likely client retry window.
- Coupon / voucher codes that allow multiple redemptions because the "used" flag is set after the award is granted.

**Remediation**:
- Require idempotency keys on all state-changing financial endpoints (RFC-aligned: `Idempotency-Key` header).
- Store keys in a table with a UNIQUE constraint on `(key, endpoint, tenant)` and retain at least long enough to cover client retry windows (24h typical; longer for fintech).
- For single-use artifacts (vouchers, one-time codes), set the "used" flag atomically with the award - in the same transaction, gated by a UNIQUE constraint or a `WHERE used = false` predicate.

### Step 5: Workflow-State Bypass

**What it is**: The UI walks a user through steps A -> B -> C, but each step is a separate endpoint. A malicious client POSTs directly to C, skipping A and B. The server did not check that the prerequisite state was reached.

**Indicators in code**:
- Multi-step wizards where each step endpoint trusts the client to have completed prior steps.
- Direct endpoints like `/checkout/complete` or `/account/delete/confirm` that accept a request without verifying the state-machine position.
- State stored only in the client (hidden form fields, query params) without server-side corroboration.
- Conditional rendering in the UI treated as authorization ("the button is not shown" is not "the endpoint is guarded").

**Remediation**:
- Enforce the state machine server-side: every action endpoint consults the persisted state and rejects any transition not in the allowed-from-here set.
- Represent the state machine explicitly (enum or typed state) rather than scattered booleans (`is_verified`, `has_paid`, `is_confirmed`). A typed state makes missing transition guards visible.
- Treat the UI path as untrusted. The state machine is the single source of truth.

### Step 6: Idempotency Violations

**What it is**: The same request produces different observable results on different calls, when it should produce the same result. Distinct from double-spending: here the intent is idempotency (retry safety), and the violation is that retry is not safe.

**Indicators in code**:
- Endpoints that increment a counter or allocate an ID on every call without checking for an existing result.
- Webhook handlers without dedup on `(event_id, event_version)`.
- "Create-or-update" endpoints where the update branch fails silently and the create branch runs instead.
- Side effects (emails, external API calls) performed before the idempotency-key lookup.

**Remediation**:
- Idempotency keys as the canonical dedup mechanism; store the response payload so a retry returns the same body.
- Webhook handlers: dedup on `event_id` at the boundary, before any downstream effect.
- Order side effects after the durable state change: don't send an email until the transaction commits.

### Step 7: Check-Sequence Abuse

**What it is**: The server validates input X, then acts on input Y, where X and Y are related but the relationship is not enforced. Canonical example: upload endpoint validates the uploaded file's MIME type, then saves the file using the client-supplied filename - attacker uploads `image/png` but names the file `malicious.php`.

**Indicators in code**:
- Validation and action use different input fields or different representations of the same field.
- Validation performed on a copy, with the original re-used downstream.
- Normalization happens after validation (e.g., `validate(filename); save(Path(filename).resolve())` - the `resolve()` may produce a different path).
- Multi-step validation where step 2 re-reads the input from the request rather than using the validated value from step 1.

**Remediation**:
- Validate, normalize, and act on the *same* value. Pass the validated object forward; do not re-read from the request.
- For uploads: server generates the filename; the client-supplied name is never used for storage.
- For permissions: the authorization decision must bind to the subject-verb-object tuple that the downstream handler acts on.

### Step 8: Output Format

Produce findings as a table so the result is consumable by `/run-penetration-test` reports, security reviews, and downstream skills:

| Severity | Rule Violated | Attack Class | Code Reference | Reproduction Sketch | Remediation |
|----------|---------------|--------------|----------------|---------------------|-------------|
| CRITICAL | "Balance cannot go negative" | Race condition | `src/payments/debit.py:87-104` | Two concurrent POSTs to `/debit` with the same `account_id` and `amount=balance` | Wrap debit in `SELECT ... FOR UPDATE` or use conditional UPDATE `WHERE balance >= amount` |
| HIGH | "A reservation is held by exactly one user" | TOCTOU | `src/booking/hold.py:52-68` | Two users POST `/holds` for the same `slot_id` within 50ms | `INSERT ... ON CONFLICT DO NOTHING` on `(slot_id)` unique constraint; reject second insert |

Severity guidance:
- CRITICAL: invariant violation causes direct financial loss, privilege escalation to admin, or breach of multi-tenant isolation.
- HIGH: invariant violation causes data corruption or gives an attacker useful but non-terminal leverage.
- MEDIUM: invariant violation is reachable only under narrow conditions, or produces a user-visible anomaly without leverage.
- LOW: defense-in-depth gap; no realistic exploit path but the code path does not enforce the intended rule.

## Best Practices

- **Stop if the rules are not known.** Guessing invariants produces false positives and wastes trust.
- **Prefer database-enforced atomicity over application-level locking.** Databases handle crash recovery, replication, and expiry correctly; homegrown locks rarely do.
- **Represent state machines explicitly.** Scattered booleans (`is_paid`, `is_shipped`, `is_refunded`) hide missing transitions. A single `status` enum with typed transition rules makes gaps visible at review time.
- **Treat every client-supplied value as potentially hostile, even values the UI constrains.** Client constraints are not authorization.
- **Order side effects after durable state changes.** Email first, commit second is a double-send waiting to happen.
- **When multiple attack classes apply to the same endpoint, fix the deepest one first.** A fix that removes the race condition often removes the TOCTOU for free; the reverse is rarely true.

## Common Patterns

### Pattern 1: Conditional UPDATE for single-writer semantics

```sql
-- Correct: debit succeeds only if funds are available; returns affected row count
UPDATE accounts
SET balance = balance - :amount
WHERE account_id = :id AND balance >= :amount
RETURNING balance;
-- If row count = 0, debit was rejected atomically.
```

### Pattern 2: Idempotency key with uniqueness constraint

```sql
-- Idempotency key table
CREATE TABLE idempotency_keys (
    key TEXT,
    endpoint TEXT,
    tenant_id UUID,
    response_body JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (key, endpoint, tenant_id)
);
-- On second request: SELECT returns the stored response_body; no-op the side effects.
```

### Pattern 3: Server-enforced state machine

```python
# Explicit typed state with transition guards
class OrderStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

ALLOWED_TRANSITIONS = {
    OrderStatus.DRAFT: {OrderStatus.PENDING, OrderStatus.CANCELLED},
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}

def transition(order: Order, to: OrderStatus) -> None:
    if to not in ALLOWED_TRANSITIONS[order.status]:
        raise WorkflowBypassError(f"{order.status} -> {to} not allowed")
    order.status = to
```

## Quality Checklist

- [ ] Every high-value workflow was elicited from the operator (not guessed from code alone)
- [ ] Every invariant has a named rule and a code reference
- [ ] Every finding names the attack class (race / TOCTOU / double-spend / workflow bypass / idempotency / check-sequence)
- [ ] Each finding includes a reproduction sketch a tester could execute
- [ ] Remediation is architectural (database constraint, state machine, idempotency key) rather than ad-hoc (extra `if` check)
- [ ] Severity reflects real exploitability, not just theoretical class

## Verification

- [ ] For each CRITICAL finding, write or request a reproduction test that fails before the fix and passes after
- [ ] Confirm database-level constraints (UNIQUE, CHECK, `FOR UPDATE`) are in place, not just application-level code
- [ ] For race-condition fixes: load-test the fixed code with N >= 10 concurrent requests; confirm the invariant holds
- [ ] For workflow-bypass fixes: attempt to POST directly to the downstream endpoint from a state where it should be rejected; confirm rejection
- [ ] For idempotency fixes: replay the same request twice; confirm identical observable result

## Related Skills

- `security-patch-advisor` - Patch generation for the remediation code
- `security-review` - General application security review (this skill extends it with domain-specific checks)
- `authentication-patterns` - Auth-specific invariants (one active session per user, MFA enrollment sequencing)
- `fintech-engineer` - Domain knowledge for financial ledger invariants
- `semantic-bug-detector` - Logic bugs beyond security (overlaps with this skill on race conditions)

---

**Version**: 1.0.0
**Last Updated**: April 2026

### Iterative Refinement Strategy

This skill is optimized for an iterative approach:
1. **Execute**: Elicit rules, audit each attack class, produce the findings table.
2. **Review**: Critically analyze each finding (exploitability, severity accuracy, remediation depth).
3. **Refine**: Downgrade theoretical findings; upgrade any you previously missed from under-elicited rules.
4. **Loop**: Continue until every elicited invariant has either a clean bill of health or a finding with a reproduction sketch.
