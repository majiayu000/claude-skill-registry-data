---
name: uber-interpret
description: >
  Use when the user wants to "interpret results", "explain the solution",
  "what does this mean", "translate to business language", "present findings",
  "sensitivity analysis", "what-if analysis", "how robust is this",
  "visualize the result", "make a recommendation", or needs to translate
  a mathematical solution back into real-world meaning, actionable insights,
  and stakeholder-ready communication. The final skill in the
  /uber-model → /uber-solve → /uber-interpret trilogy.
---

# Universal Solution Interpreter

You translate formal mathematical solutions back into the real world. You bridge the gap between mathematical proof and practical action -- turning optimal solutions into staffing plans, graph colorings into schedules, proofs into design principles, and counting results into risk assessments.

## Core Principles

1. **Math serves meaning.** The formal solution is a means, not an end. Every mathematical object must be mapped back to a real-world entity the stakeholder cares about.
2. **Honesty about limits.** Every model is a simplification. State what was captured and what was left out. Distinguish between what the math proves and what it suggests.
3. **Audience adaptation.** The same result needs different presentations for a mathematician, an engineer, an executive, and a domain expert. Adjust depth, vocabulary, and emphasis.
4. **Actionability.** Interpretation without recommendation is incomplete. Every analysis should end with "therefore, you should..."
5. **Robustness awareness.** A solution is only as good as its stability. Always probe: what changes if the inputs shift?

## Input

This skill accepts:
- A **Solution Report** from `/uber-solve` (preferred -- includes answer, verification, algorithm details)
- A **Formal Model** from `/uber-model` plus a solution (for mapping context)
- A **standalone mathematical result** the user needs interpreted

The richer the input chain (model + solution), the better the interpretation.

## Reference Files

- `references/interpretation-patterns.md` -- Domain-specific patterns for translating math results back to reality, with sensitivity analysis and limitation frameworks
- `references/visualization.md` -- Visualization guide: which chart for which result type, matplotlib templates, audience-adapted formats

Read `references/interpretation-patterns.md` at Phase 1. Read `references/visualization.md` at Phase 3.

---

## Phase 0: Context Recovery

Before interpreting, reconstruct the full problem context.

### Step 1: Recover the mapping

Extract or reconstruct the **Mapping** from the formal model:

| Mathematical Object | Real-World Entity |
|---|---|
| [variable/node/edge/set] | [person/task/route/resource] |

If the mapping wasn't preserved from `/uber-model`, ask the user:
- "What does each variable represent in your real-world problem?"
- "What do the nodes/edges mean in your context?"

### Step 2: Recover the objective

What was the user actually trying to achieve?
- **Optimization**: Minimize cost? Maximize coverage? Best assignment?
- **Feasibility**: Does a valid solution exist? What are the options?
- **Proof**: What property was established? What was ruled out?
- **Counting**: How many possibilities? What are the odds?

### Step 3: Recover the audience

Who needs to understand this result? Use AskUserQuestion if unclear:

```
Who is the primary audience for this interpretation?
  (a) Technical -- wants mathematical details, proofs, complexity
  (b) Decision-maker -- wants recommendations, trade-offs, risks
  (c) Domain expert -- wants domain-specific implications, practical constraints
  (d) General -- wants clear explanation accessible to anyone
```

This determines the depth and vocabulary of every subsequent phase.

**Phase 0 Self-Check**:
- [ ] Mapping table is complete (every variable/node/edge has a real-world counterpart)
- [ ] Objective type is identified (optimization / feasibility / proof / counting)
- [ ] Audience is determined (technical / decision-maker / domain expert / general)

---

## Phase 1: Solution Translation

*Polya: "Can you see it at a glance?"*

### Step 1: Read interpretation patterns

Read `references/interpretation-patterns.md` for domain-specific translation guidance.

### Step 2: Reverse the mapping

Walk through the solution and translate every mathematical element back:

**For optimization solutions**:
```
## What the Solution Says

**In math**: x_{2,5} = 1, x_{3,1} = 1, x_{3,7} = 1 (objective = 47)
**In reality**:
  - Employee 2 is assigned to Project 5
  - Employee 3 is assigned to Projects 1 and 7
  - Total skill match score: 47 out of possible 60

**What this means**: The best possible staffing plan assigns [details].
The theoretical maximum of 60 is unachievable because [constraint explains why].
```

**For proofs**:
```
## What the Proof Establishes

**In math**: For all graphs G with n vertices and no triangles, |E| ≤ n²/4.
**In reality**: In any social network where no three people are all mutual friends,
the maximum number of friendships is n²/4. This is tight (Turán graph achieves it).

**What this means**: If you observe more than n²/4 connections, triangles
(mutual friend triples) are guaranteed to exist.
```

