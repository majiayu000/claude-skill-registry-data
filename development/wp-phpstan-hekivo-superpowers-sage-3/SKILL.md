---
name: wp-phpstan
description: Use when configuring, running or fixing PHPStan in a WordPress project that uses Acorn - phpstan.neon, baseline, szepeviktor/phpstan-wordpress stubs, larastan, level raising, "Cannot access property on mixed", get_field() types, paths for app/. For Pint or Mago formatting use testing-wp; for runtime errors use roots-debugging.
---

# PHPStan for WordPress + Acorn (wrapper)

Full procedure: `third-party/wp-phpstan/SKILL.upstream.md` (official WordPress skill, GPL-2.0-or-later, see `third-party/UPSTREAM.md`). Read it and its `references/` (`configuration.md`, `wordpress-annotations.md`, `third-party-classes.md`) first. This file adds the Roots specifics: where to point the analysis, how Acorn code differs, and how to run everything through the runner. Paths starting with `third-party/` are relative to the kivo-wise plugin root, two levels above this skill's folder (`<skill dir>/../../third-party/...`), not inside the skill folder. In your answer, point the user to that full procedure by its resolved absolute path, and use the same resolution for any other `third-party/` path you name.

## When to use

- A project has no `phpstan.neon` yet, or the configuration scans the wrong folders.
- PHPStan reports errors on Blade composers, service providers, facades, Eloquent models or ACF Composer classes.
- You want to raise the level, generate a baseline or wire PHPStan into CI.

## Inputs required

- Profile and app path from the session context (`{{runner.composer}}`, `{{runner.test}}`, the detected app path).
- Current level and baseline file, if any; Composer constraints for `phpstan/phpstan` (PHPStan 2 needs matching extension versions).
- Which ACF and plugin classes the code touches (they need stubs or targeted ignores).

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Inspect first.** Run the official script from the plugin root, with the project as working directory: `node third-party/wp-phpstan/scripts/phpstan_inspect.mjs`. It reports the config, the baseline and whether WordPress stubs are installed. It reads files only; it does not run PHPStan.
2. **Install through the runner** (dev dependencies, in the Composer root that owns the app):
   `{{runner.composer}} require --dev phpstan/phpstan szepeviktor/phpstan-wordpress phpstan/extension-installer`.
   The extension installer loads the WordPress extension automatically; do not also include it by hand.
3. **Point `paths` at the app code, not at the whole site.** Never analyse `wp/`, `vendor/`, `node_modules/` or uploads.

   | Profile | `paths:` in `phpstan.neon` |
   | --- | --- |
   | `sage-theme` | `app/` of the theme (config lives in the theme, or in the repo root with `<theme>/app`) |
   | `acorn-mu-plugin` | `app/` of the plugin (for example `wp-content/mu-plugins/<plugin>/app`); put `phpstan.neon` at the repo root when the plugin has no own `composer.json` runner |
   | `radicle-app` | `app/` at the project root, plus `config/` if you want it checked |

   Start at level 1 and raise one level per MR; commit a baseline only for existing errors.
4. **Larastan is optional on Acorn.** It teaches PHPStan about facades, the container and Eloquent. Add `larastan/larastan` only when facade or model errors dominate the report, include its `extension.neon` from `vendor/`, and check its bootstrap requirement against the installed version first: it expects a bootable Laravel application, which Acorn only provides after WordPress has loaded. If it cannot boot, keep plain PHPStan and add PHPDoc on the few models or facades involved.
5. **Run through the runner:** `{{runner.composer}} exec phpstan -- analyse --memory-limit=1G` (Lando: `lando composer exec phpstan -- analyse`). Generate or update the baseline with `--generate-baseline`.
6. **Fix by cause**, in this order: missing stubs or autoload, wrong PHPDoc, real bug, then targeted `ignoreErrors` with a comment. `get_field()` returns `mixed`: narrow it with a type check or a typed wrapper instead of ignoring the whole file.
7. **CI:** run with `--no-progress --error-format=github` (or the format your CI reads) and fail on a baseline that grew.

## Verification

- `{{runner.composer}} exec phpstan -- analyse` exits 0 at the chosen level with the baseline applied.
- The baseline file only shrinks between MRs; a new entry needs a reason in the MR.
- The command was run through the runner (container PHP), not host PHP, so the PHP version matches production.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Function get_option not found` | WordPress stubs not loaded | Install `szepeviktor/phpstan-wordpress` and the extension installer; remove duplicate manual includes |
| Thousands of errors from `vendor/` or `wp/` | `paths` too wide | Narrow `paths` to the app folder; use `excludePaths` for generated code |
| `Class Illuminate\... not found` in a composer or provider | Analysing the app from a Composer root that lacks the app's vendor | Run from the Composer root that installs Acorn, or add `scanDirectories` for that vendor |
| Facade or model property errors | No Larastan and no PHPDoc | Add PHPDoc on the model or enable Larastan when it can boot |
| Out of memory | Default memory limit | Pass `--memory-limit=1G` or raise it in the neon |
| Works locally, fails in CI | Different PHP version or missing dev install | Match the container PHP version in CI |

## Escalation

- Raising the level above what the team agreed, or deleting a baseline: ask first.
- A fix that needs a behaviour change (not just a type) belongs in its own change with a test; hand it to `testing-wp`.
- If Larastan cannot be made to boot against the installed Acorn, stop and report the exact error rather than suppressing it.

<!-- verified: the reference acorn-mu-plugin project's phpstan.neon — level 1, paths: the mu-plugin folder; its composer.json — phpstan/phpstan ^2.1, extension-installer ^1.4, szepeviktor/phpstan-wordpress ^2.0; third-party/wp-phpstan/scripts/phpstan_inspect.mjs — read-only inspect; UNVERIFIED locally: larastan boot requirement on Acorn (package not installed in any local project) -->
