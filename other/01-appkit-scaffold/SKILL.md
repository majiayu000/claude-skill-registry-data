---
name: 01-appkit-scaffold
description: >
  Scaffold new Databricks AppKit applications using the Databricks CLI and Agent Skills.
  Creates blank or plugin-enabled AppKit projects (Lakebase, Analytics, Genie, Files).
  Use when asked to create a Databricks app, scaffold an AppKit project, bootstrap a
  new app, or set up a full-stack TypeScript Databricks application. Triggers on
  "create app", "new app", "scaffold", "AppKit", "databricks app", "blank app",
  "bootstrap app", "init app". To add a plugin to an existing app, use the
  04-appkit-plugin-add skill instead.
license: Apache-2.0
compatibility: Requires Databricks CLI >= 0.295.0 and Node.js v22+
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(git:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Scaffolding does not deploy — it delegates deploy to `03-appkit-deploy` (the `apps_deploy` contract).
  `apps init` is **usually allow-listed** on Genie Code via `runDatabricksCli` and completes without local npm
  (deps install **server-side** on deploy); the allow-list is **non-deterministic**, so if it is transiently
  blocked, retry / set `ENABLE_DATABRICKS_CLI=true` rather than declaring it impossible. Pass `--output-dir`
  so the project lands in your repo/home, not `/Workspace/<name>`. The reliable deploy spine remains the
  **SDK SNAPSHOT** path (`03-appkit-deploy`). The `aitools install` + `apps manifest` verbs are **hard-blocked** on Genie Code —
  use the `git clone` skills-install path and blank-scaffold plugin discovery instead. `npx @databricks/appkit
  docs` is IDE-only (npx absent on Genie Code → WebFetch the docs site). Omit `--profile` on Genie Code.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: scaffold
  standalone: true
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources: []  # Project-specific scaffold workflow; see See Also for canonical upstream.
---

# Scaffold Databricks AppKit Applications

Create and configure Databricks AppKit projects — blank or with plugins — using the Databricks CLI and official Agent Skills.

## When to Use

- Creating a brand-new Databricks AppKit application
- Scaffolding a blank app or one with specific plugins (Lakebase, Analytics, Genie, Files)
- Setting up a full-stack TypeScript app that deploys to Databricks Apps

**Not for adding plugins to an existing app.** Use the `04-appkit-plugin-add` skill for that.

### Working in Genie Code (client routing)

Scaffolding works on both clients; the per-step notes below carry the details. This table is the index so the skill stands alone even if you jump straight to a step:

| IDE/CLI (as written) | Genie Code substitution | Step |
|----------------------|--------------------------|------|
| `databricks aitools install` / `aitools tools` | **hard-blocked** via `runDatabricksCli` — skills are loaded in-session, so the install/gate is a no-op; if you need the files materialized, use the `git clone` install path | 1, 2 |
| `databricks apps manifest` | **hard-blocked** — discover plugins by blank-scaffolding first and reading `appkit.plugins.json`, or WebFetch the AppKit docs | 2 |
| `databricks apps init …` | **usually allow-listed** via `runDatabricksCli` (allow-list is **non-deterministic** — may be transiently blocked; if so retry or set `ENABLE_DATABRICKS_CLI=true`, don't declare it impossible); **add `--output-dir`** (`.` or an explicit home path) so it doesn't land at `/Workspace/<name>`; `⚠ npm not found` is expected (deps install server-side on deploy) | 2 |
| `databricks warehouses list` / `aitools tools get-default-warehouse` | `aitools` blocked → use `databricks warehouses list --output json` via `runDatabricksCli` | 2 |
| `npm install` / `npm run dev` (local dev server) | no local Node toolchain — skip; verify on the **deployed** app (`03-appkit-deploy`) | 3 |
| `npx @databricks/appkit docs …` | npx absent (P9) — WebFetch https://databricks.github.io/appkit/ | docs |
| `--profile <PROFILE>` on any `databricks …` | **omit** — Genie Code injects the workspace + OAuth | all |
| `databricks apps deploy` | not run from this skill — see the `03-appkit-deploy` deploy-routing contract | next |

Scaffold **into your workshop project root** (`<artifact_root>` — the local repo on IDE/CLI; `/Workspace/Users/<your-email>/vibe-coding-workshop` on Genie Code, a **git clone** of the workshop repo so generated bundles are recognized, NOT the `.assistant/skills` copy), never `/tmp`. See `skills/genie-code-environment` for the full manifest.

## Prerequisites

Before scaffolding, run the prerequisites check:

```bash
bash apps_lakebase/skills/00-appkit-navigator/scripts/validate-prereqs.sh --profile $PROFILE
```

If the script is unavailable, verify each prerequisite manually:

```bash
# 1. Databricks CLI >= 0.295.0
databricks --version

# 2. Node.js v22+
node --version

# 3. Authenticated CLI profile
databricks auth profiles

# 4. Verify access to the target workspace
databricks current-user me --host <WORKSPACE_URL>
# If this returns 403, you do not have access. Stop and ask the user for a different workspace.
```

If the CLI is not installed or outdated, see the [Databricks CLI installation guide](https://docs.databricks.com/aws/en/dev-tools/cli/tutorial).

**Profile Selection:** If the calling prompt specifies a profile, use it. Otherwise, list all profiles with `databricks auth profiles`, present them to the user, and let the user choose. Do not silently default to a profile when multiple are available.

**Programmatic profile discovery** (for scripted or multi-phase workflows):

```bash
TARGET_HOST="<WORKSPACE_URL>"
PROFILE=$(databricks auth profiles --output json 2>/dev/null \
  | jq -r --arg host "$TARGET_HOST" \
    '[.profiles[] | select(.host == $host)] | .[0].name // empty')

# If $PROFILE is empty, no CLI profile exists for this host yet:
#   IDE/CLI client → create one following PRE-REQUISITES §11, then re-run the discovery above.
#   Genie Code    → not applicable; skip this whole block (pre-authenticated, no profiles — omit --profile everywhere).
```

---

## Step 1: Install Databricks Agent Skills

Agent Skills give the AI assistant access to data exploration, CLI execution, and workspace resource discovery. They are maintained in the official repository:

**Source repository:** https://github.com/databricks/databricks-agent-skills

**IMPORTANT — Always check the upstream repo for the latest install method BEFORE installing.**
Fetch the README from the repository above (e.g. via `WebFetch`, `curl`, or browsing) to confirm the current installation commands. The install process may change between releases.

### Install to the project (all IDEs)

Clone the skills into the project-level `.agents/skills/` directory. This path follows the [agentskills.io](https://agentskills.io) cross-agent standard and is discovered by Cursor, VS Code / Copilot, Windsurf, Claude Code, and any compatible agent.

```bash
git clone --depth 1 https://github.com/databricks/databricks-agent-skills .agents/skills/databricks-skills
```

The `.agents/` directory is already in `.gitignore` — cloned skills are not committed to the repo.

**Alternative (canonical CLI method — requires Databricks CLI v1.0.0+):**

```bash
databricks aitools install
```

The CLI auto-detects your coding agent(s) and installs the stable skills to the right location (Claude Code → `~/.claude/skills/`; Cursor / Codex CLI / OpenCode / GitHub Copilot / Antigravity → their respective skill dirs). For per-skill selection use `databricks aitools install <name>`. See the [databricks-agent-skills README](https://github.com/databricks/databricks-agent-skills) and the [AI-Assisted Development docs](https://databricks.github.io/appkit/docs/development/ai-assisted-development#installing-agent-skills).

> **Note (verb name):** the canonical verb is `databricks aitools install` — the older `databricks experimental aitools install` form is deprecated. If your CLI is older than v1.0.0 and only accepts the `experimental` form, prefer the `git clone` install above (it has no CLI-version dependency), or upgrade the CLI.

> **Client note — Genie Code:** the entire `aitools` verb family (both `aitools install` and the legacy `experimental aitools install`) is **hard-blocked** via `runDatabricksCli` — it is not allow-listed, so the CLI install path does not work here. On Genie Code the Databricks skills are already available in-session, so this step is effectively a **no-op** — skip it. If you specifically need the `.agents/skills/` files materialized in the workspace, use the `git clone` path above — it is **confirmed working** on Genie Code (git is present and github.com is reachable).

### Optional: IDE-native install (in addition to the project clone)

Some IDEs have their own plugin/skill systems that provide deeper integration. These are **optional extras** on top of the project-level install above.

| IDE | Optional extra | What it does |
|-----|---------------|-------------|
| **Cursor** | `/add-plugin databricks-skills` (run in chat) | Installs to Cursor's plugin cache for cross-project availability |
| **Claude Code** | `databricks aitools install` (or `/plugin install databricks@databricks-agent-skills`) | Installs to `~/.claude/skills/` for cross-project availability |
| **VS Code / Copilot** | No extra needed | Discovers `.agents/skills/` automatically ([docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)) |
| **Windsurf** | No extra needed | Discovers `.agents/skills/` automatically ([docs](https://docs.windsurf.com/windsurf/cascade/skills)) |

### Fallback

If you cannot reach the repository, use the bundled fallback script:
```bash
bash scripts/install-agent-skills.sh
```

### Verification

After installation, confirm the skills are available. The CLI tools should respond:
```bash
databricks aitools tools --help
```

Verify the Lakebase skill is present (needed in the **Setup Lakebase** step and later):
```bash
ls .agents/skills/databricks-skills/skills/databricks-lakebase/SKILL.md 2>/dev/null \
  && echo "Lakebase skill: OK" \
  || echo "WARNING: Lakebase skill not found — re-run git clone step"
```

This is idempotent — safe to run multiple times.

---

## Step 2: Scaffold the App

### Pre-scaffold check

**GATE:** Before scaffolding, verify that agent skills from Step 1 are available:

```bash
databricks aitools tools --help
```

If this command fails or is not recognized, go back to Step 1 and install agent skills first. **Do not proceed without completing Step 1.** Checking the filesystem for skill files is NOT a substitute — the CLI integration may be broken even if files exist.

> **Client note — Genie Code:** this gate assumes the local CLI `aitools` integration (IDE path). On Genie Code the skills are loaded in-session and `apps init` (Step 2) does not depend on a local `aitools` install — if `aitools tools --help` is page-gated or unavailable, skip this gate and proceed to scaffold.

### Discover Available Plugins (Optional)

Before scaffolding with plugins, inspect the available plugin manifest:

```bash
databricks apps manifest --profile <PROFILE>
```

This shows all available plugins, which are `requiredByTemplate` (mandatory — do not add to `--features`), and what `--set` resource fields each plugin requires. Plugin names and resource keys can change between AppKit versions — always derive them from the manifest rather than guessing.

For blank scaffolds (no `--features`), this step is optional.

> **Client note — Genie Code:** `databricks apps manifest` is **hard-blocked** via `runDatabricksCli` (not allow-listed). To discover plugins/resource keys without it, do a blank scaffold first and read the generated `appkit.plugins.json` in the project, or consult the AppKit docs (via `WebFetch` of [databricks.github.io/appkit](https://databricks.github.io/appkit/)).

Reference: [Upstream SKILL.md — App Manifest and Scaffolding](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/SKILL.md)

> **Client note — Genie Code (scaffold location).** On Genie Code, `databricks apps init` **ignores** the
> `runDatabricksCli` working directory and writes the project to the **workspace root** (e.g.
> `/Workspace/<APP_NAME>`), not your home/repo folder. Verified: a flagless `apps init` landed at
> `/Workspace/<name>` and needed a re-run with `--output-dir` to reach the home directory. So on Genie Code
> **always add `--output-dir`** to the commands below — `--output-dir .` for the current folder page, or an
> explicit `--output-dir /Workspace/Users/<your-email>/<repo>`.
> *(IDE: the local CLI scaffolds into the current directory as usual — no `--output-dir` needed unless you
> want a different target.)*

### Option A: Blank Scaffold (Default)

A minimal AppKit app with only the server plugin — no data plugins.

```bash
databricks apps init --name <APP_NAME> --description "<DESCRIPTION>" --run none --profile <PROFILE>
```

### Option B: Scaffold with Plugins

Add plugins during scaffold using the `--features` flag. Combine multiple features with commas.

```bash
# Analytics only (SQL queries + dashboards)
databricks apps init --name <APP_NAME> --description "<DESC>" --features analytics --set analytics.sql-warehouse.id=<WAREHOUSE_ID> --run none --profile <PROFILE>

# Lakebase only (PostgreSQL persistence)
databricks apps init --name <APP_NAME> --description "<DESC>" --features lakebase --run none --profile <PROFILE>

# Multiple plugins
databricks apps init --name <APP_NAME> --description "<DESC>" --features analytics,lakebase,genie --set analytics.sql-warehouse.id=<WAREHOUSE_ID> --run none --profile <PROFILE>
```

**Available features:** `analytics`, `lakebase`, `genie`, `files`

### Non-Interactive Shells (AI Assistants, CI)

When running from a non-interactive shell (no TTY), `--name` is mandatory — the CLI will error with `"--name is required in non-interactive mode"` if omitted. Always provide `--name`, `--run none`, and `--profile`. *(On Genie Code, also add `--output-dir` — see the scaffold-location note above.)*

> **Client note — Genie Code:** `apps init` is **usually allow-listed** via `runDatabricksCli` and completes even though `npm` is absent (it prints `⚠ npm not found` and skips `npm install` — that is expected; deps install **server-side** on deploy). Pass `--output-dir .` (or an explicit home path) so the project does not land at `/Workspace/<name>`. The `runDatabricksCli` allow-list is **non-deterministic** (not cleanly page-gated): `apps init` may be blocked on one attempt and allowed on the next. If it is blocked, **do not declare scaffolding impossible** — retry, or set `ENABLE_DATABRICKS_CLI=true` to run the raw CLI in the shell. Whatever happens here, the **reliable deploy spine is the SDK SNAPSHOT path** (`w.apps.deploy(..., mode=AppDeploymentMode.SNAPSHOT)` via `executeCode`), which bypasses the allow-list entirely — see `03-appkit-deploy`. *blocked ≠ impossible — try the next path.*

### Naming Rules

- Max 26 characters, lowercase letters/numbers/hyphens only (no underscores)
- `dev-` prefix adds 4 chars, max 30 total

### Discover Warehouse ID (if needed)

When using `analytics` or `genie` features, you need a SQL Warehouse ID:

```bash
databricks aitools tools get-default-warehouse --profile <PROFILE>
```

If `aitools tools` is unavailable (older CLI or page-gated on Genie Code), fall back to `databricks warehouses list --output json | jq -r '.[0].id'`.

---

## Step 3: Post-Scaffold Setup

```bash
cd <APP_NAME>

# Verify scaffold produced expected files
ls app.yaml databricks.yml package.json server/server.ts
```

**Verify the server entry point uses `await`:**

```bash
grep -q 'await createApp' server/server.ts && echo "OK" || echo "FIX: replace .catch(console.error) with await"
```

If the scaffold generated `createApp({...}).catch(console.error)`, replace the file contents with the `await createApp()` pattern from [references/appkit-project-structure.md](references/appkit-project-structure.md) § "Server Entry Point Pattern."

**Note:** `app.yaml` only contains the start command — it does not include a `name` field. The app name is defined in `databricks.yml` under `resources.apps.app.name`.

```bash
npm install
npm run dev
```

If any files are missing, the scaffold may have partially failed. Re-run the scaffold command with `--run none` and try again.

This starts the dev server with hot reload on `http://localhost:8000`.

---

## What's Next

After the scaffold is working locally:

- **Build features:** Use the `02-appkit-build` skill to implement UI and backend from a PRD
- **Deploy:** Use the `03-appkit-deploy` skill for the full deploy workflow (config validation, build, deploy, UI verification, error diagnosis). Do not run `databricks apps deploy` directly from this skill — the deploy skill covers it more thoroughly.
- **Add plugins:** Use the `04-appkit-plugin-add` skill to add Lakebase, Analytics, Genie, or Files plugins

---

## Adding a Plugin to an Existing App

To add a plugin (Lakebase, Analytics, Genie, Files) to an existing AppKit project, use the **`04-appkit-plugin-add`** skill. It covers plugin registration, environment variables, `app.yaml` configuration, and frontend integration.

After scaffolding with `--features`, consult the `04-appkit-plugin-add` skill for detailed plugin configuration and frontend integration guidance.

---

## AppKit Documentation (Live)

For the latest API details, component props, and hook signatures — always consult the live docs:

```bash
npx @databricks/appkit docs              # documentation index
npx @databricks/appkit docs "<query>"    # search for a specific topic
npx @databricks/appkit docs --full       # full index with all API entries
```

> **Client note — Genie Code:** `npx`/`npm` are **absent** from the Genie Code shell (only `node` is present), so `npx @databricks/appkit docs` cannot run. Fetch the docs directly instead — `WebFetch` (or browse) [databricks.github.io/appkit](https://databricks.github.io/appkit/).

**Read** [references/appkit-project-structure.md](references/appkit-project-structure.md) § "Server Entry Point Pattern" and compare against the generated `server/server.ts`. For the full project layout and dev workflow details, see the same file.

---

## Quick Reference

| Task | Command |
|------|---------|
| Install agent skills | `git clone --depth 1 https://github.com/databricks/databricks-agent-skills .agents/skills/databricks-skills` (all IDEs) |
| Scaffold blank app | `databricks apps init --name <N> --run none --profile <P>` (Genie Code: add `--output-dir`) |
| Scaffold with analytics | `databricks apps init --name <N> --features analytics --set analytics.sql-warehouse.id=<W> --run none --profile <P>` (Genie Code: add `--output-dir`) |
| Get warehouse ID | `databricks aitools tools get-default-warehouse --profile <P>` (fallback: `databricks warehouses list`) |
| Explore table schema | `databricks aitools tools discover-schema catalog.schema.table --profile <P>` |
| Run ad-hoc SQL | `databricks aitools tools query "SELECT ..." --profile <P>` |
| Install deps | `cd <APP> && npm install` |
| Dev server | `npm run dev` |
| Build | `npm run build` |
| Validate | `databricks apps validate` |
| Deploy | `databricks apps deploy --profile <P>` |
| Browse AppKit docs | `npx @databricks/appkit docs` |

> **Client note — Genie Code:** in this table, **omit `--profile`** and run `databricks …` via `runDatabricksCli`; **add `--output-dir`** to `apps init`; replace `npx @databricks/appkit docs` with a WebFetch of the docs site; and use the `git clone` row (not `aitools`) to install skills. See the "Working in Genie Code" routing table above.

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) — canonical CLI scaffold patterns and Apps platform reference.
- AppKit docs hub: [databricks.github.io/appkit](https://databricks.github.io/appkit/)

