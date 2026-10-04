---
name: sflow-workspaces
description: Show the complete saved-workspace table and active context; workspace selection belongs to /sf-workspace.
disable-model-invocation: true

---
# Show Singularity Flow workspaces

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Run only `singularity-flow workspace list --table`.
2. Relay the complete CLI table and its active context, warnings, and handoffs verbatim. Keep every row, including inactive workspaces. Do not replace the roster with a current-workspace summary, reorder it, or add Home headings.
3. Selection belongs to singular `/sf-workspace`, not `/sf-workspaces`. Preserve that exact CLI handoff; do not select a workspace in this read-only turn.
4. Do not run Home or a second current-context command. Do not create, clone, repair, archive, switch, or modify a workspace.
