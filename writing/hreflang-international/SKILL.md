---
name: hreflang-international
description: Check or plan language and country versions of a site so search engines show each market the right page. Use for "hreflang errors", "Google shows the wrong country version", "set up a German site", "ccTLD vs subfolder", "x-default", or missing return links in hreflang tags.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/hreflang-international
---

# Hreflang and international setup

Check how a site serves different languages and countries, or plan it for a new
market: URL structure, hreflang annotations, canonicals, redirects and whether
each version is genuinely local. You hand back validated hreflang clusters, a
prioritised fix list and, for new markets, a setup plan a developer can build.

> **Romeo's rule:** Hreflang decides which version Google shows; it can't make
> a lazy translation worth showing.

## Use this when

- Searchers in one country land on another country's page (UK visitors on US prices, Austrians on the German shop).
- Search Console groups your same-language regional pages as duplicates and picks the wrong one.
- A crawler or validator reports hreflang errors: missing return links, invalid codes, non-canonical targets.
- You're launching a new language or country, or choosing between ccTLDs, subfolders and subdomains.

## Don't use this for

- Keyword research for a new market → `seo-opportunity-research`, run separately for each market in its language.
- Writing the localized pages → `seo-content-brief`, then `seo-blog-writer`.
- Moving existing pages into a new international URL structure → `site-migration-check` (plan the target here first).
- Cities or service areas inside one country → `local-seo-audit`.

## What you need

### Required
- The markets the business really serves (language plus country), and what differs between them: currency, prices, shipping, legal text, product range, support.
- The localized URLs, or the ability to fetch pages, headers and sitemaps.

### Helpful
- A crawler export with hreflang extracted (Screaming Frog, Sitebulb or similar).
- Search Console Performance filtered by country, with the Pages tab; Page indexing duplicate reasons.
- Bing Webmaster Tools data, if Bing matters in your markets.
- Existing keyword research per market, and the CMS or translation plugin in use.

### No tools?
- `view-source:` one page per locale and copy its `<link rel="alternate" hreflang>` block into a spreadsheet: one row per page, one column per code. Every row of a cluster should be identical.
- DevTools Network shows `Link:` headers (hreflang for PDFs) and any redirects triggered by your location or browser language. Retest in a private window with a different browser language.
- Search Console Performance: filter by country, open Pages, and see which locale URL gets the impressions in that country.
- Checking results from another country (VPN or a colleague there) is a hint, not proof; results vary by person.

## Ground rules

- Hreflang chooses between equivalent pages. It is not a ranking boost, and it won't make a weak page rank in a new market.
- Only canonical, indexable pages that return 200 belong in a cluster. Every target URL must be exactly its own canonical.
- Each version lists itself and every other version. Pairs that don't point at each other are ignored; the pairs that do still work.
- Pick one implementation method per set of URLs. Google treats HTML tags, HTTP headers and sitemaps as equivalent; using two only doubles the ways they drift apart.
- Never force-redirect by IP address or browser language. Googlebot mostly crawls from the US without an `Accept-Language` header, so it may never reach your other versions. Suggest with a banner; don't force.
- Research each market's keywords in its own language. Translating "cell phone" gives you neither the British "mobile phone" nor the German "Handy".
- Same-language regional versions need real differences (currency, prices, spelling, shipping, legal text) or Google may fold them together as duplicates.
- Google ignores the `lang` attribute and hreflang when detecting a page's language; it reads the visible content. Keep `lang` correct anyway for accessibility, browser translation and other engines.
- Don't recommend Search Console's International Targeting report (retired 2022, so hreflang errors now have to be found with a crawler or by hand), geo meta tags (ignored by Google), or translating only the navigation around untranslated content.

## Steps

1. **Map markets to URLs.** Build one line per market: code, URL pattern, currency, what's different.
   - Flag markets that share one identical page, and versions with no real market behind them, for example 30 machine-translated languages with no sales, support or traffic.
   - Agree the market list with the user before validating anything; hreflang only encodes decisions the business has made.

2. **Review the URL structure.**
   - Country domain (`example.de`): the clearest country signal, but each one builds authority from scratch, costs more to run and targets one country.
   - Subfolder (`example.com/de/`): easiest to run and shares the domain's strength. The sensible default for most sites.
   - Subdomain (`de.example.com`): fine when another team or platform runs it; often behaves like a separate site.
   - URL parameters (`?lang=de`), cookie-only switching, or one URL that changes language: not recommended. Google may only ever see one version: `Fix now` if a market depends on it.
   - Moving an established ccTLD setup to subfolders purely for tidiness is a migration with real risk and unclear upside: `Leave it` unless there's a business reason.

3. **Validate every code.**
   - Format: ISO 639-1 language, optionally a hyphen and an ISO 3166-1 alpha-2 region: `en`, `en-GB`, `pt-BR`, `es-MX`. Scripts use ISO 15924: `zh-Hant`, `zh-Hans`. Case doesn't matter.
   - Region only is invalid: `de-AT` works, `AT` alone does not.
   - Common mistakes: `en-UK` (use `en-GB`; `UK` is a reserved code and is ignored), `jp` (Japanese is `ja`), `cn` (use `zh-CN` or `zh-Hans`), `se` for Swedish (`sv`; `se` is Northern Sami), `dk` (`da`), `gr` (`el`), `en_GB` with an underscore.
   - `hreflang="uk"` means Ukrainian, not the United Kingdom. Check this one on every UK site.
   - Unsupported by Google: `es-419`, `EU`, `UN`. Annotate the actual countries instead, or use plain `es`.
   - Code doesn't match the page's real language (`fr` on an English page): `Fix now`.

