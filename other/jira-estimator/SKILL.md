---
name: mk:jira-estimator
description: 'Heuristic story-point estimation for a single Jira ticket via the jira-estimator agent. Read-only. Triggers: ''estimate KEY'', ''story points for KEY'', ''how complex is KEY''. NOT for complexity-only analysis (mk:jira-evaluator); NOT for full RCA (mk:jira-analyst).'
phase: on-demand
source: local
keywords:
  - jira
  - jira-estimator
  - story-points
  - fibonacci-estimation
  - ticket-estimation
when_to_use: Use when user wants a heuristic story-point estimate for a single Jira ticket. Prior `mk:jira-evaluator` output enriches the estimate when present.
user-invocable: true
context: fork
agent: jira-estimator
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
---

# mk:jira-estimator

Forks to the `jira-estimator` agent. Read-only heuristic estimation. If a prior `mk:jira-evaluator` report exists at `tasks/reports/jira-evaluate-*-{KEY}.md`, the agent reads it and incorporates the complexity signals.

## Triggers

- "estimate PROJ-123"
- "story points for PROJ-123"
- "how complex is PROJ-123 in points?"

## Examples

- Cold estimate: "estimate PROJ-456 — give me a Fibonacci range and reasoning."
- Post-evaluate: "I just evaluated PROJ-456; now estimate it."

## See also

- Agent: `../../agents/jira-estimator.md`
- Shared: `../jira/references/{install-and-auth,cli-idioms,safety-framework,estimation-guide}.md`
- Domain refs (cross-link, lives under jira-time):
  - `../jira-time/references/estimation-guide.md` — story-point vs hours-based estimation tradeoffs
- Peer intelligence: `mk:jira-evaluator` (run first for complexity signals), `mk:jira-analyst` (full ticket synthesis)
- Peer execution: `mk:jira-issue` (`update --custom-fields '{"customfield_10016": N}'` writes the estimate), `mk:jira-fields` (discover instance-specific story-points field ID), `mk:planning-engine` (capacity analysis)

## Gotchas

- (none yet)
