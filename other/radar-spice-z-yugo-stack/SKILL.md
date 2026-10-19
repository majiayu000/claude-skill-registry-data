---
name: radar
description: >-
  Maps a PR diff to user-facing API endpoints and screens, then counts
  real production usage of those surfaces. Use only when the user
  invokes /radar.
disable-model-invocation: true
---

# radar

Take a PR. Find the user-facing surfaces the diff can hit. Count how often those surfaces run in production. Report total volume and the slice the diff would actually change once deployed.

## Input

Need a GitHub PR URL (`https://github.com/owner/repo/pull/123`). A number is enough if the current workspace is that repo.

Optional: time window and environment. Default **last 7 days, production**.

If the PR is missing, ask and **stop**.

## Step 1: Fetch the PR

Done when you have title, files, and per-file patches.

```bash
gh pr view <n> --repo owner/repo --json title,body,author,baseRefName,headRefName,additions,deletions,url
gh api repos/owner/repo/pulls/<n>/files --paginate
```

If the workspace is not that repo, still use `gh`. Clone when the walk-up needs importers. Fetching one file at a time cannot search callers.

## Step 2: Map to user surfaces

Walk **up** from changed production files until you hit something a user can trigger. That thing is a **surface**.

A surface is one of:

| Kind | Name it as |
| --- | --- |
| HTTP API | `METHOD /path` (templated path, not a raw UUID) |
| GraphQL / RPC | operation name |
| Web | page route + how the user gets there |
| Mobile | screen name + navigation path |

**Walk-up:**

1. Drop tests, locales, generated files, lockfiles, CI-only, comments-only, formatting-only.
2. If the file *is* a route, controller, page, or screen — that is the surface.
3. Otherwise follow importers, registrars, and routers until you hit one. Shared helpers take **every** user-facing caller, each its own row.
4. Jobs, migrations, workers, and internal-only services are not surfaces. Note them as not user-facing.

For each surface, write the **condition** the changed code runs under:

- `always` — every hit of that surface runs the new code
- a specific action (`submit`, `cancel`, `onComplete`)
- a flag, org type, payload shape, or error path

Done when every changed production file is either on a surface (with a condition) or marked not-user-facing with a reason.

If there are no user surfaces, say so and **stop**.

## Step 3: Count real usage

Use whatever live metrics/logs this session has for **this** repo's product. This skill does not ship a product playbook.

**Affected** means traffic that would run the new code **once this PR is deployed**. Mobile screen counts lag until users update the app. Say that when the row is a screen.

1. List traffic tools in this session: metrics MCP, log MCP, analytics, RUM, warehouse, CLI. Also check installed skills, then repo `AGENTS.md` or docs, for how to query them.
2. Find how each surface is labeled (HTTP `method`+`path`, route metric, access-log URL, screen name, `track(` / `logEvent` / `capture` name). Inspect one real sample for field names. GraphQL that only appears as `POST /graphql` stays an uncounted slice unless the tool can filter by operation.
3. For each surface, after the surface list exists:
   - **Total** — calls/views in the window
   - **Affected** — the slice that would run the changed code
4. Prefer **metrics** (already counts) over **logs** (samples). Use logs only for a ratio when metrics cannot filter the condition: `affected ≈ total × (matching / sampled)`. Record the sample size. Cap at 200 events. Get high-volume totals from metrics, not by paging logs.
5. If nothing can count a surface: keep the row, **Source** = `could not measure: [missing tool]`.

**Evidence** (every number):

- **Source** holds the exact query (metric + labels, or log filter) and the absolute window (`YYYY-MM-DD` to `YYYY-MM-DD`).
- A log ratio also shows the sample, like `3/50 sampled`.
- A **`0` needs a positive control**: the same metric and labels, with only the route or event changed, must show traffic. Otherwise Source is `could not measure: label not found`, not `0`.
- Match a code route to a metric path label in Source when they differ.

**Affected** rules:

| Condition | Affected |
| --- | --- |
| `always` | same as total |
| Specific action, flag, or payload | that slice if measurable; else `≤ total` (uncounted) |
| New surface | `0` today, with positive control |
| Dead / unused | `0`, with positive control |

Done when every surface has a number, `≤ total`, `0` with control, or a "could not measure" reason. Missing tools are a reason, not a skip of the surface list.

## Step 4: Report

Lead with what pinged. Numbers first. Done when every row's Source would let someone rerun the query.

```markdown
## Radar: [PR title](url)

**Window:** YYYY-MM-DD to YYYY-MM-DD, production | **Product:** [from the PR repo]

### On the radar
- [one line: the hottest surface, volume, and whether the diff hits all of it or a slice]
- [surfaces with no traffic, if any]
- [what you could not measure]

### Surfaces

| Surface | Kind | Condition | Total | Affected | Source |
| --- | --- | --- | --- | --- | --- |
| `GET /v1/example` | API | always | 1.2M calls | 1.2M (100%) | `http_requests_total{method="GET",path="/v1/example"}` 2026-03-01 to 2026-03-08 |
| App → Detail | Screen | tap Save | 80k views | 12k saves | event `detail_save` 2026-03-01 to 2026-03-08 |
| App → Detail | Screen | tap Cancel | 80k views | ≤ 80k (uncounted) | event `detail_view` 2026-03-01 to 2026-03-08; cancel not in metrics |
| `POST /v1/unused` | API | always | 0 calls | 0 | `http_requests_total{path="/v1/unused"}` empty; sibling `/v1/used` is 4.1M |

### Not user-facing
- `path` — worker / migration / reason
```

- Units: API = **calls**, UI = **views** (and **actions** when you counted an action).
- Report counts in the window, not QPS, unless the user asked for a rate.
- One row per distinct surface. `GET` and `POST` of the same path are two rows. Large PRs: group the table by app/service.
