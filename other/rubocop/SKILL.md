---
name: rubocop
description: Use when linting, reviewing, refactoring, or implementing Ruby/Rails code where RuboCop or a RuboCop extension can provide static-analysis, style, architecture, framework, testing, performance, security-adjacent, or domain-specific feedback.
license: MIT
---

# RuboCop

## Purpose

Use RuboCop as an executable static-analysis layer and use its extension ecosystem when the repository actually contains or targets the corresponding framework/library.

RuboCop's current documentation distinguishes the core Ruby analyzer from plugins that add cops or formatters for external frameworks and libraries. Since RuboCop 1.72, the plugin system based on lint_roller is the recommended loading mechanism for extensions; older extensions may still require legacy `require` loading.

## Activate when

- the task asks for RuboCop/linting/style enforcement
- reviewing Ruby code quality
- refactoring code after RuboCop findings
- configuring `.rubocop.yml`
- deciding which RuboCop plugins apply
- reviewing a Rails/RSpec/Minitest/Rake/Capybara/factory_bot/Sequel/i18n/thread-safety/GraphQL/Sorbet/Chef/SketchUp/packaging codebase
- preparing CI linting

## Repository inspection

Before choosing plugins inspect:

1. Ruby and Rails versions.
2. `Gemfile` and `Gemfile.lock`.
3. `.rubocop.yml` and inherited configs.
4. Existing `plugins:` and legacy `require:` directives.
5. Test framework and supporting libraries.
6. CI commands and lint scripts.
7. Repository-specific cops, extensions, or exclusions.

Prefer the repository's installed versions and configuration over generic latest-version assumptions.

## Plugin-selection algorithm

Use this sequence:

```
inspect dependencies
  -> identify actual frameworks/libraries
  -> select only matching plugins
  -> verify plugin compatibility/version
  -> load via plugin API when supported
  -> run RuboCop
  -> interpret findings in repository context
  -> fix the smallest justified set
  -> rerun focused and full lint
```

Do not load every plugin simply because it exists.

### RSpec style guide

When RSpec is present, treat https://rspec.rubystyle.guide/ as the style-guide source for specification structure and test readability. The guide assumes RSpec 3 or later and identifies `rubocop-rspec` as its executable enforcement path. Focus on example-group structure, contexts, subject/let ordering, expectations, matchers, doubles, test isolation, naming, and controlled DRYing. Do not over-abstract tests merely to remove duplication.

The `rubocop-rspec` extension contains cops linked directly to the guide, including `RSpec/AnyInstance`, `RSpec/BeforeAfterAll`, `RSpec/ContextWording`, `RSpec/ExampleWording`, `RSpec/InstanceVariable`, `RSpec/LeadingSubject`, `RSpec/MultipleExpectations`, `RSpec/NamedSubject`, and `RSpec/PredicateMatcher`.

## Official plugins

The current RuboCop documentation lists:

- `rubocop-performance` — performance optimization analysis
- `rubocop-rails` — Rails-specific analysis
- `rubocop-rspec` — RSpec-specific analysis
- `rubocop-minitest` — Minitest-specific analysis
- `rubocop-rake` — Rake-specific analysis
- `rubocop-sequel` — Sequel-specific analysis
- `rubocop-thread_safety` — thread-safety analysis
- `rubocop-capybara` — Capybara-specific analysis
- `rubocop-factory_bot` — factory_bot-specific analysis
- `rubocop-rspec_rails` — RSpec Rails-specific analysis
- `rubocop-i18n` — i18n wrapper-function analysis

### Third-party plugins

The current RuboCop documentation lists:

- `rubocop-require_tools` — dynamic missing-`require` analysis
- `cookstyle` — Chef Infra Cookbook cops/configuration
- `rubocop-packaging` — packaging/downstream compatibility conventions
- `rubocop-sorbet` — Sorbet-specific analysis
- `rubocop-graphql` — GraphQL-specific analysis
- `rubocop-changed` — changed-files-only analysis
- `rubocop-sketchup` — SketchUp Ruby API analysis

Keep this list synchronized with `data/rubocop/plugins.yml` and the current upstream documentation.

## Loading configuration

Prefer the modern plugin form for extensions that support it:

```yaml
plugins:
  - rubocop-performance
  - rubocop-rails
```

The command-line equivalent is:

```bash
rubocop --plugin rubocop-performance
```

Legacy extensions may still use:

```yaml
require:
  - rubocop-extension
```

Do not convert a working extension from `require` to `plugins` without checking that its installed version supports the plugin API.

## Plugin applicability rules

### Ruby application

Usually consider:

```text
rubocop
rubocop-performance
```

Add other plugins only when their dependencies or source code justify them.

### Rails application

Consider:

```text
rubocop
rubocop-performance
rubocop-rails
```

Add:

- `rubocop-rspec` + `rubocop-rspec_rails` for RSpec/RSpec Rails
- `rubocop-minitest` for Minitest
- `rubocop-factory_bot` when factory_bot is used
- `rubocop-capybara` when Capybara is used
- `rubocop-rake` when Rake-specific checks are useful
- `rubocop-i18n` when the application relies on the covered i18n wrapper APIs

