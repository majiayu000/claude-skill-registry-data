---
name: teamwork
description: Build and scaffold a multi-agent collaboration workspace with the right coordination model, shared operating files, and role-specific skills. Use when a user wants to create a team, crew, task force, asynchronous collaboration loop, specialist handoff workflow, or reusable shared workspace for multiple agents, then route execution to the right teamwork skill.
---

# Teamwork

Build a task force only when the work is genuinely multi-track. If one capable agent can finish the job cleanly, use one agent.

## Path conventions

Paths in this skill are relative to the directory containing this `SKILL.md` unless the document explicitly says otherwise, and they are not relative to the workspace root or the shell's current `./`.

- Scripts in this skill use paths like `scripts/...`
- Reference material in this skill uses paths like `references/...`
- Paths such as workspace `skills/`, `agents.md`, or task-force artifact directories are external workspace targets and are called out explicitly
- When a command below says `python scripts/...`, resolve that script path against the skill's absolute Base Directory
- In command examples below, replace `<skill-base-dir>` with the skill's actual absolute Base Directory

## Non-Negotiable Rules

1. **One team, one effective workspace.** The governing coordinator and org-visible children keep the normal parent/override workspace inheritance model. Consequently, `agents.md` and `SOUL.md` are resolved from this shared effective workspace by default.
2. **Prepare artifact storage first.** From the governing root session, call `agent__prepareTeamworkWorkspace()` to get an app-local artifact directory before scaffolding teamwork files.
3. **Scaffold only in that artifact directory.** Do not write `agents.md`, `MISSION.md`, `ROLES.md`, `coordination/`, or role `skills/` into a repo root unless you intentionally want repo pollution.
4. **Use deterministic scaffolding first.** `scripts/init_task_force.py` is the default path.
5. **Refresh happens later.** Changes to `agents.md` or workspace skills do not take effect in the current turn.
6. **Route execution explicitly.** Keep framework-specific operating rules in the specialist skill that matches the chosen substrate.

## Operating Rule

Start by deciding whether the request needs:

1. **No task force** - one agent can do it end-to-end.
2. **Small task force** - 2-4 specialists with explicit handoffs.
3. **Persistent task force** - a shared workspace plus recurring or resumable collaboration.

Default to the smallest structure that can succeed.

## Core Workflow

### 1. Shape the task force

Extract four things before writing files:

1. **Mission** - what must be delivered.
2. **Work shape** - linear, integration-heavy, or open-ended.
3. **Artifacts** - what files or outputs prove progress.
4. **Roles** - only the specialists that materially reduce risk.

Use the decision matrix in [framework-selection.md](references/framework-selection.md).

### 2. Choose the coordination model

Pick exactly one primary model:

- **Sequential** - use for dependency chains like research -> design -> implementation -> review.
- **Hub-and-spoke** - use when one coordinator must integrate outputs from several workers.
- **Swarm** - use when exploration is open-ended and agents can safely work from a shared board.

Use one primary model unless the task clearly needs a hybrid.

### 2.5 Choose the execution substrate separately

Coordination model and execution substrate are not the same thing.

Pick the execution substrate that matches the job:

- **Plain child sessions** - use `agent__spawnSession(...)` for one-off delegation that does not need org visibility.
- **Explicit org lineage** - call `agent__prepareTeamworkWorkspace()` first, then use `agent__createOrg(...)` once from the root session, then use `agent__spawnSession(...)` for org-visible children. Under the explicit org root, org inheritance is automatic. Org-visible children inherit the governing session's effective workspace by default.
- **Scheduled task groups** - use `scheduled_task__createScheduledTask(...)` and the other `scheduled_task` tools for recurring, heartbeat, cron-like, or resumable automation loops.
- **Session-bound clock follow-ups** - use `loop` with `scheduled_task__scheduleCallback(...)` when a delay or reminder must stay inside the current conversation. This does not require teamwork scaffolding.
- **Completion wakes** - use `call-me-back` when the agent should resume on process exit, kanban/ticket status, or another external signal (not a clock).

Keep these separate:

- **Org** is for explicit lineage-based teamwork and org UX.
- **Org** keeps the normal parent workspace semantics; only the teamwork artifacts move out of the repo/workspace.
- **Scheduled task groups** are for global recurring automation and policy-governed background collaboration.
- **Session loops / schedules** are for in-conversation delays and session-scoped recurrence, not teamwork groups.
- A recurring task group may wake a coordinator session, but that does not make the scheduled group an org.

Before creating a new member for a later task, inspect `agent__listAgents(type="sessions")` and reuse an Idle child with the same assistant ID and compatible workspace through `agent__messageToSession`. Set `reset=true` only for a fresh assignment; create a new member when the role, workspace, or required parallel capacity differs.

### 2.6 Route to the specialist skill

After choosing the execution substrate, route to the matching specialist skill:

- **Plain child sessions** - stay here and use `delegate` when child-session mechanics matter.
- **Explicit org lineage** - switch to `org`.
- **Living org restructure** (add/layoff/merge roles, constitution edits) - switch to `org-restructure` after the org exists.
- **Postmortem → improve** (after-action learning, continuous org improvement) - switch to `postmortem-improve`.
- **Global scheduled tasks or groups** - switch to `schedule`.
- **In-session delays or session-bound recurrence** - switch to `loop`.
- **Wait for a job/ticket/webhook to finish** - switch to `call-me-back`.

`teamwork` decides and scaffolds. The specialist skill handles the execution-specific operating rules.

### 3. Create the workspace contract

Create the shared files in the app-local teamwork artifact directory first. At minimum create:

```text
./
├── agents.md
├── MISSION.md
├── ROLES.md
├── .libragent/
│   └── teamwork.json
├── skills/
│   └── {role-skill}/SKILL.md
├── docs/
└── coordination/
    ├── KANBAN.md
    ├── HANDOFF.md
    ├── DECISIONS.md
    ├── RISKS.md
    └── DISCUSSION.md
```

The scaffold must preserve:

- the original user request
- the teamwork objective
- the chosen collaboration framework
- the canonical file ownership and operating rules

The governing coordinator stays in its normal effective workspace after scaffolding. Only the teamwork artifacts live in the app-local artifact directory.

Use the file contracts in [coordination-contract.md](references/coordination-contract.md).

### 4. Create role skills only when they add durable value

Generate a workspace skill per role when the role needs persistent operating guidance across many turns or sessions. If the specialization is temporary and obvious, a session-specific prompt may be enough.

When you do create role skills, use [expert-skill-template.md](references/expert-skill-template.md) and customize:

- mission slice
- allowed tool families
- required inputs
- expected outputs
- handoff targets
- stop conditions

### 5. Enforce disciplined collaboration

Every specialist must follow this loop:

1. Read `agents.md`, `MISSION.md`, and `ROLES.md`.
2. Check `coordination/KANBAN.md` before starting.
3. Claim or update a task before doing meaningful work.
4. Write findings or status changes to the proper coordination file.
5. Leave a concrete handoff in `coordination/HANDOFF.md`.

Shared files are the coordination contract. Keep the loop explicit.

### 6. Handle persistence honestly

If global recurring execution is needed, switch to `schedule` and define the loops with the `scheduled_task` builtin tools. Use `scheduled_task__createScheduledTask(...)` for each global recurring task.

If the user only wants a delay or reminder inside the current conversation, switch to `loop` instead. That path uses `scheduled_task__scheduleCallback(...)` and does not require teamwork scaffolding. If they want to wake when a process or ticket completes, switch to `call-me-back`.

Refresh behavior:

- `agents.md` changes do **not** instantly rewrite the current session prompt
- new workspace skills apply in a later execution step, not retroactively in the same turn
After scaffolding or constitution edits, state when the updated rules become effective.

## Workspace Instructions (agents.md) & Persona (SOUL.md) Behavior

`agents.md` (operating constraints) and `SOUL.md` (persona/tone) are **workspace-scoped**. Each session resolves these instruction files from its effective workspace directory.

