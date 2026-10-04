---
name: uber-polya
description: >
  Use when the user presents a real-world problem and wants end-to-end help:
  "solve this problem", "help me figure this out", "model and solve",
  "full analysis", "what's the answer and what does it mean", or any problem
  that benefits from the complete Model → Solve → Interpret pipeline.
  Orchestrates /uber-model, /uber-solve, and /uber-interpret as a single
  unified workflow.
---

# Universal Problem Solver (Orchestrator)

You orchestrate Polya's complete problem-solving cycle as a single unified workflow. Instead of the user invoking three separate skills, you guide the problem seamlessly through modeling, solving, and interpretation -- passing structured artifacts between phases.

## Pipeline Overview

```
Problem → [Phase A: Model] → Formal Model → [Phase B: Solve] → Solution Report → [Phase C: Interpret] → Actionable Insight
              uber-model          ↓              uber-solve           ↓              uber-interpret
```

## Modes

Before beginning, determine the appropriate mode based on the user's request.

### Mode 1: Full Pipeline (default)

Run all three phases. Use when the user presents a real-world problem and wants the complete answer with interpretation.

### Mode 2: Fast-Track

Skip or compress the Socratic dialogue in Phase A when the problem is already well-formulated mathematically. Indicators:
- User provides a formal model directly ("Minimize c^T x subject to Ax <= b")
- User names the problem type ("This is a graph coloring problem")
- User provides code or data structures ready for solving
- Problem maps unambiguously to a single known structure

In fast-track mode: compress Phase A to confirmation only (present the formal model, ask "Does this capture your problem?"), then proceed to Phase B.

### Mode 3: Stop-After-Model

Run Phase A only. Use when the user says "just model this", "help me formalize", or "I'll solve it myself."

### Mode 4: Stop-After-Solve

Run Phases A and B. Use when the user says "just get me the answer", "solve but I'll interpret", or doesn't need stakeholder-ready communication.

If the mode is unclear, use AskUserQuestion:

```
How deep should we go?
  (a) Full analysis -- model, solve, and interpret with recommendations (Recommended)
  (b) Model and solve -- get the answer but skip the interpretation
  (c) Model only -- formalize the problem, I'll solve it myself
```

### Output Format Selection

After determining the mode, determine the output format. If the user hasn't specified, use AskUserQuestion:

```
What output format do you want?
  (a) Python -- solver script + console output + JSON (default)
  (b) LaTeX/PDF -- professional mathematical report, no code shown
  (c) Both -- full Python output AND a compiled PDF report
```

Thread the format choice through all phases. When transitioning between phases, state the format (e.g., "Output format: LaTeX/PDF") so each sub-skill populates the LaTeX data structures from `utils/latex_data.py`.

**Format behavior**:
- **Python**: Current behavior -- generate solver script, console output, `solution.json`.
- **LaTeX/PDF**: Solver still runs internally to compute the answer, but the user-facing deliverable is a `.tex` source file and compiled `.pdf` report. Do NOT present the Python solver script to the user.
- **Both**: Full Python output AND a compiled PDF report.

---

## Artifact Schemas

Each phase produces a structured artifact that the next phase consumes. Present these as formatted blocks in your output so the pipeline is traceable.

### Artifact 1: Formal Model

Produced by Phase A, consumed by Phase B.

```
## Formal Model

**Problem Type**: Find / Prove
**Domain**: [Graph Theory / Combinatorics / Logic / Number Theory / Optimization / Probability / ...]
**Named Problem**: [Classic name if applicable, e.g., "Minimum Weight Bipartite Matching"]

**Universe**:
  - [Set definitions]

**Variables**:
  - [symbol]: [meaning] [type/range]

**Structure**: [Core mathematical object and its definition]

**Mapping**:
  | Real-World Concept | Mathematical Object |
  |---|---|
  | ... | ... |

**Constraints**:
  1. [formal constraint] -- [origin: which real-world condition]
  2. ...

**Objective** (find): [Minimize/Maximize/Find/Count]: [formal expression]
**Claim** (prove): [formal statement]

**Suggested Approach**: [algorithm family]
**Complexity Class**: [P / NP-hard / ...]
**Available Tools**: [solver libraries]
```

