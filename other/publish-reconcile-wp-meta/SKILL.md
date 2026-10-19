---
name: publish-reconcile-wp-meta
description: "Publish content idempotently to WordPress and Meta for Ottili flows and reconcile unknown results: create/update posts, handle API errors, and reconcile when the result is unknown. Use when an agent must publish to WordPress or Meta; when a publish call returns an unknown result; or when reconciling a failed publish. Not for general CMS logic or non-WordPress/Meta platforms."
license: MIT-compat
compatibility: "framework-agnostic; WP REST API and Meta Graph API; offline validation"
metadata: {}
allowed-tools: []
---

# publish-reconcile-wp-meta

## When to use this skill

Use this skill when an agent must publish content to WordPress or Meta for
Ottili flows, or reconcile an unknown publish result. Do **not** use it for
general CMS logic, non-WordPress platforms, or non-Meta social platforms.

## Procedure (numbered, in order)

1. **Lookup first.** Ask the append-only idempotency store whether the
   client-generated key already maps to a post id. If yes, return it and
   never create a second post. A lookup miss is not a reason to publish —
   it is the *only* state in which publishing is allowed.
2. **Publish.** WordPress: `POST /wp/v2/posts` with Application Passwords or
   OAuth2 (Basic Auth is deprecated in WP 6.7+ core). Meta: `POST
   /{page-id}/feed` on the pinned Graph API version. Send exactly one
   request per key; the idempotency key is the same on every retry.
3. **Record.** On success, append the key → post id mapping to the store.
   Never mutate an entry in place — the store is append-only JSONL and an
   in-place edit breaks the audit trail.
4. **Handle errors.** 4xx blocks, except 409 (conflict → re-query by key).
   5xx retries with bounded exponential backoff (base 500 ms, factor 2,
   max 3 attempts, cap 30 s). Auth errors never retry with the same token.
5. **Reconcile unknowns.** On a timeout or partial success, re-query both
   platforms by idempotency key, compare state, log the delta. Persistent
   mismatch → human review, never silent overwrite.
6. **SSRF-safe.** Publish only to the configured WP/Meta endpoints. Check
   every outbound target against the allow-list; throw out IP literals and
   `localhost`, and never try to resolve them first.

## Decision tables

### Error → fix (condensed)

| Status | Meaning | Fix |
|---|---|---|
| 400 | Validation | Fix the named field |
| 401/403 | Auth | Re-issue credentials; never retry same token |
| 409 | Conflict / duplicate | Re-query by key; never re-create |
| 429 | Rate limited | Exponential backoff, up to 3 attempts |
| 5xx | Outage | Backoff; mark the post unknown |

### Reconcile outcome (condensed)

| Situation | Action |
|---|---|
| Both platforms agree | Ok; log |
| One platform is newer than the other | Re-query the older one; log the delta |
| Unknown result (timeout) | Re-query both by key; log the delta |
| Persistent mismatch | Flag for human review; never silently overwrite |

## Pitfalls from research

- **POST is not idempotent by HTTP semantics.** Neither platform provides
  native idempotency keys, so the skill constructs idempotency on top of the
  reconciliation layer.
- **WordPress Basic Auth is deprecated** as of WP 6.7+ (core). The separate
  plugin is unmaintained; use Application Passwords or OAuth2 instead.
- **Meta's pinned version is not the newest.** v19.0 is pinned, yet v20.0
  and v21.0 already appear in the changelog (re-verified 2026-10-09). Meta
  sunsets versions without notice; re-verify quarterly.
- **Never assume the first response is authoritative.** A single API call
  can time out or succeed on one platform only; the safe move is to re-query
  both platforms by the client idempotency key and compare state before
  acting on either answer.
- **SSRF-safe.** Publish only to the configured WP/Meta endpoints; never
  publish to arbitrary hosts.

## Verification checklist

- [ ] Idempotency key looked up in the store before every publish
- [ ] Duplicate key returns the existing post id (or 409 → re-query)
- [ ] WP uses Application Passwords or OAuth2 (not deprecated Basic Auth)
- [ ] Meta uses a page access token, pinned version
- [ ] 4xx treated as blocking (except 409); 5xx retried with backoff
- [ ] Unknown results re-queried by idempotency key; delta logged
- [ ] Publish target validated against the configured endpoints
- [ ] Idempotency store is append-only; no in-place mutation

## Near-miss triggers (stop and re-read)

- "I'll just POST again" → check the idempotency store first.
- "Basic Auth is fine, it's just a plugin" → deprecated in WP 6.7+ core.
- "v19.0 is the current Meta version" → v20.0 and v21.0 already exist.
- "The first response is authoritative" → re-query both platforms.


## Related skills

[webhooks-safe](../webhooks-safe/) — outbound delivery targets are validated against the same allow-list and signature rules
[gobd-archive](../gobd-archive/) — publish records and idempotency keys are correspondence (6y)

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
- [Scripts](scripts/)
