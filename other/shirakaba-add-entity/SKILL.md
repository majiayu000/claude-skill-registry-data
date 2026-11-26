---
name: shirakaba-add-entity
description: Add a database entity to a Shirakaba application - the readonly entity class with mapping attributes, relations, a generated migration, and checks that the schema matches. Use when asked to add a table, a model or a relation in a project that uses shirakaba/orm.
---

# Add an entity to a Shirakaba application

Read `vendor/shirakaba/docs/guide/06-database.md` (Entities, Migrations) and
`vendor/shirakaba/docs/design/08-database.md` first. Shirakaba entities are plain readonly objects: no lazy loading,
no unit of work, no `save()`.

1. **Look at what exists.** `app entities` and `app entities:show <a similar entity>` show
   tables, columns, relations and scopes.
2. **Entity class.** `#[Table('notes')]` on a `final readonly` class; properties map to
   columns (camelCase to snake_case unless `#[Column('name')]`). The key is
   `#[Id, Generated] public ?int $id = null` last; `#[CreatedAt]`, `#[UpdatedAt]`, `#[Version]`
   are managed columns. Use `DateTimeImmutable` and `LocalDate`, backed enums, value objects.
3. **Relations.** Declare them on the class: `#[BelongsTo('user', User::class, 'userId')]`,
   `#[HasMany(...)]`, `#[HasOne(...)]`, `#[ManyToMany(..., through: 'note_files', orderBy:
   'position')]`. Tenant data gets `#[RequiredScope(InTenant::class)]`.
4. **Register** the class in the list the application gives to `Migrations` (and to
   `EntityCommands` if it registers them).
5. **Migration.** Generate it from the mapping:
   `vendor/bin/shirakaba-migrate diff --config=migrations.php --class=CreateNotes --namespace='App\Migrations'`
   (or `app db:diff ...`). Review it, add indexes for the queries you will run, and add it to
   the migration list.
6. **Apply and check.** `app db:migrate`, then `app db:lint` and `app entities:check` (or
   `SchemaCheck::entities()` in a test).
7. **Read it through projections.** `Entities::query(Note::class)->with('user')->into(NoteView::class, $db)`;
   write with `Entities::insert()`, `update()`, `patch()`.

## Verify

- `vendor/bin/phpstan analyse`: shirakaba/phpstan checks property and relation names in queries
- `app db:diff --check` exits 0 (no missing migration)
- `app db:lint` and `app entities:check` report nothing
- the test suite, against SQLite and, if the project runs them, MySQL and PostgreSQL
