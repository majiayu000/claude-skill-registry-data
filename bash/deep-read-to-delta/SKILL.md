---
name: deep-read-to-delta
description: Use when a project-local paper dossier should produce graph delta JSON proposals and run through the human-gated delta loop.
argument-hint: "<dossier> <project>"
---

# Deep Read To Delta

Validate a paper dossier:

```bash
python3 "$PLUGIN_ROOT/tools/paper_dossier_cli.py" validate --dossier "$DOSSIER" --json
```

Export delta JSON proposals:

```bash
python3 "$PLUGIN_ROOT/tools/paper_dossier_cli.py" export-deltas --dossier "$DOSSIER" --output-dir "$WORKSPACE_PATH/.research-pilot/generated/deltas" --json
```

Dry-run exported deltas:

```bash
python3 "$PLUGIN_ROOT/tools/graph_delta_cli.py" dry-run --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --delta "$DELTA_JSON" --json
```

Register valid deltas only after dry-run passes:

```bash
python3 "$PLUGIN_ROOT/tools/graph_delta_cli.py" register --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --delta "$DELTA_JSON" --json
```

Apply a decision only after explicit human approval, rejection, parking, or revision request.
