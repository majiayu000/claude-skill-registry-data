---
name: orient
description: |
  Project-orientation workflow (/orient): installs predicate's enforcement
  into a target project, maps its structure and goal, and authors the
  persistent conditioning layer (AGENTS.md goal-hierarchy) so every
  subsequent walk is anchored and gated.
  Trigger when:
  - Onboarding a new project into predicate for the first time.
  - Refreshing an existing project's AGENTS.md hierarchy against the
    current state of the repository (re-run = refresh).
  - Prompt contains: /orient, orient workflow, onboard project, project
    orientation, AGENTS.md hierarchy, persistent conditioning layer.
---

# Orient: Project Orientation Workflow

Predicate is **project-centric**: `/orient` is its first contact with a
project. It engages *this* repository concretely — installs predicate's
enforcement, maps the repo, learns its goal, and authors the **persistent
conditioning layer** (the AGENTS.md goal-hierarchy) so every subsequent
walk is anchored and gated. Not an idealized formula imposed from outside;
a boundary fitted to the actual project.

**Quickstart:** install predicate into your harness → target a project →
run `/orient`.

---

## Phases (state machine; halts at the two human seams)

The eight phases execute in order. Two are **human seams** — the walk
halts and awaits human input before continuing. The others are
mechanical or agent-automated.

### Phase 0 — BOUND *(compose `/boundary` — do not rush)*

Before touching the repo, invoke [`/boundary`](../boundary/SKILL.md) to
draft an IBC for the orientation work itself: what is this project, what
is known vs unknown going in, what is the desired end state of onboarding
it.

