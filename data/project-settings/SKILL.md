---
name: project-settings
description: "Read and change project settings in MDL — database configuration, constant overrides, after-startup and before-shutdown microflows, the enabled languages (add/modify/remove, which decide what translations a build emits), and the rest of Studio Pro's Settings dialog. Use when configuring a deployment, wiring a startup microflow, or enabling a language before translating an app."
---

# Project Settings

## When to Use This Skill

Use this skill when the user wants to:
- Configure database connections (PostgreSQL, SQLServer, etc.)
- Set up Kafka endpoints or other constant overrides
- Change the after-startup or before-shutdown microflows
- Modify hash algorithms, Java versions, or rounding modes
- View or modify language settings
- Configure workflow settings (user entity, parallelism, groups)

## Commands

### View Settings

```sql
-- Overview table of all settings parts
list settings;

-- Full MDL output (round-trippable ALTER SETTINGS statements)
describe settings;
```

### Modify Model Settings

```sql
mdl 1;
alter settings runtime ( AfterStartupMicroflow: 'Module.MF_Startup' );  -- must return Boolean (CE0142)
alter settings runtime ( BeforeShutdownMicroflow: 'Module.MF_Shutdown' );
alter settings runtime ( HealthCheckMicroflow: 'Module.MF_HealthCheck' );
alter settings runtime ( HashAlgorithm: 'BCrypt' );
alter settings runtime ( BcryptCost: 12 );
alter settings runtime ( JavaVersion: 'Java21' );  -- or '21'; see note below
alter settings runtime ( RoundingMode: 'HalfUp' );
alter settings runtime ( AllowUserMultipleSessions: true );
alter settings runtime ( ScheduledEventTimeZoneCode: 'Etc/UTC' );
alter settings runtime ( DefaultTimeZoneCode: 'Europe/Amsterdam' );
alter settings runtime ( FirstDayOfWeek: 'Monday' );       -- Default, Monday..Sunday
alter settings runtime ( DecimalScale: 8 );
alter settings runtime ( EnableDataStorageOptimisticLocking: true );
alter settings runtime ( UseDatabaseForeignKeyConstraints: true );
alter settings runtime ( UseOQLVersion2: true );
alter settings runtime ( SslCertificateAlgorithm: 'PKIX' );   -- PKIX or SunX509
```

**Not every project stores every setting.** Mendix adds model settings over time —
a blank 9.24 project stores 12 of them, a blank 11.13 project stores 17. mxcli
refuses an `alter` naming one the project does not store rather than introducing
it, because Studio Pro refuses to open a model carrying a property its type does
not define (and `mx check` does *not* catch that). `describe settings` emits only
what the project actually stores, so its output always replays.

**`UseSystemContextForBackgroundTasks` is read but not writable.** Mendix withdrew
it: `mx check` on 11.13 rejects a project holding `true` with
**CE9436** *"The project setting 'System context tasks' is not supported anymore."*
mxcli preserves whatever the project stores and offers no way to change it.

**Optimistic locking** is App Settings → Runtime → *Optimistic locking* in Studio
Pro. With it on, the runtime tracks an `MxObjectVersion` on every persistable
entity and a commit whose version no longer matches the database throws
`ConcurrentModificationRuntimeException`.

Reach for it when a microflow reads a value, decides on it, and writes it back —
the classic "check the balance, then debit it" shape. A microflow is one
transaction, so each run is *atomic*, but that does not make two concurrent runs
*serialisable*: both can pass the check and the second overwrites the first. With
optimistic locking on, the second commit fails and its whole microflow rolls back
instead of silently overdrawing the account.

It **detects, it does not retry.** Mendix's guidance is that the handler must
catch the exception, *reload* the object, re-apply and re-commit — "trying to
commit the same object without reloading always results in an optimistic locking
error." Without that the user sees a failure rather than a transfer that works.
The money is safe either way, which is the half that matters.

**JavaVersion spelling.** Mendix renamed this property between versions: up to 11.6
it stores `JavaVersion` = `'Java21'`, from 11.12 it stores `JavaMajorVersion` =
`'21'`. Write either spelling — mxcli reads which one the project uses and stores
the value in that dialect. Getting this wrong is not a cosmetic difference: 11.12
parses the bare major and rejects the project outright with
`ArgumentOutOfRangeException: majorVersion is an unsupported value: Java21`.
`describe settings` always emits the project's own spelling, so its output replays
cleanly.

**`describe settings` never prints `DatabasePassword`.** Describe output is what gets
committed and reviewed, so the password is omitted and a comment says it is set.
Replaying the output leaves the stored password unchanged (`create or modify
configuration` only touches the keys it names); on a project that lacks the
configuration, add `DatabasePassword = '…'` yourself.

