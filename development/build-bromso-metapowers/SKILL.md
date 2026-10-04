---
description: Structure the team — roles, responsibilities, and delegation framework
---

# Build

Structure the team for "$ARGUMENTS". Define roles, responsibilities, ownership areas, and establish a delegation framework.

## Prerequisites

Read `.metapowers/leadership/$ARGUMENTS/01-assess.md` and `.metapowers/leadership/$ARGUMENTS/02-vision.md`. If `02-vision.md` does not exist, tell the user:

> Phase 2 (Vision) has not been completed for "$ARGUMENTS". Run `/leadership:vision $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/leadership/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/leadership/$ARGUMENTS/01-assess.md` for team assessment
   - Read `.metapowers/leadership/$ARGUMENTS/02-vision.md` for values and culture
   - Read `plugins/leadership/shared/decision-frameworks.md`

2. **Define team structure:**
   - Map each team member's role and primary responsibilities
   - Identify ownership areas — who owns what?
   - Clarify decision rights using the RAPID framework
   - Identify gaps: any roles or skills missing?

3. **Create delegation framework:**
   - For each team member: what can they own autonomously?
   - What needs consultation before deciding?
   - What do you retain as leader?
   - Match delegation level to team member maturity (from Assess)

4. **Define collaboration norms:**
   - How does work get assigned and tracked?
   - What's the escalation path for blockers?
   - How do team members collaborate across ownership areas?

5. **Write the artifact** to `.metapowers/leadership/$ARGUMENTS/03-build.md` with sections:
   - **Team Structure** — roles, responsibilities, ownership map
   - **Decision Rights** — RAPID matrix for key decision types
   - **Delegation Framework** — per-person autonomy levels
   - **Collaboration Norms** — assignment, tracking, escalation

## Output

The team structure written to `.metapowers/leadership/$ARGUMENTS/03-build.md`. Present a summary highlighting:
- Ownership map
- Key delegation decisions
- Any gaps identified
