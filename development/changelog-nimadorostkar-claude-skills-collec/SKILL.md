---
name: changelog
description: Use when writing a changelog or release notes. Covers what belongs in one, writing for users rather than for git, semantic versioning, and documenting breaking changes so nobody is surprised.
metadata:
  category: writing
  version: 1.0.0
  tags: [changelog, release-notes, versioning, communication]
---

# Changelog

## Purpose

Tell users what changed and what they must do about it. A changelog is not a git log; it is a communication with people who have built something on your software.

## When to Use

- Writing release notes.
- Maintaining a CHANGELOG file.
- Announcing a breaking change.
- Deciding a version number.

## Capabilities

- Changelog structure and categorization.
- Writing for users rather than for contributors.
- Semantic versioning.
- Breaking-change communication and migration guidance.

## Inputs

- The commits, pull requests, or issues in the release.
- Who uses the software and what they have built on it.
- Whether anything breaks.

## Outputs

- A changelog entry organized by impact.
- A version number that reflects what changed.
- Migration instructions for anything that breaks.

## Workflow

1. **Group by what it means to the user** — Added, changed, deprecated, removed, fixed, security. Not by component, and certainly not by commit.
2. **Lead with the breaking changes** — They are what the reader is looking for. Bury them and someone's deployment fails.
3. **Write in terms of the user's experience** — "Exports now include line items", not "refactored `ExportSerializer` to include `LineItemMixin`".
4. **Version honestly** — A breaking change is a major version, however small it is. Renaming a public field is breaking, even if it felt like a typo fix.
5. **Give the migration, not just the warning** — "This is removed" is a problem. "This is removed; use X instead, like this:" is a solution.
6. **Skip the noise** — Internal refactors, dependency bumps with no behavioral effect, and CI changes do not belong in a user-facing changelog.

## Best Practices

- The reader of a changelog has one question: "will this break my build, and what do I have to change?" Answer it first.
- A commit log is not a changelog. `fix: handle nil case in parser` means nothing to a user; "Fixed a crash when parsing an empty configuration file" does.
- Any change to a public interface — a field name, a default value, an error type, a status code — is breaking. Version it accordingly, whatever it cost you to make.
- A deprecation needs a timeline and a replacement. "Deprecated" with neither is an announcement that something will break, eventually, with no notice.
- Link to the pull request or issue for detail. Keep the entry itself short.
- Date every release. "Unreleased" at the top, dated on release.

## Examples

**A changelog entry that answers the reader's question:**

```markdown
## [3.0.0] — 2026-07-14

### Breaking changes

- **`RateLimiter.check()` now returns `LimitResult` instead of `bool`.**
  The boolean gave no way to communicate the remaining quota or the reset time,
  both of which are needed to set `Retry-After` correctly.

      # Before
      if limiter.check(key):
          ...

      # After
      result = limiter.check(key)
      if result.allowed:
          ...
      # result.remaining, result.reset_at are now available

- **Removed `RateLimiter.reset_all()`.** It was unsafe in production: it flushed
  the entire Redis keyspace, not only the rate-limit keys. Use
  `reset(key=...)` for a single key, or `reset(prefix=...)` for a namespace.

- **Minimum Redis version is now 7.0** (was 6.2). Required for the atomic
  `SET ... IFEQ` used by the new sliding-window implementation.

### Added

- Sliding-window algorithm, in addition to token bucket. See
  [choosing an algorithm](docs/explanation/algorithms.md).
- `Retry-After` and `X-RateLimit-*` headers are now set automatically on 429s.

### Fixed

- Requests behind a proxy were all attributed to the proxy's IP, so a single
  limit applied to every user. `trust_proxy=True` now reads `X-Forwarded-For`
  correctly. ([#412](https://github.com/example/rateguard/issues/412))

### Deprecated

- `limit(rate="20/minute")` string syntax. Use `limit(Rate(20, per=Minute))`.
  The string form will be removed in 4.0 (planned Q1 2027).
```

**Versioning honestly:**

```text
Renamed a public field from `retry_after` to `retryAfter` to match the rest
of the API.

That is a MAJOR version. It is a one-character-per-word change, it took two
minutes, and it will break every consumer that reads the field. The size of
the diff has nothing to do with the size of the break.
```

## Notes

- The most damaging changelog omission is a breaking change that was not recognized as one. A renamed field, a changed default, a new required parameter, a stricter validation — each of these breaks consumers, and each is routinely shipped as a patch.
- "Keep a Changelog" is a widely used convention and worth following, mostly because readers already know where to look in it.
- Automated changelogs from conventional commits are better than nothing and worse than a written one. They produce accurate, unreadable lists of commit subjects.
