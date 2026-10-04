---
name: project-gap-discovery
description: Use when the user wants papers to consider for a graph gap or missing evidence need.
argument-hint: "<project> <gap-id>"
---

# Project Gap Discovery

Status: **transition**. Keep as an agent/internal transition path for
graph-derived evidence discovery. Do not expose as a core first-run workflow;
future source/literature discovery should absorb this path.

Natural user intents this path may satisfy:

```text
Find papers that could address this project gap.
Look for sources for this missing evidence need.
```

Internal transition:

```text
graph gap -> evidence need -> search -> lead scoring -> human chooses deep-read
```

Run the agent-internal command:

```bash
python3 "$PLUGIN_ROOT/tools/research_gap_discovery_cli.py" run --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --gap "$GAP_TARGET" --source memory --json
```

Do not add papers to Zotero, approve candidates, or append graph events.
