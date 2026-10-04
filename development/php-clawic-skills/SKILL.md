---
name: PHP
slug: php
version: 1.0.2
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
description: 'Writes, debugs, and reviews PHP: type juggling, arrays, OOP, Composer, PDO, sessions, PHP-FPM, OPcache, PHP 8 features. Use when PHP returns a blank white page or a 500 with no message, when "headers already sent", "Allowed memory size exhausted", "Maximum execution time exceeded", "Class not found" after a Composer install, or an undefined array key warning appears; when `==` compares wrong, `strpos` or `preg_match` returns a falsy match, accents turn into mojibake, `DateTime` shifts by a day or an hour, `json_encode` returns false, PDO refuses to bind a parameter or emulates prepares, sessions serialize parallel AJAX requests, nginx answers 502 or 504 in front of PHP-FPM, OPcache keeps serving old code, or a version upgrade breaks on deprecations. Also for escaping output, hashing passwords, sizing FPM workers, writing PHPUnit tests, and clearing PHPStan errors. Not for framework internals — `laravel` covers Eloquent, queues, and Laravel auth.'
homepage: https://clawic.com/skills/php
metadata:
  clawdbot:
    emoji: 🐘
    requires:
      bins:
      - php
    os:
    - linux
    - darwin
    - win32
    displayName: PHP
    configPaths:
    - ~/Clawic/data/php/
    - ~/php/
    - ~/clawic/php/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/php/
      - ~/php/
      - ~/clawic/php/
---

User preferences live in `~/Clawic/data/php/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/php/` or `~/clawic/php/`), move it to `~/Clawic/data/php/`, and say in one line that you moved it and from where.

## When To Use

- Writing or reviewing PHP — read Core Rules and Output Gates before emitting code
- Any error whose cause is not obvious in ten seconds: white page, silent 500, wrong value with no exception, a hang
- Runtime and deployment work: php.ini precedence, FPM pool sizing, OPcache, CLI workers, cron
- Dependency and upgrade work: Composer constraints, autoloading, deprecations, moving to a newer 8.x
- Data-boundary work: PDO queries, JSON payloads, uploads, sessions, dates, encodings
- Hardening: escaping per context, password hashing, deserialization, path containment, upload validation
- Not for framework internals — `laravel` owns Eloquent, queues, Blade, and Laravel auth

## Quick Reference

