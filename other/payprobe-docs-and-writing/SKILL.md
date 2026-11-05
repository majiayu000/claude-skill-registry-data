---
name: payprobe-docs-and-writing
description: >
  How to write and maintain PayProbe documentation. Load when: adding or updating
  any doc (guide, README, runbook), deciding WHERE a new document belongs
  (docs/ vs docs/history/ vs ADR vs PROGRESS vs ROADMAP), writing an ADR or a
  build/migration spec (docs/history/), adding a PROGRESS iteration entry, updating
  docs/history/project-review.md, fixing stale docs, or authoring/updating a skill in
  .claude/skills/. Keywords: Diátaxis, ADR template, spec template, PROGRESS
  entry, docs of record, house style, status labels, BUILT/planned/Proposed,
  docs-as-code, adapter table row, where does this doc go, skill provenance.
---

# PayProbe Docs and Writing

House manual for the documentation of record: what exists, what is trusted,
where new writing goes, and the templates real artifacts follow. All paths are
repo-root-relative. Facts date-stamped 2026-07-03 unless noted.

**When NOT to use this skill:**

- Outward-facing claims, licensing, positioning, "what may we say publicly" →
  `payprobe-external-positioning`.
- Whether a change needs an ADR/spec at all, gates and review discipline →
  `payprobe-change-control` (it owns the ADR-vs-spec-vs-nothing decision; this
  skill owns the templates and the writing itself).

---

## 1. The docs map

### Diátaxis structure (docs/README.md)

`docs/` follows the Diátaxis framework — four modes organized by reader intent,
not by code structure. The folders are **topic-named**, not mode-named (there is
no `docs/how-to/` directory); the mapping lives in the table in `docs/README.md`:

| Mode | Reader is… | Actual location |
|---|---|---|
| Tutorial | learning by doing, start to finish | `docs/getting-started/quick-start.md`, in-app Docs page |
| How-to guide | getting one job done | topic folders: `docs/adapters/` (writing-an-adapter.md, grpc.md), `docs/scenarios/` (code-step.md), `docs/simulators/` (payshield-10k.md, visa-scheme.md, payshield-hsm-reference.md), `docs/operations/load-test-runbook.md` |
| Reference | looking a fact up | `docs/operations/configuration.md` (every env var + default), `docs/operations/observability.md`; **live API reference is generated** — Scalar at `:8000/reference` and `:8100/reference`, fed by each service's OpenAPI spec. Never hand-write API endpoint reference; it would drift |
| Explanation | understanding why | `docs/architecture/` (overview.md, streaming.md) |

Historical working notes (`project-review.md`, `standards-gap-analysis.md`,
`reports-renovation.md`, the website-page prompts, and every finished build
spec) live in `docs/history/` — moved there from the repo root and loose
`docs/` on 2026-07-18 to keep the public landing view clean. Guides that
readers still need (e.g. `participant-flow-end-to-end-guide.md`) stay under
`docs/`. `docs/adr/` holds numbered ADRs (0001–0007 as of 2026-07-18).

Note: `docs/configuration/` and `docs/deployment/` directories exist but are
**empty** (verified 2026-07-03) — do not put new docs there; operations content
goes in `docs/operations/`.

### Build/migration specs (docs/history/) vs docs/

`docs/history/` holds **working documents for phased builds and migrations**
(at the repo root until 2026-07-18):
`*-SPEC.md`, `*-PLAN.md`, `*-SCOPE.md`, `docs/history/MIGRATION-DEPLOY-RUNBOOK.md`,
`docs/history/PLAN-end-to-end-mock.md`. These are execution artifacts — status-stamped as
phases land (e.g. `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md` opens with
"**Status: COMPLETE — Phases A–F all BUILT (2026-06-26/27).**"). `docs/` is for
readers; these specs are for the people/sessions executing a change. A spec
is *done* when its status line says so — it is then a historical record, not
deleted.

### docs/history/PROGRESS.md and ROADMAP.md

