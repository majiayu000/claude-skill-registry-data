---
name: bmc-operational-risk-scanning
description: "Reads Key Partners, Key Activities, and Key Resources as an operational risk and third-party access surface — not just an operating description — to catch vendor-access, concentration, and bus-factor vulnerabilities that standard BMC facilitation misses."
---

# BMC Operational Risk Scanning

## Purpose

The BMC's left side (Key Partners, Key Activities, Key Resources) is
normally filled in as a description of how the business operates. Read
differently, it's also a map of where the business is exposed: which
third parties can touch sensitive data, which single points of failure
exist, which dependencies would hurt if they disappeared tomorrow. This
skill applies that second reading deliberately, surfacing risks that a
standard "how do we operate" facilitation pass doesn't ask about. Use it
once the left-side blocks have a first draft, as a distinct pass from
normal BMC facilitation — not folded silently into it.

## Anchored in research

This specific application — reading the BMC's own structure as a risk
surface — is this pack's own synthesis; no single named external
technique does exactly this. The risk categories and control-gap logic
below are grounded in general operational and third-party/vendor risk
management practice, anchored to ISO 31000 (the same risk-management
standard already cited in `business-case-and-analysis`, this pack's
sibling for formal risk scoring).

## Method

1. **For each Key Partner, ask four questions:**
   - What data or system access does this partner actually have, and is
     it scoped to what they need, or broader?
   - Is there a monitoring or contractual control matching that access
     level (audit rights, access logging, a data processing agreement),
     or is the access effectively unsupervised?
   - What happens to the business if this partner fails, is breached, or
     exits the relationship — is there a fallback, or is this a single
     point of failure?
   - Is this a concentration risk — does a large share of a critical
     function run through one partner with no realistic alternative?
2. **For each Key Activity, ask two questions:**
   - Is this activity dependent on one person or one small team, such
     that their absence would stop it (a "bus-factor" risk)?
   - Is this activity regulated or safety-critical, such that a failure
     has consequences beyond the business's own operations (customer
     harm, legal exposure, regulatory penalty)?
3. **For each Key Resource, ask two questions:**
   - Is this resource irreplaceable or hard to re-source on short notice
     — specific IP, a uniquely skilled person, a sole-source input, a
     specific dataset with no substitute?
   - What's the concentration risk if this exact resource were lost —
     does the business have any real continuity plan, or does the whole
     model depend on this one thing continuing to exist exactly as it
     is?
4. **Build a simple risk register from the scan** — one row per
   partner/activity/resource with a flagged issue:
   `item → risk type (access / concentration / bus-factor / regulatory)
   → severity (rough judgment) → existing control, if any → the gap`.
   This register doesn't need formal probability×impact scoring yet —
   its job is to make risks canvas-visible, not to fully quantify them.
5. **Flag the two highest-value findings explicitly, every time:**
   partners with unmonitored access to sensitive customer data (the most
   common overlooked risk in practice), and activities or resources that
   would need to keep working today with zero warning if a key partner
   walked away tomorrow.
6. **Hand off anything material for formal treatment.** Once a risk is
   identified here, it should move to
   `business-case-and-analysis/risk-matrix-and-mitigation` for proper
   probability×impact scoring and a documented mitigation plan — this
   skill's job is to FIND canvas-visible risks efficiently, not to fully
   quantify or resolve them.

## What this skill does NOT do

- Doesn't replace a formal security audit, vendor risk assessment, or
  compliance review — it's a fast diagnostic lens applied during BMC
  work, not a substitute for those processes when the stakes justify
  one.
- Doesn't score or prioritize risks with the rigor of
  `business-case-and-analysis/risk-matrix-and-mitigation` — this skill
  finds and lists risks; that skill scores and mitigates them.
- Doesn't cover risks that live outside the left-side blocks (market
  risk, competitive risk, regulatory risk to the business model itself)
  — those are covered elsewhere in this pack and in
  `opportunity-recognition/competitive-and-five-forces-mapping`.

## Refinement notes

- What's the most common unmonitored-access risk you've actually found
  hiding in a client's Key Partners block?
- Have you seen a bus-factor risk (Step 2) actually materialize for a
  client? What changed afterward?
- Is there a risk category missing from this scan that you routinely
  check for in practice?

## Continue from here

- Use once: Key Partners, Key Activities, Key Resources have a first
  draft.
- Feeds into: `../../../../business-case-and-analysis/skills/risk-matrix-and-mitigation/SKILL.md`
  for formal scoring and mitigation planning.
- Related: `../../../../opportunity-recognition/skills/competitive-and-five-forces-mapping/SKILL.md`
  for risks outside the left-side blocks.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../references/bmc-resilience-heuristics-research.md` — selection and grounding notes for this skill and its siblings
- `../../CLAUDE.md` — this pack's shared guardrails
