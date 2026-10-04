---
description: Synthesize research findings into a clear problem statement and research plan
---

# Define

Converge the broad discovery findings on "$ARGUMENTS" into a focused problem statement, "How Might We" questions, and a research plan for the solution phase.

## Prerequisites

Read `.metapowers/research/$ARGUMENTS/01-discover.md`. If this file does not exist, tell the user:

> Phase 1 (Discover) has not been completed for "$ARGUMENTS". Run `/research:discover $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/research/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/research/$ARGUMENTS/01-discover.md` for discovery findings
   - Read `plugins/research/shared/double-diamond-guide.md` for methodology reference
   - Read `plugins/research/shared/research-plan-template.md` for output structure

2. **Synthesize findings:**
   - Review all themes from the Discover phase
   - Identify the core tension or unmet need
   - Distinguish root causes from symptoms
   - Map relationships between themes

3. **Formulate the problem statement:**
   - Write a clear, specific, actionable problem statement
   - Avoid solution-language (the problem, not the answer)
   - Ensure it's scoped enough to be solvable

4. **Generate "How Might We" questions:**
   - Create 3-5 HMW questions that reframe the problem as opportunities
   - Each HMW should open a different solution direction
   - Avoid HMW questions that are too broad or too narrow

5. **Define success criteria and scope:**
   - What does "solved" look like? Specify measurable criteria
   - What's in scope and out of scope for the Design phase?
   - Identify constraints and assumptions

6. **Write the artifact** to `.metapowers/research/$ARGUMENTS/02-define.md` following the research plan template structure.

## Output

The problem definition written to `.metapowers/research/$ARGUMENTS/02-define.md`. Present a summary to the user highlighting:
- The problem statement
- Top HMW questions
- Key scope decisions
- Recommended focus for the Design phase
