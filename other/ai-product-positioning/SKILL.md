---
name: ai-product-positioning
description: "Produces positioning for an Artificial Intelligence (AI) product that survives the three hardest buyer objections - 'why not just use a general-purpose assistant', 'it is only a wrapper', and 'the model provider will ship this next' - with a scored differentiation ladder, proof-point inventory, and messaging hierarchy. Use when positioning a new AI product or feature; rewriting messaging that sounds like every other AI startup; preparing for investor or buyer questions about defensibility; or responding to a foundation-model provider launching an overlapping capability."
---

# AI Product Positioning

> If your pitch still works after the buyer opens a general-purpose assistant in another tab, you have positioning.

## What this skill is

A positioning workflow built for products whose core capability is powered by models anyone can rent. It starts from the buyer's real alternatives (including a general-purpose assistant and doing nothing), scores where durable advantage actually comes from across five layers, and turns only the defensible layers into a message hierarchy with proof. It deliberately refuses "powered by AI" as a value proposition.

## What it solves

- Messaging that leads with the model or "AI-powered" instead of the job and the outcome
- No credible answer to "I can do this with a chat assistant and a good prompt"
- Defensibility claims that collapse when a model provider ships the same feature
- Proof points that are demos rather than measured results
- Positioning that is identical to five funded competitors using the same models

## When to invoke

- Pre-launch positioning for an AI-native product or a new AI feature in an existing product
- Rewriting a homepage or pitch deck that reads as generic AI marketing
- After a foundation-model provider or platform announces an overlapping capability
- Preparing sales for "why not just build it ourselves with an Application Programming Interface (API)"
- Investor or board questions about moat and fast-follow risk

## Phase 1: Map the real alternatives

List what the buyer would actually do instead, and why they would pick it.

| Alternative | Example | Why a buyer picks it | Where it breaks for this job |
|-------------|---------|----------------------|------------------------------|
| General-purpose assistant | A chat assistant plus manual prompting | Already paid for, flexible | |
| Do it yourself | Internal build on a model API | Control, perceived low cost | |
| Incumbent adds AI | Existing system of record ships a feature | Already integrated, procurement done | |
| AI-native competitors | Similar startups | Similar pitch | |
| Status quo | People and spreadsheets | Zero change cost | |

The "where it breaks" column is the raw material for positioning. If it is empty for the general-purpose assistant, stop and fix the product before the messaging.

## Phase 2: Score the differentiation ladder

Rate each layer 0-3 on current strength and on durability against fast-follow (how long until a model provider or incumbent matches it).

| Layer | What counts | Strength (0-3) | Durability (0-3) | Evidence |
|-------|-------------|---------------:|-----------------:|----------|
| Model | Fine-tuned or specialized models, measurable quality gap on the target task | | | |
| Data | Proprietary or compounding data, feedback loops, domain corpora | | | |
| Workflow | Embedded in the system where work happens, multi-step automation, integrations, approvals | | | |
| Distribution | Existing customer base, channel partners, marketplace placement, community | | | |
| Trust | Accuracy guarantees, security certifications, audit trails, human review, liability terms | | | |

```
Layer score = Strength x Durability (max 9)
```

Lead with the highest-scoring layer. Model-layer advantages usually score low on durability; workflow, data, and trust usually score highest. A layer with Strength 3 and Durability 0 is a launch talking point, not positioning.

## Phase 3: Neutralize the three objections

Write a one-paragraph, evidence-backed answer to each. Test each answer on 3-5 target buyers.

| Objection | Weak answer (avoid) | Strong answer pattern |
|-----------|---------------------|-----------------------|
| "Why not a general-purpose assistant?" | "Ours is smarter" | Name the steps, context, and integrations the assistant lacks; quantify time or error difference on a real task |
| "It is just a wrapper" | "We have proprietary AI" | Show the system around the model: data pipeline, evaluations, workflow, guardrails, outcomes |
| "The model provider will ship this" | "They will not" | Explain why your layer (workflow, data, trust, distribution) is outside the provider's incentive or reach; show you benefit when models improve |

## Phase 4: Build the proof-point inventory

| Proof point | Type | Metric | Source | Verifiable by buyer? | Shelf life |
|-------------|------|--------|--------|----------------------|------------|
| | Outcome (time saved, errors reduced, revenue) | | | | |
| | Evaluation result on a named task set | | | | |
| | Customer reference or case study | | | | |
| | Security or compliance attestation | | | | |

Rank proof by: outcome metric beats evaluation score beats testimonial beats demo. Flag any proof older than 6 months - model progress makes quality claims stale fast.

## Phase 5: Messaging hierarchy

| Level | Content | Constraint |
|-------|---------|------------|
| Positioning statement | For <segment> who <job>, <product> is the <category frame> that <outcome>, unlike <primary alternative>, because <top ladder layer> | Internal; no adjectives without proof |
| Headline | Outcome for the job, not the technology | Under 10 words; no "AI-powered" |
| Three pillars | One per top-scoring ladder layer | Each pillar maps to 2+ proof points |
| Proof row | Metrics, logos, attestations | Dated and sourced |
| Objection handlers | From Phase 3 | Used in sales and Frequently Asked Questions (FAQ) |

Choose the category frame deliberately: an existing category ("better <tool>"), a sub-category ("<tool> for <segment>"), or a new category. New categories need budget and patience; most AI products should anchor to an existing budget line.

## Phase 6: Pressure-test and fast-follow plan

- **Swap test**: replace your brand with a competitor's in the headline - if it still reads true, rewrite
- **Assistant test**: have a skeptic attempt the core job with a general-purpose assistant for 30 minutes; document where it fails
- **Fast-follow scenario**: if a model provider ships the core capability free in 6 months, which pillar survives? Make that pillar more prominent now

## Output

- Alternatives map including the general-purpose assistant and do-it-yourself options
- Scored differentiation ladder with evidence and durability ratings
- Written answers to the three core objections
- Proof-point inventory ranked by strength and freshness
- Messaging hierarchy: positioning statement, headline, three pillars, proof row, objection handlers
- Fast-follow scenario note with the surviving pillar identified

## Operating rules

**Always**
- Position against the general-purpose assistant explicitly, even if no buyer names it
- Lead with the job and the measurable outcome, then the system that delivers it
- Score durability separately from current strength
- Tie every pillar to dated, verifiable proof
- Re-run the ladder whenever a major model or platform release lands

**Never**
- Use "AI-powered", "revolutionary", or model names as the headline value proposition
- Claim a model-quality moat without a repeatable evaluation behind it
- Dismiss the fast-follow risk instead of planning for it
- Promise accuracy levels the product does not reliably achieve in production
- Copy the category language of better-funded competitors and expect to win on features
