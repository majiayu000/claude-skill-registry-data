---
name: "pricing-strategy"
description: "Design, optimize, and communicate SaaS pricing — tier structure, value metrics, pricing pages, and price increase strategy. Use when building a pricing model from scratch, redesigning existing pricing, planning a price increase, or improving a pricing page. Trigger keywords: pricing tiers, pricing page, price increase, packaging, value metric, per seat pricing, usage-based pricing, freemium, good-better-best, pricing strategy, monetization, pricing page conversion, Van Westendorp. NOT for broader product strategy — use product-strategist for that. NOT for customer success or renewals — use customer-success-manager for expansion revenue."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# Pricing Strategy

Use this skill to design, audit, optimize, and communicate SaaS pricing: value metric, packaging, tier structure, price points, price increases, and pricing-page conversion.

Pricing is positioning. Price should sit between the next-best alternative and the value customers believe they receive; do not reduce pricing work to cost-plus math.

## Required Input Contract

Check `marketing-context.md` first. Gather or infer:

- Current pricing: plans, price points, billing model, free/trial model, conversion rate, ARPC/ARPU, churn.
- Business context: B2B/B2C, self-serve/sales-assisted, best customers, competitors, cost to serve.
- Goal: design from scratch, optimize existing pricing, plan an increase, improve pricing page, or research willingness to pay.
- Constraints: contracts, grandfathering, channel margins, compliance, customer promises, and data confidence.

## Constraints

- Confidence-tag every number: verified benchmark, estimated, or assumed.
- Do not quote non-public competitor prices or unverified benchmarks.
- Do not recommend changes that violate contracts, grandfathering, annual commitments, or partner margin rules.
- Do not recommend illegal or deceptive pricing: price-fixing, fake discounts, unlawful discrimination, or dark patterns.
- Do not fabricate case studies, customer outcomes, conversion rates, or revenue impact.
- Disclose price changes honestly; 60-90 days notice is standard for B2B increases and 30 days is the minimum.
- Do not promise specific conversion or revenue outcomes; use scenario ranges and label assumptions.
- Prefer three-tier good/better/best packaging when applicable; flag single-tier pricing when it blocks anchoring and expansion.

## Core Modes

1. **Design from scratch:** choose value metric, tier structure, price-point research, and pricing-page design.
2. **Optimize existing:** audit current model, benchmark, identify conversion or expansion gaps, and recommend specific changes.
3. **Plan a price increase:** choose rollout strategy, customer messaging, risk model, and monitoring plan.

## Core Workflow

1. Clarify goal, context, constraints, and confidence level.
2. Decide the value metric before packaging and price points.
3. Design or audit tier structure using good/better/best anchoring.
4. Use value-based pricing and research methods to justify numbers.
5. Address price-increase or pricing-page needs if in scope.
6. Provide clear recommendation, rationale, risks, and validation plan.

## Pricing Axes

Every pricing decision has three axes:

- **Packaging:** what each tier includes.
- **Value metric:** what scales with customer value.
- **Price point:** the number customers pay.

Lock in the value metric first, then packaging, then test price point.

## Decision Rules

- Use per-seat pricing for collaboration-heavy tools where users map to value.
- Use usage pricing for APIs, infrastructure, AI, and variable consumption.
- Use feature/tier gates for platform capabilities and admin/security value.
- Use flat pricing only when value variation is narrow or simplicity matters more than expansion.
- Use hybrid models when one metric cannot capture value cleanly.
- If churn is high, diagnose retention before recommending a broad price increase.

## Output Expectations

- Pricing design: value metric, three-tier structure, feature grid, price points, and rationale.
- Pricing audit: scorecard, gap analysis, benchmarks, risks, and quick wins.
- Price increase: strategy, communication plan, risk model, and 90-day rollout.
- Pricing page: above-fold layout, feature table, CTA copy, FAQ copy, and proof needs.
- Pricing research: Van Westendorp, MaxDiff, or competitor benchmarking plan.
- Scenario modeling: inputs and assumptions for `scripts/pricing_modeler.py` when relevant.

Use bottom-line-first communication. Every recommendation needs what, why, how, and a confidence tag.

## Reference Map

| Need | Read |
|---|---|
| Before-starting checklist, proactive triggers, output catalog, related skills | [operating-reference.md](references/operating-reference.md) |
| Value metrics, red flags, tier design | [pricing-models.md](references/pricing-models.md) |
| Value-based pricing process and examples | [value-based-pricing.md](references/value-based-pricing.md) |
| Van Westendorp, MaxDiff, competitor benchmarking | [research-methods.md](references/research-methods.md) |
| Price increase strategy and rollout checklist | [price-increases.md](references/price-increases.md) |
| Pricing page layout and copy templates | [pricing-page-playbook.md](references/pricing-page-playbook.md) |
