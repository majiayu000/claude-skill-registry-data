---
name: customer-vision-to-jtbd
description: "Structures a preliminary, free-form business vision into a customer profile (ICP), a Jobs-To-Be-Done analysis, and 5+2 need themes, scores them with a 5-criteria NMB+AI-advantage model, and selects an AI differentiator need (AI wedge) for further development."
---

# Customer Vision to JTBD

## Purpose

Turn a free-form, even unstructured vision of a product and customer into
structured customer understanding before writing the PRD: who the
customer is (ICP), what they're really trying to accomplish (JTBD), what
needs lie beneath that (Need Themes), and where AI brings the biggest
competitive advantage. The principle is to start from the customer, not
the technology — a spec never starts from a technical description.

## Based on

- The owner's AI-native Business Design workshop
  (the owner's own workshop), run 1–2 June 2026, Day 1 —
  Session 2 "Planning in the AI Era", steps 1–3 (vision → design
  partner → ICP/JTBD/Need Themes/AI-advantage scoring).
- The methodology of an external "AI-first SaaS Product" workshop (applied
  by the owner to one own case, see
  `../../references/ai-first-saas-workshop-source.md` and
  `../../cases/ai-decision-coach-mvp-case.md`) — deepens this skill's
  steps 5–7: verb-driven JTBD phrasing, a more detailed 5-criteria
  NMB+AI-advantage score (replacing the earlier single AI-advantage
  score), and an explicit AI wedge selection criteria set. **Note:** this
  deepened part has so far been applied only once (the owner's own case)
  — not as broadly validated as the skill's ICP/JTBD backbone, which is
  based on a multi-participant workshop.
- Ideal Customer Profile (ICP) and Jobs-To-Be-Done (JTBD) product-strategy
  frameworks (generally known, not the owner's own — the workshop applies
  them within a prompt chain run with an AI thinking partner).
- See `../../references/workshop-source.md` and
  `../../references/prompt-library.md` (prompts 3–6).

## Method

1. **Write a free-form vision.** Open a blank document and write
   freely: what is the customer's need, how does the service work from
   the customer's perspective, how significant is the problem, how does
   the customer use the service, what are your own values/principles/
   focus. It doesn't need to be logical or in order — disconnected
   thoughts and unfinished sentences are acceptable. The goal is to get
   your own thinking out into a form the AI can work with.
2. **Hand the vision to the AI thinking partner for sharpening**
   (`../../references/prompt-library.md`, prompt 3): ask it to state what
   is still unclear and needs a decision, ask at most 7 clarifying
   questions in priority order, and surface assumptions worth checking.
   Don't ask for a plan yet — at this stage the goal is sharpening your
   thinking.
3. **Ideal Customer Profile (ICP).** Ask the AI to sketch out multiple
   customer profiles that have this problem most strongly, describe each,
   and prioritize who to serve first and why.
4. **Jobs To Be Done (JTBD) — verb-driven.** Dig into the customer's real
   behavior and the situation in which the problem needs to be solved,
   and what they're really trying to achieve — look past the product to
   the customer's true goal. Phrase every JTBD starting with a verb, as a
   problem-/solution-independent *progress* ("figure out", "assess",
   "translate" — not "gets a dashboard" or "uses feature X"). Produce
   typically 5-8 JTBDs. Test: a JTBD should remain true even if the whole
   product changed into a completely different solution.
5. **Distill into 5+2 Need Themes.** Convert the JTBD analysis into 5
   functional and 2 psychological themes in table form. Each theme is a
   one- or two-word noun phrase that captures the core of the need (e.g.
   *affordability*, *reliability*, *confidence*). Use a four-column
   table: Need Theme / Type (Functional: Understand, Diagnose/Evaluate,
   Plan/Structure, Communicate, Decide/Act — or Psychological: Confidence,
   Uncertainty Reduction) / Underlying "why" / Related JTBD(s). See the
   worked example `../../cases/ai-decision-coach-mvp-case.md`, section 2.
6. **NMB + AI-advantage scoring — 5 criteria, not one.** Score each need
   theme on five criteria, each 1–5:
   - **Need Depth** — how deep/acute the need is when it's triggered.
   - **Frequency** — how often the customer encounters this need.
   - **Market Coverage** — how broadly the need touches the target market.
   - **Business Strength** — how strong YOUR OWN starting position is for
     serving this need (data, experience, existing tools).
   - **AI Advantage** — how much competitive advantage AI brings to
     serving this particular need (a genuine differentiator, not a
     nice-to-have).
   Calculate a total score (max 25) and classify each need theme as a
   **Differentiator** (high total score, competitors don't cover it well)
   vs. a **Table Stake** (necessary but generic competitors/other AI tools
   are available). See the worked example
   `../../cases/ai-decision-coach-mvp-case.md`, section 3.
7. **Select the AI differentiator need ("AI wedge").** The AI wedge is a
   need theme that SIMULTANEOUSLY satisfies: high Need Depth, high
   Frequency, weak Market Coverage among competitors, high own Business
   Strength, AND high AI Advantage. This is the one (or two) need(s)
   around which solution ideation (see
   `../ai-differentiator-solution-ideation/SKILL.md`) is built — don't try
   to serve all Differentiator-level needs at once.
8. **(Deepening, optional) Deep research.** Use an AI tool's deep
   research mode to deepen your understanding of the customer/problem,
   competing solutions, and market/research data before solution
   ideation. The result is a research draft with reports and references —
   not a final truth.
9. Carry the result (ICP + JTBD + Need Themes + NMB score + chosen AI
   wedge) into `../ai-differentiator-solution-ideation/SKILL.md` as the
   basis for ideating solution directions — or directly into
   `../ai-buildable-prd-writing/SKILL.md` if the solution direction is
   already clear and the ideation stage isn't needed.

## Gotchas

- Phrasing a JTBD around the product instead of the customer's progress
  ("gets a dashboard", "uses feature X") fails the method's own test: a
  JTBD should stay true even if the whole product changed into a
  completely different solution — if it doesn't, it's not verb-driven
  and solution-independent yet.
- A need theme can score well overall and still not be the AI wedge —
  step 7 requires it to SIMULTANEOUSLY hit high Need Depth, high
  Frequency, high own Business Strength, high AI Advantage, AND weak
  Market Coverage among competitors. A need with four strong criteria
  but a market competitors already cover well is a Table Stake, not a
  wedge.
- Deep research output (step 8) is a research draft, not verified fact
  — carrying its claims straight into the PRD without checking primary
  sources contradicts the skill's own "does NOT do" caveat.
- The 5-criteria NMB+AI-advantage scoring and AI wedge selection logic
  (steps 5-7) come from an external workshop the owner has so far
  applied to only one case — treat that part as less battle-tested than
  the ICP/JTBD backbone, which rests on a multi-participant workshop.
- Skipping the free-form vision step (step 1) and starting straight from
  a structured ICP/JTBD template reintroduces a technology-first
  framing — the whole point of step 1 is to get unstructured customer
  thinking down before any structure is imposed.

## What this skill does NOT do

- Does not replace real customer research or interviews — the AI
  structures your thinking and existing knowledge, it doesn't produce new
  empirical customer data.
- Does not make the final ICP or priority choice for you.
- Deep research results are a research draft — verify primary sources
  before carrying them into the PRD or decision-making.

## Continue from here

- Preceding skill in this pack: `../ai-native-opportunity-scan/SKILL.md`
- Next skill in this pack:
  `../ai-differentiator-solution-ideation/SKILL.md` — ideates 3 solution
  directions for the chosen AI wedge. (If the solution direction is
  already clear, you can go directly to
  `../ai-buildable-prd-writing/SKILL.md`.)
- Related skill in another pack:
  `../../../../opportunity-recognition/skills/opportunity-value-assessment/SKILL.md`
- Worked example: `../../cases/ai-decision-coach-mvp-case.md` — the full
  own case for steps 4–7.
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/prompt-library.md` — prompts 3–6
- `../../references/workshop-source.md` — source information (AI-training-P6)
- `../../references/ai-first-saas-workshop-source.md` — source information
  (external workshop, NMB scoring and AI wedge deepening)
- `../../cases/ai-decision-coach-mvp-case.md` — worked example
- `../../CLAUDE.md` — the pack's shared guardrails
