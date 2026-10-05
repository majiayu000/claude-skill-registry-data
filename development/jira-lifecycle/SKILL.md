---
name: mk:jira-lifecycle
description: 'Drive JIRA workflow lifecycle via the jira-as wrapper: transition, assign, resolve, reopen, manage versions and components. Triggers: ''transition KEY to Status'', ''mark KEY as Done'', ''assign KEY to user'', ''reopen KEY'', ''release version'', ''create component''. NOT for issue CRUD (mk:jira-issue); NOT for bulk transitions (mk:jira-bulk).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-lifecycle
  - jira-transition
  - jira-assign
  - jira-resolve
  - jira-version
  - jira-component
when_to_use: Use to change a Jira issue's status, assignee, or resolution, or to manage project versions/components. NOT for bulk operations.
user-invocable: true
context: fork
agent: jira-lifecycle
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-lifecycle

Forks to the `jira-lifecycle` agent. `lifecycle transition` takes the issue key positional + a `--to "Status Name"` flag (or `--id <transition_id>`).

**Workflow discovery is mandatory** before suggesting transitions. The agent reads `tasks/jira-workflows/` (instance-discovered cache) and runs `bash $CLAUDE_PROJECT_DIR/.claude/skills/jira/scripts/fetch-workflow.sh <KEY>` if absent. See `references/workflow-discovery.md`. The `references/patterns/*.md` files are illustrative concepts only — they are NOT your project's actual workflow.

## Triggers

- "transition PROJ-123 to In Progress"
- "mark PROJ-123 as Done with resolution Fixed"
- "assign PROJ-123 to john.doe"
- "reopen PROJ-123"
- "release version v1.0.0 in PROJ"

## Examples

- Status change: "move PROJ-123 to In Review with comment 'ready for QA'"
- Resolution-required: "close PROJ-456 with resolution Won't Fix"
- Assignment: "assign all my open PROJ tickets to john.doe" (the agent will refuse — that's bulk; redirect to `mk:jira-bulk`)

## See also

- Agent: `../../agents/jira-lifecycle.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- **Authoritative source for THIS project's workflow** (discovered, not templated):
  - `references/workflow-discovery.md` — discovery + caching protocol (READ FIRST)
  - `tasks/jira-workflows/<workflow-slug>.md` — discovered workflow definitions
  - `tasks/jira-workflows/_schemes/<PROJECT_KEY>.md` — project → workflow mapping
  - Discovery script: `bash $CLAUDE_PROJECT_DIR/.claude/skills/jira/scripts/jira-as.sh ...` — wrapped by `fetch-workflow.sh`
- Domain refs:
  - `references/workflow-transitions.md` — common transition idioms + resolution-required patterns
- Educational concept patterns (illustrative shapes, **NOT authoritative for your instance** — always prefer the discovered cache above):
  - `references/patterns/standard-workflow.md` — basic 3-state lifecycle (concept)
  - `references/patterns/software-dev-workflow.md` — engineering-team flow (concept)
  - `references/patterns/jsm-request-workflow.md` — JSM ITIL flow (concept)
  - `references/patterns/incident-workflow.md` — incident handling (concept)
- Peer leaves: `mk:jira-bulk` (bulk transition; reads same workflow cache), `mk:jira-jsm` (JSM-specific transitions), `mk:jira-collaborate` (transition `--comment` body templates)

## Gotchas

- (none yet — grow from observed failures)
