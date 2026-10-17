---
name: rails-application-bootstrap
description: Use when creating, initializing, or intentionally reshaping a Rails application with rails new, including standard monoliths, API-only applications, database choices, frontend/build choices, templates, skip options, and reproducible project bootstrap.
license: MIT
---

# Rails Application Bootstrap

## Purpose

Create the correct Rails application shape before feature development, using the resolved Rails version and explicit architectural choices.

Core flow:

resolve Ruby/Rails
-> inspect required application shape
-> inspect version-aware generator help
-> choose bootstrap options
-> run rails new
-> install dependencies
-> inspect generated diff
-> initialize database/assets/tests as appropriate
-> verify boot

## Activate when

- running `rails new`;
- creating a new Rails project;
- choosing monolith versus API-only shape;
- choosing database or frontend/build defaults;
- applying a Rails application template;
- deciding which generated framework components to skip;
- bootstrapping Rails into an existing/empty directory;
- reviewing or reproducing a Rails project's initial generator options.

Do not activate for resource generators inside an existing app; use `rails-generators`.

## Repository inspection

Inspect, in order:

1. `.ruby-version`, `.tool-versions`, or other runtime declarations;
2. Gemfile/Gemfile.lock and Rails dependency constraints;
3. existing application type, frontend/build strategy, database, and test stack when bootstrapping an existing repository;
4. CI/deployment setup when reproducing an existing project's bootstrap;
5. target directory state before running `rails new`.

## Preconditions

Resolve Ruby and Rails versions first. Prefer the repository or project constraint over current Rails documentation.

If the Rails executable is not yet available, install/use a version compatible with the intended project. For an application dependency, keep the Rails version in the Gemfile rather than relying on a global Rails executable.

Use:

```bash
rails --version
rails new --help
```

and, once a bundle exists:

```bash
bin/rails --version
```

Treat `rails new --help` for the resolved Rails version as the authoritative flag surface. Do not hard-code a historical list of flags when version-sensitive options can be inspected directly.

## Application archetypes

### Standard Rails monolith

```bash
rails new my_app
```

Use for a conventional full-stack Rails application unless requirements call for a different shape.

### API-only application

```bash
rails new my_api --api
```

API-only mode changes the generated application middleware/controller defaults and generator surface. Verify the resulting stack rather than assuming every full-stack component is absent.

### Database selection

Use the version-supported `--database` option when a specific database adapter is required, for example:

```bash
rails new my_app --database=postgresql
```

Verify the generated Gemfile and database configuration.

### Frontend/build strategy

Select the repository's required JavaScript/CSS/build approach from the resolved Rails version and current project conventions. Do not force a frontend stack into an app that does not need it.

Inspect relevant `rails new --help` options rather than copying flags from another Rails version.

### Optional framework components

Use targeted `--skip-*` options only when the architecture deliberately excludes that component. Understand dependency implications: skipping one framework component can activate or require additional skips.

Do not skip components merely to reduce file count.

### Templates and reproducibility

Use an application template when project policy requires repeatable bootstrap customization:

```bash
rails new my_app -m path/to/template.rb
```

Prefer a version-controlled template over a one-off shell history when the bootstrap must be reproduced.

## Full flag surface

Rails' `new` command evolves. Common option categories include:

- application name and destination;
- database;
- API-only mode;
- JavaScript/CSS/build choices;
- asset pipeline choices;
- framework component skips;
- test/CI/deployment options;
- template source;
- Git/skip/pretend/force/quiet controls;
- version-specific generator options.

Do not claim a flag exists in the target Rails release without inspecting `rails new --help` for that release.

## Existing directory bootstrap

Before running `rails new` in a non-empty directory:

1. inspect tracked/untracked files;
2. determine whether Rails will overwrite or conflict with existing files;
3. use `--skip`, `--force`, or a clean target only when explicitly justified;
4. inspect the resulting diff before accepting it.

Never use `--force` as a blind recovery mechanism.

## Post-bootstrap verification

Verify:

```bash
bundle install
bin/rails --version
bin/rails about
bin/rails runner 'puts Rails.version'
bin/rails db:prepare
bin/rails test
```

Run only tasks supported by the selected application shape.

Start the app when runtime verification is required:

```bash
bin/rails server
```

For CI/non-interactive verification, prefer boot/test commands that terminate deterministically.

## Agent review checklist

- [ ] Ruby version resolved
- [ ] Rails version resolved
- [ ] `rails new --help` inspected for that version
- [ ] app archetype explicitly chosen
- [ ] database explicitly chosen when required
- [ ] frontend/build strategy explicitly chosen when required
- [ ] skip options justified and dependency effects understood
- [ ] template/source provenance recorded
- [ ] generated diff reviewed
- [ ] dependencies installed
- [ ] boot/database/test verification run

## Anti-patterns

- copying `rails new` flags from an unrelated Rails release;
- using API-only mode when server-rendered UI is required;
- using full-stack mode when the application contract is intentionally API-only;
- skipping framework components solely to make a smaller directory;
- running `rails new --force` over existing work;
- treating generated defaults as architecture without review;
- running a global Rails command against a different project bundle.

## Verification

The minimum evidence for a new application is:

```text
resolved Ruby
resolved Rails
rails new invocation + selected options
generated project structure
bundle resolution
boot/test evidence
```

Record the exact command and target Rails version. Report unsuccessful or unrun checks explicitly.

## Source foundation

- Rails Command Line Guide: https://guides.rubyonrails.org/command_line.html
- Rails API-only applications: https://guides.rubyonrails.org/api_app.html
- Rails Getting Started Guide: https://guides.rubyonrails.org/getting_started.html