`/boundary` is also the **authority for the AGENTS.md contract** the
AUTHOR phase (phase 6) conforms to — composed here, not duplicated. The
required content (Goal, Requirements/Invariants/Constraints, Unknowns,
Operational entrypoint, Structure, Alignment-to-parent) and the soundness
invariants are defined in
[`/boundary §AGENTS.md`](../boundary/SKILL.md#agentsmd--the-project-scope-boundary).

### Phase 1 — ESTABLISH *(mechanical, automated — no human input)*

Run `bootstrap/install.sh init --project <dir>`: install git hooks into `.git/hooks` (untracked,
auditable, removable), initialize the `.ledger` sub-repository, wire
project config. Idempotent — safe to re-run on an already-oriented
project.

### Phase 2 — MAP *(domain — outward→structure; cheapest tier; hunt-to-dry)*

Fan out a multi-modal sweep over the repository:

- **Structure** — `git ls-files` for the file tree; directory layout.
- **Semantics** — what each component does; package/module roles.
- **History** — `git log` shape; maturity signals; areas of churn.
- **Docs** — stated purpose in READMEs, existing AGENTS.md files, or
  architectural docs.

Scale to the repo: a small project needs one pass; a large one warrants
the full sweep. Stop when no new approach-relevant structure surfaces.
This phase carries no goal-fit judgment and routes to cheap agents.

### Phase 3 — SURVEY *(arsenal — outward→environment; cheapest tier)*

Enumerate predicate's own skills plus the host harness's installed
skills, tools, and MCP servers available to this project. Project each
for relevance to the discovered structure; do not enumerate exhaustively
into context.

### Phase 4 — ELICIT *(goal — HUMAN SEAM, halt)*

**This phase halts.** The walk does not proceed until the human confirms
the goal.

From the MAP, extract a candidate goal + requirements / invariants /
constraints / known-unknowns. Present the candidate to the human with:

- the extracted goal statement (desired end state, not status);
- the requirements, invariants, and constraints identified;
- the known-unknowns with signposts (what would resolve each);
- any conflicting signals in the docs or history that affect goal-fit.

**Halt and await confirmation.** Goal-fit is not self-attestable — an
agent is least calibrated exactly here; the human is the goal authority.
Do not proceed to NEST or AUTHOR until the goal is confirmed or corrected.

### Phase 5 — NEST *(structure decision)*

Decide which directories have a goal *genuinely distinct from and in
service of* the root goal, and therefore warrant their own AGENTS.md.

**Default: root only.** Add a component AGENTS.md only when a real
sub-goal exists. Every additional file is a staleness surface: it must be
kept true, linked correctly, and synced at every refresh. The
alignment-to-parent requirement (from the AGENTS.md contract) is the
defeater substrate — a component whose goal does not serve the root is
a structural fault.

### Phase 6 — AUTHOR *(draft against the contract — authority: `/boundary`)*

Draft the root AGENTS.md and any component files decided in NEST. Each
draft MUST conform to the AGENTS.md contract in
[`/boundary §AGENTS.md`](../boundary/SKILL.md#agentsmd--the-project-scope-boundary):

- **Self-contained entrypoint.** Every pointer resolves in-repo or
  carries a URL. No assumed external knowledge.
- **Goal = desired end state**, not a status report. Marked WIP where
  the end state is not yet reached.
- **Single source.** Reference authorities
  ([rules.md](../../rules.md), [ambient.md](../../ambient.md), specs);
  never copy their text.
- **Agent-guiding only.** If removing a line changes no agent action,
  cut it.
- **Unknowns are first-class**, treated like requirements, each with a
  signpost.
- **Minimal surface area.** Every line is a liability kept true;
  brevity is anti-drift.

Component AGENTS.md files MUST include the alignment-to-parent section
(how this component serves the root goal).

#### AGENTS.md as R/I/U Hierarchy — the P-TRACK persistent anchor

Each AGENTS.md (root and component) MUST include a **Requirements /
Invariants / Unknowns** hierarchy for the construct it governs (P-TRACK
I-T1–I-T2, primitives-spec.md §P-TRACK §"The AGENTS.md fusion"). This
makes AGENTS.md the *persistent anchor* that every subsequent walk
hydrates its live tracker from, rather than reconstructing from scratch.

**Required sections per construct AGENTS.md:**

```markdown
## Requirements
Each item: statement, grounding (source/evidence), signpost (what defeats it).
Pruned to the minimal bounding set — requirement bloat is drift surface.

## Invariants
Each item: statement, grounding, signpost (what would violate it).
Constraints that must hold throughout; distinguished from requirements by
"must hold" vs "must be satisfied."

## Unknowns
Each item: statement, grounding (why it is not yet resolved), signpost
(the observable that would resolve or invalidate it).
Treated first-class like requirements — filed with a signpost, never
merely noted.

## Spec Pointers
Pointers to full specification sources for this construct: doc paths,
ADR links, contract file paths. Kept minimal — one pointer per
authoritative source, never prose summaries of the specs themselves.
```

**Authoring discipline:**
- Items MUST carry `grounding` and `signpost` (mirrors the
  `context_map.ncl` Item contract; `last_validated` is filled in by
  the walk that hydrates, not the orient author).
- The Unknowns section tracks *known-unknowns* with signposts; when
  a walk surfaces an *unknown-unknown*, it files it here (promoting
  it to a known-unknown with a signpost) via the promotion combinator.
- Do not copy spec text into AGENTS.md — point to the spec. The pointer
  is durable; the prose diverges and must be cut.

**Nest depth:** add an R/I/U hierarchy to a component AGENTS.md only
when the component has a genuinely distinct sub-goal (Phase 5 NEST
criterion). A root-only project has one R/I/U hierarchy in its root
AGENTS.md covering all constructs.

### Phase 7 — RECONCILE *(HUMAN SEAM — the sync gate)*

**This phase halts.** The persistent layer mutates only through this
reconciliation — never silently.

Present each draft AGENTS.md to the human. The human reconciles
(the volatile draft → persistent sync). On approval, land files at their
target paths (root `/AGENTS.md`; component `<dir>/AGENTS.md`).

**Unanswered questions** from the known-unknown registry that were not
resolved during ELICIT are re-presented here for prioritization, so a
topic-change does not lose them.

---

## Re-run = Refresh (anti-rot)

On an already-oriented project, `/orient` is the **sync/refresh** pass.
Run it whenever the AGENTS.md hierarchy may have drifted from reality.

The refresh pass re-executes the same eight phases but MAP and SURVEY are
diff-scoped (what changed since the last orientation). ELICIT surfaces
**drift candidates**: stale claims, dead links, a parent goal a child no
longer serves (a defeater), requirements that became constraints or vice
versa.

RECONCILE on a refresh presents only the changed sections, not the full
file. **Surfaced-but-unanswered known-unknowns from prior orientations
are re-presented** so they are never silently dropped.

---

## Hydration Protocol — live tracker hydrates from AGENTS.md

When a walk begins on an **oriented project** (AGENTS.md hierarchy
exists), it MUST hydrate its live `context_map` tracker from the
relevant construct's AGENTS.md, not from scratch. (P-TRACK I-T1–I-T2;
primitives-spec.md §P-TRACK §"The AGENTS.md fusion".)

**Hydration steps:**

1. **Locate the governing construct AGENTS.md.** For a root-scoped task:
   the root `AGENTS.md`. For a component-scoped task: the component
   `AGENTS.md` (if it exists) plus the root for alignment.
2. **Read the R/I/U sections.** Extract each item from the
   Requirements, Invariants, and Unknowns sections.
3. **Populate the context-map items.** For each extracted item, set:
   - `id`: a stable identifier (e.g. `R1`, `I2`, `U3`)
   - `statement`: the item text
   - `kind`: `'requirement`, `'invariant`, or `'unknown`
   - `grounding`: the grounding from AGENTS.md (or the AGENTS.md
     pointer itself if none is recorded: `"AGENTS.md#requirements"`)
   - `last_validated`: today's date (ISO 8601) — the hydration date
   - `signpost`: the signpost from AGENTS.md
   - `hydration_source`: `"<path>#<section>"` (e.g. `"AGENTS.md#requirements"`)
     — records that this item came from the persistent anchor
4. **Export and verify.** The populated context-map MUST pass
   `nickel export` against `context_map.ncl` (`ContextMap` contract)
   before the walk proceeds.
5. **Start from scratch only when unoriented.** An unoriented project
   (no AGENTS.md) initializes an empty context-map and populates it
   during the walk. This is the fallback, not the default.

**Hydration is the first step of every walk** on an oriented project,
before any task work. A walk that skips hydration and starts from scratch
on an oriented project violates I-T1 (absence = all-unknown-unknown). The
`tracker_fresh.sh` gate enforces this: a stale `last_validated` on a
`hydration_source` item signals the anchor has drifted.

---

## Reorientation — ongoing disposition, triggered by staleness

**Reorientation is not a scheduled re-run; it is a disposition triggered
by staleness.** (P-TRACK I-T3; primitives-spec.md §P-TRACK §"reorientation
as an ONGOING disposition".)

A staleness trigger fires when:

- The `tracker_fresh.sh` gate reports `STALE` on any context-map item
  (a `last_validated` is behind the HEAD commit date).
- A landed change **contradicts a tracked R/I** in the context-map —
  a requirement is now wrong, an invariant is now broken, or a
  known-unknown has been resolved. This is premise-freshness lifted to
  the persistent tracker.
- A walk surfaces an **unknown-unknown** that, once filed, contradicts
  an existing Requirement or Invariant in AGENTS.md.

**On a staleness trigger:**

1. Run `tracker_fresh.sh <context-map-instance.ncl>` to identify stale
   items and their `hydration_source` pointers.
2. For each stale `hydration_source`: read the corresponding AGENTS.md
   section and compare against the current state.
3. If drift is **tactical** (the item's signpost has not fired; the
   item is still valid, just needs its `last_validated` updated):
   update `last_validated` in the context-map and continue.
4. If drift is **strategic** (the item's signpost HAS fired — a
   requirement is contradicted by reality, or an unknown is resolved):
   this is a **Strategic Escalation** (ambient.md §Planning Invariants).
   Emit an ESCALATION block, update the live tracker and the AGENTS.md
   persistent anchor via `/orient` refresh, and halt for human review.

**Reorientation scope.** A tactical re-validation (step 3) does not
require re-running the full eight-phase workflow — it is a targeted
tracker update. A strategic reorientation (step 4) re-runs at minimum
MAP (diff-scoped) and ELICIT, and presents the corrected R/I/U sections
at RECONCILE for human confirmation before writing back to AGENTS.md.

**Staleness is not an error.** A stale item is a signal, not a failure.
The failure is ignoring the signal — carrying a stale, unverified
requirement forward into task work (rules.md §7: reconstruct, don't
recall).

---

## Tier Economy

| Phase | Tier | Rationale |
| :--- | :--- | :--- |
| 0 BOUND | Architect | Bounding judgment; goal-fit stakes highest here |
| 1 ESTABLISH | Mechanical | Pure bootstrap execution; no judgment |
| 2 MAP | Cheap agents | Structure survey; no goal-fit judgment |
| 3 SURVEY | Cheap agents | Enumeration and relevance projection |
| 4 ELICIT | Architect + Human | Goal-fit is not self-attestable; human seam |
| 5 NEST | Architect | Structural coupling judgment |
| 6 AUTHOR | Architect | Contract-conformant draft |
| 7 RECONCILE | Human | Persistent layer mutates only here |

---

## See Also

- [`/boundary`](../boundary/SKILL.md) — the authority for the IBC
  sufficiency conditions (phase 0) and the AGENTS.md contract (phase 6).
- [`/campaign`](../campaign/SKILL.md) — for multi-workstream orchestration
  after orientation is complete.
- [`rules.md`](../../rules.md) — the governing Prime Invariants every
  AGENTS.md references.
- [`ambient.md`](../../ambient.md) — the always-on principles the
  AGENTS.md hierarchy anchors to.
- [`ledger/gate/tracker_fresh.sh`](../../ledger/gate/tracker_fresh.sh) —
  the freshness gate; checks whether context-map `last_validated` fields
  are current against HEAD. Fresh→0, Stale→1.
- [`ledger/contracts/context_map.ncl`](../../ledger/contracts/context_map.ncl) —
  the live tracker carrier contract; `hydration_source` field records the
  AGENTS.md anchor a hydrated item came from.
- [`skills/orient/tracker_freshness.ncl`](./tracker_freshness.ncl) —
  the Nickel functional core: `is_fresh` and `stale_items` predicates.
