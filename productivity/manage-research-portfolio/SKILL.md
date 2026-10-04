---
name: manage-research-portfolio
description: Manage a multi-project research portfolio and keep its dashboard board in sync. Use when Codex needs to create, review, update, synchronize, or QA a portfolio workspace built from four slug-prefixed top-level areas (overview, project, data, ai); a project registry with owner/priority/status/next-action/evidence; challenge triage for sync drift, stale public copies, dirty worktrees, data-provenance gaps, local-rule drift, or orphaned handoffs; a copyable project template; shared data-governance notes; cross-project AI handoffs; a PROJECT_DASHBOARD.html board whose persistent overview and Project/Data/Usage views map one-to-one to the top-level folders; and a public-safe published copy of that dashboard. Keeps a lightweight Markdown-first workflow and private-data safety boundaries.
---

# Manage Research Portfolio

Use this skill as the operating guide for a research portfolio: many projects sharing one overview, one data-governance area, one cross-project AI memory, and one dashboard board. It transfers a small set of durable habits: clear folder roles, narrow record locations, a compact dashboard that is a current-state map (not a log), server-side safety, and explicit handoffs.

Two rules run through everything:

1. **Markdown first, board second.** Update the registry or the narrowest `_ai`/source note first, then sync `PROJECT_DASHBOARD.html`.
2. **The portfolio stays compact.** Detailed experiments, data dictionaries, and paper notes live inside each project; the overview only holds portfolio-level state and navigation.

And one habit that keeps the portfolio alive: **a project can start from any path.** When a new project appears, scaffold it from `_PROJECT_TEMPLATE`, add it to the registry, and sync its card onto the dashboard — so status flows *up* automatically. These behaviors are driven by the portfolio's guideline files (`PROJECT_GUIDELINES.md`, this skill); extend them by adding rules, and future actions follow. This is what makes multi-owner, multi-project management sustainable.

Use three portfolio lanes:

- **Mainline** — active or formally preparing projects with evidence, owner/status/next fields, and default dashboard visibility.
- **Parked** — future plans or possible projects that should be remembered but should not yet enter the project template, registry mainline, or dashboard default flow.
- **Archived** — abandoned, deprecated, or superseded projects preserved with a stop reason, evidence, and reactivation condition.

Do not turn every idea into a live project. Park early ideas cheaply; promote only when a decision, owner, concrete next action, or coordination need exists.

## Start Here

1. Identify scope before editing:
   - Portfolio/team scope, dashboard, templates, global skills: `<slug>-overview/`
   - Cross-project AI context and handoffs: `<slug>-ai/`
   - Data governance, data inventory, access boundaries: `<slug>-data/`
   - A concrete research project: `<slug>-project/<project-name>/`
   - Future or possible project idea: `<slug>-overview/_PROJECT_PARKING_LOT.md` or a clearly marked parked section in the registry
   - Abandoned/deprecated project: `<slug>-overview/_PROJECT_ARCHIVE.md` or `<slug>-project/_archive/`, with stop reason and evidence
   - Portfolio challenge or drift: `<slug>-overview/_CHALLENGE_REGISTER.md` or `<slug>-ai/<date>_challenge-review.md`
   - After a project exists, run project-specific edits from that project root as the working directory, not from the portfolio root. Use the portfolio root / `<slug>-overview` only for overview, deployment, global rules, global skills, or cross-project synchronization.
2. Read the smallest useful context first: `<slug>-overview/README.md` for intent, the project registry, and any recent `<slug>-ai/<date>_<topic>.md` handoff related to the request.
3. For a concrete project, switch to that project and use the `iterate-research-project` skill (root `PROJECT_GUIDELINES.md`, `_ai/project_overview.md`, `_ai/project_board_spec.md`, then the numbered folders).
4. For complex tasks, keep `task_plan.md`, `findings.md`, and `progress.md` in the relevant overview or project directory.

## Hard Boundaries

- Treat any private/sensitive data area as read-limited: default to high-level descriptions, manifests, and governance notes, not row-level content.
- Never write secrets, tokens, private keys, passwords, raw identifiers, or private-data excerpts into docs, skills, HTML, or handoff files.
- Do not force every project into one rigid template. A portfolio grows lightly; suggest structure only when a project needs it.
- Do not make broad cross-project edits unless asked. Prefer one global file or one project at a time.
- Before automatic structure changes, state which files/directories will change unless the user already specified the exact target.
- Before changing data-governance defaults, raw-data write locations, derived-data ownership, public boundaries, or permission boundaries, confirm scope and exceptions every time.

## Folder And Record System

Use four prefixed top-level areas. `<slug>` is a short portfolio name so multiple portfolios never collide (the demo uses `reasoning`).

