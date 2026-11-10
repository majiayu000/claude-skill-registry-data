---
name: clarila-security
description: "Assess the security implications of a specific change, such as auth, access boundaries, secrets or untrusted input. Not a blanket audit for every issue or permission to probe production."
---

# Assess the relevant security boundary

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the requested scope, actual diff, data sensitivity and trust boundaries. Identify assets, actors and entry points relevant to the change.
2. Trace authentication, authorization, input handling, secret exposure and dependency behavior where affected.
3. Validate concrete threats with safe local tests and permitted fixtures. Do not exfiltrate credentials, exploit unrelated systems or widen account access.
4. Propose proportionate repairs and verify them when implementation is explicitly assigned. Preserve independent review role when assessing someone else's change.
5. Return actionable source-bound findings and test evidence with coverage limits.

For each suspected issue, connect the actor-controlled input to the reachable entry point, the trust boundary crossed and the protected data or effect. State the necessary preconditions and use a local fixture or decisive source trace to distinguish an exploitable path from a hypothetical concern. When a change removes a check, inspect its callers and prior rationale. Severity follows the supported impact and reach.

This evidence-led threat and change analysis is informed by Trail of Bits' [differential-review method](https://github.com/trailofbits/skills/blob/711af095215ad4ecde5b90cd1d0124b3f1c4ca9e/plugins/differential-review/skills/differential-review/SKILL.md). Assess the requested boundary with the tools actually available.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read the private handoff described in the shared contract. When independently delegated, save an assessor-owned report and return it to the workflow owner for incorporation; do not compete to write the shared handoff. Otherwise update only the handoff you actually own using native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return relevant threats, verified findings, severity, evidence and remaining uncertainty.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
