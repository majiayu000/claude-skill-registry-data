---
name: development-design
description: Architect-posture skill for ongoing work on an existing project. Takes change_spec.md (output of development-specs) as primary input, with docs/adr/, docs/fdr.md, docs/nfdr.md and the parts table of docs/SDD.md § 3 as architectural references. Names the part that owns each new piece of logic, determines blast radius, decomposes into isolated sub-jobs when multiple modules are affected, and produces change_design.md — a targeted change blueprint with sub-job boundaries, interface contracts, build sequence, and code strategy, whose header carries a Publishes text line (yes with the places, or no) that the chain reads to decide whether the content-editor step runs. No interview. The records are optional context — used when present, never required. Run when a change_spec.md is ready.
license: MIT
metadata:
  version: "2.16.2"
  category: architecture
  risk: safe
---

# Development Design

## Purpose

For ongoing work on an existing project: analyze a change request against the existing architecture, name the part that owns each new piece of logic, determine which modules are affected, decompose the work into isolated sub-jobs when needed, and produce a targeted change blueprint.

**Produces:** `change_design.md` — a delta document describing the change, not the full system.

**Decides one header line, `Publishes text:`.** Does this change put text in front of a person to read? `**Publishes text:** yes — <the places the words live>` when it does, `no` when it does not. The chain reads that line to run or pass the `content` step, where the Content Editor writes the words before the Developer places them (`<CORE>/doctrine/flow/development_flow.md` § The stages). A `Behaviour: preserving` change is always `no`, because it adds no words.

## When to Use

- The project already has `docs/adr/`
- The change is scoped — not a full rewrite or new app
- Examples: add a new status value, add a field to an entity, add a new operation, fix an architectural coupling issue, split an oversized module
- **Architect role only.** If invoked outside an architect session, stop immediately and say: "development-design is architect work. Switch to architect? (Open a new session with the `architect:` prefix.)" Stop — no one is there to confirm a switch, and with no change folder resolved there is nowhere to write a report; the chain halts on the missing `change_design.md`.

**Do not use for:**
- New apps or first-time project setup → the foundation step (`product-fdr`, then `product-architecture`)
- Changes that touch every module or require a full architectural rethink → the foundation step, which supersedes a record rather than editing one

## Enter the worktree

development-specs created an isolated worktree for this change and landed `change_spec.md` on the branch — it is **not** on `main`. Before reading anything, derive the worktree from the **change key** and operate inside it for the whole run.

