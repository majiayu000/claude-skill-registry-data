---
name: ucp-profile
description: >
  Generates a /.well-known/ucp business profile JSON from explicit merchant
  inputs such as domain, business name, payment provider, transport, and
  capability list. Use after ucp-audit to create a deployment-ready draft.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UCP Profile Generator

Generate a public UCP discovery profile for a merchant.

## Required Inputs

- Merchant domain
- Business/display name
- Payment provider: `stripe`, `shopify`, or `adyen`
- Transport: `rest` or `mcp`
- Capabilities: comma-separated list from `checkout,cart,catalog,fulfillment,discount,order`

## Run

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate_profile.py \
  --domain example.com \
  --name "Example Store" \
  --payment stripe \
  --transport rest \
  --caps checkout,cart,catalog,fulfillment,discount,order \
  --output store/clients/example/ucp-profile.json
```

## Output Contract

The script writes `ucp-profile.json` with:

- `ucp.version`
- `ucp.services`
- `ucp.capabilities`
- `ucp.payment_handlers`

Some payment templates intentionally contain `FILL_IN` placeholders for public
merchant identifiers or publishable keys. Replace those before deployment.

## Deployment

Host the final JSON at:

```text
https://{merchant_domain}/.well-known/ucp
```

Serve it as JSON and allow public reads. The profile is public discovery data.

## Hard Rules

- Never include secret API keys in the profile.
- Do not infer capabilities that the merchant cannot actually serve.
- If `FILL_IN` remains, report it clearly and do not call the profile final.

## Downstream

- `ucp-checkout` uses the profile to design service endpoints.
- `ucp-validate` checks the deployed profile.
