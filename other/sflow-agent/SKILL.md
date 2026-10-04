---
name: sflow-agent
description: Choose or inspect the governed Agent Markdown used for the current phase; agent selection never changes human identity or approval authority.
disable-model-invocation: true
argument-hint: "[WORK-ID]"

---

# Select the governed agent

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow agent <WORK-ID>`; omit the ID when the current branch already identifies it.
2. The phase default is automatic. Only ask the contributor when more than one compatible agent is available or they explicitly request a change.
3. When a picker is required, present every displayed label, ID, and description. Never infer human identity or approval authority from the agent.
4. Run `singularity-flow session status --json`, then report the agent, source hash, phase compatibility, work-item scope, and Copilot-session binding.
5. Agent Markdown controls prompt instructions and world-model views. Git/Jira identity and configured approval groups control human decisions.
