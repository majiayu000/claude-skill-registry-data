---
name: component-verify
description: One-command, repeatable formal-verification pipeline for a single Certus component — new or already-verified. Pulls a fresh tree off origin/unstable, extracts the tool-independent property inventory (Role 1), proves it with Creusot AND Kani (Role 2), renders one combined scoring HTML (Role 3), then commits to two per-component verif branches (overwrite-in-place, component-folder-only gate) — each branch carrying the FULL metadata bundle (spec_properties + code_properties + unified_properties YAML AND the combined scoring HTML) plus that one tool's proof artifacts (Kani harnesses / Creusot verif crate). No PR and nothing to unstable; the two verif branches are the only homes. Use this as the top-level entry point so Cornel, Daniel, or a colleague can verify a component independently and reproducibly.
argument-hint: "<component> [--tools creusot,kani] [--no-push] [--dry-run]"
---

## Purpose
Turn per-component formal verification from a hand-stitched sequence (five skills + manual git + hand-curated HTML + scp-to-Box) into **one orchestrated, reproducible run**. Any team member invokes this on a component name and gets: the property inventory, Creusot + Kani proofs, one combined scoring page, and two per-component verif branches that EACH hold the full metadata bundle (all three YAML + the combined HTML) plus that tool's proof artifacts — with the safety rails that stopped last week's wasted effort on unclean trees.

This skill **orchestrates**; it does not re-implement the roles. It calls, in order:
- **Role 1** `build-property-inventory` — the single source of truth, three YAML: `spec_properties.yaml` + `code_properties.yaml` + `unified_properties.yaml` (no `.md`).
- **Role 2** `tools-verify-creusot-with-properties` **and** `tools-verify-kani-with-properties` — prove/harness every property; write per-property status/evidence/fidelity back into `unified_properties.yaml`.
- **Role 3** `tools-aggregate-coverage-by-interface` — render the one combined `<component>_scoring.html` from `unified_properties.yaml`.

It then owns **all git**: the **two per-component verif branches are the only outputs** — each gets the full metadata bundle (all three YAML + the combined HTML) plus that tool's proof artifacts. There is **no PR and nothing goes to `unstable`.** The sub-skills produce artifacts in the working tree only; they never commit or push under this orchestrator.

## Arguments
- `<component>` — the component name (e.g. `dispatch-map`), matching `components/<component>/`.
- `--tools creusot,kani` — which provers to run (default both). Loom/Spin can be added one-at-a-time later; the renderer is N-tool-ready.
- `--no-push` — do everything locally (both branches + commits) but do not push. Use for the first supervised run.
- `--dry-run` — run Roles 1–3 and the contamination gate, print what *would* be committed/pushed, but make no branch, commit, or push. Safe rehearsal on an already-verified component.

Auto-detect **new vs. already-verified**: a component is "already-verified" iff `verif/creusot/<component>` or `verif/kani/<component>` exists on the remote. Either way the run is the same: proofs are **recreated from scratch** off fresh `origin/unstable` and the branch is **overwritten in place** with the new commit — no tag, no merge, no baseline-preservation ceremony (git history keeps the prior commit automatically).

## Step 0 — Preconditions (HARD; refuse to proceed if any fail)
These rails exist because most of last week was lost to unclean/stale trees. They are enforced, not advised.

1. **Clean tree.** If the current working tree has uncommitted changes to tracked files, **stop** — print `git status --porcelain` and refuse. The operator commits/stashes first.
2. **Fresh base.** `git fetch origin`. Create a **fresh worktree off `origin/unstable`** for this run (do not reuse an old checkout). Every role runs inside this fresh worktree. Record the resolved `origin/unstable` commit as the run **pin** — it stamps every YAML and the HTML.
3. **Prover doctor (Creusot runs only).** Confirm the SMT portfolio is registered: `why3 config list-provers` must show **Alt-Ergo, Z3, CVC5, CVC4**. If any are missing, ensure `~/.local/share/creusot/bin` is on `PATH` and run `why3 config detect` (this writes absolute prover paths into `why3.conf`). Re-check; if still short, **stop** and report which prover is unavailable — do not run Creusot against a degraded portfolio and mis-attribute the misses to a tool boundary.
4. **Component exists.** `components/<component>/` must exist, and so must its interface — but the interface is **not** in the component's own directory and is **macro-generated**, so do not grep for `trait I<component>`: that text appears nowhere in the repo and every component would falsely fail this gate. Look in **`components/interfaces/src/i<component>.rs`** for the block
   ```
   component_macros::define_interface! {
       pub I<Component> {   // often under #[cfg(feature = "spdk")]
   ```
   and take the `fn` names declared inside that block as the public-method surface **`N`** (the scoreboard denominator). Example: `idispatch_map.rs` declares `pub IDispatchMap { … }` with `N = 20`.

   The filename is **not always** a literal transform of the component name (`block-device-filesys` is served by `iblock_device.rs`), and a component may implement an interface whose method count differs from its scoreboard denominator — so resolve the interface from the component's own `use interfaces::{…}` import and its `impl I<X> for …`, then confirm the `define_interface!` block. All 16 interface files in the repo follow this pattern; if you cannot locate the block for this component, stop rather than guess.

