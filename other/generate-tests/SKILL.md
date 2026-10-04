---
name: generate-tests
description: "Generate unit tests for a .NET service following the coverage-kit conventions. Use when the user asks to 'generate tests', 'backfill tests', 'characterize this service', or 'add tests for' a target after coverage-init has run. Operates in characterization mode (freeze current behavior for existing code) or spec mode (assert intended behavior for new/changed code), enforces the run-capture-fill loop, routes untestable units to the manifest cannot-test log, can fan the backfill out across a user-chosen number of parallel agents for large worklists (asking first, since more agents cost more tokens), and runs a single read-only suite critique before the baseline locks in (auditing cannot-test legitimacy, assertion/C1 depth, systematic gaps, and any frozen defect missing from the manifest latent_bugs backlog, never the C0/C1 numbers themselves)."
---

# generate-tests

Generates tests under the base rules and this repo's overlay + manifest. Read all three
before generating:
- `${CLAUDE_PLUGIN_ROOT}/rules/unit-testing.base.md`
- `.claude/coverage/refs/unit-testing.md` (repo overlay)
- `.claude/coverage/refs/coverage-manifest.yml` (categories, exclusions, gate)

## Preflight: is this repo on the current kit?

Run this before building the worklist, every time, whether or not anyone mentioned an upgrade:

```
python .claude/coverage/tools/coverage-gate.py \
  --manifest .claude/coverage/refs/coverage-manifest.yml --print-kit-drift
```

Any state other than `current` means the repo has not been reconciled against today's rules, and a
backfill is the worst moment to discover that: a pass run on superseded mechanics wastes every token
it spends. Consult `${CLAUDE_PLUGIN_ROOT}/MIGRATIONS.md` ("Preflight") and split what you find:

- **`auto` entries governing how THIS pass runs** (refresh the `.claude/coverage/tools/` copies, the
  fan-out contract, frozen-bug recording): apply them now, silently, and note them in the closing
  summary.
- **`sign-off` entries** (anything that moves scope, the denominator, or the floor): report them in
  one line and leave them alone. Re-scoping mid-backfill moves the worklist under your own feet.
  `coverage-redo` is what applies them; say so and carry on with the pass as scoped today.

If the state is `current`, say nothing and continue.

## Build the full worklist first — then cover ALL of it (do not stop early)

The scope of a backfill pass is **the entire testable set the manifest defines**, not a
handful of "priority" files. Before writing any test, enumerate that set explicitly from the
manifest and write it down as a checklist. The testable set is:

1. Every file matched by a `category_map` target category and **not** matched by an
   `exclusions` pattern (the genuine unit-scope files), AND
2. Every **carve-out method** on an exclusion entry: the structured `carve_outs:` list (each
   `{ method, lines, testable }`), or the legacy `CARVE-OUT: MethodA, MethodB` prose in `reason`
   on older manifests. These are the thin pure/decision slices of god-classes (the UserService
   pattern): testable units even though their file is integration-scope, and a DbContext-injected
   service is tested by backing the context with the EF in-memory / SQLite provider. Init recorded
   them precisely so this step covers them; the file's `excluded_rest` says what stays out of scope.

**Resolve every worklist item to a full repo-relative path, not a basename.** Repos have many
files sharing a name (`UserService.cs`, `Handler.cs`); test the exact file the manifest entry
points at, mirror the test under that same path, and never carry one file's carve-out methods onto
its same-named sibling. If a manifest pattern is ambiguous (bare basename matching several files),
flag it back to the manifest rather than guessing which file it meant.

Items already covered by existing tests are checked off, not re-done. Items in `cannot_test`
are out. Everything else in the set MUST be either tested in this backfill or appended to
`cannot_test` with a reason — there is no third option of silently leaving it untouched.

**An item is "done" only when its branches are covered — not when it has *a* green test.** This
is the definition that matters and the one most often shortcut. A method with filters, a
`switch`, asc/desc, null guards or error paths needs an input pinned per branch; one happy-path
test checks the item off the worklist while leaving 40–50% of its branches cold. A test
*existing* is not the bar — its branches being *exercised* (or sent to `cannot_test` with a
reason) is. Treat an under-covered target method exactly like an untested worklist item: not
done. See "Cover the BRANCHES" below for how.

