---
name: iru-php-phpdoc
description: >-
  Audit given PHP file(s)/scope for complete, well-formed PHPDoc — class/interface/trait/enum docblocks, public and protected methods and properties, constants, generics and array shapes (`@template`, `@extends`/`@implements`, `list<T>`, `array<K, V>`, `array{...}`, `class-string<T>`, `non-empty-string`), and `@throws` — generate any missing or incomplete docblocks grounded in the actual code and current changes, without duplicating what native type declarations already say, then verify the result with the project's own tooling: PHPStan (which rejects invalid PHPDoc types and docblocks that contradict native types; Psalm when that's the project's analyser), the WordPress-Docs/Squiz commenting sniffs of PHP_CodeSniffer when configured, the project's Pint/PHP-CS-Fixer `phpdoc_*` rules, and phpDocumentor when the project has it (`phpdoc.dist.xml`/`phpdoc.xml` or `vendor/bin/phpdoc`). Flavor-aware: Laravel and plain libraries follow the PHPStan-typed "don't repeat native types" convention; WordPress plugins/themes follow the WordPress PHP inline documentation standards (file headers, `@since`, full `@param`/`@return` tags, hook docblocks with one `@param` per argument before every `do_action()`/`apply_filters()`); PrestaShop modules follow PrestaShop's conventions (docblocks on classes, properties, and methods regardless of visibility — the license header block itself is `iru-check-license`'s job, not this skill's). Invoke as `/iru-php-phpdoc <path-or-glob>` (comma-separated paths/globs accepted), or `/iru-php-phpdoc` with no argument to scope to PHP files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Use whenever the user wants PHPDoc completeness checked and filled in for specific files, instead of relying on a full static-analysis or docs build to surface gaps.