4. **Check each cluster's integrity.** On large sites, check every template and a sample of URLs per template.
   - Self-reference present on every page.
   - Every member lists the same set. Report each missing return link as a URL pair.
   - Every target returns 200, is indexable, isn't disallowed, and exactly matches its canonical (protocol, host, trailing slash). Targets that redirect or 404: `Fix next`, `Fix now` if template-wide.
   - One URL per code per cluster. Two URLs both claiming `en-GB`: `Fix now`.
   - Targets are equivalent pages. Pointing every page's `de` alternate at the German homepage is wrong; if no equivalent exists, leave that locale out of that page's cluster.
   - `x-default` is optional: use it for a language selector or the global fallback, one per cluster.
   - Absolute URLs with `https://`. Alternates may sit on other domains.

5. **Check canonicals across locales.**
   - Each localized page canonicalises to itself. Pointing every locale's canonical at the English page tells Google to drop the others: `Fix now`, and a common, costly bug.
   - Same-language near-duplicates (`en-US`, `en-GB`, `en-AU` with identical copy) may show as "Duplicate, Google chose different canonical than user". Hreflang may still help the local URL appear, but don't rely on it: differentiate prices, currency, spelling, shipping and contact details, or merge the versions.

6. **Use one clean implementation method.**
   - HTML: `<link rel="alternate" hreflang="..." href="...">` in the `<head>` of the raw HTML. Simple for a few locales; it gets heavy at 20+.
   - HTTP `Link` header: for PDFs and other non-HTML files.
   - XML sitemap `xhtml:link`: best for large sites and many locales, generated by the same system that knows the canonicals. Checking it is covered by `xml-sitemap-check`.
   - Two methods present and disagreeing: `Fix now`. Two that agree: `Worth doing` to drop one.
   - Google stops reading `<head>` at the first element that doesn't belong there (an `<img>` or `<iframe>`, often injected by a tag manager or widget). Hreflang tags after it are lost: `Fix now` when found.
   - Example cluster, identical on all three pages:

   ```html
   <link rel="alternate" hreflang="en-US" href="https://www.example.com/pricing/" />
   <link rel="alternate" hreflang="en-GB" href="https://www.example.com/uk/pricing/" />
   <link rel="alternate" hreflang="de" href="https://www.example.com/de/preise/" />
   <link rel="alternate" hreflang="x-default" href="https://www.example.com/pricing/" />
   ```

7. **Check redirects and locale detection.**
   - Request every locale URL with no cookies, no `Accept-Language` and, if possible, a US IP. Each must return 200 with its own content. Any version that's unreachable this way: `Fix now`.
   - A root URL that picks a locale for the visitor is acceptable only if every locale URL stays directly reachable; mark that root as `x-default`.
   - Remember a visitor's explicit choice in a cookie, offer a dismissible "view the UK site?" banner, and keep a language and country switcher built from `<a href>` links to the equivalent page, not the homepage.

8. **Check that each version is actually local.**
   - Main content translated, not just navigation and buttons. Unreviewed machine translation published at scale is a quality risk; check Google's current spam policies on scaled content before recommending it.
   - Commerce details: currency and prices, tax display, shipping, returns, payment methods, legal and regulatory text, phone numbers and addresses, units, date formats, spelling.
   - Product structured data uses the locale's `priceCurrency` and matches the visible price.
   - Titles, meta descriptions and H1s come from that market's keyword research. Never invent search volumes for a market; write "not checked".
   - Internal links inside each locale stay in that locale.

9. **Measure, then write up.** In Search Console Performance, filter by country and note which URL earns impressions there. The wrong locale winning a market is the symptom you're fixing; recheck it after Google has recrawled the clusters. For new markets, write the setup plan: structure, codes, cluster template, `x-default`, method, switcher, redirect policy, research still needed, launch checks.

## What to hand back

Fill this in. Name URL pairs for every return-link or canonical problem.

```markdown
What I found: <one sentence>
What matters most: <the biggest problem and which markets it hits>
What to do first: <one concrete action>

Site: <site>, checked <date>
Markets: <code: URL pattern, currency, what differs> (one line each)
Method: <HTML | HTTP header | sitemap | mixed>. Clusters checked: <n> across <templates>

### Fixes
- [Fix now] <plain-English problem (term)>. Affects: <markets, template, count>.
  Evidence: <seen|tool|inferred>, <high|medium|low>: <URL pair or code seen>.
  Fix: <exact change, at the template, plugin or sitemap generator>.

### Wrong version showing
- <country>: <URL getting impressions> instead of <intended URL> (source: <Search Console | not checked>)

### Looks wrong, leave it
- <item>: <why>

### Setup plan (new markets only)
- Structure, codes, x-default, method, switcher, redirect policy, research needed

### What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- The business hasn't decided which markets it serves: ask before building clusters for every translation that happens to exist.
- Locale versions are force-redirected and you can't reach them: report what you could and couldn't fetch, and don't guess their markup.
- You're asked to change redirects, geo rules, CDN settings or templates: draft the change and ask permission for that specific change.
- Unacceptable output: invented keyword volumes per market, codes you haven't validated, or a plan that treats translating the English keyword list as localization.

## Next step

- `seo-opportunity-research` for each target market, in its own language, before writing localized pages.
- `xml-sitemap-check` if hreflang lives in the sitemaps, to validate the generated files.
- `seo-change-monitor` to watch which URL wins each country after the fixes ship.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
