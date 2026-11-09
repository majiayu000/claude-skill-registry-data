---
name: "qa-testing"
description: "Run QA testing on a page, feature, or full site at one of three depth tiers (smoke, standard, full). Use this skill whenever the user asks to QA a page or site, run a smoke test after a deploy, verify a page before launch, or run a regression sweep. Triggers on QA, QA sweep, smoke test, regression test, post-deploy check, pre-launch check, verify the deploy, test this page, does the page render, broken link, 404, image not loading. Also triggers proactively after a deploy or a new page launch where verification matters. Covers accessibility, performance, and SEO at the surface-signal level only: deep audits belong to `accessibility-audit`, `performance-optimization`, and `seo-technical`, and code-level debugging to `code-review-web`."
---

# QA Testing

Verify that a page, feature, or site is working before declaring it shipped. Stack-agnostic. Console-snippet driven for speed.

This skill is faster than `accessibility-audit` (which goes deeper on WCAG) and `performance-optimization` (which goes deeper on Core Web Vitals). Use this skill for general QA. Use the specialists for deep audits.

---

## When to use

- After every deploy (smoke test)
- After launching a new page or feature (standard audit)
- Before a major release (full release matrix)
- Investigating a "something looks off" report
- Pre-launch verification of a site or section

## When NOT to use

- Deep accessibility compliance work (use `accessibility-audit`)
- Deep performance investigation (use `performance-optimization`)
- Code review or debugging (use `code-review-web`)
- Initial site setup or technical SEO baseline (use `seo-technical`)

---

## Required inputs

- The page URL or site under test
- The tier of QA needed (smoke, standard, or full)
- Browser dev tools access
- Any specific concerns to check beyond the standard tier

---

## The framework: 3 tiers

QA scales with the stakes. Pick the tier that matches the context.

| Tier | When to run | Time | Coverage |
|---|---|---|---|
| Smoke | After every deploy | 2 minutes | Critical signals only |
| Standard | New page or feature | 10 minutes | On-page basics, accessibility, structure |
| Full | Major release, pre-launch | 30+ minutes | Comprehensive across all dimensions |

### Tier 1: Smoke test

The 2-minute "did the deploy break anything obvious?" check. Run after every deploy.

Console snippet (paste in browser dev tools):

```javascript
const smoke = {
  title: document.title,
  titleLen: document.title.length,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  h1Count: document.querySelectorAll('h1').length,
  missingAlts: [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
  schema: [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map(s => { try { return JSON.parse(s.innerText)['@type'] } catch(e) { return 'invalid' } }),
  // Незавершённая загрузка, в том числе lazy-loading, не доказывает ошибку.
  pendingImages: [...document.querySelectorAll('img')].filter(i => !i.complete).length,
  brokenImages: [...document.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth === 0).length,
};
console.log(JSON.stringify(smoke, null, 2));
```

**Pass criteria:**
- A meaningful title exists. Length is an editorial recommendation appropriate to the language and page, not a release blocker.
- For indexable public pages, inspect canonical against the intended production URL. For test, authenticated or embedded surfaces assess the documented indexing policy; do not require a canonical when inapplicable.
- Heading hierarchy communicates the page structure; report contextual issues rather than failing solely on H1 count.
- Zero images missing the `alt` attribute. An empty `alt=""` on a decorative image is correct markup and passes; only an absent attribute fails.
- Zero confirmed broken required images after allowing bounded loading time; report pending and intentionally unloaded lazy images separately.
- Every schema block parses (no `invalid` entries in the snippet output). Whether the types are the right ones for the page is a Full-tier check, against the Rich Results Test.

Classify findings by user impact. Continue independent checks; stop only a flow whose prerequisite is broken or whose execution would be unsafe. Do not modify production code during an audit unless a fix is authorized.

### Tier 2: Standard page audit

The 10-minute new-page-or-feature audit. Covers the on-page basics plus accessibility and structure.

Console snippet:

