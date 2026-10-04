---
name: project-init
description: '[Utilities] Use when setting up or re-evaluating portable project context end to end: project-config, reference docs, CLAUDE.md, AGENTS.md. One piece only: project-config, docs-manager --mode=init or ai-context-refresh.'
disable-model-invocation: false
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
> **[IMPORTANT]** Create complete task plan before shell checks, scans, generators, edits, or skill calls.
> **[IMPORTANT]** The config file is required, but only `project.name` is mandatory; select optional setup work from declared capabilities and repository evidence.
> **[IMPORTANT]** Run `$scan-all` only when selected built-in or generic scan targets apply; custom references default to manual ownership. Run `$workflow-code-to-spec` only for an existing spec corpus or accepted capability scope.

## Quick Summary

**Goal:** Initialize or re-evaluate portable project context through one idempotent route, requiring a valid project identity while configuring only capabilities supported by the project and task.

**Summary:**

- Plan and assess the configured project, then repair the required config until non-empty `project.name` validates.
- Keep always-on context separate from exact task-specific reference selection; add optional capabilities only from evidence.
- Run scan, spec, surface, host, and graph work only when selected; preserve native spec formats or use strict defaults, then verify, review, and report outcomes and skips.

**Workflow:**

1. **Plan Tasks** - Before setup, create task-tracking entries for required setup and review work; include conditional tasks only when their evidence and prerequisites apply.
2. **Assess** - Classify folder state and current context-file health.
3. **Bootstrap** - Require the configured config file with non-empty `project.name`; derive optional properties only from evidence.
4. **Select Context Work** - Ensure always-on `lessons.md` and `docs-index-reference.md` independently of task-specific `referenceDocs`; run only applicable selected/evidenced scans.
5. **Spec Work** - For selected spec work, preserve a valid native `specArtifacts` profile or use the strict TC/Section-8 default when absent. Select the spec workflow only when canonical specs exist or accepted capability scope is available.
6. **Review** - Run the AI-discovery gate across the whole doc set (root context → docs index → every created or changed doc; Phase 4) so its fixes are reviewed, then `$changes-review`, then `$why-review` after setup changes and selected scan/spec work are complete.
7. **Verify** - Validate the required config, declared optional sections, changed docs, selected workflow outcomes, and generated mirrors that apply to this host; re-run the AI-discovery gate only on a doc verification changed.
8. **Graph Refresh** - Run `$graph-code --mode=build` in a background sub-agent only when graph tooling is available and the project/task needs graph coverage; otherwise record an evidence-backed skip.
9. **Report** - List completed actions, evidence-backed skips, blockers, and remaining manual steps.

**Key Rules:**

- MUST ATTENTION run this before ordinary work when required config/docs/root instruction files are missing.
- MUST ATTENTION preserve user-authored `CLAUDE.md` and `AGENTS.md`; use smart-merge/update paths, never blind overwrite.
- MUST ATTENTION keep reusable skill text project-neutral; local rules belong in project config/reference docs.
- MUST ATTENTION use configured portability paths from `.claude/.ck.json` when present.
- MUST ATTENTION before any shell check, scan, generator, or file edit, create a complete task plan covering assessment, setup routes, final skill calls, verification, report, and lessons.
- MUST ATTENTION treat only the config file and non-empty `project.name` as required; valid omitted capability sections do not make the config incomplete.
- MUST ATTENTION distinguish absent `referenceDocs` (portable baseline, possibly empty, plus evidenced capabilities) from an explicit array (authoritative, including `[]`); always-on `lessons.md` and `docs-index-reference.md` are handled separately.
- MUST ATTENTION run `$scan-all` only for selected/evidenced built-in targets or custom docs explicitly marked `scanTarget: "generic"`; custom docs otherwise remain manual and are not freshness-tracked.
- MUST ATTENTION run `$workflow-code-to-spec` only when an existing canonical spec corpus or accepted project/capability scope supplies a real owner target; code/package names alone are not acceptance.
- MUST ATTENTION if both scan and spec work are selected, run them as siblings and wait for both outcomes; otherwise run only the applicable task.
- MUST ATTENTION preserve valid native `specArtifacts`; absence keeps strict TC/Section-8 defaults; an invalid declared profile blocks spec setup instead of falling back silently.
- MUST ATTENTION keep `$changes-review` then `$why-review` as final review gates after setup changes; report a no-change result when no artifacts were modified.
- MUST ATTENTION run `$graph-code --mode=build` as a background sub-agent only when graph tooling is available and graph work is relevant; do not make graph support a hidden prerequisite for non-code projects.
- MUST ATTENTION resolve Codex mirrors through the `$ai-context-refresh` completion handoff when Codex context is installed or selected; otherwise record the host-specific step as not applicable.
- MUST ATTENTION when the user asks for help, options, or "what does init decide", run **Help Mode** below and STOP — never start Phase -1.

