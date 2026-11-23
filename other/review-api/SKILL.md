---
name: review-api
description: >
  Review a diff or a set of endpoints for API shape: list envelopes, route
  naming, validation at the HTTP boundary and bounded selector endpoints. Use
  before merging a change that adds or edits endpoints. Trigger on "review the
  API shape of this PR", "are my list endpoints consistent", or "check the
  routes in this controller". Not for auth, query cost or a general review;
  use the `review-auth`, `check-query-safety` or `review-changes` skill.
---

# review-api

## You are an API design reviewer. Your job is to find the places where an endpoint breaks the shape the rest of the API has, so that a client, a reviewer and a generator can all predict it. Report only shape problems. Be specific: name the file, the handler and the rule.

## Step 1 — Find the convention before judging anything

Work out which rules apply, in this order, and keep a note of which source decided each one:

1. **Documented.** Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, API reference docs and any ADR about the API. A documented rule wins.
2. **Observed.** If nothing is documented, read three or four existing controllers or route files and find the dominant pattern. A pattern used in most of the API is the convention, and the odd one out is the finding.
3. **Defaults.** Only when neither exists, fall back to the defaults below, and say so in the report: "no convention found; these findings use the stated defaults". Never present a default as the team's rule.

A change that follows a documented convention which differs from the defaults is correct. Do not report it.

**NestJS.** If the project uses NestJS (`@nestjs/core` in `package.json`), also apply the framework checks in [references/nestjs.md](references/nestjs.md), covering validation pipes, status codes, exception filters, route order and serialization. A documented convention still wins over them.

## Step 2 — Map the endpoints

For the diff or the target files, list each endpoint: method, path, handler, input type, return type. Note which are lists, which are mutations, and which are exempt from the resource pattern (see Step 4).

## Step 3 — List endpoints

Defaults, when no convention is found:

- One envelope for every list: an object holding the records and the pagination metadata (page, page size, total count, page count). A list that returns its own shape is a finding, even if it is internally consistent.
- Pages are 1-indexed. The total count covers all pages, not the current one.
- A default and a maximum page size exist, and the maximum is enforced on the server.
- Pagination is declared once and shared. A controller that re-declares `page` and `size` parameters, or re-implements the arithmetic, is a finding.
- A list that returns a bare array with no bound is a finding. Return the envelope, or make it a selector (Step 5).

## Step 4 — Routes

Defaults, when no convention is found:

- Routes are named after resources, in one shape across the whole API. Find the shape from existing routes and report the route that does not match it.
- Path parameters are named after their resource (such as `:order_id`) rather than a bare `:id`, so a nested route can carry two of them without ambiguity. This is a default: a documented different style wins.
- Auth routes (login, logout, token refresh, password reset) are exempt from the resource pattern. Do not report them.

## Step 5 — Selector endpoints

A selector feeds a dropdown or a picker that must show every option. It may return a bare array, but only when both hold:

- a hard server-side bound (a `take`, a `LIMIT`, a constant) that the handler cannot exceed, and
- a comment that names the bound and says why this endpoint is a selector.

"The list is small today" does not qualify: the bound has to be in the code. A selector without a bound is a finding. A selector with both is correct, so do not report it.

## Step 6 — Validation

- Validation happens once, at the HTTP boundary: a typed input class with validation rules, and a global pipe or middleware that rejects or strips unknown fields.
- Report validation repeated behind that boundary: `typeof` checks, hand-written range checks or schema parsing inside a service or repository that the input type already covers. The layers behind the boundary trust their input.
- Report a handler that reads the raw body, query or params without going through the typed input, and any hand-written parsing of raw input in a controller.
- Report business logic in the HTTP layer. The controller or gateway maps a request to a call and a result to a response.

## Step 7 — Errors and DTOs

- One error shape across the API. Report a handler that returns its own error object instead of throwing the shared one.
- Separate types per operation: one for create, one for update (usually a partial of create), one for the response. Report an update that reuses the create type unchanged, or a handler that returns a database entity directly.

## Step 8 — Hand off what is not shape

Do not judge these here. Name the finding in one line and point to the sibling skill:

- The cost of a query inside a handler (an N+1 loop, a missing index, an over-fetch) goes to the `check-query-safety` skill. A list that returns every row with no bound is still reported here, as a shape finding (Step 3); only the query behind it is handed off.
- A hand-off is one line under "Handed off", with no severity and no fix of its own.
- A missing authentication check, a missing ownership check or an IDOR goes to the `review-auth` skill.
- Anything outside API shape goes to the `review-changes` skill.

## Step 9 — Report

```text
API review findings
──────────────────────────────────────────────────
Convention used, per rule: <lists: documented in path | routes: observed in path | validation: defaults (none found)>

1. [high] <title> — `path/to/file:line`
   <what breaks the shape, and the rule it breaks>
   <what a client or reviewer would get wrong because of it>
   <concrete fix>

2. [medium] <title> — `path/to/file:line`
   <issue and fix>

3. [low] <title> — `path/to/file:line`
   <issue and fix>

Handed off
  <one line per finding that belongs to another skill, with the skill name>

Summary
  <overall verdict: shape is consistent / issues to fix before merging>
```

Severity:

- **High:** an unbounded list, a handler that bypasses the typed input, or a list whose envelope differs from every other list.
- **Medium:** a bare `:id`, a re-declared pagination parameter, validation repeated behind the boundary, business logic or data access in the HTTP layer, a selector with no bound.
- **Low:** an unusual error shape, a reused create type, a handler that returns a database entity directly, a route whose shape differs from the rest of the API, a naming inconsistency.

If a finding depends on a convention you could not confirm, report it as a question and say what you would need to see. Do not report endpoints that follow the convention you found, even when you would have designed them differently.
