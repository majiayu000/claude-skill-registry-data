---
name: orc-sdlc
description: "Assess and execute engineering work on ORC-backed projects: choose proportional planning, implementation, debugging, validation and review. Preserve an assigned flow's role and outcomes. Excludes product setup and administration."
---

# Choose the process that completes the task

Read repository instructions and the current handoff. Check the installed `spec`
CLI bridge and its registered specs before declaring ORC unavailable. Use a registered
ORC spec, or `--mcp-http <selected ORC URL>/mcp` / an existing secure stdio launcher;
per-agent MCP configuration is not required. An already connected MCP tool is also
supported. Select the readable project name and call `context` first, then fetch
the effective `orc-sdlc` with `skill_read` through that interface. Read relevant
knowledge, not every document. Inspect the actual code/artifact before asking
questions that it can answer. Report a connection gap only after checking the
available bridge and direct connection; preserve scope and never use stale guidance.
User scope, authorization and project requirements govern the process.

Start with the core problem: who needs what outcome, how the current path works,
and what evidence would prove it improved. Trace the affected flow and reuse what
already fits before choosing new code. For nontrivial or uncertain work, choose a
task kind and effort level using [Planning](references/planning.md). Clear bounded
edits can use the direct route below; size alone does not choose the process.
Use the least machinery that completes the outcome safely. Reassess the route when
new evidence changes scope, risk or dependencies.

## Complete the development cycle

Context/recall -> extract requirements -> classify -> plan if needed -> implement
-> test and validate completeness -> review/rework -> authorized Git delivery.
These are checkpoints, not mandatory separate tasks or agents. Advance when the
current checkpoint has enough evidence; do not substitute a plan, green tests or
a review summary for the requested completed outcome.
For investigation-only work, the completed artifact is the cited answer. Git
delivery applies to changed artifacts within existing authorization; publishing
requires its own authorization.

- Requirements: outcome, observable examples/criteria, constraints, exclusions,
  dependencies and consequential open decisions are understood. Use grill-me-style
  questioning only for unresolved choices: one question, recommendation, then wait.
- Classify by uncertainty, connected boundaries, impact and reversibility. Direct
  execution is for clear, low-risk work. Small auth/data/API changes can be high risk.
- Plan when choices, dependencies, migration or failure consequences need a shared
  approach; map steps and validation to criteria before dependent implementation.
- Implement the complete change using the project's patterns and security boundaries.
- Verify each original criterion against actual behavior and evidence, then review
  the final artifact. Rework returns to implementation and affected revalidation.
- Deliver the reviewed result through Git within authorization; identify the actual
  commit/PR and any unimplemented or unverified work. Never label that work complete.

## Assess and route

| Situation | Approach and reference |
| --- | --- |
| Clear, bounded, low-risk change | Execute directly, validate affected behavior; [Development](references/development.md) |
| Outcome unclear or consequential design choices | Explore first, then ask one focused question with a recommendation; [Planning](references/planning.md) |
| Reported failure | Reproduce and state root cause before fixing; debugging section in [Development](references/development.md) |
| Broad/cross-boundary work | Record a concise plan and useful milestones; [Planning](references/planning.md), then development |
| High-impact auth, storage, compatibility or rollout change | Assess failure/migration/recovery and validation first; planning, then development even if the patch is small |
| Review existing work | Evaluate the actual artifact independently; review section in [Review and delivery](references/review-and-delivery.md) |
| Assigned managed node | Keep its task/session/checkout, role, declared outcomes and flow; load only its relevant reference |
| Rework or resume | Refresh feedback and effective guidance; preserve prior valid evidence and recheck changed behavior |

After compaction restore the supplied ORC session with `session_restore`, then
refresh the task, feedback, effective skills and relevant knowledge. Do not invent
an ORC session when none exists; use the existing repository handoff instead.

An engineering request alone does not require a managed flow, decomposition or
another agent. When coordination/review is warranted, inspect effective flows:
`orc-default` for development with its configured agent-review preference,
`orc-human-review` for independent review plus human signoff, `orc-review-only`
for an existing artifact. Follow project requirements and assigned flows; never
start duplicate agents or replace a missing flow silently. Delegation requires
user/project authorization. A worker cannot perform its own independent review.

Use `orc-platform` only when ORC operation details are needed. Select references
on demand; do not preload all playbooks. During work, preserve scope and unrelated
changes, record meaningful decisions/progress, and verify the actual acceptance
criteria. Before delivery or a flow outcome, follow the delivery section of
[Review and delivery](references/review-and-delivery.md).

Learning accompanies the cycle: recall relevant project memories and cited KB
lessons before decisions; record meaningful task/session evidence during work;
reconcile short durable facts and verified KB lessons at review/delivery. Reuse
what the previous agent recorded, not only your native chat history. For memory,
Learnings KB/digest operation and cross-agent scope use the relevant platform
reference. A normal worker does not call `digest_complete` or schedule another agent
as a side effect of learning; that completion token belongs to an assigned digest run.

For managed nodes the graph owns task status. Report exactly one declared outcome
with evidence, then stop; do not run the next node yourself. Outside a flow, deliver
the result and use only the agreed manual task lifecycle. Completion/review does
not authorize publishing, merging, deployment or live installation changes.