The **change key** is `<YYYY-MM-DD>_<slug>` — the Tobiishi folder (`journey/tobiishi/<key>/`) / branch name. You know it from the invocation (the change you were asked to design). If multiple worktrees exist under `<repo>/.worktrees/` and the intended change is ambiguous, stop, naming the candidates in your closing message — there is no one to ask and no change folder to write into; the chain halts on the missing `change_design.md`.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE="$REPO_ROOT/.worktrees/<key>"
test -d "$WORKTREE" || echo "No worktree for <key> — development-specs must run first."
```

If `$WORKTREE` does not exist, **STOP**: the spec stage has not run for this change (development-specs creates the worktree and the spec together). Do not create it here and do not fall back to `main`. With no worktree there is no change folder to write a report into: stop, and the chain halts on the missing `change_design.md`.

**From here on, the worktree is the working root:** read every input from `$WORKTREE/` (`change_spec.md` and the decision files), write `change_design.md` under `$WORKTREE/`, and commit with `git -C "$WORKTREE"`. The change arc stays on the branch, never `main`. The path is derived from the key alone — identical convention to development-specs Step 4 and `ad-hoc-plan`; nothing is handed between sessions.

**Locate the project.** The orchestrator passes the **project name** `<project>` alongside the change key; the change-work folder is `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`. The project's decision files are **not** assumed to be at the worktree root — a repo may hold more than one project, each owning its own `docs/`.

**Resolve `PROJECT_DOCS`.** The step resolves the path itself, from the path tool's contract — never from any header in the change_spec (the `Project:` header is retired), and never by composing a product path by hand:

```bash
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "$WORKTREE" --project <project> --key <key>
```

A non-zero exit is a STOP, with the tool's `message`. From the contract's `product_path`, `product_repo` and `product_worktree`: `<sub>` is `product_path` when it is relative, else `product_path` relative to `product_repo` (`.` when the same), and `PROJECT_DOCS = <product_worktree>/<sub>/docs`. For an in-repo product `product_worktree` is `$WORKTREE`. For an external one it is the product worktree opened for this change — by `create_change_worktree.py`, on the chain path and under `ad-hoc-plan` alike — `<product_worktree>/docs` when `Product path:` *is* the repo root — and **never** the product's primary checkout.

**Every `docs/<file>` reference in the steps below resolves to `$PROJECT_DOCS/<file>`** (`adr/`, `fdr.md`, `nfdr.md`, `SDD.md`) — never the worktree-root `docs/` unless `Product path:` points there.

**Locate the product code — anchor, do not scan.** Blast-radius analysis reads the product's *source* (its `__init__.py` export surface, the affected modules). The source tree is **not** found by searching `$WORKTREE` for "a product folder" — derive it from `$PROJECT_DOCS`:

```bash
PROJECT_ROOT="$(dirname "$PROJECT_DOCS")"   # $WORKTREE/products/<product> (in-repo) or /abs/external-product (external)
```

`$PROJECT_ROOT` is the directory holding the product's `pyproject.toml` / package / tests. **Read all product code strictly under `$PROJECT_ROOT`.** A multi-project instance commits other projects' in-repo products as siblings inside the worktree; for an **external** product `$PROJECT_ROOT` lies *outside* the worktree, so any sibling found by scanning is the **wrong** product — the external-product split-brain. Anchor on `$PROJECT_ROOT`; never scan.

## Pre-flight

Read `$PROJECT_DOCS/adr/` (the decision log and its index), `$PROJECT_DOCS/nfdr.md`, and `$PROJECT_DOCS/fdr.md` if they exist — absence is not an error. These decision files are **optional context**: when present they are first-class inputs — honour the module set and forbidden imports of `nfdr.md § 1.2`, and lean on a record in `adr/` for the *why* behind them once its Status reads **Accepted** (a record still **Proposed** is context, not a binding decision). When `adr/` / `nfdr.md` are absent — a dogfood / FDR-less project with no `docs/` — do **not** halt: fall back to `change_spec.md`'s own module boundaries and the change request for blast-radius scoping. The records sharpen the design when they exist; their absence is never an error.

**Read the parts table, `$PROJECT_DOCS/SDD.md` § 3.** Its `Owns` and `Must not own` columns say which part owns a piece of logic, and `Lives in` says where that part's code is. `nfdr.md § 1.2` cannot answer this, because it is the import graph. Step 2 places every new piece of logic by this table (`<CORE>/doctrine/flow/development_flow.md` § *Code goes where the parts table puts it*, which defines *owning part* and *misplacement*). When the product has no § 3 parts table, the §2 Blast Radius says so, and Step 2 has no placement to make.

**Sweep the records for a gate they delegate to this stage.** An NFDR or ADR entry's `verified by:` tail may name a **review at `development-design`** rather than a check — a clause a command cannot decide, handed to this stage by name. Grep `$PROJECT_DOCS/nfdr.md` and `$PROJECT_DOCS/adr/` for entries naming this stage, and for each one the change touches: perform the review, and record it in `## Architect Review Notes` with its verdict. No later stage inherits it — a downgraded obligation delegated to a pipeline step is invisible to the step it was delegated to, so an unrecorded one is simply never done. The sweep is cheap and the absence is not: reading `nfdr.md § 1.2` alone finds the module set and misses every clause that named this seat.

## Workflow

### Step 1 — Read and understand

Read `change_spec.md` from the product owner's handoff (at `$WORKTREE/system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/change_spec.md`). Derive what the change requires from the existing architecture (module design, schema, operations, dependency graph) and the spec.

**Copy the classification — do not re-derive.** Copy `Category` and `Behaviour` from the `change_spec.md` header **verbatim**; development-design is a *propagator*, never a classifier (`change_classification.md` § *Constraints* — "every downstream artifact propagates them header-to-header"). `Behaviour` selects the drafting mode in Steps 2–7. If the header is missing or out-of-vocabulary (`Behaviour` outside `{preserving, changing}`), **halt** (§ *How this skill halts*) — do not default, do not re-classify; reclassification happens only via the evidence-driven surface-and-halt escape hatch (`change_classification.md` § *Constraints* — "STOP, surface, and reclassify"). See `<CORE>/doctrine/flow/change_classification.md` (`<CORE>` is resolved at session start by the hook).

**No question is asked** — this step runs in the chain, with no one to answer. Derive what the records and `change_spec.md` settle; where the spec is ambiguous or conflicts with itself or the tree, Step 7's reading rule decides, and halts only when no reading keeps every existing contract and delivers the request.

### Step 2 — Blast-radius analysis

For every module in `docs/nfdr.md § 1.2` (the module set), determine its status:

- **Unchanged** — not affected
- **Modified** — something inside changes; state what specifically (new field, new enum value, new method, modified signature, etc.)
- **New** — a new module must be added (rare in ongoing work)

**Before writing the blast-radius table, place every new piece of logic the change adds** — on a `changing` change; a preserving one adds none. For each piece, name its owning part from `docs/SDD.md` § 3 (`<CORE>/doctrine/flow/development_flow.md` § *Code goes where the parts table puts it* defines the term). The module holding that part's `Lives in` unit goes in the blast-radius table as `Modified`, or `New` where the unit does not exist yet, even when the code that first calls the logic sits elsewhere. Its *What changes* cell names the part and the logic. Two cases depart from this, and each is logged in `## Architect Review Notes` as kind (e), below:

- **No part owns the logic.** The note says where it goes, and why no part's `Owns` covers it.
- **The caller may not import the owning part under `docs/nfdr.md § 1.2`.** The design still places the logic in its owning part, and lists `docs/nfdr.md § 1.2` under `## Records this change makes false`, with the import it must allow.

Also check the forbidden-imports graph (`docs/nfdr.md § 1.2`): if a changed module's public interface changes, any module that imports from it may be transitively affected. Include those in the blast radius.

**`Behaviour: preserving` on a product with no code** (a card reading `Test command: none`): every preserving step below swaps modules, symbols and re-exports for documents, sections and invariants, by `<CORE>/doctrine/flow/change_classification.md` § *A product with no code*. Write it with `references/change_design_template.preserving_docs.md`, which settles the blast radius, the Layout Plan, §4 (`None — no code`) and §5 (`No suite`). In place of the five preserving cold-read checks, ask three. Is every invariant from the spec placed? Is any invariant stated twice? Does the design state anything the documents did not? A pointer that says only where a moved statement now stands is not that. A "yes" to the last is a **STOP** for reclassification, the same as check 4's changed signature; never resolve it by narrowing the words, and no `## Architect Review Notes` entry keeps the label.

**`Behaviour: preserving` (relocation / structural change):** the table still lists every affected module, but mark each `Modified (relocation only)` and put *file-location-only* in the *What changes* column. The forbidden-imports **transitive** check is moot — no public interface changes, so no importing module is affected. State that explicitly in the design: "No transitive blast radius — public surfaces unchanged." (Code only: on a product with no code, a document citing a moved statement's old place is in the blast radius.)

Write the blast-radius table:

```markdown
| Module | Status | What changes |
|---|---|---|
| `pkg/domain/` | Modified | Add `TaskStatus.CANCELLED` enum value |
| `pkg/persistence/` | Modified | Serialize / deserialize new status value |
| `pkg/cli/` | Modified | Accept `'cancel'` in `task update --status` |
| `pkg/application/` | Unchanged | — |
```

### Step 3 — Sub-job decomposition

**`Behaviour: preserving` — produce a Layout Plan, not interface-contract sub-jobs.** A preserving relocation exposes no new contract: each affected module keeps its public surface identical, so sub-jobs are independent and there is no build sequence to derive. Instead, for each affected module decide the layout the spec deferred:

- **Named module(s):** the file(s) the implementation moves into (e.g. `domain/project.py`, `domain/errors.py`).
- **Symbol → module mapping:** which classes / functions / module-level constants land in which named module. Account for *every* implementation symbol currently in the `__init__.py`, including underscore-prefixed helpers and constants.
- **`__init__.py` re-exports:** the exact public surface each `__init__.py` re-exports after the move — identical to today's importable symbols, nothing added or removed.
- **Where, not how.** The mapping states *where each symbol lives* — the table is `Symbol | Kind | Target module`, nothing more. Do **not** add an internal-imports column, stdlib-dependency annotations, or any per-symbol import wiring: imports travel with the moved code and are the developer's to write; emitting them leaks implementation into the structural plan and propagates downstream into the developer instruction. Cross-layer import stability is stated once in prose in §1/§2, never as a per-symbol column. If a split risks a **circular import**, flag it once as the hint on that module's §4 row — never as per-symbol wiring in §3.

This is where layout is decided — the thing development-specs deliberately left open. Read the actual code as **structure** (symbol inventory + current location) to plan the mapping; do not re-derive behaviour or re-open the spec's locked Invariants. Name the layout, **not** the move-task sequence — task ordering and red/green discipline are development-plan's job.

Skip the interface-contract / build-sequence machinery below (it applies only to `changing`); go to Step 4.

---

**`Behaviour: changing`:**

**If only 1 module is affected:** no sub-job split. Single delta — skip to Step 4. **Unless that module holds independent internal seams with a real ordering edge between them** — separate files, changed for separate reasons, where one must land before another. Then cut sub-jobs below module granularity and say in §3's preamble what the seams are and which edge forced the cut. A single delta that hides an ordering edge sends the developer a build order that does not work, and the failure reads as a bug in whichever part is built first.

**If 2+ modules are affected:** decompose into sub-jobs — one sub-job per affected module.

For each sub-job, define:
1. **Scope** — what this sub-job changes, nothing else
2. **Interface contract** — what it exposes to downstream sub-jobs (new types, new method signatures, modified schemas). This is what the other sub-jobs depend on.
3. **Dependencies** — which sub-jobs make something this one uses (a file, a module, an interface); an order preferred for risk or readability is not a dependency, and is stated as the build sequence's reason instead

Then determine build sequence from the interface contracts:
- Sub-jobs with no dependencies can start immediately (or in parallel with each other)
- Sub-jobs that need another's contract must wait
- State this as a sequenced list or parallel-track diagram
- **A no-green-point pair is an edge too.** Where two sub-jobs — or two seams inside one — have no state between them in which the suite is green, so neither has a landing point of its own, record an **atomic-landing edge** beside the ordering edges: `<A> + <B> — no green point between them: <why>`. An ordering edge says *A before B*; this one says *no point exists between A and B*. State it as the property it is and stop: do not say how the next stage should shape its tasks, and do not name that stage — how the work is cut is not this artifact's to decide (`<CORE>/doctrine/flow/folder_state_handoff.md` § *A constraint handed down is stated as a property*). The edge is what travels; the decomposition is derived from it.

**A sub-job never spans two modules.** That defeats the isolation the decomposition exists to create. It may sit *below* one, per the single-module case above — the rule bounds a sub-job from above, not from below.

### Step 4 — Code strategy

For each sub-job (or for the single delta if no split), assign a code strategy row:

| Sub-job / change | Hint |
|---|---|
| `domain/` — add CANCELLED | None |
| `persistence/` — serialize CANCELLED | None |
| `cli/` — accept `'cancel'` in `--status` | the `argparse choices` list is the seam the new value has to reach |

**Write a hint only where the approach is non-obvious** — a non-obvious algorithm, a library-specific pattern, format parsing, or a protocol constraint. Everywhere else the row reads `None`, and the developer infers the approach from the failing tests.

**The `Complexity` column that stood beside this one is retired — the owner's call, 2026-09-09.** A row carrying a hint and a row reading `None` already say what `Simple | Complex` said, and saying it twice let the two disagree: a sub-job could be marked `Simple` and carry a hint that `development-plan` was then forbidden to write into the task (its `#### Implement` rule allowed a Simple task no content but `Infer from failing tests.`). Two plans resolved that contradiction in two different directions and recorded neither. Do not reintroduce the column.

**A hint names the approach, never the code.** Allowed: algorithm shape, data layout, atomicity pattern, the key library call. Not allowed: production code, type annotations, working function definitions, complete logic. `<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Implement section rules* (the planning body `development-plan` follows) owns that fence, because it is the stage that carries the hint down to the developer and rewrites one that fails it. A hint a developer could paste is a finished production statement, and it takes the implementation reasoning this stage is fenced out of. One exception follows: a write into another repository.

Every sub-job has a row. `None` is a stated answer; a missing row is not.

**A write into another repository is written as its commands.** This applies where the change writes into a repository that is neither of the run's own: the instance worktree and the product worktree the path tool names. One case is copying a file into a host's `about/` and committing it there. The row's hint gives each command exactly as the run will type it, `<CORE>` written as `<CORE>`, one call each, in the path form that doctrine section sets. That includes the read-only status check before the copy, and the command that undoes the copy if the commit is refused. It names the allow rule each command is meant to match, read from wherever `<CORE>/tools/agent_run.py` says a launched run loads its allow rules, which is never the change worktree. Where no rule matches a command, the hint says so in a line beginning `No allow rule:`. The owner must add the rule before the write is attempted. Never ask for the write to be done in fewer calls, or bundled with a check. The harness matches a call by its literal text, so a combined call is refused however exact the rule (`<CORE>/doctrine/governance/commit_format.md` § *A write into another repository is plain commands, one call each*). These commands sit in the Hint column but are not a hint: the permission layer, not the developer, decides their shape, and `development-plan` carries them as given rather than as a `# Hint:` block.

**`Behaviour: preserving`:** one row per affected module. A pure relocation is mechanical — a move plus a re-export — so the row almost always reads `None`. There are no failing tests to infer from either way; the existing suite stays green throughout (TDD-under-green). A hint applies only where a move is non-obvious, for example a circular-import risk introduced by the re-export, and it is then the move mapping, never task ordering.

### Step 5 — Test additions

For each sub-job, state what tests must be added or modified. Do not re-propose the full test pyramid — only what changes:

**Name what the change stops proving, not only what it adds.** This section reads as additive, and a change that moves a signature or removes a constant retires assertions in tests that stay green — the clause quietly stops being proved and no reader meets its absence. For every assertion this change retires, name it with the row that re-proves its clause, or state that the clause itself is gone. An assertion dropped without either is coverage lost silently, which is the one loss a green suite cannot report.

| Sub-job | Test file | What to add / modify |
|---|---|---|
| `domain/` | `tests/test_domain.py` | New test: `test_task_status_includes_cancelled` |
| `persistence/` | `tests/test_persistence.py` | Extend round-trip test with CANCELLED status |
| `cli/` | `tests/test_cli.py` | New test: `task update --status cancel` accepted |

**Every Example in `change_spec.md` maps to at least one row here — and so does every rule-implied edge case.** Walk in two passes. (1) **Examples:** each Example maps to a test row; an Example with no row is a coverage gap, not an omission to defer. (2) **Rules:** then walk the spec's Rules — for every rule that admits an edge / empty / failure path (empty-state, error-then-read, boundary — e.g. "list after only failed creates → `No projects.`"), require either a §5 row **or** an explicit "covered by row X" note. A rule-implied edge the Examples table happens to omit must not fall through: the Examples table is the floor, not the universe.

**`Behaviour: preserving` — test *continuity*, not additions.** No tests for new behaviour — the change introduces none. The existing suite is the characterization contract and passes unchanged. Adding a *characterization* test that pins existing behaviour is encouraged **only** where a public surface the relocation touches is currently uncovered — it tightens the regression fence without changing behaviour. If the existing suite already covers the affected surface, state: "No test additions — the existing suite is the characterization contract." **Never** add a test for new behaviour.

### Step 6 — Write change_design.md

**`Behaviour: preserving`:** write to the same path — `$WORKTREE/system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/change_design.md` — using `references/change_design_template.preserving.md`, or `references/change_design_template.preserving_docs.md` on a product with no code. §3 becomes a **Layout Plan** (per-module named modules + symbol→module mapping + `__init__.py` re-exports), §5 becomes **Test Continuity**, then `## Records this change makes false` (always) and `## Architect Review Notes` (when anything diverged), and the header stamps `Category` + `Behaviour`. Skip the `changing` router below.

**`Behaviour: changing`:** write to `$WORKTREE/system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/change_design.md` using `references/change_design_template.md`. The template carries the metadata header (`Date` / `Category` / `Behaviour: changing`) and the five sections: §1 Change Summary, §2 Blast Radius, §3 Sub-jobs (omit if only 1 module is affected), §4 Code Strategy, §5 Test Additions — then `## Records this change makes false` (always) and `## Architect Review Notes` (when anything diverged). Stamp the header — copy `Category` + `Behaviour` from the change_spec verbatim (Step 1) — and fill each section from the analysis in Steps 2–5.

**Decide and stamp `Publishes text:` in both modes**, on the line right after `Behaviour:`. Read the spec and ask whether the change puts text in front of a person to read: a label, a message, a heading, prose. Write `yes — <the places the words live>`, naming each place as the person knows it and never as an identifier or file, or write `no`. A `Behaviour: preserving` change is always `no`. The first word is the verdict and must be exactly `yes` or `no`: `Yes` and `maybe` halt the walk at the `content` step. Do not leave the template's placeholder in place.

**Record every divergence from the spec — mandatory (`## Architect Review Notes`).** As you design, log in the template's `## Architect Review Notes` section every decision where the design departed from or went beyond `change_spec.md`, **each with its reason**: (a) **resolving a contradiction** between two stated contracts — never one with the `Behaviour` label, which the preserving STOP sends back (Step 7, preserving check 4), (b) **locking an observable behaviour the spec left implicit** — in particular *how* a stated contract is realized by construction (Step 7 check 5's realize-by-construction choice, e.g. an ordering realized via an explicit sort key), (c) **overriding an upstream recommendation**, (d) **departing from this skill's own stated shape** — the sub-module cut of Step 3 is the case that recurs, and a departure logged nowhere is one the next run of the same shape re-derives from scratch and files somewhere else, (e) **placing logic the parts table alone could not place** (Step 2) — no part owns it, or `docs/nfdr.md § 1.2` forbids the import its placement needs. A silent resolution turns a reviewable decision into an unexamined assumption. Omit the section only when the design adds no decision beyond the spec. This is the architect-stage analog of development-plan's `## TL Review Notes`.

