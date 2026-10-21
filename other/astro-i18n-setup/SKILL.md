---
name: astro-i18n-setup
description: >
  Turn a new-website scaffold into a turnkey multi-language site: Astro i18n
  routing (clean default locale + prefixed others), self-referencing hreflang +
  x-default in the Base layout, i18n sitemap alternates, a language switcher, and
  the test-harness changes that keep the green-from-commit-1 gate honest across
  locales. Run at scaffold time when new-website Q4 = "two+ languages at launch", OR
  later to add a second language to a single-locale site whose default stays unprefixed
  (phased rollout). Trigger phrases: "multi-language site", "add i18n", "DE+EN site",
  "internationalization", "hreflang setup", "two languages at launch".
---

# Astro i18n setup (scaffold-time, opt-in)

Wires turnkey internationalization into the `new-website` Astro overlay. **Opt-in:**
the default scaffold stays single-locale. Run it either **at scaffold time** for a
2+-language launch (new-website §1 Q4), **or later** when you add a second language to
an existing single-locale site — see **Phased rollout** below.

Safe vs unsafe: because the default locale stays **unprefixed** (`/`, not `/en/`), adding
a *secondary* prefixed locale (`/de/…`) is purely additive — it never moves an existing
URL. What DOES break links/SEO is moving the **default locale itself** off `/` (e.g.
retrofitting `/` → `/en/`); this skill never does that, so keep `prefixDefaultLocale:
false`. A full re-prefixing of the default is a migration, not this skill.

Routing model (house default): **clean default locale, prefixed others** —
`/` and `/about` are the default language (marked `x-default`); other languages get
a prefix (`/de/`, `/de/about`). `prefixDefaultLocale: false`. This keeps the
default-locale URLs identical to a single-locale build, so nothing regresses.

Deep SEO rules (reciprocity, x-default, canonical-vs-hreflang, sitemap structure,
"translate the whole page not just chrome") live in
`seo-audit/references/international-seo.md` — read it, don't re-derive it.

## Phased rollout (primary language first, translate later)

You don't have to translate everything before launch. Because the default locale is
unprefixed, you can build and ship the **primary language first**, then add the second
locale when the translations are ready — without moving a single existing URL:

0. **Phase 0 — vendor this skill NOW.** A declared-multilingual-phased site gets
   `astro-i18n-setup` copied into its skills dir at scaffold time (new-website §3's
   conditional copy list) even while running single-locale — Phase 2 below is
   executed months later by whoever holds the handoff, and the instruction can't
   resolve if the skill isn't in the project.
1. **Phase 1 — primary only.** Build the site in the default language and ship it. Keep
   `LOCALES = [DEFAULT_LOCALE]` (one entry). `tests/i18n.spec.ts` **self-skips** while
   there's a single locale (`LOCALES.length < 2`), so the full QA gate is green with no
   half-built hreflang. You can skip this skill entirely for now, or apply it with a
   single-locale `LOCALES` to pre-wire the layout.
2. **Phase 2 — add the locale.** When translating, apply this skill's changes: add the new
   locale to `astro.config` `i18n.locales`, the `sitemap({ i18n })` map, and `LOCALES`;
   create the `src/pages/<locale>/…` pages. hreflang, `x-default`, sitemap alternates and
   `i18n.spec.ts` now enforce both locales — and the default-language URLs are exactly what
   they were in Phase 1.

The one rule: commit to an **unprefixed default** from day 1 (`prefixDefaultLocale:
false`). That's the only decision that's expensive to change later; the translations
themselves are always additive.

## Localized 404

The starter's `src/pages/404.astro` serves every unmatched URL, whatever its
locale prefix. Translate its strings to the DEFAULT locale's language; a
per-locale 404 (`src/pages/de/404.astro`) is optional and needs no routing
changes — Cloudflare Pages serves `/de/404` for unmatched `/de/*` paths when
it exists. Keep any 404 noindex and out of PAGES (@astrojs/sitemap already
excludes status-code pages from the sitemap by itself).

## Partial translation (some routes are not translated)

Not every route needs every locale. A German company running a DE+EN site whose blog
stays German-only, or an English-first site adding one German landing page, does not
have to translate everything to keep the i18n gate on.