**Hard rule: a coverage percentage is never a stopping condition — in either direction.** Do
not stop because the number "looks low" or "looks done," and do not stop at worklist
completeness while target-layer methods still have uncovered branches. The pass ends only when
every worklist item has **branch-covered** tests or a `cannot_test` entry. The classic failure
this prevents: writing one test per file, watching the suite go green, and stopping at ~50–60%
C0/C1 because each method got one path — that is an **unfinished** pass, not a complete one.

## Phasing — when the worklist is large, plan it and report progress

If the worklist is large enough that one pass is impractical (rule of thumb: more than
~15 target files or ~40 carve-out methods, or it spans multiple test projects), **do not
silently do a slice and stop.** Instead:

1. Split the worklist into phases (group by file/service/test-project so each phase is a
   coherent, runnable chunk).
2. **Tell the user the phase plan up front** — the full count of testable units, how many
   phases, and what each phase covers — before generating. This is the "let me know if it
   needs phases" contract.
3. Execute phases in order. After each phase, report progress as **N of M worklist items
   done** and what remains. Keep going through all phases unless the user says otherwise.
4. The working tree stays dirty across phases; do NOT commit between phases.

## Scaling the backfill — efficiency, then optional parallel fan-out

A legacy worklist can be enormous. Two levers: make each unit cheaper, and (optionally) do many
at once. The efficiency rules apply **whichever way you run** — sequential or parallel:

1. **Batch run-capture-fill per class, not per method.** The dominant cost is build + test
   execution. Write the whole test class for a file — **one test per branch of each method, not
   one test per method** — build once, run the class once, capture *all* actual values from that
   single run, then fill. The economy is in batching the build/run, not in writing fewer tests:
   never pay a build/run cycle per method, and never trade away branch coverage to save cycles.
2. **Pre-triage narrows the assertion, it does not discard the unit.** Before the
   write-build-run loop, scan each unit for an untestable signal (`DateTime.Now`/`UtcNow`,
   `Guid.NewGuid`, `Random`, direct infra/IO). A signal is a reason to look, not a verdict — a
   whole method is `cannot_test` only when the untestable condition is *confirmed*, not merely
   present:
   - **Confirm "no seam."** Is the dependency really un-mockable? A collaborator injected as an
     interface/abstract, an `IHttpClientFactory`, an optional `Func<DateTime>` — these are seams.
     A **constructor-injected `DbContext`** is also a seam: back it with the EF in-memory / SQLite
     provider. A `DbContext` on the constructor is NOT grounds to blanket-`cannot_test` the class;
     dumping every DbContext-touching method into `cannot_test` (as a real run did, roughly 87 false
     entries in one repo) is the canonical false-exclusion this rule exists to stop.
     Route to `cannot_test` only when the nondeterministic/infra call is made directly with no
     injectable seam, or when the specific EF op is one the in-memory provider cannot run (raw SQL,
     `ExecuteUpdate`/`ExecuteDeleteAsync`, `Batch*`, real transactions, unset-rowversion inserts,
     untranslatable LINQ).
   - **Confirm the nondeterminism reaches the assertion.** A method that logs `DateTime.Now` but
     returns a deterministic result is fully testable — assert the result. Only when the
     nondeterministic value flows into the output you would assert (and cannot be pinned) does
     that assertion drop. **Named anti-pattern — the entry-line `Stopwatch`/`Guid.NewGuid`:** event
     handlers and command handlers commonly open with `var sw = new Stopwatch()` /
     `Guid.NewGuid()` for timing and a correlation id used only in a log line. That is NOT the
     method's behavior — the behavior is the event→document/state mapping that follows. Do NOT
     route the whole handler to `cannot_test` for it; test the mapping/branches and ignore the log.
     Routing ~50 near-identical handlers to `cannot_test` on this signal (as a real run did) is the
     canonical false-exclusion this rule exists to stop.
   - **Still cover the deterministic branches.** A method with a `Guid.NewGuid()` id and three
     validation branches gets tests for the three branches (assert everything except the id, or
     assert the id is non-empty). `cannot_test` scopes to the specific method/assertion that is
     genuinely blocked — never the surrounding testable logic.

   When in doubt, run the loop — let run-capture-fill prove testability rather than pre-declaring
   it away to save a cycle. Every `cannot_test` entry you do record carries a **mitigation** (the
   seam that would unlock it), per the base rule.