## Help Mode (`--help`)

**Trigger:** `$ARGUMENTS` contains `--help`, `-h`, `help`, `options`, `what does this set up`, `what will it change`, or any other request to understand the setup surface rather than to run setup.

**Help Mode is read-only and terminal.** It creates no tasks, runs no scan, generates no file, and edits nothing. Answer, then STOP. If the user then asks to initialize, re-enter this skill at Phase -1.

### 1. What init decides (read this out, it is the part that is skill-owned)

| Decision | Inputs it reads | Effect if you get it wrong |
| --- | --- | --- |
| Route (greenfield / bootstrap / repair / re-evaluate) | `session-init-helpers.cjs` state checks in Phase 0 | A repair route run on a greenfield tree overwrites nothing but reports nothing useful; the reverse regenerates context the project already owns |
| Required config identity | the configured project-config path, non-empty `project.name` | Every downstream skill blocks on invalid config |
| Optional capability sections | repository evidence, not the project name | An invented section makes skills demand a lane the project does not have |
| Always-on vs task-specific reference docs | `lessons.md` + `docs-index-reference.md` are always-on; `referenceDocs[]` is task-specific selection | Selecting a built-in doc with no owning scan target leaves a permanently stale file |
| Spec profile | `specArtifacts` (valid native profile) else strict TC/Section-8 defaults | An invalid declared profile BLOCKS spec setup; it never falls back silently |
| Host mirrors | `$ai-context-refresh` completion handoff | Hand-edited `.agents/**` is overwritten on the next sync |

### 2. The option surface it configures

Init writes the project-config file, so the full option catalog is the same one `$project-config --help` renders. Run the generator directly:

```bash
node .claude/skills/project-config/scripts/project-config-help.cjs            # orientation + most-consumed options
node .claude/skills/project-config/scripts/project-config-help.cjs --sections # every option init can write
node .claude/skills/project-config/scripts/project-config-help.cjs --roots    # relocatable roots init resolves
node .claude/skills/project-config/scripts/project-config-help.cjs --docs     # reference docs init selects, and their owners
node .claude/skills/project-config/scripts/project-config-help.cjs --consumers # how much of the framework each option moves
node .claude/skills/project-config/scripts/project-config-help.cjs --current  # what THIS project already declares
```

### 3. Current state of this project (run before answering "what would init do here?")

```bash
node -e "const h=require('./.claude/hooks/lib/session-init-helpers.cjs'); console.log(JSON.stringify({hasProjectContent:h.hasProjectContent(), isGreenfield:h.isGreenfieldProject()}, null, 2))"
node -e "const s=require('./.claude/hooks/lib/session-init-helpers.cjs'); console.log(JSON.stringify(s.checkProjectConfig(), null, 2))"
node -e "const a=require('./.claude/hooks/lib/agent-files-state.cjs'); console.log(JSON.stringify(a.getAgentFileIssues(), null, 2))"
```

Map the result onto the Phase 1 route table and tell the user which route init would take **and which steps it would skip**, with the evidence for each skip.

**Presentation rules:**

- Show generator output verbatim; it is derived from live sources, so never retype an option list from memory.
- Name skipped steps explicitly. "Not applicable, because <evidence>" is an answer; silence is not.
- For framework-wide help beyond setup (skills, workflows, hooks, project architecture), suggest the user run `$project-help`, or read `.claude/docs/README.md`.

