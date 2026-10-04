---
name: over-the-shoulder
description: Routes product, code, architecture, UX, and business work through source-grounded expert lenses, then shows how the selected experts would critique, mimic, and improve it. Use when the user asks how top companies, famous engineers, elite teams, or "over the shoulder" reviewers would build, rate, review, or improve something.
---

# Over The Shoulder

## Purpose

Use public expert work as a practical operating standard. This skill answers: "Whose public methods should we mimic for this work, what would they notice, and what should we do next?"

Do not summon every company. Route to the smallest useful set.

The user should not have to pick categories or lenses. Infer them from the full available conversation, files, queue item, code, screenshot, plan, or feature context. Ask the user to choose only when the context is genuinely ambiguous or when they explicitly want to override the default routing.

## Hard Rules

- Source first, derive patterns second, apply third, rate fourth.
- Mimic public methods, artifacts, standards, and decision habits. Do not claim private internal knowledge.
- Cite public sources when making company-specific claims. Prefer official engineering blogs, docs, handbooks, design guidelines, talks, postmortems, or product docs.
- Do not impersonate a living person's exact voice. For named experts, apply public techniques and standards.
- Select 3 lenses for a quick pass, 5 for a normal pass, 7 for a deep pass, and 10+ only when the user explicitly asks for a full council.
- Explain selected lenses and skipped high-profile lenses so the user can see routing judgment.
- Respect ChefFlow rules: broad app work goes through queue/spec flow unless the user explicitly authorizes direct implementation.

## Workflow

1. Read the available context and infer the work type automatically: feature idea, queue item, code review, architecture, UX, mobile, marketplace, finance, reliability, AI, food ops, visual design, or a mix.
2. Read [ROUTING-RUBRIC.md](references/ROUTING-RUBRIC.md) and [LENS-MATRIX.md](references/LENS-MATRIX.md) only as needed.
3. Pick the smallest lens set that covers the work. Default to ChefFlow-native lenses for chef, food, client, event, pricing, or hospitality work.
4. Load cached research before browsing:
   - Use [CHEFFLOW-DEFAULT-PACK.md](references/CHEFFLOW-DEFAULT-PACK.md) for common ChefFlow work.
   - Use [SOURCE-CARDS.md](references/SOURCE-CARDS.md) for lens-specific public patterns.
   - Browse only when a source card is missing, stale, user asks for current/latest, or details like pricing/features/policies may have changed.
5. Extract patterns from each lens:
   - What they optimize for.
   - What artifact or workflow they would create.
   - What failure mode they would worry about.
   - What they would refuse to overbuild.
6. Apply the patterns to the current work.
7. Produce a critique, mimic plan, score, and next move. Use [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md) when the requested mode is review, build plan, mobile UX, finance, reliability, or AI.

## User Control

Default invocation should be short:

```text
Use over-the-shoulder on this.
```

The skill then reads context, classifies the work, selects lenses, and explains the selection. User-specified categories or lenses are optional overrides, not required inputs.

## Output Shape

Use this structure unless the user asks for a different format:

```md
## Selected Lenses

- Lens - reason selected - source basis.

## Skipped Lenses

- Lens - why it is not useful for this pass.

## What They Would Notice

- Concrete observations grounded in the current work.

## How They Would Build It

- Source-derived methods applied to this work.

## What They Would Reject

- Noise, overbuild, vague requirements, weak evidence, or bad UX.

## Rating

- Product, UX, architecture, reliability, operations, and verification.

## Best Next Move

- The highest-leverage action now.
```

## Quick Routing Examples

- Chef booking flow: Take a Chef, HoneyBook, Tock, Airbnb, Stripe.
- Chef dashboard/business OS: Clover, Toast, QuickBooks, Google Workspace, Linear.
- Pricing, invoices, tax: QuickBooks, TurboTax, Stripe, Restaurant365, Ramp.
- Mobile visual polish: Apple, Airbnb, Cash App, Duolingo, Flighty.
- Runtime reliability: Google SRE, Sentry, Datadog, Cloudflare, Netflix.
- TypeScript correctness: Matt Pocock, Microsoft, GitHub, Stripe, Jane Street.

## Research Cache

The skill ships with a starter research cache. Treat it as a warm start, not a permanent source of truth.

- [SOURCE-CARDS.md](references/SOURCE-CARDS.md): compact public-source cards for the most useful lenses.
- [CHEFFLOW-DEFAULT-PACK.md](references/CHEFFLOW-DEFAULT-PACK.md): default ChefFlow lens bundles and mimic moves.
- [ROUTING-RUBRIC.md](references/ROUTING-RUBRIC.md): scoring rules for selecting lenses without noise.
- [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md): response shapes for common over-the-shoulder modes.
