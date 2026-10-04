---
name: rails-8-upgrade
description: Upgrade a Rails 7 app to Rails 8 safely, and catch the subtle test-suite flake it introduces. Use when bumping Rails 7.x to 8.x (or auditing readiness), when planning a Ruby/Rails version bump, or when Rails 8 tests fail intermittently with "undefined method 'login_path'/'root_path'" / pass on serial but flake on parallel runs. Provides a pre-flight audit, a detector + fix for the LazyRouteSet route-test flake, and a 7→8 checklist grounded in a real upgrade.
---

# Rails 7 → 8 upgrade

Two things kill time in a 7→8 upgrade: deciding what to bump vs defer, and a
**flaky route-helper test** that Rails 8's `LazyRouteSet` introduces and that hides
behind single green test runs. This skill handles both.

Read [`references/rails-7-to-8.md`](references/rails-7-to-8.md) for the full checklist and the why.

## When to use

- Bumping `rails` 7.x → 8.x, or checking whether an app is ready.
- Tests started flaking after a Rails 8 bump with `undefined method
  'login_path'/'root_path'` in unrelated controllers; serial runs stay green.
- Reviewing a PR that adds/edits a `draw_test_routes`-style route helper.

## 1. Pre-flight audit (read-only)

```bash
scripts/upgrade_audit.sh path/to/app
```

Reports: Ruby/Rails versions (+ flags a `Gemfile.lock` RUBY VERSION mismatch that
makes `bundle` refuse), `config.load_defaults` vs Rails major, presence of a
`new_framework_defaults_*.rb`, **known-risky gems** (notably pagy <6 *with* custom
pagy view helpers — a real porting cost), and whether the test suite uses the
flaky route pattern. Changes nothing.

## 2. The recommended path

1. **Baseline green** on current versions first (a bisectable starting point).
2. Bump `rails ~> 8.x` and Ruby; **leave `config.load_defaults` where it is**
   (run new library code with old framework behavior — low risk).
3. `bundle update`; only hand-pin where a transitive conflict forces it.
4. Run the suite **≥6×** (parallel flakes hide — see below). Boot the server,
   check a public (200) and a protected (401/redirect) route.
5. Flip framework defaults *separately* later, via
   `config/initializers/new_framework_defaults_8_1.rb`, one line at a time.

## 3. The LazyRouteSet route-test flake (the expensive one)

If the suite appends test-only routes via a helper that toggles
`Rails.application.routes.disable_clear_and_finalize`, Rails 8 makes it flaky under
parallel runs. Detect it:

```bash
scripts/lint_route_test_helper.sh path/to/app
```

It checks the helper (a) **materializes** the LazyRouteSet
(`reload_routes_unless_loaded`) *before* setting the flag, (b) **resets** the flag
in an `ensure`, (c) doesn't use the `finalize!` dead-end, and (d) every
`draw_test_routes` caller has a `teardown { reload_routes! }`. Exits non-zero on
risk and prints the fix.

Apply `templates/routes_helper.rb.fixed` (drop into `test/support/`) and add the
missing teardowns. Then **run the suite ≥6×** to confirm — a 35%-flake bug passes
~2 of 3 single runs.

> Root cause + dead-ends: `references/rails-7-to-8.md`. Real-world instance:
> `piazza-web/wip/analysis/01`.

## Why the scripts are heuristic

Plain `grep`/`awk` text scans, not Ruby parsers — conservative and dependency-free,
meant to gate a PR and point you at the fix, not to be a type checker. They name
their ceiling in the output.
