---
model_tier: inherit
name: brand-identity
description: "Define a brand identity constraint set from a confirmed strategy — colour story, type story, logo direction, imagery direction. Defines the tokens that token emission and asset generation consume."
domain: engineering
personas:
  - design-director
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

# brand-identity

Grounding + Method skill. Turns a confirmed brand strategy into an identity constraint set: colour story, type story, logo direction, imagery direction. It DEFINES tokens and constraints — it does not render marks. Dependency direction: pack-brand (B) exports constraints; pack-ai-image (A) consumes them. `brand-to-tokens` emits the DTCG token file from these constraints. `logo-generation` and `brand-asset-generation` generate the actual marks from these constraints. Never invert that direction.

## When to use

- After `brand-strategy` is confirmed (archetype, voice, positioning settled).
- When deriving the colour story, type story, logo direction, or imagery direction for a project.
- Before running `brand-to-tokens` to emit the DTCG token file.
- Before handing constraints to `logo-generation` or `brand-asset-generation` in pack-ai-image.

## Procedure

1. **Receive the confirmed strategy** — archetype, voice, positioning, and target sector from `brand-strategy`. Refuse to proceed if strategy is still a draft.

2. **Ground the colour story** via the brand corpus:

```bash
./scripts-run <skills-root>/corpus-grounding/scripts/ground search \
  --manifest <skills-root>/brand/data/manifest.json \
  "<archetype + sector>" --domain color --json
```

   Read `confidence` and `evidence_gap` from the response. Record both verbatim in the output. Derive colour roles (primary, secondary, neutral, accent) and direction (temperature, contrast ratio floor, emotional register).

3. **Ground the type story** via:

```bash
./scripts-run <skills-root>/corpus-grounding/scripts/ground search \
  --manifest <skills-root>/brand/data/manifest.json \
  "<archetype + sector>" --domain typography --json
```

   Output is a pairing-filter + heading/body class labels, not concrete tokens. Hand this filter to `typography-system` for the actual type tokens.

4. **Ground the logo direction** via:

```bash
./scripts-run <skills-root>/corpus-grounding/scripts/ground search \
  --manifest <skills-root>/brand/data/manifest.json \
  "<archetype + sector>" --domain logo --json
```

   Capture mark style, form language, and vector requirement. Note: any mark that the consumer may need in editable form MUST be specified as editable vector (SVG/AI), not raster.

5. **Derive imagery direction** from archetype and sector context: subject matter, mood, composition style, colour treatment, and what to avoid.

6. **Assemble the identity constraint set** — the structured seed for downstream skills. Record confidence and evidence_gap verbatim from all three corpus calls.

7. **Human confirms** the constraint set before any downstream step runs.

8. **Export** — hand off: `brand-to-tokens` receives the colour + type constraints and emits `.tokens.json` (DTCG); `logo-generation` and `brand-asset-generation` receive the logo direction and imagery direction. Direction of flow: B (pack-brand) -> A (pack-ai-image).

## Output format

1. **Colour story** — roles (primary, secondary, neutral, accent) with direction (temperature, contrast floor, register), cited from corpus with confidence score.
2. **Type story** — heading class and body class derived from the archetype pairing-filter; note that concrete tokens come from `typography-system`, not from this skill.
3. **Logo direction** — mark style, form language, vector requirement (editable SVG/AI where needed), and any explicit exclusions.
4. **Imagery direction** — subject matter, mood, composition style, colour treatment, and anti-patterns to avoid.
5. **Confidence + evidence_gap** — verbatim from all corpus calls; flag any domain where evidence_gap is high before the human confirmation step.
6. **Handoff note** — which constraints go to `brand-to-tokens` (colour + type) and which go to the generation skills in pack-ai-image (logo direction + imagery direction).

## Do NOT

- Generate the actual marks here — that is `logo-generation` and `brand-asset-generation`.
- Invert the dependency direction — generation lives in pack-ai-image (A), not in pack-brand (B).
- Ship a raster as a final logo where the consumer needs an editable vector mark.
- Override an existing set of brand tokens on a live project without explicit user confirmation.

## Gotcha

- Identity DEFINES constraints; generation CONSUMES them. Keep the B->A direction in every handoff note.
- A type story is a pairing-filter plus heading/body class labels — the concrete type tokens (scale, weight, line-height) come from `typography-system`, not from this skill.
- Vector-vs-raster is a real decision for any mark: confirm with the user before recording the logo direction, because raster is irreversible for downstream editing needs.

## See also

- [`brand-strategy`](../brand-strategy/SKILL.md) — supplies the confirmed strategy.
- [`brand-to-tokens`](../brand-to-tokens/SKILL.md) — emits the DTCG token source of truth.
- [`typography-system`](../typography-system/SKILL.md) — turns the type story into type tokens.
- [`logo-generation`](../logo-generation/SKILL.md) — generates marks from this identity (pack-ai-image).
- [`brand`](../brand/SKILL.md) — the corpus grounded against.
