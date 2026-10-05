---
name: mk:jira-admin
description: 'JIRA project / user / group / scheme / automation administration via the jira-as wrapper (11 sub-domains, ~65 verbs). Triggers: ''create JIRA project'', ''list users'', ''delete user USERNAME'', ''list permission schemes'', ''create group NAME''. Requires admin role. Destructive ops (project/user/group delete) require 2-step token confirmation. NOT for per-issue ops (mk:jira-issue / mk:jira-lifecycle); NOT for JSM admin (mk:jira-jsm).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-admin
  - project-admin
  - user-admin
  - group-admin
  - permission-scheme
  - jira-automation
when_to_use: Use for Jira admin tasks — projects, users, groups, schemes, automation. Requires admin role. Destructive ops need 2-step token confirmation.
user-invocable: true
context: fork
agent: jira-admin
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-admin

Forks to the `jira-admin` agent. Highest-blast-radius leaf in the family.

## Triggers

- "create JIRA project"
- "list users"
- "delete user USERNAME"
- "list permission schemes"
- "create group NAME"
- "enable automation rule X on PROJ"

## Examples

- Project create: "create project KEY 'Project Name' as Software-Scrum"
- Project delete (DESTRUCTIVE): "delete project STAGING" → agent enforces 2-step token confirmation: human types literal project key to confirm.
- User deactivate: "deactivate user alice@..." (preferred over delete — preserves attribution)

## Required Permissions

Admin role. Insufficient permission → exit code 3.

## DESTRUCTIVE Operations

- `project delete` — IRREVERSIBLE
- `user delete` — IRREVERSIBLE (use `deactivate` instead when possible)
- `group delete` with members — affects member access globally

The agent enforces 2-step token confirmation for these. The skill triggers them via natural language; the agent never auto-executes without explicit human-typed confirmation.

## Limitations

- 11 sub-domains, ~65 verbs total — see `jira-as admin <sub-domain> --help` for the authoritative flag list.

## See also

- Agent: `../../agents/jira-admin.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Domain refs:
  - `references/voodoo-constants.md` — magic numbers (event IDs, scheme IDs, common custom field IDs) and how to discover yours
- Peer leaves: `mk:jira-fields` (field admin overlap; `fields create` requires admin), `mk:jira-jsm` (JSM-specific admin lives in jira-jsm). Most users invoke `mk:jira-admin` once per project setup, then never again.

## Gotchas

- (none yet)