- `docs/history/PROGRESS.md` — the iteration log of the autonomous test-infra hardening
  campaign. Append-only iterations (newest first), each with measured
  before/after suite counts. It declares its own Definition of Done "MET (suite
  green, 195 passed / 0 failed)" and has not been extended since (last commit
  2026-06-19). It is the canonical example of the *measure, never assume* style
  ("Root cause (measured, not assumed): …"). New hardening campaigns should
  reuse its entry format (template in §3).
- `ROADMAP.md` — versioned feature checklists (v0.1 Foundation … ). It is a
  planning artifact, **not** a status of record: last commit 2026-06-20, and
  checkboxes lag reality in both directions (v0.2 adapter items unchecked though
  several were since built; v0.3 still says "ngx-graph canvas integration"
  though ngx-graph was later replaced by a custom SVG canvas). Trust code, specs
  and the project review over ROADMAP checkboxes.

### docs/history/project-review.md — the periodic honest assessment

A distinct genre: whole-codebase review "Generated 2026-06-20 against the
current tree", with dated **Status update — review N** sections appended as
follow-up passes land (reviews 3 and 4 are in the file). Structure: Snapshot
table (LoC + test posture per package) → What's strong → **Weaknesses, ranked**
(each with a severity tag, measured evidence — e.g. "77 `except Exception` and
~54 `except …: pass`" — and a concrete **Fix:**) → Quick wins with effort
estimates ("(hours)", "(minutes)") → New ideas / roadmap → Bottom line. It
criticizes the author's own code explicitly ("High — and it's my own code").
When you run a new review pass, append a `## Status update — review N (date)`
section with a delivered-items table rather than rewriting history.

---

## 2. Docs of record vs known-stale

**Docs of record** (trust these): README.md (positioning, adapter table,
license/disclaimer), `docs/operations/configuration.md`, `docs/adr/*`
(status lines are honest), the docs/history specs' status stamps, `docs/history/project-review.md`,
the generated Scalar API references, and `examples/` — examples are *executable
documentation*: every scenario in `examples/scenarios/` runs in `make test`
(`test_example_scenarios.py`) and fails the build if it errors, so they cannot
silently drift.

**Known-stale items** (verified 2026-07-03) — fix these when touching nearby
docs; do not propagate their claims:

| Item | What's wrong | Status |
|---|---|---|
| `docs/architecture/overview.md` | Last updated 2026-06-25. The project review's claim that it "predates the load-testing subsystem and gRPC" was **addressed** on that date (load fleet + gRPC are now in the diagram, verified by grep). But it is stale again: zero mentions of the chaos dial, resilience certification, Chronoscope replay, or stuck-run reconcile (all 2026-07 features). | **Open task**: refresh the overview after each major subsystem lands |
| `docs/history/project-review.md` §9 | Says report-service is a README stub with certification living in the orchestrator — written 2026-06-20; review 4 (2026-06-21) already records `report_service` as a real library with 15 tests. Re-verify before repeating either claim. | Superseded within the same file; read newest status update first |
| `docs/README.md` reference row | Links `scenarios/schema-reference.md`, which does not exist (`docs/scenarios/` contains only `code-step.md`). | Broken link — fix or create the file |
| `CONTRIBUTING.md` PR guidelines | Requires "`scripts/test-all.sh` must exit 0" — that script does not exist (`scripts/` holds only `run_example_scenarios.py`). The real gate is `make test`. | Stale reference; use `make test` |
| `docs/history/PROGRESS.md` counts | "195 passed" was true at campaign close (2026-06-19); review 4 counts 366 backend tests (2026-06-21), more since. | Historical record, not current count |
| `ROADMAP.md` checkboxes | Lag reality both ways (see §1). | Planning artifact only |

---

## 3. Templates (extracted from the real artifacts)

### ADR — from docs/adr/0001–0003

File: `docs/adr/NNNN-short-slug.md` (next free number). Sections marked
*(0003)* appear once a proposed ADR is implemented; *(0001)*/*(0002/0003)* show
which real ADR the section comes from — include what fits, keep the order.

```markdown
# ADR-NNNN: <imperative, specific title>

**Status:** Proposed            <!-- or: Accepted — implemented (see Implementation status) -->
**Date:** YYYY-MM-DD
**Deciders:** PayProbe maintainers (<names/roles>)

## Context
<What exists today, with file/symbol references. Why now.>

### What we can reuse            <!-- 0002/0003: list existing seams before inventing -->

### Forces
<Constraints pulling in different directions.>

## Decision
<One paragraph, present tense: what we will do.>

## Options Considered

### Option A — <name> (chosen)   <!-- mark the chosen one in its heading -->
**Pros:** …
**Cons:** …

### Option B — <name>
**Pros:** … **Cons:** …

### Option C — <name>
**Pros:** … **Cons:** …

## Trade-off Analysis            <!-- 0001: prose comparing options; name the decisive factor -->

## Consequences
**Easier** / **Harder** / **Revisit**        <!-- 0001 style -->
<!-- or -->
**Positive** / **Negative / risks**          <!-- 0002/0003 style -->

## Rollout / sequencing          <!-- 0002/0003: ordered, flag-gated steps -->
<!-- or -->
## Action Items                  <!-- 0001: numbered [ ] checklist naming concrete symbols -->

## Implementation status         <!-- 0003 only, added when Status flips to Accepted:
                                      what shipped, where, with test counts -->

## Open questions
## Notes                         <!-- out-of-scope + depends-on -->
```

House rules baked into the real ADRs: options name **concrete existing
machinery** (LoadBus, worker_provisioner, run_control), not abstractions;
consequences include a "Harder" / "risks" list — an ADR with no downsides is
under-analyzed; status is never marked ahead of reality (0001 and 0002 are
**Proposed, not built** as of 2026-07-03).

### Build spec — from docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md (and siblings)

File: `<TOPIC>-SPEC.md` (or `-PLAN.md` for pure migrations) under `docs/history/` (new specs start there too).

```markdown
# <Feature/model> — spec

**Status: <phase summary>.**   <!-- lifecycle examples from real specs:
     "Phase 1 in progress." (PARTICIPANT-FLOW-BUILD-SPEC)
     "Phase X1 BUILT + Phase X2 BUILT (date, caveat)." (CONNECTION-ADAPTER-EXTENSION-SCOPE)
     "COMPLETE — Phases A–F all BUILT (date)." (DEFAULT-CONNECTION-MODEL-SPEC)
     Update this line as each phase lands; date every flip. -->

## Principle
<One-paragraph design rule the whole spec serves.>

## Current state (grounded in code)
<What exists NOW, with file paths. Key findings from reading the code —
 this section is why the spec is trustworthy.>

## Target model
<The end state, concrete config/schema shapes.>

## Phases — each backward-compatible; the fallback is removed last
### Phase A — <name>
<Change, flag that gates it, tests that prove it, rollback step.>
### Phase B — …

## Backward compatibility
<What old data/config still works and how (guardrails).>

## Test matrix
<Table: case × expected behavior, old-model and new-model rows.>

## Risks / rollback
<Per-risk mitigation; the flag(s) that turn it all off.>

## Why this is worth it
```

The phase discipline is the *reversibility* non-negotiable in written form:
every phase flag-gated, rollback stated before defaulting ON. The companion
`docs/history/MIGRATION-DEPLOY-RUNBOOK.md` shows the operational half — see §4 dry-run rule.

### PROGRESS iteration entry — from docs/history/PROGRESS.md

Append under `## Iterations` (newest first):

```markdown
### Iteration N — <one-line outcome> (category <a|b|c>)
- **Did:** <exact change: files, symbols, mechanism. Root cause stated as
  measured, not assumed — quote the failing evidence.>
- **Added test:** `test_<name>` (<what it reproduces/proves>)
- **Result:** **<X> passed, <Y> failed** (was <X0>/<Y0>). No regressions.
- **Next:** <the measured gap you'll attack next, found while doing this one.>
```

Real entries never skip **Result** with suite numbers; "Added test" may become
"**Verified:**" when the change is a dependency fix proven by the existing
suite (Iteration 1 does this).

---

## 4. House style (inferred from the artifacts, verified)

1. **Honest status labels, everywhere.** Every ADR/spec/proposal opens with a
   status line: `Proposed`, `Accepted — implemented`, `Phase N in progress`,
   `BUILT (date)`, `COMPLETE`, `proposal / brainstorm`
   (docs/reports-renovation.md), `🟡 partial` (standards-gap-analysis.md).
   Unbuilt work is never described in the present tense as existing. If you
   flip a status, date it.
2. **Evidence-linked claims: counts + dates.** Numbers come from a command you
   ran, stated with when: "180→183 passed", "366 backend tests (+29 since
   review 3)", "77 `except Exception`". A claim without a count or a
   file/symbol reference reads as opinion in this codebase — anchor it.
3. **Dry-run-first in runbooks.** `docs/history/MIGRATION-DEPLOY-RUNBOOK.md` is the model:
   "the data steps are **dry-run by default**", and every mutating step is a
   *pair* — the plain command to review the plan, then the same command with
   `?apply=true`. New runbooks must follow this shape, plus a pre-flight
   section (`make test-scenario`, `make portal-build`, smoke-check curls) that
   even documents known pre-existing failures so the operator can tell signal
   from noise.
4. **Docs change with the code — where that rule actually lives.** It is NOT
   in CONTRIBUTING.md. The verbatim rule is in `docs/README.md` §"Contributing
   to the docs (docs-as-code)": *"Docs live in this repo and ship with the code
   they describe — change them in the same pull request, reviewed together."*
   What CONTRIBUTING.md itself requires for PRs: one PR per concern; all tests
   pass (it cites `scripts/test-all.sh`, which is stale — the real gate is
   `make test`); a description (what/why/how to test); reference related
   issues; no credentials or real hostnames. Commit style is Conventional
   Commits — use the `docs(...)` type for doc changes.
5. **New adapter ⇒ README table row (CONTRIBUTING Step 8).** Adding an adapter
   is an 8-step checklist ending with: add a row to the README.md adapters
   table (name, protocol, status `✅ Stable` or `🧪 Beta`). Steps 2 and 7 also
   create docs: a `README.md` inside the adapter package and at least one
   example scenario in `examples/scenarios/` — which `make test` then executes
   forever (executable documentation, §2).
6. **Link new guides from the docs/README.md table** and put them in the
   matching topic folder — a guide that isn't linked there doesn't exist for
   readers.

---

## 5. Where does a new doc go — decision table

| You are writing… | It goes… | Modeled on |
|---|---|---|
| First-run learning path | `docs/getting-started/` | quick-start.md |
| "How do I do X" task guide | topic folder: `docs/adapters/`, `docs/scenarios/`, `docs/simulators/`, `docs/operations/` | writing-an-adapter.md, load-test-runbook.md |
| Env var / config fact | extend `docs/operations/configuration.md` (don't fork a new file) | — |
| API endpoint reference | **don't write it** — the Scalar `/reference` pages generate from OpenAPI | docs/README.md §Interactive API reference |
| Why-it's-built-this-way | `docs/architecture/` | overview.md, streaming.md |
| A decision with rejected alternatives | `docs/adr/NNNN-slug.md`, template §3 | ADR-0001..0003 |
| Phased build/migration with flags + rollback | `docs/history/<TOPIC>-SPEC.md` / `-PLAN.md`, template §3 | docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md |
| Operational steps to deploy/migrate | `docs/history/` runbook, dry-run-first (§4.3) | docs/history/MIGRATION-DEPLOY-RUNBOOK.md |
| Iteration log of a fix/hardening campaign | `docs/history/PROGRESS.md` entry, template §3 | docs/history/PROGRESS.md |
| Feature planning / promises | `ROADMAP.md` checkbox (planning only, §1) | ROADMAP.md |
| Periodic honest assessment | append `## Status update — review N (date)` to `docs/history/project-review.md` | reviews 3–4 |
| Standards/conformance posture | `docs/standards-gap-analysis.md` | its 🟡/✅ per-standard format |
| Knowledge for future AI/junior sessions | `.claude/skills/<name>/SKILL.md` (§6) | this library |

Unsure whether the thing needs an ADR vs a spec vs nothing at all → that
gating decision belongs to `payprobe-change-control`.

---

## 6. Maintaining the skill library itself (meta)

Skills live in `.claude/skills/<name>/SKILL.md`; the binding shared rules are
in `.claude/skills/_AUTHORING-BRIEF.md` — read it before writing or editing any
skill. Non-negotiable mechanics:

- YAML frontmatter with `name:` and a trigger-rich `description:` (symptoms,
  tasks, keywords that should make a session load it). Optional `scripts/` dir
  for executable helpers.
- Imperative runbook voice; copy-pasteable, repo-root-relative commands; never
  embed session-specific or user-home absolute paths; define jargon at first
  use; state when NOT to use the skill and which sibling covers it.
- Ground truth only: every path/flag/count verified against the repo, else
  labeled `UNVERIFIED:` or omitted. No oversell — statuses in skills obey the
  same honesty rule as §4.1.
- Every skill ends with a **"Provenance and maintenance"** section: the
  verification date plus one-line read-only commands to re-check anything that
  can drift.

**To re-verify / update a skill** (do this when an ADR status flips, a spec
phase lands, files move, or suite counts change):

1. Run every command in its "Provenance and maintenance" section.
2. Where output diverges from the skill body, fix the body — never the other
   way around; the repo is ground truth.
3. Re-stamp the verification date; date any newly volatile fact.
4. Claims you can no longer verify: mark `UNVERIFIED:` or delete. Do not let a
   skill silently rot into fiction — a wrong runbook is worse than none.
5. Skills are repo files: they ship in the same PR as the change that
   invalidated them (same docs-as-code rule, §4.4).

---

## Provenance and maintenance

All facts verified 2026-07-03 against the working tree. Re-verify with:

- Diátaxis map + docs-as-code rule verbatim: `sed -n '1,55p' docs/README.md`
- Actual docs folders (incl. empty configuration/ and deployment/): `ls docs/ docs/getting-started docs/adapters docs/scenarios docs/architecture docs/operations docs/simulators docs/configuration docs/deployment`
- Broken schema-reference link: `grep -n "schema-reference" docs/README.md && ls docs/scenarios/`
- ADR statuses + section skeletons: `grep -n "^#\|^## \|^\*\*Status" docs/adr/000*.md`
- Root-spec status stamps: `grep -n "^\*\*Status\|^Status" *SPEC*.md *PLAN*.md docs/history/CONNECTION-ADAPTER-EXTENSION-SCOPE.md`
- PROGRESS entry shape + campaign close: `sed -n '1,70p' docs/history/PROGRESS.md` and `git log --date=short --format=%ad -1 -- docs/history/PROGRESS.md` (expect 2026-06-19)
- ROADMAP staleness: `git log --date=short --format=%ad -1 -- ROADMAP.md` (expect 2026-06-20) and `grep -n "ngx-graph" ROADMAP.md`
- Review genre + §9 claim: `grep -n "^## \|^### " docs/history/project-review.md` and `sed -n '112,118p' docs/history/project-review.md`
- Architecture overview freshness: `git log --date=short --format=%ad -1 -- docs/architecture/overview.md` (2026-06-25 at authoring); staleness check: `grep -ci "grpc" docs/architecture/overview.md` (>0) vs `grep -ci "chaos\|resilience\|chronoscope" docs/architecture/overview.md` (0 = still missing 2026-07 subsystems)
- CONTRIBUTING PR rules + stale script: `grep -n "test-all\|same pull request\|Conventional" CONTRIBUTING.md; ls scripts/`
- Adapter-table step: `sed -n '109,116p' CONTRIBUTING.md` and `grep -n "| Adapter | Protocol | Status |" README.md`
- Dry-run-first runbook: `grep -n "dry-run" docs/history/MIGRATION-DEPLOY-RUNBOOK.md`
- Skill-library rules: `sed -n '1,60p' .claude/skills/_AUTHORING-BRIEF.md`
