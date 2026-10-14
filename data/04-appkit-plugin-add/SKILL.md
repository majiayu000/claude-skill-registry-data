---
name: 04-appkit-plugin-add
description: >
  Add plugins to an existing Databricks AppKit project. Covers Lakebase (PostgreSQL),
  Analytics (SQL queries + dashboards), Genie (natural language AI/BI), Files
  (UC Volumes), and Serving (Model Serving / Agent endpoints). Guides through plugin
  registration, environment variables, app.yaml configuration, and frontend integration.
  Use when asked to add a plugin to an existing app, integrate Lakebase, add analytics,
  connect a Genie space, enable file uploads, add a serving endpoint, or extend an
  AppKit project with new capabilities. Triggers on "add plugin", "add lakebase",
  "add analytics", "add genie", "add files plugin", "add serving", "add agent endpoint",
  "integrate postgres", "add database", "add dashboards", "add file browser",
  "extend app", "connect genie space", "model serving plugin". Not for creating a
  Lakebase project or managing Lakebase via CLI -- use the databricks-lakebase agent
  skill for that.
license: Apache-2.0
compatibility: Requires an existing AppKit project with Node.js v22+ and Databricks CLI >= 0.295.0
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Plugin registration is pure source editing (server.ts / app.yaml / databricks.yml) — client-agnostic.
  IDE: `npm install <plugin>` then `databricks apps deploy --profile $PROFILE`. Genie Code: add the
  plugin package to `package.json` (no local `npm install` — the platform installs it server-side on
  deploy) and deploy via `runDatabricksCli` (omit `--profile`) or the SDK fallback in `03-appkit-deploy`.
  `npx @databricks/appkit docs` is IDE-only (npx absent on Genie Code) — WebFetch the AppKit docs site instead.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: plugin-integration
  standalone: true
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills/databricks-apps"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-apps/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
---

# Add Plugins to an Existing AppKit Project

Add Lakebase, Analytics, Genie, Files, or Serving plugins to a Databricks AppKit project that has already been scaffolded.

## When to Use

- Adding a new plugin to an existing AppKit project
- Integrating PostgreSQL (Lakebase), SQL dashboards (Analytics), natural language queries (Genie), file management (Files), or model serving / agent endpoints (Serving)
- Extending an app that was scaffolded blank or needs an additional plugin

**Not for scaffolding a new app.** To create a new AppKit project (blank or with plugins), use the `01-appkit-scaffold` skill instead.

---

## Before You Begin

**IMPORTANT — The upstream AppKit docs are the source of truth, not this skill.**
AppKit may have plugins beyond those listed here. Always check the upstream docs first to discover all available plugins and get the latest configuration details:

- **Plugin docs:** https://databricks.github.io/appkit/docs/plugins/
- **CLI docs browser:** `npx @databricks/appkit docs "<plugin-name>"`
- **Full plugin list:** `npx @databricks/appkit docs "plugins"`

The bundled reference files below cover commonly used plugins as a fallback when the live docs cannot be reached. If the user requests a plugin not listed here, consult the upstream docs directly.

### Working in Genie Code (client routing)

This skill is written for the **IDE/CLI** path. Plugin registration itself — editing `server/server.ts`, `app.yaml`, and `databricks.yml` — is **identical on both clients**. Only the toolchain commands differ; apply these substitutions and you do not need to re-check per command:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `npm install <plugin>` / `npm install @databricks/appkit@latest` | add the package to `package.json` `dependencies`; the platform runs `npm install` **server-side** on deploy (no local npm on Genie Code) |
| `node -e "require('@databricks/appkit')…"` / `find node_modules …` (export check) | **IDE-only** — no local `node_modules`; confirm the export from the AppKit docs and let the server-side build + `databricks apps logs <name>` surface a bad import |
| `npx @databricks/appkit docs "<topic>"` | npx is absent (P9) — `WebFetch` https://databricks.github.io/appkit/docs/plugins/ instead |
| `databricks apps validate --profile $PROFILE` | hard-blocked — skip; rely on server-side build logs (see `03-appkit-deploy`) |
| `databricks <cmd> … --profile $PROFILE` | run via `runDatabricksCli`, **omit `--profile`** (pre-authenticated) |
| `databricks apps deploy …` | see the `03-appkit-deploy` deploy-routing contract (`runDatabricksCli`, else SDK `w.apps.deploy(... SNAPSHOT)`) |

Paths in this skill are relative to `apps_lakebase/$APP_NAME` — on Genie Code that resolves inside your git-cloned workshop project (`artifact_root`), never the read-only `.assistant/skills` copy and never `/tmp`. See `skills/genie-code-environment` for the full manifest.

---

## Step 1: Identify Which Plugin to Add

The table below covers plugins bundled with this skill. AppKit may offer additional plugins not listed here — check the upstream docs (`npx @databricks/appkit docs "plugins"`) for the full list.

| Plugin | Keywords | READ this reference |
|--------|----------|---------------------|
| **Lakebase** | PostgreSQL, database, persistence, CRUD, pg, ORM | [references/plugin-lakebase.md](references/plugin-lakebase.md) |
| **Analytics** | SQL queries, dashboards, charts, warehouse, data viz | [references/plugin-analytics.md](references/plugin-analytics.md) |
| **Genie** | Natural language, AI/BI, Genie spaces, conversational | [references/plugin-genie.md](references/plugin-genie.md) |
| **Files** | File upload/download, UC Volumes, file browser | [references/plugin-files.md](references/plugin-files.md) |
| **Serving** | Model serving, agent endpoint, inference, LLM, ML model | [references/plugin-serving.md](references/plugin-serving.md) |

