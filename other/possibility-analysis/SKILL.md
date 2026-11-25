---
name: possibility-analysis
description: >
  Structured exploration of what is possible within a given problem, decision, or system — before evaluating what is optimal. Use this skill whenever the user asks to explore options, brainstorm, map a solution space, think through alternatives, analyze what could be done, weigh paths forward, or reason about uncertainty and tradeoffs. Also trigger when the user says things like "what are my options", "help me think through this", "what could we do here", "I'm not sure how to approach X", "is there another way", or "let's explore this". This is not a brainstorming-list generator — it is a rigorous epistemic process that expands, structures, and interrogates a possibility space before collapsing it into a decision. Always use this skill when depth of reasoning matters more than speed of answer.
---

# Possibility Analysis Skill

Possibility analysis is the disciplined exploration of **what exists in the solution space** before committing to any path. It is a pre-decisional process: the goal is to expand the map, not yet to navigate it.

This skill governs how Claude reasons through and presents that exploration.

---

## First Principles

A possibility analysis rests on three axioms:

1. **The space is almost always larger than it appears.** Initial framings narrow options prematurely. The job is to resist closure.
2. **Constraints are not always real.** Many constraints are assumed, inherited, or historical. They must be surfaced and tested, not silently accepted.
3. **Evaluation too early kills options.** The moment you start ranking, you stop seeing. Expansion and evaluation are separate cognitive modes.

The process has two distinct phases:
- **Divergent phase**: maximize the breadth and depth of what is possible
- **Convergent phase**: apply constraints, tradeoffs, and judgment to identify the viable frontier

---

## Phase 1: Frame Acquisition

Before generating possibilities, Claude must acquire the problem frame. Do this **before** listing anything.

### 1.1 Identify the Core Question

Ask internally:
- What is the person actually trying to decide or explore?
- What does a good outcome look like for them?
- Is the stated problem the real problem, or a symptom?

If ambiguous, ask **one targeted clarifying question** — not a list. Make it the most load-bearing question for subsequent analysis.

### 1.2 Surface the Implicit Constraints

Every problem arrives with invisible walls: budget, time, people, technology, organizational politics, risk tolerance, legal context. Map them explicitly.

Distinguish between:
- **Hard constraints**: physically or logically impossible to violate (e.g., HIPAA compliance is not optional)
- **Soft constraints**: conventional, historical, or risk-averse limitations that *could* be relaxed (e.g., "we've always done it in Lambda")
- **Assumed constraints**: things the person believes are limits but haven't verified (e.g., "the vendor can't do X" — do we know that?)

Label each constraint type explicitly when presenting the analysis.

### 1.3 Identify the Dimensionality

What are the axes of variation in this space? Examples:
- Build vs. Buy vs. Adapt
- Centralized vs. Distributed
- Short-term vs. Long-term horizon
- High risk/high upside vs. Low risk/lower upside
- First-principles redesign vs. Incremental improvement

Dimensionality mapping prevents false either/or framings. A 2-axis problem has 4 quadrants; most problems have 3+ axes, yielding a rich space.

---

## Phase 2: Possibility Generation

Generate possibilities across **four levels of abstraction**. This is the core of the divergent phase.

### Level 1 — Obvious Possibilities
What a competent practitioner would immediately list. These are the "expected" options. Include them fully — they exist for good reason — but do not stop here.

### Level 2 — Non-Obvious Possibilities
Options that require stepping back from the conventional frame. Often come from:
- Analogies to adjacent domains
- Inverting the problem ("what if we don't do X at all?")
- Separating concerns that are usually bundled together
- Asking "who else has solved this, and how?"

### Level 3 — Boundary Possibilities
Options that are technically possible but require violating one or more soft constraints. Present these explicitly and name which constraint they challenge. These often become the most innovative paths once stakeholders realize the constraint is negotiable.

### Level 4 — Degenerate Possibilities
The extremes: do nothing, do everything, outsource entirely, stop the problem at its source. These are often impractical but serve a critical function — they **bracket the space** and reveal implicit assumptions about what is considered acceptable.

---

## Phase 3: Possibility Structuring

Once possibilities are generated, organize them before evaluating them.

### 3.1 Group by Strategic Shape

Cluster options by their fundamental character, not their implementation details. Examples:
- **Defer**: buy time, gather more information, delay commitment
- **Contain**: limit scope, reduce blast radius, make the problem smaller
- **Transform**: redesign the system so the problem dissolves
- **Delegate**: shift the problem to another actor (vendor, partner, team)
- **Accept**: absorb the cost or risk as a known quantity

