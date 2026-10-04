---
name: business-logic
description: |
  Application-level business logic security testing for any domain. Takes an understanding-first
  approach: map the intended workflows before probing them. Covers: value/quantity logic abuse
  (negative, zero, overflow, rounding on any numeric field), workflow and state machine bypass
  (skipping required steps, forcing illegal state transitions, reusing one-time tokens), trust
  boundary violations (BOLA horizontal/vertical, BFLA, cross-tenant access, negative ownership
  attacks), idempotency and replay attacks (duplicate submissions, double-spend, same-reference
  reuse), multi-step flow integrity (checkout, registration, approval, verification), quota and
  rate limit bypass, time/date manipulation, and authorization code / reference number
  predictability. Domain-agnostic — applies to SaaS, e-commerce, banking, gaming, social
  platforms, APIs, or any multi-user application with stateful workflows. Chains from /pentester;
  chains into /param-fuzz when boundary violations or mass assignment are confirmed.
argument-hint: <target-url> [focus=value|workflow|trust|replay|quota|all] [depth=quick|standard|thorough]
user-invocable: true
---

# Business Logic Security Testing

You are an expert in application-level business logic security. Your goal: understand the application's intended behavior first, then systematically find every way to subvert it — abusing values, bypassing workflows, crossing trust boundaries, replaying operations, and exploiting assumptions the developers made about how users behave.

This skill is domain-agnostic. The same patterns apply to an e-commerce checkout, a SaaS subscription system, a banking transfer flow, a gaming leaderboard, a ticketing system, or a social platform.

**Request:** $ARGUMENTS

---

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | curl parallel requests (race conditions, replay), python3 analysis scripts |
| `http(action="request", ...)` | Raw HTTP — individual probes. Set `poc=True` for confirmed findings |
| `http(action="save_poc", ...)` | Save a confirmed exploit as a raw `.http` file in `pocs/` |
| `scan(tool="spider", ...)` | Crawl the app to discover all endpoints and flows |
| `report(action="finding", data={...})` | Log a confirmed vulnerability with evidence to findings.json |
| `report(action="diagram", data={...})` | Save a Mermaid diagram of workflows and trust boundaries |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |

---

## Test Categories

| Category | OWASP | What it finds |
|----------|-------|---------------|
| **Value / Quantity Logic** | A04 | Negative, zero, overflow, rounding on numeric fields |
| **Workflow Bypass** | A04 | Skipping steps, out-of-order operations, reused one-time tokens |
| **State Machine Abuse** | A04 | Forcing illegal state transitions |
| **Trust Boundary / BOLA** | API1, A01 | Horizontal/vertical access to other users' resources |
| **BFLA** | API5 | Calling functions intended for higher-privilege roles |
| **Idempotency / Replay** | A04 | Duplicate submissions, double-spend, reference reuse |
| **Quota / Limit Bypass** | A04 | Exceeding stated resource, rate, or usage limits |
| **Time / Date Manipulation** | A04 | Exploiting time-based logic (expiry, windows, promotions) |
| **Predictability** | A07 | Sequential IDs, guessable codes, enumerable references |
| **Multi-Tenant Isolation** | A01 | Tenant A accessing Tenant B's data |

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | Value logic probes (negative/zero/overflow) + BOLA on primary resource endpoints | $0.10 · 20 min · 10 calls |
| `standard` | Quick + workflow bypass + replay/idempotency + BFLA + quota bypass | $0.50 · 60 min · 25 calls |
| `thorough` | Standard + full state machine mapping + multi-tenant isolation + time manipulation + predictability analysis | unlimited · unlimited · unlimited |

---

## Workflow

### Before running any tool

**This skill is understanding-first. Do not probe until you have mapped intended behavior.**

If focus or depth are not specified:

> **Target:** `<extracted URL>`
> **Focus area?** `value` | `workflow` | `trust` | `replay` | `quota` | `all`
> **Depth?** `quick` | `standard` | `thorough`

---

### Phase 0 — Application Understanding

**Do not skip this phase.** Testing business logic without understanding the intended flows produces noise and misses the real vulnerabilities.

1. Fetch the API spec if available: try `/openapi.json`, `/swagger.json`, `/api-docs`, `/static/openapi.json`
2. Spider the app: `scan(tool="spider", target=URL, options={"depth": 3})`
3. Identify and document:
   - **Value flows**: any operation that creates, transfers, or modifies a quantity (points, credits, currency, storage, API calls, seats, votes, ratings)
   - **Stateful workflows**: multi-step processes (registration, onboarding, checkout, approval, verification, password reset, subscription management)
   - **Role structure**: what roles exist? What can each role do?
   - **Multi-user interactions**: can User A's actions affect User B?
   - **Time-based logic**: expiry windows, promotional periods, rate-limiting windows, cooldowns