**List every record this change makes false — mandatory, in both modes (`## Records this change makes false`).** Pre-flight reads `adr/`, `nfdr.md`, `fdr.md` and `SDD.md` § 3 more closely than any later stage, so this is where a sentence in them that goes false when the change lands is seen — a module the design adds that `nfdr.md § 1.2` does not list, a record's stated *why* the change contradicts. This skill never writes `docs/` (§ *Output*), so the sentence is listed, never edited: the record's path and section, what goes false, and what it should say once the change has landed. `development-plan` carries each entry into its *Owed outside this change's reach* line, and can carry only what this section names. The section is never omitted; `None — read <records>; nothing in them goes false` is its zero form.

### Step 7 — Cold-read pass

Re-read `change_design.md` as if you are a developer receiving it without prior context. Check:

1. **Blast radius complete?** Any module that imports from a changed module (per `docs/nfdr.md § 1.2`) and is not listed? Does every new piece of logic have its owning part named in §2, rather than sitting in the code that first calls it?
2. **Interface contracts sufficient?** Can a developer implement sub-job B without reading sub-job A's source — relying only on what §3 states it exposes?
3. **Build sequence consistent?** Does it match the import graph in docs/nfdr.md § 1.2?
4. **Test additions cover the changed paths and the rule-implied edges?** At minimum: one test per new behaviour introduced, one test per modified signature; **every Example in `change_spec.md` has a corresponding §5 test row**; **and every rule-implied edge / empty / failure path — not just the Examples table — has a §5 row or an explicit "covered by row X" note.** A dropped Example, or a rule-implied edge that appears in no row and no covered-by note, is a coverage gap.
5. **Stated contracts realized, not coincidental?** Where `change_spec.md` states an explicit contract (an ordering, a structure, a bound — e.g. "ascending by `id`"), does the design realize it *explicitly* rather than lean on an invariant that merely coincides with it today (e.g. stored insertion order)? A design that satisfies the spec by accident must be made to satisfy it by construction.
6. **Divergences recorded?** Does `## Architect Review Notes` log every decision that departed from or went beyond `change_spec.md` — each with its reason, especially the realize-by-construction choice from #5 and any resolved spec contradiction — never one with the `Behaviour` label, which preserving check 4 sends back? A divergence that landed silently is the failure mode. (Omit the section only if there were none.)
7. **Records that go false listed?** Does `## Records this change makes false` name every sentence in `adr/`, `nfdr.md`, `fdr.md` or `SDD.md` § 3 this change makes false — path and section, what goes false, the correction — or carry the zero form naming what was read? Checked in both modes; an absent section is the gap.
8. **`Publishes text:` present and settled?** Is the line right after `Behaviour:`, with a first word of exactly `yes` or `no`, and does a `yes` name its places? Does a `Behaviour: preserving` change read `no`? Checked in both modes; a missing line halts the walk at `content`.
9. **A write into another repository written as its commands?** Where the change writes outside the run's own repositories, does the §4 row give each command as one plain call, the status check and the undo included, naming the allow rule each matches or carrying a `No allow rule:` line? Does anything in the design ask for those calls to be combined? Checked in both modes.

