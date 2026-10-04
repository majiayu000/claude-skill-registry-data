---
model_tier: inherit
name: brand
description: "Grounded brand decisions from a curated corpus — archetype, voice, naming, colour psychology, logo-style fit, messaging frameworks, archetype→type mapping. Use to ground brand strategy and identity."
domain: engineering
personas:
  - brand-strategist
workspaces:
  - engineering
packs:
  - brand
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# brand

> The grounded source for brand decisions — a **second instance of the
> ADR-061 corpus-grounding layer** ([`corpus-grounding`](../corpus-grounding/SKILL.md)),
> after [`design-intelligence`](../design-intelligence/SKILL.md). Branding is
> the layer that *constrains* UI: the corpus grounds brand **strategy** and
> **identity** decisions (archetype, voice, naming, colour, logo style,
> messaging, archetype→type filter) as a **constraint set** the human confirms —
> never the final brand. No forked engine; this plugs into the shared one via a
> manifest.

Corpus: 7 tabular CSVs under [`data/`](data/) — 12 brand `archetype`s, a
`voice`-and-tone matrix, `naming` patterns, `color` psychology by industry,
`logo`-style ↔ industry fit, `messaging` frameworks, and
`typography`-principles (archetype → pairing-filter Grounding, the layer that
upgrades [`typography-system`](../typography-system/SKILL.md) stage-2).
Provenance: [`ATTRIBUTION.md`](ATTRIBUTION.md); manifest:
[`data/manifest.json`](data/manifest.json).

## When to use

- A brand decision needs grounding: which archetype fits, what voice/tone,
  how to name, which colour direction, which logo style, which messaging
  framework, or which type pairing-filter an archetype implies.
- Before [`brand-strategy`](../brand-strategy/SKILL.md) /
  [`brand-identity`](../brand-identity/SKILL.md) commit to a direction — those
  skills consult this corpus first.
- When `typography-system` needs the brand-aware (archetype → pairing-filter)
  upgrade — query the `typography` domain here.

## Procedure: consult the brand corpus

1. **Ground or search** (paths resolve skill-relative; works from any cwd):

   ```bash
   ./scripts-run <skills-root>/corpus-grounding/scripts/ground search \
     --manifest <skills-root>/brand/data/manifest.json \
     "<brand brief: sector + intent + audience>" \
     [--domain archetype|voice|naming|color|logo|messaging|typography] \
     [--filter "Archetype Fit=Ruler"] [--json]
   ```

   `<skills-root>` is `~/.claude/skills/` for Claude Code installs,
   `src/skills/` inside this repo.
2. **Read `confidence` + every `evidence_gap` line before trusting any row** —
   surface them; the human signs off on what the corpus could NOT support.
3. **Propose grounded options** (archetype + voice + colour + logo + messaging),
   each cited per corpus row, with alternatives — the human confirms.
4. The confirmed selections become the **brand token + voice constraint set**
   that `brand-to-tokens`, `brand-consistency`, and pack-ai-image's brand-asset
   generation consume.

## Output format

1. Grounded brand candidates per domain (archetype, voice, naming, colour,
   logo style, messaging, type filter) — each selection cited per corpus row.
2. The grounded output's `confidence` label + every `evidence_gap` line,
   verbatim.
3. Alternatives per domain so the human can swap before confirming.

## Do NOT

- Do NOT let the corpus author final brand copy or names — it supplies
  constraint sets and patterns; final strings are agent-written and
  human-confirmed.
- Do NOT fork the engine — plug in via the manifest (ADR-061 §2).
- Do NOT override the consumer's existing brand tokens / voice profile with
  corpus rows — consumer brand is the source of truth; the corpus fills gaps
  (see [`brand-source-of-truth`](../../rules/brand-source-of-truth.md)).
- Do NOT hide low confidence — the user signs off on the gaps too.

## Gotchas

- Corpus grounds **pre-action selection** — not mid-task reference and not
  output validation ([`brand-consistency`](../../rules/brand-consistency.md)
  owns validation).
- Keep queries brand-shaped ("luxury law firm rebrand", "playful kids snack
  brand") — generic words land on the default `archetype` domain.
- An empty result is a legitimate outcome — surface the evidence gap and
  proceed on priors; never widen filters to force a hit.
- BM25 drops tokens ≤2 chars — pad short queries ("B2B", "AI") with companions.

## See also

- [`corpus-grounding`](../corpus-grounding/SKILL.md) — the shared engine + manifest contract.
- [`brand-strategy`](../brand-strategy/SKILL.md) / [`brand-identity`](../brand-identity/SKILL.md) — the workflow skills that consult this corpus.
- [`design-intelligence`](../design-intelligence/SKILL.md) — sibling corpus instance (style); brand constrains style.
- [`typography-system`](../typography-system/SKILL.md) — consumes the `typography` (archetype→filter) domain for its brand-aware stage-2.

## Policies

- Provenance: [`ATTRIBUTION.md`](ATTRIBUTION.md) — original-authored corpus
  from public brand frameworks; shared engine attributed in
  [`design-intelligence/ATTRIBUTION.md`](../design-intelligence/ATTRIBUTION.md).
- Refresh: quarterly per the manifest; re-review archetype↔type rows when the
  font-pairings Reference refreshes.
