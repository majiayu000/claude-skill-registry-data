---
name: routineos
description: Discover, design, build, verify, deploy, operate, improve and retire Claude routines (scheduled cloud agents) as small apps, with conventions like Rails for routines. Use this whenever the user wants a routine, scheduled agent, recurring or watch job, says "I spend time on X every week", "automate this" or "keep an eye on" something, wants a dashboard or mobile page for a routine, settings they can tune, an approval gate (ask me before it sends), memory between runs, or a "Claude app" that runs on a schedule. Also use it to review, harden, deploy or retire an existing routine. Trigger even if the user never says "framework".
---

# RoutineOS

A routine is a scheduled Claude run on a fresh sandbox. RoutineOS gives it the shape of a web app (a config file, typed settings, a store, optional gates, an optional dashboard) and stays with it from the first conversation to retirement. It builds on Claude's own routines page and does not replace it. It is a copilot: it informs, raises problems and suggests, and the person decides.

Why conventions: runs are stateless, unattended and read untrusted content. Most failures are duplicate writes, lost memory, silent partial results and unapproved sends. The conventions below close those holes by default.

## What RoutineOS never does

1. Contact any external app, read or write, without the person's explicit permission. The permission screen lists every app and what will be done with it.
2. Treat the first run as approval of any critical flow. Sends, posts, deletes and payments each need their own explicit yes.
3. Put secrets in prompts, the database, the repo or the Desk.
4. Provision anything that costs money without explicit permission.
5. Change the person's settings or data without them. It proposes; the person decides.
6. State an unverified fact as true.
7. Call an app done or set up without live and tested evidence.
8. Lose the person's data when it improves or migrates an app.
9. Waste tokens silently: costs of a routine's design are stated before it goes live.
10. Hide weak spots. Each app carries a plain-language known-risks section.

## Lifecycle

| Stage | What happens | Exit evidence | Reference |
|---|---|---|---|
| Discover (optional) | Interview, or read a brief the person already has | A written brief the person accepted | [discover](references/discover.md) |
| Design | Read current platform facts, pick routines, the right mix of code and model, store, gates, secrets pattern, cost; list risks | A design the person approved, risks listed; where the Blueprint was taken up, the person accepted the design and the Blueprint (blueprint check matches). Offer the Blueprint for complex routines (references/blueprint.md); it is optional. | [design](references/design.md), [blueprint](references/blueprint.md) |
| Build | Scaffold, write prompts and scripts, build the Desk | Lint passes; every external contact declared | [components](references/components.md) |
| Verify | Dry checks, then a real report-only first run | A run record exists and the person looked at the output | [deploy](references/deploy.md) |
| Deploy | Show the permission screen, create the live routine and triggers with `RemoteTrigger`, load seed data | The routine is listed on the account with the stated schedule | [deploy](references/deploy.md) |
| Join (optional) | Another person joins a lane of an open Desk with their own routine; the owner can release a lane | The joiner's worker is live, its first run report-only and checked by the joiner | [join](references/join.md) |
| Operate | Read run records, watch health and cost, relay approvals | Health and cost visible on the Desk | [operate](references/operate.md) |
| Improve | Change or add routines and integrations without losing data | Change applied, verified, summarised in plain words | [operate](references/operate.md) |
| Retire | Pause or archive cleanly, remove secrets | Nothing scheduled; secrets deleted | [operate](references/operate.md) |

A person who arrives with a clear description skips Discover. Deploy is done by the agent in the person's interactive session, after the permission screen and a yes; there is no hand-off checklist. `RemoteTrigger` is absent inside a run, so a run never deploys.

## Done means live and tested

The Desk shows one of three states: *not live* (the routine does not exist or is not scheduled), *live, not yet tested* (scheduled, but the first run has not been checked by the person), *live and tested* (the first run happened and the person confirmed the output is what they wanted). Only live and tested counts as finished. No claim counts as evidence, including the agent's own.

## Principles

