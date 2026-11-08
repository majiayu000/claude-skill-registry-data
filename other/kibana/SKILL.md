---
name: kibana
description: Kibana integration for AI agents via ClawLink — browser login, no API key setup. Connect kibana through ClawLink's hosted setup. Use this skill when the user wants to work with Kibana (Developer Tools) — connect Kibana, read or update Kibana data, or take actions in Kibana from chat instead of saying you cannot access it.
---

# Kibana

Use **Kibana** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Kibana once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect kibana   # opens browser → authorize Kibana
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Kibana

```bash
npx @useclawlink/cli actions kibana "<what you want to do>"   # find an action
npx @useclawlink/cli describe kibana <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run kibana <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `kibana_delete_alerting_rules` | Tool to delete an alerting rule in Kibana. Use when you need to remove a specific alerting rule by its ID. |
| `kibana_delete_connectors` | Tool to delete a connector in Kibana. Use when you need to remove an existing connector. |
| `kibana_delete_fleet_output` | Tool to delete a specific output configuration in Kibana Fleet. Use when you need to remove an existing output by its ID. |
| `kibana_delete_fleet_proxy` | Deletes a Fleet proxy configuration by its unique identifier. Fleet proxies enable agents to communicate through proxy servers. Use this action to remove proxy configurations that are no longer needed. The proxy must not be in use by any agent policies or outputs before deletion. Requires 'fleet-settings-all' privileges in Kibana. |
| `kibana_delete_list` | Deletes a list. Use when you want to delete a list by its ID. |
| `kibana_delete_osquery_saved_queries` | Delete a saved Osquery query by its saved object ID. Use this to remove a specific Osquery saved query from Kibana. IMPORTANT: This action requires the 'saved_object_id' (UUID format), not the custom 'id' field. You can obtain the saved_object_id by listing queries first or from the response when creating a query. |
| `kibana_delete_saved_objects` | Tool to delete a saved object in Kibana. Use when you need to remove a specific saved object like a visualization or dashboard. |
| `kibana_find_alerts` | Tool to find and/or aggregate detection alerts in Kibana. Use this to retrieve a list of alerts, optionally filtering them with a query and performing aggregations. |
| `kibana_get_action_types` | Retrieves all available connector types (actions) in Kibana. Connector types (also called action types) are integrations like Slack, Email, Webhook, ServiceNow, etc. that can be used with alerting rules, cases, and workflows. Use this to discover which connector types are available and their requirements (license, features) before creating a new connector instance. Returns detailed information about each connector type including: - ID (e.g., '.slack', '.email', '.webhook') - Display name and enabled status - License requirements (basic, gold, platinum, enterprise) - Supported features (alerting, cases, workflows, etc.) - Configuration and deprecation status |
| `kibana_get_alert_types` | Retrieves available rule types (alert types) in Kibana. Returns comprehensive metadata about each rule type including: - Available action groups and variables for action templates - License requirements and authorization details - Category (management, observability, securitySolution) - Configuration options like auto-recovery and timeout settings Use this to discover what types of alerting rules can be created in your Kibana instance, such as Elasticsearch query alerts, index threshold alerts, machine learning anomaly detection, and security detection rules. |
| `kibana_get_alerting_rules` | Tool to retrieve a list of alerting rules in Kibana. Use when you need to get a paginated set of rules based on specified conditions. |
| `kibana_get_cases` | Tool to retrieve a list of cases in Kibana. Use when you need to find or list existing security or operational cases, potentially filtering by various attributes like status, assignee, or severity. |

## Notes

- **No API key for Kibana itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect kibana`.
- The action list above is a snapshot; `npx @useclawlink/cli actions kibana` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
