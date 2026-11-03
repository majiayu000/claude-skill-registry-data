---
name: development-implementation
description: Developer-posture skill for ongoing work. Executes a development-plan `tl_instruction.md` in a fresh execution session — per-task TDD (red/green/refactor), developer standards, verification gates, and a self-owned closing commit, made again over an earlier one when a relaunched run re-closes the change — or, when the chain's context cap is passed, a pause commit after the task in progress so a fresh run continues at the next task. Repairs incomplete implementation and tests against the resolved contract, including inherited work, until verification passes. Writes new logic in the part that owns it in the product's parts table (docs/SDD.md § 3). External impediments are handled by the deferral contract; the run halts in three cases only. Reads execution type + test command from project.md. Does not advance pipeline inboxes — that baton-pass is handled separately.
license: MIT
metadata:
  version: "5.11.1"
  category: execution
  risk: safe
---

# Development Implementation

## Purpose

Execute a `tl_instruction.md` produced by `development-plan` — implement each task from failing tests, in controlled per-task TDD cycles, with verification and a self-owned closing commit, or a pause commit when a chain's context cap is passed.

The instruction is a **pure scaffold**: module responsibilities, behaviours to verify, and hints for complex tasks. It carries no commit choreography and no execution metadata. This skill owns the commit structure (per-task TDD commits, then the closing commit, or a pause commit when a chain's context cap is passed) and sources execution context from `system/projects/<project>/project.md`. A run that pauses finishes the task it is on and stops there. The chain starts a fresh run at the next task, and that run's launch prompt says where to start (Step 2).

**Own the finished result, including the work you inherit.** Step 2 § *Work and repair* governs implementation, verification and correction. § *Deferring a task* governs external impediments; § *When to Stop* governs run-level halts.

The developer's job is **not to transcribe the instruction into code** — it is to critically review what they received and produce a better-implemented result than the scaffold alone prescribes. The developer is the last quality gate before the code lands, exactly as the Tech Lead is the last quality gate before the developer. Improvements are made, and every improvement is logged — same discipline `development-plan` applies to the architect's design.

**Announce at start:** "I'm using the development-implementation skill to execute the `tl_instruction.md`."

## When to Use

- Stage 5 (Developer) of the iteration pipeline — after `development-plan` has produced and committed `tl_instruction.md`, and, when the design's `Publishes text:` line reads `yes`, after `development-content` has committed `change_text.md`.
- Auto-invoked in any execution session running a `tl_instruction.md`, whether headless or Docker sandbox.

## Enter the worktree

The upstream stages ran inside an isolated worktree for this change — development-specs created it and landed `change_spec.md` on the branch, development-design and development-plan added `change_design.md` and `tl_instruction.md` there. None of it is on `main`. This is the **only** stage that writes code, so landing on the wrong branch silently breaks the worktree isolation every upstream stage preserved — entering correctly is not optional.

- **Headless runs (host terminal):** derive the worktree from the **change key** and `cd` into it before reading anything; operate inside it for the whole run.
- **Docker sandbox runs:** the launcher mounts the checked-out branch at `/workdir` — skip this derivation; `$WORKTREE` is `/workdir` and the Docker startup gate (Step 1) verifies it.

The **change key** is `<YYYY-MM-DD>_<slug>` — the Tobiishi folder (`journey/tobiishi/<key>/`) / branch name. You know it from the invocation (the change you were asked to execute). If multiple worktrees exist under `<repo>/.worktrees/` and the intended change is ambiguous, ask which one — once.

```bash
# Run this FIRST, from the instance root, before any `cd` — it answers from the CWD.
REPO_ROOT=$(git rev-parse --show-toplevel)        # the INSTANCE repo
WORKTREE="$REPO_ROOT/.worktrees/<key>"
test -d "$WORKTREE" || echo "No worktree for <key> — the upstream stages must run first."
cd "$WORKTREE"
```

If `$WORKTREE` does not exist, **halt** (§ *When to Stop*, first case — no task could land): the upstream stages have not run for this change. Do not create it here and do not fall back to `main`.

**Write `$WORKTREE`'s value down — the absolute path, in your own prose — before you `cd` anywhere.** Two things make the variable alone unsafe. A shell variable does not survive from one command to the next: each command runs in a fresh shell, so `$WORKTREE` in a later command expands to the empty string and `git -C ""` silently means *here*. And for an **external product** this run spends most of itself inside the *product* worktree, which carries a `.worktrees/<key>` of its own on a branch of the same name — so re-deriving from `git rev-parse --show-toplevel` after that `cd` answers with the product worktree and nothing looks wrong. Every `$WORKTREE` below means the instance path you wrote down at entry.

**From here on, `$WORKTREE` is the working root (the CWD):** read every input from `$WORKTREE/` (`tl_instruction.md`, `change_design.md` under `system/projects/<project>/journey/tobiishi/<key>/`), write all code under `$WORKTREE/`, and commit from inside it. The change arc stays on the branch, never `main`. The path is derived from the key alone — identical convention to development-specs Step 4, development-design, development-plan, and `ad-hoc-plan`; nothing is handed between sessions.

**Locate the project.** The orchestrator passes the **project name** `<project>` alongside the change key; the change-work folder (pipeline-side) is `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`. The product root is separate (`<name>` below — it may differ from `<project>` and may even be external). The project's code and decision files are **not** assumed to be at the worktree root — a repo may hold more than one project, each owning its own `docs/` and source tree.

**Resolve `PROJECT_DOCS`**, then derive the project root from it. The step resolves it itself, every
run, from the path tool's contract — the one call § *Where each commit goes* makes at entry — and never
composes a product path by hand:

```bash
# From the contract's product_path, product_repo and product_worktree:
#   <sub>        = product_path when it is relative, else product_path relative to product_repo ('.' when the same)
#   PROJECT_DOCS = "<product_worktree>/<sub>/docs"
#     in-repo:  product_worktree is $WORKTREE, so PROJECT_DOCS="$WORKTREE/<sub>/docs"
#     external: product_worktree is the product worktree create_change_worktree.py opened for this change;
#               never the product's primary checkout
PROJECT_ROOT="$(dirname "$PROJECT_DOCS")"                     # e.g. $WORKTREE/<product> or $WORKTREE
```

Do **not** re-derive `PROJECT_DOCS` from any header in the change_spec (the `Project:` header is retired). `<name>` (used throughout below as the project root) is the path from the worktree root to `$PROJECT_ROOT` — `<product>` for the multi-project playground, `.` for a single-project repo. **All code and tests live under `$PROJECT_ROOT/` (the test command is the one exception, § *Execution context* below); every `<name>/docs/<file>` reference resolves to `$PROJECT_DOCS/<file>`** — never the worktree-root `docs/` unless `PROJECT_DOCS` points there.

## Roots and paths

This skill operates across **two roots**, both resolved in **Enter the worktree** above — the same separation `project-*` skills use, rebased onto the change worktree (the same `PROJECT_DOCS` resolution development-design and development-plan use):

| Root | Holds | Where it is |
|---|---|---|
| **pipeline-root** = `$WORKTREE` (the CWD) | `system/projects/<project>/journey/tobiishi/` | `<repo>/.worktrees/<key>` (headless) or `/workdir` (Docker mount) |
| **project-root** = `<name>` = `$PROJECT_ROOT` | `docs/adr/`, code, tests | `$(dirname "$PROJECT_DOCS")` — `$WORKTREE/<product>` (multi-project) or `$WORKTREE` (single-project) |

Every project-side path is qualified with `<name>/`; every pipeline-side path is bare from the CWD (which is `$WORKTREE`).

- **Project-side** (qualified with `<name>/`): `<name>/docs/adr/`, code, tests. Read `docs/adr/` and write all code here. The test command is the one exception: it runs from the root of the product's change worktree, not from `<name>/` — `$WORKTREE` for an in-repo product, the product worktree for an external one (§ *Execution context*).
- **Pipeline-side** (bare from the CWD = `$WORKTREE`): `system/projects/<project>/journey/tobiishi/<key>/{tl_instruction,change_design}.md`.

If `PROJECT_DOCS` is unresolved (the `project.md` resolution above yields nothing) and `<name>` cannot be derived from the instruction's `## Project layout` top directory, **halt** (§ *When to Stop*, first case), and in an interactive session ask for the project root — do not guess.

## Where each commit goes

A change's product is either **in-repo** (code inside `$WORKTREE`) or **external** (code in its own git
repo). Which it is, and which repo takes which commit, is not read by hand — ask the path tool once, at
entry, after writing `$WORKTREE` down:

```bash
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "$WORKTREE" --project <project> --key <key>
```

It reads `Product path:` from `project.md` (the single source) and returns, among the rest,
`code_worktree` and `pipeline_worktree`, and the `product_path`, `product_repo` and `product_worktree`
that `PROJECT_DOCS` above is built from. A non-zero exit is a halt (§ *When to Stop*), with the tool's
`message` in the report.

- **Code commits → `code_worktree`.** It is the worktree `$PROJECT_ROOT` sits in. For an external
  product that is the **product** worktree (the contract's `product_worktree`, where `PROJECT_DOCS` above
  sits): `cd` there for the per-task TDD cycles so
  `test-driven-development`'s commits land on the **product** branch.
- **Pipeline commits → `pipeline_worktree`** — the instance worktree, `$WORKTREE`. The closing commit is
  one: its `--repo` is the instance worktree you wrote down at entry, and for an external product it is
  **not** the `--repo` every per-task commit of this run carried.

For an in-repo product the two are one path — a single repo, CWD stays `$WORKTREE`, nothing differs.
For an external product they are two repos, and that is the whole difference. A write into a third repository is neither kind of commit: Step 2 § *A write into another repository*.

## Inputs

All inputs are **read-only**. Read the instruction, design and specification together; implement the change from their combined contract and record corrections to the instruction in Developer Review Notes.

| File | Root | Role | How it is used |
|---|---|---|---|
| `system/projects/<project>/journey/tobiishi/<key>/tl_instruction.md` | pipeline | **execution plan** | task sequence, scaffold, test cases and verification gates |
| `system/projects/<project>/journey/tobiishi/<key>/change_design.md` | pipeline | **technical contract** | implement the interfaces, topology and technical decisions; recover details the instruction omits |
| `system/projects/<project>/journey/tobiishi/<key>/change_spec.md` | pipeline | **behavioural contract** | implement the scope, business rules and acceptance criteria; recover details the instruction omits |
| `system/projects/<project>/journey/tobiishi/<key>/change_text.md` | pipeline | **the published words** | present only when the design's `Publishes text:` line read `yes` and the Content Editor ran. Every published string this run places comes verbatim from it; read it with the rest of Step 1's inputs |
| `<name>/docs/adr/` | project | **the decision log** | consulted on demand for the *why* behind a topology or import boundary, read headline-first through its index. An **Accepted** record is binding; one still **Proposed** is context |
| `<name>/docs/nfdr.md` | project | **the constraint set** | § 1.2 for the module set and the import graph, on demand |
| `<name>/docs/SDD.md` § 3 | project | **the parts table** | for every task that adds logic: `Owns` and `Must not own` say which part owns it, and `Lives in` where that part's code is (Step 1b). A product with none says so in the `Step 1b review:` block |
| Language packets, resolved per `<CORE>/doctrine/engineering/languages/README.md` | project | **required** | resolved every run and the result recorded, whatever it is — every concern the packet's router lists accounted for, and every clause the implementation turns on quoted verbatim with its line, never summarised (Step 1 sub-step 3). A packet that exists is read for the run's language practice and binds over the surrounding file's own style; no packet for the resolved language means proceed on `<CORE>/doctrine/engineering/languages/developer_standards.md` — still recorded, still never a STOP |

