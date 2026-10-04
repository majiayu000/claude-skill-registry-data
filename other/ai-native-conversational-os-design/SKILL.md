---
name: ai-native-conversational-os-design
description: "Designs the conversational UI architecture for an AI-native product in six stages — Intent, Strategy Cards, Clarification, Output Cards, Mission, Agent Execution — applying five AI-first product principles (click > question, menus > prompts, dashboards > dialogue, manual actions > agents, screens > chat + cards)."
---

# AI-Native Conversational OS Design

## Purpose

Provide a concrete, reusable architecture model for how an AI-native
product is built as a UI that is NOT a traditional collection of
screens/menus/dashboards but a conversational operating system: the
user's intent is recognized, the right internal "strategy" is selected,
clarifying questions are asked when needed, structured output cards are
produced, one clear mission is given, and an agent can continue the work
autonomously. Core message: "your product is no longer a set of screens.
It's a thinking partner."

## Based on

- The methodology of an external "AI-first SaaS Product" workshop,
  applied by the owner to one own case
  ("Decision Coach" MVP) — see `../../references/ai-first-saas-workshop-source.md` and the worked example `../../cases/ai-decision-coach-mvp-case.md`,
  section 8. **Note:** applied only once so far — not broadly validated
  across multiple different products.
- The workshop's "5 shifts" principles for designing an AI-first product
  (see the start of the Method section).

## Method (draft — to be filled in further)

### A. Five AI-first product principles (mindset before architecture)

Before designing the OS flow, internalize these five shifts from old SaaS
thinking to AI-native thinking:

1. **Click → question.** The user doesn't navigate menus to find the
   right function — they ask for what they want, and the system finds the
   right function.
2. **Menus → prompts.** Instead of fixed menu structures, the user
   expresses their intent in natural language.
3. **Dashboards → dialogue.** Instead of browsing information, information
   is brought to the user through conversation, at the right time, in the
   right context.
4. **Manual actions → agents.** The user doesn't perform every step
   themselves — an agent performs them, the user directs and approves
   (see `../closed-loop-process-and-human-oversight-design/SKILL.md` for
   choosing the level of human oversight).
5. **Screens → chat + cards.** The UI isn't a fixed collection of screens
   but a dynamic combination of conversation and structured information
   cards that appear as needed.

The shared conclusion of these five shifts: the product is no longer a
set of screens, it's a thinking partner.

### B. Six-stage OS flow

1. **Intent (user → system).** Identify WHY the user is here and what
   they want clarity on. Explicitly list the main intents your product
   supports (typically 3-6) — don't try to support an unlimited range of
   free-form requests in an MVP. Identify the dominant intent and pass it
   to the strategy layer.
2. **Strategy Cards (system → internal reasoning layer).** Define
   "playbooks" (strategy cards) the AI can choose from based on the
   user's intent. Each card is an independent reasoning module: what it
   interprets, what it produces (e.g. a 0-100 score, a classification, a
   reworded text). Design as many cards as the MVP's differentiator and
   table-stake needs require (see `../customer-vision-to-jtbd/SKILL.md`)
   — no more.
3. **Clarification (interactive micro-questions).** Ask AT MOST 2-4
   clarifying questions, only when (a) the input is too vague to
   interpret, or (b) the wrong strategy card has been activated. Keep the
   questions light and fast — this isn't a form, it's a refinement.
4. **Output Cards (core MVP results).** Design standardized, structured
   card formats in which the user receives the result of each strategy
   card execution (e.g. a score + a "why this score" rationale + "what
   would improve it"). Each output card should directly fulfill one of
   the MVP's differentiator or table-stake needs.
5. **Mission (AI summarizes the plan + the next step).** One short
   mission statement at the end of the session that frames the next
   steps around building trust and reducing uncertainty — not a long
   summary, but one concrete, action-driving sentence.
6. **Agent Execution (system → autonomous action).** After the mission
   statement, an agent can continue independently: updating scores as new
   information arrives, rewriting material, recommending existing
   tools/resources. The agent's job is to create forward momentum — not
   just answer a question and stop.

### C. Design checklist

7. **Test the flow end to end before building.** Write out one concrete
   user journey from the Intent stage to the Agent Execution stage in
   words (not code) — if any step feels forced or artificial, simplify
   the structure before the build phase.
8. **Feed the flow into `../ai-buildable-prd-writing/SKILL.md`'s "Core
   Features" section** — each stage of the OS flow (Strategy Card, Output
   Card) is one PRD feature line, described as an outcome ("the user
   gets...") rather than a technical implementation.

## What this skill does NOT do

- Does not include a technical orchestration implementation (prompt
  chaining, state, API interfaces) — it produces the conceptual
  architecture, which is handed to the build agent via the tool chosen
  through `../ai-native-tool-stack-selection/SKILL.md`.
- Does not replace `../closed-loop-process-and-human-oversight-design/SKILL.md`
  for deciding the human oversight level for the Agent Execution stage —
  use it alongside this skill to decide the in/on/outside-the-loop level
  for each agent action.
- Does not fit every product — if the product is genuinely
  tool-/dashboard-type (e.g. data visualization, continuous monitoring
  without conversational decision-making), this model forces the wrong
  shape. Use it only when the core value is AI interpretation/reasoning,
  not displaying data.

## Refinement notes

This skill has so far been applied to one case (the owner's Decision
Coach). As you apply it to more products, add:

- your own observations on when the 6-stage model needs to be simplified
  (e.g. if the Strategy Cards layer proves oversized for a small MVP)
- concrete examples of other OS flow designs in the `../../cases/` folder
- observations on how the flow performed in practice after the first
  build iteration (which stage produced the most user value, which
  proved unnecessary)

Once this section has been filled in with multiple cases, raise
`skills_index.json`'s `maturity` field to `validated`
(see `../../../../meta/maturity_levels.md`).

## Continue from here

- Preceding skill in this pack:
  `../rice-scoring-and-mvp-synthesis/SKILL.md` — produces the chosen MVP
  for which the OS flow is designed.
- Next skill in this pack: `../ai-buildable-prd-writing/SKILL.md`
  — feeds the OS flow into the PRD's Core Features section.
- Related skill in this pack:
  `../closed-loop-process-and-human-oversight-design/SKILL.md` —
  choosing the human oversight level for the Agent Execution stage.
- Related skill in another pack:
  `../../../../business-design-frameworks/skills/customer-journey-and-ai-touchpoint-mapping/SKILL.md`
  — a complementary way to structure the same product as a customer
  journey rather than an OS architecture.
- Worked example: `../../cases/ai-decision-coach-mvp-case.md`, section 8.
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-first-saas-workshop-source.md` — source information
- `../../cases/ai-decision-coach-mvp-case.md` — worked example
- `../../CLAUDE.md` — the pack's shared guardrails
