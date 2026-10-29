---
name: class-refactoring
description: Use when refactor PHP classes to improve structure, readability,
  and maintainability while preserving behavior
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Apply @rules/refactoring/general.md — shared definition of refactoring, recommended incremental process, and "no big-bang rewrite" rule.
- Apply @rules/php/core-standards.md
- Apply @rules/php/dependency-selection.md — when the refactor proposes extracting behavior into an external Composer package or replacing a hand-rolled helper with a library, run the Activity gate + Compatibility gate from that rule before recommending the dependency. A refactor that adopts an archived / abandoned / branch-pinned package is rejected on the spot.
- If the current project uses Laravel, also apply `@rules/laravel/laravel.md`, `@rules/laravel/architecture.md`, `@rules/laravel/filament.md`, and `@rules/laravel/livewire.md`
- Apply @rules/code-testing/general.md
- Never change behavior
- Keep public API stable unless explicitly required

---

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `apply`):

- **`apply` (default)** — full refactoring: modify code, author the pre-refactor coverage commit, run the tests covering the refactored surface, and chain the After Completion review. Every step below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by a caller that explicitly asks for a read-only proposal)** — **never modify code, never author tests, never stage / commit / push, never run fixers or checkers, and never chain any After Completion review.** Scope the analysis to the lines added or modified by the PR diff and return the refactoring opportunities as markdown only.
Every code-changing instruction below — apply, extract, split, consolidate, collapse, replace, remove, move, or any other verb that would touch code — is emitted as a written proposal, not applied to code; the Test Coverage Gate becomes a read-only audit (report coverage gaps as findings, do not author tests).

---

## Scope
Improve code structure and quality without changing behavior.

Focus on:
- clarity
- separation of concerns
- testability
- maintainability
- efficiency under load

---

## Execution

### Read, Map & Verify before refactoring (mandatory pre-flight)

> **`MODE=cr`:** perform Read and Map read-only to ground the proposals in the real code; Verify is the audit you already run. Do not modify code.

Reading, mapping, and verifying come first; refactoring comes last. This pre-flight is **blocking** — do not edit a single line of production code until all three steps pass, and never act on an assumption you have not confirmed by reading the code.

1. **Read** — open and read the actual class being refactored and the code it depends on (callers, called methods, related tests, configuration). Confirm what the code does by reading it, not by guessing from names.
2. **Map** — map the change's blast radius: every call site and caller of the touched code, the data-flow paths through it, the public API consumers, and the existing helpers / Services / Actions / layers to reuse instead of reinventing.
   Then run a **completeness sweep** over the whole tree. Grep the entire repository for every name, signature, and convention the refactoring renames, removes, or redefines, and every call site, test, and public API consumer bound to them — never only the files the assignment names, and never only the files you have already opened.
   Cover every file category the repository carries: source, tests, `rules/`, `skills/`, `agents/`, documentation, configuration, and generated assets such as `CHANGELOG.md` or `README.md`. Record the full match list before you rename or move anything, then classify each match as in scope for this refactoring or as a stated exception. An incomplete sweep leaves a call site bound to a signature that no longer exists, and that call site surfaces later as a failing pinned test or a broken cross-reference.
3. **Verify** — check your assumptions against the real code and its observed behavior before deciding the highest-impact refactoring. If reading and mapping contradict the task framing, stop and surface the discrepancy instead of refactoring on a wrong premise.

Only after Read, Map, and Verify are complete may the Test Coverage Gate and the refactor proceed.

### Test Coverage Gate (mandatory pre-flight)

> **`MODE=cr`:** do not write tests or commits. Run the coverage check read-only and report any target lines below 100% coverage as a refactoring finding (a refactor cannot land safely without them) — then continue the analysis. The steps below that author tests / commits apply to `MODE=apply` only.

**The gate is blocking.** Refactoring may not edit a single line of production code until tests for the target lines reach 100% coverage. Satisfy the **Test Coverage Contract** defined in `@rules/refactoring/general.md`:

