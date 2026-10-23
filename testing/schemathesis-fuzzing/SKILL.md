---
name: schemathesis-fuzzing
description: "Generates property-based API tests automatically from an OpenAPI 2/3.x or GraphQL schema using Schemathesis, runs them via the `schemathesis run` CLI or as a pytest decorator, configures the canonical checks (status_code_conformance, response_schema_conformance, content_type_conformance, response_headers_conformance, not_a_server_error), and gates CI on schema-conformance failures plus 5xx detection. Use when the project ships an OpenAPI or GraphQL schema and the team wants schema-driven coverage that scales as the API evolves."
---

# schemathesis-fuzzing

## Overview

Schemathesis is a property-based API testing tool that "automatically
generates property-based tests from your OpenAPI or GraphQL schema
and exercises the edge cases that break your API"
([schemathesis-readme][readme]). The schema is the **single source of
truth** - every endpoint, parameter, and response shape becomes a
generator that produces hundreds of targeted variations per run.

[readme]: https://github.com/schemathesis/schemathesis

This is **complementary** to example-based API testing
(`postman-collections`,
`tavern-testing`,
`restassured-testing`,
`karate-testing`) - example-based tests
verify happy paths; Schemathesis attacks the boundaries the team
forgot.

## When to use

- The repo has an OpenAPI 2.0 / 3.0 / 3.1 / 3.2 spec or a GraphQL
  schema (June 2018+).
- The team wants automatic test coverage of new endpoints without
  authoring per-endpoint tests.
