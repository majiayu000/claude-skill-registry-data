---
name: php-expert
description: Production PHP 8.3+ house rules for naming, style, typed constants, Override attributes, PHP 8.4 gotchas, strict types, Composer constraints, exceptions, PHPUnit, and anti-patterns. Use when writing or reviewing PHP code.
---

# PHP Expert

Opinion and house-rule reference for PHP 8.3+. **Assumes baseline PHP 8.0–8.2 knowledge** (constructor promotion, readonly, enums, match, nullsafe, named args, first-class callables, arrow functions, `#[\SensitiveParameter]`) — this file only covers what's house-specific, what's load-bearing, or what shifts year-to-year.

Non-negotiable defaults:
- **PHP 8.3 minimum, 8.4 preferred.** Check `composer.json` before using an 8.4-only feature.
- Every new class: `final` + `private readonly` promoted properties unless there's a reason otherwise.
- Typed class constants with the `public const string FOO = '...';` form — always the type keyword.
- `#[\Override]` on every overriding method. No exceptions.
- `match` always, `switch` never. `$this->method(...)` always, `[$this, 'method']` never.
- Singular namespace nouns, no doubled-up filenames, no abbreviations in names, camelCase acronyms in method names.
- Imports: alphabetical, one per statement, grouped `const` / `class` / `function`.
- `assertSame` always, `assertEquals` never.

---

## 1. Version landscape (April 2026)

| Version | Status | Use for |
|---|---|---|
| **8.5** (Nov 2025) | Active | Experimental / greenfield only |
| **8.4** (Nov 2024) | **Active** | Greenfield — target this |
| **8.3** (Nov 2023) | Security-only | Current practical floor |
| **8.2** (Dec 2022) | Security-only | Legacy only |
| 8.1 and below | **EOL** | Never |

Before reaching for an 8.4-only feature (property hooks, asymmetric visibility, `#[\Deprecated]`, `new Foo()->bar()` without parens, `array_find`/`array_any`/`array_all`, lazy objects), verify the target repo's `composer.json` `require.php` field.

---

## 2. Load-bearing language rules

### 2.1 Typed class constants — always with the type keyword

```php
class Exception extends \Exception
{
    public const string GENERAL_UNKNOWN = 'general_unknown';
    public const string USER_NOT_FOUND  = 'user_not_found';
    public const int    MAX_RETRIES     = 3;
}
```

The `string` / `int` / `array` keyword is what makes it a *typed* constant (PHP 8.3+) — without it, overriding subclasses can change the type. Easy to forget. Pint will not add it for you.

### 2.2 `#[\Override]` on every override

```php
use Override;

final class Autoscale extends Base
{
    #[Override]
    protected function getName(): string
    {
        return 'autoscale';
    }
}
```

Apply it to every method that overrides a parent — including `__construct`, `__toString`, and interface implementations. When touching a file that doesn't use it yet, add it alongside your changes.

### 2.3 Class defaults — `final` + `private readonly` promoted

```php
final class Autoscale
{
    public function __construct(
        private readonly KubernetesCluster $kubernetes,
        private readonly Concurrency $concurrency,
        private readonly array $projects,
        private readonly int $percentage,
    ) {
    }
}
```

Rules:
- **Every class is `final` unless it's explicitly designed for inheritance.** Opt into extensibility, don't opt out.
- **Every property is promoted and `private readonly`** unless a subclass needs it (`protected readonly`) or it's part of the public contract (`public readonly`).
- Multi-line constructors with trailing commas. One property per line. Empty `{ }` on its own line.
- **For value objects / DTOs, use `readonly class`** instead of per-property `readonly` — one word covers every field.

### 2.4 Enum house idiom

```php
enum DatabaseType: string
{
    case Shared    = 'shared';
    case Dedicated = 'dedicated';

    /** @return list<string> */
    public static function values(): array
    {
        return array_map(fn (self $case) => $case->value, self::cases());
    }

    public function isShared(): bool
    {
        return $this === self::Shared;
    }

    public function getDescription(): string
    {
        return match ($this) {
            self::Shared    => 'Serverless database (scales to zero when idle)',
            self::Dedicated => 'Dedicated database (always running)',
        };
    }
}
```

