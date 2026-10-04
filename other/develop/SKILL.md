---
description: Create growth plans for team members and set OKRs
---

# Develop

Create development plans for "$ARGUMENTS". Set OKRs, define growth paths, and establish how you'll support each team member's progression.

## Prerequisites

Read `.metapowers/leadership/$ARGUMENTS/03-build.md`. If this file does not exist, tell the user:

> Phase 3 (Build) has not been completed for "$ARGUMENTS". Run `/leadership:build $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/leadership/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/leadership/$ARGUMENTS/01-assess.md` for team member maturity
   - Read `.metapowers/leadership/$ARGUMENTS/02-vision.md` for values and success vision
   - Read `.metapowers/leadership/$ARGUMENTS/03-build.md` for roles and responsibilities
   - Read `plugins/leadership/shared/cfr-model.md` for feedback approach

2. **Set team OKRs:**
   - Define 2-3 team-level objectives for the quarter
   - Each objective has 3-5 measurable key results
   - Align with broader organizational goals
   - Make key results specific and time-bound

3. **Create individual growth plans:**
   - For each team member:
     - Current strengths and growth areas (from Assess)
     - 1-2 development goals for the quarter
     - Specific actions to achieve them (stretch assignments, mentoring, learning)
     - How you'll measure progress

4. **Define the feedback cadence:**
   - Weekly 1:1s using the CFR model
   - Monthly progress reviews
   - Quarterly OKR check-ins

5. **Write the artifact** to `.metapowers/leadership/$ARGUMENTS/04-develop.md` with sections:
   - **Team OKRs** — objectives and key results
   - **Individual Growth Plans** — per-person development goals
   - **Feedback Cadence** — 1:1, monthly, quarterly schedule
   - **Support Commitments** — what you'll do to enable growth

## Output

The development plan written to `.metapowers/leadership/$ARGUMENTS/04-develop.md`. Present a summary highlighting:
- Team OKRs
- Growth focus per person
- Feedback cadence
