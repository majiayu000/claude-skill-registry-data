---
model_tier: high
name: privacy-review
description: "Use when reviewing data flows, support macros, refund templates for GDPR/CCPA/HIPAA fit — regime, consent, PII redaction (email, order-id), breach triage. Triggers 'is this GDPR-safe', 'PII redact'."
status: active
tier: senior
domain: process
context_spine: [regulatory-regime, customer-segment, product]
recommended_for_user_types: [ops, finance, creator]
workspaces:
  - engineering
packs:
  - engineering-base
triggers:
  - phrase: "gdpr-safe"
  - phrase: "pii redaction"
---

# privacy-review

## When to use

- A new feature, integration, or vendor introduces a data flow and the question is *which regulatory regime applies*, *what consent / lawful basis is required*, *what the breach-impact tail looks like*.
- An existing data flow is being re-scoped (new geography, new customer segment, new processor) and the regulatory-regime delta must be read before the change ships.
- A customer / counterparty requests a DPA, BAA, or SCC and the question is *what we can credibly sign* given current data-handling reality.

Do NOT use as a substitute for qualified privacy counsel (this skill produces the non-lawyer cognition that prepares the counsel conversation), as a contract-level read (route to `contracts-cognition` (P5); P5 composes this skill for data-clause depth), or for privacy-platform SaaS configuration / audit-tool administration.

## Cognition cluster

- **Mental model 28 — Inversion.** *"What's the worst-case if this data flow leaks, is subpoenaed, or is mis-consented?"* Inversion sizes the regulatory tail before consent / DPA shape is debated. See [`mental-models.md`](../../../docs/contracts/mental-models.md) § 28.
- **Mental model 1 — First principles.** Strip the data flow to: *who* (data subject), *what* (data category), *why* (lawful basis / purpose), *where* (residency / transfer), *how long* (retention), *who else* (sub-processors). Six primitives anchor every regime delta. See `mental-models.md` § 1.
- **Mental model 21 — Second-order thinking.** Consent design at signup interacts with marketing automation; retention defaults interact with data-subject-rights workflow; sub-processor chains interact with breach-notification timelines. Each privacy choice has downstream regime obligations. See `mental-models.md` § 21.
- **Context-spine — regulatory-regime + customer-segment + product.** Read **regulatory-regime** (J1) for the applicable floor (GDPR, CCPA/CPRA, HIPAA, PIPEDA, LGPD, sector-specific). Read **customer-segment** for who the data subjects are (B2C-EU = GDPR primary; US-healthcare = HIPAA primary; B2B-EU-of-US-customers = mixed). Read **product** for which features touch sensitive categories.

## Cross-wing handoff

- Cites J1 `regulatory-regime` (foundation slot) for the regime floor read; without J1, this skill cannot bind which regime applies.
- Hands off to P5 `contracts-cognition` for clause-level redlines on DPAs / BAAs / SCCs.
- Hands off to P7 `data-handling-judgment` for the classification, retention, and cross-border-transfer surface that this skill flags.

## Procedure

### Step 0: Bind the regulatory-regime floor

Read the J1 `regulatory-regime` slot for the customer-segment and geography in scope. For each applicable regime, name:

1. *Which data subjects does it protect?* (EU residents → GDPR; California residents → CCPA/CPRA; US patients in covered entities → HIPAA).
2. *What categories does it gate?* (GDPR special categories; HIPAA PHI; CCPA "sensitive personal information").
3. *What lawful-basis / consent shape does it require?* (GDPR Art. 6 + Art. 9; HIPAA authorization; CCPA notice + opt-out).

Multiple regimes can apply simultaneously; the floor is the strictest applicable.

### Step 1: Map the data flow

For the feature / integration / vendor in scope, enumerate every hop:

1. **Collection** — what data category, from whom, where, with what notice / consent.
2. **Processing** — who processes (us, sub-processor), where, for what purpose.
3. **Storage** — where stored (region, system), encrypted at rest, retention default.
4. **Transfer** — cross-border hops, transfer mechanism (SCC, adequacy, BCR).
5. **Disclosure** — who sees it (internal roles, third parties, government-access risk).
6. **Deletion** — retention end-state, data-subject-rights workflow, hard-delete vs soft-delete.

A flow without all six hops named is not mapped; it's assumed. Force the enumeration.

### Step 2: Compute the regulatory-regime delta

For each hop × each applicable regime, name the obligation:

1. **Lawful basis / consent** — what's the basis for this hop under this regime; is it documented; is it user-affirmative where required.
2. **Notice** — what notice was given at the collection hop; does it cover the downstream hops.
3. **DPA / BAA / SCC** — for each sub-processor / cross-border hop, what contract is required; is it in place.
4. **Data-subject rights** — for each hop, can we deliver access / deletion / portability / objection within the regime's window.
5. **Breach-notification surface** — what's the notification timeline (GDPR 72 h, HIPAA 60 d, CCPA varies), to whom, with what content.

Gaps = obligations un-met. Surface them, don't smooth them.

### Step 3: Consent design read

For each lawful-basis claim:

1. *Is the basis defensible?* (legitimate-interest balancing test documented; consent freely given / specific / informed / unambiguous; contractual necessity actually necessary).
2. *Is withdrawal as easy as granting?* (GDPR Art. 7.3; CCPA opt-out parity).
3. *Are sensitive categories handled with explicit consent / authorization?*

