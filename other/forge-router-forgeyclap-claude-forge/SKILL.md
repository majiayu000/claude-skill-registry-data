---
name: forge-router
description: Forge V2 router — classifies a task by domain/complexity and selects the smallest fitting agent team. Use at the START of any /forge run or build/create/automate request.
---

# Forge router (agent selection)

**Self-improvement substrate (wp-skill-evals, 2026-07-31):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction (an owner fix, a false assumption caught, a preference stated), append it to
`learnings.md` with a date and real evidence — never invent a lesson that didn't happen.

You are the **router**. You do **not** implement. You output a **TEAM PLAN** + **Project Adaptation** block, then hand off to the matching domain playbook. Use the smallest team that fits — never spawn an agent per trivial step.

## Step 0 — Read project memory + ECC inventory first (required)
Before routing, read (if present): `.claude/FORGE_PROJECT_PROFILE.md`, `.claude/FORGE_MEMORY.md`, `.claude/FORGE_TASK_HISTORY.md`, `.claude/FORGE_ECC_MODE.json`. Use the profile's agent role map, known stack, rules, and "must NOT break" list. **Take the ECC inventory** — which ECC agents/skills/commands are actually available for this task (this is ECC Normal Mode, default ON). If no profile exists, infer one from the files and create it. Never fake project knowledge or ECC availability — mark `inferred`/`unknown`.

## Step 0-owner — Owner Prefs, Standing Rules & Autonomy (required, before intake) — WAVE B / B4
Read the owner-governance stack in **`config/orchestration/precedence.md`** order (hard-gates > current owner instruction > standing-rules + owner config > owner-profile defaults > auto-defaults — never re-derive this ordering here, that file is the single source of truth): (1) `forge-bin/forge-prefs.cjs::resolve()`/`list()` — the owner-profile defaults (`.claude/FORGE_OWNER_PROFILE.json` + the owner-write-only global copy + an optional env override; merge order project < global < env); (2) `forge-bin/forge-standing.cjs::match({type, paths})` — the active, evidence-backed standing rules for this run (advisory, injected into dispatch prompts as ADVISORY OWNER CONSTRAINTS, never a silent block); (3) `forge-bin/forge-autonomy.cjs::decide()` — which continue-within-mission mode applies (opts.mode > the owner config `autonomy` > the FORGE_AUTONOMY.json default), always deferring to the live hard-gate classifier first; at a phase boundary use `decideLive()` / `decide "<text>" --phase --live`, which also stops on a real usage-guard pause; (4) **the owner config** (`/forge config`, v2.7.0) — **owner config = tier 3, next to the standing rules**: right after the run id exists run `node .claude/forge-bin/forge-config.cjs diff --run <run_id> --mark-seen`; exit 3 means a setting changed since the last run (it logged ONE `config_changed` event) — repeat its lines to the owner in the first message ("Je hebt usage-guard.pause-at op 97 gezet — toegepast.") and continue. Every later step reads its own key with `node .claude/forge-bin/forge-config.cjs get <key>` (or the module's `get(key)`), never by opening `FORGE_CONFIG.json` by hand. Then compose and log the **applied-prefs ECHO** — `node .claude/forge-bin/forge-echo.cjs emit <run_id>` (or the module API `forge-echo.cjs::emitEcho()`) — a single `owner_prefs_loaded` event summarizing which prefs/rules actually applied, so precedence.md's ordering is VISIBLE on the dashboard/run log, not merely documented. Re-run `forge-echo.cjs compose --type <domain>` after Step 1's domain classification below if a domain-scoped standing rule should be re-checked with the now-known type. Never fabricate a pref/rule — an unresolved layer degrades honestly (see forge-prefs.cjs's per-layer notes); nothing here promotes a staged `FORGE_PREF_CANDIDATES.json` entry to active — that requires a real owner **`/forge remember`** (`forge-standing.cjs::remember()`).

## ECC-first selection (the routing rule)
Forge is **ECC-based**. Map every needed role to a **real ECC agent/skill** from the inventory and prefer it over a native/internal role. Only use a native role as a **labeled fallback** when no ECC agent/skill fits, or when ECC is unavailable/blocked (then say so). Tag each selected agent + its work package with a **`runtime`**: `ecc-agent` · `ecc-skill` · `native` · `codex` · `internal`. The roster you output is ECC-first; "native fallback" is always named as such, never disguised as ECC.