1. Verify coverage of the *current* code that the refactor will touch, using the project's available coverage tooling scoped to those files (per `@rules/php/core-standards.md` Testing section). Every line, branch, and condition must already be at 100%.
2. **If coverage is below 100% on the target lines, stop and write the missing tests first.** Use `@skills/create-test/SKILL.md` to author them; commit them in a dedicated `test(scope): cover <area> before refactor` commit per `@rules/git/general.md` Allowed Types. The pre-refactor coverage commit and the refactor commit are **always two separate commits** — never squash them and never mix new tests into the refactor commit.
3. The pre-refactor tests are the **behavior-preservation contract** for the refactor. Their **assertions must continue to pass unchanged** through the refactor commit, end to end. If a pre-existing assertion would have to change to make the refactor green, the change is **no longer a refactor** — it is a behavior change and must be split into a separate commit with its own justification (typically a `feat(scope): …` / `fix(scope): …` commit, not the refactor commit).
4. Only after the coverage gate is green and the assertions are confirmed stable may the refactor proceed.

### Refactoring steps

- Analyze the class and identify the highest-impact refactoring.
- Follow the incremental process from `@rules/refactoring/general.md` (stabilize → identify entry points → introduce Action pattern → split responsibilities → modernize → DRY → concurrency). Never propose a big-bang rewrite.
- Never fix a pre-existing bug, inconsistency, race condition, or security weakness inside a refactoring — not even in a separate commit. Keep the behaviour identical and file each discrepancy as a follow-up issue per `@rules/refactoring/general.md` *Behaviour stays identical — bugs included*. In `MODE=cr`, report it per that rule's *Code Review Application*.
- Apply focused refactoring **strictly per the applied rules** — `@rules/refactoring/general.md`, `@rules/php/core-standards.md`, `@rules/code-testing/general.md`, and (for Laravel projects) `@rules/laravel/laravel.md` + `@rules/laravel/architecture.md` + `@rules/laravel/filament.md` + `@rules/laravel/livewire.md`. The refactor rewrites the existing code into the **target architecture** (Action / Service / Repository / ModelManager / Data Validator / Data Builder / DTO per project rules) and the **target code-style** (naming, structure, parameter count, nesting, design principles). Anything that would deviate from the rules is rewritten until it complies; do not invent ad-hoc structure outside the rule set.
- Concrete refactoring activities:
  - simplify structure
  - reduce complexity
  - improve naming
  - extract responsibilities where needed
- **Test assertion logic must not change during the refactor.** The pre-refactor coverage commit fixed the contract; the refactor commit changes structure only. Pre-existing assertions, expected return values, expected exceptions, expected persisted state, and expected emitted events stay byte-for-byte the same — they are the proof that behavior is preserved. The only allowed test edits in the refactor commit are mechanical renames forced by the refactor itself (e.g. namespace move, constructor argument order forced by an extracted DTO), and they must be flagged in the commit body.
If an assertion would have to change to make the refactor green, treat that as a signal that you are no longer refactoring and split the behavior change into its own commit instead. New tests that cover newly introduced code paths belong in a separate `test(scope): …` commit *after* the refactor.
- **After the refactor — re-verify coverage stayed 100%.** Once the refactor commit is in place, run the coverage tooling again scoped to the refactored files and confirm every changed line, branch, and condition is still exercised and the pre-existing assertions still pass unchanged. Coverage must **remain** 100% — a refactored line that is no longer covered means the refactor introduced an untested path; fix the path (it is usually dead code or a new branch), never restore the number by editing the pre-refactor tests. This is the apply-mode enforcement of step 4 of the **Test Coverage Contract** in `@rules/refactoring/general.md`.
- Avoid unnecessary changes outside the scope.
- Prefer small, safe transformations over large rewrites.

---

## Refactoring Guidelines

