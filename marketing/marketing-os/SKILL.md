---
name: marketing-os
description: A complete marketing department in one skill. Website and landing-page audits with weighted 0-100 scores, copywriting with panel scoring and AI-slop removal, an 18-tactic ad hook engine, GEO/AEO for getting cited by ChatGPT/Perplexity/AI Overviews, paid-ads creative diagnosis and production briefs, email sequences, LinkedIn/X writing, launch playbooks, positioning and offer design, competitor teardowns, app store optimization, honest analytics and test design. Use for ANY marketing task — audit, write, rewrite, diagnose, score, plan, launch, position, price, analyze — whenever the user mentions marketing, growth, conversion, copy, ads, hooks, CPM, ROAS, SEO, GEO, email, social, landing pages, funnels, launches, competitors, brand, positioning, pricing, or app stores, or says "my landing page sucks", "nobody's converting", "why are my CPMs up", "AI doesn't recommend us", "write me 20 hooks". Route via the table inside; fan out subagents for multi-dimensional work. Not for pure engineering, legal, or finance.
license: MIT
metadata:
  author: marketing-os
  version: "1.1"
---

# Marketing OS

One skill, fourteen modules, the full surface a working marketer touches. Built by tearing down the most-starred marketing skill repos on GitHub (44K-star collections down to 100-star craft pieces), keeping what worked, and fixing what every one of them got wrong.

Three rules hold across every module, because they are what the existing ecosystem uniformly lacks:

1. **Score everything.** Findings without a number are hard to act on and easy to argue with. Every audit ends in a weighted 0-100.
2. **Ship artifacts, not advice.** Write the replacement headline, the JSON-LD block, the email, the screenshot caption. "Your headline is vague" is worthless; the rewritten headline is the deliverable.
3. **State what you couldn't determine.** Every report ends with an explicit gaps section. A stated gap is credible; a silently filled one destroys the document.

## Setup — always do this first

**Read `brand-context.md`** if it exists (working directory, `.claude/`, or `.agents/`). It holds the product, ICP, positioning, proof, voice and constraints, and it changes nearly every judgement below. If absent: proceed, say the output is un-contextualised, and offer to generate the file from what you learn — `brand-context.template.md` in this skill is the blank.

**Identify the task type**, then open ONLY the module file(s) needed. Do not load all references — the routing below exists so you load ~1 file, not 13.

## Routing

| The user wants to... | Module | Also often needed |
|---|---|---|
| Audit/review/score/roast a website, landing page, funnel; "why isn't this converting" | `references/audit.md` | `audit-rubric.md` |
| Get cited by ChatGPT/Perplexity/AI Overviews; GEO, AEO, llms.txt, "AI doesn't recommend us" | `references/geo.md` | `geo-engines.md` |
| Write/rewrite anything: headlines, ads, pages, "make this punchier", "sounds AI-written" | `references/copy.md` | `copy-frameworks.md`, `slop-patterns.md` |
| Hooks for ads/video: "write me 20 hooks", thumbstop problems, hook batches per segment | `references/hooks.md` | `paid-ads.md`, `slop-patterns.md` |
| Diagnose paid ads: CPM up, ROAS down, fatigue, "what to test next", competitor's ads | `references/paid-ads.md` | `ads-diagnostics.md`, `hooks.md` |
| Email: welcome/nurture/launch sequences, subject lines, deliverability | `references/email.md` | `slop-patterns.md` |
| LinkedIn/X posts, personal brand, content that doesn't read as AI | `references/social.md` | `slop-patterns.md` |
| Launch a product, feature, or Product Hunt run | `references/launch.md` | `copy.md` |
| Positioning, category, offer design, pricing page strategy | `references/positioning.md` | — |
| Tear down a competitor: site, ads, positioning | `references/competitive.md` | `paid-ads.md` |
| App Store / Google Play: listing, screenshots, keywords, install rate | `references/app-store.md` | `store-specs.md` |
| Read performance data honestly, design a test, "did this work?" | `references/analytics.md` | — |

Multi-part requests load multiple modules. "Audit my site and rewrite the homepage" = `audit.md` then `copy.md`, carrying the audit findings forward rather than re-researching.

Every de-slop pass — copy, email, social — runs `slop-patterns.md` before delivery. No exceptions. A reader who clocks output as AI-written discounts the claim, not just the prose.

## Subagent fan-out

When subagents are available and the task is multi-dimensional, parallelize. This is the difference between a 15-minute audit and a 2-hour one.

