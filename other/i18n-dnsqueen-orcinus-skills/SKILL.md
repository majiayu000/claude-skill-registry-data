---
name: i18n
description: "Internationalize a project: language tags and negotiation, dates/times/time zones, numbers and currency, RTL layout, pluralization and ICU messages, collation, Unicode, and localization testing. Use when adding a language or locale, or when text, dates, numbers, or RTL layout must render correctly. Only invoke via the orcinus router."
license: MIT
user-invocable: false
---

# Internationalization (i18n)

Make a codebase correct outside a single locale. This skill audits and then implements internationalization across nine domains, each documented in a reference module under `references/`.

## The Scope Contract

The user may narrow the work by naming aspects, languages, or both. Parse the request before doing anything else.

| Request                                                | Languages in scope                        | Domains in scope                     |
| ------------------------------------------------------ | ----------------------------------------- | ------------------------------------ |
| `/i18n` (bare)                                         | Detect from the project; ask if ambiguous | All nine                             |
| `/i18n I want language just to be english and spanish` | `en`, `es` only                           | All nine                             |
| `/i18n only fix the date and time handling`            | Current set                               | `intl-date-and-time-format.md` only  |
| `/i18n add Arabic support`                             | Existing plus `ar`                        | All nine, with RTL and BiDi promoted |
| `/i18n audit only, change nothing`                     | Detect                                    | All nine, report without editing     |

Two rules govern a narrowed request:

1. **A narrowed language set narrows the configuration, not the correctness of the code.** If only `en` and `es` are requested, do not add RTL stylesheets or Arabic plural rules — but _do_ still use logical CSS properties, locale-aware formatting APIs, and ICU messages, because those cost nothing now and make the next language a configuration change rather than a rewrite.
2. **A narrowed domain set does not excuse breaking a sibling domain.** Adding date formatting while leaving hardcoded concatenated strings still produces broken output. Note the out-of-scope defects you observe, report them, and do not fix them unless the user widens the scope.

When the language set is ambiguous and the user did not name one, ask before implementing. Do not guess a target market.

## Phase 1 — Reconnaissance

Establish what exists before proposing anything. Never recommend a library the project already uses, and never migrate an existing i18n library without the user asking.

**Detect the stack and the existing i18n surface:**

```bash
ls -a
cat package.json 2>/dev/null | head -60
cat pyproject.toml composer.json Gemfile go.mod 2>/dev/null | head -60
```

**Find an existing i18n implementation before writing one:**

```bash
grep -rIl --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "i18next|react-intl|vue-i18n|next-intl|formatjs|intl-messageformat|gettext|babel|lingui|icu|MessageFormat" . | head -30

find . -path ./node_modules -prune -o \
  \( -name "*.po" -o -name "*.xliff" -o -name "*.arb" -o -name "*.ftl" -o -name "messages*.json" -o -name "locales" -o -name "i18n" \) -print 2>/dev/null | head -30
```

**Record these findings** — they drive every later decision:

| Question                                                                 | Why it matters                                                  |
| ------------------------------------------------------------------------ | --------------------------------------------------------------- |
| What is the runtime? (Node, browser, Python, PHP, JVM, Go, Rust, mobile) | Determines whether `Intl` is available or a library is required |
| Which i18n library is already present?                                   | Extend it; do not replace it                                    |
| Where do translations live? Which format?                                | Determines the catalog structure                                |
| Is there a TMS or a translation vendor in the loop?                      | Constrains the file format and key policy                       |
| Is a locale stored per user? Where?                                      | Determines the negotiation source                               |
| Does the project already store timestamps with a zone?                   | Determines how much date work is a migration                    |
| Are there existing locale-specific branches (`if (locale === 'en')`)?    | These are the highest-signal defects                            |

## Phase 2 — Load Only the Relevant Modules

Load a reference module when its domain is in scope. Read the file in full; each is written to be self-contained.