1. Copilot, user decides: vocal, never blocking.
2. Right mix per routine: scripts for mechanical, repeated steps; the model for reading, judging and drafting. Design states the mix and why, and shows token savings; the person decides. Budget checks, gates and secrets handling are fixed mechanisms for safety.
3. Live platform knowledge: search current docs before relying on a platform behaviour. The platform is a research preview.
4. Honest tags on every platform claim: pilot, docs, unverified, call. See [platform-facts](references/platform-facts.md).
5. Staging before production: report-only first, promotion is its own explicit step.
6. Conventions over configuration: report-only first run, gate before send, idempotent writes, one writer per entity.

## Workflow

Commands run as `python3 skills/routineos/scripts/routineos.py <cmd>`.

1. **Classify** the request into one routine type (table below). Ask one question only if two types fit.
2. **Scaffold**: `new <name> --type <type>` creates `routine.toml`, `prompt.md`, `README.md`; watch and interactive also get `definition.json` and `dashboard/index.html` (the Desk). `--from-template jobs-watch` copies a ready template. It refuses to overwrite. `new <name> --app` also writes `app.toml`, `risks.md`, `CHANGELOG.md`, `lib/budget.py` and the prompt header; `app-init <dir>` adds the first three to a v0 folder. Runs call `lib/budget.py` (`decide` at the start, `record` at the end) as the fixed header says.
3. **Edit** `routine.toml` (UTC schedule, settings, connectors, gate, actions) and `prompt.md`. For a watch or interactive routine ask **Self-improving? (default on)**: it learns per-item suggestions from what people keep and drop, and never applies one itself. See [improve](references/improve.md). For a Desk ask **Should other people be able to join this Desk with their own routines?** A yes adds the `join` block with `"open": true`; `join-settings <dir> --open` or `--closed` switches it later. See [join](references/join.md).
4. **Lint**: `lint <dir>`. Fix every FAIL line; it exits non-zero on problems.
5. **Platform check**: `platform check <dir>` prints each capability id in `[risks].relies_on` with its registry status, marks stale records, and exits non-zero on conflict or broken (shown on the permission screen; the person decides). `platform list` shows the registry.
6. **Permission screen**: `permissions <dir>` prints every app, host, connector, schedule, secret name, cost ceiling and unverified reliance in plain words. Nothing is created until the person says yes.
7. **Doctor**: `doctor [dir]` checks the environment (Python 3.11 for `tomllib`) and an app folder.
8. **Desk**: `seed <dir> --out <batch-dir>` plans the one-time setup, `write` plans a run's writes, `learn` plans its learned suggestions, `bundle` builds the Desk as one file, `dashboard/index.html`, the form to publish (`--split` is an alias that writes the same one file to `dashboard/artifact/`). Publish the page privately first.
   Before writing any Desk code run `desk components --routine <dir>` and read [desk-components](references/desk-components.md).
   Order of preference: a default module, then a view module (`desk module add view <id> --routine <dir> --type <type>`), then a spec page (`desk.pages`, data only), then a custom field cell component, then a code page, then a raw React page. See [desk-pages](references/desk-pages.md) and [desk-raw-pages](references/desk-raw-pages.md).
   A raw React page runs with full access to the Desk as the viewer; the owner must read it before approving.
   `desk lint --routine <dir>` checks the registry and the routine's modules; `lint` runs the registry check too.
9. **Deploy and first run** as in [deploy](references/deploy.md): create the routine, run it once report-only, have the person check the output.

`prompt <gate-email|gate-slack|action-queue|adapter-contract|app-header>` prints a gate, queue, adapter or app header fragment.

## Installing a template pack

A pack is one JSON file holding a whole routine. The catalog is `catalog/index.json`.

1. **Find**: `pack list <index-file-or-url>` prints each template with its maturity, type and connectors. Say whether a template is `unpiloted` (no real run has checked it).
2. **Check**: `pack validate <file-or-url>` refuses unknown keys, secrets, contact details, control characters, an unsafe command and a send without a gate. A URL must be https; redirects are refused.
3. **Install**: `pack install <file-or-url> --dir <target>` (`--name` renames it) writes the folder and prints the connector report. It connects nothing and runs nothing.
4. **Connector walk-through**: read the report to the person one connector at a time: what it is for, required or optional, read or write, which stages use it, and its `connect` text. Products under alternatives are unverified. Add each connector only with their yes; a write connector waits until gated messages start.
5. Then follow the Workflow above from **Lint** onward. The first run stays report-only.

