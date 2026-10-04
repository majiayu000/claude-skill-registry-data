---
name: rsr-synthesis
version: 1.0.0
description: Merge many sources into one cited, deduplicated answer with per-claim confidence.
author: matrixx0070
tags: [research, synthesis, citation, deduplication, confidence]
capabilities: []
---

# Synthesis

## When to use
Reach for this when you already have a pile of sources and need one coherent answer out of them — deduplicated, cited, and honest about where sources agree, conflict, or fall silent. It's the step that turns collected material into a usable narrative.

**Not for:** gathering the sources in the first place (use rsr-deep-dive); verifying a lone claim (use rsr-fact-check); grading one source (use rsr-source-eval); packaging for a decision-maker (use rsr-brief). Synthesis assumes the sources are in hand.

## Method
1. **Extract claims.** From each source, pull discrete claims tagged with source and date. Ignore the prose; work at the claim level.
2. **Cluster by assertion.** Group claims that make the same point, regardless of wording, so you can see agreement and dedupe.
3. **Score agreement.** For each cluster: how many *independent* sources back it? *Decision:* count sources that echo one origin as one — independence, not headcount, drives confidence.
4. **Resolve conflicts.** Where claims contradict, prefer the more primary, more recent, better-evidenced source; if you can't resolve, present both and say why.
5. **Assign confidence.** High (multiple independent primaries agree), Medium (limited or secondary support), Low (single/weak source or unresolved conflict).
6. **Write the answer.** Lead with the high-confidence throughline, then caveats and conflicts, every claim carrying an inline citation.

## Example
Six sources on "did remote work lower productivity?" Cluster A (4 sources, incl. 2 primary studies): mixed effects by role — High. Cluster B (2 sources, both citing one 2021 survey): "productivity dropped" — really one origin, so Medium at best. Conflict: a vendor blog claims a clear gain; it's self-interested and uncited, downgraded. Synthesis leads with "effects vary by role and task [1][2]," notes the survey-based drop claim is single-origin [3], and flags the vendor claim as unsupported [4].

## Pitfalls
- Vote-counting: treating five sources that all cite one study as five-fold confirmation.
- Averaging conflicting claims into a mushy middle instead of adjudicating by source quality.
- Writing fluent prose with citations bolted on at the end that don't actually map to specific claims.
- Hiding disagreement to make the answer look cleaner than the evidence is.

## Output format
```
Answer: <2-4 sentence throughline, inline [n] citations>

Supported claims:
- <claim> [High|Med|Low] — sources [1][2] (n independent)
- ...

Conflicts / unresolved:
- <claim A> [1] vs <claim B> [3] — resolved toward <..> because <..> / unresolved

Overall confidence: <High | Medium | Low>
Sources: [1] title — date … 
```
