---
name: wengz-notifications-locale
description: Adds or fixes Wengz email, in-app, or SSE notifications and locale handling. Use when editing src/lib/notifications, user-locale, cron notify paths, or when Arabic/English copy is wrong for recipients.
---

# Wengz notifications and locale

## Prerequisites

- `docs/ADVANCED_TECHNICAL.md` § Internationalization + recipient notify locale
- `docs/ADVANCED_BUSINESS.md` § Notifications
- Code: `src/lib/notifications/index.ts`, `src/lib/user-locale.ts`, `src/lib/error-handler.ts`

## Rules

1. **Recipient wins** — Single-user `notify*` helpers must call `localeForUser(userId)` / `getPreferredLocaleForUser`. Never pass staff `ctx.locale` as the client/provider language.
2. **Staff fan-out** — `notifyStaffByRoles` builds once per locale group from each admin’s `preferredLocale`.
3. **Account emails by address** — `sendAccountApprovedEmail` / `Rejected` resolve locale via email → user row.
4. **UI toasts** — Client components: `useTranslations` + `showError`/`showSuccess` from `@/lib/error-handler` with `t`.
5. **Both languages** — New `notifications.*` / `errors.*` keys in `messages/en.json` **and** `messages/ar.json`.
6. **Cron dedupe** — Stable `Notification.type` (e.g. `subscription_expiring`), not English title strings.
7. **SSE** — Prefer `sseI18n` keys when the client can re-translate; still persist a sensible title/message for the feed.

## Adding a notification

1. Add translation keys (en + ar).
2. Add email template helper in `src/lib/notifications/email.ts` if email is needed.
3. Export `notifyX` that resolves recipient locale first.
4. Call from router/lib/cron; do not inline HTML in routers.
5. Cover staff vs client/provider audience correctly (roles).

## Anti-patterns

- Using `ctx.locale` for “the other party” on approve/reject/status.
- Deduping cron notifies by translated title.
- Hardcoding English-only admin emails.