- Ensure single responsibility per class.
- Separate orchestration from business logic.
- **Speculative interfaces:** Collapse project-owned `interface` types that have neither at least two non-test consumers nor at least two non-test implementations back into their concrete class. Test doubles, mocks, and fakes do not count toward either threshold. Implementing a framework or vendor interface (e.g. `ShouldQueue`, `HasLabel`, `Arrayable`) is always allowed. Keep a single-implementation, single-consumer project interface only when there is a documented architectural reason — a published package API surface or a plugin extension point with a written contract. See `@rules/php/core-standards.md` Design Principles.
In `MODE=cr`, raise each speculative interface the diff introduces or touches as a refactoring finding proposing the collapse into the concrete class — never perform the collapse.
- **Business Logic Layers (Laravel projects only):** Business logic must live in exactly one of the seven allowed class types — **Actions**, **Model Services**, **Repositories**, **ModelManagers**, **Data Validators**, **Data Builders**, or an **Eloquent model** (last one only for simple, self-contained own-data methods — see the boundary in `@rules/laravel/architecture.md` "Business Logic Layers").
When a class file contains business logic that spans more than one of these layers, contains business logic that does not fit any of them, or holds an Eloquent model method that crosses the simple-logic boundary (calls services / repositories / model managers, issues new queries, performs persistence side effects, or coordinates multiple entities), propose a refactoring that splits the responsibilities into dedicated classes from the seven-layer list. Surface every detected violation in the refactoring plan with the target layer for each extracted responsibility. In `MODE=cr`, the CR report replaces the refactoring plan: raise each violation the diff introduces as a finding naming the offending class and the target layer for each responsibility, instead of splitting the classes.
- Replace per-row DB queries inside loops with batch operations per `@rules/sql/optimalize.md` "Batch over per-row operations" — ModelManager `batchUpdate` / `batchInsert`, `whereIn(...)->delete()`, or a single bulk read keyed in memory. Keep per-row work only when an explicit side-effect dependency between iterations cannot be batched. In `MODE=cr`, raise each per-row query loop the diff adds or modifies as a finding proposing the concrete batch operation, instead of rewriting the loop.
- **Query performance is part of the behavior-preservation contract.** When a refactor moves, rewrites, or reshapes a SQL / Eloquent / query-builder query, the refactored query must stay **at least as fast as the original — ideally faster**, per `@rules/sql/optimalize.md` "Performance Non-Regression on Query Changes". Capture the original query's baseline (`EXPLAIN` / `EXPLAIN ANALYZE`) before the refactor and compare after. If the refactored query is measurably slower, it is **not a clean refactor** — stop, document why it is slower and the remaining optimization options (or that none exist and why), and surface the trade-off in the refactoring plan / PR description instead of shipping the regression silently.
In `MODE=cr`, raise a slower query introduced by the diff as a finding with the same reason + options requirement.
- **Runtime efficiency is part of the behavior-preservation contract.** The refactored code must stay **at least as efficient as the original** under production load: do not raise algorithmic complexity (e.g. a single pass rewritten into nested or repeated iterations over the same data), do not move work into a loop that previously ran once outside it, and do not drop memoization or recompute a value the original computed once. This clause covers non-query runtime cost only —
for SQL / Eloquent / query-builder changes the query-performance bullet above applies instead, never both on the same line. When the refactored class sits on a genuinely latency-critical path (realtime dashboards, streaming, queues, caches, execution gateways), apply `@skills/latency-critical-systems/SKILL.md` to measure the hot path before and after the refactor; for ordinary classes this bullet is a static judgment on the diff, not a measurement mandate. If a structural improvement is evidently or measurably slower, surface the trade-off in the refactoring plan / PR description instead of shipping the regression silently. In `MODE=cr`, raise an efficiency regression introduced by the diff as a refactoring finding with the same reason + trade-off requirement.
- Remove duplication (DRY). In `MODE=cr`, raise duplication the diff introduces — including duplication between added code and an existing helper — as a DRY finding with the concrete consolidation target, instead of deduplicating the code.
- Before modifying code, enumerate every place that modifies data before it is saved or passed downstream (DTO mapping, payload shaping, key renaming, default fallbacks, format normalization, business-driven derivation). Surface the list in the refactoring plan and consolidate duplicates into the canonical layer per `@rules/laravel/architecture.md` Data Modification (DRY) section (Data Builder, DTO named constructor, Data Validator, ModelManager, Repository). In `MODE=cr`, run the same enumeration read-only over the diff and raise each duplicated data-modification site as a finding with its canonical target layer, instead of consolidating it.
- Prefer small, focused methods.
- **Simplicity First.** A refactor must leave the touched code at least as simple as it found it — never trade structural clarity for unrequested flexibility. Reject any proposed step that adds an abstraction for code with a single call site, introduces a configurability / extension point not justified by an existing caller, adds error handling for impossible scenarios (catching exceptions the call surface cannot throw, defensive guards on internal values the caller already validates, fallbacks for unreachable branches), or expands a method's line count without an architectural justification anchored in `@rules/php/core-standards.md` Design Principles or, on Laravel projects, `@rules/laravel/architecture.md`.
When two refactoring options preserve behavior equally well, pick the shorter, less layered one ("if you write 200 lines and it could be 50, rewrite it"). Reuse existing helpers / Services / Actions / Repositories before extracting a new class. In `MODE=cr`, surface every such speculative addition the PR diff introduces as a refactoring proposal rather than a code change.
- Extract intention-revealing private methods when it improves clarity.
- **A refactor removes every PHP comment that is not an `@` annotation.** Renaming a variable, extracting a well-named private method, or introducing a DTO turns explanatory prose into a second, unexecuted source of truth. Delete it in the same commit. A PHP comment keeps only `@` annotations and tool directives (`@param`, `@return`, `@var`, `@throws`, `@template`, `@see`, `// @codeCoverageIgnore`), never a new suppression, per `@rules/php/core-standards.md` *Documentation*. A *why* moves to the commit message or the PR description, never into the file.
Keep the `@` annotations, and remove every other comment in the refactored region. In `MODE=cr`, raise each comment block the diff adds or modifies that carries a line which is not an `@` annotation as a **Moderate** finding, instead of deleting it. The finding proposes the code without the comment plus the rename or extraction that replaces it.
- Avoid deep nesting and complex conditionals.
- Keep method signatures clear and minimal.
- **Method parameter count (>4 → DTO):** when a method, function, closure, constructor, `__invoke()`, or other callable crosses the threshold, propose extracting a dedicated typed DTO and passing it as a single argument, per `@rules/php/core-standards.md` Structure section (parameter counting rules, exemption list, and required fix are defined there). In `MODE=cr`, raise each callable the diff adds or modifies above the threshold as a finding proposing the DTO extraction.

