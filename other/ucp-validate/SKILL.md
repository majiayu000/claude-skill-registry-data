---
name: ucp-validate
description: >
  Performs profile-oriented validation for a deployed UCP integration. It
  fetches /.well-known/ucp, checks basic structure, spot-checks spec/schema URLs,
  and reports official tool availability. Use after profile deployment or as a
  lightweight preflight before full UCP schema/conformance testing.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# UCP Validate

Run a lightweight validation pass against a deployed UCP profile.

## Run

```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate_ucp.py \
  https://example.com \
  --output store/clients/example/validation-report.md
```

## What This Script Checks

- `/.well-known/ucp` or `/.well-known/ucp.json` exists
- JSON parses and has a top-level `ucp` object
- `ucp.version` uses `YYYY-MM-DD`
- `ucp.services`, `ucp.capabilities`, and `ucp.payment_handlers` exist
- service entries include required basics such as `version` and endpoint for
  network transports
- payment handler entries include `id` and `version`
- up to five capability `spec`/`schema` URLs are reachable
- offline validation against the vendored official UCP profile schema
  (`refs/ucp-schema/2026-04-08/`), when `jsonschema` is installed
- local availability of official `ucp-schema` and conformance tooling

## What It Does Not Yet Check

- Catalog search/lookup behavior
- Checkout create/update/retrieve/cancel lifecycle
- Payment handler runtime behavior
- Real conformance-suite execution

Use official UCP tools for those deeper checks.

## Output

Writes:

- `validation-report.md`
- `validation.json` when `--json-output` is provided

The validator returns PASS, CONDITIONAL PASS, or FAIL based on critical and
error-level checks.

## Hard Rule

Never call checkout completion or trigger real payment capture during validation.