| Domain                                                | Module                                                                               | Load when                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Language tags, locale negotiation, language selection | [references/intl-language.md](references/intl-language.md)                           | Always. This is the entry point for every other domain.              |
| Dates, times, time zones, calendars                   | [references/intl-date-and-time-format.md](references/intl-date-and-time-format.md)   | The project renders, parses, or stores any date or time              |
| Numbers, currency, units, measurement                 | [references/intl-number-and-currency.md](references/intl-number-and-currency.md)     | The project displays money, counts, percentages, or quantities       |
| Bidirectional text and RTL layout                     | [references/intl-bidi.md](references/intl-bidi.md)                                   | Any RTL language is in scope, or the UI uses physical CSS directions |
| Pluralization, gender, ICU messages                   | [references/intl-pluralization.md](references/intl-pluralization.md)                 | Any user-facing string interpolates a count or a variable            |
| Collation, sorting, string comparison                 | [references/intl-collation-and-sorting.md](references/intl-collation-and-sorting.md) | The project sorts, searches, deduplicates, or compares user text     |
| Unicode text processing and segmentation              | [references/intl-text-processing.md](references/intl-text-processing.md)             | The project truncates, counts, normalizes, or manipulates strings    |
| Content, assets, cultural adaptation                  | [references/intl-content-and-assets.md](references/intl-content-and-assets.md)       | Always, for the catalog structure and layout resilience              |
| Localization testing and QA                           | [references/intl-testing-and-qa.md](references/intl-testing-and-qa.md)               | Always. Establishes the gate that prevents regression.               |

If the user narrowed the domains, load only those plus `intl-language.md` and `intl-testing-and-qa.md`. The language module defines the tag vocabulary every other module depends on, and the testing module defines how you prove the work.

## Phase 3 — Audit

Produce a findings list before editing. Each finding names a file, a line, the defect, and the concrete fix.

Search for the defects that indicate a locale-hardcoded codebase. These greps are starting points, not a complete audit:

```bash
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "toLocaleDateString\(\)|toLocaleString\(\)|new Date\(.*\)\.getDate\(\)" . | head -40

grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "\.toUpperCase\(\)|\.toLowerCase\(\)" . | head -40

grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "=== *1|=== *0|count *[<>=]+ *1|\$\{count\}" . | head -40

grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "margin-left|margin-right|padding-left|padding-right|text-align: *(left|right)|left:|right:" . | head -40

grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} \
  -E "\.sort\(\)|ORDER BY" . | head -40
```

Classify each finding by severity, because the user needs to know what to fix first:

| Severity     | Meaning                                          | Examples                                                                                                                                        |
| ------------ | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Critical** | Produces wrong data, not just wrong presentation | Storing a local wall-clock time as an instant; parsing a localized number with `parseFloat`; truncating a string by code unit and corrupting it |
| **High**     | Visibly broken for a real locale                 | `if (count === 1)` pluralization; `toUpperCase()` on Turkish text; `sort()` on non-ASCII; date rendered in the server's zone                    |
| **Medium**   | Correct today, blocks the next language          | Physical CSS properties; concatenated sentence fragments; a hardcoded `MM/DD/YYYY` format                                                       |
| **Low**      | Polish and completeness                          | Missing `lang` on inline foreign text; no pseudolocale in CI                                                                                    |

## Phase 4 — Implement

Apply fixes in this order. The order matters because later work depends on earlier decisions.

1. **Locale model.** Define how a locale is represented, negotiated, resolved, and persisted. Everything else consumes this.
2. **Catalog structure.** Establish the message file layout, key policy, and placeholder syntax before migrating a single string.
3. **String extraction.** Replace hardcoded user-facing strings with catalog lookups, including the ones that look safe.
4. **Formatting.** Replace hand-rolled date, number, and currency formatting with the platform formatter or the library's.
5. **Pluralization and grammar.** Convert every count-dependent string to an ICU plural. Never leave a numeric conditional.
6. **Direction and layout.** Introduce `dir`, logical CSS properties, and bidi isolation where needed.
7. **Sorting and comparison.** Replace code-unit comparison with a locale-aware collator.
8. **Testing.** Add the pseudolocale, the lint rules, and the locale matrix so the work cannot regress.