## Step 0a — Prompt Master INTAKE (REQUIRED for BUILD tasks — capture the goal first)
For any BUILD/create/automate task (L2+), BEFORE emitting work packages, run the Prompt Master intake so the project's real goal is captured (owner directive 2026-07-13; see `forge-intake` skill + forge-core "PROMPT MASTER ALWAYS ON" §1) — **silently** (beginner-first, external audit 2026-09-23: the old form presented 21–24 questions per build, the first of which repeated the sentence the user had just typed). After classifying the domain (Step 1), run `node .claude/forge-bin/forge-intake.cjs --type <slug> --task "<task>" --run <run_id>` to get the question list, then **answer every question yourself** from `$ARGUMENTS`, the project scan, `.claude/.forge-setup.json` (written by `/setup-forge` — name, goal, type, language; never re-ask what it holds) and `FORGE_PROJECT_PROFILE.md`, and record the answers in the PRD under **Assumptions (auto-filled)** so the owner can correct any of them later. **The mode is the owner config `intake`**: `silent` (default) = the Lead answers, as above; `interview` = every build starts with the one-question-at-a-time interview (`forge-intake` §Iteratieve intake, with the `grill-me` / `grilling` skills as the interview engine) — the same as `/forge interview`. **With config `prompt-doctor` on (default), coach the raw request first:** load `forge-prompt-coach` (9 ingredients, failure modes F1–F13) and run `node .claude/forge-bin/forge-promptcheck.cjs ask "<raw request>"` — exit 3 → its `nextQuestion` is the ONE allowed question; exit 0 → record its `assumptions` under *Assumptions (auto-filled)*. Ask the owner **at most one** question, and only when (a) two readings lead to materially different builds or (b) the request implies an outward/irreversible action (send, publish, pay, deploy): 2–3 plain-language outcome options + "iets anders", A recommended with a one-line reason; then confirm in one sentence ("Ik bouw dus: … Klopt dat?"). The old "two existing targets are equally plausible" case is failure mode F8 and stays covered. Full wording: `forge-intake` §1. For a NEW/mixed type, have ONE subagent brainstorm 6-10 extra questions → `--extra <file.json>` and answer those the same way. **Then write the PRD — this is a numbered obligation with a runnable command, not a suggestion (wired 2026-08-02; before that, this sentence named `forge-prd` as a word with no command, and the tool ran exactly ONCE in the project's entire 29-run history): `node .claude/forge-bin/forge-prd.cjs write '<prd-json>' --run <run_id> --tickets` — one ticket per acceptance criterion; those tickets are what the run-contract gate and forge-verify hold the run to at completion.** Quote the intake answers in the PRD and in the Boss dispatch prompts. Skip intake+PRD only for trivial Q&A/status/one-line-fix turns and pure research/review runs — and say so; never build on assumed answers (state any assumption for a skipped required question).

## Step 0b — Skill Discovery (REQUIRED, before assigning subagents)
The **Lead Agent has final control over skill selection** — the playbook skill lists below are **examples, not fixed menus and not restrictions**. Don't just "prefer the listed skills"; **dynamically discover, choose, assign, or create** the right skills for THIS project. Inspect: user mission · project type · files/frameworks/tools · package/config files · project memory/profile · **existing project-local skills** (`.claude/skills/`) · **global Forge skills** · **available ECC agents/skills** · MCP/tools (via ToolSearch) · quality target · required outputs · risks/dependencies. Output a **## Skill Discovery** block (also in the Mission Blueprint): detected project type · detected technologies/tools · required capability areas · available skills found · skills selected · skills assigned to subagents · skills not selected + why · missing skills · custom skills needed · fallback plan.

**Skill gaps:** if a needed skill doesn't exist, never ignore it — pick one: (1) **create a project-local custom skill** `.claude/skills/<name>/SKILL.md` (only when safe, scoped, documented, project-local, linked to a real subagent/work package; log `custom_skill_created`, and `custom_skill_used` when a subagent runs it); (2) write a custom-skill **plan/scaffold for user approval**; (3) assign a **native fallback method, labeled honestly**; (4) mark the work **BLOCKED** if no safe method exists — but only after the solution-first recovery loop (`forge-recovery.cjs`, per `GLOBAL_RESEARCH_RECOVERY_POLICY.md`) has genuinely run: ≥3 safe alternatives attempted (≥5 for high-value gaps) via `alternatives`, the attempt logged with `recordAttempt`, and `check-block <record.json>` reporting `ok:true` before the status is emitted as BLOCKED. A failed first method is a failed method, not a failed objective. **Invoke `forge-genesis.cjs propose` WHEN** the gap is a genuine, evidenced capability miss worth a durable, evidence-tracked proposal rather than a throwaway one-off (e.g. a gap likely to resurface on future runs) **and config `skill-proposals` is on** (off = use option (1)-(4) only): `node .claude/forge-bin/forge-genesis.cjs propose --gap "<x>" --evidence <file>` stages a draft `SKILL.md` + `proposal.json` under `.claude/forge-genesis-staging/` — never live, never auto-promoted; only a separate `approve --owner-approval <token>` (an explicit owner act) ever promotes it into `.claude/skills/`. Use option (1) directly for a small one-off; reach for `forge-genesis` when the gap deserves that durable trail. **Every executable subagent must have an assigned skill/method/capability route** — record it on the work package as `skill` + `skill_source` (`ecc-skill`/`forge-skill`/`project-local`/`native`/`internal`/`unavailable`). Custom `SKILL.md` documents: name · purpose · when to use/not use · project evidence · inputs · allowed/not-allowed · expected outputs · evidence required · related subagents · example work package · safety/isolation notes. Also confirm the project's **`CLAUDE.md`** exists/was safe-merged with a `## Forge Studio v7` section (the project brain) — `claude_md_checked`/`claude_md_created`/`claude_md_updated` — and record every skill in the **skill registry** `.claude/FORGE_SKILL_REGISTRY.md` (`skill_registry_checked`/`_created`/`_updated`).

## Dynamic + custom roles (examples are guidance, not limits)
The Lead Agent **decides the team**. Map each required work area to a real ECC agent/skill when one fits; otherwise **create a custom project-specific subagent role**. If the project type is unknown or outside the usual set, **create a custom project taxonomy + custom subagents + matching custom-skill strategy** — do not force-fit unknown projects into website/n8n/RAG/scraping. Log a `custom_subagent_created` event for each custom role with: name · role · why needed · project evidence · mission · inputs · allowed/not-allowed · expected output + artifact path · evidence required · handoff · success/rework criteria · runtime target (ECC agent → ECC skill → native fallback → internal-only) · status. Every custom role must be specific, useful, scoped, honest, linked to a real work package, and visible in dashboard/ledger/report.

