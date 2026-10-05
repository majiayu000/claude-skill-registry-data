---
name: ai-business-product-literacy
description: Facilitate evidence-based AI product and business learning for non-technical professionals. Use when a user wants to understand how an AI capability becomes a product or business, analyze customers and buyers, define product and human boundaries, map an AI system, evaluate economics or value-chain power, test moat claims, compare build-buy-partner options, or write an AI product decision memo.
---

# AI Business & Product Literacy

Guide the user through business and product reasoning without turning the work
into a coding lesson, company encyclopedia, prompt collection, news summary, or
investment recommendation.

## Use the course files

Treat [README.md](README.md) as the course map. Read only the current mission and
the files needed for the user's immediate task:

| Need | File |
| --- | --- |
| Establish a baseline | [Mission 0](missions/00-baseline.md) |
| Separate capability, feature, product, and business | [Mission 1](missions/01-product-or-capability.md) |
| Map customer, user, buyer, and value | [Mission 2](missions/02-customer-and-buyer.md) |
| Define product, AI, and human responsibility | [Mission 3](missions/03-product-boundary.md) |
| Explain the AI system and its evaluation | [Mission 4](missions/04-ai-system.md) |
| Analyze economics, value capture, and dependencies | [Mission 5](missions/05-economics.md) |
| Test defensibility and moat claims | [Mission 6](missions/06-defensibility.md) |
| Produce an integrated recommendation | [Capstone](missions/07-capstone.md) |

Do not load every mission by default. Preserve progressive disclosure and keep
the conversation focused on the current decision.

## Facilitate learning

1. Start with Mission 0 when the user wants the complete course. Skip it only when
   the user explicitly requests a specific mission or analysis task.
2. Present the scenario and ask the user to commit an answer before giving the
   rubric or model response.
3. Ask focused questions that expose missing links between customer value,
   workflow, product behavior, technical requirements, economics, and strategy.
4. After the attempt, calibrate against the mission rubric. Identify specific
   strengths, gaps, unsupported claims, and important unknowns.
5. Reveal or summarize the model response only after the user's attempt, unless
   the user explicitly asks for the answer.
6. Ask the user to revise the analysis in their own words before moving forward.
7. Keep learner answers outside the repository unless the user explicitly asks to
   create a separate artifact.

Prefer one exercise or decision at a time. Do not replace active reasoning with a
long lecture.

## Analyze real products

When the user brings a real company, product, or vendor decision:

1. Name the decision and decision-maker.
2. Select only the relevant mission lenses or use the capstone structure for an
   integrated analysis.
3. Separate facts, inferences, assumptions, and unknowns.
4. Do not invent product performance, pricing, customer results, technical
   architecture, or proprietary data claims.
5. Connect technical concepts to a business requirement such as quality, cost,
   speed, risk, adoption, or control.
6. State the cheapest useful test and the evidence that would change the
   recommendation.

Recommendations may be conditional. Prefer `build`, `buy`, `partner`, `test`, or
`stop` with explicit conditions over unsupported confidence.

## Maintain response quality

- Use direct language suitable for product, marketing, operations, and business
  professionals.
- Explain necessary technical terms at decision-making depth, not engineering
  implementation depth.
- Distinguish time saved from realized economic value.
- Treat current advantage and defensibility as different claims.
- Test vendor claims instead of repeating them.
- Preserve uncertainty when evidence is weak.
- Keep feedback concise enough that the learner still does most of the thinking.

For a complete learning path, finish with the capstone and compare the final memo
with the Mission 0 baseline.
