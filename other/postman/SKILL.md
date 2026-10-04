---
name: postman
description: "Build Postman collections and environments, write request scripts, and run API smoke checks with Newman."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["postman", "api", "collections", "newman", "testing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Postman API Collections AI Skill Guide

## Overview & Engine Architecture

Postman organizes HTTP requests into collections with folders, environments (variables), and optional tests/pre-request scripts. Team workspaces sync shared collections; Newman runs collections in CI. Agents keep secrets in environments - not hard-coded in requests - write assertions that catch contract breaks, and prefer versioned collection exports in git when teams treat APIs as code.

```
Workspace
   -> Collections (folders / requests)
       -> Environments (local / ci / prod vars)
       -> Tests + pre-request scripts
Newman / Collection Runner -> CI reports
```

## When to use this skill

- Building shareable API smoke suites
- Documenting auth flows for other engineers
- Running Newman in PR pipelines
- Contrasting with `@bruno` git-native collections

## Operational directives

1. Never store production tokens in shared collection JSON; use environment secrets / vault injection.
2. Name requests by intent (`POST /orders - create`); keep examples minimal and current.
3. Assert status codes and critical JSON paths; avoid over-fitting to volatile fields (timestamps).
4. Parameterize base URLs via `{{baseUrl}}` per environment.
5. Export/collection sync should not overwrite teammates' in-progress edits without coordination.

## Test script sketch

```js
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("has id", () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property("id");
  pm.environment.set("lastOrderId", json.id);
});
```

## Newman CI sketch

```bash
newman run collection.json -e ci.environment.json \
  --env-var "baseUrl=$BASE_URL" \
  --env-var "token=$API_TOKEN" \
  --reporters cli,junit --reporter-junit-export newman.xml
```

## Collection hygiene

| Smell | Better approach |
| --- | --- |
| Prod password in collection | Environment secret / CI variable |
| One giant unsorted dump | Folders by resource; happy-path + negative cases |
| Tests only check `status !== 500` | Assert schema-critical fields |
| Duplicated auth on every request | Collection auth or pre-request token refresh |

## Best practices

- Keep a "smoke" collection small enough for every PR; deeper suites nightly.
- Document required env vars in the collection description.
- For git-first workflows with PR review of requests, also consider `@bruno`.
- Rotate tokens used in shared team environments regularly.

## Limitations

- Postman Cloud vs local-only workflows differ on sync, forks, and governance.
- GraphQL and gRPC support exist but patterns differ from plain REST collections.
- Contract testing at scale may need OpenAPI-driven tools beyond Postman.

## Related skills

- `@bruno` - file-based collections complementary to Postman
- `@openapi-endpoint-filtering` - shrink large specs before client gen
- `@playwright` - full UI flows when API smoke is not enough