### 3.2 Map Dependencies and Prerequisites

Which options unlock others? Which options foreclose others? This reveals the **sequencing constraint** — some paths must come before others, and some are mutually exclusive.

Draw these relationships explicitly when they matter:
```
Option A → enables → Option C
Option B → forecloses → Option D
Option A + B → together enable → Option E
```

### 3.3 Identify the Key Uncertainties

What information, if known, would change which options look viable? These are the **resolution points** — the pivots on which the analysis turns. Name them.

Examples:
- "If the vendor exposes a webhook API, Option 2 becomes dominant."
- "If team velocity stays below X, Option 3 is not executable in the timeframe."

---

## Phase 4: Possibility Evaluation

Now, and only now, apply judgment. This is the convergent phase.

### 4.1 Evaluate Against Explicit Criteria

For each candidate path, assess across relevant dimensions. Common ones:
- **Feasibility**: Can we actually do this, given real constraints?
- **Risk profile**: What can go wrong, how likely, how recoverable?
- **Reversibility**: Is this a one-way door or can we undo it?
- **Time to value**: When does benefit materialize?
- **Alignment**: Does this fit organizational/strategic direction?
- **Leverage**: Does this create future options, or close them?

Weight criteria based on context — don't apply a generic rubric blindly.

### 4.2 Identify the Viable Frontier

The viable frontier is the set of options that are **not dominated** by any other option. An option is dominated if another option is strictly better on every dimension that matters. Present the frontier, not a single "winner" — unless one option genuinely dominates.

### 4.3 Apply the Pre-Mortem Test

For the top 2–3 options, ask: *"If we chose this and it failed 12 months from now, what would be the most likely cause?"* This surfaces hidden failure modes that don't appear in forward-looking analysis.

### 4.4 Recommend with Epistemic Honesty

Make a recommendation only when there is genuine basis for one. Structure it as:

- **Recommended path**: [option] — because [reasons grounded in their constraints and goals]
- **Key condition**: This recommendation depends on [assumption]. If [assumption] is false, reconsider [alternative].
- **The path not taken**: [runner-up option] is viable if [circumstance]. Keep it on the table.

Do not manufacture false confidence. "It depends" is a legitimate answer when the pivoting variable is named.

---

## Output Format

Adapt format to complexity. Three modes:

### Compact (simple decisions, 1–2 axes)
Inline prose with bolded option names. No headers. Max ~400 words. End with a clear recommendation or named tradeoff.

### Standard (moderate complexity, 2–4 axes, 4–8 options)
Structured with Phase headers. Options listed with brief characterization, key tradeoffs, and a viability assessment. Recommendation at the end. Target ~600–1000 words.

### Full Analysis (high complexity, strategic decisions, many axes)
Full phase structure as documented here. May reference the detailed reference files below. Can exceed 1500 words. Include:
- Constraint map
- Possibility matrix or structured list by level
- Dependency graph (textual or ASCII)
- Viable frontier table
- Recommendation with conditions and alternatives

Use the Standard format by default. Escalate to Full only when the decision is genuinely high-stakes or multi-dimensional. Compact is appropriate when the person just needs a quick map before moving forward.

---

## Anti-Patterns to Avoid

These are failure modes in possibility analysis:

| Anti-Pattern | What It Looks Like | Why It's Harmful |
|---|---|---|
| Premature convergence | Jumping to "the answer" without mapping the space | Kills options before they're seen |
| False exhaustiveness | A long list that all cluster around the same idea | Creates illusion of breadth without actual coverage |
| Constraint acceptance | Treating soft constraints as hard | Artificially narrows viable frontier |
| Evaluation contamination | Ranking options while still generating them | Anchoring bias kills creative options |
| Missing the meta-option | Not asking "what if we reframe the problem?" | Optimizing within the wrong frame |
| Vague tradeoffs | "Option A is faster but riskier" without specifics | Untestable claims that don't help decisions |
| Fake confidence | Recommending without naming key assumptions | Misleading — confidence without conditions is noise |

---

## Reference Files

For extended guidance, read the relevant reference file:

- `references/cognitive-models.md` — Mental models and heuristics for Phase 2 (possibility generation): lateral thinking, inversion, constraint relaxation, analogical reasoning
- `references/domain-patterns.md` — Common possibility structures for recurring domains: software architecture, team/org decisions, product strategy, technical debt, build-vs-buy
- `references/uncertainty-handling.md` — How to handle deep uncertainty: Bayesian reasoning under incomplete information, real options thinking, decision staging

Read a reference file when the problem falls clearly in its domain or when the standard guidance is insufficient for the complexity at hand.