## Scope

`$project-init` is the canonical coordinator for portable setup. It does not replace lower-level skills; it decides which one to run and when:

| Concern | Primary route |
| --- | --- |
| Project config | `$project-config`; the configured file is required and its minimum valid content is non-empty `project.name`. Add optional capabilities only from evidence. |
| User/downstream experience | `$experience-review` after a runnable outcome exists; during setup, configure the matrix or record evidence-backed `NOT-APPLICABLE`/`ENVIRONMENT-BLOCKED` |
| Project reference docs | Ensure always-on `lessons.md` and `docs-index-reference.md` separately. Use `$scan-all` only for selected/evidenced applicable targets; use `$docs-manager --mode=init`, a built-in `$scan --target=<key>`, or the configured generic target for a selected stub/focused repair. |
| Root AI context | `$ai-context-refresh` |
| Codex mirror, `AGENTS.md`, `.agents`, `.codex` | Consume the `$ai-context-refresh` completion handoff when Codex context is present or requested; if required and unavailable, report the exact `$sync-codex` route. |
| Canonical specification and test-case artifacts | `$workflow-code-to-spec` only when canonical artifacts exist or an accepted product/capability scope identifies the owner target. Resolve `specRoots.business.path` when configured; a valid `specArtifacts` profile supplies the native format, while absence keeps strict TC/Section-8 defaults. |
| Knowledge graph | Background `$graph-code --mode=build` only when graph tooling is available and selected by code relationships or the active task. |

> **Project-init test matrix** — Defines config validity, optional capability selection, reference-doc semantics, spec-profile routing, and project-neutral setup behavior.
> MUST ATTENTION read `references/use-cases-and-test-cases.md` when creating plans, tests, or reviewing changes to this setup.

## Phase -1: Required Task Plan

Before Phase 0 shell checks, create a full task-tracking plan. The plan MUST include many small, observable tasks and MUST NOT start execution until these rows exist.

Minimum required task rows:

1. Read `project-init` instructions and setup reference files.
2. Assess configured config path/status, always-on docs, task-selected references, applicable root instructions/host mirrors, and evidence for optional capabilities.
3. Run `$project-config` when the required config is missing, invalid, or stale; accept a valid config containing only `project.name`.
4. Verify or initialize always-on `lessons.md` and `docs-index-reference.md` independently of task-specific `referenceDocs`.
5. Select scan targets from the exact `referenceDocs` selection or repository evidence; call `$scan-all` only when at least one applicable target exists, otherwise record each evidence-backed skip.
6. Decide whether an existing spec corpus or accepted product/capability scope provides a real spec owner; call `$workflow-code-to-spec` only for that scope, otherwise record an evidence-backed deferral.
7. If both scan and spec work are selected, wait at a barrier until both finish or return an explicit blocker/deferral.
8. Run `$ai-context-refresh` when root instructions are missing or stale; otherwise record the verified state.
9. Resolve Codex mirrors through the completed `$ai-context-refresh` handoff only when Codex context is present or requested.
10. Configure or review `experienceVerification` only for evidenced observable surfaces; do not invent surface commands or baselines.
11. Run the AI-discovery gate (`SYNC:ai-discovery-doc-quality`, Phase 4 doc-set check) on every doc this run created or changed plus the root instruction file and the docs index; route each failure to its owner fix before the reviews.
12. Call `$changes-review` after selected setup/scan/spec work.
13. Call `$why-review` after `$changes-review`.
14. Run focused verification for changed config, selected docs, and generated outputs; run broader harness gates only when the change plan calls for them.
15. Spawn `Spawn background $graph-code --mode=build sub-agent` only when graph tooling is available and graph work is relevant; otherwise record the evidence-backed skip.
16. Record the graph sub-agent outcome or skip reason.
17. Report the configured identity, changed optional properties, applicable scan/spec outcomes, always-on context, reviews, verification, graph outcome/skip, and remaining actions.
18. Analyze AI mistakes and reusable lessons.

