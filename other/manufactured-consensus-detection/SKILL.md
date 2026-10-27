---
name: manufactured-consensus-detection
description: >-
  "Are these sources agreeing independently, or echoing the same origin?" -
  When multiple sources converge on the same claim in similar language, test
  whether this is genuine independent agreement or coordinated messaging from
  a single origin. Use when (1) multiple independent sources say the same
  thing in similar language, (2) convergence warning fires during
  verification, (3) evaluating media campaigns or narrative coordination, (4)
  investigating PR/comms strategy behind claims.
---

# Manufactured Consensus Detection

**Seed question:** *Are these sources agreeing independently, or echoing the same origin?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

Consensus is evidence — but only when it is genuine. When multiple "independent" sources agree, this can mean the claim is true (genuine consensus), OR that a single source successfully propagated its framing to others (manufactured consensus), OR that everyone is making the same cognitive error (groupthink/confirmation bias).

Distinguishing these is critical because manufactured consensus creates the appearance of verification without actual independent confirmation.

This applies to consensus about *sources* as much as about *claims*: a discrediting label — "fringe", "conspiracist", "discredited" — is often one profile's editorial aside echoed downstream until it reads as settled consensus. Topology-map the label's provenance before importing it as a verdict, the same way you would any manufactured agreement.

**The anti-pattern this counters:**
```
❌ "Multiple sources agree, so it must be true"
❌ Counting agreement without checking independence
❌ Treating simultaneous publication as independent corroboration
❌ Accepting "experts agree" without checking if they share a funding source
```

**The pattern this enforces:**
```
✅ Trace each agreeing source back to its origin
✅ Test independence before treating agreement as corroboration
✅ Check for coordination signals (timing, language, PR firms)
✅ Distinguish four types of agreement before relying on consensus
```

## When This Applies

**TRIGGER:**
- Multiple "independent" sources use similar language about the same claim
- Convergence warning fires during an iterative-verification loop
- Investigating whether a narrative is organic or orchestrated
- Evaluating PR campaigns, media strategy, or information operations
- Sources agree quickly and uniformly (the speed itself is a signal)
- "Experts agree" or "studies show" claims that lack citation diversity

**DO NOT TRIGGER:**
- Sources agree on easily verifiable facts (dates, locations, public statements)
- Scientific consensus built over decades with published methodology
- User wants quick answer, not meta-analysis of sourcing

## The Four Types of Agreement

Before treating consensus as evidence, classify it:

| Type | Definition | Test | Evidence Value |
|------|-----------|------|---------------|
| **Genuine consensus** | Multiple independent observers reach the same conclusion through separate investigation | Origins are independent; methodologies differ; conclusion converges | HIGH — strong evidence |
| **Manufactured consensus** | A single source, PR firm, or coordinated campaign pushed the same framing to multiple outlets | Trace to single origin; check PR firms; compare language patterns | ZERO — one source disguised as many |
| **Groupthink** | Sources share assumptions and social incentives that produce agreement without coordination | Sources are in same professional/social network; no explicit coordination but shared priors | LOW — reflects shared bias, not independent verification |
| **Confirmation bias** | Sources (and investigator) gravitate toward the same conclusion because it matches prior beliefs | Check if contrarian sources also agree; check if agreeing sources share the investigator's priors | LOW — needs adversarial testing |

## Detection Protocol

### Step 1: Trace to Origin

For each source that makes the claim:
- **When** did they first publish it?
- **Who** do they cite (if anyone)?
- **What** is the earliest instance of this specific framing?

If multiple outlets published within 24-48 hours with no independent reporting trail, the origin is likely a shared briefing, press release, or embargo lift.

### Step 2: Check for Coordination Infrastructure

- **PR firms:** Is the same communications firm behind multiple outlets or spokespeople?
- **Press releases:** Did a press release precede the coverage? (Check PR Newswire, Business Wire, GlobeNewswire)
- **Think tank papers:** Did a single paper seed the narrative? (Check publication date vs coverage dates)
- **Embargoed briefings:** Did a government or corporate briefing pre-position the story?