```text
<portfolio>/
├── PROJECT_GUIDELINES.md      global operating rules for the whole portfolio
├── GIT_WORKFLOW.md            shared git identity + commit policy
├── <slug>-overview/           team entry: dashboard, requirements, templates, global skills, public-dashboard
├── <slug>-project/            one folder per project + a copyable _PROJECT_TEMPLATE
├── <slug>-data/               data inventory, access boundaries, governance (raw/authoritative only)
└── <slug>-ai/                 cross-project AI handoffs and durable context (<date>_<topic>.md)
```

Default landing places:

- Long-lived portfolio rules: `<slug>-overview/README.md`, `PROJECT_GUIDELINES.md`, data-governance notes, or global skills.
- Cross-project AI handoff: `<slug>-ai/<date>_<topic>.md`.
- Project objective/status/next action: the project's `_ai/project_overview.md` and `_ai/task_plan.md`.
- Project-derived data (features, trajectories, analysis-ready tables, QC intermediates, project data dictionaries): the project's own `2-Data/`, not the global `<slug>-data` area. Keep the global data area for raw/authoritative datasets, inventory, access boundaries, and governance.

Modular collaboration language — encourage the user to name the module type instead of saying "organize this":

- "This is a document" → one topic/meeting/method/decision; project `1-Docs/` + update `1-Docs/README.md`.
- "This is a small project / attempt" → one concrete experiment or route; project `0-Project/<attempt-name>/`.
- "This is a note about an existing attempt" → project `0-Project/<attempt>/docs/<date>_<topic>.md`; use the `iterate-research-project` skill.
- "This is a future project idea" → parked lane first; do not scaffold or dashboard it until promoted.
- "This project is deprecated / abandoned" → archived lane with stop reason, replacement if any, evidence, and reactivation condition.
- "This is data information" → source/version/permissions/QC/boundary; project `2-Data/DATA.md`.
- "This is context to survive compression or task switching" → write the narrowest handoff: project `_ai`/`1-Docs`/attempt `docs/`, or `<slug>-ai/<date>_<topic>.md` for portfolio-wide context.
- "This is a challenge / drift / messy state" → record a challenge first; do not fix everything in one broad edit.
- If unsure, classify first, explain the landing place, then edit.

See `references/portfolio-system.md` for the full folder-and-record contract, registry fields, working memory, and new-project initialization.

## The Portfolio Board (看板)

The portfolio board is `<slug>-overview/PROJECT_DASHBOARD.html`: a team-browsable current-state console, visually distinct from any single-project roadmap (control-console feel, not a single research roadmap). It is a map and navigation surface, not a file browser or execution log.

Basic elements, coordinated with the folders:

- **Persistent Portfolio Overview** (always visible, compact, low height): project count, dataset count, project abbreviations, dataset abbreviations. No roadmap phases and no long prose here.
- **Three mutually-exclusive views** below the overview:

  | View | Fed by | Shows |
  | --- | --- | --- |
  | Project Board | `<slug>-project/` + registry | one card per project: title, priority + owner tags, status, time, next action, and a link to the project's public page. Core view; the template project is pinned first. |
  | Data Board | `<slug>-data/` | a two-level classification (access boundary → data type) with actual registered datasets listed under each category, distinct from the classification dimensions themselves. |
  | Usage Guidelines | `<slug>-overview` + template | folder-structure cards that mirror the real tokens: the four top-level `<slug>-*` folders (big-project idea) and the six `_PROJECT_TEMPLATE` folders `0-Project/1-Docs/2-Data/3-Paper_Survey/4-Skills/_ai` (single-project iteration), plus behavior norms split into everyday use and initialization. |

- **Narrow sidebar:** title, version status, and only these three nav items — do not put the Portfolio Overview in the nav.
- **Project focus** (weaker area under the nav): owner filter + priority filter + a subtle matching-project list. Session-only UI state (resets on refresh); never persisted to team state.
- **Editable team facts** (priority, owner, status, next) belong in a protected server state store; HTML text is a fallback for failed reads, not the source of truth. Personal preferences (theme, sort, active tab) may live in browser local storage only.
- **Version marker** `YYYY-MM-DD-vN` with a freshness/refresh indicator; optional theme selector (small, cornered) and a feedback launcher (bottom-right).
- Mutually-exclusive view switching; long tokens wrap; no private data, secrets, or real local paths.

See `references/portfolio-board.md` for the full dashboard contract. A small portfolio can start with the text registry and add the dashboard once several projects need coordination.

## Project Registry

Keep the registry in `<slug>-overview/` (mirror a short index in `<slug>-project/README.md`). Represent mainline projects with: Project (folder/short name), Goal, Priority (`TBD`/`low`/`medium`/`high`), Owner (or `TBD`), Status (`proposed`/`planning`/`preparing`/`active`/`blocked`/`paused`/`done`/`archived`), Next action, Blocker, Evidence, Last sync. Status must have evidence; without it keep `TBD`, `preparing`, `active`, or `needs review`.

Keep parked and archived work separate:

| Lane | Minimum fields | Promotion / exit rule |
| --- | --- | --- |
| Parked future plan | Idea, why it matters, trigger to revisit, possible owner, evidence/source | Promote to mainline only when it has a concrete next action or coordination need |
| Archived/deprecated project | Stop reason, replacement/superseded-by, last evidence, what not to repeat, reactivation condition | Keep out of default dashboard unless reviewing history or reactivating |

## Challenge Triage

Treat portfolio challenges as records before repairs. Use this for sync drift, stale public copies, oversized dirty worktrees, data-provenance gaps, local-rule drift, orphaned handoffs, or deleted/archived artifacts that still appear active.

Default record: `<slug>-overview/_CHALLENGE_REGISTER.md`. Use `<slug>-ai/<date>_challenge-review.md` when the review is narrative or spans several projects.

Minimum fields: Challenge, Type, Evidence, Blast radius, Owner/TBD, Next action, Safety boundary, Sync level, Last reviewed. Keep evidence as public-safe relative paths or high-level descriptions. Do not paste private data, raw logs, local absolute paths, or source-domain details into the record.

After recording, choose one next action only: update a registry/dashboard field, open a project-level challenge note, create a concrete repair attempt, archive stale work, or ask the user to resolve ownership/safety. Broad automatic cleanup across many projects is a separate confirmed task.

## New Project Creation

1. Confirm the operator's Git identity (`git config user.name`, `git config user.email`). If missing, ask the user to configure their own and pause until done. Identity is attribution + commit authorship, never a credential.
2. Create formal projects under `<slug>-project/<project-name>/` by copying `_PROJECT_TEMPLATE`.
3. Minimally adapt every template file to the new project (`README.md`, `PROJECT_GUIDELINES.md`, `PROJECT_BOARD.html`, `1-Docs/README.md`, `2-Data/DATA.md`, `3-Paper_Survey/README.md`, `4-Skills/PROJECT_SKILLS.md`, and all `_ai/` files). Use `TBD` for missing facts; do not invent owner, priority, status, boundary, data source, or results.
4. Initialize the public-safe page `<slug>-overview/public-dashboard/projects/<project-slug>/index.html`, add the project card to the dashboard and its server-state defaults, and set the card link to `/projects/<project-slug>/`.
5. Stage explicit paths and commit (never `git add -A`; never commit raw/derived data, logs, pid, cache, or secrets).

## Sync Scale

| Level | Trigger | Update |
| --- | --- | --- |
| 0 | Read-only exploration, no new decision | Nothing |
| 1 | Local project work changed, or a challenge is recorded without changing active state | Project source files, `_ai` notes, or `_CHALLENGE_REGISTER.md` only |
| 2 | Project status, blocker, evidence, next action, owner, or priority changed | Project summary + portfolio registry + the dashboard Project Board card |
| 3 | Public claim, shared data rule, ownership, deployment/version, or a cross-project rule changed | Registry, dashboard, published public copy, and a cross-project handoff |

## Asking And Reminder Rules

- If user requests, portfolio rules, project docs, HTML display, or data boundaries conflict, stop the change and ask.
- Ask when missing information affects owner, public boundary, project status, next action, data safety, or whether to sync the dashboard.
- Ask before turning any decision into a portfolio-wide or cross-project rule; confirm scope, exceptions, and which rule files to update.
- For low-risk formatting/naming/classification, choose the conservative option and record the assumption in `progress.md`.
- If a challenge has multiple causes, split it into separate records instead of creating one vague mega-task.
- Before context gets long, after a meaningful step, or before switching projects, write a compact handoff in the narrowest matching Markdown file. Include current goal, completed step, key decisions, evidence paths, open questions, next action, and whether dashboard/board sync is needed.
- Keep questions short and concrete, preferably 2-3 options.

## Publishing

Publish only reviewed, public-safe static files from `<slug>-overview/public-dashboard/`; never deploy the whole workspace, and never expose Markdown, scripts, logs, pid files, raw feedback, or private data as web pages. See `references/public-sharing.md` before preparing any public dashboard, repository, example, or community post.

## Standard Workflow

1. Restore context from the overview README, registry, and recent handoff/progress notes.
2. State scope and affected files when the task will modify structure or shared rules.
3. Make the smallest durable update that solves the task; record discoveries in `findings.md` and actions/validation in `progress.md`.
4. If status, next action, evidence, data version, or public state changed, update the registry / dashboard / public copy per the Sync Scale.
5. End with a short handoff: files changed, current status, validation performed, next useful action, and the commit made.

## References

- Read `references/portfolio-system.md` when creating or reorganizing portfolio folders, the registry, the template project, working-memory files, or handoffs.
- Read `references/portfolio-board.md` when creating, reviewing, or syncing `PROJECT_DASHBOARD.html`.
- Read `references/public-sharing.md` before preparing a public-facing board, repository, example, or community post.
