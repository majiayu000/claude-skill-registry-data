---
name: swap-translations
description: Serve translations from somewhere other than the bundled JSON (a database, a translation service) so copy changes without a deploy. Use when the user wants editable copy, a CMS for strings, or translations loaded at runtime. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the translation source

- **Interface:** `MessageSource` (`load(locale): Promise<Messages>`) in
  `packages/i18n/src/index.ts`.
- **Today:** `bundledMessages`, the JSON in `packages/i18n/messages/`, type-checked
  against English. Changing copy needs a deploy.
- **Env:** none today.

## Swap

1. Implement `MessageSource` over the new store, e.g. a table
   `i18n.message(locale, key, value)` (db-change skill), cached in Redis and dropped on
   write. Validate loaded messages against English's shape and fall back to
   `bundledMessages` for missing keys, so a bad row never renders a raw key.
2. Wire it where messages are loaded:
   - Nest services: `I18nModule.forRoot({ source })` (`packages/nest-common/src/i18n.ts`),
     registered in `apps/api/src/app.module.ts` and `apps/notifications/src/app.module.ts`
     (everything that renders copy injects it with `@InjectI18n()`). Call
     `i18n.invalidate(locale)` on every replica when copy changes (a Redis pub/sub
     message).
   - apps/web: `bundledMessages.load` in `apps/web/src/i18n/request.ts`.
   - apps/mobile: `bundledMessages.load` in `apps/mobile/src/lib/i18n.tsx` (keep the
     bundle as the offline fallback).
3. New variables (the store's URL, cache TTL) in each service's `src/env.ts`,
   `.env.example` and `docs/environment.md`.

## Tests

`packages/i18n/src/index.test.ts` (loading, caching, invalidation, catalog completeness)
with a fake source; `packages/email/src/render.test.tsx` renders emails through a
translator; integration tests for the store in the owning service.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
