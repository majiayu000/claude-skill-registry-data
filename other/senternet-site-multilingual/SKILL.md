---
name: senternet-site-multilingual
description: Add fully localized, URL-based multilingual support with prerendering, locale-correct structured data, hreflang, and SEO release gates.
---

# Multilingual / i18n Support

Add multi-language support with URL-based routing (`/es/`, `/fr/`), hreflang tags, localized prerendering, and Firebase Hosting i18n.

An indexable locale is a complete content release, not translated navigation wrapped around default-language content. Do not publish a locale prefix, prerender it, or add it to hreflang/sitemaps until every indexable route passes the translation and metadata gates below.

## Step 0: Gather language requirements

**Before writing any code**, ask the user:

> "Which languages do you want to support? English is the default (at `/`). List any additional languages you want — for example: Spanish, French, German, Japanese, Portuguese, Arabic, etc. I'll generate all routes, copy scaffolding, hreflang tags, and prerender config for each one."

Wait for their response. Then derive a locale config table like this (fill in based on their answer):

| Language    | Code | URL prefix | RTL? |
|-------------|------|------------|------|
| English     | `en` | `/`        | No   |
| Spanish     | `es` | `/es`      | No   |
| French      | `fr` | `/fr`      | No   |
| Arabic      | `ar` | `/ar`      | Yes  |
| …           | …    | …          | …    |

Use ISO 639-1 codes. For RTL languages (Arabic, Hebrew, Persian, Urdu), note them — they need `dir="rtl"` on `<html>`.

Show the table to the user and confirm before proceeding. Example:

> "Got it — I'll add support for English (default), Spanish (`/es`), and French (`/fr`). Proceeding with implementation."

---

## Architecture decision

This implementation uses:
- **URL prefix routing**: English at `/`, all other locales at `/{code}/` (not `?lang=es` query params)
- **React Context** for current language state
- **A single `i18n.ts` file** with all copy for all locales (not separate JSON files)
- **`window.__LANG__`** flag so the prerender script can force a specific locale during static generation
- **hreflang `<link>` tags** in the prerendered HTML so Google serves the right language
- **One locale-aware URL helper** shared by canonicals, hreflang, internal links, sitemap entries, and structured data
- **A publication gate** that keeps incomplete locale scaffolding out of indexable output

---

## Steps

### 1. Create `src/i18n.ts`

Build the file using the confirmed language list. The `Language` type must include every confirmed code. The `copy` object must have a key for every locale. The `languageNames` map must list every locale.

```typescript
import { createContext, createElement, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

// Replace with the union of all confirmed language codes, e.g. 'en' | 'es' | 'fr'
export type Language = 'en' | '<code2>' | '<code3>';

// All locale codes except English, used for URL prefix detection
const NON_DEFAULT_LOCALES: Language[] = ['<code2>', '<code3>'];

export interface LocaleCopy {
  languageLabel: string;
  languageNames: Record<Language, string>;
  nav: {
    home: string;
    about: string;
  };
  home: {
    meta: { title: string; description: string };
    hero: { headline: string; body: string; cta: string };
    // Add all copy keys for every page
  };
  // Add all pages
}

const copy: Record<Language, LocaleCopy> = {
  en: {
    languageLabel: 'Language',
    languageNames: {
      en: 'English',
      // Add native name for each additional locale, e.g. es: 'Español', fr: 'Français'
    },
    nav: { home: 'Home', about: 'About' },
    home: {
      meta: {
        title: 'APPNAME - Tagline',
        description: 'Description for search results.',
      },
      hero: {
        headline: 'Your headline here',
        body: 'Supporting copy here.',
        cta: 'Get started',
      },
    },
  },
  // Repeat for every additional locale with complete, reviewed translations.
  // Never publish placeholder or default-language fallback strings at locale URLs.
  '<code2>': {
    languageLabel: '…',          // "Language" in this language
    languageNames: { en: 'English', '<code2>': '…' },
    nav: { home: '…', about: '…' },
    home: {
      meta: { title: 'APPNAME - …', description: '…' },
      hero: { headline: '…', body: '…', cta: '…' },
    },
  },
};

const LanguageContext = createContext<{ language: Language; setLanguage: (l: Language) => void }>({
  language: 'en',
  setLanguage: () => {},
});

// All confirmed locale codes (including 'en') — keep in sync with ALL_LOCALES in MetaTags
const ALL_LOCALES: Language[] = ['en', ...NON_DEFAULT_LOCALES];

function detectLanguage(): Language {
  // 1. Prerender script injects window.__LANG__ before navigating to locale routes
  if (typeof window !== 'undefined' && (window as any).__LANG__) {
    return (window as any).__LANG__ as Language;
  }
  // 2. URL prefix — explicit locale in the path takes priority over any stored preference
  if (typeof window !== 'undefined') {
    for (const code of NON_DEFAULT_LOCALES) {
      if (window.location.pathname.startsWith(`/${code}`)) return code;
    }
  }
  // 3. Explicit user override stored in localStorage by the language switcher
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('lang') as Language | null;
    if (stored && (ALL_LOCALES as string[]).includes(stored)) return stored;
  }
  // 4. Browser Accept-Language preference (navigator.languages mirrors the header)
  if (typeof window !== 'undefined' && navigator.languages?.length) {
    for (const lang of navigator.languages) {
      const code = lang.split('-')[0] as Language;
      if ((NON_DEFAULT_LOCALES as string[]).includes(code)) return code;
    }
  }
  return 'en';
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(detectLanguage);
  useEffect(() => {
    const newLang = detectLanguage();
    if (newLang !== language) setLanguage(newLang);
  }, [typeof window !== 'undefined' ? window.location.pathname : '']);
  return createElement(LanguageContext.Provider, { value: { language, setLanguage } }, children);
}

export function useLanguage() {
  return useContext(LanguageContext);
}

export function useCopy(): LocaleCopy {
  const { language } = useLanguage();
  return useMemo(() => copy[language], [language]);
}
```

