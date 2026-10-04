---
name: hitl-maturity-and-confidence-routing
description: "Classifies an AI process against a four-level Human-in-the-Loop maturity model (Smoke-and-Mirrors, Reactive HOTL, Intentionally Designed, Collaborative Intelligence) and designs a confidence-score routing table that sends work to automation, assisted validation, or human escalation — with the override-rate red flags that catch a stalled or fake HITL setup and a named accountable calibration owner."
---

# HITL Maturity & Confidence Routing

## Purpose

Moves "a human checks it" from a vague promise to an assessable, designed
architecture. Most organizations describe their human oversight in
aspirational terms ("we have a human in the loop") without ever checking
which of four very different maturity levels that claim actually
corresponds to — and the gap between the claimed level and the real one is
usually invisible until something goes wrong. This skill classifies the
current state, designs the routing logic that should replace it, and names
who is accountable for keeping it calibrated.

## Anchored in research

- Su Belagodu (Managing Partner, Intellectus Advisors; former product
  leadership at Pegasystems, IBM, Wipro) — a four-level HITL maturity model
  and a confidence-score routing table, presented in her public "Humans +
  AI = Impact" HITL series. Her general focus on HITL maturity and
  override-rate diagnostics is independently confirmed; the exact wording
  of quotes attributed to her in the source material for this skill could
  not be independently verified word-for-word — treat the *structure* of
  the model as reliably sourced and any verbatim quote as illustrative
  paraphrase, not a confirmed direct quote.
- Databricks engineering blog, "What is Human-in-the-Loop (HITL)?" — used
  as an independent, verifiable industry anchor for the general HITL
  maturity concept, so this skill doesn't rest on a single named source.
- The human-in/on/outside-the-loop model already used in this repo (see
  `../../../specialisation-packs/ai-native-startup-design/skills/closed-loop-process-and-human-oversight-design/SKILL.md`)
  as this skill's simpler predecessor layer — this skill is the deeper,
  operational version for a process that's already live.

## Method

