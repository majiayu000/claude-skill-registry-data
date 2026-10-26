---
name: prd-draft
description: Use when drafting product requirements from a reviewed problem or discovery notes.
---

# PRD Draft

Expand reviewed product rationale only when it helps the increment. A small change
can keep its canonical discovery brief; do not mandate a PRD, UI exercise or ticket
copy. If audience, value or material constraints are unresolved, use discovery
and retain an investigate decision with a bounded evidence goal.

Use `docs/templates/prd.md` when present (`agents/templates/prd.md` in ai-dlc's
source repository). Without that asset, use these exact sections:

- **Problem and audience** — link the canonical brief and supporting sources.
- **Evidence and decisions** — distinguish observations and their limits, actual
  user decisions/authorization, and hypotheses. Retain source links.
- **Options and rationale** — compare feasible alternatives, including no change
  when meaningful, by impact, confidence, effort and dependencies.
- **Outcomes and acceptance** — reuse canonical OUT-001/RQ-001 IDs and map criteria
  to outcomes with observable evidence. If no brief exists, declare this document
  the canonical owner. Mark unconfirmed criteria as proposals.
- **Scope and exclusions** — bounded increment and explicit compatibility.
- **Constraints and risks** — consumers, migration/recovery and verification needs.
- **Open questions** — material unknowns, contradictions and decision owners.
- **Links** — canonical brief, applicable design, formal specification and work.

Keep draft status and owner explicit. Record a proceed, investigate or stop decision
and reason at the end using discovery's rules. Proceed hands off to needs-spec
and the configured specification provider before implementation where required.
Do not silently choose unresolved format/error semantics, claim unspecified
headers are approved, or promote a hypothesis to an acceptance fact. A fixture
result establishes only what was exercised, not live integration or user value.

Store durable rationale in repository `docs/design` when requested. Formal
behavior belongs to the specification role; the PRD explains intent and scope.
Keep existing user approval distinct from this recommendation, and publish tracker
work only with authorization.

Resolve provider-specific commands from the configured role provider’s instructions.
The agent supplies judgment; services store, validate, and link artifacts.
