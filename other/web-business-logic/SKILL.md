---
name: web-business-logic
description: >
  Find business-logic flaws — abusing intended functionality in unintended ways. Load on
  workflows with money/quantity/state/limits: checkout, coupons, refunds, transfers, quotas,
  multi-step flows, role/tenant boundaries. Signals: price/qty params, discount codes, step
  skipping, negative/overflow values.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A04:2021-Insecure-Design]
cwe: [CWE-840, CWE-841]
tools: [burp]
schema_version: 1
---

# Business-logic flaws

## When it applies
The app works "correctly" per code but the *rules* can be gamed: paying less, getting more,
skipping a required step, or crossing a boundary the designers assumed users would respect.

## Why it works
Scanners can't find these — they require understanding intent. Servers trust client-supplied
economics/state and assume the happy path; deviate from it and constraints (price, quantity,
sequence, ownership) aren't re-enforced.

## Method
1. **Model the intended flow** and its invariants (what must stay true: price ≥ 0, step order,
   one coupon, my-cart-only).
2. **Break each invariant**:
   - **Value tampering**: negative/zero/huge quantity or price, currency/decimal tricks, integer overflow.
   - **Coupon/refund abuse**: reuse, stack, apply after total, refund more than paid.
   - **Step skipping / state**: jump to the confirmation/paid step, replay a step, reorder.
   - **Quota/limit bypass**: race the check (→ `web-race-conditions`), reset counters, parallel requests.
   - **Boundary crossing**: act on another tenant's resource (→ `web-idor`), escalate role via workflow.
3. **Quantify impact** in business terms (free goods, money, privilege) for the report.

## Gotchas
- These are context-specific — read the app like a user trying to cheat, not a scanner.
- Prove real impact (an order placed for $0, a limit bypassed), not just an odd response.
- Often chains with IDOR/race/mass-assignment — combine primitives.

## Verify success
A completed abuse of the workflow with concrete gain (paid less/nothing, exceeded a limit,
accessed disallowed state) reproduced step-by-step.

## References
PortSwigger business-logic labs; OWASP WSTG business-logic testing.