Follow the conventions already in the repository. If the project has an `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or a documented i18n policy, that policy wins over any recommendation in these modules. Report the conflict rather than silently overriding it.

Do not introduce a new dependency when the platform formatter covers the need. `Intl` in JavaScript, `ICU` in Java and PHP, `Babel` in Python, and `golang.org/x/text` in Go all cover far more than most teams assume.

## Phase 5 — Verify

Never claim the work is done without running these.

- [ ] The app builds and the existing test suite passes.
- [ ] Every locale in scope renders the audited screens without a fallback to the default language.
- [ ] No raw formatting API remains on a user-facing path (`toLocaleDateString()` with no locale or options, `new Date().toString()`, `strftime` with a hardcoded pattern).
- [ ] No count-dependent string uses a numeric comparison.
- [ ] No `toUpperCase()`/`toLowerCase()` remains on a value used for comparison or identity.
- [ ] Sorting of user-visible lists uses a locale-aware collator.
- [ ] Timestamps are stored with an explicit zone or as an instant, and rendered in the viewer's zone.
- [ ] Layout uses logical properties; an RTL locale was rendered if one is in scope.
- [ ] Truncation and character counting respect grapheme clusters.
- [ ] The pseudolocale build runs and surfaces no hardcoded strings.
- [ ] The locale matrix is wired into CI.

Report what you could not verify and why. An unverified claim is worse than a stated gap.

## Output

Report back in this shape, trimmed to what is relevant:

```markdown
## Scope

Languages: en, es — Domains: all nine

## What Exists

Runtime: Node 22 / React 19. Library: react-intl 7. Catalogs: JSON per locale.
Timestamps: stored as UTC epoch ms. Locale source: user profile.

## Findings

| Severity | Location               | Defect                                         | Fix                                                     |
| -------- | ---------------------- | ---------------------------------------------- | ------------------------------------------------------- |
| Critical | src/orders/total.ts:42 | `parseFloat(row.amount)` on a localized string | Parse with the API formatter, keep a raw numeric column |
| High     | src/cart/Cart.tsx:88   | `items.length === 1 ? 'item' : 'items'`        | ICU plural via `<FormattedMessage>`                     |

## Changes Applied

<grouped by domain, naming the files touched>

## Verification

<the checklist above, with the actual result of each>

## Out of Scope / Not Verified

<defects observed but not fixed, and why>
```

For a change touching many files, publish the report as an Artifact so the team can review it; keep a short summary in the reply.

## Common Mistakes

| Mistake                                                                 | Why It Breaks                                                                       | Correct Approach                                                                            |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Adding a library before checking for one                                | Two i18n systems fight over the same strings                                        | Detect first; extend what exists                                                            |
| `if (count === 1)`                                                      | Plural rules are per-language; Polish has four categories, Arabic six, Japanese one | Use ICU `plural` with the CLDR categories                                                   |
| `parseFloat(localizedString)`                                           | German `1.234,56` parses as `1.234` — a silent 1000x error                          | Parse with the locale-aware formatter; store a raw numeric value                            |
| `toLocaleDateString()` with no locale                                   | Uses the server or CI locale, not the viewer's                                      | Pass the resolved locale explicitly                                                         |
| Storing a local wall-clock time as an instant                           | DST transitions corrupt it and it renders wrong in other zones                      | Store an instant plus an IANA zone, or a zone-free local time when that is the true meaning |
| `margin-left` for direction-aware spacing                               | The layout does not mirror in RTL                                                   | Use `margin-inline-start` and friends                                                       |
| `str.toUpperCase()` for comparison                                      | Turkish dotless `ı` and German `ß` break equality and search                        | Use `Intl.Collator` with `sensitivity: 'accent'`, or `toLocaleUpperCase(locale)`            |
| `arr.sort()` on user text                                               | Sorts by code unit; `Å`, `é`, and `Z` land in the wrong places                      | `Intl.Collator(locale).compare`                                                             |
| Concatenating sentence fragments                                        | Word order and grammar differ per language; the result is untranslatable            | One complete message per unit with named placeholders                                       |
| Truncating with `.substring()`                                          | Splits grapheme clusters and corrupts emoji, flags, and Indic scripts               | `Intl.Segmenter` with `granularity: 'grapheme'`                                             |
| Adding RTL styling only when RTL is requested, but keeping physical CSS | The next language costs a rewrite                                                   | Use logical properties from the start; it is free                                           |
| Machine-translating legal or regulatory copy                            | Legally invalid and often wrong                                                     | Flag it for human translation                                                               |
| Assuming English text length                                            | German and Finnish run 30-40% longer and break fixed layouts                        | Design for expansion; test with the pseudolocale                                            |
