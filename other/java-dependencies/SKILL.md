---
name: java-dependencies
description: "Add, update, remove and audit a module's Maven/JAR dependencies in MDL — Studio Pro's Module Settings → Java dependencies tab. Use when a Java action needs an external library, when bumping a library version, or when auditing which modules pull what."
---

# Managing Maven / JAR Dependencies

This skill explains how to add, update, and remove Maven/JAR dependencies in a
Mendix module using MDL. These are the dependencies declared in Studio Pro's
**Module Settings → Java dependencies** tab, stored as
`Projects$JarDependency` entries inside the module's `Projects$ModuleSettings`
unit.

## When to Use This Skill

- Adding a new external library for a Java action (Jackson, Apache HTTP client, etc.)
- Updating a library version across modules
- Disabling a dependency without removing it (`included = false`)
- Auditing which modules have JAR dependencies

If you only need to copy JARs into `vendorlib/` for a local build (without
registering them in module settings), that is a different operation and does
NOT require MDL.

## Listing Dependencies

```sql
-- All modules
LIST JAR DEPENDENCIES;

-- Single module
LIST JAR DEPENDENCIES IN MyModule;
```

Output columns: `module`, `group`, `artifact`, `version`, `included`.

## Describing a Dependency

```sql
DESCRIBE JAR DEPENDENCY MyModule 'com.fasterxml.jackson.core:jackson-databind';
```

Outputs a re-executable `ALTER MODULE ... ADD JAR DEPENDENCY (...)` block.

## Adding a Dependency

```sql
mdl 1;
ALTER MODULE MyModule
  ADD JAR DEPENDENCY (
    group    = 'com.fasterxml.jackson.core',
    artifact = 'jackson-databind',
    version  = '2.21.2',
    included = true,
  );
```

- `included` defaults to `true` when set explicitly; always set it to be explicit.
- The coordinate `group:artifact` must be unique within the module.

## Updating a Dependency

```sql
mdl 1;
-- Change the version
ALTER MODULE MyModule
  SET JAR DEPENDENCY 'com.fasterxml.jackson.core:jackson-databind' VERSION '2.21.3';

-- Disable without removing (keeps the entry, classpath excluded at build time)
ALTER MODULE MyModule
  SET JAR DEPENDENCY 'com.fasterxml.jackson.core:jackson-databind' INCLUDED false;
```

## Managing Transitive Exclusions

```sql
mdl 1;
-- Exclude a transitive dependency
ALTER MODULE MyModule
  SET JAR DEPENDENCY 'org.duckdb:duckdb_jdbc'
    ADD EXCLUSION 'com.example:conflicting-lib';

-- Remove an exclusion
ALTER MODULE MyModule
  SET JAR DEPENDENCY 'org.duckdb:duckdb_jdbc'
    DROP EXCLUSION 'com.example:conflicting-lib';
```

## Removing a Dependency

```sql
mdl 1;
ALTER MODULE MyModule
  DROP JAR DEPENDENCY 'com.fasterxml.jackson.core:jackson-databind';
```

## Jackson Version Gotcha

Jackson 2.x and 3.x use different package namespaces:

| Version | Group ID | Import prefix |
|---------|----------|---------------|
| 2.x | `com.fasterxml.jackson.core` | `com.fasterxml.jackson.*` |
| 3.x | `tools.jackson.core` | `tools.jackson.*` |

If Java code imports `com.fasterxml.jackson.databind.*` you need **2.x**.
Pin to the version the Mendix runtime bundles to avoid classloader conflicts:

```bash
ls ~/.mxcli/mxbuild/<runtime-version>/runtime/bundles/ | grep jackson
```

## After Adding a Dependency

MDL writes the `Projects$JarDependency` entry into the `.mpr` file. Gradle
still needs to resolve and download the JAR:

1. Open the project in Studio Pro — it will trigger Gradle to populate `vendorlib/`.
2. Or run `mxcli docker build` which invokes `mx` and triggers the Gradle sync.

Until Gradle runs, the JAR is declared but not yet present in `vendorlib/`.
This is the same state as adding a dependency in Studio Pro before clicking OK.

## Coordinate Format

Coordinates use the `group:artifact` format (no version):

```
'com.fasterxml.jackson.core:jackson-databind'
'org.duckdb:duckdb_jdbc'
```

The version is stored separately and shown in `LIST JAR DEPENDENCIES` output.

## Related Skills

- [java-actions](../java-actions/SKILL.md) — authoring Java actions
- [project-settings](../project-settings/SKILL.md) — other module/project settings