### Other frameworks/libraries

Select from the catalog only when the corresponding technology is actually present:

```text
Sequel      -> rubocop-sequel
GraphQL     -> rubocop-graphql
Sorbet      -> rubocop-sorbet
Chef        -> cookstyle
SketchUp    -> rubocop-sketchup
packaging   -> rubocop-packaging
threading   -> rubocop-thread_safety
require     -> rubocop-require_tools
CI diff     -> rubocop-changed
```

## Configuration strategy

Do not generate an enormous `.rubocop.yml` automatically.

First establish:

- target Ruby version
- target Rails version when applicable
- plugin versions
- project style conventions
- enabled/disabled cops
- generated-code exclusions
- test/support-code exclusions
- CI performance constraints

For RuboCop Rails, use `AllCops: TargetRailsVersion` when the repository needs an explicit Rails target; otherwise inspect the lockfile behavior described by the installed extension.

When the task is producing a standardized `.rubocop.yml` for a target Rails application, start from `data/rubocop/reference-config.yml` and resolve its version placeholders per `docs/RUBOCOP_REFERENCE_CONFIG.md` instead of assembling the config from scratch; its RSpec block must stay consistent with the RSpec consumer snippet that `docs/RSPEC_STYLE_GUIDE.md` indexes and that `test/test_engineering_system_test.rb` keeps identical to the repository policy.

## Finding interpretation

A cop finding is evidence, not an unconditional design verdict.

For each finding:

1. identify the cop and source of the rule;
2. inspect the surrounding code and contract;
3. check whether the cop is applicable to this repository/version;
4. determine whether the issue is correctness, maintainability, performance, consistency, or intentional style;
5. make the smallest justified change;
6. add/update tests for behavior changes;
7. rerun the relevant cop/plugin and then broader RuboCop.

Do not rewrite correct code solely to reduce a metric.

## Auto-correct safety

Before using `rubocop -A` or broad auto-correction:

- inspect the target cops;
- prefer safe autocorrect where available;
- review the complete diff;
- run tests;
- rerun RuboCop;
- avoid mixing unrelated formatting changes with behavior changes.

Use narrower commands such as:

```bash
rubocop path/to/file.rb
rubocop --only Layout/...,Style/...
```

when diagnosing a focused issue.

## Baseline and migration

When introducing RuboCop into an existing codebase:

1. establish the current Ruby/framework versions;
2. load only applicable plugins;
3. run the configured/default cops;
4. capture existing violations without hiding new violations indefinitely;
5. decide which cops are project policy;
6. migrate incrementally;
7. keep CI enforcing the intended baseline.

Prefer explicit documented exclusions to unexplained broad disabling.

## Reference example

A pinned, reviewable RuboCop configuration: new cops enabled consciously, and every deviation from default justified in place.

```yaml
# .rubocop.yml
plugins: [rubocop-rails]

AllCops:
  NewCops: enable          # new rules appear loudly, not silently
  SuggestExtensions: false
  Exclude:
    - db/schema.rb
    - vendor/**/*

Style/Documentation:
  Enabled: false           # this repo documents skills, not every PORO

Metrics/MethodLength:
  Max: 12
  CountAsOne: [array, hash, heredoc]

Rails/Output:
  Exclude:
    - lib/tasks/**/*       # rake tasks legitimately print

# Prefer correcting with `bin/rubocop -a`, then reviewing the diff - never
# auto-commit corrections with generated bulk changes mixed in.
```

## Agent review checklist

- [ ] Ruby/Rails version resolved
- [ ] Gemfile/Gemfile.lock inspected
- [ ] existing RuboCop configuration inspected
- [ ] applicable plugins identified from actual dependencies
- [ ] plugin versions/compatibility checked
- [ ] plugin API vs legacy require loading resolved
- [ ] findings interpreted in repository context
- [ ] auto-correction scope controlled
- [ ] behavior changes covered by tests
- [ ] focused RuboCop run executed
- [ ] broader lint/CI-equivalent run executed
- [ ] final diff reviewed

## Verification

Use the repository's configured RuboCop command first. When no command exists, prefer `bundle exec rubocop` for bundled applications.

For plugin-specific work, verify both:

```bash
bundle exec rubocop --show-cops
bundle exec rubocop path/to/changed/files
```

Then run the repository's full lint/test checks.

Never claim RuboCop is clean unless the command actually ran and passed.

## Source foundation

RSpec Style Guide: https://rspec.rubystyle.guide/

RuboCop RSpec extension: https://docs.rubocop.org/rubocop-rspec/

Current upstream plugin taxonomy and loading guidance: RuboCop documentation, version 1.89, Plugins page. The page states that RuboCop 1.72 introduced the plugin system and recommends it for extensions that support it; it lists the official and third-party plugins catalogued by this repository.

Source: https://docs.rubocop.org/rubocop/latest/plugins.html
