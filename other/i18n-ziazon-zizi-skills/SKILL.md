---
name: i18n
description: >
  Multi-language support (i18n/l10n). Use when a task touches a translation file or a
  user-facing string in a product that ships more than one language: adding a language or key,
  extracting strings, vue-i18n/nestjs-i18n/go-i18n, locale formatting, translated data (enums,
  emails, PDFs), locale routing, hreflang, RTL. Its core failure is a key that reaches one pack
  and not the others.
---

# Multi-language builds (i18n)

Goal: every user-facing string, in every surface, reaches every supported language, and
the build *fails* when one doesn't. Translation itself is the easy part. What breaks
multi-language products is **completeness**. A key gets added to the source pack only. A
label lives in a database row instead of a template. An English literal hides as a
"fallback". A copy change leaves every other pack saying the old thing. None of those show
on an English-speaking reviewer's screen. This skill exists to make them fail CI instead.

**Read alongside:** [surfaces.md](surfaces.md), the inventory of where strings hide. Run
it during planning; it is where "we missed a field" comes from. Also
[stack-notes.md](stack-notes.md), for per-stack mechanics and the **message-syntax table**
(Vue / Vite SSR, NestJS, Go, Postgres, plain JSON packs). Project specifics, when your
copy keeps them, are in `LOCAL.md` beside this skill.

## The failure classes (each one has shipped somewhere)

| # | Failure | How it hides | The rail that catches it |
|---|---|---|---|
| F1 | Key added to the source pack only | A per-call-site fallback renders English, so the page "works" | Key-parity gate (§3) + no call-site fallbacks (§2) |
| F2 | Missing key blanks a region, or prints the raw key | That layer has no fallback while another layer does | One fallback policy, implemented once (§2) |
| F3 | Source copy changed, translations stale | Same key, new meaning; every other pack still says the old thing | New meaning → new key (§4) |
| F4 | Machine-translation defects | Transliterated into Latin script, diacritics stripped, domain term translated three ways, polysemous word mistranslated | Script check + glossary + native review gate (§3, §6) |
| F5 | Data-driven text untranslated | Category labels, enum values, statuses, survey/CMS text live in data, not templates | Codes in data, labels in packs, enum-coverage gate (§3, §5) |
| F6 | Proper nouns inconsistent | "Do not translate" was never decided, so some packs translate it and some don't, and a "fixed" claim is never re-checked | Do-not-translate list as data, read by the gate (§6) |
| F7 | Non-ASCII mangled at ingest | A file or CSV read with the platform default encoding | Explicit encoding at every boundary + a non-ASCII fixture (§7) |
| F8 | Locale files missing from the deployed artifact | Packaging manifest or bundler config lists files by hand | Test the built artifact, not the source tree (§7) |
| F9 | Language list drifts | Supported codes live in three places (server list, fallback map, client list) | One locale registry; everything derives from it (§1) |
| F10 | RTL language shipped LTR | `dir` never set; physical CSS (`margin-left`) everywhere | `lang` + `dir` on the root; logical CSS properties (§8) |
| F11 | Fallback across languages | A creole falls back to its lexifier, a dialect to a different script | Fallback chains stay inside one language (§1) |
| F12 | Concatenated or hand-pluralised strings | `"You have " + n + " items"`; `n === 1 ? "item" : "items"` | Whole-sentence keys + CLDR plural categories, checked per locale (§2, §3) |
| F13 | One user's language served to another | SSR or CDN cache not keyed on locale; a module-level i18n singleton on the server | Locale in every cache key; per-request i18n instance (§1, stack-notes) |

## 1. One locale registry

A single module (or JSON file) is the only list of supported locales. Each entry carries:

- the BCP 47 code, and the **per-library code mapping** where libraries disagree
  (`pt-BR` in BCP 47, `pt-br` in dayjs, `pt_BR` in ICU and Postgres collation names);