3. **Pattern-replicate across siblings.** Legacy services are full of structurally identical
   units (handlers, validators, mappers). Solve the seam/mock setup once on a representative,
   then replicate the shape across the lookalikes. A "phase 0" that builds the shared
   fixtures/builders once feeds this.
4. **Risk-order the worklist** by complexity × churn × fan-in so the most valuable coverage lands
   first and the hardest seam problems surface early (while there is budget to fix them). This
   does not reduce total work — the worklist is still covered in full — it just sequences it well.

### Optional parallel fan-out (ask the user first)

The worklist is independent per file, so it parallelizes cleanly. For a large worklist, **offer**
to run the backfill as a fan-out workflow — but **never auto-spawn agents**. Parallel agents burn
tokens fast, and the right count depends on how quickly the user wants it done and their budget,
so present the trade-off and let them choose:

1. Build and risk-order the full worklist (above). State the total count of testable units.
2. Ask the user how many agents to run, mapping count to a *rough* wall-clock for **this**
   worklist (scale the examples to the real size; caveat that they are estimates and that more
   agents = proportionally more token burn):
   - **1 agent** — sequential, lowest token burn, ~a day for a big service.
   - **3 agents** (default) — balanced, ~6 hours.
   - **10 agents** — fastest, highest burn, ~1 hour.
3. On their choice, **write the risk-ordered worklist to disk** as a JSON array at
   `coverage/backfill/worklist.json` (each item shaped `{ file, methods?, group?, mode? }`), then
   invoke the workflow with the manifest **path, not the list itself**. Get the call exactly right
   (each rule below is a real field failure this kit has hit, where ZERO agents ran and the launch
   still looked like success):
   - **No item may live under a `scope.vendored_paths` directory.** Those are copies of other repos'
     sources, owned and tested there. A worklist item inside one is a scoping bug upstream in the
     sweep, not work to do: drop it, and say so, rather than writing a test for another team's
     library against a copy the next vendoring sync overwrites. Filter the worklist against
     `scope.vendored_paths` before writing it, and if anything was dropped, report the count.
   - **Write the file FIRST and confirm it is non-empty** (`test -s coverage/backfill/worklist.json`).
     The workflow's Plan agent reads this file off disk; if it is missing or empty the run bails with
     `empty-worklist` and spawns nothing.
   - **Pass `args` as a real JSON object, never a JSON-encoded string.** A stringified payload makes
     every field undefined inside the workflow, so it silently defaults and runs nothing.
   - **Pass `worklistManifest` (the path). There is NO `worklist` arg.** An inline `worklist:[...]`
     is ignored by the workflow AND, when large, trips the approval-dialog control-char guard. Do not
     put the array in `args` at all.
   - **Invoke via `scriptPath`, not `name`** (name + inline args is what tripped the guard in the
     field).

   `Workflow({ scriptPath: "${CLAUDE_PLUGIN_ROOT}/workflows/coverage-backfill.workflow.js",
   args: { concurrency: <chosen>, solution: "<sln>", worklistManifest: "coverage/backfill/worklist.json" } })`.
   If the user just says "go", default `concurrency: 3`.

4. **After launch, drive it to completion. Do not re-ask, re-explain, or fall back to one-by-one.**
   Once concurrency is chosen and the workflow is launched, the fan-out IS the plan; executing it is
   the goal, not a checkpoint. Monitor the background run to done. If a run dies mid-flight (session
   exit, interruption), **resume it** with `resumeFromRunId` so completed chunks replay from cache; do
   NOT fresh-relaunch, which orphans the prior run's git worktrees and duplicates work. Only start a
   truly new run when there is no prior run to resume. Never quietly abandon the workflow and generate
   the remaining worklist with sequential `Agent()` calls: that is the exact regression this fan-out
   exists to prevent (it burns the same tokens without the parallelism and drags the user through
   dozens of turns). If the workflow is genuinely unusable, say so and ask; do not silently downgrade.