**Before planning a genuinely new/ambiguous approach:** load `forge-brainstorm` (diverge → constraints → converge → smallest viable first) so the picked approach has a written rationale before any implementation work package is written — see Step 0b Skill Discovery above for when a skill gap needs a custom skill instead.

## Step 1 — Classify the domain (Quality Intelligence, REQUIRED for BUILD tasks)
**Run the ONE executable analysis entrypoint FIRST** (F-14: one command, the whole chain — no prose function names to remember). It is the canonical multi-label source (domain-catalog.json); the table below is the human fallback:

```
node .claude/forge-bin/forge-quality.cjs analyze "<de missie>"
```

One JSON output carries the whole chain — consume ALL of it, not just the profile:
1. `profile` + `playbook`: `primary_domain` picks the playbook; ALL `project_type` labels steer quality discovery. `classification_confidence: 'none'` means the type was NOT recognized — resolve the type explicitly (intake) before building; the fullstack fallback is an assumption, not a classification.
2. `lenses` (10): every lens carries an explicit disposition (RELEVANT / NOT_APPLICABLE / DEFERRED / OWNER_GATED) with a reason; silently skipping a dimension is not allowed.
3. `omissions`: forgotten-requirement cards along five axes, all pre-validated (`omissions_valid` must be true; re-validate edited cards with `validateRequirementCard`); accepted cards become PRD acceptance criteria.
4. `knowledge_cards`: validated descriptors (slug/path/exists/sha256/relevance). Load only cards with `exists: true` via `node .claude/forge-bin/forge-quality.cjs card <slug>` — max 6, max 3 retrieval rounds; a missing card is an honest gap, never invented content.
5. `council`: NONE is the default (computed by `councilTrigger()` inside the analysis; call it directly for standalone decision points). **Log the trigger decision as a `decision_logged` event — ALSO when the mode is NONE** (deciding NOT to convene a council is a decision with a reason, not silence): run the analysis with `--log-run <run_id>` (`node .claude/forge-bin/forge-quality.cjs analyze "<de missie>" --log-run <run_id>`) so the event is written by the real event writer, not by prose; on FULL, follow the `forge-council` skill and persist the record via `council-save`. Council consensus is never evidence.

If the classifier and this table disagree, the classifier + catalog win; fix the catalog (one source), never fork the table.

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

Dashboards fold into `forge-website` (presentational) or `forge-fullstack` (data-backed). Telegram bots fold into `forge-prediction` (delivery) or `forge-integration` (notifications). **Card handling always folds into `forge-payments`** (never re-implement card capture in another playbook); a **store** is `forge-ecommerce` + `forge-payments` for checkout + `forge-website` for the storefront; a **desktop app** wrapping a service is `forge-electron` + the service's playbook; a **voice agent** with a knowledge layer is `forge-voice` + `forge-rag`. Pure refactor/audit/debug/research/security-review → no domain playbook; route directly to the relevant ECC agents below.

