---
name: webhooks-safe
description: "Ingest inbound webhooks safely for Ottili flows: verify HMAC signatures over the raw body, dedupe by event id with a TTL, preserve per-stream order, respect provider replay windows, route persistent failures to a dead-letter queue, and validate outbound delivery targets against an allow-list to prevent SSRF. Use when an agent must receive, verify or process a webhook payload; when a webhook arrives out of order or twice; or when a webhook handler fails. Not for outbound retry engineering."
license: MIT-compat
compatibility: "framework-agnostic; HMAC-SHA256 webhook verification; offline validation"
metadata: {}
allowed-tools: []
---

# webhooks-safe

## When to use this skill

Use this skill when an agent must ingest an inbound webhook for Ottili
flows: verify its signature over the raw body, dedupe it by event id,
preserve delivery order within a stream, respect the provider's replay
window, route persistent failures to a dead-letter queue, and — if the
skill ever needs to deliver outbound — do so only against an allow-listed
Ottili endpoint. Do **not** use it for outbound retry engineering or for
providers whose signature scheme is unknown.

## Procedure (numbered, in order)

1. **Verify the signature over the raw body.** Recompute the HMAC with the
   provider's secret. Reject on mismatch. Never trust headers alone, never
   parse-then-re-encode the body, and always use `hmac.compare_digest`.
2. **Dedupe.** Every webhook carries an event id; store it with a TTL; on a
   duplicate id, ack and skip. Never process twice. Check-and-set must be
   atomic.
3. **Preserve order.** Within one delivery stream, process events as they
   arrive; an out-of-sequence event waits until the missing one shows up or
   the replay window expires. Ordering is per stream, never global.
4. **Respect replay windows.** Stripe bakes the timestamp into the
   signature itself — stale signatures get rejected before the HMAC is even
   checked. Hold unprocessed events for the window before declaring them lost.
5. **Dead-letter.** After three failed attempts, park the event in the
   dead-letter queue together with the raw payload and the reason it failed;
   a webhook must never vanish without a trace.
6. **SSRF-safe delivery.** Check every outbound target against the allow-list
   of Ottili endpoints; throw out IP literals and `localhost`, and never try
   to resolve them first.
7. **Log.** Record every verify/dedupe/delivery decision with the event id.

## Decision tables

### Provider signature schemes

| Provider | Header | Algorithm | Replay window |
|---|---|---|---|
| GitHub | `X-Hub-Signature-256` | HMAC-SHA256, `sha256=<hex>` | 24h TTL on event id |
| Stripe | `Stripe-Signature` | HMAC-SHA256, `t=<ts>,v1=<hex>` | 5 minutes |
| PayPal | `X-PayPal-Signature` | HMAC-SHA256 (unverified) | provider-defined |
| Twilio | `X-Twilio-Signature` | HMAC-SHA256 over URL + body (unverified) | provider-defined |

### Dedupe outcome

| Situation | Action |
|---|---|
| Event id seen, within TTL | Ack and skip; never process twice |
| Event id seen, TTL expired | Re-process (idempotency must still hold) |
| Event id new | Process and store with TTL |

### Dead-letter trigger

| Trigger | Action |
|---|---|
| Signature invalid | Reject immediately; do not dead-letter (it is not our event) |
| Processing throws 3 times | Move to dead-letter with raw payload + reason |
| Replay window expired | Move to dead-letter marked "lost" |

### Outbound allow-list check

| Target | Action |
|---|---|
| Allow-listed Ottili host + path | Deliver |
| Allow-listed host, different path | Reject (path not allowed) |
| Any other host | Reject immediately (SSRF) |
| IP literal or `localhost` | Reject (never resolve) |

## Worked examples

