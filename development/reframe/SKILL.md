---
name: reframe
description: Cognitive reframe for any problem statement or belief. Returns 5 reframes across different lenses. Changes the problem, not just the options. Pre-pitch, pre-negotiation, when stuck.
version: 1.0.0
execution-mode: advisory
argument-hint: "\"<problem statement or belief to reframe>\""
category: fleet-ops
status: tested
providers:
  required: [bash, python]
---
# [reframe]

> The problem you're solving is almost never the problem you started with. This skill finds the better problem.

Different from `[brainstorm]` (generates options for a fixed problem) — this **changes the problem statement itself**. A reframe doesn't give you more answers; it gives you a better question.

## When to Use
- Before a pitch call when your current angle isn't landing
- When you've been stuck on something for > 30 minutes
- When someone rejected your proposal — reframe before proposing again
- When the narrative about HUMMBL needs fresh air
- Pre-negotiation: reframe the dynamic before the conversation

## The 5 Frames

### 1. Inversion Frame
*"What if the opposite were true?"*
Flip the problem inside out. If your problem is "AI governance is too complex for enterprises", the inversion is "What if enterprises are too simple for AI governance?" What does that suggest?

### 2. Abundance Frame
*"What if this constraint were actually an asset?"*
The constraint that feels like the problem becomes the moat. "HUMMBL requires enterprises to slow down before deploying AI" → "HUMMBL is the only product that turns governance slowdown into competitive advantage."

### 3. BKI Frame
*"What's the belonging/trust gap underneath this?"*
Most business problems are belonging problems in disguise. Who doesn't trust whom? What's the threat-state causing the resistance? If legal doesn't adopt the governance framework, the real problem isn't compliance — it's that legal doesn't feel safe enough to change behavior.

### 4. Time-Horizon Frame
*"What does this look like 10× longer out?"*
Extend the time horizon until the problem dissolves or becomes obvious. "We can't close Wave 1 clients fast enough" → in 10 years, what would someone say was the real blocker? Usually: "They didn't start early enough" or "They were building the wrong thing." Which is it?

### 5. Stakeholder Frame
*"Who benefits from this problem staying unsolved?"*
Every persistent problem has a beneficiary. Who is it? What would they lose if the problem were solved? This often reveals the real constraint — not technical, not strategic, but political.

## Execution

For `$ARGUMENTS` (the problem statement):

1. State the original problem clearly
2. Apply each frame — generate the reframed problem statement
3. Rate each reframe 1–3 for "most generative" (not most comfortable)
4. Pick the one that changes your thinking most — that's the one to act on

## Output Format

```
Reframe | "<original problem>"
══════════════════════════════

## Original Problem
"<problem statement as given>"

## The 5 Reframes

### 1. Inversion
Reframe: "<flipped problem statement>"
Implication: <1 sentence on what this suggests>

### 2. Abundance
Reframe: "<constraint as asset>"
Implication: <1 sentence on what this suggests>

### 3. BKI Lens
Reframe: "<belonging/trust gap underneath>"
Implication: <1 sentence on what this suggests>

### 4. 10× Time Horizon
Reframe: "<problem at extended time scale>"
Implication: <1 sentence on what this suggests>

### 5. Stakeholder (who benefits from the problem?)
Reframe: "<who needs this problem to stay>"
Implication: <1 sentence on what this suggests>

## Most Generative Reframe
#N — "<reframe>"
Why: <why this one changes the thinking most>

## Next Action
Based on the most generative reframe: <concrete next step>
```

## Chain
- After reframe → `[press-release]` with the new problem definition
- Reframe reveals a BKI gap → `[fitness-assessment]` for the org
- Reframe reveals a stakeholder problem → `[discovery-call]` to probe it
- Reframe changes the pitch → update `[pitch]` materials