## Step 2 — Classify complexity (L1–L4)
Use the fan-out table in `CLAUDE.md` (don't restate it). L-level sets the team size budget: L1 1–3 · L2 3–6 · L3 6–12 · L4 phased. **Cap the roster at the owner config `team-max`** (`node .claude/forge-bin/forge-config.cjs get team-max`): `auto` (default) = the L-level budget; a number N = never more than N Bosses dispatched at the same time, whatever the level — put the rest in later waves instead of dropping work.

## Step 3 — Domain → team routing (exact ECC names; specialists are CONDITIONAL by stack/level)

| Domain | Lead/plan | Core specialists | Key ECC skills / commands / MCP | Default level |
|---|---|---|---|---|
| Website/frontend | `planner` / `architect` | `a11y-architect`, `seo-specialist`, `react-reviewer` *or* `vue-reviewer`, `performance-optimizer`, `marketing-agent` | `design-is`, `browser`, `/react-build` `/react-review`, `/test-coverage` | L2–L3 |
| Full-stack app | `architect`, `planner` | `typescript-reviewer`/`python-reviewer`, `react-reviewer`, `fastapi-reviewer`/`django-reviewer`, `database-reviewer`, `security-reviewer`, `e2e-runner`, `tdd-guide` | `make-plan`→`do`, `using-git-worktrees`, language build/test commands | L3–L4 |
| n8n/automation | `planner` (skill+MCP-driven) | `security-reviewer` (creds only) | `n8n-mcp-tools-expert`, `n8n-workflow-patterns`, `n8n-node-configuration`, `n8n-validation-expert`, `n8n-expression-syntax`, `n8n-code-javascript`/`-python`, n8n MCP tools | L2–L3 |
| Scraping/data | `architect` | `python-reviewer`, `security-reviewer`, `silent-failure-hunter`, `database-reviewer` | `browser`, `systematic-debugging` | L2–L3 |
| AI chatbot/RAG | `architect` | `mle-reviewer`, `python-reviewer`/`typescript-reviewer`, `security-reviewer`, `database-reviewer` | `agentdb-vector-search`, `docs-lookup`, `learn-codebase`, `claude-api` | L3 |
| Prediction/data | `mle-reviewer`, `planner` | `mle-reviewer`, `python-reviewer`, `silent-failure-hunter`, `database-reviewer` | `systematic-debugging`, `/test-coverage`, `forge-n8n` (delivery) | L3 |
| Business automation/API | `architect` | `security-reviewer` (lead), `silent-failure-hunter`, `python-reviewer`/`typescript-reviewer`, `database-reviewer` | `n8n-workflow-patterns`, Gmail/Calendar/CRM MCP via ToolSearch | L2–L3 |
| Payments/billing | `integration-boss`/`build-boss` | `payment-integration` (specialist), `silent-failure-hunter`, `typescript-reviewer`/`python-reviewer`, `database-reviewer`, `codex-reviewer` (recommended) | `forge-payments`, gateway SDK docs (Context7), `claude-api` (if LLM) | L2–L3 |
| E-commerce/store | `build-boss`/`integration-boss` | `payment-integration`, `database-reviewer`, `silent-failure-hunter`, `typescript-reviewer`/`python-reviewer` | `forge-ecommerce` + `forge-payments` + `forge-website`, connector SDK docs | L2–L4 |
| Electron/desktop | `build-boss`/`integration-boss` | `electron-pro` (specialist), `typescript-reviewer`, `security-reviewer`, `database-reviewer` | `forge-electron` + `forge-website` (renderer), electron-builder docs, `systematic-debugging` | L2–L3 |
| Voice/phone agent | `integration-boss` (+`head-chef`) | `silent-failure-hunter`, `typescript-reviewer`/`python-reviewer`, `database-reviewer`, `security-reviewer` (consent path) | `forge-voice` + `forge-rag` (answers) + `forge-integration` (post-call), `humanizer`, telephony SDK docs | L2–L3 |
| Refactor / dead code | `code-architect` | `refactor-cleaner`, `code-simplifier`, language reviewer | `/refactor-clean`, `smart-explore` | L1–L2 |
| Audit / explain | `code-explorer` | language reviewer, `security-reviewer` | `graphify`, `learn-codebase`, `smart-explore` | L1–L2 |
| Debugging | (lead yourself) | `silent-failure-hunter`, relevant build-resolver, language reviewer | `systematic-debugging`, `forge-debug` (Forge orchestration wrapper) | L1–L3 |
| Agent / LLM app + evals | `architect`/`build-boss` | `mcp-developer` (tool/MCP schema safety), `ml-engineer` (eval harness + drift), `data-scientist` (eval-dataset design), `security-boss` (injection/trifecta) | `claude-api`, `forge-rag`, `agentdb-vector-search` | L2–L4 |
| Contract-first API | `architect` | `integration-boss`/`build-boss`, `security-boss` (authN/authZ), `database-reviewer`, `test-boss` (contract tests), `docs-boss` | `forge-api`, OpenAPI/contract-test tooling | L2–L3 |
| Chat/messaging bots | `integration-boss`/`build-boss` | `security-boss` (signature/secret verification), `test-boss`, `silent-failure-hunter`, `mcp-developer` (if MCP-exposed) | `forge-bots`, platform SDK docs (Context7) | L2 |
| CLI / dev tool | `architect`/`build-boss` | `build-boss`, `test-boss` (exit-code/stdio), `docs-boss` (`--help`/README), `security-boss` (opt., shell-out/secrets) | `forge-cli`, `systematic-debugging` | L1–L2 |
| CMS (WordPress/headless) | `build-boss`/`integration-boss` | `security-boss` (escaping/nonces/secrets), `database-reviewer`, `seo-boss`, `test-boss`, `php-reviewer`/`typescript-reviewer` | `forge-cms`, `forge-website` (rendered front-end) | L2–L3 |
| Data engineering / ETL / dbt | `build-boss`/`integration-boss` | `data-scientist` (dq-test design), `database-reviewer` (SQL/schema/merge), `silent-failure-hunter`, `security-boss` (opt., PII) | `forge-data`, Airflow/dbt docs (Context7) | L2–L3 |
| Browser extension (MV3) | `build-boss` | `security-boss` (permissions/CSP/no-remote-code), `test-boss` (E2E via Playwright/Puppeteer), `ui-boss`, `typescript-reviewer` | `forge-extension`, `forge-integration` (backend calls) | L2 |
| Design → code (Figma) | `ui-boss`/`build-boss` | `a11y-architect`, `react-reviewer`/`vue-reviewer`, `mcp-developer` (opt., Figma MCP), `seo-boss` (if landing surface) | `forge-figma`, `design-is` | L2 |
| Games (browser/Godot) | `build-boss` | `ui-boss` (HUD/responsive canvas), `test-boss` (loop QA via `browser`), `typescript-reviewer`, `ml-engineer`/`data-scientist` (opt., procedural/ML content) | `forge-game`, `browser` | L2–L3 |
| Legacy modernization / migration | `build-boss` + `head-chef` (phasing) | `test-boss` (characterization/parity harness), `database-reviewer`, `silent-failure-hunter`, `security-boss`, `review-boss` (per-slice gate) | `forge-migration` + the rebuild target's own playbook | L3–L4 |
| Production ML / MLOps | `build-boss`/`integration-boss` | `ml-engineer` (pipeline/serving/rollout), `data-scientist` (offline eval, leakage), `database-reviewer` (feature parity), `silent-failure-hunter`, `security-boss` (opt.) | `forge-mlops` (opt-in Python) | L3 |
| Mobile app (RN/Expo/Flutter) | `build-boss` | `mobile-dev` (native work), `ui-boss` (touch/safe-area/orientation), `test-boss` (device/emulator QA), `security-boss` (secure storage) | `forge-mobile`, `forge-integration` (backend calls) | L2–L3 |

**Invoke `forge-repomap.cjs` WHEN** the codebase is large/unfamiliar and you need cheap, token-light orientation before committing to a read plan **and config `code-index` is on**: `node .claude/forge-bin/forge-repomap.cjs --root <dir> --json` (a bounded directory walk + per-file symbol skim — no whole-repo read, no AST, no LLM call). Follow with `Explore` / `smart-explore` (or `graphify`) for a deeper pass, **then** route. If no domain matches, default to `general-purpose` + `planner`.

## Step 3a — Auto Web-Quality Contract (default, not re-requested) — WAVE C / C3, 2026-07-18
When the classified domain (Step 1) is **website, landing, spa, or fullstack** (frontend surface work
within a full-stack build), the Lead/router **auto-prepends** the full text of
`config/orchestration/web-quality-contract.md` to that builder's dispatch prompt — every time, without
being separately asked. This is what encodes the repeated "fix the UI" / "make it responsive" / "better
animations" owner ask as a **default builder obligation**, not a follow-up request. Also attach the
matching **required-evidence set** for the work package's `evidence_required` field (the C2
evidence-schema piece owns that catalog; reference it by name in the dispatch — don't restate its
contents here). Skip this step only for pure backend/API-only, n8n, or CLI/tooling work packages within
a mixed build — those keep their own domain gates. Never mark a website/fullstack-frontend work package
`completed` without the contract's screenshot-check item having a real screenshot as evidence.