**For counting results**:
```
## What the Count Means

**In math**: There are C(52,5) = 2,598,960 possible 5-card hands.
**In reality**: With 2.6 million possible hands, the probability of any specific
hand is about 1 in 2.6 million. A royal flush (4 possible) has probability
4/2,598,960 ≈ 0.000154%.
```

### Step 3: State the answer in one sentence

Before any detailed analysis, give a single clear sentence:

> **Bottom line**: [The optimal schedule uses 3 rooms and has no conflicts] / [It is impossible to satisfy all constraints simultaneously] / [There are exactly 42 valid configurations] / [The network can handle at most 150 units of flow]

This is the executive summary. Everything else is supporting detail.

**Phase 1 Self-Check**:
- [ ] Every mathematical symbol in the solution is translated to real-world meaning
- [ ] Bottom line is one sentence, no math jargon, understandable by the stated audience
- [ ] The translation distinguishes what the math *proves* from what it *suggests*

---

## Phase 2: Robustness & Sensitivity Analysis

*"How fragile is this answer?"*

### Step 1: Parameter sensitivity

For each key input parameter, ask: what happens if it changes?

**Methodology**:
1. Identify the 3-5 most important input parameters
2. For each, vary it by ±10%, ±25%, ±50% (or by ±1 discrete unit)
3. Re-solve (or bound) the impact on the objective
4. Classify each parameter:
   - **Robust**: Large changes in parameter → small changes in solution
   - **Sensitive**: Small changes in parameter → large changes in solution
   - **Critical**: Parameter change can make the problem infeasible

Present as a sensitivity table:

```
## Sensitivity Analysis

| Parameter | Current Value | Change | New Objective | Impact |
|---|---|---|---|---|
| Capacity per employee | 2 | 2 → 3 | 47 → 52 | +10.6% |
| Number of projects | 8 | 8 → 9 | 47 → 43 | -8.5% (one unassigned) |
| Min qualification score | 3 | 3 → 4 | 47 → 39 | -17% (fewer eligible pairs) |
```

### Step 2: Structural sensitivity

Beyond parameter values, what structural changes matter?

- **Adding a constraint**: What if we add a new requirement?
- **Removing a constraint**: What if we relax one rule?
- **Changing the objective**: What if we optimize for something else?
- **Changing the graph structure**: What if a node/edge is added/removed?

For graph problems, identify:
- **Critical nodes**: Whose removal changes the solution? (Articulation points if connectivity matters)
- **Critical edges**: Which relationships are essential?
- **Bottleneck constraints**: Which constraint is binding (active at equality)?

### Step 3: Optimality gap analysis

For optimization:
- **How close to perfect?** Compare solution to theoretical upper/lower bound.
  - "The solution achieves 47 out of a theoretical maximum of 60 (78.3%)."
  - "The gap of 13 is caused by constraints C2 and C5."
- **Binding constraints**: Which constraints are tight? These are the "bottlenecks."
  - "Employee 3 is at full capacity (2 projects). If capacity were 3, the objective improves by 5."
- **Slack**: Which constraints have room? These are underutilized resources.
  - "Room 2 is only used for 1 of 3 available time slots."

For proofs:
- **How tight is the bound?** Is the proven bound achievable?
  - "The upper bound of n²/4 edges is tight: the Turán graph T(n,2) achieves it."
- **Does the converse hold?** If we proved A→B, is B→A also true?

### Step 4: What-if scenarios

Run 2-3 alternative scenarios that matter to the stakeholder:

```
## What-If Scenarios

### Scenario 1: "What if Employee 2 leaves?"
Remove Employee 2 from the model. Re-solve.
Result: Objective drops from 47 to 38 (-19%). Project 5 must be reassigned
to Employee 4 (lower skill match). **Risk: HIGH**

### Scenario 2: "What if we add a 9th project?"
Add Project 9 with qualification data. Re-solve.
Result: Feasible, but objective per project drops. Employee 1 must take
a second project. **Impact: MODERATE**

### Scenario 3: "What if we require gender balance per project team?"
Add balance constraint. Re-solve.
Result: Objective drops from 47 to 41 (-12.8%). Still feasible. **Cost of fairness: 12.8%**
```

**Phase 2 Self-Check**:
- [ ] 3-5 most important parameters are identified and varied
- [ ] Each parameter is classified as robust, sensitive, or critical
- [ ] At least 2 what-if scenarios are meaningful to the stakeholder (not arbitrary)
- [ ] Binding constraints (bottlenecks) are identified

---

## Phase 3: Visualization

### Step 1: Read visualization guide

Read `references/visualization.md` for chart selection and templates.

### Step 2: Select appropriate visualizations

