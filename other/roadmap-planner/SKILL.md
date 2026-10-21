---
name: roadmap-planner
owner: baseline
description: >
  Derive an execution roadmap from a project's vision/spec docs by first principles, then diff that
  fresh derivation against the existing roadmap to prove the task ORDER is correct. Use this whenever
  the user wants to review, validate, re-derive, or sanity-check an execution roadmap or delivery plan;
  asks whether the tasks/epics are "in the right order"; suspects a task is scheduled before its
  prerequisite (a producer-after-consumer / dependency-inversion error like "OpenAPI after the web
  client that consumes it", OR a cross-cutting inherited default like observability/auth/tenancy
  scheduled after the feature work that inherits it — a seam-after-consumer error); wants to find
  missing tasks, circular dependencies, or over-fragmented epics; or wants to compact a plan to raise
  velocity. Also trigger on "review the roadmap", "re-derive the plan from the spec", "is this the right
  build order", "check the dependency graph of our epics", "which task should come first". It reads the
  vision + spec corpus, decomposes actors → use-cases → modules → epics → typed tasks, identifies
  cross-cutting inherited-default seams, builds a real dependency graph with hard + soft (seam) edges
  (deterministic helper), breaks cycles, topologically orders, compacts, and emits a derived roadmap
  PLUS a delta report against the current one — it never blindly overwrites a hand-crafted roadmap.
disable-model-invocation: true
---

# roadmap-planner

Prove an execution roadmap's task **order** is correct by re-deriving it from the source of truth
(the vision + spec), then diffing the derivation against the existing plan.

The core insight: a roadmap is a **schedule over a dependency graph**. Most planning errors are not
"wrong task" — they are **producer-after-consumer**: a task that produces something (a contract, a
schema, an SDK, a service) is scheduled *after* a task that consumes it. Reading the roadmap top-to-
bottom never catches this; only building the actual dependency graph does. So we derive the tasks
from use-cases, wire the graph explicitly, and let a deterministic pass find every ordering violation.

**You produce two artifacts, never a silent overwrite:**
- a freshly-derived, dependency-ordered roadmap (a *proposal*), and
- a **delta report** vs the existing roadmap — ordering violations, missing/extra tasks, circular
  dependencies found + how they were broken, and compaction candidates.

The human reviews the delta and decides what to adopt. The existing roadmap is often hand-crafted with
context the spec doesn't capture; the derivation's job is to *challenge* it, not replace it.

## Inputs (parameterize per project)

- **Corpus** — the vision/spec/requirements docs to derive from. Point it at wherever the project keeps
  its source of truth (a `docs/spec/**` tree, a product-requirements doc, a genesis/seed file, ADRs).
  Actors + use-cases usually live in the requirements/product docs; modules/engines/services in the
  architecture/design docs. If the project has no written spec, derive from the README + issue tracker
  and flag the thin provenance as a finding.
- **Existing roadmap** — the plan to validate. Default: `project.json → roadmap.path` (this baseline's
  default is `docs/roadmap-execution-plan.md`).
- **Buckets** — the delivery lanes, project-defined. Set them in the `tasks.json` top-level `buckets`
  array; they only rank ties in ordering. A single-lane project can use one bucket (e.g. `app`); a
  platform/product split might use `platform`, `product`, `web`, `app`. There is no fixed lane set.

If the user names a different corpus or roadmap, use those. If no roadmap exists yet, skip the delta
and emit only the derived roadmap.

## The method (10 steps)

Steps 1–4 are **read-heavy discovery** — run them as a multi-agent workflow when the corpus is large
(see "Execution engine"). Steps 5–10 are **synthesis + mechanical graph work** in main context.

**A running rule for every step: derive AND reconcile.** Do not derive in a vacuum. The spec usually
already declares modules (e.g. a module-boundaries chapter) and actors (e.g. a user-roles chapter).
Derive fresh from use-cases, then reconcile against what the spec declares. Every disagreement
(a module you derived that the spec omits, or vice-versa) is a **finding**, not something to silently
paper over.

1. **Actors → use-cases.** Read the corpus and list every actor and the use-cases each performs. The
   union of use-cases is the complete solution. Capture each use-case with a stable id, its actor, and
   a one-line intent. Cite the source doc/section. This is the ground truth everything else traces to.
2. **Black-box → modules.** Treat the system as one black box that satisfies all use-cases, then break
   it into `n` functional modules by cohesion (a module owns a coherent slice of the use-cases). Name
   modules by *capability*, not technology.
3. **Interfaces + NFRs.** For each module, state its high-level interface (the intent it exposes to
   other modules — not signatures) and extract the non-functional requirements that bear on it
   (security/tenancy, performance, availability, compliance, versioning, **maintainability/diagnosability**).
   NFRs become task *constraints* (a hard `deps`/`seamDeps` edge when they gate) **and feed the
   non-functional scoring lens** (Step 8b) — they are not free-floating prose.
