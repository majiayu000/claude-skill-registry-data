---
name: roots-triage
description: Use when you need to know what kind of project the working directory is (Sage theme, Acorn mu-plugin, Radicle, Bedrock, plain WordPress), when the session context is missing or contradicts the files, when there is no .roots-stack.json, or when a detector warning (ACORN_BASEPATH, misplaced env_file, truncated scan, flag drift) needs explaining. Runs scripts/detect-roots-project.mjs and writes .roots-stack.json. For choosing a skill after triage use roots-router; for Lando commands use lando-wp.
license: MIT
compatibility: Filesystem agent with bash and node 20+; the detector is read-only and never runs project commands.
---

# Roots triage

Deterministic classification of a Roots-stack project: run the detector, read its JSON, act on the warnings, pin the result in a flag file.

## When to use

- No session context names a profile, or the context disagrees with the files in front of you.
- The request needs facts the detector owns: layout, core directory, Acorn apps and their namespaces, package versions, runner commands, Lando tooling names.
- A warning from the detector needs explaining or fixing.
- A project should stop relying on heuristics: write `.roots-stack.json`.
- Not for: deciding which skill handles the request (that is `roots-router`), or running `lando` itself (`lando-wp`).

## Inputs required

- The project root (defaults to the working directory; pass `--path=<dir>` otherwise).
- Read access to `composer.json`, `composer.lock`, `.lando.yml` and companions (`.lando.base.yml`, `.lando.dist.yml`, `.lando.upstream.yml`, `.lando.local.yml`), `wp-cli.yml`, `.roots-stack.json`, theme `style.css` and plugin headers.
- The plugin root: the directory that contains `skills/` and `scripts/`. Nothing else; no network, no containers.

## Procedure

1. **Run the detector from the plugin root.**

   ```bash
   node scripts/detect-roots-project.mjs --path=/abs/path/to/project            # JSON (default)
   node scripts/detect-roots-project.mjs --path=/abs/path/to/project --format=text  # compact table
   ```

   Without `--path=` the working directory is the project root. The same file name exists inside this skill folder (`scripts/detect-roots-project.mjs`) as a wrapper that forwards to the plugin-root copy, so the relative path works from either place. The script exits 0 always; absence becomes `null` plus an entry in `notes`.

2. **Read the top level first:** `layout`, `coreDir`, `apps.length`, `active`, `runtime.runner`, `flag`, `warnings`, `truncated`. The shape is fixed by [references/triage.schema.json](references/triage.schema.json); the meaning of every field is in [references/output-fields.md](references/output-fields.md).

   | Field | Read it as |
   |---|---|
   | `layout` | `radicle` / `bedrock` / `composer-wordpress` / `plain-wordpress` / `unknown` - where core and content live |
   | `coreDir` | the local WordPress source; never edit it, always read it to verify native behaviour |
   | `apps[active].kind` | the profile: `sage-theme`, `acorn-mu-plugin`, `radicle-app` (or `acorn-theme`, `acorn-plugin`, `acorn-unknown`) |
   | `apps[active].path`, `.namespace`, `.basePathHint`, `.boot`, `.providers`, `.blocks`, `.postTypes`, `.versions` | where the code is, how it boots, which mechanisms are in use, which versions to document against |
   | `site.versions`, `site.wpCli` | site-wide versions (`roots/wordpress`, ACF Pro) and where WP-CLI expects core |
   | `runtime.runners` | the only commands you may suggest: `wp`, `acorn`, `composer`, `node`, `test`, `lint`, `cache`, `logs` |
   | `flag` | the committed decision; when present it overrides `apps` for routing |