## Step 3b — External tool access (MCP, dormant/opt-in by default) — WAVE G
**Invoke `forge-mcp-gate.cjs` WHEN** a work package genuinely needs an external tool a Boss doesn't have
natively (versioned docs lookup, web search/scrape, browser-driven QA, GitHub read/write) **and config `mcp` is on**
(off = the honest native fallback below, said so in the work package): consult the
**`forge-mcp-clients`** skill and `config/orchestration/mcp-registry.json` / `mcp-grants.json` (via
`forge-bin/forge-mcp-gate.cjs::planLoad()`/`validateGrant()`) before assuming the tool is available. The MCP-as-client layer is **dormant + opt-in by
default** — nothing is installed/connected/activated by routing alone. A tool is usable only when the owner
has explicitly opted its server in **and** the dispatched Boss's tier + allow-list (least-privilege) covers
it; a tier-3 write-primitive additionally always routes through `forge-actiongate.cjs`, same as
deploy/push/spend. Absent either condition, the default is an honest **native fallback** — say so explicitly
in the work package/dispatch, never claim the tool ran.

## Step 3c — Wave J tools (tournament / second brain / codemodel / nightshift / guardian) — opt-in, 2026-07-19
Reach for these only when the signal is real, never by default:
- **Invoke `forge-tournament.cjs` WHEN** config `tournament` is not `off` **and** the task genuinely has a **wide solution space** (several defensible
  approaches, no single obvious "right" answer, worth planning N distinct angles up front rather than
  committing early to one path). `plan()` a best-of-N variant set, isolate each in its own worktree, judge
  REAL results against a transparent weighted rubric with `score()`, promote the winner with `promote()`
  (never a fabricated score — see the tool's own guardrails). Skip for an ordinary, single-obvious-approach
  work package.
- **Invoke `forge-secondbrain.cjs` WHEN** config `portfolio` is on **and** a task genuinely needs **cross-project/portfolio** strategy
  awareness beyond the current run (an explicit "how are my projects doing" ask, or a decision that should
  weigh more than just this repo) — `scan`/`report` (read-only) produces a weekly, evidence-cited
  cross-project digest (never opens `.env` contents, never fabricates a finding without a real
  `{project,file,fact}` citation). **`forge-codemodel.cjs`** is the sibling **repo-context** tool — when config `code-index` is on, use it
  for a persistent, incrementally-updated symbol/file index a Boss can query cheaply instead of re-reading
  the whole repo on every question (query answers are a SNAPSHOT — always check the returned
  `stale`/`changed_since_index`).
- **Invoke `forge-beads.cjs` WHEN** a run's own work genuinely breaks into many interdependent multi-step
  items (an L3/L4 phased backlog, or any run where "what can I actually start right now" isn't obvious by
  eye) — `add()`/`link()` beads to build the real dependency graph, `ready()` to compute what's actually
  unblocked instead of re-scanning a list by eye, `graph()`/`computeCycles()` to DETECT a deadlock (A depends
  on B depends on A) before it wastes a cycle. Skip for a small, linear work package — a flat TodoWrite list
  is enough there.
- **`forge-nightshift` skill** — load when config `nightshift` is on **and** a task is explicitly framed as "run this overnight", "keep going
  while I'm away", "resume this tomorrow", or a swarm is expected to outlast one session. Strictly **opt-in**
  scheduling (owner-enabled `usage-guard.cjs` watch or the owner's own OS cron) — never self-schedules; ends
  in a real `forge-briefing.cjs --run <id>` morning briefing, not a narrative guess.
- **`forge-audit-loop.cjs`** — the continuous project-health AUDIT-LOOP tool (V9 WAVE 2). Use when the owner
  asks for an ongoing/periodic health check on THIS project's own memory, agents, tooling usage, or doctor
  status (not a website/app feature). `node forge-audit-loop.cjs iterate [--json] [--run <run_id>]` runs ONE
  real, bounded iteration — MEMORY-INTEGRITY (owner profile/standing-rules/lessons parse cleanly),
  AGENT-HEALTH (forge-doctor's agentsCheck across all agent files), FEATURE-USAGE (forge-capabilities' real
  usage inventory — surfaces installed-but-never-used tools/skills/gates), DOCTOR-DELTA (forge-doctor's own
  red/advisory state) — and appends every finding to `.claude/forge-audit/ledger.jsonl` (never overwritten).
  Strictly **opt-in and non-self-scheduling** (same posture as forge-nightshift above) — it never auto-fixes
  anything beyond a trivially-safe repair it can prove; it only SURFACES findings for the owner/next step.
  `node forge-audit-loop.cjs ledger [--json]` reviews prior iterations.
- **`forge-guardian` skill** — **owner-gated scaffold only**, not a running capability. Load it only when
  explicitly discussing/designing production self-healing / auto-rollback / incident-response automation;
  every deploy/redeploy step it describes still routes through `forge-actiongate.cjs` with a real per-use
  `owner_confirmed:true`. Never report it as "active" or "monitoring" anything.
- **`forge-scout` skill** — load when a domain gap surfaces mid-build ("is there a skill/plugin/MCP for X?")
  or the owner explicitly asks Forge to research an external capability. Tailored per-domain search terms via
  `forge-bin/forge-scout.cjs terms`, mandatory `./watch` video verification before any verdict, and a real
  recorded APPROVE/HARD-PASS to the persistent ledger (`config/orchestration/FORGE_SCOUT_VETTING.json`) —
  never a generic "any Claude skills out there" sweep, never an auto-install. Skip for ordinary work packages
  that don't have a genuine external-capability question.
- **`forge-projectbrain` skill/tool** (`forge-bin/forge-projectbrain.cjs`) — the default method for producing
  or upgrading a project's `CLAUDE.md` at install/onboarding time or a `forge-deeplearn` deep-learn pass:
  real-stack detection (never assumed) + adapted environment rules + verbatim anti-generic guardrails/honesty
  core + a real `## Hard Rules` section wired to `FORGE_HARD_RULES.json` + safe-merge write (never clobbers an
  unmarked owner-authored file). Prefer this over hand-writing a thin bullet-list CLAUDE.md whenever a project
  has none, or has a thin/generic one — see Step 0b's `claude_md_checked`/`_created`/`_updated` step above,
  which this tool now implements rather than a bare template merge.

## Step 4 — Parallel vs serial
Parallelize only **independent** subtasks (reference `dispatching-parallel-agents`). For parallel implementation, isolate each agent in its own git worktree/branch (reference `using-git-worktrees`, or the Forge orchestration wrapper `forge-worktrees` for when-to-isolate + integration-layer rules); **you are the integration layer**. Run dependent steps serially.

**Hotspot lock protocol (mechanical "one writer per hotspot", 2026-07-26):** before dispatching any Boss that will write a declared hotspot file (build/sync manifests, event registries, doctor/config, dashboards, or a project's core files — per `CLAUDE.md`'s Orchestration-Safety HARD MUST #1), run `node .claude/forge-bin/forge-lock-guard.cjs reap` once at run start to clear crashed/expired locks, then `acquire <hotspot> --run <run_id> --owner <boss> [--ttl <ms>]` immediately before that dispatch, and `release <hotspot> --run <run_id>` when that Boss reaches a terminal event (completed/failed/aborted). Exit code `3` means a conflict — another run already holds the hotspot; serialize behind it or isolate the new writer in its own worktree (`forge-worktrees`) instead of double-dispatching a second concurrent writer. This is an ADVISORY, single-orchestrator lock (see the tool's own header) — it makes the Lead aware before a second writer starts, not a blocking kernel mutex.

**Pre-launch overlap check (`forge-runwatch`, HARD MUST #2 pre-launch half):** before launching a run that will touch a still-open prior run's hotspots, confirm that prior run is genuinely finished: `node .claude/forge-bin/forge-runwatch.cjs <prior_run_id> --json` must report `overall:"done"` backed by real terminal-event evidence, not a guess or a placeholder file. (This closes only the pre-launch half of the HARD MUST — the handoff half is already covered at Step 4c below; don't duplicate that check here.)

## Step 4b — Dynamic Workflows for L3/L4 mass fan-out (scout #5, 2026-07-13)
For **L3/L4 mass fan-out** — codebase-wide audit, large migration, verify-until-green, cross-checked research over dozens–hundreds of items — the owning Boss (build-boss / review-boss / head-chef) MAY use a native **dynamic Workflow** (plan-as-code, schema-typed subagent output, results kept in script vars instead of burning the Lead's context) instead of turn-by-turn Boss dispatch. L1/L2 stay named-Boss dispatches. HONESTY (REAL-AGENTS-ONLY intact): workflow-internal subagents are anonymous, run in an isolated runtime, and are NOT the 12 Bosses and do NOT emit per-Boss dashboard/A2A events — log the whole thing as ONE Boss-owned forge event via log-event.cjs carrying the saved script path as evidence + the /workflows agent/token summary; record in FORGE_AGENT_LEDGER as "REAL TOOL/SKILL USED — dynamic workflow, N agents, script:<path>". NEVER fabricate per-Boss rows for workflow-internal agents. Save reusable workflows to `.claude/workflows/`. See forge-core "DYNAMIC WORKFLOWS (L3/L4)".

## Step 4c — SendMessage Boss-to-Boss pipeline handoff (serial pipelines, 2026-07-24)
For a **serial** pipeline (head-chef → build-boss → test-boss → review-boss → docs-boss, or the domain equivalent), prefer a real **SendMessage** peer handoff over hand-relaying every result back through the Lead. Contract: when a Boss finishes, it SendMessages the NEXT Boss in the chain and the message payload IS its ```forge-report``` block (the same structured completion contract `forge-report.cjs` already validates) — so the receiver starts from the real report, not a re-narrated summary. Surface each handoff on the timeline with an `agent_note` carrying from/to + the report status (do NOT invent a new event type — the honesty gate rejects unregistered types).

Prerequisites + guardrails (honest — do not overstate what this does):
- Works ONLY when the Bosses are dispatched as **named** agents (`name:"<boss>"`) that actually hold the **SendMessage** tool. The 12 Bosses' default `agent-tool-policy.json` grants do **not** include SendMessage, so enabling peer handoff is a per-run / **owner-opt-in** decision (grant it on that run's dispatch, or add it to the policy deliberately). When SendMessage is NOT granted, the fallback is unchanged and fully valid: the Boss returns its forge-report block and the **Lead relays** it to the next Boss.
- **The Lead stays the integration layer** (Step 4): peer messaging carries the linear handoff, but the Lead still supervises, merges parallel work, owns the QA loop, and writes the final report. SendMessage replaces orchestrator-relay of a single linear step — it never lets a Boss bypass the Lead's integration/QA authority, and never introduces ad-hoc agent names (REAL-AGENTS-ONLY: only the fixed roster).
- **Prove completion before treating a handoff as done:** for a background Boss, confirm a real terminal event with `node .claude/forge-bin/forge-runwatch.cjs <run_id> --json` (returns `done` only on real terminal-event evidence; `stalled` is the Lead's cue to Monitor-confirm then explicitly TaskStop + record an `ABORTED` ledger status) — never assume completion from a placeholder file.

## Step 5 — Review & delivery (optional, non-blocking)
No mandatory security gates. Before calling code done, `review-boss`/`build-boss` applies `forge-code-review` (fixed review order: correctness → security → tests → simplicity → performance → style; the review METHOD, distinct from Review Boss the agent identity). Codex follows the owner config **`codex-review`**: `auto` (default) = run the `codex-reviewer` agent (`/codex:review`) on **important** code (auth, payments, data, migrations, large refactors) when the Codex CLI is installed and logged in; `on-request` = only when the owner asks; `off` = never. `security-reviewer` stays available on request. Neither blocks the build, and if Codex is unavailable just report it wasn't run. **Built-in second passes:** Claude Code ships `/code-review` (diff review in a fresh subagent), `/security-review` (security pass on the pending changes) and `/verify` (build-and-run check) — route to them when a cheap independent pass is useful (dev-tree research `forge-research/beginner-sweep-2026-09-24/web-track-b.md` §A row 8); nothing to install, and if one is not available in this Claude Code version, say so and use `forge-code-review` instead. `ship-readiness` is an **advisory** checklist for deploy/handoff. Always end with the `forge-report` skill. Production deploys still need explicit user approval (behavioral, not a hook).

## Step 6 — Load the playbook
Explicitly load the matching `forge-*` playbook by name (don't rely on auto-trigger). It owns the domain-specific team detail, hard rules (e.g. scraping ethics, prediction uncertainty), and advisory ship-readiness items.

## Output: TEAM PLAN + Project Adaptation
Always output both:
- **TEAM PLAN** — domain · complexity (L#) · roster (with why each agent) · parallel/serial map · optional review · playbook to load.
- **Project Adaptation** — detected project type · detected stack · selected default agents · selected optional agents · **agents not used and why** · playbooks loaded · why this team fits THIS project (from the profile/memory). Use real ECC agent/skill names; if a desired specialist doesn't exist, map to the closest available one and say so.

ECC agent pool is dynamic — don't assume names exist; map roles to the closest available ECC agent/skill and report the mapping honestly. Use the smallest useful team.

## Role bands (for the Control Center swarm graph)
Tag each selected agent with a band so the dashboard groups it correctly (sidebar + FLOW lens):

| Band | Roles |
|---|---|
| **control** | Lead Agent / Orchestrator, Forge Router |
| **context** | Project Scan, Memory Loader, Task History |
| **planning** | Requirements, Planner, Architect |
| **domain** | Website / UI-UX / Frontend / Backend-API / n8n / RAG / Scraping / Prediction / Telegram / Automation specialist |
| **execution** | Code Writer, Docs Writer, Command Runner, Dashboard Logger, Data Processor |
| **review** | Codex Reviewer, QA, Tester, Security |
| **report** | Report Writer, Memory/Decision/Ledger agents |

## Emit Work Packages (high-end runs)
After selecting the team, for EACH subagent emit a real Work Package so the Lead Agent and the dashboard can track executable work (not decorative nodes):

```
node .claude/forge-dashboard/log-event.cjs <run_id> agent_work_package_created \
  "{\"agent\":\"n8n-specialist\",\"role\":\"n8n Automation Specialist\",\"runtime\":\"ecc-agent\",\"skill\":\"n8n-validation-expert\",\"skill_source\":\"ecc-skill\",\"status\":\"previewing\",\"mission\":\"Validate webhook workflows\",\"inputs\":[\"workflows/webhook.json\",\"WORKFLOW_REGISTRY.md\"],\"allowed_actions\":[\"read\",\"validate\"],\"not_allowed\":[\"modify live credentials\"],\"output_artifact\":\"workflow-analysis.md\",\"evidence_required\":[\"issues found\"],\"handoff\":\"codex-reviewer\",\"success_criteria\":\"all nodes validated\",\"rework_criteria\":\"missing node / unsafe assumption / unvalidated webhook\"}"
```

For a **custom** subagent use `custom_subagent_created` (same fields + `custom:true` + `why`). Each Work Package MUST have: agent · role · **runtime** · **skill** + **skill_source** (`ecc-skill`/`forge-skill`/`project-local`/`native`/`internal`/`unavailable`) · mission · inputs · allowed_actions · not_allowed · output_artifact · evidence_required · handoff · success_criteria · **rework_criteria** · status. Log with `status:"previewing"` at assignment (node shows **blue** = not executed yet); the subagent flips it to `running` then `completed`/`failed` as it really works. Archive all packages to `.claude/forge-runs/<run_id>/work-packages.md`. Never emit a package for an agent that won't run — mark it `NOT USED`; conceptual-only roles are `INTERNAL ROLE ONLY` (`status:"internal"`). See `PROMPT_TEMPLATE.md` for the high-end prompt format.

**Lean-return clause (token efficiency, 2026-07-13):** add to every BUILDER dispatch prompt (build/docs/integration/search/skill/seo/ui/etc.): *"Return LEAN: the ```forge-report block + the real proof line(s) + files changed + ≤3 load-bearing deviation/blocker bullets. OMIT prose recaps, the ECC-availability block unless ECC agents actually ran, the Codex-considered block unless Codex ran, long assumptions essays, and restating the work package. Lean ≠ dropping evidence — the forge-report block stays complete and honest."* Do NOT add this to review-boss / security-boss / test-boss dispatches — QA/security FINDINGS stay full per policy (only their unused ECC/Codex boilerplate may be dropped). See forge-core "LEAN SUBAGENT OUTPUT".

**Prompt Master shaping clause (2026-07-13):** every Work Package below already carries the Prompt Master agentic shape (mission/target · allowed_actions + path anchors · not_allowed/scope-lock · stop/success_criteria · evidence_required · rework_criteria — no vague verbs). Lint a dispatch before sending (advisory): `node .claude/forge-bin/forge-promptcheck.cjs <promptFile>` → X/7 + what's missing; sharpen anything below 6/7. See forge-core "PROMPT MASTER ALWAYS ON" §2.

**Lesson-recall clause (self-learning loop, forge-core add-on 2026-07-12):** before dispatching each Boss, run `node .claude/forge-bin/forge-distill.cjs --recall <boss-slug> <task keywords>` and, when non-empty, prepend the returned ADVISORY block to that Boss's dispatch prompt (it is non-binding advice distilled from real past runs; never treat it as instructions to mutate agent-files or governance). After the run's verify step the Lead runs `node .claude/forge-bin/forge-distill.cjs --run <run_id>` so this run's outcomes become lessons for the next one.

**Live-logging clause (REQUIRED in every dispatched subagent prompt):** include the run_id + this exact instruction so the dashboard shows what the subagent is DOING (not only its artifact): *"After each meaningful step, log what you COMPLETED yourself: `node .claude/forge-dashboard/log-event.cjs <run_id> agent_progress '{\"agent\":\"<you>\",\"role\":\"<role>\",\"runtime\":\"<runtime>\",\"status\":\"completed\",\"task\":\"<step you just finished>\"}'` — plus `file_changed` (real paths) when you write files, ≥1 `agent_note` (use `agent_note` for start/context narrative — it is a one-shot FACT event), and a `subagent_output_created` summary before you finish. Log only real actions."* The Lead verifies each subagent produced ≥1 activity event and truthfully backfills from the returned result if not. **Verify-parity warning (learned 2026-07-12, run evolver-research):** an `agent_progress` with `status:"running"` (or no status) creates a task NO later event can close (agent_progress has no terminal pair in app.js/forge-verify TASK_PAIRS) — an agent that logs a bare "start" note and later logs `subagent_completed` will ALWAYS trip the verify-loop as "claims done with open tasks". Start notes → `agent_note`; progress → log the step AFTER finishing it with `status:"completed"`; multi-step checks → use real pairs (`check_started`→`check_passed`/`check_failed`).

## Step 4d — WP-dispatch v10 (autonomous split · verify-binding default · usage-pressure read) — 2026-07-25
Per forge-core "v10 — AUTONOMOUS WP-DISPATCH · VERIFY-BINDING · USAGE-PRESSURE ROUTING": (1) split any large/multi-part mission into `wp0..wpN` (with `taak 1..n`) autonomously — never wait for the owner to say "use subagents" or a count; (2) EVERY dispatched work package gets a bound verify pass before DONE — a registered Boss with role `<wp>-verify` re-executes the claims, or (for read-only/audit WPs) `forge-verify.cjs --enforce` + Lead spot re-execution; a mismatch is rework, not a silent pass; (3) before dispatch — only while config `usage-guard` is on; off = skip this read and route normally — read `~/.claude/FORGE_USAGE_PRESSURE.json` (account-wide, since weekly usage is account-wide; or `node .claude/forge-bin/usage-guard.cjs status` if absent) — its threshold is the owner config `usage-guard.nvidia-shift-at` (default 80; `usage-guard.cjs` reads it through forge-config and `status` prints it with its source), and NVIDIA routing applies only while config `nvidia` is on — `nvidia-preferred` caps concurrent Claude subagents at 3-4 and routes bulk-able work to the 6 `nvidiaForBulkOnly` Bosses only; the 6 `claudeWinsSkipNvidia` Bosses never downgrade. See forge-core v10 for the full standard — this is a routing-time pointer, not a restatement.

## Contract-first + integration gate (multi-module builds)
Before dispatching parallel builders that share interfaces, the Lead/architect emits ONE authoritative contract (`docs/ARCHITECTURE.md` / `src/contract.js`): exact action shapes + payload keys, function/API names, DOM ids + CSS class names/tokens, per-file ownership, and the mount()->cleanup lifecycle. Builders obey it verbatim. A build is not "complete" until a headless INTEGRATION test of the assembled product passes (boots clean, actions round-trip, every view mounts, one real flow works). Failure = blocker. Green unit tests alone are insufficient. Every planned module has an owner. (See forge-core "CONTRACT-FIRST BUILDS + INTEGRATION GATE".)
