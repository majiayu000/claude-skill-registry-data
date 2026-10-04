---
name: project-gap-analysis
description: Use when a Research Pilot project needs read-only gap detection or Evidence Need extraction from the Project Understanding Graph.
argument-hint: "<project>"
---

# Project Gap Analysis

Status: **advanced**. Keep for graph rigor and evidence-gap inspection. Do not
present as a normal first-run product concept.

Detect structural gaps:

```bash
python3 "$PLUGIN_ROOT/tools/project_gap_cli.py" detect --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --json
```

Optional cap:

```bash
python3 "$PLUGIN_ROOT/tools/project_gap_cli.py" detect --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --limit 10 --json
```

Do not mutate graph, Zotero, dossiers, or dashboard state. If a gap becomes an update, route it through `delta-update-protocol`.