5. **Verify the frozen-bug write landed: the fan-out's one silent data loss.** A chunk agent works
   in a throwaway worktree, so a suspected defect it froze exists only in its returned `latentBugs`
   array; the assemble step is what turns those into manifest `latent_bugs:` entries. Read
   `latentBugsTotal` off the workflow result and confirm the manifest now holds that many entries
   (they are also returned verbatim as `latentBugs`, precisely so you can re-do the write rather
   than trust the assemble prose). **If the counts disagree, write the missing entries yourself
   before the promotion gate** (see "First-run triage" for the shape). An unwritten entry is not a
   cosmetic loss: `coverage-gate.py` renders section 7 and the ACTION REQUIRED banner from the
   manifest alone, so a green suite over live bugs reads as a correct one.

The workflow reads the worklist off disk and partitions it into `concurrency` chunks (one agent
each, in its own git worktree so parallel writes don't collide), generates + adversarially verifies
each chunk, then a
single assemble step applies every chunk's patch to the main tree, merges both `cannot_test` and
`latent_bugs` discoveries once (no manifest write races), and confirms the full suite is green. It
leaves the tree dirty: the promotion gate below still governs when the baseline report and commit
happen.

## Measure for feedback DURING the pass (this is not the baseline)

You cannot judge branch completeness by eye — measure it, and measure it *before* you decide
you are done, not after. Measuring for feedback and *locking the baseline* are two different
acts; only the latter is a promotion step. So:

- **In-loop, as often as useful:** run `./.claude/coverage/tools/report.sh` read-only to see
  C0/C1 and the **Risk Hotspots** table. This writes a throwaway `REPORT.md` but you do NOT
  write `baseline.recorded_overall` from it — it is a feedback instrument, nothing more.
- **Read the signal and act:** every **target-layer** (non-`excl:`) row in Risk Hotspots, and
  every target method with an uncovered branch that is not in `cannot_test`, is an unfinished
  worklist item. Go back and pin inputs for its missing branches (run-capture-fill). Re-measure.
  Loop until every target-layer method is either fully branch-covered or its remaining uncovered
  branches are logged in `cannot_test` — i.e. 100% of the testable set, per the exit gate. (The
  manifest's diff-coverage branch threshold is a per-PR floor, not the backfill target — do not
  stop the backfill at it.) This is the part that moves a pass from ~50–60% to full testable
  coverage — and it belongs **in the generation loop**, not in a later cleanup.

This is explicitly NOT "stopping on a number" — you are not chasing a percentage, you are
discharging worklist items whose branches the number reveals are still uncovered. The pass is
done when that list is empty, whatever the resulting percentage happens to be.

## Exit gate — the testable set is 100% branch-covered; the only residual is documented `cannot_test`

The backfill exits ONLY when the entire testable set is covered — not "most", not "the priority
files", 100% of it. The testable set is: every target unit-scope method + every carve-out method
(the pure/branching slices of excluded files, including controllers and IO orchestrators), with
**all branches exercised** (see "Cover the BRANCHES"). The single permitted residual is
`cannot_test`, and it is not a free pass:

- **Every uncovered branch is either covered or a `cannot_test` entry — there is no third state.**
  If a target-layer method sits below 100% branch coverage and it is not in `cannot_test`, the
  pass is not done; go pin the missing branches. A worklist item is closed only when its branches
  are exercised OR the specific blocked branch/method is in `cannot_test`.
- **Each `cannot_test` entry is a documented, mitigated decision**, scoped to a method (never a
  file/folder): `{ target, category, lines, reason (signal at file:line), mitigation }`. The
  mitigation is the concrete source change that would unlock it (extract `IClock`, inject the
  repository interface, move the pure slice out), or an explicit "none — genuinely
  nondeterministic external boundary". This is the "detailed report + mitigation plan for what
  truly cannot be covered" that the exit requires.
- **The residual is reported, not buried.** Report §6 ("Not Testable") renders every entry with
  its lines, reason, and mitigation; the suite critique (below) audits each one hardest before
  the baseline locks. A large `cannot_test` list is a signal to escalate a shared-seam refactor
  to the human, not to accept as-is.

This is not "stopping on a number" — you are not chasing the overall %, you are driving the
testable set's uncovered branches to zero. The resulting overall % is whatever falls out of that.

**The manifest `target` (default C0 95% / C1 85% on the Adjusted slice) is an ACCEPTANCE bar, not
this exit condition.** The exit gate above is stricter: it drives the testable set to 100% branch
coverage with `cannot_test` as the only residual. The target is a downward sanity check on the
*result*: once the exit gate is met, if the measured Adjusted is still BELOW target, the residual
(the `cannot_test` list / exclusions) is too large to be honest, which is a signal to re-open the
sweep or escalate a shared-seam refactor (the systematic-seam clusters in the suite critique), not
to lower the bar. Do not confuse the two: you never *stop early* at the target, and you never accept
an Adjusted below it without escalating why. The target is also what the diff gate is set to, so new
code lands at the goal; the recorded baseline floor sits a few points below it (see the manifest).

## Promotion gate — set the baseline and commit only when the exit gate is met

`coverage-report` (to set/raise the **baseline**) and any commit are **promotion steps**. They
run ONLY after the exit gate above is met (the testable set 100% branch-covered, every residual a
mitigated `cannot_test` entry) **and the suite critique below has run**. Per
the action ladder, generation itself is edit-only: leave the tree dirty and stop. The
distinction from the in-loop measurement: that one is read-only feedback you may run anytime;
this one *writes the floor*, so it runs once, last. Do not write `baseline.recorded_overall`
mid-backfill, and do not propose committing a partial backfill — a partial baseline locks in a
misleadingly low floor.

**Measure via the wrapper, not by hand.** When you do measure, run the one-command wrapper
`./.claude/coverage/tools/report.sh` (it collects with the repo filefilter, joins the manifest, and
**persists a dated `reports/<YYYY-MM-DD>/REPORT.{md,html}` + `CANNOT-TEST.md`**). Do NOT hand-run `run-coverage.sh` + `coverage-gate.py` and
read the numbers off stdout — that leaves no saved report and skips the repo scoping, so the
report effectively goes missing. If `report.sh` isn't installed yet (repo pre-dates it), copy
it from `${CLAUDE_PLUGIN_ROOT}/scripts/report.sh` first, then run it. Only after `REPORT.md`
exists do you write the measured Adjusted into `baseline.recorded_overall`.

**Never record a baseline off a red suite.** Coverage measured while any test fails is
unreliable — a failing test may not have executed the lines it was meant to, so the numbers are
not the real output. If `report.sh`'s Test Results show any failure (the report prints a ⚠️
banner), the baseline step is blocked: fix every failure until the suite is fully green, then
re-measure. A backfill that ends with, say, 54 failing tests is unfinished, not ready to
promote — do not write `baseline.recorded_overall` from that run.

