---
name: forge-router
description: Forge router — classifies a task by domain/complexity and selects the smallest fitting agent team. Use at the START of any /forge run or build/create/automate request.
---

# Forge router (agent selection)

**Self-improvement substrate (wp-skill-evals, 2026-07-31):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction (an owner fix, a false assumption caught, a preference stated), append it to
`learnings.md` with a date and real evidence — never invent a lesson that didn't happen.

You are the **router**. You do **not** implement. You output a **TEAM PLAN** + **Project Adaptation** block, then hand off to the matching domain playbook. Use the smallest team that fits — never spawn an agent per trivial step.

This file is the **always-loaded core** numbered, non-negotiable, short enough to survive compaction. The full, unmodified wording of every step lives in on-demand reference docs under `.claude/docs/forge-reference/` (index at the bottom). Open the doc named in a step before you carry that step out; do not work from memory of an earlier, longer version of this file. The `/forge` core (`.claude/commands/forge.md`) governs project isolation, honesty, the scribe gate, the run contract (`node .claude/forge-bin/forge-runcontract.cjs plan --run <run_id>`) and the hard gates; nothing here relaxes them.

## Core routing checklist (in order)
1. **Step 0 — memory + ECC inventory.** Read `.claude/FORGE_PROJECT_PROFILE.md`, `.claude/FORGE_MEMORY.md` (current-state summary; history in `FORGE_MEMORY_ARCHIVE_*.md`), `.claude/FORGE_TASK_HISTORY.md`, `.claude/FORGE_ECC_MODE.json`; take the ECC inventory; mark `inferred`/`unknown`, never fake. → `router-intake-and-skill-discovery.md`
2. **Step 0-owner — prefs, standing rules, autonomy, owner config** in `config/orchestration/precedence.md` order; after the run id: `node .claude/forge-bin/forge-config.cjs diff --run <run_id> --mark-seen`, then `node .claude/forge-bin/forge-echo.cjs emit <run_id>`. Only `/forge remember` writes a new active standing rule. → `router-intake-and-skill-discovery.md`
3. **ECC-first.** Map every role to a real ECC agent/skill; native only as a labeled fallback; tag `runtime` (`ecc-agent` · `ecc-skill` · `native` · `codex` · `internal`). → `router-intake-and-skill-discovery.md`
4. **Step 0a — intake (BUILD, L2+), silent by default.** `forge-intake.cjs --type <slug> --task "<task>" --run <run_id>`, answer it yourself (what `/setup-forge` saved in `.claude/.forge-setup.json` counts as already answered, never re-ask it), record *Assumptions (auto-filled)*; with config `prompt-doctor` on, `forge-promptcheck.cjs ask "<raw request>"` first; at most ONE owner question. Then the PRD is an obligation: `node .claude/forge-bin/forge-prd.cjs write '<prd-json>' --run <run_id> --tickets`. L3/L4 also: `node .claude/forge-bin/forge-mindmap.cjs from-outline '<goal/modules/criteria outline>' <prd_id> --write --run <run_id>` (the Command Center Mind Map view). → `router-intake-and-skill-discovery.md`
5. **Step 0b — Skill Discovery (required before assigning subagents).** Output a `## Skill Discovery` block; a skill gap is never ignored (custom project skill · scaffold for approval · labeled native fallback · BLOCKED only after the recovery loop); `forge-genesis.cjs propose` for durable gaps when config `skill-proposals` is on. Every executable subagent has `skill` + `skill_source`. Custom roles log `custom_subagent_created`; new/ambiguous approaches load `forge-brainstorm` first. → `router-intake-and-skill-discovery.md`
6. **Step 1 — classify the domain** (table below; run the analyze entrypoint first). → `router-classify-domain-complexity.md`
7. **Step 2 — complexity L1–L4** (fan-out table in `CLAUDE.md`), roster capped by config `team-max`. → `router-classify-domain-complexity.md`
8. **Step 3 — domain → team** with exact ECC names (specialists conditional by stack/level, e.g. `payment-integration` for payments/stores, `electron-pro` for desktop); `forge-repomap.cjs` for large unfamiliar code when config `code-index` is on. → `router-team-routing-and-goat.md`
9. **Step 3x — GOAT routing (HARD MUST).** Head Chef triage `{route, risk, checks}` (fallback `forge-policy.cjs route`); dispatch on the route (Workflow `agent({agentType, label, model, effort})` preferred, every `agent()` routed; Agent tool fallback); Verify Boss verifies; ONE escalation via `forge-policy.cjs escalate <route> <process|context>`; one lesson line. Never `escalate` up front. Log `escalation` + `wp_verified` events via log-event.cjs. → `router-team-routing-and-goat.md`
10. **Step 3a — web quality.** For a website, landing, spa or fullstack (frontend surface) builder, auto-prepend the full text of `config/orchestration/web-quality-contract.md` to its dispatch prompt and attach the required-evidence set; never mark such a package completed without a real screenshot. → `router-web-quality-mcp-wave-j.md`
11. **Step 3b / 3c — opt-in tools.** MCP access only via `forge-mcp-gate.cjs` when config `mcp` is on (else an honest native fallback); Wave J tools (tournament, secondbrain, codemodel, beads, nightshift, audit-loop, guardian, scout, projectbrain) only when their signal is real. → `router-web-quality-mcp-wave-j.md`
12. **Step 4 — parallel vs serial.** Parallelize only independent work, one worktree per parallel writer; you are the integration layer. **Hotspot lock protocol:** `forge-lock-guard.cjs reap` at run start, `acquire <hotspot> --run <run_id> --owner <boss>` before a hotspot writer, `release` on its terminal event (exit 3 = conflict → serialize or isolate). Pre-launch: `forge-runwatch.cjs <prior_run_id> --json` must say `done`. Step 4b dynamic Workflows for L3/L4 fan-out; Step 4c SendMessage handoff (owner-opt-in). → `router-parallel-handoff-review.md`
13. **Step 5 — review & delivery** (`forge-code-review` order; Codex per config `codex-review`; `/code-review`, `/security-review`, `/verify` as cheap second passes; `ship-readiness` advisory; end with `forge-report`). **Step 6 — load the playbook by name.** → `router-parallel-handoff-review.md`
14. **Output TEAM PLAN + Project Adaptation; emit work packages.** Each `agent_work_package_created` carries agent · role · runtime · skill + skill_source · route + risk + checks · model + effort · mission · inputs · allowed_actions · not_allowed · output_artifact · evidence_required · handoff · success_criteria · rework_criteria · status `previewing`. Every dispatch prompt gets: the lean-return clause (builders only), `forge-promptcheck.cjs <promptFile> --strict`, the `forge-prd.cjs clarifications <prd_id>` check, the lesson-recall block (`forge-distill.cjs --recall`), and the live-logging clause (log steps AFTER finishing them with `status:"completed"`; start notes are `agent_note`). A review-found `SPEC GAP` gets a failing-first regression test plus `forge-prd.cjs amend`; run `forge-loophealth.cjs --run <run_id>` before a new rework round. Tag each agent with its dashboard role band. → `router-team-plan-and-work-packages.md`
15. **Step 4d — WP-dispatch v10 + contract-first.** Split big missions into `wp0..wpN` yourself; bind a Verify Boss pass to every package; read usage pressure only while config `usage-guard` is on. Parallel builders that share interfaces need ONE authoritative contract, and nothing is complete until the headless integration gate of the assembled product passes. → `router-dispatch-v10-contract-first.md`