**`Behaviour: preserving` cold-read checks (replace 1–4 above):**

1. **Every symbol accounted for?** Does the Layout Plan place *every* implementation symbol currently in each affected `__init__.py` (classes, functions, constants, underscore helpers) into a named module?
2. **Re-exports exact?** Does each `__init__.py` re-export *exactly* its current public surface — nothing added, nothing dropped?
3. **No collisions?** Do the proposed module names avoid clashing with existing files in that layer?
4. **Negative assertion.** Does the design introduce **no** new behaviour and **no** change to the public import surface? If any layout choice would change an importable symbol or its signature, **STOP** — the change is not preserving; halt for reclassification (§ *How this skill halts*, reason `behaviour-delta-detected`, mirroring `development-specs`). Never resolve it by narrowing this rule's words — the label is the PM's, and the STOP is how it goes back. **No `## Architect Review Notes` entry keeps a label this contradicts:** a design that stays `preserving` over a changed signature has answered the PM's question for it.
5. **No import wiring in §3?** Is the §3 mapping strictly `Symbol | Kind | Target module` — carrying **no** internal-imports column, stdlib-dependency annotations, or per-symbol import lines, and no prose naming the intra-package import chain? Import wiring is the developer's to write; if §3 (or its prose) emits any, strip it — flag a circular-import risk, if real, as the hint on a single §4 row instead.

