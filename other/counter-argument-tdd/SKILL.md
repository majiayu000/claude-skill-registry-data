---
name: counter-argument-tdd
version: 1.4.1
description: Use before drafting sections or paragraphs to enumerate counter-arguments and draft resolutions that withstand peer review
---

# Counter-Argument Driven Writing Skill (Counter-Argument TDD)

## Purpose
Apply Test-Driven Development (TDD: Red -> Green -> Refactor) discipline to paper writing. Before drafting main text, enumerate potential objections, edge cases, and counter-evidence. Then draft paragraphs that directly resolve those objections, followed by polishing for style and cohesion.

## Trigger Conditions
- Before drafting each section or paragraph
- When constructing a new argument or extending an existing one

## Workflow Cycle

```text
[1. List Objections] -> [2. Draft Resolution] -> [3. Polish Style]
```

### Phase 1: List Objections
Before drafting a paragraph or section, document potential objections in `docs/design/test-cases.md`.

Use the following **progressive dialogue pattern** ([Cognitive Scaffolding Rule S4](../../../rules/en/cognitive-scaffolding-rule.md)):

1. The agent presents one objection candidate first and asks: "Could this type of objection apply?"
2. After the user responds, present the next objection axis one at a time.
3. Walk through structured checks (Heterogeneity Check, Data Re-Interpretation Check) one by one.
4. Ask the open-ended "Any other objections you can think of?" **only at the end**.

Format:

```markdown
## Section 3.2: Economic Transition in 17th Century
- [ ] **Objection 1**: "Was self-sufficient exchange still dominant in rural areas?"
- [ ] **Objection 2**: "Does Source A represent a localized urban anomaly?"
```

#### 1. Heterogeneity Check & Mandatory Evidence Logging
When listing objections, always perform the following check:
- **Ask: "Could an objection be raised against treating this group or category as homogeneous?"**
- When the unit of analysis is a social group (workers, migrants, beneficiaries, etc.), you **must either enumerate at least one objection regarding internal differentiation (by skill level, region, gender, generation) OR record an explicit non-applicability justification (e.g. "Pure conceptual analysis; no social groups involved") in `docs/design/test-cases.md`**.
- *Note: This check functions as pre-validation for the `Internal Heterogeneity` axis in [claim-evidence-gate](../claim-evidence-gate/SKILL.md).*

#### 2. Data Re-Interpretation Check
When using statistical trends or comparative figures in your argument, evaluate the following generalized 3-axis objections and add applicable items to `docs/design/test-cases.md`:
- ① **Pace & Elasticity**: Is the rate of change sluggish relative to background macroeconomic growth? (e.g., slow inequality reduction despite high GDP growth).
- ② **Absolute Benchmark Evaluation**: Does the post-change level still touch or exceed international, clinical, or academic warning thresholds?
- ③ **Factor Decomposition**: Is the numerical change driven by structural market income convergence or temporary fiscal transfers (4Ps) / measurement revisions?

#### 3. Faction Check
When listing objections, consult the Contestation Status column of `docs/<paper-id>/literature/literature-matrix.md` (or `docs/literature/literature-matrix.md` in single-paper repositories):
- If any claim relies on `contested` / `contradicted` literature or propositions, **enumerate at least one objection drawn from the opposing camp's representative papers** as a test case.
- If a load-bearing claim remains `unknown`, consider returning to `literature-search` Step 1.5 (Faction Discovery).

For diachronic papers, add cherry-picking of period-sections, anachronism (reading a coined concept back onto historical actors), and missing transmission evidence if they are not already listed ([`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md)).

*Note: This check reinforces "imagined objections" with "real objections" and functions as pre-validation for the `Field Disagreement` axis in [claim-evidence-gate](../claim-evidence-gate/SKILL.md).*

### Phase 2: Draft Resolution
Draft text incorporating Topic-Sentence-First structure, directly resolving each listed objection:
- Acknowledge rural exceptions and explicitly scope claims to urban trade centers.
- Pair Source A with corroborating Sources B and C to eliminate regional bias.
- Mark resolved objections as complete.

### Phase 3: Topic-Sentence-First & Style Refinement
- Place a strong topic sentence at the start of each paragraph.
- Use active voice ("We demonstrate...") with explicit logical signposts ("However,", "Consequently,"). In disciplines where impersonal/passive voice is standard, adapt accordingly while retaining strong topic sentences.

## ⚠️ Output Boundary Rule
Internal workflow labels and process metaphors used within this skill instruction (TDD, Red, Green, Refactor, Test Case, Phase, etc.) are **for use exclusively within `docs/design/test-cases.md` (internal design documents) and agent execution prompts**.

- Text output to the manuscript body (`docs/chapters/` files) **must never contain or quote these internal process labels or metaphors**.
- Section headings and body paragraphs must use purely academic language (e.g., "Addressing potential objections", "Empirical examination of the statistical artifact hypothesis").

## Outputs
- `docs/design/test-cases.md` (Counter-Argument Validation List)
