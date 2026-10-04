---
name: herdr-cockpit
description: "Guide the main agent in routing workflow-shaped tasks, managing context, explaining project status, and integrating work across the user's six-pane Herdr coding cockpit."
license: MIT
---

# Herdr Cockpit

This skill defines the operating model for the user's six-pane Herdr coding
cockpit. It is guidance for the main agent after the human starts the layout;
it is not a second Herdr launcher and it must never start a nested Herdr
session. The main agent treats the cockpit as a context-management system:
workflow is the unit of delegation, not the pane or model identity. Read
[references/workflow-routing.md](references/workflow-routing.md) when selecting
a workflow or writing a helper prompt.

The human startup flow is:

```text
outside Herdr:  herdr
inside Herdr:   choose a workspace and any tab, cd to the project, type hc
```

`hc` is the zsh entrypoint in `config/zsh/cockpit.zsh`. It uses the current
workspace, current tab, and current `$PWD` for the active project, then expands
a single-pane tab into this layout. The left column has two large controller
panes; the right column has four stacked worker/utility panes. Claude is always
launched from `~/Work/github/idea`. Every named worker/Claude agent
receives a workspace-qualified live name, for example `w1-idea-center`:

```text
┌──────────────────────┬──────────────────────┐
│ main / Codex         │ lazygit / utility     │
│ orchestrator         │ lazygit               │
│                      ├──────────────────────┤
│                      │ w1-worker-1 / Agy     │
│                      │ agy                   │
├──────────────────────┼──────────────────────┤
│ w1-idea-center /     │ w1-worker-2 / Pi      │
│ Claude               │                       │
│ claude               │ pi                    │
│                      ├──────────────────────┤
│                      │ w1-worker-3 / Pi      │
│                      │ pi                    │
└──────────────────────┴──────────────────────┘
```

The `w1` prefix above is illustrative. At runtime `hc` uses the current
`HERDR_WORKSPACE_ID` as a lowercase namespace, so `wC` becomes `wc` and a
second workspace gets a separate name such as `w2-worker-1` instead of
colliding with `w1-worker-1`. The role labels `idea-center`, `worker-1`,
`worker-2`, and `worker-3` remain logical roles; use the workspace-qualified
live name for Herdr commands.

It is idempotent for the expected six-pane layout and fails closed when the
current tab already contains an unrelated multi-pane layout. Existing four- and
five-pane layouts are not upgraded automatically because doing so would require
stopping or moving running agents. Open a new single-pane tab for the new
layout. Do not run bare
`herdr` from a managed pane: Herdr's nested-launch guard is intentional. For
control calls, require `HERDR_ENV=1` and use the existing Herdr CLI/socket API.

## Pane semantics

The top-left Codex pane is the orchestrator and owns the user-facing task,
decomposition, decisions, integration, and final report. The other panes are
workers or utilities, not independent owners of the overall task:

- `idea-center / Claude`: maintain `~/Work/github/idea`, incubate ideas,
  and help brainstorm how an idea can land in the current project. It may read
  the target project when Codex supplies its path, but it is never the owner of
  target-project implementation. Any write assignment is limited to the idea
  repo and its requested topic.
- `worker-1 / agy`, `worker-2 / pi`, and `worker-3 / pi`: form a scheduling
  pool. Their physical runtime is fixed by the launcher, but their workflow is
  not: Codex may assign status explanation, context audit, research,
  implementation, review, or documentation to any available worker. Agy is
  the preferred owner when the user explicitly requests the ELI5 project-state
  workflow.
- `lazygit / utility`: provide a visual Git status and diff surface. It is not
  an agent and should not be used to stage, commit, reset, or publish changes
  without an explicit main-agent decision.

Codex, Agy, both Pi workers, and lazygit initially use the current project
checkout. The idea-center Claude pane uses `~/Work/github/idea` instead.
Claude may inspect the target project read-only when Codex supplies its path,
but implementation and integration remain owned by Codex. The right-side
workers are context consumers and bounded executors; none of them becomes the
owner of the user's overall task.

## Workflow routing and context ownership

The orchestrator chooses the smallest workflow that answers the user's need,
then selects an available worker by capability and current context. Do not
infer a permanent role from `worker-1`, `worker-2`, or `worker-3`. The standard
workflow types are:

