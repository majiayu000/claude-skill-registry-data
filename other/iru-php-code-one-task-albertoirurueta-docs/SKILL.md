---
name: iru-php-code-one-task
description: >-
  Implement a single task from a PHP `implementation_plan.md`-style task list — the implementation, its tests, and
  its checkbox update. Detects the project's flavor with the same markers as `iru-explore` and
  `iru-php-code-quality` (Laravel application, WordPress plugin, WordPress theme including block themes,
  PrestaShop module, or plain Composer library), its PHP floor, its style tooling (Pint, PHP-CS-Fixer, PHPCS with
  WordPressCS), and its test runner (Pest or PHPUnit, and which suites are fast vs. integration), then loads only
  the matching guidance from this skill's own `reference/` directory — this catalog's PHP code agreements
  (PER-CS 3.0 unless the project's formatter says otherwise, `declare(strict_types=1)` where the project uses it,
  PSR-4, native types, enums/`match`/readonly, `final` by default, no closing tag, PHPDoc only for what native
  types can't express), testing rules (follow the project's Pest-or-PHPUnit choice, attributes, `assertSame`,
  fakes over mocks, one test class per class, data providers), security rules (escape on output, prepared
  statements, allow-lists, password hashing, CSRF, uploads, SSRF), and exactly one flavor file (Laravel thin
  controllers/Form Requests/policies/actions/Eloquent/queues; WordPress prefixing, hooks, nonces plus
  capabilities, sanitize/escape, `$wpdb->prepare`, REST `permission_callback`, i18n, enqueueing, block themes and
  `theme.json`; PrestaShop module class, hooks, `Configuration`, `pSQL`/`DbQuery`, upgrade scripts, Symfony
  controllers, translations), plus — when the task adds or changes a screen, component, list or other UI — the
  catalog's UI contract and its server-rendered mapping (screen › region › component decomposition, Blade/Livewire
  components, blocks, Smarty/Twig partials, paginated collections with one item component, Playwright UI tests
  with a left-to-right/right-to-left × light/dark screenshot matrix and axe checks, written but never run here).
  Re-checks the current code state, implements exactly what the task specifies,
  writes or updates tests, runs only the fast tests it touched (never coverage, the full suite, or anything that
  needs Docker, a database server, wp-env, or a PrestaShop shop), then checks off this task's own checkbox in
  `implementation_plan.md` with a "group validation pending" note and hands back a short summary. Does not
  capture a quality baseline, add license headers, audit PHPDoc, or run coverage/quality checks — those happen
  once per task group in `iru-php-code-one-task-group`, which invokes this skill once per task. Invoke as
  `/iru-php-code-one-task <task description>`, passing the task's own text including its exact
  `implementation_plan.md` checkbox line(s). The PHP counterpart to `iru-typescript-code-one-task` and
  `iru-java-springboot-code-one-task`.