### Modify Configuration Settings

```sql
mdl 1;
-- Full database configuration
alter settings configuration 'Default' (
  DatabaseType: 'PostgreSql',
  DatabaseUrl: 'localhost:5432',
  DatabaseName: 'mydb',
  DatabaseUserName: 'mendix',
  DatabasePassword: 'mendix',
  HttpPortNumber: 8080,
  ServerPortNumber: 8090
);

-- Update a single field
alter settings configuration 'Default' (
  DatabaseUrl: 'newhost:5432'
);
```

`HttpPortNumber`, `ServerPortNumber`, `BcryptCost`, `DefaultTaskParallelism` and
`WorkflowEngineParallelism` and `DecimalScale` are Integer-typed;
`AllowUserMultipleSessions`, `EnableDataStorageOptimisticLocking`,
`UseDatabaseForeignKeyConstraints` and `UseOQLVersion2` are Boolean; `FirstDayOfWeek`
and `SslCertificateAlgorithm` are enumerations, matched case-insensitively and
stored in Mendix's own spelling (MDL-SET03 rejects a non-member rather than writing
it through — an unresolvable enum value is what makes Studio Pro throw
"Sequence contains no matching element").
An unparseable value is rejected by `mxcli check` (MDL-SET01 / MDL-SET02)
and by the write itself — it is no longer silently ignored. Quoted numbers are
fine: `HttpPortNumber = '8080'` and `HttpPortNumber = 8080` are equivalent.

### Constant Overrides

```sql
mdl 1;
-- View constant values across all configurations
list constant values;
list constant values in MyModule;    -- Filter by module

-- Override a constant value in a configuration
alter settings constant @BusinessEvents.ServerUrl value 'kafka:9092'
  in configuration 'Default';

-- Without IN CONFIGURATION (uses first configuration)
alter settings constant @MyModule.ApiKey value 'abc123';

-- Remove a constant override (reset to default)
alter settings drop constant @MyModule.ApiKey in configuration 'Default';
```

#### Shared vs private values

A constant override's value is either **shared** — stored in the model and therefore
in version control, where every developer gets it — or **private**, stored on the
developer's own workstation and deliberately kept out of the repository. Development
API tokens are the usual reason to make one private.

MDL **preserves that choice but never changes it**. The two statements above operate
on shared values only:

- `list constant values` reports a private override as `(private)` rather than a blank
  cell — the value is not in the project, so mxcli cannot show it.
- `describe settings` reports a private override as a comment, not as a re-executable
  `alter settings constant` line — replaying that line would publish into the shared
  model a value the developer chose to keep local.
- `alter settings constant ... value ...` on a private override is **refused**, with a
  pointer to change it in Studio Pro first. Setting a value would convert it to a
  shared one and break the developer's local binding.
- `alter settings drop constant ...` **is** allowed: it removes the whole override,
  private marker included, which is what was asked for.

### Create / Drop Configurations

```sql
mdl 1;
-- Create a new server configuration
create configuration 'Staging';

-- Create with properties
create configuration 'Production' (
  DatabaseType: 'PostgreSql',
  DatabaseUrl: 'prod-db:5432',
  HttpPortNumber: 8080
);

-- Drop a configuration
drop configuration 'Staging';
```

`DatabaseType` must name a Mendix database type — `Db2`, `Hsqldb`, `MySql`,
`Oracle`, `PostgreSql`, `SapHana` or `SqlServer` — matched case-insensitively and
stored in that spelling. Any other value is rejected; a configuration stored with
one Mendix does not recognise cannot be opened in Studio Pro.

### Language Settings

A project's **enabled languages** are the only ones a build emits translations
for. Writing translations for any other language stores them, passes `mx check`,
and produces nothing at build time — so enable the language first.

```sql
mdl 1;
-- enable, change, disable
alter settings LANGUAGE add 'de_DE';
alter settings LANGUAGE add 'ar_SD' (CheckCompleteness: true, CustomDateFormat: 'yyyy-MM-dd');
alter settings LANGUAGE modify 'de_DE' (CheckCompleteness: true);
alter settings Language drop 'de_DE';

-- the default must already be enabled
alter settings LANGUAGE ( DefaultLanguageCode: 'en_US' );
```

A language is identified by its **code** — "Arabic, Sudan" is derived from
`ar_SD` for display and is not stored.

- `CheckCompleteness` reports errors for texts with no translation in that
  language; the **default language is always checked** regardless.
- `MODIFY` touches only the options it names. `ADD OR MODIFY` is the upsert, and
  is what `describe settings` emits.
- The **default language cannot be removed** (everything falls back on it).
  Removing any other language does **not** delete its translations — they stay in
  the model and stop being built.

