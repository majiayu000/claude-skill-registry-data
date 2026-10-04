---
name: conventional-commits
description: Turn a staged diff summary into this team's Conventional Commit message.
disable-model-invocation: true
---

# Conventional Commits

Convert the staged diff summary into one commit message. Emit the message verbatim, nothing else.

## Format

```
<type>(<scope>)[!]: <subject>

- <bullet per notable change, when 2+ files changed>

BREAKING CHANGE: <impact> (only for breaking changes)
```

## Team conventions

1. Scope is the top-level directory of the dominant change (`api`, `web`, `infra`). Dependency
   manifest bumps (`package.json` + lockfile) use type `build` and scope `deps`.
2. Subject: imperative mood, lowercase start, no trailing period.
3. Breaking changes carry BOTH the `!` marker and a `BREAKING CHANGE:` footer.
4. Multi-file changes get a body of `- ` bullets, one per notable change; single-file changes
   get subject only.
5. Reverts: `revert: <original first line>`, body starts `This reverts commit <sha>.`, then bullets.

## Example

Input: api/routes/exports.ts (new) + api/services/export-service.ts (new)

```
feat(api): add streaming CSV account export endpoint

- add GET /v1/exports streaming account data as CSV
- build the CSV stream with cursor pagination in export-service
```