### Artifact 2: Solution Report

Produced by Phase B, consumed by Phase C.

```
## Solution Report

**Answer**: [the solution value / proof / count]
**Objective Value**: [for optimization]
**Optimal**: Yes / No / Unknown
**Feasible**: Yes (all [N] constraints verified) / No
**Algorithm**: [name] | O([complexity])
**Time**: [X.XXXXs]
**Certificate**: [optimality proof description]

### Solution Details
[The assignment, path, proof steps, count breakdown, etc.]

### Verification
[Independent check results -- every constraint checked]
```

### Artifact 3: Interpretation Report

Produced by Phase C. The final deliverable.

```
## Interpretation Report

### The Question
[One sentence: what were we trying to find/prove/count?]

### The Answer
[One sentence: the bottom line result in real-world language]

### What This Means
[2-3 paragraphs translating the solution]

### How Robust Is This?
[Sensitivity summary with parameter classification: robust/sensitive/critical]

### Recommendations
[Actionable next steps]

### Limitations
[What the model doesn't capture]
```

### Artifact 4: PDF Report (optional)

Produced by Phase D when LaTeX/PDF output is requested.

**Files**:
- `report.tex` -- LaTeX source (always generated)
- `report.pdf` -- compiled PDF via fpdf2 (always generated, no system LaTeX needed)
- `polya.sty` -- custom style file (copied to output directory)

The PDF report contains all three phases typeset as a professional mathematical document with equations, tables, embedded figures, and branded styling.

---

## Phase A: Model the Problem

Read and follow the protocol in `skills/uber-model/SKILL.md`.

**Reference files to read** (at Phase 2 of uber-model):
- `skills/uber-model/references/heuristics.md`
- `skills/uber-model/references/structures.md`
- `skills/uber-model/references/problem-classification.md` (read first for rapid pattern matching)
- `skills/uber-model/references/common-mistakes.md` (read during Phase 3 as a pre-flight check)

**Key steps**:
1. Receive the problem and classify (find vs. prove)
2. Understand: identify unknown, data, conditions (Socratic dialogue)
3. Devise a plan: match to mathematical structures, propose candidates
4. Build the formal model with complete mapping
5. Verify the model (specialization, symmetry, completeness)

**Phase A Gate**: Present the **Formal Model** artifact. Use AskUserQuestion to confirm:
```
Does this model capture your problem correctly?
  (a) Yes, proceed to solving
  (b) Mostly, but [correction needed]
  (c) No, let's remodel
```

**Self-check before proceeding**:
- [ ] Every data point maps to a mathematical object
- [ ] Every real-world condition appears as a constraint
- [ ] The unknown is captured in the objective/claim
- [ ] No constraint was added that isn't in the original problem
- [ ] The model passes a trivial-case test (n=1 or n=2)

If mode is Stop-After-Model, present the Formal Model artifact and stop.

---

## Phase B: Solve the Model

Read and follow the protocol in `skills/uber-solve/SKILL.md`.

**Reference files to read** (at Phase 1 of uber-solve):
- `skills/uber-solve/references/algorithms.md`
- `skills/uber-solve/references/solvers.md`

**Key steps**:
1. Classify the computational problem (use the classification table in uber-solve)
2. Select algorithm and solver library
3. Implement a complete, self-contained Python solver with `Instance`, `Solution`, `solve()`, `verify()`
4. Execute and verify: check all constraints, produce optimality certificate
5. Present the Solution Report artifact

**Phase B Gate**: Present the **Solution Report** artifact. If verification passes, proceed. If it fails, debug and re-solve.

**Self-check before proceeding**:
- [ ] All constraints verified as SATISFIED
- [ ] Optimality certificate produced (or gap reported)
- [ ] Independent verification method used (not just trusting the solver)
- [ ] Edge cases handled (empty input, single element, disconnected components)
- [ ] Solution is reproducible (deterministic or seeded)

If mode is Stop-After-Solve, present the Solution Report artifact and stop.

---

## Phase C: Interpret the Solution

Read and follow the protocol in `skills/uber-interpret/SKILL.md`.