### 2. Update `src/App.tsx` for locale routing

Add a route group for every non-default locale. English routes stay at root.

```tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './i18n';

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          {/* English (default) routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />

          {/* Repeat the block below for every additional locale */}
          <Route path="/es" element={<HomePage />} />
          <Route path="/es/about" element={<AboutPage />} />

          <Route path="/fr" element={<HomePage />} />
          <Route path="/fr/about" element={<AboutPage />} />

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}
```

### 3. Use copy in page components

No change needed in component logic — `useCopy()` returns the right locale automatically.

```tsx
import { useCopy } from '../i18n';

function HomePage() {
  const t = useCopy();
  return (
    <>
      <MetaTags title={t.home.meta.title} description={t.home.meta.description} />
      <h1>{t.home.hero.headline}</h1>
      <p>{t.home.hero.body}</p>
    </>
  );
}
```

Apply the same rule to every indexable route and every content source, not only top-level UI components:

- article titles, summaries, dates, headings, body paragraphs, lists, captions, and image alt text
- project detail metadata, introductions, sections, pricing labels, CTAs, and related links
- About, legal, tool, comparison, landing, tag, and pagination pages
- strings stored in route registries, post/project data modules, component constants, and schema builders

Do not leave `POST_TITLE`, `POST_DESCRIPTION`, project data, or article bodies hardcoded in the default language while only translating the surrounding template. If a route has long-form content, model that content in the locale layer or a locale-specific content module and render it from the active locale.

### 3a. Gate incomplete locales before creating URLs

Maintain an explicit coverage matrix of route IDs × locales. A locale is publishable only when every indexable route has complete visible copy, metadata, image text, and schema labels.

If translations are incomplete:

- keep the locale disabled in the published locale list
- do not register its routes, prerender them, add hreflang alternates, or emit sitemap URLs
- do not publish fallback English bodies under locale-prefixed URLs
- do not use cross-locale canonicals or `noindex` as a substitute for finishing the translation

It is fine to scaffold an unpublished locale behind a separate development-only list, but the production `PUBLISHED_LOCALES` list must contain only complete locales.

### 4. Add hreflang links in MetaTags (or `usePageHead`)

Generate one `<link rel="alternate">` per locale plus `x-default`. Build the list dynamically from the confirmed locale codes.

