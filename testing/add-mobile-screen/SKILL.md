---
name: add-mobile-screen
description: Add a screen, tab or component to the Expo app (apps/mobile). Use when the user wants something new in the mobile app, or a web feature brought to mobile.
argument-hint: <screen name>
---

# Add a mobile screen

Same API client and translations as the web app, its own primitives.
`.claude/rules/mobile.md` and `apps/mobile/CLAUDE.md` have the rules.

1. **Data.** Hooks from `@repo/client/api/<area>/<operation>`, the same the web uses. A
   missing one is added in `packages/client` (the add-feature skill), never a local
   `fetch` or a hand-written query key.
2. **Route.** A file in `apps/mobile/src/app/`: `(app)/<name>.tsx` for signed-in screens
   (a new tab also needs a `Tabs.Screen` in `apps/mobile/src/app/(app)/_layout.tsx`),
   `(auth)/<name>.tsx` for sign-in flows. Wrap content in `Screen`
   (`src/components/screen.tsx`), as `(app)/settings.tsx` does.
3. **UI.** Primitives from `src/components/ui/` (Button, Card, Input, Text, …). A missing
   one: copy it from the React Native Reusables registry
   (`https://reactnativereusables.com/r/uniwind/<name>.json`; its CLI hangs without a
   terminal) and install what it lists with `bunx expo install` in `apps/mobile`.
4. **Text.** `useTranslations("<namespace>")` from `use-intl`, keys in every
   `packages/i18n/messages/*.json`, usually under `mobile.*`. They aren't type-checked
   here: confirm each key exists in `en.json`. Errors through `useApiErrorMessage()`
   from `@repo/client`, shared with web.
5. **Native.** A new permission, config plugin or native dependency changes
   `app.config.ts` and needs a store build; say so in the pull request.
6. **Tests.** Logic in `src/lib` or a hook gets a Jest test beside it
   (`bun run --filter @repo/mobile test`). The screen gets a case in
   `apps/mobile/e2e/app.spec.ts` (Playwright on the web build). Anything only a device
   shows (permissions, OS links, restarts) gets a Maestro flow in `apps/mobile/maestro/`.

## Done when

- `bun run lint`, `bun run --filter @repo/mobile check-types` and
  `bun run --filter @repo/mobile test` pass.
- `bun run test:e2e --app mobile` passes (stop `bun dev` first).
- The `frontend-reviewer` and `i18n-checker` agents report nothing blocking.
