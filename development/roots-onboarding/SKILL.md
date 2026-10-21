---
name: roots-onboarding
description: Use when you are new to a Roots-stack WordPress project and need a map - "orient me", "what does this project do", an inventory of providers, blocks, post types, routes, Livewire components, runner and versions, or architecture discovery before scoping a feature. Read-only. For a bug use roots-debugging; for a convention audit use roots-reviewing.
---

# Roots onboarding: a read-only project map

Builds a short, factual map of an unfamiliar project from the detector JSON and an app inventory, then proposes next steps. It changes nothing: no files, no branches, no commits.

## When to use

- First session in a project, or returning after a break.
- The user asks what exists, how the project is wired, or where a thing should go.
- Before designing a new feature: the same map plus the discovery procedure in `references/discovery-procedures.md`.

## Inputs required

- The project root (working directory).
- The detector JSON: `node scripts/detect-roots-project.mjs` from the kivo-wise plugin root (C1 contract: `layout`, `apps[]`, `active`, `runtime`, `flag`, `warnings`). The session context already carries a compact form; run it again only when you need the full document.
- The runner from the session context (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.node}}`, `{{runner.test}}`, `{{runner.cache}}`). Lando default: `lando wp`, `lando wp acorn`, `lando composer`; the exact tooling names come from the landofile.

## Procedure

1. **Read the detector JSON.** Note `layout`, the active app (`apps[active]`: `kind`, `path`, `namespace`, `boot`, `providers.source`, `blocks`, `postTypes`, `versions`), `runtime.runner`, and every entry of `warnings`. If `flag` is set, `.roots-stack.json` overrides detection; say so. If `apps` is empty, the project is plain WordPress: stop the Acorn steps and report that.
2. **Run the inventory on the active app.**
   `node scripts/inventory-project.mjs --app <apps[active].path>` (the script path is relative to the kivo-wise plugin root, two levels above this skill's folder; the app path is relative to the project root, pass it absolute). When you cannot run scripts (read-only tools), say so, show both commands with resolved paths and the detected app path (never a theme path on `radicle-app` or `acorn-mu-plugin`), and build the same map by reading the files the inventory reads. It lists, without executing PHP: namespace, key packages, providers (and where they are registered), block mechanism, post-type mechanism, fields, options, components, composers, Livewire components, console commands, models, routes, views, migrations.
3. **Read the project rules.** `AGENTS.md`, `.ai/`, `.claude/rules/`, the README of the app, and `.docs-brain.json` if present (see `docs-brain`). These override every generic statement below.
4. **Check the pieces that depend on the profile** (table below), and the runner: are the containers up, which webroot, which cache and test commands exist.
5. **Look for work in progress**: the branch (`git branch --show-current`), plans or specs where the project keeps them (commonly `docs/plans/`), open TODO files. A plan marked in-progress whose branch is already merged is stale: confirm with `git branch --merged <default branch>` before saying so.
6. **Present the map** in the template below, then **suggest next steps** by state: new feature -> `references/discovery-procedures.md` (note template in `references/output-contract.md`) then the planning skill; bug -> `roots-debugging`; existing code to check -> `roots-reviewing`; unclear boot or provider placement -> `acorn-stack`.

### What differs per profile

| Topic | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
| --- | --- | --- | --- |
| Boot | `functions.php` configures Acorn, base path inferred from the theme | A mu-plugin boots Acorn (often through a configurator class) on `after_setup_theme`; `ACORN_BASEPATH` may be set | The project root is the base path; a tracked mu-plugin boots it |
| Providers registered in | `functions.php` / `config/app.php` | the configurator, `config/app.php`, or `composer.json` `extra.acorn.providers` | `composer.json` `extra.acorn.providers` |
| Post types | Poet config or classes | classes, or Poet | `roots/acorn-post-types` (`config/post-types.php`) |
| Blocks | ACF Composer classes | ACF Composer classes | native `block.json` + Blade render, no ACF by default |
| Livewire | optional | often present (version 4) | absent by default |
| Where the app lives | the theme folder | the plugin folder | the project root |
| Tests | project-chosen | PHPUnit or Pest | Pest |

### Map template

```
## Project map: <name>
- Profile: <kind> at <path>   Namespace: <ns>   Layout: <layout>
- Versions: WordPress <x>, Acorn <x>, PHP <x>, plus ACF Composer / Livewire / Poet when present
- Runner: <lando | ddev | none>; commands: wp=<..> acorn=<..> composer=<..> node=<..> test=<..> cache=<..>
- Boot: <file, hook, base-path source>
- Providers: <n> registered in <source>; <n> on disk not registered: <names>
- Blocks: <mechanism, count>   Post types: <mechanism, names>   Livewire: <n>   Routes: web <n>, api <n>
- Rules found: <AGENTS.md, .ai/, rules>   Docs corpus: <roots or none>
- Work in progress: <branch, plans>
- Warnings: <detector warnings and inventory notes>
- Next steps: <2-4 concrete suggestions>
```

## Verification

- Every number in the map comes from the detector JSON, the inventory JSON or a file you read; nothing is guessed.
- `unregisteredOnDisk` and the detector `warnings` are reported, not silently dropped.
- The map fits on one screen; deeper detail is offered, not dumped.
- No file was written and no command changed state (`git status` is unchanged).

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Detector returns `apps: []` | Plain WordPress, or Acorn not in `composer.json` | Report it; do not invent a profile; ask for the app path and offer a `.roots-stack.json` flag |
| Inventory shows `providers.source: none` | Providers registered in a file the scan does not read | Search the boot file for `withProviders`; read `composer.json` `extra.acorn` |
| Inventory lists far fewer classes than expected | Wrong `--app` path (project root instead of the plugin or theme) | Re-run with `apps[active].path` |
| `truncated: true` | More than 5,000 files in scope | Narrow `--app`, or inspect the folders by hand |
| Runner commands fail | Containers are down | Start them through the runner; report the exact error |
| Two apps detected | Theme and mu-plugin both boot Acorn | Name both, ask which is in scope, point at the detector warning |

## Escalation

- Contradictory signals (flag file says one profile, files say another): show both and ask; do not pick.
- Anything the user must decide (profile override, which app is in scope, whether to start discovery): ask once, with your recommendation.
- This skill never fixes what it finds. Hand the finding to the skill named in step 6.

<!-- verified: scripts/inventory-project.mjs — run against the sage theme clone (providers from functions.php), an mu-plugin app (providers from a configurator, ACF Composer blocks) and a root app (providers from composer extra.acorn.providers, native block.json); refs/roots-acorn/src/Roots/Acorn/PackageManifest.php:84 — extra.acorn is read as package discovery data; refs/roots-acorn/src/Roots/Acorn/Configuration/ApplicationBuilder.php:140 — withProviders(); references/discovery-procedures.md — ACF Builder field key = field_<group>_<name> (vendor/stoutlogic/acf-builder/src/Transform/NamespaceFieldKey.php:44-55), order of addX() does not matter (upstream claim corrected); detector fields from plan contract C1; not run here: the detector script (built in Phase 2) -->
