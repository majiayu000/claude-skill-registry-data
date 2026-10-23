---
name: plan-create
description: Create a final implementation-ready plan from a user brief, settled decisions, and repository evidence. Use when work needs ordered phases, concrete deliverables, dependencies, risks, and validation before coding.
---

# Plan Creation

Synthesize an implementation-ready plan rather than repeating discovery, architecture sparring, or research.

## Workflow

1. Confirm the brief, authoritative repository evidence, applicable instructions, output location, and whether writing a repository plan file is authorized.
2. Identify only decisions whose absence changes the implementation path. Resolve them with the user or record a blocker; keep safe assumptions explicit.
3. Use `architecture-refine` for unresolved architecture decisions and `technical-spike` for blocking unfamiliar or version-sensitive behavior. When an autonomous delivery workflow calls this skill, follow that workflow's rule for open decisions instead of asking the user.
4. Lock ownership boundaries, non-goals, compatibility, rollout order, validation gates, risks, and unresolved blockers.
5. Divide the work into phases ordered by real dependencies. Each phase must leave the build and tests passing and be small enough to validate and review alone. A phase is one or more commits on the task's single branch and pull request, not a separate pull request. Plan separate or stacked pull requests only when the user asks for them or when one change must be deployed before the next can merge.
6. Give each phase a goal, concrete deliverables, dependencies, steps, acceptance evidence, and structural traps to avoid.
7. Challenge the design against the code before you finalize it:
   - Root cause: confirm that each fix acts where the defect starts. When an option only narrows the defect's window, for example with more retries, longer timeouts, or added guards, say so in the option and offer the root-cause fix beside it.
   - Callers: for each changed unit, read its callers up to the entry point and what they run after it returns. Check each new wait, retry, or detached context against every enclosing deadline, timeout, loop, and cancellation path, and confirm that a later attempt can succeed.
   - Reuse: name the existing helper to extend before you plan a new one.
   - Removed behavior: for each guard, log, error path, or wait that the plan replaces, state where its behavior moves or why it goes.
   - Touched units: list known defects in the functions the plan changes, and fix each one in a phase or record it as a non-goal.
8. Reread the plan for hidden assumptions, missing prerequisites, contradictory acceptance criteria, failure and recovery gaps, and duplicate ownership.

Use the repository's established plan format. Omit empty ceremony. Name concrete subsystems, files, interfaces, migrations, UI surfaces, or test layers only where they remove implementation ambiguity.

Do not implement, validate, commit, push, or release. Keep a local behavior-preserving structural plan proportionate to its actual risk.

Finish when implementation-changing decisions are settled or explicit blockers, phases are dependency-ordered, and every phase has observable acceptance evidence.
