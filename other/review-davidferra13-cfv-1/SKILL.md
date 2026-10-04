---
name: review
description: Code review on uncommitted changes before shipping. Quality gate between coding and /ship.
user-invocable: true
---

# Code Review

Review all uncommitted changes. This is the quality gate before `/ship`.

## 1. Gather Changes

```bash
git diff --stat
```

```bash
git diff
```

```bash
git diff --cached
```

```bash
git status --short
```

## 2. Review Checklist

For each changed file, check:

- [ ] **Security:** No hardcoded secrets, no SQL injection, no XSS, tenant scoping intact
- [ ] **Data safety:** No unguarded deletes, no silent failures returning zeros, try/catch on optimistic updates
- [ ] **Types:** No `any` casts, no `@ts-ignore` added, no `@ts-nocheck`
- [ ] **Zero Hallucination:** No success without confirmation, no hidden failures, no non-functional UI
- [ ] **Cache busting:** Mutations bust all related caches (`revalidateTag` for `unstable_cache`)
- [ ] **Auth:** Server actions have `requireChef()`/`requireAuth()`, tenant_id from session not input
- [ ] **Side effects:** Notifications/emails/logs wrapped in try/catch, non-blocking
- [ ] **Em dashes:** None introduced
- [ ] **OpenClaw in UI:** Not exposed in user-facing surfaces

## 3. Report Format

```
REVIEW - [X] files changed

CLEAN:    [files with no issues]
FLAGS:    [file:line - issue description] (one per line)
VERDICT:  [ship it / fix first]
```

If verdict is "fix first," list exact fixes needed. Keep terse.
