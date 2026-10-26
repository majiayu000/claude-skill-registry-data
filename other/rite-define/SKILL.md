---
name: rite-define
description: "Define the first build plan from an approved spec: architecture, task slices, traceability, and state. Use when turning approved intent into its initial plan."
argument-hint: "[feature-slug]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/spec-grammar.md","rite-define/reference/plan-template.md","rite-define/reference/gates.md","rite-define/reference/anti-patterns.md","rite-plan/reference/slicing.md","rite-plan/reference/task-breakdown.md","rite-spec/reference/acceptance-criteria.md","rite-spec/reference/state-workspace.md"],"triggers":{"afk":["devrites-lib/reference/standards/afk-hitl.md"],"agents":["devrites-lib/reference/standards/agents.md"],"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"documentation":["devrites-lib/reference/standards/documentation.md"],"elicitation":["devrites-lib/reference/standards/elicitation.md"],"frontend":["devrites-frontend-craft/reference/fullstack.md"],"principles":["devrites-lib/reference/standards/principles.md"],"visual":["devrites-lib/reference/visual-playbooks/index.md"],"workflow":["devrites-lib/reference/standards/development-workflow.md"],"workflow-artifacts":["devrites-lib/reference/workspace-artifact-schema.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","strategy.md","design-brief.md","references.md"],"workspaceByRole":{"plan-drafter":["brief.md","spec.md","decision-coverage.md","questions.md","decisions.md","assumptions.md","architecture.md","strategy.md","design-brief.md","references.md","state.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase define` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-define: plan from the spec

Turn `spec.md` into architecture, vertical slices, traceability, and state. Spec owns
what/why; Define owns how. **Do not write code.**

## Rules consulted (read on demand from `.claude/skills/devrites-lib/reference/standards/`)

Pull these via `Read` when shaping the plan:

- [`development-workflow.md`](../devrites-lib/reference/standards/development-workflow.md): small batches, trunk-always-green, definition of done.
- [`principles.md`](../devrites-lib/reference/standards/principles.md): the project invariants (`.devrites/principles.md`) the chosen approach must conform to.
- [`documentation.md`](../devrites-lib/reference/standards/documentation.md): record plan-time decisions and rationale.
- [`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md), [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md), and [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md):
  load only for matching `spec.md` applicability rows; each applicable owner is mandatory.
- `../devrites-lib/reference/workspace-artifact-schema.md`: artifact purposes, budgets, IDs, and read triggers (trigger `workflow-artifacts`).

## Operating rules

- **Requires a readied spec.** Gate conditions and STOP routing are step 0;
  never plan it.
- Apply [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md) ownership. Prefer conventions; source-check new dependencies/design
  systems, asking only about licensing, cost, security, or policy.
- Author one `architecture.md`/`plan.md` section at a time. Before slicing, use
  [`elicitation.md`](../devrites-lib/reference/standards/elicitation.md) Tournament for open
  designs and Delphi for uncertain estimates.
