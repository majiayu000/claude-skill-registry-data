---
name: roadmap-planning
description: "PM-GATED. Shape research into ratified roadmap batons."
version: 2.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "Skill"]
argument-hint: "<input-corpus-path|problem-set-path|roadmap-seed-stub-path> [--run-id <slug>]"
---

# Roadmap Planning — From Inputs to Sequenced Spinoff Stubs

Turns a corpus of inputs (research, deep-dives, brainstorming, or a ratified problem-set) into a
sequenced backlog of `kind: roadmap-baton` stubs — dispatchable, pickup-able handoffs, not a plan
doc. Use when 5+ candidate items need sequencing into gated waves (one feature → `coordinator:plan`;
architecture call → `coordinator:staff-session`; bug batch → `coordinator:bug-blitz`; option
exploration → `coordinator:brainstorming`). **Exception:** a `kind: roadmap-seed` pickup (Entry
Point B) is exempt from the 5+ floor — goal-setting already scoped it as one roadmap's worth of work.

## Entry points

Detail for B/C/D, read before starting Phase 1 on that path: `residue/entry-points-b-c-d.md`.

- **A** — direct invocation, `<input-corpus-path>` is the corpus dir. Begin at Phase 1.
- **B** — pickup of a `kind: roadmap-seed` stub (goal-seeded) → `§ Entry Point B`.
- **C** — chain from `/shape` (`estimated_horizon: week`) → `§ Entry Point C`.
- **D** — conform intake from a sizing-object (`xl_exit: roadmap`), never a gate → `§ Entry Point D`
  (`residue/entry-points-b-c-d.md`). Receive-and-use-if-present: with no sizing-object present this
  skill runs exactly as today, and the sizing lobby never gates or refuses a `roadmap-planning`
  invocation absent one.

## Ceremony ladder

```
/goal-setting → kind: roadmap-seed stubs → /roadmap-planning → kind: roadmap-baton stubs
  → coordinator:plan → plan-doc → execute-plan → executor chunks
```

Batched, the tail is `plan-blitz → mise-prep → the run`: **each exit is the next entry, read off
disk, never retyped** (`A-HANDOFF-AN-EM-RETYPES-IS-NOT-A-SEAM`).

`/mise-prep` drives the mise-prep stage (`commands/mise-prep.md`); the engine's
`plan.stamp_prepped` is the only writer of the attest and re-runs the authoring bar itself.
`/mise-en-place` § Phase 0 consumes it.

---

## Phase 1 — Synthesize: input corpus → verdict-grid

Every cluster gets exactly one verdict — no "we'll see". Inverse coverage (verdict → stub) is
Step 2.6's job (below).

1. Inventory every input file (title + summary) → `state/roadmap/<run-id>/inventory.md`. Also read
   `docs/architecture/systems-index.md` and the system pages the corpus touches, noting each
   `last_attested`; every pass, sizing-object or not. The inventory row also MARKS each input that
   is a live plan under `docs/plans/` — this is the only step that walks the corpus, so the only one
   that can record it (`residue/source-plan-supersession.md`).
2. Cluster into coverage units (typically 20–60/roadmap); a sub-floor cluster folds into a
   sibling here, pre-verdict (wiki: grain-fold vs. MERGE) → `state/roadmap/<run-id>/clusters.md`.
   Every cluster carries `loe:`; `roadmap.blitz_stage` refuses a clusters.md missing one.
   **A cluster is a unit of coverage accounting, never a unit of dispatch** — how many batons
   these become is Step 2.1.6's call, not this step's.
3. Verdict each cluster — MERGE / DEFER / KEEP / DROP / MOVE — into
   `state/roadmap/<run-id>/reconciliation.md`. Verdict count must equal cluster count.
4. Conflicts → `state/roadmap/<run-id>/COORDINATOR-RESOLUTIONS.md` (template:
   `residue/coordinator-resolutions-format.md`), authoritative over any stub.

**Exit:** inventory + verdicts complete and balanced; resolutions doc present if conflicts; every
sub-floor cluster folded or dispatched.

