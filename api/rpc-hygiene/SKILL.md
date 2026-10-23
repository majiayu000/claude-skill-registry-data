---
name: rpc-hygiene
description: Reach Solana only through the ordered RPC failover list with rate limits, and never log keys or URLs that carry secrets.
bots:
  - bot-01-scout
  - bot-03-whale
  - bot-04-sniper
  - bot-05-rug
  - bot-06-exit
gates: []
required_tools: []
required_data:
  - solana_rpc
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/http/priority_fee.json
---

# RPC Hygiene

## L1 - Summary

Solana reads go through the ordered failover list with per-endpoint rate limits, and secrets never touch logs. Each seat uses only its own granted `onchain.*` and `market.*` subset; when the primary endpoint degrades, the client fails over in order and marks stale data instead of guessing.

```
primary slow/error -> next endpoint in order -> all degraded -> mark data stale, stop ticket flow
secret in URL or log line -> redact immediately, rotate the key out of band
```

## L2 - Method

1. S1 - Use the ordered list: send reads to the primary Solana RPC first, then fail over strictly in the configured order. Never reorder by latency hunches and never fan out to unlisted endpoints.
2. S2 - Respect the rate limits: each endpoint carries a budget; when the budget is spent, back off with the configured retry (timeout, 5xx, and 429 only) instead of hammering. Malformed responses are typed `DataStale`, never exceptions that skip handling.
3. S3 - Keep keys out of text: the API key travels in headers or redacted config, never in URLs, log lines, or error messages. If a key leaks into a log, redact the line and rotate the key.
4. S4 - Mark staleness honestly: when every endpoint is degraded, label the data stale with its age and stop ticket flow that depends on it. A stale price is information; a guessed price is a lie.
5. S5 - Stay in your grant: SCOUT, WHALE, SNIPER, RUG, and EXIT each call only their rostered subset. Needing another subset is a roster change through RISK, not a reason to borrow.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| All endpoints degraded | Outage or exhausted budgets | Mark stale, halt dependent tickets, keep polling on schedule |
| Key in a log line | URL-built client or verbose error dump | Redact, rotate the key, fix the client to use headers |
| Wrong-subset call refused | Seat reaching outside its roster | Request the roster change; never work around PermissionDenied |
| Silent fallback to a cache | Stale data presented as fresh | Attach age and source to every read; fail closed past the freshness bound |

## References

- RPC client: `src/pumpgrok/tools/onchain/rpc.py` (failover order plus rate limits)
- Fixture: `tests/fixtures/http/priority_fee.json` (recorded fee response shape)
- Companion skills: `solana-rpc-and-wallet` (wallet plus failover rules), `key-custody` (secret handling)
