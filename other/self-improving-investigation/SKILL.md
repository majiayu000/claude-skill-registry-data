---
name: self-improving-investigation
description: >-
  Am I investigating, or just confirming what I already believe? Self-correcting
  research methodology combining blind worker agents, nested iteration loops, and
  dialectic synthesis. Use when (1) research requires factual certainty not just
  plausibility, (2) topic has high bias risk, (3) multiple perspectives must be
  systematically tested, (4) user explicitly requests deep/thorough investigation,
  (5) previous single-pass research proved insufficient. Integrates with
  iterative-loop-engine and deep-investigation-protocol.
---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

# Self-Improving Investigation Methodology

**Seed Question:** *Am I investigating, or just confirming what I already believe?*

## Status: DESCRIPTIVE, NOT PRESCRIPTIVE

**Version:** 1.2 (2026-03-09) - Added source diversity framework integration, worker source assignment, dialectic source category checking

This methodology emerged from actual use, not theory. It documents what worked during real investigation, with notes on what could be improved. **It is open to further improvement through iteration.**

Treat this as a starting point, not a rulebook. If something doesn't work for your task, adapt it and document what you learned.

### Recent Improvements (v1.2)
- **Source diversity in worker assignment** - Assign workers sources from DIFFERENT categories to prevent perspective monoculture
- **Dialectic source category check** - Verify thesis and antithesis come from different source categories
- **Integration with SOURCE_DIVERSITY_FRAMEWORK.md** - Full source taxonomy for multi-perspective research

### Previous Improvements (v1.1)
- **Parallel loops** - Run independent research dimensions simultaneously to prevent bias transfer
- **Multiple antitheses** - Seek 4+ antitheses, not just one; each challenges different assumption
- **Conceptual distinction emergence** - Watch for vague terms that need splitting into distinct concepts

---

## Core Architecture

### The Problem Being Solved

Standard research suffers from:
1. **Confirmation bias** - Finding evidence for pre-existing beliefs
2. **Premature exit** - Stopping when "good enough" instead of when criteria pass
3. **Context pollution** - Previous conclusions influencing new research
4. **Single-perspective analysis** - Missing counter-arguments and alternatives

### The Solution: Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: ORCHESTRATION                                  │
│ (Main session - sees everything, intervenes minimally)  │
├─────────────────────────────────────────────────────────┤
│ LAYER 2: BLIND WORKERS                                  │
│ (Fresh context per task - no awareness of orchestration)│
├─────────────────────────────────────────────────────────┤
│ LAYER 3: DIALECTIC SYNTHESIS                           │
│ (Thesis → Antithesis → Synthesis for each major claim) │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 1: Orchestration

**Role:** Observe, judge, minimally intervene.

### Orchestrator Responsibilities

1. **Define completion criteria BEFORE starting**
2. **Spawn blind workers** with task-only prompts
3. **Read worker output** (one-way data flow)
4. **Judge whether intervention needed**
5. **Log orchestrator decisions** for methodology improvement
6. **Synthesize findings** using dialectic method

### Minimal Intervention Principle

| Situation | Orchestrator Action |
|-----------|---------------------|
| Worker producing good results | **DO NOTHING** |
| Minor inefficiency | **DO NOTHING** |
| Clear bias emerging | **MINIMAL prompt modification** |
| Fundamental approach wrong | **Brief redirect** |
| Multiple issues | **Consult user** |

**Ideal:** Prompt stays EXACTLY the same across iterations.
**Reality:** Sometimes minimal changes needed - but RESIST the urge.

---

## Layer 2: Blind Workers

**Critical:** Workers must be BLIND to orchestration.

### What Workers DON'T Know

- That they're part of a loop
- That they're called "workers"
- What iteration this is
- That logs exist
- That orchestration is happening

### Worker Prompt Pattern

```
[Task description only]

Use web search extensively. Label each finding:
- VERIFIED: Primary sources, official statements
- CREDIBLE: Multiple independent sources
- ALLEGED: Single source
- SPECULATIVE: Inference from patterns

Write findings to [output location].
```

**No meta-context. No "previous iteration found X." Just the task.**

### Source Diversity in Worker Assignment

**Critical**: Assign workers sources from DIFFERENT categories to prevent perspective monoculture.

When spawning multiple blind workers on the same topic:
- Worker A gets Western mainstream + independent investigative sources
- Worker B gets non-Western/Global South + anti-interventionist sources
- Worker C gets financial/market + think tank sources (with funding noted)

This is the research equivalent of jury selection — different vantage points produce different signal.

See `SOURCE_DIVERSITY_FRAMEWORK.md` (in the cui-bono skill) for the full source taxonomy with 6 categories, outlet-level strengths/weaknesses, and think tank funding maps.

### Why Blindness Matters

1. **Prevents confirmation of previous conclusions**
2. **Fresh perspective on each pass**
3. **Avoids "groove deepening" (reinforcing existing patterns)**
4. **Context rot** - LLM performance degrades as context fills
5. **Source diversity** - Different workers using different source categories prevents echo chamber

---

## Layer 3: Dialectic Synthesis

