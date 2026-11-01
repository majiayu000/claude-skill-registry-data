---
name: migration-traceability
description: Keep docs/migration/TRACEABILITY.md (the Flutter→React Native master matrix) accurate and check it against the code with scripts/trace-check.mjs, which scans apps/ and packages/ for `// Ported from:` headers. Use it whenever you add, move, split, finish or test a ported file, change a status, add a route/endpoint/test, want to know what's left to port or who owns a Dart file, or are asked for migration progress, a parity check or a traceability report.
---

# Migration traceability

`docs/migration/TRACEABILITY.md` is the single source of truth for *what each Flutter artefact became*. The code proves it with headers:
every ported file starts with `// Ported from: lib/<path>.dart` (tests: `// Ported from: test/<x>_test.dart`).

## The matrix

| Section | One row per | Key columns | Who updates |
|---|---|---|---|
| a. Files | hand-written Dart file under `lib/` (146; `lib/l10n/gen/*` listed once as replaced by JSON) | Dart path, lines, TS target(s), owner, status, notes | the owner, when a file is started / ported / tested |
| b. Features | row or bullet of Flutter `docs/FEATURES.md` | route(s), RN screen file(s), API, tests, status | screen owners, QA |
| c. API | repository method (82 distinct method + path pairs) | method, path, Dart method, TS method, hook, screens | API owner (repos), App-Architecture (hooks) |
| d. Firebase | Auth / Firestore / Storage / FCM area and FCM message type | Dart source, RN service file, tap routing | Native owner |
| e. Tests | Dart test file (36) | test / testWidgets counts, Jest target(s), status | QA and owners |
| f. Routes | route string (48) | RN screen, navigator, member-only, deep link | App-Architecture |
| g. Gotchas | finding | — | anyone who finds one |

Statuses: `pending` → `in-progress` → `ported` (code + header exist) → `tested` (parity tests green) → `done` (reviewed by QA). `n/a`
needs a reason in the notes.

## When you change code

1. **Starting a file:** set its §a row to `in-progress`.
2. **Adding the TS file:** first line `// Ported from: lib/<path>.dart`. Several sources merged → list them all
   (`// Ported from: lib/a.dart, lib/b.dart`); `{a,b}` groups are allowed. Barrels (`index.ts`) and globs aren't checked.
3. **Target differs from the plan** (another file name, an extra split, a different package): edit the TS target cell so it lists the
   real paths (`<br>` between paths, or `dir/{A,B}.tsx`). The matrix must describe reality, not the plan.
4. **Finished:** status `ported`; after the ported tests pass, `tested`. Mention behaviour changes, omissions and follow-ups in the notes.
5. **New endpoint, route, test or feature found:** add a row to the right section (keep the numbering) and, for files, update the counts
   in the header paragraph.
6. **Run the check** (below) and fix what it reports for your rows before handing back.

Only edit rows you own, apart from adding a note. Don't touch `docs/migration/BUILD_AND_RELEASE.md`.

## trace-check.mjs

```bash
node .claude/skills/migration-traceability/scripts/trace-check.mjs            # full report
node .claude/skills/migration-traceability/scripts/trace-check.mjs --owner API --summary
node .claude/skills/migration-traceability/scripts/trace-check.mjs --json     # for tooling
node .claude/skills/migration-traceability/scripts/trace-check.mjs --strict   # exit 1 on mismatches (CI / end of phase)
```

It parses §a and §e, scans `apps/` and `packages/` (skipping `node_modules`, `android`, `ios`, build output) for headers in the first 15
lines, and, when the Flutter checkout is available (`$FLUTTER_SRC`, `--flutter`, or the path in `CLAUDE.md`), lists Dart files missing from
the matrix. Report sections:

| # | Meaning | What to do |
|---|---|---|
| 1 | Dart files with no TS counterpart yet | Expected while porting; it's the to-do list, grouped by owner. |
| 2 | Header names a Dart file that isn't in the matrix | Typo in the header (relative path, missing `lib/`), or add the row. |
| 3 | TS file has a header but isn't listed as a target of that row | Add the real path to the row's targets (or fix the header). |
| 4 | Row is `ported`/`tested`/`done` but a listed target file doesn't exist | Fix the path or the status. |
| 5 | Row is still `pending`/`in-progress` but ported files exist | Update the status. |
| 6 | Dart file in the Flutter checkout isn't in the matrix | Add a row (generated l10n and fixtures are excluded). |
| — | Not checked: barrels, globs, generated l10n, sources outside `lib/`/`test/` | Informational. |

`--strict` fails on 2–6 (not 1). Run it before you report back, and QA runs it at the end of each phase.

## Answering progress questions

- "What's left for <owner>?" → `--owner "<Owner>"`, section 1.
- "Is <file> done?" → its §a row status + whether a header exists (`grep -rn "Ported from: lib/<path>" apps packages`).
- "Which screens call <endpoint>?" → §c. "Which tests cover <screen>?" → §b / §e.
- Phase summary → `docs/migration/STATUS.md` (update its board when a scope changes state).