| Workflow | Default owner | Write policy | Result |
| --- | --- | --- | --- |
| `idea-maintenance` | `idea-center` | Idea repo only | Updated idea artifact and receipt |
| `brainstorm-to-land` | `idea-center` + Codex | Read-only target project; idea repo only if requested | Options, assumptions, landing path, next experiment |
| `status-explain` | Codex, with optional workers | Read-only | Evidence-backed progress report |
| `context-audit` | Any right-side worker | Read-only | Current repo/task/context snapshot |
| `scout-research` | Any right-side worker | Read-only unless explicitly bounded otherwise | Findings with sources and uncertainty |
| `eli5-project-state` | Agy worker | Read-only source tree; isolated artifact output | Visual, plain-language HTML explanation opened for user review |
| `build` | Any right-side worker | Isolated worktree required | Diff, tests, risks, and receipt |
| `review-verify` | Any right-side worker | Read-only by default | Review findings and verification evidence |

Codex owns the canonical context ledger, dispatch decisions, synthesis, and
integration. Workers receive a compact context packet and return a receipt;
they do not redefine the task, silently broaden scope, or update the global
status from a green command alone. The detailed routing matrix, packet, receipt
format, progress workflow, and Agy ELI5 prompt are in
[references/workflow-routing.md](references/workflow-routing.md).
The idea-center discovery procedure is in
[workflows/idea-center-project-discovery.md](workflows/idea-center-project-discovery.md).

Worker-generated artifacts have a separate ownership boundary: the assigned
worker owns the artifact bytes and all artifact revisions. Codex may inspect
the artifact, verify its claims, request corrections through the live agent,
and open the accepted artifact for the user; Codex must not edit, rewrite, or
patch a worker-owned artifact directly. If verification finds a gap, preserve
`REVIEW_STATUS: changes-requested`, send a focused correction receipt to the
same owner, and wait for a new artifact receipt. If the owner cannot revise it,
report `blocked` rather than taking over the artifact.

## Execution policy, worktrees, and task identity

The user's default execution policy is dangerous mode for Claude, Agy, and both
Pi workers. This is an intentional permission-prompt trade-off, not a transfer
of user authority. Every prompt must still state its scope, boundaries, and
evidence requirements; no worker may decide to push, merge, deploy, contact an
external service, or handle secrets unless Codex has explicit authorization.

The pane's workspace-qualified live agent name is only a control handle. Codex
must keep a durable task record separate from Herdr names and pane IDs. At
minimum, each task
record contains:

- `task_id` and exactly one `owner_agent`;
- target repository, branch or commit, and assigned worktree;
- objective, acceptance criteria, permissions, and budget;
- current pane/name plus a receipt containing status, files, checks, risks,
  review state, and the next step.

Any task that can write files must receive an isolated Git worktree before
parallel execution. Never assign overlapping write tasks to the initial shared
checkout. Read-only reconnaissance may use the current checkout; implementation
work must use one worktree per task, and Codex owns integration back into the
main checkout. A successful prompt or green command is not a receipt, and a
receipt is not downstream acceptance until Codex verifies it.

## Main-agent control loop

At the beginning of a task, the main agent should:

1. Inspect the repository state and the current Herdr workspace, tab, and panes.
2. Resolve live pane IDs or live agent names from Herdr responses; never guess
   IDs from screen position or old output.
3. Classify the request into a standard workflow; for "explain current
   progress", start with `status-explain` and use read-only workers only where
   they add independent evidence.
4. Before dispatching any worker, run the context preflight in
   [references/workflow-routing.md](references/workflow-routing.md). Treat
   `unknown` as a failed gate; clear and re-probe once before routing elsewhere
   or reporting blocked.
5. Build a minimal current context packet and record its verified facts,
   unknowns, task ID, owner, acceptance criteria, permissions, and budget.
6. Allocate an isolated worktree for every task that may write.
7. Send each helper one narrow assignment with an explicit workflow, scope,
   context packet, and evidence requirement.
8. Wait for the helper, read its receipt, inspect the resulting files and tests,
   and only then update the ledger or assign the next step.
9. Integrate changes and perform the final verification from the main pane.