---

## Phase 1.5 — Substantiate: research + OVERVIEW + peer-team asks (PM-gated, double-approved)

Mandatory, never skipped (wiki: why).

**UE-cluster precondition:** confirm `mcp__project-rag__project_semantic_search(query="UClass",
source="unreal", limit=1)` returns a hit before any UE-internal-API cluster proceeds; unavailable →
STOP those clusters, never substitute web scouts, surface to PM. Other clusters unaffected.

1.5.0. Assess research depth (EM judgment, PM-authorized) — `residue/research-depth-assessment.md`
   before dispatching scouts; `/research` is PM-gated, never EM-auto-invoked.
1.5.1. Dispatch one scout per KEEP/MERGE-target cluster (cap 8 concurrent), brief =
   `${CLAUDE_PLUGIN_ROOT}/snippets/internet-research-scout.md` + cluster scope → `research-corpus/<topic-
   slug>.md`, ≥2KB. Exceptions (per-project material, measurement-derived corpus): wiki.

   > **Do not ask whether to dispatch** — invoking this skill IS the request; no other gate dissolves.
1.5.2. Author `OVERVIEW.md`, one section per KEEP cluster, headed by NAME never number (wiki:
   why); each section cites its research-corpus file and carries `### Contested` (required, even
   empty). Frontmatter template: wiki. It carries a `### Atlas consult` section (pages read,
   `last_attested`, what changed).
1.5.3. `peer-team-asks.md` — must be present, empty as `- None identified at authoring time.`
   (template: `residue/peer-team-ask-format.md`); the consumer-render probe for any cross-repo contract is answered here, before 1.5.4 — wiki: writing-plans.md § Consumer-Surface Enumeration Before Fixing Deliverable Shape.
1.5.4. PM round 1 (shape approval) before reviewers run — framing template: wiki. On approval,
   `status: shape-approved`.
1.5.5. Sequential reviews — the Staff Engineer, or the Director of Engineering on cross-repo/cross-team boundaries; domain reviewer
   by flavor. Sidecar contract + altitude rule (shared with Step 2.8): wiki.
1.5.6. PM round 2 (final approval) with a diff vs. shape-approved — framing template: wiki. On
   approval, `status: final-approved`. **Phase 2 MUST NOT start without it** — unless the PM
   pre-waived round 2 at round 1 with a recorded "execute and adjust" ruling (verbatim utterance,
   recorded alongside the round-1 approval); that waiver stands in for round 2 and Phase 2 may
   start on it directly.

**Exit:** research-depth recorded; every KEEP cluster has a research-corpus file; OVERVIEW cites +
`### Contested` per section; peer-team-asks present; both reviews integrated; `status:
final-approved`.

---

## Phase 2 — Plan: stubs + STUB-INDEX + constraint graph + PM-gates + reviews

**Entry:** OVERVIEW `status: final-approved`, Phase 1.5 exit checked — else STOP, return to Phase 1.5.
Step 1.1's live-plan marks are CHECKED here, never re-discovered; each marked plan with a KEEP or
MERGE-target cluster owes retirement at Phase 2 close
(`residue/source-plan-supersession.md`).

2.1. Scaffold each stub (Shape W, `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`):
   `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-doc-new.exe" --type roadmap-baton --title "<title>" --roadmap-id <run-id> --stub-id <slug>-<N> --out state/handoffs/<date>_<HHMMSS>_roadmap-<slug>-<N>.md`,
   mint the id (`bin/mint-deliverable-id --stub-id "<slug>-<N>"` → `deliverable_id:`), fill the rest
   from Step 2.1.5's numbering output. **Read `residue/stub-frontmatter-schema-and-field-notes.md`
   first.**

<!-- engine-gap: field=roadmap_planning.stub_body_section_completeness producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->
2.1a. **Every stub carries its own sizing, never the roadmap's.** `roadmap.blitz_stage` mints
   a per-baton sizing and stamps `sizing_object:`. Never pass the roadmap's sizing to a stub:
   batons sharing a sizing all link to its plan. Tripwire:
   `A-BATON-IS-NOT-A-SIZING-ARTIFACT`.