## Suite critique — once, before the baseline locks in

When the worklist is exhausted and the suite is green, run a single critique over the *finished*
suite **before** `coverage-report` sets the baseline. This is the natural moment: fixing is
cheapest now, and a dodged `cannot_test` or shallow tests would otherwise freeze a misleading
floor. Run `report.sh` first so the critique can use the report's analytics (e.g. low-C1
buckets) as leads.

Spawn **one read-only subagent** over the whole suite + the manifest + the report. **Single and
read-only on purpose** (same reasoning as the init critique): systematic problems — a bucket
dodged wholesale, the same smell everywhere — are only visible to one reviewer seeing all of it,
applying one standard; it produces findings, it does not silently rewrite tests. Its mandate:

1. **`cannot_test` legitimacy.** Re-check **every** `cannot_test` entry against the rubric
   signal: is it genuinely untestable (no seam, real infra, nondeterministic), or did generation
   take the easy out? Flag any entry where a seam exists or a deterministic test is feasible.
   This is the escape hatch — audit it hardest. Watch specifically for the entry-line
   `Stopwatch`/`Guid.NewGuid` false-exclusion (a whole handler dropped because it opens with a
   timing/correlation id used only in logging) — the handler body is testable and must be covered.
2. **Assertion quality / C1 depth.** Find files where C0 is high but C1 is low (lines run but
   branches never asserted → shallow tests) and any vacuous/tautological assertions the
   per-chunk verify missed (asserting a mock returns what it was set to). Whole-suite view —
   do not re-do the per-test check the backfill workflow already did.
3. **Systematic patterns — cluster and quantify, do not just note.** Group `cannot_test` by
   shared signal and **count** each cluster: "N handlers share `Stopwatch`+`Guid.NewGuid`",
   "M types blocked on `InternalsVisibleTo`". A cluster of ≥3 is almost always ONE fix that
   unlocks all of them (an `IClock`/`IGuidProvider` on a shared base class, a single
   `InternalsVisibleTo`, one extracted interface) — the highest-ROI move and the one most often
   missed in a long flat list. Escalate each such cluster to the human with its count and the one
   seam that clears it, rather than accepting N near-identical entries. Also normalize category
   vocabulary while here (e.g. `framework_mismatch`/`framework-incompatible` → one label) so the
   report groups cleanly. Also flag any category dodged wholesale and repeated smells.