model: sonnet
allowed-tools: Read Edit Write Bash(php *) Bash(vendor/bin/*) Bash(./vendor/bin/*) Bash(composer dump-autoload*) Bash(composer show *) Bash(./vendor/bin/sail ps*) Bash(./vendor/bin/sail test *) Bash(./vendor/bin/sail bin *) Bash(ddev exec *) Bash(docker info *) Bash(command -v *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(mkdir -p build*) Bash(rm -f build/iru-php-*)
---

# Implement one plan task (PHP)

Carry out a single task's implementation, tests, and checkbox update against the real codebase — nothing else.
This is the narrowest execution unit for a PHP project in the `iru-code` pipeline: `iru-php-code-one-task-group`
calls it once per task in a bucket (potentially several at once, in parallel agents), then handles license headers,
PHPDoc, coverage, code quality, the full suite, and any container-backed integration tests itself, once for the
whole bucket. It uses a medium model on purpose — the plan already carries the hard reasoning; this skill executes
one task against code agreements that live in `reference/` rather than being re-derived per task.

PHP projects vary more by flavor than by language: a WordPress hook callback, a Laravel controller, and a
PrestaShop hook method look nothing alike, and each ecosystem has its own coding standard and security API. Getting
the flavor right first is what keeps the rest of this skill cheap.

## Step 1 — Detect the flavor and toolchain, then read only the reference this task needs

Detect, once, before reading any reference file:

1. **Flavor** — the same markers `iru-explore` uses for its `Project type:` line and `iru-php-code-quality`/
   `-phpdoc` use for theirs, first match wins:
   - `laravel/framework` in `composer.json` `require` **and** an `artisan` file at the root → **laravel**.
   - A root-level PHP file whose header comment carries `Plugin Name:`
     (`grep -l '^[ \t/*#@]*Plugin Name:' *.php`) → **wordpress-plugin**.
   - `style.css` whose header carries `Theme Name:`, and/or a `theme.json` → **wordpress-theme**.
   - A root `<module>.php` with a class that `extends Module` (or `PaymentModule`/`CarrierModule`), a
     `config.xml`, and/or `prestashop/*` packages in `composer.json` → **prestashop-module**.
   - Anything else with a `composer.json` → **library**.

   In a monorepo, apply the markers to the directory the task's files live in (a `wp-content/plugins/<slug>/`, a
   `modules/<name>/`), not the repository root.
2. **PHP floor** — `require.php` in `composer.json`, else the plugin/theme `Requires PHP:` header, else
   PrestaShop's supported range for `ps_versions_compliancy`. Don't use syntax above it (`code-style.md`).
3. **Style tooling** — `pint.json`/`laravel/pint`, `.php-cs-fixer.dist.php`, `phpcs.xml(.dist)` and the standards
   it references (`code-style.md`'s first table).
4. **Test runner and suites** — `pestphp/pest` vs. `phpunit/phpunit` in `require-dev` (and the PHPUnit major in
   `composer.lock`: attributes on 10+, annotations on 9), the PHPUnit config(s) (`phpunit.xml`, `phpunit.xml.dist`,
   `phpunit-unit.xml`, `tests/phpunit.xml`, …) and their `<testsuite>`s. Classify each suite **fast** (no external
   service: plain unit tests, Brain Monkey/WP_Mock tests, Laravel feature tests on SQLite `:memory:`) or
   **integration** (`WP_UnitTestCase`, Laravel tests whose `phpunit.xml`/`.env.testing` points at
   MySQL/PostgreSQL/Redis, PrestaShop shop-backed bootstraps) — the same split `iru-php-test` Step 3 uses.
5. **Where PHP runs** — host `php` (`command -v php`, version satisfying the floor) or the project's container
   (`.ddev/config.yaml` → ddev; `vendor/bin/sail` + a Sail compose file → Sail). Only Step 6 needs it.

Then read `reference/README.md` first — it is short and routes you to the rest — and read only what it points at.
The routing, restated:

| Read | When |
|---|---|
| `reference/code-style.md` | **Always.** |
| `reference/testing.md` | The task writes or updates tests — nearly every task, since Step 5 is part of implementing it. |
| `reference/security.md` | The task touches request input, rendered output, SQL, files, outgoing HTTP, auth/sessions, or secrets — always for a controller, hook callback, form/AJAX/REST handler, or template. |
| `reference/laravel.md` | Flavor is **laravel**. |
| `reference/wordpress.md` | Flavor is **wordpress-plugin** or **wordpress-theme**. |
| `reference/prestashop.md` | Flavor is **prestashop-module**. |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | The task adds or changes a screen, component, list or other UI — Blade/Livewire views, blocks, patterns, template parts, `.tpl`/`.twig` templates, or their CSS/JS assets. |

Read exactly one flavor file — none for **library** (and no UI files for a library either). If `reference/` is missing (e.g. the skill directory was
copied without it), proceed using this repository's own `CLAUDE.md` conventions and the surrounding code's style,
and say so in Step 8's report — don't guess at what the reference would have said.

## Step 2 — Re-check the current code state

Read the actual current content of the file(s) the task touches before editing — don't assume any "current code
state" notes passed in with the task are still accurate; other tasks in the same bucket may be landing
concurrently, or the file may have changed for unrelated reasons.

Also read one or two neighbouring files in the same directory and note what they do about the things `reference/`
has opinions on: `strict_types`, `final`, WPCS vs. PER layout, `$fillable` vs. `#[Fillable]`, attribute vs.
annotation test metadata, how errors are surfaced (exceptions, `WP_Error`, `false`), the plugin's prefix and text
domain, the module's translation domain. The reference's rules are the default for new code; a directory that
consistently does something else wins (README rule 1) — **except on security**, where new code follows
`security.md` and the flavor file regardless, and the insecure neighbour goes in Step 8's report.

## Step 3 — Implement exactly what the task specifies

The named file(s), the described class/function/hook/route/template, the behavior. Apply `reference/code-style.md`,
`reference/security.md` where routed, and the flavor file, plus this repository's own `CLAUDE.md` conventions where
they are more specific (PHP version, license header, banned functions or packages, Laravel Boost guidelines).

Non-negotiable, because a later gate or reviewer enforces them:

- **Every input validated or sanitized, every output escaped for its context, every SQL value bound** — with the
  flavor's own API (`security.md` + flavor file). Every state-changing handler checks CSRF (CSRF middleware /
  nonce / PrestaShop token) **and** authorization (policy / capability / employee access).
- **Native types on everything new**; PHPDoc only where native types can't express the contract (generics, array
  shapes, `@throws`) — plus the fuller docblocks WordPress (`@since`) and PrestaShop (every member) require.
- **Names the platform requires**: WordPress prefix and literal text domain on every global name and string;
  PrestaShop `Configuration` keys, tables, and translation domains prefixed with the module name; PSR-4 paths that
  match `composer.json`.
- **No new Composer dependency, no new migration/upgrade script, no `phpunit.xml`/`phpstan.neon`/`phpcs.xml` edit**
  unless the task explicitly calls for it. A schema or hook change in a PrestaShop module that the task *does* ask
  for needs its `upgrade/upgrade-<version>.php` and version bump in the same task (`prestashop.md`); a Laravel one
  needs a new migration, never an edit of an old one.
- **No debugging leftovers** (`dd`, `dump`, `var_dump`, `print_r`, `ray`, `error_log`) and no `?>` at the end of
  a pure-PHP file.

If a new class lives under a new PSR-4 namespace root, that's a `composer.json` change (only if the task asks); for
a class under an existing root, `composer dump-autoload` is only needed if the project uses a classmap — PSR-4
resolves new files on its own.

For UI work (`ui-contract.md` + `ui-implementation.md`): **decompose first** — write the `Screen › Region ›
Component` tree (inputs, events, visual states, what each reuses) before touching a template, search for an
existing component before creating one, build leaves first, keep queries and permission logic out of templates,
and render every collection through a bounded paginated query plus one item component. The tree goes in Step 8's
report.

Don't add anything the task didn't ask for — no speculative abstraction, no unrelated cleanup, no restyling of code
the task doesn't touch.

## Step 4 — When to interrupt the user

Keep interruptions rare — most tasks should complete unattended. Stop and use `AskUserQuestion` (or plain text if no
real choice is being offered) only when:

- The task is ambiguous in a way that changes correctness or scope and can't be safely inferred — conflicting
  instructions, or a decision only the user can make (which capability gates an action, whether a PrestaShop
  change must still support 8.x). Don't ask about anything with an obvious best-practice answer.
- The task's approach is infeasible against the real code (it names a class, hook, route, or table that doesn't
  exist and isn't a trivial typo).
- **The task as written would require insecure code** — echoing unescaped input, string-built SQL with request
  data, a state-changing GET, an endpoint with no authorization check, a REST route with
  `permission_callback => '__return_true'` that writes data. Report it with the secure alternative; don't
  implement the insecure version, and don't silently implement something different either.
- Flavor detection in Step 1 is genuinely ambiguous (a Laravel app vendoring a WordPress install, a repository
  holding both a plugin and a theme) in a way that changes which reference file and conventions apply.

Do not stop merely because the task is nontrivial — implement it. Do not report the task done to work around a
blocker; report it as blocked (Step 8) with what was tried, what failed, and why.

## Step 5 — Write or update the tests

Follow `reference/testing.md`, the flavor file's test section, and the existing tests in the same directory —
runner (Pest or PHPUnit), base class, naming, attribute vs. annotation metadata, which doubles the project uses
(framework fakes, Brain Monkey/WP_Mock, Mockery, PHPUnit stubs). Cover the new/changed behavior, every documented
`@throws`/`WP_Error`, the validation-failure and unauthorized paths of anything handling input, and the meaningful
boundaries. Put each test in the suite that matches what it needs: a test that boots WordPress or a shop, or needs
a real MySQL, goes into the project's integration suite, never the fast one.

For UI work, also write the browser UI specs `ui-implementation.md` describes (`tests/e2e/specs/<Name>.spec.ts`,
through the shared `tests/e2e/support/ui-screenshots.ts` helper): each visual state with the contract's data sets,
behaviour asserted once (left-to-right, light), a screenshot per state × `.ui-quality.yml` directions × themes
under `.ui-screenshots/<kind>/<Id>/`, and the axe check at the configured level. Follow Dusk/Pest browser tests
instead where the repository already uses them. **Write them, never run them** — they need a browser plus a
server, wp-env or shop; the group runs them behind its integration lock. If the project has no Playwright setup and
the task doesn't ask for one, write none and say so in Step 8.

If the project has no test setup at all for this flavor (common for small WordPress plugins and PrestaShop
modules), don't scaffold one — that's a plan-level decision. Write nothing, and say so in Step 8 so the group's
coverage gate failure has an explanation.

## Step 6 — Run only the fast tests this task touched

Run the fast test file(s) you wrote or changed, scoped by path — nothing more:

```bash
mkdir -p build
vendor/bin/pest tests/Unit/Billing/FineCalculatorTest.php                 # Pest
vendor/bin/phpunit -c <fast config if not the default> tests/Unit/Billing/FineCalculatorTest.php   # PHPUnit
php artisan test tests/Feature/BookStoreTest.php                           # Laravel, SQLite :memory: suite
```

Use the environment prefix Step 1 found (`./vendor/bin/sail test …`, `ddev exec vendor/bin/phpunit …`) only if its
containers are **already running** (`./vendor/bin/sail ps`) — never start them from here. If no usable PHP or no
`vendor/` exists, skip the run and say so in Step 8; the group runs the tests anyway.

**Never run, by any means:** a `WP_UnitTestCase` suite, `npx wp-env …`, `bin/install-wp-tests.sh`, a browser UI
test (`npx playwright test`, `npm run test:e2e`, `wp-scripts test-playwright`, Dusk, Pest browser tests), any test
whose suite needs MySQL/PostgreSQL/Redis or a PrestaShop installation, coverage (`--coverage*`, `XDEBUG_MODE=
coverage`, `pcov.enabled=1`), `--parallel`, `--mutate`, the whole suite (a bare `vendor/bin/pest` /
`php artisan test` with no path), or any static-analysis/formatter tool. Several of these agents run concurrently;
the integration stack is serialized behind the group's lock, and everything else is validated once per bucket.

If a test fails, fix the implementation or the test and re-run until green — don't hand back a red test. If the
behavior genuinely can't be verified without WordPress/a shop/a real database, write the integration test (unrun),
write whatever unit test *is* meaningful, and say so in Step 8. Do not delete an assertion to make a file pass.

## Step 7 — Check off this task's checkbox now

If this task did not stop on a blocker (Step 4), update `implementation_plan.md` at the repository root before
reporting back — don't leave this for the caller. Re-read the file fresh (not any earlier cached view — other tasks
in the same bucket may be landing concurrently) and locate this task's own checkbox line by the exact text passed
in with the task. Flip its `[ ]` to `[x]`, and do the same for every sub-task checkbox covered by the work just
completed, adding a short note naming the files touched, e.g.:

```
- [x] Task 2. **Add `acme_loans_handle_save` admin-post handler** — includes/admin/class-loan-form.php; Brain
  Monkey unit tests added (passing), WP_UnitTestCase test added (unrun); group validation pending.
```

The "group validation pending" wording is what `iru-php-code-one-task-group` expects, since coverage, quality, and
integration outcomes aren't known until it validates the whole bucket. Edit only this task's own line(s) — never
rewrite surrounding lines or other tasks' checkboxes, since sibling tasks in a parallel bucket may be editing the
same file at nearly the same moment.

If this task stopped on a blocker instead, leave its checkbox untouched — there's nothing finished to mark done.

## Step 8 — Report the outcome

Hand control back to the caller with a short summary:

- **The flavor Step 1 detected** (library/laravel/wordpress-plugin/wordpress-theme/prestashop-module), the PHP
  floor, the runner, and the reference file(s) actually read.
- **The file(s) touched** and **the tests added/updated**, split into fast tests (with Step 6's result, or why
  they weren't run) and integration tests (written, not run — the group runs them).
- **For UI work**: the `Screen › Region › Component` tree from Step 3, and the UI specs added (screens/components
  and states covered — written, not run), or why none were written.
- **Whether this task stopped on a blocker** per Step 4, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`** — e.g. no `strict_types` to match the directory, WPCS layout,
  `$fillable` on Laravel 12, PHPUnit 9 annotations, a non-`final` class because Mockery doubles it — and any
  **insecure neighbouring code** noticed and left alone. Say so here too if `reference/` was missing (Step 1) or the
  project had no test setup (Step 5).

This is what `iru-php-code-one-task-group` records for this task before its own consolidated
license/PHPDoc/test/coverage/quality/integration validation across the whole bucket; this skill has already checked
off its own checkbox with a pending-validation note (Step 7). It never captures a quality baseline, adds license
headers, runs coverage or code-quality checks, runs the full suite, or runs any integration test.
