---
name: winning-pattern-synthesis
description: >
  Cross-reference competitor ad patterns against the user's own strong-performing creatives and psychological hook analysis to find cross-source overlap, own-account test gaps, and market whitespace. Use whenever the user wants to know what to actually build next — after competitor research and/or own-creative diagnosis have already run, or when they explicitly ask "what should we test" or "what's the whitespace." This is a synthesis skill — it consumes the outputs of competitor-ad-intelligence, own-creative-diagnosis, and creative-psychology-hooks rather than pulling new data itself.
---

# Winning Pattern Synthesis

Takes the outputs of the other three analysis skills and turns them into a ranked set of creative directions worth actually building — the step between "here's what we found" and "here's what to brief."

## When to use this skill

- "What should we test next?"
- "Where's the whitespace vs competitors?"
- Any time competitor intel + own-creative diagnosis have both run and the user wants a single synthesized direction rather than two separate reports
- As the step before `ad-brief-generator`

## Inputs

This skill doesn't fetch new data — it reasons over what's already been produced:
- **Competitor patterns** from `competitor-ad-intelligence` (angles, hooks, formats, scale signals)
- **Own performance patterns** from `own-creative-diagnosis` (what showed strong first-party results in the stated analysis window)
- **Psychological grading** from `creative-psychology-hooks` (mechanism, valence/intensity, micro-moment)

If one or more inputs are missing, say explicitly which are missing and whether to proceed with a partial synthesis or run the missing skill(s) first. Competitor-only or own-creative-only synthesis is possible but weaker — flag it as partial.

## Step 1: Build the pattern matrix

Lay out every distinct pattern (angle × hook mechanism × format) found across both sources in one table, tagging each occurrence:

| Pattern | Seen in competitors? | Seen in own strong performers? | Scale/strength signal |
|---|---|---|---|

## Step 2: Classify each pattern

- **Cross-source overlap** — the pattern has strong first-party results and competitor duration/spend/variation proxy evidence. This is the strongest observed overlap, but competitor performance remains unverified; recommend a controlled variation test rather than calling it proven.
- **Competitor-backed test gap** — competitors are running it with meaningful proxy signals, but the user hasn't tested it. This is an own-account test gap, not market whitespace or a guaranteed winner.
- **Own-only market whitespace** — has strong first-party results in the analysis window but was not observed in the competitor sample. It could be a differentiator, a sample-coverage gap, or an account-specific result — note all applicable interpretations.
- **Neither** — untested by anyone visible. Highest risk/highest potential differentiation; only surface if the user wants aggressive experimentation, not as a default recommendation.

## Step 3: Rank by confidence and apply psychological lens

For each pattern surfaced, pull in the Baader mechanism / valence-intensity classification from `creative-psychology-hooks` if hooks for that pattern were graded. Present it as a testable hypothesis for why the pattern may attract attention, not a causal explanation of performance.

Rank output: cross-source overlap first, then competitor-backed test gaps, then own-only market whitespace. Cap at the top 5–7 directions unless the user asks for the full list — a synthesis that recommends everything recommends nothing.

## Step 4: Flag conflicts

If a pattern is a competitor favorite but has performed poorly in the user's own account (or vice versa), don't average it out — call out the conflict directly and suggest a hypothesis for the divergence (audience difference, execution quality, offer mismatch).

## Output Format

```
### Winning Pattern Synthesis: [Product/Category]

Inputs used: [competitor intel / own diagnosis / psych grading — note any missing]

Top directions:
1. [Pattern] — CROSS-SOURCE OVERLAP
   - Competitor signal: [brands, scale]
   - Own signal: [ad, metrics]
   - Mechanism: [Baader tag, valence/intensity]
   - Recommendation: [controlled variation test / new variant angle]

2. [Pattern] — COMPETITOR-BACKED TEST GAP
   - ...

Conflicts worth noting:
- [Pattern]: strong for competitors, weak in our account — possible reason: [hypothesis]

Not recommended right now:
- [pattern seen but low-confidence, and why]
```

## Guardrails

- Never present competitor proxy evidence as verified performance or competitor-backed patterns as proven for the user's account.
- Don't let this skill turn into a restatement of the two input reports — its entire value is the cross-reference and ranking. If there's no real overlap or conflict to surface, say that plainly rather than padding the output.
- Hand off the final ranked list directly to `ad-brief-generator` — don't re-derive angles from scratch there.