- the endonym (the language's name in itself; that is what the switcher shows);
- text direction and the expected script(s) for the §3 script check;
- the fallback chain;
- release status (`live` / `beta` / `hidden` / `pseudo`) and review record
  (`reviewedBy`, `reviewedAt`; §6).

The server, the client, every service, the completeness gate, the build config and the
switcher all import it. Anything that re-lists the codes is a bug in waiting.

- **Fallback chains stay within one language.** `es-419 → es → <source>` is fine.
  Falling a creole back to its European lexifier, or a Chinese variety to a different
  script, shows the reader a different language. The source language with a reported gap
  is better.
- **The switcher shows endonyms, not flags.** A flag is a country, not a language: Spanish,
  Arabic, French and Portuguese each span many countries. Add regional qualifiers where
  variants coexist ("Português (Brasil)").
- **Locale resolution order, fixed:**
  1. **Public, indexable routes:** the URL locale (`/es/…`) is authoritative. A request
     without one is redirected to the best match from cookie → `Accept-Language` → default.
     A saved profile never overrides the URL here, or `/es/foo` renders English and search
     engines index the wrong language.
  2. **Signed-in app routes:** saved profile preference → URL / `?lang=` → cookie →
     `Accept-Language` → default. Changing language in the switcher writes the profile and
     the cookie.
  3. Name the cookie once in the registry module (e.g. `locale`; `Path=/`,
     `SameSite=Lax`, one-year expiry). Don't invent a second one.
- **Cache keys carry the locale.** Every SSR render cache, CDN rule and HTTP cache varies
  on the resolved locale (URL segment, or `Vary` on the cookie/header that decides it). A
  page cached without it serves one user's language to the next.
- **Pass the resolved locale explicitly**: through the request context, into every
  downstream service call (one header, e.g. `X-Locale`, defined in the shared contract),
  into queued jobs and event payloads, and from the stored `user.locale` for anything sent
  later (emails, reminders). Never infer it from a translated object.

## 2. One lookup, one fallback policy

All string resolution goes through one function per runtime (`t()` / `$t` /
`i18n.translate` / `localizer.Localize`). The missing-key behaviour is configured there,
once:

- **dev and test: loud.** Throw, or render a visible marker (`⟦missing:key⟧`) and log. The
  point of dev is to see the gap.
- **production: fall back along the chain to the source language, and report** (log or
  metric with key and locale). Never blank, never the raw key, never silent.

Check what your library does by default rather than assuming. Some return the key
silently. nestjs-i18n, for example, returns the key with no log unless `throwOnMissingKey`
is set (stack-notes).

**Banned: call-site fallbacks with user-facing literals.** Examples:
`t('x') || 'English text'`, `t('x') ?? 'Text'`, `pack$x %||% "…"`, and a library's
per-call `defaultValue: 'Text'`. A literal at the call site defeats the parity gate (the
key need not exist for the page to look right). It also hides the gap from reviewers and
makes two layers of one app disagree about what a missing key does (F1, F2). Enforce it
with a lint (stack-notes has an ESLint selector).

**Never render translated strings as raw HTML.** Translators and MT are an input you don't
control. Use the library's component interpolation (vue-i18n's `<i18n-t>`, tag
placeholders) instead of `v-html` / `innerHTML` / `template.HTML` on a translation.

**Message format.** Keys hold whole sentences with their arguments, never fragments glued
together in code. Plurals use the library's CLDR plural support. Languages have one to six
plural categories, and `n === 1` is right for only some of them. **Use the library's
native syntax:** vue-i18n, nestjs-i18n and go-i18n each have their own placeholder and
plural syntax, and none of them uses ICU MessageFormat by default. See the syntax table
in stack-notes. Use named arguments wherever the syntax allows, so translators can reorder.
Where it is positional (printf-style), use explicit indexes (`%[1]s`), never bare `%s`.

**Dynamic keys go through an explicit map.** `t(`status.${s}`)` is invisible to
missing-key and unused-key lints. Write `const STATUS_LABEL: Record<Status, Key> = {…}`
(typed against the enum, so a new member fails type-check), or rely on the §3 enum-coverage
check. Never leave a key reachable only by string building.

**Key naming.** Namespace by feature or surface (`orgDetails.cardGenderTitle`) and
describe *meaning*, not English wording (`cta.save`, not `saveButtonText`).