Follow cited product-document sources when needed to resolve a detail or constraint; a prior upstream review does not replace the developer's judgment. Step 1b owns how omissions and disagreements are resolved.

**A correction owed outside this change's reach is not this skill's to discharge.** A line under `tl_instruction.md`'s `## Corrections owed while there` in the shape *Owed outside this change's reach* names a record this change may not edit — a product record under `docs/`, a file the instance keeps unedited such as `about/`, an untracked file, or a file in another repository. Leave that record as it stands, and do not count the line as undone work. **A line in that shape naming a file tracked on this branch is mislabelled, and the label does not bind you.** The file is in reach, so its correction is a defect found while walking (`<CORE>/doctrine/governance/found_while_walking.md` clause 1): make it on the branch, and log the re-shape in `Developer Review Notes` as a divergence. A station guardrail that holds such a file byte-identical does not bar it either — the guardrail holds scope, and a sentence this change makes false is not scope. The other two correction shapes name files this change opens.

### Execution context

From `system/projects/<project>/project.md` — the card is the execution context's owner — extract:

| What to extract | Source |
|---|---|
| Execution type (`headless` \| `Docker sandbox`) | `system/projects/<project>/project.md` `Execution type:` |
| Test command (run from the product's change worktree root — `$WORKTREE` in-repo, the product worktree for an external product — never from `<name>/`; the seal runs it there too, `tobiishi-seal` Step 1a) | `system/projects/<project>/project.md` `Test command:` |

Execution type and the test command come from `system/projects/<project>/project.md` — never from `tl_instruction.md`, which no longer carries them, and never from the decision log, which does not hold them.

Execution context always resolves from `system/projects/<project>/project.md`, so a project with no `docs/` at all is unaffected. Halt only if the card carries no execution context:

> "Execution context unresolvable — `system/projects/<project>/project.md` provides no Execution type + Test command."

The working root is resolved in **Enter the worktree** above: for **headless** runs this skill derives `$WORKTREE` from the change key and `cd`s into the worktree development-specs already created; for **Docker** runs the launcher mounts the checked-out branch at `/workdir`. This skill never *creates* worktrees, symlinks venvs, or mounts repos — headless enters an existing worktree, Docker uses the existing mount. The startup gates (Step 1) confirm the working root is the change branch before any code is written.

---

## Workflow

1. Enter the worktree (headless: derive `$WORKTREE` + `cd`; Docker: confirm the `/workdir` mount), then run the startup gates for the execution type (verify branch + toplevel); load + read `tl_instruction.md`
2. Per task: red commit → green commit → optional refactor commit — or, for a no-test structural task, a review-verified task, an already-green task, a red-at-baseline task or a `Behaviour: preserving` relocation, one plain commit (developer commits as it goes)
3. Close — the self-owned closing commit, which carries a `Deferred:` line for every task deferred along the way, and is made again when the branch already carries one (Step 3 § *A re-close makes a new marker*). Or, when the context cap's notice arrives, finish the task in progress, make the pause commit, and end (Step 2 § *Pausing at the context cap*). Or, in the three halt cases only, a `halt_report.md` and no marker (§ *When to Stop*)

### Step 1 — Load and review the change

1. **Enter the worktree, then run the startup gates for the execution type** (below) before anything else — headless derives `$WORKTREE` from the change key and `cd`s in (per **Enter the worktree**) then verifies the entry landed; Docker confirms the `/workdir` mount. Both end on the change branch, in the worktree, never the primary checkout / `main`.
2. Read `tl_instruction.md`, `change_design.md` and `change_spec.md` in full. If the change already has a `code-integrity-report.md`, read its findings against the current code and tests as part of this review; apply § *Work and repair* to unfinished work it identifies.
3. **Resolve the language packet — every run, no exceptions.** This skill's chain has no plan step (`tl_instruction.md` carries no execution metadata, § Execution context above), so it is `system/projects/<project>/project.md` `Languages:` → extension inference → the floor. Open the resolved language's `README.md` and read **every** concern entry it lists — not only the ones that look like they bear on the task. Which concerns bear on the change is a verdict the block records per concern (below), never a filter applied before reading. Honour precedence: the records above the packet, the packet above the surrounding file's own style, the floor below. **Write what you found into the `Language resolution:` block of the closing commit (Step 3).** A missing or partial packet is **never a halt and never a deferral**; not resolving is the failure. This step replaces the `optional context` input row that stood here until 2026-08-21, under which this skill required no record at all and a skipped resolution left no trace.

   **A claim about the packet is a quote, never a paraphrase.** Every packet clause the implementation turned on gets its own line in the block: the concern file and the line, the clause **verbatim between quotes**, and what the code does about it — followed, or diverged with the reason. A concern file you read that bore on nothing this change wrote or ran says *that*, which is also a line. **Open each file at the line you are about to cite and confirm the quoted sentence is there** — a heading line, or the line the section starts at, is not the line the clause sits on, and a clause cited at the wrong line is one a reader holding only the commit cannot check, which is the whole reason the block quotes. **Every concern the router sends to a packet file gets its own line** — a verbatim clause where it bore on the change, the trivially-borne-on ones included, or the bore-on-nothing line where it did not: a file named with a summary instead of a quote is the paraphrase re-entering through the one door this rule left open. **And the list is the packet's, not yours.** Completeness is measured against every concern the resolved packet's own `README.md` routes — open it, and account for each by its destination: a packet file by a quoted clause or by the line saying it bore on nothing this change wrote or ran; a named owner outside the packet exactly like a packet file — it is a file too, so by a quoted clause or the bore-on-nothing line, cited by its own path; and only a concern routed to the floor, where there is no file to quote, by a line naming the floor and what, if anything, bore on this change. A block reporting *all N read*, where N is the number the run chose to open, cannot show the destination it never opened: on 2026-09-10 a closing commit named five of the Python packet's six and said all five were read, and the one missing was Toolchain — on a run whose own gate commands were `uv run …`, and which shipped two over-length lines past a formatter nobody ran. *Ran* is not decoration: a concern can govern the commands a run uses — its toolchain, its formatter, its linter — without governing one line of the code it wrote, and *bore on nothing this change wrote* is then true and still the miss. Toolchain on 2026-09-10 was that case. The paraphrase is what makes the block unfalsifiable: one closing commit rendered the Python packet's version-marker clause as "`__version__` per module", where `<CORE>/doctrine/engineering/languages/python/conventions.md:133-137` says every non-test module carries the marker **and** that "a package carries the marker once, in its `__init__.py`". Seventeen new package members each carried their own — a real departure from the packet, recorded as compliance, because the summary was close enough to read as obedience and wrong enough to hide the departure. A reader holding the packet can check a quote; nobody can check a summary. **This is additive to the block and never a licence to shorten it:** the block is still written on a run that fell to the floor, where there is simply no packet to quote (`<CORE>/doctrine/flow/step_outcome_contract.md` — "`packet: null` is a real answer; an absent `language` is not").
4. Run the critical review pass (Step 1b).
5. Apply Step 2 § *Work and repair* to concerns the developer can resolve. For a remaining external impediment, apply § *Deferring a task* and § *When to Stop*.
6. Otherwise create TodoWrite and proceed.

### Step 1b — Critical review pass

The developer is the last quality gate before the code lands. Before implementing, check the instruction against the design and specification, and scan each task for gaps the implementation must fix:

| Check | Action when gap found |
|---|---|
| The instruction omits or contradicts a detail in the design or specification | Apply the **Resolving the implementation contract** rules below |
| A task's `#### Behaviours to verify` does not fully cover its stated responsibility | Add the missing behaviours as tests in the red phase; log it |
| An obvious edge case is absent from a task's behaviours | Add it as a test; log it |
| An imprecise construct (string field with a closed value set, stringly-typed state) | Upgrade it (e.g. → enum) during implementation; log it |
| Implementation housed in `__init__.py` — the layout lists `<package>/__init__.py ← modified` as the target for entities/services/repositories/CLI logic, or sanctions keeping code there | Split into named modules (`domain/models.py`, `domain/exceptions.py`, `persistence/json_repository.py`, …); `__init__.py` re-exports the module's public interface only; log it. Internal file layout is layout, not topology — the package boundary (`nfdr.md § 1.2`) stays binding. **Unless the design mandates a composition edge** — an `__init__.py` that only wires the package's own modules — which is the standard's one exception: build it and log it as such |
| New logic — placed by the instruction or added in this run — would sit outside its owning part's code, typically inline where it is first called (`<CORE>/doctrine/flow/development_flow.md` § *Code goes where the parts table puts it* defines *owning part*) | Write it in the owning part's code, within the task that needs it, and import it at the call site; log it. A new file inside a unit the design lists is layout, as in the `__init__.py` row above. **Unless that needs a unit `change_design.md §2` does not list, or an import `docs/nfdr.md § 1.2` forbids and the design does not allow** — both are the design's decisions: leave the logic where the instruction put it and log the case |
| A complex-task hint is unusable or misleading | Implement the correct architectural approach; log the divergence. Never the commands for a write into another repository: those run unchanged (Step 2 § *A write into another repository*) |
| Build order in the instruction violates a stated dependency | Reorder tasks; log it |
| A behaviour contradicts the spec or another task | Resolve against the owning contract below; record the correction, or defer an unresolved conflict |
| A resumed task is declared committed, but its code or proof does not satisfy the task | Apply **A landing commit** below to the current implementation; reopen the task and record the missing requirement and the earlier commit. A commit subject does not override the contract |

The two behaviour-coverage rows apply only to tasks that *have* behaviours. Three task shapes legitimately have no `#### Behaviours to verify`, and none is a coverage gap — do not fabricate behaviours or defer a task over their absence:
- A task whose `#### Implement` reads `No spec tests — implement per project layout above.` — the planner's signal for a structural/interface task (Step 2, step 2). Build it as a single plain commit.
- A task carrying `#### Deliverables verified by review` *in place of* `#### Behaviours to verify` — the planner's signal that no test can assert the deliverable (Step 2, step 2c). Its gate is that subsection's criteria, checked by reading the diff. For these tasks, read `#### Deliverables verified by review` wherever the rows above say `#### Behaviours to verify`; there is nothing to cover with tests.
- A `Behaviour: preserving` relocation task, which carries `#### Invariant gate` *in place of* `#### Behaviours to verify`. Its gate is the existing suite as the characterization contract, not a list of behaviours to red-test (Step 2, step 2 — the preserving lane). For these tasks, read the `#### Invariant gate` wherever the rows above say `#### Behaviours to verify`; there is nothing to cover.

**Preserving caveat on the `__init__.py` row.** For a `Behaviour: preserving` relocation, reducing `__init__.py` to re-export-only and moving implementation into named modules **is the task itself** (development-design's §3 Layout Plan), not a developer-initiated split — implement the move as planned; it needs no Developer Review Note.

**Resolving the implementation contract.** The specification owns behaviour and scope; the design owns technical structure; the instruction turns those into executable tasks. Read `## TL Review Notes` to distinguish a deliberate improvement from an omission or mistake.
- When the instruction omits or misstates a detail already settled by the design or specification, implement the settled contract, add the tests it requires, and cite the source and correction in Developer Review Notes. An incomplete instruction alone is not a blocker.
- Respect a documented TL improvement within the change's behavioural and architectural constraints. Apply the standing standards to implementation details and record the reasoning. `CONTENT.md` supplies verbal rules, not a required catalogue of per-change strings: write copy that satisfies those rules and the specified behaviour. An absent literal sentence is not a missing content decision. Honour prescribed wording where a source actually requires it. **Where the branch holds `change_text.md`, that is the source: every published string comes from it verbatim, and this run writes none of its own.** Where `tl_instruction.md` carries wording of its own for a place the file covers, `change_text.md` wins and the instruction's wording is set aside and logged. A string that cannot be placed as written (a fragment assembled at runtime, a control with no name to give) is recorded in Developer Review Notes as a finding for the Content Editor and is not reworded, and the rest of the task is built. Without a `change_text.md`, this paragraph's CONTENT.md rule above is unchanged.
- When the sources leave a required product, architectural or content rule undecided, or conflict on one, **defer the affected task** and its dependents (Step 2 § *Deferring a task*). Name the missing rule or conflicting sources and the decision needed; do not turn implementation latitude into an upstream decision request. Continue independent tasks. Only a decision that blocks every task is a halt; the developer does not author an upstream companion.

**Boundaries (the same the TL observes relative to the architect):** topology is binding. Do not add or rename modules, change package structure, or alter the architect's and TL's structural decisions. Writing new logic in the part that owns it, inside a unit the design lists, is not one of these (Step 1b's row on new logic outside its owning part). Type-level and test-coverage improvements are in scope; structural changes are not. Do not remove behaviours — they carry forward unless one directly contradicts the spec, and any reduction requires a logged reason.

**Record every divergence from the instruction — mandatory.** Log in `Developer Review Notes` (closing commit body, Step 3) every decision where the implementation departed from or went beyond `tl_instruction.md`, **each with its reason**: every improvement (edge case added, imprecise construct upgraded, coverage raised) **and in particular** any decision that (a) **resolves a contradiction** between `tl_instruction.md` and `change_design.md` (per Resolving the implementation contract), (b) **locks an observable behaviour the instruction left implicit**, or (c) **overrides an upstream recommendation** (e.g. an unusable hint). Omit the block only when nothing diverged **and** no task ran in the review-verified, already-green or red-at-baseline lane **and** no task landed more than one rule at one entry point. Those notes — the per-deliverable verdicts, why a red phase was impossible, which baseline-red tests went green, and the per-rule discrimination lines — are required whether or not anything diverged (Step 2, lanes c, d, f and e). **The licence covers this block alone, and not on a product with no code**, where the block carries each preserving invariant's quoted text before and after (lane (a)) — `Step 1b review:` is its own block and is never omitted, so "nothing diverged" is a thing this run says rather than a silence it leaves. A silent divergence turns a reviewable decision into an unexamined assumption — the divergence record exists for downstream review. (This is the developer-stage analog of development-plan's `## TL Review Notes`.)

**The pass leaves a record whose zero case says something — mandatory.** A run that adds no case and logs no divergence is indistinguishable from one that never made this pass, and that has happened: in one change unit every delivered test mapped one-to-one onto a test the instruction named, none was added, two rule-implied edges escaped to the next step, and the run broke no rule doing it — because every obligation above is conditional on having found something. So the `Step 1b review:` block (Step 3) is written on **every** run, and what it carries is the **derivation** rather than the verdict: per task with a gate subsection, the edges you derived from that task's own stated responsibility and where each one landed — already covered by a named test, added as a named test, or out of scope with its reason. `none beyond the listed behaviours, because <why>` is a legal entry and is the zero form; an absent line is not. A transcribing run has no edges to name, and that is the whole of the signal. This is the fence the `Language resolution:` block already stands behind (`<CORE>/doctrine/flow/step_outcome_contract.md`, "`packet: null` is a real answer; an absent `language` is not"), applied to the other thing this step could not prove it did. **And the block counts in both directions.** `Cases added beyond the instruction` has a counterpart line, `Instruction cases not delivered`, because a count that can only rise reads healthy whether the run delivered everything the instruction named or quietly dropped one of them. `0` is legal and is the usual answer; an absent line is not. On 2026-09-09 that asymmetry is what let a dropped case land invisibly and let a mis-tally in the other direction pass as a healthy positive number. **A case is delivered when it asserts everything the instruction states for it**, not when a test carries its name: a case written under its name with a stated assertion missing goes on the not-delivered line, naming what is missing. On 2026-09-10 a closing commit read `0` while five assertions the instruction stated were missing inside correctly named cases.

**Headless startup gates** (when `system/projects/<project>/project.md` execution type is `headless`):

You entered the worktree in **Enter the worktree** above (`cd "$WORKTREE"`). These gates confirm the entry actually landed on the change branch before any code is written — this is the only stage that writes code, so a wrong branch silently breaks the worktree isolation every upstream stage preserved; the gate is mandatory, not advisory.

1. The change branch is `<key>` — the folder name holding `tl_instruction.md` (`system/projects/<project>/journey/tobiishi/<key>/`), identical to the worktree path suffix (`<repo>/.worktrees/<key>`) by the worktree convention.
2. From the CWD (now `$WORKTREE`), `git branch --show-current` must equal `<key>` — if it prints the default branch (`main` / `master`) or any other branch, **halt** (no task could land). A mismatch means the `cd` did not land in the change worktree (e.g. `$WORKTREE` was missing and the enter was skipped); do not write a line of code.
3. `git rev-parse --show-toplevel` must be the worktree (`…/.worktrees/<key>`), not the primary checkout — if it is the primary checkout, **halt**: the session is not inside the worktree. For an external product this is not enough on its own: the product repo carries a `.worktrees/<key>` on a branch of the same name, so gates 2 and 3 pass inside *either* repo. Gate 4 is what tells them apart.
4. The `tl_instruction.md` path must resolve (`ls system/projects/<project>/journey/tobiishi/<key>/tl_instruction.md`) — if not, halt. It resolves only in the **instance** worktree, so this gate is also the proof that `$WORKTREE` is the instance one and not the product's namesake.
5. Do **not** run `git worktree add` — development-specs created the worktree; this skill only enters it.

**Docker startup gates** (when `system/projects/<project>/project.md` execution type is `Docker sandbox`):
1. `pwd` must print `/workdir` — if not, halt
2. `git branch --show-current` must match the branch the launcher checked out — if not, halt
3. The `tl_instruction.md` path from the launch prompt must resolve (`ls <path>`) — if not, halt
4. Do **not** run `git worktree add` — the repo is already mounted
5. Read `## Project layout` and create every listed directory and `__init__.py` (under `<name>/`) before starting tasks. If `## Project layout` is absent, derive directories from each task's path annotation and create missing `__init__.py` files before that task's first implementation step.

### Step 2 — Developer batch

Execute all tasks unless the launch prompt limits the batch (e.g. "First 3 tasks only"). **`Tasks 1–<N> are committed; start at task <N>+1` locates progress; it does not certify completeness.** The chain derives that offset from a pause or landing commits. Step 1 and Step 1b run in full: check the tasks declared committed against their current code and proof using **A landing commit** below. Reopen any that fail that check, record the evidence in Developer Review Notes, and finish them before continuing at `<N>`+1. Keep valid prior work; do not repeat it merely because the session is fresh. An explicit batch limit still bounds which tasks may be built. If that limit leaves later tasks untouched, end at the requested boundary with committed work and a statement of what remains; do not write an `implementation complete` marker or invent a context-cap notice. This owner-scoped exit is not one of the workflow's failure halts. Otherwise, when no task remains to implement or defer, go to Step 3, even when a closing marker already exists (Step 3 § *A re-close makes a new marker*).

All code and tests are written **under `<name>/`** (project-root), per the instruction's `## Project layout`. The test command from `system/projects/<project>/project.md` runs from the product's change worktree root, not from `<name>/` (§ *Execution context*).

**For an external product (the contract's `code_worktree` apart from its `pipeline_worktree`, § *Where each commit goes*):** `<name>/` = `$PROJECT_ROOT` sits inside the **product** worktree, a separate git repo. Do the per-task TDD work with that worktree as the working dir so the red/green/refactor commits land on the **product** branch (`git -C $PROJECT_ROOT`); the closing commit (Step 3) stays on the **instance** branch (`git -C $WORKTREE`) — a different `--repo` value from every per-task commit you just made. For an in-repo product the two are the same repo — no difference.

**Task isolation:** Step 1 reviews the whole instruction; implementation works one task at a time. Complete task N's full cycle and commit it before implementing task N+1.

#### Work and repair

For each task, compare the current code and tests with the specification, design and instruction, then implement, verify and repair until the whole contract is delivered. Apply this loop to inherited work as well as work written in this run; a previous commit, completion marker or review is evidence to inspect, not a reason to leave a defect in place.

- Write missing tests and finish incomplete assertions from the required behaviour. Repair defective implementation. When this change deliberately replaces behaviour, replace the obsolete expectations and prove the replacement while retaining unrelated guarantees. A failing test does not decide whether the test or the implementation is wrong; the owning contract does.
- Run the task's full verification gate, await its completed result and diagnose failures with `debugging-and-error-recovery`. Correct their cause and verify again. An unfinished test, a missing test seam, repeated failures or a partially working implementation remains developer work; do not convert it into a deferral or a proposal for someone else to finish.
- Improve defects encountered while doing this work under `<CORE>/doctrine/governance/found_while_walking.md`. Resolve omissions from the upstream contract through Step 1b, preserving the specified behaviour and architecture. Record corrections in Developer Review Notes.
- Finish only through § *A landing commit*, an evidenced external impediment under § *Deferring a task*, or the existing batch-limit, context-cap and run-halt rules. The preserving lane retains its baseline and reclassification halts; this loop does not authorize changing its characterization tests.

For each task:

1. Establish the task's full responsibility, required assertions and verification gate from the resolved contract before marking it in_progress. Resolve decision blockers through Step 1b before writing red tests, so tests for a task already known to be blocked do not prevent independent tasks from compiling or verifying. **Before any landing commit in any lane, apply the completion check in A landing commit below.**
2. **Route the task by its gate header and its `#### Implement` marker — six lanes.** Read both before doing anything else. The gate header names the lane where the task has a distinctive one; where a lane shares `#### Behaviours to verify` with another, or has no gate subsection at all, the `#### Implement` marker decides. Both are literal text `development-plan` and `ad-hoc-plan` are required to write (`<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Implement section rules*), never something inferred from what the task looks like:

   **(a) Preserving relocation lane** — the task carries `#### Invariant gate` (in place of `#### Behaviours to verify`) and its `#### Implement` body ends in **`No new tests — TDD under green`**. On a card reading `Test command: none` the steps below run on the gate's checks instead of a suite (`<CORE>/doctrine/flow/change_classification.md` § *A product with no code*). Step 1: every invariant holds at its before-place, or the run halts as § *When to Stop* case 2. Step 3: every invariant holds at its after-place and nowhere else, or it is the step-4 reclassification halt. Each invariant's quoted text before and after goes in `Developer Review Notes`, which this path never omits. This is a `Behaviour: preserving` move: production (and any mirrored tests that reference a relocated path) move together, green→green, **no red phase**. Execute it as one atomic relocation:
   1. **Baseline green** — run the test command (`system/projects/<project>/project.md`). The full existing suite must be green *before* the move, **except** for the tests the task's `#### Invariant gate` lists on `Red at baseline:` lines. Those are the violations `change_spec.md` names as the ones this change repairs, and they must be red. Any other red test, or a listed test that is already green, means the baseline is not the one the spec described: **halt** (§ *When to Stop*, second case) and do not move on top of it.
   2. **Move** — perform the relocation per the §3 Layout Plan referenced in `#### Implement`: shift the symbols into the named module(s), reduce `__init__.py` to re-export-only (public surface identical), and write the imports that travel with the moved code. Move a test file only where it references a relocated path; an intra-package move behind the preserved re-export leaves tests put. **Do not invent a red.**
   3. **Green again** — re-run the suite. It must pass **unchanged**, and every `Red at baseline:` test must now pass too: every symbol importable before is importable after, same signature; no public symbol dropped from any `__init__.py`. A listed test still red means the change did not repair what the spec named: return to § *Work and repair* without editing the characterization test.
   4. **Reclassification halt** — if a previously-green test goes red, that is a **reclassification event**, not a bug to fix: the "preserving" classification was wrong (a test reached into an internal path the move disturbed). **Halt and surface it (§ *When to Stop*, third case). Never edit a test to make it pass.**
   5. Commit **one** plain `developer: task N <slug>` commit (production + any co-moved tests together). Skip steps 3–5, then go to step 6.

   **(b) No-test structural lane** — `#### Implement` reads `No spec tests — implement per project layout above.`. The task has nothing to test — a package skeleton, an `__init__.py` set, a Protocol definition, a `pyproject.toml`, or a prose file like a README. Build it to the `## Project layout` and the task's `**What to build:**`, satisfy its `#### Verification gate` (run the command if the gate is automated — `python -c "import …"`, `pytest` collects-zero; verify by hand if the gate is prose), and commit **one** plain `developer: task N <slug>` commit. No red phase is invented — the task has no tests, so it was never in the red/green lane. This is the tracker5 shape: `developer: setup tasktracker5 package structure`, `developer: task-4 ports protocols`, `developer: README.md — package docs`. A per-task subject carries no ` — ` in its slug: § *A landing commit* reads what follows one. Skip steps 3–5, then go to step 6.

   **(c) Review-verified lane** — the task carries `#### Deliverables verified by review` (in place of `#### Behaviours to verify`) and its `#### Implement` reads `Verified by review — no test.`. The deliverable is a content change no test can assert — a pinned version in a manifest, a generated file's shape, a copy string — or a check that holds only while this change is built. Build it, then check **each line of that subsection against the criterion it states, by reading the diff** — and where a line names a command, by running it, in the repository whose files it names — satisfy the `#### Verification gate`, and commit **one** plain `developer: task N <slug>` commit. No red phase is invented — there is no test to make fail. **Record the review in `Developer Review Notes`** (Step 3): one line per deliverable, with the verdict you read off the diff. The record is required even when nothing diverged — a review that leaves no trace is indistinguishable from a review that did not happen, which is the whole reason this lane exists. Skip steps 3–5, then go to step 6.

   **(d) Already-green lane** — the task has `#### Behaviours to verify` and its `#### Implement` reads `Tests cannot go red.` followed by a `Reason:` line. The behaviours are real and must be asserted; their subject already satisfies them, so no test of them can be made to fail first. Write the tests, run them (they pass on the first run), satisfy the `#### Verification gate`, and commit **one** plain `developer: task N <slug>` commit. **Never manufacture a red by breaking the subject** — that edits working code to produce a signal, which is the opposite of what a red phase proves. **A `Developer Review Note` naming why the red was impossible is required** (Step 3): restate the plan's `Reason:` line and say whether you found it true. Without that note the missing red is silent and reads exactly like a skipped phase, which is the failure this lane exists to end. **Steps 3 and 4 below still apply** — this lane writes tests, so the behaviours are read as their specification and any inline TL stub is materialized rather than discarded. Skip only step 5, whose `test-driven-development` call owns a red/green commit pair this task does not have, and go to step 6.

   **A TDD-lane task whose red does not go red is in lane (d), and the plan did not know.** Write the tests the red phase asks for; if they pass the moment they are written, do **not** edit the subject to force a failure and do **not** land a red/green pair that never happened. Finish the task in lane (d) — one plain commit — and log **both** facts in `Developer Review Notes`, on one line in exactly this form: `- Task N no red (lane d) — <why a red phase was impossible>, <confirmed | the plan's reason did not hold: ...>`, the template line in Step 3. The line itself says the task was re-laned; the chain reads it by that form. This is a divergence from `tl_instruction.md` and is recorded like every other one (Step 1b).

   **(f) Red-at-baseline lane** — the task has `#### Behaviours to verify` listing `Red at baseline:` tests, and its `#### Implement` reads `Tests are red at baseline.` followed by a `Reason:` line. The tests already exist and already fail on `main`, committed there by an earlier change unit that deferred the task that turns them green. Their red is real but it is not yours to commit, so there is no red commit to make. Before touching the subject, **run the listed tests and confirm each one fails**: that run is the red phase, witnessed rather than committed. Then build the task, re-run them until every listed test passes and the rest of the suite has no new failures, satisfy the `#### Verification gate`, and commit **one** plain `developer: task N <slug>` commit. The lane writes no test: the task carries nothing but its listed tests, so an edge you find missing is recorded in `Step 1b review:` as out of scope or owned by another task, never added here, where its red would land inside the one commit. A listed test that already passes at baseline means the plan's reason did not hold for it; say so in the note rather than halting. **A `Developer Review Note` is required** (Step 3): name the listed tests, red before and green after, and say whether the plan's `Reason:` held. Skip steps 3–5, then go to step 6.

   **A TDD-lane task whose failing tests are already on `main` is in lane (f), and the plan did not know.** When the red phase asks for tests that already exist and already fail at the change's base — left there by an earlier change unit — there is no red commit you can make. Do **not** commit a reworded copy of them to manufacture one. Finish the task in lane (f) — one plain commit — and log **both** facts in `Developer Review Notes`, on one line in exactly lane (f)'s note form: `- Task N red at baseline (lane f) — <the listed tests, red before and green after>, <confirmed | the plan's reason did not hold: ...>`, the template line in Step 3. The line itself says the task was re-laned; the chain reads it by that form. This is a divergence from `tl_instruction.md` and is recorded like every other one (Step 1b).

   **(e) TDD lane** — the task has `#### Behaviours to verify` and an `#### Implement` that is none of the markers above. Continue with the TDD path below.

   **A `Red is probabilistic:` line in any lane's `#### Behaviours to verify` is a contract, not a note.** It says the plan knows that behaviour's red is not deterministic on the tree as it stands. What to do about it is yours: make the red **reproducible** before treating it as a red phase — repeat the case enough to be sure, or constrain the schedule so the failure is forced — and if you cannot, diagnose the proof gap through § *Work and repair*. Only an evidenced external impediment qualifies for § *Deferring a task*; a single observed failure or green is insufficient proof. A race that went red once is not a red phase, and a green over a race proves nothing. Record what you did in `Developer Review Notes`, naming the behaviour and how the red was forced.

   **A task landing more than one rule behind one entry point proves them one at a time.** A red phase answers *did the task's cases go red* and never *red because of which rule* — so where the green phase would satisfy several separately-removable rules at one call site (three conditions enforced by one function, three fields validated by one constructor, three checks reported by one command), land them **one rule at a time** and re-run the task's cases after each. A case that flips red→green exactly when a rule lands is the case that goes red when that rule alone is reverted; that is what *the red phase proves this rule* means, and a phase that was red overall establishes nothing about any single rule inside it. **A rule whose landing flips no case is proved by nothing in this task** — add the case that discriminates it (Step 1b latitude), or say in `Developer Review Notes` that none can exist and why. Record the mapping there either way, one line per rule (Step 3, the `Rule discrimination` entries). This is not a hypothetical cost of the bundled shape: three rules of one change unit were deletable with the whole suite green, each caught later by mutation in the next step's code-integrity report, and each had been genuinely red before its task and green after.

   **Key the note to the entry point, not to the task.** Name the function or the call site that carries the rules — a task number names a boundary the code does not have, and a note written against the wrong task can read as complete while the seam that actually holds two rules carries nothing. Where the discrimination was established by a later step rather than by this one, say so and cite it rather than claiming the red phase proved it.
3. *(Not for a preserving, no-test, review-verified or red-at-baseline task — each already committed at step 2. An already-green task does read this: it writes the tests, and only the red/green pair is absent.)* Read the task's `#### Behaviours to verify` as required assertions for the red phase, including each case's stated conditions and negative guarantees. Resolve any disagreement through Step 1b; do not narrow the task to the first reproducible failure.
4. **Honor inline TL stubs.** If the task carries minimal test stubs (development-plan emits them only when prose was insufficient), use them as the seed of the red phase — materialize them into the test file and expand. The stubs are TL-authored fragments; do not discard them.
   **A task whose proof starts a real process gates on the finished start, and is run more than once.** Where the verification starts a server, a thread or a subprocess and then asserts against what it bound, opened or wrote, state the readiness condition as a property of the **completed** start — every listener registered, not the first — and re-run the case before closing the task. A gate that returns on the first observable can compare a half-built state against the expected one and pass by timing: one such case reproduced at 1 failure in 60 runs, green on the pass that closed it. A single green pass is not the gate for this shape.

5. Invoke `test-driven-development` for this task:
   - Pass the slug `task N <slug>` and the whole task's required assertions as context — `test-driven-development` owns the red/green/refactor commits and writes their messages. Its green commit must satisfy **A landing commit**, not merely the tests written so far.
   - Invoke `source-driven-development` during red or green when writing against unfamiliar libraries or APIs.
   - If a listed behaviour depends on a later task, resolve the build order through Step 1b before starting this task. A TODO naming the prerequisite is not delivered proof; an unresolved dependency follows § *Deferring a task*.
   - A no-test task (the `No spec tests` marker), a review-verified task (the `Verified by review — no test.` marker), an already-green task (the `Tests cannot go red.` marker), a red-at-baseline task (the `Tests are red at baseline.` marker) and a `Behaviour: preserving` relocation (the `#### Invariant gate` / `No new tests — TDD under green` markers) are all handled at step 2 — as a single plain commit, never a manufactured red. If a *behaviour* on a TDD-lane task genuinely cannot be automated, verify it by hand at the green step and note it in the commit body.
6. **Finish each verification execution before judging its result.** Preserve its full return record, including running handles and exit status; forwarding only output text discards the means to await it. If a tool call yields, await that call; if its result contains a running process handle, poll that same process until it exits. Partial output or a tool wait limit is not a test failure or an unavailable verdict. Do not launch a duplicate suite while its earlier execution is live, or end the run with its verification still pending. Read the completed output and exit status, then invoke `debugging-and-error-recovery` for an unexpected failure. A genuinely terminated or unreachable execution needs its concrete error recorded before a retry or deferral.
7. **After the completion check and landing commit, confirm the task's files are committed.** Run `git -C $PROJECT_ROOT status --porcelain` over the files the task wrote — the product worktree for an external product, not `$WORKTREE`. Commit any remaining task work before marking it completed. A clean tree proves the work was saved, not that the task was delivered. Repeat until all tasks are done or deferred, or until the run pauses at the context cap (§ *Pausing at the context cap*, below).

Commit per task — one logical unit per commit. Intermediate units may be saved with `— in-progress`; they do not earn a landing subject until the whole task passes the completion check.

#### A landing commit

**A task earns a landing commit only when its whole resolved contract is delivered.** Before writing that commit, compare the implementation and proof with the task's responsibility and each required assertion or review criterion, then run its verification gate. Read the assertions themselves: an absent test cannot fail, and a correctly named test can still omit the required check. Record the requirement-to-proof mapping in the landing commit body, using tests or reviewed code as appropriate to the lane. Structural and preserving tasks keep their own gate; do not invent new tests for them.

**An incomplete task returns to § *Work and repair*.** If an earlier commit claimed it landed, retain that history and append the correction with its evidence; apply the current completion check before declaring it delivered.

**The on-disk landing signal is the subject.** The chain's resume, `development-code-integrity`'s check 2 and the seal's check 2 read `developer: task <N> <slug>` (or `developer: task-<N> <slug>`) with no ` — ` suffix, or a final suffix exactly `green` or `refactor`. Every other suffix, including `red`, `in-progress` and `deferred`, is non-landing. This signal locates work for review; it is not evidence that the completion check passed.

**A deferral must not hide delivered work.** Ordinarily a deferred task has no landing subject. If it has one, the closing marker's Developer Review Notes must identify that commit, the unmet contract requirement, and the code or proof that falsifies the claim. A reader checking the deferral verifies that evidence against the current tree; an assertion that the old commit was wrong is not enough. A task that now satisfies the completion check cannot remain deferred.

#### Deferring a task

Defer only when § *Work and repair* cannot proceed without a specific external decision, permission, capability or dependency. A write into another repository defers without that recovery, as its own § says. Otherwise, establish that boundary after diagnosis and attempted authorized recovery: name the command or conflicting sources, the corrective action or approval requested, its result, and what must be supplied from outside this run. For a permission failure, request the required operation through the runner's supported approval mechanism or use an already-authorized environment that preserves the gate; never bypass a denial. Resolve product or architectural uncertainty through Step 1b before declaring an external decision necessary.

A qualified deferral carries its evidence in the closing marker. Continue independent tasks; apply the dependency rule below to the others. When every task is externally blocked, § *When to Stop* applies.

- **Dependents.** A task depends on a deferred task only when it uses something that task would have made — a file, a module, an interface it calls. Defer it too, and commit nothing for it. A `**Dependencies:**` line is the plan's claim about that, not the test. A task that uses nothing the deferred task would have made is built even when the line names that task, and its `Developer Review Notes` entry says why. The task's own text saying it is independent is evidence of that, not a second test.
- **The blocked case stays in the tree.** Tests that state it are committed as written, under `developer: task <N> <slug> — red`. Any partial code kept for the task is committed as `developer: task <N> <slug> — deferred`, never under `— green`, `— refactor` or a plain subject, because those say the task landed (§ *A landing commit*). Nothing is deleted, weakened, skipped, deselected or marked expected to fail, and no guardrail, threshold or property is loosened to get past the block.
- **No document is edited.** Not the change's `change_spec.md`, `change_design.md` or `tl_instruction.md`, not any document under the product's docs, and not any `*_open_issues.md`. For each blocked task the marker body carries the evidence — the command run and what it returned — and may propose a fix, marked *not applied* (Step 3).
- **An instruction's own "stop" adds no halt or deferral.** The one exception is a `No allow rule:` line on a write into another repository, which defers the task (§ *A write into another repository*). Resolve its reason through Step 1b and this section; the word alone establishes no external impediment.
- **The suite stays honest.** `Suite:` is the test command's real exit. A blocked case that fails makes it `Suite: red`, and it is never made green by excluding a case.

#### A write into another repository

Some tasks write into a repository that is neither the instance worktree nor the product worktree, such as copying a file into a host's `about/` and committing it there. Make that write only as plain calls: the copy is one call and the builder's commit another, every path a literal in the form that doctrine section sets. The task's `**What to build:**` gives those calls, under `Commands for a write into another repository:`. Run them unchanged, except that `<CORE>` is replaced by this run's resolved core path, written out literally. Step 1b improves the instruction, but it does not reshape these calls. Never wrap them in a script, set a shell variable for a path, chain them with `&&`, `;` or a pipe, or fold a check into them. Run each read-only check as its own call before the write, the other repository's status among them, and keep its output. Where the task carries a `No allow rule:` line, do not attempt the write: defer the task with that line as its evidence. The harness matches a call by its literal text, so any of those makes the write match no allow rule, and a launched run has no one to approve it (`<CORE>/doctrine/governance/commit_format.md` § *A write into another repository is plain commands, one call each*).

**A refused write defers the task directly.** § *Deferring a task*'s recovery does not apply to it: never retry it in another shape or another environment. If the copy landed and the commit was refused, first undo the copy with the task's own undo command, as a call of its own. Then read the other repository's status again and compare it with the output kept before the copy. Then defer the task, with the refused call and the allow rule it needed as the deferral's evidence. A commit the builder or the other repository's hook refuses, or a status that still differs after the undo, is deferred the same way, without the undo or a re-run. The other repository's status goes in the deferral's evidence.

**A write that lands still lands the task on the run's own branch.** The other repository's commit is not the task's landing commit, because the chain reads landing subjects only on the change branch. The task lands through § *A landing commit* as usual, and the developer writes that commit's body naming the other repository's commit by its full hash, in either lane. If the task changed nothing in the run's own repositories, the landing commit is made with `--allow-empty`, to the repository its per-task commits go to.

#### Pausing at the context cap

When a chain runs this skill it may set a context cap, and a hook reports once the session's current context is over it. The notice arrives after a Bash call and names the size and the cap. **It is a pause, not a stop.**

1. Finish the task in progress, through its last commit and step 7's clean-tree check. Never leave a task half-built, and never start the next one.
2. Make the **pause commit**, an empty commit made exactly the way Step 3's marker is made: through the builder, with the instance worktree as `--repo`, `--allow-empty`, the same `--actor developer` and `--skill development-implementation`.
   - **Subject:** `developer: <key> — implementation paused after task <N>`, where `<N>` is the last task committed. The subject must never contain `implementation complete`. The chain reads that phrase as the closing marker, and the seal would take a paused run as finished.
   - **Body:** the run's record so far, in Step 3's shape: the `Language resolution:` block under one plain heading (Step 3, **One language block**), the `Step 1b review:` block, and the `Developer Review Notes` for the tasks done, and the `Deferred:` lines so far, as bare lines. Leave out the `Suite:` line and the `Skills run this session:` checklist, which belong to the closing marker only.
3. Read it back with `git -C "<instance-repo>/.worktrees/<key>" log -1 --format=%s`. The newest subject must be `developer: <key> — implementation paused after task <N>`. An inherited closing marker remains in history; this run must not write a new one while pausing. That is not § *Exit*'s test, which looks for the marker. If the pause commit is missing, it went to the wrong repo: remake it through the builder with the instance worktree as `--repo`, and read it back again.
4. Check that the trees are clean: `git -C "<instance-repo>/.worktrees/<key>" status`, and for an external product `git -C $PROJECT_ROOT status` too. Then end the run.

The chain reads `<N>` off the pause commit and relaunches the rest (the batch-scope rule above). A relaunch that pauses again makes another pause commit, with its own `<N>`.

### Step 3 — Close

After every task has passed **A landing commit**'s completion check or been deferred. If preparing the closing record reveals missing work, return to that task; a green suite and an earlier landing subject do not discharge it. An explicit batch limit leaving later tasks untouched is not completion of the change.

1. Make the closing commit. This skill owns the closing commit — its subject, body, and skills-run checklist are defined here, not read from the instruction. The per-task code is already committed, so this is an **empty marker commit** whose body carries the run's whole record — the `Suite:` verdict and the `Environment:` lines it ran in, the `Language resolution:`, the `Step 1b review:` and the `Developer Review Notes` — the developer-stage audit record the architect reads downstream. The change is identified by its Tobiishi `<key>` (the branch / folder name), not an issue number.

**After a pause, the marker's record covers the whole change, not only this run.** Read the body of every pause commit on the branch (`git -C "<instance-repo>/.worktrees/<key>" log main..<key> --grep='implementation paused after task' --format=%B`). On a re-close, read only the pause commits made after the superseded marker (**A re-close makes a new marker**, below): replace `main..<key>` with `<superseded marker>..<key>`, because the superseded marker already carries every pause made before it. A re-close with no pause after its superseded marker skips this paragraph. Carry their `Step 1b review:` task lines, `Deferred:` lines and `Developer Review Notes` entries into the marker's blocks, so a reader holding only the marker sees every task. The language block is the next paragraph's.

**One language block.** The marker carries one `Language resolution:` block under one plain heading, and so does every pause commit. Write no second heading, and no label between the words and the colon (`Language resolution (tasks 1 to 3):`). `development-audit` counts one block's concerns against the packet's list, and a second block is a second roll-call to reconcile. This replaces the earlier rule to carry pause clause lines into the block, which said neither where they go nor whether this run re-derives them. What fills the block depends on what this run built:

- **A run that landed no task**, because earlier runs committed every task, re-derives every line against the code the whole change wrote (`main..<key>` in the repo the code lands in). It carries nothing from the pause commits. They are its inputs, not its record.
- **A run that landed tasks** writes its own roll-call and its per-concern lines for the code it wrote. For a concern its code did not bear on, it adds the pause's line under the same heading with ` — tasks <a>–<b>, from <pause short SHA>` appended. A pause's roll-call lines are dropped, because this run's roll-call is the block's only one. Where this run and a pause both cover a concern, only this run's line stays.

**A re-close makes a new marker.** A run can reach Step 3 on a branch that already carries a `developer: <key> — implementation complete` commit. That happens when the owner starts implementation again, including a chain restart after integrity rejects a declared deferral. The usual reason is an earlier marker that says `Suite: red` for cases no deferral owns, after that red has cleared. After the current completion checks, look for an earlier marker:

```bash
git -C "<instance-repo>/.worktrees/<key>" log -1 main..<key> --grep='<key> — implementation complete' --format='%H'
```

The grep carries `<key>` because the chain only counts commits whose subject names the key (`_own_commits`), and another change's marker carried onto the branch by a merge is not this change's. If it prints a SHA, record it as the **superseded marker** and make a new closing commit anyway. Never stop at the old marker, and never amend or rewrite it. The chain reads the newest marker (`<CORE>/tools/chain_development.py` `Git.commits_ahead` lists `main..<key>` newest first, and `DiskReader.marker_commit` takes the first match), and so do `tobiishi-seal` and `development-code-integrity`. The old marker stays in history, and the new one is the whole record:

- `Language resolution:` and `Step 1b review:` are this run's own. Step 1 and Step 1b ran in full on this launch (Step 2), so their blocks replace the superseded marker's. Where the superseded `Step 1b review:` has a task line this run did not re-derive, carry that line over unchanged.
- Carry the superseded marker's `Developer Review Notes` forward, then the notes of any pause made after it (**After a pause**, above), then this run's own. That marker already holds the records of every pause made before it. Leave out a `Task N blocked` note for a task that has landed since.
- Write `Deferred:` lines fresh from each task's current completion check and blocker, by § *Deferring a task*. Include a reopened task that remains blocked despite an earlier landing subject. Drop an earlier deferral only when the task now passes the completion check, and name it on the re-close line below.
- **Run the test command** (`system/projects/<project>/project.md` `Test command:`) now, once, after any task this run landed, **through the gate tool** (§ *The closing run goes through the gate tool*, below, and `<CORE>/prompts/gate_suite.md`). The `Suite:` line, the `Environment:` lines and the `Failing:` lines come from that run and from nothing else. A run from earlier in the session does not count — an earlier narrowed task gate supplies neither the `Suite:` line nor any `Environment:` line — and nothing is copied from the superseded marker.
- Add one `Developer Review Notes` line: `Re-close — supersedes <superseded marker's short SHA>; <what changed since, or "no commits since; the suite was re-run">; <deferrals dropped as landed, or "no deferral dropped">`.

**Declare the suite verdict.** The `Suite:` line states the test command's exit state at the moment this commit is made — `Suite: green` when the last run of the test command (`system/projects/<project>/project.md` `Test command:`) exited clean, `Suite: red` when it did not. A red suite is declared, not omitted: `Suite: red` is written exactly like a green one, never left off the marker so a downstream reader of the commit alone can see it. It is the command's real exit: a blocked case that fails makes it `Suite: red`, and it is never made `green` by excluding, skipping or deselecting a case.

**A card with no suite is the one exception.** A product with no code has nothing for a test runner to run, and its card says so with `Test command: none`. On that card there is no command to run, here or on a re-close, and the line is `Suite: none`. Nowhere else is `none` a verdict. The chain reads the card on `main`, never the branch's copy, and halts `missing-suite` on a `Suite: none` beside any card there that names a command, so `none` cannot stand in for a red suite. Where the card names a command that cannot pass on this product, for example `pytest tests/` over a product with no `tests/`, the line is `Suite: red`. Changing the card is not this run's to do. Say so in `Developer Review Notes`, so the card can be settled on `main`.

**The closing run goes through the gate tool.** The run whose exit the `Suite:` line states is the card's whole `Test command:`, issued by `<CORE>/tools/gate_suite.py` in the environment the product's CI calls for. The owner's Mac is that environment only when the product has no CI, the product's decision files choose it, or the owner asked. Read `<CORE>/prompts/gate_suite.md` and follow it: it owns how the evidence is read, where the owner's ask comes from, and the three calls. This skill's own call, with the evidence file that recipe's Step 3 builds, is:

```sh invocation
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate developer --inputs "<inputs file>" \
  > "<output file>" 2> "<error file>"
```

On a card reading `Test command: none` no evidence is read, and the call carries none:

```sh invocation-no-inputs
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate developer \
  > "<output file>" 2> "<error file>"
```

Where the owner's ask applies, the recipe's second call replaces the first, with `--gate developer`.

- **Every `Environment:` line the tool printed is copied whole.** Read them by `<CORE>/prompts/gate_suite.md` § *Reading the run's lines*: one line for one environment, and one line per container when the run resolved several. Write them as consecutive bare lines directly under `Suite:`, in the order the tool printed them. Never compose one from the evidence you read, never carry one from an earlier marker, and never take one from a task's own red or green run. Never leave one out. The commit builder refuses a marker that lacks a line the run printed, or carries one it did not. The tool's exit is the run's: `Suite: green` for 0, and `Suite: red` for anything else.
- **Failure is stated as a failure.** Whatever the environment, a refusal or an unreachable environment is `Suite: red`, not a failing test: the test command was not run. The `Environment:` lines are the ones the tool printed, and the chain halts on a marker where any one of them is `unresolved`. Write the first line the tool wrote to standard error in `Developer Review Notes` as `The test command was not run. It reported: {reason}`. Never run the card's command by hand to get a result, and never write `Suite: green` over such a run. An environment that was not ready, including one whose test command exited 127, is `Suite: red` too, and never a failing test. The tool prints an `Environment: not-ready — …` line for it among its `Environment:` lines, and that line is copied whole with the others. Write the line the tool wrote to standard error that begins `gate_suite: the environment was not ready for the suite in ` in `Developer Review Notes` as `The environment was not ready. It reported: {reason}`. The chain halts `environment-not-ready` on a marker where any `Environment:` line is `not-ready`.
- **A card with no suite** takes `Suite: none` and `Environment: none — no suite`, with nothing probed or run.
- **The per-task red and green runs keep the invocation they have** (Step 2). Only this closing run goes through the tool.

**The seal refuses a branch that does not carry it.** `tobiishi-seal` § Step 1 halts
`missing-implementation-marker` rather than sealing a change whose developer stage left no record on
the branch. Skipping this commit does not cost the run a formality — it stops the change from
landing, and it is caught by a `git log` over the branch rather than by anything this run says about
itself. It has been skipped: on one change the per-task bodies in the product repository held the
substance while the instance branch carried nothing from the developer at all.

**It is not usually skipped — it is misaddressed, and twice now by the same hand.** That change made
its marker; it made it with the *product* worktree's `--repo`, the value its per-task commits had
carried all run. It happened again on 2026-09-17, on a satellite change with an external
product: nine builder calls, the ninth carrying the
eighth's `--repo`, the marker on the product branch, the instance branch holding `specs`, `design` and
`plan` and nothing from the developer — and `chain-development` halted at `implementation` on a step
that had in fact finished its work. Nothing in that run was in a position to notice: the commit
succeeded where it was pointed, and both working trees were clean at exit. The prose above was already
here both times. What was missing was a run that reads its own marker back, which is why § Exit below
requires one.

Commit it through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = **the instance worktree**, written out as the absolute path you recorded at entry (`<instance-repo>/.worktrees/<key>`) — never `git rev-parse --show-toplevel` re-run from wherever you are now, and never a bare `$WORKTREE`, which by this point in the run expands to nothing. **For an external product this is deliberately not the `--repo` your per-task commits carried**: those went to the product worktree, and reusing that value puts the marker in the product repo, where neither `chain-development` nor `tobiishi-seal` looks. **Nothing staged** plus `--allow-empty` (the empty-marker case the recipe notes), **`--actor developer`** (the agent `launcher.md` launches this skill as — name it, never derive it), **`--skill development-implementation`** (this skill's own name, so the closing marker's `Skill-Version:` records what produced the implementation — provenance is explicit-only now, no longer derived from the actor), and the subject + body below. Never hand-write `git commit` or a trailer.

- **Subject:** `developer: <key> — implementation complete`
- **Body:**

```
Suite: <green | red | none>                   # NEVER omitted; none only on a card with Test command: none — declared either way, see Step 3 above
Environment: <one line the closing run's tool call printed, copied whole>   # NEVER omitted; one bare line for each Environment: line the call printed, all of them, in the order printed; none — no suite on a card with Test command: none — see Step 3, The closing run goes through the gate tool

Deferred: task <N> — <the blocked case> — <record>            # one bare line per blocked task; a run with no deferral writes none
Deferred: task <N> — depends on task <M> — <record>           # one bare line per dependent task
Failing: <case id> — task <N>                                  # when Suite: red — one bare line per failing case; `— no task` for one that belongs to none

Language resolution:                          # NEVER omitted — see Step 1 sub-step 3; one plain heading, after pauses too (Step 3)
- <language | none> — <declared in project.md | inferred from file extensions | none — <why no language resolved>>, chain step <n>
- <the packet opened, and every concern its `README.md` routes | no packet for this language — proceeded on the floor>   # the roll-call is the README's list, not the run's — see Step 1 sub-step 3
- <concern file>:<line> — "<the clause, verbatim>" → <what the code does, at the <file>:<line> this change wrote | under the clause's own words: "<the exception, quoted from the same clause>", <what the code does> | diverged: <what the code does instead>, <why>>   # one line per clause the implementation turned on; a concern file that bore on nothing this change wrote or ran says so; absent only when there was no packet
- <concern> → the floor — <what bore on this change | nothing this change wrote or ran>   # only for a concern the router sends to the floor; a named owner outside the packet is a file, and takes the clause line above

Step 1b review:                               # NEVER omitted — see Step 1b
- Design coverage: <the instruction covers change_design.md | omits <what>, and I <what I did>>
- Task N — edges derived from its stated responsibility: <edge> → <covered by test_x | added as test_y | out of scope, <why>>   # one line per task with a gate subsection; "none beyond the listed behaviours, because <why>" is the zero form
- Cases added beyond the instruction: <n>
- Instruction cases not delivered: <n> — <case the instruction named>: <the whole case, or the stated assertion missing from it> — <why>   # NEVER omitted; `0` is the legal and usual answer; a named case missing a stated assertion counts
- Task N placement: <each piece of new logic> → <its owning part>, <already in place | written there instead of <file> | left in <file>, <why>> | no new logic | no owning part | no parts table   # one line per task; NEVER omitted

Developer Review Notes (vs tl_instruction.md):
- <divergence / improvement> — <reason>
- Task N blocked — command: <the command run>; returned: <what it returned>; proposed fix (not applied): <optional>    # required per blocked task
- The test command was not run. It reported: {reason}    # required when the closing run was refused or could not reach its environment; {reason} is the first line the tool wrote to standard error
- The environment was not ready. It reported: {reason}    # required when the closing run's environment was not ready; {reason} is the line the tool wrote to standard error that begins `gate_suite: the environment was not ready for the suite in `
- Task N review (lane c) — <deliverable>: <verdict read off the diff>    # required per review-verified task
- Task N no red (lane d) — <why a red phase was impossible>, <confirmed | the plan's reason did not hold: ...>    # required per already-green task
- Task N red at baseline (lane f) — <the listed tests, red before and green after>, <confirmed | the plan's reason did not hold: ...>    # required per red-at-baseline task
- I-<n> — before: "<quoted text at its before-place>"; after: "<quoted text at its after-place>"    # required per invariant on a preserving change to a product with no code
- Rule discrimination (task N) — <rule>: <case> flips red→green when this rule alone lands    # required per task landing more than one rule at one entry point; <rule>: no case discriminates it — <added test_x | why none can exist>

Skills run this session:
- <[x] test-driven-development (tasks <numbers>) | none — no TDD task ran>
```

The builder derives `Role:` from `--actor` and lays down the full trailer block (directional topmost + Role + Surface + Co-Authored-By) in canonical order. **Resolve the `<directional>` once at the start of the session** (before the first task) — with a station open, `Shukuba: <YYYY-MM-DD>_<slug> — progress: <how>` if the commit advances it, `— aside: <why>` if not; with none open, `Agari: <project> — progress: <how>`; never `Shukuba: none`, which doctrine retired — and reuse it across the session's commits, the closing one included. The per-task red/green/refactor commits are ordinary commits you make by hand and carry that same `Shukuba:` trailer per `<CORE>/doctrine/governance/commit_format.md`.

The `Deferred:` and `Failing:` lines are bare lines with no trailing comment, because the chain, `development-code-integrity` and the seal read the whole line and match it by its prefix. Write the `Failing:` lines together, one directly after another with no other line between them. The chain and the commit builder read only the first block of consecutive `Failing:` lines, so a `Failing:` line written apart from the others is not read. `<record>` is the repository-relative path of the record whose owner can make the fix, optionally followed by `§ <section>` — any file on the branch whose owner is not the developer, such as the change's `change_spec.md`, `change_design.md` or `tl_instruction.md`, a product document, a doctrine file or a seed. `<case id>` is the test runner's own id for the case (pytest's node id, for example), and `task <N>` is the task whose `#### Behaviours to verify` names the case or whose code it tests. The chain lands a `Suite: red` marker only when it has at least one `Failing:` line and every one names a task some `Deferred:` line names; any other red halts it as `red-suite`, so a failing case that belongs to no deferred task is still written, honestly.

The `Developer Review Notes` block is the developer's analog of `development-plan`'s `## TL Review Notes`: it tells the architect what changed vs the instruction and why. Examples: `test_<edge_case> added to Task 2 — implied by the responsibility but absent from the behaviours`; `status string → Status enum — closed value set`; `Task 4 implemented before Task 5 — Task 5 imports it`.

#### Exit — read the marker back, then check the trees

**Read the marker back where the chain will look for it, before anything else at exit.** The builder
exiting 0 says the commit landed *somewhere*; it says nothing about which repo, and that is the one
thing this step gets wrong. Run, against the instance worktree path you wrote down at entry:

```bash
git -C "<instance-repo>/.worktrees/<key>" log main..<key> --format=%s
```

The output **must** contain `developer: <key> — implementation complete`. **On a re-close, that is not enough,** because the superseded marker already satisfies it. There, `git -C "<instance-repo>/.worktrees/<key>" log -1 main..<key> --grep='<key> — implementation complete' --format='%H'` must print a SHA other than the superseded marker's. If it does not, the marker
went to the wrong repo — find it (`git -C $PROJECT_ROOT log main..<key> --format=%s`), remake it
through the builder with the instance worktree as `--repo`, and run this read-back again before you
exit. This is the same question, asked of the same repository, that `<CORE>/tools/chain_development.py`
(`DiskReader.marker_commit`) and `tobiishi-seal` § Step 1 each ask — they run it against the instance
repo's primary checkout rather than its worktree, and a linked worktree shares that repo's refs, so
either path answers identically. Both halt on an empty answer, so a read-back that comes up empty here
is the halt they would raise, met while there is still a session able to fix it.

**A halt reads back its report instead of a marker.** A run that halts (§ *When to Stop*) writes `system/projects/<project>/journey/tobiishi/<key>/halt_report.md`, commits it on the instance branch through the builder with the instance worktree as `--repo` (subject `developer: <key> — implementation halted`), and makes no `implementation complete` commit. Read it back with `git -C "<instance-repo>/.worktrees/<key>" log main..<key> --format=%s -- system/projects/<project>/journey/tobiishi/<key>/halt_report.md`: it must print the halt commit, and the branch must hold no `implementation complete` subject. On a re-close, the check is for no `implementation complete` subject newer than the superseded marker: the same `log -1 … --grep='<key> — implementation complete' --format='%H'` must still print the superseded SHA. The superseded marker stays on the branch, so the chain still reads it, and the halt report is the record that says the re-close did not land.

Then run `git -C "<instance-repo>/.worktrees/<key>" status` — and, for an external product, `git -C $PROJECT_ROOT status` too, since its code sits in the product worktree — and verify each working tree is clean. A dirty tree at skill exit is an error.

**No routing.** This skill writes no queue or inbox — the per-role pipeline mailboxes are retired and handoff is folder-derived (`<CORE>/doctrine/flow/folder_state_handoff.md`). It produces code and a `Suite:` verdict with the `Environment:` lines it ran in — green, or red only for cases the marker's `Deferred:` lines own, or none on a card with no suite — or, on a halt, a `halt_report.md`, and returns its step-outcome message (`step_outcome_contract.md`); the chain sequences the next stage from the folder. The front-door inbox item is closed by `tobiishi-seal` at the end of the run, not here.

---

## Bite-Sized Task Granularity

A well-scoped task covers exactly one module or one cohesive responsibility:

- **One file** (`domain.py`) or a **closely coupled pair** (`exceptions.py` + `enums.py` for the same module)
- **Independently testable** — can be implemented, verified, and committed without state from a parallel in-progress task
- **One test file section** — the task's spec tests occupy one named section of a test file

A task is too large when it spans multiple unrelated modules, bundles a feature and an adjacent refactor, or requires two independent sub-features each testable in isolation. Split its implementation into manageable units while retaining the instruction's task number and full responsibility. Save intermediate units per Step 2; only the whole task earns a landing commit.

## Developer Standards

These apply unconditionally — every task, every line, regardless of what `tl_instruction.md` says. The TL defines the scaffold; the developer brings implementation expertise to it. The developer is not a transcriber — they are the last quality gate before the code lands.

**Engineering judgment — improve what is imprecise (Step 1b)**
- Upgrade imprecise constructs encountered during implementation (string with a closed value set → enum) — even if the instruction did not say so.
- Add test behaviours clearly implied by a task's responsibility but not enumerated; cover edge cases the implementation would hit anyway.
- Increase coverage or precision wherever the scaffold is thin.
- **Every improvement is logged in `Developer Review Notes`** (closing commit body) with its reason. Topology stays binding — type-level and coverage improvements are in scope, and so is writing new logic in its owning part (Step 1b); module/package/layer changes are not.

**SOLID**
- **Single Responsibility** — one class, one reason to change
- **Open/Closed** — extend via addition, not modification
- **Liskov Substitution** — subtypes honour the parent contract
- **Interface Segregation** — small, focused interfaces
- **Dependency Inversion** — depend on abstractions; inject dependencies

**Clean code**
- Intent-revealing names — no abbreviations, no generic labels (`manager`, `handler`, `utils`)
- One level of abstraction per function
- No magic numbers or strings — named constants
- Pure functions by default — minimise hidden state and side effects
- Immutable data structures unless mutability is required
- **`__init__.py` is for package initialization and public re-exports only — never implementation.** Entities, services, repositories, CLI logic live in named modules (`domain/models.py`, `domain/exceptions.py`, `persistence/json_repository.py`, …); `__init__.py` re-exports the public interface the module set specifies. This holds **even when the instruction lists `<package>/__init__.py ← modified` as the target or sanctions keeping code there** — treat it as an imprecise layout (Step 1b): create the named modules, re-export, log it in Developer Review Notes. Splitting a package's internal files is layout, not topology — the package boundary (`nfdr.md § 1.2`) stays binding, so it is squarely within the developer's improvement latitude. **The one exception is a package's composition edge** — an `__init__.py` whose whole content wires that package's own named modules and holds no domain logic. Where the design mandates that shape, build it and log the choice as the exception it is (`<CORE>/doctrine/engineering/languages/developer_standards.md`, which owns both halves).

**Design patterns**
- Apply when the problem shape matches — do not force a pattern
- A forced pattern is worse than no pattern

**Always**
- DRY — no duplicated logic
- YAGNI — implement what is needed now
- Every public interface has an explicit contract (types, signatures, documented invariants)
- Every commit leaves the codebase cleaner than it found it

## When to Stop

Task-level repair and deferral are governed by Step 2 § *Work and repair* and § *Deferring a task*.

**The run halts in exactly three cases**, and only these:

1. **No task could land.** Each deferral must satisfy § *Deferring a task*'s (a write into another repository defers as its own § says) recovery and evidence requirement; an all-deferred batch does not waive it. That includes a stop before any task starts — a failed startup gate, a missing `tl_instruction.md`, an execution context or `<name>` that cannot be resolved, a Step 1 concern that blocks every task — and a run in which every task ended deferred.
2. **The preserving lane's baseline is red beyond what the task names** — a red test the `#### Invariant gate` does not list on a `Red at baseline:` line, or a listed test already green. On a product with no code: an invariant not stated at its before-place.
3. **A reclassification event** — a previously-green test goes red during a `Behaviour: preserving` relocation, or on a product with no code an invariant is not stated at its after-place, or is stated twice. The move disturbed an internal path, and the "preserving" classification was wrong. Never edit a test to make it pass.

**A halt writes `halt_report.md`** into the change folder on the branch, commits it through the builder, and makes no `implementation complete` commit (§ *Exit*). The context cap's pause is not a halt.

**Document the blocker clearly in the session output, and do not guess.**

## Remember

- Review `tl_instruction.md` critically before starting
- Source execution type + test command from `system/projects/<project>/project.md`, never from the instruction
- Don't skip verifications
- Invoke skills at the exact moment they fire — not as a preamble
- Apply Step 2 § *Work and repair* and § *Deferring a task*; run-level halts are owned by § *When to Stop*.
- Always work in the correct directory: for headless runs derive `$WORKTREE` from the change key and `cd` in (development-specs created the worktree — never create it here), `/workdir` for Docker — never on main. The Step 1 enter + startup gate enforces this per execution type; do not start tasks until it passes

## Integration

**Input from:**
- `development-plan` — produces the `tl_instruction.md` this skill executes
- `development-design` — produces `change_design.md`; see Inputs
- `development-specs` — produces `change_spec.md`; see Inputs

**Skills invoked during execution:**
- `test-driven-development` — Step 2, full TDD cycle per task (owns red/green/refactor commits)
- `source-driven-development` — Step 2, inside the TDD cycle when touching unfamiliar libraries or APIs
- `debugging-and-error-recovery` — Step 2, if tests or verifications fail unexpectedly

## Critical Rules

- **Task completion and external impediments:** Step 2 § *Work and repair*, § *A landing commit* and § *Deferring a task*. Run-level halts: § *When to Stop*.
- **The context cap's notice is a pause, taken at a task boundary.** Follow Step 2 § *Pausing at the context cap*. Step 2's batch rule also owns how a relaunch checks prior progress; Step 3 owns carrying the pause records into the closing marker.
- **A run sent to Step 3 always makes a closing commit, even over an existing one.** A branch that already carries `implementation complete` is closed again. The run makes one test-command run and a new marker, and the old marker is never amended (Step 3 § *A re-close makes a new marker*). The chain, the seal and code-integrity all read the newest marker. A run that stops at the old one leaves the walk halted on a verdict that no longer holds.
- **Never bundle tasks.** Each task gets its own TDD cycle and commit sequence. A single commit spanning multiple tasks (e.g. `tasks 6-14`) is always a violation.
- **The suite verdict is declared every run: red, green, or none on a card with no suite.** Step 3, and the `Suite:` line is unconditional — `Suite: red` is written exactly as `Suite: green` is, never left off the marker. It states the test command's exit state when the closing commit is made, and `<CORE>/tools/chain_development.py` gates the walk on it: a `Suite: red` marker halts `red-suite` unless it carries at least one `Failing:` line and every `Failing:` line names a task one of its `Deferred:` lines names, a `Suite: none` marker passes only when the card on `main` reads `Test command: none` and otherwise halts `missing-suite`, and a line declaring anything other than exactly `green`, `red` or `none`, or no line at all, halts `missing-suite`. An omitted line is not a quieter green — it is the one answer that cannot be told apart from a run that never ran its suite. **The `Environment:` lines beside it are declared every run too:** every `Environment:` line the closing run's gate-tool call printed, each copied whole, and `none — no suite` on a card with no suite. The chain halts `missing-environment` on a marker with no such line, or with any one that names no real kind or is `unresolved`, after every reason above it, so a refused run cannot be recorded as a green one. The chain halts `environment-not-ready`, ahead of `red-suite`, on a marker with any `Environment:` line whose first word is `not-ready`.
- **The language packet is resolved every run, and the resolution is recorded whether or not it found anything.** Step 1 sub-step 3, and the `Language resolution:` block is unconditional — written on a run that opened a packet and on a run that fell to the floor alike. This replaces the `optional context` input row retired 2026-08-21, under which this skill required no language record at all. **A packet that exists binds over the surrounding file's own style** — where they disagree the packet wins and the divergence from the file is recorded, because deferring to local style makes the packet unfalsifiable. **And what the block says about the packet is quoted, not summarised, and complete against the packet's own list** — the concern file, its line, and the clause verbatim, beside what the code does about it; and every concern the router lists is accounted for — by such a clause or a bore-on-nothing line — an owner outside the packet included — or, for a concern routed to the floor, a floor line, as Step 1 sub-step 3 sets out — rather than only the ones the run chose to open. A summary reads as obedience whether or not the code obeyed, which is how a seventeen-module departure from a clause landed recorded as compliance. **The verdict is decided by the quoted words, and the evidence is the code this change wrote.** An exception is available only where it can be quoted from the same clause; a clause carrying none leaves `diverged:` as the only honest verdict, whatever the surrounding rules appear to allow. And where this change wrote code bearing on the clause, that is the site the line names — a pre-existing site is evidence only when the change wrote nothing that bears on the clause, and then the line says so. Both failures survive a correct citation and a correct quote, which is why the rule above does not reach them: on 2026-09-09 one line claimed an exception its clause does not carry, and another discharged a clause against the one file the change did not touch.
- **Never merge phases.** `developer: task N <slug> — red/green` is always a violation. Red (failing tests, no implementation) and green (passing implementation) are separate commits, in that order. **A task whose tests cannot go red was never in the red/green lane** (Step 2, lane d), so there is no phase to merge and this rule does not reach it — the missing red is stated in `Developer Review Notes`, never manufactured by breaking the subject. **Nor was a task whose failing tests are already on `main`** (Step 2, lane f): its red phase is the run that watches them fail, and the note records it.
- **A red phase proves the task; each rule inside it is proved one at a time.** *Did it go red* is not *red because of which rule*, and a task landing several separately-removable rules behind one entry point answers only the first. Land them one at a time and record, per rule, the case that flips red→green with it (Step 2, lane e; the `Rule discrimination` entries of `Developer Review Notes`). **A rule whose landing flips no case is unfalsifiable in this task** — add the discriminating case, or state that none can exist and why. Never read the phase's overall redness as proof of any single rule inside it: three rules of one change unit were deletable with the whole suite green, each of them red before its task and green after, each caught only by mutation in the next step.
- **A review-verified task is one plain commit, and its review is recorded.** When the task carries `#### Deliverables verified by review` and `#### Implement` reads `Verified by review — no test.`, build it, check each stated criterion by reading the diff, and commit a single `developer: task N <slug>`. No red phase is invented — no test asserts the deliverable. **The per-deliverable verdicts go in `Developer Review Notes` unconditionally**, because a review that leaves no trace is indistinguishable from one that did not happen. Before this lane existed, three tasks of one change unit invented the subsection `**Deliverables verified by review of the diff, not by a test**`, routed to the TDD lane with zero behaviours, and the developer improvised a red phase for a manifest edit.
- **An already-green task is one plain commit, and the missing red is stated.** When `#### Implement` reads `Tests cannot go red.` with a `Reason:` line, write the behaviours as tests, watch them pass first time, and commit a single `developer: task N <slug>`. Never break the subject to manufacture a red. **A `Developer Review Note` naming why the red was impossible is required**, and it is required equally when the plan did not predict the lane and you discovered it at the red phase — in which case log the re-lane too. Two tasks of one change unit landed twelve tests that were never observed failing, with the lane choice recorded nowhere; the note is what makes the absence of a red a result rather than a silence.
- **A red-at-baseline task is one plain commit, and its red is watched, not committed.** When `#### Implement` reads `Tests are red at baseline.` with a `Reason:` line, the `Red at baseline:` tests already fail on `main` — an earlier change unit committed them and deferred the task that passes them. Run them and see each fail before touching the subject, build until they pass, and commit a single `developer: task N <slug>`. **A `Developer Review Note` naming the tests, red before and green after, is required**, and so is the re-lane note when a TDD-lane task turns out to be this shape at its red phase. Never commit a copy of the failing tests to manufacture a red: on 2026-10-04 a finished, green change halted at the chain's commit-shape check because its plan had no shape for this case and the developer had no red commit it could honestly make.
- **A no-test structural task is one plain commit.** When `#### Implement` reads `No spec tests — implement per project layout above.` (a package skeleton, `__init__.py` set, Protocol definition, `pyproject.toml`, README), build to the layout, satisfy the `#### Verification gate`, and commit a single `developer: task N <slug>`. This is not a merged red/green phase — the task has no tests, so it was never in the red/green lane. tracker5 precedent: `developer: setup tasktracker5 package structure`, `developer: task-4 ports protocols` — the slug carries no ` — `, since § *A landing commit* reads what follows one.
- **Consume the classification — never re-derive it.** The change's `Category` + `Behaviour` are decided upstream (development-specs stamps, development-design and development-plan propagate verbatim). The developer is a *consumer*, never a classifier: the task's gate shape — `#### Invariant gate` → preserving relocation lane; `#### Deliverables verified by review` → review-verified lane; `#### Behaviours to verify` or no gate subsection → already-green / red-at-baseline / TDD / no-test lanes, split by the `#### Implement` marker — is the authoritative classification signal and is followed as-is. Never infer, default, or override `Behaviour`. If a task's lane signal is absent or contradictory (both gate types present, or neither where one is required), resolve it through Step 1b and § *Deferring a task* — do not guess a lane. (Defense-in-depth parity with development-design / development-plan's copy-not-classify header rule.)
- **Two-axis classification (`Behaviour: preserving`).** Every change carries `Category` + `Behaviour` (`<CORE>/doctrine/flow/change_classification.md`). A `Behaviour: preserving` task swaps the task shape only — it carries `#### Invariant gate` (in place of `#### Behaviours to verify`) and a `No new tests — TDD under green` body. Execute it as one atomic **green→green relocation** (baseline green, or red on exactly the gate's `Red at baseline:` tests → move per the §3 Layout Plan → green), committed as **one** plain `developer: task N <slug>` commit — never a red/green pair, never a manufactured red. Tests mirror the relocated production **only where they reference a relocated path** (`<CORE>/doctrine/engineering/testing_doctrine.md`). Altitude fences: the §3 Layout Plan is binding (do not re-open module boundaries — development-design's decision); this skill executes the move as planned. Do not fork this skill — the axis selects the lane (Step 2, step 2a).
- **A red existing test during preserving is a reclassification halt.** If a previously-green test goes red while executing a `Behaviour: preserving` relocation, the "preserving" classification was wrong (the move reached an internal path a test depends on). Halt and surface — never edit the test to make it pass, and never debug-and-patch your way to green. This is the developer-side enforcement of the Invariant gate development-plan writes.
- **The instruction carries no commit choreography.** Per-task commits come from `test-driven-development`; the closing commit is owned by this skill. Do not look for `## Commit 1/2/N` sections in the instruction — development-plan does not write them. **On a TDD-lane task (lane e), a commit instruction the plan wrote anyway is not one you follow.** A task the plan says lands as *one commit* or *a single commit* still lands as a red commit and then a green one — a red commit is not a green point, and the chain halts a TDD-lane task with no red commit (`missing-red-commit`). Log the instruction you set aside in `Developer Review Notes` as a divergence.
- **Two roots — qualify every path, both resolved from `$WORKTREE`.** Pipeline-side artifacts (`system/...`) are bare from the CWD (= `$WORKTREE`); project-side artifacts (`docs/adr/`, code, tests) are under `<name>/` = `$PROJECT_ROOT` = `$(dirname "$PROJECT_DOCS")`, where `PROJECT_DOCS` is resolved from `project.md` `Product path:` — the same resolution development-design and development-plan use, never a separate repo or an invocation-context path. If `<name>` cannot be derived, halt, and in an interactive session ask.
- **Code commits target the product's repo, pipeline commits target the instance (the path tool).** Ask `<CORE>/tools/development_path.py resolve` at entry (§ *Where each commit goes*): code → its `code_worktree`, pipeline → its `pipeline_worktree`. The contract is one line: **code → `git -C $PROJECT_ROOT`; pipeline → `git -C $WORKTREE`.** For a relative product they are the same repo (today's behavior, untouched); for an external product `$PROJECT_ROOT` is inside the product worktree (a separate repo) — do the per-task TDD work there so its commits land on the product branch, keep the closing commit on the instance branch. Never commit code from `$WORKTREE` when the product is external — a different repo would not capture it. **And the closing marker is a pipeline commit**, so the run's last `--repo` changes back to the instance worktree after a whole session of product-worktree commits — the one place this contract is actually dropped. The run proves it did not drop it by reading the marker back (`git -C <instance worktree> log main..<key>`) before it exits, per Step 3 § Exit.
- **A write into another repository is plain calls, run as the instruction gives them.** One call per command, every path a literal (the other repository absolute, `--add` relative to `--repo`), no script, variable, chain or check folded in. A commit the harness refuses undoes the copy before the task defers. A commit the builder or the other repository's hook refuses defers without an undo or a re-run (Step 2 § *A write into another repository*).
- **Execution context comes from `system/projects/<project>/project.md`, not the instruction.**
- **The developer critically reviews and improves the instruction — not transcribes it.** The commands for a write into another repository are the exception: they run unchanged (Step 2 § *A write into another repository*). Step 1b is mandatory. Topology is binding; type-level and coverage improvements are in scope, and so is writing new logic in its owning part. **Record every divergence** in `Developer Review Notes` with its reason — improvements **and** the three discriminators (resolving a contradiction between `tl_instruction.md` and `change_design.md`, locking an observable behaviour the instruction left implicit, overriding an upstream recommendation). This is the developer-stage analog of development-plan's `## TL Review Notes`; silent divergence is the failure mode. **And the pass itself leaves a record on every run** — the `Step 1b review:` block, never omitted, carrying the edges derived from each task's stated responsibility and where each landed. A run that added nothing has something to say there; a run that never made the pass has nothing, and until this block existed the two were the same commit.
- **Resolve the implementation contract** from the instruction, design and specification per Step 1b.
- **New logic is written in the part that owns it.** Where the instruction puts it elsewhere, the developer writes it in the owning part and logs the correction (Step 1b). Each task's placement line in the `Step 1b review:` block is written on every run.
- **No routing.** Handoff is folder-derived — the pipeline inboxes are retired; this skill returns its step-outcome message and the chain sequences the next stage from the folder, not this skill.
- Do not skip verification commands.

## Error Handling

| Error | Likely Cause | Action |
|-------|-------------|--------|
| `tl_instruction.md` not found | Path incorrect or file not committed | Halt — document the expected path (no task could land) |
| Execution context unresolvable — `system/projects/<project>/project.md` carries no Execution type + Test command | The card is the only source | Halt — document the missing source (no task could land) |
| `<name>` (project root) not derivable | `PROJECT_DOCS` unresolved (the `project.md` resolution yields nothing) and no `## Project layout` top dir | Halt — in an interactive session ask for the project root; do not guess |
| Startup gate fails — wrong branch / not in the change worktree (headless: branch ≠ `<key>` or toplevel is the primary checkout; Docker: `pwd` ≠ `/workdir` or branch mismatch) | The worktree is absent (upstream stages did not run) or the enter (`cd "$WORKTREE"`) was skipped; for Docker, the launcher mounted the wrong branch | Halt — do not write code; surface that the session must run inside `.worktrees/<key>` on branch `<key>` |
| A TDD-lane task's red phase does not go red — the tests pass the moment they are written | The subject already satisfies the behaviours; the plan ordered the task in the wrong lane | **Not a halt or a deferral** — finish in the already-green lane (Step 2, lane d): one plain commit, and log both the re-lane and why the red was impossible in `Developer Review Notes`. Never edit the subject to manufacture a red |
| A TDD-lane task's red phase asks for tests that already exist and already fail at the change's base | An earlier change unit committed them to `main` and deferred the task that passes them; the plan ordered the task in the wrong lane | **Not a halt or a deferral** — finish in the red-at-baseline lane (Step 2, lane f): watch the tests fail, build, one plain commit, and log the re-lane and the tests that went green in `Developer Review Notes`. Never commit a copy of them to manufacture a red |
| Step 3's earlier-marker read prints a SHA, meaning an `implementation complete` commit is already on the branch | Implementation was entered again with an inherited marker | **Not a reason to stop.** Run the test command, and make a new marker that carries the superseded record forward. Read it back against the superseded SHA (Step 3 § *A re-close makes a new marker*, § *Exit*) |
| The context cap's notice arrives mid-run | The chain set a cap and the session's current context passed it | **Not a halt** — finish the task in progress, make the pause commit, read it back and end (Step 2 § *Pausing at the context cap*). The chain relaunches the rest |
| Ambiguous task description | Step underspecified | Resolve from the design, specification and relevant cited sources per Step 1b; defer only the ambiguity that remains unresolved |
| Task uses what a deferred task would have made | A task it uses the output of failed or was deferred (§ *Deferring a task*, Dependents) | Defer this task too: `Deferred: task <N> — depends on task <M> — <record>`; commit nothing for it |
| Verification command fails | Tests, checks or execution environment failing | Return to § *Work and repair* |
| Previously-green test goes red during a `Behaviour: preserving` relocation | The move disturbed an internal path a test depends on — "preserving" was misclassified | Halt — surface as a reclassification event; do **not** edit the test or invoke `debugging-and-error-recovery` to patch it green |
| Blocker mid-execution | Unexpected state, conflicting files, missing context | Apply § *Work and repair*, then § *Deferring a task* if an external impediment remains |
