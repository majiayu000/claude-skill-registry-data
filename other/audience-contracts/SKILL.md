---
name: audience-contracts
description: Design for four user classes — humans, agents, hybrid systems, software — with progressive contracts.
version: 1
triggers: audience, user classes, api design for agents, interface design, contracts
category: Engineering & code
blurb: Design for four user classes — humans, agents, hybrid systems and software — with progressive contracts.
archetype: knowledge
example: Design this interface so both humans and agents can use it well.
---

# Audience Contracts

Every artifact has four kinds of users: **humans, agents, systems (human+agent+software together), and software**. Author once; contract four times — never four products, never one lowest-common-denominator interface.

## When to use
- Designing anything meant to be used, invoked, or operated by more than one class.
- Auditing an existing artifact for missing contracts (which user class falls off?).
- Before shipping: confirm all four classes have a working path.

## Method
1. **Name the classes and their needs**:
   - *Human*: visual, narrative, progressive disclosure, forgiving input; approves.
   - *Agent*: procedure — when to use, method, gates, red lines; executes within caps.
   - *System*: handoff contracts, approvals, shared state, audit; binds the others.
   - *Software*: schemas, stable IDs, versioned API/CLI/JSON, exit codes; deterministic.
2. **Single truth, multiple renderings**: one canonical artifact (markdown+frontmatter, JSON) rendered per audience. Forking truth per class = drift.
3. **Progressive formality**: human view most forgiving → software least. Same content: card → procedure → gates → schema → signature.
4. **Fail per class**: humans get readable errors + retry; agents get instructive errors + safe fallback; systems get escalation; software gets structured errors + exit codes.
5. **Authority lattice**: dangerous actions need capability (agent) + approval (human) + determinism (software) + audit (system). Miss one → no action.
6. **Verify by class, never by self-report**: agents → verify with software (tests/signatures); humans → evidence; software → spec tests; systems → cross-verification via audit trails.
7. **Identity per class**: humans (passkey/MFA), agents (scoped short-lived tokens), systems (policy engine), software (service creds/mTLS).

## Quality gates
- [ ] All four classes have a named, working path to the artifact.
- [ ] One canonical source; renderings are generated, not maintained separately.
- [ ] Failure behavior defined per class.
- [ ] Danger paths pass the authority lattice; audit exists.

## Red lines
- Never ship for one class and assume others "will cope"; never fork truth per audience; no dangerous path that skips the lattice.

## Related
`multi-surface-webapp` · `skill-ops` · `technical-writing` · `zero-trust-architecture`.
