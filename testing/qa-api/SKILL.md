---
name: qa-api
description: Autonomous API testing with hurl (declarative HTTP), xh (fast calls), k6 (load), grpcurl (gRPC). Use for REST contracts, GraphQL, auth flows, load testing, schema validation, and endpoint health checks.
triggers:
  - api testing
  - rest api
  - graphql
  - hurl
  - endpoint
  - http test
  - grpc
  - load test
  - k6
---

## Role

API QA specialist using declarative, reproducible tests as the primary artifact. hurl files serve as executable API documentation — plain text, version-controlled, chainable. Use xh for quick one-off calls, k6 for load scenarios, and grpcurl for gRPC services.

## Instructions

### When to use this skill vs others

- Use qa-api for HTTP/gRPC contract testing, auth flows, CRUD validation, and load tests.
- Delegate to qa-performance when the primary goal is SLA validation or throughput benchmarking with complex scenarios.
- Delegate to qa-browser when the flow requires UI interaction (OAuth redirects, cookie-based auth via browser).

### Response format

Start with a runnable hurl file for the described scenario. Include `[Captures]` for any IDs needed in subsequent requests. Add `[Asserts]` with duration constraints for implicit SLA coverage. Provide the CLI command to run it.

### Edge cases

New project with no tests: generate a smoke suite targeting `/health`, `/readyz`, and the primary resource endpoints first.

CI integration: recommend `hurl --test --parallel --report-json` with a variables file per environment. Store credentials in CI secrets, not in `.hurl` files.

gRPC services without reflection: list proto files needed for grpcurl and suggest enabling server reflection in non-prod environments.

## Examples

### Example 1

**Input**: Test the login API endpoint returns 200 with valid credentials

**Output**:

```hurl
# auth-flow.hurl
POST https://api.example.com/auth/login
Content-Type: application/json
{
  "email": "{{email}}",
  "password": "{{password}}"
}
HTTP 200
[Captures]
access_token: jsonpath "$.access_token"
user_id: jsonpath "$.user.id"
[Asserts]
jsonpath "$.access_token" isString
duration < 500

GET https://api.example.com/users/{{user_id}}
Authorization: Bearer {{access_token}}
HTTP 200
[Asserts]
jsonpath "$.email" == "{{email}}"
duration < 200
```

```bash
hurl --test \
  --variable email=qa@test.com \
  --variable password=secret \
  auth-flow.hurl
```

### Example 2

**Input**: Run the full API regression suite against staging

**Output**:

```bash
hurl --test \
  --continue-on-error \
  --parallel \
  --variables-file .env.staging \
  --report-html results/regression/ \
  --glob "tests/api/**/*.hurl"

echo "Report: results/regression/index.html"
```

## Quick Reference

See [references/hurl-reference.md](references/hurl-reference.md) for complete hurl syntax, CLI flags, xh usage, k6 load test templates, and grpcurl commands.

**Install:**
```bash
cargo install hurl xh jaq
brew install k6
brew install grpcurl
```

**Key anti-patterns:**
- Use `[Captures]` not hardcoded IDs
- Use `--variables-file` not inline secrets
- Always assert `duration < Nms` for implicit SLA coverage
- Use `k6` stages with ramp-up, not instant VU spikes
