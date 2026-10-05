---
name: mk:jira-jsm
description: 'JIRA Service Management via the jira-as wrapper: service desks, request types, requests, customers, organizations, queues, SLAs, approvals (8 sub-domains). Triggers: ''create JSM request'', ''list service desks'', ''SLA status for KEY'', ''approve request KEY'', ''list queue NAME''. Requires JSM-licensed tenant + agent role. NOT for core Jira issue ops (mk:jira-issue); NOT for project admin (mk:jira-admin).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-jsm
  - service-management
  - service-desk
  - sla
  - jira-customer
  - jira-queue
  - jira-approval
when_to_use: Use for any JIRA Service Management operation — service desks, requests, queues, SLAs, customers, organizations, approvals. Requires JSM license + agent role.
user-invocable: true
context: fork
agent: jira-jsm
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-jsm

Forks to the `jira-jsm` agent. Service Management (JSM) operations — service desks, requests, SLAs, customers, organizations, queues, approvals, request types.

## Triggers

- "create JSM request in service desk 'IT Support'"
- "list service desks"
- "SLA status for KEY-123"
- "approve request KEY-123"
- "list queue 'Tier 1 Support'"
- "add comment to JSM request KEY-123" (agent will confirm internal vs public)

## Examples

- Get service desk status: "show me the queues for service desk 'IT Support'"
- Customer-facing comment: "add public comment to KEY-123: '<message>'" → agent confirms internal-vs-public per safety-framework.

## Required Permissions

JSM-licensed tenant + agent or admin role. Insufficient permission → exit code 3.

## Limitations

- 8 sub-domains, ~45 verbs total — see `jira-as jsm <sub-domain> --help` for the authoritative flag list.
- Internal-vs-public comments are a privacy concern; the agent enforces explicit confirmation before posting customer-facing content.

## See also

- Agent: `../../agents/jira-jsm.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Domain refs:
  - `references/decision-tree.md` — when to use `mk:jira-jsm` vs `mk:jira-{issue,lifecycle,collaborate}` etc.
  - `references/itil-workflows.md` — ITIL 4 process implementations (incident / service-request / problem / change management)
- Peer leaves: `mk:jira-collaborate` (internal-vs-public discipline applies on JSM tickets too), `mk:jira-lifecycle` (`patterns/jsm-request-workflow.md`), `mk:jira-admin` (request-type / queue config)

## Gotchas

- (none yet)