- Negative-scenario coverage ("what happens with a malformed
  request?") is missing or thin.
- A CI gate on **5xx responses** (any unexpected server error) is
  desired.

If the API has no schema, Schemathesis cannot help - generate a
schema first (FastAPI, Flask-Smorest, NestJS Swagger, dropwizard, or
hand-author a spec), then return.

## How to use

1. Confirm the API ships an OpenAPI 2/3.x or GraphQL schema (see When to use).
2. Install the CLI (`pip install schemathesis`, or `uvx` for a one-off run).
3. Run `schemathesis run <schema>` against **staging** with the default checks; reproduce any failure from the printed `curl` command + Hypothesis seed.
4. Promote it to a first-class pytest test (`@schema.parametrize()`) and gate CI on schema-conformance + 5xx detection - deep CI wiring and advanced auth hooks live in [references/ci-and-pytest-integration.md](references/ci-and-pytest-integration.md).

## Install

```bash
pip install schemathesis
```

(Per [schemathesis-readme][readme].)

For the latest CLI without modifying the project's Python env:

```bash
uvx schemathesis run <schema-url>
```

(Adapted from [schemathesis-docs][docs] - `uvx` is the `uv` runner
for one-off tool execution.)

[docs]: https://schemathesis.readthedocs.io/en/stable/

## Running via CLI

Basic invocation per [schemathesis-readme][readme]:

```bash
schemathesis run <schema-url>
```

`<schema-url>` can be:

- Remote URL: `https://api.example.com/openapi.json`.
- Local file: `./openapi.yaml`.

### Key flags

Per [schemathesis-readme][readme]:

| Flag                              | Purpose                                                |
|-----------------------------------|--------------------------------------------------------|
| `--base-url <url>`                | Override the API base URL (test against staging vs prod). |
| `--checks <name>` (repeatable)    | Restrict to specific validations.                      |
| `--hypothesis-max-examples <N>`   | Number of generated cases per endpoint.                |
| `--workers <N>`                   | Parallel workers; speeds up large schemas.             |
| `--header 'X-API-KEY: ...'`       | Inject auth header on every generated request.         |
| `--auth user:pass`                | HTTP Basic Auth.                                        |
| `--cassette-har <path>`           | Record / replay using HAR files (debug aid).            |

### Worked example

```bash
schemathesis run https://api.example.com/openapi.json \
  --base-url https://staging.example.com \
  --checks status_code_conformance \
  --checks response_schema_conformance \
  --checks not_a_server_error \
  --hypothesis-max-examples 200 \
  --workers 4 \
  --header "Authorization: Bearer $API_TOKEN"
```

## Built-in checks

Per [schemathesis-readme][readme], the canonical checks:

| Check                               | What it verifies                                            |
|-------------------------------------|-------------------------------------------------------------|
| `status_code_conformance`           | Response status code is one of the codes documented in the schema for that endpoint. |
| `response_schema_conformance`       | Response body matches the documented schema (types, required fields, enum values). |
| `content_type_conformance`          | `Content-Type` header is one of the schema's documented media types. |
| `response_headers_conformance`      | Response headers conform to the schema's `headers` declaration. |
| `not_a_server_error`                | The response is **not** in the 5xx range; any 5xx is a hard fail. |

Run all checks (default), or restrict via repeated `--checks`:

```bash
# Strict: every check active
schemathesis run <schema>

# Only flag 5xx errors (cheap smoke test)
schemathesis run <schema> --checks not_a_server_error
```

A failing check produces a deterministic reproduction - Schemathesis
prints the exact `curl` command and Hypothesis seed to reproduce the
generated request.

## Pytest integration

For projects that want Schemathesis cases as first-class pytest
tests ([schemathesis-readme][readme]):

```python
# tests/api/test_schemathesis.py
import schemathesis

schema = schemathesis.openapi.from_url("https://your-api.com/openapi.json")

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
```

`@schema.parametrize()` generates one pytest test per endpoint × method
combination. `case.call_and_validate()` issues the generated request
and runs every default check.

For project-specific auth injection, header signatures, or response
post-processing, use `before_call` hooks - see
[references/ci-and-pytest-integration.md](references/ci-and-pytest-integration.md).

## Operating in CI

Gate PRs on Schemathesis with a shallow per-PR run
(`--hypothesis-max-examples 50`) and a deeper nightly cron (200+), always
against staging via `--base-url`. Hypothesis shrinks any failure to a
minimal reproducer, so a 50-example PR run catches most regressions while
the nightly depth surfaces the rare ones. The full GitHub Actions workflow
(JUnit reporting, artifact upload) and the per-PR / nightly / weekly cadence
table live in [references/ci-and-pytest-integration.md](references/ci-and-pytest-integration.md).

## Anti-patterns

| Anti-pattern                                                    | Why it fails                                                | Fix |
|-----------------------------------------------------------------|-------------------------------------------------------------|-----|
| Running with `--checks not_a_server_error` only and calling it done | 5xx detection misses 4xx-with-wrong-content cases.         | Run all default checks; 5xx-only is a smoke check, not coverage. |
| `--hypothesis-max-examples 5` to keep CI fast                     | Coverage too thin; flaky-looking results.                  | 50+ on PR; if too slow, parallelize via `--workers`. |
| Targeting production URL                                          | Generated requests can mutate prod data; 5xx alerts trigger oncall. | Always `--base-url <staging>`; production should never see fuzz traffic. |
| Stale schema URL                                                  | Schemathesis fuzzes the schema's authoritative version, not what the deploy actually serves; false negatives mask bugs. | CI fetches the schema from the PR's deployed staging artifact, not from a checked-in copy. |
| Ignoring shrunk failures                                          | A `not_a_server_error` failure with a 5-byte input is a real bug, not noise. | Triage every failure; close as "won't fix" only with a documented schema-amendment plan. |

## Limitations

- **Authentication state.** Schemathesis can attach a token but
  doesn't model multi-step auth flows (login → token → use).
  Combine with `tavern-testing` or
  `restassured-testing` for the
  auth chain.
- **Stateful sequences.** Out of the box, every Schemathesis case is
  independent. For stateful API fuzzing (POST → GET created
  resource → DELETE), use
  `restler-fuzzing`, which is built
  for stateful sequences.
- **Schema drift.** If the schema doesn't match the implementation,
  every case fails for the wrong reason. Run a Schemathesis baseline
  pre-PR to catch schema drift early.
- **OpenAPI 2.0 limitations.** Some OpenAPI 2.0 features (e.g.
  `formData`) generate weaker variations than 3.x; consider migrating
  the schema to 3.x.

## References

- [schemathesis-readme][readme] - main repo: install, CLI flags,
  built-in checks, pytest integration with `@schema.parametrize()`.
- [schemathesis-docs][docs] - full docs (CLI reference, hooks,
  authentication strategies).
- `restler-fuzzing` - stateful
  fuzzing complement.
- `postman-collections`,
  `tavern-testing`,
  `restassured-testing`,
  `karate-testing` - example-based
  authoring; use alongside Schemathesis for happy-path coverage.
