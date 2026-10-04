---
name: ps-ai-opportunity-screening-for-public-value
description: "Screens a raw AI idea for public-sector fit before it enters formal opportunity scoring: checks mandate alignment, identifies which type of public value it targets, and runs the 'would this survive being on the front page' test. Use when a public-sector or non-profit client brings an AI idea and you need to know if it's worth taking to full scoring."
---

# Public-Sector AI Opportunity Screening

## Purpose

A fast pre-screen for an AI idea originating in, or aimed at, a public
sector, municipal, regional-administration, or non-profit context —
**before** it goes into `ai-strategy-and-governance`'s full 5-dimensional
scoring (Business Impact, Technical Feasibility, Data Readiness, Strategic
Alignment, Speed to Value/Risk). Private-sector opportunity screening
implicitly optimizes for revenue or cost impact; a public-sector idea can
score well on those dimensions and still be the wrong thing to build,
because its legitimacy depends on a different, largely non-financial set
of tests. This skill runs those tests first, so the idea that reaches
full scoring is one that's actually fit to be scored that way.

## Method

### 1. Check the mandate, not just the demand

A private company can chase almost any opportunity it can execute on. A
public body can only act within its statutory mandate and policy remit.
Before anything else:

- What law, policy, or governing document gives this organization the
  authority (or the obligation) to act here?
- Is this squarely inside the mandate, at its edge, or genuinely outside
  it (in which case it needs a different sponsor, or a policy change
  first)?
- If the idea comes from "we could technically do this," but no mandate
  clearly covers it, flag this explicitly — don't let technical
  feasibility substitute for legitimacy.

### 2. Identify which public-value type the idea targets

Public value doesn't reduce to one number the way private ROI often
does. Name the primary type(s) the idea targets — most real ideas target
one or two, not all four:

| Type | What it means | Example AI use |
|---|---|---|
| **Efficiency** | Same or better outcome at lower cost/time | Automating a permit-processing step |
| **Service quality** | Better experience or outcome for the same cost | AI triage that routes citizens to the right service faster |
| **Equity** | Closes a gap between groups, not just an average improvement | Multilingual AI assistant reducing access gaps for non-native speakers |
| **Trust / legitimacy** | Increases transparency, accountability, or confidence in the institution | AI-assisted audit trail on how a benefits decision was made |

If the idea can't name a primary type, that's a signal it's a
technology-first idea looking for a use case, not a use-case-first idea —
send it back for reframing before scoring.

### 3. Run the front-page test

Ask: if this AI system's most defensible, best-case version were
described accurately on the front page of a local newspaper, would it
read as a responsible use of public resources and public trust? This is
not a legal test (see `ps-regulatory-and-ethical-guardrails-for-public-ai`
for that) — it's a fast, non-technical gut check for ideas that are
legal but reputationally fragile: opaque decision-making about
individuals, anything that looks like surveillance without a clearly
stated purpose, or automation of a function citizens expect a human to
exercise judgment over.

### 4. Distinguish pilot-worthy from scale-worthy at this stage

In the public sector, a pilot serves a distinct function: it tests a
policy-aligned idea against real users without committing the full
budget or triggering full procurement, and its success is read against
policy goals as much as usage numbers. An idea can be very pilot-worthy
(cheap to test, high learning value, low commitment) while being a poor
candidate for full scoring and scaling right now, e.g. because its
funding case only closes if related infrastructure work lands first.
Mark explicitly which of these the idea is being screened *for* — a
pilot decision and a scale decision use different thresholds.

### 5. Hand off with the right framing

Once an idea passes steps 1-4, hand it to
`../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
for full scoring — but carry forward the named public-value type(s) from
step 2, since they should weight the Business Impact dimension there
(a high-equity, low-revenue idea can be a strong public-sector "Quick
Win" even though it would score weakly on a private-sector Business
Impact axis).

## What this skill does NOT do

- Doesn't replace full opportunity scoring — it's a pre-filter, not a
  substitute for `ai-opportunity-portfolio`.
- Doesn't assess legal or regulatory risk — see
  `ps-regulatory-and-ethical-guardrails-for-public-ai`.
- Doesn't map who needs to approve the idea — see
  `ps-stakeholder-and-political-landscape-mapping`.
- Doesn't make the mandate determination itself when it's genuinely
  ambiguous — flags it for the client's own legal/policy function.

## Refinement notes

The four public-value types (efficiency, service quality, equity, trust)
are a synthesis for this pack, not a single named external framework —
they draw on general public-value management literature (Moore's public
value framework is the closest named anchor) rather than one canonical
source. Treat as a working taxonomy, refine if the owner has a preferred
alternative framing from direct client work.

## Continue from here

- Full scoring: `../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
- Business case with public-value framing: `../ps-public-value-business-case-framing/SKILL.md`
- Who needs to say yes: `../ps-stakeholder-and-political-landscape-mapping/SKILL.md`
- Legal/regulatory triage: `../ps-regulatory-and-ethical-guardrails-for-public-ai/SKILL.md`

## References

- `../../references/source-notes.md` — sourcing for the pilot-vs-scale
  framing in step 4.

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
