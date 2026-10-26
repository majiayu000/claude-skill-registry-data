---
name: Cook It
description: Full-cycle orchestrator chaining all five phases with gates and controls
---

# Cook It Skill

## Overview

Chain all 5 phases end-to-end: Spec Dev, Plan, Work, Review, Compound. This skill governs the orchestration -- phase sequencing, gates, progress tracking, and error recovery.

## CRITICAL RULE -- READ BEFORE EXECUTE
Before starting EACH phase, you MUST use the Read tool to open its skill file:
- .claude/skills/compound/spec-dev/SKILL.md
- .claude/skills/compound/plan/SKILL.md
- .claude/skills/compound/work/SKILL.md
- .claude/skills/compound/review/SKILL.md
- .claude/skills/compound/compound/SKILL.md

Do NOT proceed from memory. Read the skill, then follow it exactly.

## Session Start
When a cooking session begins, IMMEDIATELY print the banner below (copy it verbatim):

         o
        /|\
       o-o-o
      /|\ /|\
     o-o-o-o-o
      \|/ \|/
       o-o-o
        \|/
         o

Then proceed with the protocol below.

## Phase Execution Protocol
0. Initialize state: `ca phase-check init <epic-id>`
For each phase:
1. Announce: "[Phase N/5] PHASE_NAME"
2. Start state: `ca phase-check start <phase>`
3. Read the phase skill file (see above)
4. Run `ca search` and `ca knowledge` with the current goal -- display results before proceeding
5. Execute the phase following the skill instructions
6. Update epic state: `bd update <epic-id> --notes="Phase: NAME COMPLETE | Next: NEXT"`
7. Verify phase gate before proceeding to the next phase

## Phase Gates (MANDATORY)
- **After Plan**: Run `bd list --status=open` and verify Review + Compound tasks exist, then run `ca phase-check gate post-plan`
- **After Plan (AC Gate)**: Run `bd show <epic-id>` and verify the `## Acceptance Criteria` section exists in the epic description. If missing, the plan phase MUST be re-entered to generate the AC table before proceeding to Work. This gate ensures the contract between plan and work is fulfilled.
- **After Plan (Verification Contract Gate)**: Run `bd show <epic-id>` and verify the `## Verification Contract` section exists in the epic description. If missing, the plan phase MUST be re-entered to define the epic-local proof of done before proceeding to Work.
- **After Work (GATE 3)**: `bd list --status=in_progress` must be empty. Then run `ca phase-check gate gate-3`
- **After Review (GATE 4)**: /implementation-reviewer must have returned APPROVED. Then run `ca phase-check gate gate-4`
- **After Compound (FINAL GATE)**: Run `ca verify-gates <epic-id>` (must PASS), `pnpm test`, and `pnpm lint`. Then read the epic's `## Verification Contract` and run every required evidence item that remains open, including `pnpm build` when `build` is required, before running `ca phase-check gate final` (auto-cleans phase state)

If a gate fails, DO NOT proceed. Fix the issue first.

## Phase Control
- **Skip phases**: Parse arguments for "from PHASE" (e.g., "from plan"). Skip earlier phases.
- **Resume**: After interruption, run `bd show <epic-id>` and read notes for phase state. Resume from that phase.
- **Retry**: If a phase fails, report and ask user to retry, skip, or abort via AskUserQuestion.
- **Progress**: Always announce current phase number before starting.

## Stop Conditions
- Spec dev reveals goal is unclear -- stop, ask user
- Tests produce unresolvable failures -- stop, report
- Review finds critical security issues -- stop, report

## Common Pitfalls
- Skipping the Read step for a phase skill (NON-NEGOTIABLE)
- Not running phase gates between phases
- Not announcing progress ("[Phase N/5]")
- Proceeding after a failed gate
- Not updating epic notes with phase state (loses resume ability)
- Batching all commits to the end instead of committing incrementally
- Not verifying AC table exists after plan phase before starting work
- Not verifying the Verification Contract exists after plan phase before starting work

## Quality Criteria
- All 5 phases were executed (3/5 is NOT success)
- Each phase skill was Read before execution
- Phase gates verified between each transition
- **AC table verified present after plan phase**
- **Verification Contract verified present after plan phase**
- Epic notes updated after each phase
- Memory searched at the start of each phase
- `ca verify-gates` passed at the end

## Verification Contract
Cook-it does not invent "done" late in the cycle. The `## Verification Contract` written during plan is the epic-local source of truth for:
- product profile (`webapp`, `api`, `cli`, `library`, `service`, or `mixed`)
- touched surfaces
- principal risks
- required evidence

If the contract is missing, stop and go back to plan. The fallback to legacy `test` + `lint` exists for older epics, not for newly planned work.

## SESSION CLOSE -- INVIOLABLE
Before saying "done": git status, git add, bd sync, git commit, bd sync, git push.
If phase state gets stuck, use the escape hatch: `ca phase-check clean` (or `ca phase-clean`).