```javascript
const audit = {
  title: document.title,
  titleLen: document.title.length,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  metaDesc: document.querySelector('meta[name="description"]')?.content,
  metaDescLen: document.querySelector('meta[name="description"]')?.content?.length,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  ogTitle: document.querySelector('meta[property="og:title"]')?.content,
  twitterCard: document.querySelector('meta[name="twitter:card"]')?.content,
  h1Count: document.querySelectorAll('h1').length,
  h1Text: document.querySelector('h1')?.innerText,
  h2Count: document.querySelectorAll('h2').length,
  h2s: [...document.querySelectorAll('h2')].map(h => h.innerText.trim().slice(0, 60)),
  totalImages: document.querySelectorAll('img').length,
  missingAlts: [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
  // Незавершённая загрузка, в том числе lazy-loading, не доказывает ошибку.
  pendingImages: [...document.querySelectorAll('img')].filter(i => !i.complete).length,
  brokenImages: [...document.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth === 0).length,
  externalLinksWithoutNoopener: [...document.querySelectorAll('a[target="_blank"]')]
    .filter(a => !a.rel?.includes('noopener')).length,
  schema: [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map(s => {
      try {
        const d = JSON.parse(s.innerText);
        return d['@graph'] ? d['@graph'].map(x => x['@type']) : d['@type'];
      } catch(e) { return 'invalid' }
    }),
  // Это кандидаты, а не доказательство доступности: текст может быть на любом языке.
  skipLinkCandidates: [...document.querySelectorAll('a[href^="#"]')]
    .filter(a => {
      try { return !!document.getElementById(decodeURIComponent(a.hash.slice(1))); }
      catch { return false; }
    }).map(a => ({ text: a.textContent.trim(), target: a.hash })),
  pageLanguage: document.documentElement.lang || 'NOT SET',
  hasFavicon: !!document.querySelector('link[rel*="icon"]'),
};
console.log(JSON.stringify(audit, null, 2));
```

**Pass criteria** (in addition to smoke):
- Review meta description for page relevance; length is a recommendation, not a universal pass/fail threshold.
- For pages intended for social sharing, review applicable og:image, og:title and twitter:card metadata; otherwise mark not applicable.
- Where the page has subsections, headings describe them; a short single-section page need not have H2s.
- All external links with `target="_blank"` have `rel="noopener"`
- Page language declared (`lang` attribute on `<html>`)
- Review favicon when applicable to the surface; absence is not by itself a functional blocker.

### Tier 3: Full release matrix

The 30-minute pre-launch check. Cover all dimensions.

| Dimension | Pass criteria |
|---|---|
| Smoke and standard | All pass |
| Accessibility (basic) | Run browser audit tool (e.g., Lighthouse), score above 90 |
| Performance (basic) | Every threshold in the report template's Performance checklist, INP included |
| Mobile responsiveness | Every viewport in the report template's responsiveness checklist |
| Cross-browser | Tested in Chrome, Safari, Firefox (and Edge if relevant audience) |
| Forms | All forms submit successfully and validate correctly |
| Internal links | No broken internal links (sample 20 random) |
| External links | All return 200 (sample 10) |
| Sitemap | Returns 200, lists canonical URLs only |
| robots.txt | Allows production crawlers, blocks staging if applicable |
| Security headers | HSTS, X-Frame-Options, X-Content-Type-Options present |
| HTTPS | All resources load over HTTPS, no mixed content |
| 404 handling | 404 pages return HTTP 404 (not soft 200) |
| Schema validation | All schema validates in Rich Results Test |
| Analytics | Events fire as expected on key user actions |
| Cache behavior | Cache headers appropriate for page type |

For headers, run:

```javascript
fetch(window.location.origin, { method: 'HEAD' })
  .then(r => {
    const headers = {};
    for (const [k, v] of r.headers.entries()) headers[k] = v;
    console.log(JSON.stringify(headers, null, 2));
  });
```

Look for: `strict-transport-security`, `x-frame-options`, `x-content-type-options`.

---

## Specific QA snippets

### Image audit

```javascript
const imgs = [...document.querySelectorAll('img')].map(i => ({
  src: i.src.split('/').pop().split('?')[0].slice(0, 60),
  alt: i.hasAttribute('alt') ? (i.alt === '' ? 'DECORATIVE (empty alt)' : i.alt) : 'MISSING',
  width: i.naturalWidth,
  height: i.naturalHeight,
  // Три состояния позволяют отличить ожидание загрузки от подтверждённого отказа.
  state: !i.complete ? 'pending' : i.naturalWidth > 0 ? 'loaded' : 'broken',
}));
console.table(imgs);
console.log({
  total: imgs.length,
  broken: imgs.filter(i => i.state === 'broken').length,
  pending: imgs.filter(i => i.state === 'pending').length,
  noAlt: imgs.filter(i => i.alt === 'MISSING').length,
  decorative: imgs.filter(i => i.alt.startsWith('DECORATIVE')).length,
});
```

### Heading hierarchy check

```javascript
const headings = [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].map(h => ({
  level: parseInt(h.tagName[1]),
  text: h.innerText.trim().slice(0, 80),
}));
console.table(headings);

// Check for skipped levels
const levels = headings.map(h => h.level);
let skipped = false;
for (let i = 1; i < levels.length; i++) {
  if (levels[i] > levels[i-1] + 1) {
    console.warn(`Skipped from H${levels[i-1]} to H${levels[i]}: "${headings[i].text}"`);
    skipped = true;
  }
}
if (!skipped) console.log('No skipped heading levels');
```