**Set the default language BEFORE authoring content.** The default is not only a
fallback — it is the language a new caption is stored under, because Mendix has no
language-neutral text. `alter settings LANGUAGE (DefaultLanguageCode: 'nl_NL')`
*after* creating a page leaves that page's texts in the old language, and nothing
reports it: `mx check` is 0 errors either way and the symptom shows up only in
Studio Pro, as the empty-caption placeholder plus a "no translation" warning.

Wrong order is recoverable — **re-run the `create` statements** and the texts are
rewritten under the new default (the old copy stays alongside, harmless).
`create translations for '<the default>'` is refused: the default is the source
language, not a translation target.

⚠️ `list languages` lists languages that have **translations**, not enabled ones —
a stock app reports 8 while 1 is enabled. Use `describe settings` for the enabled
list.

### Workflow Settings

```sql
mdl 1;

alter settings workflows (
  UserEntity: 'System.User',
  DefaultTaskParallelism: 3
);
```

### Workflow Groups (Mendix 11.2+)

The named buckets under App Settings ▸ Workflows ▸ Groups that a user task's
group targeting selects from.

```sql
mdl 1;
alter settings workflows add group 'Approvers' (Description: 'Primary approval group');
alter settings workflows add group 'Reviewers';

-- the upsert, and what `describe settings` emits
alter settings workflows add or modify group 'Approvers' (Description: 'Approves budget requests');

-- changes only the options it names
alter settings workflows modify group 'Reviewers' (Description: 'Second-line review');

alter settings workflows drop group 'Reviewers';

list workflow groups;
```

Four things worth knowing:

- **`Description` is the only option.** A `Settings$WorkflowGroup` stores `Name`
  and `Description` and nothing else, so there is no identifier to set and the
  **name is the group's identity** — which is what MODIFY and REMOVE address, and
  why a second group differing only in case is refused rather than created.
- **The version floor is 11.2, not 11.6.** `Settings$WorkflowGroup` and the
  `groups` property were both introduced in the 11.2 metamodel; Mendix's release
  notes call the feature GA in 11.6, which is a different question from whether
  the document loads. On an earlier version the statement is refused with the
  floor.
- **An edit keeps the group's runtime identity.** Booting the app materialises one
  `System.WorkflowGroup` row per entry, keyed on the group's element id — so
  changing a description updates that row in place rather than replacing it, and
  the group memberships and assigned user tasks survive.
- **Nothing in the model points at a group.** A user task targets groups through a
  microflow or an XPath returning `System.WorkflowGroup` objects, never by a
  reference to the settings entry, so REMOVE has no dangling reference to check
  for. What it does mean is that the removed group's runtime row stops being
  maintained while the user tasks already assigned to it keep their association.

## Common Patterns

### PostgreSQL Configuration
```sql
mdl 1;
alter settings configuration 'Default' (
  DatabaseType: 'PostgreSql',
  DatabaseUrl: 'localhost:5432',
  DatabaseName: 'myapp',
  DatabaseUserName: 'mendix',
  DatabasePassword: 'mendix',
  HttpPortNumber: 8080
);
```

### SQL Server Configuration
```sql
mdl 1;
alter settings configuration 'Default' (
  DatabaseType: 'SqlServer',
  DatabaseUrl: 'localhost:1433',
  DatabaseName: 'myapp',
  DatabaseUserName: 'sa',
  DatabasePassword: 'MyPassword',
  HttpPortNumber: 8080
);
```

## Checklist

- [ ] Always run `list settings` or `describe settings` first to see current values
- [ ] Verify changes after modification with `list settings`
- [ ] There is always exactly one ProjectSettings document; it cannot be created or deleted
- [ ] Model setting key names are case-sensitive (e.g., `JavaVersion`, not `javaversion`)
- [ ] Configuration names are case-insensitive (e.g., `'default'` matches `'default'`)
- [ ] Integer / Boolean settings must parse — `mxcli check` reports MDL-SET01 / MDL-SET02 before the write

## AfterStartupMicroflow Must Return Boolean

A microflow wired as the project's **after-startup** microflow must return `Boolean` — Mendix build fails with **CE0142** on a void (no-return) microflow. A common trip-up: a seed/demo-data microflow wired to after-startup will not build until it ends with a `return true` (Boolean).

`mxcli check` now reports it (**MDL073**), which it could not before: #274 made `ALTER SETTINGS` resolve the qualified names it writes, but the name here *resolves* — the constraint is on the thing it names, not on the reference. The check runs with **no project** when the script creates the microflow itself (the usual shape), and against the stored return type when it does not. A microflow whose return type cannot be established is left alone rather than guessed at. `BeforeShutdownMicroflow` and `HealthCheckMicroflow` are deliberately **not** type-checked — their rules have not been measured here.
