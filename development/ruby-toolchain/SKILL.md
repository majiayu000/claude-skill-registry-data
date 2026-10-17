---
name: ruby-toolchain
description: Use when installing, selecting, inspecting, or troubleshooting the Ruby runtime, RubyGems, Bundler, gem executables, PATH, native extensions, and local Ruby development tooling before application work.
license: MIT
---

# Ruby Toolchain

## Purpose

Establish a reproducible Ruby execution environment before changing application code.

Core flow:

inspect repository
-> resolve required runtime/toolchain
-> verify executable provenance
-> install/select the smallest compatible toolchain
-> verify RubyGems/Bundler
-> verify dependencies
-> diagnose native-extension/platform failures
-> record evidence

## Activate when

- installing or selecting Ruby;
- checking `ruby --version`, RubyGems, or Bundler;
- choosing between mise, rbenv, RVM, system Ruby, or another repository-supported manager;
- installing gems globally or into an application bundle;
- running `bundle install`, `bundle exec`, `bundle check`, or `bundle config`;
- debugging PATH, executable, GEM_HOME/GEM_PATH, or Bundler provenance issues;
- compiling or diagnosing native gem extensions;
- bootstrapping a workstation/container before Rails work.

Do not activate for Ruby language semantics when the toolchain is already known and healthy; use `ruby-core`.

## Repository inspection

Inspect, in order:

1. `.ruby-version`, `.tool-versions`, `mise.toml`, or another explicit tool-version file;
2. Gemfile and Gemfile.lock;
3. gemspec `required_ruby_version`;
4. Gemfile Ruby/Bundler constraints;
5. CI matrices;
6. Docker/container and deployment runtime declarations;
7. existing project scripts and documented setup commands.

Separate minimum requirements, supported matrices, lockfile resolution, and the currently executing runtime.

## Runtime verification

Use concrete commands:

```bash
ruby --version
gem --version
bundle --version
gem env
bundle env
bundle check
```

For Rails projects also run:

```bash
bundle exec rails --version
```

Prefer project-local executables through `bundle exec` or binstubs when a project bundle exists.

Never report a runtime as selected merely because a version manager configuration exists; execute the interpreter and record the observed version.

## Installation and selection

Use the repository's existing version manager when one exists.

When no manager is prescribed, choose a documented, reproducible manager appropriate to the environment rather than silently replacing system tooling.

Do not install multiple Ruby versions until the supported version matrix or compatibility evidence requires them.

Verify after switching:

```bash
ruby --version
gem env home
bundle --version
```

## Bundler and dependencies

Treat Gemfile as dependency intent and Gemfile.lock as the concrete resolution where present.

Prefer:

```bash
bundle install
bundle check
bundle exec <command>
bundle add <gem>
bundle update <gem>
```

Do not use a global gem executable when the application bundle provides the project version.

Do not delete or regenerate Gemfile.lock casually.

Commit `Gemfile.lock` so CI, deployment, and every developer install the same resolved versions. Install against it rather than re-resolving it:

```bash
bundle config set --local frozen true   # BUNDLE_FROZEN=true
bundle install
```

`bundle config set frozen true` refuses to change the lockfile, so a `Gemfile` edit without a matching lockfile entry fails instead of silently resolving new versions. `bundle config set deployment true` (`BUNDLE_DEPLOYMENT`) additionally installs into `vendor/bundle` and implies frozen.

Never run `bundle update` in CI: it re-resolves the dependency tree and rewrites `Gemfile.lock`, so the build tests a version set nothing else has.

## RubyGems installation

For a standalone tool or explicitly requested global gem, inspect its version and installation target before:

```bash
gem install GEM_NAME
```

For application dependencies, prefer the Gemfile/Bundler path instead of global installation.

For native extensions, distinguish the Ruby gem from its system-library/compiler prerequisites and surface build flags explicitly.

## Native extension diagnosis

When installation fails:

```text
Ruby engine/version
-> gem version/platform
-> compiler/toolchain
-> system library/header
-> build flags
-> Bundler resolution
```

Capture the first concrete compiler/library error. Do not paper over it with retries or a different gem version without compatibility evidence.

Use platform-specific build configuration only when the dependency documents it or repository conventions require it.

## PATH and executable provenance

Check:

```bash
command -v ruby
command -v gem
command -v bundle
ruby -e 'puts RbConfig.ruby'
gem env
```

If ruby, gem, and bundle originate from different installations, stop and reconcile the toolchain before changing application dependencies.

## Reproducibility

A healthy setup should make the following unambiguous:

- Ruby engine and version;
- RubyGems version when relevant;
- Bundler version/lock requirement;
- dependency lockfile;
- executable source;
- native build prerequisites where applicable.

Document machine-specific exceptions rather than encoding them into application code.

## Anti-patterns

- changing .ruby-version merely to make one dependency install;
- running `gem install` for an application dependency that belongs in the bundle;
- mixing system Ruby and version-manager Ruby;
- using global Bundler/Rails executables against a project bundle;
- deleting Gemfile.lock to resolve ordinary dependency conflicts;
- running `bundle update` in CI, so each build resolves a version set nothing else has;
- hiding native-extension compiler errors behind repeated installation attempts;
- declaring compatibility from configuration without executing the runtime.

## Agent review checklist

- [ ] repository runtime declarations inspected
- [ ] Ruby engine/version observed
- [ ] RubyGems provenance checked
- [ ] Bundler provenance/version checked
- [ ] lockfile requirements separated from local runtime
- [ ] CI/deployment install mode observed (`frozen`, `deployment`, or neither)
- [ ] application dependencies installed through Bundler
- [ ] native-extension prerequisites identified when relevant
- [ ] executable provenance is consistent
- [ ] toolchain evidence recorded

## Verification

For a project bootstrap, run the project's documented setup and then:

```bash
ruby --version
gem --version
bundle --version
bundle check
bundle exec ruby -e 'puts RUBY_VERSION'
```

For Rails:

```bash
bundle exec rails --version
```

Report actual command results. If a command was not run, do not mark it verified.

## Source foundation

- Ruby documentation: https://www.ruby-lang.org/en/documentation/
- RubyGems command reference: https://guides.rubygems.org/command-reference/
- Bundler command reference: https://guides.rubygems.org/command-reference/bundle/
- Repository runtime evidence takes precedence over generic version assumptions.
