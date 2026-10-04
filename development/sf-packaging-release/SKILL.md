---
name: sf-packaging-release
description: Second-generation packaging (2GP) and unlocked packages as a release mechanism - deciding between org-based deployment, unlocked packages and managed packages, the sfdx-project.json packaging attributes (package, versionName, versionNumber with NEXT and LATEST, ancestorVersion, dependencies, seedMetadata, unpackagedMetadata, apexTestAccess), the sf package command surface from create through version create, promote, install and uninstall, installation keys, upgrade types and data loss on component removal, org-dependent unlocked packages, dependency graphs across repositories, and why StandardValueSet needs seedMetadata. Use when splitting a monorepo into packages, publishing or installing a package version, wiring package dependencies, or deciding whether packaging is the right release model at all.
---

# Packaging and Release

## When to use

- Deciding how a codebase is released: org-based deployment, unlocked packages, or managed.
- Creating, versioning, promoting, installing or uninstalling a package.
- Wiring dependencies between packages, or splitting a monorepo.
- A package install fails on a prompt, a dependency, or a standard picklist value.

This is not part of the per-PR gate. `vf-check` gates a change into an org; packaging targets ISV
and multi-repo release concerns. Day-to-day deployment is skill `sf-deployment-strategies`.

## First question: do you need packages at all?

| Situation | Model | Why |
| --- | --- | --- |
| One team, one org lineage, one repo | **Org-based deployment** | `sf project deploy start` with validate plus quick deploy. No version graph to maintain |
| Several teams shipping on independent cadences into the same org | **Unlocked packages** | Each package versions and releases on its own clock |
| Metadata you cannot untangle from existing org configuration | **Org-dependent unlocked package** | Dependencies validate at install time, not at version-create time |
| Distributing to orgs you do not control | **Managed package (2GP)** | Namespace, intellectual property protection, upgrade paths, AppExchange |
| One repo, and you just want releasable units | **Nothing yet** | Package directories in `sfdx-project.json` are already the ownership boundary |

The cost of packaging is real: version pinning, a dependency graph to maintain, and cross-package
refactors that stop being a single commit. Take it when independent release cadence is a
requirement, not because it sounds tidier.

Multi-repo and cadence trade-offs in detail:
[references/release-models.md](references/release-models.md).

## `sfdx-project.json` packaging attributes

```json
{
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "67.0",
  "packageDirectories": [
    {
      "path": "util",
      "default": true,
      "package": "Expense Manager - Util",
      "versionName": "Summer '26",
      "versionNumber": "4.7.0.NEXT",
      "definitionFile": "config/scratch-org-def.json"
    },
    {
      "path": "exp-core",
      "default": false,
      "package": "Expense Manager",
      "versionName": "v 3.2",
      "versionNumber": "3.2.0.NEXT",
      "definitionFile": "config/scratch-org-def.json",
      "dependencies": [
        { "package": "Expense Manager - Util", "versionNumber": "4.7.0.LATEST" }
      ]
    }
  ],
  "packageAliases": {}
}
```

| Attribute | Required | What it does |
| --- | --- | --- |
| `package` | yes | The package name |
| `path` | yes | Directory holding the package contents. Without one the CLI uses a placeholder |
| `versionNumber` | yes | `MAJOR.MINOR.PATCH.BUILD`, for example `1.2.1.8`. **Increment it before creating a new version** or you get duplicates at the same number |
| `versionName` | no | Defaults to `versionNumber` |
| `versionDescription` | no | Free text |
| `packageAliases` | yes | The CLI writes aliases here on create; use the alias instead of the `0Ho`/`04t` id |
| `namespace` | no | 1-15 alphanumeric characters distinguishing your package from others |
| `dependencies` | no | Packages this one needs, each with `package` and `versionNumber` |
| `ancestorVersion` / `ancestorId` | no | Defines the upgrade path |
| `seedMetadata` | no | Path to a directory of metadata seeded at install. **Standard value sets only** |
| `unpackagedMetadata` | no | Path to metadata that is not part of the package, available to package-creation Apex tests |
| `apexTestAccess` | no | Permission sets and permission set licenses granted to the user running Apex tests at version create |
| `includeProfileUserLicenses` | no | Default false. `true` retains user licences associated with profiles in unlocked packages |
| `postInstallUrl`, `releaseNotesUrl` | no | URLs shown to subscribers |
| `definitionFile` | no | A scratch-org-like definition describing the org the package is built against |

