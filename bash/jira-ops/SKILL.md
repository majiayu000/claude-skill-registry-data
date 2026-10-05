---
name: mk:jira-ops
description: 'JIRA-side cache + project-context discovery via the jira-as wrapper. Triggers: ''jira cache status'', ''clear jira cache'', ''discover project context for PROJ''. Diagnostic-only — no Atlassian state changes. NOT for issue CRUD; NOT for project admin (mk:jira-admin).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-ops
  - jira-cache
  - jira-discover
  - jira-diagnostic
when_to_use: Use to inspect / clear the jira-as local cache or discover project context (default issue types, mandatory fields). NOT for project admin (use mk:jira-admin).
user-invocable: true
context: fork
agent: jira-ops
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-ops

Forks to the `jira-ops` agent. Diagnostic surface only.

## Triggers

- "jira cache status"
- "clear jira cache"
- "discover project context for PROJ"

## Examples

- Cache check: "is the jira-as cache fresh?"
- Cache clear: "clear the cache, my admin renamed a status"
- Discovery: "what's the default issue type and mandatory field set for PROJ?"

## Power-User Note

`cache-warm` is intentionally NOT exposed as a primary trigger. If a user explicitly needs it, they can invoke directly:

```bash
bash $CLAUDE_PROJECT_DIR/.claude/skills/jira/scripts/jira-as.sh ops cache-warm --project PROJ
```

## See also

- Agent: `../../agents/jira-ops.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Domain refs:
  - `references/rate-limits.md` — Atlassian rate-limit ceilings + back-off behaviour
- Peer leaves: any leaf hitting Atlassian-side throttling first lands here for diagnosis. `mk:jira-bulk` is the most common trigger for cache-warm + rate-limit awareness.

## Gotchas

- (none yet)
