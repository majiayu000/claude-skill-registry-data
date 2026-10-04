---
name: apply-page-language
description: Use when building any web page or SPA — to declare the language of the page and any inline content in a different language, so screen readers select the correct text-to-speech voice and language rules.
source: W3C WCAG 2.1 SC 3.1.1 Language of Page (Level A), SC 3.1.2 Language of Parts (Level AA); IETF BCP 47 language tag specification; MDN HTML lang attribute guide
tags: [accessibility, wcag, a11y, language, lang-attribute, screen-reader, internationalization, developer]
related: [write-semantic-html-structure, design-accessibility-standards]
---

# Apply Page Language

Declare the page language on `<html lang>` and mark inline content in a different language —
so screen readers use the correct pronunciation, TTS voice, and hyphenation rules.

## Why This Is Best Practice

**Adopted by:** WCAG 2.1 SC 3.1.1 (Level A, required universally) and SC 3.1.2 (Level AA, required
by Section 508 US, EU EN 301 549, UK PSBAR 2018). The HTML Living Standard and every major framework
(Next.js, Nuxt, SvelteKit, Angular) provide built-in mechanisms for setting `lang` as a baseline
HTML requirement. Google Lighthouse, axe-core, and WAVE all flag missing `lang` as a critical error.
**Impact:** Screen readers switch TTS voice engines based on the `lang` attribute — reading French
text with an English voice produces unintelligible output. NVDA, JAWS, and VoiceOver all implement
automatic language switching per the `lang` attribute. WebAIM's 2024 screen reader survey found 68%
of screen reader users rely on automatic language switching. Without `lang`, browsers also fail to
apply correct spell-check, hyphenation, and quotation mark rules for language-specific characters.
**Why best:** The HTTP `Content-Language` header and `<meta http-equiv="Content-Language">` cannot
substitute — screen readers do not use these for TTS voice selection. The `lang` attribute on HTML
elements is the only mechanism supported across all screen readers and browsers for per-element
language switching.

Sources: W3C WCAG 2.1 SC 3.1.1, 3.1.2 (2018); IETF BCP 47; MDN HTML lang; WebAIM Screen Reader
Survey 2024

## Steps

### Step 1: Set `lang` on every `<html>` element (3.1.1)

Every HTML page must have a valid BCP 47 language tag on the root element:

```html
<!-- Wrong — no lang, or invalid tag -->
<html>
<html lang="">
<html lang="english">    <!-- not a BCP 47 tag -->

<!-- Right — BCP 47 primary language subtag -->
<html lang="en">         <!-- English (any region) -->
<html lang="en-US">      <!-- English, United States — use when dialect matters -->
<html lang="fr">         <!-- French -->
<html lang="de">         <!-- German -->
<html lang="zh-Hans">    <!-- Chinese, Simplified -->
<html lang="ar">         <!-- Arabic -->
```

Use just the two-letter ISO 639-1 code (`en`, `fr`, `de`) unless a regional variant matters
for pronunciation (`en-US` vs `en-GB`, `pt-BR` vs `pt-PT`).

### Step 2: Mark inline content in a different language (3.1.2)

Any phrase, word, or passage in a language different from the page language needs a `lang`
attribute on its containing element:

```html
<!-- Page language: English -->
<html lang="en">
<body>

  <!-- Wrong — French phrase read with English TTS voice -->
  <p>The menu offered <em>carte blanche</em>.</p>

  <!-- Right — French phrase gets French TTS voice -->
  <p>The menu offered <em lang="fr">carte blanche</em>.</p>

  <!-- Right — foreign-language publication title -->
  <li><cite lang="de">Der Spiegel</cite> — German news magazine</li>

  <!-- Right — extended foreign-language block -->
  <blockquote lang="ja">
    <p>すべての人間は、生まれながらにして自由であり...</p>
  </blockquote>

</body>
```

Proper nouns — people's names, place names, brand names — do not need `lang`. They are
pronounced consistently regardless of surrounding language.

### Step 3: Update `lang` on SPA locale changes (3.1.1)

In SPAs where locale changes without a full page reload, update `document.documentElement.lang`:

```javascript
// React — update when locale changes
function App() {
  const { locale } = useLocale();

  useEffect(() => {
    document.documentElement.lang = locale; // e.g. "fr", "de", "ja"
  }, [locale]);

  return <RouterProvider router={router} />;
}
```

```javascript
// Vue Router — update on every navigation
router.afterEach((to) => {
  document.documentElement.setAttribute('lang', to.meta.locale ?? 'en');
});
```

Without this update, a user switching to French in a SPA hears English TTS voice reading
French content for the entire session.

### Step 4: Set `lang` in framework base templates

| Framework | Where to set `lang` |
|-----------|-------------------|
| Next.js (App Router) | `<html lang="en">` in `app/layout.tsx` |
| Next.js (Pages) | `i18n.defaultLocale` in `next.config.js` + `<html lang={locale}>` in `_document.js` |
| Nuxt | `app.head.htmlAttrs.lang` in `nuxt.config.ts` |
| SvelteKit | `<html lang="en">` in `src/app.html` |
| Angular | `<html lang="en">` in `src/index.html` |
| Create React App | `<html lang="en">` in `public/index.html` |
| Vite | `<html lang="en">` in `index.html` |

### Common BCP 47 tags

| Language | Tag | | Language | Tag |
|----------|-----|-|----------|-----|
| English | `en` | | Japanese | `ja` |
| English (US) | `en-US` | | Korean | `ko` |
| English (UK) | `en-GB` | | Arabic | `ar` |
| French | `fr` | | Hebrew | `he` |
| German | `de` | | Russian | `ru` |
| Spanish | `es` | | Chinese (Simplified) | `zh-Hans` |
| Portuguese (Brazil) | `pt-BR` | | Chinese (Traditional) | `zh-Hant` |

Full registry: IANA Language Subtag Registry (iana.org/assignments/language-subtag-registry)

## When NOT to Use

- **Proper nouns and brand names** — "Google", "Paris", "Marie Curie" don't need `lang` even
  inside foreign-language text.
- **Code snippets** — programming keywords (`const`, `function`) are not natural language.
  No `lang` needed on `<code>` blocks unless they contain natural-language strings in a
  foreign language.
- **Placeholder or decorative text** — content marked `aria-hidden="true"` doesn't need `lang`.

## Common Mistakes

**`lang` missing from `<html>`.** Most common failure — flagged by Axe, Lighthouse, and WAVE.
Add `lang="en"` (or correct language) to the `<html>` element in your base template immediately.

**Framework scaffold output lacks `lang`.** Create React App, Vite, and many starters omit `lang`.
Check your `index.html` or base layout file before deploying.

**`lang="en"` on a non-English page.** A French website with `lang="en"` reads the entire page
in English TTS voice. Verify `lang` matches actual content, not developer preference.

**`lang` not updated in multilingual SPAs.** When a user switches locale, `document.documentElement.lang`
must update. Static `lang="en"` in the HTML template is wrong when the page renders French content.