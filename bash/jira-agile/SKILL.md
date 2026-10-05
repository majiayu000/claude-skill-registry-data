---
name: mk:jira-agile
description: 'JIRA agile via the jira-as wrapper: epics, sprints, backlog, ranking, story points, subtasks, velocity. Triggers: ''create sprint'', ''add KEY to sprint'', ''set story points on KEY'', ''rank KEY before KEY'', ''velocity for board'', ''epic add''. Board ID ≠ project key. NOT for issue CRUD (mk:jira-issue); NOT for time tracking (mk:jira-time).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-agile
  - jira-sprint
  - jira-epic
  - jira-backlog
  - story-points
  - velocity
when_to_use: Use to manage epics, sprints, backlog, ranking, story-point estimates, subtasks, or velocity reports. NOT for individual issue CRUD.
user-invocable: true
context: fork
agent: jira-agile
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-agile

Forks to the `jira-agile` agent. Sprint operations require a numeric `--board-id`, not the project key. The agent resolves project name → board ID via `agile board list --name "..."` first.

## Triggers

- "list sprints on board 'Team Alpha'"
- "add PROJ-123, PROJ-124 to sprint 42"
- "set 5 story points on PROJ-123"
- "rank PROJ-123 before PROJ-456 in backlog"
- "velocity for board 42"
- "create epic 'Auth Rewrite' in PROJ"

## Examples

- Sprint create: "create sprint 'Sprint 21' on board 'Team Alpha' from 2026-05-13 to 2026-05-27"
- Epic populate: "add PROJ-123, PROJ-124, PROJ-125 to epic EPIC-1"
- Subtask: "create subtask of PROJ-123 — 'write integration test'"

## Sprint commitment hooks (Agile-context-only — gated by `agile-sprint-commitment.md` 2/3 when loaded)

When `tasks/contracts/sprint-state-{date}-sprint-{N}.md` exists with `status: active`, wrap these operations:

### `sprint add KEY` and `sprint remove KEY` (post-start)

1. Read newest sprint-state file matching the active sprint
2. **Acquire `flock` on the sprint-state file before any read-modify-write.** YAML frontmatter append is non-atomic across shells; lock is the only mitigation
3. Per `agile-sprint-commitment.md` 2: `AskUserQuestion` "Reason for mid-sprint scope change?" — required free-text
4. Append `{ ts: <ISO ts>, action: add|remove, ticket: KEY, reason: <text> }` to `amendments:` list
5. Release lock
6. Proceed with the underlying `jira-as agile sprint add|remove` call

If sprint-state contract is absent OR `status: closed` → skip the amendment ceremony silently.

### `sprint close`

1. Read `committed_tickets:` from newest active sprint-state
2. Query each via `mk:jira-issue get KEY`
3. For each non-terminal ticket (not Done/Cancelled/Won't-Do), `AskUserQuestion`: "PROJ-X is in {status}. Carry over to next sprint? Drop? Mark as not delivered?"
4. Write closure summary: `status: closed`, `closed_at: <ts>`, `delivered: [...]`, `carried_over: [...]`
5. Proceed with the underlying `jira-as agile sprint close` call

### Validator scope (sprint-state vs sprint-contract)

`mk:sprint-contract/scripts/validate-contract.sh` validates per-story sprint-CONTRACT files only (those with `contract_schema_version`, `### [AC-N]` entries). Sprint-STATE files at `sprint-state-{date}-sprint-{N}.md` use NO validator — YAML is parsed inline by this skill, `mk:agent-detector`, and `mk:sprint-contract sprint-goal`. Do not invoke `validate-contract.sh` on a sprint-state path; it WILL fail (sprint-state lacks contract schema fields by design).

### Glob-collision safety verified

| Script | Mechanism | Verdict |
|---|---|---|
| `check-contract-signed.sh` | Globs `tasks/contracts/*-"$slug"-sprint-*.md` (per-task slug between leading `*` and `-sprint-`) | SAFE — sprint-state files have no slug between leading `sprint-state-` prefix and `-sprint-` |
| `validate-contract.sh` | Takes single explicit `$1` path; no glob | SAFE |

## See also

- Agent: `../../agents/jira-agile.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Domain refs:
  - `references/sprint-operations.md` — board/sprint/velocity wrapper patterns
  - `references/agile-field-reference.md` — agile-specific field IDs (Sprint, Epic Link, Story Points)
- Peer leaves: `mk:jira-fields` (`../jira-fields/references/agile-field-ids.md` is the canonical instance-discovery source), `mk:jira-time` (capacity = velocity ÷ team time), `mk:jira-relationships` (epic-children outside epic-link via issue links)

## Gotchas

- (none yet — grow from observed failures)
