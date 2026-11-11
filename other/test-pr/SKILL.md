---
name: test-pr
description: Prepare a feature or PR for manual testing on the local dev server and hand the user a ready-to-follow test document. Reads the change, derives test scenarios, gets the dev server and database running, independently makes sure the local database holds good test data for every scenario (seeding it if missing), resolves the real local URLs from env vars (custom domains), and delivers one numbered checklist with links, logins, steps and expected results. Use for "test this PR", "help me test this feature", "QA this branch locally", "set up test data for X".
argument-hint: "[pr-number | branch | feature description]"
---

# Test PR locally

Do all the preparation yourself, then give the user **one readable test
document**: go here, log in as this, do this, expect that. The user tests at
their own pace and reports back in chat.

Target: $ARGUMENTS — a PR number, branch name, Linear issue, or a feature
description. Empty = the current branch versus the default branch.

## Hard rules

- **Never use the `ask` tool** in this skill — no question blocks, no
  Pass/Fail pickers, no "Go?" confirmations. Work independently and make
  sensible choices; mention any assumption in the document.
- **Never hand out a URL you did not resolve and check** (see step 3).
  `localhost:<port>` is wrong whenever the project uses a custom domain.
- Only ever write to a **local** database. Before any write, confirm the
  connection host is `localhost`, `127.0.0.1`, a docker-compose service, or a
  local socket. If it is anything else, stop and tell the user.
- Never truncate, reset, or drop data.
- Mark created data with a `qa-` prefix in names/emails/slugs where the schema
  allows it, and log every created record (table + id, or seed command) to
  `.work/test-pr/<slug>/data.md` in the project.

## 1. Understand the change

- Resolve the diff: `pr://<N>/diff/all` for a PR number, otherwise
  `git diff <default-branch>...HEAD` plus uncommitted changes. If the target
  branch is not checked out and the working tree is clean, check it out;
  if the tree is dirty, stop and say so.
- Read the PR description, linked Linear issue, and commit messages for intent
  and acceptance criteria.
- Read the changed code enough to know: entry points (routes, screens, API
  endpoints, jobs), who can use them (roles, permissions, feature flags), and
  what data they read and write.

## 2. Derive scenarios

Pick 3–10 scenarios, happy path first:

- Happy path for each user-facing story.
- Permission/role variants the code actually checks.
- Edge cases the diff touches: empty states, validation errors, limits,
  states the new code branches on (e.g. `status = archived`).
- One regression check for nearby existing behaviour the change could break.

For each scenario work out: preconditions (data + user + flags), steps,
expected result. Scenarios that cannot be tested manually go in a short
"Not covered" list with the reason.

## 3. Get the environment running and resolve the URLs

Discover, don't guess: `.work/config.json` servers, `package.json` scripts,
`Makefile`, `docker-compose*.yml`, README.

- Start the database and dependencies if they are not running; run pending
  migrations with the project's own command.
- Start the app with the `dev_server` tool when the project has servers
  configured; otherwise a named long-lived `bash` service. Wait until ready.

**Resolve the real base URLs.** The user runs custom local domains, so:

- Read every `.env*` file the dev server loads (`.env`, `.env.local`,
  `.env.development`, per-app env files in monorepos) and the env of the
  `.work/config.json` server entry. Look for URL/host vars: `*_URL`, `*_HOST`,
  `*_DOMAIN`, `*_ORIGIN`, `BASE_URL`, `APP_URL`, `NEXTAUTH_URL`,
  `PUBLIC_*`/`NEXT_PUBLIC_*`/`VITE_*` URLs, cookie domains, CORS origins.
- Also check local proxy/hosts setup when referenced: `/etc/hosts`, Caddyfile,
  nginx/Traefik config, `*.localhost`/`*.test` domains.
- When several apps exist (app, admin, API, marketing), map which domain serves
  which scenario.
- Verify each base URL with `curl -sk -o /dev/null -w '%{http_code}'` (or open
  it with `agent-browser`). Use the domain that works and matches the env; fall
  back to `localhost:<port>` only when no custom domain is configured.

## 4. Make sure good test data exists

For every scenario precondition, query the database (read-only) or the app's
API and decide: reuse an existing record, or create one.

Fill gaps in this order of preference:

1. The project's seed scripts / fixtures / factories.
2. The app's own API or admin endpoints, so validations and side effects run.
3. Direct SQL as the last resort, matching constraints and required columns.

Good data means the scenario is actually exercisable: records in each state
the new code branches on, enough rows for lists/filters to show a difference,
realistic names, and a login for every role tested (known password or
magic-login route). Enable feature flags the change sits behind.

Then **smoke-check each scenario's start page** with `agent-browser` (logged in
as the scenario's user where possible): page loads, the needed data is
visible, no console errors. Fix setup problems before writing the document.

## 5. Deliver the test document

Write it to `.work/test-pr/<slug>/test-plan.md` and post the same content as
your final chat message. Format — a plain markdown document, nothing else:

```markdown
# Testing: <PR title>

**App:** https://<resolved-domain>  ·  **Login:** qa-admin@example.test / <password>
**Test data:** Baltic Freight (renewing), Nordic Paper (no outlook), … — logged in data.md

## 1. <Scenario title>
Open https://<resolved-domain>/customer-health
1. Find the "Renewal outlook" column.
2. Click the chip on **Baltic Freight**, pick *Renewing*.

Expected: chip turns blue "Renewing"; hover shows "Updated <today> by <you>".

## 2. …

## Not covered
- Low-role user check — no such role exists locally.
```

Rules for the document:

- Every scenario starts with a full clickable URL on the resolved domain.
- Steps are a numbered list, one action per line; name the exact record to use.
- "Expected:" on its own line after the steps.
- Login and data summary once at the top; repeat a login only when a scenario
  uses a different user.
- No pass/fail pickers. End with one line: "Tell me which numbers fail and
  what you saw."

## 6. When the user reports back

- For each reported failure: check server logs and DB state, find the likely
  cause with file and line, and say whether it is a bug in the change, a data
  problem, or an environment problem. Fix data/env problems yourself; fix code
  only if the user asks.
- If a scenario consumed its data, create fresh data and give the updated
  step.
- On request: post results as a PR or Linear comment, remove the `qa-` data
  listed in `data.md`, stop the dev server. Never do these unprompted.