Keep exactly one row `in_progress`. Mark each row `completed` immediately after its evidence is recorded.

## Phase 0: Assess State

Use shell checks, not memory. Record evidence for every state claim:

```bash
node -e "const h=require('./.claude/hooks/lib/session-init-helpers.cjs'); console.log(JSON.stringify({hasProjectContent:h.hasProjectContent(), isGreenfield:h.isGreenfieldProject()}, null, 2))"
node -e "const s=require('./.claude/hooks/lib/session-init-helpers.cjs'); console.log(JSON.stringify(s.checkProjectConfig(), null, 2))"
node -e "const a=require('./.claude/hooks/lib/agent-files-state.cjs'); console.log(JSON.stringify(a.getAgentFileIssues(), null, 2))"
```

Also check:

- Config path: `node -e "console.log(require('./.claude/hooks/lib/project-config-loader.cjs').getConfiguredProjectConfigPath())"`
- Config status: only the file and non-empty `project.name` are required. A valid config with omitted optional properties is initialized, not a skeleton; repair any invalid declared section before ordinary work.
- Reference selection: absent `referenceDocs` lets the resolver choose its portable baseline (which can be empty) plus evidenced capabilities; an explicit array, including `[]`, is authoritative for task-specific docs. Do not compare it with or restore a full reference catalog.
- Custom reference ownership: `referenceDocs[].scanTarget` is optional. Built-in docs keep their framework target; custom docs default to `manual`, while `generic` opts into one selected evidence-based scan using configured `purpose` and optional `sections`.
- Always-on inputs: check `lessons.md` and `docs-index-reference.md` under the configured project-reference root independently of `referenceDocs`.
- Experience path: inspect `experienceVerification` only when an observable project surface is evidenced or in scope; configuration never substitutes for live evidence.
- Docs index path: `node -e "console.log(require('./.claude/hooks/lib/project-config-loader.cjs').getConfiguredDocsIndexPath())"`
- Project-reference root: resolve it with `getDocsRoot('projectReference')`; inspect only the always-on docs and task-selected/evidenced references needed for this run.
- Placeholder/stale docs: use `isPlaceholderFile()` and `getStaleReferenceDocs()` for selected task-specific docs, not every file in the reference catalog.
- Spec inventory: inspect a configured or repository-evidenced canonical spec root only when a spec corpus or accepted capability scope is found. A missing default root alone does not select spec creation.

If `specArtifacts` is present, require it to validate before spec work. Preserve a valid native profile; absence keeps the strict TC/Section-8 default when a spec workflow is selected; a malformed declared profile blocks that work rather than silently falling back.

## Phase 1: Decide Route

