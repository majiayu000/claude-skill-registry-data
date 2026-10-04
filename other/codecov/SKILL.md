---
name: codecov
description: Query Codecov for flaky-test signal, failure history, and coverage data via the codecov-api wrapper. Use when asked about flaky tests, intermittent test failures, why a test is failing, coverage on a PR/file/branch, or whenever browser access to Codecov is blocked by the login wall.
---

# Codecov

Auth is already in env — `dot_bashrc` exports `CODECOV_API_TOKEN`. The
`codecov-api` wrapper in `~/.local/bin/` injects auth + the
`https://api.codecov.io` base. Don't shell out to `curl` directly.

## Triggers

- "Is `<test>` flaky?" / "What's its failure rate?"
- "Show failed tests on `<branch>` recently."
- "Why is `<test>` failing?" (stack trace lookup)
- "What's the coverage delta on this PR / file / branch?"
- Any Codecov UI URL behind the login wall.

## Repo coordinates

Most paths take `{service}/{owner}/{repo}` where `service` is one of
`github`, `gitlab`, `bitbucket` (no `.com`). Derive from the current
checkout via `git remote get-url origin`.

## REST — flaky / failed tests

`GET /api/v2/{service}/{owner}/repos/{repo}/test-results/`

Verified query parameters:

- `branch` — filter by branch name
- `commit_id` — filter by commit SHA
- `outcome` — `pass` | `failure` | `skip` | `error`
- `duration_min` / `duration_max` — seconds
- `page` / `page_size` — pagination

```sh
codecov-api "/api/v2/github/<owner>/repos/<repo>/test-results/?branch=main&outcome=failure&page_size=100"
```

Detail (stack trace, etc.):

```sh
codecov-api "/api/v2/github/<owner>/repos/<repo>/test-results/<id>/"
```

REST has **no `flake_rate` filter and no test-name filter**. For a
ranked flake answer, paginate `outcome=failure`, group by name,
divide by total runs of that name (separate call without `outcome`),
or use GraphQL.

## GraphQL — ranked flake aggregates

`POST /graphql/` is the same wrapper:

```sh
codecov-api /graphql/ \
  -X POST -H 'Content-Type: application/json' \
  -d '{"query":"...","variables":{...}}'
```

Schema entry points worth knowing: `repository.testAnalytics.testResults`,
`repository.testAnalytics.flakeAggregates`. When in doubt, fetch the
schema (`{ __schema { types { name } } }`) and read it.

## Coverage queries

The full v2 swagger lives at <https://api.codecov.io/api/v2/docs/>
— consult it for `commits/`, `report/`, `pulls/{id}/`, `compare/`
endpoints rather than memorising paths. All take the same `{service}/
{owner}/{repo}` prefix and the same auth.

## Caveats

- **60-day retention** on test results. Older history is gone.
- **Repo must be opted into Test Analytics** (CI uploads test results
  to Codecov). Repos without uploads return empty `results`.
- **Don't suggest the web UI** as a fallback — it's the login-walled
  surface this skill exists to bypass.

## When the API gap bites

If a workflow needs `flake_rate`/`failure_rate`/test-name filters and
the GraphQL ergonomics are painful, the right escalation is a feature
PR to `egulatee/mcp-server-codecov` adding `get_test_results` and
`get_flake_aggregates` tools. Don't fork or build a custom MCP.
