---
name: 00-appkit-navigator
description: >
  Entry-point navigator for Databricks AppKit + Lakebase development. Routes
  tasks to the correct skill based on keyword detection: scaffolding, plugin
  integration, feature building, or deployment. This is a routing skill -- it
  does not generate code. It directs the agent to the correct specialized skill.
  Use this skill as the starting point for any AppKit-related task.
  Triggers on "AppKit", "Lakebase app", "Databricks app", "build app", "deploy
  app", "scaffold app", "add plugin", "AppKit project", "agent endpoint",
  "wire agent", "serving plugin", "agent app proxy", "chat history",
  "feedback".
license: Apache-2.0
clients: [ide_cli, genie_code]
coverage: full
# Client-awareness body layer added in Milestone 06 (batch 6e, criterion 3 / step 4):
# Tier-1-thin client callout (client_context via skills/vibecoding-state, skills/genie-code-environment
# pointer), npx docs IDE-gated with a Genie Code alternative, $PROFILE annotated as an IDE/CLI concept,
# and the Development-Lifecycle deploy(agnostic)/local-test(IDE-only) split — all by reference, no inline behavior.
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: meta
  role: navigator
  standalone: true
  last_verified: "2026-06-02"
  volatility: low
  upstream_sources: []  # Routing skill; canonical Apps guidance lives in databricks-agent-skills (see See Also).
---

# AppKit Lakebase Navigator

Route AppKit + Lakebase tasks to the correct specialized skill.