### Step 3: Compare Language Patterns

Identical or near-identical phrasing across outlets is the strongest manufactured consensus signal:
- Same adjectives, same framing, same metaphors
- Same statistics cited in the same order
- Same "expert" quoted across multiple pieces
- Same counterargument preemptively addressed in the same way

**Legitimate reuse:** Wire service copy (AP, Reuters) is designed to be republished. This is transparent, not manufactured. The signal is when language converges across outlets that claim independent editorial judgment.

### Step 4: Check Publication Timing

| Timing Pattern | Suggests |
|---------------|----------|
| Simultaneous publication (same day, multiple outlets) | Embargo lift or coordinated campaign |
| Cascading within 24-48 hours | One outlet broke it, others followed (may be genuine) |
| Gradual convergence over weeks | More likely genuine consensus building |
| Suspiciously timed relative to policy/event | Strategic communications |

### Step 5: Test Independence

For sources that agree, check:
- Do they share funding sources?
- Do they share board members or advisors?
- Are they in the same professional network?
- Did they cite each other or a common source?
- Would their business model suffer from reaching a different conclusion?

If YES to any: their agreement is not independent. Downgrade from "consensus" to "aligned interests."

### Step 6: Hard cases — the five discriminators

When Steps 1–5 leave the classification contested, or the stakes are high,
apply the five measurable discriminators (inferential distance ·
dimensionality · lexical fingerprint · temporal granularity ·
pre-positioning) and the template-level check in
`references/discriminators.md`. Cite instances per discriminator — the
point of the file is that each one is checkable against the texts.

## Convergence Warning Template

When rapid convergence is detected, issue this warning:

```
WARNING: All sources converge on [X]. Testing consensus type:

Convergence details:
- [N] sources agree within [timeframe]
- Language similarity: [HIGH/MEDIUM/LOW]
- Earliest origin identified: [source, date]
- Independence test: [PASS/FAIL — details]

Consensus classification: [GENUINE / MANUFACTURED / GROUPTHINK / CONFIRMATION BIAS]
Evidence: [why this classification]

Action: [adversarial search / trace origin / check PR infrastructure / accept as genuine]
```

## Affiliate/SEO Manufactured Consensus (Product Domain)

In product reviews and recommendations, manufactured consensus takes a specific form:

- Multiple "review" sites with identical rankings (affiliate coordination)
- "Best X 2025" listicles that all recommend the same products in the same order
- No methodology disclosure, no failure mode discussion
- High-commission products consistently ranked first

**Detection:** Check for affiliate disclosure. If all agreeing sources have financial incentive to agree, their consensus is manufactured by the affiliate program, not by product quality.

**Cross-reference:** `deep-investigation-protocol` Stage 3 (Affiliate/SEO Gaming Detection) for detailed red flags.

## Output Pattern

```markdown
## Consensus Analysis: [Claim]

### Sources Agreeing
1. [Source] — published [date] — cites [origin/none]
2. [Source] — published [date] — cites [origin/none]
...

### Origin Trace
- Earliest instance: [source, date, context]
- Propagation path: [how it spread]
- Coordination signals: [PR firm / press release / embargo / none detected]

### Independence Test
- Shared funding: [YES/NO — details]
- Shared personnel: [YES/NO — details]
- Language similarity: [HIGH/MEDIUM/LOW — examples]
- Timing pattern: [simultaneous / cascading / gradual]

### Classification
**[GENUINE / MANUFACTURED / GROUPTHINK / CONFIRMATION BIAS]**
Evidence: [summary of why]

### Implications
- If manufactured: [what the actual evidence base is, stripped of false amplification]
- If genuine: [confidence level for relying on this consensus]
```

## Examples from Practice