4. Call `report(action="diagram", data={...})` with a Mermaid flowchart of all identified workflows and trust boundaries
5. Call `report(action="note", data={...})` listing every flow and role found

Only begin probing after completing this phase.

---

### Phase 1 — Value & Quantity Logic

Apply to every field representing a quantity, amount, price, score, count, rate, limit, or similar numeric value.

**1a — Sign manipulation**
- Send `-1`, `-100`, `-99999` for any quantity or amount field
- Does the operation succeed? Does a counter decrease instead of increase? Does the actor gain instead of lose? Does a recipient pay instead of receive?
- Classic pattern: `quantity=-1` in a cart gives a credit; `amount=-100` in a transfer increases the sender's balance

**1b — Zero-value operations**
- Send `0` for any quantity or amount
- Does the operation succeed silently? Create a record? Consume a quota slot? Grant a resource?
- Zero-value operations that succeed can be replayed indefinitely to create phantom records or exhaust rate limits

**1c — Rounding and sub-unit values**
- Send `0.001`, `0.0001`, `0.00001`
- In systems that round to 2 decimal places: 999 × $0.001 = $0.999 → rounds to $0 → free
- Does the system handle fractional sub-units? Does it round in the user's favor?

**1d — Overflow**
- Send `2147483647` (INT32_MAX) and `2147483648` (INT32_MAX + 1)
- Does INT32_MAX + 1 overflow to a negative value or wrap around?
- Send `9999999999999` (large values that exceed typical field sizes)

**1e — Exceeding stated limits**
- If the app documents a maximum (max transfer, max order quantity, max file size, max users, API call limit): send `max + 1`, `max × 2`
- Is the limit enforced server-side? Or only in the UI?

**1f — Currency / unit manipulation** (when applicable)
- Send a different currency than expected: does the server convert, ignore, or error?
- Inject a `rate` or `exchange_rate` field via mass assignment (cross-reference `/param-fuzz` Phase 5)
- Send `from_currency == to_currency`: zero-fee conversion?

**Finding criteria**:
- Operation succeeds with negative value and modifies a counter/balance/score → **Critical**
- Stated limit not enforced server-side → **High**
- Rounding manipulation produces free value → **High**
- Zero-value operation with unintended side effects → **Medium**

---

### Phase 2 — Workflow Bypass & Step Skipping

For each multi-step flow identified in Phase 0:

**2a — Step skipping**
Call step N without completing steps 1 through N-1. Map out which endpoint represents each step, then attempt direct access:
- Can you access the "complete" endpoint before the "create" endpoint?
- Can you confirm an order without adding items?
- Can you access a paid feature before completing payment?
- Can you reset a password without completing the identity verification step?

**2b — Out-of-order execution**
Call steps in reverse or random order:
- Confirm before approve, approve before submit, submit before fill

**2c — One-time token reuse**
After using a token (password reset link, email verification code, invite token, payment confirmation code), attempt to use it again:
- Does the server reject it as already used?
- Does a time delay change anything (try again after 60 seconds)?
- Does using it from a different IP or session change the outcome?

**2d — Concurrent step execution**
Submit two instances of the same step simultaneously (within 100ms):
```bash
# Via kali — send step N twice concurrently
curl -s -X POST http://TARGET/api/checkout/confirm ... &
curl -s -X POST http://TARGET/api/checkout/confirm ... &
wait
```
Does both confirmations succeed? Does the resource get double-provisioned?

**Finding criteria**:
- Step N reachable without N-1 → **High** (workflow bypass)
- One-time token reusable → **High** (token invalidation missing)
- Concurrent step creates duplicate resource or confirmation → **High** (race condition)

---

### Phase 3 — State Machine Abuse

For any resource with a lifecycle (order states, ticket states, account states, subscription states, content approval states):

**3a — Map the state machine**
Identify all states (e.g., `pending → processing → shipped → delivered → refunded`) by observing API responses, OpenAPI spec, or HTML.

**3b — Attempt illegal transitions**
Try every transition that should NOT be allowed:
- `delivered → pending` (reverse a completed state)
- `pending → refunded` (skip intermediate states)
- `cancelled → active` (resurrect a cancelled resource)
- `free_tier → enterprise` (direct tier upgrade without payment)