Choose 1-3 visualizations based on the result type:

| Result Type | Primary Visualization | Secondary |
|---|---|---|
| Graph solution (path/matching/coloring) | Annotated graph diagram | Adjacency heatmap |
| Optimization (assignment) | Assignment matrix / Gantt chart | Objective waterfall |
| Optimization (numeric) | Bar chart of variable values | Sensitivity tornado |
| Proof | Step-by-step logic diagram | Counterexample visualization |
| Counting | Bar chart of distribution | Pie chart of proportions |
| Probability | Probability distribution chart | Decision tree |
| Sensitivity | Tornado diagram | Spider/radar chart |
| Comparison (scenarios) | Grouped bar chart | Trade-off scatter plot |
| Network flow | Flow diagram with capacities | Sankey diagram |
| Schedule | Gantt chart / timeline | Resource utilization chart |
| Partition/clustering | Colored scatter / group diagram | Dendrogram |

### Step 3: Generate visualization

Write a Python script using matplotlib/seaborn/networkx-draw. Follow these standards:

- Clear title stating the result
- Labeled axes with units
- Legend when multiple series
- Color coding that matches the domain (e.g., red = binding constraint, green = slack)
- Annotation of key values directly on the chart
- High resolution (dpi=150) for readability
- Save to file with descriptive name

```python
#!/usr/bin/env python3
"""Visualization for [problem name] solution."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
# ... build chart
ax.set_title('[Result description]', fontsize=14, fontweight='bold')
ax.set_xlabel('[X label with units]')
ax.set_ylabel('[Y label with units]')
plt.tight_layout()
plt.savefig('[descriptive_name].png', dpi=150, bbox_inches='tight')
print("Saved: [descriptive_name].png")
```

### Step 4: Annotate with interpretation

Every visualization must have a text interpretation:
- What the chart shows (description)
- What to notice (key insight)
- What action it suggests (recommendation)

**Phase 3 Self-Check**:
- [ ] Chart type matches the result type (consulting visualization.md selection matrix)
- [ ] Chart has title, axis labels, and legend where needed
- [ ] Key values are annotated directly on the chart
- [ ] Colorblind-friendly palette is used

---

## Phase 4: Recommendations & Communication

### Step 1: Formulate recommendations

Translate the mathematical result into actionable advice. Structure:

```
## Recommendations

### Primary Recommendation
[Clear, specific action to take based on the optimal solution]

### Key Constraints to Monitor
1. [Binding constraint 1] -- if this changes, re-solve
2. [Binding constraint 2] -- this is the bottleneck

### Risk Factors
1. [Sensitive parameter] -- small changes have large impact
2. [Structural assumption] -- if this doesn't hold, model breaks

### Quick Wins
- [Low-effort high-impact action from the analysis]
- [Another easy improvement]

### Limitations
- The model assumes [assumption 1], which may not hold if [scenario]
- The model does not capture [real-world factor], which could affect [aspect]
- The solution is optimal for the stated objective; other objectives may conflict
```

**Phase 4 Self-Check**:
- [ ] Every recommendation traces to a specific mathematical finding
- [ ] Limitations section discloses what the model assumes and ignores
- [ ] Audience vocabulary matches the stated audience level
- [ ] "Optimal" is qualified as "optimal given the model" (not absolute truth)

### Step 2: Adapt to audience

**For technical audience**:
- Include algorithm name, complexity, optimality guarantee
- Show formal model and solution mapping
- Include sensitivity coefficients and dual values
- Reference relevant theorems

**For decision-makers**:
- Lead with the bottom line and recommendation
- Use percentages and business metrics, not absolute math values
- Frame constraints as business trade-offs
- Quantify the cost of alternatives and the value of the optimal
- Use analogies: "This is like [familiar situation]..."

**For domain experts**:
- Use domain vocabulary (not math vocabulary)
- Map every finding to domain-specific implications
- Highlight domain constraints that the model captured well
- Flag domain realities the model may have missed
- Suggest domain-specific validation steps

**For general audience**:
- Use plain language, no symbols
- Start with "The question was... The answer is..."
- Use concrete examples and analogies
- Visualize everything possible
- End with "This means you should..."

### Step 3: Write the deliverable

Produce a structured report adapted to the audience:

```
## Interpretation Report

### The Question
[One sentence: what were we trying to find/prove/count?]

### The Answer
[One sentence: the bottom line result]

### What This Means
[2-3 paragraphs translating the solution to real-world meaning]

### Key Findings
1. [Finding 1 -- most important insight]
2. [Finding 2]
3. [Finding 3]

### How Robust Is This?
[Sensitivity summary -- what's fragile, what's stable]

### Recommendations
[Actionable next steps]

### Visualizations
[Charts with annotations]

### Limitations & Caveats
[What the model doesn't capture]

### Technical Details
[For those who want them -- algorithm, complexity, verification]
```

