---
name: uat
description: Create user acceptance test journeys from a target user's perspective, with role-based scenarios, acceptance criteria, and evidence capture
type: analysis
version: v0.17
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "[--variant-evaluation] [optional: persona, feature, release, journey, app, or variation spec]"
context_intake: artifact_only
invocation: sub-skill
parent: logic-wiring
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# UAT

Invoke as `$uat`.

Create a user acceptance testing plan from the perspective of a potential or target user. Read the product surface, specs, journeys, stories, roadmap, and relevant research, then produces realistic end-to-end user journeys with click-by-click or surface-appropriate checklists that validate whether the product satisfies user goals.

UAT is not dogfooding. Dogfood asks how the app owner can adopt the product into their own workflow to understand and evaluate it. UAT asks whether a target user can complete meaningful real-world journeys and would accept the product as fit for use.

This is a human-run acceptance plan, not automated testing. Do not start servers, drive browsers, call APIs, create accounts, or perform the scenarios yourself.

When invoked with `--variant-evaluation` (or when the user asks to test/review UI variants), create a hands-on evaluation plan for built UX/UI variants before any consolidation decision. This mode helps the user try each variant in a comparable way using explicit walkthrough checklists and capture enough evidence to form a defensible consolidation opinion.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. Human-run prototype/UAT evaluation belongs in `tasks/manual-todo.md`; confirmed implementation fixes may enter `tasks/todo.md` only after human evidence exists.

## Design-Tree Role

`uat` is a **sub-skill** in the design-tree loop (`DESIGN-TREE-LOOP.md`). Its `parent:` is `logic-wiring`, and it is also invoked inline by `consolidate-prototypes` (variant evaluation) and by the execution loop (release/journey UAT). It enters at its own **checklist/evaluation stage** — building hands-on journeys and capturing human evidence — and does **no pipeline routing of its own**: it returns evidence to the invoking parent, which owns the handoff. Its existing recommendations (e.g. `$consolidate-prototypes`, `$customer-discovery`) are fallback suggestions, not design-tree branch routing.

## Handoff Verification

Immediately before final handoff text in `--variant-evaluation` mode, classify readiness from `design/**/flow-tree-*.yaml`, `research/**/uat-variant-evaluation-*.md`, and `tasks/manual-todo.md` as exactly one of `continue-design-branch`, `manual-uat-needed`, `single-variant-convergence-needs-explicit-scope`, or `ready-for-consolidation`. Do not use `research/.progress.yaml` for UX branch state, prototype readiness, UAT status, or consolidation readiness; it remains product-path/product-line state only.

Use conservative routing when artifacts conflict: choose `manual-uat-needed` or `continue-design-branch`, never `$consolidate-prototypes`. The final response must include a compact readiness line before any `Next Work`, `Recommended next command`, or `agent_routing` text, for example: `Handoff verification: manual-uat-needed; $consolidate-prototypes is blocked until evidence is recorded for built variants and every approved sibling branch has an explicit MVP-scope decision.`

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, read pre-prototype design artifacts under `design/{slug}/`, read finalized implementation specs under `specs/{slug}/`, and treat top-level `research/*.md` and `design/*.md` files as flat-mode documents or cross-path summaries.

1. **Resolve project context**
   - Read `.agents/project.json` if it exists.
   - Use `project_type` and `enabled_packs` when present.
   - If project metadata is missing, infer the project type from repo signals:
     - business-app: SaaS, marketplace, productivity, workflow, enterprise, or user-facing app
     - devtool: SDK, CLI, API, library, infrastructure, docs, examples, or package-first developer workflow
     - game: game engine files, playable prototypes, store assets, or game-specific README/spec language
     - generic: no strong domain signal
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `spec.md`, and `tasks/` files when present.

