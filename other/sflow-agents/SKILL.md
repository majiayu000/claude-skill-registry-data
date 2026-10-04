---
name: sflow-agents
description: Inspect governed Agent Markdown, mappings, and hash-pinned remote Markdown dependencies; agents are instructions, never human approval authorities.
disable-model-invocation: true

---

# Manage governed agents

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

- Discover: `singularity-flow agents list`.
- Inspect Copilot-agent routing: `singularity-flow agents mappings`.
- Inspect: `singularity-flow agents status [AGENT]`.
- First trust: `singularity-flow agents lock <AGENT>`.
- Review an update: `singularity-flow agents lock <AGENT> --update`.
- Materialize locked content: `singularity-flow agents sync <AGENT>`.
- Refresh generated Markdown: `singularity-flow agents refresh-output <RESOURCE-ID> [--replace]`.

First trust and updates require exact agent-name confirmation. Never edit `singularity/agents.lock.yml` manually, bypass a changed hash, send credentials, or overwrite local output unless the user explicitly requests `--replace`.

An agent combines its own instructions and world-model view declarations with optional remote Markdown dependencies. It cannot act as a human or approve/reject lifecycle state.

Copilot custom-agent IDs may map to different governed-agent IDs in `singularity/agent-mappings.yml`. Explicit mappings win; omitted agents use same-name fallback.