4. **Platform vs solution.** Cluster modules into **platform** (reusable, product) vs **solution**
   (customer-specific assembly). This is the level-1 system design. A module that encodes customer
   logic is solution; a reusable capability is platform. Record the rationale per module.
4a. **Inherited-default seams (cross-cutting).** Extract the project's **inherited-defaults family** — the
   cross-cutting concerns every feature is expected to pick up automatically (commonly security, audit,
   tenancy, and observability; a project's spec may name its own). These concerns create **no hard `deps`
   edge** — feature code compiles and runs without them — so a plain producer→consumer graph scatters
   them to the tail. For each concern: (a) apply the **contract/backend split** — a *seam/contract* task
   (the interface every consumer is written against; scheduled early) and a *backend* task (the concrete
   sink/implementation; deferrable); (b) draw a soft **`seamDeps`** edge from each first-consumer task to
   the seam/contract task (Step 8). The helper floats the seam early and relaxes it (advisory) only if a
   hard edge legitimately forbids earliness. **Reconcile:** if the project treats a concern as an
   automatic default, a feature epic with no seam edge to that applicable default is itself a **finding** —
   a seam-after-consumer waiting to happen — not something to pass over.

5. **Epics.** Cluster use-cases by high-level intent → `n` epics. An epic is a coherent capability a
   demo/release can show. Each use-case lands in exactly one epic.
6. **Typed tasks.** Within each epic, split its use-cases into three task categories:
   **Infrastructure** (scaffolding, storage, wiring, contracts), **Business Logic** (domain rules,
   engines), **Interface** (APIs, UI, SDKs). One use-case may yield tasks in more than one category.
7. **Bucket + intra-epic order.** Map each typed task onto one of the 4 buckets
   (platform / solution / web / app) and arrange within the epic. Natural intra-epic flow is usually
   Infrastructure → Business Logic → Interface, and platform → solution → web/app — but that is a
   heuristic, not the truth. The truth is the dependency graph (Step 8), which overrides any bucket
   heuristic.
8. **Dependency graph + cycle-breaking (DETERMINISTIC).** Give every task a stable id and declare its
   dependency edges (`A depends on B` means B must ship before A). Then run the helper:
   `node .claude/skills/roadmap-planner/scripts/graph.mjs analyze <tasks.json>`. It topologically sorts, **detects cycles**, and
   flags any task ordered before a task it depends on. **On a cycle**, split *both* tasks into
   independent sub-tasks that break it (e.g. extract the shared contract A and B both need into a
   third task both depend on), update the edges, and re-run. This is **recursive** — keep splitting
   until the graph is acyclic. The judgment (what depends on what, how to split) is yours; the cycle
   detection + topo-sort is the script's. **Also declare `seamDeps`** (soft/seam edges) alongside `deps`
   for the Step-4a inherited-default concerns: the helper floats seams early, relaxes any a hard edge
   forbids (advisory, never a gridlock), and — when `order` is present — flags a **`seam-after-consumer`**
   (an admitted seam scheduled at/after its consumer) as a blocker (exit 3). See `references/graph-schema.md`.
8b. **Priority scoring — two lenses (WSJF).** The edges answer "is this order *legal*?"; the
   score answers "among legal orders, which is *good*?" **Impact is stakeholder-relative** — a single
   impact number hard-codes one stakeholder (usually business) and starves engineering-discipline work
   (the meta-cause of seam-after-consumer). So score each task through **two lenses**: `functionalValue`
   (business value — **product-owned**) and `nonFunctionalValue` (maintainability / diagnosability /
   security-posture — **owned by the architecture owner**, not the feature stakeholder; that ownership is
   the structural seat that stops engineering from being business-scored). The helper ranks the
   *topologically-ready set* by `weightedAverage(functionalValue, nonFunctionalValue; weights) / effort`
   (top-level `weights`, default 50/50) — it **never crosses a hard edge**, so it only sequences work
   that is already eligible. This buys **deferral for free**: a low-value/high-effort task (e.g. a
   deferred backend from Step 4a) floats as late as its dependents allow — no milestone node needed.
   Genuine hard phase-gates stay `deps`. For a **judgment call** the score gets wrong, set
   `scoreOverride` + a required `overrideReason` (a human-directed call; auditable). Scoring
   is **advisory** — it never blocks. See `references/graph-schema.md`.

9. **Ordered roadmap.** The topological order (with buckets + epics preserved) is the derived
   execution roadmap. Emit it. **Sanity-check the emitted order:** the helper proves the order is
   *legal*, not *sensible* — if a backend/Infrastructure/hardening task lands before the Business-Logic
   it supports, that is an under-scored or under-anchored deferral (raise its consumers' scores, add the
   real gate as a `dep`, or set a `scoreOverride`), not a valid plan.
10. **Compaction.** Re-run `node .claude/skills/roadmap-planner/scripts/graph.mjs compact <tasks.json>` to list merge candidates —
    tasks in the same epic+bucket with no dependency between them (parallelizable → one slice), or a
    chain `A → B` where B depends only on A in the same bucket (collapsible). Reducing task count
    raises velocity: every extra task boundary is intake/spec/review ceremony. Merge where it doesn't
    hide a real dependency or blow up slice size. Compaction never reorders across a real edge.

## The graph helper (`scripts/graph.mjs`)

The deterministic core of Step 8/10. It reads a tasks JSON and does the mechanical graph work so
"is the order correct?" is a computed answer, not a vibe. Full I/O contract + the tasks JSON schema:
`references/graph-schema.md`. Quick reference:

- `node .claude/skills/roadmap-planner/scripts/graph.mjs analyze <tasks.json>` — topo-sort; report **cycles** (with the cycle path),
  and **order violations** (a task whose `order` is ≤ a dependency's `order`, i.e. scheduled too
  early). Exit 0 = acyclic + no violations; exit 2 = cycle; exit 3 = ordering violation(s).
- `node .claude/skills/roadmap-planner/scripts/graph.mjs order <tasks.json>` — print one valid dependency-respecting order (stable:
  ties broken by bucket rank then id) — the Step 9 order.
- `node .claude/skills/roadmap-planner/scripts/graph.mjs compact <tasks.json>` — list Step-10 merge candidates.

The JSON is *your* structured output from Steps 1–7 (tasks with `id`, `epic`, `bucket`, `category`,
`title`, `deps`, and — for validating an existing roadmap — `order` = its current position). You build
it; the script judges it. Keep the intermediate `tasks.json` in the workspace so a re-run is cheap.

## Execution engine (large corpus → multi-agent workflow)

Steps 1–4 read the whole corpus (here: ~45 spec chapters). That is a fan-out shape: one reader per
doc-cluster extracting `{actors, use-cases, modules, interfaces, NFRs}` as structured JSON, merged in
main context. Use the `Workflow` tool for this when the corpus is more than a handful of files —
parallel readers, then a synthesis/dedup barrier, then the (single-context) Steps 5–10. For a small
corpus, a single-context read is fine. The workflow is the engine; this skill is the recipe it runs.

Fan-out sketch (adapt to the corpus):
- **Readers** (parallel): partition the corpus (e.g. requirements/roles/ACs in one cluster;
  architecture modules/engines/services in another; the API/UI/data chapters). Each returns structured
  actors/use-cases/modules/NFRs with source citations.
- **Synthesis** (barrier): dedup + reconcile into one actor/use-case/module set; flag spec-vs-derived
  disagreements.
- **Order + compact**: build `tasks.json`, run the helper, break cycles, emit derived roadmap + delta.

## Output

Write two files (default under `docs/roadmap/`, or where the user says):

- `derived-<YYYY-MM-DD>.md` — the derived, dependency-ordered roadmap: actors/use-cases traceability
  table, module + platform/solution split, epics, and the ordered typed tasks with their deps.
- `delta-<YYYY-MM-DD>.md` — findings vs the existing roadmap, ranked by severity:
  1. **Ordering violations** (producer-after-consumer) — the highest-value finding; name the task, the
     prerequisite it precedes, and the fix.
  2. **Circular dependencies** found + how they were broken.
  3. **Missing / extra tasks** — in the derivation but not the roadmap (or vice-versa), each traced to
     a use-case (or flagged as unjustified).
  4. **Compaction candidates** — over-fragmented epics that can merge without hiding a dependency.
  5. **Spec-vs-derivation disagreements** (Step-1/4 reconciliation).

Lead the delta with a one-paragraph verdict: is the current order sound, and what are the top 3 fixes?

## Constraints

- **Never blindly overwrite the existing roadmap.** Emit a proposal + delta; the human adopts.
- **The dependency graph is the source of truth for order**, not the bucket/category heuristics. If the
  graph and the heuristic disagree, the graph wins and that disagreement is a finding.
- **Every task traces to a use-case; every use-case traces to an actor + a spec citation.** A task with
  no use-case behind it is a finding (possible gold-plating). A use-case with no task is a gap.
- **Deterministic where it can be.** Cycle detection, topo-sort, and violation-flagging go through the
  helper, not eyeballing. The model supplies judgment; the script supplies proof.
- **Reduce, then stop.** Compaction serves velocity; don't over-merge into mega-tasks that hide
  dependencies or exceed a sane slice size.
