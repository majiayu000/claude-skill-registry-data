---
name: remove-app
layer: stack
description: Cleanly tear down a crouton poc/app — the inverse of /deploy. Removes the code, the Cloudflare Worker + D1 + KV (both env scopes), the app's stray branches, and closes its epic/sub-issues — with a --dry-run first and a typed confirm for anything destructive. Use when asked to "remove an app", "tear down a poc", "delete app X and its resources", or to clean up after an abandoned proof-of-concept. Counterpart to /deploy, /poc-deploy, crouton init.
allowed-tools: Bash, Read, Grep, Glob, Edit, AskUserQuestion
---

# Remove-app Skill — Teardown

One-command teardown of a crouton **poc/app** — the inverse of `/deploy`. Where
`crouton init` + `/deploy` scaffold an app and auto-provision its Cloudflare
Worker + D1 + KV, this removes all of it: **code, Cloudflare resources, GitHub
branches, and the tracking epic/sub-issues**.

> **Always `--dry-run` first.** Every destructive step has a dry-run that lists
> exactly what it would remove and touches nothing. Only run the real teardown
> after the dry-run output looks right.

## Why a CI workflow exists (the whole reason for this skill)

The interactive agent **cannot** do the two destructive halves itself:

1. **Cloudflare deletes** — no `CLOUDFLARE_API_TOKEN` in the chat environment.
2. **Branch deletes** — the chat git proxy `403`s on deleting refs.

So those run in CI via **`.github/workflows/teardown-app.yml`** (mirrors
`db-clone.yml`): Cloudflare deletes use `CLOUDFLARE_API_TOKEN`; branch deletes +
issue closes use the **Nuxt Harness App token** (like `comment-dispatch.yml`).

What the agent **can** do directly: remove the code (`rm pocs/<app>`) and the
docs references — those land as a normal **PR** on a feature branch.

## What a teardown removes

| # | Surface | Who does it | How |
|---|---------|-------------|-----|
| 1 | **Code** — `pocs/<app>` or `apps/<app>` (+ `deploy.config.json`, layers, schemas, the per-app CI caller `deploy-<app>.yml`) | the agent (PR) | `git rm -r` (default `--delete`) or `git mv` to `retired/` (`--archive`) — commit via `/commit`, open PR |
| 2 | **Cloudflare** — Worker + D1 + KV for both scopes (`<app>` and `<app>-staging`) | **CI** (`teardown-app.yml`) | `scripts/teardown-app.mjs` → `wrangler delete` / `d1 delete` / `kv namespace delete` |
| 3 | **GitHub** — delete the app's branches (`epic/<NN>-<app>`, `feat/*-<app>`, `claude/*-<app>`), close the epic + sub-issues/PRs with a note | **CI** (`teardown-app.yml`) | github-script via the Harness App token |
| 4 | **Labels** (optional) — drop `app:<app>` / `poc:<app>` from `.github/labels.yml` | the agent (PR) | `Edit` |
| 5 | **Docs/refs** — sweep `docs/` + `writeups/` for references, flag/remove | the agent (PR) | `Grep` then `Edit` |

## Guardrails

- **`pocs/` is the safe default.** A poc has no production counterpart, so the
  default `--scope staging` removes only its staging Worker/D1/KV.
