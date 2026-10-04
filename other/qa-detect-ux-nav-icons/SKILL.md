---
name: qa-detect-ux-nav-icons
section: visual
description: "Detects nav/sidebar/tab consistency issues: icons mixed with iconless items, icon size variance across siblings, icon style mix (filled/outlined/colored), label-icon vertical misalignment, missing active-state indicator, label truncation. Catches the 'sidebar looks sloppy' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasNavigation, hasIcons]
---

## What it catches — 7 issue types

| issueType | severity | What |
|---|---|---|
| `navItemIconInconsistent` | medium | Sibling nav/tab items in same list: some have icons, others don't — visual rhythm broken |
| `navItemIconSizeInconsistent` | low | Sibling nav items have icons with differing rendered sizes (> 4px delta) |
| `navItemIconStyleInconsistent` | low | Sibling nav items mix icon styles (filled + outlined, colored + monochrome) |
| `navItemLabelIconMisaligned` | low | Nav item's label and icon are vertically misaligned (> 4px diff between icon center and label baseline) |
| `navItemLabelTruncated` | medium | Nav item label is visually truncated with no `title` attribute / no tooltip — user can't read it |
| `navItemActiveStateMissing` | medium | Nav list has a clearly-active page (URL match) but the corresponding nav item has no visible distinguishing style |
| `navItemHeightInconsistent` | low | Sibling nav items have differing heights (> 4px delta) — visual asymmetry |

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

  // Find nav containers
  const navContainers = document.querySelectorAll('nav, [role="navigation"], .sidebar, .side-nav, .nav-menu, [role="tablist"], .mat-tab-list, ul.nav, ul.menu, ul.list-group, .nav-list, [class*="sidenav"]');

  let containers = [...navContainers].filter(visible).slice(0, 4);

  for (const nav of containers) {
    // Find sibling nav items — direct children that are clickable list items
    let items = [...nav.querySelectorAll(':scope > li, :scope > a, :scope > [role="tab"], :scope > [role="menuitem"], :scope > .nav-item, :scope > .menu-item, :scope > .sidebar-item')]
      .filter(visible);
    // If no direct children, look one level deeper
    if (items.length < 2) {
      items = [...nav.querySelectorAll('li, a.nav-link, [role="tab"], [role="menuitem"], .nav-item, .menu-item, .sidebar-item, .mat-list-item, [class*="nav-item"], [class*="menu-item"], [class*="sidebar-item"]')]
        .filter(visible).slice(0, 12);
    }
    // Last resort for generic nav containers: direct child divs/buttons that look item-shaped
    if (items.length < 2) {
      items = [...nav.children]
        .filter(c => visible(c) && (c.tagName === 'DIV' || c.tagName === 'BUTTON' || c.tagName === 'A'))
        .filter(c => {
          const txt = (c.innerText || '').trim();
          return txt.length > 1 && txt.length < 80;
        })
        .slice(0, 12);
    }
    if (items.length < 3) continue;   // need ≥3 to spot inconsistency

    // ── 1. Icon present/absent inconsistency ─────────────────────────────
    const iconCounts = items.map(it => {
      const icons = it.querySelectorAll('svg, i.fa, i.material-icons, i[class*="icon"], img');
      return [...icons].filter(visible).length;
    });
    const withIcon = iconCounts.filter(n => n > 0).length;
    const withoutIcon = items.length - withIcon;
    if (withIcon > 0 && withoutIcon > 0 && withIcon !== items.length && withoutIcon !== items.length) {
      // Mixed — but only flag if substantial (>= 2 of each side)
      if (withIcon >= 2 && withoutIcon >= 2) {
        out.push({
          issueType: 'navItemIconInconsistent', severity: 'medium',
          selector: sel(nav), bbox: bb(nav),
          description: `Nav list has ${items.length} items: ${withIcon} with icons, ${withoutIcon} without. Inconsistent — either icon every item or none.`
        });
      }
    }

    // ── 2. Icon size variance among items WITH icons ─────────────────────
    const iconSizes = [];
    for (const it of items) {
      const ic = it.querySelector('svg, i.fa, i.material-icons, i[class*="icon"], img');
      if (!ic || !visible(ic)) continue;
      const r = ic.getBoundingClientRect();
      iconSizes.push({ size: Math.round(Math.max(r.width, r.height)), item: it, icon: ic });
    }
    if (iconSizes.length >= 3) {
      const sizes = iconSizes.map(s => s.size);
      const sizeDelta = Math.max(...sizes) - Math.min(...sizes);
      if (sizeDelta >= 5) {
        out.push({
          issueType: 'navItemIconSizeInconsistent', severity: 'low',
          selector: sel(nav), bbox: bb(nav),
          description: `Nav icons range ${Math.min(...sizes)}-${Math.max(...sizes)}px across ${iconSizes.length} items (${sizeDelta}px variance). Use one icon size.`
        });
      }
    }

    // ── 3. Icon style mix (filled vs outlined) — best-effort heuristic ───
    if (iconSizes.length >= 3) {
      const styles = new Set();
      for (const { icon } of iconSizes) {
        const cls = icon.className.toString().toLowerCase();
        const tag = icon.tagName.toLowerCase();
        let style = 'other';
        if (cls.includes('fa-solid') || cls.includes('-fill') || cls.includes('solid')) style = 'filled';
        else if (cls.includes('fa-regular') || cls.includes('-outline') || cls.includes('outline')) style = 'outlined';
        else if (tag === 'svg') {
          // Check fill vs stroke
          const path = icon.querySelector('path');
          if (path) {
            const fill = path.getAttribute('fill') || icon.getAttribute('fill') || '';
            const stroke = path.getAttribute('stroke') || icon.getAttribute('stroke') || '';
            if (fill && fill !== 'none' && (!stroke || stroke === 'none')) style = 'filled';
            else if (stroke && stroke !== 'none' && (!fill || fill === 'none')) style = 'outlined';
          }
        }
        styles.add(style);
      }
      styles.delete('other');
      if (styles.size >= 2) {
        out.push({
          issueType: 'navItemIconStyleInconsistent', severity: 'low',
          selector: sel(nav), bbox: bb(nav),
          description: `Nav icons mix styles: ${[...styles].join(' + ')}. Pick one (filled OR outlined) for visual coherence.`
        });
      }
    }

    // ── 4. Label-icon vertical misalignment ──────────────────────────────
    let misalignFlagged = 0;
    for (const it of items) {
      if (misalignFlagged >= 2) break;
      const ic = it.querySelector('svg, i.fa, i.material-icons, i[class*="icon"], img');
      if (!ic || !visible(ic)) continue;
      // Find first text node inside the item
      const txt = (it.innerText || '').trim();
      if (txt.length < 2) continue;
      const labelSpan = [...it.querySelectorAll('span, label, .label, .nav-text')].find(s => visible(s) && (s.innerText || '').trim().length > 0);
      const label = labelSpan || it;
      const ir = ic.getBoundingClientRect();
      const lr = label.getBoundingClientRect();
      const iconCenterY = ir.top + ir.height / 2;
      const labelCenterY = lr.top + lr.height / 2;
      const drift = Math.abs(iconCenterY - labelCenterY);
      if (drift > 4 && ir.height > 12 && lr.height > 12) {
        misalignFlagged++;
        out.push({
          issueType: 'navItemLabelIconMisaligned', severity: 'low',
          selector: sel(it), bbox: bb(it),
          description: `Nav item "${txt.slice(0, 30)}" — icon center is ${drift.toFixed(0)}px off label center. Use flex align-items: center.`
        });
      }
    }

    // ── 5. Label truncation without tooltip ──────────────────────────────
    let truncFlagged = 0;
    for (const it of items) {
      if (truncFlagged >= 3) break;
      const labelSpan = [...it.querySelectorAll('span, .label, .nav-text')].find(s => visible(s) && (s.innerText || '').trim().length > 0) || it;
      if (labelSpan.scrollWidth > labelSpan.clientWidth + 2) {
        const cs = getComputedStyle(labelSpan);
        if (cs.textOverflow === 'ellipsis' || cs.overflow === 'hidden') {
          const hasTooltip = it.getAttribute('title') || it.getAttribute('aria-label') || labelSpan.getAttribute('title');
          if (!hasTooltip) {
            truncFlagged++;
            const fullText = (labelSpan.innerText || '').trim();
            out.push({
              issueType: 'navItemLabelTruncated', severity: 'medium',
              selector: sel(it), bbox: bb(it),
              description: `Nav item label "${fullText.slice(0, 30)}..." is truncated with ellipsis and no title/aria-label tooltip. User can't read full label.`
            });
          }
        }
      }
    }

    // ── 6. Active-state indicator missing ────────────────────────────────
    const currentPath = location.pathname.toLowerCase();
    let activeMissingFlagged = 0;
    if (activeMissingFlagged < 1) {
      // Find item whose href matches current path
      const matchingItem = items.find(it => {
        const a = it.tagName === 'A' ? it : it.querySelector('a[href]');
        if (!a) return false;
        const href = a.getAttribute('href') || '';
        return href.length > 1 && currentPath.endsWith(href.toLowerCase().replace(/^\/+/, '/'));
      });
      if (matchingItem) {
        const cs = getComputedStyle(matchingItem);
        const hasActiveClass = /\b(active|selected|current|is-active|router-link-active)\b/.test(matchingItem.className.toString());
        const hasAriaCurrent = matchingItem.getAttribute('aria-current');
        // Compare background to sibling — distinct background = active state shown
        const sibling = items.find(it => it !== matchingItem);
        let hasDistinctBg = false;
        if (sibling) {
          const sibCs = getComputedStyle(sibling);
          if (cs.backgroundColor !== sibCs.backgroundColor || cs.color !== sibCs.color || cs.fontWeight !== sibCs.fontWeight) {
            hasDistinctBg = true;
          }
        }
        if (!hasActiveClass && !hasAriaCurrent && !hasDistinctBg) {
          activeMissingFlagged++;
          out.push({
            issueType: 'navItemActiveStateMissing', severity: 'medium',
            selector: sel(matchingItem), bbox: bb(matchingItem),
            description: `Nav item matches current URL (${currentPath}) but has no .active class, no aria-current, no distinguishing background/color. Users can't tell which page they're on.`
          });
        }
      }
    }

    // ── 7. Item height inconsistency ─────────────────────────────────────
    const heights = items.map(it => Math.round(it.getBoundingClientRect().height));
    if (heights.length >= 3) {
      const hDelta = Math.max(...heights) - Math.min(...heights);
      if (hDelta >= 5 && Math.max(...heights) > 0) {
        out.push({
          issueType: 'navItemHeightInconsistent', severity: 'low',
          selector: sel(nav), bbox: bb(nav),
          description: `Nav items heights range ${Math.min(...heights)}-${Math.max(...heights)}px (${hDelta}px variance). Set uniform line-height/padding.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~14 findings (1-3 per container × 4 containers)
- Self-skips: page with no nav containers returns []
- The `navItemIconInconsistent` + `navItemIconSizeInconsistent` catch the exact bug pattern from the user's sidebar screenshot (Administrative Units with icon, Departments without — or with different icon size/style)
- The `navItemActiveStateMissing` is the highest-impact: it tells users "you're on the wrong page" until they figure out where they are
