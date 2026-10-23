---
name: laravel-pest
description: "Use when a Laravel project already runs Pest and the task goes past plain tests: architecture tests, datasets, mutation testing, type coverage, parallel runs and sharding, and picking a named assertion. Not a reason to move a PHPUnit project to Pest."
---

# laravel-pest

Step 5 (`tdd`) of the pipeline (`WORKFLOW.md`), the Pest-specific half of `skills/laravel-conventions` §9
(tests and static analysis). It assumes the project **already** uses Pest: the choice of runner is a project
decision (some houses are PHPUnit-only, and then this block does not apply).

**Special status.** New block, 🟡: never run on real work in house. Re-checked on 2026-10-20 against the
documentation repository's 5.x branch (its default branch). Pest majors move fast (Pest 5 is dated 2026-07-28
in its support policy); confirm against the installed major (`skills/source-freshness`).

## When
A `tests/Pest.php`, an `arch()` expectation, a `->with(...)` dataset, a `--mutate` or `--type-coverage` run,
CI sharding, or a test suite that is slow or order-dependent.

## Steps
1. **Check the major against PHP.** The support policy ties each major to a minimum PHP (at the reading:
   Pest 5 needs 8.4, Pest 4 needs 8.3, Pest 3 needs 8.2) and gives bug fixes for the previous major for twelve
   months after the latest release (support policy page, 5.x branch; the older 3.x-era branch said two years, so
   read the branch that matches the installed major). A project below the line upgrades the runner or stays on its major; it does not mix.
2. **Architecture tests state conventions as code.** `arch()->expect('App\Models')->toExtend(...)`,
   `->not->toUse(['die', 'dd', 'dump'])`, `->toOnlyBeUsedIn(...)`, `toUseStrictTypes()`, `toBeFinal()`,
   `toHaveSuffix()`, `toHaveLineCountLessThan()`. This is how `skills/code-baseline` §8's "name the
   enforcing line" is done for a layering rule: a direction that must hold (a low layer never importing a
   higher one, `skills/laravel-conventions` §10) becomes a failing test, not a sentence. Wildcards
   (`App\*\Traits`) arrived in 3.8.
3. **Presets are a starting set, not the rule.** `php`, `security`, `laravel`, `strict`, `relaxed` and a custom
   preset a team defines. Read what a preset enforces before enabling it (the `strict` preset makes classes
   final, which conflicts with a house that extends); use `ignoring()` for a named exception with a reason
   (own guidance: the reason). The `laravel` preset expects controllers to expose only the seven conventional
   resource methods as public methods and to carry the `Controller` suffix.
4. **Datasets replace copy-pasted tests.** Key a dataset so the test name says which case failed; use named
   keys so parameters bind by name regardless of order; closures in datasets need typed test arguments;
   shared datasets live in the datasets directory; a dataset that needs the database is a bound dataset
   (closures resolved after `beforeEach`), with a typed parameter. One test per behaviour, many rows: not one
   row per test.
5. **Mutation testing measures whether tests would notice a change.** Declare what a test covers with
   `covers()` or `mutates()`, run `--mutate` (add `--parallel`), read each `UNTESTED` diff, and write the
   assertion that kills it (a status check that never looked at the body is the typical survivor). Needs
   Xdebug 3 or PCOV. Gate with `--min=<score>`; exclude lines that are noise with the ignore annotation
   rather than lowering the bar. It is a review tool for the tests the diff added, not a number to chase
   across a legacy suite (`skills/code-baseline` §0).
6. **Type coverage checks declarations, not tests.** The plugin's `--type-coverage` with `--min` finds
   parameters, returns and properties missing a type; the ignore annotation is for a line the language cannot
   type. It complements the static analyser (`skills/laravel-larastan`), it does not replace it.
7. **Parallel and sharded runs need independent tests.** Each process gets no shared database state and no
   order guarantee; a test that depends on another test's data fails only in parallel. `--profile` names the
   slowest tests before anyone parallelises. In CI, time-balanced `--shard` uses a committed timing file that
   `--update-shards` regenerates; a stale file still runs every test, with a warning.
8. **Pick the assertion for the subject.** A response gets a named response assertion (`assertNotFound()`, not
   `assertStatus(404)`), a database fact a database assertion, a model's existence `assertModelExists`, a plain
   value an `expect()` chain; one chain per subject; the expected value is written in the test, never computed
   with the code under test. A write is asserted completely: response, stored state, dispatched jobs and
   events, sent mail and notifications, and on the failure path that none of them happened. Confirm an
   expectation exists in the documentation before using it.
9. **A skipped or todo test is a visible debt**, never a way to turn a build green
   (a check that runs on every edit can refuse them).

## Output / checkpoint
New tests use named assertions and datasets where rows repeat; a layering rule that matters is an `arch()`
expectation; the diff's new behaviour survives `--mutate` on its own tests when the project runs mutation
testing. Checked at `gate` (7).

## Guardrails
No comments in the code produced. Never edit a mutation or coverage threshold as a side effect. Do not add
Pest, a plugin or a preset to a project that did not choose it; name the dependency and stop
(`CONVENTIONS.md`).

## Origin
Rewritten from the Pest documentation repository (`pestphp/docs`, MIT, LICENSE read 2026-10-20, 5.x branch):
architecture testing (expectations, presets, `ignoring()`, wildcards since 3.8), datasets (keys, parameter
binding by name, typed closure arguments, `tests/Datasets`, bound datasets), mutation testing (`covers()` and
`mutates()`, `--mutate`, `--parallel`, `--min`, `@pest-mutate-ignore`, Xdebug 3 or PCOV), type coverage (a
separate plugin; `--type-coverage`, `--min`, `@pest-ignore-type`), optimizing tests (`--parallel`, `--profile`,
`--shard`, `tests/.pest/shards.json`, `--update-shards`) and the support policy table; and the
`testing-best-practices` rule files of Laravel Boost (`laravel/boost`, MIT, LICENSE read 2026-10-20) for named
assertions, known-value assertions and complete-result assertions. Every figure in steps 1 to 8 was re-opened
and matched on 2026-10-20. Own guidance, not a documentation statement: step 6's "complements the static
analyser", step 9 (skipped and todo tests, absent from both sources), and the advice to confine mutation runs
to the diff's tests. Mechanisms only, rewritten in our words.

Independent verification 2026-10-21: 16 checked, 16 matched, 0 corrected, 0 unverified.
