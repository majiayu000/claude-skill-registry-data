---
name: gap-driven-search
description: Use when a graph gap or Evidence Need should become a targeted paper-search contract or candidate lead list.
argument-hint: "<project> <gap-id>"
---

# Gap-Driven Search

Status: **transition**. Keep for graph-derived evidence discovery. Do not expose
as a core first-run workflow; future source/literature discovery should absorb
this path.

Build a search contract from a graph gap:

```bash
python3 "$PLUGIN_ROOT/tools/gap_search_cli.py" contract --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --target "$GAP_TARGET" --json
```

Run a small search:

```bash
python3 "$PLUGIN_ROOT/tools/gap_search_cli.py" search --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --target "$GAP_TARGET" --source memory --json
```

Generate a paper-discovery handoff:

```bash
python3 "$PLUGIN_ROOT/tools/gap_search_cli.py" handoff --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --target "$GAP_TARGET" --source memory --json
```

Do not approve papers, write Zotero records, or append graph events.
