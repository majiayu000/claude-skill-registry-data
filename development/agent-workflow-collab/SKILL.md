---
name: agent-workflow-collab
description: "Use for Crewrift-specific agent workflow collab recipes when optimizing a player."
---

# Agent workflow & collaboration — recipes (crewrift tier)

On-demand recipes (1). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Use the fixed crewrift agent roster; route param vs source-code changes correctly
`crewrift` · ⚠ _session-derived, unverified_

Use the fixed crewrift improvement-loop agent roster (orchestrator, debugger, analyst, reporter, exploiter, policy-improver, policy-engineer, skill-improver) and do not invent new agents. Route param-only changes to policy-improver; if a proposal needs source-code edits (not just config params), require policy-engineer to materialize the codeChangePlan in a workspace. Routing this wrong wastes a loop iteration.
  <sub>sources: claude-code:38ddef93-3214-489f-a178-33dddf030d9e, claude-code:f56285d5-42aa-49e2-92d5-844f590d7865</sub>
