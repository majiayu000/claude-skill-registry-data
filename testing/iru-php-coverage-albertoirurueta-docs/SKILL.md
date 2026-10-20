---
name: iru-php-coverage
description: Run a PHP project's tests (Pest, PHPUnit, or Laravel's `php artisan test`, in whichever environment the project uses — host PHP, Sail, ddev, or wp-env) with code coverage enabled, using PCOV when loaded and falling back to Xdebug in `coverage` mode, write a Clover XML report (`--coverage-clover`), and read it to report the exact per-class / per-file line coverage (plus method coverage, and branch/path coverage when Xdebug path coverage is enabled) and uncovered line ranges for the target classes. Invoke as `/iru-php-coverage <selector> [TargetClass1,TargetClass2,...]` — the selector uses the same syntax as the `iru-php-test` skill's (file, directory, `--filter <pattern>`, `--testsuite <name>`, `--group <name>`) — or `/iru-php-coverage` with no argument to run the whole suite and report whole-project coverage. Detects the coverage driver via `php -m` and reports "no coverage driver available" (with how to install PCOV) instead of a false 0%, and avoids the `php -d extension=...` pitfall with `php artisan test`'s child process. Use whenever the user wants to check, or verify a bar (e.g. "at least 80% line coverage") for, a PHP class, file, or the whole project, instead of eyeballing the runner's console table.
model: haiku
allowed-tools: Read Bash(php *) Bash(vendor/bin/*) Bash(./vendor/bin/*) Bash(composer *) Bash(./vendor/bin/sail *) Bash(npx wp-env *) Bash(ddev *) Bash(docker info *) Bash(docker ps *) Bash(XDEBUG_MODE=* *) Bash(PHP_INI_SCAN_DIR=* *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(awk *) Bash(sort *) Bash(test *) Bash(mkdir -p build*) Bash(rm -f build/iru-php-coverage-*)
---

# PHP Coverage

Run the project's PHP tests with a coverage driver enabled and report the exact, measured coverage percentage for
the class(es)/file(s) the user cares about, read from a Clover XML report. This skill only measures and reports
coverage — it does not add tests, modify source/test code, or install extensions unless asked to as a follow-up.

## Step 1 — Determine the test scope, environment, and runner

If the user (or the calling skill) gave a selector, it uses the exact same syntax as the `iru-php-test` skill's
Step 4 table (file, directory, `--filter <pattern>`, `--testsuite <name>`, `--group <name>`, `-c <config>`). If no
selector was given, run the whole suite.

Detect the execution environment (host PHP / Sail / ddev / wp-env, including the `docker info` check), the runner
(Pest / PHPUnit / `php artisan test`), the PHPUnit config file(s), and the unit-vs-integration split exactly as
`iru-php-test` Steps 1–3 do, and stop with the same plain-words report when the environment is missing.

Important, same caveat as `iru-java-coverage`: coverage is only recorded for code exercised by the tests that run in
this invocation. If a class is covered by tests spread across several files or suites (e.g. a Laravel class hit by
both `tests/Unit` and `tests/Feature`, or a WordPress plugin class hit by both the Brain Monkey unit suite and the
`WP_UnitTestCase` integration suite), a narrow selector undercounts it — when in doubt, prefer a broader selector
(the containing directory, the whole suite) over a narrow one, and say which suites were included.

## Step 2 — Determine the target class(es)/file(s) to report on

- If the user (or the calling skill) explicitly named target class(es), use those (short name `Foo` or FQCN
  `App\Services\Foo`).
- Otherwise infer them from the selector by convention: `tests/Unit/FooTest.php` / `--filter FooTest` targets
  `Foo`; `FooTest::testBar` still targets `Foo`; a Pest file `tests/Unit/FooTest.php` likewise targets `Foo`.
- A directory, testsuite, group, or description filter can't be inferred by name — report on every class/file the
  Clover report lists for the run (Step 5 surfaces them), or ask which ones matter if the run touches many unrelated
  ones.
- Procedural code (WordPress plugin/theme `functions.php`, hook callbacks, PrestaShop module main files with free
  functions) has no class row — report it per **file** instead.
- What gets measured at all comes from the `<source>` element of `phpunit.xml` (`<coverage>` on PHPUnit 9 configs,
  `<filter><whitelist>` on very old ones). Files under `<source><include>` that no test loaded still appear at 0% —
  so a target missing from the report means it's outside `<source>` (or excluded), not that it's uncovered. Check
  the config before concluding anything; and note that `#[CoversClass]`/`@covers` restricts which code a test is
  allowed to count (with `requireCoverageMetadata`/`beStrictAboutCoverageMetadata` set, tests without it contribute
  nothing).

## Step 3 — Detect the coverage driver (never trust a 0% without this)

Run the check **in the same environment the tests run in** (`php -m`, `./vendor/bin/sail php -m`, `ddev exec php
-m`, or for wp-env the test environment's `cli` — `npx wp-env run cli --config=.wp-env.test.json php -m`, or
`tests-cli` only on older projects still using the deprecated `testsEnvironment`; never the development site):

```bash
php -m | grep -i -E '^(pcov|xdebug)$'
php -r 'echo "pcov.enabled=", ini_get("pcov.enabled"), " pcov.directory=", ini_get("pcov.directory"), " xdebug.mode=", ini_get("xdebug.mode"), PHP_EOL;'
```

Choose, in order:

1. **PCOV loaded** → use it (much faster; line coverage only — no branch/path data). It must be enabled
   (`pcov.enabled=1`); pass `-d pcov.enabled=1` when invoking the runner binary directly. PCOV's default
   `pcov.directory` is auto-detected as `src/`, else `lib/`, else `app/` under the working directory — a project whose
   code lives elsewhere (WordPress plugins' `includes/`/`inc/`, PrestaShop modules' `classes/`/`controllers/`, code at
   the root) silently records **nothing** for it. In that case pass `-d pcov.directory=.` (and optionally
   `-d pcov.exclude='~vendor~'`).
2. **Xdebug loaded** (and PCOV not) → run with `XDEBUG_MODE=coverage` in the environment (Xdebug 3 ignores coverage
   unless `coverage` is in `xdebug.mode`). Slower than PCOV, but the only driver that can produce branch and path
   coverage (Step 4).
3. **Neither** → **stop and report "no coverage driver available"** — PHPUnit/Pest still run the tests but only
   print a `No code coverage driver available` warning and write no Clover file. Never report 0%. Tell the user how
   to install PCOV: `pecl install pcov` then `extension=pcov.so` in a `conf.d` ini (`php --ini` shows where); in a
   Docker image, `install-php-extensions pcov` (mlocati/docker-php-extension-installer) or the distro package
   (`apt-get install php8.x-pcov`); in Sail, check `./vendor/bin/sail php -m` (the Sail runtimes ship Xdebug, enabled
   for coverage with `SAIL_XDEBUG_MODE=develop,debug,coverage` in `.env` and `sail up`); in ddev, `ddev xdebug on`
   loads Xdebug; in wp-env, restart the **test** environment with Xdebug, `npx wp-env start --config=.wp-env.test.json
   --xdebug=coverage` (restarts it — ask first; never start the development environment for this).

**The `php -d` pitfall with `php artisan test`**: `artisan test` (and `--parallel` in any runner) re-launches Pest/
PHPUnit in a **child process that does not inherit `-d` options** — `php -d extension=pcov.so -d pcov.enabled=1
artisan test --coverage` measures nothing. Either call the runner binary directly (`php -d pcov.enabled=1
vendor/bin/pest ...`, preferred — same tests, same `phpunit.xml`), or load the driver through an ini file the child
also reads: create a directory containing `pcov.ini` (`extension=pcov.so` + `pcov.enabled=1`) and run
`PHP_INI_SCAN_DIR="<original scan dir from php --ini>:<that dir>" php artisan test ...`. Never add `--parallel`
here. Environment variables such as `XDEBUG_MODE=coverage` *are* inherited by the child, so Xdebug doesn't hit this.

## Step 4 — Run the coverage build

Write the report **inside the project** (so the path works in Sail/ddev/wp-env containers too), delete any stale one
first, and keep a JUnit log only if you also need failure details:

```bash
rm -f build/iru-php-coverage-clover.xml && mkdir -p build

# PHPUnit, PCOV
php -d pcov.enabled=1 vendor/bin/phpunit [scope] --coverage-clover build/iru-php-coverage-clover.xml
# PHPUnit, Xdebug
XDEBUG_MODE=coverage vendor/bin/phpunit [scope] --coverage-clover build/iru-php-coverage-clover.xml
# Pest (same PHPUnit coverage options)
php -d pcov.enabled=1 vendor/bin/pest [scope] --coverage-clover build/iru-php-coverage-clover.xml
# Laravel artisan (driver loaded via ini or XDEBUG_MODE, see Step 3)
XDEBUG_MODE=coverage php artisan test [scope] --coverage-clover build/iru-php-coverage-clover.xml
# Sail / ddev / wp-env — same command behind the Step 1 prefix, e.g.
./vendor/bin/sail php -d pcov.enabled=1 vendor/bin/pest [scope] --coverage-clover build/iru-php-coverage-clover.xml
ddev exec XDEBUG_MODE=coverage vendor/bin/phpunit [scope] --coverage-clover build/iru-php-coverage-clover.xml
npx wp-env run cli --config=.wp-env.test.json --env-cwd=wp-content/<plugins|themes>/<dir> env XDEBUG_MODE=coverage vendor/bin/phpunit -c phpunit-integration.xml.dist [scope] --coverage-clover build/iru-php-coverage-clover.xml
# (mirror the project's own test:integration script when it exists; `tests-cli` without --config only for older
#  projects still on the deprecated testsEnvironment)
```

Add `-c <config>` when the selection lives in a non-default config. Don't add `--min=N`/`--coverage` table flags:
this skill compares against the user's bar itself from the Clover numbers.

**Branch and path coverage** (Xdebug only): add `--path-coverage` and also write a text summary,
`--coverage-text=build/iru-php-coverage-text.txt`. Clover is line/method-oriented, so take the per-class
`Branches:`/`Paths:` percentages from that text file (its `Summary:` block and per-class rows). Only do this when the
user asks for branch/path coverage — it is noticeably slower. With PCOV, say branch/path coverage is unavailable
rather than reporting n/a as 0.

If the run fails (fatal error, environment missing, or test failures), report that — a Clover file may still be
written after test failures, but say the numbers come from a failing run; if no Clover file was written, don't read
a stale one.

## Step 5 — Read the exact coverage from the Clover XML

Shape written by phpunit/php-code-coverage (also for Pest and `artisan test`):

```xml
<coverage generated="...">
  <project timestamp="...">
    <package name="App\Services">            <!-- namespaced files may be grouped in packages; others sit directly under <project> -->
      <file name="/var/www/html/app/Services/Foo.php">   <!-- absolute path, as seen by the PHP that ran (container paths in Docker) -->
        <class name="App\Services\Foo" namespace="App\Services">
          <metrics complexity="4" methods="3" coveredmethods="2" conditionals="0" coveredconditionals="0"
                   statements="20" coveredstatements="15" elements="23" coveredelements="17"/>
        </class>
        <line num="12" type="method" name="bar" visibility="public" complexity="1" crap="1" count="3"/>
        <line num="13" type="stmt" count="3"/>
        <line num="17" type="stmt" count="0"/>
        <metrics loc="40" ncloc="32" classes="1" methods="3" coveredmethods="2" ... statements="20" coveredstatements="15" .../>
      </file>
    </package>
    <metrics files="12" loc="..." ... statements="410" coveredstatements="301" .../>   <!-- whole-project totals -->
  </project>
</coverage>
```

Compute:

```
line coverage %    = coveredstatements / statements * 100        (n/a if statements is 0, e.g. an interface or enum)
method coverage %  = coveredmethods / methods * 100
```

Match a target class by its `name` attribute — exactly the FQCN, or ending in `\<ShortName>` (some versions put
only the short name in `name` and the namespace in `namespace`; handle both) — never a substring, so `FooBar` doesn't
match `Foo`. Match a target **file** by path suffix (`app/Services/Foo.php`), since paths are absolute and differ
between host and container.

With PHP available in the environment, extract totals, the target rows, and uncovered lines in one pass:

```bash
php -r '$x = simplexml_load_file($argv[1]); $want = array_filter(explode(",", $argv[2] ?? ""));
  $t = $x->project->metrics;
  printf("TOTAL lines %d/%d (%.2f%%) methods %d/%d\n", $t["coveredstatements"], $t["statements"], $t["statements"] > 0 ? 100 * $t["coveredstatements"] / $t["statements"] : 0, $t["coveredmethods"], $t["methods"]);
  foreach ($x->xpath("//file") as $f) {
    foreach ($f->class as $c) {
      $n = (string) $c["name"]; $fq = (string) $c["namespace"] !== "" && !str_contains($n, "\\") ? $c["namespace"] . "\\" . $n : $n;
      $hit = !$want; foreach ($want as $w) { if ($fq === $w || str_ends_with($fq, "\\" . $w)) $hit = true; }
      if (!$hit) continue; $m = $c->metrics;
      printf("%s lines %d/%d (%s) methods %d/%d\n", $fq, $m["coveredstatements"], $m["statements"], $m["statements"] > 0 ? sprintf("%.2f%%", 100 * $m["coveredstatements"] / $m["statements"]) : "n/a", $m["coveredmethods"], $m["methods"]);
    }
    $u = []; foreach ($f->line as $l) { if ((string) $l["type"] === "stmt" && (int) $l["count"] === 0) $u[] = (int) $l["num"]; }
    if ($u && (!$want || array_filter($want, fn($w) => str_contains((string) $f["name"], "/" . basename(str_replace("\\", "/", $w)) . ".php")))) {
      sort($u); $r = []; $s = $p = array_shift($u); foreach ($u as $n) { if ($n === $p + 1) { $p = $n; continue; } $r[] = $s === $p ? "$s" : "$s-$p"; $s = $p = $n; } $r[] = $s === $p ? "$s" : "$s-$p";
      printf("  %s uncovered: %s\n", $f["name"], implode(", ", $r));
    }
  }' build/iru-php-coverage-clover.xml 'Foo,App\Services\Bar'
```

(Omit the second argument to list every class.) Run it through `./vendor/bin/sail php` / `ddev exec php` when PHP
only exists in the container. Without any PHP to parse with, fall back to `awk` on one file's block:

```bash
# Uncovered statement lines of one file, collapsed into ranges
awk -v f='app/Services/Foo.php' 'index($0,"<file ") && index($0,f"\"") {p=1} p && /type="stmt"/ && /count="0"/ {match($0,/num="[0-9]+"/); print substr($0,RSTART+5,RLENGTH-6)} p && /<\/file>/ {p=0}' \
  build/iru-php-coverage-clover.xml | sort -n | awk '
  { if (NR==1) { start=$1; prev=$1; next }
    if ($1==prev+1) { prev=$1; next }
    print (start==prev ? start : start"-"prev); start=$1; prev=$1 }
  END { if (NR>0) print (start==prev ? start : start"-"prev) }'
```

If a target class/file doesn't appear in the report at all, it is outside the config's `<source>` (or excluded, or
PCOV's `pcov.directory` didn't include it — Step 3) — report that explicitly rather than a false 0%. A target that
appears with `coveredstatements="0"` genuinely is 0%.

Delete the generated files afterwards (`rm -f build/iru-php-coverage-*`; remove `build/` only if this run created
it) so they don't get committed.

## Step 6 — Report results

State the driver used (PCOV / Xdebug) and the environment/runner, then, per target class (or file for procedural
code), the line coverage percentage (and method coverage; branch/path only when collected with Xdebug
`--path-coverage`), computed from the actual Clover numbers — never estimate or guess, and never paste the Clover
XML or the runner's console table. If the user's bar is "at least N%", say clearly whether each target and the total
meets it.

For targets under the bar, give the uncovered line ranges (e.g. `App\Services\Foo: lines 75.00% — uncovered: 17,
24-31`) so the user (or a follow-up skill) knows exactly where to add tests.

If no coverage driver was available, the environment was missing, or a target fell outside `<source>`, report that
instead of a percentage, with the exact command that failed and the fix.

Do not add tests, modify source/test code, install extensions, or re-run anything to try to raise coverage — that's a
follow-up the user (or another skill, e.g. `iru-code`) drives explicitly.

## Verification notes

Verified in Docker (`php:8.4-cli` with PCOV from PECL, `composer:2`) against PHPUnit 12 and Pest 4: `php -d
pcov.enabled=1 vendor/bin/{phpunit,pest} --coverage-clover …` writes the Clover file, and both the `php -r` parser
and the `awk` fallback above report the correct totals, per-class line/method figures, and uncovered line ranges —
the Clover `class@name` was the fully-qualified name (`App\Services\Foo`) for both runners, and file paths are the
container's (`/app/src/Foo.php`), which is why targets are matched by path suffix. Still unverified: Xdebug
`--path-coverage` branch/path rows, `php artisan test --coverage` with `PHP_INI_SCAN_DIR`, Sail's bundled drivers,
and wp-env's `--xdebug=coverage`.
