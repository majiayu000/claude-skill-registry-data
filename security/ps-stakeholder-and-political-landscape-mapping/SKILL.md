---
name: ps-stakeholder-and-political-landscape-mapping
description: "Extends power/interest stakeholder mapping with the actor types specific to public-sector projects (elected officials, civil servants, unions, oversight bodies, citizens) and their distinct veto points and time horizons. Use when scoping an AI initiative for a public body and 'who's the sponsor' isn't a single, simple answer."
---

# Public-Sector Stakeholder and Political Landscape Mapping

## Purpose

`business-case-and-analysis:stakeholder-analysis-and-raci` gives the
general power/interest mapping method and RACI structure. In a public
organization, "who's the sponsor" rarely has one clean answer the way it
often does in a private company: authority is split across elected
officials, career civil servants, and sometimes external oversight
bodies, each on a different clock and answering to a different kind of
pressure. This skill adds the actor-type map and veto-point logic that
makes the generic method actually work in this setting.

## Method

### 1. Separate the four recurring actor types

| Actor type | What drives them | Typical veto point | Time horizon |
|---|---|---|---|
| **Elected officials / political leadership** | Re-election, public perception, party platform | Budget approval, public vote, policy sign-off | Election cycle (often 2-4 years) |
| **Civil servants / administration** | Operational continuity, legal defensibility, workload | Implementation sign-off, procurement process, day-to-day veto by inaction | Career-length, largely cycle-independent |
| **Unions / staff representative bodies** | Job security, working conditions, role change | Formal consultation rights where they exist, informal resistance | Contract-cycle length |
| **Oversight and audit bodies** | Legality, fairness, correct process | Can halt or reverse a decision after the fact | Reactive, triggered by complaint or audit |
| **Citizens / community groups / service users** | Direct impact on their access to a service | Public opinion, formal consultation, media attention | Immediate to long-term, depends on visibility |

Map every real stakeholder against these five types, not against a
generic "sponsor / influencer / user" template — the type determines
which lever actually moves them.

### 2. Locate every veto point before proposing a timeline

A private-sector project usually has one or two approval gates. A
public-sector AI initiative typically has several, often sequential and
non-negotiable in order: administrative sign-off, budget approval,
sometimes a formal consultation or union process, sometimes an oversight
or legal review, and only then implementation. List every veto point
this specific initiative will pass through and who holds it — a
timeline built without this list will be wrong, not just optimistic.

### 3. Read the political and administrative clocks separately

Elected leadership operates on an election cycle; a mid-cycle proposal
carries different risk than one made right after an election.
Administration operates largely independent of that cycle but is bound
by budget-year timing. When scoping a project, ask explicitly: where are
we in both clocks right now, and does that change what's fundable or
politically safe to propose this year versus next?

### 4. Distinguish formal power from practical influence

The nominal decision-maker (a board, a council) is not always the actor
whose informal buy-in actually determines the outcome. Career staff who
will operationally own the system after launch often have effective veto
power through implementation quality even without formal sign-off
authority. Map both the formal RACI and an informal "who can quietly
kill this" layer.

### 5. Feed into RACI, don't replace it

Once actor types and veto points are mapped, build the formal RACI in
`../../../../business-case-and-analysis/skills/stakeholder-analysis-and-raci/SKILL.md`
as normal — this skill's output (actor-type tags, veto-point list,
clock-position note) becomes input to that RACI, not a separate
deliverable that competes with it.

## What this skill does NOT do

- Doesn't replace the core RACI/power-interest method — it's an input
  layer for it.
- Doesn't tell you how to navigate procurement process itself — see
  `ps-procurement-and-public-funding-navigation`.
- Doesn't predict election outcomes or specific political dynamics —
  it structures the questions to ask locally, not a generic answer.

## Refinement notes

The five-actor-type table is a working synthesis for this pack. If the
owner has direct engagement experience with a specific type of public
body (municipal vs. national agency vs. regional administration), the
veto-point column should be refined with that experience rather than
left as a generic placeholder.

## Continue from here

- Formal stakeholder mapping: `../../../../business-case-and-analysis/skills/stakeholder-analysis-and-raci/SKILL.md`
- Procurement/funding constraints: `../ps-procurement-and-public-funding-navigation/SKILL.md`
- Presenting to the decision body once mapped: `../ps-decision-readiness-and-public-communication/SKILL.md`

## References

- `../../references/source-notes.md`

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
