---
name: ticket-brief
description: >
  Fetch a ClickUp/Linear/GitHub ticket URL, summarize into a
  work-brief: goal, acceptance criteria, blast radius, suggested branch name,
  suggested commit prefix, related repos.

  Trigger this skill when:
  - User pastes a `*.clickup.com/t/…` URL.
  - User pastes a `linear.app/…/issue/…` URL.
  - User pastes a `github.com/*/issues/…` or `pull/…` URL.
  - User says "brief this ticket", "summarize this issue", or invokes
    `/ticket-brief`.
---

## Prerequisite

- **ClickUp**: `mcp__clickup__*` tools available via ClickUp MCP.
- **GitHub**: `gh` CLI authenticated.
- **Linear**: Linear MCP if configured (fall back to WebFetch if not).

Check with `ToolSearch`. If the source is unreachable, tell the user which
MCP/tool needs setup.

## Behavior

1. **Detect source** from URL pattern.
2. **Fetch**:
   - ClickUp: `mcp__clickup__clickup_get_task(task_id=…, include=["description"])`.
   - GitHub: `gh issue view <url> --json title,body,labels,assignees,state`.
   - Linear: Linear MCP fetch.
3. **Distill** into a brief with these sections:
   - **Goal** (one sentence, imperative).
   - **Why** (business/technical reason if stated).
   - **Owner** + deadline if stated.
   - **Acceptance criteria** (checklist, pulled from ticket body).
   - **Blast radius**: which repos, which subprojects, which files.
   - **Branch name**: the ClickUp-generated branch name — see
     [Branch naming](#branch-naming) below. Do **not** invent a `feat/<slug>`.
   - **Suggested commit prefix**: `<type>(<scope>): …`.
   - **Dependencies / blockers** if any.
   - **Ticket URL** at the end.
4. **Format** as a compact Markdown brief, ≤ 30 lines.

## Branch naming

When starting work on a ClickUp task, **use the branch name ClickUp generates** —
do not hand-roll a `feat/<slug>`. This keeps ClickUp's GitHub integration able to
auto-link commits, branches, and PRs back to the task.

- Each task exposes **Create branch** / **Copy branch name** via the ClickUp
  GitHub integration. The Nimbus format is `CU-<taskid>_<slug>`
  (e.g. `CU-86agn85vm_Hector-Duran`). The exact template is set in ClickUp →
  Settings → Integrations → GitHub.
- If the ClickUp UI isn't handy, reconstruct it from the task id returned by
  `clickup_get_task` — the id in the `*.clickup.com/t/<id>` URL — as
  `CU-<id>_<short-slug>`.
- Cut the branch off the repo's default base (`dev` for `cidca-platform` /
  `cidca-services`) unless the ticket says otherwise.
- This overrides the generic `feat/fix/chore` branch guidance in the
  `conventional-commit` skill for any ClickUp-tracked work. Commit *message*
  prefixes still follow conventional-commit.

## Status transitions

Once the user confirms scope and work starts, **the agent owns the ticket's
status** and moves it forward as work progresses — do not wait to be told.

- **Start of work** → move the task to `In Progress` (or the workspace's
  equivalent active status) via
  `mcp__clickup__clickup_update_task(task_id=…, status="in progress")`.
- **PRs opened / awaiting review** → move to `In Review` (or equivalent).
- **All relevant PRs merged** → move the task to `Done` (or the workspace's
  final/closed status). "All relevant PRs" = every PR opened for this ticket
  and its subtasks; if any is still open or in draft, the ticket stays in
  `In Review`, not `Done`.
- Read the list's real status names first (`clickup_get_list` /
  `clickup_get_task` returns the current status set) — don't assume a status
  string exists; map to the closest active / review / closed status.
- If a status transition fails (permissions, unknown status), tell the user
  which move failed rather than silently continuing.

## Subtask budget

The agent may decompose work into subtasks, but is **bounded**:

- **At most 1 parent ticket + 5 subtasks.** Never exceed 5 subtasks per
  ticket. If the work needs more than 5, stop and ask the user to re-scope
  rather than spawning a 6th.
- Create subtasks with
  `mcp__clickup__clickup_create_task(parent=<ticket_id>, …)` to address
  distinct sub-pieces (per-repo work, per-subproject, cleanup, follow-ups).
- **PRs are unbounded** — open as many as the work warrants. The 1+5 cap is on
  *tickets/subtasks only*, not PRs. Multiple PRs can map to one subtask.
- Apply the same status-transition rule to subtasks: move each subtask through
  `In Progress` → `In Review` → `Done` as its own PRs land. The parent ticket
  only reaches `Done` when every subtask and every relevant PR is merged.

## Nimbus-specific inferences

- Ticket mentions `ecg-ui/…` or React component → frontend PR in cidca-platform.
- Ticket mentions `ecg-*-lambda` → cidca-services repo, specific lambda dir.
- Ticket titled `[FERIA] …` → part of the July 8 event sprint (ClickUp list `Sprint 36`).
- Ticket mentions `Reporte v1 CIDCore` → touches `HTMLReportTemplate` row seed
  + `ecg-gw-parsescp-lambda/view_ecg.py` (see samples in cidca-platform if
  present).

## Do not

- Assume you can auto-implement from the brief — always confirm scope with user first.
- Include the full ticket body — you're distilling, not copying.
- Include secrets that appear in the ticket body (Vercel URLs with tokens, etc.).
- Add freeform comments to the ticket unless the user asks — but status
  transitions and the 1+5 subtask budget are agent-owned once work starts
  (see [Status transitions](#status-transitions) / [Subtask budget](#subtask-budget)).
- Exceed 1 ticket + 5 subtasks. Re-scope with the user instead of a 6th subtask.

## Follow-up

After presenting the brief, ask the user: `Start on this? (branch name / next
step)`. Let them choose whether to proceed or defer.
