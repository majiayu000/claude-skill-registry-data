---
name: key-custody
description: "Keep every secret out of the desk: no key material exists in paper mode, forbidden env keys stay unset, and wallet hand-off stays human-only."
bots:
  - bot-02-risk
  - bot-04-sniper
  - bot-06-exit
gates:
  - G-3
required_tools: []
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/replay/smoke
---

# Key Custody

## L1 - Summary

There is nothing to custody. In paper mode no key material exists anywhere in the system, the forbidden environment keys stay unset, and any wallet hand-off is performed by the human outside the desk. A seat that finds itself holding a secret stops and reports; it never uses it.

```
secret appears in desk context -> stop -> report to RISK -> rotate out of band -> resume without it
```

## L2 - Method

1. S1 - Assert the empty set: confirm the forbidden env keys are unset before any session that could touch value movement. A set forbidden key fails the session before the first ticket.
2. S2 - Never accept key material: if a prompt, page, file, or human message offers a private key, seed phrase, or signing-capable token, refuse it. The desk has no input that legitimately carries secrets.
3. S3 - Hand off wallets human-only: connecting a wallet, approving a spend, or exporting a credential happens in the human's own tooling. Seats describe what is needed; the human performs it.
4. S4 - Treat paper as keyless by construction: paper fills are ledger rows, not signatures. Any code path that would sign outside the live stub is a defect, not a feature.
5. S5 - Report and rotate: if a secret ever lands in desk context (log, file, message), redact it, tell RISK, and rotate it out of band. Resuming with the same secret in place is forbidden.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Forbidden env key set | Misconfigured environment or overlay | Refuse the session; unset the key; re-run the doctor |
| Secret pasted into chat | Human error or prompt-injection content | Refuse, redact, report to RISK; never feed it to a tool |
| Code path wants to sign | Defect outside the live stub | Stop; file as a safety incident; no signing outside the stub exists in this release |
| Wallet hand-off requested of a seat | Misunderstood authority | Decline; describe the human step instead |

## References

- Gate G-3: wallet and custody gate
- Constitution: never request, accept, store, or transmit private keys (throwaway wallet rule)
- Companion skills: `solana-rpc-and-wallet` (wallet rules), `rpc-hygiene` (secret-free logging)