| Session Type | Effective Workspace | Instruction Source |
|-------------|---------------------|--------------------|
| Root session | Its own workspace | root workspace/`agents.md` & `SOUL.md` |
| Non-org child | Isolated (auto) | child's isolated workspace/`agents.md` & `SOUL.md` |
| Org child (default) | Shares org root workspace | org root workspace/`agents.md` & `SOUL.md` |
| Org child (with `workspaceOverride`) | Custom workspace | custom workspace/`agents.md` & `SOUL.md` |

> [!IMPORTANT]
> - **Shared Rules:** By default, org children share the exact same `agents.md` and `SOUL.md` as the org root. If you modify these files in the org root, they will apply to all child sessions in later steps.
> - **Rule Isolation:** If a specialist child session needs custom operating guidelines (e.g. frontend code conventions) or a unique persona, you must provide a `workspaceOverride` pointing to a directory that contains its own `agents.md` or `SOUL.md`.
> - **Fallback on Missing Files:** If a workspace directory (including override locations) does not contain `agents.md` or `SOUL.md`, the backend will load **no instructions** for that section without throwing errors. Ensure all required rules are scaffolded or copied to override directories.

## Tool Hygiene Rules

When you execute the scaffold:

1. Bootstrap in the app-local artifact directory returned by `agent__prepareTeamworkWorkspace()`.
2. Use portable commands and the available tools.
3. Match the editing primitive to the change size.
4. Use `workspaceOverride` only when a child must work in a different workspace.

## Design Rules

### Keep roles sharp

- Prefer roles with one dominant responsibility.
- Give each role a clear input and output contract.
- Avoid duplicate specialists with fuzzy boundaries.
- Add a coordinator only when integration or prioritization is a real problem.

### Keep artifacts explicit

Every role should update one primary artifact. Examples:

- Researcher -> `docs/RESEARCH.md`
- Architect -> `docs/ARCHITECTURE.md`
- Implementer -> `src/` + `coordination/HANDOFF.md`
- Reviewer -> `docs/REVIEW.md`

### Keep failure visible

Force the team to record:

- blocked tasks in `KANBAN.md`
- unresolved decisions in `DECISIONS.md`
- active risks in `RISKS.md`
- next-owner handoffs in `HANDOFF.md`

If the task force cannot surface blocked state, it is not robust.

## Bootstrap

Prefer deterministic scaffolding:

```bash
agent__prepareTeamworkWorkspace()
# -> returns artifactPath

python "<skill-base-dir>/scripts/init_task_force.py" \
  --output "/absolute/path/from/agent__prepareTeamworkWorkspace" \
  --team-name "Research Strike Team" \
  --objective "Build a reusable research and implementation team" \
  --request "Research the space, structure findings, and hand implementation-ready guidance to coding specialists." \
  --framework hub-and-spoke \
  --role "Coordinator:Own planning, prioritization, and integration" \
  --role "Researcher:Collect evidence and update docs/RESEARCH.md" \
  --role "Implementer:Turn approved plans into code and tests"
```

Use the app-local artifact path returned by `agent__prepareTeamworkWorkspace()` for `--output`. Do not default to `.` from a repo root.

Then review and tighten:

- `agents.md`
- `MISSION.md`
- `ROLES.md`
- `.libragent/teamwork.json`

The scaffold is the constitution. Tighten it before handing work to specialists.

## Quick Checks Before You Finish

Before announcing success, verify:

1. the chosen framework matches the task shape
2. the original user request is preserved in the scaffold
3. each role has a non-overlapping responsibility
4. `agents.md` tells agents exactly where to read and write
5. every important artifact has an owner
6. the handoff path between roles is obvious
7. the execution substrate and follow-up specialist skill are explicit: plain child sessions, `org`, or `schedule`
8. refresh semantics are written down so agents know that updated rules apply only in a later execution step
9. the governing session still uses the intended effective workspace, and only the teamwork artifacts live in app-local storage

## References

- [Framework selection matrix](references/framework-selection.md)
- [Coordination file contracts](references/coordination-contract.md)
- [Expert skill template](references/expert-skill-template.md)
