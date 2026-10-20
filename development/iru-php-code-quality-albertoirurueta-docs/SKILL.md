---
name: iru-php-code-quality
description: >-
  Run this project's wired PHP static-analysis and coding-style tools — PHPStan (including Larastan, `szepeviktor/phpstan-wordpress`, and PrestaShop's `prestashop/php-dev-tools` config, honoring the project's baseline) with `--error-format=json`, Psalm (`--output-format=json`), Laravel Pint (`--test` with a JSON report file), PHP-CS-Fixer (`check`/`fix --dry-run --diff --format=json`), PHP_CodeSniffer (`phpcs --report=json` with whatever standards `phpcs.xml(.dist)` references — WordPress/WordPress-Extra/WordPress-Docs, PHPCompatibilityWP, PSR12, PER), and Rector (`process --dry-run --output-format=json`) when configured — then report every issue found (file, line, rule id/identifier, message), grouped by tool and classified by rule id. Detects the project's flavor (Laravel application, WordPress plugin or theme, PrestaShop module, or plain Composer library) from `composer.json` and file markers (`artisan`, a `Plugin Name:` header, `style.css` `Theme Name:`/`theme.json`, a class that `extends Module`/`config.xml`) to know which tools to expect and which rule-id prefixes matter, and verifies each tool is actually installed and configured before trusting a "zero issues" result from it. Runs through whichever environment the project uses for PHP (host `php`, Laravel Sail, ddev, or wp-env). Invoke as `/iru-php-code-quality` to check the whole project, or `/iru-php-code-quality <path-or-glob>` to scope the run and the report — every one of these tools accepts paths, so a scoped invocation narrows what actually runs. When the prompt supplies a baseline (a prior per-rule-id issue count from an earlier run of this skill, e.g. captured by `iru-php-code-one-task-group` before a task group's changes), reports only the new-vs-baseline diff per rule id. Report-only: never fixes issues or edits tool configuration. Use whenever the user wants a static-analysis/style pass called out separately from `iru-php-test`/`iru-php-coverage`, instead of eyeballing `composer lint` output.
model: haiku
allowed-tools: Read Bash(php *) Bash(vendor/bin/*) Bash(./vendor/bin/*) Bash(composer *) Bash(_PS_ROOT_DIR_=* *) Bash(PHP_CS_FIXER_IGNORE_ENV=* *) Bash(./vendor/bin/sail *) Bash(npx wp-env *) Bash(ddev *) Bash(docker info *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(git *) Bash(mkdir -p build*) Bash(rm -f build/iru-php-cq-*)
---

# PHP Code Quality

Run every static-analysis and coding-style tool this PHP project actually has wired — PHPStan, Psalm, Pint,
PHP-CS-Fixer, PHP_CodeSniffer, Rector — and report every issue they find, grouped by tool and by rule id. This skill
only runs checks and reports results — it does not fix issues, apply Rector/Pint/PHP-CS-Fixer changes, update a
baseline, or modify any tool configuration unless asked to as a follow-up.

## Step 1 — Detect the flavor, the environment, and which tools are wired

**Flavor detection** (same markers `iru-explore` uses for its `Project type:` line, and shared with `iru-php-test`/
`-coverage`/`-phpdoc`/`-code-one-task*` — apply them in this order, the first match wins):

| Flavor | Markers |
|---|---|
| **laravel** | `laravel/framework` in `composer.json` `require` **and** an `artisan` file at the root |
| **wordpress-plugin** | a root-level PHP file whose header comment carries `Plugin Name:` (`grep -l '^[ \t/*#@]*Plugin Name:' *.php`) |
| **wordpress-theme** | `style.css` whose header comment carries `Theme Name:`, and/or a `theme.json` |
| **prestashop-module** | a root `<module>.php` with a class that `extends Module` (or `PaymentModule`/`CarrierModule`), a `config.xml`, and/or `prestashop/*` packages in `composer.json` |
| **library** | anything else with a `composer.json` |

The flavor decides which tools are *expected* (a missing expected tool is worth a note in the report; a missing
optional one isn't) and which rule-id prefixes matter in Step 3:

| Flavor | Expected tools | Typical config |
|---|---|---|
| laravel | Pint (`laravel` preset, ships with the skeleton), PHPStan + Larastan (`larastan/larastan`) | `pint.json` (optional — Pint runs zero-config), `phpstan.neon(.dist)` including `vendor/larastan/larastan/extension.neon` |
| wordpress-plugin / -theme | PHP_CodeSniffer + WordPressCS (`wp-coding-standards/wpcs`, usually with `phpcompatibility/phpcompatibility-wp`), optionally PHPStan + `szepeviktor/phpstan-wordpress` | `phpcs.xml.dist` / `.phpcs.xml.dist` referencing `WordPress`, `WordPress-Extra`, `WordPress-Core`, `WordPress-Docs`, `PHPCompatibilityWP`; `phpstan.neon.dist` including `vendor/szepeviktor/phpstan-wordpress/extension.neon` (or registered by `phpstan/extension-installer`) |
| prestashop-module | PHP-CS-Fixer + PHPStan from `prestashop/php-dev-tools` | `.php-cs-fixer.dist.php` built on `PrestaShop\CodingStandards\CsFixer\Config`; `tests/phpstan/phpstan.neon` including `vendor/prestashop/php-dev-tools/phpstan/ps-module-extension.neon` |
| library | PHP-CS-Fixer (`@PER-CS`) or PHP_CodeSniffer (`PSR12`/PER), PHPStan or Psalm; Rector optional | `.php-cs-fixer.dist.php`, `phpcs.xml(.dist)`, `phpstan.neon(.dist)`/`phpstan.dist.neon`, `psalm.xml(.dist)`, `rector.php` |

Any flavor may wire any extra tool — always run whatever is actually configured, not just the expected list.

**Environment** — static analysis needs no database, so prefer host PHP: `command -v php` succeeds and its version
satisfies `composer.json`'s `require.php` (`php -r 'echo PHP_VERSION;'`). Otherwise use the project's container,
detected exactly as `iru-php-test` Step 1 does (`.ddev/config.yaml` → `ddev exec <cmd>`; Laravel Sail →
`./vendor/bin/sail php <cmd>` / `./vendor/bin/sail bin <tool>`; wp-env → `npx wp-env run cli --config=.wp-env.test.json --env-cwd=wp-content/<plugins|themes>/<dir> <cmd>` when the
project has that test config, else plain `cli` — static analysis doesn't touch the database, but never start an
environment just for it; ask first),
after confirming `docker info` succeeds — if Docker isn't running, stop and say so. No usable PHP at all → stop and
report it; never report "0 issues".

**`vendor/` missing** → stop and report "dependencies not installed — run `composer install`" (ask before running it).
Many WordPress plugins/themes have **no `composer.json` at all**: then nothing is wired locally — report "no PHP
quality tooling wired" rather than reaching for a globally installed `phpcs`, whose standards and version won't match
what the project's CI uses (if the user explicitly asks to use a global install, check `phpcs -i` lists the standard
first).

**Verify each tool is actually wired before trusting a zero result from it** — a binary in `vendor/bin/` plus the
config that tells it what to check:

- **PHPStan** — `vendor/bin/phpstan` plus a config: `phpstan.neon`, `phpstan.neon.dist`, or `phpstan.dist.neon` at the
  root (PHPStan's own lookup order), or one the composer scripts pass via `-c` (PrestaShop: `tests/phpstan/phpstan.neon`).
  Read it for `level`, `paths`, and `includes` — the baseline (`phpstan-baseline.neon`, or `.php`) and extensions
  (Larastan, phpstan-wordpress, the PrestaShop extension) are only active when included there or registered by
  `phpstan/extension-installer`. A `phpstan-baseline.neon` that exists but isn't included anywhere is worth a note:
  the project's gate ignores nothing, so neither does this run.
- **Psalm** — `vendor/bin/psalm` plus `psalm.xml`/`psalm.xml.dist`; note its `errorLevel` and `errorBaseline`
  attribute (the baseline, usually `psalm-baseline.xml`, is applied automatically when that attribute is set).
- **Pint** — `vendor/bin/pint` (`laravel/pint`). It runs with no config (`laravel` preset); `pint.json` only refines
  preset/rules/excludes — note which preset is in force.
- **PHP-CS-Fixer** — `vendor/bin/php-cs-fixer` plus `.php-cs-fixer.dist.php`/`.php-cs-fixer.php` (or a legacy
  `.php_cs.dist`, which current versions ignore — report it as misconfigured rather than a clean pass). Without a
  config it would only apply `@PSR12` defaults to whatever paths it's given — report that distinction.
- **PHP_CodeSniffer** — `vendor/bin/phpcs` plus `.phpcs.xml`, `phpcs.xml`, `.phpcs.xml.dist`, or `phpcs.xml.dist`
  (auto-detected in that order). Without one, `phpcs` falls back to the `PEAR` standard — never report that as a
  clean pass of the project's style. Confirm referenced standards are installed: `vendor/bin/phpcs -i` must list
  e.g. `WordPress`, `WordPress-Extra`, `WordPress-Docs`, `PHPCompatibilityWP` (installed through
  `dealerdirect/phpcodesniffer-composer-installer`); a missing one makes `phpcs` abort with a "standard not
  installed" error, which is a tooling failure, not a code issue.
- **Rector** — `vendor/bin/rector` plus `rector.php`. Only run when that config exists: Rector proposes refactorings
  (PHP-version upgrades, dead code, type declarations), so its findings are "code Rector would rewrite", reported
  separately from defects.

If a tool's binary or config is missing, **skip it and say so in the report** ("Psalm: not configured, skipped")
instead of silently omitting it or reporting a misleading "0 issues". Also read `composer.json` `scripts` (`lint`,
`analyse`, `cs`, `phpstan`, `test:types`, …): the project's real invocation (an extra `-c`, `--memory-limit`, a
non-default config path) is the one to mirror.

## Step 2 — Run each configured tool, scoped to `[scope]` when given

`[scope]` is one or more files, directories, or globs; expand globs with `find` first (these tools take paths, not
shell globs) and pass the resulting paths. With no argument, pass no paths so each tool analyses what its own config
lists. Write every machine-readable report **inside the project** under `build/` (so the same relative path works on
the host and inside Sail/ddev/wp-env containers), prefixed `iru-php-cq-`, and delete them afterwards
(`rm -f build/iru-php-cq-*`; remove `build/` only if this run created it).

1. **PHPStan** —
   `vendor/bin/phpstan analyse --no-progress --error-format=json [-c <config>] [--memory-limit=1G] [paths] > build/iru-php-cq-phpstan.json`.
   - Paths on the command line replace the config's `paths` for this run but keep its `level`, `excludePaths`,
     `includes` (so the baseline still applies), and extensions. Pass `--memory-limit=1G` for Larastan, phpstan-wordpress, and
     the PrestaShop extension (all load large stub sets), whenever the composer script does, or when a run dies with
     `Allowed memory size ... exhausted` (see **Memory** below).
   - JSON goes to stdout; `Note: Using configuration file ...` and the "Result is incomplete because of severe
     errors" warning go to stderr — keep them separate (verified with PHPStan 2.x). Shape:
     `{"totals":{"errors":0,"file_errors":2},"files":{"/abs/src/Report.php":{"errors":2,"messages":[{"message":"Offset 'yaer' does not exist on array{title: string, year: int}.","line":19,"ignorable":true,"identifier":"offsetAccess.notFound","tip":"..."}]}},"errors":[]}`
     — `identifier` and `tip` are present only when the error has them; file keys are absolute paths (inside a
     container, e.g. `/app/src/...`). `errors` (top level) holds non-file errors: configuration problems, crashed
     workers, and "Ignored error pattern ... was not matched in reported errors" (a stale baseline or `ignoreErrors`
     entry) — report them under a `<config>` bucket, not as code issues. Verified: a scoped run (explicit paths) with a
     baseline covering other files reports nothing for those unmatched entries, and baseline-covered errors in the
     scoped file are suppressed as expected. Exit `1` when any error exists, `0` when clean.
   - **Memory**: PHP's default `memory_limit` (128M, also the `php:*-cli` Docker images' default) is not enough once
     stubs are loaded — verified: with `szepeviktor/phpstan-wordpress` registered, a single-file run produced no
     file results at all, only a top-level `errors` entry `Child process error (exit code 255): Fatal error: Allowed
     memory size of 134217728 bytes exhausted ... while running parallel worker`. Treat that entry as "run
     incomplete — re-run with `--memory-limit=1G`", never as a clean or partial result.
   - **PrestaShop**: the module's PHPStan config needs the shop's sources —
     `_PS_ROOT_DIR_=<path-to-prestashop> vendor/bin/phpstan analyse -c tests/phpstan/phpstan.neon --no-progress --error-format=json [paths]`.
     Find the shop path from the composer script, CI workflow, or a `.env`; if none exists locally, report
     "PrestaShop installation not available — PHPStan skipped (set `_PS_ROOT_DIR_`)" instead of a wall of
     `class.notFound` errors. An older generated config still using `excludes_analyse` fails on PHPStan 2.x with an
     invalid-configuration error — report that as a config problem (it needs `excludePaths`), not as code issues.
   - **WordPress**: phpstan-wordpress loads `php-stubs/wordpress-stubs`, so core functions resolve without a
     WordPress install; plugin-specific constants or third-party plugin APIs may still need `bootstrapFiles`/
     `scanDirectories` in the config — a burst of `function.notFound`/`constant.notFound` for another plugin's API
     points at that, which is worth flagging as likely config gaps.
2. **Psalm** — `vendor/bin/psalm --output-format=json --no-progress --show-info=false [paths] > build/iru-php-cq-psalm.json`.
   Psalm accepts file paths as arguments (otherwise it scans `<projectFiles>`). Output is a JSON **array**, one object
   per issue: `{"severity":"error","type":"PossiblyNullReference","message":"...","file_path":"/abs/src/Foo.php","file_name":"src/Foo.php","line_from":25,"column_from":9,"shortcode":...,"link":"https://psalm.dev/..."}`.
   Exit `2` when issues were found, `0` when clean, `1` when Psalm itself failed to run (verified with Psalm 6.x,
   which also adds `line_to`, `column_to`, `snippet`, `selected_text`, `error_level`, `taint_trace`, … per issue — ignore
   those). The `errorBaseline` from
   `psalm.xml` is applied automatically; never pass `--ignore-baseline` or `--set-baseline`/`--update-baseline` (the
   latter two rewrite the baseline file).
3. **Pint** — `vendor/bin/pint --test -v [paths] --format=json --output-to-file=build/iru-php-cq-pint.json --output-format=json`.
   - `--test` reports without changing files; never omit it, and never use `--repair` (it writes). `--dirty`
     (uncommitted files) and `--diff=<branch>` exist but scope by git state, not by `[scope]` — use explicit paths.
   - **Always read the report file, not stdout**: recent Pint versions detect an AI agent environment and switch
     stdout to their own compact agent format regardless of `--format`; `--output-to-file` with `--output-format=json`
     still writes the standard PHP-CS-Fixer JSON report. Verified with Pint 1.x under `CLAUDECODE=1`: stdout was
     `{"tool":"pint","result":"fail","files":[{"path":"src/Report.php","fixers":[...]}]}` while the file held the
     standard report. `-v` is what makes each file entry include `appliedFixers` (the rule names) — verified: without
     it the file entry is just `{"name":"src/Report.php"}`.
   - Report shape (PHP-CS-Fixer's JSON reporter): `{"files":[{"name":"app/Models/User.php","appliedFixers":["ordered_imports","no_unused_imports"],"diff":"--- ..."}],"time":{...},"memory":...}`.
     Only files that would change are listed. Exit `1` when any file would change.
4. **PHP-CS-Fixer** — `vendor/bin/php-cs-fixer check --format=json --diff -v --path-mode=intersection [paths] > build/iru-php-cq-php-cs-fixer.json`
   (`check` is `fix --dry-run`; on versions without `check`, use `fix --dry-run`). With paths, `--path-mode=intersection`
   keeps the config's own `Finder` excludes (the default `override` mode would ignore them). Same JSON shape as Pint;
   `appliedFixers` only appears with `-v`; the `diff` headers carry absolute paths. Exit code is a bitmask: `8` = some
   files need fixing (verified), `4` = some files have invalid syntax, `16`/`32` = configuration errors, `64` = an
   exception — a non-zero exit with 16/32/64 set is a tooling failure to report, not a style result (verified: a path
   argument that doesn't exist exits `16`, so check scoped paths exist before blaming the config). A stderr warning
   that PHP is newer than `composer.json`'s minimum is informational — the run still completes. If it refuses to run
   because the PHP version is newer than it officially supports, report that; only set `PHP_CS_FIXER_IGNORE_ENV=1`
   if the project's own scripts/CI do.
5. **PHP_CodeSniffer** — `vendor/bin/phpcs --report=json --report-file=build/iru-php-cq-phpcs.json -q --no-colors --basepath=. [paths]`.
   The config file (and its `<file>`/`<exclude-pattern>`/`<arg>` entries) is picked up automatically; explicit paths
   replace its `<file>` list. Shape: `{"totals":{"errors":3,"warnings":1,"fixable":2},"files":{"src/Foo.php":{"errors":3,"warnings":1,"messages":[{"message":"All output should be run through an escaping function ...","source":"WordPress.Security.EscapeOutput.OutputNotEscaped","severity":5,"fixable":false,"type":"ERROR","line":42,"column":10}]}}}`.
   Don't rely on the exit code (verified `2` with issues on PHPCS 3.13; its meaning changed in PHPCS 4.x); read
   `totals` from the report. Note WordPressCS 3.x still pins PHP_CodeSniffer 3.x (verified: requiring
   `wp-coding-standards/wpcs` installed PHPCS 3.13.6), so WordPress projects run PHPCS 3 even though 4.x is current.
   Respect the config's own `<arg name="warning-severity">`/`<config name="ignore_warnings_on_exit">` choices when
   deciding whether warnings count against the gate, but always list them.
6. **Rector**, only when `rector.php` exists — `vendor/bin/rector process --dry-run --output-format=json --no-progress-bar [paths] > build/iru-php-cq-rector.json`.
   Shape: `{"totals":{"changed_files":2,"errors":0},"file_diffs":[{"file":"src/Legacy/Loan.php","diff":"...","applied_rectors":["Rector\\Php80\\Rector\\Switch_\\ChangeSwitchToMatchRector"],"changes":[{"rector":"...","line":21}]}],"changed_files":[...],"errors":[{"message":"...","file":"...","line":3}]}`
   (verified with Rector 2.7: `changes` carries per-rector line numbers; older releases lack it — fall back to the
   diff's hunk headers; `errors` is only present when non-empty). Exit `2` when the dry run would change files (verified),
   `0` when nothing would change. Never run without `--dry-run`.

If a tool fails outright for a reason unrelated to code issues (missing extension, unparseable config, memory
exhaustion, a fatal error while bootstrapping Larastan), report that cause for that tool and move on — don't read a
stale or empty report.

Parse the JSON reports with PHP itself (available wherever the tools ran), e.g. for PHPStan (verified against real
PHPStan 2.x output):

```bash
php -r '$r = json_decode(file_get_contents($argv[1]), true);
  foreach ($r["files"] as $f => $d) foreach ($d["messages"] as $m)
    printf("%s:%d\t%s\t%s\n", $f, $m["line"] ?? 0, $m["identifier"] ?? "<none>", $m["message"]);
  foreach ($r["errors"] as $e) printf("<config>\t%s\n", $e);' build/iru-php-cq-phpstan.json
```

and the same pattern for the others (`files.*.messages[]` → `source` for phpcs; the top-level array → `type` for
Psalm; `files[]` → `appliedFixers` for Pint/PHP-CS-Fixer; `file_diffs[]` → `applied_rectors` for Rector). For the
fixers, which report per file rather than per line, take line numbers from the `diff`'s `@@ -<line>,<n> +... @@`
hunk headers.

## Step 3 — Classify by rule id, diff against a baseline if given, and report

Make paths project-relative (PHPStan and Psalm's `file_path` are absolute), and if `[scope]` was given, drop
anything outside it (PHPStan can still report a config-level error for the whole project). Bucket every issue by
tool first, then by rule id (the same id can exist in two tools — keep them separate):

- **PHPStan** — by `identifier` (`return.type`, `argument.type`, `missingType.iterableValue`, `property.nonObject`,
  `offsetAccess.notFound`, …; an entry with no identifier goes to `<none>`). Call out extension-specific prefixes:
  `larastan.*` (Larastan's own rules, e.g. `larastan.noEnvCallsOutsideOfConfig`), and phpstan-wordpress's hook-docs
  findings (`paramTag.count`, `phpDoc.parseError`, `parameter.phpDocType` reported on `apply_filters()`/`do_action()`
  docblocks). PHPDoc-related identifiers (`phpDoc.*`, `missingType.*`, `parameter.phpDocType`, `return.phpDocType`)
  are the ones `iru-php-phpdoc` fixes — group them as "docblock" so a caller can hand them off.
- **Psalm** — by `type` (`PossiblyNullReference`, `MixedAssignment`, `TaintedSql`, …); list `Tainted*` (taint
  analysis) first if present.
- **Pint / PHP-CS-Fixer** — by fixer name from `appliedFixers` (`ordered_imports`, `no_unused_imports`,
  `binary_operator_spaces`, `phpdoc_align`, `Pint/...` custom rules); one entry per file per fixer.
- **PHP_CodeSniffer** — by full `source` (`Standard.Category.Sniff.Code`), errors and warnings counted separately,
  grouped by standard prefix:
  - WordPress flavor: `WordPress.Security.*` (escaping, nonces, input sanitization — list first), `WordPress.DB.*`
    (prepared SQL, direct queries), `WordPress.WP.*` (i18n text domains, enqueues, discouraged functions),
    `WordPress.NamingConventions.*` (`PrefixAllGlobals`, `ValidHookName`), `WordPress.PHP.*`, `WordPress.WhiteSpace.*`;
    `Squiz.Commenting.*`/`Generic.Commenting.*` (the WordPress-Docs inline-documentation checks — "docblock",
    handled by `iru-php-phpdoc`); `PHPCompatibility.*` (PHPCompatibilityWP — code that breaks on a PHP version in
    the configured `testVersion`); `Universal.*`, `Modernize.*`, `NormalizedArrays.*` (PHPCSExtra); `Generic.*`,
    `Squiz.*`, `PEAR.*`, `PSR2.*`.
  - Other flavors: `PSR1.*`, `PSR2.*`, `PSR12.*`, `Generic.*`, `Squiz.*`, `PHPCompatibility.*`, and any third-party
    standard the config references (`SlevomatCodingStandard.*`, …).
- **Rector** — by rector class short name (`ChangeSwitchToMatchRector`, `ReadOnlyPropertyRector`, …), one entry
  per file per rector; Rector `errors` get their own `<error>` bucket.

**Report**: an overall total across all tools at the top, the detected flavor and environment, then per tool: a
total, the config used (and baseline in force, if any), and the skipped/not-configured note if applicable; within
each tool, one line per rule-id bucket with its count and — for a scope smaller than the whole project, or on request
— its `file:line — message` list. Note expected-but-missing tools for the flavor (e.g. "WordPress plugin with no
PHPCS/WordPressCS configured") as a recommendation, not a failure. Never paste the raw JSON reports or diffs.

**Baseline diff** — when the prompt that invoked this skill supplies a baseline (a prior run's per-tool/per-rule-id
counts or itemized issues, e.g. `iru-php-code-one-task-group` capturing one before a task group's changes), compute
the diff yourself: report only issues that are new since the baseline (a rule id whose count increased, a rule id
that didn't exist before, or a new `file:line` entry when the baseline was itemized). A rule id whose count fell or
stayed the same is not a regression and is omitted from the diff. State explicitly when a tool couldn't be diffed
because it wasn't run in the baseline — treat all its current issues as new. (This is separate from the project's
own PHPStan/Psalm baseline file, which the tools already applied before reporting.)

Do not fix any issue, run Pint/PHP-CS-Fixer/phpcbf/Rector without their dry-run flags, regenerate or edit a
baseline, or modify any tool configuration — those are follow-ups the user drives explicitly.