4. **Highest-ROI next moves** — concrete, not vibes.
5. **In-scope coverage gaps — TARGET layer only (the lens that is easiest to miss).** From the
   report's **Risk Hotspots** and per-file table, list every **target-layer** method/file with
   any uncovered testable branch that is not in `cannot_test` — uncovered branches in code we
   OWN. These are NOT `cannot_test` and NOT shallow-assertion cases (item 2 only catches
   covered-but-unasserted lines); they are **unfinished characterization** — a complex method got a
   happy-path test and its other branches (filters, switch arms, error paths) were never executed.
   A **target**-bucket row in Risk Hotspots is the signal. An `excl:*` hotspot is fine to leave (it
   is integration/E2E-covered, not unit) — only target-layer gaps count here. Close them before the
   baseline locks (see Output).

6. **Unrecorded frozen defects (the backstop for a lost `latent_bugs:` entry).** Read the
   assertions, not just the coverage: find every test that freezes behaviour a reviewer would call
   wrong, and check each against manifest `latent_bugs:`. Any that is missing is a live product bug
   the suite is now certifying as correct. The tells: a test name that states the defect
   (`..._ThrowsRuntimeBinderException`, `..._IgnoresCurrentStudioFilter`, `..._ReturnsNull`,
   `..._SwallowsException`), an expected value that is plainly wrong (an empty collection where the
   scenario has matching rows, a tenant/studio filter absent from the captured query, a swallowed
   exception, a 500-shaped path asserted as-is), or a defect described in a test comment rather than
   in the manifest. This lens is cheap and load-bearing: a chunk agent's finding lives only in its
   returned data, so anything the assemble step failed to write is invisible from here on. Report
   each as a proposed `latent_bugs:` entry with its `pinned_by` test. **Recording is a manifest
   write, never a behaviour fix**: do not change the test or the source.

**Trust the C0/C1 numbers; do not second-guess them** — they are tool output; if a number looks
wrong that is a pipeline check (file-filter, merge, instrumentation), never an LLM opinion. But
trusting the numbers is NOT ignoring them: item 5 exists precisely to ACT on the in-scope gaps they
reveal. (A target method at 70% slipping into the baseline because the critique was "number-blind"
is the exact failure this item closes.)

Output: split findings into (a) **clear-cut fixes to apply now**, before baseline — a
`cannot_test` entry that is actually testable → write the test and remove the entry; **a
target-layer coverage gap (item 5) → write the missing branch tests (run-capture-fill) until the
method's testable branches are fully covered (or the unreachable ones are in `cannot_test`) and it
drops off Risk Hotspots**; and (b) **judgment calls / larger
refactors** escalated to the human. Apply the clear-cut fixes, then re-check them (loop until none
remain) — a fix can surface another, e.g. writing the test that retires one `cannot_test` reveals a
shared seam that retires more. **The baseline does not lock while any target-layer in-scope gap
remains.** Append the findings to the report under `## Suite review`. Only after this loop settles
does the baseline report run.

## Pick the mode

- Target existed at the baseline → **characterization**.
- Target is new, or a line changed after the baseline → **spec**.
- Mixed file → characterize baseline methods, spec the new/changed ones.

Skip anything matched by a manifest `exclusions` pattern — that uncovered state is
intentional and explained by the manifest.

## Characterization mode — run-capture-fill (hard precondition)

For each target method:

1. Write the test: explicit pinned inputs, dependencies mocked through interfaces,
   a placeholder expected value. Assert observable output/state/exceptions — not mock
   call order (interaction verification only where the side effect IS the behavior:
   message publish, email send, external sink with no return value).
2. **Run the single test.** This is required. Do not write an expected value from
   reading the source.
3. Read the actual value from the run. Write it into the assertion.
4. Re-run until green.

