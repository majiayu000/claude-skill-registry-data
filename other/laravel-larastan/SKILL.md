---
name: laravel-larastan
description: "Use when configuring Larastan or reading its findings in a Laravel app: which of its rules are on by default and which to opt into, how model properties are inferred from migrations, how to type builders, factories and collections so the analyser understands them, and how to handle a baseline or an ignore without hiding a real defect."
---

# laravel-larastan

Step 7 (`gate`) of the pipeline (`WORKFLOW.md`), and the typing side of step 6. `skills/laravel-conventions` §9
says that static analysis runs and that a baseline only shrinks; this block is the detail underneath:
the rule catalogue, the settings that change what the analyser can see, and the ways to feed it types.

**Special status.** New block, 🟡: never run on real work in house. Checked on 2026-10-20 against the Larastan
repository's own documentation, 3.x line (its default branch). Parameter names and defaults are version facts:
re-read `docs/rules.md` and
`docs/custom-config-parameters.md` of the pinned version before changing a setting (`skills/source-freshness`).

## When
A `phpstan.neon` is created or edited, a Larastan error needs a decision (fix, type, ignore, baseline), or new
Eloquent code (a builder, a factory, a custom collection, an accessor) is written.

## Steps
1. **Know what it is.** An extension for PHPStan that boots the application's container to resolve types only
   knowable at runtime, so it executes some of your code at analysis time. The README at the 2026-10-20 reading:
   the 3.x line needs PHP 8.2+ and Laravel 11.15+ (its version table says 11.16+ for the line, an inconsistency
   inside the page: take the stricter); Laravel 9 to 11.16 stays on 2.x and older Laravel on 1.x. The operator installs it as a dev dependency and includes its extension file in the PHPStan
   config; this block installs nothing.
2. **Default rules are on for a reason; do not switch them off to make an error go away.** Documented as on by
   default at the reading: `Model::make()` (use `new`), collection calls that a database query could answer,
   `env()` outside the config directory (it returns null when config is cached), `$appends` entries that are not
   computed properties, and the relation existence check on queries, eager loads and a model's default
   `$with` / `$withCount` (always on, no switch). The rule catalogue lists four more without stating a default
   or a parameter (dispatch argument types against the job constructor, useless `value()` and `with()` calls,
   a deferrable provider missing `provides()`): treat them as present but check the installed version.
3. **Opt into the rules that catch real production defects.** Disabled by default at the reading, each behind a
   named parameter: model property names in methods that take one (typos in `create([...])`), unique jobs
   that do not declare a lock lifetime or an id for a parameterised job, unique jobs dispatched through
   batches or bulk, queued jobs holding a model in a public property without the model-serialising trait,
   batched jobs missing the batch trait, batchable jobs that never check cancellation, and a job dispatched
   inside a transaction without deferring to commit (`skills/laravel-dispatch-after-commit`). Enable them one
   at a time and fix or baseline the first run, deliberately.
4. **Opt-in rules with a stated false-positive risk stay a choice.** The catalogue itself warns that the
   unused-views rule may report false positives; the missing-translations check cannot see translations stored in a
   database, so it stays off there (the catalogue says so); the Octane compatibility check is for apps that
   run on it; the implicit builder-call rule enforces `Model::query()->where()` over `Model::where()`.
   Turn them on when the team decided, not as a default.
5. **Help the analyser see the schema.** It reads model properties from migrations (and squashed schema
   dumps). Migrations in non-default places need `databaseMigrationsPath`; conditional migration code is
   assumed to evaluate true; PostgreSQL schema dumps parse poorly with the default parser, so either use a
   parser the docs name (installing the second SQL parser package makes it switch automatically) or generate
   migrations it can read. Schema dumps have their own path option (`squashedMigrationsPath`, default
   `database/schema`). By default only the declared return type of a `casts()` method is used; the method body is
   parsed for cast types only when `parseModelCastsMethod` is on, at a speed cost.
6. **Type the Eloquent extension points.** A custom builder (the model uses the builder trait, declares the
   builder class), a factory whose generic template is the model and which the model names, and a custom
   collection with its generic type give the analyser what it needs (the builder and collection traits are
   documented for Laravel 11+, older versions override the model methods); the docs say custom builders analyse
   better than model scopes. An attribute accessor must be a protected method returning the attribute type
   with its generic types (getter type first, setter argument second). Where a project forbids
   scopes (`skills/laravel-no-fat-models`), the builder is the typed alternative.
7. **Choose the level and hold it.** The sample config starts at level 5, and level 10 is the highest; raise it as
   the codebase allows, never lower it to pass. A raise is its own change.
8. **An ignore is a reviewed decision.** Prefer fixing, then a PHPDoc type, then a narrow ignore with the
   error identifier and a reason (`skills/code-baseline` §8 point 13; own guidance, the documentation only shows
   the line and regex forms). Blanket line ignores and loose regexes
   hide the next real error of the same shape. The one documented error to ignore is a higher-order message on a
   plain support collection; anything else is investigated first.
9. **A baseline freezes the past, not the future.** Generate it once for a legacy codebase; the diff must not
   add entries (`skills/laravel-verification`). A memory-limit failure is fixed with the memory option, not by
   narrowing the analysed paths.

## Output / checkpoint
Analysis passes at the project's level with no new baseline entry and no new ignore without a reason; each
enabled optional rule is named in the config with the decision that enabled it. Checked at `gate` (7).

## Guardrails
No comments in the code produced. Do not edit the baseline to hide a finding the diff introduced. A rule
turned off to make a build green is reported, not applied.

## Origin
Rewritten from the Larastan repository documentation (`larastan/larastan`, MIT per repository metadata, 3.x
line, read 2026-10-20): the README (requirements, support matrix, config skeleton, memory limit, ignoring and
baseline), `docs/rules.md` (25 rules with defaults and parameters, every opt-in name in step 3 matched),
`docs/custom-config-parameters.md`, `docs/features.md` (builders, factories, collections, accessors) and
`docs/errors-to-ignore.md`. Not covered by the configuration page and therefore sourced to the rule catalogue
only: the Octane, unused-views, missing-translations and implicit-builder options. Independent verification 2026-10-21: 20 checked, 17 matched, 3 corrected (casts() body versus return type, the scale wording, the translations remark was documented), 0 unverified. Own guidance: the baseline
discipline of steps 7 to 9 beyond what the README shows, and the "diff must not add entries" rule. Mechanisms
only, rewritten in our words. Version-sensitive: rule names, parameter names and defaults.
