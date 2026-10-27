---
name: source-omission-analysis
description: >-
  "What is everyone NOT saying about this?" - After any multi-source research
  sweep, analyze what each perspective is SILENT about. Omissions reveal
  structural position more reliably than statements. Use when (1) after
  completing multi-source research, (2) comparing coverage across ideological
  positions, (3) a claim appears in some sources but not others, (4)
  evaluating media bias or narrative framing.
---

# Source Omission Analysis

**Seed question:** *What is everyone NOT saying about this?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

What a source is silent about reveals its structural position more reliably than what it says — because statements are cheap and can be strategic, while sustained silence is costlier to maintain and harder to fake. Every source occupies a position relative to power, funding, and ideology. That position determines what it can see — and what it structurally cannot or will not see.

Silence is not absence of opinion. Silence is evidence that a topic is inconvenient for that source's position.

**The anti-pattern this counters:**
```
❌ Analyzing only what sources SAY
❌ Treating absence of coverage as absence of relevance
❌ Assuming silence means agreement or ignorance
```

**The pattern this enforces:**
```
✅ After gathering sources, map what each is SILENT about
✅ Treat omission as informative signal, not neutral gap
✅ Cross-reference omissions to find structurally hidden truths
```

## When This Applies

**TRIGGER:**
- After completing a multi-source research sweep (especially multi-bubble per comprehensive methodology)
- When comparing how different outlets cover the same event
- When a claim appears in some source categories but not others
- When evaluating media bias, narrative framing, or information warfare
- When an investigation feels "complete" but something feels missing

**DO NOT TRIGGER:**
- Single-source fact checks (need multiple sources to compare omissions)
- Technical how-to questions
- Preference or opinion questions
- When user explicitly wants quick answer

## The Omission Map Protocol

After gathering sources from multiple perspectives, construct this table:

```markdown
| Topic/Claim | Who Reports It | Who Is Silent | What Does Silence Suggest? |
|-------------|---------------|---------------|---------------------------|
| [Event X]   | [Sources A, B] | [Sources C, D] | [C's funding depends on...; D's position requires...] |
| [Claim Y]   | [Sources E]    | [Sources A-D, F] | [Only E reports → check if manufactured or genuinely underreported] |
| [Pattern Z] | [None explicitly] | [All sources] | [Universal silence → structurally invisible or actively suppressed] |
```

### Building the Map

**Sweep-omission guard.** Before analyzing what sources omit, audit what your own sweep omitted: does the source set include fact-based analyses favoring the disfavored side, or was the set itself valence-filtered at intake? An omission map built on a filtered set reports your filter as everyone's silence. (Intake counterpart: engage-the-disfavored.)

1. **List all claims and events** from your research sweep
2. **For each claim, note which source categories reported it** (use bubble taxonomy A-J from comprehensive methodology if available)
3. **For each claim, note which source categories are silent**
4. **For each silence, hypothesize WHY** — funding? access dependency? ideological commitment? audience expectations?
5. **Look for patterns across silences** — when the same source is silent about multiple related topics, that maps its structural blind spot

## Common Omission Patterns

| Source Type | Tends to Omit | Structural Reason |
|-------------|--------------|-------------------|
| **Western mainstream** (CNN, NYT, BBC) | Allied military atrocities, civilian casualties by Western forces, structural economic violence | Access-dependent on government sources; audience expects "our side" framing |
| **Anti-interventionist** (Quincy, Jacobin, Greenwald) | Genuine security threats from adversaries, complexity of authoritarian governance, atrocities by actors the West opposes | Structural opposition to Western policy can create reflexive contrarianism |
| **State media** (RT, CGTN, Press TV) | Anything unflattering to the sponsoring state | Definitionally — that is the source's function |
| **Financial press** (Bloomberg, WSJ, Economist) | Human costs, environmental externalities, labor conditions, regulatory capture | Audience is investors; costs borne by non-investors are externalities |
| **Think tanks** (CSIS, Brookings, Heritage) | Conclusions that would displease their funders | Funding dependency shapes research agenda and publishable conclusions |
| **Progressive media** (MeidasTouch, TYT, Mother Jones) | Trade-offs without progressive solutions, complexity that undermines clean narratives, inconvenient data | Audience expects actionable hope; pure complexity without solution doesn't serve that |

## Interpreting Omissions

### What Silence DOES Mean

- The topic is **inconvenient** for that source's position, audience, or funders
- The source **may lack access** to information in that domain
- The topic **falls outside** the source's self-defined scope
- Covering it would **create cognitive dissonance** with the source's other positions

