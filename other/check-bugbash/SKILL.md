---
name: check-bugbash
description: Full bug bash of a Keelokit project across every dimension (data, API, contracts, logic, integrity, auth, UX, UI, web, mobile, i18n, copy, a11y, security, NFRs, config, ops, and dx, docs and packaging for what developers use) — parallel lenses on the running app with seeded personas, adversarial validation of each finding, fixes at the root cause, and, for every class of bug, a new automatic check so it can't come back. Use when the user says "bug bash", "cazá bugs", "revisá todo", "buscá errores", "QA completo", before a release, or after each wave.
---

# Bug bash — find, prove, fix at the root, and never again

Autonomous until the report. The one exception: a fix that would change a **product rule** (what
the product should do, not how) is not decided — it becomes a pending decision with options and
a recommendation, and work continues on everything else.

**Source of truth for "expected":** `docs/context/`, `docs/prd.md`, the stories in `backlog/`,
the project's style guide if any. If the expected behaviour doesn't follow from them, it is a
pending decision, not a bug.

Findings format and severity: `references/finding-format.md`. Lenses: the ones the project's
profile calls for (`.keelokit/profile.toml` and "Which lenses a project gets" in
`${CLAUDE_PLUGIN_ROOT}/references/dimensions.md`) — a data model, contracts and screens for a
product; developer experience, docs and packaging for a library, CLI or plugin. If the code shows
something the profile doesn't, update the profile first (`/keelokit:check-health`). Name every
skipped lens in the report with its reason. The
`integrity` lens attacks every invariant in `docs/context/domain.md` with its class's attack from
`${CLAUDE_PLUGIN_ROOT}/references/invariants.md`, the way `agents/breaker.md` does for one story.

## How it runs

Where Claude Code can run workflows (the Workflow tool is available), steps 1–5 run as the
plugin's workflow `keelokit:check-bugbash-flow`: the same procedure, with its shape fixed in code
— lenses at most `maxParallel` at a time, every finding reproduced by an independent skeptic (two
for P0 and P1, one on the session's model), rounds of a completeness critic until nothing new
turns up, fixes one at a time each checked by an agent that didn't write it (a rejected fix is
undone, not left half-done), and the report. Its intermediate results stay out of this
conversation, and a run cut short resumes where it stopped.

Start it with the Workflow tool, name `keelokit:check-bugbash-flow` (or `scriptPath`
`${CLAUDE_PLUGIN_ROOT}/workflows/check-bugbash-flow.js`), and `args`:
`{date, pluginRoot: "${CLAUDE_PLUGIN_ROOT}", scope: "incremental" | "full", lenses: [...] (only
if the user named some), fix: true, maxParallel: 4, notes: "anything the user asked for"}`. Tell
the user in one line what will run (scope, lenses, that fixes commit on the current branch and
nothing is pushed) and that `/workflows` shows its progress. When it returns: show the summary,
ask the pending decisions one by one, turn `stories` (and decisions the user has now taken)
into backlog stories through `/keelokit:plan-backlog`, push per the project's flow, and refresh
the dashboard.

**Cut short** (the session restarted, the container was recycled, the user stopped it): the
Workflow tool's result gave a `runId` and the script's path — tell the user the runId when it
starts, and keep it. To go on, start it again with `scriptPath`, `resumeFromRunId` and the **same**
`args`: every agent that finished returns its saved result, and the rest runs again. Fixes are
safe to repeat — a fixer first looks for a commit of its root cause and doesn't make it twice.
Without the runId (a new session), start over: it's a new run, and the fixes already on the
branch are skipped the same way.

Without workflows, follow the steps below in this conversation.

## 1. Prepare

1. Read product, users, roles, critical journeys per role. List the journeys.
2. Scope — default is **incremental**: the diff since the last bug bash (`docs/bugbash/` has the
   previous reports; none → since the first commit) and only the dimensions its stories declare
   plus `ux`, `i18n`, `a11y` for any touched screen, and `integrity` whenever the diff touches a
   critical area (`.keelokit/critical.toml`) or an invariant's code. `--full` runs every lens on
   `main`. Record the sha and the lenses chosen, and why.