| State | Action |
| --- | --- |
| Empty folder, no real project content | Do not deep-scan. Create a valid minimal config only when initialization was explicitly requested; derive `project.name` from repository metadata or the root directory. Do not invent capabilities, reference docs, or specs. |
| Greenfield project with manifests/code scaffold | Run `$project-config` when the required config is missing or invalid. Add only metadata and capabilities proven by the manifest/source. Manifests and package names alone do not define accepted product scope. |
| Existing project, config missing or invalid | Run `$project-config` first and stop ordinary setup until the required file validates. A minimal valid config with `project.name` is sufficient when no optional capability is evidenced. |
| Existing project, config valid but optional properties omitted | Treat it as initialized. Add only requested/evidenced capabilities; do not route back to `$project-config` solely to fill every optional section. |
| Custom workflow-route protocol requested (team or machine-only) | Team value → `portability.workflowRouteProtocol` in the configured project-config file; machine-only value → git-ignored `.claude/.ck.local.json` (a valid local value replaces the team value). Runtime-only: never regenerate tracked `CLAUDE.md`/`AGENTS.md`/Codex context to apply it. |
| Configured observable surface is in scope | Preserve existing testing practices. Configure only evidence-backed surface/tool facts, then defer live `$experience-review` until an entry point and inspection capability are available. |
| `e2eTesting.execution` is absent or partial for an evidenced E2E surface | Preserve known facts, then derive only the missing values from the linked surface config, E2E reference, runner configs, package/task scripts, compose/CI files, fixtures/seed scripts, and auth docs. Record `file:line` evidence; never invent commands, ports, accounts, selectors, or secrets. |
| Configured observable surface is relevant but cannot run or be inspected | Record `ENVIRONMENT-BLOCKED` with the missing capability and evidence. Do not substitute a screenshot, source review, or passing automated test for the missing exercise. |
| Always-on `lessons.md` or `docs-index-reference.md` missing/stale | Create/refresh these through their owner setup routes at the configured project-reference root; their lifecycle is independent of task-specific `referenceDocs`. |
| A selected/evidenced task-specific reference is missing, a placeholder, or stale | Run only its applicable built-in scan target or explicitly generic custom target, using `$scan-all` when multiple targets are selected. Manual custom docs remain owner-managed. Explicit `referenceDocs: []` selects no task-specific doc scan. |
| `referenceDocs` absent | Use the resolver's portable baseline (possibly empty) and capability-aware selection from config/repository evidence; keep the property absent unless the project wants a fixed explicit selection. |
| `referenceDocs` explicitly lists a subset or `[]` | Preserve it exactly as task-specific selection. Do not restore unselected catalog entries; continue ensuring always-on docs separately. |
| `CLAUDE.md` missing | Run `$ai-context-refresh --mode init` when the Claude host/root context is in use. |
| `CLAUDE.md` exists but is stale, markerless, or still carries legacy universal sections | The root holds project information only; universal rules reach every session by hook, so never copy framework rules or protocol text into it. Marker-managed and stale → `$ai-context-refresh --mode update`. Markerless/project-only → project-owned: keep it as is, or run `$ai-context-refresh --mode update` to smart-merge the generated project sections around its text. Legacy universal sections or sentinels → `$ai-context-refresh --mode update --strip-legacy-universal` (writes a backup first). |
| `AGENTS.md`, `.agents`, or `.codex` missing/incomplete and Codex is present/requested | Consume the `$ai-context-refresh` completion handoff; if unavailable, report the `$sync-codex` route. |
| Canonical specs exist, or accepted product/capability scope identifies a spec owner | Run `$workflow-code-to-spec` for the selected owner. Existing specs normally select `audit`, or `update` when an active requirement/change is in scope. If no owner/scope exists, defer spec authoring with evidence; code/package names alone are insufficient. |
| Existing native spec profile is valid | Preserve `specArtifacts` and route through its configured identifiers, sections, owners, and carriers. Do not translate it to TC identifiers. |
| `specArtifacts` is absent | When a spec workflow is selected, apply strict business-spec and Section-8 TC defaults. Do not create a profile just to avoid those defaults. |
| `specArtifacts` is declared but malformed/unsupported | Stop spec-related setup, retain the declared profile for diagnosis, and route to `$project-config` to repair it. Never drop the declaration and continue with TC defaults. |
| Graph tool and code relationship scope are available | Run `$graph-code --mode=build` in a background sub-agent after setup/review/verification; otherwise record an evidence-backed skip. |
| Everything present and valid | Report verified idempotent state. Do not schedule scans, spec creation, or graph work without a selected/evidenced capability. |

## Phase 2: Execute Order

Run required setup in order. Only scan/spec work selected from project evidence may run in parallel. After a material setup phase, re-check the configured project state.

