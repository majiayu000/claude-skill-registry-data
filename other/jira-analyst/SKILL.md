---
name: mk:jira-analyst
description: 'Full Jira ticket context analysis via the jira-analyst agent — including media (attached images / PDFs / screenshots) and linked issues. Produces structured findings suitable for posting back as a Jira comment. Read-only. Triggers: ''analyze KEY'', ''rca for KEY'', ''describe KEY with media''. NOT for complexity scoring (mk:jira-evaluator); NOT for story-point estimation (mk:jira-estimator).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-analyst
  - ticket-analysis
  - ticket-rca
  - media-analysis
  - attachment-analysis
when_to_use: Use when user wants full ticket context (description + comments + attachments + links + media analysis) consolidated into a structured report. Read-only — user reviews before posting back.
user-invocable: true
context: fork
agent: jira-analyst
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-analyst

Forks to the `jira-analyst` agent. Read-only. The agent has Write tool privilege ONLY for persisting the report to `tasks/reports/jira-analyze-*.md` — it never writes to Jira itself.

## Triggers

- "analyze PROJ-123"
- "rca for PROJ-123"
- "describe PROJ-123 including the screenshots"

## Examples

- Standalone: "analyze PROJ-456 — what is this ticket about?"
- With investigation: "I investigated and found <findings>; now analyze PROJ-456 with full RCA"
- Media-heavy: "PROJ-789 has 3 screenshots — analyze them and synthesize"

## See also

- Agent: `../../agents/jira-analyst.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework}.md`
- Peer intelligence: `mk:jira-evaluator` (complexity signals), `mk:jira-estimator` (point estimate)
- Peer execution: `mk:jira-issue` (read ticket fields incl. attachments), `mk:jira-collaborate` (post analysis as comment — see `mk:jira-collaborate/references/comment-templates.md`)
- Output: report at `tasks/reports/jira-analyze-*.md` consumable by `mk:planning-engine` and downstream skills.

## Gotchas

- (none yet)