2. **Load user evidence**
   - Business app: read `research/icp.md`, `research/journey-map.md`, `research/customer-feedback.md`, `research/metrics.md`, and `research/mvp-gap.md` when present.
   - Devtool: read `research/devtool-user-map.md`, `research/devtool-dx-journey.md`, `research/devtool-integration-map.md`, docs, examples, and package manifests when present.
   - Game: read `research/game-audience.md`, `research/game-fantasy.md`, `research/game-core-loop.md`, `research/game-prototype-test.md`, and `research/game-playtest-metrics.md` when present.
   - Generic: use specs, README, routes, tests, examples, issue descriptions, and task acceptance criteria.
   - In product-path workspaces with `research/{slug}/` or `specs/{slug}/`, produce product-path-scoped UAT journeys for the requested app. If no app is specified and multiple apps are plausible, ask the user to choose.

2b. **Variant evaluation mode**
   - Trigger this branch when invoked with `--variant-evaluation`, when `design/ui-layout-variations-*.md`, `design/ux-variations-*.md`, or product-path-scoped equivalents exist for the requested topic, or when the user asks how to test/review built variants. Legacy `specs/ui-layout-variations-*.md` may also trigger this branch during migration.
   - Read `design/ui-layout-variations-[topic].md`, `design/ux-variations-[topic].md`, `design/ui-requirements-[topic].md`, `design/**/flow-tree-*.yaml`, `design/prototype-build-plan-[topic].md`, product-path-scoped equivalents, built prototype directories under `prototypes/{topic}/`, built variant routes/components, and any existing `research/uat-variant-evaluation-[topic].md`.
   - Treat legacy `specs/ui-layout-variations-[topic].md`, `specs/ux-variations-[topic].md`, and `specs/ui-requirements-[topic].md` as fallback evidence only when the corresponding `design/` artifact is missing.
   - Identify each variant, its intended thesis, implementation location, and the target user task it should support.
   - Create comparable journeys that make the user perform the same core task in every variant, with step-by-step checklist instructions for each built variant. Use click-by-click language for UI prototypes, command-by-command language for CLI prototypes, request-by-request language for API prototypes, and mixed checklist steps for hybrid surfaces.
   - Include a side-by-side comparison matrix, per-variant walkthrough checklists, and a "Ready for `$consolidate-prototypes`?" checklist.
   - In the variant inventory and readiness output, distinguish these four statuses explicitly: `built + evaluated`, `built + not run`, `approved but unbuilt/deferred`, and `explicitly excluded from MVP`.
   - Human execution still belongs in `tasks/manual-todo.md`; this skill writes the plan and manual tasks, but does not run the variants.
   - While any built variant result log is `Not run`, recommend manual UAT/evidence capture rather than `$consolidate-prototypes`.
   - Mention `$consolidate-prototypes` only after result logs record evidence and either every MVP-scope approved variant is evaluated or the user explicitly chooses a single-variant MVP and excludes, defers, or marks all other approved unbuilt branches as spec-only references.
   - Before any final handoff that mentions `$consolidate-prototypes`, emit `Handoff verification: ready-for-consolidation; ...` and only use that classification when UAT evidence exists and every approved branch is evaluated, excluded, deferred, or spec-only by explicit user decision.
   - Stop after this branch. Do not generate generic target-user acceptance journeys unless the user also requested them.

3. **Define acceptance perspective**
   - Identify 1-3 target user personas or roles from the evidence.
   - For each selected persona, define the job-to-be-done, context, goal, constraints, and acceptance threshold.
   - Prefer external target users, buyers, evaluators, administrators, developers, or players over the product owner unless the owner is also the target user.
   - If the target user is unclear, stop and recommend `$customer-discovery`, `$journey-map`, or the relevant pack research skill. For `$customer-discovery`, `$journey-map`, and other pack-based skills, apply the Pack Availability Guard — if the target skill's pack is not in `.agents/project.json` `enabled_packs`, recommend `npx skillpacks install <pack>` before the skill.