### What Silence DOES NOT Mean

- The claim is false (silence ≠ refutation)
- The source disagrees (silence ≠ disagreement)
- The topic is unimportant (silence ≠ irrelevance)

### The Intersection Pattern

The most important findings often emerge from the **intersection of omissions**:

- When Source A omits X and Source B omits Y, but both X and Y are verified, you have mapped two structural blind spots
- When ALL sources omit Z, that is either genuinely unimportant OR the most structurally hidden finding
- When sources from opposed positions BOTH omit the same topic, that topic likely threatens both positions (e.g., class analysis omitted by both corporate media and identity-focused media)

## Output Pattern

```markdown
## Source Omission Analysis

### Omission Map
| Topic/Claim | Reported By | Silent Sources | Silence Interpretation |
|-------------|------------|----------------|----------------------|
| ...         | ...        | ...            | ...                  |

### Key Omission Patterns
1. [Pattern]: [Which sources share this omission and what it reveals]
2. [Pattern]: ...

### Structurally Hidden Findings
- [What the omission analysis surfaced that direct analysis missed]

### Blind Spot Self-Check
- My own structural position may cause me to miss: [...]
- Sources I am most sympathetic to omit: [...]
```

## Examples from Practice

### Iran: Internal Dynamics Omission (March 2026)

All source positions covering the Iran war — mainstream, anti-interventionist, Gulf media, Global South — were silent about the December 2025 protests context for internal dynamics analysis.

> **Omission:** "30,000+ killed by regime. Largest uprising since 1979. Report mentions pre-war protests once in passing but doesn't integrate this into its analysis of internal dynamics. This is the single most important omission." — Adversarial Critique, Iran assessment
>
> **What silence revealed:** Without this context, the "rally around the flag" claim went unchallenged. The omission map surfaced evidence of celebrations in 7+ cities, contradicting the dominant narrative. *Source: iran-critique.md, Source Omission Map*

### China: Iran War Omission in Tech/Trade Report (March 2026)

A comprehensive tech/trade investigation covering the Trump-Xi summit made zero mentions of the Iran war — the largest geopolitical variable affecting the summit.

> **Omission:** "The Iran war. The report was written on March 11, 2026 — Day 12 of the US-Israel military campaign against Iran. This is the single largest geopolitical variable affecting the Trump-Xi summit, rare earth politics, oil prices, and global trade patterns, yet it receives ZERO mentions." — Adversarial Critique, China tech/trade assessment
>
> **What silence revealed:** Wang Yi's "thorough preparations needed" and "remove unnecessary disruptions" language was clearly referencing Iran, but the report's probability distributions were calculated without this variable. *Source: china-critique.md, Source Omission Analysis*

### Corporate Positioning: Key Researcher Departure Omission (March 2026)

An investigation of a company's public stance omitted the resignation of its head of safety research two weeks before a major policy release.

> **Omission:** The head of safety research departing with public concerns about the company's direction is material evidence. It was absent from the initial report entirely — the adversarial critique surfaced it.
>
> **What silence revealed:** The omission protected the "company standing up for safety" narrative. Including the departure materially weakened the "genuinely principled" probability assessment (revised down from 70-80% to 55-70% after the critique surfaced it).

## Integration

This skill connects to the research-toolkit ecosystem:

| Skill | Relationship |
|-------|-------------|
| **deep-investigation-protocol** | Use omission analysis after Stage 2 (Flow Tracing) to identify gaps in the evidence chain |
| **iterative-verification** | Omissions can downgrade evidence tiers — if only one source position reports a claim, it stays ALLEGED until independently verified |
| **cui-bono** | SOURCE_DIVERSITY_FRAMEWORK provides source position examples; omission analysis is the complementary technique |
| **frame-rotation** | When omission analysis reveals a blind spot, frame-rotation can shift perspective to see what was hidden |
| **manufactured-consensus-detection** | When all sources AGREE (opposite of omission), check for manufactured consensus |

**Workflow position:** Run AFTER multi-source sweep, BEFORE final synthesis. The omission map should inform the dialectic spiral — the critic should challenge findings that only appear in one source position.

## Self-Reflexivity

This skill maps what sources omit — but the skill itself omits. Its source-type categories embed assumptions about how media works. Its "common omission patterns" table is a claim about reality that could be wrong. If you detect this framework obscuring rather than revealing, say so and adapt.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