Use Herdr's agent control sequence for recognized agents. Resolve the current
workspace namespace first. For workspace `w1`, the live names are
`w1-idea-center`, `w1-worker-1`, `w1-worker-2`, and `w1-worker-3`; another
workspace has different names:

```bash
workspace_namespace="${HERDR_WORKSPACE_ID:l}"
idea_agent="${workspace_namespace}-idea-center"
agy_agent="${workspace_namespace}-worker-1"
pi_agent_2="${workspace_namespace}-worker-2"
pi_agent_3="${workspace_namespace}-worker-3"

herdr agent list
herdr agent prompt "$idea_agent" "<question plus current-project context>" --wait --timeout 120000
herdr agent read "$idea_agent" --source recent-unwrapped --lines 120
herdr agent prompt "$agy_agent" "<bounded Agy assignment>" --wait --timeout 120000
herdr agent prompt "$pi_agent_2" "<bounded Pi assignment>" --wait --timeout 120000
herdr agent prompt "$pi_agent_3" "<bounded Pi assignment>" --wait --timeout 120000
```

Use `pane run` for ordinary shell commands, tests, or starting a process in a
known shell pane. Use `agent get` and `agent read` before reacting to a
`blocked` state. Do not send blind keys to a pane that may contain unsent
input.

## Assignment contract

Every helper prompt should state:

```text
ROLE: idea-center | worker-1 | worker-2 | worker-3
LIVE_AGENT_NAME: <lowercase-workspace-id>-<logical-role>
WORKFLOW: idea-maintenance | idea-center-project-discovery | brainstorm-to-land | status-explain | context-audit | scout-research | eli5-project-state | build | review-verify
TASK_ID: durable task identifier
OWNER_AGENT: exactly one named live owner
OBJECTIVE: one concrete outcome
CONTEXT_SNAPSHOT: current repo/branch/head, user goal, verified facts, unknowns
WORKTREE: isolated checkout for any write task
ARTIFACT_OWNER: exactly one worker owner for any generated artifact
ARTIFACT_MUTATION: owner-agent-only; Codex may verify and open, but must not edit
SCOPE: files, commands, or question in scope
BOUNDARIES: what must not be changed or published
ACCEPTANCE: observable conditions for acceptance
EVIDENCE: tests, diff, citations, or reproduction required
OUTPUT_FORMAT: receipt and any requested artifact
OPEN_FOR_REVIEW: yes | no
RETURN: status, files, checks, risks, review state, and blocker/next step
```

Every helper handoff must distinguish `done`, `blocked`, `unknown`, and
`in-progress`. A green command alone is not proof that the requested behavior
is complete. The main agent must preserve uncertainty and ask the user when a
decision, permission, worktree, secret, deployment, push, or merge is needed.

## Safety rules

- Before every Herdr CLI call, verify `test "${HERDR_ENV:-}" = 1`; stop if the
  call is not originating from a managed pane.
- Use the current workspace and tab as the default scope. Do not create,
  attach, focus, move, resize, close, or stop unrelated workspaces or panes.
- Use explicit pane IDs returned by Herdr and re-read state after layout or
  agent changes.
- Keep `idea-center` limited to idea maintenance and landing brainstorms; do
  not ask it to implement the target project.
- Keep worker-generated artifact revisions with their named owner. Do not use
  the main pane to patch an Agy or Pi artifact after inspection; route the gap
  back through Herdr and verify the replacement receipt.
- Keep the `codexyolo` alias within the user's requested scope. Claude, Agy,
  and both Pi workers are started as named Herdr agents in dangerous mode by
  default. Dangerous mode does not authorize push, merge, deploy, external
  messages, paid actions, or secret handling.
- Never use dangerous mode as a reason to skip worktree isolation, task
  ownership, acceptance checks, or receipt verification.
- Keep final integration and external mutations in the main pane unless the
  user explicitly delegates them.
- If the Herdr client and server report a protocol mismatch, report it and
  stop; never stop the shared server to repair a client mismatch.

## Validation

From the dotfiles repository:

```bash
zsh -n config/zsh/.zshrc config/zsh/cockpit.zsh
python3 /Users/memorysaver/.codex/skills/.system/skill-creator/scripts/quick_validate.py agents/skills/herdr-cockpit
just validate-skills
git diff --check
```