3. **Act on each warning.** Warnings are plain sentences; match them by what they mention.

   | Warning mentions | Meaning | Action |
   |---|---|---|
   | an Acorn app without `ACORN_BASEPATH` while a theme has `composer.json` | Acorn may infer the theme as base path, so the plugin's `config/`, views and storage resolve to the wrong directory | Define `ACORN_BASEPATH` or pass the path to `Application::configure()` in the plugin's boot file; re-run the detector |
   | `env_file` under `config:` / `misplacedEnvFile` | Lando only injects the top-level `env_file` list; nested, it is dropped silently | Move `env_file` to the top level of `.lando.yml` and rebuild, or confirm PHP loads `.env` itself (then the variables exist for PHP but not for tooling) |
   | flag vs detected app (drift) | `.roots-stack.json` names a profile or path the heuristics no longer find | Fix the flag (or the project); until then the flag still wins |
   | two apps booting, or a second app with `wordpress: true` routing | Double boot: two Acorn applications fight for hooks and request routing | Keep one booted app, or make the second one a library |
   | `tailwind.config.js` next to Tailwind 4 | Stale v3 configuration; v4 reads `@theme` from CSS | Remove or migrate the file into CSS |
   | Blade views outside the theme with an older `roots/acorn` | Template resolution for non-theme views needs a newer Acorn on recent WordPress | Upgrade `roots/acorn` in the app's `composer.json` |
   | `truncated` | The walk hit depth 4 or 5,000 files | Narrow with `--path=` to the app, or write the flag file so the walk is not needed |
   | `runner: none` | No `.lando.yml` or `.ddev/` found | Commands run on the host; say so explicitly and prefer the project's documented wrapper |
   | `layout: unknown` and no apps | Not a Roots project, or the signals live deeper than the walk | Ask the user; do not guess a profile |

4. **Pin the result.** When the classification is right, propose committing `.roots-stack.json` at the project root:

   ```json
   { "profile": "acorn-mu-plugin", "app": "wp-content/mu-plugins/<plugin>", "runner": "lando", "corpus": ["~/hekivo/kivo-wisdom/corpus"] }
   ```

   `profile` is one of `sage-theme`, `acorn-mu-plugin`, `radicle-app`; `app` is relative to the root (`.` for Radicle); `runner` is `lando`, `ddev` or `none`; `corpus` is optional. The same keys are accepted under `extra.roots-stack` in the root `composer.json`. The flag wins over heuristics, and the detector keeps computing `apps` so it can warn about drift. Writing the file is the user's decision: show the content and the reason.

5. **Hand back to routing.** Report profile, app path, namespace, runners and open warnings in one line, then continue with `roots-router`.

## Verification

- The command exits 0 and prints one JSON document that has every required top-level key of `references/triage.schema.json` (`tool`, `root`, `layout`, `coreDir`, `apps`, `active`, `site`, `runtime`, `flag`, `warnings`, `notes`, `truncated`).
- `apps[active].kind` is one of the three routed profiles, or you asked the user which it should be.
- `flag`, when present, agrees with `apps[active]` (no drift warning).
- `truncated` is `false`, or you explained why it is acceptable.
- `--format=text` prints the compact line that matches what the session context shows.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `detector not found` JSON from the wrapper | The skill wrapper could not find `scripts/detect-roots-project.mjs` at the plugin root | Run the command from the plugin root; check the plugin installation is complete |
| `apps` is empty on a Roots project | The app sits deeper than depth 4, or its `composer.json` does not require `roots/acorn` | Run with `--path=` pointing at the app, or write `.roots-stack.json` |
| Wrong `active` app (theme chosen over the mu-plugin) | The working directory is inside the theme and no flag exists | Write the flag file; the flag overrides the "contains cwd" rule |
| `runtime.lando` is `null` although `.lando.yml` exists | The YAML subset parser gave up (see `notes`) | Simplify the construct it names, or read the Landofile by hand for that session |
| `coreDir` is `null` on `composer-wordpress` | `extra.wordpress-install-dir` missing and no `wp-includes/version.php` found | Read `wp-cli.yml` `path:`; set `wordpress-install-dir` in the root `composer.json` |
| Classification flips between runs | `.lando.local.yml` or an untracked flag file differs between machines | Commit `.roots-stack.json`; keep personal overrides out of it |
| Script throws or prints a stack trace | Contract violation (it must never throw) | Report the input tree and the message; fall back to reading the files by hand |

## Escalation

- A field or warning you cannot interpret: read `references/output-fields.md`; if it is still unclear, the detector's `notes` name the file it read.
- The detector contradicts the project's own documentation: the project documentation wins for this session; file the discrepancy with the project maintainers and, if the detector is wrong, with the plugin.
- Classification needs human knowledge (brand-new layout, custom boot): ask one question - theme, must-use plugin or repository root? - and pin the answer in `.roots-stack.json`.