- **`apps/` (production) needs an explicit, typed confirm.** Deleting a prod
  scope (`--scope prod` or `both`) aborts unless you pass `--confirm <prod-worker-name>`
  (mirrors `db-clone`'s prod guard). Never delete production data without it.
- **Back up first for prod.** Before tearing down a launched app's prod D1, take a
  backup with the `db-clone` skill (clone prod → a keep-safe env) or
  `wrangler d1 export`.
- This skill removes infrastructure on purpose — it is exempt from the
  "staging-only deploy" standing rule, but prod teardown stays deliberate +
  guarded, exactly like prod deploys.

## Workflow

### Step 1 — Identify the app & confirm it's removable
- `pocs/<app>` (safe) or `apps/<app>` (prod — extra confirm). Note its tracking
  **epic** number and `app:`/`poc:` label.
- Find its branches and resources before deleting anything:
  ```bash
  git branch -a | grep -i <app>            # branches (also try short aliases, e.g. "libcat")
  node scripts/teardown-app.mjs --app <app> --scope staging --dry-run   # CF resources
  ```

### Step 2 — Dry-run the Cloudflare plan
```bash
node scripts/teardown-app.mjs --app <app> --scope staging --dry-run
```
This needs **no credentials** — it prints the exact `wrangler` deletes it would
run (resolving names from the app's `wrangler.jsonc`, or from the crouton naming
convention `<app>[-staging]` / `<app>[-staging]-db` / `<app>[-staging]-kv` if the
code is already gone).

### Step 3 — Remove the code (agent, via PR)
On a feature branch:

**Default (`--delete`)** — delete the code outright:
```bash
git rm -r pocs/<app>                       # or apps/<app>
git rm -f .github/workflows/deploy-<app>.yml   # the per-app CI caller, if present
```

**Archive (`--archive`)** — move the code to `retired/` instead of deleting it:
```bash
git mv pocs/<app> retired/pocs/<app>       # or git mv apps/<app> retired/apps/<app>
git rm -f .github/workflows/deploy-<app>.yml   # the per-app CI caller, if present
```
Then write a **`.retired.json`** age-stamp into the archived directory (this is
written automatically during the archive flow):
```bash
cat > retired/pocs/<app>/.retired.json << 'EOF'
{
  "archivedAt": "<current ISO timestamp>",
  "sourceEpic": <epic number>,
  "sourceDir": "pocs/<app>"
}
EOF
```
Schema: `archivedAt` is the ISO-8601 date of the archive commit, `sourceEpic` is
the epic being closed, `sourceDir` is the original path (e.g. `pocs/blog` or
`apps/myapp`). The retirement digest band and GC trigger read this stamp.

> `--archive` preserves the code as browsable reference under `retired/` while
> still tearing down all live Cloudflare resources, branches, and issues (Steps 4+).
> Archive != keep-deployed — the Worker/D1/KV are deleted either way.

Then sweep docs/refs and optionally drop the label:
```bash
grep -rn "<app>" docs writeups --include=*.md --include=*.html
# remove the `app:<app>` / `poc:<app>` entry in .github/labels.yml if dropping it
```
Commit with `/commit` referencing `(#618)` / the app's epic, and open a PR
(`Closes <epic#>` in the body). Run `pnpm typecheck` first.

### Step 4 — Run the destructive teardown in CI
From the GitHub app: **Actions → "teardown-app" → Run workflow**. Inputs:

| input | for a poc | for a prod app |
|-------|-----------|----------------|
| `app` | `<app>` | `<app>` |
| `scope` | `staging` | `both` |
| `dry_run` | **`true` first**, then `false` | `true` first, then `false` |
| `delete_cloudflare` | `true` | `true` |
| `branch_patterns` | `<app>` (add aliases: `<app>,short`) | `<app>` |
| `close_issues` | epic + sub-issue numbers | epic + sub-issue numbers |
| `confirm` | _(leave blank)_ | the **prod worker name** (`<app>`) |

Run once with `dry_run: true` → read the run summary (it lists every branch,
issue, and CF resource it would touch). If correct, re-run with `dry_run: false`.

### Step 5 — Verify it's clean
- `git branch -a | grep -i <app>` → empty.
- A fresh `crouton init <app>` / `/deploy` works with **no leftover CF resource or
  branch collisions** (the acceptance test in #618).

## Reference case — library-catalog (the first dogfood)

`library-catalog` was torn down by hand (PR #606 + epic #566 closed), but two
things were left because the interactive env couldn't do them — this skill's first
real run cleans them:

- **14 stray branches:** `claude/fix-libcat-lockfile`, `claude/issue-44{1,2}-*`,
  `claude/issue-454-*`, `claude/issue-471-*`, `claude/issue-567-*`,
  `claude/issue-569-*`, `claude/library-catalog-deploy-lds0jn`,
  `epic/{428,440,453,566}-library-catalog*`, `feat/{431,455}-scaffold-library-catalog`.
- **Cloudflare staging:** Worker `library-catalog-staging`, D1
  `library-catalog-staging-db`, KV `library-catalog-staging-kv`.

Note the lockfile branch uses the alias **`libcat`**, so pass both patterns. The
dispatch:

```
Actions → teardown-app → Run workflow
  app:              library-catalog
  scope:            staging
  dry_run:          true            # then re-run with false
  delete_cloudflare:true
  branch_patterns:  library-catalog,libcat
  close_issues:     (none — #606/#566 already closed)
  confirm:          (blank — staging only)
```

## Relationship to #613

**#613** is the *automatic* post-merge cleanup of a *merged epic's* branches. This
skill is the broader, *on-demand* "remove the whole app" — code + Cloudflare +
branches + issues. They're complementary; #613 stays the automatic path.

## Credentials (CI)

`teardown-app.yml` reuses the secrets the deploy/db-clone workflows already use —
nothing new to set up:
- **`CLOUDFLARE_ACCOUNT_ID`** + **`CLOUDFLARE_API_TOKEN`** (Workers Scripts / D1 /
  KV Edit) — for the `wrangler` deletes.
- **`HARNESS_APP_ID`** + **`HARNESS_APP_PRIVATE_KEY`** (App with Contents: write +
  Issues: write) — for branch deletes + issue closes attributed to `nuxt-harness[bot]`.