### Contrast spot-check

```javascript
function contrast(bg, fg) {
  function lum(hex) {
    return [hex.slice(1,3), hex.slice(3,5), hex.slice(5,7)]
      .map(h => parseInt(h, 16) / 255)
      .map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4))
      .reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  }
  const [l1, l2] = [lum(bg), lum(fg)];
  const r = ((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)).toFixed(2);
  return r + ':1 ' + (parseFloat(r) >= 4.5 ? 'PASS body' : parseFloat(r) >= 3 ? 'PASS large only' : 'FAIL');
}

// Examples
contrast('#FFFFFF', '#4B5563'); // body color check
contrast('#FFFFFF', '#9CA3AF'); // verify gray choices
```

### Form audit (per form)

```javascript
[...document.querySelectorAll('form')].forEach((form, i) => {
  const fields = [...form.querySelectorAll('input, select, textarea')].map(field => ({
    type: field.type || field.tagName.toLowerCase(),
    name: field.name,
    hasLabel: !!form.querySelector(`label[for="${field.id}"]`) || !!field.closest('label'),
    required: field.required,
  }));
  console.log(`Form ${i + 1}:`);
  console.table(fields);
});
```

### External link audit

```javascript
const externalLinks = [...document.querySelectorAll('a[href^="http"]')]
  // Сравниваем hostname, иначе example.com.evil.test ошибочно окажется внутренним.
  .filter(a => new URL(a.href, window.location.href).hostname !== window.location.hostname);
const issues = externalLinks.filter(a =>
  a.target === '_blank' && !a.rel?.split(/\s+/).includes('noopener')
);
if (issues.length) {
  console.warn(`${issues.length} external links to review for explicit noopener:`);
  issues.forEach(a => console.warn(a.href));
} else {
  console.log(`No missing explicit noopener among ${externalLinks.length} inspected external links`);
}
```

---

## Workflow

1. **Pick the tier.** Smoke for routine deploys. Standard for new work. Full for releases.
2. **Run the snippet.** Paste the appropriate console snippet, review output.
3. **Note failures.** Each failure either gets fixed before ship or filed as a known issue.
4. **For Standard tier**, add: visual review at 375px, 768px, and 1440px. Standard deliberately skips 1024px; the Full tier picks it up with the rest of the template's responsiveness checklist. Test the primary user flow.
5. **For Full tier**, add: cross-browser testing, Lighthouse audit, schema validation, security headers, 404 handling.
6. **Document.** Use the template in [`references/qa-report-template.md`](references/qa-report-template.md) for full audits.

---

## Failure patterns

- **Skipping smoke tests on "small" deploys.** Half of broken-production incidents start with a deploy that "looked safe."
- **Running snippets but not reading the output.** The console snippet is a tool. The judgment is reading what it returns.
- **Visual-only QA.** Eyeballing a page misses missing alt text, broken schema, missing canonical. Always run the snippet.
- **Single-browser testing.** Mobile Safari and Chrome differ enough to surprise you. Test at least Chrome and Safari.
- **No mobile QA.** The 375px viewport is where most users live. Test there or get burned later.
- **Pass-fail with no remediation.** A failed QA must produce a fix or a known-issue ticket. Failed QA that ships unfixed is process theater.

---

## Output format

For smoke tests: console output is the report.

For standard and full audits: a markdown report at `qa-report-[date].md`. Use the template in [`references/qa-report-template.md`](references/qa-report-template.md).

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/qa-report-template.md`](references/qa-report-template.md) - Markdown report template for standard and full audits.


## Interpretation and safe execution

Treat snippets as diagnostic signals, not certification. For skip links, use the keyboard to verify visibility on focus, a meaningful accessible name in the page language, and movement past repeated navigation to main content. A matching anchor alone does not pass this check. For images, scroll relevant lazy content into view and wait within a bounded deadline before distinguishing failed from pending loads.

Select applicable checks for the actual surface: marketing pages, authenticated apps and embedded tools need different SEO/social requirements. Automated accessibility scores supplement manual checks; they do not prove conformance. Use available browser capabilities without assuming a specific plugin is installed. Report missing browser coverage as unverified. Form submissions, bookings and purchases must use an authorized test environment or be explicitly in scope.

The link snippet checks an explicit rel convention, not exploitability across every browser. Assess actual opener behavior for supported targets. Do not require noreferrer unless the intended referrer/privacy policy calls for suppressing referral information.

## Regression checks

Run `node tests/qa-snippets.test.cjs` from this skill directory. The [fixture tests](tests/qa-snippets.test.cjs) execute the actual snippets for pending/broken images, localized anchors and external hostnames. They do not replace a real browser accessibility audit.
