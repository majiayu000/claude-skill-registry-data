---
name: gov-regulatory
description: Federal Register rules, notices, and agency documents. 4 tools for regulatory monitoring.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"📜","requires":{"bins":["mcporter"]}}}
---

# Regulatory Monitor

Search the Federal Register for rules, proposed rules, notices, and presidential documents.

## Setup

```bash
mcporter add gov-regs --url https://regulatory-monitor-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-regs": {
      "url": "https://regulatory-monitor-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `reg_search_documents`
Search Federal Register for rules, notices, and presidential documents.

```
Search Federal Register for AI regulations
Find EPA rules published this month
```

Parameters: `term`, `documentType` ("RULE", "PRORULE", "NOTICE", or "PRESDOCU"), `agency` (slug), `dateFrom` (YYYY-MM-DD), `dateTo`, `significant` (boolean), `perPage`, `page`

### `reg_get_document`
Get full details of a specific Federal Register document by document number.

```
Get Federal Register document 2024-12345
```

Parameters: `documentNumber` (required)

### `reg_search_public_inspection`
Search pre-publication documents on public inspection before they appear in the Federal Register.

```
Search public inspection for upcoming SEC rules
Any upcoming EPA notices?
```

Parameters: `term`, `agency`, `documentType` ("RULE", "PRORULE", "NOTICE", or "PRESDOCU")

### `reg_list_agencies`
List or search federal agencies in the Federal Register.

```
List all federal agencies
Search for agencies related to energy
```

Parameters: `search`

## Data Sources

- **Federal Register** — Official journal of the US government (rules, notices, executive orders)

## Use Cases

- Regulatory compliance monitoring
- Policy tracking and analysis
- Government affairs research
- Rulemaking comment preparation

All data from free US government APIs. Zero cost. No API keys required.