Fix any self-resolvable gaps directly. **A spec that conflicts with itself or with the tree is settled by the architect, never put to a person** — this skill runs in the chain, where no one is there to answer. The rule holds wherever the conflict is met, in any step; met here, rework §2–§5 to the reading taken and walk this cold-read again.

- **What counts.** An *existing contract* — distinct from a contract the spec states, which check 5 realizes — is a test in the suite the spec does not name as changing, or the product's present behaviour outside what the request asks. A record — an FDR, NFDR or ADR line — is not one here: a record the design leaves unmet is listed under `## Records this change makes false` if the change makes it false, and otherwise handed on in `deferred_decisions.md`. *The request* is `change_request.md` in the change folder, read for this check.
- **The reading rule.** A reading only sets spec lines aside; it adds no behaviour that neither the spec nor the request states — adding one would define product scope, which is not the architect's (`<CORE>/roles/CROSS_ROLE.md` § Decision authority). Where a reading keeps every existing contract and still delivers what the request asks, take it; where several do, take the one that sets aside the least of the spec. Design to it, log the choice and every reading not taken under `## Architect Review Notes`, and add one *reading set aside* entry to `deferred_decisions.md` in the change folder — created from `<CORE>/../skills/product-owner/.claude/skills/development-specs/references/deferred_decisions_template.md` when absent — so `shukuba-refine` places the lines not carried after the unit lands.
- **Never the `Behaviour` label.** A conflict between the design and the `preserving` label is preserving check 4's STOP, not this rule.
- **A spec silent on a decision** — it states nothing on it — is no conflict: lock the conservative reading and log it under `## Architect Review Notes`, as check 6 asks. A spec whose lines admit two readings is ambiguous, and the reading rule above decides it.
- **Halt only when no reading works** — every reading breaks an existing contract the spec does not release in a Rule, or drops something the request asks for. Halt per § *How this skill halts*, the report numbering each conflict and the decision that settles it.

