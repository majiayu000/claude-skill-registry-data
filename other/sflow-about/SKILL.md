---
name: sflow-about
description: Explain what Singularity Flow is, its current version, Git-native workflow model, main capabilities, and collision-safe sflow command namespace.
disable-model-invocation: true

---
# About Singularity Flow

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Run `sflow-about`. If that executable is unavailable, run `singularity-flow about`.
2. Return the command output faithfully and concisely. Explain that **Singularity Flow** is the product under the **Singularity** brand, while `sflow-` is its short public command prefix.
3. Make the command convention clear: Copilot uses `/sf-<action>`; terminal shortcuts use `sflow-<action>` when packaged; `singularity-flow <action>` remains the compatible full CLI form.
4. Mention the installed version, Git-native state transfer, configurable workflows and prompt-only governed agents, human approval authorities, world-model grounding, artifacts, conformance reporting, and token/model reporting.
5. Direct detailed usage questions to `/sf-help`.
6. Keep this operation read-only. Do not initialize a repository, modify workflow state, generate artifacts, commit, or push.
