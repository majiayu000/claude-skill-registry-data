---
name: multi-agent-team
description: Run a gated multi-agent coding workflow for development requests. Use when the user asks Codex to use multiple agents, a team of agents, subagents, architect/frontend/backend/test/review/merge agents, Git worktree isolation, or to execute a feature until it is implemented, reviewed, integrated, merged, and independently verified.
---

# Multi-Agent Team

Use this skill to execute a development request with a coordinated Codex agent team. The Controller is the current Codex session. The workflow is mandatory unless the user explicitly asks only for planning or analysis.

## Global Rules

1. Start with the Architect Agent.
2. Clarify only requirement gaps that affect implementation, acceptance criteria, data contracts, safety boundaries, or testability.
3. Use the smallest reasonable assumption for low-risk details the user cannot answer, and record it in the acceptance criteria.
4. Use these roles unless the Architect Agent explicitly says a role is not applicable:
   - Architect Agent
   - Frontend Agent
   - Backend Agent
   - Review Agent
   - Test Agent
   - Merge Agent
5. The Controller MUST NOT start the Test Agent before code review passes.
6. The Controller MUST NOT start the Merge Agent before integration testing passes.
7. Every agent that writes code MUST work in an isolated Git worktree.
8. Every gate report MUST include the relevant commit SHA.
9. Any failed gate sends the work back to the responsible agent. After rework, all later gates must run again.
10. Do not stop after a plan, partial implementation, or local success claim.
11. After merge, the Architect Agent must dispatch an independent verification subagent to inspect the real current codebase.
12. Never revert user changes or unrelated changes made by other agents.

If subagent tools are unavailable in the current environment, report that the multi-agent requirement is blocked and do not pretend that separate agents were used.

## Worktree Rules

The Architect Agent must detect and record `<base-branch>` before any worktree is created.

Recommended PowerShell pattern:

```powershell
git worktree add ..\<repo-name>-worktrees\<task-id>-frontend -b codex\<task-id>\frontend <base-branch>
git worktree add ..\<repo-name>-worktrees\<task-id>-backend -b codex\<task-id>\backend <base-branch>
git worktree add ..\<repo-name>-worktrees\<task-id>-review -b codex\<task-id>\review <base-branch>
git worktree add ..\<repo-name>-worktrees\<task-id>-test -b codex\<task-id>\test <base-branch>
git worktree add ..\<repo-name>-worktrees\<task-id>-merge -b codex\<task-id>\merge <base-branch>
```

Rules:

1. `<task-id>` is created by the Architect Agent in kebab-case.
2. Each coding agent owns only the files/modules assigned by the Architect Agent.
3. Each agent runs `git status --short` before reporting completion.
4. The Test Agent should primarily add or update tests, fixtures, integration scripts, or test harnesses.
5. The Review Agent reviews by default and should not directly rewrite implementation code except tiny documentation or formatting fixes.
6. The Merge Agent only integrates branches that already passed review and testing.

## Architect Agent

Responsibilities:

1. Read the user request and inspect the current codebase.
2. Detect `<base-branch>`.
3. Identify material unclear points.
4. Ask the user through the Controller until material requirements are clear enough.
5. Define low-risk assumptions when needed.
6. Split work into frontend, backend, review, testing, and merge tasks.
7. Define API/module contracts, ownership scopes, and forbidden edit areas.
8. After merge, dispatch an independent verification subagent.

Required output:

```text
Requirement summary:
- ...

Base branch:
- <base-branch>

Acceptance criteria:
- ...

Task split:
- Frontend Agent:
- Backend Agent:
- Review Agent:
- Test Agent:
- Merge Agent:

Contract:
- Inputs:
- Outputs:
- Error behavior:
- Data shape:

Ownership:
- Frontend editable files/modules:
- Backend editable files/modules:
- Test editable files/modules:
- Forbidden areas:
```

## Frontend Agent

Responsibilities:

1. Implement assigned UI, interaction, frontend state, validation, and API calls.
2. Use mock data or a mock API before integration.
3. Run a frontend self-test against the mock data/API.
4. Submit to Review Agent only after self-test passes.
5. If review or testing fails, fix the frontend part, rerun self-test, and resubmit through review before integration testing.

Required report:

```text
Frontend completion report:
- Changed files:
- Mock data/API used:
- Self-test command:
- Self-test result:
- Self-tested commit:
- Implemented contract fields:
- Known limitations:
```

Constraints:

1. Prefer existing frontend style and patterns.
2. Avoid unnecessary state management, global abstractions, frameworks, or generic utilities.
3. Stay inside the assigned ownership scope.

## Backend Agent

Responsibilities:

1. Implement assigned APIs, business logic, data handling, persistence, or service-layer changes.
2. Use mock requests, mock frontend calls, fixtures, or mocked external dependencies before integration.
3. Run a backend self-test against mock input/dependencies.
4. Submit to Review Agent only after self-test passes.
5. If review or testing fails, fix the backend part, rerun self-test, and resubmit through review before integration testing.

Required report:

