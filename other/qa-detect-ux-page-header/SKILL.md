---
name: qa-detect-ux-page-header
section: visual
description: "Detects page-header layout problems — page title smaller than metric/content text (broken typographic hierarchy), page title sitting before the home icon in the breadcrumb row, page title text duplicated as a breadcrumb item, home icon not the first breadcrumb item, page title using same style as breadcrumb. Runs even when there is no breadcrumb. Goes beyond qa-detect-ux-breadcrumb which checks the breadcrumb itself in isolation."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `pageTitleBeforeBreadcrumbHome` | medium | A page title (h1/h2 with `pageTitle`/`page-title` class or `Purchase Order Report`-style heading) appears in the same horizontal band as a breadcrumb home icon, sitting BEFORE it — non-standard, confusing (your Purchase Order Report screenshot) |
| `pageTitleDuplicatedInBreadcrumb` | medium | The page title text matches one of the breadcrumb items (excluding the current-page item) — useless duplication |
| `breadcrumbHomeIconMidPath` | medium | The home (🏠) icon appears at position > 0 in the breadcrumb — should be the FIRST item, not in the middle |
| `pageTitleNoH1` | low | Page title is rendered with `<div>` or `<span>` instead of `<h1>` — breaks semantic structure |
| `pageTitleSameStyleAsBreadcrumb` | low | Page title font-size and weight match the breadcrumb items — no visual hierarchy between them |
| `pageHeaderSmallerThanContent` | medium | The page title's font-size is noticeably smaller than other prominent text on the page (metric values, body text, button labels). Page title should sit at the TOP of the typographic hierarchy. Your Dashboard screenshot: "Dashboard" at ~18px while "1225" metric at ~48px and other headings ~16-18px |

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = [];

  // Find page title candidates
  let pageTitle = null;
  const titleCandidates = [
    ...document.querySelectorAll('h1, h2, .page-title, .pageTitle, [class*="page-title"], [class*="pageTitle"], header > h1, header > h2'),
    ...document.querySelectorAll('main > h1, main > h2, [role="main"] > h1, [role="main"] > h2')
  ];
  for (const t of titleCandidates) {
    if (!visible(t)) continue;
    const txt = (t.innerText || '').trim();
    if (txt.length < 2 || txt.length > 80) continue;
    pageTitle = { el: t, text: txt };
    break;
  }

  // ── 0. Page header smaller than other content (runs WITHOUT a breadcrumb) ──
  //     Page title font-size must sit at the TOP of the typographic hierarchy.
  //     If any non-title prominent text is noticeably larger, flag it.
  if (pageTitle) {
    const titleCs = getComputedStyle(pageTitle.el);
    const titleFs = parseFloat(titleCs.fontSize);
    const titleFw = parseInt(titleCs.fontWeight) || 400;
    // Scan candidate "prominent" text: headings, .stat / .metric / .value / .number / .count, button labels, h1-h3
    const promptSel = 'h1, h2, h3, .stat, .metric, .value, .count, .number, .kpi, [class*="metric"], [class*="stat-value"], [class*="kpi"], [class*="count"], [class*="number"], button, .btn, [class*="card"] [class*="value"], [class*="card"] [class*="number"]';
    const candidates = [...document.querySelectorAll(promptSel)].filter(visible);
    let maxOtherFs = 0;
    let maxOtherEl = null;
    let maxOtherText = '';
    for (const c of candidates) {
      if (c === pageTitle.el || c.contains(pageTitle.el) || pageTitle.el.contains(c)) continue;
      const txt = (c.innerText || '').trim();
      if (txt.length < 1 || txt.length > 80) continue;
      const cs = getComputedStyle(c);
      const fs = parseFloat(cs.fontSize);
      // Only consider "prominent" text — font-weight >= 500 OR digit-only metric
      const fw = parseInt(cs.fontWeight) || 400;
      const isMetric = /^[\d.,$%]+$/.test(txt);
      if (!isMetric && fw < 500) continue;
      // Skip elements smaller than the title — we want the largest "other" text
      if (fs > maxOtherFs) {
        maxOtherFs = fs;
        maxOtherEl = c;
        maxOtherText = txt;
      }
    }
    // Flag when other content is >= 1.4× the title's font-size (title is clearly subordinate)
    if (maxOtherEl && maxOtherFs >= titleFs * 1.4 && maxOtherFs - titleFs >= 8) {
      out.push({
        issueType: 'pageHeaderSmallerThanContent', severity: 'medium',
        selector: sel(pageTitle.el), bbox: bb(pageTitle.el),
        description: `Page title "${pageTitle.text.slice(0, 40)}" is ${titleFs}px (weight ${titleFw}) but other prominent text "${maxOtherText.slice(0, 30)}" on the page is ${maxOtherFs}px — ${(maxOtherFs/titleFs).toFixed(1)}× larger. Page title should be the LARGEST text in the visual hierarchy. Bump page title to at least ${Math.round(Math.max(maxOtherFs * 0.7, 24))}px or restructure so the metric values do not visually compete with the page title.`
      });
    }
  }

  // Find breadcrumb
  const bcContainer = [...document.querySelectorAll('.breadcrumb, .breadcrumbs, [class*="breadcrumb"], nav[aria-label*="breadcrumb" i]')]
    .filter(visible)[0];

  if (!bcContainer) return out;

  // Get breadcrumb items + check for home icon position
  const items = [...bcContainer.querySelectorAll('a, span, li, .breadcrumb-item')]
    .filter(visible)
    .filter(el => {
      const t = (el.innerText || '').trim();
      const hasHomeIcon = el.querySelector('svg, i.fa-home, i[class*="home"], i.material-icons') ||
                         /home/i.test(el.getAttribute('aria-label') || '');
      return t.length > 0 || hasHomeIcon;
    })
    .filter((el, i, arr) => !arr.some(o => o !== el && el.contains(o)));

  // ── 1. Page title before breadcrumb home icon ────────────────────────
  if (pageTitle && items.length >= 1) {
    const titleR = pageTitle.el.getBoundingClientRect();
    const homeItem = items.find(it =>
      it.querySelector('svg[class*="home"], i.fa-home, i.material-icons') ||
      /home/i.test(it.getAttribute('aria-label') || '') ||
      (it.querySelector('svg') && it.querySelectorAll('svg').length === 1 && (it.innerText || '').trim() === '')
    );
    if (homeItem) {
      const homeR = homeItem.getBoundingClientRect();
      // Same horizontal band: title.bottom > home.top AND title.top < home.bottom
      const sameBand = titleR.bottom > homeR.top - 4 && titleR.top < homeR.bottom + 4;
      // Title is BEFORE home (left of it)
      if (sameBand && titleR.right < homeR.left + 4) {
        out.push({
          issueType: 'pageTitleBeforeBreadcrumbHome', severity: 'medium',
          selector: sel(pageTitle.el), bbox: bb(pageTitle.el),
          description: `Page title "${pageTitle.text.slice(0, 40)}" sits to the LEFT of the breadcrumb home icon in the same row. Convention: page title on its own line, OR home icon as the first breadcrumb item before any text label.`
        });
      }
    }
  }

  // ── 2. Page title duplicated in breadcrumb ──────────────────────────
  if (pageTitle) {
    const titleLow = pageTitle.text.toLowerCase().trim();
    // Find non-last breadcrumb items (exclude current-page item)
    const middleItems = items.slice(0, -1);
    const dup = middleItems.find(it => {
      const txt = (it.innerText || '').trim().toLowerCase();
      return txt.length > 0 && txt === titleLow;
    });
    if (dup) {
      out.push({
        issueType: 'pageTitleDuplicatedInBreadcrumb', severity: 'medium',
        selector: sel(dup), bbox: bb(dup),
        description: `Page title "${pageTitle.text.slice(0, 40)}" appears as a middle breadcrumb item. Useless duplication — either remove from breadcrumb or restructure the page hierarchy.`
      });
    }
  }

  // ── 3. Home icon not the first breadcrumb item ──────────────────────
  if (items.length >= 3) {
    let homeIdx = -1;
    for (let i = 0; i < items.length; i++) {
      const it = items[i];
      if (it.querySelector('svg[class*="home"], i.fa-home, i.material-icons') ||
          /home/i.test(it.getAttribute('aria-label') || '')) {
        // SVG with no obvious "home" class but standalone icon
        homeIdx = i;
        break;
      }
      // Heuristic: icon-only item (svg only, no text)
      const text = (it.innerText || '').trim();
      if (text === '' && it.querySelector('svg')) {
        homeIdx = i;
        break;
      }
    }
    if (homeIdx >= 1) {
      out.push({
        issueType: 'breadcrumbHomeIconMidPath', severity: 'medium',
        selector: sel(items[homeIdx]), bbox: bb(items[homeIdx]),
        description: `Home icon is at position ${homeIdx + 1} of ${items.length} in the breadcrumb. Convention: home should be the FIRST item.`
      });
    }
  }

  // ── 4. Page title using non-heading tag ─────────────────────────────
  if (pageTitle) {
    const tag = pageTitle.el.tagName;
    if (tag !== 'H1' && tag !== 'H2') {
      // Check it's the actual page title (large font + bold)
      const cs = getComputedStyle(pageTitle.el);
      const fs = parseFloat(cs.fontSize);
      const fw = parseInt(cs.fontWeight);
      if (fs >= 18 && fw >= 600) {
        out.push({
          issueType: 'pageTitleNoH1', severity: 'low',
          selector: sel(pageTitle.el), bbox: bb(pageTitle.el),
          description: `Page title "${pageTitle.text.slice(0, 40)}" rendered as <${tag.toLowerCase()}> instead of <h1> or <h2>. Hurts SEO + screen-reader navigation.`
        });
      }
    }
  }

  // ── 5. Page title same visual style as breadcrumb ───────────────────
  if (pageTitle && items.length > 0) {
    const titleCs = getComputedStyle(pageTitle.el);
    const itemCs = getComputedStyle(items[0]);
    const titleFs = parseFloat(titleCs.fontSize);
    const itemFs = parseFloat(itemCs.fontSize);
    const titleFw = parseInt(titleCs.fontWeight);
    const itemFw = parseInt(itemCs.fontWeight);
    const fsDelta = Math.abs(titleFs - itemFs);
    const fwDelta = Math.abs(titleFw - itemFw);
    if (fsDelta < 2 && fwDelta < 200) {
      out.push({
        issueType: 'pageTitleSameStyleAsBreadcrumb', severity: 'low',
        selector: sel(pageTitle.el), bbox: bb(pageTitle.el),
        description: `Page title and breadcrumb items have nearly identical font (size ${titleFs}px vs ${itemFs}px, weight ${titleFw} vs ${itemFw}). Make page title visibly larger/bolder.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max 5 findings per cell
- Self-skips: page with no breadcrumb container returns []
- The `pageTitleBeforeBreadcrumbHome` catches your Purchase Order Report screenshot — title sits before the home icon
- The `breadcrumbHomeIconMidPath` catches the "Fee > 🏠 > Fee Navigator" pattern from your Fee Navigator screenshot