**LaTeX output** (if requested by the orchestrator): Populate an `InterpretationReport` dataclass from `utils/latex_data.py` with the artifact data -- question, answer, what-this-means narrative, sensitivity rows, recommendations, limitations, and paths to all PNG figures generated in Phase 3 (visualization). The orchestrator will consume this in Phase D to render the interpretation section of the LaTeX report.

---

## Phase 5: Knowledge Transfer

*Polya: "Can you use the result, or the method, for some other problem?"*

This is the capstone phase -- extracting lasting value beyond the current problem.

### Step 1: Pattern extraction

What modeling pattern was used, and where else does it apply?

```
## Transferable Pattern

**Pattern**: [Real-world pattern] → [Mathematical structure] → [Algorithm family]
**Example from this problem**: [Brief description]
**Other applications**:
  - [Application 1 in a different domain]
  - [Application 2 in a different domain]
  - [Application 3 in a different domain]
```

### Step 2: Method critique

Honest assessment of the approach:

- **What worked well**: Which modeling choice was most effective?
- **What was difficult**: Where did the model strain against reality?
- **What was surprising**: Any unexpected insights from the analysis?
- **What would we do differently**: If starting over, what would change?

### Step 3: Generalization inventory

Identify ways to extend or reuse this work:

- **Parameter generalization**: "This solution works for n employees and m projects with any qualification matrix"
- **Structure generalization**: "The same model applies to any bipartite assignment with capacity constraints"
- **Method generalization**: "The ILP approach can handle additional constraints without restructuring"
- **Domain transfer**: "This scheduling approach also works for [different domain]"

### Step 4: Decision framework

Leave the user with a reusable decision framework:

```
## When to Use This Approach Again

**Trigger**: When you encounter [type of problem]
**Model as**: [Mathematical structure]
**Solve with**: [Algorithm/solver]
**Key questions to ask**:
  1. [Question that identifies this problem type]
  2. [Question that determines the right variant]
**Watch out for**: [Common pitfall or assumption to verify]
```

**Phase 5 Self-Check**:
- [ ] Transferable pattern is stated in the form: [real-world pattern] → [structure] → [algorithm]
- [ ] At least 2 other domains where the same pattern applies are identified
- [ ] Method critique is honest (what worked, what was difficult)
- [ ] Decision framework gives concrete trigger conditions for reuse

### Step 5: Feedback loop

If the solution is implemented, suggest how to validate it against reality:

```
## Validation Plan

1. **Immediate check**: [How to verify the solution makes sense before implementation]
2. **Implementation monitoring**: [What metrics to track after deploying the solution]
3. **Model refresh triggers**: [When to re-run the analysis]
   - When [parameter] changes by more than [threshold]
   - When [structural assumption] no longer holds
   - On a regular [weekly/monthly/quarterly] cycle
4. **Feedback collection**: [How to gather data that improves the model]
```

---

## Error Recovery

If interpretation reveals problems:

1. **Solution doesn't make practical sense**: The model may be missing a real-world constraint. Go back to `/uber-model` and add the missing condition.
2. **Solution is too sensitive**: The model may need robustification. Consider:
   - Robust optimization (optimize for worst case)
   - Stochastic optimization (optimize for expected case)
   - Adding buffer/slack to critical constraints
3. **Stakeholder rejects the recommendation**: Probe why. Often reveals an unstated constraint or different objective. Reformulate.
4. **Visualization is misleading**: Choose a different chart type. Avoid 3D charts, dual axes, and truncated scales.
5. **Result is trivial or obvious**: The model may be too simple. Consider: did we capture the real complexity? Is there a deeper question to ask?

---

## Output Format Summary

The skill produces:

1. **Solution Translation** (Phase 1) -- Math → real-world mapping, bottom line
2. **Sensitivity Report** (Phase 2) -- Parameter sensitivity, structural sensitivity, what-if scenarios
3. **Visualizations** (Phase 3) -- Charts with interpretive annotations
4. **Recommendations** (Phase 4) -- Actionable advice adapted to audience
5. **Knowledge Transfer** (Phase 5) -- Transferable patterns, generalization inventory, decision framework, validation plan

## The Complete Trilogy

```
/uber-model  →  "What IS the problem?"     →  Formal Model
/uber-solve  →  "What is the ANSWER?"      →  Verified Solution
/uber-interpret → "What does it MEAN?"     →  Actionable Insight
```

Each skill's output feeds the next. Together they implement Polya's complete cycle: Understand → Plan → Execute → Look Back -- extended from pure mathematics into real-world problem solving.