**Version number keywords:**

- `NEXT` in the build position (`1.2.1.NEXT`) auto-increments to the next available build.
- `LATEST` in a dependency's `versionNumber` (`4.7.0.LATEST`) pins to the latest build of that
  major.minor.patch.

**Ancestry keywords:**

- `"ancestorVersion": "HIGHEST"` sets the ancestor to the highest promoted and released version.
- `"ancestorVersion": "NONE"` breaks the upgrade path - **an existing customer cannot upgrade to
  that version.** Use it deliberately or not at all.

A CLI flag always overrides the value in the project file.

## Core patterns

### 1. Create a package and its first version

```bash
sf package create \
  --name "Expense Manager - Util" \
  --package-type Unlocked \
  --path util \
  --target-dev-hub devhub

sf package version create \
  --package "Expense Manager - Util" \
  --installation-key-bypass \
  --code-coverage \
  --wait 30 \
  --target-dev-hub devhub
```

`--package-type` is `Managed` or `Unlocked`, and it is required. `--path` and `--name` are required.
`sf package create` writes the `0Ho` id into `packageAliases` for you.

`--code-coverage` calculates and stores the coverage percentage by running the packaged Apex tests.
You need it: **a version created with `--skip-validation` cannot be promoted.**

### 2. Promote before anyone installs it in production

```bash
sf package version promote --package "Expense Manager - Util@4.7.0-1" --target-dev-hub devhub
```

Promote moves the version to **released** status. `--no-prompt` skips the confirmation, which is
what CI needs and what a human should not use casually. A version that is not promoted is a beta.

### 3. Install, without a prompt hanging your pipeline

```bash
sf package install \
  --package 04t... \
  --target-org acme-uat \
  --wait 20 --publish-wait 20 \
  --no-prompt
```

| Flag | Meaning |
| --- | --- |
| `-p, --package` | `04t` id or alias of the **version** |
| `-k, --installation-key` | Required for a key-protected package |
| `-r, --no-prompt` | Allows, without confirmation: Remote Site Settings and Content Security Policy websites sending or receiving data, and `--upgrade-type Delete` |
| `-s, --security-type` | Default `AdminsOnly` |
| `-t, --upgrade-type` | `Mixed` (default), `DeprecateOnly`, `Delete`. Unlocked packages only |
| `-a, --apex-compile` | `all` (default) or `package` |
| `-b, --publish-wait` | Minutes to wait for the `04t` id to become available |

`RemoteSiteSetting` and `CspTrustedSite` prompts are the classic cause of a pipeline that hangs
forever with no output. `--no-prompt` is the fix.

### 4. Understand `--upgrade-type` before you use it

Upgrading an **unlocked** package where components were removed from the new version:

| Value | Removed components | Risk |
| --- | --- | --- |
| `Mixed` (default) | Deprecated or deleted per component type | Moderate |
| `DeprecateOnly` | Deprecated, never deleted | Safe |
| `Delete` | Deleted from the subscriber org | **Can result in the loss of data associated with the deleted components** |

`Delete` is one of the two things `--no-prompt` silently authorises. Do not combine them without
knowing exactly which components were removed.

### 5. Declare dependencies, and let transitive ones be computed

```json
"dependencies": [
  { "package": "Expense Manager - Util", "versionNumber": "4.7.0.LATEST" }
]
```

With `calculateTransitiveDependencies` set to `true` you list only **direct** dependencies and the
indirect ones are calculated. Without it, you list the whole chain by hand and it drifts.

### 6. `seedMetadata` for standard value sets

A package cannot contain a `StandardValueSet`. If your package depends on standard picklist values,
the install fails. The supported route is a seed metadata directory:

```json
"packageDirectories": [
  {
    "path": "force-app",
    "package": "Expense Manager",
    "versionNumber": "3.2.0.NEXT",
    "seedMetadata": { "path": "my-unpackaged-seed-directory" }
  }
]
```

Seed metadata is available to **standard value sets only**. It is not a general-purpose escape
hatch for unpackageable metadata.

### 7. `unpackagedMetadata` for test-only fixtures