**Full marketing audit** — spawn six, one per scoring dimension (messaging, conversion, search, competitive, trust, growth), each with the URL set and its slice of `audit-rubric.md`. Synthesize their sub-scores into the weighted total yourself; never delegate the synthesis, because the pattern across dimensions is the product.

**GEO audit** — spawn one per target question to query engines and record who gets cited, plus one for on-page extractability.

**Competitor teardown** — one per competitor.

**Copy generation** — one per angle family (problem/outcome/contrarian/identity/mechanism/offer) generating 3-4 variants each; you run the scoring panel on the merged set.

**Paid ads** — one per concept cluster for classification; you do the fatigue diagnosis on the merged concept table.

Rules for fan-out: give each subagent its exact reference slice and output schema; launch all in one turn; never let a subagent write the final report. If subagents are unavailable, work the dimensions sequentially in the order listed — the sequence is deliberate.

## Shared output standards

**Reports** follow this skeleton, adapted per module:

```
# [Deliverable] — [subject]
[date] · Score: XX/100 (where applicable) · Basis: [what you had access to]

## The one thing
[The pattern behind the findings, one paragraph. If they read nothing else.]

## Scorecard / Findings
## Do these first
[3-5 items, each with the actual fix written out, effort S/M/L, confidence H/M/L]

## What's already working
[Never skip. All-negative reports read as generated.]

## What I couldn't determine
```

Write reports to files (`[module]-[subject]-[date].md`), not into the chat — these are documents people forward.

**Copy deliverables** lead with the copy, reasoning after. Recommended option first, scored runners-up, then the single sharpest test contrast.

## Honesty spine — applies to every module

- **All scores are heuristics** from marketing judgement, not measured performance or anyone's internal ranking data. Say so in the report, every time.
- **Never invent proof.** No fabricated statistics, testimonials, customer names, or case studies — not as placeholders. Write `[NEED: figure]` and flag it. A plausible fake number in marketing copy is how a client ships a false-advertising claim.
- **Never declare winners on small samples.** If the data can't support the claim, say the result is directional and state what volume would settle it. `analytics.md` has the discipline.
- **Do not anchor** on scores, numbers, or conclusions the user supplies. Form an independent read first, then compare and say where you differ.
- **Say when the problem isn't the deliverable.** If the offer is weak or the positioning is undifferentiated, better copy won't fix it. One uncomfortable sentence saves a wasted quarter.
- **Verify anything time-sensitive** (platform rules, character limits, engine behavior, crawler user-agents) with search before shipping it, when search is available. These change on a scale of weeks.
- Never handle credentials or touch live campaigns/accounts. Diagnose and prescribe; the human executes in-platform.

## Module directory

```
references/
├── audit.md              Website & funnel audit workflow
├── audit-rubric.md       Scoring bands for the six dimensions
├── geo.md                AI-search citability workflow
├── geo-engines.md        Per-engine behavior (Google AI, ChatGPT, Perplexity), llms.txt, crawlers
├── copy.md               Generate wide → panel-score → de-slop
├── copy-frameworks.md    Awareness stages, 12 angles, headline groups, offer construction, channel limits
├── hooks.md              Hook engine: 3-component spec, 18 tactics, diagnostic funnel, fidelity ladder
├── slop-patterns.md      AI-tell catalogue — run before delivering any prose
├── paid-ads.md           Concept classification, fatigue, coverage gaps, production briefs
├── ads-diagnostics.md    The fatigue decision table & honest data reads
├── email.md              Sequence architecture, subject lines, deliverability
├── social.md             LinkedIn/X writing that survives the feed
├── launch.md             Launch playbook incl. Product Hunt
├── positioning.md        Positioning, offer design, pricing strategy
├── competitive.md        Competitor teardown protocol
├── app-store.md          ASO: diagnosis, metadata, screenshots, reviews
├── store-specs.md        App Store vs Play field rules (they invert)
└── analytics.md          Test design, sample honesty, attribution traps
```

## Chaining

Modules feed each other. Common chains, in order:

- audit → copy (audit found messaging problems; now write the fixes)
- audit → geo (page ranks but is never cited)
- paid-ads → hooks → copy (brief → hooks written to spec → body copy)
- paid-ads → production (an ad-generation MCP is connected, e.g. Arcads: generate the briefed assets directly — see the production handoff in `paid-ads.md`)
- competitive → hooks (cluster their hooks to read their strategy) → positioning (the open flank)
- positioning → copy → launch (new positioning cascades outward)
- app-store → copy (listing copy needs real work)

When chaining, carry evidence forward. Re-researching what a previous module established wastes the user's tokens and your coherence.