---

## Laravel Context (if applicable)

- Delegate business logic to Actions and Services. Simple logic that does not repeat stays where it is; never extract it into a new class (`@rules/php/core-standards.md` Design Principles → *Do not create a class for simple logic that does not repeat*).
- **Pass-through Actions (Action pattern).** Per `@rules/laravel/architecture.md` *Pass-through Action rule*, an Action whose entire `__invoke()` body is a single delegating call to one Service / Facade / Model Service method — with no orchestration of its own (no validation delegation, no DTO / data transformation, no coordination of multiple collaborators, no extra business step, no return-value reshaping) — is a redundant indirection layer and must be collapsed during the refactor. Detect every such pass-through Action touched by the refactor and resolve it one of two ways:
(1) if the wrapped Service / Facade method is used **only once** in the codebase, move its logic into the Action and delete the method (the **Single-use Service/Facade method rule**), so the Action does real work; (2) if the method is **reused** elsewhere, remove the Action entirely and rewrite the entry point to call the Service / Facade method directly (`$action($payload)` → `$service->method($payload)`), updating every call site. In `MODE=cr`, emit each pass-through Action as a written refactoring proposal (target resolution + every call site that must change) rather than applying the change.
- **Action-to-Action pass-through (Action pattern).** Per `@rules/laravel/architecture.md` *Action-to-Action pass-through rule*, the same collapse applies when the single delegated call targets **another Action** — an `__invoke()` whose entire body is `($this->otherAction)($payload)` and nothing else. An Action composing several collaborators, one of them an Action an entry point also calls, is the pattern working as intended and is left alone; an Action that only forwards to one other Action is two names for one use case.
Because an Action is a use case rather than a reusable method, the resolution is always to collapse the two into one: (1) when the outer Action is the inner one's **only** caller, merge them into the single Action whose name states the use case and delete the other; (2) when the inner Action has **other callers**, delete the outer Action and repoint its entry point at the inner one (`$outerAction($payload)` → `$innerAction($payload)`), updating every call site.
In `MODE=cr`, emit it as a written refactoring proposal rather than applying the change. **Gating — one finding per violation, never both:** this applies only when the **entire** `__invoke()` body is that single delegating call; an Action that keeps orchestration of its own around the block is the *general / reusable logic in an Action* finding instead.
- **An Action nothing outside the Action layer calls (Action pattern).** Per `@rules/laravel/architecture.md` **Actions** → *An Action is the application's entry-point contract, never a step inside another Action*, an Action whose every non-test caller is another Action is a private step of the caller's flow carrying the name of a public use case. Resolve it by deleting the inner Action and returning its body to the calling Action, or by moving it to the layer that owns the concern — a Data Validator, a Data Builder, a Repository, a ModelManager, or a Model Service an existing second flow already calls. Never resolve it into a differently named second Action.
An Action a controller, job, command, listener, or Livewire component also calls is left alone, however many other Actions compose it. In `MODE=cr`, write the resolution up as a proposal instead of applying it. **Gating — one finding per Action, never both:** when the calling Action's entire `__invoke()` body is the single delegating call, the Action-to-Action pass-through entry above owns it.
- Do not place business logic in controllers or Livewire components.
- Use existing query scopes instead of duplicating conditions.
- Prefer DTOs over raw arrays when the project uses them.
- **Chain collection operations into one fluent pipeline.** Per `@rules/laravel/laravel.md` *Collections*, rewrite a single variable reassigned step by step through successive `Collection` calls, a `foreach` that accumulates into an array what `map()` / `filter()` / `groupBy()` / `sum()` already expresses, and a pipeline that leaves the collection mid-way (`->toArray()`, an array function, `collect()` back) into one chain, broken one operation per line. A step whose closure needs more than one statement becomes a named method the chain calls. Leave an intermediate two or more later statements genuinely read — that value has a name, and re-chaining it computes it twice. In `MODE=cr`, emit the chained rewrite as a written proposal rather than applying it.
- Keep all SQL query composition in the Repository. When refactoring uncovers a Service or an Action that composes a query — it extends a `Builder` / `Relation` a Repository returned, passes a closure that receives the query builder, assembles conditions for a generic Repository method beyond an equality `*ByParams` lookup, or filters Repository results in memory in place of a query condition — move that composition into an intent-named Repository method and call the method instead (see `@rules/laravel/architecture.md` Repositories and ModelManagers section). In `MODE=cr`, raise each such composition the diff adds or modifies as a finding naming the target Repository method, instead of moving it.
- **Livewire / Blade view splitting.** When the refactor touches a Livewire component or Blade view (`app/Livewire/**/*.php`, `resources/views/livewire/**/*.blade.php`, `resources/views/**/*.blade.php`), analyze its HTML as a tree of UI concerns per `@rules/laravel/livewire.md` *HTML / Blade Layout Splitting*. Walk every trigger in that section (repeated markup, >150 Blade lines, self-contained `wire:*` cluster, self-contained data shape, cross-page reuse, independent loading / empty / error state, distinct named UI concern) and propose an extraction for each match. Pick **Livewire** children only for blocks with their own state / lifecycle / server interaction;
pick **Blade** components for stateless presentation — wrapping presentational markup in a Livewire component just to enable reuse is itself a refactoring finding. Every extracted component must satisfy the **Reusability contract** in that rule (typed input, one concern, no business logic, events not parent reach-through, independently renderable, correct tree placement, concern-based name). The layout split is a structural refactor — the **Test Coverage Gate** above applies in spirit:
every rendered branch of the touched view (initial render, `wire:loading`, `@empty`, error banner, each `@if` / `@foreach` arm) must be exercised by a Livewire / Blade feature test committed before the layout refactor, and the same feature tests must stay green through the refactor commit unchanged. PHP `--coverage-clover` does not measure `.blade.php` line-by-line, so the binding gate is feature-test parity, not a numeric coverage percentage on the view file. In `MODE=cr`, emit each matched trigger as a written extraction proposal (component type, concern, and the Reusability-contract points it must satisfy), and report missing rendered-branch feature tests as a coverage finding per the Test Coverage Gate's cr note — never author tests or commits during a CR.