1. **Classify the process's current state against four maturity levels** —
   be honest about where it actually is, not where the team believes it is:
   - **Level 0 — Smoke and Mirrors (Automation First).** A human is
     nominally "in the loop" but rarely exercises real judgment. Diagnostic
     sign: the override rate is below 5%, which usually means reviewers
     have stopped exercising critical judgment and are rubber-stamping AI
     output — a dangerous form of automation bias, not evidence the AI is
     simply that good.
   - **Level 1 — Reactive (Human-on-the-Loop).** A human monitors and
     intervenes only after an error has already happened. This is
     exhausting "babysitting automation" that catches mistakes but doesn't
     systematically improve the process.
   - **Level 2 — Intentionally Designed HITL.** Routing is explicit and
     rule-based: confidence scores determine whether a case is automated,
     sent for assisted validation, or escalated to a human — see the
     routing table in step 3.
   - **Level 3 — Collaborative Intelligence (AI-in-the-Loop).** The
     relationship inverts: the AI is now the assistant. It surfaces rich
     context, comparable cases, confidence scores, and its own reasoning
     transparency; the human makes the final call with full information.
     This is the target state for high-stakes, expertise-dependent
     workflows — not a universal goal for every process (see "What this
     skill does NOT do").
2. **Don't take a claimed level at face value — check it against usage
   data.** A team that describes itself as Level 2 or 3 but whose override
   rate sits under 5% is very likely still operating as Level 0 in
   practice. Cross-check the claimed level against
   `../hitl-override-metrics-and-feedback-audit/SKILL.md`'s override-rate
   measurement before accepting a self-reported maturity level.
3. **Design the confidence-score routing table** for the specific process
   being designed, using this as a starting structure — adjust the
   thresholds to the process's actual risk profile, don't treat 80/60 as a
   universal constant:

   | Confidence score | Routing decision | Human's role |
   |---|---|---|
   | 80–100% | Automated | Process runs unattended; random-sample audits catch drift |
   | 60–79% | Assisted validation | AI proposes, human confirms before it proceeds |
   | Below 60%, or flagged high-stakes regardless of score | Escalate to human | Human decides; the system must supply reasoning transparency (what the AI considered, and why it's uncertain), not just the raw score |

4. **Name a single accountable calibration owner** — a "Chief Calibration
   Officer" role in spirit, not necessarily title: one named person or
   small team responsible for reviewing where the thresholds and routing
   rules are drifting, and for balancing experimentation, risk management,
   and the development of the humans doing the reviewing. Don't leave
   calibration as "everyone's job," which in practice means no one's.
5. **Design the one-click override as a hard requirement, not an
   afterthought.** If undoing or correcting an AI suggestion takes more
   than one deliberate action, experts will route around the system rather
   than through it, and the override-rate metric in step 6 stops being
   trustworthy (people stop bothering to record disagreement they can't
   act on cheaply).
6. **Track the override rate as an ongoing health signal, not a one-time
   design check** — hand this off to
   `../hitl-override-metrics-and-feedback-audit/SKILL.md` for the full
   audit methodology. As a first-pass rule: below ~5% signals automation
   bias risk (investigate before trusting it); above ~30% signals the
   model isn't yet fit for the task at this confidence threshold.
7. **Watch for the "Clippy 2.0" anti-pattern.** Don't over-personify the
   AI (a name, a face, chatty first-person language) in ways that make its
   real capability and confidence level harder for the human to judge
   accurately. A collaborator the human trusts appropriately needs to look
   exactly as reliable as it is — no more comforting, no less.
8. **Produce a structured output**: current maturity level (with the
   evidence for it, not just the claim), target level and why that target
   — not necessarily Level 3 — is the right one for this process, the
   confidence-score routing table, the named calibration owner, and the
   override-rate baseline to track going forward.

## What this skill does NOT do

- Doesn't assume Level 3 (Collaborative Intelligence) is always the goal —
  a low-stakes, high-volume, well-understood task may be entirely
  appropriate at Level 2's rule-based routing, or even a well-audited
  Level 0-adjacent automation once its accuracy is genuinely proven, not
  assumed.
- Doesn't implement the technical confidence-scoring model itself (the
  underlying classifier/model that produces the 0–100% number) — that's a
  data-science and engineering task; this skill designs what happens with
  the score once it exists.
- Doesn't replace
  `../../../specialisation-packs/ai-native-startup-design/skills/closed-loop-process-and-human-oversight-design/SKILL.md`'s
  simpler three-tier model for early-stage product design, before a
  process has real usage data to calibrate against.
- Doesn't perform the regulatory/ethics risk check — see
  `../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
  for whether human-oversight obligations are legally required, not just
  operationally wise.

## Refinement notes

Areas to keep deepening with real practice:

- your own calibrated thresholds by task type — the 80/60 split above is a
  starting structure, not a validated universal rule
- concrete examples of a claimed maturity level that didn't survive an
  override-rate check, and what that revealed
- your own template for naming and scoping the calibration-owner role in a
  client organization (into `../../references/`)

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Simpler predecessor model: `../../../specialisation-packs/ai-native-startup-design/skills/closed-loop-process-and-human-oversight-design/SKILL.md`
- Applied to content specifically: `../../../ai-strategy-and-governance/skills/ai-output-curation-and-quality-control/SKILL.md`
- Next in this pack (specify how the AI behaves within the routing this
  skill designs): `../ai-behavioral-specification-design/SKILL.md`
- Next in this pack (verify the routing is actually working):
  `../hitl-override-metrics-and-feedback-audit/SKILL.md`
- Related skill in this pack (draw the hard boundary the routing table
  must never cross): `../expert-agency-and-apprenticeship-protection/SKILL.md`
- Related skill in another pack: `../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/hitl-partnership-heuristics-research.md` — full
  sourcing and grounding-strength notes for this pack
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