## 3. The completeness gate (CI, from P0, before any string is extracted)

**One language-neutral script** (Node or Python) reads the registry and every pack. It
runs in **every** service's CI job (UI, API, Go, workers), so no codebase can drift. Each
stack's syntax needs its own parser for items 3–4 (stack-notes). It fails on:

1. **Key parity.** Every locale's flattened key set equals the source pack's. Missing
   *and* extra keys both fail (an extra key is usually a typo of a missing one).
2. **Empty values**: `""` or whitespace.
3. **Argument and tag parity.** Every placeholder and every markup tag in the source
   (`{name}`, `{{.Name}}`, `<b>`, `<0>`) appears in each translation, and no others. Every
   message parses with its stack's parser.
4. **Plural categories.** Each plural message provides every CLDR category the locale
   needs (`new Intl.PluralRules(locale).resolvedOptions().pluralCategories`, plus `other`).
   Argument parity passes a Russian message with only `one|other`; this check doesn't.
5. **Untranslated copies.** A value byte-identical to the source in a non-source locale
   fails. Exempt it only via the do-not-translate list (brands, product names) or the
   per-locale `allowIdentical` list (true cognates: "Menu", "Hotel"), both kept as data.
   Skip pure numbers and symbols.
6. **Script check.** Strip placeholders, tags, do-not-translate terms and digits. At least
   50% of the remaining letters must be in the locale's expected script(s) from the
   registry. Latin-only output for a Cyrillic, Arabic or Han locale is transliteration (F4).
   List several scripts where a locale needs them (Japanese: Han + Kana; Serbian: pick one).
7. **Length.** Values over the `maxLength` recorded in the key's metadata sidecar fail.
8. **Registry parity.** Each registry code has a pack and each pack has a registry entry.
   No `pseudo` locale in a production build's registry.
9. **Enum coverage.** Every member of every user-visible enum and every API error code in
   the shared contract has a label key in every locale. This is how data labels (F5) and
   dynamic keys get covered.
10. **Content parity.** Every data-driven content item (§5) has every locale.
11. **Release.** A locale whose status is `live` has a review record (§6).

**Prove the gate can fail** before trusting it. Delete one key from one pack and watch it
go red. Drop a plural category, and watch it go red. Empty the registry: the run must
fail, not pass vacuously over zero locales. A parity test that iterates an empty list is
green forever.

Add **source lints** per stack too: no raw text in templates, no missing keys, no unused
keys, and no call-site literal fallbacks (stack-notes).

## 4. Changing source copy

Changing the source text of an existing key silently invalidates every translation of it
(F3). **Default policy: new meaning → new key.** Any rewording that changes meaning gets a
new key and the old key is deleted, so parity forces every pack to be revisited. Typo and
punctuation fixes keep the key.

Projects with frequent copy churn may instead track staleness, but only with all of this
specified:

- the sidecar stores `sourceHash` per translation: sha256 of the NFC-normalised, trimmed
  source string at the time the translation was written or reviewed;
- the gate fails when the current source hash ≠ the stored one;
- a reviewer who decides a translation still holds re-stamps it with one documented
  command. That stamp is the record that the language was *looked at* rather than skipped.

A PR that edits the source pack and touches fewer locale files than that implies needs
the reason in its description.

## 5. Data-driven content is UI

The strings missed most often are not in templates at all ([surfaces.md](surfaces.md) §B):
enum and status labels, categories and taxonomies, seeded reference data, survey or CMS
text, generated documents.

- **Store codes in the data; translate at the edge.** The row says
  `status = 'awaiting_parts'`; the label comes from the pack via the §2 map. Never store an
  English label as the value and translate by matching the string.
- **Content that must stay with its data** (long-form, per-record text) goes in a
  translations table or file keyed by `(item_id, locale)`, covered by gate item 10.
- **Sensitive data stays opaque.** If a record is confidential but its text is
  translatable, store an opaque key in the protected record and keep the text and its
  translations in the translation layer, so translators never see which record a
  sentence belongs to.
- **Vocabularies that drive matching or filtering are separate from display labels.** A
  translated label must never be the thing that's matched.
