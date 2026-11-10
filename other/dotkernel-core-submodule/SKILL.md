---
name: dotkernel-core-submodule
description: >
  Use whenever a change touches the Core layer of a Dotkernel project — adding or editing a
  Doctrine entity, repository, enum, DBAL type, fixture, migration or shared service — or when
  deciding whether code belongs in Core versus an application module. Also use for git submodule
  mechanics (.gitmodules, git submodule add/init/update, committing from inside src/Core) and for
  questions about sharing code between Dotkernel projects on one database.
---

# The shared Core layer

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
  Packages:  - none
```

Dotkernel's headless platform is a set of projects over one database: an API as the root, and
optionally an Admin for management. The arrangement is flexible — two APIs and one Admin is
equally valid.

`src/Core` is the codebase they share, so one change to a shared entity or service propagates
rather than being copy-pasted into each project. The stock API and Admin ship the same `Core`
modules — `Admin`, `App`, `Security`, `Setting`, `User`.

The stock Frontend, Light and Queue have no `Core`: Frontend keeps its entities inside its own
modules, and Light and Queue have no persistence. A derived project can adopt `Core`, but do not
assume it has.

In API and Admin, `src/Core` ships as an ordinary module, designed as the starting point for
extraction into a git submodule. **Treat it as if it already were one.**

## Rules for Core code

1. **Core is the only place that manages database entities.** All Doctrine entities,
   repositories, enums and DBAL types live under `src/Core/src/<Module>/src/`.
2. **Core must never depend on a project namespace.** No `Api\…`, `Admin\…`, `Frontend\…`
   imports; nothing HTTP-request-shaped, no HAL, no forms. If a Core service must signal failure,
   throw a Core-level exception or return null and let the application layer translate it.
3. **Anything in Core is potentially consumed by every other project.** Before changing a
   Core signature, ask whether it breaks the siblings. Prefer additive changes; deprecate rather
   than rename.
4. **Not everything shared-looking belongs in Core.** Logic used by exactly one project stays
   in that project's module. Core is for genuinely common code.
5. Migration directories under Core are **generated** — never hand-edit.

## Splitting a change

A typical feature spans both layers:

```text
src/Core/src/Book/src/Entity/Book.php               ← schema, invariants, accessors
src/Core/src/Book/src/Repository/BookRepository.php ← query builders
src/Book/src/Service/BookService.php                ← use-case orchestration
src/Book/src/Handler/Book/…Handler.php              ← HTTP / presentation
```

Both layers get their own `ConfigProvider`, and both are registered in `config/config.php`.

## Creating the submodule

Create a new git repository for the Core code, then from the project root:

```bash
git submodule add <url> src/Core
```

Git writes `.gitmodules`, mapping the URL to the local path so it can clone, update and track it.
**Delete the existing `src/Core` directory before adding the submodule** to a second project.

No Dotkernel project ships `.gitmodules` out of the box — it only exists once you have
isolated Core into its own repository.

## Day-to-day mechanics

Cloning a project that has one:

```bash
git submodule init
git submodule update
# or: git clone --recurse-submodules <url>
```

Committing Core changes — **from inside the submodule directory**, which is its own repository:

```bash
cd src/Core
git add .
git commit -m "…"
git push
```

Then, in the parent repository, commit the updated submodule pointer:

```bash
cd ../..
git add src/Core
git commit -m "Bump Core submodule"
```

Skipping that second step is the classic failure: teammates pull and still get the old Core.

## Working rules for an agent

- Before editing Core, state that the change is cross-project and name the likely consumers.
- `git submodule` and `git push` are in the deny tier and refused by the `guard-bash.sh` hook,
  approval or not — never try to run them. Give the user the exact commands to run instead.
- `git add` and `git commit` prompt for approval; run them only when the user has asked for the
  commit.
- If `.gitmodules` exists, do not stage Core content changes from the parent repo — they belong
  to the submodule's own history.
- Schema changes need a migration, generated not written, and **applied by every project on
  that database**.
- A schema-validation CI job will catch entity/migration drift.

## Why this design

Consistency across projects, one place to fix a bug, work splittable across developers
without merge storms, easier onboarding, and a platform that scales by adding projects that
all speak to the same Core-defined model.
