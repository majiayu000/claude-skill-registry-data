---
name: threat-model-data-flow
description: Create a lightweight threat model from data flows, trust boundaries, assets, actors, and abuse cases for a feature or service.
---

# Threat Model Data Flow

## Goal

Identify high-impact security risks early enough to shape architecture and tests instead of relying only on a late checklist.

## Inputs to inspect

Architecture diagram or source map, sensitive data, users/roles, external dependencies, interfaces, and planned changes.

## Workflow

1. Define the feature boundary, valuable assets, sensitive data, trust zones, actors, and security-relevant assumptions.
2. Draw data flows through browser/client, API, services, database, queues, files, third parties, and administrative tools; mark trust-boundary crossings.
3. For each crossing, enumerate plausible threats such as spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation.
4. Rank risks by impact, reachability, required privilege, and likelihood; connect each material risk to a preventive control and a verification test.
5. Review with the feature owner, record accepted risks and owners, and update the model when interfaces, permissions, or data classifications change.

## Validation checklist

- [ ] Trust boundaries and sensitive data stores are explicit.
- [ ] Threats are tied to a concrete flow or asset rather than generic category labels.
- [ ] Every high risk has a control, a test, a mitigation decision, or a named acceptance owner.
- [ ] Operational/insider and third-party risks are included where relevant.
- [ ] Unverified assumptions and out-of-scope systems are stated clearly.

## Required output

Deliver a data-flow diagram, threat table, control/test mapping, accepted-risk register, and triggers for revisiting the model.

## Boundaries and failure handling

Do not present a lightweight model as a penetration test; do not label risks solved without checking that the control is implemented.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
