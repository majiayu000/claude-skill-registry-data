---
name: blueprint-authoring
description: Compose, check, and iterate Amdahl workflow recipes (blueprints) for the console's Workflows surface — and route "make this recur" asks to Routines. Use when the user wants to create / edit / fork / validate a workflow (blueprint), save a multi-step GTM workflow as a reusable recipe, customize a starter, schedule recurring work, or learn the blueprint DSL. Workflow authoring is a console capability — the `blueprints` MCP tool was retired and the endpoints behind the console aren't reachable with an external API key; over MCP, recurring work is a Routine (`agents` tool, a cron that fires a Chat) and one-shot deep work is a Chat (`agents` `start_chat`).
---

# Amdahl blueprint authoring

When the user wants to **save a repeatable multi-step workflow as a reusable recipe**, or to **create / edit / fork / validate** an Amdahl blueprint (the console calls them **Workflows**), your job is to **compose and check the DSL body with them, then hand off to the console's Workflows surface** — where validate, create, fork, and publish run. Authoring is console-only: the `blueprints` MCP tool was **retired**, and the endpoints behind the console are not on the public API (an external API key gets `403 not_on_public_api`). Never present an API call as the authoring path.

**Route the ask first — Routine or Workflow?**

- The user wants a **standing, scheduled refresh** in plain language ("every Monday, refresh the pipeline report") → don't author a blueprint. Create a **Routine** with the connected Amdahl MCP `agents` tool (`create_routine` with `name` + `prompt` + `cron`): a Routine is a cron that fires a Chat — one server-side Master agent turn in a fresh Session — each occurrence. `run_routine_now` fires one immediately. (Mind `actions_allowed` on its config: absent = ALL outbound actions allowed; name a list to narrow, `[]` to disable.)
- The user wants **one-shot deep work run server-side** → the MCP `agents` tool's Chat (`start_chat` → poll `chat_status` → `respond`); set `depth: 'deep'` for a thorough investigation.
- The user wants the **fully-typed, step-by-step contract** — declared inputs/outputs, a validated step graph, forkable starters → author a **Workflow (blueprint)** per this skill: compose + explain the body, then point the user at the console's Workflows surface to validate and save it.

Rollout note: the v2 surface is enabled per workspace — if this session's tool list still carries a `blueprints` tool (and no `search`/`agents`), the workspace is on the pre-rollout surface: author/run blueprints with that tool as before and skip the Routine routing above.

If an MCP call fails on auth, tell the user to run `/amdahl-gtm:setup`.

Hold this mental model and keep the user on it:

- A blueprint is a **structured recipe (a typed DSL artifact) with two ways to run.** The platform runs Workflows **headlessly** (fired from the console, and cron schedules fired server-side); an agent in the console reading the recipe can also **walk it interactively**, making the primitive calls itself (`data.query`, `external_search.execute`, `artifacts.create`, ...).
- **Blueprints are off MCP and off the public API.** Never tell the user to author or run a blueprint from an MCP session or an API-key script; from MCP the automation surfaces are Routines and Chat (both the `agents` tool), plus the fast-lane `search` tool for quick synchronous lookups.
- `policy.tool_allowlist` is **load-bearing on headless runs** — the platform derives the run's scopes from it (least-privilege) — and guidance for an interactive walker. `timeout_seconds` and `cost_cap_usd` are advisory authoring metadata.
- A cookbook *recipe/prompt* (paste-into-Claude text) is a DIFFERENT thing from an in-app *blueprint* (the DSL artifact). If the user conflates them, clarify once.

## Where each job lives (console Workflows surface)

| Job | Where |
|---|---|
| Browse every blueprint the workspace sees (Amdahl starters + tenant rows) | The Workflows list |
| Read one blueprint's full v1 DSL body | Open it from the list (starters resolve by slug) |
| The 8 step kinds with fields + example bodies | The step-kind reference in the editor (also the DSL reference on docs.amdahl.ai) |
| Registered `prompt://` fragments | The fragment browser (filter by scheme; open one for its text) |
| Dry-run a draft body through the moat | The editor's **Validate** action — returns `{ valid, errors[] }` |
| Persist a new tenant blueprint | **Save as draft** in the editor |
| Edit a tenant blueprint (content is REPLACE-semantic) | Edit + save (always the whole body) |
| Soft-archive / restore | The blueprint's actions menu |
| Copy a starter or tenant blueprint into a fresh draft | The **Fork** action (new slug + name) |
| Fire one headless run of a published workflow | **Run** on the blueprint's page |

## The loop you drive

Always: **orient -> draft -> hand off to validate -> iterate.** Never let the user save before validating.

1. **Orient.** If the user's ask is close to an existing recipe, have them open that starter in the Workflows list (forking beats authoring from scratch) and paste you its body; otherwise pull what you need from the DSL anatomy below.
2. **Draft.** Compose the v1 DSL body in your reasoning loop. Show it to the user, explain the step graph, and self-check it against the anatomy + the error table before handing it over.
3. **Validate.** Have the user paste the body into the console editor and run **Validate**. Fix the returned `errors[]` with them by `code` (see the table). Re-validate until `valid: true`.
4. **Create or fork.** Save as draft for net-new; or Fork a starter, then edit the fork. The fork lands with a fresh id, `version` reset to `1.0.0`, `status: "draft"`.
5. **Iterate.** Edit, re-validate, re-save the full body. Bump `identity.version` on a real change. Publish when the user is happy.