```tsx
// All confirmed locale codes (including 'en')
const ALL_LOCALES: Language[] = ['en', '<code2>', '<code3>'];

const origin = import.meta.env.VITE_BASE_URL || window.location.origin;

// Strip any locale prefix to get the canonical English path
const stripLocale = (path: string) => {
  for (const code of NON_DEFAULT_LOCALES) {
    if (path.startsWith(`/${code}`)) return path.slice(code.length + 1) || '/';
  }
  return path;
};

const englishPath = stripLocale(currentPath);

ALL_LOCALES.forEach((code) => {
  const href = code === 'en'
    ? `${origin}${englishPath}`
    : `${origin}/${code}${englishPath === '/' ? '' : englishPath}`;
  setAlternate(code, href);
});
setAlternate('x-default', `${origin}${englishPath}`);
```

Use this same localized canonical URL in structured data. Every localized page's page-specific `@id`, `url`, `mainEntityOfPage`, and breadcrumb `item` must reference the localized canonical, not the English URL. Global entities such as the author `Person` or publisher `Organization` may keep one stable site-wide `@id`.

```tsx
const canonicalPath = localizePath(basePath, language);
const canonicalUrl = `${origin}${canonicalPath}`;

const schema = {
  '@type': 'BlogPosting',
  headline: t.title,
  description: t.description,
  mainEntityOfPage: { '@type': 'WebPage', '@id': canonicalUrl },
};

const breadcrumbs = [
  { '@type': 'ListItem', position: 1, name: t.home, item: `${origin}${localizePath('/', language)}` },
  { '@type': 'ListItem', position: 2, name: t.blog, item: `${origin}${localizePath('/blog', language)}` },
  { '@type': 'ListItem', position: 3, name: t.title, item: canonicalUrl },
];
```

### 5. Update the prerender script for locales

Build the `LOCALES` array from the confirmed list and loop over all routes × all locales.

```js
// One entry per locale. English has an empty dir prefix.
const LOCALES = [
  { language: 'en', dir: '' },
  { language: '<code2>', dir: '<code2>' },
  { language: '<code3>', dir: '<code3>' },
  // Add one entry per additional locale
];

for (const locale of LOCALES) {
  // Clear stale locale output before re-rendering
  if (locale.dir) {
    fs.rmSync(path.join(buildDir, locale.dir), { recursive: true, force: true });
  }

  for (const route of ROUTES) {
    const page = await browser.newPage();
    if (locale.language !== 'en') {
      await page.evaluateOnNewDocument((lang) => { window.__LANG__ = lang; }, locale.language);
    }
    const requestPath = locale.dir
      ? `/${locale.dir}${route === '/' ? '' : route}`
      : route;
    await page.goto(`http://localhost:9999${requestPath}`, { waitUntil: 'networkidle2' });
    // ... render and save HTML
    const outDir = locale.dir
      ? path.join(buildDir, locale.dir, route === '/' ? '' : route.slice(1))
      : (route === '/' ? buildDir : path.join(buildDir, route.slice(1)));
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'index.html'), html);
  }
}
```

### 6. Update the sitemap with hreflang alternates

See the `senternet-site-sitemap` skill — the `LOCALES` array drives `<xhtml:link>` alternates automatically. Pass the same locale list.

### 7. Language switcher component

Build the switcher from the locale list — do not hardcode a binary EN↔ES toggle.

```tsx
import { useLanguage, type Language } from '../i18n';

const LOCALE_LABELS: Record<Language, string> = {
  en: 'English',
  '<code2>': '…',  // native name
  '<code3>': '…',
};

const NON_DEFAULT_LOCALES: Language[] = ['<code2>', '<code3>'];

function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  const switchTo = (lang: Language) => {
    localStorage.setItem('lang', lang);
    setLanguage(lang);
    const current = window.location.pathname;
    // Strip any existing locale prefix
    const basePath = NON_DEFAULT_LOCALES.reduce(
      (p, code) => (p.startsWith(`/${code}`) ? p.slice(code.length + 1) || '/' : p),
      current
    );
    const newPath = lang === 'en' ? basePath : `/${lang}${basePath === '/' ? '' : basePath}`;
    // Locale pages are distinct prerendered documents. Force a document navigation so
    // the browser loads and hydrates the target locale's HTML and metadata.
    window.location.assign(newPath);
  };

  return (
    <select value={language} onChange={(e) => switchTo(e.target.value as Language)}>
      {(Object.entries(LOCALE_LABELS) as [Language, string][]).map(([code, label]) => (
        <option key={code} value={code}>{label}</option>
      ))}
    </select>
  );
}
```

### 8. RTL support (if applicable)

For any RTL locale (Arabic, Hebrew, Persian, Urdu), add `dir` to `<html>` based on the active language:

```tsx
const RTL_LOCALES: Language[] = [/* list RTL codes here, e.g. 'ar', 'he' */];

