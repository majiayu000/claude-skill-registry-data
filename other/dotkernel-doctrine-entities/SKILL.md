---
name: dotkernel-doctrine-entities
description: >
  Use when adding or changing anything persisted in a Dotkernel project — a Doctrine
  entity, column, relation, index, repository, backed enum with its DBAL type, fixture, or
  migration. Also use for questions about UUID versus numeric identifiers, timestamps, the
  table prefix, why doctrine-migrations diff produces an unexpected diff, or why a
  schema-validation CI job is failing.
---

# Entities, repositories and migrations

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
             - Dotkernel Frontend
  Packages:  - none
```

In the stock API and Admin, everything here lives in the `Core` layer —
`src/Core/src/<Module>/src/` — and migrations in `src/Core/src/App/src/Migration/` (see
`dotkernel-core-submodule`). The stock Frontend also uses Doctrine but keeps entities in its own
modules and migrations in `data/doctrine/migrations/`; there, match its layout rather than this
skill's paths.

## Entity anatomy

```php
#[ORM\Entity(repositoryClass: BookRepository::class)]
#[ORM\Table(name: 'book')]
#[ORM\HasLifecycleCallbacks]
class Book extends AbstractEntity
{
    use TimestampsTrait;
    use UuidIdentifierTrait;

    #[ORM\Column(name: 'title', type: 'string', length: 191)]
    protected string $title;

    #[ORM\Column(
        type: 'book_status_enum',
        enumType: BookStatusEnum::class,
        options: ['default' => BookStatusEnum::Draft]
    )]
    protected BookStatusEnum $status = BookStatusEnum::Draft;

    /** @var Collection<int, Review> */
    #[ORM\OneToMany(targetEntity: Review::class, mappedBy: 'book', cascade: ['persist', 'remove'])]
    protected Collection $reviews;
}
```

Rules:

- Extend the `Core` abstract entity — it implements `ArraySerializableInterface`, which the
  hydrators and serialisers rely on.
- UUID identifier trait for anything exposed in a URL; the numeric trait only for internal
  join and lookup tables. Public identifiers are UUIDs, never auto-increment ids.
- Timestamps trait plus `#[ORM\HasLifecycleCallbacks]` for created/updated.
- Password trait for anything with a password — it hashes for you. Never hash by hand.
- Initialise every `Collection` property in the constructor with `new ArrayCollection()`, and
  call `parent::__construct()`.
- `length: 191` is the house default for indexed strings (utf8mb4-safe). Keep the matching
  `StringLength` validator in sync.
- Reserved words need backticks in the table name.
- Annotate collections (`@var Collection<int, X>`) or phpstan will fail.
- Fluent setters returning `self`, matching the rest of the codebase.

## Backed enums need three pieces

A column backed by an enum requires:

1. `Core\<Module>\Enum\BookStatusEnum` — a string-backed enum.
2. `Core\<Module>\DBAL\Types\BookStatusEnumType`, extending the `Core` abstract enum type and
   implementing `getEnumClass()` and `getName()`. The name is the string used in the column's
   `type:`.
3. Registration under `doctrine.types` in the module `ConfigProvider`.

The abstract enum type emits the right SQL per platform — a native enum on MySQL/MariaDB and
PostgreSQL, `TEXT` on SQLite. That last one is why in-memory functional tests work; a
hand-rolled type that ignores SQLite will pass locally and fail in CI.

## Repositories

Extend the `Core` abstract repository. Query builders live here; business rules do not. Return
`QueryBuilder` from list methods so the caller can paginate.

Pagination parameters are normalised by the shared paginator helper, and the sort column
**must be whitelisted** in the service before it reaches the query builder.

## Migrations

```bash
php ./vendor/bin/doctrine-migrations diff      # generate — ASK FIRST, it reads the live DB
php ./vendor/bin/doctrine-migrations migrate   # apply    — the user runs it; see below
php ./vendor/bin/doctrine-migrations status
```

`diff` and `status` prompt for approval. `migrate` and `execute` are refused outright by the
`guard-bash.sh` hook, approval or not — never try to run them. Give the user the exact command to
run and say what it will change.

- Generated into the configured migrations path — **never hand-edit**. A wrong diff means the
  entity is wrong; fix that and regenerate.
- Review the generated SQL before applying. `diff` will happily propose dropping a column.
- One logical schema change per migration.
- Where a table prefix is supported, it is applied by an event listener — never hardcode
  prefixes into table names.
- **The same migration must be applied by every project sharing that database.**
- A schema-validation CI job will fail when entities and migrations drift. If it is red, a
  migration is missing — do not edit the entity to match an old migration.

## Fixtures

Seed data via the data-fixtures package. Order matters: roles before the records referencing
them.

```bash
php ./bin/doctrine fixtures:list
php ./bin/doctrine fixtures:execute                      # the user runs it
php ./bin/doctrine fixtures:execute --class=BookLoader   # the user runs it
```

`fixtures:list` prompts for approval. `fixtures:execute` writes to the database and is refused
outright by the `guard-bash.sh` hook — give the user the command to run instead.

Functional tests typically build a fresh schema and load every fixture per test, so a new
fixture immediately affects all of them. Keep fixtures small and deterministic.

## Checklist

- [ ] Entity + Repository in `Core`.
- [ ] Enum + DBAL type + `doctrine.types` registration for every enum column.
- [ ] Collections initialised and annotated.
- [ ] Column lengths mirrored in the validators.
- [ ] Migration generated (not written), reviewed, applied.
- [ ] Fixture added if the table needs seed data.
- [ ] Every other project on this database accounted for.
- [ ] Static analysis clean — the Doctrine phpstan extension is strict.
