---
name: threat-modeling
description: Use when designing a system and identifying what could go wrong. Applies STRIDE to a data-flow model, ranks threats by realistic risk, and produces mitigations that are actually built.
metadata:
  category: security
  version: 1.0.0
  tags: [threat-model, stride, risk, design, security]
---

# Threat Modeling

## Purpose

Find the security problems in a design before they are built. Threat modeling is cheap; the same finding after launch is a rewrite, and after a breach it is a disclosure.

## When to Use

- Designing a new system or a significant feature.
- Adding a new trust boundary: a new integration, a new user role, a new data flow.
- Before a security review or a compliance audit.
- After an incident, to find the siblings of what just happened.

## Capabilities

- Data-flow modeling and trust-boundary identification.
- STRIDE analysis: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- Risk ranking by likelihood and impact.
- Mitigation design and acceptance of residual risk.

## Inputs

- The design: components, data flows, and data stores.
- The assets worth protecting and to whom.
- The realistic attacker: an external attacker, a malicious tenant, a compromised dependency, a departing employee.

## Outputs

- A data-flow diagram with trust boundaries marked.
- A ranked threat list with mitigations.
- Explicit acceptance of the risks not being mitigated.

## Workflow

1. **Draw the data flow** — Components, data stores, external entities, and the flows between them. Simple boxes and arrows; the diagram is a tool, not a deliverable.
2. **Mark the trust boundaries** — Every line data crosses where the trust level changes: internet to your edge, your service to a third party, tenant A's data to tenant B's request. Threats live on these lines.
3. **Apply STRIDE at each boundary** — For each flow, ask each of the six questions. It is mechanical, and that is the point: it finds what intuition skips.
4. **Rank by realistic risk** — Likelihood times impact. A theoretical attack requiring physical access to the datacenter ranks below an IDOR that a bored user could find.
5. **Design mitigations** — For each threat above the acceptance line, a specific control, with an owner.
6. **Accept the rest explicitly** — Write down what you are not mitigating and why. Undocumented acceptance is indistinguishable from oversight.

## Best Practices

- Threat model the design, not the code. By the time it is code, the expensive mistakes are already made.
- The most productive question is "what does this component trust, and why?" Trust that has never been examined is where the vulnerabilities are.
- Include the insider and the compromised dependency in the attacker list. Both are more likely than a nation-state, and both are usually ignored.
- A threat with no mitigation and no explicit acceptance is a threat that will be forgotten. There are only two valid states.
- Multi-tenant systems: the highest-value threat is nearly always "tenant A reads tenant B's data". Model it first, and enforce isolation at the lowest layer you can.
- Keep the model updated. A threat model from the original design, two years and forty features later, is a historical document.

## Examples

**STRIDE applied to one flow, producing a real finding:**

```text
Flow: Browser -> API Gateway -> Orders Service -> Postgres
Boundary: internet / internal (at the gateway)
Asset: order data, including customer PII and amounts

S - Spoofing
    Threat: Attacker forges a JWT to impersonate another user.
    Mitigation: Signature verified with a pinned algorithm (RS256); `alg`
    from the header is never trusted. Keys rotated quarterly.
    Status: MITIGATED

T - Tampering
    Threat: Client modifies `total_cents` in the create-order payload.
    Finding: The API currently trusts the client-supplied total.
    Mitigation: Server recomputes the total from the line items and the
    price list. The client-supplied value is ignored entirely.
    Status: ACTION REQUIRED — owner @sam, due 2026-04-02

R - Repudiation
    Threat: A user denies having placed an order.
    Mitigation: Append-only audit log with the authenticated subject, the
    request ID, and the source IP. Retained 7 years.
    Status: MITIGATED

I - Information disclosure
    Threat: Tenant A reads tenant B's orders by guessing an ID.
    Mitigation: ULIDs (not enumerable) AND a row-level security policy on
    tenant_id. Two independent controls, because this is the highest-impact
    threat in the system.
    Status: MITIGATED

D - Denial of service
    Threat: An expensive report query is called in a loop.
    Mitigation: Rate limit per tenant; query timeout of 5s; the report is
    served from a materialized view.
    Status: MITIGATED

E - Elevation of privilege
    Threat: A read-only API key performs a write.
    Finding: Scopes are checked at the gateway but not re-checked in the service.
    Risk: A service reachable from inside the VPC bypasses the check entirely.
    Mitigation: Enforce scope in the service, not only at the edge.
    Status: ACTION REQUIRED — owner @maya, due 2026-04-09
```

## Notes

- The tampering finding above ("the server trusts the client's total") is one of the most common and most costly real-world flaws, and it is found in about five minutes by mechanically walking STRIDE. That is the entire argument for the method.
- Defense in depth means two independent controls for the highest-impact threat. In multi-tenant systems, that is cross-tenant access — application-level filtering *and* row-level security.
- A threat model produced by one person is a review of that person's blind spots. Do it with at least two people, one of whom did not design the system.