- **User-generated content is not machine-translated by default.** Decide explicitly:
  show it as written (with a `lang` attribute if known), or translate on demand and label
  it as translated.
- **Text a user agrees to** (terms, consent, legal) is versioned per locale. Store the
  locale and version at acceptance.

## 6. Translation quality

Machine translation is a draft. Before a locale goes `live`:

- **Glossary per language** for domain terms (the product's core nouns), so one concept
  is one word across the whole pack. Inconsistent terminology is the most common defect in
  machine-translated packs.
- **Do-not-translate list** (brand, product and place names you keep), as data the gate
  reads. Then "we fixed the untranslated place name" is a check, not a claim.
- **Script and diacritics.** The gate catches transliteration. Review catches stripped
  accents (`Configuracion` for `Configuración`).
- **Native-speaker review is a release gate** for each locale, recorded as `reviewedBy`
  and `reviewedAt` in the registry and enforced by gate item 11. Prioritise it for
  lower-resource languages (many creoles and regional varieties), where MT quality is
  weakest.
- **Give translators context**: a description per key (what it labels, where it shows,
  `maxLength`) in the sidecar, and screenshots for anything ambiguous ("Resume": the verb
  or the CV?).

## 7. Encoding, packaging, build

- Declare the encoding at every ingest boundary: file reads, CSV imports, the DB
  connection, HTTP `Content-Type: …; charset=utf-8`, email MIME. Keep a fixture with
  accented Latin, CJK, Arabic and an emoji, and round-trip it through each pipeline.
- Locale files must reach the deployed artifact. If the build lists files explicitly (a
  deploy manifest, a bundler `include`, a Dockerfile `COPY`), test the **built output** for
  every registry locale. For lazy-loaded locale chunks, assert each one exists in `dist/`.
- Every build target loads translations its own way: SSR server, client, embeddable
  widget, email renderer, PDF worker, each Go binary. Inventory them; each one is a place a
  locale can be missing.

## 8. Layout, RTL, fonts, formatting

- Set `<html lang="…" dir="…">` from the registry on the server for SSR. Use CSS logical
  properties (`margin-inline-start`, `text-align: start`). Mirror **directional** icons
  only (arrows, chevrons, "back"), not play buttons, checkmarks or logos. Force LTR on
  embedded numbers, codes and phone numbers with `dir="ltr"`. Use `<bdi>` around
  interpolated text whose direction is unknown (a user's name).
- Fonts: the font stack must cover every script you ship. Set `lang` correctly, because
  Han characters render with different glyph forms per language and `:lang()` rules key
  off it.
- Allow 30–40% text expansion; short labels can double. No fixed-width buttons sized to
  English.
- **Formatting** goes through the locale-aware formatter (`Intl.*` in JS, CLDR-backed
  libraries elsewhere) with the resolved locale passed explicitly. Never build a date
  string by hand. Digit system (Latin vs Arabic-Indic) is a CLDR numbering-system choice;
  decide it per locale.
- **Time.** Store **instants** in UTC and format at the edge, with an explicit IANA
  timezone. Store **future local-time events** (appointments, bookings) as local datetime
  plus the IANA zone id, because a stored UTC instant shifts when DST or zone rules change.
- **SSR hydration.** Server and browser can format the same `Intl` call differently (ICU
  versions differ, and so does the default timezone). Render formatted dates with an
  explicit timezone on both sides, or format on the client only. Include hydration
  warnings in the verification sweep.
- Currency is a business fact, not a locale fact; don't infer it from the language.
- Sorting and search: locale-aware collation where users see sorted text. For paginated
  lists, sort in the database, not in the app, or page order breaks (stack-notes).

## Planning a multi-language program

Front-load these decisions program-wide, before any build phase. Each one left open
becomes a mid-build stall or a rewrite.

1. **Which locales, in what order**, and who decides a locale is ready.
2. **Scope:** UI chrome only? Server messages? Emails, SMS, push? PDFs and exports?
   Data-driven labels? User-generated content? Admin and internal tools (often: no)?
3. **Where translations live** (repo JSON vs a translation-management service), who
   translates (MT + review, agency, community), and the review gate per locale.
4. **Pack layout across stacks:** one shared pack source compiled into each stack's
   syntax, or per-stack packs with one shared gate. Decide this before P0; it fixes the
   gate's parsers.
5. **Fallback policy** (§2). **Copy-change policy** (§4; default new key).
6. **Locale resolution, persistence and propagation** (§1): the profile column, the cookie,
   the inter-service header, the field in job and event payloads.
7. **Server contract:** for an API with its own UI client, return stable codes plus
   arguments and let the client render. Localize on the server for emails, PDFs, SMS and
   anything rendered without a client. Decide per surface, once.
8. **Formatting facts that aren't language:** currency, units (miles/km), timezones,
   address and phone formats, name order.
9. **SEO** for public pages: localized URLs, `hreflang`, translated `<title>` and meta,
   `og:locale`, per-locale sitemap entries.
10. **RTL** in scope, or explicitly deferred.

Then phase the build:

- **P0 Foundation.** Registry, lookup with the fallback policy, the completeness gate in
  every CI job, lints, the pseudo-locale and its e2e sweep, the encoding fixture, cache
  keys. No user-visible change.
- **P1 Extraction, surface by surface.** Walk [surfaces.md](surfaces.md), one surface per
  unit. Each unit ends with that surface's pseudo-locale sweep clean.
- **P2 Formatting.** Dates, numbers, currency, plurals, time storage.
- **P3 Server and data.** API error codes, enum and category labels, content tables, the
  locale header between services.
- **P4 Out-of-app channels.** Emails, SMS, push, PDFs, exports.
- **P5 Translation and review**, per locale. Flip locales to `live` one at a time.

## Verifying (the proof, not the claim)

- **Pseudo-locale sweep, automated.** Add a dev/CI-only locale (`en-XA`, status `pseudo`)
  generated from the source pack. It accents letters, pads ~35% and wraps each value in
  markers: `⟦Ŝàvé çĥàñĝéš ·····⟧`. The generator must preserve placeholders, plural syntax
  and tags untouched. The pseudo-locale is excluded from parity and release rules.
  An e2e test walks **every route from the router table** in that locale and fails on:
  - any visible text node without the markers;
  - any `placeholder`, `title`, `alt` or `aria-label` without them;
  - `document.title` without them.

  Unmarked text is a missed string. A clipped marker is a layout that won't survive
  expansion. This is the single highest-yield check for "we missed fields". Seed data
  and user content will legitimately be unmarked: allowlist those selectors explicitly
  rather than loosening the rule.
- **Positive control first.** Confirm the pseudo-locale is actually active (read
  `<html lang>` back) before trusting a clean sweep. A knob that didn't move proves nothing.
- **RTL sweep** in one RTL locale (or a pseudo-RTL) for every route.
- **Built-artifact check** (§7) for every registry locale.
- **Non-UI channels.** Render each email, PDF, SMS and Go-generated document in the
  pseudo-locale and check the *rendered output* for unmarked text, not the template.
- **Screenshots per locale** of key flows, for the native reviewers.

## Review checklist (per PR)

- [ ] New user-facing text goes through the lookup. No literals, no call-site fallbacks,
      no translated string rendered as raw HTML.
- [ ] Every new key exists in every locale, with every plural category (the gate is
      green, and it ran).
- [ ] Source copy changes use a new key, or a re-stamped hash with a reason.
- [ ] No concatenation or hand-pluralisation. Dynamic keys go through a typed map.
- [ ] Data-driven labels are stored as codes, translated at the edge and covered by enum
      or content coverage.
- [ ] Dates, numbers and currency go through the locale formatter with explicit locale and
      timezone.
- [ ] The locale propagates to any new service call, job or email.
- [ ] New surfaces (template, email, export, build target) are added to the inventory.
- [ ] The pseudo-locale sweep of the touched routes is clean.

## Related skills

- [code-quality](../code-quality/SKILL.md): the hard rules every diff meets, translation plumbing included — one responsibility per file, readable by a junior engineer, and one rhythm per kind of work.