### China: Nexperia "40% Global Market Share" (March 2026)

A single statistic propagated across multiple outlets without independent verification, inflating perceived supply chain risk.

> **Origin trace:** "This figure appears in SCMP, Tom's Hardware, Microchip USA, and the report, all sourcing it from China's commerce ministry statement. None independently verified it. The actual overall market share is 9.7%." — Adversarial Critique, China tech/trade assessment
>
> **Classification: MANUFACTURED** — Single interested source (China's commerce ministry has incentive to inflate the figure to maximize perceived leverage). The ~40% figure applies to the automotive segment only; overall global share is 9.7% per Nexperia's own 2024 annual report. *Source: china-critique.md, Manufactured Consensus Check*

### China: Think Tank "Bifurcated Ecosystem" Convergence (March 2026)

Multiple prestigious think tanks converged on the same synthesis despite ostensibly independent analysis.

> **Circular citation detected:** "CFR, Brookings, CSIS, and the report itself all arrive at essentially the same synthesis despite starting from different premises. This convergence is suspicious. Test: are they reading each other? Yes — CFR cites Brookings, Brookings cites CSIS, all cite the same pool of SemiAnalysis data. This is circular citation, not independent convergence." — Adversarial Critique, China tech/trade assessment
>
> **Classification: GROUPTHINK** — Shared data source (SemiAnalysis) + cross-citation + same professional network produced agreement without coordination but also without independence. *Source: china-critique.md, Manufactured Consensus Check*

### Anthropic: "Standing Up for Safety" Narrative (March 2026)

Effective corporate PR created the appearance of independent consensus around a framing that served the company's brand positioning.

> **Consensus indicators:** "Anthropic's PR team crafted a carefully worded statement (Dario Amodei blog post) that was widely quoted verbatim... The framing shifted from 'contract dispute' to 'David vs. Goliath safety story' within 48 hours. App Store charts created a self-reinforcing loop: public support -> downloads -> 'proof' of support -> more coverage." — Adversarial Critique, Anthropic assessment
>
> **Classification: PARTIALLY MANUFACTURED** — PR successfully shaped the dominant frame, but substantive independent journalism also occurred (WaPo on Iran targeting, The Intercept on contract language, EFF structural critique). The "both principled AND strategic" conclusion appeared across multiple analyses as a "path of least resistance" for analysts. *Source: anthropic-critique.md, Manufactured Consensus Check*

## Integration

| Skill | Relationship |
|-------|-------------|
| **iterative-verification** | Convergence Warning Protocol (Section in iterative-verification) triggers this skill; this skill provides the detailed detection methodology |
| **deep-investigation-protocol** | Affiliate/SEO Gaming Detection is a product-domain instance of manufactured consensus; this skill generalizes the pattern |
| **source-omission-analysis** | Complementary — omission analysis maps what sources DON'T say; this skill tests what they DO say in unison |
| **cui-bono** | Contradiction Analysis methods (Direct, Deductive, Falsification, Standpoint) apply to testing whether consensus survives challenge |
| **frame-rotation** | When manufactured consensus is detected, frame-rotation helps find the perspective that the manufactured narrative was designed to displace |
| **engage-the-disfavored** | Intake-time counterpart: a manufactured label-consensus ("fringe"/"conspiracist" echoed downstream) is exactly what pre-discounts a disfavored source before its facts are read — map the label's consensus here, engage the source there |

**Workflow position:** Invoke when convergence warning fires during iterative-verification, OR when the source-omission-analysis reveals that everyone is saying the same thing. Run BEFORE accepting consensus as evidence in the dialectic spiral.

## Self-Reflexivity

This skill's four-type taxonomy (genuine/manufactured/groupthink/confirmation bias) is itself a frame that could manufacture its own consensus — once you have the categories, you may see everything through them. If a pattern of agreement doesn't fit these four types, or if the taxonomy itself is leading you to a predetermined conclusion, override it.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
