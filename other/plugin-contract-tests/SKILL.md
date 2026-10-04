---
name: plugin-contract-tests
description: Sets up, regenerates or debugs the shared MyAdmin plugin contract harness for this package — tests/ContractTest.php, the contract inspectors, and `composer myadmin:scaffold-tests`. Use when the user says 'add tests to this plugin', 'set up the harness', 'scaffold tests', 'why is ContractTest failing', or when deciding whether a contract failure is the plugin's fault or the harness's. This is a type=service package, so the service lifecycle assertions apply too. Do NOT use for this package's own non-plugin classes — its other testing skills cover those.
---
# Plugin contract tests

The class under contract here is `Detain\MyAdminParallels\Plugin`.

## Critical

- **Never hand-write or hand-edit `tests/ContractTest.php`.** It is generated. Run
  `composer myadmin:scaffold-tests` from inside this repo; regenerate with `--force`. A hand
  edit is invisible to the next regeneration and to the next person.
- **Never write a reflection-only test for the plugin class.** Asserting that a handler exists,
  is static and takes one parameter passes whether or not the handler works. Execute it. The
  harness has already done the hard part — priming the constants that used to make that
  impossible.
- **Never delete an existing test to make room.** The harness is strictly additive: `ContractTest`
  runs *alongside* whatever this package already had. Duplicate coverage is the cheaper mistake.
  Removing anything is a question for the owner first — that is a standing rule on this fleet.
- **Run the whole suite, never just `--filter ContractTest`.** The contract class primes constants
  and calls `register_module()`, neither of which can be undone, so it can change how this
  package's *other* tests behave. A filtered run cannot show that.
- **`composer myadmin:scaffold-tests` does not exist in MyAdmin core.** Core sets
  `config.allow-plugins: false`, so Composer never activates the installer there and no
  `myadmin:*` command is registered. Run it from this repo.
- This package declares `$module = 'licenses'`. Changing it detaches the plugin from the events core dispatches to it, so the generated pin asserts it.

## Instructions

### Step 1 — regenerate, do not edit

```bash
composer myadmin:scaffold-tests            # plan only; writes nothing
composer myadmin:scaffold-tests --write    # create what is missing
composer myadmin:scaffold-tests --force --write   # also re-emit tests/ContractTest.php
```

`CREATE` means a file is missing. `KEEP` means one exists and will not be touched. `DRIFT`
means an existing `phpunit.xml.dist` is missing a setting the harness depends on.

If Composer deadlocks, this package still vendors installer `v2.0.2`, which predates Composer
2's `PluginInterface` and fatals while activating — break it once with `composer update
--no-plugins`.

### Step 2 — fix a reported DRIFT by hand

The three settings are load-bearing, not stylistic:

- `failOnWarning="true"` — several findings surface first as a PHP warning; without it PHPUnit
  prints the finding and exits 0.
- `failOnRisky="true"` — a test asserting nothing because its subject would not load is risky,
  not passing.
- `beStrictAboutOutputDuringTests="true"` — assertion B-15 (a plugin must not echo while its
  handlers run) is unenforceable without it.

### Step 3 — classify a failure before changing anything

This decides *which repository you touch*, so do it first:

| symptom | verdict | action |
|---|---|---|
| the plugin genuinely does the wrong thing — uses a variable before assigning it, constructs a class with the wrong arity, registers a requirement path that does not exist | **P-bug** | fix in this repo, on its own branch, with its own review. Do not bundle it into a test-scaffolding commit |
| the harness accuses the plugin of something it did not do | **H-bug** | fix in `detain/myadmin-plugin-installer`, never here, and add the counter-test proving the inspector can still fail |
| the blocker is the environment — a `require` of a path that only exists inside a MyAdmin checkout | neither | the inspector should *skip*, naming the blocker. If it fails instead, that is an H-bug |

Three H-bugs have shipped, and all three were the harness falsely accusing a plugin: a shadowed
observer read as dead code (v2.1.1), a failed `require` read as the handler's own logic (v2.1.2),
and a Windows path treated as relative so every package looked like it shipped no templates
(v2.2.1). **Suspect the harness first** when a verdict changes depending on how the suite was
launched, or when a finding fires on every package at once.

### Step 4 — if the generated file is wrong, change the generator

`src/Testing/Scaffold/ContractTestGenerator.php` in the installer is the single source of truth
for all 66 generated copies. Fix it there, tag, then regenerate here.

## Three ordering rules the generated file encodes

They look like style. They are not.

1. **`primeConstants()` runs before the plugin class is mentioned at all.** A static property
   initializer can reference a bare constant — `$settings` holding
   `REPEAT_BILLING_METHOD => PRORATE_BILLING` is the common shape — and initializers run on class
   *load*, so even reading `::$type` fatals on an unprimed class.
2. **The hook table is read through `TierA5HooksAreIdempotent::hookTable()`,** never a direct
   `getHooks()` call. A direct call is a second, independent answer to a question A-5 owns, and
   the two disagree for any plugin whose body touches a bare constant.
3. **The table is evaluated exactly once.** Calling `getHooks()` twice asserts idempotence by
   accident and doubles whatever side effect the body has.

Plus `@runTestsInSeparateProcesses` + `@preserveGlobalState disabled`, always.

### Namespaced stubs

If this package ships a `tests/stubs.php` declaring helpers **inside the plugin's own
namespace**, PHP binds the plugin's unqualified calls to those rather than to the harness's
observers. Eight packages in the fleet do this. The harness detects the shadow and skips instead
of accusing, but the assertion is then vacuous. Prefer forwarding such a stub into the harness
over making it a no-op, so the observation still lands.

## Service lifecycle (this package is `type=service`)

`ContractTest` extends `ServicePluginTestCase`, which adds the assertions the eighteen shared
inspectors cannot make: it drives `getActivate()`, `getDeactivate()`, `getChangeIp()` and
`getQueue()` **twice** — once for a service type this plugin owns and once for a type it does
not — and asserts it acts on the first and stays inert for the second.

That second half is the one that finds things. A handler that ignores its service-type guard
looks perfectly healthy until something else in the fleet dispatches the same event.

If one of these fatals, read it as a P-bug until proven otherwise: it means the handler has
never run under test before, which is precisely the gap the harness was built to close.

## Verify

```bash
vendor/bin/phpunit
```

Whole suite, green, before committing.

## Reference

- `docs/testing-harness.md` in `detain/myadmin-plugin-installer` — §1.5 scaffolding, §3 traps,
  §7 the P-bug/H-bug split, §11 the generated file.
- `.claude/rules/plugin-tests.md` in MyAdmin core.