---
name: mk:jira-search
description: 'JIRA search + filter management via the jira-as wrapper. Triggers: ''search jira'', ''find issues where X'', ''jql for ...'', ''export search results'', ''manage saved filters''. JQL injection-safe via the shared sanitizer. NOT for single-issue CRUD (mk:jira-issue); NOT for bulk write ops (mk:jira-bulk).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-search
  - jql
  - jql-query
  - jira-filter
  - jira-export
when_to_use: Use to find Jira issues by JQL, validate JQL, build queries from natural language, manage saved filters, or export results. NOT for single-issue CRUD.
user-invocable: true
context: fork
agent: jira-search
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-search

Forks to the `jira-search` agent. JQL is positional on `search query` and `search validate`; flags everywhere else. The agent enforces JQL sanitization for any user-derived term via `../jira/scripts/jql-sanitize.sh`.

## Triggers

- "search jira for ..."
- "find issues where assignee = me and sprint is open"
- "build a jql for ..."
- "export the search to /tmp/out.csv"
- "list / create / update / delete a saved filter"

## Examples

- "find unresolved bugs in PROJ created in the last 7 days, top 20"
- "validate this jql: project = PROJ AND status = 'In Progress'"
- "save a filter named 'My open bugs' with this jql: ..."

## See also

- Agent: `../../agents/jira-search.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Domain refs:
  - `references/jql-patterns.md` — canonical JQL templates (curated)
  - `references/jql-reference.md` — full JQL operator + function reference
  - `references/search-examples.md` — practical query examples per scenario
- Peer leaves: `mk:jira-bulk` (write-side bulk by JQL — same dry-run discipline), `mk:jira-time` (time-related JQL → see `mk:jira-time/references/jql-snippets.md`)

## Gotchas

- (none yet — grow from observed failures)
