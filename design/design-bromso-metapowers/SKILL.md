---
description: Generate and evaluate multiple solution concepts for the defined problem
---

# Design

Diverge on solutions for "$ARGUMENTS". Generate multiple solution concepts, evaluate feasibility, and prioritize the most promising approaches.

## Prerequisites

Read `.metapowers/research/$ARGUMENTS/01-discover.md` and `.metapowers/research/$ARGUMENTS/02-define.md`.

If `02-define.md` does not exist, tell the user:

> Phase 2 (Define) has not been completed for "$ARGUMENTS". Run `/research:define $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/research/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/research/$ARGUMENTS/01-discover.md` for research findings
   - Read `.metapowers/research/$ARGUMENTS/02-define.md` for problem statement, HMW questions, and success criteria
   - Read `plugins/research/shared/double-diamond-guide.md` for methodology reference

2. **Research existing solutions:**
   - Use WebSearch to find case studies, best practices, and proven approaches related to each HMW question
   - Use WebFetch to read detailed implementations or methodologies
   - Note what worked, what failed, and why

3. **Generate solution concepts:**
   - Create 3-5 distinct solution concepts, each addressing the problem statement from a different angle
   - For each concept: describe the approach, key components, and how it addresses the HMW questions
   - Include at least one unconventional or contrarian approach

4. **Evaluate each concept:**
   - **Feasibility:** How realistic is implementation? What resources are needed?
   - **Impact:** How well does it address the problem statement and success criteria?
   - **Effort:** What's the relative effort to implement?
   - **Risk:** What could go wrong? What assumptions are being made?

5. **Prioritize and recommend:**
   - Rank concepts by impact/feasibility balance
   - Recommend top 1-2 concepts for validation in the Deliver phase
   - Explain trade-offs between the top options

6. **Write the artifact** to `.metapowers/research/$ARGUMENTS/03-design.md` with sections:
   - **Problem Recap** — one-paragraph summary from Define
   - **Solution Concepts** — each concept with description and rationale
   - **Evaluation Matrix** — feasibility, impact, effort, risk per concept
   - **Recommendations** — top concepts with reasoning
   - **Validation Plan** — what to test in the Deliver phase

## Output

The solution concepts written to `.metapowers/research/$ARGUMENTS/03-design.md`. Present a summary to the user highlighting:
- Number of concepts generated
- Top recommendation and why
- Key trade-offs between top options
- What needs validation in the Deliver phase
