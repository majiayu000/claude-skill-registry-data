---
name: ucp-checkout
description: >
  Generates or guides a sandbox Python FastAPI UCP shopping checkout server from
  ucp-profile.json and catalog.json. Use after ucp-profile and ucp-catalog are
  complete to create catalog search/lookup and checkout create/retrieve/update/
  cancel endpoints for local preflight validation.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UCP Checkout

Generate a sandbox FastAPI server for UCP catalog and checkout preflight.

## Required Inputs

- `store/clients/{client_name}/ucp-profile.json`
- `store/clients/{client_name}/catalog.json`

## Generate

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate_api.py \
  --profile store/clients/{client}/ucp-profile.json \
  --catalog store/clients/{client}/catalog.json \
  --output-dir store/clients/{client}/ucp-server
```

Use `--force` only when intentionally replacing an existing generated server.

## Generated Endpoints

```text
GET  /.well-known/ucp
POST /ucp/v1/catalog/search
POST /ucp/v1/catalog/lookup
POST /ucp/v1/checkout
GET  /ucp/v1/checkout/{id}
POST /ucp/v1/checkout/{id}
POST /ucp/v1/checkout/{id}/cancel
```

## Validate Locally

```bash
cd store/clients/{client}/ucp-server
pip install -r requirements.txt
uvicorn app.main:app --port 8000

python ${CLAUDE_SKILL_DIR}/../ucp-validate/scripts/validate_ucp.py \
  http://localhost:8000 \
  --runtime-endpoint http://localhost:8000/ucp/v1
```

## Hard Rules

- Generated code is sandbox-only.
- Do not implement real payment capture in generated output.
- Never call checkout completion during automated validation.
- Keep secrets out of `ucp-profile.json` and generated sample data.

Read `references/checkout-lifecycle.md` for lifecycle and totals rules.
