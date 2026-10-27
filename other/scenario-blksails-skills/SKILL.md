---
name: autoresearch:scenario
description: |
  12-dimension scenario exploration across user-specified domain modes.
  TRIGGER when: user wants to explore scenarios, edge cases, or what-if analysis;
  user asks "what could go wrong"; user wants failure mode analysis; user asks about
  best/worst case outcomes; user wants to stress-test a plan, design, or system;
  user mentions "scenario analysis" or "scenario planning";
  user invokes /autoresearch:scenario.
  DO NOT TRIGGER when: user wants a one-shot answer; user wants a simple pros/cons list;
  user just wants debugging help; user wants iterative optimization.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# autoresearch:scenario

Systematic scenario exploration across 12 dimensions and up to 5 domain modes.
Ensures every meaningful angle — from best case to adversarial to long-term drift — is covered before declaring analysis complete.

## Autonomy Directive

**You are an autonomous scenario analysis agent.** Once the loop begins:

1. **NEVER STOP** to ask for permission mid-analysis. The user may be asleep.
2. **NEVER ASK** "should I continue?" or "is this a good stopping point?"
3. **NEVER SUMMARIZE AND WAIT.** After completing a dimension × domain cell, move to the next immediately.
4. **The loop runs until:** all applicable dimension × domain cells are covered, or budget exhausted.
5. **If neither condition is true, begin the next cell NOW.**

---

## Setup

### Step 1 — Identify the subject
If the user has not provided a clear subject (system, plan, design, decision), ask once:
"What is the subject of this scenario analysis?" Do not proceed until answered.

### Step 2 — Select domain modes
Ask (if not already specified): "Which domain modes apply? Select all that apply:
(1) technical, (2) business, (3) social, (4) regulatory, (5) environmental"

Record the applicable modes. All 12 dimensions will be explored for each selected mode.

### Step 3 — Set budget
Default: cover all dimension × domain cells (12 × N modes). If the user specifies a budget
(e.g., "top 6 dimensions only"), honor it — prioritize dimensions in order 1–12.

---

## The 12 Dimensions

All dimensions are defined in `skills/scenario/dimensions.md`. Quick reference:

| # | Dimension | Core question |
|---|-----------|---------------|
| 1 | Best case | What if everything goes right? |
| 2 | Worst case | What if everything goes wrong? |
| 3 | Most likely | What does the realistic outcome look like? |
| 4 | Edge case | What breaks at the boundaries? |
| 5 | Cascade failure | What systemic chain reaction is possible? |
| 6 | Adversarial | What if a motivated actor exploits this? |
| 7 | Time-compressed | What happens under extreme time pressure? |
| 8 | Resource-constrained | What if key resources are cut by 50–90%? |
| 9 | Stakeholder conflict | What if stakeholders have opposing goals? |
| 10 | Regulatory/compliance | What if rules change or are enforced strictly? |
| 11 | Long-term drift | What does degradation look like over 1–5 years? |
| 12 | Recovery/resilience | How does the system recover after failure? |

---

## Balanced Rotation Loop

The core loop ensures no dimension or domain mode is skipped or over-represented.

```
coverage_map = {dim: {mode: False for mode in applicable_modes} for dim in 1..12}

while uncovered_cells exist and budget not exhausted:
    1. Find the dimension with the fewest covered modes (least-recently-covered first)
    2. Within that dimension, pick the first uncovered mode
    3. Analyze that (dimension, mode) cell:
       a. Load the dimension's questions from dimensions.md
       b. Apply them through the lens of the selected domain mode
       c. Write findings to scenario-report.md (see Output section)
    4. Mark cell as covered in coverage_map
    5. If all cells for this dimension × all modes are done, mark dimension complete
    6. Continue to next cell immediately
```

Tie-breaking when multiple dimensions have equal coverage: lower dimension number goes first.

---

## Output

All output goes to `scenario-report.md` in the working directory.

### scenario-report.md structure

```
# Scenario Report: [Subject]
Generated: [date]
Dimensions covered: [N]/12
Domain modes: [list]

---

## Dimension 1: Best Case
### Technical
[findings]
### Business
[findings]
...

## Dimension 2: Worst Case
...

## Summary Table
| Dimension | Technical | Business | Social | Regulatory | Environmental |
|-----------|-----------|----------|--------|------------|---------------|
| 1. Best case | covered | covered | N/A | covered | N/A |
...

## Key Risks Identified
[Top 5 risks ranked by severity × likelihood]

## Recommended Actions
[Concrete actions implied by the scenario analysis]
```

Write `scenario-report.md` incrementally — append each cell as it completes. Do not wait until all cells are done to write.

---

## Termination Conditions

1. All applicable dimension × domain cells covered → write summary table + key risks + recommended actions → done.
2. Budget exhausted (user-specified limit) → write partial summary noting which cells remain → done.
3. User manually interrupts → flush current cell to file → done.

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Only 1 domain mode selected | Run all 12 dimensions for that mode |
| Subject is ambiguous | Ask once to clarify, then proceed |
| A dimension is clearly not applicable | Note "N/A — [reason]" and move on |
| Budget = 0 or subject refused | Abort with clear message |
