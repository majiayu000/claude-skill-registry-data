---
name: ruby-quality
description: Interpretive guidance for Ruby code quality using RuboCop (configurable) or StandardRB (zero-config). Use when linting Ruby files, configuring Ruby tools, troubleshooting lint errors, or understanding tool selection.
---

# Ruby Quality Skill

This skill teaches how to apply Ruby linting and formatting tools effectively using mr-sparkle's tool selection system. It provides guidance on what the tools do, when each tool group is used, and how our configuration balances configurability with zero-config simplicity.

## Official Documentation

Claude knows how to use RuboCop and StandardRB. Fetch these docs only when you need:

- Specific cop (rule) codes or error messages you don't recognize
- Advanced configuration options
- Recent feature changes

**Reference URLs:**

- **<https://docs.rubocop.org/rubocop/>** - RuboCop cops and configuration
- **<https://github.com/standardrb/standard>** - StandardRB philosophy and usage

## Core Understanding

### Tool Selection Philosophy

**Key principle:** Prefer zero-config tooling (StandardRB) when project has it configured; fall back to configurable tool (RuboCop) when configured; default to StandardRB if no configuration exists.

**What this means:**

- **StandardRB preferred** - Zero-config, opinionated, removes decision fatigue
- **Project config wins** - Respects existing project tooling choices
- **Smart fallback** - Uses RuboCop if project has it configured
- **Zero-config default** - Falls back to StandardRB with sensible defaults

**Decision test:** Does the project have explicit tool configuration? Use configured tools. Otherwise use StandardRB.

### How Tool Selection Works

The linting system uses **group-based priority selection** for Ruby files:

```text
Priority 1: standardrb (if project has standard config)
    ↓
Priority 2: rubocop (if project has rubocop config)
    ↓
Fallback: standardrb (with default config)
```

**Detection logic:**

1. Find project root (`Gemfile`, `.git`, or other markers)
2. Check for StandardRB configuration (first group)
3. Check for RuboCop configuration (second group)
4. If no config found, use StandardRB with defaults

**Tool in winning group runs** (only one tool needed for Ruby).

## StandardRB: Zero-Config Tool (Official Specification)

**From official docs:**

- **Purpose:** Ruby style guide, linter, and formatter with zero configuration
- **Philosophy:** "No configuration, just use it"
- **Based on:** RuboCop engine with curated rule set
- **Capabilities:** Linting + auto-fixing in a single tool
- **Commands:** `standardrb` (check), `standardrb --fix` (auto-correct)

**Configuration locations:**

- `.standard.yml` (optional overrides, but goes against philosophy)
- Generally: no config needed or wanted

See [standardrb.md](./standardrb.md) for detailed overview.

## StandardRB: Zero-Config Tool (Best Practices)

**When StandardRB shines:**

- ✅ New projects (no legacy style preferences)
- ✅ Want to eliminate bikeshedding about style
- ✅ Prefer "just make it consistent" over customization
- ✅ Teams that value simplicity
- ✅ Want fast onboarding (no config decisions)

**Philosophy:**

StandardRB removes decision fatigue by providing a curated, opinionated rule set. You don't configure it; you use it. This is intentional.

**Basic usage:**

```bash
# Check for issues
standardrb

# Auto-fix issues
standardrb --fix

# Check specific files
standardrb app/models/**/*.rb
```

**Rare configuration** (discouraged but possible):

```yaml
# .standard.yml - only if absolutely necessary
ignore:
  - 'vendor/**/*'
  - 'db/schema.rb'
```

See `configs/standard.yml` for minimal example and `standardrb.md` for philosophy details.

## RuboCop: Configurable Tool (Official Specification)

**From official docs:**

- **Purpose:** Ruby static code analyzer and formatter
- **Philosophy:** Highly configurable, community-driven style enforcement
- **Capabilities:** 500+ cops (rules) covering style, performance, security
- **Commands:** `rubocop` (check), `rubocop -a` (safe auto-correct), `rubocop -A` (all auto-correct)

**Configuration locations:**

- `.rubocop.yml` (standard config file)
- Can inherit from shared configs (`rubocop-rails`, `rubocop-rspec`, etc.)

See [rubocop.md](./rubocop.md) for detailed overview.

## RuboCop: Configurable Tool (Best Practices)

**When RuboCop shines:**

- ✅ Existing projects with established style preferences
- ✅ Teams with specific coding standards
- ✅ Need fine-grained control over rules
- ✅ Want to use community extensions (rubocop-rails, rubocop-rspec, etc.)
- ✅ Projects that haven't migrated to StandardRB

**Philosophy:**

RuboCop is powerful and flexible. You configure exactly which cops to enable, at what severity, with what parameters. This is ideal when you have strong opinions or legacy codebases.

**Basic usage:**

```bash
# Check for issues
rubocop

# Auto-fix safe issues
rubocop -a

# Auto-fix all issues (use with caution)
rubocop -A

# Check specific files
rubocop app/models/**/*.rb
```

**Common configuration pattern:**

```yaml
# .rubocop.yml
AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable

Style/StringLiterals:
  EnforcedStyle: single_quotes

Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'
```

See `configs/rubocop.yml` for sensible defaults and `rubocop.md` for configuration guidance.

## Tool Selection in Practice (Best Practices)

### Scenario 1: New project, no config

```bash
$ lint.py file.rb
# Runs: standardrb --fix
# Uses: StandardRB defaults (zero config)
```

### Scenario 2: Project with StandardRB config