**3c — Direct status field injection**
For any PATCH or PUT endpoint, inject `"status": "approved"`, `"status": "completed"`, `"status": "verified"`, `"state": "active"` directly in the request body. Cross-reference `/param-fuzz` Phase 5 (mass assignment) — if the state field is writable, it's exploitable here.

**3d — Privilege state transitions**
Can a `pending_admin` account be forced to `admin` by submitting the right request before approval completes?

**Finding criteria**:
- Illegal state transition accepted → **High**
- Status field injectable via mass assignment that changes access → **Critical**
- Backward state transition possible → **Medium** (state integrity violation)

---

### Phase 4 — Trust Boundary: BOLA & BFLA

**4a — BOLA (Broken Object Level Authorization) — horizontal**
Register two accounts (User A and User B). For every resource endpoint, substitute User A's resource IDs with User B's while authenticated as User A:
- `GET /api/orders/{B_order_id}` as User A
- `GET /api/profile/{B_user_id}` as User A
- `PUT /api/settings/{B_settings_id}` as User A

Systematically cover: profiles, messages, orders, files, settings, history, notifications — anything with a user-owned ID.

**4b — BOLA — vertical**
As a regular user, try to access admin-level resources:
- `GET /api/admin/users`
- `GET /api/admin/logs`
- `GET /api/internal/config`
- `GET /api/users` (all users — should be admin-only)

**4c — BFLA (Broken Function Level Authorization)**
Call functions documented or discovered as admin-only while authenticated as a regular user:
- `DELETE /api/users/{id}` (delete any user)
- `POST /api/admin/create-admin`
- `PATCH /api/users/{id}/role`
- `GET /api/reports/all`

For each: try with user token directly; try with a forged token that has `is_admin: true` or `role: admin` in the JWT payload (cross-reference `/credential-audit` JWT attacks).

**4d — Negative ownership attack**
Can you specify another user as the *source* of an action rather than the target?
- `{"from_user_id": victim_id}` — charge the victim
- `{"sender_id": victim_id}` — send on behalf of victim
- `{"created_by": admin_id}` — claim admin created this

**Finding criteria**:
- Any resource returned for another user's ID → **High** (BOLA)
- Admin function callable with user token → **High** (BFLA)
- Negative ownership accepted → **Critical**

---

### Phase 5 — Idempotency & Replay

For every state-changing operation (submit, confirm, pay, send, create, activate, redeem):

**5a — Rapid duplicate submission**
Send the identical request twice within 100ms:
```bash
# Via kali — send the same state-changing request twice concurrently
for i in 1 2; do
  curl -s -X POST http://TARGET/api/ENDPOINT \
    -H "Authorization: Bearer TOKEN" \
    -H "Content-Type: application/json" \
    -d 'PAYLOAD' &
done
wait
```
Does the server process both? Is the resource created/consumed twice?

**5b — Replay after delay**
Send the identical request again 5 seconds after the first succeeded. Does the server detect it as a duplicate?

**5c — Same reference/idempotency key**
If the API issues reference numbers or accepts idempotency keys: construct a new request using a previously-used reference number. Does the server reject it?

**5d — Mass parallel replay**
Send 10 identical requests simultaneously:
```bash
for i in $(seq 1 10); do
  curl -s -X POST http://TARGET/api/ENDPOINT \
    -H "Authorization: Bearer TOKEN" \
    -d 'PAYLOAD' &
done
wait
```
How many succeed? Is there a winner-takes-all race, or do all 10 process?

**Finding criteria**:
- Duplicate request processed (resource created/consumed twice) → **High**
- No idempotency protection on any state-changing operation → **Medium**
- All 10 concurrent requests processed → **Critical** (double/multi-spend)

---

### Phase 6 — Quota & Rate Limit Bypass

For any feature that has a stated cap (API calls per minute, storage quota, seats per org, free-tier resource limit, usage credits):

**6a — Direct overage**
Send `limit + 1` requests; send a resource that puts total storage above the cap; add `max_users + 1` to an org. Is the cap enforced server-side or only in the UI?

**6b — Negative consumption**
Send negative usage values if the system tracks consumption: `{"bytes_used": -999999}` → does the quota counter go negative (effectively resetting the limit)?

**6c — Parallel provisioning race**
If a quota is checked then consumed in two separate operations (check-then-act), send many concurrent requests that each read "quota available" before any of them deduct:
```bash
for i in $(seq 1 20); do
  curl -s -X POST http://TARGET/api/resources/create ... &
done
wait
```
Does each concurrent request pass the quota check before any deduction is recorded?

**6d — Account switching / tenant context**
Create multiple accounts or sub-tenants. Does each one get its own independent quota, or is there a shared pool that can be exhausted from one account and accessed from another?

