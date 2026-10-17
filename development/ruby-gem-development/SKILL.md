---
name: ruby-gem-development
description: Use when creating, developing, packaging, releasing, or maintaining a reusable Ruby gem or gem repository.
license: MIT
---

# Ruby Gem Development

## Purpose

Build a real reusable Ruby package with an explicit public API, gemspec, dependency contract, test suite, packaging boundary, and release process.

Core flow:

classify reusable boundary
-> generate or inspect gem skeleton
-> define namespace/load path
-> complete gemspec
-> implement public API
-> declare dependencies
-> test
-> build
-> inspect package
-> install locally
-> verify
-> publish/release only when authorized

## Activate when

- creating a gem with `bundle gem`;
- editing a `.gemspec`;
- defining gem namespace or require paths;
- adding gem runtime/development dependencies;
- adding a gem executable;
- testing a gem independently of an application;
- building or inspecting `.gem` artifacts;
- locally installing a built gem;
- preparing RubyGems/GitHub releases.

Do not activate merely because an application uses gems; use `ruby-gems-io-services` or `ruby-toolchain` as appropriate.

## Repository inspection

Before creating or changing a gem, inspect:

1. the gemspec and current public require paths;
2. `Gemfile`/`Gemfile.lock` and supported Ruby versions;
3. existing namespace and file layout;
4. test/lint conventions and CI;
5. release/versioning conventions;
6. package contents and existing executables/extensions.

Do not replace an existing gem architecture merely because `bundle gem` would produce a different skeleton.

## Start with the skeleton

Bundler provides:

```bash
bundle gem GEM_NAME
```

Common generation choices can include executable, extension, test framework, linter, CI, license, Git, and whether to run bundle install. Inspect `bundle gem --help` for the installed Bundler version.

A generated skeleton is a starting point, not proof of a finished gem.

## Gem boundary

Define:

- canonical gem name;
- stable Ruby namespace;
- top-level require path;
- entry point (`lib/gem_name.rb`);
- public classes/modules and methods;
- supported Ruby versions;
- runtime dependencies;
- development dependencies;
- executables;
- license and metadata;
- test strategy.

Keep application-specific configuration, models, credentials, and deployment assumptions out of a reusable gem unless the gem's API explicitly owns them.

## Gemspec

The gemspec is the package contract.

Verify:

```bash
gem specification GEM.gemspec
```

Review:

- name;
- version;
- summary/description;
- authors/homepage/source code/license metadata;
- `required_ruby_version`;
- runtime dependencies;
- development dependencies;
- included files;
- executables/extensions.

Do not use broad filesystem globs that accidentally package credentials, test artifacts, local logs, or unrelated application files.

## Versioning

Use an explicit versioning policy and keep code, gemspec, and release metadata consistent. Treat breaking public API changes as release changes, not ordinary internal refactors.

Do not infer semantic-versioning promises that the gem has never documented; inspect existing release conventions.

## Dependencies

Add runtime dependencies only when the public gem behavior requires them. Keep development-only tools in development dependencies.

For Bundler-managed development:

```bash
bundle install
bundle exec rake test
bundle exec rubocop
```

Use the gem's declared test/lint conventions rather than imposing another stack.

## Load-path and require contract

Test the gem the way consumers load it:

```bash
ruby -Ilib -e 'require "gem_name"; puts GemName'
```

Check that the top-level require does not depend on the developer's working directory or an application boot process.

Avoid requiring optional integrations at top-level unless they are genuine mandatory runtime dependencies.

## Executables

For a gem with a CLI:

- keep the executable thin;
- delegate business behavior to the library API;
- declare it in the gemspec;
- test argument/error/exit semantics;
- verify the installed executable, not only the source-tree executable.

## Extensions and native code

When a gem has native extensions, verify:

- build configuration;
- required headers/libraries;
- supported Ruby engines/platforms;
- source files included in the package;
- install/build behavior in CI.

Do not require native code when a pure-Ruby implementation satisfies the contract without material cost.

## Package verification

Build with:

```bash
gem build GEM.gemspec
```

Then inspect:

```bash
gem specification GEM_FILE
gem contents GEM_FILE
```

Install into an isolated target when possible:

```bash
gem install GEM_FILE --install-dir tmp/gem-install
```

Then exercise the consumer-facing require path and executable.

Never treat `gem build` success alone as proof that the published artifact is usable.

## Release

Before publishing, verify:

- clean working tree or documented release state;
- version and changelog;
- gemspec metadata;
- package contents;
- tests/lint/security;
- install smoke test;
- credentials and publishing target;
- release artifact provenance.

Publishing to RubyGems is a separate authorization step. Do not publish merely because packaging passes.

## Anti-patterns

- extracting a gem without a real reuse boundary;
- application code leaking into the gem;
- wildcard package files that include secrets;
- public API that depends on application boot state;
- runtime dependencies declared as development-only;
- development tools declared as runtime dependencies;
- testing only inside the source checkout;
- assuming a successful build means successful installation;
- publishing without explicit release authorization.

## Agent review checklist

- [ ] real reusable boundary identified
- [ ] gem skeleton inspected/generated
- [ ] require/namespace contract explicit
- [ ] gemspec metadata complete
- [ ] Ruby/dependency requirements explicit
- [ ] package file set reviewed
- [ ] runtime/development dependency split correct
- [ ] public API tested
- [ ] build succeeds
- [ ] package contents inspected
- [ ] isolated install/require smoke test passes
- [ ] release authorization is explicit

## Verification

Minimum evidence:

```text
bundle exec test/lint evidence
gemspec inspection
gem build evidence
artifact contents inspection
isolated install evidence
consumer require/CLI smoke test
```

Never claim publication or install success unless the command actually ran.

## Source foundation

- Bundler `bundle gem`: https://guides.rubygems.org/command-reference/bundle-gem/
- RubyGems command reference: https://guides.rubygems.org/command-reference/
- RubyGems Gemfile/gemspec guide: https://guides.rubygems.org/gemfile-and-gemspec/