The three idioms to copy:
- `static function values(): array` returning `list<string>` — for validators and form options.
- `public function is<State>(): bool` — one per case.
- `getDescription()` / `getLabel()` / `getPort()` using `match ($this)` with **no `default:`** — an added case becomes a compile-time error via `UnhandledMatchError` instead of a silent fall-through.

Centralize the behavior on the enum itself — don't leave it bare and write an inline `match ($type) { ... }` at every call site.

### 2.5 PHP 8.4 — the parts that trip me up

**Property hooks** — useful but boxed in:

```php
class User
{
    public string $fullName {
        get => trim("{$this->firstName} {$this->lastName}");
    }

    public string $email {
        set(string $value) {
            if (! filter_var($value, FILTER_VALIDATE_EMAIL)) {
                throw new \InvalidArgumentException('Invalid email');
            }
            $this->email = strtolower($value);
        }
    }

    public function __construct(public string $firstName, public string $lastName) {}
}
```

Limitations I forget:
- **Cannot combine with `readonly`.**
- No `unset()` on hooked properties.
- `set`-hooked properties cannot be assigned by reference (`$r = &$o->name`) or indirectly mutated (`$o->arr[] = ...`).
- Virtual properties (hooks that don't touch `$this->name`) have no backing storage and no default value.

Use for: validation, normalization, derived fields. Avoid for: multi-statement logic (use methods).

**Asymmetric visibility** — replaces "public getter + private setter":

```php
final class Session
{
    public function __construct(
        public private(set) string $token,
        public private(set) int $expiresAt,
    ) {
    }

    public function refresh(string $token, int $expiresAt): void
    {
        $this->token     = $token;
        $this->expiresAt = $expiresAt;
    }
}
```

Set-visibility must be `≤` get-visibility. `private(set)` alone is shorthand for `public private(set)`.

**`new Foo()->method()`** — drop the outer parens:

```php
$slug = new Slugger()->slug($title);   // 8.4+
$slug = (new Slugger())->slug($title); // pre-8.4
```

Constructor parens are still required even for zero-arg constructors.

**`#[\Deprecated]`** — native replacement for `@deprecated` PHPDoc:

```php
#[\Deprecated(message: 'Use createFromRequest() instead', since: '2.0')]
public function legacyCreate(array $input): self { /* ... */ }
```

Emits `E_USER_DEPRECATED` at call time; static analyzers pick it up.

**New array functions** — prefer over `foreach` + break:

```php
$admin = array_find($users,     fn (User $u) => $u->role === 'admin');  // first match or null
$key   = array_find_key($users, fn (User $u) => $u->role === 'admin');  // first key or null
$has   = array_any($errors,     fn (Error $e) => $e->isFatal());        // bool (any)
$ok    = array_all($validators, fn (Validator $v) => $v->isValid($x));  // bool (every)
```

**Implicit nullable parameters are deprecated.** `function f(string $x = null)` must become `function f(?string $x = null)`. Rector will fix a whole repo in one pass.

### 2.6 `declare(strict_types=1)` — match the repo

If the repo uses it, put it at the top of every new file. If the repo doesn't use it, don't sprinkle it in — the change shows up in every diff forever. For greenfield repos, turn it on everywhere from day one.

```php
<?php

declare(strict_types=1);

namespace Acme\Database\Exception;
```

---

## 3. Naming and style

### 3.1 Naming rules (house)

- **Single-word names when context makes meaning obvious.** `connections` not `backendConnections`; `pools` not `backendPools`; `timeout` not `connectTimeout` (when it's the only timeout).
- **No abbreviations in general names.** `certificate` not `cert`, `connection` not `conn`, `request` not `req`, `message` not `msg`, `database` not `db` (outside variable names like `$dbHandle`), `authorization` not `auth` (in class names).
- **Well-known acronyms are fine** — `TLS`, `HTTP`, `TCP`, `CA`, `JWT`, `SDK`, `DNS`, `MFA`, `MTLS`.
- **Acronyms in method names are camelCase, not UPPER.** `updateMfa()` not `updateMFA()`. Upper-case runs break SDK generation into `create_m_f_a` instead of `create_mfa`.
- **In constants / config keys**, acronyms are fully uppercase — `APP_AUTH_TYPE_JWT`, `cacheTTL`, `parseURL`.
- **No doubled-up namespace in filenames.** `Engine/Driver.php` not `Engine/EngineDriver.php` — namespace already provides context. Concrete implementations go in nested subdirectories: `Engine/Driver/{Postgres,MySQL,Mongo}.php`.
- **Singular nouns for namespaces.** `Adapter` not `Adapters`, `Validator` not `Validators`, `Worker` not `Workers`. A namespace is a folder; plurality is implied.
- **REST endpoints**: plural nouns (`/collections`, not `/collection`), kebab-case for multi-word paths (`/acme-challenge`, not `/acmeChallenge`).

### 3.2 Imports

- Alphabetical.
- One per statement. **Never** combined imports (`use Foo\{A, B};`).
- Grouped `const` / `class` / `function`, in that order. Pint rule:

```json
"ordered_imports": {
    "sort_algorithm": "alpha",
    "imports_order": ["const", "class", "function"]
}
```

Use `as` to disambiguate clashing names (`Acme\Exception as AcmeException`) — don't work around with fully-qualified names in the body.

### 3.3 Strings

Single quotes by default. Double quotes only when the string contains a single quote, or when interpolation beats concatenation (`"Deleted pod: {$pod->getName()}"`). Heredoc/nowdoc for long multiline SQL/JSON — prefer nowdoc (`<<<'SQL'`) when no interpolation is needed.

### 3.4 Comments

- **Never** use section-header comments like `// ---------------- HANDLERS ----------------` or `// === Section ===`. If you see them, delete them.
- PHPDoc only for non-trivial generic or shape information (`@param array<string, mixed>`, `@return list<Document>`, `@throws`). Do NOT add PHPDoc that just repeats the type signature.
- Inline `//` only when intent can't be inferred from the code (external-bug workaround, deliberately empty block, subtle invariant). Do not narrate what the code already says.
- `/** @phpstan-ignore ... */` inline when silencing PHPStan — always add a reason.

### 3.5 Domain-driven organization

No `helpers/`. No `utils/`. No `common.php` of global functions. Group by **domain**:

```
src/Acme/
├── Auth/          # passwords, OAuth, sessions
├── Event/         # event publishers
├── Exception/     # custom exception hierarchy
├── Http/          # HTTP glue
├── Messaging/     # SMS, email, push
├── Payment/       # billing, invoicing
└── Storage/       # file upload, blob storage
```

One class per file; filename matches symbol name. A `MetricsCollector` lives in `src/Acme/Metric/`, not `src/Acme/Util/MetricsCollector.php`.

### 3.6 Sparse updates

When updating a record, pass only the **changed attributes**, never the whole object. Full-object updates cause unnecessary conflict writes in high-concurrency paths and break audit diffing.

### 3.7 Fix nearby violations

When you edit a file that contains older style (dynamic callables, `switch` statements, untyped params, plural namespaces, section-header comments), **fix them in the same commit** if the scope is reasonable. Don't leave inconsistent patterns in files you just touched.

---

## 4. Project structure

| Directory | Contents | Autoloaded? |
|---|---|---|
| `src/` | PSR-4 production code. No side effects on file load — class definitions only. | Yes (`autoload`) |
| `app/` | Bootstrap code with side effects — route/container/listener wiring. Loaded by entry scripts. | No — explicit `require` |
| `bin/` | Executable CLI scripts. Each file is a tiny entry that hands off to a `src/` class. | No |
| `tests/unit/` | Pure unit tests — no IO, no subprocess. | Yes (`autoload-dev` as `Tests\Unit\`) |
| `tests/e2e/` | Integration tests — real DB, real HTTP, real queues. | Yes (`autoload-dev` as `Tests\E2E\`) |
| `tests/resources/` | Fixtures. Never PSR-4. Exclude from PHPStan scan. | No |

**Library** (`"type": "library"`) — only `src/`, `tests/`, tooling config. **Project** (`"type": "project"`) — add `app/`, `bin/`, Docker, CI.

Test-only classes go in `autoload-dev`, not `autoload` — `composer install --no-dev` strips them entirely:

```json
"autoload": {
    "psr-4": {"Acme\\": "src/Acme"}
},
"autoload-dev": {
    "psr-4": {
        "Tests\\Unit\\": "tests/unit",
        "Tests\\E2E\\":  "tests/e2e"
    }
}
```

---

## 5. Composer

### 5.1 Constraint style — `^` carets

| Style | Meaning | When |
|---|---|---|
| `^1.2` | `>=1.2, <2.0` | Default for every dependency |
| `^0.33` | `>=0.33, <0.34` | Pre-1.0 packages — the caret already locks the minor |
| `dev-branchname` | VCS branch | For forks, paired with a `repositories` entry |

**Never `~` or `*` wildcards.** `"utopia-php/framework": "^0.33"`, not `"0.33.*"` or `"~0.33.0"`.

### 5.2 VCS repositories for forks

Never shim a dependency locally. If you need a fork or branch, add a VCS repo:

```json
"repositories": [
    {"type": "vcs", "url": "https://github.com/acme/php-k8s"}
],
"require": {
    "acme/php-k8s": "dev-main"
}
```

**Never** write a patch file or copy a package into `vendor-patches/`. Fix upstream, commit, push, then `composer update <package>` in the consumer.

### 5.3 Standard script names

```json
"scripts": {
    "test":    "vendor/bin/phpunit",
    "lint":    "vendor/bin/pint --test",
    "format":  "vendor/bin/pint",
    "check":   "./vendor/bin/phpstan analyse -c phpstan.neon --memory-limit=2G",
    "analyze": "./vendor/bin/phpstan analyse -c phpstan.neon --memory-limit=2G",
    "refactor":"vendor/bin/rector process",
    "fix":     ["@refactor", "@analyze", "@format"]
}
```

Run `composer format` before every commit. Run `composer check` (or `analyze`) before every PR.

### 5.4 `config.platform` + deploy flags

Pin the target PHP version so local installs resolve like production:

```json
"config": {
    "platform": {"php": "8.3"},
    "allow-plugins": {"php-http/discovery": false}
}
```

Deploy invocation (never `composer update`):

```bash
composer install --no-dev --prefer-dist --no-interaction --no-progress --optimize-autoloader
```

Composer 2 generates `vendor/composer/platform_check.php` by default — keep it on, run `composer check-platform-reqs` in CI.

---

## 6. Pint + PHPStan + Rector

### 6.1 Pint (`pint.json`) — house preset

```json
{
    "preset": "psr12",
    "exclude": [
        "./tests/resources"
    ],
    "rules": {
        "array_indentation": true,
        "single_import_per_statement": true,
        "simplified_null_return": true,
        "ordered_imports": {
            "sort_algorithm": "alpha",
            "imports_order": ["const", "class", "function"]
        }
    }
}
```

Preset is always `psr12` unless the project is a framework-specific one (then `laravel` / `symfony`).

### 6.2 PHPStan — target `level: max`

Greenfield code starts at **`level: max`**. Retrofitting to higher levels later is painful — start strict, keep it strict. PHPStan 2.x has 11 levels (0–10); `max` is level 10, which treats all `mixed` strictly.

```neon
includes:
    - phpstan-baseline.neon

parameters:
    level: max
    paths:
        - src
        - tests
    tmpDir: .phpstan-cache
    excludePaths:
        - tests/resources
```

Existing codebases that can't reach max yet can sit at a lower level **as long as there's a written plan to raise it**. Never lower the level to silence an error. Add to `phpstan-baseline.neon` with a dated `# TODO(2026-09): revisit` instead, and shrink the baseline over time.

Useful extensions: `phpstan/phpstan-strict-rules`, `phpstan/phpstan-deprecation-rules`, `phpstan/phpstan-phpunit`.

### 6.3 Rector (`rector.php`)

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\SetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/src', __DIR__ . '/tests'])
    ->withPhpSets(php84: true)
    ->withSets([
        SetList::DEAD_CODE,
        SetList::CODE_QUALITY,
        SetList::TYPE_DECLARATION,
        SetList::PRIVATIZATION,
    ])
    ->withPhpunitSets(phpunit120: true);
```

Adopt in greenfield. Rector handles: implicit nullable → explicit, docblock types → native types, PHPUnit annotations → attributes, `switch` → `match`, `[$this, 'method']` → `$this->method(...)`, constructor promotion migration, PHP version upgrades.

---

## 7. Typed exceptions (the house pattern)

### 7.1 Typed string error codes

Every service has one Exception class with **typed class constants** for each error type:

```php
namespace Acme\Extend;

class Exception extends \Exception
{
    public const string GENERAL_UNKNOWN          = 'general_unknown';
    public const string GENERAL_ACCESS_FORBIDDEN = 'general_access_forbidden';
    public const string GENERAL_RATE_LIMITED     = 'general_rate_limited';
    public const string USER_NOT_FOUND           = 'user_not_found';
    public const string USER_EMAIL_EXISTS        = 'user_email_already_exists';
    public const string USER_BLOCKED             = 'user_blocked';

    public function __construct(
        string $type = self::GENERAL_UNKNOWN,
        ?string $message = null,
        int|string|null $code = null,
        ?\Throwable $previous = null,
    ) {
        parent::__construct($message ?? $type, (int) ($code ?? 0), $previous);
    }
}
```

Naming: `ENTITY_ERRORTYPE` in SCREAMING_SNAKE for the constant, `entity_errortype` in snake_case for the value. The value is a stable string used by SDKs, error pages, and translations — **never rename it** once published.

Throwing:

```php
if ($email === '') {
    throw new AcmeException(AcmeException::USER_EMAIL_INVALID);
}

throw new AcmeException(
    AcmeException::USER_COUNT_EXCEEDED,
    "User count exceeded: {$total}/{$limit}",
);
```

**Never** throw the base `\Exception` or `\RuntimeException` in new code. Throw a domain exception with a typed code so the global error handler can map it to an HTTP status + user-facing message.

### 7.2 Custom exceptions with public readonly context

Specialized exceptions carry structured context as **public readonly properties** — far better than stashing data in `getMessage()` with `sprintf`:

```php
declare(strict_types=1);

namespace Acme\Database\Exception;

use RuntimeException;
use Throwable;

final class Provisioning extends RuntimeException
{
    public function __construct(
        public readonly string $databaseId,
        public readonly string $step,
        string $message,
        ?Throwable $previous = null,
    ) {
        parent::__construct($message, 0, $previous);
    }
}
```

Caller reads context fields directly:

```php
try {
    $this->provision($id);
} catch (Provisioning $e) {
    $log->error("Step {$e->step} failed for database {$e->databaseId}: {$e->getMessage()}");
    throw $e;
}
```

### 7.3 Typed exception hierarchy

Expose a tree so callers can `catch` at any level of specificity:

```
Acme\Database\Exception (base)
├── Exception\Authorization
├── Exception\Conflict
├── Exception\Duplicate
├── Exception\Limit
├── Exception\Structure
├── Exception\Timeout
└── Exception\Transaction
```

Callers write `catch (Conflict $e)` for a narrow case, `catch (DatabaseException $e)` for a broad fallback.

### 7.4 `finally` for cleanup, not log-and-rethrow

```php
// Right
$handle = $this->open();
try {
    return $this->process($handle);
} finally {
    $handle->close();
}

// Wrong — adds noise, loses stack
try {
    return $this->process($handle);
} catch (\Throwable $e) {
    $log->error($e->getMessage());
    throw $e;
}
```

Only catch exceptions you can actually handle. Leave logging to a top-level error handler. Cleanup goes in `finally`.

---

## 8. Array idioms worth the rule

Most array idioms are elementary. These two are the foot-guns worth naming:

### 8.1 `array_push($arr, ...$new)` in loops, not `array_merge`

`array_merge` copies the entire left array on every call — O(n²) in a loop.

```php
// Right
foreach ($batches as $batch) {
    array_push($results, ...$fetch($batch));
}

// Wrong — quadratic
foreach ($batches as $batch) {
    $results = array_merge($results, $fetch($batch));
}
```

### 8.2 PHPStan shape annotations on `array` returns

`array` is a useless return type — PHPStan/Psalm can't help you. Annotate shape:

```php
/** @return list<User> */
public function allActive(): array { /* ... */ }

/** @return array<string, int> */
public function countByEmail(): array { /* ... */ }

/** @return array{name: string, age: int, tags: list<string>} */
public function getProfile(): array { /* ... */ }
```

At `level: max` PHPStan enforces these. Prefer a typed collection class over `list<>` when the collection has behavior (methods, iteration).

---

## 9. Testing — PHPUnit 12

### 9.1 Attribute migration reminder

PHPUnit 12 **removed** docblock annotations. Attributes to know:

- `#[Test]` — mark a method as a test (lets you drop the `test` prefix).
- `#[TestDox('human readable')]` — override the reported name.
- `#[DataProvider('methodName')]` / `#[DataProviderExternal(Class::class, 'method')]` — parameterised tests.
- `#[CoversClass(Foo::class)]` — coverage target (replaces `@covers`).
- `#[Group('slow')]` — tag for `--group slow` / `--exclude-group slow`.
- `#[Before]`, `#[After]`, `#[BeforeClass]`, `#[AfterClass]` — lifecycle.
- `#[RequiresPhp('>=8.4')]`, `#[RequiresPhpExtension('gd')]` — skip tests.

Migration tool: Rector's `AnnotationsToAttributesRector`.

### 9.2 `assertSame` always

`assertSame` = strict `===` (checks type and value). `assertEquals` = loose `==` (tolerates `'1' == 1`, object field shuffles). **Default to `assertSame` in new tests.** Reach for `assertEquals` only when you genuinely want loose semantics (rare — use `assertEqualsWithDelta` for floats, assert on `$date->format('c')` for dates).

### 9.3 Test organisation — unit vs e2e is a hard line

- One test file per class under test. Filename = `<Class>Test.php`.
- Namespace = `Tests\Unit\` + the class's package suffix. Test for `Acme\Auth\Hash` → `Tests\Unit\Auth\HashTest`.
- `final class FooTest extends TestCase` — tests are `final`; no test inheritance chains.
- **Integration tests go in `tests/e2e/`, not `tests/unit/`.** Keep unit tests pure — no IO, no subprocess, no network. If it touches a real DB, HTTP server, or queue, it's not a unit test.

### 9.4 Never mock the database

Hit a real database — SQLite in memory, a dedicated test DB, or a testcontainer. Mocked database tests pass while real migrations/schemas fail, which is a guaranteed future bug.

Never mock your own code under test — you're only testing the mock.

### 9.5 Mandatory regression test for bug fixes

**Every bug fix must include a regression test that fails without the fix and passes with it. No exceptions.**

There are no "pre-existing issues". If tests fail, fix them regardless of when the issue was introduced.

### 9.6 Use paratest

Anything beyond ~100 tests should run through `brianium/paratest`, not raw phpunit:

```bash
vendor/bin/paratest --configuration phpunit.xml --functional --processes 4
```

Drop-in compatible with PHPUnit. CI should always use paratest.

---

## 10. Wrong defaults — refuse on sight

**Every entry in this section is a pattern that comes from training data.** The left column is what I'll write if I'm not actively applying the rules in §2–§9. The right column is the correct pattern. Scan this section before committing any PHP; every row is a likely diff in a review.

### 10.1 Language

| About to write | Write instead | Why |
|---|---|---|
| `public const FOO = 'foo';` | `public const string FOO = 'foo';` | Typed class constant (8.3+). Pint won't add the type keyword for you. |
| Overriding method with no attribute | `#[\Override]` on the method | Catches rename/refactor typos at class load. |
| `class Foo { private Database $db; public function __construct(Database $db) { $this->db = $db; } }` | `final class Foo { public function __construct(private readonly Database $db) {} }` | House default: `final` + constructor-promoted `private readonly`. |
| Bare enum + inline `match ($type) { ... }` at every call site | Methods on the enum (`values()`, `is<State>()`, `getDescription()` using `match ($this)`) | Centralize behavior on the enum. |
| `switch ($x) { case 'a': ...; break; }` | `match ($x) { 'a' => ..., }` | Strict `===`, no fall-through, expression-valued, exhaustive. |
| `[$this, 'method']` / `Closure::fromCallable('foo')` | `$this->method(...)` / `foo(...)` | First-class callable syntax (8.1+). |
| `function f(string $x = null)` | `function f(?string $x = null)` | Implicit nullable deprecated in 8.4. |
| `function f($x, $y) { ... }` (untyped) | Full type hints on every param and return | `mixed` only when genuinely unbounded. |
| `json_decode($body)` → `stdClass` DTO | Typed `readonly class` hydrated from an array | No `stdClass` in the domain layer. |
| `throw new \RuntimeException("User {$id} not found")` | `throw new AcmeException(AcmeException::USER_NOT_FOUND)` with a `public const string` code | Typed domain exception with stable error code. |
| Exception message built via `sprintf(...)` with context | `public readonly` context fields on the exception, read directly at the catch site | Caller reads `$e->databaseId` instead of parsing strings. |
| `try { ... } catch (\Throwable $e) { $log->error(...); throw $e; }` | `try { ... } finally { $cleanup(); }` — let the exception propagate | Logging belongs at the top-level handler. |
| `global $db;` / static `Container::get('db')` | Inject through the constructor | No service locators. |
| Magic strings for a closed set | Enum (backed or pure) | No magic strings anywhere. |
| `die()` / `exit()` for control flow | `throw new DomainException(...)` | Only `exit` at program entry points. |
| `sprintf('Hello %s', $name)` | `"Hello {$name}"` | Interpolation beats `sprintf` for simple concat. |
| `strftime` / `gmstrftime` / `utf8_encode` / `utf8_decode` | `IntlDateFormatter` / `date()` / `mb_convert_encoding(..., 'UTF-8', 'ISO-8859-1')` | Deprecated or removed. |
| Docblock `@var` / `@param` / `@return` that duplicates a native type | Native type, drop the docblock | PHPDoc is for shape/generic info, not native types. |
| `Validators\`, `Adapters\`, `Workers\` namespace | `Validator\`, `Adapter\`, `Worker\` | Singular namespace nouns. |
| `Adapter/MySQLAdapter.php` | `Adapter/MySQL.php` | No doubled-up namespace in filenames. |
| `updateMFA()` / `parseHTML()` / `toJSON()` | `updateMfa()` / `parseHtml()` / `toJson()` | camelCase acronyms in methods — UPPER breaks SDK generation into `update_m_f_a`. |
| Hydrate full record, mutate, pass whole thing back to `update()` | Build a small array with only the dirty fields | Sparse updates only. |
| `array_merge($acc, $batch)` inside a loop | `array_push($acc, ...$batch)` | `array_merge` in a loop is O(n²). |
| `array` return type with no docblock | `array` return type + `@return list<X>` / `@return array<string, X>` / `@return array{...}` shape | PHPStan at `level: max` can't type-check otherwise. |

### 10.2 Testing

| About to write | Write instead | Why |
|---|---|---|
| `$this->assertEquals($a, $b)` | `$this->assertSame($a, $b)` | Strict `===` checks type and value. |
| `$mock = $this->createMock(Database::class)` for a "unit" test | Real database — SQLite in memory, testcontainer, or test DB | Mocked DB tests pass while real migrations fail. |
| Mocking the class under test itself | Don't — you're only testing the mock | You're not testing anything real. |
| Integration test inside `tests/unit/` | Move to `tests/e2e/` | Unit tests are pure — no IO, no network, no subprocess. |
| `/** @dataProvider cases */` | `#[DataProvider('cases')]` | Docblock annotations removed in PHPUnit 12. |
| `class FooTest extends TestCase` (not `final`) | `final class FooTest extends TestCase` | No test inheritance chains. |
| Shipping a bug fix PR without a new test | Add a regression test that fails without the fix and passes with it | Mandatory for every bug fix. |

### 10.3 Tooling & workflow

| About to do | Do instead | Why |
|---|---|---|
| `composer update` in production | `composer install --no-dev --prefer-dist --no-interaction --no-progress --optimize-autoloader` from a committed `composer.lock` | Lockfile is the contract. |
| Writing a `~` or `*` constraint (`"~0.33.0"`, `"0.33.*"`) | `"^0.33"` caret range | House rule: carets for every dependency. |
| Writing a patch file / `vendor-patches/` / copying a dep locally | Fix the dep upstream, commit, push, `composer update <package>` | No shims. |
| Committing without running `composer format` / `composer lint` | Format first, then commit | Pre-commit hook if possible. |
| Lowering PHPStan level to make an error disappear | Fix the error, or add a line to `phpstan-baseline.neon` with a dated `# TODO(2026-09): revisit` | Shrink the baseline over time; never grow it. |
| `git commit --no-verify` to skip hooks | Investigate why the hook fails; fix the underlying issue | Only skip if the user explicitly asks. |
| Leaving `// TODO: remove`, dead code, abandoned branches, commented-out iterations in the final commit | Clean up before stopping — the last commit of a finished change reads as if the iterations never happened | Finalize, don't accrete. |
| Leaving "we can migrate this later" comments | Finish the migration in the same commit | No loose ends. |
| Creating `helpers.php` / `utils.php` / `src/Util/` | Put the code in the domain that owns it | No helper files. |