## Step 1 — Classify the domain (Quality Intelligence, REQUIRED for BUILD tasks)
Run the ONE executable analysis entrypoint FIRST (canonical multi-label source: domain-catalog.json); the table below is the human fallback:

```
node .claude/forge-bin/forge-quality.cjs analyze "<de missie>" --log-run <run_id>
```

Consume ALL of its output: `profile` + `playbook` (`classification_confidence: 'none'` = resolve the type in intake first), the 10 `lenses` (each with an explicit disposition), `omissions` (pre-validated; re-validate edited cards with `validateRequirementCard`; accepted cards become PRD acceptance criteria), `knowledge_cards` (only `exists: true`, max 6), and `council` from `councilTrigger()` — the trigger decision is logged as a `decision_logged` event ALSO when the mode is NONE; on FULL follow `forge-council`. Council consensus is never evidence. If the classifier and this table disagree, the classifier + catalog win. Full contract: `.claude/docs/forge-reference/router-classify-domain-complexity.md`.

Pick the primary domain (if mixed, pick the primary and attach the secondary playbook):

| Signals / keywords | Domain | Playbook |
|---|---|---|
| website, landing page, hero, CTA, responsive, UI/UX, a11y, SEO, frontend | Website/frontend | `forge-website` |
| app, SaaS, backend + frontend + DB, login/auth, CRUD, dashboard with data | Full-stack app | `forge-fullstack` |
| n8n, workflow, webhook, node, trigger, schedule/cron, automation pipeline | n8n/automation | `forge-n8n` |
| scrape, crawler, harvest, data collection, lead list, API pull | Scraping/data | `forge-scraping` |
| chatbot, assistant, RAG, retrieval, embeddings, knowledge base, ingestion | AI chatbot/RAG | `forge-rag` |
| prediction, forecast, sports, betting, odds, value, backtest, tips | Prediction/data | `forge-prediction` |
| integration, API, Gmail/Calendar/CRM, OAuth, webhook between apps, sync | Business automation | `forge-integration` |
| payment, checkout, Stripe/Mollie/Adyen/PayPal, iDEAL, card, PCI, subscription, refund, charge, webhook signature | Payments/billing | `forge-payments` |
| shop, store, cart, catalog, product/SKU, inventory, order, Shopify/WooCommerce/Etsy, digital product, cashflow | E-commerce | `forge-ecommerce` |
| electron, desktop app, .exe, installer, preload, IPC, contextIsolation, nodeIntegration, code signing, an accounting desktop app | Electron/desktop | `forge-electron` |
| voice agent, voicebot, phone, call, telephony, IVR, Twilio/Vapi/Retell, barge-in, Dutch call, outbound | Voice/phone agent | `forge-voice` |
| agent, LLM app, tool use, function calling, tool schema, prompt injection, jailbreak, eval, benchmark, guardrail, agent loop, MCP tool | Agent / LLM app + evals | `forge-agent` |
| API, REST, endpoint, route, OpenAPI, Swagger, GraphQL, gRPC, proto, contract test, versioning, idempotency, rate limit, pagination, error envelope, backend | Contract-first API | `forge-api` |
| bot, Discord, Slack, Telegram, slash command, interaction, webhook, Ed25519, Slack-Signature, bot token, intents, gateway, dead-letter | Chat/messaging bots | `forge-bots` |
| CLI, command line, argparse, commander, clap, cobra, flag, --help, exit code, stdin/stdout/stderr, pipe, dry-run, shell tool, terminal, subcommand | CLI / dev tool | `forge-cli` |
| CMS, WordPress, wp-config, theme, plugin, ACF, custom post type, WP-CLI, headless CMS, Contentful, Sanity, Strapi, Payload, content model | CMS | `forge-cms` |
| data pipeline, ETL, ELT, dbt, warehouse, Snowflake, BigQuery, Redshift, staging, marts, medallion, incremental load, backfill, data quality, lineage, Airflow, Dagster | Data engineering / ETL | `forge-data` |
| chrome extension, browser extension, MV3, manifest v3, service worker, content script, chrome.runtime, host_permissions, chrome.storage, CSP, CRX, Web Store | Browser extension | `forge-extension` |
| figma, design to code, mockup, redlines, design tokens, component library, variants, auto-layout, pixel-perfect, breakpoints, dev mode | Design → code | `forge-figma` |
| game, browser game, canvas, WebGL, Phaser, vanilla JS game, Godot, GDScript, game loop, win state, lose state, sprite, collision, playtest | Games | `forge-game` |
| migration, modernization, legacy, rewrite, port, upgrade, strangler fig, characterization test, golden master, parity, shadow traffic, dual-write, feature flag, replatform | Legacy modernization | `forge-migration` |
| mlops, ML pipeline, training pipeline, model registry, MLflow, DVC, feature store, train/serve skew, drift, canary, retraining, rollback, model serving | Production ML / MLOps | `forge-mlops` |
| mobile, mobile app, React Native, Expo, EAS, Flutter, Dart, iOS, Android, apk, aab, ipa, emulator, simulator, secure storage, App Store, Play Store | Mobile app | `forge-mobile` |