1. **Required config** — run `$project-config` when the configured file is missing, invalid, or stale for an in-scope capability. A schema-valid config with only `project.name` is sufficient when no optional capability applies.
2. **Always-on context** — ensure `lessons.md` and `docs-index-reference.md` at the configured project-reference root through their owner setup routes. This is independent of `referenceDocs`.
3. **Select reference scans** — absent `referenceDocs` uses the portable resolver baseline (which may be empty) plus configured/repository-evidenced capabilities; an explicit array, including `[]`, is authoritative for task-specific docs. Do not merge to a fixed floor, rename files, or generate an unselected reference. Use `$scan-all` only when one or more applicable targets are selected.
4. **Select spec work** — create a task for `$workflow-code-to-spec` only when a canonical spec corpus exists or accepted project/capability scope names the owner to document. If neither exists, record an evidence-backed deferral; code/package names alone do not establish acceptance. Preserve a valid native `specArtifacts` profile; absent profile means strict TC/Section-8 behavior; an invalid declared profile blocks the spec task.
5. **Post-config selected work** — when both scan and spec tasks apply, create them as sibling tasks and run them in parallel when the host supports it; otherwise finish both before crossing the barrier. When only one applies, run only that task. Every selected task must return completed, blocked, or evidence-deferred before final review.
6. **Experience/E2E** — configure or review the `experienceVerification`/`e2eTesting` matrix only for evidence-backed observable surfaces. Use `$experience-review` or E2E workflows when the surface can actually run and be inspected; missing prerequisites are `ENVIRONMENT-BLOCKED`, not PASS/N/A. Never create an expected baseline from current output.
7. **Convention classes** — run the detector only when stable `contextGroups` or convention injection is selected. Apply a write only when the configured preference or explicit request authorizes it; do not turn on injection merely because the detector found candidates. Verify a representative file with `file-conventions.cjs --lookup` when enabled.
8. **Root instructions** — run `$ai-context-refresh --mode init|update` when `CLAUDE.md` or equivalent root context is missing/stale, preserving user-authored content.
9. **Codex mirror** — consume the `$ai-context-refresh` completion handoff when Codex files/host are present or requested; otherwise record the Codex-only step as not applicable.
10. **Enhance** — use `$prompt-enhance` for newly created or materially updated project guidance when prompt quality warrants it.
11. **Verification** — validate config, selected references, root files, and mirrors that apply; run focused checks for changed behavior.
12. **Graph refresh** — after verification and reviews, run `$graph-code --mode=build` in a background sub-agent only when graph tooling is available and relevant; otherwise record the evidence-backed skip.

## Phase 2.5: Conditional Spec Workflow

When existing canonical specs or accepted product/capability scope selects spec work:

- Resolve the configured business-spec root. Do not infer a new owner from a missing default directory.
- For existing specs, choose `audit` unless an active requirement/code change selects `update`.
- For accepted new capability scope, choose `init-full` for only the accepted scope; apply the workflow's large-scope decomposition rules to that set.
- Use the existing valid `specArtifacts` profile as the native section/ID/case format. If absent, apply strict business-spec and Section-8 TC defaults. If malformed/unsupported, stop spec setup and repair through `$project-config`; do not drop it or fall back silently.
- If no existing spec owner or accepted capability scope exists, do not call the spec workflow to manufacture one. Report the evidence and the route needed to establish scope.

## Phase 2.6: Final Review Skills

After selected setup, scan, and spec work, create and execute these final tasks in order:

1. `Run the AI-discovery gate` - the Phase 4 doc-set check, run BEFORE the reviews so any doc it fixes is reviewed.
2. `Call $changes-review` - run after all selected setup, scan, and spec work so changed config/context/artifacts are reviewed from the current diff.
3. `Call $why-review` - run after `$changes-review` to validate rationale and avoid closing on unchallenged setup decisions.

If a listed task's skill cannot run because the environment lacks the required tool, stop and report the missing tool. If no files changed, still record that result rather than claiming a review of nonexistent changes.

## Phase 3: Agent Rule When The Init Gate Has Not Run

For Codex or any environment where the init-prompt gate has not run:

- If the configured project-config file, always-on docs, applicable root instruction files, or a task-required reference doc is missing or stale, invoke `$project-init` before ordinary task work. Resolve config/index paths through the configured path helpers and the reference root through `getDocsRoot('projectReference')`.
- If `$project-init` cannot run because required tools are absent, report the missing tool and the exact lower-level route that remains.
- Do not proceed with project-specific coding from guessed context.

## Phase 4: Verification

Verify the required project identity, every declared optional property, and each changed or selected output before declaring setup complete. A valid config containing only non-empty `project.name` passes when no optional capability applies.