Mark such a route in `src/config.ts`'s `ROUTES` registry (§2) with an explicit
`locales` list; a route with no `locales` field exists in every locale (unchanged
default):

```ts
export const ROUTES: readonly RouteSpec[] = [
  { path: '/' },
  { path: '/privacy' },
  { path: '/blog/some-post', locales: ['de'] },  // German-only, no EN variant
];
```

One registry drives everything: `tests/_helpers.ts` PAGES (the EN variant is never
expected to exist), Base.astro's head hreflang (the route emits one `de` alternate +
a self-referencing `x-default` — never a link to a never-built page), the sitemap
`serialize` hook (§1 — no advertised-but-missing alternate), and
`tests/i18n.spec.ts`'s completeness/x-default/reciprocity/thin-translation checks
(all per-route via `routeLocales()`; a route without a default-locale variant gets a
deterministic x-default — its first listed locale — on every variant). Google's
guidance is explicit that hreflang belongs only on pages that actually have variants
(international-seo.md) — this is that rule, made enforceable.

## Light path: twin pages (no prefixed routing)

For a handful of translated pages on an otherwise single-language site, the full
routing setup above is more machinery than the job needs. The default kit
`Base.astro` ships an optional `alternates` prop instead — no astro.config changes,
no locale prefixes, no `LOCALES`:

Give each paired page its own localized slug (see "Localized slugs" in
`seo-audit/references/international-seo.md`) — e.g. `/ai-events-munich` (EN) and
`/ai-treffen-muenchen` (DE) — and pass BOTH pages the full cluster, including a
self-referencing entry and `x-default`:

```astro
<!-- /ai-events-munich (EN page) -->
<Base title="…" description="…" alternates={[
  { hreflang: 'en', href: '/ai-events-munich' },
  { hreflang: 'de', href: '/ai-treffen-muenchen' },
  { hreflang: 'x-default', href: '/ai-events-munich' },
]}>

<!-- /ai-treffen-muenchen (DE page) -->
<Base lang="de" title="…" description="…" alternates={[
  { hreflang: 'de', href: '/ai-treffen-muenchen' },
  { hreflang: 'en', href: '/ai-events-munich' },
  { hreflang: 'x-default', href: '/ai-events-munich' },
]}>
```

`tests/seo.spec.ts`'s twin-page reciprocity check (in the default suite) enforces
that both halves agree: a self-referencing entry equal to the canonical, no dead
same-site targets, and A→B implies B→A. Forgetting the cluster on one twin — the
exact bug that shipped live on a real site built from this kit (an English event
page with no `alternates`, so its German twin's hreflang went unreciprocated,
which makes Google ignore the pair) — now fails the build. Also add a visible
`<a href="/ai-treffen-muenchen" lang="de" hreflang="de">Deutsch</a>` near the
nav/footer: `alternates` only talks to crawlers, not visitors.

Pick the heavy path (everything above this section) when most of the site is
translated and you want prefixed routing + a language switcher; pick this light
path for a few one-off translated pages. Don't mix both on the same SITE: a
localized-slug twin can't be expressed in ROUTES (non-default locales map to
`/prefix` paths there), so on a heavy site a light-path page fails i18n.spec's
completeness check by design.

## What it changes

### 1. `astro.config.mjs` — i18n routing + sitemap alternates
Add the `i18n` block (default + launch locales, `prefixDefaultLocale: false`)
and give `sitemap()` the matching `i18n` map so it emits `<xhtml:link>`
hreflang alternates — plus a `serialize` hook that filters each entry's
alternates down to the locales the route actually exists in (sparse routes:
routes given an explicit `locales` list in §2's ROUTES registry — see
"Partial translation" above). The hook imports the shared registry from
`src/config.ts` (Vite loads the Astro config, so the TS import works).
Verbatim config: `references/heavy-path-code.md` §1.
Fully-translated sites (no `locales` overrides in ROUTES): the hook is a no-op.

### 2. `src/config.ts` — replace the single locale, add the route registry
Replace `SITE.locale` with `LOCALES` / `DEFAULT_LOCALE` / `LOCALE_LABELS`, and
add the per-route `ROUTES` registry — THE single registry that Base.astro
(head hreflang), astro.config.mjs (sitemap alternates) and the tests all read,
so they can't drift apart; a route with NO `locales` field exists in every
locale. The block also carries fail-loud import-time validation of the
registry (duplicate path, unknown or repeated locale) and the `pathLocale()` /
`neutralPath()` / `routeLocales()` helpers everything else imports — apply it
whole. Verbatim code: `references/heavy-path-code.md` §2.

