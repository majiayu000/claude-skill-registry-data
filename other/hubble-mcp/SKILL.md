---
name: hubble-mcp
description: Use Hubble MCPorter CLI to investigate Airflow DAGs and SYNQ entities, lineage, freshness, quality, executions, and incidents.
---

# Hubble MCP

Run the generated `hubble-mcp` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/hubble-mcp/scripts/run.mjs" synq-search-entities --help
node "$PI_CODING_AGENT_DIR/skills/hubble-mcp/scripts/run.mjs" synq-entity-health --help
node "$PI_CODING_AGENT_DIR/skills/hubble-mcp/scripts/run.mjs" airflow-dag-runs --help
```

Resolve the exact entity or DAG before requesting lineage, executions, task instances, quality, freshness, or incidents.
Bound lineage direction and depth, execution windows, and result counts.
Report identifiers, timestamps, environment, evidence, and time zone separately from hypotheses.
When Hubble OAuth is unavailable, authenticate with `npx --yes mcporter@0.13.3 --config "$MCPORTER_CONFIG" auth hubble-mcp`.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- hubble-mcp`, then run `nix run .#sync-agents`.