4. **Create UAT journeys**
   - Generate 3-7 journeys unless the user requested a narrower focus.
   - Cover at least one critical happy path, one realistic obstacle or recovery path, and one return-use or handoff path when supported by the product evidence.
   - Each journey must include:
     - target user
     - user goal
     - real-world trigger
     - setup and preconditions
     - end-to-end task sequence
     - click-by-click, command-by-command, request-by-request, or hybrid tester checklist
     - expected user-visible success state
     - acceptance criteria
     - non-acceptance signals
     - evidence to capture
     - tester notes prompt
     - follow-up routing
   - Use concrete product language from specs and journeys. Avoid vague instructions such as "verify the feature works." Every tester checklist item should be directly executable by a human and checkable after completion.

5. **Classify follow-up work**
   - Human-run UAT journeys go in `tasks/manual-todo.md` under `## UAT Journeys`.
   - Use `_(after: research/uat-plan.md)_` unless the journey blocks or follows a known roadmap step. If tied to a known step, use `_(blocks: Step N.X)_` or `_(after: Step N.X)_`.
   - Do not put human-run UAT journeys in `tasks/todo.md`.
   - Implementation or documentation fixes discovered after a completed UAT run belong in `tasks/todo.md`, but do not invent fixes before the user journey has been attempted.
   - One-time evidence collection belongs in `tasks/record-todo.md`.
   - Recurring release acceptance checks belong in `tasks/recurring-todo.md` only when there is a clear release cadence.
   - If a journey needs click-by-click help for a human-only external blocker, recommend `$guide`.

6. **Present findings before writing when risk is high**
   - If source material is thin, contradictory, or missing target-user evidence, summarize the gap and ask whether to proceed with assumptions.
   - If source material is sufficient, write the plan and task sections directly.

## Deliverables

- `research/uat-plan.md` - persona assumptions, journey matrix, source evidence, acceptance checklist, result log template, and follow-up guidance.
- In variant evaluation mode: `research/uat-variant-evaluation-[topic].md` - variant inventory, task script, comparison matrix, result logs, and consolidation readiness checklist.
- `tasks/manual-todo.md` - append or replace only the `## UAT Journeys` section.
- `tasks/recurring-todo.md` - optional, only when recurring UAT is useful and not already tracked.

If `tasks/manual-todo.md` does not exist, create it with a `# Manual Tasks - [Project Name]` title, a short note that these items require human-only action, and the UAT section. Preserve all non-UAT sections when updating an existing file.

Use this journey format in `research/uat-plan.md`:

```markdown
### Journey N: [Name]

- Target user: [persona or role]
- User goal: [what the user is trying to accomplish]
- Trigger: [real-world reason the user starts]
- Setup: [accounts, data, environment, permissions, or sample state needed]
- Task sequence:
  - [step the human tester performs as the target user]
- Tester checklist:
  - [ ] [Click/type/run/send the exact first action, including route, button, field, command, or request detail]
  - [ ] [Observe the expected intermediate state before continuing]
  - [ ] [Capture evidence at the named point]
- Expected success state: [observable user-visible result]
- Acceptance criteria:
  - [ ] [specific criterion]
- Non-acceptance signals: [confusion, delay, missing affordance, incorrect result, trust issue, or blocker]
- Evidence to capture: [screenshots, recordings, notes, timestamps, records, command output, or artifacts]
- Tester notes prompt: [question that captures whether the target user would accept this]
- Follow-up routing: [manual note, $customer-discovery, $journey-map, $guide, or task promotion guidance]

#### UAT result log

- Status: Not run | Pass | Fail | Blocked
- Evidence captured:
- Tester notes:
- Follow-up tasks promoted:
```

Use this variant evaluation format in `research/uat-variant-evaluation-[topic].md`:

```markdown
## Variant Evaluation Plan

### Variant Inventory

| Variant | Implementation location | Thesis | Primary task |
|---|---|---|---|

### Variant Readiness Inventory

| Variant | Branch status | UAT status | MVP scope decision | Notes |
|---|---|---|---|---|
| [Variant name] | built + evaluated | Pass | in MVP scope | [evidence link] |
| [Variant name] | built + not run | Not run | undecided | manual UAT required before consolidation |
| [Variant name] | approved but unbuilt/deferred | Not run | undecided | build/evaluate, explicitly exclude/defer, or include as spec-only reference before consolidation |
| [Variant name] | explicitly excluded from MVP | Skipped | excluded | explicit user decision required |

### Shared Evaluation Script

- Target user:
- Scenario:
- Setup:
- Core task sequence:
- Shared tester checklist:
  - [ ] [Open or start the prototype surface]
  - [ ] [Complete the first comparable task action]
  - [ ] [Capture evidence at the first checkpoint]
- Success criteria:
- Non-acceptance signals:
- Evidence to capture:

### Per-Variant Result Log

#### [Variant name]

- Walkthrough checklist:
  - [ ] [Variant-specific click/type/run/send step]
  - [ ] [Variant-specific checkpoint to observe]
  - [ ] [Variant-specific evidence to capture]
- Status: Not run | Pass | Fail | Blocked
- Evidence captured:
- What worked:
- What felt wrong:
- Time/friction notes:
- Keep for consolidation:
- Reject for consolidation:
- Confidence: Low | Medium | High

### Side-by-Side Comparison Matrix

| Dimension | Variant A | Variant B | Variant C | Current preference | Evidence |
|---|---|---|---|---|---|

### Ready for `$consolidate-prototypes`?

- [ ] Every built MVP-scope variant has been tried and has evidence in its result log.
- [ ] No built MVP-scope result log is still `Not run`.
- [ ] Every approved but unbuilt/deferred branch is explicitly excluded from MVP, deferred from MVP, or marked spec-only by the user.
- [ ] If converging from one built variant, the user explicitly chose a single-variant MVP and named how all other approved branches are handled.
- [ ] Evidence exists for each kept/rejected design element.
- [ ] Open blockers are documented.
- [ ] The user has enough confidence to converge.
```

Use this item format in `tasks/manual-todo.md`:

```markdown
## UAT Journeys

- [ ] Run UAT journey: [Journey name] as [target user] _(after: research/uat-plan.md)_ - capture evidence in `research/uat-plan.md`.
```

## Task Classification

- Human UAT journey execution goes in `tasks/manual-todo.md`.
- Variant evaluation tasks go in `tasks/manual-todo.md` under `## UAT Journeys` and should reference `research/uat-variant-evaluation-[topic].md`.
- Immediate implementation or documentation fixes confirmed by completed UAT go in `tasks/todo.md`.
- One-time condition-gated evidence collection goes in `tasks/record-todo.md`.
- Release-cadence UAT checks go in `tasks/recurring-todo.md`.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Do not run or operate the product in this skill.
- Do not start dev servers, launch browsers, use Playwright, call APIs, create accounts, or perform CLI workflows.
- Do not mark journeys complete; only a human tester can do that after performing them.
- Do not recommend `$consolidate-prototypes` before variant evaluation evidence exists and no built MVP-scope result log is `Not run`.
- Do not recommend `$consolidate-prototypes` while approved UX/UI branches remain unbuilt or deferred unless the user explicitly excludes or defers them from MVP scope, marks them spec-only, or explicitly chooses a single-variant MVP from the current built set.
- Do not duplicate existing unchecked UAT or manual tasks. Reference existing items when they already cover the same journey.
- Prefer evidence-backed target-user journeys over exhaustive feature coverage.
- Keep dogfood and UAT separate: use `$dogfood` for owner/operator adoption into the builder's workflow; use `$uat` for target-user acceptance journeys.
- If no credible user journey, story, spec, or product surface can be found, stop and recommend `$customer-discovery`, `$journey-map`, or the relevant pack research skill. Apply the Pack Availability Guard for pack-based skills.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/uat-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