| Situation | Play |
|-----------|------|
| `==` compares wrong, a numeric string misbehaves, floats do not add up | `===` everywhere; `"0e12" == "0e34"` is true → `hash_equals` → `types.md` |
| Keys vanish, order is wrong, a filtered list encodes as a JSON object | `array_filter` keeps keys; `array_values()` before encoding → `arrays.md` |
| Accents break, `strlen` disagrees with what you see, a regex silently fails | `mb_*` for text, `/u` on every pattern, check `preg_last_error()` → `strings.md` |
| Class design: traits, `static::`, readonly, enums, magic methods, clone | `self::` binds at compile time, `static::` at call time → `oop.md` |
| Exceptions, error handlers, warnings you cannot see, fatal errors | Catch `\Throwable`; fatals need `register_shutdown_function` → `errors.md` |
| Injection, XSS, uploads, `unserialize`, passwords, tokens | Bind every value, escape per output context, `random_bytes` for secrets → `security.md` |
| Which PHP 8 feature to use, and how it bites | `match` is strict and exhaustive; named args make parameter names API → `modern.md` |
| Upgrading PHP, a deprecation wall, "which version can I still target" | Run the OLD version with deprecations as errors first → `versions.md` |
| `Class not found`, lock conflicts, `^` vs `~`, slow or huge installs | Commit the lock for apps, never for libraries → `composer.md` |
| White page, silent 500, "it worked yesterday", a hang with no output | Symptom → cause chains, plus the Xdebug 3 setup that actually works → `debugging.md` |
| Slow requests, high memory, "should we turn on JIT" | OPcache first, profile second; JIT does almost nothing for I/O-bound web → `performance.md` |
| A setting you changed has no effect; CLI and web disagree | `php --ini` per SAPI; `.user.ini` is cached for 300s → `php-ini.md` |
| 502, 504, "server reached pm.max_children", workers eating RAM | Size from measured RSS; `slowlog` names the hung function → `fpm.md` |
| Console scripts, daemons, cron, signals, exit codes | `max_execution_time` is 0 on CLI; recycle workers on a job count → `cli.md` |
| PHPUnit setup, flaky or falsely-passing tests, coverage, mocks | `assertSame` not `assertEquals`; static state leaks between tests → `testing.md` |
| PHPStan or Psalm errors, baselines, coding standard, automated refactors | Baseline the legacy, ratchet one level per merge → `static-analysis.md` |
| PDO connections, binding, transactions, "MySQL server has gone away" | `charset=utf8mb4` in the DSN, `EMULATE_PREPARES => false` → `database.md` |
| Request/response handling, JSON bodies, uploads, outbound HTTP calls | JSON bodies live in `php://input`, not `$_POST` → `http.md` |
| Parallel requests from one user run one at a time; logins do not stick | `session_start()` holds an exclusive lock — `session_write_close()` early → `sessions.md` |
| Dates off by a day or an hour, DST, parsing, storage | `DateTimeImmutable` + IANA zones; `createFromFormat` inherits today → `datetime.md` |
| `json_decode` returns null, big IDs lose digits, `json_encode` returns false | Always pass `JSON_THROW_ON_ERROR` → `json.md` |
| Reading or writing files, CSV, streams, temp files, permissions | Stream instead of slurping; write temp then `rename()` → `files.md` |
| Parallel work, queues, locks across processes, long-running runtimes | Share-nothing per request; `proc_open` deadlocks if you read one pipe → `concurrency.md` |
| Anything else | Core Rules below, then reproduce with `php -d error_reporting=E_ALL -d display_errors=1 -r '<five suspect lines>'` and add one thing back at a time |

Each file above is one sub-job and is self-contained: read SKILL.md by default, open exactly one guide when the situation matches.

## Core Rules

1. `declare(strict_types=1);` on line 1 of every file. It is per-file and governs the CALLS made in that file, not the functions declared there — so an untyped legacy caller still passes `"7"` into your `int` parameter. Return values are checked against the mode of the file where the function is DECLARED (`types.md`).
2. `===` and `!==` by default; `==` only where both operand types are proven. Worked case: `"0e12" == "0e34"` is `true` because both are numeric strings equal to 0 — a hash compared with `==` accepts the wrong password. Compare digests with `hash_equals($known, $given)`, which is also constant-time.
3. Check anything that can return `false` with `!== false`, never with truthiness. `strpos($haystack, $needle)` returns `0` for a match at offset 0, and `if (!strpos(...))` reads that correct answer as a miss; the same shape breaks `preg_match` (`0` = no match, `false` = engine error) and `file_get_contents` (`""` is a valid file).
4. Every SQL value is a bound parameter; every identifier comes from an allowlist you wrote. Placeholders cannot stand in for table or column names, and with the MySQL driver's default emulation the "prepared" statement is interpolated client-side — set `PDO::ATTR_EMULATE_PREPARES => false` (`database.md`).
5. Escape at output, per context, never at input. `htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')` covers HTML body and quoted attributes only; a value going into JavaScript needs `json_encode` with the HEX flags, one going into a URL needs `rawurlencode`, one going into a shell needs `escapeshellarg` (`security.md`).
6. Text is characters, not bytes: `strlen`, `substr`, `str_pad`, `strrev`, and `ucfirst` count bytes and will cut a UTF-8 sequence in half. Use `mb_strlen`/`mb_substr`/`mb_str_pad` (`php >=8.3`) for anything a human reads; keep the byte functions for binary data, where they are the correct tool.
7. `DateTimeImmutable` everywhere. `DateTime::modify()` mutates the object that every reference shares, so a helper that "returns tomorrow" also moves the caller's date. The same call on an immutable returns a new instance and the bug cannot happen (`datetime.md`).
8. Every call that leaves the process gets an explicit timeout: `CURLOPT_TIMEOUT` plus `CURLOPT_CONNECTTIMEOUT`, a stream context `timeout` for `fopen`, `PDO::ATTR_TIMEOUT` for connections. `max_execution_time` will not save you — on Unix it does not count time spent inside system calls, so a hung socket read is only killed by FPM's `request_terminate_timeout` (`fpm.md`).
9. Stream instead of slurping. `file_get_contents` on a 400 MB export needs 400 MB plus copies inside the default 128M `memory_limit`; `fgetcsv` in a loop, or a generator, holds one row. The same rule retires `fetchAll()` on large result sets (`files.md`, `performance.md`).