Signal: **"change_design: clean."** On a halt, signal **"change_design: halted — halt_report.md"** instead.

### Step 8 — Commit outputs

Commit `change_design.md` on the change branch through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = `$WORKTREE`, `<staged file(s)>` = `change_design.md` (+ `deferred_decisions.md` when Step 7 wrote to it), plus subject / body / **`--actor architect`** (the agent `launcher.md` launches this skill as — name it, never derive it) / `--skill development-design` (this skill's own name, so `Skill-Version:` records what ran) / directional. Never hand-write `git commit` or a trailer. This skill does not advance the pipeline inboxes — that baton-pass is handled separately.

The skill is done.

### How this skill halts

Every halt and STOP in this skill that happens once `$WORKTREE` exists ends the same way (the stops before it — the posture gate, an unresolvable change key, a missing worktree — only stop, as each says). Write `halt_report.md` in the change folder (`$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`), in the sections of `<CORE>/../skills/product-owner/.claude/skills/development-specs/references/halt_report_template.md`, titled `Halt Report — development-design`, its **Request** field naming the change folder's `change_request.md`. Its Halt Reason is one of this skill's own: `invalid-behaviour-classification` (Step 1), `path-unresolved` (the path tool's STOP), `behaviour-delta-detected` (a preserving change that is not — preserving check 4, or the no-code preserving STOP), or `spec-conflict` (Step 7, no reading works). The report cites the lines that conflict and numbers each decision that would settle them. **Leave no `change_design.md` in the change folder** — delete a draft Step 6 wrote — because the chain reads that file's presence as the step's success and would walk past the report to plan. Revert any `deferred_decisions.md` entry this run wrote, since it describes a design that will not land. Commit through the builder as Step 8 does, staging `halt_report.md` alone (and the draft's deletion, if it had been committed), and signal **"change_design: halted — halt_report.md"**.

---

## Output

| File | Produced by |
|---|---|
| `change_design.md` | This skill, with its `Publishes text:` header line |
| `deferred_decisions.md` | Written to (created when absent) when Step 7 takes one reading of a conflicting spec |
| `halt_report.md` | On any halt (§ *How this skill halts*), with no `change_design.md` beside it — including when Step 7 finds no reading that keeps every existing contract and delivers the request |

`docs/adr/`, `docs/fdr.md`, `docs/nfdr.md` and `docs/SDD.md` are **not updated** by this skill. They document the project's foundation. `change_design.md` documents the delta, and names in § *Records this change makes false* every sentence in them the delta makes false. When development-plan is invoked for this change, the tech lead reads both the records and `change_design.md`.

---

## Critical Rules

- **Worktree-first.** development-specs created the worktree `<repo>/.worktrees/<key>` and committed `change_spec.md` on the branch — it is **not** on `main`. Derive `$WORKTREE` from the change key before reading anything; read all inputs from `$WORKTREE/`, write `change_design.md` under `$WORKTREE/`, and commit with `git -C "$WORKTREE"`. If the worktree doesn't exist, STOP — development-specs must run first; never create it here and never fall back to `main`. The path is derived from the key alone — no handoff payload.
- **Project root from `project.md`, not a header.** A repo may hold multiple projects, each with its own `docs/`. Resolve `PROJECT_DOCS` (absolute) from `project.md` `Product path:`: relative → `$WORKTREE/<Product path>/docs`; absolute → the product worktree opened for this change, by `create_change_worktree.py`, on the chain path and under `ad-hoc-plan` alike (never the primary checkout). Assuming `$WORKTREE/docs/` halts on a multi-project repo where the project lives in a subfolder (e.g. `<product>/docs/`). **Product *code* roots the same way — `PROJECT_ROOT=$(dirname "$PROJECT_DOCS")`; read all product source strictly under it, never by scanning `$WORKTREE` for a product folder.** A sibling in-repo product would be the wrong one — the external-product split-brain.
- **No interview.** The architect reads the records and derives everything from them and the change request. A conflict in the spec is settled by Step 7's reading rule — take the reading that keeps every existing contract and delivers the request, adding nothing, log it, hand the rest on in `deferred_decisions.md` — and halts only when no reading does, per § *How this skill halts*.
- **Blast radius must be complete.** Check the forbidden-imports graph (`docs/nfdr.md § 1.2`) for transitive impact. A module that imports from a changed module and whose call sites are affected must appear in §2.
- **New logic is placed by the parts table.** Step 2 names the owning part of every new piece of logic from `docs/SDD.md` § 3 and puts that part's code in §2. Reading the import graph does not settle placement.
- **Interface contracts before build sequence.** You cannot determine what is parallel and what is sequential without knowing what each sub-job exposes. Write the contracts first.
- **A sub-job never spans two modules.** A sub-job spanning two blurs the isolation the decomposition exists to create. It may sit below one where a single module holds independent seams with an ordering edge between them (Step 3) — the rule is a ceiling, not a floor.
- **Code strategy is mandatory.** Every sub-job has a §4 row. A row states a hint or states `None` — both are answers, and an omitted row is neither. Write a hint only where the approach is non-obvious, and keep it to the approach: `<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Implement section rules* (the planning body `development-plan` follows) owns the fence between a hint and a production statement. There is no `Complexity` column (retired 2026-09-09, the owner's call — Step 4 states why).
- **A write into another repository is written as its commands.** Where the change writes outside the instance and product worktrees, its §4 row gives each command as one plain call, the status check and the undo included, and names the allow rule each matches or carries a `No allow rule:` line (Step 4). Never ask for those calls to be combined, because a combined call matches no rule.
- **Decide and stamp `Publishes text:`.** Every `change_design.md` carries the line right after `Behaviour:`, `yes — <places>` or `no`, decided from the spec by whether the change puts text in front of a person to read. A `Behaviour: preserving` change is `no`. The chain reads its first word, which must be exactly `yes` or `no`, and a missing or other value halts the walk at `content`. Step 7 checks it.
- **Cold-read before signalling clean.** Step 7 is not optional. Signal "change_design: clean" only after every Step 7 check this mode walks holds.
- **Every spec Example — and every rule-implied edge — is covered.** §5 maps every Example in `change_spec.md` to at least one test row, and every rule-implied edge / empty / failure path to a row or an explicit "covered by row X" note. A dropped Example, or an uncovered rule-implied edge, is a coverage gap, not a deferral. The Examples table is the coverage floor, not the universe.
- **Realize stated spec contracts explicitly.** When `change_spec.md` states an explicit contract — an ordering, a structure, a bound — the design realizes it *by construction*, never by relying on an invariant that only coincides with it today. Satisfying a stated contract by accident (e.g. spec "ascending by `id`" met only by the design's incidental stored order) is a latent break; make the design satisfy it on purpose.
- **Record every divergence in `## Architect Review Notes`.** Every design decision that departed from or went beyond `change_spec.md` — resolving a spec contradiction (never one with the `Behaviour` label — the preserving STOP sends that back), locking *how* a stated contract is realized by construction, overriding an upstream recommendation, departing from this skill's own stated shape, or placing logic the parts table alone could not place — is logged with its reason (the architect-stage analog of development-plan's `## TL Review Notes`). A silent resolution turns a reviewable decision into an unexamined assumption. Omit the section only when the design adds no such decision.
- **Name every record this change makes false.** `## Records this change makes false` is written on every run, in both modes — each entry the record's path and section, what goes false, and the correction; the zero form names what was read. The record is never edited here; `development-plan` carries each entry into its *Owed outside this change's reach* line.
- **Two-axis classification.** Every change carries `Category` + `Behaviour` (see `<CORE>/doctrine/flow/change_classification.md`). `Behaviour: preserving` switches Steps 2–7 to structural-relocation mode: blast radius is relocation-only (no transitive impact; on a product with no code, the documents citing a moved statement's old place), §3 is a **Layout Plan** (not interface-contract sub-jobs), §5 is test-continuity, the cold-read asserts the negative. Do not fork the skill per axis — the axis selects the step bodies.
- **development-design owns the layout; nothing more.** On a preserving change, development-design decides the named modules and symbol partitioning the spec deferred — but it does **not** re-open the spec's locked Invariants (up-fence) and does **not** shape TDD move-tasks or red/green sequencing (down-fence — development-plan's job). Layout is *what-goes-where*, not *how-to-sequence-the-moves* and not *how-modules-import* — the symbol→module table carries no import wiring, stdlib annotations, or per-symbol dependency lines; that implementation travels with the moved code and is the developer's to write.
- **Read the code as structure, not behaviour.** A preserving change *requires* reading the implementation to inventory symbols for the layout — that is correct here, and differs from `development-specs`, which reads bodies only to *verify* a claim and never *sources* an invariant from one (at PO altitude, sourcing from code leaks mechanism into invariants). development-design reads the code to map current symbol locations onto target modules — never to re-derive behaviour or second-guess the locked Invariants.