```bash
# Project has .standard.yml or uses 'standard' gem
$ lint.py file.rb
# Runs: standardrb --fix
# Uses: project's .standard.yml (if exists)
```

### Scenario 3: Project with RuboCop config

```bash
# Project has .rubocop.yml
$ lint.py file.rb
# Runs: rubocop -a
# Uses: project's .rubocop.yml config
```

### Scenario 4: Mixed config (StandardRB wins)

```bash
# Project has both .standard.yml and .rubocop.yml
$ lint.py file.rb
# Runs: standardrb only (first group with config wins)
```

## Common Pitfalls

### Pitfall #1: Over-Configuring StandardRB

**Problem:** Trying to customize StandardRB extensively.

```yaml
# ❌ Fighting StandardRB's philosophy
# .standard.yml
ignore:
  - 'app/**/*'
  - 'lib/**/*'
```

**Why it fails:** If you need this much customization, you should use RuboCop instead. StandardRB's value is zero-config consistency.

**Better:** Either accept StandardRB's defaults or switch to RuboCop for full control.

### Pitfall #2: Using `rubocop -A` Without Review

**Problem:** Auto-correcting all issues without understanding changes.

**Why it fails:** `-A` (aggressive auto-correct) can make unsafe changes. Some fixes need human review.

**Better:**

```bash
# Safe auto-correct first
rubocop -a

# Review remaining issues
rubocop

# Only use -A for specific safe cops if needed
rubocop -A --only Style/StringLiterals
```

### Pitfall #3: Not Using Community Extensions

**Problem:** Reinventing rules that exist in community gems.

```yaml
# ❌ Custom rules for Rails-specific issues
# .rubocop.yml
Style/MyCustomRailsRule:
  Enabled: true
```

**Why it fails:** Community gems like `rubocop-rails` already have comprehensive Rails-specific cops.

**Better:**

```ruby
# Gemfile
gem 'rubocop-rails', require: false
```

```yaml
# .rubocop.yml
require:
  - rubocop-rails

# Now use built-in Rails cops
Rails/Validation:
  Enabled: true
```

### Pitfall #4: Disabling Too Many Cops

**Problem:** Disabling cops because they're "annoying."

```yaml
# ❌ Over-disabling
AllCops:
  DisabledByDefault: true

Style/StringLiterals:
  Enabled: false
Metrics/MethodLength:
  Enabled: false
Layout/LineLength:
  Enabled: false
```

**Why it fails:** Defeats the purpose of linting. Rules exist for good reasons.

**Better:** Understand why rules trigger, fix the code, or selectively disable with inline comments:

```ruby
# Selective disable when truly needed
def legacy_method # rubocop:disable Metrics/MethodLength
  # ... complex legacy code that can't be refactored yet
end
```

### Pitfall #5: Ignoring `.rubocop_todo.yml`

**Problem:** Committing a massive `.rubocop_todo.yml` and forgetting about it.

**Why it fails:** Todo file is meant to be temporary. It lets you enable RuboCop gradually but shouldn't be permanent.

**Better:**

```bash
# Generate todo file for existing codebase
rubocop --auto-gen-config

# Then incrementally fix issues
# After fixing some cops, regenerate:
rubocop --auto-gen-config --exclude-limit 0

# Goal: Eventually delete .rubocop_todo.yml entirely
```

## Automatic Hook Behavior

The mr-sparkle plugin's linting hook:

1. Triggers after Write and Edit operations
2. Detects Ruby files (`.rb`, `.rake`, `Rakefile`, `Gemfile`)
3. Runs selected tool automatically (standardrb OR rubocop)
4. Applies auto-fixes where possible
5. Reports unfixable issues (non-blocking)
6. Silently skips if tools not installed

**What this means:** Most formatting issues auto-fix on save. Pay attention to reported unfixable issues.

## Quality Checklist

**Before finalizing Ruby code:**

**Auto-fixable (tools handle):**

- ✓ String quote style consistency
- ✓ Indentation and spacing
- ✓ Line length and wrapping
- ✓ Trailing whitespace
- ✓ Method spacing
- ✓ Hash syntax (old vs new)

**Manual attention required:**

- ✓ Method complexity
- ✓ Undefined variables
- ✓ Security issues
- ✓ Performance anti-patterns
- ✓ Naming conventions
- ✓ Documentation completeness

## CLI Tool Usage

The universal linting script handles Ruby files automatically:

```bash
# Lint Ruby file (applies fixes)
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.rb

# JSON output for programmatic use
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.rb --format json
```

**Exit codes:**

- `0` - Clean or successfully fixed
- `1` - Lint errors found (non-blocking)
- `2` - Tool execution error

See `linting` skill for complete CLI documentation.

## Reference Documentation

**Detailed guides** (loaded on-demand for progressive disclosure):

- [rubocop.md](./rubocop.md) - RuboCop overview, philosophy, key features
- [standardrb.md](./standardrb.md) - StandardRB overview, zero-config philosophy
- `configs/rubocop.yml` - Sensible default RuboCop configuration
- `configs/standard.yml` - Minimal StandardRB configuration example

**Official documentation to fetch:**

- <https://docs.rubocop.org/rubocop/> - RuboCop documentation and cops reference
- <https://github.com/standardrb/standard> - StandardRB documentation
- <https://rubystyle.guide/> - Ruby Style Guide (RuboCop's basis)

**Remember:** This skill documents mr-sparkle's tool selection logic for Ruby. Fetch official docs when you need specific cop definitions or configuration syntax you're unsure about.