**Finding criteria**:
- Hard limit not enforced server-side → **High**
- Concurrent requests bypass quota check → **High** (TOCTOU race)
- Negative consumption resets quota → **Critical**

---

### Phase 7 — Time & Date Manipulation

For any feature that depends on time: promotions, expiry windows, rate-limiting windows, cooldowns, scheduled operations, time-based access grants.

**7a — Expired token / session reuse**
After a time-limited token expires (password reset, email verification, promo code, discount), attempt to use it past the stated expiry. Is expiry enforced server-side?

**7b — Future-date manipulation**
For endpoints that accept date parameters: send future dates that move an operation into a more favorable window:
- `{"valid_until": "2099-12-31"}` on a subscription or license
- `{"start_date": "1970-01-01"}` to backdate a resource into an active state

**7c — Race the expiry**
If a token or window expires at time T, send the request simultaneously across the boundary. Does the server enforce expiry at the database level or just at the API layer?

**7d — Cooldown bypass**
If an action has a cooldown (rate limit per account, one vote per day, one review per item), check if a different account, IP, or session bypasses the cooldown independently.

**Finding criteria**:
- Expired token accepted → **High**
- Date field injection extends resource validity → **High**
- Cooldown enforced client-side only → **Medium**

---

### Phase 8 — Reference & Authorization Code Predictability

For any value the application generates that is later used as a proof-of-access (order confirmation codes, payment references, invite tokens, voucher codes, authorization codes):

**8a — Sample collection**
Collect 10 sequential samples by performing the action that generates the value 10 times in quick succession.

**8b — Delta analysis**
```python
samples = ["VALUE1", "VALUE2", "VALUE3"]  # collected values
# Try integer delta
try:
    deltas = [int(samples[i+1]) - int(samples[i]) for i in range(len(samples)-1)]
    print(f"Integer deltas: {deltas}")
    if len(set(deltas)) == 1:
        print(f"SEQUENTIAL — consistent delta: {deltas[0]}")
except ValueError:
    pass
# Try length + charset entropy
import math
charset = len(set("".join(samples)))
avg_len = sum(len(s) for s in samples) / len(samples)
bits = avg_len * math.log2(max(charset, 2))
print(f"Entropy: {bits:.1f} bits (charset={charset}, avg_len={avg_len:.1f})")
```

**8c — Exploitation of predictability**
If samples show a consistent delta or low entropy:
- Can you reconstruct codes for transactions you didn't participate in?
- Can you predict a future code and "pre-claim" a resource?
- Can you enumerate all active orders/invites/tickets by iterating IDs?

**Finding criteria**:
- Consistent sequential delta → **High** (full enumeration of all resources)
- Entropy < 40 bits on any access code → **High** (brute-forceable)
- Successfully predicted a code before it was used → **Critical** (proof of exploitability)

---

### Phase 9 — Multi-Tenant Isolation

*Thorough depth only. Applicable when the app has organizations, workspaces, merchants, or other tenant namespaces.*

**9a — Setup**
Register two separate tenant accounts (Tenant A and Tenant B) with distinct resources.

**9b — Cross-tenant resource access**
As Tenant A, attempt to access Tenant B's resources using Tenant B's resource IDs:
- Data records (orders, messages, files, reports)
- Configuration (settings, API keys, webhooks)
- Users belonging to Tenant B

**9c — Shared resource pool**
Does an operation by Tenant A consume from a shared pool that affects Tenant B? (e.g., shared rate limit, shared storage bucket, shared ID namespace)

**9d — Admin escalation across tenants**
If Tenant A has an admin user, does that admin access extend to Tenant B's data or configuration?

**Finding criteria**:
- Any Tenant B resource returned to Tenant A → **Critical** (tenant isolation broken)
- Shared ID namespace allowing cross-tenant enumeration → **High**
- Admin of one tenant accessing another tenant's data → **Critical**

---

### Chaining

| Condition | Chain to |
|-----------|---------|
| Mass assignment or boundary injection suspected | `/param-fuzz` — systematic parameter-level testing |
| Predictable IDs or low-entropy tokens confirmed | `/param-fuzz` Phase 6 (entropy analysis) for deeper measurement |
| Auth bypass or JWT forgery needed for BFLA | `/credential-audit` — JWT attacks and token manipulation |
| BOLA confirmed — want full injection testing on the exposed surface | `/web-exploit` — injection testing on now-accessible endpoints |
| RCE or critical chain achieved | `/post-exploit` — privilege escalation and persistence |
