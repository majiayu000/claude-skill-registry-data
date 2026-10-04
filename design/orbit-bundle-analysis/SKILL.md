---
name: orbit-bundle-analysis
description: JavaScript / CSS bundle analysis for a WordPress plugin — total weight, per-chunk breakdown, source-map-explorer visualisation, unused CSS detection (PurgeCSS), tree-shake opportunities, and asset weight regression vs the previous release. Use when the user says "bundle size", "JS weight", "CSS bloat", "source map explorer", "PurgeCSS", "unused CSS", or after Webpack/Rollup refactor.
---

# 🪐 orbit-bundle-analysis — JS/CSS bundle profiler

Your plugin ships JavaScript and CSS to every site. 1MB on the homepage = 30,000 sites × 1MB = 30GB of bandwidth per day if your plugin has any traction. Trim it.

---

## Quick start

```bash
# Asset weight summary (per file, totals)
bash ~/Claude/orbit/scripts/check-asset-weight.sh ~/plugins/my-plugin

# Visual breakdown (JS only — needs source maps)
npx source-map-explorer assets/js/main.js

# Find unused CSS
purgecss --css assets/css/frontend.css --content http://localhost:8881 \
  --output reports/purgecss/
```

Or via gauntlet (Step 4):
```bash
bash scripts/gauntlet.sh --plugin . --mode quick
```

---

## What it reports

| Asset | Target | Bad |
|---|---|---|
| Total JS (all loaded on frontend) | < 100KB | > 300KB |
| Total CSS (all loaded) | < 50KB | > 150KB |
| Single largest JS file | < 80KB | > 200KB |
| Single largest CSS file | < 40KB | > 100KB |
| Unused CSS (% of shipped) | < 30% | > 60% |
| `console.log` in production JS | 0 | any |
| Source maps shipped to prod | No | Yes |

---

## Source-map-explorer (the visual tool)

```bash
# Generate sourcemaps in your build
# webpack: devtool: 'source-map'
# rollup: sourcemap: true

# Then run:
npx source-map-explorer assets/js/main.js
# → opens an interactive treemap in browser

# Save the SVG report
npx source-map-explorer assets/js/main.js --html reports/bundle-treemap.html
```

What it shows:
- Every imported module sized by its contribution to the final bundle
- Click any block → see exactly which import added what
- Hot tip: if `lodash` shows 70KB, you're importing the whole library — switch to `lodash-es` with named imports + tree-shake

---

## Common findings + fixes

### Importing all of lodash
```js
// BAD — pulls in 70KB
import _ from 'lodash';
_.map(arr, fn);

// GOOD — pulls in 2KB
import { map } from 'lodash-es';
map(arr, fn);
```

### Importing all of moment.js
```js
// BAD — moment.js is 67KB minified
import moment from 'moment';

// GOOD — date-fns: 2KB per function, tree-shakeable
import { format } from 'date-fns';
```

### Polyfills you don't need
```js
// BAD — shipping polyfills WP already has
import 'core-js/stable';
import 'regenerator-runtime/runtime';

// GOOD — target modern browsers only (WP supports modern enough)
// In .browserslistrc:
//   > 1%
//   not dead
//   not IE 11
```

### Unused dependencies
```bash
# Find them
npx depcheck

# → "Unused dependencies: jquery-ui-something" → npm uninstall
```

### Whole-file CSS imports
```scss
// BAD — pulls in everything
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

// GOOD — Tailwind v3 already tree-shakes by default. But verify:
purgecss --css dist/main.css --content "src/**/*.{js,php}" --output dist/purged/
```

### Source maps shipped to production
```bash
# Check
ls assets/js/*.map  # → these should NOT be in your release zip

# Fix in build config:
# webpack: devtool: false (production)
# rollup: sourcemap: false (production)
```

Plus add `*.map` to `.distignore` (WP.org submission).

---

## Asset weight regression

Compare current bundle vs the previous release:

```bash
bash ~/Claude/orbit/scripts/compare-versions.sh \
  --old ~/downloads/my-plugin-v2.3.zip \
  --new ~/downloads/my-plugin-v2.4.zip
```

Output:
```
Asset weight diff: v2.3 → v2.4

  JS:   238 KB → 287 KB  (+49 KB, +20.6%)  ⚠
  CSS:   42 KB →  51 KB  ( +9 KB, +21.4%)  ⚠

  Largest growers:
    + assets/js/main.js     +35 KB  (new lodash import?)
    + assets/css/admin.css   +6 KB  (new modal styles)
```

Any +20% growth in a release = sanity-check before shipping.

---

## CSS specificity audit

Specificity wars cause CSS bloat (devs add `!important` to override the override). Check:

```bash
# Count !important uses
grep -c '!important' assets/css/*.css
# → > 5 = code smell

# Specificity max
npx css-specificity assets/css/frontend.css | sort -nr | head
# → any value > 30 = nested too deep, refactor
```

---

## Best practices for WP plugins

1. **Enqueue conditionally** — don't load admin assets on frontend, don't load front assets on admin.
2. **Minify in production** — use `wp_register_script(..., '...', deps, ver, $in_footer)` with versioned URLs.
3. **Defer non-critical** — `wp_script_add_data($handle, 'strategy', 'defer')` (WP 6.3+).
4. **Bundle per-feature** — don't ship the whole plugin's JS on every page.
5. **HTTP/2 push** is overrated; cache headers + gzip/brotli are not.

---

## Output

```
[Bundle Analysis] my-plugin v2.4

JavaScript:
  ✓ frontend.min.js     42 KB   (gzip: 14 KB)
  ⚠ admin.min.js       180 KB   (gzip: 58 KB)  → review: large
  ✓ block-editor.js     28 KB   (gzip:  9 KB)

CSS:
  ✓ frontend.css        18 KB   (gzip:  5 KB)
  ✓ admin.css           36 KB   (gzip: 10 KB)
  ❌ admin.css unused: 47% of rules never apply
       Run: purgecss --css admin.css --content http://localhost:8881/wp-admin

Source maps in production: ✓ none found
console.log in production: ✓ none found

Total weight (frontend, gzipped): 19 KB ✓
Total weight (admin, gzipped):    73 KB ⚠
```

---

## Pair with `/orbit-lighthouse`

Lighthouse scores the **rendered page**. This skill profiles the **shipped assets**. Lighthouse says "reduce unused JavaScript by 250 KiB" — this skill tells you exactly which file and which import.