```json
"unpackagedMetadata": { "path": "my-unpackaged-directory" }
```

Metadata that is not part of the package but must exist for package-creation Apex tests to pass -
test custom objects, sample records' supporting configuration. **You cannot include the same
metadata in both an unpackaged directory and a packaged directory.**

When the tests need permissions rather than metadata, use `apexTestAccess`:

```json
"apexTestAccess": {
  "permissionSets": ["Permission_Set_1", "Permission_Set_2"],
  "permissionSetLicenses": ["SalesConsoleUser"]
}
```

### 8. Installation keys

```bash
sf package version create --package "Expense Manager" --installation-key "s3cret" --wait 30 --target-dev-hub devhub
sf package install --package 04t... --installation-key "s3cret" --target-org acme-uat --wait 20 --no-prompt
```

The key is checked **first**, before any package information such as the name or component list is
disclosed. `--installation-key-bypass` (`-x`) creates a version with no key; either `-k` or `-x` is
required at version create.

Do not put the key on the command line in CI. The vibe-force Bash guard denies credentials as
command-line arguments; read it from the environment or a secret store.

## Anti-patterns

### Promoting a version created with `--skip-validation`

You cannot. The CLI says so: "you can't promote unvalidated package versions." If your pipeline
uses `--skip-validation` for speed, it has quietly given up on releasing that build.

### `ancestorVersion: NONE` left in place

It breaks the upgrade path. Existing customers cannot move to that version. It is a deliberate
break-glass setting, not a default.

### Not incrementing `versionNumber`

Two versions with the same `MAJOR.MINOR.PATCH.BUILD` is a mess you cannot untangle afterwards. Use
`NEXT` in the build position so the CLI handles it.

### `--no-prompt` plus `--upgrade-type Delete` in CI

That combination deletes components from the subscriber org and can take data with them, with no
human in the loop. If CI must be unattended, pin `--upgrade-type DeprecateOnly`.

### Packaging a monorepo that has no independent cadence

Version pinning, a dependency graph and expensive cross-package refactors, bought for nothing.
Package directories already give you ownership boundaries.

### Putting fflib in every package

A base package containing fflib plus your shared utilities, depended on by the rest, is the shape
that works. Duplicating the library into each package guarantees version skew. See skill
`sf-fflib-foundations`.

### Same metadata in a packaged and an unpackaged directory

Explicitly unsupported. Decide which one owns it.

## Verification

```bash
# What exists
sf package list --target-dev-hub devhub
sf package version list --packages "Expense Manager" --target-dev-hub devhub

# Was the version created, and did validation pass
sf package version create report --package-create-request-id 08c... --target-dev-hub devhub

# What the version actually depends on, and its ancestry
sf package version displaydependencies --package 04t... --target-dev-hub devhub
sf package version displayancestry --package "Expense Manager" --target-dev-hub devhub

# Install progress
sf package install report --request-id 0Hf... --target-org acme-uat

# What is installed in the org right now
sf package installed list --target-org acme-uat

# The ordinary local gate still applies to the source
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
```

## References

- [references/package-command-matrix.md](references/package-command-matrix.md) - every `sf package` command with required flags and gotchas
- [references/sfdx-project-packaging.md](references/sfdx-project-packaging.md) - the full `packageDirectories` packaging attribute set
- [references/release-models.md](references/release-models.md) - org-based versus unlocked versus managed, and multi-repo dependency management

Sibling skills: `sf-project-structure` (`sfdx-project.json` outside packaging, package directories
as ownership boundaries), `sf-deployment-strategies` (the org-based release path and the per-PR
gate), `sf-cli-operations` (auth to a Dev Hub, JSON output, CI patterns),
`sf-scratch-orgs-sandboxes` (the orgs package versions are built and tested against),
`sf-fflib-foundations` (base package containing the framework),
`sf-code-analyzer-quality` (the static gate that runs before any of this),
`sf-apex-testing` (the coverage `--code-coverage` measures).

Sources: Salesforce DX Developer Guide, "Project Configuration File for Unlocked Packages",
"Package Installation Key", "Specify Unpackaged Metadata or Apex Access for Apex Tests",
"Manage Apex Access for Package Version Creation Tests"; Salesforce CLI command reference for
`sf package`. All Summer '26 / API version 67.0.
