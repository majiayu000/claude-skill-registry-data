---
name: delta-update-protocol
description: Use when a Research Pilot project graph change must be previewed, registered, accepted, rejected, parked, or revised through human-gated D* deltas.
argument-hint: "<project> <delta-json|delta-id>"
---

# Delta Update Protocol

All Q/C/E/W/L/RL/TL changes go through D* deltas.

Preview:

```bash
python3 "$PLUGIN_ROOT/tools/graph_delta_cli.py" dry-run --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --delta "$DELTA_JSON" --json
```

Register:

```bash
python3 "$PLUGIN_ROOT/tools/graph_delta_cli.py" register --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --delta "$DELTA_JSON" --json
```

First graph bootstrap:

If the project is only a shell and has no `wiki/graphs/graph.db`, dry-run/register can still work for first deltas that create nodes, or create links whose endpoints are created in the same delta. Update ops still require existing graph state.

Apply explicit human decision:

```bash
python3 "$PLUGIN_ROOT/tools/graph_delta_cli.py" decide --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --id "$DELTA_ID" --decision accept --json
```

Never accept, reject, park, or revise without explicit human instruction.
