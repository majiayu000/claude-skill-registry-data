---
name: sflow-push
description: Inspect or safely retry a preserved pre-Story transport intent without force-pushing or guessing remote state.
disable-model-invocation: true
argument-hint: "[status [INTENT-ID] | retry <INTENT-ID>]"
---

# Transport recovery

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

Use this skill when a workspace, capability, configuration, or initialization push was interrupted before a Story publication journal existed.

1. Run `singularity-flow push status --json`, or `singularity-flow push status <INTENT-ID> --json` when the user supplied an ID.
2. Explain the preserved local commit, exact target ref, attempt budget, and classified fault. Never request a token, disable TLS, bypass hooks, or suggest force.
3. Ask before mutation. When the user selects retry, run `singularity-flow push retry <INTENT-ID> --json` exactly once.
4. Report the returned status. `outcome-unknown` means stop: the remote could not be read, so another push is not authorized. `remote-diverged` or `needs-user` requires human reconciliation.

Story publication remains owned by `singularity-flow sync`; do not substitute this outbox for a Story pending-publication record.
