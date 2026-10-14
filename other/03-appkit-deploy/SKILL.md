---
name: 03-appkit-deploy
description: >
  Deploy a Databricks AppKit application to Databricks Apps. Covers config
  validation, build verification, deployment, UI verification, error diagnosis
  with fix loop, and workspace app limit handling. Use when asked to deploy an
  AppKit app, push to production, ship the app, or troubleshoot a failed deploy.
  Triggers on "deploy app", "push to databricks", "ship app", "deploy appkit",
  "databricks apps deploy", "fix deploy error", "app won't start".
license: Apache-2.0
compatibility: Requires a built AppKit project with Node.js v22+ and Databricks CLI >= 0.295.0
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(curl:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  IDE: `databricks apps deploy --profile $PROFILE` (local Node build + bundle sync + start).
  Genie Code: run `databricks apps deploy` via `runDatabricksCli` where the project page
  allows it (omit `--profile` — pre-authenticated), else fall back to the SDK
  `w.apps.deploy(<name>, AppDeployment(source_code_path=…, mode=AppDeploymentMode.SNAPSHOT))`
  via `executeCode`. The frontend build runs **server-side** in the container, so no local
  `npm install` / `npm run build` is required on Genie Code (Gap 4 resolved).
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.2.0"
  domain: apps
  role: deploy
  standalone: true
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources: []  # Deployment workflow / fix-loop is project-specific; canonical upstream in See Also.
---

# Deploy Databricks AppKit Applications

Deploy an AppKit project to Databricks Apps, verify it runs, and fix common errors.

## When to Use

- Deploying an AppKit app to Databricks Apps (first deploy or redeployment)
- Verifying a deployed app loads correctly
- Diagnosing and fixing deploy failures
- Freeing workspace app slots when the limit is reached

**Not for scaffolding.** Use `01-appkit-scaffold` to create a new project.
**Not for building features.** Use `02-appkit-build` to implement UI and backend code.

## Prerequisites

Before deploying, ensure:

- The app builds locally (`npm run build` succeeds)
- `$APP_NAME` and `$PROFILE` are set by the calling prompt. **If a `.vibecoding-state.md` exists from a prior phase**, use the `APP_NAME`, `PROFILE`, and workspace URL values from it directly — do not re-derive them with `databricks current-user me` or `databricks auth profiles`.
- The app directory contains `app.yaml` and `databricks.yml`
- If deploying to a **different workspace** than where the app was scaffolded: update the `host` in `databricks.yml`, update `sql_warehouse_id` for the new workspace, and remove stale bundle state with `rm -rf $APP_NAME/.databricks`
- If no CLI profile exists for the target workspace, create one per **[PRE-REQUISITES §11](../../../PRE-REQUISITES.md)** before deploying (the IDE/CLI auth path; it uses `auth login`, not the interactive `configure` flow that fails in automated/agent contexts). **IDE/CLI only** — on Genie Code the runtime is already authenticated to its host workspace; skip profile creation and drop `--profile` from every command (see the routing note below).
- All commands in this skill assume the working directory is `apps_lakebase/`. Paths like `$APP_NAME/app.yaml` are relative to `apps_lakebase/`, not the repo root. On Genie Code, this is `<artifact_root>/apps_lakebase/` inside your git-cloned workshop project (NOT the read-only `.assistant/skills/` copy) — `cd` there first; never operate from `/tmp`.
- **Do NOT run `rm -f package-lock.json && npm install` locally before deploying.** The platform's `npm install` depends on lockfile stability; regenerating the lockfile locally causes `ENOTEMPTY` / `Exit handler never called` failures during platform install. See [references/lockfile-and-recreation.md](references/lockfile-and-recreation.md) for the full rule, scenario table, and recovery ladder — plus the Lakebase ownership consequences of app recreation.

### Working in Genie Code (deploy routing)

This skill is written for the **IDE/CLI path** — the commands below are correct as-is when you have a local terminal, Node.js, and a CLI profile. If you are running in **Genie Code** (no local toolchain, pre-authenticated to one workspace), apply these four substitutions to every step and you do not need to re-read this note per command:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `databricks <cmd> … --profile $PROFILE` | run `databricks <cmd> …` via `runDatabricksCli`, **omit `--profile`** (ambient auth) |
| `databricks apps deploy …` (when the project page blocks it) | SDK fallback via `executeCode`: `w.apps.deploy(<name>, AppDeployment(source_code_path=<workspace path>, mode=AppDeploymentMode.SNAPSHOT))` |
| `npm run build` / `npm run dev` (local) | **skip** — the frontend build runs server-side in the container during deploy; the build error is **not readable from compute** (`databricks apps logs <name>` → OAuth error) — read it at `<app-url>/logz` in a browser instead |
| `databricks bundle deploy` (targetless) | add `--target dev` (a targetless bundle deploy is guardrail-blocked on Genie Code) |

Everything else (config validation, log streaming, the fix loop, error table) is identical across clients. Inline `> **Client note — Genie Code:**` callouts below flag the few steps where the behavior — not just the syntax — differs. See `skills/genie-code-environment` for the full behavioral manifest.

---

## Before You Begin

**The upstream Databricks agent-skills repo and AppKit docs are the source of truth for deploy commands, platform rules, and options.**

- **Agent Skills (deploy patterns, platform rules):** https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/SKILL.md
- **Platform guide (SP permissions, runtime constraints, errors):** https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/platform-guide.md
- **App management:** https://databricks.github.io/appkit/docs/app-management
- **Configuration:** https://databricks.github.io/appkit/docs/configuration
- **AppKit docs (in-terminal):** `npx @databricks/appkit docs "app-management"`
- **CLI help:** `databricks apps deploy --help`

The bundled reference at [references/app-management.md](references/app-management.md) covers commonly used commands as a fallback when live docs cannot be reached.

> **Do NOT improvise workarounds.** If a deployment fails, check the app logs and match
> the error against the Common Errors table below. Do NOT add npm lifecycle hooks
> (`preinstall`, `postinstall`), platform-detection conditionals, or workarounds that skip
> the platform's build pipeline. These consistently cause cascading failures that are harder
> to diagnose than the original error. When in doubt, consult the authoritative sources above.

---

## Authoritative References

The [databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) repository contains the canonical AppKit deployment patterns. When in doubt, consult these references:

| Topic | Reference |
|-------|-----------|
| AppKit scaffolding, validation, workflow | [databricks-apps SKILL.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/SKILL.md) |
| Platform rules (SP permissions, runtime limits, common errors) | [platform-guide.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/platform-guide.md) |
| AppKit project structure and checklists | [appkit/overview.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/appkit/overview.md) |
| Lakebase pool, CRUD, schema ownership | [appkit/lakebase.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/appkit/lakebase.md) |
| Smoke tests and Playwright guidance | [testing.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/testing.md) |
| Lakebase two-phase deploy (Phase 1/2 binding) | [plugin-lakebase.md](../04-appkit-plugin-add/references/plugin-lakebase.md) — **read before any Lakebase deploy** |
| AppKit docs (in-terminal) | `npx @databricks/appkit docs "app-management"` |

### Platform Constraints (from platform-guide.md)

These runtime constraints affect deployment and troubleshooting:

- **Startup timeout:** App must start within 10 minutes (including dependency installation)
- **HTTP proxy timeout:** 120 seconds per request (not configurable; use WebSockets for long operations)
- **Max apps per workspace:** 100
- **Max file size:** 10 MB per file in bundle
- **Filesystem:** Ephemeral — no persistent local storage; use UC Volumes or Lakebase
- **No shell in `command`:** `app.yaml` `command` does not run in a shell; env vars outside `app.yaml` are inaccessible
- **Graceful shutdown:** SIGTERM → 15 seconds → SIGKILL
- **Logging:** Only stdout/stderr captured; file-based logs are lost on container recycle
- **Destructive updates:** `bundle run` / `apps update` does full replacement and can wipe OBO scopes

### Platform Build Pipeline

When `databricks apps deploy` pushes code to the platform, the following sequence runs inside the container:

1. **Download source** — workspace files are extracted into `/home/app/`
2. **`npm install`** — installs dependencies from `package.json` / `package-lock.json`. Runs in **production mode** (`NODE_ENV=production`), so `devDependencies` are skipped.
3. **`npm run build`** (if the `build` script exists) — compiles the project. `prebuild` hooks fire automatically before this step.
4. **Run `command`** — executes the `command` from `app.yaml` (e.g., `npm run start`)

**Hard timeout:** The entire sequence (steps 1-4) must complete within **10 minutes**. If npm install or build exceeds this, the deploy fails with `App process did not start within 10 minutes`.

**Critical rules:**

- **NEVER** add `preinstall` or `postinstall` scripts that modify `node_modules`. These create infinite loops or corrupt the install.
- **NEVER** add platform-detection conditionals (e.g., `[ "$HOME" = '/home/app' ]`) to skip build steps.
- **NEVER** modify the scaffold's `package.json` dependency versions, aliases, or overrides. If `rolldown-vite`, `@playwright/test`, or other packages were included by `databricks apps init`, leave them as-is — the scaffold is tested to deploy on the platform.
- **DO** let scaffolded `prebuild` hooks run (`appkit sync`, `appkit generate-types`). Warnings about `@ast-grep/napi` are harmless and guarded by `2>/dev/null; true`.
- **DO** note that `databricks bundle deploy` (and `databricks apps deploy` which calls it internally) uses `.gitignore` patterns for file exclusion — NOT `.databricksignore`.

**Authoritative source:** [Databricks Apps deploy — deployment logic](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy) and [post-deployment behavior](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime).

> **Client note — Genie Code (verified):** because this build pipeline runs **server-side in the container**, a Genie Code user with **no local npm** can deploy by editing source directly in the workspace and triggering a deployment via the SDK — `w.apps.deploy(<name>, AppDeployment(source_code_path=<workspace path>, mode=AppDeploymentMode.SNAPSHOT))`. This was tested end-to-end: editing an un-built `client/src/App.tsx` and redeploying produced deploy status `Building app…` and the edited string appeared in the **server-built** JS bundle (`/assets/index-*.js`). No local `npm install`/`npm run build` and no pre-synced `dist/` are required on Genie Code.

### Package Lock Management

The platform's `npm install` depends on `package-lock.json` stability. Scenario table:

| Lockfile state | Platform behavior | Action |
|----------------|-------------------|--------|
| Present, matches platform cache | Fast install | Deploy |
| Regenerated locally with foreign registry URLs | Mixed URLs → `ENOTEMPTY` / `Exit handler never called` after ~3 min | Revert or delete lockfile, redeploy |
| Absent | Fresh resolve, slower but succeeds | Acceptable for first deploy |
| Refreshed via `npm install --package-lock-only` | Keeps lockfile coherent, no tarball install | Preferred when bumping dep versions |

> **NEVER run `rm -f package-lock.json && npm install` locally before deploying.** The regenerated lockfile picks up your local npm proxy URLs, breaking platform install. If you must refresh, use `--package-lock-only`, or delete the lockfile and let the platform resolve.

> **Client note — Genie Code:** the "Absent → acceptable for first deploy" row does **NOT** apply on the SDK SNAPSHOT path. With no `package-lock.json`, the deploy **hard-fails at the source-export phase in ~10s** (`RESOURCE_DOES_NOT_EXIST`), before `npm install` runs — so the lockfile is a **hard requirement**, not optional. Never delete it as a "reset"; change deps by editing `package.json` and keeping the lockfile consistent.

Full recovery ladder + prevention rules: [references/lockfile-and-recreation.md](references/lockfile-and-recreation.md).

### App Deletion Is Destructive (Lakebase Ownership)

Deleting and recreating a Databricks App assigns a **new Service Principal UUID**. Lakebase schemas owned by the old SP become inaccessible (`permission denied for schema`, `must be owner of table`) even though `psql` as admin still sees them.

Fix, as workspace admin via `databricks psql`:

```sql
DROP SCHEMA IF EXISTS <schema_name> CASCADE;
-- Then redeploy — the new SP's DDL will recreate and own the schema.
```

Prevention: avoid app deletion. If deploys are broken, use the lockfile recovery ladder first. App deletion is a last resort.

---

## Step 1: Validate Configuration

Verify `app.yaml` has a startup command:

```bash
grep -E "build/index\.mjs|npm.*start" $APP_NAME/app.yaml
```

Accepted patterns:

- `command: ['npm', 'run', 'start']` — AppKit default (scaffold output)
- `command: [node, build/index.mjs]` — legacy / alternative

If using `npm run start`, verify the `start` script in `package.json` points to the correct built output (e.g., `node dist/server.js`).

If no startup command is present, add the default:

```yaml
command:
  - npm
  - run
  - start
```

Check that required environment bindings are present. At minimum, apps using the analytics plugin need:

```bash
grep "DATABRICKS_WAREHOUSE_ID" $APP_NAME/app.yaml
```

You should see `valueFrom: sql-warehouse`. If missing, add it:

```yaml
env:
  - name: DATABRICKS_WAREHOUSE_ID
    valueFrom: sql-warehouse
```

The calling prompt may require additional plugin-specific env vars (e.g., `LAKEBASE_ENDPOINT` for Lakebase). Validate those before proceeding.

Verify `databricks.yml` references the correct `$APP_NAME`:

```bash
grep "name:" $APP_NAME/databricks.yml | head -2
```

Note: The AppKit scaffold does not include a `name:` field in `app.yaml` — the app name is defined only in `databricks.yml` under `bundle.name` and `resources.apps`.

Run the AppKit validator to check `app.yaml` schema, resource bindings, and manifest validity:

```bash
cd $APP_NAME && databricks apps validate --profile $PROFILE
```

Fix any reported errors before proceeding.

> **Client note — Genie Code:** `databricks apps validate` is **hard-blocked** via `runDatabricksCli` (not allow-listed). Skip this gate on Genie Code. The platform runs the same validation server-side during the build pipeline, but those build logs are **not readable from compute** — `databricks apps logs <name>` returns an OAuth-token error. Read the authoritative schema/compile signal at **`<app-url>/logz` in a browser** (where you are already authenticated) instead.

**Cross-validate `valueFrom` references against `databricks.yml` resources.** Every `valueFrom:` in `app.yaml` must have a matching resource declaration in `databricks.yml`. If not, `databricks apps deploy` (which runs `bundle deploy` internally) will fail to resolve the resource and the env var will be empty at runtime.

```bash
for ref in $(grep 'valueFrom:' $APP_NAME/app.yaml | awk '{print $2}'); do
  if ! grep -q "$ref" $APP_NAME/databricks.yml 2>/dev/null; then
    echo "ERROR: app.yaml references valueFrom: $ref but no matching resource in databricks.yml"
    echo "  bundle deploy will strip manually-attached resources. Add the resource to databricks.yml."
  fi
done
```

This catches the common failure where Lakebase `postgres` resources were attached via REST API or `databricks apps update` but not declared in `databricks.yml` — `bundle deploy` resets the resource list on every deploy, stripping anything not in the bundle config.

**Check for Lakebase project conflicts with bundle declarations.** If `databricks.yml` declares `postgres_projects` and the project already exists, the correct action depends on who created it:

- **Bundle created it** (Phase 1 deploy already ran, `.databricks/` state exists): **Keep `postgres_projects`.** Terraform state tracks it. Phase 2 redeploy is idempotent. See `04-appkit-plugin-add/references/plugin-lakebase.md` for Phase 2 binding instructions.
- **Created outside the bundle** (CLI, UI, or different bundle; no `.databricks/` state): **Remove `postgres_projects`** and skip to Phase 2 binding. Terraform has no state for it.

> **CRITICAL: Never remove `postgres_projects` from `databricks.yml` after a bundle deploy has created the project.** Removing a Terraform-tracked resource declaration tells `bundle deploy` to destroy the resource. This causes a cascading failure: project destroyed → re-adding hits soft-delete retention ("already exists" for ~5-10 min) → manual recreation required outside the bundle.

```bash
PROJECT_ID=$(grep -A2 'postgres_projects:' $APP_NAME/databricks.yml | grep 'project_id:' | awk '{print $2}' | tr -d "'" | tr -d '"')
if [ -n "$PROJECT_ID" ]; then
  EXISTS=$(databricks postgres list-projects --profile $PROFILE --output json 2>/dev/null \
    | jq -e --arg pid "$PROJECT_ID" '[.[] | select(.name | contains($pid))] | length > 0' 2>/dev/null)
  BUNDLE_STATE=$(test -d "$APP_NAME/.databricks" && echo "true" || echo "false")
  if [ "$EXISTS" = "true" ] && [ "$BUNDLE_STATE" = "true" ]; then
    echo "OK: Lakebase project '$PROJECT_ID' exists and is tracked by this bundle. Keep postgres_projects."
  elif [ "$EXISTS" = "true" ] && [ "$BUNDLE_STATE" = "false" ]; then
    echo "WARNING: Lakebase project '$PROJECT_ID' exists but is NOT tracked by this bundle."
    echo "  Remove postgres_projects from databricks.yml to avoid 'already exists' Terraform errors."
    echo "  Keep only app.resources.postgres binding."
  fi
fi
```

---

## Step 2: Build

Run `npm run build` locally to catch TypeScript and compilation errors early. The deploy pipeline rebuilds on the platform, but catching errors locally avoids a slow deploy-fail-fix cycle.

```bash
cd $APP_NAME
npm run build
```

This must complete without errors. A successful build produces the output referenced by `app.yaml`'s command (typically `build/index.mjs` or `dist/server.js`).

> **Client note — Genie Code:** this local pre-build is an **IDE/CLI convenience**, not a hard gate — there is no local Node toolchain on Genie Code. **Skip Step 2 entirely** and deploy directly (Step 3); the platform runs the same `npm install` + `npm run build` **server-side** during the deploy pipeline. TypeScript/compile errors do **NOT** come back through `databricks apps logs <name>` (it returns an OAuth error from compute); they appear only at **`<app-url>/logz` in a browser** — read the exact `error TS…` line there and feed it into the Step 5 fix loop. Because there is no local `tsc`/`npm` to catch them first, run the import-specifier grep gate (see the `99-deploy_databricks_app.genie-code.md` fork, Step 2b) before deploying. (Build-runs-server-side was verified end-to-end — see the Platform Build Pipeline note above.)

Verify the build output exists before deploying:

```bash
ls build/index.mjs 2>/dev/null || ls dist/server.js 2>/dev/null || echo "WARNING: No build output found — check app.yaml command"
```

If there are TypeScript or build errors, fix them before proceeding.

### Fixing TS6133 (Unused Import/Variable) Errors

These are the most common build errors at deploy time. Before removing any symbol:

1. **Grep the full file** for each symbol name — do not rely on reading only the import section.
2. **If the import has other used names**, remove only the unused name from the import list.
3. **If ALL names from a module are unused**, delete the entire import line. Never produce `import {} from "..."` — this is a side-effect import that loads the module for nothing.
4. **If the error is on a variable declaration** (e.g., `const navigate = useNavigate()`), remove both the declaration and its import.

After fixes, run the linter on edited files before rebuilding.

---

## Step 3: Deploy

Before running the deploy, verify the lockfile has not been regenerated locally — a regenerated lockfile will often fail on the platform with `ENOTEMPTY` after ~3 minutes:

```bash
cd $APP_NAME
test -f package-lock.json && git diff --quiet -- package-lock.json \
  || echo "WARN: package-lock.json modified locally; review references/lockfile-and-recreation.md before deploy"
```

If the warning fires, read [references/lockfile-and-recreation.md](references/lockfile-and-recreation.md) and apply the recovery ladder (revert → delete → `--package-lock-only` refresh) before proceeding.

Deploy using the AppKit CLI pipeline — a single command that builds the frontend, syncs code to the workspace via bundle deploy, and starts the app:

```bash
cd $APP_NAME
databricks apps deploy --profile $PROFILE
```

This is equivalent to running `npm run build` + `databricks bundle deploy` + `databricks apps start` in sequence.

> **Client note — Genie Code:** run `databricks apps deploy` (no `--profile`) through `runDatabricksCli` from the `$APP_NAME` directory. If the project page blocks `apps deploy`, use the SDK fallback via `executeCode` — `w.apps.deploy(<name>, AppDeployment(source_code_path=<workspace path>, mode=AppDeploymentMode.SNAPSHOT))` — which triggers the same server-side build (no pre-synced `dist/` needed). Then poll `w.apps.get(<name>)` for the `Building app…` → `ACTIVE` transition; on `FAILED`, read the build error at `<app-url>/logz` in a browser (`databricks apps logs <name>` returns an OAuth error from compute).

For faster iteration after the first deploy, skip the build step:

```bash
databricks apps deploy --skip-build --profile $PROFILE
```

> **Resource-sensitive deploys:** `databricks apps deploy` runs `bundle deploy` internally, which resets the app's resource list to match `databricks.yml`. If resources were added outside the bundle (e.g., via REST API), a bundle deploy removes them. In that case, sync code first with `databricks bundle deploy --profile $PROFILE`, then trigger a run separately with `databricks apps deploy --profile $PROFILE` (which rebuilds from the already-synced workspace source without resetting resources). If no code changes are needed, skip redeployment entirely.

For Lakebase Autoscaling, use `postgres_project`/`postgres_branch`/`postgres_endpoint` resources (CLI v0.287.0+) if you want bundle-managed project lifecycle. For Lakebase Provisioned, use `database_instance` + `app.resources[].database` (CLI v0.265.0+). Do not mix the two models.

> **Client note — Genie Code (SDK SNAPSHOT path):** the `postgres_*` bundle resources and the `bundle deploy` resource-reconciliation above are the **IDE/CLI** path. On Genie Code the reliable deploy is `w.apps.deploy(<name>, AppDeployment(source_code_path=…, mode=SNAPSHOT))`, which **copies source and does NOT apply `databricks.yml` app-`resources`** (P35) — so bind the `postgres` resource over REST/SDK (`PATCH /api/2.0/apps/{name}` or `w.apps.update`) **before** the plugin-bearing deploy, never via `databricks.yml`. `valueFrom: postgres` resolves only once that resource is bound; an unbound app carrying it boots `CRASHED` (P37b/d). See `04-appkit-plugin-add/references/plugin-lakebase.md` "SNAPSHOT-path counterpart" for the exact body. Deployed-app verification on Genie Code: the browser OAuth session is the authoritative path — the programmatic 3-hop `requests.Session()` replay is best-effort and frequently fails from serverless compute.

> **Client note — Genie Code (SNAPSHOT write-race, P40):** `w.apps.deploy(…, mode=SNAPSHOT)` captures `<APP_ROOT>` through the workspace **export** path, which can read a file BEFORE an `open().write()` has flushed to the workspace — shipping STALE source that `FAILED`s or renders blank while your local files look correct. This silently poisons attribution across a deploy spiral. Guard it deterministically (do NOT rely on a blind `sleep`): (1) **pre-deploy flush-verify** — read every changed file back through the export API (`w.workspace.download` / `GET /api/2.0/workspace/export`) and assert its content-hash == what you intended, backoff-looping until all match; (2) **post-deploy verify** — after `SUCCEEDED`, re-export and assert deployed == local (a green deploy on stale source is a *phantom success*); (3) **baseline-first bisect** — on an unexpected `FAILED`, re-deploy the last-known-good source UNCHANGED first (write-race is suspect #1) and persist `last_known_good` (deployment id + changed-file hashes) in `.vibecoding-state.md`. The `activation_deploy_validate.genie-code` fork Step 3 carries the full procedure.

> **Client note — Genie Code (`server()` serves the client; "Cannot GET /" is an outDir mismatch, not missing static code):** Phase 0 confirmed `server()` auto-serves the built client from a project-root-relative auto-detected dir — `dist`, `client/dist`, `build`, `public`, or `out` (`build/` is **NOT** platform-reserved) — with **no** `express.static`/`sendFile` in `server/server.ts`. So do not author static serving. "Cannot GET /" comes from the client bundle landing OUTSIDE that list: the classic trap is a root-level `vite.config` with `root: "client"` + `outDir: "../dist/client"` (emits `dist/client/`). Fix: use the scaffold's `client/vite.config.ts` (outDir → `client/dist`) or pass `server({ staticPath: "<resolved-dir>" })`. Note the server bundle (`build/index.mjs` / `dist/server.js` in `app.yaml`'s command) is the esbuild SERVER output — unrelated to the client bundle, and further evidence `build/` is fine. SPA deep-link fallback is also built in: AppKit's `StaticServer.setup()` registers `app.get("*", serveIndex)` for every non-`/api`/`/query` GET, so react-router deep links survive a hard refresh with no server code from you (verified in AppKit source).

> **Provisioned is being retired.** Databricks is migrating Lakebase Provisioned to Autoscaling through 2026 with no customer action required. New work should use the Autoscaling `postgres_*` model; the Provisioned `database_instance` path above is retained only for pre-existing instances.

Wait for completion — typically 1-3 minutes for redeployments, 3-5 minutes for first deploys. Do not treat longer waits as failures until 7+ minutes have elapsed.

Verify the app is running before proceeding:

```bash
databricks apps get $APP_NAME --output json --profile $PROFILE | jq '{status: .status.state, compute: .compute_status.state}'
```

> **Note:** `status.state` may be `null` for up to 60 seconds after deployment even when the app is healthy. The definitive health signal is `compute_status.state: "ACTIVE"` plus clean logs showing the server is listening. If `compute` is `ACTIVE` but `status` is `null`, the app is running — proceed to Step 4.

If `compute` is not `ACTIVE`, wait 30 seconds and re-check. Use `databricks apps logs $APP_NAME --follow --profile $PROFILE` to stream logs in real-time instead of polling repeatedly.

---

## Step 4: Verify UI Loads

Run the verification script — it handles polling, retries, and health checks in one call:

```bash
bash scripts/verify-deploy.sh $APP_NAME $PROFILE
```

Exit code 0 = healthy. Exit code 1 = still starting (wait 30s, re-run). Exit code 2 = error (proceed to Step 5).

**Manual fallback** (only if `scripts/verify-deploy.sh` does not exist):

```bash
APP_URL=$(databricks apps get $APP_NAME --output json --profile $PROFILE | jq -r '.url')
echo "App URL: $APP_URL"
```

Open `$APP_URL` in a browser. You should see the React application — not an error page or JSON.

If the page shows an error or doesn't load, proceed to Step 5.

---

## Testing Deployed App APIs

Databricks Apps require authentication for all API requests. Generate a bearer token before testing:

```bash
TOKEN=$(databricks auth token --profile $PROFILE | jq -r '.access_token')
curl -s -H "Authorization: Bearer $TOKEN" "$APP_URL/api/health" | jq .
```

If `curl` returns HTML (a login page) or 401, the token has expired. Re-run the `TOKEN=...` line to refresh it. Tokens are short-lived (~1 hour).

> **Client note — Genie Code:** `databricks auth token` is **hard-blocked** via `runDatabricksCli`, and a raw `Authorization: Bearer` header (even from SDK `w.config.token`) is **rejected by AppKit's OAuth middleware** (`/api/health` → `401`; `/` → `302`). Two working ways to test a deployed app from Genie Code:
>
> 1. **Browser (simplest manual verify):** open the app URL (SDK `w.apps.get(<name>).url`) — the Databricks Apps OAuth flow establishes the session automatically. Confirm the React UI actually renders (a green deploy with a client-side runtime crash still shows a blank/error page — the scaffold's `ErrorBoundary` surfaces the stack). For backend/build logs, open `<app-url>/logz` in the same browser; `databricks apps logs <name>` returns an OAuth error from Genie compute.
> 2. **Programmatic (`executeCode`, for automated `/api/*` testing):** replay the 3-hop Apps OAuth handshake in **one `requests.Session()`** so the CSRF cookie persists (PKCE match), then reuse the session for all calls:
>    ```python
>    import requests
>    from databricks.sdk import WorkspaceClient
>    w = WorkspaceClient(); app_url = w.apps.get("<name>").url
>    s = requests.Session()
>    r1 = s.get(app_url, allow_redirects=False)                                  # __Host-databricksapps_csrf cookie
>    r2 = s.get(r1.headers["location"],                                          # Databricks OIDC authorize
>               headers={"Authorization": f"Bearer {w.config.token}"}, allow_redirects=False)
>    s.get(r2.headers["location"])                                               # /.auth/callback → session cookie
>    print(s.get(f"{app_url}/api/health").status_code)                          # now authenticated
>    ```
>    The single Session must carry the CSRF cookie through all 3 hops or the callback returns `403`.

---

## Step 5: Check Logs and Fix Errors (up to 3 iterations)

Stream the app logs:

```bash
databricks apps logs $APP_NAME --tail-lines 100 --profile $PROFILE
```

If errors exist:

1. Identify the error from the log output
2. Apply the fix in the app directory
3. Redeploy: `databricks apps deploy --profile $PROFILE`
   - For config-only changes (e.g., `app.yaml` or `databricks.yml`): `databricks apps deploy --skip-build --profile $PROFILE`
4. Check logs again

If no errors: deployment is successful.

Repeat up to 3 times. If errors persist after 3 attempts, report them for manual investigation.

> **Client note — Genie Code (fix loop):** Step 1 above (`databricks apps logs`) does **not** work — it returns an OAuth error from compute, and the SDK/REST `deployment.status.message` only says "check /logz". On `FAILED`, **first re-deploy the last-known-good source UNCHANGED** — the SNAPSHOT write-race (P40) is suspect #1 for a failure that "should have worked", and if the same bytes now deploy green the earlier failure was a stale-source capture, not your edit. If the unchanged redeploy still `FAILED`s, route to the **`/logz`-human loop**: print `<app-url>/logz`, have the operator open it (already authenticated) and paste back the exact `error TS…`/Vite line, fix that file:line, and redeploy. If no browser is available, use the **2–3-file batch ladder** (revert to the last `SUCCEEDED` source, re-apply changes 2–3 files at a time, redeploy after each ~50s batch; the batch that flips green→`FAILED` holds the break). See the `99-deploy_databricks_app.genie-code.md` fork Steps 2b/3 for the full procedure.

> **Before diagnosing errors:** Run `npx @databricks/appkit docs "app-management"` and `databricks apps deploy --help` for the latest CLI options and deployment behavior. These are the source of truth for deploy commands.

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module 'build/index.mjs'` | Build output missing or `app.yaml` command wrong | Verify `app.yaml` command matches the build output (see Step 1) and `npm run build` succeeds |
| `DATABRICKS_WAREHOUSE_ID is not set` | Analytics plugin can't find the warehouse | Add `valueFrom: sql-warehouse` for `DATABRICKS_WAREHOUSE_ID` in `app.yaml` |
| Connection refused / timeout on SQL queries | SQL warehouse starting up or stopped | Wait 30s and retry; check warehouse is running in the workspace |
| TypeScript / build errors during deploy | Compilation issues in `server/` or `client/` | Run `npm run build` locally, fix errors, redeploy |
| `ERR_MODULE_NOT_FOUND` for `@databricks/appkit` | Dependencies not installed | Verify `package.json` lists `@databricks/appkit` and `@databricks/appkit-ui`; redeploy |
| `databricks apps restart` -> command not found | `restart` subcommand does not exist | Always redeploy: `databricks apps deploy --profile $PROFILE`. There is no restart command. |
| App loses resources after `stop` then `start` | `stop`/`start` cycle detaches manually-attached resources (e.g., postgres) | Avoid `stop`/`start` for apps with non-bundle resources. Redeploy instead. |
| `databricks api put/patch` with complex JSON silently fails | The CLI `api` subcommand does not reliably handle nested JSON payloads | Use `curl` with bearer token for REST API calls that require complex JSON bodies |
| `error resolving resource postgres for env LAKEBASE_ENDPOINT: resource postgres not found` | `app.yaml` uses `valueFrom: postgres` but no `postgres` resource declared in `databricks.yml`; `bundle deploy` stripped manually-attached resources | Add `postgres_project`/`postgres_branch`/`postgres_endpoint` resources to `databricks.yml` app definition; see `05-appkit-lakebase-wiring` skill prerequisites |
| `app.yaml` syntax / validation error | Invalid YAML or bad `valueFrom` reference | Run `databricks apps validate --profile $PROFILE` to diagnose |
| Env vars not available at startup | `command` does not run in a shell; env vars outside `app.yaml` are inaccessible | Define all needed variables in `app.yaml`'s `env` section |
| `PERMISSION_DENIED` after deploy | SP missing permissions on declared resources | Ensure resources in `databricks.yml` have `permission` field; platform auto-grants on deploy |
| `File is larger than 10485760 bytes` | Bundled file exceeds 10 MB limit | Use `requirements.txt`/`package.json` for deps; do not bundle large artifacts |
| 504 Gateway Timeout | Request exceeded 120s proxy timeout | Use WebSockets for long operations; SSE may be buffered |
| OBO scopes missing after deploy | `apps update` / `bundle run` does full replacement, can wipe scopes | Re-apply OBO scopes after each deploy that modifies resources |
| `project with such id already exists in the workspace` | Lakebase project was recently deleted; platform has ~5-10 min soft-delete retention | Wait 5-10 min for retention to expire, then retry. Or create the project manually via `databricks postgres create-project` with a different project ID. If using bundle, clear `.databricks/` state before retry. |
| `Failed to create role for SP... NOT_FOUND: project id not found` | `postgres_projects` was removed from `databricks.yml`, causing Terraform to destroy the project | Re-add `postgres_projects` to `databricks.yml`. If the project ID is stuck in soft-delete, wait 5-10 min or create manually via CLI. See the Lakebase project conflict check in Step 1. |
| `ENOTEMPTY: directory not empty, rmdir '.../node_modules/<pkg>'` or `Exit handler never called` during platform `Installing packages...` | `package-lock.json` regenerated locally (e.g., after switching npm registries or running `rm -f package-lock.json && npm install`), producing mixed registry URLs the platform cache cannot satisfy | Revert the lockfile (`git checkout -- package-lock.json`); if that isn't possible, delete the lockfile and redeploy for a fresh platform resolve. Full recovery ladder + prevention rule in [references/lockfile-and-recreation.md](references/lockfile-and-recreation.md). |
| `permission denied for schema <name>` (or `relation does not exist`) after deleting and recreating the app | Recreated app got a new SP UUID; Lakebase schemas are still owned by the old SP | DROP + recreate affected schemas as a workspace admin so the new SP owns them. Detailed steps in [references/lockfile-and-recreation.md](references/lockfile-and-recreation.md) (Rule 2). |
| `unknown field: endpoint_name` / `missing required field: name` from `databricks bundle validate` | `serving_endpoint` app resource in `databricks.yml` uses `endpoint_name` — the schema field is `name` | Rename to `name:` in the `serving_endpoint` block. See [04-appkit-plugin-add/references/plugin-serving.md](../04-appkit-plugin-add/references/plugin-serving.md) ("Add Serving Endpoint as App Resource") for the correct snippet. |

The calling prompt may define additional plugin-specific errors (e.g., Lakebase connection or permission errors). Check those if the errors above don't match.

---

## If the Workspace App Limit Is Reached

If deployment fails because the workspace has hit its app limit, do NOT rename your app. Instead, free up a slot by removing the oldest stopped app:

Find the oldest stopped app:

```bash
OLDEST=$(databricks apps list -o json --profile $PROFILE | jq -r '[.[] | select(.compute_status.state == "STOPPED")] | sort_by(.update_time) | .[0] | .name // empty')
if [ -z "$OLDEST" ]; then
  echo "No stopped apps to delete. Manual workspace cleanup needed."
else
  echo "Deleting oldest stopped app: $OLDEST"
  databricks apps delete "$OLDEST" --profile $PROFILE
  sleep 10
fi
```

Retry the deployment.

If the limit error persists, repeat with the next oldest stopped app — but stop after 3 total attempts (increase the wait to 20s, then 40s between retries). If it still fails after 3 tries, stop and report the issue for manual workspace cleanup. Never delete apps in RUNNING state.

---

## Quick Reference

| Task | Command |
|------|---------|
| Build | `npm run build` |
| Validate config | `databricks apps validate --profile $PROFILE` |
| Deploy (full) | `databricks apps deploy --profile $PROFILE` |
| Deploy (skip build) | `databricks apps deploy --skip-build --profile $PROFILE` |
| Sync code only (no restart) | `databricks bundle deploy --profile $PROFILE` |
| Get app URL | `databricks apps get $APP_NAME --output json --profile $PROFILE \| jq -r '.url'` |
| Stream logs | `databricks apps logs $APP_NAME --tail-lines 100 --profile $PROFILE` |
| Follow logs live | `databricks apps logs $APP_NAME --follow --profile $PROFILE` |
| Search logs | `databricks apps logs $APP_NAME --follow --search ERROR --profile $PROFILE` |
| Stop app | `databricks apps stop $APP_NAME --profile $PROFILE` |
| Start app | `databricks apps start $APP_NAME --profile $PROFILE` |
| Delete app | `databricks apps delete $APP_NAME --profile $PROFILE` |
| List all apps | `databricks apps list --profile $PROFILE` |
| AppKit deploy help | `databricks apps deploy --help` |
| Live docs | `npx @databricks/appkit docs "app-management"` |

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) — canonical deploy guidance for Databricks Apps.
- AppKit references: [`appkit`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps/references/appkit), [App management](https://databricks.github.io/appkit/docs/app-management), [Configuration](https://databricks.github.io/appkit/docs/configuration), [Project setup](https://databricks.github.io/appkit/docs/development/project-setup), [LLM guide](https://databricks.github.io/appkit/docs/development/llm-guide).
- Databricks Apps docs: [Deploy](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy), [App runtime](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime).