```bash
node -e "const{spawnSync}=require('child_process');const path=require('path');const configPath=require('./.claude/hooks/lib/project-config-loader.cjs').getConfiguredProjectConfigPath();const result=spawnSync(process.execPath,[path.resolve('.claude/hooks/lib/project-config-schema.cjs'),'--validate',configPath],{stdio:'inherit'});if(result.error){console.error(result.error.message);process.exitCode=1}else process.exitCode=result.status??1"
node -e "const l=require('./.claude/hooks/lib/project-config-loader.cjs');console.log(JSON.stringify({docsIndex:l.getConfiguredDocsIndexPath(),referenceRoot:l.getDocsRoot('projectReference')},null,2))"
node .claude/skills/skill-creator/scripts/validate-skills.cjs --path .claude/skills/project-init
```

For setup behavior changes, run focused tests that cover the changed contract. For example, use `node .claude/hooks/tests/run-all-tests.cjs --filter=init-reference-docs` when changing reference selection, and `--filter=docroot-relocation` or `--filter=reference-doc-freshness` when those behaviors changed. Do not run the full hook suite merely because project initialization completed; include broader harness checks when the framework-change plan requires them.

For selected spec work, confirm:

- Confirm an existing canonical owner or accepted capability scope selected the work; otherwise do not create specs or test cases and record the evidence-backed deferral.
- Confirm the configured business-spec root resolves through `getSpecDocsPath()` only when selected spec work needs it; the default is `docs/specs` (a `specRoots.business.path` entry in `docs/project-config.json` overrides it).
- Preserve and validate a declared native `specArtifacts` profile. When absent, use strict TC/Section-8 defaults for the selected spec work; malformed declarations block that work.
- Apply the spec workflow's large-scope decomposition rules only to the accepted scope actually selected.

For selected observable-surface work, validate only declared or evidenced surfaces. Configuration is not live-review evidence; a relevant but unusable surface is `ENVIRONMENT-BLOCKED`, and first-run expectations remain `ACCEPTANCE-PENDING`.

**AI-discovery gate (`SYNC:ai-discovery-doc-quality`) — across the doc set, not per file.** For every doc this run created or changed, plus the root instruction file and the docs index: purpose + critical rules on the first screen and closing reminders when long; the root context's Doc Lookup and the docs index route each question/task class to one doc through a `read <path> when <situation>` trigger; every routed path exists; each selected reference doc is reachable from the root or the index (no orphan); not-applicable docs are named once as a skip. Record each failure as a fix at its owner (`$scan --target=<key>` for a reference doc, `$project-config` then `$ai-context-refresh` for a root-context route or generated section — the Doc Lookup routes only docs selected in `referenceDocs`), never a hand-edit of a generated mirror.

Run `$changes-review` and then `$why-review` after setup and selected work are complete. If no files changed, record that result without claiming a review of nonexistent changes.

Check root instructions and host mirrors only when those hosts/context files are installed or selected. Preserve user content; if Codex mirrors need regeneration, use the documented `$ai-context-refresh` completion handoff, or report the `$sync-codex` route when that handoff is unavailable.

## Phase 5: Conditional Graph Refresh

Run graph work only when graph tooling is available and the project/task has code relationships for which graph coverage helps:

1. When applicable, `Spawn background $graph-code --mode=build sub-agent` to run `$graph-code --mode=build` with an evidence-supported scope and return a concise outcome.

Rules:

- When graph work is selected, run it in the required background/sub-agent lane and track it to a returned result or an explicit tool/dependency blocker.
- Existing graph presence is not enough by itself to select a refresh; use the active task's scope and graph freshness evidence.
- When graph tooling or relevant code relationships are absent, record why graph work was skipped.

## Output

Report:

- Folder classification: empty, greenfield, existing, or already initialized.
- Files created/updated/skipped: configured project config, always-on and selected reference docs, applicable root instructions and host mirrors.
- Lower-level skills/scripts invoked.
- Selected reference scans and spec work: outcome plus evidence, or an explicit applicability-based skip/deferral for each.
- Always-on `lessons.md` and `docs-index-reference.md`: configured paths and health, independently of task-specific `referenceDocs`.
- Experience applicability matrix: each configured or observed surface, intended outcome, exercise/inspection capability, evidence status, acceptance state, and limitation/`NOT-APPLICABLE`/`ENVIRONMENT-BLOCKED` reason.
- Final review skill calls: `$changes-review`, `$why-review`, each with outcome and evidence.
- Graph refresh: `$graph-code --mode=build` sub-agent outcome when selected, or evidence-backed skip.
- Spec workflow: invoked mode (`init-full`, `audit`, `update`), profile validation result, or evidence-backed deferral reason and next trigger.
- Verification commands and results.
- Remaining manual action, especially any `$sync-codex` step that did not run.


<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md

<!-- PROTOCOL-GUIDES:END -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** any agent, with or without hooks, reaches a verified project-context state before project-specific work.

**MUST ATTENTION Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.
- **AI-Discovery Doc Quality:** every AI-read doc leads with purpose + critical rules, ends with reminders when long, and routes to other docs by trigger to existing targets; no orphan doc.

**IMPORTANT MUST ATTENTION** use `$project-init` as the unified missing-context route; lower-level skills remain implementation steps.
**IMPORTANT MUST ATTENTION** run the AI-discovery gate across the doc set before the final reviews — root context and docs index route every selected doc by trigger, no orphan or dead route; fix each failure at its owner skill.
**IMPORTANT MUST ATTENTION** create task-plan rows for required setup and final reviews; add scan, spec, surface, root-sync, and graph tasks only when evidence selects them.
**IMPORTANT MUST ATTENTION** the configured project-config file and non-empty `project.name` are required; omitted optional properties are valid unless a declared property is invalid.
**IMPORTANT MUST ATTENTION** keep absent `referenceDocs` separate from an explicit selection: absent uses the resolver baseline (possibly empty) plus evidenced capability docs; explicit arrays, including `[]`, remain exact. Always-on lessons/index inputs are ensured independently.
**IMPORTANT MUST ATTENTION** run `$scan-all` only when applicable selected/evidenced scan targets exist; run `$workflow-code-to-spec` only for an existing canonical owner or accepted capability scope.
**IMPORTANT MUST ATTENTION** when both scan and spec work are selected, run them as parallel siblings when supported and wait for both outcomes; otherwise run only selected tasks.
**IMPORTANT MUST ATTENTION** preserve valid native `specArtifacts`; absence uses strict TC/Section-8 defaults when spec work is selected, while an invalid declaration blocks spec work.
**IMPORTANT MUST ATTENTION** run `$graph-code --mode=build` only when graph tooling exists and relevant code relationships or task needs justify it; record an evidence-backed skip otherwise.
**IMPORTANT MUST ATTENTION** run `$changes-review` and then `$why-review` after setup and selected work; report no-change explicitly.
**IMPORTANT MUST ATTENTION** record explicit blocker for any unavailable required skill/tool; silent skip is not completion.
**IMPORTANT MUST ATTENTION** preserve user-authored root instruction files; do not overwrite project-only content.
**IMPORTANT MUST ATTENTION** rerun Phase 0 after every setup phase because the next route depends on current evidence.
**IMPORTANT MUST ATTENTION** keep reusable setup logic project-neutral; project-specific facts belong in config/reference docs.

**Anti-Rationalization:**

| Evasion | Rebuttal |
| --- | --- |
| "Config exists, skip planning" | Create full task plan first; missing-context setup drifts without visible rows. |
| "A valid minimal config looks incomplete" | Require only non-empty `project.name`; derive optional sections from evidence. |
| "Partial reference selection needs the full registry" | Preserve the explicit selection; the catalog is metadata, and always-on inputs are separate. |
| "Package names are enough to define spec scope" | Require an existing canonical owner or accepted scope before creating specs or test cases. |
| "Graph already exists" | Select refresh from graph freshness and task relevance; do not turn graph support into a setup prerequisite. |
| "Review is enough" | Run `$changes-review`, `$why-review`, and all applicable focused verification before reporting. |

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->
