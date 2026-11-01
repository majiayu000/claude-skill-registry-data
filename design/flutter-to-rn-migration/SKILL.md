---
name: flutter-to-rn-migration
description: End-to-end procedure for porting any Flutter/Dart file from the poc_vedaxl app into this React Native monorepo (models, repositories, services, state, widgets, screens, navigation, l10n). Use it whenever you start, continue or review the port of a `lib/**/*.dart` file, when you're asked "port X", "convert this Dart file", "where does <dart file> go", or when you need the Flutter→RN concept mapping (widgets, ChangeNotifier, FutureBuilder, Navigator, ThemeData, sheets, animations, CustomPainter, ARB). For a single screen use flutter-screen-to-rn; for models/repositories use dart-model-to-ts; for tests use flutter-test-to-jest.
---

# Flutter → React Native: porting one file

The goal is **parity**: same behaviour, same API calls, same copy and error codes, same edge cases, written as idiomatic React Native.
`CLAUDE.md` (repo root) has the layout, the stack and the Dart → TS mapping rules; they win over anything here.

- Flutter source (read-only): `$FLUTTER_SRC`, default
  `/private/tmp/claude-503/-Users-ayushk-React-Native-Projects-vidaXl-react-native/50b515c6-db3a-4680-82b7-a5636dffbc7d/scratchpad/src/flutter`
- Matrix: `docs/migration/TRACEABILITY.md` · Guide: `docs/migration/MIGRATION_GUIDE.md` · ADRs: `docs/migration/DECISIONS.md`

## Procedure

1. **Find the row.** Search `docs/migration/TRACEABILITY.md` §a for the Dart path. Note the target path(s), the owner, the notes, and the
   gotchas in §g. If you're not the owner, stop and report. If the row is missing, add it (see the `migration-traceability` skill).
   Set the status to `in-progress`.
2. **Read the Dart file completely**, plus the `lib/` files it imports that you don't know yet. List every public symbol
   (`grep -nE "^(class|enum|typedef|[A-Za-z<>?]+ [a-z]\w*\()" <file>`). Find its tests: `grep -ln "<file name>" $FLUTTER_SRC/test/*.dart`.
3. **Decide the split.** Use the matrix targets. Pure logic → `@vidaxl/core`; HTTP/parsing → `@vidaxl/api`; presentational →
   `@vidaxl/ui`; anything with state, navigation, queries or native modules → `apps/mobile`. Never import RN/React/Firebase/i18n into
   `@vidaxl/api` or `@vidaxl/core`.
4. **Port** using the mapping references:
   - Widgets and layout: [references/widget-mapping.md](references/widget-mapping.md)
   - ChangeNotifier / scopes / async: [references/state-mapping.md](references/state-mapping.md)
   - Firebase, FCM, local notifications, storage: [references/firebase-mapping.md](references/firebase-mapping.md)
   - ARB / `context.l10n` / `l10nNow()`: [references/l10n-mapping.md](references/l10n-mapping.md)
   - `AppNav.go`, routes, sheets, deep links: [references/navigation-mapping.md](references/navigation-mapping.md)
5. **Header.** The first line of every target file: `// Ported from: lib/<path>.dart` (one line per source when you merge files).
   Barrels (`index.ts`) and new glue files without a Dart source don't need one.
6. **Keep names.** Dart class/method/field names camelCased; files camelCase, components PascalCase; named exports.
   Keep the doc comments that explain API rules or backend quirks.
7. **Test.** Port the Dart tests covering the file (skill `flutter-test-to-jest`), keeping the same test names. Then run
   `npm run typecheck -w <workspace>` and `npm test -w <workspace>`.
8. **Re-read the Dart file** side by side with your TS once more: requests, omitted keys, defaults, error codes, every branch of
   `switch`, every `?? fallback`, every `if (!mounted) return`.
9. **Update the matrix row**: real target paths, status `ported` (or `tested` once its tests pass), and notes on anything changed or
   left out. Run `node .claude/skills/migration-traceability/scripts/trace-check.mjs --owner "<Owner>"` to check it.

## Parity checklist (the things that usually get lost)

- Request shape: method, path (`encodeURIComponent` on ids), query keys left out when null/empty, body keys left out when null
  (Dart `'key': ?value`), `auth: false` only on `/auth/signup` and `/health`.
- Tolerant parsing: Dart `fromJson` never throws; numbers may arrive as strings; lists may be missing.
- Copy: the same ARB key. Don't invent strings; if one is missing, add it to `en/nl/fr` and note it.
- Errors: `ApiError.code` values (`already_checked_in`, `max_too_low`, `discounts_not_combinable`…) and the screens' mapping functions.
- States: loading, error + "Try again", empty, needs sign-in, demo fallback (`LiveMode.demo | needsSignIn | live`).
- Side effects: cache invalidation (`GET /me`, `/home`, `/rewards` after point changes), toasts, reward wheel, push-token unregister
  before sign-out.
- Timers and lifecycle: countdowns, 10 s polling, app-resume refresh, cleanup on unmount.
- Accessibility: `Semantics` labels → `accessibilityLabel` / `accessibilityRole` / `accessibilityState`.
- Reduced motion (`MediaQuery.disableAnimationsOf`) → `useReduceMotion()` from `@vidaxl/ui`.

## Don'ts

- Don't install packages; report the need instead.
- Don't "fix" Flutter behaviour silently (e.g. the exact-match member gate). Port it, note it in the row, and raise it.
- Don't commit. The orchestrator commits each phase.
- Don't edit rows owned by other agents beyond adding a note, and don't edit `docs/migration/BUILD_AND_RELEASE.md`.
