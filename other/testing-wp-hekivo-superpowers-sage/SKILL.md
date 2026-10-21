---
name: testing-wp
description: Use when writing, running or fixing tests on a Roots/Acorn WordPress project - PHPUnit, Pest, tests/bootstrap.php, WordPress function stubs ("Call to undefined function" in a test), Playwright specs, "run the tests", "is it done", and which runner command runs them. For static analysis use wp-phpstan; for a failing page use roots-debugging.
---

# Testing a WordPress project on Acorn

Pick the cheapest level that proves the behaviour, run it through the project runner, and report only what you observed.

Runner placeholders (`{{runner.test}}`, `{{runner.node}}`, `{{runner.wp}}`, `{{runner.composer}}`, `{{runner.cache}}`) come from the session context. `{{runner.test}}` is the profile's PHP test command (PHPUnit or Pest). On Lando the default is a tooling command such as `lando phpunit` or `lando pest`; `lando-wp` explains the wiring.

## When to use

- Adding tests for a service, provider, view composer, block class, REST endpoint or Blade component.
- A test fails with an undefined WordPress function, a container error or a database error.
- Setting up or running Playwright specs, headless or headed.
- The user asks whether a change is done: this skill defines the minimum evidence.

Not for lint rules or type analysis (`wp-phpstan`, the project's formatter), and not for diagnosing a broken page that has no test (`roots-debugging`).

## Inputs required

1. Profile and Acorn base path (session context).
2. Which test tooling the project has: `phpunit.xml` or `phpunit.xml.dist`, `tests/bootstrap.php` or `tests/Pest.php`, `playwright.config.*`, the `composer.json` scripts. Read them first; follow the project's conventions rather than introducing a second runner.
3. Whether a browser can run where you are (containers usually have no display).
4. Whether the target environment is local. Tests that hit a real environment, create real accounts or send real mail run only when the user asks.

### Test levels per profile

| Level | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Static / lint | formatter and static analysis through their runners | same | project formatter and linter scripts (`composer.json` scripts) |
| Unit, no WordPress | PHPUnit if the theme has it; keep logic in plain classes under `app/` | PHPUnit with a bootstrap that does not boot WordPress; WordPress functions are stubbed | rarely needed; Pest tests are normally integration |
| Integration, WordPress booted | `{{runner.wp}} eval` or `eval-file` smoke scripts | same, or the WordPress core test library if the project adopts it | Pest, whose bootstrap loads WordPress and Acorn and runs against the configured database |
| HTTP / REST | Playwright `request` tests or `curl` | same | same, or Pest feature tests |
| Browser / visual | Playwright | Playwright | Playwright |

Native-first: for WordPress behaviour (hooks, REST routes, capabilities) the native tool for integration tests is WordPress's own PHPUnit test library with its separate test database. Use it when the project already does or when isolation matters. Do not invent a new in-house harness when one of the existing ones fits.

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Discover.** Read the test config and one existing test of the kind you are about to write. Match its naming, namespace and assertions.
2. **Choose the level.** Pure data shaping, validation, middleware rules and services: unit. Anything that needs real hooks, the database or rendered output: integration or browser.
3. **Unit tests without WordPress (mu-plugin style).**
   - The bootstrap defines the constants the code reads, registers stubs for WordPress functions **before** the Composer autoloader (so framework helpers do not win), then loads the autoloader. No WordPress, no Acorn boot.
   - When a test needs another WordPress function or class, add a stub to the bootstrap guarded with `function_exists` or `class_exists`. Do not boot WordPress to avoid writing a stub.
   - Keep logic in small methods that do not call WordPress directly, so the test needs few stubs. For classes whose constructor needs the framework, create them with `ReflectionClass::newInstanceWithoutConstructor()` and test protected helpers through `ReflectionMethod`.
   - Details: [references/unit-without-wordpress.md](references/unit-without-wordpress.md).
4. **Integration tests with WordPress booted (Radicle style).** Read [references/pest-wordpress.md](references/pest-wordpress.md) before writing: these run against a real database.
5. **Browser tests.** Read [references/playwright.md](references/playwright.md): base URL, projects, headed runs on the host, API request tests, visual checks.
6. **Run.** Execute the narrowest command first (a filter on the test class or name), then the whole suite: `{{runner.test}} --filter <Name>` then `{{runner.test}}`. Read the output, not only the exit code.
7. **Before reporting done.** Run, in this order, whatever the project defines: formatter/linter check, `{{runner.test}}`, the asset build when CSS or JS changed (`{{runner.node}} run build`), and `{{runner.cache}}` if PHP registration code changed. State which you ran and the result.
8. **Never** claim a pass you did not observe; say so when a level could not run (no browser, no database).

## Verification

- The new test fails for the right reason before the fix (when fixing a bug) and passes after.
- The test fails when you break the behaviour on purpose (revert the line, expect red). A test that cannot fail proves nothing.
- The whole suite is green through `{{runner.test}}`, not only your file.
- The final report lists commands run and results, and names anything skipped and why.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Call to undefined function get_option()` (or any WordPress function) in a unit test | The unit bootstrap does not load WordPress | Add a guarded stub in the bootstrap, or move the call behind a small method the test does not exercise |
| Framework helper `__()` or `app()` behaves unexpectedly in tests | Stub declared after the Composer autoloader, so the framework helper was defined first | Declare stubs before `require vendor/autoload.php` |
| `Target class [x] does not exist` or empty container | Test relies on a booted Acorn application | Build the needed object by hand, or move the test to the integration level |
| Eloquent model fails with no connection | No database in the unit bootstrap | Configure an in-memory SQLite connection in the bootstrap for model scopes; use the booted suite for anything WordPress-specific |
| Integration test changes or deletes real data | The suite runs against the development database | Create and remove your own records inside the test; use a dedicated database where the project provides one; never run destructive tests unasked |
| Pest or PHPUnit not found through the runner | The tool is not installed for that Composer project (nested app has its own `vendor/`) | Install it in the right `composer.json` with `--working-dir`, or call the runner pointing at the correct config file |
| Playwright cannot launch a browser in the container | No browsers or system libraries installed, no display | Install browsers once, run headless in the container, run headed on the host |
| Playwright passes locally, fails against a remote | Edge or page cache serving old HTML, or different data | Check response headers; use the project's cache-bypass option if it has one |
| Spec creates real accounts or sends data to third parties | A "live" project or spec ran by default | Keep live specs in a project that must be selected explicitly; run only on request |
| `acorn test` is missing | The installed Acorn does not register a test command in this setup | Call the test runner binary directly through `{{runner.test}}` |

## Escalation

- A test that needs secrets or a real environment: ask the user for the environment and credentials source; never write secrets into specs or `.env` files.
- Changing the CI configuration or adding a new test framework: propose and wait for approval.
- Flaky browser tests: capture a trace and stop after two failed fixes; report the evidence.

<!-- verified: tests/bootstrap.php in the reference acorn-mu-plugin project — stubs before vendor/autoload.php, container shim, in-memory SQLite capsule, WP_Post stub class;
its phpunit.xml.dist — suite by directory, bootstrap tests/bootstrap.php, no WordPress boot;
its playwright.config.js — baseURL from env var with local default, headless unless E2E_HEADED, optional env file, live specs excluded from the default project;
its package.json — pw:install, pw:test scripts;
vendor/roots/acorn/src (6.2) — ArtisanServiceProvider registers ScheduleTest only; no TestCommand class (docs list `acorn test`);
refs/roots-docs/acorn/wp-cli.md — lists the `acorn test` command;
radicle-app facts checked against a licensed local Radicle project; not reproduced here;
lando wp acorn list (the reference acorn-mu-plugin project) — no test command listed;
unverified: WordPress core test library (WP_UnitTestCase) setup, not present in the local sources -->
