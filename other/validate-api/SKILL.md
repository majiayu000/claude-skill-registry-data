---
name: validate-api
description: Run the project's Hurl scenarios with an OIDC access token passed as a secret variable
argument-hint: "[hurl-file-or-dir]"
user-invocable: true
---

# Validate API

Use `$ARGUMENTS` or discover the project's Hurl scenarios. Resolve
`API_BASE_URL` from project configuration. Confirm before contacting production.

Use `$TOKEN` when present. Otherwise run `${TOKEN_COMMAND:-scripts/get-backend-token.sh}`;
if that command is absent, route through `/backend-validator:get-dev-token`.

Confirm the backend is reachable using a project-defined readiness or health
surface when one exists. Do not invent an endpoint.

Run the target with the installed Hurl secret-variable interface:

```bash
hurl --test \
  --secret token="$TOKEN" \
  --variable base_url="$API_BASE_URL" \
  "$TARGET"
```

On failure, identify the exact scenario/assertion and distinguish backend,
fixture, token, environment, and test defects.

Use the project's existing validation stack rather than replacing it. Load
`references/hurl-patterns.md` for captures, retries, parallel isolation, and
report-leakage details.
