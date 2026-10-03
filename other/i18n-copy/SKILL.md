---
name: i18n-copy
description: Add, change or translate user-visible copy in apps/console and packages/ui-web — which file a string belongs in, the en/de parity rule, the hard-coded-copy ratchet, and how to add a locale. Use whenever a task involves a label, heading, empty state, error message, button text, a translation, German, i18next, useCopy, locales/*.json, or a failing i18n test.
---

# Adding and translating copy

English is the **source of truth**. Every key exists in `apps/console/locales/en/<ns>.json` first;
`de` is a translation of it. Never a key that exists only in `de`.

Contract and reasoning: `docs/knowledge/i18n.md` and ADR 0017.

## Where does this string go?

| The string is...                                           | Put it in                                                                 |
| ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Anything a console **screen** decides                      | `apps/console/locales/{en,de}/<ns>.json`, used via `t('…')`               |
| A **`dashboards.yaml`** panel title/subtitle/rowLabel/unit | The `dashboards` namespace — the YAML carries the **key**                 |
| A word a Typst **template** prints on its own behalf       | The `reports` namespace → `report.labels`                                 |
| Something a `packages/ui-web` **section** displays         | A **prop**, passed in from the console                                    |
| A string baked into a `ui-web` **primitive's behaviour**   | `useCopy()` (`packages/ui-web/src/lib/copy.tsx`), with an English default |

Namespaces are one per **area**: `common`, `nav`, `dashboards`, `admin`, `settings`, `auth`,
`reports`. Pick by area, not by screen — a screen's copy moves between containers, an area's does
not.

**`packages/ui-web` never calls `t()`.** It has no i18n runtime; Storybook and `apps/lci`/
`apps/authz-ui` render it with no app around it. There are exactly two mechanisms, and no third.

## The sequence

1. Add the key to `apps/console/locales/en/<ns>.json`.
2. Add the same key to `apps/console/locales/de/<ns>.json`. **Not optional** — the client ships only
   the active locale, so a missing `de` key renders the raw key at runtime.
3. Use it:
   - Server component / route handler: `const { t } = await getServerTranslation(locale, ns)` —
     bind the locale **per request**.
   - Client component: `useTranslation(ns)` from `apps/console/src/i18n/client.tsx`.
4. If you replaced a hard-coded string, **lower `REMAINING_HARDCODED_COPY`** in
   `apps/console/src/i18n-hardcoded-copy.test.ts` in the same commit.
5. Run the tests below.

## Rules that are correctness, not style

- **Plurals are i18next's** (`_one`/`_other`), never `count === 1 ? '' : 's'` in JSX. German
  pluralises on a different rule.
- **A module-level constant cannot be copy** — it resolves at import time, before any request has a
  locale. Return a **fact** instead (a number, a `{shown, total}`), or take the caller's `t`.
- **Counts and dates** go through `Intl` with the active locale (`useIntlLocale`).
- **Money keeps ONE currency.** USD in both languages. Only notation changes (DIN 5008:
  `$1 131.80` → `1.131,80 $`). Never swap the symbol — this console has no exchange rate.
- **Interpolation placeholders must be identical across locales.** The parity test enforces it.

## Adding a locale

1. Add the code to `LOCALES` in `apps/console/src/i18n/config.ts`.
2. Create `apps/console/locales/<code>/` with **all seven** namespace files.
3. Add the seven `import()` entries to `LOADERS` in `apps/console/src/i18n/resources.ts`. The table
   is explicit rather than a template literal, so a namespace with no file is a **`tsc` error**.
4. Add a case to `money.ts` if the notation differs — it is hand-rolled, not `Intl.NumberFormat`.
5. Add a story variant alongside `pages-stories/i18n-german.stories.tsx`.

## Verify

```sh
pnpm --filter console test -- i18n     # resources.test.ts + i18n-hardcoded-copy.test.ts
pnpm --filter console typecheck
pnpm --filter console build:web
pnpm --filter @lightbridge/ui-web test
```

Then look at the German story (`i18n-german.stories.tsx`) — German strings are longer and are what
break tight layouts. See the `console-story-verify` skill.

## Pitfalls

- **A visible raw key on a card means the `de` (or `en`) file is missing that key.** It is not a
  renderer bug.
- **`dashboards.yaml` holds keys, not prose.** Writing English into a title there ships English
  panel titles to a German session, and the parity test does not cover the YAML's own strings — the
  story does, by showing the key.
- **Raising `REMAINING_HARDCODED_COPY` fails the build.** That is the point. If you added a
  hard-coded string, translate it instead of bumping the number.
- **`budget-period-caption.ts` is deliberately still English** — it composes a sentence whose German
  wants a different clause ORDER. Do not half-translate it; take it whole
  ([#490](https://github.com/ADORSYS-GIS/converse-frontends/issues/490)).
- **Tests read English with no provider** (`apps/console/src/test/setup.ts`), so a test asserting a
  literal is simultaneously asserting the key exists — do not "fix" such a test by hard-coding.
