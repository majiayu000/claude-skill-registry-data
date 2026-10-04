---
name: autoresearch
description: Run Karpathy-style autoresearch optimization on any content. Generates 50+ variants, scores with a 5-expert simulated panel, evolves winners through multiple rounds, outputs optimized version + full experiment log. Use when optimizing landing pages, email sequences, ad copy, headlines, form pages, CTA text, or any conversion-focused content. Triggers on "optimize this page", "run autoresearch", "score these variants", "A/B test this copy".
when_to_use: |
  Use when pre-launch optimizing conversion-focused content — landing pages, email sequences, ad copy, headlines, form pages, or CTA text — by generating and scoring 50+ variants before shipping. Triggers on "optimize this page", "run autoresearch", "score these variants", or "A/B test this copy".

  Not when: you need post-launch real-traffic A/B testing (that requires real analytics, not simulated scoring). Not when the task is designing or analyzing a live GROWTH EXPERIMENT or A/B test program — experiment management, logged data points, statistical significance — use `growth-engine`. Not when the task is auditing a LIVE landing-page URL for conversion (fetch the page, then score it across CRO dimensions like CTA visibility, social proof, trust signals, form friction) rather than generating and optimizing copy variants pre-launch — use `conversion-ops`. Not when you need a general quality gate on existing content — use `content-ops` instead.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Autoresearch Skill

Karpathy-style optimization loops for any conversion-focused content. No traffic needed. Simulated expert panel. Minutes, not weeks.

> **The sequence:** Run autoresearch FIRST to hit 85+ simulated score. Then deploy. Then validate with real traffic.

## What You'll Produce

Every run outputs 3 files:

| File | Purpose |
|------|---------|
| `{name}-optimized.{ext}` | The winning optimized content |
| `data/{name}-experiments.json` | Full experiment log — all variants + all scores |
| `data/{name}-optimization-report.md` | Human-readable summary with winner rationale |

## Core rules

1. Intake: parse content type from file extension (HTML → landing/form page; markdown → email/ad copy). List all optimizable elements and confirm with user before starting.
2. Score every variant against the 5-expert panel in a single batched API call per round — never one call per variant.
3. Run up to 3 rounds per element; stop early when top variant hits the minimum score threshold (default: 80).
4. Cross-breed only after each element has its own winner — premature cross-breeding creates incoherent combinations.
5. Write 3 output files: optimized content, experiments JSON, optimization report.
6. Report back: winning score, biggest score jump, top 2 runner-ups, file paths, next step.

## User Options

| Option | Default | Description |
|--------|---------|-------------|
| `elements` | all | Which elements to optimize |
| `variants_per_round` | 10 | How many variants per round |
| `min_score` | 80 | Stop when this score is hit |
| `rounds` | 3 | Max rounds before stopping |
| `auto_apply` | false | Overwrite source file with winners |
| `content_type` | auto-detect | Force a content type if auto-detect is wrong |

## Quality Gates

- **< 70:** Don't ship. Something fundamental is broken.
- **70-79:** Marginal. One more round targeting the lowest-scoring dimension.
- **80-84:** Good. Shippable. Validate with real traffic.
- **85-89:** Strong. Ship with confidence.
- **90+:** Rare. Ship immediately.

## Anti-Patterns

- Never call the API once per variant. Always batch. A 10-variant round = 1 call.
- Don't over-optimize for one dimension — a 95 clarity + 45 trust is a misleading overall score.
- Don't run more than 5 rounds. If not hitting 80 after 3, the problem is strategic, not tactical.

## References

- [references/round-structure.md](references/round-structure.md) — round-by-round procedure and 5-expert panel definitions
- [references/content-types.md](references/content-types.md) — elements and score dimensions per content type (landing pages, email, ads, forms)
- [references/execution-protocol.md](references/execution-protocol.md) — 6-step execution protocol with JSON schema

## Related skills

- [content-ops](../content-ops/SKILL.md) — quality scoring gate; run after autoresearch optimization
- [conversion-ops](../conversion-ops/SKILL.md) — audits a LIVE landing-page URL across CRO dimensions; use it instead when scoring a live page rather than optimizing copy variants pre-launch
