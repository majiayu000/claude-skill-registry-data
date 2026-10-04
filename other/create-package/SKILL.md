---
name: create-package
description: Create a new package in the One Page monorepo with the required LICENSE symlink, README, and workspace registration. Use when adding a new core or feature package.
argument-hint: "<core|features> <package_name>"
---

# Create Package

Parse `$ARGUMENTS` as `<directory> <package_name>` where `<directory>` is either `core` or `features`.

Follow every step below in order. Do not skip steps or use alternative methods.

---

## Step 1 — Scaffold the package

Use the official Flutter command. Manual directory creation is strictly forbidden.

```bash
fvm flutter create -t package packages/<directory>/<package_name> --project-name <package_name>
```

Example:

```bash
fvm flutter create -t package packages/core/my_utils --project-name my_utils
fvm flutter create -t package packages/features/my_feature --project-name my_feature
```

---

## Step 2 — Replace the LICENSE with a symbolic link

The generated LICENSE file must be replaced with a symlink to the root LICENSE file to keep the project consistent.

```bash
# For core packages
rm packages/core/<package_name>/LICENSE
ln -s ../../../LICENSE packages/core/<package_name>/LICENSE

# For features packages
rm packages/features/<package_name>/LICENSE
ln -s ../../../LICENSE packages/features/<package_name>/LICENSE
```

---

## Step 3 — Replace the generated README.md

Overwrite the flutter-create template README with actual content following this structure:

````markdown
# <package_name>

A concise description of what this package does.

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Getting Started

Add the package to your `pubspec.yaml`:

```yaml
dependencies:
  <package_name>:
    path: ../../../packages/<directory>/<package_name>
```
````

## Usage

```dart
// Practical example showing the primary use case
```

````

Do NOT leave any flutter-create template text (e.g., "A starting point for a Dart package.") in the README.

---

## Step 4 — Update the root README.md

Add a new entry for the package in the root `/README.md`. Follow the existing format and maintain alphabetical order within the `core/` or `features/` section. Use a brief, informative description.

---

## Step 5 — Register in Pub Workspaces

**Root `pubspec.yaml`** — add the package path to the `workspace:` section, keeping alphabetical order:

```yaml
workspace:
  - packages/core/<package_name>   # core packages
  - packages/features/<package_name>  # features packages
````

**Package `pubspec.yaml`** (`packages/<directory>/<package_name>/pubspec.yaml`) — add the workspace resolution field:

```yaml
resolution: workspace
```

---

## Step 6 — Set standard dev_dependencies

In `packages/<directory>/<package_name>/pubspec.yaml`, replace the generated `dev_dependencies` block with the project-standard set. Match the versions used in existing packages (check `packages/features/haptics/pubspec.yaml` as the reference):

```yaml
dev_dependencies:
  altive_lints: ^2.3.0
  build_runner: ^2.15.0
  flutter_test:
    sdk: flutter
  mockito: ^5.6.4
```

Also replace the generated `analysis_options.yaml` content to use `altive_lints`:

```yaml
include: package:altive_lints/altive_lints.yaml
```

---

## Step 7 — Verify the new package

```bash
fvm dart run melos bootstrap
fvm dart analyze
```

Both commands must complete without errors before the task is considered complete.