---

## Testing

- **`MODE=cr`:** this section is apply-mode only — the read-only lens audits coverage per the Test Coverage Gate note and reports gaps as findings; it never authors tests or commits.
- The **Test Coverage Gate** in the Execution section is the binding rule — pre-existing target lines must be at 100% coverage *before* the refactor, written into a dedicated `test(scope): cover <area> before refactor` commit per `@rules/refactoring/general.md` Test Coverage Contract.
- Inside the refactor commit, **assertion logic of pre-existing tests must remain unchanged**. Expected return values, expected exceptions, expected persisted state, expected emitted events, and expected side effects all stay identical — they are the behavior-preservation proof. Mechanical renames forced by the refactor itself (namespace move, constructor argument shape forced by an extracted DTO) are the only allowed test edits and must be flagged in the commit body. An assertion that has to change is a behavior change, not a refactor — split it out.
- New tests covering code paths introduced by the refactor go in a separate `test(scope): …` commit *after* the refactor.
- Prefer realistic tests over heavy mocking.

---

## Output

- **`MODE=apply`:**
  - Refactored code
  - Short explanation of changes:
    - what was improved
    - why it matters
  - Summary of test coverage impact
  - Each discrepancy found and kept unchanged, with its follow-up issue URL
- **`MODE=cr`:** refactoring opportunities as markdown only (no code) — for each, the `file:line` on the PR diff, the structural problem in one sentence, the concrete consolidation step (target layer per `@rules/laravel/architecture.md`), and the rule reference it satisfies, returned to the caller.

