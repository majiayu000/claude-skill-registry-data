---
name: deep-research
description: >
  Use when conducting deep research on any topic that benefits from multiple behavioral
  perspectives, evidence gathering, and adversarial verification. Deploys math-optimized
  persona pairs with web search, source verification, and structured evidence synthesis.
  Beats single-perspective deep research (Perplexity, DeepSeek) by producing 3-4
  independent research tracks with productive tension and conviction-scored verdicts.
---

# Constellation Deep Research

Multi-perspective deep research engine that deploys math-optimized persona pairs to investigate any question. Each pair conducts independent research with web search, then debates findings internally. Captain synthesizes across all tracks.

## Why This Beats Single-Perspective Research

| Perplexity / DeepSeek | Constellation Deep Research |
|---|---|
| 1 agent, 1 perspective | 3-4 optimized pairs, 6-8 behavioral lenses |
| Finds consensus | Finds productive disagreement |
| "Here's what the internet says" | "Here's what 4 teams found independently" |
| No blind spot detection | Blind spots ARE the product |
| Neutral tone | Each pair has behavioral signature |
| Research → report | Research → verdict with conviction scores |
| No adversarial check | Pairs stress-test each other's findings |

## Commands

| Command | Pair Selection | Purpose |
|---|---|---|
| `/deep-research <question>` | Auto-select | General deep research |
| `/deep-research competitive <topic>` | Knowledge Bomb + Controlled Burn + Recon | Competitive intelligence |
| `/deep-research technical <topic>` | Mirror Match + Knowledge Bomb + Recon | Technical deep dive |
| `/deep-research market <topic>` | Knowledge Bomb + The Humanitarian + The Bridge | Market/people research |

## Research Pair Roles

| Combo | Research Role |
|---|---|
| **Knowledge Bomb** (Analyzer + Persuader) | Core research. Finds evidence, packages for impact. ALWAYS included. |
| **Mirror Match** (Maverick + Specialist) | Innovation scan. Finds what nobody's tried, verifies feasibility. |
| **Controlled Burn** (Maverick + Guardian) | Risk assessment. Finds the bold angle, checks what could blow up. |
| **Recon** (Analyzer + Adapter) | Terrain mapping. Scouts adjacent spaces, stages context. |
| **The Humanitarian** (Altruist + Controller) | Impact analysis. Who benefits, who's harmed, what's the human cost. |
| **The Bridge** (Collaborator + Controller) | Stakeholder mapping. Who needs to know, how to translate findings. |

## Execution Protocol

### Step 1: Parse Query
Extract: research question, depth (quick/standard/deep), scope, pair override.

### Step 2: Select Research Pairs
Default: Knowledge Bomb (always) + 2-3 pairs based on query type.

### Step 3: Write Research Brief
~200 token brief: question, known context, what we're looking for, scope boundaries.

### Step 4: Dispatch Research Pairs (Parallel)

Each pair subagent gets:
- Both persona profiles
- The research brief
- Access to web search and web fetch tools
- Instructions to conduct independent research AND debate findings

**IMPORTANT:** All pairs dispatch in a SINGLE message (parallel).

Each subagent prompt:

```
You are a RESEARCH PAIR: {COMBO_NAME} ({PERSONA_A} + {PERSONA_B}).
Pair Math: Balance {BALANCE}, Energy {ENERGY}.

## Research Question
{BRIEF + QUESTION}

## Your Research Task
1. Use WebSearch and WebFetch to investigate the question
2. Gather 3-5 high-quality sources
3. Debate findings as {PERSONA_A} and {PERSONA_B}
4. Deliver a joint research verdict

## Format

### Sources Found
1. [Source title](URL) — key finding
2. [Source title](URL) — key finding
3. ...

### Research Discussion
{PERSONA_A}: [initial findings, in character]
{PERSONA_B}: [challenges, adds rigor, in character]
{PERSONA_A}: [responds]
{PERSONA_B}: [final verification]

### {COMBO_NAME} RESEARCH VERDICT
- Key finding: [one clear statement backed by evidence]
- Evidence strength: [strong/moderate/weak]
- Gaps in evidence: [what we couldn't find or verify]
- Recommended follow-up: [specific next research step]
- Conviction: [0-10]
```

### Step 5: Collect Research Tracks
Parse each pair's findings, sources, evidence strength, and verdict.

### Step 6: Cross-Reference Sources
- Flag contradictions between pairs
- Identify sources cited by multiple pairs (high confidence)
- Note gaps where no pair found evidence

### Step 7: Captain Synthesis
Synthesize across all research tracks:
- **Consensus findings** — what all pairs agree on, with sources
- **Contested findings** — where pairs disagree, with evidence for each side
- **Blind spots** — what no pair investigated
- **Source quality map** — which sources are most/least reliable
- **Actionable conclusions** — ranked by evidence strength and conviction

### Step 8: Persist Report
Write to `~/Desktop/Airlock/repos/airlock-coordination/reports/`
Include: `format: deep_research`, `pairs:`, `sources:`, `evidence_map:`.

### Step 9: Render Report

```
══════════════════════════════════════════════════
  CONSTELLATION DEEP RESEARCH
  Query: "{question}"
  Date: {date} | Research Pairs: {count}
  Sources: {total_sources} | Avg Conviction: {N}
══════════════════════════════════════════════════

RESEARCH BRIEF
{brief}

──────────────────────────────────────────────────
{COMBO_NAME} — Research Track
Sources: {N} | Evidence: {strong/moderate/weak} | Conviction: {N}

Key Finding: {finding}
Sources:
  1. {source + key takeaway}
  2. {source + key takeaway}

Discussion Highlights:
  {PERSONA_A}: {key point}
  {PERSONA_B}: {key challenge/addition}

Gaps: {what couldn't be verified}
──────────────────────────────────────────────────

(repeat for each pair)

══════════════════════════════════════════════════
  EVIDENCE MAP
  Strong (cited by 2+ pairs): {findings}
  Moderate (single pair, good source): {findings}
  Weak (single pair, limited source): {findings}
  Contested: {finding} — {pair_A} says X, {pair_B} says Y
══════════════════════════════════════════════════

SYNTHESIS
{Captain's synthesis with ranked conclusions}

Recommended Actions:
1. {action + evidence strength}
2. {action + evidence strength}
══════════════════════════════════════════════════
```

## Cost Comparison

| Service | Cost | Perspectives | Adversarial Check |
|---|---|---|---|
| Perplexity Pro | $20/mo flat | 1 | No |
| Deep Research (3 pairs) | ~$0.20/query | 6 | Yes, per-pair |
| Deep Research (4 pairs) | ~$0.30/query | 8 | Yes, per-pair |

100 deep research queries/month = ~$25. Comparable to Perplexity Pro but with behavioral optimization, adversarial tension, and conviction scoring.

## The Moat

Nobody else has the sovereign balance math to know WHICH pairs to deploy for WHICH type of question. The 136-pair matrix ranked by behavioral mathematics is not a prompt trick — it's a research methodology grounded in PI behavioral science. Perplexity can't replicate behavioral tension because they don't have the framework underneath.