model: sonnet
allowed-tools: Read Edit Glob Grep Bash(git *) Bash(php *) Bash(vendor/bin/*) Bash(./vendor/bin/*) Bash(composer *) Bash(_PS_ROOT_DIR_=* *) Bash(./vendor/bin/sail *) Bash(npx wp-env *) Bash(ddev *) Bash(docker info *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p build*) Bash(rm -f build/iru-php-phpdoc-*) Bash(rm -rf build/iru-php-phpdoc-*)
---

# PHP PHPDoc

Make sure a set of PHP files carry complete, well-formed PHPDoc, filling in whatever is missing, then prove the result
is valid through the project's own tooling. This skill only adds/completes documentation comments — it does not
change behavior, signatures, native type declarations, attributes, or any non-comment code. Test code (`tests/`,
`*Test.php`, Pest files, `phpunit` bootstrap files) is out of scope for documentation requirements — it doesn't need
docblocks added, even if named explicitly — but any docblock a test file already has must be left as-is; never
strip or "clean up" existing comments in test code. It makes no assumptions about this being any particular
repository — discover the project's actual flavor, conventions, and tooling fresh each run.

## Step 0 — Detect the project's flavor and environment

Use the same flavor markers as `iru-php-code-quality` Step 1 (and `iru-explore`), first match wins:
`laravel/framework` + `artisan` → **laravel**; a root PHP file with a `Plugin Name:` header → **wordpress-plugin**;
`style.css` with `Theme Name:` and/or `theme.json` → **wordpress-theme**; a class that `extends Module`
(`PaymentModule`/`CarrierModule`) in the root `<module>.php`, `config.xml`, or `prestashop/*` packages →
**prestashop-module**; anything else → **library**. The flavor decides the documentation convention (Step 2) and
which verification tools apply (Step 5).

Resolve where PHP runs exactly as `iru-php-code-quality` does (host `php` preferred; else ddev/Sail/wp-env after
`docker info` succeeds). Editing comments needs no PHP; only Step 5 does.

## Step 1 — Determine scope

- **Argument provided** (comma-separated paths or globs): resolve each to its `.php` file(s) via `find`/`ls`. Drop
  any resolved test file per the definition above — say so in the Step 6 report rather than silently ignoring it.
- **No argument**: default to every non-test `.php` file touched by uncommitted changes plus commits on the current
  branch not yet on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask the
  user only if genuinely ambiguous).
- Always filter out `vendor/`, `node_modules/`, generated or cached code (`bootstrap/cache/`, `storage/`, `var/`,
  `build/`), Blade templates (`*.blade.php`), and PrestaShop's `index.php` guard files (the
  `header('Location: ../')` stubs `autoindex` drops in every folder).
- If the resulting scope is empty, tell the user there is nothing to document and stop.
- **What gets documented**, per in-scope file (the audit set for Step 3):
  - **library / laravel / prestashop-module**: every class, interface, trait, and enum; their public and protected
    methods (including constructors), properties (including constructor-promoted ones), and constants; enum cases
    whose meaning isn't obvious from the name; and top-level functions. PrestaShop requires docblocks on classes,
    properties, and methods **regardless of visibility**, so private members are in scope there too.
  - **wordpress-plugin / -theme**: all of the above, plus a **file header docblock** in every PHP file (theme template
    files such as `header.php`, `single.php`, or `template-parts/*.php` included — they need nothing else), every
    function (plugins and themes are largely procedural), `require`/`include` statements of other plugin files, and
    **every hook invocation** — `do_action()`, `do_action_ref_array()`, `apply_filters()`, `apply_filters_ref_array()`.

## Step 2 — Discover this project's actual PHPDoc bar before auditing

Don't assume a fixed convention — discover it from the project itself:

- Check a contributor guide (`CLAUDE.md`, `AGENTS.md`, `README`, `CONTRIBUTING`, Laravel Boost guidelines under
  `.ai/`/`.github/`) for a stated PHPDoc convention.
- **PHP_CodeSniffer config** (`phpcs.xml(.dist)`, `.phpcs.xml(.dist)`): `WordPress` or `WordPress-Docs` (the
  WordPress inline-docs rules, built from `Squiz.Commenting.*` and `Generic.Commenting.DocComment` — e.g.
  `Squiz.Commenting.FunctionComment.MissingParamTag` requires a `@param` for every parameter, typed or not, and
  `...MissingParamComment` a description on each — verified with WordPressCS 3.4), any
  `Squiz.Commenting.*`/`PEAR.Commenting.*` rules, and Slevomat rules that **forbid** redundant docs
  (`SlevomatCodingStandard.TypeHints.*TypeHint.UselessAnnotation`, `SlevomatCodingStandard.Commenting.UselessFunctionDocComment`).
  Note each rule's severity — they decide what Step 5 accepts.
- **Pint / PHP-CS-Fixer rules** that rewrite docblocks: `no_superfluous_phpdoc_tags` (in Pint's `laravel` preset
  and PHP-CS-Fixer's `@Symfony`/`@PhpCsFixer` sets — removes `@param`/`@return`/`@var` tags that only repeat the
  native type without adding a description), `phpdoc_align`, `phpdoc_separation`, `phpdoc_order`,
  `phpdoc_summary` (summary must end with a period), `phpdoc_to_comment`, `no_empty_phpdoc`. If `pint.json` enables
  **`Pint/phpdoc_type_annotations_only`**, the project deliberately keeps only `@`-annotation lines (prose summaries
  are stripped on the next `pint` run) — then write type annotations only, no summaries. Note Pint's `laravel`
  preset aligns tags with two spaces (`@param  array{title: string}  $row` — verified, `phpdoc_align`); match it.
- **PHPStan / Psalm**: the level (PHPStan ≥ 6 reports `missingType.iterableValue`/`missingType.generics` — every
  `array`, `iterable`, and generic class in a signature then *needs* a PHPDoc value type), and whether
  `treatPhpDocTypesAsCertain` is turned off (it changes how strongly a narrower PHPDoc type is trusted).
- If none of the above give a clear answer, skim 2-3 documented classes/functions near the ones in scope to see
  whether the project writes summaries on every method, `@param` for typed parameters, `@throws`, etc. — treat that
  observed practice as the bar, following the **stricter** of stated vs. observed so the output passes the
  project's own checks.

Skim a couple of existing, well-documented symbols structurally similar to what's in scope (a model if auditing a
model, a hook-heavy class if auditing hooks) to internalize phrasing, tag order, alignment, and whether a blank line
separates the summary from tags and tag groups from each other. If the project has nothing to learn from, fall back
to the flavor convention below.

**library / laravel — PHPStan-typed convention** (the docs reference's own guidance):

- One-sentence summary (third person, present tense — "Finds the books…"), optional description paragraph.
- **Don't repeat in PHPDoc what a native type already says.** `@param string $author` next to `string $author` adds
  nothing; add a `@param`/`@return`/`@var` only when it says something the native type can't —
  `list<Book>`, `array<string, int>`, `non-empty-array<…>`, array shapes `array{title: string, year: int, subtitle?: string}`,
  `non-empty-string`, `positive-int`, `int<1, 5>`, `class-string<Book>`, `callable(string): int`,
  `Closure(Book): bool`, `iterable<int, Book>`, `Collection<int, User>`, `T|null` for a generic — or when its
  description carries meaning (units, accepted values, what `null` means). A bare `array`/`iterable` in a signature
  always gets a value type.
- Generics: `@template T` / `@template T of object` on the class or method, `@extends Collection<Book>`,
  `@implements IteratorAggregate<int, Book>`, `@use HasFactory<UserFactory>` (as the Laravel skeleton does) — only
  where the type actually is generic.
- `@throws` for every exception the body throws or deliberately lets propagate from a call (`@throws InvalidArgumentException When $author is blank.`).
- Laravel specifics: relation methods get `@return HasMany<Post, $this>` (Larastan's generic relation types);
  `casts()` gets `@return array<string, string>`; Eloquent attributes Larastan already infers from migrations don't
  need `@property` tags unless the project already uses them (e.g. via IDE-helper conventions).
- Tool-specific overrides (`@phpstan-param`, `@phpstan-return`, `@psalm-…`, `@phpstan-assert`) only where the project
  already uses them.
- `@deprecated` is carried over verbatim, never added — and note the native `#[\Deprecated]` attribute is how new
  code emits a runtime notice; that's a code change, out of scope here.

**wordpress-plugin / -theme — WordPress PHP inline documentation standards**:

- Summary: one sentence, third-person singular verb, ending in a period. Functions say what they do; filters say
  what is filtered ("Filters the excerpt length."); actions say when they fire ("Fires after a book is saved.").
- `@since x.y.z` on every function, class, method, property, constant, and hook — the version that introduces the
  element: the plugin header's `Version:` (or `style.css` `Version:` for themes) when the change is part of the
  upcoming release; if that's ambiguous (the version wasn't bumped yet and no unreleased changelog entry names the
  next one), ask the user rather than guessing.
- `@param` for **every** parameter, with type and description — WordPress-Docs requires it even when the native
  type is declared: `@param int    $post_id Post ID.`; mark optional ones "Optional." with the default ("Default
  'publish'."); `bool`/`int`, not `boolean`/`integer`; aligned columns. Array arguments use hash notation, one
  `@type` line per key inside the `@param`'s braces. `@return` with type and description when the function returns
  something (no `@return void`). `@global` for globals used. Never add `@author`; `@copyright`/`@license` belong
  only to bundled third-party libraries.
- **File header**: a summary statement with no trailing period, an optional description, `@package <PluginName>`
  (themes: `<Theme_Name>` with underscores; never `@package WordPress`), and `@since`.
- **Hooks**: a docblock on the line immediately before the `do_action()`/`apply_filters()` call (or before the
  enclosing HTML block / long conditional when the call sits inside one), with summary, optional description,
  `@since`, and one `@param` per argument passed after the hook name, in order — no `@return`. phpstan-wordpress
  validates these (verified against phpstan-wordpress 2.x): its rule reports `paramTag.count` ("Expected N @param tags, found M."), `phpDoc.parseError` (a
  malformed or `$this`-named `@param`), and `parameter.phpDocType` (a `@param` type that doesn't accept the actual
  argument), and it treats a filter's first `@param` type as the filter's return type. Dynamic hook names
  (`"save_post_{$post->post_type}"`) are documented the same way with the variable part kept in the name. A hook
  fired in more than one place is documented fully once; other occurrences get a one-line
  `/** This filter is documented in path/to/file.php */`.

**prestashop-module — PrestaShop conventions**:

- The file must already start with the module's AFL-3.0 license block — that block is maintained by
  `iru-check-license` (or `vendor/bin/header-stamp`); never edit it here, and place new docblocks after it.
- Classes, properties, and methods get docblocks regardless of visibility; describe intent rather than
  implementation, and document parameters and return values in both type and meaning.
- Arrays: `string[]` for simple collections, `array<int, string>` when keys matter, array shapes for structs with a
  known schema. Module code that still supports PHP versions without native parameter/return types (check
  `composer.json` `require.php` and `config.xml`'s `ps_versions_compliancy`) relies on docblocks for every type —
  write full `@param`/`@return` tags there.
- Hook methods (`hookDisplayHeader(array $params)`, …) document the `$params` keys the hook actually passes.
- Deprecations, when already present, keep PrestaShop's `@deprecated Since x.y.z, use …() instead.` form.

## Step 3 — Audit each in-scope file

Read the full file, then for every symbol in Step 1's audit set check that a `/** ... */` docblock exists, sits
directly above the declaration (attributes may sit between docblock and declaration), and actually describes the
symbol's purpose rather than restating its name, per the bar from Step 2:

- **Classes, interfaces, traits, enums**: a docblock on the type, with `@template`/`@extends`/`@implements`/`@use`
  where the type is generic or extends/implements/uses a generic type.
- **Methods and functions**: summary; `@param` where the bar requires it (always for WordPress/PrestaShop; for
  library/laravel only where a native type can't express the real type, or there is no native type at all);
  `@return` likewise; `@throws` for each exception that can propagate. Check existing tags still match the current
  signature — a `@param` for a renamed/removed parameter, or in the wrong order, is a gap too.
- **Properties and constants**: a docblock (or a one-line `/** @var list<string> */` where only the type needs
  refining); constructor-promoted properties are documented through the constructor's `@param`.
- **Overrides / interface implementations**: only document them separately if the project does; otherwise rely on
  inherited PHPDoc (PHPStan and phpDocumentor inherit it), or `{@inheritDoc}` if that's the project's habit.
- **WordPress**: file header; every hook invocation; `require`/`include` lines get a short `/** ... */` comment
  saying what is loaded.

For each gap record: the symbol, its kind, what's missing (whole docblock vs. a missing/stale tag), and the file.

## Step 4 — Generate the missing PHPDoc

Before editing, if PHPStan (or Psalm) is wired, run it once on the in-scope files exactly as Step 5 does and keep
the per-file results as this run's baseline — Step 5 needs it to tell pre-existing errors from ones the new docs
caused.

For every gap from Step 3, write the docblock grounded in:

- The actual implementation — read the body: which array keys are read or written (for a shape), what the list
  elements are, which exceptions are thrown or rethrown, what `null`/`false` returns mean, which arguments a hook
  passes. Never invent a narrower type than the code guarantees: a `@return list<string>` on something that can
  return an associative array is a lie PHPStan will either reject or, worse, trust.
- Current uncommitted/branch changes (`git diff` / `git log -p` for that file) — describe current behavior, not what
  the name suggests.
- The conventions from Step 2 — voice, tag order, alignment, blank-line layout — so new comments are
  indistinguishable from hand-written ones.

Apply the edits with the Edit tool. Do not modify code logic, signatures, native types, attributes, the license
header, or formatting outside the added/completed comments, and don't reorder members.

## Step 5 — Verify

Run what the project has, scoped to the in-scope files, through the environment from Step 0. Write any report under
`build/` with an `iru-php-phpdoc-` prefix and delete it afterwards (remove `build/` only if this run created it).

1. **PHPStan** (when wired — config and flags exactly as `iru-php-code-quality` Step 2 runs it, including
   `_PS_ROOT_DIR_` for PrestaShop):
   `vendor/bin/phpstan analyse --no-progress --error-format=json [-c <config>] [--memory-limit=1G] <files> > build/iru-php-phpdoc-phpstan.json`
   (pass `--memory-limit=1G` whenever phpstan-wordpress/Larastan/the PrestaShop extension is loaded — verified: with
   phpstan-wordpress the default 128M crashes the worker and the JSON holds only a top-level `errors` entry about
   `Allowed memory size`, i.e. no validation happened). PHPStan validates PHPDoc from level 2 up. Compare against the Step 4 baseline: any **new** error in an in-scope
   file was caused by the docblocks, since nothing else changed — typically `phpDoc.parseError` (unparseable type
   or tag), `parameter.phpDocType` / `return.phpDocType` / `property.phpDocType` (PHPDoc type incompatible with the
   native type), `parameter.notFound` (`@param` naming a parameter that doesn't exist), `throws.notThrowable` /
   `class.notFound` (an unimported or misspelled class in a PHPDoc type — import it with `use` or fully qualify it),
   `throws.unusedType` (a `@throws` for an exception the body never throws), `missingType.*`, `generics.*`,
   `paramTag.count` (phpstan-wordpress hook docs), or a new error in the body because a narrower PHPDoc type is now
   trusted (`*.alwaysTrue`, `deadCode.*`) — the last one means the docblock overstates the code; widen it. Fix and
   re-run until no new errors remain. Pre-existing errors are not this skill's to fix. Because narrower types also
   flow into callers, when the project's PHPStan run is affordable (result cache warm, or a small project) also run
   it project-wide and report — not fix — any new error outside scope.
   If the project uses **Psalm** instead, run `vendor/bin/psalm --output-format=json --no-progress <files>` the
   same way (`InvalidDocblock`, `MismatchingDocblockParamType`, `MismatchingDocblockReturnType`,
   `UndefinedDocblockClass`).
   With neither wired, at least run `php -l <file>` on each edited file and say in the report that no PHPDoc type
   validation was available.
2. **PHP_CodeSniffer documentation sniffs** (when the config references `WordPress`, `WordPress-Docs`, or any
   `*.Commenting.*` rules):
   `vendor/bin/phpcs --report=json --report-file=build/iru-php-phpdoc-phpcs.json -q --basepath=. <files>`, then look at
   messages whose `source` starts with `Squiz.Commenting.`, `Generic.Commenting.`, `PEAR.Commenting.`,
   `SlevomatCodingStandard.Commenting.`, or ends in `.UselessAnnotation`. Fix every one in the comments you wrote.
   For a WordPress project whose config doesn't include WordPress-Docs but has WordPressCS installed
   (`vendor/bin/phpcs -i` lists it), you may additionally run `--standard=WordPress-Docs` on the files as an
   advisory check — say so, and don't treat its findings as failures the project enforces.
3. **Pint / PHP-CS-Fixer docblock rules** (when configured): run the style check on the edited files in dry-run mode
   (`vendor/bin/pint --test -v <files> --output-to-file=build/iru-php-phpdoc-pint.json --output-format=json`, or
   `vendor/bin/php-cs-fixer check --format=json -v --path-mode=intersection <files>`) and adjust the comments you
   wrote for any `phpdoc_*`, `no_superfluous_phpdoc_tags`, `no_empty_phpdoc`, or `Pint/phpdoc_type_annotations_only`
   fixer the report lists — by hand, never by running the fixer (it would reformat code beyond the comments).
   Pre-existing non-docblock style findings are out of scope.
4. **phpDocumentor**, only when the project has it — a `phpdoc.dist.xml`/`phpdoc.xml` (a `phpdoc.xml` takes
   precedence over `phpdoc.dist.xml`), `vendor/bin/phpdoc`, or a composer script that builds API docs:
   `vendor/bin/phpdoc run [-c <config>] -t build/iru-php-phpdoc-site --cache-folder build/iru-php-phpdoc-cache`
   (when the project runs it from the `phpdoc/phpdoc` Docker image or a downloaded `phpDocumentor.phar`, use that
   same invocation with the same output overrides). Writing to a throwaway target keeps the project's real docs
   output untouched. Treat a non-zero exit or any error-level log line naming an in-scope file (a docblock it
   couldn't parse, an unresolvable type) as a failure to fix; phpDocumentor also lists parse problems in the
   generated site's errors report. Delete the throwaway output afterwards.

A failure naming a symbol or file **outside** the current scope is pre-existing — mention it in the report as a
follow-up, don't fix it unless the user asks.

## Step 6 — Report

Per file in scope: how many symbols were already fully documented, how many gaps were found and filled (name each,
with its kind and what was added — e.g. "`Shelf` class: `@template T of object`", "`titlesBy()`: `@param list<array{...}> $books`, `@throws InvalidArgumentException`",
"`apply_filters( 'myplugin_excerpt_length' )`: hook docblock with 2 `@param`"), and for WordPress files whether a
file header was added. Then the verification result per tool that ran — PHPStan/Psalm: no new errors vs. baseline
(or the identifiers still open), phpcs commenting sniffs: pass or the remaining sources, Pint/PHP-CS-Fixer docblock
rules: pass or remaining fixers, phpDocumentor: pass/fail — and which tools weren't available. Name any argument
that resolved to a test file and was excluded, any `@since` version you had to ask about, and any out-of-scope
pre-existing failures as follow-ups. Never paste raw tool output or JSON.

Do not fix static-analysis or style issues unrelated to docblocks, change code to make a docblock "true", edit
license headers, or add/modify tests — those are a separate quality/implementation skill's job.
