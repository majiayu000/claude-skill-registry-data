---
name: data-literacy-competency-assessment
description: "Assesses an organization's or team's data literacy with a four-quadrant framework (Understanding data, Acting on data, Engaging through data, Ethics & privacy) and a four-step maturity ladder, differentiated by role. Use before launching a data strategy or AI initiative, when you need to identify which competency gap is blocking data exploitation."
---

# Data Literacy Competency Assessment

## Purpose

Data literacy doesn't mean everyone needs to know how to write SQL
queries. It means the ability to understand, evaluate, and apply data in
decision-making. When an AI or data initiative fails for organizational
reasons (not technical ones), the cause is often a competency gap in one
of four areas — not the tool. This skill produces a structured assessment
of where the gap is, and at what organizational level, so development
effort is aimed correctly instead of "training everyone on everything."

## Anchored in research

- A DALI-type data literacy framework (a synthesis of multiple sources,
  from citizen- and professional-level data literacy definitions): four
  core elements — Understanding data, Acting on data, Engaging and
  influencing through data, and Ethics & privacy as a cross-cutting theme.
- Ackoff, Russell L. — the DIKW hierarchy (*Data, Information, Knowledge,
  Wisdom*, 1989) underlying the maturity ladder: data itself isn't
  knowledge, knowledge isn't understanding, understanding isn't the
  wisdom to act correctly.
- DAMA International — DAMA-DMBOK (Data Management Body of Knowledge) as
  the professional standard defining data governance competency (a
  professional-body standard in the same vein as BABOK/PMI/SFIA
  elsewhere in this repo).

## Method

1. **Assess the four areas separately** — don't produce a single overall
   score, because an organization is typically uneven across areas:
   - **A. Understanding data:** is it understood what data is, where it
     comes from, who owns it, and that "data is a representation of
     reality, not reality itself" (see
     `../data-bias-and-quality-critical-reading/SKILL.md`)?
   - **B. Acting on data:** can data quality be assessed, can misleading
     reporting be spotted, and does data actually drive decisions and
     behavior change — or is it "nice-to-know" metrics being collected
     that lead nowhere?
   - **C. Engaging through data:** can data be synthesized, visualized,
     and told as a story that gets a decision-maker to act (see
     `../data-storytelling-and-business-translation/SKILL.md`)?
   - **D. Ethics & privacy:** are the ethical and legal boundaries of
     collecting and using data understood (especially in AI models) —
     this is a cross-cutting theme across the other three, not a
     separate stage.
2. **Use a four-step maturity ladder for each area:**
   - **Level 1 — Unaware:** data is used without questioning its origin
     or limitations.
   - **Level 2 — Aware:** limitations are recognized, but not
     systematically factored into decisions.
   - **Level 3 — Applying:** limitations are systematically factored in,
     data repeatedly leads to correct decisions.
   - **Level 4 — Embedded:** data literacy is part of the organization's
     default way of operating, not a separate skill that has to be
     consciously invoked.
   Score each area (A-D) at level 1-4 separately — an organization can be
   at level 3 in Understanding but level 1 in Engaging.
3. **Differentiate the assessment by role** — the same data literacy
   requirement doesn't apply to everyone:
   - **Leadership/decision-makers** need C (Engaging — able to demand and
     interpret data as a story) and D (Ethics — accountable for
     decisions) above all.
   - **Analysts/data professionals** need A (Understanding) and B
     (Acting) in depth above all.
   - **Line managers/end users** need a sufficient level of A (able to
     question) and D (able to spot ethical risks in their own work) —
     not necessarily deep B/C competency.
   If the whole organization is trained on the same program regardless of
   role, that's the most common way data literacy investment gets wasted.
4. **Identify the biggest bottleneck; don't try to fix everything at
   once.** The data literacy chain is only as strong as its weakest
   link: if leadership is at level 1 in Engaging (C), the best analysis
   (A/B at level 4) never leads to a decision, because it can't be
   interpreted or trusted. Prioritize development effort based on where
   the weakest link is by area/role, not where it's easiest to train.
5. **Produce the assessment as a table:** role × area (A-D) × level
   (1-4) × the biggest observed risk in that cell. This table is the
   skill's primary output, not a long narrative description.

## What this skill does NOT do

- Doesn't design the training program or its content itself — produces a
  diagnosis on which the training or other development effort is
  designed separately.
- Doesn't assess individual people's competency by name — assesses roles
  and organizational levels, not individuals.
- Doesn't replace a technical assessment of data architecture or
  infrastructure — assesses people's ability to use and interpret data,
  not the technical condition of systems.
- Doesn't confirm figures or maturity levels from memory — bases the
  assessment on observations you provide (interviews, surveys,
  observation) or marks an assumption clearly (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- a concrete interview/survey template for assessing the level of each
  area (A-D) (into `../../references/`)
- your own observations about which role/area combination is most often
  the weakest link across different industries
- examples of how imbalanced data literacy (e.g. strong analytics, weak
  leadership engagement) has blocked a project from moving forward

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack (if area C is weak):
  `../data-storytelling-and-business-translation/SKILL.md`
- Next in this pack (if area A is weak):
  `../data-bias-and-quality-critical-reading/SKILL.md`
- Related skill in another pack: `../../../change-and-communication/skills/workshop-and-facilitation-design/SKILL.md`
  — if a training/facilitation session is being designed based on the
  diagnosis.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
