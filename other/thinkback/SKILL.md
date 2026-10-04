---
name: thinkback
description: When the user wants to review past decisions, understand why something was built a certain way, audit decision quality, or learn from past reasoning. Use when the user says "why did we," "look back," "thinkback," "decision review," "was that the right call," "what were we thinking," "review our decisions," "decision audit," "trace back," "replay thinking," or when revisiting old code and needing to understand the reasoning behind it.
metadata:
  version: 1.0.0
  inspired_by: thinkback/thinkback-play commands
---

# Thinkback — Decision Archaeology & Reasoning Replay

You are a decision archaeologist. You dig up past decisions, reconstruct the reasoning that led to them, evaluate whether those reasons still hold, and extract lessons for future decision-making.

## Why Thinkback Exists

Every codebase is a fossil record of decisions. Most of those decisions made sense when they were made — but the context that justified them is lost. Developers inherit code and either: (a) blindly preserve decisions they don't understand, or (b) blindly undo decisions that were actually good. Thinkback prevents both.

## Three Modes

### Mode 1: Decision Archaeology (`/thinkback dig [topic]`)

Reconstruct the full reasoning chain behind a past decision.

#### The Dig Process:

**Step 1: Evidence Collection**
Gather every trace of the decision:

```
Evidence Sources:
1. Git blame — who wrote this code, when, what commit message?
2. Git log — what changed around the same time?
3. PR history — was there a PR? What was discussed?
4. Comments in code — any TODO, HACK, FIXME, NOTE annotations?
5. Decision files — LINEAGE.md, ADRs, design docs?
6. Memory files — MEMORY.md, SCARS.md references?
7. The code itself — what does the implementation reveal about intent?
8. Dependencies added — what was introduced around the same time?
9. Config changes — did environment or settings change?
10. Test files — what was tested (and what wasn't)?
```

**Step 2: Context Reconstruction**
Build a picture of the world when the decision was made:

```
DECISION CONTEXT:
═══════════════════
When: [date from git blame/log]
Who: [author]
What existed then:
- [tech stack at the time]
- [scale/usage at the time]
- [team size/skills at the time]
- [constraints that may no longer exist]

What didn't exist yet:
- [features built after this decision]
- [tools/libraries that now exist]
- [requirements that came later]
```

**Step 3: Reasoning Reconstruction**
Based on the evidence, reconstruct the likely reasoning:

```
RECONSTRUCTED REASONING:
═══════════════════════
The decision was: [what was decided]

Likely because:
1. [First reason — evidence: commit message / code pattern / timing]
2. [Second reason — evidence: dependency added / test written]
3. [Third reason — evidence: config change / comment in code]

Alternatives they likely considered:
- [Alternative A] — probably rejected because [reason]
- [Alternative B] — probably rejected because [reason]

Confidence in this reconstruction: [HIGH / MEDIUM / LOW]
- [Why this confidence level — what evidence is strong/weak]
```

**Step 4: Present the Archaeology**

```markdown
## Decision Archaeology: [Topic]

### The Decision
[What was decided, in one sentence]

### The Evidence
[List of sources consulted with key findings]

### The Reconstructed Reasoning
[Why this decision was likely made, with evidence for each reason]

### What's Changed Since
[Factors that have changed since the decision was made]
- [New constraint or capability]
- [Scale change]
- [Team change]
- [Technology change]

### Verdict
[STILL VALID / NEEDS REVIEW / SHOULD CHANGE]
[Explanation of why]

### If Changing
[What the new decision should be and what migration looks like]
```

---

### Mode 2: Decision Audit (`/thinkback audit`)

Review multiple recent decisions for quality and consistency.

#### The Audit Process:

**Step 1: Collect Decisions**
Scan for decisions made in a time period:
- Recent commits with architectural changes
- LINEAGE.md entries
- Design documents
- Dependency additions/removals
- Config changes
- Significant refactors

**Step 2: Evaluate Each Decision**

Score on five dimensions:

| Dimension | Question | Score (1-5) |
|-----------|----------|-------------|
| **Reversibility** | How easy is this to undo if wrong? | |
| **Evidence** | Was this based on data or gut feeling? | |
| **Alternatives** | Were other options explored? | |
| **Documentation** | Can someone understand WHY 6 months from now? | |
| **Alignment** | Does this serve the stated goals? | |

**Step 3: Pattern Analysis**

Look for decision-making patterns:
- Are we consistently choosing complexity over simplicity?
- Are we making decisions under time pressure without recording rationale?
- Are we revisiting the same decisions repeatedly? (decision churn)
- Are we ignoring risks we've been burned by before?
- Are we over-indexing on one voice/perspective?

**Step 4: Audit Report**

```markdown
## Decision Audit — [Period]

### Decisions Reviewed: [N]

### Quality Distribution
- Strong decisions (score 20+): [N]
- Adequate decisions (score 15-19): [N]
- Weak decisions (score <15): [N]

### Patterns Detected
- [Pattern 1] — [frequency] — [impact]
- [Pattern 2] — [frequency] — [impact]

### Decisions That Need Revisiting
1. [Decision] — reason: [context changed / evidence was weak / alternatives exist now]

### Decision-Making Recommendations
- [Suggestion for improving future decision quality]
```

---

### Mode 3: Reasoning Replay (`/thinkback play [session/feature]`)

Replay the thinking process from a past session or feature build to extract lessons.

#### The Replay Process:

**Step 1: Find the Trail**
Locate the session or feature's history:
- Git log for the branch/feature
- Session review notes if they exist
- MEMORY.md entries from that period
- Code evolution (first commit → final state)

**Step 2: Reconstruct the Journey**

```
REASONING REPLAY: [Feature/Session]
═══════════════════════════════════

Turn 1: Started with [initial approach]
Reason: [why this seemed right]

Turn 2: Hit [obstacle]
Response: [how we adapted]
Insight: [what this revealed]

Turn 3: Changed direction to [new approach]
Reason: [what evidence triggered the pivot]

Turn 4: [Final approach settled]
Result: [outcome]

HINDSIGHT NOTES:
- Turn 1 → We could have skipped this if we'd checked [X] first
- Turn 2 → The obstacle was predictable if we'd read [Y]
- Turn 3 → The pivot was right but took too long to make
```

**Step 3: Extract Transferable Lessons**

```
LESSONS FROM THIS REPLAY:
1. [Lesson] — applies when [situation]
2. [Lesson] — applies when [situation]

INSTINCT CANDIDATES:
(Patterns worth promoting to INSTINCT.md)
- [Pattern]: [when to apply it]
```

## Integration with Kai Files

Thinkback reads from and writes to:
- **LINEAGE.md** — primary decision journal (reads existing, adds reconstructed decisions)
- **INSTINCT.md** — promotes recurring lessons to reflexes
- **SCARS.md** — connects past failures to decisions that caused them
- **MEMORY.md** — uses session notes as evidence

## Rules

- **Never judge past decisions by present knowledge.** Evaluate them based on what was known THEN.
- **Evidence over speculation.** If you can't find evidence for why a decision was made, say so. Don't fabricate reasoning.
- **Confidence levels matter.** Always state how confident you are in your reconstruction and why.
- **Respect the authors.** Past decisions were usually made by smart people under constraints. Start from that assumption.
- **Forward-looking bias.** The point isn't to assign blame — it's to make better future decisions.
- **Save everything.** Every thinkback session should produce entries in LINEAGE.md for decisions that weren't previously documented.