```text
Backend completion report:
- Changed files:
- Mock request/fixture/dependency used:
- Self-test command:
- Self-test result:
- Self-tested commit:
- Implemented API/module contract:
- Error behavior:
- Known limitations:
```

Constraints:

1. Prefer existing backend style and patterns.
2. Avoid unused layers, queues, plugin systems, factories, service registries, or broad abstractions for hypothetical future needs.
3. Stay inside the assigned ownership scope.

## Review Agent

Responsibilities:

1. Review frontend and backend implementation before integration testing.
2. Focus on over-engineering, unnecessary abstraction, needless dependencies, and simpler ways to satisfy the current requirement.
3. Check correctness, maintainability, project style, necessary boundary handling, and test coverage.
4. Use the review worktree to inspect frontend/backend diffs against `<base-branch>`, or temporarily merge the frontend/backend branches into the review worktree for read-only inspection.
5. If review fails, send concrete required changes to the responsible agent.
6. If review passes, notify Controller that integration testing may start.
7. When reviewing rework, the Review Agent may review only the rework diff, but must confirm it does not break previously approved behavior.

Required output:

```text
Review result: pass / fail
Reviewed scope: full implementation / rework diff
Approved frontend commit:
Approved backend commit:

Required changes:
- [agent] [file/module] [issue] [recommended fix]

Optional suggestions:
- ...

Verified tests:
- ...
```

## Test Agent

Responsibilities:

1. Receive reviewed frontend/backend branches and approved commit SHAs.
2. Integrate reviewed branches in the test worktree.
3. Run integration, contract, E2E, or equivalent project verification.
4. If integration fails, identify whether failure belongs to frontend, backend, contract mismatch, test setup, or unclear requirements.
5. Report failures with clear ownership and evidence.
6. When integration passes, send the result to Controller so Merge Agent can start.

Required report:

```text
Integration test report:
- Branches tested:
- Tested frontend commit:
- Tested backend commit:
- Test commands:
- Test result:
- Evidence:
- Failures, if any:
- Responsible agent, if failed:
- Required fix, if failed:
```

Constraints:

1. Do not lower acceptance criteria to make tests pass.
2. Do not silently work around frontend/backend contract mismatches.
3. Send requirement ambiguity back to Architect Agent.

## Merge Agent

Start only after Review Agent passes and Test Agent passes after that review.

Responsibilities:

1. Use an isolated merge worktree.
2. Merge approved frontend, backend, and test branches.
3. Resolve merge conflicts.
4. Ask the responsible agent when a conflict cannot be resolved safely.
5. Run the full verification command set defined by Architect Agent.
6. Prepare the merged result for `<base-branch>`.

Required report:

```text
Merge report:
- Target base branch:
- Branches merged:
- Merged frontend commit:
- Merged backend commit:
- Merged test commit:
- Conflict files:
- Conflict resolution summary:
- Verification commands:
- Verification result:
- git status --short:
```

Constraints:

1. Do not remove feature behavior just to resolve conflicts.
2. Do not add new business behavior.
3. Use the Architect Agent's recorded `<base-branch>`.

## Workflow

1. Requirement clarification:
   - Architect Agent inspects code and clarifies only material requirement gaps.
   - Exit with requirement summary, `<base-branch>`, acceptance criteria, task split, contract, and ownership scopes.
2. Parallel implementation:
   - Frontend and Backend Agents work in isolated worktrees.
   - Both must pass mock self-tests and report self-tested commit SHAs.
3. Code review:
   - Review Agent reviews before integration testing.
   - Exit only when review passes and approved frontend/backend commit SHAs are recorded.
4. Integration testing:
   - Test Agent starts only after review passes.
   - If testing fails, responsible agent fixes, reruns self-test, returns to review, then retests integration.
5. Merge:
   - Merge Agent starts only after reviewed commits pass integration.
   - Merge into `<base-branch>` and run full verification.
6. Independent final verification:
   - Architect Agent dispatches a separate verification subagent.
   - Verification subagent reads the real current codebase after merge and checks original acceptance criteria.
   - If incomplete, Architect Agent assigns the failure to the correct phase and the workflow repeats from there.

Final completion requires:

1. All acceptance criteria satisfied.
2. Frontend mock self-test passed.
3. Backend mock self-test passed.
4. Code review passed before integration testing.
5. Integration testing passed after review.
6. Merge to `<base-branch>` succeeded.
7. Independent final verification passed.

## Communication Protocol

All cross-agent messages must use:

```text
From agent:
To agent:
Subject:
Context:
Required confirmation or change:
Blocking level: blocking / non-blocking
Related files:
Related commands or logs:
```

Any interface or contract change must go to Architect Agent. Frontend and Backend Agents must not independently invent incompatible fields or behavior.

## Final User Response

When complete, reply in the user's preferred language:

```text
Task completed.

Completed work:
- ...

Verification:
- Frontend mock self-test: passed, command: ...
- Backend mock self-test: passed, command: ...
- Review: passed
- Integration test: passed, command: ...
- Merge: completed on <base-branch>
- Independent final verification: passed

Key files:
- ...
```

If blocked or incomplete, do not claim completion. Report current phase, responsible agent, blocking reason, and next action.
