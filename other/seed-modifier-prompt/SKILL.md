---
name: seed-modifier-prompt
description: Layer 1a of the keyword research pipeline. Generates seed keywords (broad niche terms) and modifiers (best, how-to, vs, calculator, etc.) from brand-config so the keyword multiplier has a real foundation to expand from. Replaces the "AI gives you generic keywords" problem with the structured 10-second hero prompt.
allowed-tools: Read, Write, Bash, Agent
---

# Seed + Modifier Prompt Skill

Take `brand-config.md` and produce a structured `seeds.json` that the keyword multiplier (Semrush Keyword Magic Tool via `/content-gap-analysis`) uses to expand into real keyword ideas.

This is the upstream of all autonomous keyword research. Without good seeds and modifiers, every downstream layer (BID, AIO, redteam) is filtering an irrelevant pool.

## Input

`/seed-modifier-prompt [--regen]`

Reads:
- `brand-config.md` — brand name, audience, products, monetization
- `content-pipeline/0-keywords/seeds.json` — previous output (for change detection)

`--regen` forces a fresh run even if the brand-config hash hasn't changed.

## Process

1. **Compute brand-config hash.** SHA-256 of `brand-config.md` content. Compare against `seeds.json`'s `brand_snapshot` field if it exists. If unchanged AND `--regen` not passed, exit cleanly with a message saying "seeds are current, skipping" — Layer 1 stays idempotent.

2. **Read brand-config.** Extract:
   - Brand name + tagline (one-line positioning)
   - Audience persona + pain points
   - Live products (drop coming-soon — they're not stable foundations for keyword research)
   - Monetization model (ads / subscription / affiliate / SaaS / etc.)
   - Category positioning

3. **Dispatch the hero-prompt agent.** Use the Agent tool with `subagent_type=general-purpose` and a self-contained brief based on the keyword-research transcript's "10-second hero prompt":

   > You are doing keyword research for **{brand}**, a {category-positioning} that {tagline}. The site makes money through {monetization}. Target audience: {audience-persona} who care about {top-3-pain-points}. Live products: {product-list}.
   >
   > Give me **10 seed keywords** that are 1-2 words max — broad niche terms the audience would type. Then give me **10+ modifiers** that turn seeds into real searches: a mix of intent modifiers (best, vs, alternative, review, comparison), how-to modifiers (how to, guide, tutorial, ways to), and **AI-resistant modifiers** (calculator, checker, generator, tool, examples, templates). The seeds and modifiers must NOT share words.
   >
   > Output as JSON:
   > ```json
   > {
   >   "seeds": ["..", "..", ...],
   >   "modifiers": ["..", "..", ...],
   >   "rationale": "one sentence per seed explaining why it's relevant to the brand's audience and products"
   > }
   > ```
   >
   > Discipline:
   > - Seeds are nouns or noun phrases. NOT product names. NOT brand-specific terms. Generic enough that competitors also rank for them.
   > - Modifiers turn seeds into searchable phrases. Don't overlap categories (don't include "best" twice in different surface forms).
   > - Tool-style modifiers (calculator, checker, generator) are critical because tool keywords are AI-Overview-immune — include at least 3.

4. **Validate the agent's output.**
   - JSON parses cleanly
   - 10 seeds, each 1-2 words, lowercase
   - 10+ modifiers, each 1-3 words, lowercase
   - At least 3 tool-style modifiers (calculator/checker/generator/tool/template/examples/quiz/test)
   - Zero word overlap between seeds and modifiers (split on whitespace, intersect, must be empty)
   - If validation fails, re-run the agent once with the validation error in the brief. If it still fails, exit with the failure reason.

5. **Write `content-pipeline/0-keywords/seeds.json`** with:
   ```json
   {
     "seeds": [...],
     "modifiers": [...],
     "rationale": "...",
     "generated_at": "ISO8601 UTC",
     "brand_snapshot": "sha256-hex-of-brand-config-md",
     "brand_name": "..."
   }
   ```

6. **Print a one-line summary** with seed count, modifier count, tool-modifier count, and the first 3 seeds for sanity-check.

## Output

`content-pipeline/0-keywords/seeds.json`

## Quality checklist

- [ ] 10 seeds, all 1-2 words
- [ ] 10+ modifiers, all 1-3 words
- [ ] At least 3 AI-resistant modifiers (calculator/checker/generator/tool/template/examples)
- [ ] Zero word overlap between seeds and modifiers
- [ ] Each seed has a one-sentence rationale tied to brand audience or products
- [ ] `brand_snapshot` matches current `brand-config.md` SHA-256
- [ ] No product names in seeds (seeds are generic, modifiers do the differentiation)

## Why this exists

The keyword-research transcript's first principle: AI given nothing returns nothing useful. Seeds + modifiers + a real keyword research tool (Semrush Power 1 MCP) is the formula that produces volume-validated, intent-grounded keyword ideas. Without this layer, the pipeline's only ideation channel is "what do competitors rank for that we don't" — which is good but narrow. Adding the seeded-multiplier source widens the pool to "what does our audience search for" regardless of competitor coverage.

## When the agent returns generic seeds

If seeds look like "marketing" / "business" / "online" — they're too broad. Re-run with the addition: "Seeds must be specific enough that someone outside the {category-positioning} category would not search for them. If a seed could apply to any industry, it's too broad — replace it."

## When the brand-config has no live products

(e.g., personal blog, agency site without a SaaS) — adapt the prompt: drop the "live products" line and emphasize audience pain points harder. The downstream `product_fit` scoring already handles the no-products case (weight zeroed out in `keyword-prioritization` line 79-80).

## Invocation from the master orchestrator

`/keyword-research-pipeline` calls this skill first. It runs idempotently — no API costs, no Semrush quota, just one agent dispatch — so the master can call it on every run without worrying about waste.

## Topic-graph enrichment (when Layer 0 has run)

If `content-pipeline/0-keywords/topic-graph.json` exists (the output of Layer 0 `/topic-discovery`, which runs Semrush Topic Research + .Trends ahead of seed generation), pre-feed the agent with the **top 5 KSB cluster names** from that file plus their representative keywords as a "Pre-discovered topical clusters" section in the brief. Semrush has already done topical clustering at the category level; using its clusters as anchors produces seeds that map onto real ranking opportunities rather than abstract category words. The agent should treat the clusters as evidence, not constraints — it can still propose seeds outside them when brand-config strongly motivates one.

If `topic-graph.json` is absent (Layer 0 was skipped, or the brand has no Semrush coverage in the category yet), the skill falls back to brand-config-only behavior — the original 10-second hero prompt, unchanged. The pipeline never blocks on Layer 0; topic-graph is enrichment, not a hard input.
