---
name: qa-detect-layout
section: responsiveness
description: "Detects fixed/sticky overflow, narrow content, CTA below fold, dropdown cutoff, content bleed-through, critical-element-hidden, excessive whitespace, sticky-covers-action, table overflow, fixed header obstructing content, element overlap, grid/flex collapse failures, sticky header too tall on mobile"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it checks
- `fixedElementOverflow` — fixed/sticky element extending past viewport
- `contentTooNarrow` — main content < 280px wide
- `ctaBelowFold` — primary CTA below the fold
- `dropdownCutOff` — visible dropdown/menu/listbox extending past viewport
- `contentBleedThrough` — drawer/modal open without making background inert
- `criticalElementHidden` — submit/CTA covered by overlay OR completely off-screen
- `excessiveWhitespace` — section with >300px combined padding+margin taking >60% of viewport with little content
- `stickyElementCoversAction` — fixed/sticky bottom element overlapping a button
- `tableOverflow` — `<table>` wider than its container with no horizontal scroll wrapper (mobile/tablet only)
- `fixedHeaderObstructsContent` — fixed/sticky top navbar covers the first main content element
- `elementOverlap` — any interactive element (button, link, input, select) covered by an unrelated element at its center point — not clickable/tappable
- `gridCollapseIssue` — CSS Grid with fixed multi-column template at mobile/tablet without auto-fit/minmax (won't collapse), OR flex container with flex-wrap:nowrap overflowing at small viewport
- `stickyHeaderTooTall` — fixed/sticky top header exceeds 15% of viewport height on mobile (≤768px)

## Probe (browser_evaluate)
```js
() => {
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0,120);
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const vw = innerWidth, vh = innerHeight;

  // 1. fixedElementOverflow
  // Only a real bug if the PAGE actually scrolls horizontally. A fixed/sticky panel
  // positioned off the right edge (settings drawer, slide-in sidebar, off-canvas menu)
  // is intentional and invisible — it does NOT create a horizontal scrollbar. Flagging
  // it produces false "element extends beyond viewport" tickets on every page.
  const docEl = document.documentElement;
  const pageScrollsHorizontally = docEl.scrollWidth > docEl.clientWidth + 2;
  for (const el of document.querySelectorAll('*')) {
    if (out.length >= 20) break;
    if (!pageScrollsHorizontally) break;             // no real horizontal scroll → nothing to flag
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    // Skip elements that are ENTIRELY off-screen (a hidden drawer parked past the edge):
    // left at/beyond the right edge, or fully left/above the viewport.
    if (r.left >= vw - 2 || r.right <= 2 || r.top >= vh - 2 || r.bottom <= 2) continue;
    if (r.right > vw + 2 || r.bottom > vh + 2) {
      out.push({ issueType:'fixedElementOverflow', severity:'high', selector:sel(el),
        description:`${s.position} element extends beyond viewport: right=${Math.round(r.right)}px (vw=${vw}px)`, bbox: bb(el) });
    }
  }

  // 2. contentTooNarrow
  const main = document.querySelector('main, [role="main"], #main, #content, .content, .container');
  if (main) {
    const r = main.getBoundingClientRect();
    if (r.width > 0 && r.width < 280) {
      out.push({ issueType:'contentTooNarrow', severity:'medium', selector:sel(main),
        description:`Main content area is only ${Math.round(r.width)}px wide (minimum usable: 280px)`, bbox: bb(main) });
    }
  }

  // 3. ctaBelowFold
  const cta = document.querySelector('button[type="submit"], a.cta, .btn-primary, [data-testid*="cta"]');
  if (cta) {
    const r = cta.getBoundingClientRect();
    if (r.top > vh) {
      out.push({ issueType:'ctaBelowFold', severity:'medium', selector:sel(cta),
        description:`Primary CTA is below the fold: top=${Math.round(r.top)}px, viewport height=${vh}px`, bbox: bb(cta) });
    }
  }

  // 4. dropdownCutOff — visible dropdowns/menus/listboxes extending past viewport
  const dropdownSel = '[role="menu"],[role="listbox"],[role="combobox"][aria-expanded="true"],.dropdown-menu.show,.dropdown.open .dropdown-menu,[class*="dropdown"][class*="open"] [class*="menu"],.menu-open .menu-content,[data-testid*="dropdown"][aria-expanded="true"]';
  for (const el of document.querySelectorAll(dropdownSel)) {
    if (out.length >= 20) break;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > vw + 2 || r.bottom > vh + 2 || r.left < -2 || r.top < -2) {
      out.push({ issueType:'dropdownCutOff', severity:'medium', selector:sel(el),
        description:`Dropdown/menu panel extends beyond viewport: rect=[${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}] vw=${vw} vh=${vh}`, bbox: bb(el) });
    }
  }

  // 5. contentBleedThrough — open dialog/drawer without making main content inert
  const openDialogs = document.querySelectorAll('[role="dialog"][aria-modal="true"]:not([aria-hidden="true"]),.drawer.open,.sidebar.open,.modal.show,[class*="drawer"][class*="open"]');
  let hasOpenDialog = false;
  for (const d of openDialogs) {
    const r = d.getBoundingClientRect();
    const s = getComputedStyle(d);
    if (s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0) {
      hasOpenDialog = true; break;
    }
  }
  if (hasOpenDialog) {
    const bgMain = document.querySelector('main, [role="main"]');
    if (bgMain && !bgMain.hasAttribute('inert') && bgMain.getAttribute('aria-hidden') !== 'true') {
      const tabs = bgMain.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])');
      if (tabs.length > 0) {
        out.push({ issueType:'contentBleedThrough', severity:'high', selector:sel(bgMain),
          description:`Open drawer/modal but background <main> still has ${tabs.length} tabbable elements — add inert or aria-hidden="true"`, bbox: bb(bgMain) });
      }
    }
  }

  // 6. criticalElementHidden — submit/CTA either off-screen OR covered by another element
  const criticals = document.querySelectorAll('button[type="submit"]:not([disabled]), input[type="submit"]:not([disabled]), a.cta, .btn-primary, .primary-button, [data-testid*="submit"]');
  for (const el of criticals) {
    if (out.length >= 20) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const offScreen = r.right < 0 || r.left > vw || r.bottom < 0 || r.top > vh;
    if (offScreen) {
      out.push({ issueType:'criticalElementHidden', severity:'high', selector:sel(el),
        description:`Critical button completely off-screen: rect=[${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}] viewport=${vw}x${vh}`, bbox: bb(el) });
      continue;
    }
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    if (cx >= 0 && cx <= vw && cy >= 0 && cy <= vh) {
      const topEl = document.elementFromPoint(cx, cy);
      if (topEl && topEl !== el && !el.contains(topEl) && !topEl.contains(el)) {
        out.push({ issueType:'criticalElementHidden', severity:'high', selector:sel(el),
          description:`Critical button covered by another element at center: ${sel(topEl)} is on top`, bbox: bb(el) });
      }
    }
  }

  // 7. excessiveWhitespace — section with massive padding+margin and little content
  for (const el of document.querySelectorAll('section, main > div, .container > div, .row, .row > div')) {
    if (out.length >= 20) break;
    const s = getComputedStyle(el);
    const padTop = parseFloat(s.paddingTop) || 0;
    const padBot = parseFloat(s.paddingBottom) || 0;
    const marTop = parseFloat(s.marginTop) || 0;
    const marBot = parseFloat(s.marginBottom) || 0;
    const totalSpace = padTop + padBot + marTop + marBot;
    if (totalSpace < 300) continue;
    const r = el.getBoundingClientRect();
    if (r.height < vh * 0.6) continue;
    const innerText = (el.innerText || '').trim();
    if (innerText.length > 100) continue;
    out.push({ issueType:'excessiveWhitespace', severity:'medium', selector:sel(el),
      description:`Section has ${Math.round(totalSpace)}px combined padding+margin, ${Math.round(r.height)}px tall, only ${innerText.length} chars of text — wasted screen space`, bbox: bb(el) });
  }

  // 8. stickyElementCoversAction — fixed/sticky bottom element overlapping a button
  const stickies = [];
  for (const el of document.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    // bottom-anchored: bottom of element in lower 1/3 of viewport
    if (r.bottom > vh - vh / 3 && r.top > vh / 2) {
      stickies.push({ el, r });
    }
  }
  for (const { el: fixed, r: fr } of stickies) {
    if (out.length >= 20) break;
    const buttons = document.querySelectorAll('button:not([disabled]), [role="button"], input[type="submit"]:not([disabled]), a.btn, .btn');
    for (const btn of buttons) {
      if (fixed.contains(btn) || btn.contains(fixed)) continue;
      const br = btn.getBoundingClientRect();
      if (br.width === 0 || br.height === 0) continue;
      const overlapH = Math.min(br.right, fr.right) - Math.max(br.left, fr.left);
      const overlapV = Math.min(br.bottom, fr.bottom) - Math.max(br.top, fr.top);
      if (overlapH > 0 && overlapV > 0) {
        out.push({ issueType:'stickyElementCoversAction', severity:'medium', selector:sel(btn),
          description:`Button covered by sticky/fixed bottom element (${sel(fixed)}): button at top=${Math.round(br.top)}, sticky at top=${Math.round(fr.top)}`, bbox: bb(btn) });
        break;
      }
    }
  }

  // 9. tableOverflow — table wider than container without horizontal scroll wrapper (mobile/tablet only)
  const isMobileOrTablet = vw <= 1024;
  if (isMobileOrTablet) {
    for (const table of document.querySelectorAll('table')) {
      if (out.length >= 20) break;
      const parent = table.parentElement;
      if (!parent) continue;
      const tr = table.getBoundingClientRect();
      const pr = parent.getBoundingClientRect();
      if (tr.width === 0 || pr.width === 0) continue;
      if (table.scrollWidth <= parent.clientWidth + 5) continue;
      const parentOverflow = getComputedStyle(parent).overflowX;
      if (parentOverflow === 'auto' || parentOverflow === 'scroll') continue;
      out.push({ issueType:'tableOverflow', severity:'medium', selector:sel(table),
        description:`Table wider than container without horizontal scroll: tableScrollWidth=${table.scrollWidth}px, parentClientWidth=${parent.clientWidth}px, parent overflow-x=${parentOverflow}`, bbox: bb(table) });
    }
  }

  // 11. elementOverlap — REAL collision between two sibling content elements only.
  //
  // A bounding-box / center-point intersection is NOT a bug by itself: the vast
  // majority of overlaps are INTENTIONAL and correct — dropdowns/tooltips/popovers/
  // dialogs rendered over content, absolutely- or fixed-positioned badges on avatars,
  // z-stacked modals, sticky headers sitting over scrolled content, an icon inside a
  // button, a label inside its field. We only flag a genuine collision: two SIBLING
  // content elements (one is NOT an ancestor/descendant of the other, NEITHER is an
  // overlay) that actually clip each other's TEXT.
  //
  // Helpers:
  const OVERLAY_ROLES = ['tooltip','status','alert','progressbar','menu','listbox','dialog','alertdialog','menuitem','option','presentation'];
  const OVERLAY_CLASS_RE = /(dropdown|popover|popper|tooltip|menu|overlay|badge|chip|pill|backdrop|modal|dialog|toast|snackbar|notification|cdk-overlay|MuiPopover|MuiMenu|MuiPopper|ant-dropdown|ant-popover|ant-tooltip|ant-select-dropdown)/i;
  const isOverlayLike = node => {
    if (!node || node.nodeType !== 1) return false;
    const role = node.getAttribute && node.getAttribute('role');
    if (role && OVERLAY_ROLES.includes(role)) return true;
    const cls = (node.className && typeof node.className === 'string') ? node.className : '';
    if (OVERLAY_CLASS_RE.test(cls)) return true;
    const st = getComputedStyle(node);
    // Positioned out-of-flow layers stack ON TOP intentionally — not a content collision.
    if (st.position === 'absolute' || st.position === 'fixed' || st.position === 'sticky') return true;
    return false;
  };
  // An element is overlay-like if it OR any ancestor (up to body) is overlay-like —
  // covers the inner text node of a dropdown/badge/popover whose wrapper carries the role/class/position.
  const inOverlayChain = node => {
    let n = node;
    while (n && n !== document.body && n !== document.documentElement) {
      if (isOverlayLike(n)) return true;
      n = n.parentElement;
    }
    return false;
  };
  const hasOwnText = node => {
    if (!node || node.nodeType !== 1) return false;
    for (const c of node.childNodes) { if (c.nodeType === 3 && c.textContent.trim().length >= 2) return true; }
    return false;
  };
  const isTransparent = node => {
    const st = getComputedStyle(node);
    if (parseFloat(st.opacity) === 0) return true;
    const bg = st.backgroundColor || '';
    const m = bg.match(/rgba?\(([^)]+)\)/);
    const transparentBg = !bg || bg === 'transparent' || (m && m[1].split(',').map(s => s.trim())[3] === '0');
    // transparent only counts if it ALSO has no background image and no border — i.e. visually empty
    const noImg = st.backgroundImage === 'none';
    return transparentBg && noImg;
  };

  const interactiveEls = document.querySelectorAll('button:not([disabled]), a[href], input:not([type="hidden"]):not([disabled]), select:not([disabled]), textarea:not([disabled]), [role="button"]:not([disabled])');
  for (const el of interactiveEls) {
    if (out.length >= 20) break;
    const r = el.getBoundingClientRect();
    if (r.width < 5 || r.height < 5) continue;
    if (r.right < 0 || r.left > vw || r.bottom < 0 || r.top > vh) continue;
    // off-canvas / hidden interactive element — never a visible collision
    const elStyle = getComputedStyle(el);
    if (elStyle.display === 'none' || elStyle.visibility === 'hidden' || parseFloat(elStyle.opacity) === 0) continue;
    // EXEMPT: the element itself sits in an overlay chain (it's part of a dropdown/menu/dialog/badge) —
    // overlapping the content beneath is the whole point of an overlay.
    if (inOverlayChain(el)) continue;
    const cx = Math.round(r.left + r.width / 2);
    const cy = Math.round(r.top + r.height / 2);
    if (cx < 0 || cx > vw || cy < 0 || cy > vh) continue;
    const topEl = document.elementFromPoint(cx, cy);
    if (!topEl || topEl === el) continue;
    // EXEMPT: parent/child containment (icon-in-button, label-in-field, text node of the control itself)
    if (el.contains(topEl) || topEl.contains(el)) continue;
    const topR = topEl.getBoundingClientRect();
    if (topR.width < 20 && topR.height < 20) continue; // tiny badge/dot — decorative
    if (getComputedStyle(topEl).pointerEvents === 'none') continue; // passthrough overlay
    // EXEMPT: the covering element is an intentional overlay (dropdown/tooltip/popover/dialog/badge,
    // or anything absolutely/fixed/sticky-positioned stacked above) — NOT a sibling-content collision.
    if (inOverlayChain(topEl)) continue;
    // EXEMPT: one of the two is visually transparent (it isn't actually clipping anything visible).
    if (isTransparent(topEl) || isTransparent(el)) continue;
    // REQUIRE A REAL COLLISION: both the interactive element and the covering element must
    // render their OWN text, and that text must measurably overlap — i.e. they clip each other.
    if (!hasOwnText(el) || !hasOwnText(topEl)) continue;
    const ox = Math.min(r.right, topR.right) - Math.max(r.left, topR.left);
    const oy = Math.min(r.bottom, topR.bottom) - Math.max(r.top, topR.top);
    if (ox <= 4 || oy <= 4) continue; // negligible touch — not a clipping collision
    // Skip if already caught by criticalElementHidden (submit/CTA buttons)
    const isCritical = el.matches('button[type="submit"], input[type="submit"], a.cta, .btn-primary, .primary-button, [data-testid*="submit"]');
    if (isCritical) continue;
    out.push({ issueType:'elementOverlap', severity:'high', selector:sel(el),
      description:`Two sibling content elements collide: ${sel(el)} and ${sel(topEl)} overlap by ${Math.round(ox)}×${Math.round(oy)}px and clip each other's text (neither is an overlay/dropdown/badge).`, bbox: bb(el) });
  }

  // 12. gridCollapseIssue + flexNoWrapOverflow — grid/flex that doesn't collapse at mobile/tablet
  const isSmallViewport = vw <= 1024;
  if (isSmallViewport) {
    for (const el of document.querySelectorAll('*')) {
      if (out.length >= 20) break;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;

      if (s.display === 'grid' || s.display === 'inline-grid') {
        const gtc = s.gridTemplateColumns;
        if (!gtc || gtc === 'none') continue;
        if (gtc.includes('auto-fit') || gtc.includes('auto-fill') || gtc.includes('minmax')) continue;
        // Expand repeat(N, ...) to count columns
        const expanded = gtc.replace(/repeat\((\d+),\s*[^)]+\)/g, (_, n) => Array(parseInt(n)).fill('col').join(' '));
        const colCount = expanded.split(/\s+/).filter(Boolean).length;
        if (colCount < 2) continue;
        if (el.scrollWidth > el.clientWidth + 5) {
          out.push({ issueType:'gridCollapseIssue', severity:'medium', selector:sel(el),
            description:`CSS Grid has ${colCount} fixed columns (${gtc.slice(0,60)}) at ${vw}px viewport without auto-fit/minmax — content overflows instead of collapsing to single column`, bbox: bb(el) });
        }
      } else if ((s.display === 'flex' || s.display === 'inline-flex') && s.flexWrap === 'nowrap') {
        if (el.scrollWidth <= el.clientWidth + 10) continue;
        const visibleChildren = [...el.children].filter(c => {
          const cr = c.getBoundingClientRect();
          return cr.width > 0 && cr.height > 0;
        });
        if (visibleChildren.length >= 2) {
          out.push({ issueType:'gridCollapseIssue', severity:'medium', selector:sel(el),
            description:`Flex container has flex-wrap:nowrap with ${visibleChildren.length} children and overflows at ${vw}px — items don't wrap on small screens`, bbox: bb(el) });
        }
      }
    }
  }

  // 13. stickyHeaderTooTall — sticky/fixed header disproportionately tall on mobile
  if (vw <= 768) {
    for (const el of document.querySelectorAll('*')) {
      if (out.length >= 20) break;
      const s = getComputedStyle(el);
      if (s.position !== 'fixed' && s.position !== 'sticky') continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      if (r.top > 10) continue; // not anchored at top
      if (r.height > vh * 0.15) {
        out.push({ issueType:'stickyHeaderTooTall', severity:'medium', selector:sel(el),
          description:`Sticky/fixed header is ${Math.round(r.height)}px tall at ${vw}px mobile viewport — exceeds 15% of viewport height (${Math.round(vh * 0.15)}px), leaving insufficient content area`, bbox: bb(el) });
      }
    }
  }

  // 10. fixedHeaderObstructsContent — fixed/sticky top navbar covers first main content element
  let topFixed = null;
  let topFixedHeight = 0;
  for (const el of document.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && s.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    // Anchored at top
    if (r.top > 5) continue;
    if (r.bottom > topFixedHeight) {
      topFixed = el;
      topFixedHeight = r.bottom;
    }
  }
  if (topFixed && topFixedHeight > 0) {
    const main = document.querySelector('main, [role="main"], #main, router-outlet, ng-component');
    if (main) {
      // Find first visible child of main with text content
      let firstChild = null;
      for (const child of main.querySelectorAll('h1, h2, h3, p, button, a, section, article, div')) {
        const cr = child.getBoundingClientRect();
        if (cr.width === 0 || cr.height === 0) continue;
        const cs = getComputedStyle(child);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        firstChild = child;
        break;
      }
      if (firstChild) {
        const cr = firstChild.getBoundingClientRect();
        if (cr.top < topFixedHeight) {
          out.push({ issueType:'fixedHeaderObstructsContent', severity:'medium', selector:sel(firstChild),
            description:`Fixed/sticky header (${sel(topFixed)}, height=${Math.round(topFixedHeight)}px) covers first content element (${sel(firstChild)}, top=${Math.round(cr.top)}px). Add padding-top or scroll-margin-top to compensate.`, bbox: bb(firstChild) });
        }
      }
    }
  }

  // 14. cardIconOverlapsText — icon inside a stat/summary card overlaps the card title text.
  // Triggered on mobile/tablet where cards are narrow and an absolutely-positioned icon
  // (top-right corner) bleeds into the label text — e.g. "TOTAL STUDENTS" with user-circle icon.
  if (vw <= 900) {
    const CARD_SEL = '[class*="stat-card"],[class*="stat_card"],[class*="kpi-card"],[class*="summary-card"],[class*="metric-card"],[class*="widget-card"],[class*="info-card"],[class*="count-card"],[class*="dashboard-stat"],[class*="overview-card"],[class*="overview-item"]';
    let cardIconFlagged = 0;
    for (const card of document.querySelectorAll(CARD_SEL)) {
      if (cardIconFlagged >= 4 || out.length >= 20) break;
      const cr = card.getBoundingClientRect();
      if (cr.width === 0 || cr.height === 0) continue;
      const textEls = [...card.querySelectorAll('span,p,h1,h2,h3,h4,h5,h6,label,[class*="title"],[class*="label"],[class*="heading"],[class*="card-title"]')]
        .filter(el => {
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) return false;
          const t = (el.innerText || '').trim();
          return t.length >= 2 && t.length <= 50;
        });
      const iconEls = [...card.querySelectorAll('img,svg,i[class*="pi"],i[class*="fa"],i[class*="icon"],[class*="card-icon"],[class*="stat-icon"],[class*="widget-icon"]')]
        .filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && r.height > 0 && r.width <= 80 && r.height <= 80;
        });
      for (const icon of iconEls) {
        if (cardIconFlagged >= 4 || out.length >= 20) break;
        const ir = icon.getBoundingClientRect();
        if (ir.right < cr.left || ir.left > cr.right) continue;
        for (const textEl of textEls) {
          if (textEl.contains(icon) || icon.contains(textEl)) continue;
          const tr = textEl.getBoundingClientRect();
          if (tr.width === 0) continue;
          const overlapX = Math.min(ir.right, tr.right) - Math.max(ir.left, tr.left);
          const overlapY = Math.min(ir.bottom, tr.bottom) - Math.max(ir.top, tr.top);
          if (overlapX > 8 && overlapY > 4) {
            cardIconFlagged++;
            const label = (textEl.innerText || '').trim().slice(0, 35);
            out.push({ issueType:'cardIconOverlapsText', severity:'high', selector:sel(textEl),
              description:`Card icon overlaps text label "${label}" by ${Math.round(overlapX)}px at ${vw}px viewport. Add padding-right to the label container or constrain the icon with position/size to prevent overlap.`,
              bbox: bb(textEl) });
            break;
          }
        }
      }
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| fixedElementOverflow | high | "{position} element extends beyond viewport" |
| contentTooNarrow | medium | "Main content area is only {w}px wide" |
| ctaBelowFold | medium | "Primary CTA is below the fold" |
| dropdownCutOff | medium | "Dropdown/menu panel extends beyond viewport" |
| contentBleedThrough | high | "Open drawer/modal but background still tabbable" |
| criticalElementHidden | high | "Critical button off-screen or covered" |
| excessiveWhitespace | medium | "Section has {N}px padding+margin with little text" |
| stickyElementCoversAction | medium | "Button covered by sticky/fixed bottom element" |
| tableOverflow | medium | "Table wider than container ({tableScrollWidth}px vs {parentClientWidth}px) without horizontal scroll wrapper" |
| fixedHeaderObstructsContent | medium | "Fixed/sticky header covers first content element — add padding-top or scroll-margin-top" |
| elementOverlap | high | "Interactive element covered by {coveringEl} at center point — may not be clickable/tappable" |
| gridCollapseIssue | medium | "CSS Grid has {N} fixed columns at {vw}px without auto-fit/minmax — overflows instead of collapsing" |
| gridCollapseIssue | medium | "Flex container has flex-wrap:nowrap with {N} children and overflows at {vw}px — items don't wrap" |
| stickyHeaderTooTall | medium | "Sticky/fixed header is {h}px tall at {vw}px mobile — exceeds 15% of viewport height" |
| cardIconOverlapsText | high | "Card icon overlaps text label '{label}' by {N}px at {vw}px viewport" |
