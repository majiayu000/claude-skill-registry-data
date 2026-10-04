---
name: Fetch Agent Card
skill_key: fetch_agent_card
description: Fetch an A2A agent card JSON from a given endpoint URL. Tries direct GET first, then falls back to /.well-known/agent.json.
runner:
  kind: python_file
  target: fetch_agent_card.py
requires:
  always: true
---

This skill fetches the agent card (JSON) from an A2A endpoint.

**Input parameters** (via stdin JSON):
- `url` (string, required): The A2A endpoint URL to fetch the agent card from.

**Output** (stdout JSON):
- `ok` (bool): Whether the fetch succeeded.
- `card` (string): The raw agent card JSON text (truncated to 2000 chars).
- `source` (string): `"direct"` or `"well_known"` indicating which fetch strategy succeeded.
- `error` (string): Error message if both attempts failed.