useEffect(() => {
  document.documentElement.dir = RTL_LOCALES.includes(language) ? 'rtl' : 'ltr';
  document.documentElement.lang = language;
}, [language]);
```

### 9. Add multilingual SEO regression tests

Add tests that inspect the production prerender output, not only React source. For every published route × locale, assert:

- the output file exists and contains meaningful rendered content
- `<html lang>` and `dir` match the locale (`zh-Hans` is preferred for Simplified Chinese)
- the canonical is the page's own locale URL
- the page has exactly one H1 plus non-empty localized title and description
- the hreflang set contains every published locale, itself, and `x-default`, with identical reciprocal targets
- every hreflang target exists in the build and is indexable
- JSON-LD parses and page-specific `@id`, `url`, `mainEntityOfPage`, and breadcrumbs use the localized canonical
- the localized main-content text is not byte-for-byte or normalized-text identical to the English version
- route/content coverage has no fallback default-language values for published locales
- title-length checks flag likely truncation for human review rather than silently accepting oversized translated titles

Make the tests enumerate route/content registries so adding a new post, project, or locale automatically expands coverage. A test that checks only one sample route is insufficient.

After the build, crawl the full generated sitemap and fail the task if any URL redirects, 404s, cross-canonicalizes, omits a return hreflang, has invalid JSON-LD, or contains untranslated main content.

---

## Notes

- All visitor-facing copy must come from a locale-aware source — never hardcode default-language page content in components
- Every published locale needs a complete entry for every indexable route; TypeScript shape checks are necessary but do not prove that fallback English values are absent
- Placeholder translations are development scaffolding only and must never enter `PUBLISHED_LOCALES`
- The prerender script must clear each locale's output directory before re-rendering to avoid stale pages
- Firebase Hosting's `"i18n": { "root": "/" }` config is optional — URL prefix routing handles i18n at the app level
- After adding translations: run the full production build and the multilingual SEO regression suite, then inspect representative deep pages in each locale

### Language detection priority

`detectLanguage()` resolves the active locale in this order:

1. **`window.__LANG__`** — injected by the prerender script; always wins
2. **URL prefix** — `/es/`, `/fr/`, etc.; takes precedence over any stored preference so that shared locale links always work
3. **`localStorage.lang`** — written by the language switcher; persists explicit user choice across sessions
4. **`navigator.languages`** — browser's Accept-Language preference; first matching supported locale wins
5. **`'en'`** — hardcoded default

The language switcher writes `localStorage.lang` before navigating, so a user who picks a language at `/` is remembered on their next visit even if they land on `/` again.

## Framework: Next.js track

The URL structure and hreflang policy are unchanged (`/es/...` prefixes, `x-default` pointing at English). The mechanism is the router, not a context provider plus prerender loop.

- Move routes under a dynamic segment: `app/[locale]/page.tsx`, `app/[locale]/about/page.tsx`. Export `generateStaticParams()` returning the locale list so every locale is rendered statically at build time.
- Use a library built for the App Router (e.g. `next-intl`) for message loading and locale detection, rather than the `LanguageProvider` pattern. Do not add `i18next` wired through a client context — it forces the whole tree client-side.
- Locale detection and redirects go in `middleware.ts`.
- `hreflang` comes from `alternates.languages` in each page's `metadata`, and must match the alternates emitted by `app/sitemap.ts`. Set both from the same locale list.
- Localize page-specific JSON-LD URLs and breadcrumb items from the same canonical URL helper used by `metadata.alternates`.
- Generate static params and sitemap entries only from `PUBLISHED_LOCALES`; incomplete locale message files must not create public routes.
- Extend `config/routes.mjs` with the locale prefixes so the sitemap and IndexNow cover every localized URL.
- There is no `/es/` loop to add to a prerender script, because there is no prerender script.

See `/senternet-site-framework` for the full convention map.