**Reference files to read**:
- `skills/uber-interpret/references/interpretation-patterns.md` (at Phase 1)
- `skills/uber-interpret/references/visualization.md` (at Phase 3)

**Key steps**:
1. Recover context: mapping, objective, audience
2. Translate: reverse the mapping, state the bottom line in one sentence
3. Sensitivity analysis: vary key parameters, classify as robust/sensitive/critical
4. Visualize: select and generate appropriate charts
5. Recommend: actionable advice adapted to audience
6. Transfer knowledge: extract reusable patterns

**Phase C Gate**: Present the **Interpretation Report** artifact as the final deliverable.

**Self-check before finishing**:
- [ ] Bottom line is stated in one clear sentence (no math jargon)
- [ ] Every mathematical object is mapped back to real-world meaning
- [ ] At least 3 parameters tested for sensitivity
- [ ] Recommendations are specific and actionable (not generic)
- [ ] Limitations are honestly disclosed
- [ ] Audience level is appropriate (confirmed or inferred)

---

## Phase D: Generate Report (LaTeX/PDF modes only)

Skip this phase if output format is Python-only.

1. **Populate data classes**: Build `FormalModel`, `SolutionReport`, and `InterpretationReport` objects from `utils/latex_data.py` using the artifacts produced in Phases A, B, and C.

2. **Generate LaTeX source**: Instantiate `LatexRenderer` from `utils/latex_renderer.py` with a `ReportConfig`. Call `render_tex()` to produce `report.tex` in the working directory. This also copies `polya.sty` and any PNG figures.

3. **Generate PDF**: Call `render_pdf()` to produce `report.pdf` using fpdf2 (no system LaTeX needed).

4. **Optionally compile with system LaTeX**: Call `compile_tex()` for higher-quality PDF if `pdflatex` or `latexmk` is available.

5. **Present to user**:
   - "LaTeX source saved to: `report.tex`"
   - "PDF report saved to: `report.pdf`"
   - If **Both** mode: also show the Python solver script as usual.
   - If **LaTeX/PDF** mode: do NOT present the Python solver script.

**Self-check**:
- [ ] `report.tex` is syntactically valid LaTeX
- [ ] `report.pdf` contains all applicable sections (model, solution, interpretation)
- [ ] All figures embedded correctly
- [ ] Math equations render correctly in PDF
- [ ] No LaTeX special characters leaked into text

---

## Fast-Track Protocol

When fast-tracking (Mode 2), compress Phase A as follows:

1. **Skip Socratic dialogue**. Instead, directly classify the problem:
   - Read `skills/uber-model/references/problem-classification.md`
   - Match the problem to a named problem class
   - Build the Formal Model artifact directly

2. **Present for confirmation only**:
   ```
   I recognize this as [named problem]. Here's the formal model:
   [Formal Model artifact]

   Shall I proceed to solving?
     (a) Yes, this is correct
     (b) Not quite -- [let me clarify]
   ```

3. **Proceed to Phase B immediately** upon confirmation.

Fast-track should still read `common-mistakes.md` and run the self-check. Speed should not sacrifice correctness.

---

## Error Recovery Across Phases

### Phase B fails (solver error, infeasible, timeout)
1. Check if the model is over-constrained → loop back to Phase A
2. Check if the algorithm choice was wrong → re-classify in Phase B
3. Check if the instance is too large → switch to approximation in Phase B

### Phase C reveals nonsensical results
1. The model may be missing a real-world constraint → loop back to Phase A
2. The solution may be a degenerate edge case → re-examine in Phase B
3. The audience may need a different framing → adjust in Phase C

### User redirects mid-pipeline
If the user says "wait, I want to change something" at any point:
- Acknowledge immediately
- Determine which phase the change affects
- Loop back to the earliest affected phase
- Preserve work from unaffected phases

---

## Output Format

Throughout the pipeline, clearly label which phase you're in:

```
---
## Phase A: Modeling
[... Socratic dialogue, formal model ...]

---
## Phase B: Solving
[... classification, code, solution report ...]

---
## Phase C: Interpretation
[... translation, sensitivity, visualization, recommendations ...]
```

This makes the pipeline traceable and allows the user to revisit any phase.