### Good output — valid Stripe event, first delivery
Input: raw body `{"type":"invoice.paid","data":{"object":{"id":"in_123"}}}`,
header `Stripe-Signature: t=1700000000,v1=abc123...` (valid HMAC).
Expected behaviour: signature verifies over the raw bytes, event id
`evt_01F...` is new → process, store with TTL, log `verified ok, processed`.
`scripts/verify.py --provider stripe` exits 0.

### Bad output — signature recomputed over parsed JSON
Input: the agent parses the body with `json.loads`, then re-serialises with
`json.dumps(..., separators=(",", ":"))` and computes the HMAC over that.
Result: the signature never matches, because the original payload had
whitespace or key ordering the re-serialization changed.
`scripts/verify.py` exits 2 with:
`FAIL: signature mismatch — recompute over the raw body, never the parsed body`
Fix: read `sys.stdin.buffer` (raw bytes) and HMAC those.

### Bad output — old signature accepted anyway
Input: `Stripe-Signature: t=1699990000,v1=...` — 6 minutes old, outside
the 5-minute replay window.
`scripts/verify.py` exits 2 with:
`FAIL: signature timestamp 1699990000 is outside the 5-minute replay window`
Fix: reject before the HMAC check. A stale signature is a replay attempt.

### Good output — duplicate delivery acked and skipped
Input: the same event id arrives a second time (within TTL).
Expected behaviour: dedupe returns `duplicate`, the handler acks and does
**not** process again. Log `dedupe: duplicate, skipped`.

### Bad output — out-of-order event processed immediately
Input: stream `acc_1` receives event 3 before event 2.
Expected behaviour: event 3 is **held** until 2 arrives or the replay window
expires; it is not processed out of order.
`scripts/ordering.py` returns `held`, and a near-miss test asserts the held
set is written back (the old `state.get("held", {})` bug dropped held events
on restart — fixed with `setdefault`).

## Pitfalls from research

- **Verify over the raw body, not the parsed body.** Re-encoding the JSON
  changes byte order and every signature fails. Read the raw bytes.
- **Stripe's timestamp is part of the signature.** A signature older than the
  replay window is a replay attack — reject it before checking the HMAC.
- **GitHub's `X-Hub-Signature-256` carries the value `sha256=<hex>`.** The older
  `X-Hub-Signature` (SHA1) has been deprecated; never fall back to it.
- **Dedupe must be atomic.** Check-and-set on the event id must be one
  operation; a race that checks then sets processes the event twice.
- **Never deliver to arbitrary hosts.** A webhook payload that an attacker
  controls can trigger an outbound call, which is an SSRF. Validate the target
  against the allow-list before any delivery.
- **Ordering is per delivery stream, not global.** Two independent providers
  can interleave; only enforce order within one stream.
- **PayPal and Twilio schemes are unverified** until their docs are fetched
  at build time; the scripts fall back to plain HMAC-SHA256 and the skill
  flags the result as unverified.

## Verification checklist

- [ ] Signature verified over the raw body; reject on mismatch
- [ ] Stripe timestamp within replay window before HMAC check
- [ ] Event id stored with TTL; duplicates acked and skipped
- [ ] Out-of-sequence events held until missing event or replay window expires
- [ ] Persistent failures moved to dead-letter with raw payload and reason
- [ ] Outbound delivery target validated against the allow-list
- [ ] Every decision logged with the event id

## Near-miss triggers (stop and re-read)

- "I'll parse the JSON and verify against that" → raw bytes only.
- "The signature is old, but it's probably fine" → replay window first.
- "I'll just deliver to whatever URL is in the payload" → SSRF; allow-list it.
- "PayPal/Twilio use the same scheme as GitHub" → unverified; flag it.
- "I'll skip the atomic check for speed" → a race processes the event twice.


## Related skills

[dsgvo-ai-act-labeling](../dsgvo-ai-act-labeling/) — a webhook payload that carries personal data must be disclosed in the Art. 30 register
[gobd-archive](../gobd-archive/) — delivery and dedupe state is correspondence (6y)

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
- [Scripts](scripts/)