Remove `SITE.locale` — and the matching `lang = SITE.locale` default prop in
`Base.astro` (the `lang = SITE.locale` default in the Props destructure): the layout derives the locale from `Astro.currentLocale` now
(step 3), so leaving that default referencing the deleted export breaks the build.
Everything reads `DEFAULT_LOCALE` / `Astro.currentLocale`.

### 3. `src/layouts/Base.astro` — locale-aware (VERIFIED build output)
Add the imports + derive locale/alternates, set `<html lang>` from the current
locale, and emit self-referencing hreflang + `x-default`. Verbatim code, with
the hard-won caveats preserved as inline comments:
`references/heavy-path-code.md` §3. Build and confirm the output (reciprocal
hreflang, and clean trailing slashes under `trailingSlash: 'never'`).

The starter's CHROME chrome-strings lookup keys on `SITE.locale`, which §2
removed — rekey it on `Astro.currentLocale ?? DEFAULT_LOCALE` (per-page chrome
language IS correct on a locale-routed site, unlike the single-locale starter).
The template's LIGHT-path pieces are superseded on a heavy site: **delete the
`{alternates.map(…)}` render line** (the hreflang cluster from
`references/heavy-path-code.md` §3 replaces it) — the
`alternates` prop and `altHref` helper then sit unused; remove them too or leave
them, but never feed both emission paths on one page.
The starter's `Astro.locals.lang = lang;` line becomes `Astro.locals.lang = currentLocale;`
(in the §3 code), so a contact form on the page speaks the page's language.
Keep the `ogLocale` line (config.ts's shared `ogLocaleFor` maps `lang → og:locale`);
optionally add `og:locale:alternate` for the non-current locales. `inLanguage` in the
WebPage/WebSite schema should use `currentLocale`.

### 4. `src/components/LanguageSwitcher.astro` (new)
Copy the ready component from `references/LanguageSwitcher.astro` into
`src/components/` and render it in the site's nav/header on every page. It links
the **current page** in each locale the route exists in — `routeLocales(neutral)`
(§2), NOT `LOCALES`, so a sparse route's switcher never links a never-built
variant — labelled from `LOCALE_LABELS`, active locale `aria-current="true"`.
`tests/i18n.spec.ts` asserts every multi-locale page carries it and that each
switcher's links point at exactly the route's real siblings (hreflang AND
href). Rendering it twice (header + footer) is fine — the check runs per
switcher — but give the second one a distinct `ariaLabel` (axe's
landmark-unique rule).

### 5. Page/content structure
- Default-locale pages stay at `src/pages/*` (e.g. `src/pages/about.astro` → `/about`).
- Each other locale lives under `src/pages/<locale>/*` (e.g. `src/pages/de/about.astro` → `/de/about`).
- With Content Collections, add a `locale` field (or per-locale entry dirs) and render
  locale routes from it. **Translate the whole page**, not just the chrome — partial
  translation reads as thin/duplicate (international-seo.md).

### 6. `public/llms.txt` — keep ONE unified file
List the key pages across all locales in a single `/llms.txt` (do not split per
locale) — each entry's description written in THAT page's language (the German
entries in German), per website-seo-geo's GEO rule.

## Test-harness changes (the part that keeps the gate honest)

### `tests/_helpers.ts` — generate PAGES from the route registry
```ts
import { DEFAULT_LOCALE, ROUTES, routeLocales } from '../src/config';
export const PAGES = ROUTES.flatMap((r) =>
  routeLocales(r.path).map((loc) =>
    loc === DEFAULT_LOCALE ? r.path : (r.path === '/' ? `/${loc}` : `/${loc}${r.path}`),
  ),
) as readonly string[];
```
Only the PAGES export changes — KEEP the rest of the file (`THEMES`,
`germanFunctionWordDensity`, `GERMAN_FUNCTION_WORDS`, and `toneViolations` with the
tone rules it reads): the tone and i18n specs import
them, and replacing the whole file with just this snippet breaks the suite at compile
time.
With no `locales` overrides this yields the identical set as before — `/`,
`/privacy`, `/de`, `/de/privacy` (route-major order instead of locale-major; every
consumer sorts or iterates, so nothing observes the order). A sparse route appears
only under its own locales, so navigation.spec never 404-checks a variant that was
deliberately not built. `seo.spec.ts`'s canonical check (`canonical === SITE.url +
path`) and the sitemap-drift test pass unchanged, because the i18n sitemap still
emits one `<loc>` per page (alternates are `<xhtml:link>`, not extra `<loc>`s).

Adding a locale also brings the new `/de*` pages under `seo.spec.ts`'s own-OG-card
guard. Give each real CONTENT page a translated card — an entry with German
title/subtitle text in `generate_og_cards.py` PAGES plus `image=` on the page.
Do NOT just exempt content routes: an exempted `/de` page shares the ENGLISH
default card into German chats, the same silent-wrong-language failure the
German gates exist to stop. Utility twins are the exception — make the
exemption locale-neutral with one line in seo.spec.ts (both places that
consult it), so `/de/privacy` inherits `/privacy`'s exemption. The HOME route
must NOT inherit: `/` is exempt only because the default card IS the home
card — a rationale that does not transfer to `/de`, which needs its own
translated card in `generate_og_cards.py` like any content page:
```ts
const isCardExempt = (p: string) =>
  OWN_CARD_EXEMPT.has(p) || (neutralPath(p) !== '/' && OWN_CARD_EXEMPT.has(neutralPath(p)));
```
(import `neutralPath` from `../src/config`; replace the two `OWN_CARD_EXEMPT.has(path)`
call sites with `isCardExempt(path)`.)

### `tests/i18n.spec.ts` (new) — hreflang contract
Drop in the ready spec `references/i18n.spec.ts` (copy it to the project's `tests/`).
Like every `tests/*.spec.ts`, that copy is frozen — after a `make refresh` reports
`astro-i18n-setup` stale, diff `references/i18n.spec.ts` against the project's
`tests/i18n.spec.ts` by hand (and treat it + `tests/_helpers.ts` as a pair: the spec
imports helpers, so refresh both together or the import breaks loudly).
For every page in PAGES it asserts: exactly one `<link hreflang>` per locale THE ROUTE
EXISTS IN (`routeLocales()`, §2) **plus** `x-default`; every href is the absolute
production URL; the page's canonical equals its OWN-locale alternate; `x-default` → the
default-locale variant (or the route's first listed locale when it has no default-locale
variant); and cross-page **reciprocity** (A→B implies B→A — the #1 hreflang mistake). It also machine-checks the
"translate the whole page" rule below, in two parts (word-count thinness and wrong-language
body are different failure modes — one check can't catch both):
- **Stub/thin translation**: for every non-default-locale page it follows its own
  default-locale hreflang alternate back to the original, counts words in both via
  `document.body.innerText`, and fails if the translated page has under 40% as many words —
  catching a dramatically shorter placeholder page. Word-splitting assumes a whitespace-
  delimited language (this skill's documented use case, DE+EN) — it does not work for
  scripts without whitespace word boundaries (Japanese, Chinese, Thai, …); see the code
  comment in `i18n.spec.ts` if you need one of those.
- **Wrong-language body** (German only): word count can't tell a same-length body that's
  still in the original language from a real translation — nav/footer translated, body left
  untranslated, and the ratio check above passes clean since nothing got shorter. For pages
  whose locale's PRIMARY subtag is `de` (`de`, `de-DE`, `de-AT`, `de-CH`, …), a second check
  strips `nav`/`header`/`footer` first (their own translated chrome can otherwise mask an
  untranslated body on a short page — verified empirically) and counts common German
  function words (der/die/das/und/ist/…) in what's left, failing if their density is near
  zero — real German body prose runs ~15–20%, a non-German body runs ~0%.

All checks self-skip on a single-locale site (the loop has nothing to iterate). The
matching `<xhtml:link>` sitemap alternates come from the `sitemap({ i18n })` config
above — `i18n.spec.ts` machine-checks them against `routeLocales()` per entry (no
manual dist/sitemap-0.xml grep needed).

### `tests/positioning.spec.ts` — key per locale
Add a `POSITIONING` row per locale path (`'/de/about': { term: '…DE term…' }`); the
positioning term is translated, so each locale owns its own phrase.

`tests/tone.spec.ts` already branches on `<html lang>` (through `toneViolations` in
`tests/_helpers.ts`): universal rules (the em-dash ban)
always apply, and English-specific rules layer on top for `lang` starting `en`, German-
specific rules layer on top for `lang` starting `de` — other languages get only the
universal rules. No change needed.

`tests/placeholders.spec.ts` iterates `PAGES`, so it covers each locale's pages with no
change. One edit, before launch only: a second locale's legal page built from one of the kit's drafts
(`/de/privacy` from `_datenschutz.astro`) carries `[BRACKET]` slots until the owner
fills them, so add its route to `UNFILLED_UNTIL_LAUNCH` next to `/privacy`. That is
the one case in which the list may grow; on a launched site, fill the slots instead.

## Regional German (DACH)

Default to bare **`de`** for one German variant — it targets every German-speaking
market at once, and `de-DE`/`de-AT`/`de-CH` variants whose content barely differs
are a near-duplicate risk, not a win (international-seo.md, "Near-Duplicate
Regional Variants"). Go regional only when content genuinely differs per market
(prices in CHF, different legal entities, Swiss ß→ss spelling).

For real multi-region German, the Astro-level mechanism is `{ path, codes }`
locale objects — NOT `LOCALES = ['de-DE', 'de-CH']` with plain string routing,
which yields ugly `/de-DE/…` URL prefixes:

```js
// astro.config.mjs — Astro syntax reference ONLY, see the warning below
i18n: {
  defaultLocale: 'de',
  locales: [{ path: 'de', codes: ['de', 'de-DE'] }, { path: 'ch', codes: ['de-CH'] }],
  routing: { prefixDefaultLocale: false },
}
```

**The kit's harness does NOT yet support path≠code locales** — `config.ts`
`LOCALES` holds plain strings that must equal the URL prefixes: applying the
config above to a kit-built site crashes the build (`getRelativeLocaleUrl`
throws for unknown locales), and mapping regioned codes into
`sitemap({ i18n })` makes the sitemap say `de-DE` where `routeLocales()` says
`de` — failing the sitemap-consistency test with a genuine head/sitemap
contradiction. Treat multi-region as a harness EXTENSION: `LOCALES`,
`pathLocale()`, PAGES generation and the serialize hook all need the
path↔codes mapping first. Two Astro behaviors to know when you build that:
the sitemap i18n map takes ONE code per path key (pick the canonical one),
and `Astro.currentLocale` returns `codes[0]` — order matters, and `<html
lang>` (which drives the German tone/density checks via the primary subtag)
follows it. Until then: bare `de` is the supported answer.

## Wiring (done once in the suite)
- `new-website/SKILL.md` §1 Q4 → "if 2+ languages: run `astro-i18n-setup`"; add the
  skill to the §3 bundled-skills copy list (so multilingual handoffs are self-contained).
- `references/WEBSITE_ARCHITECTURE.md` Part 7 → point at this skill.

## Verify (scaffold a throwaway 2-locale site in /tmp)
```
npm run build
# dist/ has /index.html + /de.html (served /de) + nested /de/<page>.html
grep -o 'hreflang="[^"]*"' dist/index.html      # en, de, x-default present & reciprocal
grep -c '<xhtml:link' dist/sitemap-0.xml        # alternates present
npm test                                        # green, INCLUDING tests/i18n.spec.ts
```
Confirm: every page self-references + lists every locale its route exists in +
`x-default`; default-locale URLs are unchanged from a single-locale build; trailing
slashes are consistent (`/` keeps its slash, `/de` and sub-pages have none).

Testing a **sparse route**? Add `{ path: '/nur-de', locales: ['de'] }` to ROUTES,
create only `src/pages/de/nur-de.astro`, rebuild, and confirm: `/de/nur-de` emits
exactly one locale alternate + a self-referencing `x-default`; `npm test` stays
green with no EN variant anywhere; and `dist/sitemap-0.xml` carries no
`<xhtml:link>` pointing at a never-built `/nur-de` (the §1 `serialize` hook).
