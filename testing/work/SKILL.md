---
name: Work
description: Team-based TDD execution with adaptive complexity and agent delegation
---

# Work Skill

## Overview
Execute implementation through an AgentTeam using adaptive TDD. The lead coordinates and delegates -- agents write code.

## Methodology
1. Pick tasks from `bd ready` or `$ARGUMENTS`
2. Mark tasks in progress: `bd update <id> --status=in_progress`
3. Read the epic description (`bd show <epic>`) for spec context -- EARS requirements guide what "done" looks like
4. **Read Acceptance Criteria**: Locate the `## Acceptance Criteria` table in the parent epic description. Each AC row defines a testable criterion that the implementation must satisfy. If no AC section exists, flag as a process gap and proceed using EARS requirements directly.
5. **Read Verification Contract**: Locate the `## Verification Contract` section in the parent epic description.
   - Treat `Required evidence` as the epic's definition of done.
   - Use `Profile`, `Surfaces`, and `Risks` to decide what evidence must be produced during implementation, not just at review time.
   - If the contract is **missing**: flag it as a process gap and fall back to the acceptance criteria, EARS requirements, and legacy `test` + `lint` gates.
6. Run `ca search` per agent/subtask for targeted context. Display results.
7. Assess parallelization: identify independent tasks that can be worked simultaneously
8. Deploy an **AgentTeam** (TeamCreate + Task with `team_name`) with MULTIPLE test-writers and implementers:
   - Role skills: `.claude/skills/compound/agents/{test-writer,implementer}/SKILL.md`
   - Scale teammate count to independent tasks; pairs coordinate via SendMessage on shared interfaces
9. Agents communicate via SendMessage when working on overlapping areas.
10. Lead coordinates: review agent outputs, resolve conflicts, verify tests pass. Do not write code directly.
11. If implementation diverges from spec requirements, acceptance criteria, or the Verification Contract, stop and discuss with user via AskUserQuestion before proceeding.
12. If blocked, use AskUserQuestion to get user direction.
13. Shut down the team when done: send shutdown_request to all teammates.
14. Commit incrementally as tests pass.
15. Run full test suite for regressions.
16. Close tasks: `bd close <id>`

## Memory Integration
- Run `ca search` per delegated subtask with the subtask's specific description
- Each agent receives memory items tailored to their assigned task, not a shared blob
- Run `ca learn` after corrections or novel discoveries

## MANDATORY VERIFICATION -- DO NOT CLOSE TASK WITHOUT THIS
Before `bd close`, you MUST:
1. Read the parent epic's `Required evidence` list and satisfy every listed item. The minimum legacy floor is `test` and `lint`.
2. Run `pnpm test` then `pnpm lint`
3. If `Required evidence` includes `build`, run `pnpm build`
4. Produce the contract-specific evidence needed for the touched surfaces:
   - `browser_evidence` / `responsive_check` / `edge_states_check` / `a11y_smoke`: capture runtime/browser proof and summarize it in the review handoff
   - `contract_checks` / `contract_examples`: run representative requests/examples and record outcomes
   - `command_transcript`: record happy-path and bad-input CLI flows
   - `examples_run` / `docs_examples_sync`: run or update public examples alongside the code
5. Run `/implementation-reviewer` on changed code -- wait for APPROVED
If REJECTED: fix ALL issues, re-run required evidence, resubmit. INVIOLABLE per CLAUDE.md.

The full 8-step pipeline (invariant-designer through implementation-reviewer) is recommended
for complex changes. For all changes, `/implementation-reviewer` is the minimum required gate.

## Beads Lifecycle
- `bd ready` to find available tasks
- `bd update <id> --status=in_progress` when starting
- `bd close <id>` when all tests pass

## Parallelization Strategy
- **Always prefer parallel work**: independent tasks should be assigned to different teammate pairs simultaneously
- **Scale the team adaptively**: deploy multiple test-writer + implementer pairs proportional to independent task count
- **Subagent spawning within teammates**: each teammate should spawn opus subagents for independent subtasks (e.g., a test-writer spawning subagents to write tests for multiple modules in parallel)
- **Coordinate on shared interfaces**: teammates working on overlapping APIs must communicate via SendMessage before implementing

## Literature
- Consult `docs/compound/research/tdd/` for TDD methodology, test-first development evidence, and best practices
- Consult `docs/compound/research/property-testing/` for property-based testing theory and invariant design
- Run `ca knowledge "TDD test-first"` for indexed knowledge on testing methodology
- Run `ca search "testing"` for lessons from past TDD cycles

## Common Pitfalls
- Lead writing code instead of delegating to agents
- Not injecting memory context into agent prompts
- Modifying tests to make them pass instead of fixing implementation
- Not running the full test suite after agent work completes
- Ignoring acceptance criteria from the parent epic
- Ignoring the Verification Contract and closing work with only test/lint evidence

## Quality Criteria
- Tests existed before implementation code
- Agents received relevant memory context
- Lead coordinated without writing implementation code
- Incremental commits made as tests pass
- All tests pass after refactoring
- Task lifecycle tracked via beads (`bd`)
- Implementation aligns with spec requirements from epic
- **Implementation satisfies acceptance criteria from parent epic**
- **Implementation produced the evidence required by the parent epic's Verification Contract**

## PHASE GATE 3 -- MANDATORY
Before starting Review, verify ALL work tasks are closed:
- `bd list --status=in_progress` must return empty
- `bd list --status=open` should only have Review and Compound tasks remaining
If any work tasks remain open, DO NOT proceed. Complete them first.
