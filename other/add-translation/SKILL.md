---
name: add-translation
description: Add or change user-facing text (a UI string, email, push, SMS or error message), or add a new language. Use whenever a change shows new words to a user, or the user asks for another locale.
argument-hint: <key or locale code>
---

# Add a string or a locale

Every user-facing string is a key in `packages/i18n/messages/<locale>.json` (`en.json`
and `es.json` today). `.claude/rules/i18n.md` has the rules.

## A string

1. Pick the namespace (top-level key) the surface uses: `auth`, `settings`, `dashboard`,
   `email`, `notification`, `sms`, `errors`, `mobile`, … and put the key next to its
   siblings. Reuse `common.*` for shared words (Save, Cancel).
2. Add it to **every** catalog, at the same path, in the same change. Write real
   translations; if you can't, say so in the pull request rather than copying English.
3. ICU for anything variable: `{name}`, `{count, plural, one {# item} other {# items}}`.
   Never concatenate translated fragments. Arguments aren't type-checked (the catalog is
   imported as JSON), so pass exactly the ones the message names.
4. Use it: `useTranslations("<ns>")` (web client, and `use-intl` on mobile),
   `getTranslations` from `next-intl/server` (web server components), the translator in
   `apps/notifications` for emails, push and SMS. Dates, numbers and money through
   `useFormatter()` / `getFormatter()`.
5. Keys the code checks for: an error code needs `errors.<CODE>`; an event
   `workspace.audit.events.<domain>.<fact>.v<N>` (nested, like `todo.created.v1`); an API-key scope `workspace.apiKeys.scopes.<scope>`;
   a notification category `notificationSettings.categories.<name>`.

## A locale

1. Copy `packages/i18n/messages/en.json` to `<code>.json` and translate it.
2. Add the code to `locales` and to `catalogs` in `packages/i18n/src/index.ts` (the
   `satisfies` clause makes a missing key a type error).
3. Right-to-left: add it to `RTL` in `apps/web/src/app/layout.tsx`.
4. The language switcher (`apps/web/src/modules/shell/components/language-switcher.tsx`)
   and mobile settings list `locales`, so they pick it up.

## Done when

- `bun run check-types` passes (web keys are checked against English).
- `bun run --filter @repo/i18n test` passes (every catalog complete; codes, events,
  categories and scopes all have their keys).
- `bun run --filter @repo/email test` if an email changed.
- The `i18n-checker` agent reports nothing blocking.