Dashboards fold into `forge-website` or `forge-fullstack`; card handling always folds into `forge-payments`; pure refactor/audit/debug/research/security-review → no domain playbook (fold-in rules in the reference doc). If no domain matches, default to `general-purpose` + `planner`.

## Reference index (on-demand, full verbatim wording)
| Doc | Read it when |
|---|---|
| `.claude/docs/forge-reference/router-intake-and-skill-discovery.md` | Steps 0, 0-owner, ECC-first, 0a intake + PRD, 0b Skill Discovery, custom roles |
| `.claude/docs/forge-reference/router-classify-domain-complexity.md` | Step 1 analyze contract and mixed-domain fold-ins; Step 2 |
| `.claude/docs/forge-reference/router-team-routing-and-goat.md` | Step 3 domain → team table (exact ECC names), repomap, Step 3x GOAT |
| `.claude/docs/forge-reference/router-web-quality-mcp-wave-j.md` | Step 3a web-quality contract, 3b MCP, 3c Wave J tools |
| `.claude/docs/forge-reference/router-parallel-handoff-review.md` | Step 4 (hotspot locks, runwatch), 4b workflows, 4c handoff, Step 5 review, Step 6 playbook |
| `.claude/docs/forge-reference/router-team-plan-and-work-packages.md` | TEAM PLAN output, role bands, work-package example and every dispatch clause |
| `.claude/docs/forge-reference/router-dispatch-v10-contract-first.md` | Step 4d v10 dispatch and the contract-first + integration gate |
| `PROMPT_TEMPLATE.md` (this folder) | the high-end prompt format |