If the plugin you need is listed above, **READ its reference file before proceeding** — it contains the import, config, env vars, `app.yaml` changes, frontend hooks, and gotchas. For any other plugin, consult the upstream docs directly.

> **MANDATORY:** You MUST read the plugin's reference file before making any changes. Do not treat the reference as optional supplementary material. For Lakebase specifically, the reference contains critical Terraform state management warnings that prevent destructive deploy failures. After reading, note any "Critical" or "Keep" warnings in `.vibecoding-state.md` under a "Critical Notes for Next Phase" section so downstream agents inherit the context.

---

## Step 1b: Verify the Plugin Export Exists (before importing)

Before adding the plugin to `server/server.ts`, confirm it is exported by your installed AppKit version. The server bundler (`tsdown`) does not type-check — a nonexistent import bundles silently and only fails at client build or runtime, usually after a long deploy round-trip.

```bash
cd apps_lakebase/$APP_NAME
node -e "const m = require('@databricks/appkit'); console.log(typeof m.<pluginName>);"
```

- **`function`** → plugin is available, proceed to Step 2.
- **`undefined`** → plugin is **not** in your installed AppKit version. Do NOT write `import { <pluginName> } from "@databricks/appkit"` — the bundler will accept it and your deploy will fail silently.
  - If the plugin was recently published to npm: `npm install @databricks/appkit@latest @databricks/appkit-ui@latest` and rerun the check. If this triggers a `package-lock.json` regeneration, read [03-appkit-deploy/references/lockfile-and-recreation.md](../03-appkit-deploy/references/lockfile-and-recreation.md) before deploying.
  - If the plugin is not yet published: use a custom proxy fallback. For the Serving plugin specifically, read [06-appkit-serving-wiring/references/custom-proxy-fallback.md](../06-appkit-serving-wiring/references/custom-proxy-fallback.md). For other plugins, consult the upstream docs for a supported fallback before hand-rolling one.

Confirm the method / hook names you plan to call the same way — inspect the installed `.d.ts`:

```bash
find node_modules/@databricks/appkit -name "*.d.ts" | xargs grep -l "<ExportName>" | head -5
```

> **Anti-pattern — "Import it and see if it compiles."** The server bundler (tsdown) skips type checking and will silently bundle a broken import. The error surfaces only when the client build runs tsc or the server crashes at runtime — usually after a 2-3 minute deploy round-trip. Always run the `node -e` check above before writing the import.

> **Client note — Genie Code:** the `node -e` / `find node_modules` checks are **IDE-only** (no local `node_modules`). Instead, confirm the export name against the AppKit plugin docs (WebFetch https://databricks.github.io/appkit/docs/plugins/), then deploy and treat the **server-side build logs** (`databricks apps logs <name>`) as the authoritative signal — a nonexistent import fails the platform build there with the same error.

---

## Step 2: Register the Plugin

In `server/server.ts`, import the plugin and add it to the `plugins` array:

```typescript
import { createApp, server, <pluginName> } from "@databricks/appkit";

await createApp({
  plugins: [
    server(),
    <pluginName>(),
  ],
});
```

### Multiple Plugins

Plugins compose freely — add as many as needed:

```typescript
import { createApp, server, analytics, lakebase, genie, files, serving } from "@databricks/appkit";

await createApp({
  plugins: [
    server(),
    analytics(),
    lakebase(),
    genie(),
    files(),
    serving(),
  ],
});
```

---

## Step 3: Configure Environment Variables

Each plugin requires specific environment variables. After reading the plugin reference file, add the required variables to:

1. **`.env`** — for local development
2. **`app.yaml`** — for deployed apps

See the plugin-specific reference for exact variable names and values.

> **After editing `databricks.yml` and `app.yaml`, run `databricks apps validate --profile $PROFILE` to catch YAML syntax or resource binding errors before deploy.**

---

## Step 4: Frontend Integration

Most plugins provide React hooks and/or components from `@databricks/appkit-ui/react`:

| Plugin | Key frontend exports |
|--------|---------------------|
| **Analytics** | `useAnalyticsQuery` hook, `sql` parameter helpers |
| **Genie** | `GenieChat` component, `useGenieChat` hook |
| **Files** | `DirectoryList`, `FileBreadcrumb`, `FilePreviewPanel` components |
| **Lakebase** | Server-side only (no frontend components) |
| **Serving** | `useServingStream` hook, `useServingInvoke` hook |

See the plugin-specific reference for usage examples.

---

## AppKit Documentation (Live)

For the latest API details, component props, and hook signatures:

```bash
npx @databricks/appkit docs              # documentation index
npx @databricks/appkit docs "<query>"    # search for a specific topic
npx @databricks/appkit docs --full       # full index with all API entries
```

---

## Quick Reference

| Task | Command / Action |
|------|-----------------|
| Check live plugin docs | `npx @databricks/appkit docs "<plugin>"` |
| Get warehouse ID (for Analytics/Genie) | `databricks aitools tools get-default-warehouse --profile <P>` (fallback: `databricks warehouses list`) |
| Generate query types (Analytics) | `npm run typegen` |
| Validate app | `databricks apps validate` |
| Deploy | `databricks apps deploy --profile <P>` |

---

## See Also

- Upstream platform skill: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) (tracked in `upstream_sources`).
- AppKit plugin docs: [databricks.github.io/appkit/docs/plugins/](https://databricks.github.io/appkit/docs/plugins/)

