---
name: ai-native-opportunity-scan
description: "Uses an agentic/closed-loop lens to find genuinely new AI-enabled business opportunities in your own startup case, and scores/prioritizes the findings by feasibility and the smallest prototypeable version."
---

# AI-Native Opportunity Scan

## Purpose

Find areas within your own startup case where AI enables something
genuinely new — not just speeding up existing work. This skill uses a
two-stage prompt chain with an AI thinking partner: first identifying
five opportunities enabled by agentic/closed-loop-level AI, then
pressure-testing and prioritizing them by business potential, customer
value, and feasibility — arriving at one opportunity that is carried into
the next stages of design.

## Based on

- The owner's AI-native Business Design workshop
  (the owner's own workshop), run 1–2 June 2026, Day 1 — Session 1
  "The New AI Mindset" exercise and the core distinction preceding it: AI
  is not just a productivity tool that speeds up existing work — it's a
  new capability and capacity that enables products and workflows that
  were previously too slow, too costly, or impossible.
- See `../../references/workshop-source.md` (source information) and
  `../../references/prompt-library.md` (prompts 1–2, the basis of this
  skill).

## Method

1. **Make sure the AI thinking partner has your own business context
   available** — a project (Claude/ChatGPT) with your pitch, business
   plan, customer notes, etc. loaded. Without this, findings stay generic
   ("automate customer service with an AI agent"-type suggestions).
2. **Run the discovery prompt** (`../../references/prompt-library.md`,
   prompt 1): ask the AI to identify 5 areas where AI would create
   GENUINELY NEW business opportunities — not "do X faster" but new
   features, products, workflows, or business models. Require
   agentic/closed-loop-level thinking rather than basic productivity use
   (see `../closed-loop-process-and-human-oversight-design/SKILL.md` for
   a more detailed distinction).
3. For each of the five findings, capture: a name, a description (2-3
   sentences), why it's newly possible thanks to AI, and what would need
   to be true for us to do this.
4. **Write your own preliminary assessment before the pressure-test
   stage.** This forces your own thinking before the AI's assessment —
   the workshop's principle: think for yourself first, don't let the AI
   assess on your behalf without your own view.
5. **Run the pressure-test/prioritization prompt**
   (`../../references/prompt-library.md`, prompt 2): ask for an
   assessment of each of the five on: business potential, customer value,
   feasibility for a small team with current AI tools
   (low/medium/high), and the smallest version that could be
   prototyped this week.
6. Ask for a ranking of 1–5 with rationale, and a recommendation for
   which to prototype first.
7. Choose one opportunity to carry forward — feed it into
   `../customer-vision-to-jtbd/SKILL.md` and
   `../ai-buildable-prd-writing/SKILL.md`.

## Gotchas

- Running the discovery prompt without the AI thinking partner having
  your actual business context loaded (pitch, business plan, customer
  notes) produces generic "automate customer service with an AI
  agent"-type findings that only look like real opportunities — the
  method calls this out directly as the default failure mode.
- Skipping step 4 (writing your own preliminary assessment before the
  pressure-test prompt) silently defeats the point of that step: the
  workshop's principle is to think for yourself first, not let the AI's
  scoring become the only judgment in the room.
- The five findings from the discovery prompt can end up being
  faster/cheaper versions of existing work rather than genuinely
  agentic/closed-loop opportunities unless prompt 1's requirement is
  enforced — cross-check candidates against
  `closed-loop-process-and-human-oversight-design/SKILL.md`'s open-loop
  vs. closed-loop distinction before treating them as valid.
- Treating the AI's 1-5 ranking and "prototype first" recommendation as
  the answer rather than an input is the mistake the "does NOT do"
  section warns about explicitly — the human still has to make the
  final call.
- This is a lightweight, single-founder prompt chain, not the
  systematic portfolio process for an existing company's broader AI
  initiatives — reach for `ai-opportunity-portfolio` instead when the
  case is a running business with multiple candidate use cases, not a
  pre-startup idea.

## What this skill does NOT do

- Does not make the choice for you — the scoring and ranking are an AI
  assessment, not the truth; the human makes the final choice.
- Does not replace the `ai-opportunity-portfolio` skill
  (in the `ai-strategy-and-governance` pack) — that one is meant for the
  systematic prioritization of an existing company's broader AI
  portfolio. This skill is a lighter, faster prompt chain for a single
  pre-startup founder to work through their own case.
- Does not generate business ideas out of thin air without your own
  business context — quality depends directly on how well the AI knows
  the case.

## Continue from here

- Next skill in this pack: `../customer-vision-to-jtbd/SKILL.md`
  — deepens the chosen opportunity into customer understanding.
- Related skill in this pack:
  `../closed-loop-process-and-human-oversight-design/SKILL.md` — deepens
  the "agentic/closed-loop" lens, which in this skill is only used as an
  identification criterion.
- Related skill in this pack:
  `../ai-native-conversational-os-design/SKILL.md` — carries this
  skill's mindset shift forward into a concrete UI architecture (the "5
  shifts": click>question, menus>prompts, dashboards>dialogue, manual
  actions>agents, screens>chat+cards).
- Related skill in another pack:
  `../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/prompt-library.md` — prompts 1–2
- `../../references/workshop-source.md` — source information
- `../../CLAUDE.md` — the pack's shared guardrails
