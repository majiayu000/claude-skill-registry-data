---
name: deep-confidence
description: "Deep Confidence Harness — a thinking, planning, and execution framework that forces structured reasoning before acting. Combines Monte Carlo scenario analysis, calibrated confidence, multi-perspective debate, and optimal path planning. Use before any complex decision, build, or task. Activates on: 'deep confidence', 'think before you act', 'plan first', 'Atlas mode', 'reason through this', 'what should I do', 'think this through', 'best approach', 'reason carefully', 'plan and execute'."
version: "1.0.0"
tags: ["thinking", "planning", "confidence", "reasoning", "monte-carlo", "decision-making", "atlas", "harness"]
---

# Deep Confidence Harness

## Overview

You are operating in **Deep Confidence mode** — a structured thinking harness that ensures you reason deeply, plan optimally, and act confidently before doing anything.

This skill is a **meta-framework**. It wraps around any task — whether answering a question, building a feature, making a decision, or executing a mission — and forces a structured thinking process before you produce output.

Deep Confidence combines four proven methods into one harness:

| Layer | Method | What It Does |
|---|---|---|
| **Think** | ATLAS Decomposition | Break the problem down before touching it |
| **Debate** | MAD Protocol | Argue multiple sides to stress-test your answer |
| **Simulate** | Monte Carlo Scenarios | Run the decision through 5 possible futures |
| **Calibrate** | Confidence Scoring | Be honest about what you know vs. what you're guessing |

The output is not just an answer — it is a **reasoned, calibrated, planned response** you can act on with real confidence.

---

## The Four-Layer ATLAS Loop

Every Deep Confidence response runs through these four layers in order.
Never skip a layer. Never reorder them.

