---
name: scpr-framework
description: "Structure executive communications using McKinsey SCPR framework (Situation, Complication, Problem, Recommendation). Produces crisp, actionable executive memos with MECE recommendations."
---

# /scpr -- McKinsey SCPR Framework for Executive Communication

Structure strategic arguments using Situation-Complication-Problem-Recommendation format. Produces crisp, actionable executive memos with MECE recommendations and time-bound actions.

> Before executing, read `../../_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **No MCP required** -- SCPR is a pure analytical framework
- Works with any domain data provided by the user or retrieved from other skills

## Usage Modes
- `/scpr` -- Interactive: asks clarifying questions, then builds full SCPR
- `/scpr <topic>` -- Direct: generate SCPR analysis on a given topic
- `/scpr --review <text>` -- Critique an existing SCPR for structural issues
- `/scpr --template` -- Output a blank SCPR template with guidance notes

## The Four Elements

| Element | Purpose | Length | Common Mistake |
|---------|---------|--------|----------------|
| **Situation** | Baseline facts everyone agrees on | 2-3 sentences | Too long, includes opinions |
| **Complication** | What changed or is changing | 2-3 sentences | Conflated with Problem |
| **Problem** | The crisp question to answer | 1 sentence, as a question | Too vague or too broad |
| **Recommendation** | Actionable, time-bound answers | 3-5 bullets, MECE | No timelines, overlapping actions |

## Critical Distinction: Complication vs Problem

| | Complication | Problem |
|---|---|---|
| **Nature** | An external change or force | A strategic question |
| **Grammar** | Statement (declarative) | Question (interrogative) |
| **Focus** | What happened | What should we do about it |
| **CRE example** | "Class B office vacancy rose from 12% to 22% over 18 months" | "Should we reposition to life sciences or invest in amenity upgrades?" |
| **PE example** | "Largest customer (28% of revenue) announced in-house competing capability" | "How should we protect revenue while maintaining the exit timeline?" |

## Workflow

### Step 1: Gather Context
Identify: domain (PE, CRE, LP, fund, platform), stakeholders (IC, Board, LP, team), urgency (timeline for decision).

### Step 2: Build the Situation
Write 2-3 sentences of verifiable facts. No opinions, no adjectives like "strong" or "concerning." Include 1-2 quantitative anchors.

### Step 3: Identify the Complication
Write 2-3 sentences describing what CHANGED. Test: "What is different now compared to 6 months ago?"

### Step 4: Crystallize the Problem
Write exactly 1 sentence as a question. Must be specific enough that answering it leads directly to action. Format: "Should [entity] [option A] or [option B] given [constraint]?"

### Step 5: Develop Recommendations
Write 3-5 bullets. Each follows: "[Action verb] [specific action] by [date], [expected outcome]. Owner: [who]."

MECE test:
1. Could any two recommendations be merged? If yes, overlap exists.
2. If all executed, is the Problem fully answered? If no, gap exists.

### Step 6: Validate Structure
- [ ] Situation contains only verifiable facts
- [ ] Complication describes a change, not a problem statement
- [ ] Complication is distinct from Problem
- [ ] Problem is exactly 1 question
- [ ] Each Recommendation has action + deadline + owner
- [ ] Recommendations are MECE
- [ ] Total length fits on 1 page (~400 words max)

## Output Format

```markdown
## SCPR Analysis: [Title]

**Prepared for**: [Audience]  |  **Date**: [Date]  |  **Domain**: [PE / CRE / LP / Fund]

### Situation
[2-3 sentences of verifiable baseline facts with quantitative anchors]

### Complication
[2-3 sentences describing what changed, with evidence and trend direction]

### Problem
[1 sentence as a question -- specific, answerable, single-threaded]

### Recommendations
1. **[Action verb + specific action]** by [date]
   - Expected outcome: [quantified result]
   - Owner: [who]

2. **[Action verb + specific action]** by [date]
   - Expected outcome: [quantified result]
   - Owner: [who]

3. **[Action verb + specific action]** by [date]
   - Expected outcome: [quantified result]
   - Owner: [who]
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Situation includes opinions | Audience may disagree, erodes trust | Strip to facts and numbers |
| Complication = Problem | Skips diagnostic step | Separate: what changed? vs what do we do? |
| Problem is a statement | Not answerable, no decision point | Rewrite as "Should we X or Y?" |
| Vague recommendations | Not actionable | Add action + owner + deadline + outcome |
| Non-MECE recommendations | Confuses execution | Test: can any two merge? Full coverage? |

## Rules
- Never skip any of the 4 elements
- Situation must be 3 sentences or fewer
- Problem must be exactly 1 question
- Each recommendation: action + owner + deadline + expected outcome
- Total output fits on 1 page (~400 words)

## Related Skills
- `/consulting-strategy` -- Strategic analysis frameworks feeding into SCPR
- `/deal-memo-writer` -- Investment memos that may use SCPR structure
- `/competitive-analysis` -- Competitive evidence for SCPR arguments

## Confidence Calibration

Apply three-pass calibration per `../../_shared/plugin-context.md` SteerConf protocol. SCPR quality depends on input data quality -- flag where Situation facts are unverified or Complication trends are ambiguous.
