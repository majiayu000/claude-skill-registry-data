---
name: changelog-generator
description: Generate a categorized changelog from conventional-commit history for release notes.
when_to_use: Reach for this when producing release notes / a CHANGELOG from conventional commits (feat/fix/perf grouping, breaking-change detection). Standalone release-tooling skill; not related to git-town branch workflow or CI pipelines.
allowed-tools: Read, Bash, Grep, Glob
---

# Changelog Generator Skill

**Quick Reference** - Parse conventional commits and generate categorized changelog

## Mission

Generate changelog from conventional commits with categorization (Features, Bug Fixes, Breaking Changes, Performance, Documentation) and formatted output for release notes.

## Core Capabilities

- **Conventional Commit Parsing**: Extract type, scope, description, breaking changes
- **Change Categorization**: Group by type (feat, fix, perf, docs, refactor, test, chore)
- **Breaking Change Detection**: Identify BREAKING CHANGE footer and ! syntax
- **Semantic Version Integration**: Suggest version bump based on change types
- **Multi-Format Output**: Markdown, JSON, plain text formats

## Quick Start

```javascript
const { ChangelogGenerator } = require('./scripts/generate-changelog.js');

const generator = new ChangelogGenerator({
  fromTag: 'v2.0.0',
  toTag: 'HEAD',
  format: 'markdown'
});

const changelog = await generator.generate();
console.log(changelog);
```

## Conventional Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Supported Types**:
- `feat`: New feature → **Features** section
- `fix`: Bug fix → **Bug Fixes** section
- `perf`: Performance improvement → **Performance** section
- `docs`: Documentation → **Documentation** section
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Test additions/updates
- `chore`: Build/tooling changes

**Breaking Changes**:
- `BREAKING CHANGE:` footer → **Breaking Changes** section
- `!` after type/scope → **Breaking Changes** section

## Category Priority

1. **Breaking Changes** (highest impact)
2. **Features** (new functionality)
3. **Bug Fixes** (fixes)
4. **Performance** (optimizations)
5. **Documentation** (docs updates)

## Example Output

```markdown
## [2.1.0] - 2025-11-05

### Breaking Changes
- **auth**: Remove deprecated OAuth 1.0 support (c4f3b2a)

### Features
- **api**: Add rate limiting with Redis backend (a1b2c3d)
- **ui**: Implement dark mode toggle (e5f6g7h)

### Bug Fixes
- **database**: Fix connection pool exhaustion (i8j9k0l)
- **auth**: Resolve JWT token expiration edge case (m1n2o3p)

### Performance
- **api**: Optimize query performance with database indexes (q4r5s6t)
```

## Pass/Fail Criteria

**Pass**: Changelog generated with all changes categorized
- ✅ All conventional commits parsed correctly
- ✅ Changes grouped by category (breaking, features, fixes, etc.)
- ✅ Commit hashes included for traceability
- ✅ Execution time <60 seconds

**Fail**: Parsing or generation errors
- ❌ Non-conventional commits cannot be parsed
- ❌ Category detection fails
- ❌ Output format invalid
- ❌ Execution time exceeds 60 seconds

## Configuration

```yaml
# skills/changelog-generator/templates/changelog-config.yaml
fromTag: v2.0.0
toTag: HEAD
format: markdown  # or 'json', 'plain'
categories:
  - breaking
  - features
  - fixes
  - performance
  - documentation
excludeTypes:
  - style
  - test
  - chore
includeCommitHash: true
```

## Performance Target

**Target**: <60 seconds for 1000 commits
- Git log parsing: <20s
- Commit analysis: <20s
- Markdown generation: <20s

## Need More Detail?

**Load**: `skills/changelog-generator/REFERENCE.md` (~15KB)
- Advanced parsing patterns
- Custom category configuration
- Multi-repository support
- Integration examples
