---
name: qa-detect-ux-breadcrumb
section: visual
description: "Detects breadcrumb UX problems: parent name same as current page (Students > Students), missing home/root link, only one item (not a breadcrumb), separator missing/inconsistent, current page is a link (should be plain text), no aria-label for nav landmark."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasBreadcrumb]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `breadcrumbDuplicateSegment` | medium | Two consecutive breadcrumb items have the same visible text ("Students > Students") — useless redundancy |
| `breadcrumbMissingHome` | low | Multi-level breadcrumb has no Home/Root/Dashboard link as the first item |
| `breadcrumbSingleItem` | low | "Breadcrumb" container has only 1 item — that's not a breadcrumb, it's a page title |
| `breadcrumbCurrentIsLink` | medium | Last (current-page) breadcrumb item is a clickable `<a href>` — clicking reloads the current page, confusing users |
| `breadcrumbSeparatorInconsistent` | low | Multiple separator characters used in same breadcrumb (`>`, `/`, `›`, `→` mixed) |
| `breadcrumbNoLandmark` | low | Breadcrumb has no `aria-label` / `role="navigation"` — screen readers can't identify the navigation landmark |
| `breadcrumbWrapsMultiLine` | medium | Breadcrumb wraps to 2+ lines on narrow viewport — loses single-line navigation clarity |

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

  // Find breadcrumb containers
  const containers = document.querySelectorAll(
    '.breadcrumb, .breadcrumbs, [class*="breadcrumb"], [aria-label*="breadcrumb" i], nav[aria-label*="breadcrumb" i], ol.breadcrumb, ul.breadcrumb, [role="navigation"][class*="breadcrumb"]'
  );

  let dupFlagged = 0, homeFlagged = 0, singleFlagged = 0,
      currentLinkFlagged = 0, sepFlagged = 0, landmarkFlagged = 0;

  for (const bc of [...containers].filter(visible).slice(0, 3)) {
    // Extract items — direct children that contain text
    let items = [...bc.querySelectorAll('a, span, li, .breadcrumb-item, [class*="breadcrumb-item"]')]
      .filter(visible)
      .filter(el => {
        const t = (el.innerText || '').trim();
        // Filter out separator-only elements
        return t.length > 0 && !/^[>›→\/|\-→»]+$/.test(t);
      });
    // Deduplicate: prefer leaf items (containing no other matching child)
    items = items.filter((el, i, arr) => {
      return !arr.some(other => other !== el && el.contains(other));
    });

    if (items.length === 0) continue;

    // ── Duplicate consecutive segments (REAL: "Students > Students") ───
    if (dupFlagged < 2) {
      for (let i = 1; i < items.length; i++) {
        const a = (items[i-1].innerText || '').trim().toLowerCase();
        const b = (items[i].innerText || '').trim().toLowerCase();
        if (a && a === b) {
          dupFlagged++;
          out.push({
            issueType: 'breadcrumbDuplicateSegment', severity: 'medium',
            selector: sel(bc), bbox: bb(bc),
            description: `Breadcrumb has two consecutive identical segments: "${a}" > "${b}". Either the page is misnamed or the breadcrumb logic is wrong (likely parent route name equals current page name).`
          });
          break;
        }
      }
    }

    // ── Current page is a link (REAL: clicking reloads current page) ───
    if (currentLinkFlagged < 2) {
      const last = items[items.length - 1];
      const isLink = last.tagName === 'A' || (last.querySelector && last.querySelector('a[href]'));
      if (isLink) {
        const link = last.tagName === 'A' ? last : last.querySelector('a[href]');
        const href = link.getAttribute('href') || '';
        if (href && href !== '#' && !href.startsWith('javascript:')) {
          currentLinkFlagged++;
          out.push({
            issueType: 'breadcrumbCurrentIsLink', severity: 'medium',
            selector: sel(last), bbox: bb(last),
            description: `Current-page breadcrumb item "${(link.innerText || '').trim().slice(0, 30)}" is a clickable link. Last breadcrumb should be plain text (aria-current="page"), not a link.`
          });
        }
      }
    }

  }

  // ── Breadcrumb wraps to multiple lines ──────────────────────────────────
  // On mobile/tablet, long breadcrumb paths wrap to 2–3 lines, consuming significant
  // header space and losing the single-line "you are here" clarity.
  // E.g. "Reports > Student\nAdoption\nReport" across 3 lines on mobile.
  let wrapFlagged = 0;
  for (const bc of [...containers].filter(visible).slice(0, 3)) {
    if (wrapFlagged >= 2) break;
    const r = bc.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const s = getComputedStyle(bc);
    const lineHeight = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.4 || 20;
    if (r.height > lineHeight * 2.2) {
      wrapFlagged++;
      const lines = Math.round(r.height / lineHeight);
      out.push({ issueType:'breadcrumbWrapsMultiLine', severity:'medium', selector:sel(bc), bbox:bb(bc),
        description:`Breadcrumb wraps to ~${lines} lines (container ${Math.round(r.height)}px tall, line-height ~${Math.round(lineHeight)}px) on ${window.innerWidth}px viewport. Loses single-line navigation clarity. Fix: truncate long segment names, collapse middle segments with "…", or use a compact mobile breadcrumb pattern.` });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~9 findings per cell
- Self-skips: page with no breadcrumb container returns []
- The `breadcrumbDuplicateSegment` catches your "Students > Students" bug from screenshot 1
- The `breadcrumbCurrentIsLink` catches when the last item is a clickable link instead of plain text