**Method:** Thesis → Antithesis → Synthesis

For each major claim from worker research:

### Step 1: State Thesis
What does the evidence suggest?

### Step 2: Find Antithesis
What would DISPROVE this? What counter-evidence exists?

### Step 3: Synthesize
What nuanced conclusion accounts for both thesis and antithesis?

### Source Category Check

During synthesis, verify: **Do thesis and antithesis come from the same source category?**

If both thesis and antithesis come from, say, Western mainstream sources — you haven't actually tested the claim against a different vantage point. You've found disagreement within one perspective.

True dialectic requires sources positioned differently relative to power, geography, and economic interest. A thesis from the Financial Times and an antithesis from Al Jazeera or Responsible Statecraft tests the claim more rigorously than FT vs Bloomberg (same category, same vantage).

### Example

**Thesis:** European illustrators can't access US children's book market.
**Antithesis:** Some European illustrators DO succeed in US market.
**Synthesis:** Market access is theoretically possible but structurally constrained through specific barriers (tax, agents, style). Success requires specific pathways (prizes, diversity initiatives).

---

## Nested Loop Structure

Combine with `iterative-loop-engine` for multi-level investigation:

```
OUTER LOOP: Investigation completion
├── INNER LOOP 1: Define terms/scope
├── INNER LOOP 2: Region/category A research
├── INNER LOOP 3: Region/category B research
├── ...
├── INNER LOOP N: Cross-category synthesis
└── EXIT when all criteria pass
```

Each inner loop follows `iterative-loop-engine` criteria:
- Define completion criteria
- Execute passes until criteria pass
- Never claim completion with failing criteria

---

## Evidence Tier System

| Tier | Definition | Usage |
|------|------------|-------|
| **VERIFIED** | Primary sources, official statements, regulatory filings | Can be stated as fact |
| **CREDIBLE** | Multiple independent sources agree | Can be stated with high confidence |
| **ALLEGED** | Single source, unverified | Must note source and uncertainty |
| **SPECULATIVE** | Inference from patterns | Must clearly label as inference |

---

## Completion Criteria

Investigation is complete when:

- [ ] All planned inner loops executed
- [ ] Evidence labeling ≥80% of claims
- [ ] Independent sources ≥2 per major claim
- [ ] Dialectic synthesis completed for major findings
- [ ] Counter-arguments explicitly addressed
- [ ] Nuanced conclusion (not binary unless evidence is binary)
- [ ] Limitations admitted

**Promise:** `ALL FALSIFICATION CRITERIA PASS`

---

## What Worked (From Actual Use)

### Effective Patterns

1. **Blind worker agents** - Each produced comprehensive, unbiased research
2. **Nested loop structure** - Clear progression from definition → research → synthesis
3. **Evidence tier labeling** - Made verification explicit, prevented overclaiming
4. **Dialectic synthesis** - Forced consideration of counter-arguments
5. **NO TOKEN LIMIT directive** - Allowed thorough investigation

### Areas for Improvement

1. **Adversarial verification** - Did not spawn dedicated falsification agents
2. **Cross-source triangulation** - Could structure explicit cross-validation
3. **Orchestrator intervention logging** - Should formally track prompt mutations
4. **Quantitative gaps** - Some claims rely on qualitative reports

See `layers/improvement-notes.md` for detailed analysis.

---

## Integration Points

- **iterative-loop-engine** - Provides loop structure and criteria files
- **deep-investigation-protocol** - Provides evidence flow tracing and bias detection
- **cui-bono** (if available) - Provides power structure analysis for complex topics
- **cui-bono/SOURCE_DIVERSITY_FRAMEWORK.md** - Source taxonomy for multi-perspective worker assignment and dialectic source category checking
- **frame-rotation** - Can help escape stuck thinking patterns

---

## Quick Start

1. **Define what "done" looks like** - Explicit criteria
2. **Design inner loops** - What regions/categories need separate research?
3. **Spawn blind workers** - Task-only prompts, no meta-context
4. **Collect findings** - Let workers write to designated outputs
5. **Synthesize with dialectic** - Thesis → Antithesis → Synthesis
6. **Check criteria** - All pass? Done. Gaps? Iterate.

---

## Logging (CRITICAL for Improvement)

### Public Logs (Git-tracked)

- Methodology evolution notes
- Anonymized patterns observed
- Improvement suggestions

Location: This skill directory

### Private Logs (Gitignored)

- Full research transcripts with personal data
- Specific user queries
- Detailed intermediate outputs

Location: `.claude/local/research-logs/`

Reference private logs from public methodology notes WITHOUT including personal content.

---

## Generalization Notes

### Applies To (Tested)
- Multi-market research (cultural differences)
- Product/brand investigation (from deep-investigation-protocol)
- Factual accuracy verification

### May Apply To (Untested - Experiment Carefully)
- Technical architecture decisions
- Code review with bias concerns
- Creative research (style exploration)

### Probably Doesn't Apply To
- Simple Q&A
- Implementation tasks with clear specs
- Tasks without verification criteria

**When uncertain:** Try it, document results, update this section.
