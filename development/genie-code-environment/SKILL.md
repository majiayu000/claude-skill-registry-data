---
name: genie-code-environment
description: Session-start behavioral manifest for running this workshop inside Databricks Genie Code. Read FIRST when the client is Genie Code (the coding agent embedded in the Databricks workspace) so you begin knowing how it behaves — surface/page tool-scoping, the three execution paths (runDatabricksCli → SDK → native tools) and the "blocked ≠ impossible, try the next path" discipline, the runDatabricksCli allow-list tiers, bundle-deploy reality (--target dev mandatory, CWD pinned to the page's bundle root, FUSE create-then-validate gap), AppKit/Node reality (apps init --output-dir, no local npm but server-side build, SDK app deploy), agent-skills git-clone install, the Genie-Space deploy tiers, and how to verify a deployed app (3-hop OAuth session). Detection of WHICH client is active lives in vibecoding-state; this skill explains HOW the Genie Code client behaves. Not needed for the IDE+CLI client.
metadata:
  author: prashanth subrahmanyam
  version: "1.0"
  domain: common
  role: shared
  used_by_stages: [all]
  last_verified: "2026-06-03"
  volatility: high
  clients: [genie_code]
  evidence:
    - "retrospectives/genie-code-field-guide.md (narrative)"
    - "probe Ledger P1–P18 (00-overview.md + genie-code-refactor-handoff.md)"
    - "probe Ledger P19–P23 (uv/pip toolchain; uv-FastAPI SNAPSHOT server-side build; agent-app /invocations OAuth; Knowledge-Assistant REST via api_client.do on SDK 0.67.0; mlflow.genai eval stack incl GEPA) — agents+mlflow track session 2026-06-03"
    - "probe Ledger P24–P33 (AppKit hardening: import-specifier root-cause bisect; pristine scaffold defaults; build logs unreadable from compute; /logz human-readable; deploy ladder + ~50s cost; package-lock.json hard requirement; no-npm/local-typecheck-impossible + non-deterministic CLI allow-list; green-deploy != working app; don't-fabricate-state; P33 round-2: residual static-but-uncaught classes — unused import TS6133, empty Radix value, escaped-quote, \\uXXXX artifact, harmful value='' skill advice, image egress) — AppKit hardening sessions 2026-06-03"
    - "coding_assistant='genie-code' fork lessons (03-prompt-section-chain.md §2a, Buckets A-rationale + C)"
---

# Genie Code Environment — session-start manifest

> **Confidence tags.** `[DOC]` = Databricks documentation; `[TESTED]` = observed directly in a probe
> (probe IDs `P1`–`P18`); `[CONTESTED]` = probes once conflicted — now resolved, see §"Resolved vs.
> open"; `[INFERENCE]` = reasoned, unverified. Every behavioral claim below carries a tag + a citation.

## Why this skill exists

The single highest-leverage fix for working in Genie Code is to **begin each session knowing how it
behaves, instead of re-discovering it live in front of the user** (field guide §6.8 — the meta-fix for
every other gap). This skill is that durable manifest. `skills/vibecoding-state` **detects** which client
is active and writes the capability block; this skill explains **how the Genie Code client behaves** —
detection vs. explanation, no duplication. If `client_context == ide_cli`, you do not need this skill.

> **Record the load (G3 manifest-load gate).** The moment you have read this manifest in the current
> thread, set `environment_capabilities.genie_code_manifest_loaded: true` in the live state file. This skill
> is the **owner** of the `genie_code_manifest_loaded` preflight check (`skills/vibecoding-state`
> § *Preflight Check Registry*): on Genie Code, the first deploy / client-divergent prompt's `enter`
> **halts** until this flag is `true`, so the deploy machinery (allow-list tiers, CWD pin, FUSE gap, App
> scaffold/deploy, OAuth-session verify) is in context before you act. The check is **inert on `ide_cli`**.

## The one operating rule (read this first)

> **Match the surface to the task. If a path is blocked, try the next of the three execution paths. Never
> conclude "impossible" from one path or one page.** Every operation that was hard-blocked on one path in
> the probes had a working alternative on another. [TESTED, recurring P1–P18]

> **Don't fabricate state — report unverified facts as `unknown`.** Never claim a page, surface, deploy
> state, or capability you did not actually observe (e.g. "I'm on the Apps page" when you never navigated
> there, or "the deploy succeeded" without reading `deployment.state`). If you haven't verified it this
> turn, say so and probe it. The `runDatabricksCli` allow-list is **non-deterministic** (a verb blocked on
> one attempt can be allowed on the next), so "blocked once" is not "impossible" — and "worked once" is not
> "always works." [TESTED P32]

## 1. What Genie Code is, and why the surface matters

Genie Code is Databricks' context-aware AI assistant embedded throughout the workspace — notebooks, SQL
editor, jobs, AI/BI dashboards, the file editor, and bundle folders. It runs on **serverless compute** and
is **pre-authenticated** to the workspace (no `auth login`, no token export). [DOC; TESTED P-runtime]

**The defining fact:** Genie Code **adapts its available tools to the surface (page/asset) you are
currently on.** [DOC] A dashboard page exposes dashboard tools; a notebook page exposes code execution; a
bundle folder exposes bundle operations. This **surface-scoping** is the single most important thing to
understand — the same request can succeed on one page and be "not in the allow-list" on another. The first
move when a capability seems missing is to **navigate to the right surface**, not to conclude it's
impossible. [TESTED P10 — `apps deploy` blocked on a file-editor page]

## 2. The three execution paths

Genie Code can act on Databricks three independent ways, in order of preference:

1. **`runDatabricksCli`** — a pre-authenticated, API-routed CLI path with a per-command **allow-list** and
   safety guardrails. The primary path. [TESTED]
2. **Python SDK** — `from databricks.sdk import WorkspaceClient` via `executeCode`; auto-authenticated;
   full REST surface. This is the **most capable** path for **read and deploy** operations: it **bypasses
   the CLI allow-list** and is the
   reliable way to `w.apps.deploy(...)`, obtain a runtime bearer via `w.config.authenticate()` (note:
   `w.config.token` is `None` on serverless — see §7), and poll deployment/run state.
   **Caveat:** the SDK has **no bundle-deploy equivalent** — `bundle deploy` is a composite client-side
   operation (read `databricks.yml`, resolve templates, sync files, Terraform state), so it stays on
   `runDatabricksCli`. [TESTED]
3. **Native workspace tools** — `createAsset`, `editAsset`, `openAsset`, `readTable`, `tableSearch`,
   `findReferencesTool`, `checkPermissions`, `renderChart`, `askDataroom`, … operating on governed APIs.
   [TESTED]

A fourth, **raw shell** (`executeCode` language `sh` calling the `databricks` binary), is **blocked by a
trampoline** unless `ENABLE_DATABRICKS_CLI=true` — an escape hatch, not an intended path. [TESTED]
**Discipline:** try path 1 → if blocked, path 2 → if still blocked, path 3.

> **Second gate — the action-safety checker (distinct from the CLI allow-list).** `executeCode`
> independently screens for **mutating** operations: an unauthorized create/update/delete issued via the
> SDK or `w.api_client.do` (POST/PATCH/PUT/DELETE) can be **blocked even though it bypasses the CLI
> allow-list** — the SDK is *not* a universal escape hatch for writes. **Read-only** calls (`GET`,
> `.list()`, `DESCRIBE`) pass. Consequence for governed provisioning (e.g. Lakebase): the create path is
> the **bundle** (`bundle deploy`), and the SDK/REST role is the read-only verify GET — not a
> `POST /postgres/projects` or `PATCH …/endpoints/*` workaround. See P35.

> Full per-command allow-list tiers and the deploy/CWD/FUSE detail live in
> **[references/allow-list-and-commands.md](references/allow-list-and-commands.md)** — load on demand.

## 3. Bundle deploy reality (the spine, on Genie Code)

The deploy contract is identical to the IDE — `bundle deploy --target dev`, run through
`runDatabricksCli` (see `databricks-asset-bundles` for the canonical contract). The Genie-specific facts:

- **`--target dev` is mandatory** — a *targetless* `bundle deploy` is rejected by a **content safety
  guardrail** ("could affect staging/production"); it is **not** a page block. `--help` / `validate` /
  `summary` are pre-approved from any bundle-context page. [TESTED P4/P5/P6]
- **CWD is pinned to the current page's bundle root** — be **on the page of the bundle you are deploying**.
  There is no `cd`, no `--bundle-root` flag; you can only validate/deploy the bundle tied to the current
  page. [TESTED P2]
- **How to GET on the bundle page: open the bundle editor.** As soon as a folder contains a `databricks.yml`,
  the Databricks workspace file browser shows an **"Open in bundle editor"** affordance for that folder (and an
  "Open in editor" button at the top of the folder view). Click it to enter the **Bundle UI**, whose page CWD
  IS that bundle root — this is the reliable way to satisfy the CWD pin above, and Genie Code operates more
  predictably (deploy/run pre-approved) from inside the bundle editor than from a generic file page. So the
  canonical sequence is: write `databricks.yml` under `dp_bundle_root` → open that folder's **bundle editor** →
  run `bundle validate`/`deploy`/`run` there. A `databricks.yml not found` error means you are NOT on the
  bundle page — open the bundle editor for the `dp_bundle_root` folder; never fall back to direct SQL. [TESTED — user-observed]
- **Bundle recognition requires a git working tree — this is why `artifact_root` is a git clone.** A 3x2
  workspace probe settled the rule: a folder's `databricks.yml` shows the "Open in bundle editor" affordance
  (and a working Deploy surface) **only when it sits inside a git working tree**. A **web `git clone`** (a
  plain workspace "Folder" containing `.git`) is sufficient — recognized at the root AND in **nested**
  subfolders (so `<artifact_root>/<use_case_slug>_dab/databricks.yml` is recognized when `artifact_root` is the
  clone); a managed Databricks **Repos** object is NOT required (it is the documented fallback). A plain
  `mkdir` directory (no `.git`), even with a valid `databricks.yml`, is **NOT** recognized. This is the whole
  reason the kickstart `git clone`s the workshop repo INTO `artifact_root` (and merely *copies* the tree to the
  `.assistant/skills` discovery path). [TESTED — 3x2 workspace probe]
- **Surface a clickable bundle-editor link — don't make the operator hunt for the icon.** With the
  pre-authenticated `WorkspaceClient` (`w`): `host = w.config.host`; `o = w.get_workspace_id()`;
  `file_id = w.workspace.get_status("<dp_bundle_root>/databricks.yml").object_id`;
  `folder_id = w.workspace.get_status("<dp_bundle_root>").object_id`. Then the **bundle-editor URL** is
  `{host}/editor/files/{file_id}?o={o}&contextId=folder%3A{folder_id}` (the plain folder is
  `{host}/browse/folders/{folder_id}?o={o}`). Print the bundle-editor link and tell the operator to open it
  *before* deploy. [TESTED — user-observed]
- **🛑 Blocked `bundle` command ⇒ navigate, don't improvise. If still blocked, STOP.** `bundle deploy`/`run`
  are page-context-gated: BLOCKED on a generic file/notebook page, but they work normally from the bundle
  editor — CONFIRMED in the field, the *same* `bundle deploy` that returned "blocked by safety guardrails" from
  a file page returned "Deployment complete!" and `bundle run … SUCCESS` once the operator opened the bundle
  editor. So a "blocked" / `databricks.yml not found` message is a **wrong-page signal, not a dead end**: open
  the bundle-editor link and retry. Only if it still fails *from the bundle editor* do you STOP and report the
  blocker. Do **NOT** fall back to the Jobs/Pipelines REST API (`jobs/create`, `/api/2.0/pipelines`), the SDK,
  or direct SQL to "get the tables created" — that silently defeats version control and `bundle destroy`
  cleanup and is the exact regression this spine prevents. The REST/SDK route is an **escape hatch available
  only on explicit operator authorization.** [TESTED — user-observed]
- **Edit the *existing* on-page `databricks.yml`.** Files newly written via `createAsset`/the workspace API
  **do not reach the CLI's FUSE mount** in the same session, so "create a new bundle then validate it"
  fails — edit the bundle already on the page. [TESTED P3]
- Use `bundle validate` / `bundle summary` as safe pre-flight (pre-approved, any page). [TESTED P4]

## 4. AppKit / Node reality

- **`apps init` needs `--output-dir`** — it defaults to the workspace root (`/Workspace/<name>`), ignoring
  the page CWD. Pass `--output-dir .` (page folder) or an explicit `/Workspace/Users/<email>/<repo>`.
  [TESTED P14]
- **No local `npm`/`npx`/`corepack`** in the shell (only `node` is present), **but the Apps runtime builds
  server-side**: a SNAPSHOT deploy runs `npm install` + `npm run build` (Vite) from un-built source. A
  Genie-Code participant can edit `client/src/*.tsx` directly and redeploy with **no local Node toolchain**.
  [TESTED P9/P11/P18 — verified: an edited string appeared in the server-built JS bundle]
- **`apps deploy` via `runDatabricksCli` is unreliable** — the allow-list is **non-deterministic** (blocked
  on one attempt, allowed on the next on the same page type — not cleanly page-gated) **and CWD-defeated**
  (the enhanced build flow only fires when CWD = the project root, which never held in probes → it demands
  `APP_NAME` and falls through to the build-skipping API-direct path; the enhanced flow also runs a *local*
  build/typecheck/lint that needs `npm`, which is absent). The reliable cross-context path is the
  **SDK**: `w.apps.deploy(<name>, AppDeployment(source_code_path=…, mode=SNAPSHOT))` via `executeCode`,
  which bypasses the allow-list and runs the build server-side. **Prefer the SDK SNAPSHOT path; treat a
  blocked `apps deploy`/`apps init` as transient — retry or set `ENABLE_DATABRICKS_CLI=true`, never declare
  it impossible.** [TESTED P10/P11/P32]
- **Python toolchain IS present (Track A agent apps are Python, not Node).** Unlike npm, the **`uv`** binary
  (`/usr/local/bin/uv`), **`pip` 25.0.1**, and **Python 3.12** in a writable ephemeral venv ARE available in
  the shell — `uv pip install -e .` / `python -m pip install -e .` against a `pyproject.toml` complete
  in-session. The venv is **ephemeral** (no persistence across sessions/cluster restarts), so treat installs
  as per-session. (The field guide only tested the *Node* toolchain; this closes the Python side.) [TESTED P19]
- **A `uv`-based FastAPI app builds server-side on a SNAPSHOT deploy, exactly like Node/Vite.** The
  `agent-openai-advanced` Track A template (`pyproject.toml` + `app.yaml` with a `uv run …` command) deploys
  via the SDK `w.apps.deploy(<name>, AppDeployment(source_code_path=…, mode=SNAPSHOT))`: the platform resolves
  deps with `uv` and starts the process **server-side**, reaching `SUCCEEDED` ("App started successfully") —
  no local build. So Track A agent apps follow the **same SDK-SNAPSHOT deploy path** as AppKit, and the agent
  app can live at a clone-rooted top-level root (SNAPSHOT *copies* the source). [TESTED P20]
  - **SDK ergonomics (carry into the deploy code):** `w.apps.deploy(...)` returns a **`Wait`** object — read
    `wait.response` / `wait.deployment_id`, then poll `w.apps.get_deployment(app_name, deployment_id)` →
    `dep.status.state.value` (`IN_PROGRESS`→`SUCCEEDED`) / `dep.status.message`. The `App` object has **no
    `.status`** attribute — use `app.compute_status`, `app.active_deployment`, `app.pending_deployment`,
    `app.url`. [TESTED P20]
- **AppKit build failures trace to two import specifiers — preserve the scaffold.** A pristine `apps init`
  ships `client/src/index.css` with `@import "@databricks/appkit-ui/styles.css";` and `.tsx` importing from
  `@databricks/appkit-ui/react`. Hand-regenerating these from memory reintroduces the bare
  `@databricks/appkit-ui` (no React export) and extension-less `…/styles` (unresolvable) — the dominant
  first-deploy failure. Edit `App.tsx`/`index.css` incrementally; keep `ErrorBoundary.tsx`. [TESTED P24/P25]
- **There is no local typecheck — a regex pre-flight is the only static gate.** `npm`/`npx`/`corepack` are
  dangling symlinks and `tsc` cannot resolve `@databricks/appkit-ui`/`vite/client` without `node_modules`,
  so the import-specifier failure is **not** catchable locally. Before a (~50s) deploy, scan
  `client/src/**` via `executeCode`+regex for the two bad specifiers and fix hits first. [TESTED P30]
- **The static gate catches more than import paths; author with literal characters.** A round-2 run still
  burned deploy cycles on classes the path-only gate missed, so the regex pre-flight now also **blocks** an
  empty Radix `<SelectItem value="">` (runtime crash on menu open), an escaped single-quote in a JSX
  attribute (Vite/rolldown parse crash), and a stray `\uXXXX` escape artifact, and **flags for review** any
  unused named import (`noUnusedLocals` → hard `TS6133` build failure). Because you author `.tsx` through
  Python `open().write(...)`, prefer **triple-quoted raw strings** and write the real `'`/`"` characters —
  double-escaping is what produces the `\u0027`-style artifacts the gate flags. [TESTED P33]
- **Build logs are unreadable from compute — escalate to `/logz` in a browser.** `deployment.status.message`
  + REST only say "check /logz"; `databricks apps logs <name>` → OAuth error; `/logz` over raw HTTP → 401.
  On `FAILED`, hand the operator `<app-url>/logz` (already authenticated) to read the exact `error TS…`
  line; no-browser fallback = the 2–3-file batch ladder (redeploy small batches; the batch that flips
  green→FAILED holds the break). [TESTED P26/P27/P28]
- **`package-lock.json` is a hard requirement on SNAPSHOT.** Deleting it hard-fails the source-export phase
  in ~10s (`RESOURCE_DOES_NOT_EXIST`), before `npm install`. Never delete it as a reset. [TESTED P29]
- **A green deploy does NOT mean a working app.** A server boot crash → `FAILED` (agent-visible); a client
  runtime crash compiles and deploys `SUCCEEDED`/`ACTIVE` but renders blank — invisible to the agent.
  Require a **human render check** in the browser (the scaffold `ErrorBoundary` surfaces the stack). [TESTED P31]

## 5. Agent-Skills install

`databricks aitools install` (and the legacy `experimental aitools install`) is **hard-blocked** via
`runDatabricksCli` — the whole `aitools` verb family is not allow-listed. [TESTED P12] The working path is
**`git clone` of `databricks/databricks-agent-skills`** (git present, github.com reachable). [TESTED P13]
`npx @databricks/appkit docs` is unavailable (no npm); fetch AppKit docs via `WebFetch` instead. [TESTED P13]

## 6. Genie Spaces

Use the **RULE_8 three tiers** from `databricks-asset-bundles` ("Genie Spaces — three deploy tiers"):
Tier 1 native `genie_spaces` resource (preferred, landing ~this month), Tier 2 provisioning-job (active
fallback, both clients), **Tier 3 `createAsset({assetType:"genie", …})` + REST `PATCH`** — the Genie-Code
hybrid dev-authoring loop. [TESTED P8] `createAsset` returns a live Space ID but builds only a **shell**
(tables registered; **0 instructions, 0 benchmarks, and metric views miscategorized under
`data_sources.tables`**). Populate the FULL `serialized_space` with `PATCH /api/2.0/genie/spaces/{id}`,
then PERSIST that JSON into the bundle so a job reproduces it — Tier 3 is sanctioned for dev iteration
**only when the JSON is persisted** (an orphan Space with no file is the regression). The Space title
always carries the per-user prefix. See §6c for the create→extract-back→persist mechanics. Point to the
spine for the canonical recipe; do not restate it.

> **Genie API gotchas (TESTED).** Find Spaces with `searchAssets(assetTypes=["datarooms"])`, but the ONLY
> supported mutation is `PATCH /api/2.0/genie/spaces/{id}` with a full body — **NEVER `PATCH
> /api/2.0/data-rooms/{id}`** (it silently wipes `serialized_space` to `{}`). Export config only via
> `GET /api/2.0/genie/spaces/{id}?include_serialized_space=true` (there is **no `/export` endpoint** — it
> 404s). `readAssetById(assetType="genie")` is unsupported — use the REST GET. Every text field in
> `serialized_space` is `List[str]`; `data_sources.tables`/`metric_views` entries carry NO `id`; all IDs are
> `uuid4().hex`. The canonical contract + `_assert_sql_arrays` validator live in
> `semantic-layer/04-genie-space-export-import-api/SKILL.md`.

## 6b. Knowledge Assistants (Agent Bricks)

A Knowledge Assistant is **not a bundle resource** (no `knowledge_assistant` DABs type) — like Genie Spaces
it is an authoring-discipline exception created via the Agent Bricks **REST API**. The Genie-Code gotcha:
the bundled **`databricks-sdk 0.67.0` has no `w.knowledge_assistants` wrapper** (`hasattr → False`), **even
though the REST API is live**. Call it through the generic SDK escape hatch `w.api_client.do(<verb>, <path>,
body=…)` — **no SDK upgrade needed** (an `uv pip install -U databricks-sdk` would be ephemeral and is
unnecessary). Verified contract (mirrors the newer SDK's `KnowledgeAssistantsAPI`): [TESTED P22]

| Operation | Verb + path |
|---|---|
| list | `GET /api/2.1/knowledge-assistants` |
| create | `POST /api/2.1/knowledge-assistants` (body requires ≥1 knowledge source) |
| get / update / delete | `GET` / `PATCH` / `DELETE /api/2.1/{name}` |
| list / create sources | `GET` / `POST /api/2.1/{parent}/knowledge-sources` |
| sync sources | `POST /api/2.1/{name}/knowledge-sources:sync` |

`GET /api/2.1/knowledge-assistants` returned a live KA under Genie Code runtime auth. Some verbs also answer
on the older `/api/2.0/...` prefix (the API is mid-migration) — **prefer `2.1`, fall back to `2.0` only if a
`2.1` verb 404s.** Readiness polls via `serving-endpoints get` / `WorkspaceClient.serving_endpoints` (both
available). [TESTED P22]

## 6c. Semantic-layer authoring — native create + extract-back (TVF / Metric View / Dashboard)

The semantic layer (TVFs, Metric Views, Genie Spaces, AI/BI Dashboards) uses a **hybrid** model distinct
from the lakehouse table-DDL discipline in §8 (schemas/tables remain bundle-job-only): author the
definition file FIRST, apply it natively for a fast dev loop, extract the live asset back and diff it
against the file, then keep the Asset Bundle as the version-controlled source of truth and the non-dev
deploy mechanism. The invariant: **persisted file + live matches file + bundle validates + job ran once in
dev.** An orphan asset (no file) or drift (live ≠ file) is the regression.

| Artifact | Create natively (dev) | Extract definition back | Persist to bundle | Notes / blocked |
|---|---|---|---|---|
| TVF | `executeCode` SQL `CREATE OR REPLACE FUNCTION … RETURNS TABLE(…)`; INVOKE-test `SELECT * FROM fn(…)` | `DESCRIBE FUNCTION EXTENDED` + `information_schema.routines.routine_definition` | `.sql` with `${catalog}`/`${gold_schema}` placeholders | `SHOW CREATE FUNCTION` blocked (PARSE_SYNTAX_ERROR) |
| Metric View | `executeCode` SQL `CREATE OR REPLACE VIEW … WITH METRICS LANGUAGE YAML AS $$…$$`; validate with a `MEASURE()` query | `readTable → metadata.view_query_text` (or UC REST `GET /api/2.1/unity-catalog/tables/{full_name}.view_definition`) | `.yaml` with placeholders | `SHOW CREATE TABLE` blocked for METRIC_VIEW; appears in `information_schema.tables` (type METRIC_VIEW), NOT `.views` |
| Genie Space | `createAsset(assetType="genie", tableIdentifiers=[…])` shell → `PATCH /api/2.0/genie/spaces/{id}` full `serialized_space` (run `_assert_sql_arrays` first) | `GET /api/2.0/genie/spaces/{id}?include_serialized_space=true` (assert non-zero instructions/benchmarks/sql_functions; MV under `metric_views`) | full `serialized_space` JSON | see §6 gotchas; never PATCH `/data-rooms/{id}` |
| AI/BI Dashboard | `createAsset(assetType="dashboard")` then **AUTO-NAVIGATE** `openAsset(assetType="dashboard", assetId=<uuid>)` + print a clickable link; author widgets on the canvas | `readAssetById(assetType="dashboard", assetId=<uuid>)` → full `.lvdash.json` (UUID=published; treeNodeId=draft+path) | `.lvdash.json` | widget editing requires the canvas page; no remote widget edit |

Native authoring competence: TVFs and Metric Views are FULLY native — use the native `using-metric-views`
and `writing-sql` skills (more accurate than the workshop `01`/`02`, which are CI/validation references
only). Genie Spaces need the workshop `04` (JSON schema + `_assert_sql_arrays` validator) — load it.
Dashboards are authored by navigation, then the extracted `.lvdash.json` feeds the existing
`deploy_dashboard.py` bundle job for persistence + cross-env redeploy.

**BYO BI import — `/importBI` (native slash command; requires partner-powered AI features).** Attach a
Tableau (`.twb/.twbx/.tds/.tdsx`) or Power BI (`.pbit`) file (≤100 MB direct, or reference a UC volume
path `@/Volumes/…` for larger). It builds an **AI/BI dashboard + LOCAL (dashboard-scoped) metric views +
detected relationships** — the local views are **NOT reusable by a Genie Agent** until you **promote**
them ("Export to a Unity Catalog metric view" → your write catalog/schema). Keep only the views matching
the signed-off inventory; imported field aliases become MV synonyms. Full procedure + gotchas:
`data_product_accelerator/skills/semantic-layer/01-metric-views-patterns/references/import-bi-to-metric-view.md`.

## 7. Verifying a deployed app

A deployed App sits behind the Databricks Apps **OAuth gate** — a raw `Authorization: Bearer` token (even
SDK `w.config.token`) is rejected (`/api/health` → 401). [TESTED P16] Two working ways:

1. **Browser** (simplest manual verify) — open `w.apps.get(<name>).url`; the OAuth flow establishes the
   session. Use `apps logs <name>` for backend assertions.
2. **Programmatic** — replay the **3-hop Apps OAuth handshake in one `requests.Session()`** so the CSRF
   cookie persists through the callback (PKCE match), then reuse the session for all `/api/*` calls.
   [TESTED P17] Reusable snippet in
   **[references/app-verification.md](references/app-verification.md)**.

> **Serverless token nuance (decisive — captured live).** On serverless compute **`w.config.token` is
> `None`**; the runtime bearer that the OIDC *authorize* endpoint (Hop 2) accepts comes from
> **`w.config.authenticate()["Authorization"]`** (a short `dkea…` token). Use that for Hop 2 — a missing/raw
> token bounces Hop 2 to `/login.html`. After Hop 3 the `__Host-databricksapps` session cookie authenticates
> everything; **no `Authorization` header is needed post-handshake.** The 3-hop handshake is confirmed not
> just for static apps but against a **Track A Agent App `/invocations`** (FastAPI host, not Model Serving):
> `POST /invocations` carrying only the session cookie → `200` + a valid ChatCompletion body. [TESTED P21]

## 8. How a Genie Code session actually operates (operating model)

This is *how* a session runs — distilled from the field forks (someone ran this workshop on Genie Code):

- A **pre-authenticated `WorkspaceClient`** is available via `executeCode` (no auth step). Run Python/SQL on
  **serverless** directly.
- **Read and write *workspace* files**, not `/tmp` — `/tmp` is not durable and is not where artifacts
  belong. Build artifacts **in memory** or write to a project/workspace path.
- **Anchor every relative artifact path to `artifact_root`, never the page CWD or your home dir.**
  `artifact_root` is the workshop PROJECT root that `skills/vibecoding-state` captures into the
  `## Environment Capabilities` block (= the local repo root on `ide_cli`; the USER PROJECT path
  `/Workspace/Users/<email>/<repo>` on `genie_code`, which is a **git clone** of the workshop repo — a git
  working tree, so generated bundles/apps/docs are recognized as Databricks Asset Bundles). The skill tree is
  **copied** from `artifact_root` to `skills_install_root` = `/Workspace/Users/<email>/.assistant/skills/<repo>`
  (the read-only discovery path); artifacts build in `artifact_root`, skills load from `skills_install_root`. A
  bare `docs/design_prd.md` is
  unsafe here because Genie Code's CWD is **page-type-dependent** (the bundle root on a bundle page, the
  workspace home otherwise — see §"Resolved vs. open"), so the same relative path resolves to different
  places.   Write deliverables to `<ARTIFACT_ROOT>/<relpath>` (e.g. `<ARTIFACT_ROOT>/docs/design_prd.md`),
  filling `<ARTIFACT_ROOT>` from the captured `artifact_root`. `/tmp` remains forbidden. **The kickstart `git
  clone`s the workshop repo INTO `artifact_root`** (the workspace path), making it a git working tree where
  bundles are recognized — a bare `mkdir` does NOT (TESTED, §3). Confirm `<artifact_root>/.git` is present
  before the first write (`vibecoding-state`'s `resolve_root` / `bootstrap` step 0 do this; `git clone` if
  absent, then confirm with `os.path.exists` to clear the FUSE create-then-validate gap; a Repos-managed Git
  folder is the documented fallback). [TESTED P2]
- **The data-product bundle anchors to `dp_bundle_root`, a dedicated subdir — not the bare `artifact_root` root.**
  `skills/vibecoding-state` captures `dp_bundle_root = <artifact_root>/<use_case_slug>_dab` (e.g.
  `…/vibe-coding-workshop/booking_app_dab`). The whole DP pipeline (bronze→silver→gold→semantic) writes its
  `databricks.yml` / `src/` / `resources/` UNDER `<DP_BUNDLE_ROOT>`. Writing them at the bare `artifact_root`
  root (the framework clone itself) is the observed "one level too high" bug — the bundle then has no clean
  page-context root to deploy from. Because `bundle
  deploy`'s CWD is pinned to the current page's bundle root, `<DP_BUNDLE_ROOT>` is ALSO the page you deploy
  from: be on that folder's page, then run `bundle validate`/`deploy`/`run`. A `databricks.yml not found`
  error means you are on the wrong page — navigate to `<DP_BUNDLE_ROOT>`; never fall back to direct SQL.
- **Load every workshop skill by its clone-rooted `readSkillFile` path, never a bare repo-relative path or
  `@`-mention.** Genie Code loads skills through `readSkillFile`, which has **no repo-root-relative
  resolution**: a file under `.assistant/skills/` is loadable only as `skills/{path-after-.assistant/skills/}`.
  Because the skill tree is copied to `.assistant/skills/<clone-folder>/`, a repo-relative skill path `X/Y/SKILL.md`
  must be loaded as `readSkillFile("<skill_ref_root>/X/Y/SKILL.md")` where `skill_ref_root` is captured by
  `skills/vibecoding-state` (= `"skills/" + basename(skills_install_root)`, default `skills/vibe-coding-workshop`;
  **empty on `ide_cli`**, where `@`-mentions resolve from the workspace root). Note `skill_ref_root` is anchored
  to `skills_install_root` (the `.assistant/skills/<repo>` copy), NOT `artifact_root` (the git-cloned user
  project) — so skills keep loading from the `.assistant/skills` copy even though artifacts build in the project. Nesting depth is irrelevant —
  e.g. `data_product_accelerator/skills/bronze/00-bronze-layer-setup/SKILL.md` loads as
  `skills/vibe-coding-workshop/data_product_accelerator/skills/bronze/00-bronze-layer-setup/SKILL.md`. A bare
  `@data_product_accelerator/…` sends Genie Code on a goose chase. **`AGENTS.md` does not help here** — it is
  read once at the clone root and does **not** propagate across Agent threads, so each prompt must name the
  skill by its `skill_ref_root`-prefixed path (the `genie-code` prompt forks do exactly this). [TESTED — user-observed]
- The forks evolved a small helper shape — `w`, `read_file`/`write_file`, `run_sql`, `run_job_by_name`.
  These are **session conveniences for inspection and orchestration, NOT artifact-creation channels.**

> **SUPERSEDED — do not resurrect.** The forks also carried ad-hoc SDK-creation primitives
> (`create_job`, `create_pipeline_idempotent`, `make_job_notebook`). Those created un-versioned workspace
> state that diverged from the IDE's bundle output — **that divergence was itself the regression.** They
> are **superseded by the bundle-deploy spine** (`databricks-asset-bundles`): every artifact is a bundle
> resource brought to life by `bundle deploy`, identically on both clients. The only sanctioned in-session
> creation is RULE_8 **Tier 3** Genie-Space `createAsset` (last-resort). [decision #6/#8; M3 §2a Bucket C]
>
> **This explicitly includes data-product table DDL.** Creating Bronze/Silver/Gold schemas and tables —
> `CREATE SCHEMA`, `CREATE TABLE`, `DEEP CLONE`, `ALTER TABLE … SET TBLPROPERTIES`, `CLUSTER BY`, and the
> data load — directly via `executeCode`/`spark.sql` is the SAME regression: it produces live tables with
> no versioned bundle behind them. Those statements are the **body of a bundle job notebook**, executed by
> `bundle run`, not run by hand. The frictionless `executeCode` path is the trap (it "works" and the tables
> appear, so the gate passes) — but it bypasses the spine. If `bundle deploy` is blocked, FIX the page
> context (open the `dp_bundle_root` **bundle editor**, §"bundle-deploy reality"); do **not** fall back to
> direct SQL, the Jobs/Pipelines REST API (`jobs/create`, `/api/2.0/pipelines`), or the SDK — those are an
> escape hatch only on explicit operator authorization, and the field-confirmed fix is the bundle editor, not
> the API. Read-only inspection (`SHOW TABLES`, `DESCRIBE`, `SELECT COUNT(*)`) via `executeCode` is fine.

This section is the **canonical home** for the session operating model — the RULE_0 `client_context`
preamble and the PRE-REQUISITES Genie branch point **here** rather than re-inlining it.

## 9. Why the portability rules exist (rationale)

The single-body portability rules (authored elsewhere) exist because of these Genie behaviors — kept here
as the *explanation*, not the rule:

- **No `--var` resolver at the page.** Asset Bundle variables resolve **at deploy time**; you cannot
  "pass a var" interactively. The agnostic body states the concrete-value requirement once.
- **`/tmp` is not durable** and is not the place to write deliverables — write to a workspace/project path.
- **CWD is page-type-dependent**, so a bare relative path (`docs/design_prd.md`) is unstable across pages.
  The `artifact_root` rule above exists for this reason: resolve relative artifacts against the captured
  clone root, not the page CWD. The agnostic body keeps a single anchored form (`<ARTIFACT_ROOT>/…`).
- **No repo-root-relative skill resolution and no cross-thread `AGENTS.md`.** `readSkillFile` only resolves
  `skills/{path-after-.assistant/skills/}`, and `AGENTS.md` is read once at the clone root without propagating
  to later Agent threads. The `skill_ref_root` rule above exists for this reason: prompts (and the
  `genie-code` forks) name each skill by its `skill_ref_root`-prefixed path so it loads regardless of thread.
- **Don't rely on `jq` / raw shell** for control flow — build and inspect artifacts in-memory via the SDK.

## 10. Session ergonomics — parallel skill reads, file-write tiers, and `executeCode` timeouts

Three behaviors that materially change session speed and reliability. All [TESTED — user-observed,
Gold-design run].

- **Read every skill a phase needs in ONE batched turn.** `readSkillFile` calls run **in parallel** —
  issuing all of a phase's skill reads in a single turn returned every file successfully, whereas
  serializing them costs one full turn each. When a step's Step-1 list (or an orchestrator's "Mandatory
  Skill Dependencies") names several skills with **no inter-dependency**, load them together, not one per
  turn. [TESTED]
- **File writes — two paths, choose by situation (there is NO single-call, compute-free file-creation
  tool):**
  - **`executeCode` with `open(path,"w").write(...)`** — one call; creates and writes any workspace file
    directly; but **needs warm serverless compute** (see cold-start below). Best for creating **many** files
    or **large** content — once compute is warm.
  - **`createAsset` → `readFile` → `workspaceUpdateFile`** — a **compute-free** trio (no cold-start risk),
    but with two field-proven constraints: `workspaceUpdateFile` **cannot create a new file** (the file must
    already exist) **and requires the file to have been read in the current thread first**. So:
    `createAsset` (with `assetType: file`) makes the empty file → `readFile` satisfies the read-first guard →
    `workspaceUpdateFile` populates it. Three calls, zero compute. Best for **updating a single
    already-read file**, or writing a few files **before** compute is warm. [TESTED]
- **Verify file writes with `os.path.exists` / `os.listdir`, NOT `listFiles`.** After writing a file via
  `executeCode` `open(...)`, confirm it landed with `os.path.exists(path)` (or `os.listdir(dir)`) **in the
  same `executeCode` block**. Do **NOT** use `listFiles` to confirm a just-written file: the workspace REST
  API that backs `listFiles` lags files written through the FUSE mount, so it returns false "missing-file"
  negatives — and you waste turns recreating files that already exist. [TESTED — a live run saw
  `listFiles`=7 while `os.listdir`=12 for the same directory immediately after writing]
- **`executeCode` cold start & timeout — never starve the first call.** The **first** `executeCode` in a
  session pays a **serverless cold start of ~3–5 minutes** before any code runs; subsequent calls are warm
  (~0 s). `timeoutMinutes` **defaults to 15** (minimum 5). **Never set `timeoutMinutes` below 15** — the
  only thing a smaller budget buys is a cold-start timeout and a wasted retry (the retry then "succeeds"
  only because the failed first attempt warmed the compute). For **heavy phases** (e.g. Gold design — CSV
  parsing, per-table YAML generation, cross-table validation) set it **higher (≥ 20)**, and/or send a
  trivial `print("ready")` **warm-up** call first so the cold start is paid once, up front. [TESTED — two
  5-min timeouts on cold first calls; identical code on warm compute ran instantly]

## Resolved vs. open

The field guide flagged several items `[CONTESTED]`/`[INCOMPLETE]`. The session-2/3 probes **closed** them
— do not re-import stale doubt:

| Field-guide open item | Status now |
|---|---|
| Does the Apps runtime run `npm run build` server-side from un-built source? `[INCOMPLETE]` | **RESOLVED — yes.** [TESTED P18 / field guide §6.2] |
| Is `bundle deploy` page-context-gated or safety-guardrail-gated? `[CONTESTED]` | **Practical rule settled** (formally still `[CONTESTED]`): `--help`/`validate`/`summary` always run; a real deploy needs an explicit non-prod `--target dev` (targetless → content guardrail). Operate on that rule; don't re-litigate the *why*. [TESTED P4–P6] |
| Is the `runDatabricksCli` CWD the page's bundle root or the workspace home? `[CONTESTED]` | **Page-type-dependent:** = the **bundle root on a bundle page** (proven), = workspace **home on non-bundle pages** (notebook/AppKit). **Be on the bundle's page to deploy it.** [TESTED P2] |
| Is FUSE-invisibility of new files latency or a hard boundary? `[OPEN]` | Unresolved upstream — treat as a boundary in-session: **edit the on-page file.** [TESTED P3] |
| Does any allow-listed path reach the AppKit *enhanced* (`apps deploy`) build in-session? `[OPEN]` | Not demonstrated — use the **SDK SNAPSHOT** path (build still runs server-side). [TESTED P11/P18] |
| Does a `uv`/FastAPI (non-Node) app also build server-side on SNAPSHOT? (not in field guide) | **RESOLVED — yes.** uv-based Track A agent apps install deps + start server-side → `SUCCEEDED`. [TESTED P20] |
| Does the 3-hop OAuth handshake work against a Track A Agent App `/invocations`, and what token does Hop 2 need on serverless? (extends P16/P17) | **RESOLVED — yes; Hop 2 uses `w.config.authenticate()` (not `w.config.token`, which is `None` on serverless).** [TESTED P21] |
| Does the Knowledge Assistant API work on Genie Code's SDK 0.67.0? (agents track) | **RESOLVED — REST yes, SDK wrapper no.** `w.knowledge_assistants` absent in 0.67.0; call `/api/2.1/knowledge-assistants` via `w.api_client.do` (no upgrade). [TESTED P22] |
| Is the full `mlflow.genai` eval stack on the Genie runtime? | **RESOLVED — yes.** mlflow 3.8.1 has scorers, `evaluate`, and `optimize_prompts` (GEPA). [TESTED P23] |

## AppKit hardening ledger (P24–P41)

Live Genie-Code probes from the AppKit hardening sessions (2026-06-03), distilling an ~11-deploy booking-app
failure (P24–P32) plus a round-2 deploy of the hardened skills (P33) and the Lakebase fork probes (P34–P37d)
into preventable causes. These extend the P1–P23 ledger; the §4 AppKit facts cite these rows.

| # | Finding | Result |
|---|---|---|
| P24 | Root cause of the original build failures (reproduce-then-bisect) | Green **only** when BOTH fixed: `index.css` `@import "@databricks/appkit-ui/styles"` → `styles.css`; component imports `from "@databricks/appkit-ui"` → `/react`. Neither alone. |
| P25 | Scaffold defaults are correct | Pristine `apps init` ships `styles.css` + `/react`; the agent had overwritten correct files with hallucinated specifiers (regenerating from memory). |
| P26 | Build logs unreadable from compute | SDK/REST return only generic "check /logz"; `apps logs` → OAuth error; programmatic `/logz` → PKCE/401. No agent-visible build error. |
| P27 | `/logz` is human-readable in a browser | Authenticated `<app-url>/logz` shows the exact `App.tsx(L,C): error TS…` + full Vite/tsc pipeline. Escalation = hand the operator the link. |
| P28 | Deploy ladder localizes a break; cost = the deploy loop | 2–3-file batches localize a break; deploy ≈ 50s cold / 30s warm; file writes ≈ 0.15s → deploy loop is the bottleneck, not file I/O. |
| P29 | `package-lock.json` is a hard deploy requirement | Deleting it fails at the source-export phase in ~10s (`RESOURCE_DOES_NOT_EXIST`), before `npm install`. |
| P30 | No functional npm; local full typecheck impossible | `node` present; `npm`/`npx`/`corepack` dangling symlinks; `tsc` can't resolve appkit-ui/vite without `node_modules`. → grep/regex pre-flight is the only static gate. |
| P31 | Green deploy ≠ working app | Server boot crash → `FAILED` (visible); client runtime crash → `SUCCEEDED`/`ACTIVE` but blank (invisible) → human render check required; keep `ErrorBoundary`. |
| P32 | CLI allow-list non-deterministic; agent fabricated page-state | `apps init` blocked once then allowed on the same page type; agent reported an "Apps page" it never navigated to. SDK deploy bypasses the guardrail → reliable. Don't-fabricate-state. |
| P33 | Round-2 run of the hardened skills — residual static-but-uncaught classes | Import-specifier gate + lockfile rule + human render gate all held. New misses: deploy #1 FAILED on an unused import (`TS6133`/`noUnusedLocals`); a green deploy then crashed at runtime on `<SelectItem value="">` (Radix needs a non-empty value) — the 02-build skill's own gotcha had prescribed `value=""`. Also external Unsplash hotlinks went blank (browser egress) and `\u0027` artifacts appeared from Python-written source. → extend the regex gate (empty value, escaped quote, `\uXXXX` blocking + unused-import review), fix the harmful gotcha, mandate an `onError` data-URI image fallback. |
| P34 | Dependencies edit `package.json` directly (no local install) | Adding a dependency by editing `package.json` works — the server-side install at deploy reconciles it; the lockfile must stay in place (P29). The Lakebase setup fork edits `package.json` rather than shelling a local install. |
| P35 | `databricks.yml` resources are inert **on the SDK SNAPSHOT app-deploy path only** | A `postgres_projects` declared in `databricks.yml` never materializes via the **`w.apps.deploy(…, mode=SNAPSHOT)`** deploy (SNAPSHOT *copies source*; it does not apply the Terraform spine) → for the AppKit **app** path, provision Lakebase over REST (`POST /api/2.0/postgres/projects`) + `PATCH /api/2.0/apps/{name}` to bind. **This does NOT generalize to `bundle deploy`:** a `databricks bundle deploy --target dev` (the DP-bundle Terraform path) DOES materialize `postgres_projects` — there, declare it as a bundle resource with `default_endpoint_settings` for the caps (see the `databricks-asset-bundles` SKILL "Lakebase Resources" pattern + common-errors Error 18), NOT over REST. **Pick by deploy mechanism: SNAPSHOT app → REST create; `bundle deploy` → bundle resource.** |
| P36 | `databricks apps validate` is blocked / page-dependent | Not reliably runnable from the agent on Genie Code → substitute a local YAML structural check (parse `app.yaml` + `package.json`, assert `valueFrom: postgres` + `DB_SCHEMA` + the dependency). |
| P37b/d | Canonical Lakebase wiring boots straight to RUNNING when bound | The supported wiring shape is the `onPluginsReady(appkit)` hook on `createApp` + `appkit.server.extend(...)` — NOT `server({ autoStart: false })` + a manual `AppKit.server.start()` (the listener double-`listen()`s → boot crash; the earlier "autoStart:false broken" read was self-inflicted by omitting/duplicating `start()`). The `lakebase` **plugin** imports from the framework entrypoint (`@databricks/appkit`), not from the driver package (`@databricks/lakebase`). Binding the `postgres` resource BEFORE the first plugin-bearing deploy → RUNNING with no CRASHED hop; an unbound app carrying `valueFrom: postgres` boots CRASHED. |
| P38 | A built-in skill can be **domain-authoritative yet wrong for the governed path** | The Genie Code runtime `databricks-lakebase` skill is CLI/SDK-first (`databricks postgres …`, `w.postgres.*`) — fine for ad-hoc use, but it knows nothing about DAB `postgres_*` and its create path is blocked here. For the workshop's **bundle-only** governance the correct combo is: **create** via the `bundle deploy` `postgres_projects` resource (caps in `default_endpoint_settings`; never a second `postgres_endpoints.primary` → 400 "read_write endpoint already exists", see `databricks-asset-bundles` common-errors Error 18), and use `databricks-lakebase` only for the **read-only verify GET** + downstream connection/reverse-ETL patterns. Do not let a built-in skill's domain authority override the governed provisioning path. |
| P39 | Activation app-track deploy binds/verifies over the **already-synced** project | The `activation_deploy_validate` fork binds the app's `postgres` resource to the synced project over REST/SDK **before** the SNAPSHOT deploy. Body verified against databricks-sdk `service.apps`: `AppResourcePostgres` = `{branch, database, permission}` (both `branch` and `database` are FULL resource paths), wrapped as `AppResource{name:"postgres", postgres:{…}}` via `w.apps.update(name, App(resources=[…]))` / `PATCH /api/2.0/apps/{name}`; the only permission enum is `CAN_CONNECT_AND_CREATE`. The `database` value is the resource FQN — its id is RFC 1123 (hyphenated; read `.name` from `postgres list-databases`), NOT the underscore PG dbname `databricks_postgres`. `valueFrom: postgres` resolves ONLY when bound (unbound → CRASHED, P37b/d); a `databricks.yml` app-`resources` block stays inert on SNAPSHOT (P35). The pre-deploy static gate now also parses `app.yaml`/`databricks.yml` (assert `LAKEBASE_ENDPOINT` present; block an inert `databricks.yml` app-`resources` block; block an underscore `databricks_postgres` in a resource `database:` FQN). Deployed-app verification: the browser OAuth session is authoritative; the programmatic 3-hop replay is **best-effort** and often fails from serverless. Read-only app over synced tables → schema grants are SELECT-only even though the DB-level resource enum is `CAN_CONNECT_AND_CREATE`. |
| P40 | SNAPSHOT capture races un-flushed workspace writes → stale-source deploys (the "hall of mirrors") | `w.apps.deploy(…, mode=SNAPSHOT)` captures `<APP_ROOT>` through the workspace **export** path, which can read a file BEFORE an `open().write()` has flushed to the workspace — so a deploy ships STALE source and `FAILED`/blank while the local files look correct. This poisoned causal attribution across an ~N-deploy spiral (fixes "worked" only because a later deploy happened to capture flushed source). **Guards, all in `activation_deploy_validate`:** (1) **pre-deploy flush-verify** — read every changed file back through the export API (`w.workspace.download` / `GET /api/2.0/workspace/export`), assert content-hash == intended, backoff-loop; deterministic replacement for a blind `sleep`. (2) **post-deploy snapshot verify** — after `SUCCEEDED`, re-export and assert deployed == local; a green deploy on stale source is a **phantom success**. (3) **baseline-first bisect** — on an unexpected `FAILED`, re-deploy the last-known-good source UNCHANGED first (write-race is suspect #1); persist `last_known_good` (deployment id + changed-file hashes) in `.vibecoding-state.md`. **Attribution hygiene:** during a spiral, label each suspected cause **Verified** (reproduced with the flush-verify guard on) vs **Suspected**; never hard-code a Suspected cause into a guard until an isolated re-run promotes it. |
| P41 | `runDatabricksCli` is **blocked for the `postgres`/`lakebase` subcommands**; `w.postgres.*` is not in the pre-installed SDK | On Genie Code the `runDatabricksCli` **tool** denies `databricks postgres …` / `databricks lakebase …`, and the pre-installed SDK has no `w.postgres.*` service. Read Lakebase/Postgres state either by shelling the CLI **inside `executeCode`** (`subprocess.run(["databricks","postgres","get-endpoint",…,"--output","json"])`) or via REST `w.api_client.do("GET"/"POST", …)` (e.g. the `/api/2.0/postgres/credentials` mint the wire step already uses). The `activation_deploy_validate` cost re-checks (`get-endpoint`) and the `list-roles` auth probe were rewritten to this path — never route a `postgres`/`lakebase` command through the `runDatabricksCli` tool. |

### Phase 0 — Confirmed vs Suspected (activation deploy-spiral re-verification)

The P40 write-race poisoned attribution, so the spiral's findings were **held as Suspected** until isolated re-runs — WITH the P40 flush-verify guard in place, toggling one variable at a time — promoted or dropped each. Phase 0 (plus two follow-up discovery runs) has now RESOLVED all of L6, L7, L8, and L9, and surfaced a correction to the L5 `devDependencies` premise.

- **L8 — vite `outDir` under `build/` is platform-reserved. → REFUTED.** Two flush-verified SNAPSHOT deploys from the same pristine app changing only `outDir`: `client/dist` (scaffold default) and `../build` (project-root `build/`) BOTH deployed GREEN and `server()` served the client. `build/` is not reserved — it is auto-detect entry #3, and the server bundle itself emits to `build/index.mjs`. The non-blocking REVIEW (K) "reserved" heuristic was **removed** and replaced by a BLOCKING gate (below) in the `927`/`929` gates + `02-appkit-build`.
- **L9 — "Cannot GET /". → ROOT-CAUSED (path mismatch, not missing static code).** With ZERO static-serving code in `server/server.ts`, `server()` auto-served the client in both L8 runs. `server()` auto-detects the client bundle from a project-root-relative dir: `dist`, `client/dist`, `build`, `public`, `out`. "Cannot GET /" came only from the app's `root: "client"` + root-level `vite.config.ts` + `outDir: "../dist/client"` → emits `dist/client/`, which is in none of those. Fix: scaffold `client/vite.config.ts` (outDir → `client/dist`) or `server({ staticPath })`. **No static-serving `server.ts` was pinned** (correctly — `server()` owns it, per P37). Encoded as a BLOCKING **outDir-auto-detect gate (K)** in `927`/`929`, a `server()`-auto-serves note in `activation_wire_lakebase` + `03-appkit-deploy`, and the structural rule in `01-appkit-scaffold`. **SPA deep-link fallback — RESOLVED from AppKit source (browser probe was blocked by the token-egress guard, so resolved deterministically instead):** `StaticServer.setup()` registers `app.get("*", serveIndex)` for every non-`/api`/`/query` GET, so react-router deep links survive a hard refresh with no server code. No catch-all is authored; the `server()`-auto-serves notes now say so affirmatively.
- **L6 — Tailwind gate was v3-only. → RECALIBRATED.** The `(J)` gate hard-required v3 (`tailwind.config.*` + `postcss.config.*`), so it would false-BLOCK a correct v4 (`@tailwindcss/vite`) app. It now accepts EITHER generation and instead flags the real build-breaker: a v3 PostCSS setup that also `@import`s the v4 `@databricks/appkit-ui/styles.css`.
- **L7 — `@import "@databricks/appkit-ui/styles.css"` breaks server-side Vite. → RESOLVED (toolchain-conditional; fresh scaffold is v4).** The isolated L7 deploy (P40 guard on, only the `@import` in `index.css`) DID `FAILED` the build — but under a **v3** toolchain; the same import is correct under **v4**. A fresh-scaffold discovery run confirmed today's `databricks apps init` React template ships **Tailwind v4** (`@tailwindcss/vite` wired into `client/vite.config.ts`, no `postcss.config`/`tailwind.config`, `index.css` uses the `@import`, not `@tailwind` directives). So the scaffold's `@import` is correct as-is — "preserve verbatim" stands, now with an explicit "baseline is v4, do not swap to v3 `@tailwind`" note in `activation_build_wire` Step 4. The toolchain-aware `(J)` gate still catches the one failing combo (a v3 PostCSS setup that also `@import`s the v4 stylesheet).
- **L5 — build tools stranded in `devDependencies` fail the prod install. → CORRECTED (premise was wrong).** The fresh-scaffold run showed the pristine v4 template ships EVERY build tool (`vite`, `typescript`, `@tailwindcss/vite`, `@vitejs/plugin-react`) in `devDependencies` and deploys GREEN — the platform build installs devDeps. The `(I)` gate no longer flags `devDependencies` placement; it now BLOCKS only a build tool absent from BOTH `dependencies` and `devDependencies` (a genuinely-missing tool). Widened `(J)`'s v4 detection to accept `@tailwindcss/vite` in either `dependencies` or `devDependencies`. Encoded in `927`/`929` + `02-appkit-build`.

## Reference files

- **[allow-list-and-commands.md](references/allow-list-and-commands.md)** — the full `runDatabricksCli`
  allow-list tiers (per-command, probe-cited), deploy/CWD/FUSE detail, `apps init --output-dir`,
  `postgres list-*`, the git-clone install path.
- **[app-verification.md](references/app-verification.md)** — the 3-hop OAuth `requests.Session()` snippet
  and the server-side build evidence.

## Related skills

- **`databricks-asset-bundles`** — the canonical deploy contract + Genie-Space tiers (this skill points
  there; it does not restate deploy mechanics).
- **`databricks-expert-agent`** — surface-scoping + path-fallback discipline (cross-references this skill).
- **`skills/vibecoding-state`** — detects the client and writes the capability block; points here for the
  behavioral detail.