`pack export <dir> --out <file>` turns a routine folder back into a pack. To add a template, follow [authoring](references/authoring.md); keys are in [pack-schema](references/pack-schema.md).

## Migrating from n8n, Windmill or Zapier

To turn an existing n8n workflow, Windmill flow or Zap into a routine, use the [routineos-migrate](../routineos-migrate/SKILL.md) skill and `migrate` (`migrate n8n <file-or-url> --out <dir>`, `migrate windmill <file> --out <dir>`, `migrate search <query>`, `migrate steps <plan> --out <dir>`). The output is a pack, so `pack validate` and `pack install` apply. The result is report-only and unpiloted, every source is treated as untrusted unless `--trusted` is given for the person's own file, and `MIGRATION.md` lists what a person must finish. Docs: [migrate](../routineos-migrate/references/README.md).

## Routine types

| Type | Use when | Workspace | Gate |
|---|---|---|---|
| serverless | Runs, writes a report, nobody watches | no | no |
| watch | Monitors sources, user checks a report on a phone | yes | optional |
| approval-gated | Sends, posts or deletes after a human says yes | optional | yes |
| interactive | User steers it (settings, requests) from a page | yes | when acting externally |

## Conventions that matter

- Memory lives in the artifact db or a connector, never on disk. Write the report first, then update state.
- Settings are typed and human-owned. Each run snapshots the values it used. The agent may propose a change, never write one.
- Minimum schedule interval is one hour.
- Every platform claim to the user carries a tag; owner-reported items stay `unverified` until a pilot run checks them.

## Docs through MCP

The RoutineOS MCP (`routineos` in this plugin) serves docs.routineos.org: `get_started`, `search_docs`, `get_page`, `list_pages`. Use it for anything not in `references/`, and always for raw React pages: `get_page /desk/raw-pages`, then `/desk/component-catalog` for which component to use and `/desk/page-recipes` for a starting page. If the MCP is not connected or a page is missing, say so and use `references/desk-raw-pages.md` only.

## Read this reference when

| Cue | Reference |
|---|---|
| Interviewing, a brief, "I spend time on X" | [discover](references/discover.md) |
| Choosing routines, code versus model, cost, risks | [design](references/design.md) |
| Where a routine's logic lives (repo, account skill, inline) | [design](references/design.md#where-the-logic-lives) |
| Blueprint: requirements, parts, states, approval, drift | [blueprint](references/blueprint.md) |
| Permission screen, creating the routine, first run, promotion | [deploy](references/deploy.md) |
| Health, budget, approvals, changing or retiring an app | [operate](references/operate.md) |
| Refreshing or checking platform facts | [platform-refresh](references/platform-refresh.md) |
| About to state anything about cloud behaviour, limits, connectors | [platform-facts](references/platform-facts.md) |
| Explaining the model, or choosing parts | [components](references/components.md) |
| User knows Rails, Django or Laravel | [rails-map](references/rails-map.md) |
| Settings, tunables, "let me change X from my phone" | [settings](references/settings.md) |
| "Ask me before it sends", approvals, replies | [gates](references/gates.md) |
| Where data lives, sheets, files, object storage | [storage-adapters](references/storage-adapters.md) |
| Writing or reviewing `prompt.md` | [prompt-craft](references/prompt-craft.md) |
| Building the artifact page | [dashboard](references/dashboard.md) |
| Writing a raw React page, choosing Mantine components | [desk-raw-pages](references/desk-raw-pages.md), then the MCP pages above |
| Desk writes, ids, versions, the run record | [write-contract](references/write-contract.md) |
| "Join this Desk", lanes, workers, leave, release | [join](references/join.md) |
| "Run it now", buttons, requests from a page | [live-actions](references/live-actions.md) |
| Daytona, Modal, other sandboxes or hosts | [runtimes](references/runtimes.md) |

## Boundaries

Do not send, post, push or delete on the user's behalf while building. Do not put secrets in prompts, the db or the repo. Do not promise live latency, push replies or webhooks: they are unverified in the registry. Search the live docs before relying on a platform behaviour. If a needed skill is missing, create it with skill-creator rather than failing.
