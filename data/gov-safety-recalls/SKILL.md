---
name: gov-safety-recalls
description: Search NHTSA vehicle recalls, FDA food/drug recalls, and CFPB consumer complaints. 3 tools for product safety monitoring.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🚗","requires":{"bins":["mcporter"]}}}
---

# US Safety Recalls

Real-time access to NHTSA vehicle recalls, FDA product recalls, and CFPB consumer complaints.

## Setup

```bash
mcporter add gov-safety --url https://us-safety-recalls-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-safety": {
      "url": "https://us-safety-recalls-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `safety_search_vehicle_recalls`
Search NHTSA vehicle safety recalls by make, model, and year. Returns recall campaigns with defect summaries, consequences, and remedies.

```
Search for Ford F-150 recalls in 2024
Are there any Toyota Camry recalls?
```

Parameters: `make`, `model`, `modelYear`

### `safety_search_fda_recalls`
Search FDA enforcement actions (recalls) for drugs, food, or medical devices. Returns classification, status, distribution, and reason for recall.

```
Search FDA recalls for infant formula
Any recent Class I drug recalls?
```

Parameters: `searchQuery`, `classification` (I/II/III), `status`, `limit`

### `safety_search_consumer_complaints`
Search the CFPB Consumer Complaint Database for complaints against financial companies.

```
Show consumer complaints about Wells Fargo
Search CFPB complaints about mortgage servicing
```

Parameters: `company`, `product`, `issue`, `limit`

## Data Sources

- **NHTSA** — National Highway Traffic Safety Administration (vehicle recalls)
- **FDA** — Food and Drug Administration (food, drug, device recalls)
- **CFPB** — Consumer Financial Protection Bureau (consumer complaints)

## Use Cases

- Check if your vehicle has open recalls
- Monitor food safety alerts
- Research company complaint history
- Product safety due diligence

All data from free US government APIs. Zero cost. No API keys required.
