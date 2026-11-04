---
name: grafana
description: Use Grafana MCPorter CLI for dashboards, Prometheus metrics, Pyroscope profiles, annotations, datasource health, and alerting investigations.
---

# Grafana

Run Grafana through Context Mode and its bounded runner.
Grafana currently uses MCPorter's typed-client fallback, so pass one JSON argument to each method:

```sh
node "$PI_CODING_AGENT_DIR/skills/grafana/scripts/run.mjs" help
node "$PI_CODING_AGENT_DIR/skills/grafana/scripts/run.mjs" search_dashboards '{"query":"service-name"}'
node "$PI_CODING_AGENT_DIR/skills/grafana/scripts/run.mjs" query_prometheus '{"datasourceUid":"<uid>","endTime":"now","expr":"up","startTime":"now-15m"}'
```

Use `help` to list generated methods and inspect `generated/grafana-client.d.ts` only when exact parameters are unknown.
Start with a named service, the shortest useful time window, and one signal.
Separate timestamps, scope, evidence, and time zone from hypotheses.
Treat alert-routing and alert-rule changes as mutations.
After confirmation of the exact action, set `MCP_WRITE_CONFIRMED=1` only for that runner process.

Refresh this generated client with `nix run .#update-mcp-skills -- grafana`, then run `nix run .#sync-agents`.
