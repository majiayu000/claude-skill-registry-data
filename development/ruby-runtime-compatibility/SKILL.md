---
name: ruby-runtime-compatibility
description: Use when determining or enforcing Ruby, Rails, Bundler, and runtime-version compatibility before implementing, upgrading, linting, debugging, or reviewing Ruby/Rails code.
license: MIT
---

# Ruby Runtime Compatibility

## Purpose
Establish the actual Ruby/Rails/Bundler runtime contract before using version-sensitive APIs, gems, framework features, or tooling.

This skill separates:

- **Ruby engine** — CRuby, JRuby, TruffleRuby, or another implementation;
- **resolved runtime** — a concrete version established by repository evidence;
- **declared constraint** — a version/range the project permits;
- **supported matrix** — versions exercised by CI or tooling;
- **tooling target** — versions configured for linters/type checkers/formatters;
- **conflict** — repository evidence that does not agree.

Do not silently convert a constraint into a concrete runtime version.

## Activate when
- adding or changing Ruby/Rails code with version-sensitive behavior
- upgrading Ruby, Rails, Bundler, or core dependencies
- adding/updating gems or RuboCop plugins
- debugging environment-specific failures
- reviewing compatibility or deprecation issues
- choosing Rails APIs or configuration options
- generating a project profile for an AI coding agent

## Repository inspection
Inspect these sources in descending specificity:
1. `Gemfile.lock`
2. `.ruby-version`
3. `Gemfile`
4. gemspec files
5. `.tool-versions`
6. `.mise.toml` / `mise.toml`
7. Dockerfiles/container build configuration
8. CI workflow version matrices
9. deployment/runtime configuration
10. project documentation only when executable/configuration evidence is absent

Record the source and exact evidence for every resolved value.

## Resolution rules
### Ruby

Resolve the Ruby implementation separately from the version. A version such as 3.3 can behave differently across CRuby/JRuby/TruffleRuby, and native extensions may impose engine/platform constraints.
Prefer:
```text
Gemfile.lock RUBY VERSION
→ .ruby-version
→ Gemfile ruby directive
→ gemspec required_ruby_version
→ tool-version files
→ CI/deployment declarations
```

A CI matrix may describe supported versions without identifying the local runtime. Preserve it as a support range/list.

### Rails
Prefer:
```text
Gemfile.lock exact rails version
→ Gemfile rails constraint
→ explicit framework configuration/documentation
```

`Gemfile` constraints such as `~> 7.2` are constraints, not proof that Rails 7.2.x is actually installed.

### Bundler
Prefer:
```text
Gemfile.lock BUNDLED WITH
→ environment/tooling declaration
```

Do not assume the lockfile Bundler version is the runtime's currently executing Bundler version; it is lockfile requirement/evidence.

### Ruby compatibility across dependencies
When changing a gem:
- inspect its declared Ruby requirement;
- inspect Rails compatibility;
- inspect adjacent framework plugins/extensions;
- inspect lockfile resolution;
- check CI-supported Ruby versions;
- identify deprecations/removals between the current and target runtime.

Never infer compatibility merely because a gem can be installed in an unrelated environment.

## Conflict handling
If repository evidence conflicts:
```text
collect evidence
→ identify stronger source
→ report conflict
→ do not invent a winner
→ ask for clarification when implementation depends on it
```

Example:
```text
.ruby-version = 3.3.6
Gemfile.lock RUBY VERSION = 3.2.4

Result:
ruby.resolved = unknown
ruby.conflict = true
```

Do not choose one value merely because its source looks newer.

## Compatibility classification
For a requested feature/API/tool, classify the result as one of:
- `supported` — evidence establishes availability in the resolved runtime;
- `constrained` — project permits it but no concrete runtime is resolved;
- `unsupported` — project/runtime explicitly rules it out;
- `version_sensitive` — behavior/API differs across relevant versions;
- `unknown` — repository evidence is insufficient;
- `conflict` — authoritative repository sources disagree.

## Version-sensitive implementation procedure
```text
1. resolve runtime profile
2. identify API/framework feature
3. determine version boundary
4. compare project version with boundary
5. inspect local conventions/deprecations
6. implement compatible form
7. run focused tests
8. run version-sensitive verification/lint
9. inspect final diff
```

Do not use the newest API merely because it is available in current documentation.

## Upgrade procedure
```text
baseline
→ inventory dependencies
→ read release/deprecation notes
→ update compatibility constraints
→ update lockfile
→ run focused tests
→ run full tests
→ run RuboCop/security/dependency checks
→ inspect generated/application changes
→ document remaining deprecations
```

Treat major/minor framework upgrades as migration projects, not dependency-edit-only tasks.

## CI and deployment
CI matrices and deployment configurations are evidence of supported/runtime targets.

They must be distinguished from:
- the local developer runtime;
- the lockfile's resolved runtime;
- the minimum gem requirement.

If CI tests Ruby 3.2, 3.3, and 3.4, report a supported matrix rather than claiming one runtime is the runtime.

## Reference example

Version gates decide between APIs instead of rescue-ing NoMethodError; requirements state the supported floor.

```ruby
require "rubygems/version"

RUBY_FLOOR = Gem::Version.new("3.1")
raise "requires Ruby >= #{RUBY_FLOOR}" if Gem::Version.new(RUBY_VERSION) < RUBY_FLOOR

def filter_present(list)
  if RUBY_VERSION >= "3.4"          # targeted adoption of newer stdlib
    list.filter_map { |v| v unless v.empty? }
  else                              # documented fallback for the floor
    list.reject(&:empty?)
  end
end

result = filter_present(["a", "", "b"])
raise "filter broken" unless result == %w[a b]
puts "#{RUBY_VERSION}: #{result.inspect}"
```

## Agent review checklist
- [ ] Ruby engine resolved or explicitly marked unknown
- [ ] Ruby runtime resolved or explicitly marked unknown
- [ ] Rails runtime resolved or explicitly marked unknown
- [ ] Bundler requirement inspected
- [ ] version constraints separated from resolved versions
- [ ] CI/deployment support matrix inspected when relevant
- [ ] conflicting evidence surfaced
- [ ] version-sensitive API boundaries checked
- [ ] gem/plugin compatibility checked
- [ ] upgrade work treated as a migration when applicable
- [ ] focused tests run
- [ ] relevant lint/security/dependency checks run
- [ ] final compatibility assumptions documented

## Verification
Use the repository's configured tools first.

When available, verify:
```bash
ruby --version
bundle --version
bundle exec rails --version
bundle exec rubocop --version
```

For the repository-independent profile generator, use:
```bash
ruby bin/runtime-profile PATH
```

It must report evidence and conflicts rather than silently selecting a version.

Never claim compatibility has been established unless the relevant runtime/tool evidence was actually observed.

## Source foundation
This skill is repository-process guidance synthesized for AI coding agents. It intentionally does not hard-code a single Ruby or Rails version. Runtime truth comes from the target application's configuration, lockfile, CI, and deployment evidence.