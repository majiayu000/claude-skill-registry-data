---
name: plan-rebrand
description: Plans a rebrand by testing the reasons and risks, auditing what to keep, setting research, rollout across touchpoints, communications and success measures. Use when a company outgrows its brand.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: branding
  source: https://hermes-ide.com/prompts/plan-rebrand
  catalog: 2026.1014.1
---

# Plan a rebrand

## Inputs

- [CURRENT_BRAND] (required): The company and the brand today - name, logo, colours, taglines and other assets, how long they have been used, how well known they are, markets, and the main touchpoints.
- [REASONS] (required): Why a rebrand is being considered (merger, new market, repositioning, outdated look, reputation problem, name conflict) and any evidence, budget, deadline and who is sponsoring it.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Rebrands fail for two opposite reasons. Some solve the wrong problem: a new logo for what is really a product, price or service issue, or a change driven by internal boredom while customers still recognise and like the old look. Others throw away years of recognition by replacing every distinctive asset at once, and sales or search traffic drop while customers wonder whether this is the same company. A good rebrand plan first proves that the brand is the problem, decides what to keep, tests with customers, and rolls out in an order that protects the business.
</context>

<task>
Plan this rebrand.

<current_brand>
[CURRENT_BRAND]
</current_brand>

<reasons>
[REASONS]
</reasons>

If the current brand or the reasons are too vague to assess, ask up to four questions and stop.

1. **Diagnosis.** Test each reason: is it a brand problem (perception, relevance, differentiation, a name conflict, a merger) or a product, service, pricing or distribution problem that a rebrand will not fix? Use the evidence given and mark gaps. If the reasons are mostly internal ("we're bored of it", "the new CEO doesn't like it"), say so plainly and explain the risk.
2. **Scope recommendation.** Recommend the smallest change that solves the real problem: no change, a refresh (tidy up and modernise the existing identity), an evolution (reposition and redesign while keeping key assets), or a full rebrand (new name and identity). Give the reasoning and what would change the recommendation.
3. **Equity audit.** List every brand asset (name, logo, symbol, colours, typography, tagline, characters, sounds, packaging shapes) and judge each on fame (how many customers link it to the brand) and uniqueness (whether it points only to this brand). Recommend keep, evolve or drop for each. Recognition levels without research are marked as estimates.
4. **Research plan.** What to learn before and during design: customer and non-customer perception, recognition of current assets, employee and partner views, and testing of new directions for recognition, fit and distinctiveness against competitors. Name methods and sample sizes appropriate to the budget.
5. **Risks.** Loss of recognition and sales, search traffic and links (domains, redirects), legal (trademark clearance in every market and class, domain and social handles, existing contracts), cost overruns, internal resistance, public backlash, and inconsistent half-finished rollout. Give a mitigation for each.
6. **Rollout plan.** A touchpoint inventory (digital, product, packaging, signage, vehicles, uniforms, documents, legal entities, app stores, partners), each prioritised by visibility and cost, and a choice between a single launch date and a phased rollout, with what must be ready on day one. Include the asset handover to teams and agencies, and decommissioning old materials.
7. **Communications.** Employees first (why, what changes, what does not, and their role), then key customers and partners, then the public. The story of why the change matters to customers, an FAQ, and how to handle questions about cost or the old brand.
8. **Success measures.** Baselines to capture before launch (awareness, recognition, consideration, brand search volume, conversion, sentiment, employee understanding) and targets with dates; a check at 3, 6 and 12 months.
9. **Timeline and budget drivers.** Phases with typical durations and the decisions that drive cost most (name change or not, number of physical touchpoints, markets).
</task>

<constraints>
- Do not invent research results, recognition levels, costs or legal conclusions. Mark estimates and recommend professional trademark clearance and legal review where needed.
- Default to keeping recognised assets; justify every drop.
- Be candid if a rebrand is the wrong answer.
- Separate what you verified from what you inferred. Mark inferences as such.
- When you do not know, say "I don't know" once and state what would settle it.
</constraints>

<output_format>
Markdown with the contract's sections as `##` headings. Equity audit as a table: | Asset | Fame (est.) | Uniqueness (est.) | Recommendation | Reason |. Risks as a table: | Risk | Likelihood | Impact | Mitigation |. Rollout as a table: | Touchpoint | Priority | Day-one? | Owner (role) | Notes |.
</output_format>