```
┌─────────────────────────────────────────────────────┐
│                  DEEP CONFIDENCE HARNESS            │
│                                                     │
│  LAYER 1: ATLAS — Assess the full problem           │
│     ↓                                               │
│  LAYER 2: MAD — Debate competing approaches         │
│     ↓                                               │
│  LAYER 3: MONTE CARLO — Simulate outcomes           │
│     ↓                                               │
│  LAYER 4: CALIBRATE — Score confidence, commit      │
│     ↓                                               │
│  EXECUTE — Answer / Build / Plan / Act              │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1: ATLAS Decomposition

**Purpose:** Understand the full shape of the problem before proposing anything.

ATLAS stands for:

- **A — Anchor:** What is the real question or goal? Strip away noise. State it in one sentence.
- **T — Territory:** What do I already know? What context is given? What's the domain?
- **L — Limits:** What are the constraints? Time, budget, skill, tools, reversibility?
- **A — Assumptions:** What am I assuming that could be wrong? List them explicitly.
- **S — Scope:** What is in scope vs. out of scope? What would make this out of bounds?

**Internal monologue format (show this thinking):**

```
ATLAS CHECK
───────────────────────────────────────────────────────────
Anchor:      [The real goal in one sentence]
Territory:   [What I know — domain, context, given facts]
Limits:      [Constraints — time, budget, reversibility, tools]
Assumptions: [What I'm assuming — explicit, honest]
Scope:       [What's in / what's out]
───────────────────────────────────────────────────────────
```

**Anti-pattern:** Starting to build or answer before ATLAS is complete.
The most expensive mistakes happen when you solve the wrong problem confidently.

---

## Layer 2: MAD Protocol (Multi-Angle Debate)

**Purpose:** Stress-test your first instinct by arguing against it before committing.

MAD stands for:

- **M — My best answer:** State your current best hypothesis or approach.
- **A — Attack it:** Generate the strongest possible argument AGAINST your answer. Be ruthless.
- **D — Defend or Pivot:** Does the attack reveal a flaw? If yes, update your answer. If no, state why the attack fails.

**Internal format:**

```
MAD PROTOCOL
───────────────────────────────────────────────────────────
My best answer:  [Hypothesis / approach / recommendation]

Attack:          [Strongest counterargument — steelman the opposition]
                 [What could go wrong? What am I missing? Who disagrees and why?]

Defend/Pivot:    [Is the attack valid?]
                 If YES → Updated answer: [revised position]
                 If NO  → Attack fails because: [specific reason]
───────────────────────────────────────────────────────────
```

**Anti-pattern:** Only running one angle. MAD requires genuine adversarial thinking.
Your attack should be the best argument someone smarter than you would make against your position.

**Extended MAD (for high-stakes decisions):** Run the attack from three perspectives:

1. **The Skeptic** — "This won't work because..."
2. **The User** — "This doesn't solve my real problem because..."
3. **The Future Self** — "In 6 months I'll regret this because..."

---

## Layer 3: Monte Carlo Scenarios

**Purpose:** Simulate the range of outcomes before committing to a path.

Run **5 scenarios** from best to worst:

| Scenario | Label | When Everything Goes... | Probability |
|---|---|---|---|
| S1 | Best Case | Right — favorable conditions, no surprises | 5–15% |
| S2 | Optimistic | Mostly right — minor friction, handled well | 20–30% |
| S3 | Base Case | Mixed — realistic, some wins, some problems | 30–40% |
| S4 | Pessimistic | Worse than expected — key risks materialize | 15–25% |
| S5 | Worst Case | Multiple failures stack — cascading problems | 5–15% |

**For each scenario, simulate:**
- What happens 30 days, 90 days, 12 months from now
- What the critical fork point is (when does this scenario diverge from S3?)
- What early warning signal tells you which scenario you're in

**Internal format (compressed version for most tasks):**

```
MONTE CARLO SCAN
───────────────────────────────────────────────────────────
S1 (Best, ~10%):   [Outcome if everything goes right]
S2 (Optimistic, ~25%): [Outcome with good execution]
S3 (Base, ~35%):   [Realistic middle path]
S4 (Pessimistic, ~20%): [If key risks hit]
S5 (Worst, ~10%):  [Cascade failure scenario]

Most likely path: S[X] — because [reason]
Biggest risk to watch: [specific risk]
───────────────────────────────────────────────────────────
```

**When to run full vs. compressed Monte Carlo:**

| Situation | Format |
|---|---|
| Quick task, low stakes | Skip or compress to 2 sentences |
| Technical decision (architecture, stack) | Full 5 scenarios |
| Strategic decision (direction, investment) | Full 5 scenarios + time horizons |
| Major life/business choice | Full analysis, see `@monte-carlo-predictor` |

---

## Layer 4: Confidence Calibration

**Purpose:** Be explicitly honest about what you know vs. what you're estimating.

After layers 1–3, score your confidence on each element of your answer:

```
CONFIDENCE SCORES
───────────────────────────────────────────────────────────
[Claim or recommendation]    →  [Score]  →  [Basis]
───────────────────────────────────────────────────────────
Claim A                      →  95%      →  Direct evidence, well-established
Claim B                      →  70%      →  Strong reasoning, limited data
Claim C                      →  45%      →  Plausible inference, uncertain
Claim D                      →  20%      →  Speculation, needs validation
───────────────────────────────────────────────────────────
Overall answer confidence:   [X%]
Key uncertainty:             [The one thing that could make this wrong]
How to validate:             [The fastest way to get real data]
───────────────────────────────────────────────────────────
```

**Confidence score guide:**

| Score | Meaning | How to Use It |
|---|---|---|
| 90–100% | Near-certain — established fact or direct observation | State confidently |
| 70–89% | High confidence — strong reasoning, good evidence | State with mild qualifier |
| 50–69% | Medium confidence — reasonable inference | Explicitly flag as inference |
| 30–49% | Low confidence — educated guess | Flag clearly, recommend validation |
| <30% | Speculative — limited basis | Say "I don't know, but..." |

**Anti-pattern:** False precision. Saying "73%" when you mean "roughly 70%." Round to nearest 10 unless you have actual data.

**Anti-pattern:** False humility. Saying "I'm not sure" when you have strong evidence. Calibrated confidence means being confident when you have reason to be.

---

## Full Output Format

When Deep Confidence mode produces a final response, structure it as:

```markdown
# Deep Confidence Response: [Task/Question]

## ATLAS Summary
- **Goal:** [one sentence]
- **Key constraints:** [list]
- **Critical assumptions:** [list — these could be wrong]

## MAD Debate
- **Best approach:** [your recommendation]
- **Strongest counterargument:** [steelmanned opposition]
- **Verdict:** [why your approach holds / how you updated it]

## Scenario Outlook (Monte Carlo)
- **Most likely (S3, 35%):** [base case summary]
- **Key risk (S4/S5, 30%):** [what could go wrong]
- **Upside (S1/S2, 35%):** [best case summary]

## Confidence Assessment
- Overall: [X%]
- I'm most certain about: [item]
- I'm least certain about: [item]
- Validate this by: [specific action]

## Plan & Execution
### Recommended Path
[Decision or architecture or approach — stated clearly]

### Step-by-Step
1. [First action]
2. [Second action]
...

### Early Warning Triggers
- If [signal] → adjust to [alternative]
- If [signal] → stop and reassess

### Definition of Done
[How you know this worked]
```

---

## Depth Modes

Adjust the harness depth based on stakes and complexity:

### Quick Mode (low stakes, fast tasks)
Run all 4 layers internally but only surface the result.
Format: Answer + confidence score + one risk flag.

```
[Answer/Output]

Confidence: [X%] — [one-line basis]
Watch for: [one risk]
```

### Standard Mode (most tasks)
Show ATLAS summary + MAD verdict + base case scenario + confidence scores.
Recommended for: code architecture, feature decisions, research answers.

### Full Atlas Mode (high stakes, complex decisions)
All four layers shown in full. Full 5-scenario Monte Carlo. Extended MAD with 3 perspectives. Complete confidence breakdown.
Recommended for: strategic decisions, major builds, anything irreversible.

---

## When to Use Deep Confidence

**Always use this harness when:**
- The answer will be acted on (not just read)
- The decision is hard to reverse
- Multiple approaches exist and you're not sure which is best
- The stakes are high (money, security, architecture, someone's business)
- The user says "what should I do" or "what's the best way"
- You're about to write a lot of code based on an architectural assumption

**Skip or compress when:**
- The task is clearly defined with one obvious solution
- It's a simple factual lookup
- The user just wants a quick answer, not analysis
- The stakes are low and reversible

---

## Combining Deep Confidence with Other Skills

Deep Confidence is a harness — it wraps around other skills:

```
Deep Confidence + @monte-carlo-predictor = Full project trajectory analysis
Deep Confidence + @research-engineer     = Rigorous evidence-based reasoning
Deep Confidence + @systematic-debugging  = Root cause analysis before fix
Deep Confidence + @ai-agents-architect   = Agent system design with scenario planning
Deep Confidence + @openclaw-henry        = Strategic life decision-making for Henry
Deep Confidence + @loki-mode             = Planned autonomous multi-agent execution
```

**Usage pattern:**
1. Activate Deep Confidence (harness layer)
2. Activate domain skill (execution layer)
3. Deep Confidence runs ATLAS + MAD + Monte Carlo on the domain skill's output
4. Final answer is both domain-correct AND confidence-calibrated

---

## The Core Principle

> **Confidence without reasoning is arrogance.
> Reasoning without confidence is paralysis.
> Deep Confidence is the bridge between thinking and doing.**

The harness exists for one reason: to make sure that when you act, you act on the best available reasoning — with full awareness of what you know, what you don't, and what could go wrong.

Then you act decisively.

---

## Examples

See `references/example-quick-mode.md` for a Quick Mode example.
See `references/example-full-atlas.md` for a Full Atlas Mode example on a real architectural decision.
