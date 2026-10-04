---
model_tier: inherit
name: brand-strategy
description: "Ground a brand strategy from the corpus — archetype, opposable positioning, voice and tone, messaging framework. Use to decide who a brand is for, what it stands for, and how it sounds."
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

# brand-strategy

Grounding skill. Consults the brand corpus to surface archetype, positioning, voice/tone, and messaging constraints. Output is a constraint set the human confirms — never final brand copy — then handed to brand-identity and brand-to-tokens.

## When to use

- Deciding brand archetype, opposable positioning, voice/tone, or messaging framework before any identity work begins.
- Before invoking brand-identity — the confirmed constraint set is its required input.
- When a brief lacks a named audience, an opposable difference, or supporting proof.
- When a brand refresh or extension needs grounding before token changes.

## Procedure

1. **Pressure-test the brief.** Is the audience named (not "everyone")? Is the difference opposable (could a competitor claim the opposite)? Is there at least one proof point? If any are missing, challenge — do not proceed on a vague brief.

2. **Ground via the corpus.** Run the corpus engine for each required domain. Start with archetype, then voice, then messaging:

```bash
./scripts-run <skills-root>/corpus-grounding/scripts/ground search \
  --manifest <skills-root>/brand/data/manifest.json \
  "<sector + audience + intent>" --domain archetype --json
```

   Repeat with `--domain voice` and `--domain messaging`. Each call returns ranked rows with `confidence` and `evidence_gap`.

3. **Read confidence and evidence gaps.** Before trusting any row, read `confidence` and every `evidence_gap` entry verbatim. Low-confidence rows must be surfaced as gaps — never silently promoted.

4. **Draft the constraint set.** Produce:
   - An **opposable positioning statement** naming the audience AND a difference a competitor could legitimately claim the opposite of.
   - A **voice profile**: 3-5 traits, each with a do and a don't.
   - A **chosen messaging framework** (problem-solution, jobs-to-be-done, category creation, etc.) with a rationale sentence.

5. **Surface gaps and low-confidence calls.** Name every evidence gap and every row below the confidence threshold. Flag where the corpus was thin.

6. **Human confirms.** Present the full constraint set. Wait for confirmation before handing off. Do not proceed autonomously.

7. **Hand off.** Pass the confirmed constraint set to brand-identity (identity execution) and brand-to-tokens (DTCG token emission).

## Output format

1. Named archetype cited to the corpus row (domain, row id, confidence).
2. One-line opposable positioning statement (audience + difference).
3. Voice profile: 3-5 traits, each with a do/don't pair, plus chosen messaging framework with rationale.
4. Confidence label (High / Medium / Low) and every `evidence_gap` from the corpus verbatim.

## Do NOT

- Author final taglines, brand names, or headlines as decided output — those are identity artifacts.
- Invent values or traits absent from the corpus or the consumer's existing brand.
- Accept a brief with no named audience, no opposable difference, and no proof point.
- Override the consumer's existing brand tokens or voice — they are the source of truth; this skill grounds net-new or refresh decisions only.

## Gotcha

- The corpus grounds pre-action selection, not validation. Post-production consistency checking belongs to brand-consistency, not here.
- "Premium + approachable + innovative" is three briefs, not one. Force the trade-off before drafting a positioning statement.
- An empty corpus result is legitimate signal — surface the gap and ask whether to proceed with a thin foundation or pause for more evidence.

## See also

- [`brand`](../brand/SKILL.md) — the corpus this skill grounds against.
- [`brand-identity`](../brand-identity/SKILL.md) — consumes the confirmed strategy.
- [`brand-to-tokens`](../brand-to-tokens/SKILL.md) — emits the DTCG token source of truth.
- [`corpus-grounding`](../corpus-grounding/SKILL.md) — the shared engine.
