---
name: project-experiment-proposal
description: Use when a Research Pilot project needs an experiment proposal from a weak or bounded project claim.
argument-hint: "<project> <claim-id>"
---

# Project Experiment Proposal

Status: **transition**. Keep for compatibility with existing graph-claim
proposal workflows. New product work should model project experiment design and
completed result evidence, not proposal-only artifacts.

Experiment proposals are planning artifacts, not graph evidence.

Generate an experiment proposal:

```bash
python3 "$PLUGIN_ROOT/tools/project_experiment_cli.py" suggest --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --target "$CLAIM_ID" --json
```

Optional artifact:

```bash
python3 "$PLUGIN_ROOT/tools/project_experiment_cli.py" suggest --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --target "$CLAIM_ID" --save-artifact --json
```

Do not append graph events or claim experiment results.