Consent-as-checkbox-at-signup is the canonical failure mode. Inversion check: *"if a regulator inspects the consent flow tomorrow, what would they find un-defensible?"*

### Step 4: Breach-impact triage

For each data category × hop, size the breach tail:

1. **Volume** — how many subjects per hop.
2. **Sensitivity** — special-category / PHI / financial / identity-document presence.
3. **Notification surface** — 72-hour clock starts when; who notifies (us as controller, vendor as processor); content requirements.
4. **Regulatory-fine exposure** — GDPR up to 4 % global turnover or €20M; HIPAA tiered; CCPA per-record statutory damages.

A hop without a sized breach-tail is unstressed.

### Step 5: Validate the privacy read before emitting

Before producing the artifact, verify three things:

1. **Hop coverage** — confirm all six data-flow hops (collection, processing, storage, transfer, disclosure, deletion) were inspected; silent skips mean the flow was not mapped.
2. **Regime delta completeness** — assert every applicable regime was checked for lawful basis, notice, DPA/BAA/SCC, data-subject rights, breach notification; un-checked obligations are gaps in disguise.
3. **Counsel handoff** — verify the artifact explicitly flags which findings need privacy-counsel sign-off vs which are operational decisions; this skill does not replace counsel.

All three must pass. If any fails, return to the failing step.

### Step 6: Emit the privacy-review note

Produce the privacy-review artifact for the feature owner, legal / counsel, and DPO if applicable. The artifact is the non-lawyer cognition that prepares the counsel conversation and gates the ship decision; it is not the legal opinion.

## Related Skills

**WHEN to use this**

- Reviewing a new feature / integration / vendor data flow against applicable regulatory regimes.
- Re-scoping an existing flow under a new geography, segment, or processor.
- Sizing the breach-impact tail before a ship decision.

**WHEN NOT to use this**

- Contract-clause redline depth — route to [`contracts-cognition`](../contracts-cognition/SKILL.md) (P5); P5 composes this skill for data-clause sections.
- Data-classification / retention / cross-border judgment in isolation — route to [`data-handling-judgment`](../data-handling-judgment/SKILL.md) (P7); P7 is composed by this skill.
- Regulatory-regime floor read in general — route to `regulatory-regime` (J1); this skill cites J1, doesn't replace it.
- Legal privacy opinion — route to qualified privacy counsel.

## When the agent should load this

- "Is this GDPR-safe?"
- "Do we need a DPA / BAA / SCC for this vendor?"
- "What's the breach exposure on this data flow?"
- "Review the consent flow for the new signup."
- "Wir starten in der EU — was ändert sich datenschutzrechtlich?"

## Output

1. **`data-flow-map.md`** — six hops × what / who / where / how-long / who-else per hop.
2. **`regime-delta.md`** — applicable regimes × obligations × gaps per hop.
3. **`consent-design-note.md`** — lawful-basis defensibility, withdrawal parity, sensitive-category handling.
4. **`breach-impact-triage.md`** — sized tail per category × hop; notification clock; fine exposure.
5. **`counsel-handoff.md`** — findings that need counsel sign-off vs operational decisions.

## Gotcha

- "We're US-only, GDPR doesn't apply" is often wrong; GDPR follows the data subject, not the company.
- Consent checkboxes pre-ticked at signup are not consent under GDPR; this is a canonical regulator-attention pattern.
- Sub-processor chains drift silently; a vendor adds a sub-processor 6 months in and your DPA is stale.
- Retention defaults of "forever" interact badly with data-subject-rights timelines under every regime.

## Do NOT

- Do NOT issue privacy legal opinions; this skill prepares cognition for counsel, not replaces counsel.
- Do NOT collapse multiple regimes into the most familiar one; the floor is the strictest applicable.
- Do NOT skip breach-impact triage; un-stressed flows ship with un-sized tail.

## Runnable example

Growth-stage SaaS adds an EU customer cohort; existing US-only flow now serves EU data subjects.

- Step 0 — Bind regime: GDPR applies (EU data subjects); CCPA still applies for California subset; HIPAA n/a (no PHI).
- Step 1 — Map flow: collection (signup, EU IP), processing (US-east region), storage (US-east + analytics warehouse), transfer (US-east → analytics vendor in US-west; analytics vendor uses sub-processor in India), disclosure (internal CS team, no third parties), deletion (soft-delete, 7-year retention default).
- Step 2 — Regime delta: lawful basis missing for analytics (no opt-in); notice doesn't disclose Indian sub-processor; no SCC with analytics vendor; data-subject-rights workflow is manual ticket only; breach-notification process undocumented.
- Step 3 — Consent: signup checkbox is pre-ticked for marketing — fails Art. 7. Withdrawal requires support email — fails parity.
- Step 4 — Breach-impact: 12k EU subjects, no special categories, GDPR fine exposure up to 4 % global turnover; 72-hour notification clock with no documented owner.
- Step 5 — Validate: six hops mapped; both regimes checked; counsel-handoff names SCC + analytics-vendor sub-processor chain + consent UX redesign as counsel-led; retention default + DSR workflow as operational. Pass.
- Step 6 — Emit privacy-review note; gate EU launch on (a) SCC with analytics vendor; (b) consent UX redesign; (c) DSR workflow with named owner and 30-day window; (d) breach-notification runbook.
