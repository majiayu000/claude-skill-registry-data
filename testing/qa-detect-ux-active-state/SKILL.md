---
name: qa-detect-ux-active-state
section: visual
description: "Detects inconsistent active-state styling within the same navigation, tab group, or list — when one active item uses a background highlight and another uses only text color, users get confused about what's selected. Catches the 'two different active styles in the same menu' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasNavigation, hasTabs]
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `activeStateMixedStyle` | medium | Same nav/menu has multiple "active" items styled differently — one with background highlight, another with only color/weight change (your sidebar: Human Resource = blue bg, Employee Attendance = blue text only) |
| `noActiveStateOnCurrentRoute` | medium | Page URL matches a nav item's href but the item has no visible active style (no .active class, no aria-current, no distinct bg/color) |
| `multipleActiveItemsInGroup` | medium | A nav group / tab list has 2+ items marked active simultaneously (.active or aria-selected="true") — only one should be active |
| `activeIndicatorTooSubtle` | low | Active item's background/border differs from siblings by less than 5% RGB delta — visually indistinguishable |
| `activeStateNoAriaCurrent` | low | Visually-active item has no `aria-current` attribute — screen reader users can't tell the current page |

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
  function parseRGB(s) {
    if (!s) return null;
    const m = s.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)/);
    if (!m) return null;
    return { r: +m[1], g: +m[2], b: +m[3], a: m[4] !== undefined ? +m[4] : 1 };
  }
  function colorDelta(a, b) {
    if (!a || !b) return 999;
    return Math.abs(a.r - b.r) + Math.abs(a.g - b.g) + Math.abs(a.b - b.b);
  }
  const out = [];

  // Find nav containers
  const navContainers = document.querySelectorAll('nav, [role="navigation"], .sidebar, .side-nav, .nav-menu, [role="tablist"], .mat-tab-list, ul.nav, ul.menu, ul.list-group, .nav-list, [class*="sidenav"]');

  for (const nav of [...navContainers].filter(visible).slice(0, 4)) {
    // Get items
    let items = [...nav.querySelectorAll('a[href], [role="tab"], [role="menuitem"], li, .nav-item, .menu-item, .sidebar-item')]
      .filter(visible).slice(0, 25);
    if (items.length < 3) continue;

    // ── 1. Active-state mixed styles ─────────────────────────────────────
    // Find all items that LOOK active (matching path OR having "active" class
    // OR aria-selected/aria-current)
    const activeItems = items.filter(it => {
      const cls = (it.className || '').toString();
      const ariaCurr = it.getAttribute('aria-current');
      const ariaSel = it.getAttribute('aria-selected');
      const hasActiveClass = /\b(active|selected|current|is-active|router-link-active|router-link-exact-active)\b/.test(cls);
      return hasActiveClass || ariaCurr === 'page' || ariaCurr === 'true' || ariaSel === 'true';
    });

    if (activeItems.length >= 2) {
      // Compare their visual style
      const styles = activeItems.map(a => {
        const cs = getComputedStyle(a);
        return {
          item: a,
          bg: parseRGB(cs.backgroundColor),
          color: parseRGB(cs.color),
          fontWeight: cs.fontWeight,
          borderColor: parseRGB(cs.borderLeftColor || cs.borderColor)
        };
      });
      // Look at first vs others
      for (let i = 1; i < styles.length; i++) {
        const s0 = styles[0], si = styles[i];
        const bgDelta = colorDelta(s0.bg, si.bg);
        const colorDelta_ = colorDelta(s0.color, si.color);
        // If backgrounds differ a lot OR weights differ a lot → mixed
        if (bgDelta > 60 || (s0.fontWeight !== si.fontWeight && Math.abs(parseInt(s0.fontWeight) - parseInt(si.fontWeight)) > 100)) {
          out.push({
            issueType: 'activeStateMixedStyle', severity: 'medium',
            selector: sel(nav), bbox: bb(nav),
            description: `Nav has ${activeItems.length} items marked active but styled differently — first item bg ${s0.bg ? `rgb(${s0.bg.r},${s0.bg.g},${s0.bg.b})` : 'none'}, another item bg ${si.bg ? `rgb(${si.bg.r},${si.bg.g},${si.bg.b})` : 'none'}. Use ONE active style.`
          });
          break;
        }
      }
    }

    // ── 2. Multiple active items in same group ──────────────────────────
    if (activeItems.length >= 2) {
      // Check siblings only (same nav level)
      const directSiblings = activeItems.filter(it => it.parentElement === activeItems[0].parentElement);
      if (directSiblings.length >= 2) {
        out.push({
          issueType: 'multipleActiveItemsInGroup', severity: 'medium',
          selector: sel(nav), bbox: bb(nav),
          description: `${directSiblings.length} sibling nav items are marked active simultaneously. Only one item should be active in a group.`
        });
      }
    }

    // ── 3. Active indicator too subtle ──────────────────────────────────
    if (activeItems.length >= 1 && items.length > activeItems.length) {
      const active = activeItems[0];
      const inactive = items.find(it => !activeItems.includes(it));
      if (active && inactive) {
        const aCs = getComputedStyle(active);
        const iCs = getComputedStyle(inactive);
        const bgDelta = colorDelta(parseRGB(aCs.backgroundColor), parseRGB(iCs.backgroundColor));
        const colorDelta_ = colorDelta(parseRGB(aCs.color), parseRGB(iCs.color));
        const weightDiff = Math.abs(parseInt(aCs.fontWeight) - parseInt(iCs.fontWeight));
        if (bgDelta < 15 && colorDelta_ < 30 && weightDiff < 100) {
          out.push({
            issueType: 'activeIndicatorTooSubtle', severity: 'low',
            selector: sel(active), bbox: bb(active),
            description: `Active item differs from siblings by only ${bgDelta} bg / ${colorDelta_} color / ${weightDiff} weight delta. Visually indistinguishable from inactive items.`
          });
        }
      }
    }

    // ── 4. Active item missing aria-current ─────────────────────────────
    if (activeItems.length >= 1) {
      const a = activeItems[0];
      if (!a.getAttribute('aria-current') && !a.getAttribute('aria-selected')) {
        out.push({
          issueType: 'activeStateNoAriaCurrent', severity: 'low',
          selector: sel(a), bbox: bb(a),
          description: `Visually-active nav item has no aria-current/aria-selected. Screen readers can't tell which page is current.`
        });
      }
    }

    // ── 5. No active state for current route ────────────────────────────
    const currentPath = location.pathname.toLowerCase();
    const matchingItem = items.find(it => {
      const a = it.tagName === 'A' ? it : it.querySelector('a[href]');
      if (!a) return false;
      const href = (a.getAttribute('href') || '').toLowerCase();
      return href.length > 1 && (currentPath === href || currentPath.endsWith(href.replace(/^\/+/, '/')));
    });
    if (matchingItem && activeItems.length === 0) {
      out.push({
        issueType: 'noActiveStateOnCurrentRoute', severity: 'medium',
        selector: sel(matchingItem), bbox: bb(matchingItem),
        description: `Nav item matches current URL (${currentPath}) but no item in the menu has any active style. Users can't tell what page they're on.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~10 findings per cell
- Self-skips: page with no nav containers returns []
- The `activeStateMixedStyle` catches your sidebar's bug — Human Resource has a blue background while Employee Attendance has only blue text (two different "active" patterns in the same menu)