2.1.5. Number stubs in dependency order before writing any — run (Shape W,
   `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`)
   `& "$env:COORDINATOR_SETTINGS_HOME\bin\roadmap-number-stubs.exe" <edges-file>`
   and transcribe its `N`/`sprint`/`wave` output verbatim (multi-sprint boundary assignment is hand
   judgment it doesn't resolve). Covers only DECLARED edges. Format + the dependency-order
   invariant it enforces: wiki.

   **`<edges-file>`** — one `A <- B` per line (A blocked_by B; prose form NOT accepted); no `<-` =
   isolated node; `@N` tags sprint N; `#` comments; unparseable line exits 2. E.g. `C1 <- C3`, `C4@2`.
2.1.6. **Fold to size — the baton is the parallel wave, not the idea.** Runs on 2.1.5's `wave`
   output; sets how many stubs 2.1 scaffolds. `loe:` is the whole-baton t-shirt read.
   - **Band: mostly M and L.** `roadmap.blitz_stage` folds XS/S only along a declared edge,
     dependent first, stopping at M. An edge-free XS/S is flagged `unfoldable-small`, and XL is
     flagged and never auto-split. An XXL stub means the roadmap is mis-made; go back to Phase 1.
   - **Same-wave stubs run in parallel** (`wave` is the dependency tier). Collapsing them into one
     baton is an EM call once scopes are known; same-file units never split.
   - **Split only on a real barrier** — a gate that cannot clear until the first half lands, or a
     decision the first half's output determines.
   - **Re-price on scope change**, or a stale size routes a go-do-it through a full lifecycle.

   Distinct ideas are sections, never batons; each keeps its cluster id in `covers:`.
2.2. Body, per stub, in order: title; why-its-own-session paragraph; `## What this covers`; `##
   Reference materials (read first)` (cite `OVERVIEW.md § <name>` + research-corpus, by name never
   number); `## Specification`; `## Acceptance criteria`; `## Recommended next steps for the
   picking-up EM` (3–7); `## Anti-scope`; `## Soft seams` (may be `- None identified`, must be
   present); `## Session Ledger` (empty until the first close appends a row; omitting it makes
   `handoff.append_session_ledger` unwritable on the baton); trailing `<!-- roadmap-baton: <run-id> <stub_id> by
   roadmap-planning -->`.
2.3. `STUB-INDEX.md` — a query callout, never a hand table (template + rationale: wiki).
2.4. Before any fan-out: run `audit-roadmap <run-id>`; then **what it cannot check** —
   confirm every wave-N stub set is file-disjoint per `scope:`. A same-wave pair that is not
   disjoint is a fold to make and re-number; a disjoint pair runs in parallel.

   **`scope:` names a SUBJECT, not a blast radius** — grep each item's symbols for its real touched
   set before splitting. Mark EM-fenced items (`archive/`, permission settings); never send a
   dispatched agent at the fast/full tier. `A-SCOPE-FIELD-NAMES-A-SUBJECT-NOT-A-BLAST-RADIUS`.
2.5. `pm-gates.md` — one row per stub whose `gate_notes`/`gate_dependency` carries a
   product-coupled signal (`PM `-prefix, named stakeholder, decision/approval/policy/scope/
   user-facing language). Template + detection rule: wiki. Origin: the stub's author prose; the EM reads it, no engine field exists.
2.6–2.7. Phase 2 close (Shape W, `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`):
   `& "$env:COORDINATOR_SETTINGS_HOME\bin\audit-roadmap.exe" <run-id>` — one gate, five audits (stub-coverage, `ready_to_fire`
   uniqueness, pm-gates cross-reference, dependency-order). Exit 1 blocks close and names the
   offender. `kind: roadmap-baton` frontmatter must be validator-clean; the engine requires `roadmap_id` to name
   a cluster that exists on disk. **No applicable cluster → the stub is not a `roadmap-baton`;
   scaffold it `kind: spinoff`** (never a null `roadmap_id` or a placeholder cluster).
2.8. Sequential reviews — same altitude rule and sidecar contract as Step 1.5.5. Domain reviewer
   skippable when its Step-1.5.5 findings are already pinned into the stub ACs verbatim AND each
   stub becomes a downstream `coordinator:plan` that re-applies the lens at PLAN altitude — record
   the skip rationale in the roadmap dir.
2.9. Retire each marked source plan, in order: migrate its uniquely load-bearing prose into the
   inheriting stubs, THEN stamp `status: superseded` + `superseded_by:
   state/roadmap/<run-id>/STUB-INDEX.md`, THEN stand down the owed review. **MUST NOT stamp before
   migrating** — stamping first strands the prose. Mechanics: `residue/source-plan-supersession.md`.

**The stub:cluster relation is MANY-TO-ONE.** One stub may name many KEEP clusters in `covers:`;
every cluster is named exactly once across all stubs — coverage and non-duplication, never a count
of stubs. Step 2.1.6 mandates the fold, so a `stub_count == keep_count` check fails a compliant
roadmap by construction; any gate must read `covers:`.

**Exit:** every KEEP cluster named in exactly one stub's `covers:`; every stub `loe:` M–XL;
frontmatter validator-clean, `## Soft seams` present; STUB-INDEX regenerates; resolutions doc
covers every conflict; `audit-roadmap <run-id>` exits 0; primary review integrated, domain
integrated or its skip recorded; Step 2.4's disjointness check done; every owed source plan retired
per Step 2.9 (migrated, stamped, review stood down).

---

## After Phase 2 — the stubs go live

Phase 2 close IS the deliverable; a fresh session picks each stub up via `/pickup`. This skill has
no execution phase and never invokes `coordinator:plan`.

**Owned downstream, never run here:** the readiness view (`roadmap-number-stubs --state <run-id>`);
`awaiting_gate → ready_to_fire` transitions, made by *another* session's `/handoff` or
`/workstream-complete` — **never auto-transition or pre-mark a sibling's stub ready**; and the
end-of-roadmap review. **Roadmap stubs are NEVER handed to `/mise-en-place` directly** (its Phase 0
gate rejects them). Full spec: wiki § Downstream mechanisms.

---

## Output artifacts

`inventory.md` · `clusters.md` · `reconciliation.md` · `COORDINATOR-RESOLUTIONS.md` (if any) ·
`research-corpus/<topic-slug>.md` × N · `OVERVIEW.md` · `peer-team-asks.md` · `STUB-INDEX.md` ·
`pm-gates.md` (all under `state/roadmap/<run-id>/`) · `state/handoffs/{YYYY-MM-DD}_{HHMMSS}_
roadmap-{stub_id}.md` × N, clustered by `roadmap_id:` alongside ad-hoc spinoffs.

## Contact points

`/handoff`, `/spinoff`, `/repo-setup`, `/workstream-start`, `/workstream-complete`,
`/workday-start`, boot-time archival sweep — read `residue/contact-points-checklist.md` before
touching any on behalf of a roadmap stub.

## Anti-scope

- Auto-derive `gate_notes:`/`gate_dependency:` from natural language. Author-supplied only.
- Cross-repo roadmap rollup (single-repo only).
- Auto-trigger gate-meaningfulness on `/pickup`.
- Render dashboards.
- **Replace `coordinator:plan` for single-plan work.** A picking-up EM keeps `deployment_state:
  in_flight`, writes `predecessor: none`, cites `roadmap_id/stub_id` in the plan-doc's "Why this
  plan" — never a `roadmap_parent:` field.
- **Leave a re-sliced live plan standing** — retire it at Phase 2 close (Step 2.9).

## See also

`commands/distill.md` · `coordinator:plan` · `coordinator:brainstorming` ·
`coordinator/skills/shape/SKILL.md` · `coordinator:goal-setting`