5. **Write the run-local excludes (do this; do not rely on the repo's `.gitignore`).** Append to the
   worktree's `$(git rev-parse --git-path info/exclude)`:
   ```
   components/*/creusot                       # machine-specific creusot-std symlink
   components/*/verif/*_advisory.yaml         # Step 4 forbids committing these
   components/*/verif/.run/                   # stage logs
   components/*/verif-creusot/target/
   components/*/verif-creusot/_creusot_erasure/
   components/*/verif-creusot/.why3find/
   components/*/verif-kani/target/
   ```
   Two reasons this is a pipeline step rather than operator lore. First, the repo `.gitignore` covers
   only `tools/creusot/creusot`, **not** the per-component `components/<c>/creusot` symlink — a
   machine-specific absolute path that the `git add -A components/<c>/` in Step 4 would happily commit.
   The published branches are clean only because staging happened to be selective: luck, not a rail.
   Second, `info/exclude` is run-local and uncommitted, so it can never become a *committed* ignore
   rule that hides proof artifacts from a future commit — which is exactly how an agent-created
   `.gitignore` nearly shipped a proof-free branch (see Step 4's artifact-presence gate). Never use a
   committed `.gitignore` inside `components/<component>/` for this.

Print a one-line precondition summary (`clean ✓ | base <pin> | provers alt-ergo/z3/cvc5/cvc4 ✓ | component ✓`) before continuing.

## Step 1 — Role 1: property inventory + YAML
Run `build-property-inventory <component>` inside the fresh worktree. It performs the two BLIND extractions (spec, code) and reconciles them. Confirm it produced, under `components/<component>/verif/` (**three YAML, no `.md`**):
- `spec_properties.yaml`, `code_properties.yaml` — the two blind extractions in shareable YAML (the two blind denominators `spec_total`, `code_total`).
- `unified_properties.yaml` — the reconciled single source of truth (denominator `unified` M) with **empty per-tool status blocks** (schema below).

If `unified_properties.yaml` did not materialize, stop — Role 2 has nothing to consume.

## Step 2 — Role 2: PRODUCE proof artifacts (the agent does not grade itself)
Run the two Role-2 skills. They are independent, so **launch them in parallel** as two subagents (one per tool) **inside the ONE shared fresh worktree** — they write disjoint artifact trees (Kani → `#[cfg(kani)]` harnesses under `src/`; Creusot → the `verif/` crate + `.coma`), so their files never collide and **there is no merge step across trees**. Neither subagent writes `unified_properties.yaml` directly (concurrent writes would race); each writes its advisory fields to a per-tool side-file `verif/<tool>_advisory.yaml`, and the **orchestrator is the single writer** that folds those into `unified_properties.yaml` before the gate. The critical rule of the strong gate: **a Role-2 subagent produces artifacts; it never writes its own `status`.** Status is derived by the gate scorer in Step 2.5, which *executes* the artifacts. Each subagent:
- consumes the inventory by `id` (never re-extracts),
- attempts **every** property it can express (no lane pre-filtering — coverage discipline is in the sub-skills),
- produces, **per property `id`, a runnable proof artifact** the scorer can find by the naming convention (Kani: a `#[kani::proof] fn verify_<id>`; Creusot: a proof module `verify_<id>` → `verif/<crate>_rlib/verify_<id>.coma`) — or points the scorer at an existing artifact via `kani.evidence.harness` / `creusot.evidence.module(s)`,
- **for any property it cannot prove on the first attempt, produces the lever-battery variant artifacts** the battery requires for the observed failure class (Kani `verify_<id>__nounwindcheck|__concrete|__split_*|__stub`; Creusot `verify_<id>__fmap|__trusted|__inv`, `lemma_<id>`) — the scorer will run each; a missing required variant scores UNRESOLVED, never tool-boundary,
- builds a `verify_<id>__mutant` anti-vacuity twin wherever the property could be vacuously true (the scorer requires it to FAIL),
- may emit only the *advisory* fields the scorer does not own — `fidelity`, a human `note`, and, for a genuine delegation, a **resolvable referent** (`delegate_to:` a named component + concrete obligation) — into its per-tool side-file `verif/<tool>_advisory.yaml`, keyed by property `id`. It must **not** write `status`, `symbol`, or `evidence`, and must **not** touch `unified_properties.yaml` directly (the orchestrator folds in the side-file; the scorer overwrites status/evidence and stamps `_scored_by`).

Heavy runs: the **binding** per-property time budget is enforced downstream by the scorer in Step 2.5 (adaptive cap `--cap-seconds` → `--cap-max`, with a whole-process-tree kill on breach), so a hung solver can never stall the run — the subagents here need only self-limit their exploration and must not busy-wait on a wedged prover. Because both run in the one shared worktree and touch only disjoint artifact trees + their own advisory side-file, there is nothing to merge across trees.

**Step 2 environment post-check (new rail, ~1s, do not skip).** Role 2 can break the component's
build for the *other* tool. Measured on eviction-policy-session-lists: the Creusot agent wrote
`[patch.crates-io]` into `components/<component>/.cargo/config.toml`, and because a cargo **config**
at component scope applies to every cargo invocation whose cwd is inside the component, the Kani
scorer's own preflight would have aborted the entire Kani gate before scoring one property. So after
Role 2 returns, run **one full `cargo metadata` with cwd = `components/<component>/`** — deliberately
NOT `--no-deps`, which returns 0 on exactly this fault while full resolution fails. If it fails, stop
and report it as an environment fault; do not run the scorers and do not blame the harnesses.

**Step 2 hard-stop (do not skip):** when both subagents return, count the proof artifacts actually present in the worktree for each requested tool (Kani `#[kani::proof]` fns; Creusot `verify_*` modules / `.coma`). If a requested tool produced **zero** artifacts, **stop** — do **not** run the scorer, do **not** write `unified_properties.yaml`, do **not** create any branch — and report the empty tool. This is precisely the failure that produced last night's all-pending dispatch-map YAML: the pipeline ran to the end over an empty tree instead of failing loudly.

**Do not launch Step 2 unsupervised as part of a first bring-up unless the operator asked for a full run.** Under `--dry-run` you may skip re-proving if branches already carry a verified run; instead run the scorer in `--dry-run` (artifact/battery/registry checks only) and note "status carried forward, not re-verified this run."

## Step 2.5 — GATE: run the shipped scorer (NON-SKIPPABLE; this is the enforcement)
First, as the single writer, fold each `verif/<tool>_advisory.yaml` into the matching `creusot:`/`kani:` blocks of `unified_properties.yaml` (advisory fields only — `fidelity`, `note`, `delegate_to`, the `evidence` artifact pointer). Then run the gate: the scorer — not the agent, not this orchestrator's prose — decides every property's status by **reproducing** it. Run each scorer **through the shipped stage-runner `gate/run_stage.py`**, from the gate dir shipped with this skill (`.claude/skills/component-verify/gate/`):
```
python3 gate/run_stage.py --name kani-scorer    --log components/<component>/verif/.run/kani.log    --watchdog <W> -- \
    python3 gate/scorer_kani.py    components/<component>/verif  --component-dir components/<component>/verif-kani     --cap-seconds 60 --cap-max 300 --resume
python3 gate/run_stage.py --name creusot-scorer --log components/<component>/verif/.run/creusot.log --watchdog <W> -- \
    python3 gate/scorer_creusot.py components/<component>/verif  --crate-dir     components/<component>/verif-creusot  --cap-seconds 60 --cap-max 300 --resume
```
**Run the gate from the SKILLS checkout, not from the run worktree's copy.** The fresh worktree
Step 0 creates contains its own `.claude/skills/component-verify/gate/`, frozen at whatever commit the
worktree was made from — so invoking `gate/…` relative to the worktree silently runs a STALE gate.
Measured: a run worktree cut at an earlier commit still carried a gate without the lemma-crediting fix,
and a reviewer inspecting it concluded the fix was missing. Invoke the scorers by absolute path from the
skills-branch checkout (the same tree this SKILL.md lives in), and sanity-check the `run:` block
afterwards — `gate_commit` records which gate actually scored, so a stale one is visible in the
deliverable rather than silent.

**Get these three directories right — two of them are NOT `verif/`.** The metadata bundle (the YAML the scorers read and write) lives in **`verif/`**, but each tool's *proof artifacts* live in its **own sibling crate**: Kani harnesses in **`verif-kani/`**, the Creusot proof crate in **`verif-creusot/`**. Pointing a scorer at `verif/` instead of its tool crate is a silent, expensive mistake: the scorer still *finds* harness/module names (it searches recursively) and then runs `cargo` in a directory where they are not part of the crate, so every property fails with `no harnesses matched the harness filter` or `no generated proof module(s)` and the gate reports mass UNRESOLVED that says nothing about the proofs. This has now been mis-invoked once per tool during bring-up; copy the paths above rather than retyping them.
The stage-runner exists so this run is **safe to leave unattended and legible to a colleague afterwards**: it prints `SENTINEL: <stage> START/DONE exit=<n>` (a `Monitor` or a human sees exactly when each stage begins and ends and with what code), **tees the full transcript** to `verif/.run/<stage>.log` for audit, drops a `verif/.run/<stage>.done` completion marker, and enforces a **watchdog** wall budget that SIGKILLs the whole process tree (cbmc/why3/solvers included) if the scorer itself wedges. Set the watchdog `<W>` to `max(1800, harness_count × 300 × 1.5)` seconds (the per-property caps below are the fine-grained control; the watchdog is the coarse backstop). The two scorer flags do the per-property work:
- **Adaptive cap** (`--cap-seconds 60 --cap-max 300`): a property runs at the 60 s base; only if it *times out* (not a real failure) is it retried once at 300 s before the scorer may class it a sat-timeout/goal-unproved boundary — so a merely-slow proof is never mislabelled a tool-boundary, and a fast failure is still decided in seconds. On timeout the scorer tree-kills that run's own systemd scope by cgroup (no orphaned solvers).
- **Resume** (`--resume`): the scorer checkpoints `unified_properties.yaml` atomically after **each** scored property and, on a re-run, skips any property already carrying a scorer-owned ACCEPT status. An interrupted or watchdog-killed run resumes where it stopped instead of re-proving everything.

Each scorer executes each property's artifact, captures wall-clock + peak RSS **from the run**, and writes the scorer-owned `status`/`evidence`/`note`/`_scored_by` back into `unified_properties.yaml`. On a real (non-dry) run it also stamps a **`run:` provenance block** — the gate's own commit/branch (and `gate_dirty: true` if the gate had uncommitted edits), the exact scorer command, and the tool versions (`cargo-kani …`; the Creusot checkout's `git describe`, why3, and the prover portfolio). Each scorer owns only `run.<tool>`, so the two never clobber each other. Because that block rides on `unified_properties.yaml`, it travels onto **both** verif branches and renders into the HTML's provenance footer — so a result always says which gate and which command produced it. Do not hand-write or edit it. It assigns exactly one of a closed set and **exits non-zero if any verifiable property is UNRESOLVED**:
- `proved` — the scorer re-ran the artifact (base, a scorer-applied lever escalation, or an agent-supplied lever variant) and it verified; anti-vacuity mutant, if present, went red.
- `tool-boundary` — the scorer ran the **full lever battery** for the observed failure class and each still failed, and the residual signature is **not** in `known_defeats.yaml`. The signature is captured from the run.
- `refuted` — **the obligation is FALSE and that was machine-checked: the code violates it.** A found defect is the return on the verification effort, so this is an ACCEPTED terminal rating, not a gate failure — the run records it and moves on. It is earned only by a `refute_<id>` artifact that the scorer runs and that *succeeds*: in Creusot a module stating the NEGATION which **proves**; in Kani a harness demonstrating the violation is **reachable**. A merely-failing `verify_<id>` is never a refutation — it could equally be a bad bound, a wrong harness or a solver limit. If the property AND its refutation both pass, that is a `CONTRADICTION` → UNRESOLVED, because one of them is vacuous and a defect claim on that footing would not be trustworthy. Rendered as `‼` in the scorecard, in the KPI headline, and in its own **“Defects found”** section carrying the spec place and the code lines a reader needs to act on it.
- `delegated` — a resolvable referent (named component + obligation) exists.
- `UNRESOLVED` — everything else: no artifact, a claimed pass the scorer could not reproduce, a missing required lever variant, a signature matching a known defeat, a broken/translate-error harness, or an unclassifiable failure.

**Hard gate:** if either scorer exits non-zero, the run is **not done**. Do **not** proceed to commit either branch. Feed the printed UNRESOLVED list back to the Role-2 subagent as its next work-list (produce the missing artifact / the demanded lever variant / fix the broken harness) and re-run the scorer (with `--resume`, so it only re-attempts the outstanding ids). The scorer's `.coma`/harness regeneration is from source (Creusot `touch`es `src/**.rs`; Kani rebuilds), so a hand-edited artifact cannot fake a pass.

**Bounded iterate (7th rail — do NOT loop forever).** Cap this UNRESOLVED → re-attempt cycle at **3 iterations**. If both scorers have not reached exit 0 after the 3rd, **stop and PAUSE** — do not commit, do not push, do not start a 4th round. Print `COMPONENT-VERIFY: PAUSED(iterate-cap)` followed by the still-outstanding property `id`s and their last UNRESOLVED notes, so the operator (or a colleague) picks up a bounded, legible work-list instead of an agent spinning on the same wall. A paused run is resumable: its per-property progress is already checkpointed in `unified_properties.yaml`, so a later supervised re-run with `--resume` continues from the outstanding ids only. Pausing is a first-class outcome, not a failure to hide.

## Re-scoring an ALREADY-PUBLISHED component — change exactly ONE variable (mandatory protocol)

Re-scoring is how correctness debt on public results gets paid: a gate defect is fixed, and the
already-published cells that bypassed the fixed check are re-derived. It is **not** the same activity
as scoring a fresh component, and it has its own failure mode — **a parameter difference that mimics
the very finding you are testing for.**

Measured on 2026-09-28, re-scoring `eviction-policy-optimized` to recheck 58 `bounded-shallow`
proofs. Two separate misconfigurations EACH produced a large drop in `proved` that had nothing to do
with the fix, and each would have supported the false headline "the proofs collapsed under the new
check":

1. **`--wall-budget` left at its default 3.** After 3 properties fail escalation with the same
   timeout signature, later ones skip escalation. But the known-defeat registry matches against the
   LAST output, so with no 300s escalation the signature never matched
   `KD-MULTIMAP-UNWIND-TIMEOUT`, its mandated `nounwindcheck` lever was never applied, and properties
   that legitimately prove at `--unwind 4` scored UNRESOLVED. 20 of the first 24 hit this; all 20 are
   `proved` on the published branch, 17 via that exact lever.
2. **`--cap-seconds 60` instead of the published 240.** The lever run inherits `--cap-seconds`, so the
   lever itself timed out. 12 properties reported "its mandated lever did not discharge it either"
   while being `proved` via that lever on the branch.

### The protocol
1. **Read the published `run:` block FIRST, before stripping anything.** It records the exact command,
   caps and tool versions that produced the numbers you are comparing against:
   ```
   python3 -c "import yaml;print((yaml.safe_load(open('unified_properties.yaml'))['run']['kani'])['command'])"
   ```
   This is what the provenance stamp is FOR. One query replaced a guess-and-rerun loop here.
2. **Reproduce its parameters exactly** — `--cap-seconds`, `--cap-max`, `--component-dir`, and a
   `--wall-budget` high enough that escalation is never skipped (the budget is a cost heuristic, not a
   verdict input, so it must not differ between the two runs being compared).
3. **Strip only the tool being re-scored** (`status`, `_scored_by`, `evidence`, and that tool's `run`
   entry), so the other tool's verified column is untouched and cannot be blamed for a change.
4. **Change ONE thing: the fix under test.** If a count moves, the fix is the only candidate
   explanation. If two things differ, the result is uninterpretable and worse than no result.
5. **Record the baseline before you start** (per-status counts, and which cells the fix targets), so
   the comparison is arithmetic rather than recollection.
6. Expect a similar wall-clock to the original. EPO's published run took 5h17m; a re-score that
   finishes far faster has probably skipped the expensive levers — treat that as a red flag, not a win.

**A drop is a legitimate outcome** — it means a claim never had content. But it is only reportable
when the parameters matched. Never publish a re-score number without saying which `run:` block you
reproduced.

## Step 2.6 — Refuter: attack every surviving tool-boundary (separation of powers)
For each property the scorer scored `tool-boundary`, spawn the **`refute-tool-boundary`** sub-skill as an *independent* subagent (a different agent than the one that produced the artifact). It re-attacks the wall with the full lever arsenal plus anything the battery has not yet encoded. Outcomes:
- **Refuted** (the refuter lands a reproducible proof): the boundary was false. Adopt the refuter's artifact, re-run the scorer (it will now score `proved`), and **append the beaten signature + the lever that broke it to `known_defeats.yaml`** (only the orchestrator appends, only from this reproduced defeat) so the wall can never be claimed again.
- **Upheld** (the refuter also fails after exhausting the arsenal): the tool-boundary stands, with two independent agents' captured signatures. Only now is `⊘` a legitimate final rating.

A `tool-boundary` that has **not** been through the refuter is not a finished rating — treat it like `UNRESOLVED` for the purpose of the Done gate.

## Step 3 — Role 3: one combined scoring HTML
Run `tools-aggregate-coverage-by-interface <component>` (which renders via the shipped `gate/render_scoring.py`). It reads the now-populated `unified_properties.yaml` and renders the **single combined `<component>_scoring.html`** (superset layout: per-tool KPI cards, combined `Props | Method | Creusot | Kani` scorecard, property-bundle table, spec-vs-each-tool table, glossary, measurement table, unproved-causes narrative, anti-vacuity, provenance, FROM_SPEC callout) **into `components/<component>/verif/` alongside the three YAML**, so it travels onto both verif branches in Step 4. No separate slide-8/9/11 files under this orchestrator — one page per component, extensible to more tool columns later.

**Complete-data-only render (6th rail).** The deliverable render MUST pass `--require-complete`:
```
python3 gate/render_scoring.py components/<component>/verif --require-complete
```
If any verifiable property lacks a scorer-owned status for a rendered tool, the renderer writes `<component>_scoring.INCOMPLETE.html` (still inspectable) and **exits non-zero (2)** instead of writing the shippable `<component>_scoring.html`. This makes it structurally impossible for a partial or interrupted run to be committed under the deliverable name — a non-zero exit here is a gate failure exactly like an UNRESOLVED scorer, and blocks Step 4. (This should not fire when the Step 2.5 gate already passed 0; it is the belt-and-braces check that the page and the gate agree.)

## Step 4 — Git: two per-component verif branches (overwrite-in-place) — the ONLY outputs
Both branches carry the **identical full metadata bundle**; they differ only in which tool's proof artifacts sit alongside it. For **each** tool run (`--tools`):
1. From the fresh `origin/unstable`, check out `verif/<tool>/<component>` if it exists, else create it off `origin/unstable`. Overwrite-in-place — do **not** branch off a stale local tip.
2. Stage, all under `components/<component>/`:
   - **the full metadata bundle (identical on both branches):** `verif/spec_properties.yaml`, `verif/code_properties.yaml`, `verif/unified_properties.yaml`, and the combined `verif/<component>_scoring.html`;
   - **plus that one tool's proof artifacts:** Kani branch → the `#[cfg(kani)]` harnesses (under `src/`); Creusot branch → the `verif/` crate + its `.coma`.
   Do **not** stage the *other* tool's artifacts, and do **not** commit the scratch advisory side-files (`verif/<tool>_advisory.yaml`).
3. **Artifact-presence gate (HARD — absence is a contamination too).** Before committing, count that
   tool's proof artifacts **on disk** and count them **in `git diff --cached --name-only`**. If the
   staged count is lower, **abort and print the difference.** The contamination gate below checks only
   for *stray* paths, and the Step 2 hard-stop counts artifacts on **disk**, not in the **commit** — so
   nothing else in this pipeline can see an artifact that silently failed to stage. Measured on
   eviction-policy-session-lists: an agent-created `components/<component>/.gitignore` containing
   `*.coma` caused **230 of 230** emitted Creusot proof modules to be `git check-ignore`d. Every
   existing rail passed; the branch would have shipped with zero proofs. (For reference, the published
   `verif/creusot/eviction-policy-optimized` carries 242 `.coma` and no component `.gitignore`.)
   **Do not "fix" a shortfall with `git add -f`** — that hides the cause. Fail loudly, find out why the
   path was ignored, and remove the rule.

4. **Contamination gate (HARD):** `git diff --cached --name-only` must be entirely under `components/<component>/`. If **any** staged path is outside that prefix, **abort the commit and print every stray path.** This is exactly the stale-base leak measured on the old `-rerun` branches (543 files on `verif/kani/dispatch-map-rerun`, 1,037 on `verif/kani/memory-tier-rerun` — apps/, Cargo.toml, scripts/, others' deleted `.coma`). A clean run touches only the component folder.
   Gates 3 and 4 are the two halves of one question and you need **both**: gate 3 asks "is everything that should be here, here?", gate 4 asks "is anything here that should not be?". For years only gate 4 existed, which is why a run could ship an empty branch and still look clean.
5. Commit with a message naming the component, tool, run pin, and headline score (`X/N` methods, VCs/`.coma` or harness count, wall-clock/RSS).
6. **Push** `verif/<tool>/<component>` unless `--no-push`/`--dry-run`.

Both branches thus stand alone: each shows the complete scoring picture (the combined HTML + all three YAML) and carries its own tool's reproducible artifacts. There is **no third deliverables branch and nothing goes to `unstable`.**

## Re-VERIFYING a component that already has verif branches (read before you start)

Distinct from a re-score: a re-score keeps the artifacts and re-derives statuses; a re-verify
regenerates the proofs from scratch. Three things behave differently and none is obvious.

1. **The push CANNOT fast-forward — expect `--force-with-lease`, and expect it to be BLOCKED.**
   Step 4 branches from fresh `origin/unstable`, but the existing branch tip is also
   `origin/unstable` + commits, so the new commit is not its descendant. Measured: with
   `origin/unstable` at 937838a9 and `verif/kani/eviction-policy-optimized` two commits ahead of it,
   the existing tip is not an ancestor of `origin/unstable`, so a fresh one-commit branch diverges.
   The agent's force-push is refused by the permission classifier, so **a human has to run it** — this
   already happened for the two eviction-policy-lru branches. Plan for it: finish the run under
   `--no-push` and hand the operator the exact `--force-with-lease` command.
   **NEVER branch off the existing tip to avoid the force.** It looks like it works and it silently
   carries the previous run's artifacts into the new commit — the opposite of a clean-slate re-run.
2. **Property ids may not match the published run.** Role 1 re-extracts blind, so ids, the unified
   count M, and the spec/code split can all legitimately differ. The new bundle is therefore NOT
   cell-by-cell comparable with the old one. If you want a comparison, record the previous per-status
   counts BEFORE starting (they are on the branch) and compare totals, not ids.
3. **The previous page and YAML leave the branch tip** (git history keeps them). That is the intended
   overwrite-in-place behaviour, but anyone asked "what changed?" needs the old tip's hash, so put it
   in the commit message.

Untested as of 2026-09-28: no full re-verify has been run end to end. The re-scores we have done
exercise Step 2.5 onward only, so Steps 1, 2 and 4 on an already-verified component are unproven.
Treat the first one as supervised.

## Step 5 — Done report
Print a compact summary the operator can read at a glance:
- run pin (origin/unstable commit), tools run, new-vs-existing;
- `N` public methods; per tool `X/N` methods proved; property counts `spec_total / code_total / unified M`;
- measurement: wall-clock + peak RSS per tool, VCs/`.coma` (Creusot), harness count (Kani);
- the two branch names pushed (or "local only" under `--no-push`) — each carrying the full metadata bundle (all three YAML + combined HTML) plus its tool's artifacts;
- any flags: spec-only/code-only divergences, tool-boundary misses (with signatures), phantom-coverage on a re-run.

**End every run with one blunt verdict line** so the operator — or a colleague skimming the console or a `verif/.run/` log — knows the outcome without interpreting the report. It is exactly one of:
- `COMPONENT-VERIFY: PASSED` — both scorers exited 0, the `--require-complete` render wrote the deliverable, and every `tool-boundary` was upheld by the refuter. Branches committed (and pushed unless `--no-push`).
- `COMPONENT-VERIFY: FAILED` — a hard precondition, the zero-artifact hard-stop, the contamination gate, or the deliverable render blocked the run. Say which; nothing was committed.
- `COMPONENT-VERIFY: PAUSED(iterate-cap)` — the 3-iteration cap was reached with properties still UNRESOLVED. Nothing committed; the outstanding `id`s are listed and the run is `--resume`-able.

The pass condition is mechanical: **both scorers exited 0** (every verifiable property is `proved` / `tool-boundary` / `delegated`, each carrying `_scored_by`) **and every `tool-boundary` has been upheld by the refuter.** If either scorer last exited non-zero, or any tool-boundary has not been through the refuter, the run is **not done** — say so explicitly, print the outstanding `id`s, and do not commit or push. A property with no artifact is a gate failure, not a rating.

## Safety rails (summary — all non-negotiable)
- **Fresh `origin/unstable` worktree every run.** No reusing month-old trees. Refuse dirty trees.
- **Two commit gates, not one:** an **artifact-presence** gate (every artifact on disk is also staged — absence is a contamination) AND the **component-folder-only** gate (nothing staged outside `components/<component>/`); abort + print the difference or the strays. Only the second existed until 2026-09-28, which is why an agent-created `.gitignore` carrying `*.coma` could have shipped a Creusot branch with **zero** proofs past every rail.
- **Overwrite-in-place** the two verif branches; never delete the prior verified branch history.
- **Prover doctor** before any Creusot run; never mis-attribute a missing prover as a tool boundary.
- **The scorer is the gate, not the prose.** Status is written only by `scorer_kani.py` / `scorer_creusot.py`, which *reproduce* every proof from source. The agent produces artifacts + lever variants; it never grades itself. Both scorers must exit 0 before commit.
- **Four end-states** (Proved ✓ / Refuted ‼ with a machine-checked witness / Delegated ⤴ / Tool-boundary ⊘ with reproducible signature). **Anti-vacuity applies to EVERY `proved`, on every path** — including a proof earned through a scorer-applied lever, and the mutant must run under the SAME flags as the proof. `--no-unwinding-checks` prunes paths rather than truncating them, so a `bounded-shallow` pass is the *most* vacuity-prone, not the least: measured, 36 mutants passed under that lever on one component, and 63 already-published `proved` cells had bypassed the check entirely. **Refutations get the lever battery too** — a refutation that times out used to fall through to the base harness and be published as a proof. "Harness/contract not written" ≠ a rating — it is a gate failure (UNRESOLVED).
- **Every tool-boundary survives the refuter.** An unproven wall is `⊘` only after an independent `refute-tool-boundary` agent also failed to break it; a broken wall's signature is appended to `known_defeats.yaml` so it can never be re-claimed.
- **Report Creusot as VCs/goals + `.coma` count**, never "files"; capture wall-clock + peak RSS.
- **Everything ships on the two verif branches** — each carries the full metadata bundle (all three YAML + combined HTML) plus its tool's artifacts. No PR, nothing to `unstable`, no Box, no scp.
- **Unattended-safe (won't wreck the box, lose progress, or ship a partial page).** Every heavy stage runs under `gate/run_stage.py`: a **watchdog** tree-kills a wedged stage (whole process group + its systemd scope, so no orphaned cbmc/why3/solvers survive); the scorers **checkpoint atomically after each property** and `--resume` skips what is already scored; a timed-out run's own cgroup scope is SIGKILLed and the property retried once at `--cap-max` before any boundary claim; and the deliverable render is `--require-complete` so a partial run writes `…INCOMPLETE.html` and exits non-zero rather than masquerading as the shippable page. This makes runs safe to kick off and check back on — it does **not** make the agent steps autonomous: an UNRESOLVED gate still fail-closes (halts, does not commit), and the iterate loop **PAUSES after 3 rounds** rather than spinning.
- **Legible & shareable (a colleague can run it and trust it).** Every stage tees a full transcript to `verif/.run/<stage>.log` and prints `SENTINEL` START/DONE lines and a blunt final `COMPONENT-VERIFY: PASSED | FAILED | PAUSED(iterate-cap)` verdict — an audit trail, not just a console blur. **No machine-specific hardcoding:** the gate scripts resolve their own dir from `__file__` (scorers default `--gate-dir` to `os.path.dirname(os.path.abspath(__file__))`), take the component/crate/verif dirs as arguments, and derive the prover PATH from `$HOME`; the inexpressibility probe's `creusot-std` is resolved from the component's own `Cargo.toml` (a relative patch path is anchored to the crate dir, as cargo does), else a **checkout-relative** candidate under the repo root, else an explicit `$CREUSOT_STD_PATH` override — nothing assumes `/home/cornel`, so the same skill runs unchanged in Daniel's checkout.

## Reuse (do not reinvent)
- Roles 1–3 skills above (this skill only sequences them and owns git).
- FROM_SPEC YAML schema (`SEPT_2026/SEPT_14/PROPERTIES/FROM_SPEC/*.yaml`) — template for `spec_properties.yaml`/`code_properties.yaml`.
- The hand-curated `SEPT_2026/SEPT_14/*_scoring.html` — reference layout Role 3 reproduces from `unified_properties.yaml`.
- Skill-invokes-skill precedent: `build-property-inventory` already calls `extract-verifiable-properties`.

## `unified_properties.yaml` — the single source of truth (schema)
Superset of the inventory record + the FROM_SPEC fields + per-tool status blocks. This is what Role 2 writes into and Role 3 renders from.
```yaml
component: dispatch-map
interface: IDispatchMap
pin: <origin/unstable commit>            # the run base; stamps every deliverable
generated: <ISO date>
spec_source:  components/dispatch-map/specs/<...>/spec.md
code_source:  components/dispatch-map/src/**
tools: [creusot, kani]
counts:
  methods:     20      # N — public methods of IDispatchMap (the scoreboard denominator)
  spec_total:  102     # blind spec extraction (spec_properties.yaml)
  code_total:  <n>     # blind code extraction (code_properties.yaml)
  unified:     49      # M — reconciled distinct obligations
  attachments: <n>     # Σ|methods|
  not_verifiable: <n>  # NV ledger size
properties:
  - id: DM-CONTAINS-POST
    subject:  contains                    # the ONE public method / named global invariant
    methods:  [contains, get]             # full bundle (⊇ {subject})
    object_fn: "DispatchMap::contains -> HashMap::contains_key"
    kind:     postcondition               # precondition|postcondition|error-case|frame|invariant
    verifiable: true
    global:   false                       # true iff |methods| > 1 (shared/maintained invariant)
    attachments: 2
    origin:   spec+code                   # spec+code | spec-only | code-only | divergent
    source:   {spec: [FR-006], code: ["map.rs:88"]}
    statement: >
      contains(k) returns true iff key k is present in the map after the call, with no state change.
    traces:   [FR-006, US4.1]
    creusot:
      # SCORER-OWNED (scorer_creusot writes these; the agent must NOT): status, evidence, _scored_by.
      # AGENT-SUPPLIED: fidelity, note, and evidence.module(s) pointer / delegate_to referent.
      evidence: {module: verify_contains_post}   # agent: the artifact pointer (or use the verify_<id> convention)
      fidelity: ghost-mirror              # real-type | ghost-mirror | trusted-boundary
      note: "proved over FMap ghost mirror of Mutex<HashMap>"
      status:   proved                    # <- scorer writes: proved | tool-boundary | delegated
      _scored_by: scorer_creusot          # <- scorer stamps provenance; evidence is overwritten with the live run
    kani:
      evidence: {harness: verify_contains_post}   # agent: the artifact pointer (or the verify_<id> convention)
      fidelity: real-type-bounded         # real-type-bounded | representative | arithmetic-core | bounded-shallow
      note: "one symbolic representative entry, real Mutex<HashMap> type kept"
      status:   proved                    # <- scorer writes
      _scored_by: scorer_kani
  # ---- not-verifiable ledger ----
  - id: NV-1
    scope:  "timing of eviction"
    kind:   not-verifiable
    verifiable: false
    reason: >
      wall-clock duration is not machine-checkable (the timeout's occurrence is verifiable, its duration is not).
    traces: [FR-021]
    # NV records carry no tool blocks.
```
- `status` domain: `proved | refuted | delegated | tool-boundary` — **written by the scorer, never the agent.** `refuted` means the scorer reproduced a *violation*: the code breaks the obligation, with a witness. It is a RESULT, not a failure — it is what rewards the verification effort — and it is earned the same way a proof is, by execution (Creusot proves the negation; Kani demonstrates the violation is reachable). The scorer's fourth outcome, `UNRESOLVED`, is a *gate failure*, not a persisted rating: it is never written as a property's status; it fails the gate (exit non-zero) until the agent produces the missing artifact/lever. Any pre-existing agent-written `status` is overwritten. A block carrying `_scored_by` is authoritative; a block without one has not been through the gate and does not count.
- `symbol` domain: `✓` proved native · `★` proved against a faithful ghost mirror / trusted boundary, or under a narrowed claim (`bounded-shallow`, `arithmetic-core`) · `‼` refuted, the code violates the obligation · `⤴` delegated to a named referent OUTSIDE this pipeline (not a tool limit) · `⊘` this tool CANNOT prove it — not expressible in its model, or the lever battery was exhausted — with reproducible evidence · `·` open, nothing settles it yet.
- `fidelity` **is the abstraction-vs-real finding, captured structurally**: Creusot `ghost-mirror` (proved over an FMap/Seq model of the real container) or `trusted-boundary` (★ over a `#[trusted]` effect: block-device I/O, crc32fast, UTF-16, Mutex) vs Kani `real-type-bounded` (real product type, bounded scope / one symbolic representative). Where both tools prove a property, this is where their difference is recorded.
- `miss_class` is `TOOL` (capability limit, with a reproducible signature) vs `AGENT` (effort/expressibility we could close) — set only when `status != proved`.
- `spec_properties.yaml` / `code_properties.yaml` keep the simpler blind-extraction schema (FROM_SPEC style: `id/subject/kind/verifiable/statement/traces`, `reason` for NV) — **no tool blocks** — and supply the two blind denominators.

## Anti-patterns
- ❌ Running on a dirty or reused tree. (Step 0 refuses it.)
- ❌ Committing anything outside `components/<component>/` to a verif branch. (Contamination gate aborts.)
- ❌ Re-extracting properties inside Role 2/3. (Inventory owns the set; attach by `id`.)
- ❌ Reporting a missing prover as a tool boundary. (Prover doctor first.)
- ❌ Putting `[patch.crates-io]` in `components/<component>/.cargo/config.toml`. A cargo *config* at component scope breaks every cargo invocation inside the component, including the Kani scorer's preflight. It belongs in `verif-creusot/Cargo.toml`.
- ❌ A committed `.gitignore` inside `components/<component>/`. Use the run-local `info/exclude` (Step 0.5) so an ignore rule can never hide a proof artifact from a commit.
- ❌ `git add -f` to get past an artifact-presence shortfall. Find out why the path was ignored.
- ❌ Harnesses generated by `macro_rules!`. The gate discovers them by regex over source text, so they are invisible and score "no runnable harness".
- ❌ Pushing a run while the scorer still returns UNRESOLVED / exits non-zero for any property. (Not done — the gate, not a YAML field, decides.)
- ❌ Emitting the old three thin HTML slides or a hand-maintained `.md`. (One combined `<component>_scoring.html`; deliverables are the YAML + that HTML.)