If step 2 is genuinely impossible — needs real infrastructure with no seam, or depends on
wall-clock/id/random that flows into the asserted output with no seam — DO NOT write a
predicted assertion. Add the target (the specific method, not the file) to the manifest
`cannot_test` list with a category, a reason (the signal at `file:line`), and a **mitigation**
(the source change that would unlock it, or "none — genuinely nondeterministic external
boundary"). Make no source change to fix it; the backfill freezes source.

**A failing-to-compile test is NOT "impossible" — it is unfinished authoring.** Rule out the
authoring causes first (mock wiring, a legitimate missing test-project reference, an unstubbed
constructor argument). Only route to `cannot_test` when the unit cannot be constructed or
exercised through any interface after those are addressed — never on the first red build.

**Cover the BRANCHES, not just one happy path** — a target method is "done" only when its
branches are exercised, not when it merely has *a* green test. For a method with branching
(filters, a `switch`, error paths, asc/desc, null guards), one input lands ~one path and leaves
the rest uncovered — that is the partial-coverage gap that otherwise slips to the report's Risk
Hotspots (e.g. a `GetAll` with keyword + type + unit filters and a 3-way order switch needs a
test per filter and per switch arm). Enumerate the method's branches and pin an input for each;
a branch that genuinely cannot be reached without real infra goes to `cannot_test`, not ignored.
**Do this here, at write time — it is the plan, not an afterthought.** The in-loop measurement
("Measure for feedback") tells you which methods you missed; the suite critique's item 5 is only
a final backstop for what slips through, never the place you first go looking for branch coverage.

## Spec mode

Expected values come from the requirement/acceptance criteria, not from running the code.
The run-capture-fill loop does not apply. If a new unit is not testable through its
interfaces, that is a dependency problem to fix in this change (extract interface, inject
seam) — do not skip and do not widen the test project's references.

## First-run triage (characterization backfill)

A characterization test is green by construction once run-capture-fill completes, because
the assertion holds the actual output. The only judgment calls are the units where the
captured output looks like a latent bug. Freeze them anyway (assert the actual value) and
**record each one as a `latent_bugs:` entry in the manifest**: frozen, not endorsed. Do not
change behavior.

Record it in the MANIFEST, not in prose. `coverage-gate.py` renders `latent_bugs:` as a red
"7. Latent bugs frozen by characterization (ACTION REQUIRED)" section plus a banner at the top of
every report, so the backlog reaches the artifact people actually read and survives regeneration.
A note written into the report body instead is lost the next time `report.sh` runs.

One entry per suspected defect:

```yaml
latent_bugs:
  - severity: A            # A security/cross-tenant · B data loss · C unhandled 500
                           # D correctness/observability · E dead code or note, not a defect
    target: "OrderRepository.DeleteAsync"
    file: "src/Data/OrderRepository.cs:214"   # optional
    summary: "Ignores the current-tenant filter, so a caller can delete another tenant's rows."
    pinned_by: "DeleteAsync_DeletesAcrossTenants_IgnoresTenantFilter"
```

`pinned_by` is the test that freezes the behaviour, and it is what makes the entry actionable: a
correct fix turns that test red, so whoever fixes the bug knows exactly which assertion to update
in the same change.

**`latent_bugs` is a defect backlog, not a coverage exemption.** It does not affect scope, the
Adjusted number, the ratchet, or the diff gate. Untestable *code* still goes to `cannot_test`.
Do NOT append findings to `CANNOT-TEST.md`: that file is regenerated from the manifest on every
`report.sh` run, so an append is silently lost.

## Output of a generation pass

- New/updated test files mirroring source structure, named `Method_Scenario_Expected`.
- Any newly discovered untestable targets appended to the manifest `cannot_test` list, each
  scoped to a method and carrying `{ category, lines, reason, mitigation }`.
- A `latent_bugs:` entry in the manifest for every suspected defect frozen by a test, each
  carrying `{ severity, target, file?, summary, pinned_by }`. Do not fix them; the red
  section 7 of the report is what surfaces them.
- The updated worklist checklist: N of M items done, what remains (and which phase, if phased) —
  the testable set at 100% branch coverage, with the residual `cannot_test` list and its
  mitigation plan called out explicitly (this is the exit-gate evidence).

Only once the exit gate is met (testable set 100% branch-covered, every residual a mitigated
`cannot_test` entry) **and the suite critique has run** (see the exit/promotion gates and "Suite
critique"), run `coverage-report` to measure and set the baseline. Do not assert
coverage numbers yourself — they come from the tool. Until then, leave the tree dirty and stop
without committing.