## Version Floors

The floors that shape everyday code. Individual guides carry more, inline in this same `php >=X.Y` form next to the instruction each one gates. Support windows and the upgrade procedure: `versions.md`.

| Feature | Needs |
|---|---|
| Typed properties, arrow functions `fn() =>`, spread in calls, `??=`, covariant return types | php >=7.4 |
| `match`, named arguments, constructor promotion, `?->`, union types, attributes, `str_contains`/`str_starts_with`/`str_ends_with`, `static` return type, `throw` as an expression, saner string-to-number comparison, PDO defaulting to exception error mode | php >=8.0 |
| Enums, `readonly` properties, fibers, `never`, first-class callables `f(...)`, `new` in initializers, `array_is_list()`, string-keyed array unpacking, overridable interface constants, `htmlspecialchars` escaping single quotes by default | php >=8.1 |
| `readonly` classes, DNF types, `null`/`false`/`true` as standalone types, locale-independent `strtolower`/`strtoupper`, dynamic properties deprecated, `${var}` interpolation deprecated | php >=8.2 |
| Typed class constants, `#[\Override]`, `json_validate()`, `mb_str_pad()`, readonly reinitialization inside `__clone`, stack-overflow detection via `zend.max_allowed_stack_size` | php >=8.3 |
| Property hooks, asymmetric visibility, `new Foo()->m()` without parentheses, lazy objects, `array_find`/`array_any`/`array_all`, `mb_trim`, implicit nullable parameters (`Foo $x = null`) deprecated | php >=8.4 |
| Pipe operator `\|>`, `#[\NoDiscard]` | php >=8.5 |

## Output Gates

Before delivering PHP code, check:

- `declare(strict_types=1);` present, and every parameter, property, and return typed as narrowly as the value allows
- No `==`, `!=`, or `switch` on values whose types are not both proven; `in_array` and `array_search` carry `true` as the strict flag
- Every SQL value bound, every identifier allowlisted, `EMULATE_PREPARES` off
- Every value reaching HTML, an attribute, JavaScript, a URL, or a shell escaped with that context's function, at the point of output
- Nothing user-controlled reaches `unserialize`, `include`/`require`, `eval`, `extract`, a filesystem path, or a `header()` value without validation
- Every outbound call (HTTP, DB, subprocess, lock) has a timeout, and every `false`-returning call has its return inspected
- Dates are `DateTimeImmutable` with an explicit IANA timezone; human-facing text handled with `mb_*`
- `json_encode`/`json_decode` carry `JSON_THROW_ON_ERROR`
- Syntax and functions stay within `min_php`; layout matches `style`; new behavior arrives with a test that was seen failing first

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/php/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| min_php | 7.4 \| 8.0 \| 8.1 \| 8.2 \| 8.3 \| 8.4 \| 8.5 | 8.2 | Gates which Version Floors features may be emitted unguarded, and which fallback appears instead (`versions.md`) |
| sapi | fpm \| cli \| apache-mod \| swoole \| roadrunner | fpm | Assumptions about request lifetime, static state, timeouts, and where output goes (`fpm.md`, `cli.md`, `concurrency.md`) |
| framework | none \| laravel \| symfony \| wordpress \| slim | none | Whether to emit plain PHP or framework idiom, and when to hand off to a framework skill |
| strict_types | always \| new-files \| never | always | Whether emitted files open with `declare(strict_types=1)`, and how coercion is discussed (`types.md`) |
| style | per-cs \| psr-12 \| custom | per-cs | Layout of emitted code and the fixer ruleset produced (`static-analysis.md`) |
| static_analysis | none \| phpstan \| psalm | phpstan | Which checker's annotations, config file, and baseline commands appear (`static-analysis.md`) |
| analysis_level | number (0-9) | 6 | Strictness assumed when annotating, and whether a docblock is required alongside a native type (`static-analysis.md`) |
| test_framework | phpunit \| pest \| none | phpunit | Shape of emitted tests, assertions, and data providers (`testing.md`) |
| db_layer | pdo \| doctrine \| eloquent \| mysqli | pdo | Which data-access idiom every query example uses (`database.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: fixer (PHP-CS-Fixer vs PHP_CodeSniffer), Rector adoption, Xdebug vs pcov for coverage, profiler of choice, local runtime (Docker, Homebrew, Valet, WSL) — affects every emitted config block and command
- **Conventions**: namespace and directory layout, DTO style (arrays vs readonly classes vs enums), exception hierarchy, naming, docblock policy — affects generated code and review comments
- **Platform**: deployment target (FPM behind nginx, shared hosting, container, serverless, long-running runtime), OS, extension availability (`ext-intl`, `ext-mbstring`, `ext-pcntl`), private Packagist — affects `composer.md`, `php-ini.md`, `fpm.md`
- **Safety posture**: how aggressively to flag `unserialize`, dynamic `include`, `extract`, `@`, missing timeouts, unpinned dependencies, and emulated prepares — affects `security.md` and review depth
- **Dependencies**: banned or mandated packages (Guzzle vs Symfony HttpClient, Carbon vs native `DateTimeImmutable`), tolerance for new transitive dependencies, stdlib-only constraints — affects every recommendation
- **Output format**: whole file vs minimal diff, how much explanation, whether tests and a changelog entry accompany every change — affects the shape of the answer, never the correctness rules
- **Work order**: which gates run before a change is proposed rather than after — analyzer and suite green first, a plan approved before editing, a profile before any optimization — affects the sequence of every task, never the correctness rules

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `if (!strpos($s, $x))` | Returns `0` for a match at position 0 — the correct answer reads as failure | `strpos($s, $x) !== false`, or `str_contains()` on `php >=8.0` (`strings.md`) |
| `==` to compare a password hash or token | `"0e12" == "0e34"` is `true`; both are numeric strings equal to zero | `hash_equals()`, or `password_verify()` for passwords (`security.md`) |
| `array_filter()` then `json_encode()` | Keys survive, so the gap turns the array into a JSON object and the client's `.map()` fails | `array_values()` after every filter that feeds JSON (`arrays.md`, `json.md`) |
| `json_decode($s)` with no flags | Returns `null` for the input `"null"` AND for a parse error — indistinguishable | Always `JSON_THROW_ON_ERROR` (`json.md`) |
| `$_POST` for a JSON request body | Populated only for form-encoded and multipart bodies | `json_decode(file_get_contents('php://input'), ...)` (`http.md`) |
| Trusting `$_FILES['f']['type']` | The MIME type is supplied by the client and is trivially forged | `finfo_file()` on the temp file plus an extension allowlist (`security.md`) |
| `session_start()` at the top and never closing | The session lock is held for the whole request, so one user's parallel requests execute one at a time | `session_write_close()` as soon as the last write is done (`sessions.md`) |
| `DateTime::createFromFormat('Y-m-d', $d)` | Unspecified fields default to NOW, so the date carries the current time and can roll the day | Prefix the format with `!` to zero them, then check `getLastErrors()` (`datetime.md`) |
| `@` to silence a warning | Hides the diagnosis and leaves the broken value in flight; on `php >=8.0` it no longer even silences fatals | Handle the failure, or narrow `error_reporting` deliberately (`errors.md`) |
| `mt_rand`/`uniqid()` for a token or password reset | Predictable: `uniqid()` is a formatted timestamp, `mt_rand` is a seeded PRNG | `random_bytes()`/`random_int()` (`security.md`) |
| `PDO::ATTR_PERSISTENT` without cleanup | A worker inherits an open transaction, session variables, or temporary tables from the previous request | Non-persistent connections, or an explicit rollback on checkout (`database.md`) |
| A closing `?>` at the end of a PHP file | One trailing newline becomes output, and every later `header()` fails with "headers already sent" | Omit the closing tag in pure-PHP files (`http.md`) |
| `readfile()` for a large download | Fills the output buffer with the whole file before sending | `fpassthru` with buffers flushed, or `X-Accel-Redirect`/`X-Sendfile` (`http.md`) |
| `opcache.validate_timestamps=0` with a deploy that only swaps files | Workers keep executing the previous release's bytecode | Reload FPM (`kill -USR2`) as the last deploy step (`performance.md`, `fpm.md`) |
| `SELECT` then `INSERT` to avoid duplicates | Two workers pass the check in the same millisecond | Unique index plus catching the duplicate-key error (`concurrency.md`) |

## Where Experts Disagree

- **Arrays vs objects for structured data.** The array-shape school keeps everything a `list<array{id:int,…}>` and lets the analyzer verify it: no boilerplate, refactors are grep-based. The value-object school makes each shape a readonly class: constructor validation, no key typos, IDE completion. Boundary: data crossing a module or process boundary earns a class; a shape used in three lines of one function does not (`static-analysis.md`).
- **Active record vs data mapper.** Eloquent-style records are faster to write and let any layer reach the database; Doctrine-style mappers keep the domain persistence-free and make the unit of work explicit. Boundary: how long the codebase must outlive its storage decisions — not how large it is (`database.md`).
- **How strict to run the analyzer.** One camp treats anything below `max` as unfinished; the other stops where the false-positive rate exceeds the bug-catch rate. Boundary: a greenfield typed domain reaches high levels cheaply; a decade-old codebase baselines and ratchets, and measures success as baseline shrinkage rather than level number (`static-analysis.md`).
- **Long-running runtimes.** Swoole, RoadRunner, and FrankenPHP remove per-request bootstrap and can cut latency materially; they also delete PHP's strongest safety property, that every request starts from a clean process. Boundary: adopt when bootstrap is a measured share of p95 AND the team accepts hunting state leaks — never as a default (`concurrency.md`).
- **Framework or none.** A framework supplies routing, DI, migrations, and a hiring pool; plain PHP with a few PSR packages supplies a dependency tree you can read end to end. Boundary: the number of cross-cutting concerns you would otherwise hand-write — auth, queues, and migrations together is the tipping point.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/php (install if the user confirms):
- `laravel` — Eloquent, queues, Blade, and Laravel-specific auth
- `mysql` — schema design, indexes, and query plans behind PDO
- `nginx` — the server in front of PHP-FPM: buffering, timeouts, static files
- `regex` — PCRE pattern design; this skill's `strings.md` covers only the PHP bindings
- `debugging` — language-agnostic fault isolation; the PHP-specific version is this skill's `debugging.md`

## Feedback

- If useful, star it: https://clawic.com/skills/php
- Latest version: https://clawic.com/skills/php

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/php.
