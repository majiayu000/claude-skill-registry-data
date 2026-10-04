---
name: stripe-spend
description: "Create real Stripe test-mode charges for bounded business actions, with an authority-band budget cap and human escalation above the cap."
version: 1.0.0
author: argobox
license: MIT
platforms: [linux]
metadata:
  custodian:
    band: L2
    cost_usd: 0.0
    configured: true
    allowed_hosts:
      - api.stripe.com
  hermes:
    tags: [Payments, Stripe, Budget, Authority, Finance]
---

# Stripe Spend (bounded authority)

Create a real Stripe PaymentIntent (test mode) when you decide to spend money on an action — for
example, starting a monitored worker, buying alerting credits, or charging a customer for a
completed job. Every call is logged to the authority ledger and checked against the current
authority band before the request is sent.

You are operating under **bounded authority**, not unlimited spend. Read `references/authority-bands.md`
before your first spend decision this session.

## Quick Reference

| Action | Command |
|--------|---------|
| Check current authority band + remaining budget | `python3 scripts/authority.py status` |
| Propose + execute an in-budget spend | `python3 scripts/spend.py --amount 0.50 --description "..."` |
| Propose a spend that exceeds the cap (escalates) | same command — the script decides, you don't pre-check |
| View the audit log | `python3 scripts/authority.py log` |

## How spend.py decides

1. Reads the current band's cap from `references/authority-bands.md` (band state lives in
   `state/authority.json`).
2. If `amount <= cap - already_spent_this_band`: executes the Stripe PaymentIntent immediately.
   This is an **autonomous, in-budget action** — no human needed.
3. If `amount` would exceed the remaining budget: the script does **not** call Stripe. It writes an
   `escalation_required` record to the audit log and exits with a message telling you to surface
   this to the human operator and wait for an explicit approve/deny before retrying with
   `--approved-by <name>`.
4. Every outcome (executed, escalated, denied) is appended to `state/audit_log.jsonl` — never
   overwritten, never deleted. This is the evidence trail.

## Retry behavior

The underlying OpenShell sandbox proxy can occasionally drop the first connection to
`api.stripe.com` (`NET:FAIL` immediately after `NET:OPEN ALLOWED` in the sandbox logs). This is a
transient proxy issue, not a policy or auth failure. `scripts/spend.py` already retries once
automatically after a 1s backoff before reporting failure — you do not need to retry manually.

## Example session

```
$ python3 scripts/authority.py status
Band: L2 (auto-approve up to $2.00/action, $10.00/session)
Spent this session: $0.45
Remaining: $9.55

$ python3 scripts/spend.py --amount 0.50 --description "Start monitoring worker for example.com"
[authority] L2 cap OK ($0.50 <= $9.55 remaining) — executing autonomously
[stripe] PaymentIntent created: pi_3Tk... ($0.50, test mode)
[audit] logged: executed

$ python3 scripts/spend.py --amount 5.00 --description "Scale monitoring to 100 targets"
[authority] L2 cap exceeded ($5.00 > $9.55 remaining is fine, but per-action cap is $2.00)
[authority] ESCALATION REQUIRED — this exceeds the L2 per-action authority band.
[audit] logged: escalation_required
Surface this to the human operator. Do not retry without --approved-by.

$ python3 scripts/spend.py --amount 5.00 --description "Scale monitoring to 100 targets" --denied-by operator
[audit] logged: denied (by operator)
No Stripe call made.
```

## Files

- `references/authority-bands.md` — the L0-L4 band definitions and current active band
- `scripts/authority.py` — status/log CLI
- `scripts/spend.py` — the spend decision + Stripe call
- `state/authority.json` — current band + session spend (read/write)
- `state/audit_log.jsonl` — append-only decision log (read-only to you; never edit by hand)