- **Derive the slice count from the work.**
  One per independently-shippable increment, sized by [`slicing.md`](../rite-plan/reference/slicing.md); map every acceptance
  criterion. User counts are hints: explain honest differences, never pad/compress.
  `.devrites/AFK` `max_slices` is an iteration budget, not decomposition. A derivation
  over the [feature ceiling](../rite-plan/reference/slicing.md#feature-ceiling-split-an-epic-never-override-the-budget)
  is a split signal, never a `Budget override`: keep the thinnest shippable subset
  here and route the rest to Non-goals + continuation workspaces via the Drift Guard.
- **Complexity does not shrink scope.** Split/reorder; never drop/defer approved REQ/AC.
  Reduction needs Drift Guard + human decision; hard/large means decompose.
- **Wide refactors use expand → migrate → contract.** Add compatibility, migrate green
  batches, then remove the old path; if batches cannot stay green, use an integration branch
  plus final verify.
- **Root writes; drafter proposes** under bounded fresh context
  ([`agents.md`](../devrites-lib/reference/standards/agents.md)); root owns choices and canonical files.

## Workflow

0. **Read `.claude/skills/devrites-lib/reference/standards/core.md`:** the always-on operating rules and anti-rationalizations.
   Resolve the active slug from `.devrites/ACTIVE`, require its `state.md`, and
   re-open `spec.md` and apply [`spec-grammar.md`](../devrites-lib/reference/standards/spec-grammar.md)'s Native grammar re-read
   checklist. If there is no active workspace, no `spec.md`, the checklist
   fails, or its readiness gate hasn't passed →
   **STOP** and tell the user to run `/rite-spec <feature>` first.
   If `decision-coverage.md` is absent or does not say `Decision coverage: CLEAR`,
   **STOP** → `/rite-clarify`.
   If `checklists/` has no `<domain>.md` or any carries an open CRITICAL fail,
   **STOP** → `/rite-spec`.
1. **Read the spec:** `spec.md` (objective, requirements, acceptance, **placement**,
   design references, gaps/decisions), plus `references.md`, `decisions.md`,
   `assumptions.md`, `decision-coverage.md`, **`strategy.md` if present** (the scope mode, deferred / out-of-scope
   register, and pre-mortem risks from `/rite-temper`: cut slices to mitigate the top risks
   and respect the IN/OUT line; map coverage against the **hardened** spec), and
   **`design-brief.md` if the feature touches UI** (the UX/UI contract `/rite-spec` shaped:
   its key states, interaction model, and proof targets drive how UI slices are cut). If a blocking
   `[NEEDS CLARIFICATION]` remains, stop → `/rite-clarify`. Run the [`spec-grammar.md`](../devrites-lib/reference/standards/spec-grammar.md) marker
   sweep; a kept hit stops the same way, and its `marker sweep:` line goes in the step-7 digest.
   Reconcile every `Applicability map` row against live repository evidence. Load each
   applicable standard; a false `not applicable` is a blocking spec gap, not a planning
   shortcut.
1a. **Draft from fresh context.** Freeze the planning inputs and dispatch
   `devrites-plan-drafter` in `define` mode for one atomic candidate bundle:
   `architecture.md`, `plan.md`, `tasks.md`, and `traceability.md` with proof mapping.
   Validate its bounded result; it does not write/ask, and returns human choices to root.
   In the same parallel wave, dispatch one `devrites-evidence-scout` per external
   capability the plan will rest on — OS/SDK/native API, permission or sandbox,
   file format, toolchain, or third-party behavior — that neither live code nor a
   cited dossier already proves (at most three, as in Spec). Fold each dossier
   before step 2a: cite a proven capability in `architecture.md`; an unproven or
   contradicted one becomes a risk spike ordered before its dependent slices,
   never an assumption the build discovers.
2. **Reconcile architecture + approach** against live seams; root writes at step 6.
   `architecture.md` owns layers/boundaries/integrations/data/dependencies/risks/impact;
   `plan.md` owns build strategy. Use codebase-memory-mcp for structure/impact
   (`get_architecture`, `trace_path`; [`code-navigation.md`](../devrites-lib/reference/standards/code-navigation.md)) and source-check external behavior.
   Record significant options as `DEC-###` only for non-obvious real trade-offs where
   independently built lower units could choose incompatibly; leave other details to convention/
   slice. Compare ≥2 viable approaches for hard-to-reverse boundaries, models, contracts, or
   dependencies by drivers, trade-offs, and consequences. Specify cross-boundary interfaces for independent work:
   invariants, I/O, ordering/idempotency, errors, versioning, config, and relevant budgets.
   Establish repository/deployable roots, state and contract ownership, shared mutable
   resources, and deployment order under [`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md). For applicable durable
   data or integration rows, include the exact required plan table from [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md)
   or [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md); do not replace it with "handle retries/migration" prose.
   For any changed provider/consumer boundary, complete `plan.md`'s canonical
   `Shared contract proof` table with one reused contract artifact and provider- and
   consumer-side asserting tests that both consume it. Otherwise record the exact justified
   no-impact statement. Missing, one-sided, duplicated-contract, vague, or non-consuming proof blocks.
   **Deep-module check:** prefer small, stable interfaces hiding meaningful, testable
   behavior. Deepen/delete shallow modules whose interface matches implementation
   complexity. Put their independent behavior in `Tests/proof`; `/rite-vet` confirms.
2a. **Decision-horizon sweep.** Apply `reference/plan-template.md`'s classification to every
   question, assumption, architecture/dependency/proof choice, and checkpoint. Resolve
   planning items from source; only necessary executable evidence warrants a risk spike with
   discriminating criteria/fallback branches. Human blockers route to `/rite-clarify`.
   dispositions per `reference/plan-template.md` §Decision horizons.
3. **Create vertical tasks:** each delivers one independently verifiable, observable
   capability end to end; first is the thinnest useful path, ordered by dependency then
   risk. Apply the slice-count and broad-refactor rules above plus
   [`slicing.md`](../rite-plan/reference/slicing.md) and [`task-breakdown.md`](../rite-plan/reference/task-breakdown.md).
   Run `devrites-engine recall --paths <files likely touched>`; fold each relevant prior
   decision, carry-forward constraint, or finding into that slice's `Prior-slice learnings`.
   Mark per slice: **Frontend craft required**
   and **Browser proof required** (UI), and whether it's **fullstack** (FE+BE → contract
   first, see [`fullstack.md`](../devrites-frontend-craft/reference/fullstack.md)). **For UI slices, name which
   of `design-brief.md`'s key states + interaction the slice delivers, and give it a binary
   **Visual acceptance** target (state × viewport × input + target R-id/brief rule)**, so
   the design contract maps to slices as well as acceptance criteria.
   `Tests/proof` names exact command, cwd, expected signal, prerequisites, and mutable
   provenance inputs; `/rite-vet` preflights them. Write the portable repository command,
   never RTK/local wrappers, user-specific absolute paths, or temporary proof trees. When a
   shared contract changes, order its canonical artifact before both asserting tests and make
   provider/consumer dependencies explicit. Each exact `Characterization:
   characterize-before-modify` row is the first touching slice's prerequisite: observe and test
   unchanged baseline green, perturb realistic behavior red, restore green, then modify. Never
   expand this into repository-wide coverage.
4. **Map coverage and wiring:** every `AC-###` spec acceptance criterion maps to ≥1 `SLICE-###`
   ([`acceptance-criteria.md`](../rite-spec/reference/acceptance-criteria.md)); no orphaned criteria, no slice without a
   criterion except a [deferred slice](../rite-plan/reference/slicing.md#deferred-slice). Every proof row quotes the spec line it proves (`Proves`); proof that proves
   none goes to `test-plan.md` `## Deferred hardening`, never into a slice
   ([artifacts.md](../rite-vet/reference/artifacts.md)). Lift covered/backstop `Edge Coverage` rows and resolved `Prohibitions (must-NOT)`
   rows into `traceability.md` and `test-plan.md`; unresolved rows get a gate/owner. Each
   `Existing behavior to preserve` row becomes a regression row whose current evidence is
   observed green on the unchanged baseline at Vet (preflight `Run at` `vet`), again before the
   first slice touching that seam edits it, and green at Prove; a red baseline is recorded
   pre-existing, never relabelled. A slice whose `Files likely touched` names a manifest or
   lockfile also plans a `dependency-dry-run SLICE-###` preflight row ([artifacts.md](../rite-vet/reference/artifacts.md)).
   Mark a proof row `RUN: writer` only when it is local, needs no network, container or browser,
   and passes in an uncommitted worktree (an empty-`git diff` check stays root); its `gates.md`
   gate carries the attribute, the wright pre-runs it via `gates precheck`, and root still runs it.
   Evidence that cannot run takes `characterize-before-modify` or blocks. Each
   cross-slice boundary names producer, consumer, invariant, integration step, and proof.
   Map each applicable topology/data/integration risk to a slice, failure/recovery path,
   and discriminating proof; a risk cannot live only in the architecture narrative.
4a. **Persist traceability natively.** The drafter proposes and root writes
   `traceability.md` (`AC/REQ ID → slice → proof → evidence ID → files → status`).
   Re-read spec, tasks, and proof fields: every ID must exist and every mapping
   preserve meaning, not just labels. Reject orphans, inventions, and false mappings;
   `/rite-prove` and `/rite-seal` read this file directly. Reference the plan's
   `Shared contract proof` rows from existing slice/proof mappings; do not create a second
   traceability system.
5. **Complexity and deviations gate:** justify anything outside DevRites defaults (new dep,
   extra abstraction, second design system) in the plan; if you can't justify it, simplify.
   **Principles conformance:** read `.devrites/principles.md` (if present) and confirm the
   approach honors every declared invariant. A plan that conflicts with one is not "a deviation
   to justify away": either reshape the approach to conform, or, when the conflict is genuine and
   intended, route it through the Spec Drift Guard plus a recorded decision and a scoped principle
   exception a human approves. Never ready a plan that silently violates an invariant. (Re-scored
   as a blocking gate at `/rite-vet`; no file → none declared → nothing to check.)
6. **Write** `architecture.md`, `plan.md`, `tasks.md`, and `traceability.md` — save the
   accepted bundle under `packets/` and apply it with `devrites-engine state
   apply-bundle <slug> <bundle.json>` before root reconciliation edits; update
   `state.md` (phase: plan → next `/rite-vet`). When diagrams clarify, also write optional
   `flows.md` (**Mermaid-first**). If a richer reviewable visual earns it, emit
   `visual/<flow>.html` + `visual/<flow>.outline.md` after loading matching playbooks from
   [`../devrites-lib/reference/visual-playbooks/index.md`](../devrites-lib/reference/visual-playbooks/index.md)
   (progressive; never preload all seven), link the pair from `flows.md`, treat outline as
   SSOT (outline wins), and never require Lavish or a new phase.
6a. **Cross-artifact gate.** Read spec, tasks, and traceability together: every
   buildable AC/REQ maps to an existing slice/proof, every slice maps to real
   acceptance, and names/prose agree. Missing, duplicate, contradictory, or
   meaning-changing mappings block. Then run
   `devrites-engine check task-graph <slug>`; a malformed dependency graph blocks
   before Vet rather than spending a reviewer context on invalid tasks. Resolve each
   `ADVISORY size:`/`hub:` line now (split or seam slice, or a rationale); never blocking.
7. **Readiness gate** (`plan-template.md`): require CLEAR coverage; complete acceptance,
   wiring, shared-contract proof, applicable outputs, and rollback; risk-first acyclic order;
   justified deviations; and every horizon item present, with blockers resolved, planning
   items resolved/validly spiked, and local/action entries bounded and owned.
   **Stop and confirm** before code. Render the review-before-code
   digest first: `Intent` (one sentence from the spec), `Done means` (acceptance coverage x/y),
   `Plan sanity` (slice count + riskiest boundary/gate), `Expected build interruptions`
   (`none` or only justified action-time gates), and `Build exactly this?` (yes → approve;
   no → `/rite-plan revise`). When the human confirms the plan, write `Plan approved: <iso>` to
   `state.md` (see [state-workspace](../rite-spec/reference/state-workspace.md)).

## tasks.md slice format

Use the canonical slice grammar in
[`workspace-artifact-schema.md`](../devrites-lib/reference/workspace-artifact-schema.md#canonical-slice-grammar).
Every slice must satisfy that complete field set; phase-specific gate details live in
[`reference/gates.md`](reference/gates.md).

> **Mid-flight discipline.** Do not skip vertical slicing, coverage mapping, or
> dependency ordering. See [`anti-patterns`](reference/anti-patterns.md).