> **Client awareness (Tier-1-thin).** Routing is identical for every client; only the run/test/docs mechanics differ. `skills/vibecoding-state` detects and gates `client_context`; on the in-workspace agent load `skills/genie-code-environment` for behavior (pre-auth, serverless, page-context CLI, project-rooted artifacts — skills load from the `.assistant/skills` copy). The **deploy** verb is client-agnostic, but the **local dev server / E2E test** steps below are IDE/CLI-only — Genie Code verifies against the deployed app (see `03-appkit-deploy` and the routed skill's `deploy_note`). Routed prompts open with a client-specific RULE_0 preamble; follow it.

> **Genie Code first-run (once).** Two locations: `git clone` the workshop repo into your user project (`/Workspace/Users/<your-username>/vibe-coding-workshop` = `artifact_root`, git-backed so generated bundles are recognized), then **copy** the tree into `/Workspace/Users/<your-username>/.assistant/skills/vibe-coding-workshop` for skill discovery. After the copy lands, **start a NEW Agent-mode chat thread** (hard-refresh if skills don't appear) so Genie Code recurses the `.assistant/skills` copy and loads these skills. Full block: [repo-root AGENTS.md](../../../AGENTS.md) ("Genie Code" section) / [PRE-REQUISITES.md](../../../PRE-REQUISITES.md). Grounded in the [Genie Code skills docs](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills).

## Development Lifecycle

AppKit apps follow a branch-aware development lifecycle. Each step maps to a skill or prompt:

```
Step 1          Step 2         Step 3            Step 4
Scaffold ──► Build ──► Deploy mock ──► Setup Lakebase
 (01)        (02)     (03-deploy)    (04-plugin-add + bundle config)
                                      │
                                      ├─► Wire Lakebase ────────────────┐
                                      │    (05-lakebase-wiring)         │
                                      │                                  │
                                      ├─► Wire Serving endpoint ────────┤
                                      │    (06-serving-wiring)           │
                                      │                                  │
                                      └─► Wire separate Agent App ──────┤
                                           (06d-agent-app-proxy)         │
                                                                         ▼
                                      Optional Chat History ──► Feedback ──► Deploy+E2E
                                      (07-appkit-chat-history) (08-appkit-feedback) (03-deploy)
```

> **Lakebase, serving endpoint wiring, and separate Agent App proxy wiring are independent branches.** An app may use Lakebase only, agent chat only, or both. Choose `06` for Model Serving / Agent Serving endpoints and `06d` for an agent deployed as its own Databricks App.
>
> **Use `06d-appkit-agent-app-proxy` instead of `06-appkit-serving-wiring`** when the agent is deployed as its own Databricks App rather than a Model Serving / Agent Serving endpoint. `06d` is the canonical 2-Apps path used by the root `genai-agents/PROMPT-GUIDE.md`.
>
> **Steps 7 and 8 are optional** and apply to agent-chat apps. `07-appkit-chat-history` requires Lakebase (05) and either the Serving endpoint path (06) or the separate Agent App proxy path (06d). `08-appkit-feedback` requires `07-appkit-chat-history` (it reads the `Vote` table and `traceId` column that 07 creates).

| Step | Skill / Prompt | What It Does |
|------|---------------|-------------|
| Scaffold, Build & Test | `01-appkit-scaffold` + `02-appkit-build` | Scaffold a blank AppKit project, build UI with mock data from PRD |
| Deploy to Databricks Apps | `03-appkit-deploy` | Deploy mock-data app to Databricks Apps |
| Setup Lakebase | `04-appkit-plugin-add` + `apps_lakebase/prompts/03-setup-lakebase.md` | Install Lakebase plugin and configure bundle resources in `databricks.yml` |
| Wire Lakebase Backend | `04-appkit-plugin-add` + `05-appkit-lakebase-wiring` + `apps_lakebase/prompts/04-lakebase-wiring.md` | Add Lakebase plugin, design schema, build APIs, wire frontend — code changes only, does NOT deploy |
| Wire Agent Endpoint | `04-appkit-plugin-add` + `06-appkit-serving-wiring` | Install Serving plugin, wire agent endpoint to frontend — code changes only, does NOT deploy |
| Wire Separate Agent App | `06d-appkit-agent-app-proxy` | Connect AppKit frontend to a separate Agent App backend with OBO forwarding and `/api/chat` SSE |
| Persist Chat History | `04-appkit-plugin-add` + `05-appkit-lakebase-wiring` + (`06-appkit-serving-wiring` or `06d-appkit-agent-app-proxy`) + `07-appkit-chat-history` | Add chat schema, session auth, sidebar, stream+persist proxy, ephemeral mode |
| Add User Feedback | `07-appkit-chat-history` + `08-appkit-feedback` | Add thumbs up/down linked to MLflow assessments (AppKit-native auth) |
| Deploy and E2E Test | `03-appkit-deploy` + `apps_lakebase/prompts/05-e2e-test.md` | Deploy with Lakebase/Serving (SP creates DB objects) + E2E test |

**Start at Scaffold, Build & Test** for new projects. Jump to any step if prior steps are complete.

**Lakebase flow:** After **Wire Lakebase Backend**, the app has Lakebase code but runs locally with mock fallback data. **Deploy and E2E Test** deploys so the Service Principal creates database objects, then runs E2E verification.

**Skill-driven vs prompt-driven steps:** Scaffold/Build and Wire Lakebase Backend are skill-driven — the prompt delegates to skills for reusable patterns. Setup Lakebase and Deploy and E2E Test are prompt-driven — the prompt contains application-specific procedures with skills as supplementary references. Skills encode reusable, PRD-independent knowledge (how to scaffold, deploy, register a plugin, wire a database). Prompts encode orchestration and application-specific context (variable values, step prerequisites, handoff instructions).

---

## Task Routing Table

Match the user's request keywords to the correct skill. Read the skill's `SKILL.md` before proceeding.

| Keywords | Route To | Purpose |
|----------|----------|---------|
| "create app", "scaffold", "init", "new app", "bootstrap", "start new project" | `apps_lakebase/skills/01-appkit-scaffold/SKILL.md` | Create a new AppKit project |
| "add plugin", "add lakebase", "add analytics", "add genie", "add files", "integrate postgres", "extend app" | `apps_lakebase/skills/04-appkit-plugin-add/SKILL.md` | Add a plugin to an existing project |
| "build UI", "implement PRD", "create dashboard", "add page", "build features", "develop frontend", "create components" | `apps_lakebase/skills/02-appkit-build/SKILL.md` | Build features from a PRD or spec |
| "setup lakebase", "add lakebase plugin", "lakebase bundle resources", "configure lakebase" | `apps_lakebase/skills/04-appkit-plugin-add/SKILL.md` + `apps_lakebase/prompts/03-setup-lakebase.md` | Install Lakebase plugin, declare bundle resources |
| "wire lakebase", "connect lakebase", "lakebase wiring", "lakebase backend", "CRUD API", "lakebase tables", "DDL" | `apps_lakebase/skills/05-appkit-lakebase-wiring/SKILL.md` (patterns) + `apps_lakebase/prompts/04-lakebase-wiring.md` (orchestration) | Wire Lakebase to UI — code changes only, does NOT deploy |
| "database schema design", "useLakebaseData", "ConnectionStatus", "mock fallback", "database design" | `apps_lakebase/skills/05-appkit-lakebase-wiring/SKILL.md` | Lakebase wiring patterns (DDL, API routes, frontend hooks, testing) |
| "e2e test", "test lakebase", "deploy lakebase", "verify live data" | `apps_lakebase/Instructions.md` **Deploy and E2E Test** step or `apps_lakebase/prompts/05-e2e-test.md` | Deploy with Lakebase (SP creates DB objects), test APIs, verify idle resilience |
| "lakebase CLI", "lakebase troubleshoot", "lakebase branches", "lakebase roles" | `databricks-lakebase` agent skill (installed via Databricks Agent Skills). Fallback: https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-lakebase/SKILL.md | Advanced Lakebase CLI operations, troubleshooting, branches, roles |
| "wire agent", "agent endpoint", "serving plugin", "agent UI", "chat interface", "model serving", "useServingStream", "serving wiring" | `apps_lakebase/skills/06-appkit-serving-wiring/SKILL.md` | Wire a Model Serving / Agent endpoint to the AppKit frontend |
| "agent app backend", "two apps", "separate Agent App", "appkit plus agent app", "agent app proxy", "OBO forwarding", "x-forwarded-access-token" | `apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md` | Wire AppKit to a separate Agent App with app-to-app auth and end-user OBO forwarding |
| "chat history", "save conversations", "persistent chat", "conversation sidebar", "message storage", "save messages", "ephemeral chat" | `apps_lakebase/skills/07-appkit-chat-history/SKILL.md` | Persist agent chat conversations to Lakebase with session auth + sidebar |
| "feedback", "thumbs up", "thumbs down", "rate response", "MLflow assessment", "user rating", "vote on message" | `apps_lakebase/skills/08-appkit-feedback/SKILL.md` | Add user feedback linked to MLflow assessments (AppKit-native auth) |
| "deploy", "push to production", "ship app", "fix deploy error", "app won't start", "redeploy" | `apps_lakebase/skills/03-appkit-deploy/SKILL.md` | Deploy to Databricks Apps |

---

## Routing Algorithm

```
1. User request received
2. Detect keywords from the routing table above
3. IF "create" / "new" / "scaffold" / "init"         → Read apps_lakebase/skills/01-appkit-scaffold/SKILL.md
4. IF "add plugin" / "integrate" / "add lakebase"     → Read apps_lakebase/skills/04-appkit-plugin-add/SKILL.md
5. IF "build" / "implement" / "PRD" / "UI"            → Read apps_lakebase/skills/02-appkit-build/SKILL.md
6. IF "setup lakebase" / "add lakebase plugin"         → Read apps_lakebase/skills/04-appkit-plugin-add/SKILL.md (plugin install)
                                                        + apps_lakebase/prompts/03-setup-lakebase.md (bundle resources)
7. IF "wire lakebase" / "connect lakebase" / "DDL"   → Read apps_lakebase/skills/05-appkit-lakebase-wiring/SKILL.md (patterns)
                                                        + apps_lakebase/prompts/04-lakebase-wiring.md (orchestration, no deploy)
8. IF "wire agent" / "serving plugin" / "agent endpoint" / "model serving"
                                                      → Read apps_lakebase/skills/06-appkit-serving-wiring/SKILL.md
9. IF "agent app proxy" / "two apps" / "separate Agent App" / "OBO forwarding"
                                                      → Read apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md
10. IF "chat history" / "save conversations" / "persistent chat" / "conversation sidebar"
                                                      → Read apps_lakebase/skills/07-appkit-chat-history/SKILL.md
11. IF "feedback" / "thumbs" / "MLflow assessment" / "rate response" / "user rating"
                                                      → Read apps_lakebase/skills/08-appkit-feedback/SKILL.md
12. IF "e2e test" / "test lakebase" / "deploy lakebase" → Read apps_lakebase/prompts/05-e2e-test.md (deploy + E2E)
13. IF "lakebase CLI" / "lakebase troubleshoot"       → Read and follow databricks-lakebase agent skill
14. IF "deploy" / "ship" / "fix deploy"               → Read apps_lakebase/skills/03-appkit-deploy/SKILL.md
15. IF ambiguous or multi-step                        → Ask user to clarify, or follow
                                                        the lifecycle order (scaffold → build → deploy)
```

---

## Skill Inventory

| Skill | Path | Role | Standalone | Upstream Sources |
|-------|------|------|-----------|-----------------|
| `01-appkit-scaffold` | `apps_lakebase/skills/01-appkit-scaffold/` | scaffold | yes | [AppKit docs](https://databricks.github.io/appkit/), [databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) |
| `04-appkit-plugin-add` | `apps_lakebase/skills/04-appkit-plugin-add/` | plugin-integration | yes | [AppKit plugin docs](https://databricks.github.io/appkit/docs/plugins/) |
| `02-appkit-build` | `apps_lakebase/skills/02-appkit-build/` | build | no (needs scaffold) | [AppKit docs](https://databricks.github.io/appkit/), [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) |
| `03-appkit-deploy` | `apps_lakebase/skills/03-appkit-deploy/` | deploy | yes | [App management](https://databricks.github.io/appkit/docs/app-management), [Configuration](https://databricks.github.io/appkit/docs/configuration) |
| `05-appkit-lakebase-wiring` | `apps_lakebase/skills/05-appkit-lakebase-wiring/` | lakebase-wiring | no (needs plugin-add) | [Lakebase plugin docs](https://databricks.github.io/appkit/docs/plugins/lakebase) |
| `06-appkit-serving-wiring` | `apps_lakebase/skills/06-appkit-serving-wiring/` | serving-wiring | no (needs plugin-add) | [Serving plugin docs](https://databricks.github.io/appkit/docs/plugins/serving) |
| `06d-appkit-agent-app-proxy` | `apps_lakebase/skills/06d-appkit-agent-app-proxy/` | agent-app-proxy | no (needs deployed Agent App) | [Databricks agent apps docs](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent), [AppKit server docs](https://databricks.github.io/appkit/docs/plugins/server) |
| `07-appkit-chat-history` | `apps_lakebase/skills/07-appkit-chat-history/` | chat-history | no (needs 05 + 06 or 06d) | [Lakebase plugin docs](https://databricks.github.io/appkit/docs/plugins/lakebase), [Serving plugin docs](https://databricks.github.io/appkit/docs/plugins/serving) |
| `08-appkit-feedback` | `apps_lakebase/skills/08-appkit-feedback/` | feedback | no (needs 07) | [Serving plugin docs](https://databricks.github.io/appkit/docs/plugins/serving), [MLflow Traces API](https://docs.databricks.com/api/workspace/mlflowtraces) |

---

To see the full directory tree, run: `find apps_lakebase/skills/ -type f -name "*.md" | sort`

## Skill Dependencies

- **`02-appkit-build`** requires a scaffolded project (`01-appkit-scaffold` must run first)
- **`02-appkit-build`** cross-references `03-appkit-deploy` in its "What's Next" section
- **`03-appkit-deploy`** expects `$APP_NAME` and `$PROFILE` to be set by the caller. `$PROFILE` is an IDE/CLI concept (a `~/.databrickscfg` profile); on the in-workspace agent there is no profile (pre-auth/serverless) — see `skills/genie-code-environment`.
- **`04-appkit-plugin-add`** can run at any point after scaffolding
- **`05-appkit-lakebase-wiring`** requires the Lakebase plugin to be registered first (`04-appkit-plugin-add`)
- **`06-appkit-serving-wiring`** requires the Serving plugin to be registered first (`04-appkit-plugin-add`)
- **`06-appkit-serving-wiring`** is independent of `05-appkit-lakebase-wiring` — an app may use either or both
- **`06d-appkit-agent-app-proxy`** requires a deployed Agent App and AppKit app resource binding (`CAN_USE` on the Agent App)
- **`07-appkit-chat-history`** requires `05-appkit-lakebase-wiring` plus either `06-appkit-serving-wiring` or `06d-appkit-agent-app-proxy` (persists agent responses to Lakebase)
- **`08-appkit-feedback`** requires `07-appkit-chat-history` (reads the `chat."Vote"` table and `chat."Message".traceId` column created there)

---

## AppKit Documentation (Live)

For the latest API details, always consult the live docs first:

```bash
# IDE/CLI clients (local Node + npx):
npx @databricks/appkit docs              # documentation index
npx @databricks/appkit docs "<query>"    # search for a specific topic
npx @databricks/appkit docs --full       # full index with all API entries
```

> **Genie Code:** `npx` (local Node) is not available. Use the AppKit docs hub under **See Also** ([databricks.github.io/appkit](https://databricks.github.io/appkit/)) or the per-skill reference docs, and run any AppKit commands via the workspace page-context CLI (`runDatabricksCli`) — see `skills/genie-code-environment`.

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) — back-up reference for canonical Databricks Apps platform guidance.
- AppKit docs hub: [databricks.github.io/appkit](https://databricks.github.io/appkit/)

