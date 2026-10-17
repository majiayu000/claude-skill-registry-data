---
name: policy-as-code
description: Write and ship authorization policy as code — OPA/Rego-class rules, tests, decision logs, safe rollout.
version: 1
triggers: policy as code, opa, rego, authorization policy, access rules as code
category: Security & privacy
blurb: Write access policy as code — tested rules, decision logs and safe rollouts.
archetype: knowledge
example: Turn my access rules into policy-as-code with tests.
---

# Policy as Code

Authorization logic belongs in testable policy — not scattered `if` statements. Write it, test it, shadow it, log every decision.

## When to use
- Access control beyond simple roles (attribute/resource rules, agent permissions).
- Compliance rules that must be consistently evaluated and provable.
- Anywhere "who can do what" changes often or matters a lot.

## Method
1. **Model the decisions**: enumerate the questions to answer (can subject S do action A on resource R, under context C?); define the input schema; **default deny**.
2. **Write policy as code** (OPA/Rego or Cedar-class): small composable rules; data separated from logic (policy data versioned); decision explanations available for humans.
3. **Test like code**: unit tests per rule — positive, negative, edge cases; decision-space coverage for key roles; lint + format in CI (`opa fmt`/`check`).
4. **Roll out safely**: **shadow mode** (log decisions without enforcing) → staging enforcement → production; break-glass path documented, gated, and audited; no silent policy edits.
5. **Decision logs**: who asked, what was decided, under which policy version, why — retained immutably; sample in prod, full in sensitive flows.
6. **Governance**: second pair of eyes on policy PRs; version + changelog; keep the human-readable policy summary in sync with code.
7. **Enforcement points**: app middleware, gateways, sidecars — enumerated in an inventory; decide fail-open vs fail-closed per surface (default: fail closed for sensitive).

## Quality gates
- [ ] Tests green + edge coverage for key decisions; lint clean.
- [ ] Shadow period completed before enforcement.
- [ ] Decision logs retained; break-glass tested once.
- [ ] Integration points inventoried; failure mode chosen consciously.

## Red lines
- No default-allow; no untested policy to production; no bypass paths around enforcement points.

## Related
`authentication-authorization` · `zero-trust-architecture` · `regulatory-compliance`.