## DSL anatomy (what a valid body needs)

Top-level (strict — no extra keys): `schema_version` (`"1.0.0"`), `identity`, `inputs`, `outputs`, `policy`, `trigger`, `steps`, `outputs_mapping`, optional `metadata`.

- `identity`: `slug` (`[a-z0-9-]`, 3-60), `name` (<=80), `description` (**30-500 chars**), `version` (semver). Optional `category`, `tags`, `icon`.
- `inputs`: typed declarations (`string` / `integer` / `number` / `boolean` / `date` / `datetime` / `enum` / `json` / `artifact_ref` / `artifact_ref_list`), each with `name` (snake_case), optional `required`, optional `validate` (e.g. `enum` needs `validate.values`; `artifact_ref` needs `validate.artifact_type`).
- `outputs`: `kind` = `artifact` (with `artifact_type` + `cardinality`) | `data` (with `schema`) | `side_effect` (with `category`). May be `[]` (pure side-effect recipe).
- `steps` (non-empty): each has `kind`, unique `id`, optional `output_alias`. The 8 kinds:
  - `tool` — call one op: `tool` (op id) + `args`. The workhorse.
  - `llm` — `effort` (`fast`/`medium`/`deep`/`research`) + `prompt` + `output_schema` (required); optional `prompt_resources`, `input_data`, `temperature`.
  - `loop` — `over` + `as` + `step`, optional `parallel`.
  - `branch` — `condition` + `if_true`, optional `if_false`.
  - `parallel` — `steps` (>=1), optional `merge`.
  - `blueprint` — compose a sub-blueprint: `blueprint` + `args`.
  - `transform` — `input` + JSONata `expression`.
  - `assert` — `condition` + `halt_message`.
- References (`$`): `$inputs.NAME`, `$STEP_ID` / `$alias`, `$alias.field`, `$now`, `$today`, `$random_uuid`, `$secret.NAME` (never goes into prompts), `$builtin.X`. Prefer referencing `output_alias` over the raw step id.
- `prompt://<scheme>/<id>` in an `llm` step's `prompt_resources` inlines a shared fragment. Two schemes: `content_writer/*` (grounding_rules, audience_scoping, channel_budget, cta_synthesis, hook_patterns, ...) and `researcher/*` (topic_decomposition, evidence_synthesis, confidence_scoring, metric_grounding, document_render, ...). DON'T guess ids — have the user check the console's fragment browser.
- `policy.tool_allowlist` (>=1 op id) is required — headless runs derive their scopes from it, so keep it honest. `trigger`: `{ "manual": { "enabled": true } }`; `schedule` (cron) also ships, though for a plain-language cadence a Routine is usually the better fit.
- `outputs_mapping`: map each declared output name to a `$`-reference (e.g. `{ "report": "$report_id" }`); `{}` when `outputs` is `[]`.

A minimal valid body:

```json
{
  "schema_version": "1.0.0",
  "identity": { "slug": "topic-pulse", "name": "Topic pulse", "description": "Runs a fused internal + external search on a topic and returns the brief. The smallest reusable research recipe.", "version": "1.0.0" },
  "inputs": [{ "name": "topic", "type": "string", "required": true, "validate": { "min_length": 3, "max_length": 300 } }],
  "outputs": [{ "kind": "data", "name": "brief", "schema": { "type": "object" } }],
  "policy": { "tool_allowlist": ["external_search.execute"] },
  "trigger": { "manual": { "enabled": true } },
  "steps": [{ "id": "pulse", "kind": "tool", "tool": "external_search.execute", "args": { "action": "enrich_topic", "topic": "$inputs.topic" }, "output_alias": "pulse_result" }],
  "outputs_mapping": { "brief": "$pulse_result" }
}
```

## Validation errors and how to fix them

The console's Validate (and save) return errors keyed by a stable `code`:

- `schema_error` — body failed the strict v1 schema (wrong field, missing required, bad enum). Re-check the anatomy.
- `unknown_reference` — a `$alias.field` points at nothing (usually a typo). Check the step that bound the alias.
- `unknown_fragment` — a `prompt://` id isn't registered (e.g. `grounded_rules` vs `grounding_rules`). Re-check the fragment browser.
- `duplicate_step_id` — two steps share an `id` (common after copy-paste). Rename one.
- `invalid_tool_id` — a `tool_allowlist` entry isn't a real operation id.

## Operating rules

- Validate before every save. Walk the `errors[]` with the user and fix by code, don't just retry blindly.
- Edits are REPLACE-semantic: always work from the WHOLE body, never a partial patch — omitted top-level keys are dropped.
- Prefer forking a starter (`draft-piece`, `research-report`, ...) over authoring from scratch when the ask is close to an existing recipe. Starters are read-only; fork first, then edit the fork.
- Never put a literal secret in the body — reference `$secret.NAME`. A literal key is stored in plaintext on the artifact.
- When the user says "run" the blueprint: publish it in the console, then fire a run from its page (headless) — or, if what they really want is "run this on a cadence," offer a Routine instead (`agents create_routine` over MCP).
- When the user asks to do any of this from an MCP-connected chat or with an API key: route them to the console — or to Routines + Chat (both the `agents` tool) for the MCP-native equivalents.
- The full narrative guide (mental model, anatomy, two worked examples) lives at `prompts/blueprints/authoring-a-blueprint.md` — point the user there for depth.

This skill composes and checks the DSL; it stays thin and defers depth to the guide so it remains correct as the platform's starters + fragments evolve.