---

## Principles

- Preserve behavior — change how, not what
- Prefer clarity over cleverness
- Prefer simple solutions over complex abstractions
- Avoid over-engineering
- Improve only what is necessary

---

## Quality gates

> Skip this entire section in `MODE=cr` — a read-only lens pushes nothing.

- **Do not run fixers or checkers here.** The project's gate runs once, immediately before the merge (`@skills/resolve-issue/references/quality-gates.md` *Gate placement — deferred to the merge boundary*), executed by `@skills/merge-github-pr/SKILL.md` *Pre-merge quality gate*, which commits the fixes it produces as their own commit.
- **Do run the tests covering the refactored surface** after each step — a refactor is behaviour-preserving by definition, so the tests are the proof of that and are not a style gate.
- When the gate later reports a static-analysis error on refactored code, it is resolved **in the code** — a refactor that ends with a `phpcs:ignore`, `@phpstan-ignore`, or any other suppression annotation in the diff has not resolved anything, and `@rules/php/core-standards.md` PHP Practices admits no exception. When restructuring cannot satisfy the analyser and no scoped tool-configuration entry fits, stop and report it rather than silencing the tool.

## After Completion

> Skip this entire section in `MODE=cr` — the CR is the caller, so chaining back into it would recurse. Return the findings to the caller and stop.

- **Run the review inline.** Invoke `@skills/code-review/SKILL.md` directly in this skill's context, passing the refactor commit range plus the instruction to return Critical / Moderate findings with their reproducer fields. Do not dispatch the review as a subagent — run it sequentially in the current context.
- Resolve findings via `@skills/process-code-review/SKILL.md` (also invoked inline per its own contract).

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