3. Budget: at most 4 lenses in parallel (the rest queue); lens and validator agents run on
   Sonnet. Each lens that runs the app gets its own ports (`E2E_PORT`, `E2E_MOBILE_PORT`, `PORT`)
   and, when it writes data, its own database (`docker run … postgres` on a free port, then
   `prisma:migrate:deploy` and `db:seed`).
4. Run what the project is: the app with seeded personas (`pnpm --filter ./apps/api db:seed`; add the personas the
   product needs to `apps/api/prisma/seed.ts` if they're missing — one per role and relevant
   state: new, with data, no permission, expired session), all locales — or, for a developer-facing
project, the package itself from a clean install, with personas like a newcomer following the
README, a user upgrading from the last version, and a contributor running the tests.
5. Baseline: `pnpm verify` result, so pre-existing failures aren't blamed on fixes.

## 2. Survey — one agent per lens, in parallel, no fixing yet

Each lens agent gets: its row of `dimensions.md`, the journeys, the personas, the finding format,
and a write-only findings file `docs/bugbash/<date>/<lens>.md`. It tests expected cases **and**
edges: empty, error, huge, zero/one/many, other role, other locale, 320 px, offline, twice in a
row, two at once (N parallel requests on the same resource, two cron instances), and every
promise the screens make (COPY-1). Every finding needs evidence.

## 3. Validate — adversarially

A separate agent tries to refute each finding: reproduce it from the steps on the same sha.
Not reproducible → discarded (listed as such). Merge duplicates by **root cause**, keeping the
highest severity. Re-rate severities with the rubric.

## 4. Fix — by priority, root cause first

For each confirmed finding (P0 → P3, product-rule changes excluded):
1. A test that fails, citing the finding id in its title (and the story scenario id if any).
2. The fix where the cause lives; grep every caller of what you change — siblings of the
   reported path are usually broken too.
3. **Escape analysis**: which check should have caught it (see "Automatic" in `dimensions.md`)
   and why it didn't. Add or tighten the check for the **class**, not the case: a race escaped →
   a `race()` concurrency test for that kind of write, not only for that endpoint; a lying text
   → a test of the promised behaviour and a copy line in the contract. A test, a lint rule, a
   type, a contract, an E2E step, a mutation area (`.keelokit/critical.toml`) or a new invariant
   in `domain.md` (with the user's yes: it is a product rule). If it expresses a rule, register it
   with `/keelokit:check-health` (rule + enforcer). Log the escape in `docs/escapes.md` (ESC-1): found
   by `check-bugbash`, its class, the check added.
4. One commit per finding: `fix(<area>): … (<finding id>)`; if it completes a story's scenario,
   add the `Story: <ID>` trailer. Re-walk the affected journeys.

`pnpm verify` green after every few fixes and at the end; push per the project's flow.

## 5. Report — `docs/bugbash/<date>/report.md`

- A `## Scope` section first: the sha, lenses run, personas, what couldn't be verified and why.
- Table: id · lens · severity · title · status (`fixed` / `pending decision` / `open` /
  `story <ID>`) · fix commit · **check added**.
- A `## Pending decisions` section for the human: options + recommendation each.
- Findings not fixed here — too big for one fix, or a product decision the user has now taken —
  become backlog stories through `/keelokit:plan-backlog`, each with
  `origin = "bugbash:<date> <finding id>"`; their row's status says `story <ID>`. That is how the
  dashboard shows what each bug bash fed into the backlog and the build.
- **Escapes by dimension and by class** and the checks added; compare with the previous report
  and with `docs/escapes.md` (what the build loop caught before merge) — the trend should go
  down. A dimension or class escaping two bug bashes in a row → propose a house rule for
  Keelokit. Code that produced a P0 or P1 and isn't in a critical area yet → propose adding it.
- Mutation score of the critical areas (`pnpm mutation --all`) and its survivors.
- Final `pnpm verify` and `doctor` results.

Refresh the dashboard (`/keelokit:project-dashboard`): its Bug bashes section reads these reports.
