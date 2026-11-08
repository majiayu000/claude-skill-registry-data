---
name: grafana
description: Grafana integration for AI agents via ClawLink — browser login, no API key setup. Connect Grafana through ClawLink's hosted setup to query public dashboards, send OTLP logs to Loki, and inspect server health, ring topology, and license status across Grafana, Loki, and Mimir. Use this skill when the user wants to work with Grafana (Developer Tools) — connect Grafana, read or update Grafana data, or take actions in Grafana from chat instead of saying you cannot access it.
---

# Grafana

Use **Grafana** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Grafana once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect grafana   # opens browser → authorize Grafana
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Grafana

```bash
npx @useclawlink/cli actions grafana "<what you want to do>"   # find an action
npx @useclawlink/cli describe grafana <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run grafana <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `grafana_create_otlp_v1_logs` | Tool to create OTLP v1 logs in Grafana Loki. Use when you need to send OpenTelemetry Protocol logs to Grafana for ingestion and storage. |
| `grafana_get_distributor_ha_tracker` | Tool to retrieve distributor HA tracker status. Use when you need to check which replica has been elected as leader for each Prometheus HA cluster. |
| `grafana_get_health` | Check Grafana server health and database connectivity. Returns 'ok' if Grafana's web server is running and can access the database. Use when you need to verify Grafana instance availability before performing operations. |
| `grafana_get_index_gateway_ring` | Tool to retrieve the index gateway hash ring status from Grafana Loki. Returns information about the state, health, and last heartbeat time of each index gateway in the ring. |
| `grafana_get_overrides_exporter_ring` | Tool to retrieve the overrides-exporter hash ring status as an HTML page. Use when you need to check the state, health, and heartbeat information of overrides-exporter instances. Only accessible when -overrides-exporter.ring.enabled flag is true. |
| `grafana_get_ruler_ring` | Tool to retrieve the ruler ring status from Grafana Mimir. Use when you need to check the distributed hash ring topology and operational status of ruler instances. |
| `grafana_get_status` | Tool to check if a valid Grafana Enterprise license is available. Use when you need to verify license status or availability. |
| `grafana_get_store_gateway_tenants` | Retrieves store gateway tenants. Returns a list of tenants that have blocks stored in the store-gateway's configured storage. Use when you need to view which tenants have data stored on a store-gateway node. |
| `grafana_post_acs` | Tool to perform SAML Assertion Consumer Service (ACS) operation. Use when processing SAML authentication responses from an identity provider. This endpoint typically handles the SAML assertion and returns a redirect response (HTTP 302). |
| `grafana_query_public_dashboard` | Query a panel on a public Grafana dashboard to retrieve time-series data and metrics. Use when you need to fetch visualization data from a publicly shared dashboard without authentication. Returns data frames with query results for the specified time range. |
| `grafana_retrieve_jwks` | Tool to retrieve JSON Web Key Set (JWKS) with all public keys for token verification. Use when you need to get the keys that can verify JWT tokens. |

## Notes

- **No API key for Grafana itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect grafana`.
- The action list above is a snapshot; `npx @useclawlink/cli actions grafana` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
