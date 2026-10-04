---
name: no-vibes
description: Use when completion depends on an end-to-end outcome across components, environments, or external systems.
---

# No Vibes

Treat each check as evidence for one claim, not as a substitute for the requested outcome.

## Map the outcome

Before coding—or immediately when invoked mid-task:

1. State the requested outcome in one observable sentence.
2. Trace the shortest flow from its initiating action to final state.
3. Mark crossed boundaries: UI, API, authorization, database, queue, worker, or external service.
4. Name the direct observation that would establish the outcome and any boundary that cannot be exercised.

Keep this proportional; ignore unrelated components.

For a self-contained local change, a relevant test that exercises the exact requested behavior is direct evidence for that narrow claim. Do not invent a broader flow.

## Classify the evidence

Give each material claim one status:

- **Verified**: A relevant check observed the claim itself in a named environment. It verifies only the scope exercised.
- **Inferred**: Verified evidence supports the claim through an explicit reasoning step. Name it.
- **Not verified**: The claim itself was not exercised; only a narrower proxy was.
- **Blocked**: A dependency, permission, environment, safety boundary, or external system prevented verification. Name the blocker and remaining check.

Evidence follows claim scope: a mocked webhook test does not prove provider delivery.

## Apply the completion gate

Claim the outcome complete only after end-to-end observation in an environment representative of the claim. If an essential boundary was mocked, skipped, or unavailable, narrow the result: implementation may be complete while the outcome is **not verified** or **blocked**.

Never upgrade **inferred** to **verified** or collapse a partial flow into one success.

## Report the result

End with a compact evidence ledger:

```text
Outcome: <observable user result>
Verified: <checks run, environment, and observations>
Inferred: <claim and supporting reasoning>
Not verified: <unexercised parts of the critical flow>
Blocked: <blocker and remaining verification, if any>
Conclusion: <full completion or an accurately narrowed claim>
```

Omit empty lines, but never an unverified essential part of the flow.

## Example

For subscription cancellation, trace click → authorization → provider → webhook → entitlement → UI. If the webhook was mocked and no entitlement change was observed, mark local checks **verified**, that path **not verified**, and the flow incomplete.
