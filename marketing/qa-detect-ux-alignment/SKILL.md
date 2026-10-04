---
name: qa-detect-ux-alignment
section: visual
description: "Detects vertical baseline / inline alignment issues: breadcrumb items at different baselines, label not aligned with its input, icon not aligned with adjacent text, sibling buttons in a row with different heights, table cells in same row with mismatched vertical centers, form action group not aligned to the same side."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it catches — 7 issue types

| issueType | severity | What |
|---|---|---|
| `breadcrumbItemsBaselineDrift` | medium | Breadcrumb items (text labels and separators) in the same row have visibly different vertical baselines (> 3px drift). Your screenshot — "Students" page title and "Students" breadcrumb item at different baselines |
| `labelInputBaselineDrift` | low | `<label>` and its associated `<input>` rendered side-by-side have center-Y drift > 4px — label sits above or below input center |
| `iconTextBaselineDrift` | low | Icon (`<svg>`/`<i>`/`<img>`) next to text label has center-Y drift > 4px from the text baseline. Common in buttons and nav items |
| `inlineGroupHeightMismatch` | low | Sibling buttons / inputs in the same row have heights differing by > 6px — vertical rhythm broken |
| `tableCellContentBaselineMixed` | low | Cells in the same table row position their content at different vertical baselines (e.g. some top-aligned, others center-aligned) — > 6px drift |
| `formActionsAlignmentInconsistent` | low | Multiple form action button groups (Save/Cancel) on the same page use mixed alignment — left-aligned in one form, right-aligned in another |
| `verticalCenterMisaligned` | low | Two visible elements sitting side-by-side in the same horizontal band have a vertical-center delta > 8px when they should align (e.g. logo + brand name in header) |

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
  // Estimate the text BASELINE Y (not bbox top). Heuristic: top + height - (font-size * 0.2)
  function textBaseline(el) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const fs = parseFloat(cs.fontSize) || 14;
    return r.bottom - fs * 0.2;
  }
  function centerY(el) {
    const r = el.getBoundingClientRect();
    return r.top + r.height / 2;
  }
  const out = [];

  // ── 1. Breadcrumb items baseline drift ──────────────────────────────
  // Look at the breadcrumb container PLUS the parent block that includes
  // a sibling page title.
  let crumbFlagged = 0;
  const crumbContainers = [...document.querySelectorAll('.breadcrumb, .breadcrumbs, [class*="breadcrumb"], nav[aria-label*="breadcrumb" i]')]
    .filter(visible);
  for (const bc of crumbContainers.slice(0, 2)) {
    if (crumbFlagged >= 1) break;
    // Get items (text labels + separators) inside the breadcrumb
    const items = [...bc.querySelectorAll('a, span, li, .breadcrumb-item, [class*="breadcrumb-item"]')]
      .filter(visible)
      .filter(el => (el.innerText || '').trim().length > 0);
    // (Note: even if items.length === 1, we still continue — the bug we catch is
    // misalignment between the breadcrumb's content and the sibling page title.)
    // Also consider the breadcrumb's sibling page title if it sits in same row
    const candidates = [...items];
    const wrap = bc.parentElement;
    if (wrap) {
      for (const sib of wrap.children) {
        if (sib === bc) continue;
        if (!visible(sib)) continue;
        const sr = sib.getBoundingClientRect();
        const br = bc.getBoundingClientRect();
        if (Math.abs(sr.top - br.top) < 16 || Math.abs(sr.bottom - br.bottom) < 16) {
          // Same band — include for baseline check
          const childTextEls = [...sib.querySelectorAll('*')].filter(visible).filter(el => (el.innerText || '').trim().length > 0 && el.children.length === 0);
          candidates.push(sib);
          for (const t of childTextEls) candidates.push(t);
        }
      }
    }
    // Get baselines AND visual centers — whichever drifts more is the bug
    const measures = candidates.map(el => ({
      el,
      base: textBaseline(el),
      centerY: centerY(el),
      top: el.getBoundingClientRect().top
    }));
    const baseDrift = Math.max(...measures.map(m => m.base)) - Math.min(...measures.map(m => m.base));
    const centerDrift = Math.max(...measures.map(m => m.centerY)) - Math.min(...measures.map(m => m.centerY));
    const topDrift = Math.max(...measures.map(m => m.top)) - Math.min(...measures.map(m => m.top));
    const drift = Math.max(baseDrift, centerDrift, topDrift);
    if (drift > 3 && measures.length >= 2) {
      crumbFlagged++;
      const samples = measures.slice(0, 5).map(m => `"${(m.el.innerText || '').trim().slice(0, 20)}" top=${m.top.toFixed(0)} center=${m.centerY.toFixed(0)}`);
      out.push({
        issueType: 'breadcrumbItemsBaselineDrift', severity: 'medium',
        selector: sel(bc), bbox: bb(bc),
        description: `Breadcrumb / page-title row has ${candidates.length} text elements with vertical drift of ${drift.toFixed(0)}px (top Δ${topDrift.toFixed(0)}, center Δ${centerDrift.toFixed(0)}, baseline Δ${baseDrift.toFixed(0)}). Items not in line: ${samples.slice(0,3).join('; ')}. Use display:flex + align-items:center (or baseline).`
      });
    }
  }

  // ── 2. Label-input baseline drift ──────────────────────────────────
  let labelInputFlagged = 0;
  for (const lbl of document.querySelectorAll('label')) {
    if (labelInputFlagged >= 3) break;
    if (!visible(lbl)) continue;
    // Find associated input by for=, or inside the label
    let inp = null;
    if (lbl.htmlFor) inp = document.getElementById(lbl.htmlFor);
    if (!inp) inp = lbl.querySelector('input, select, textarea');
    if (!inp || !visible(inp)) continue;
    const lr = lbl.getBoundingClientRect();
    const ir = inp.getBoundingClientRect();
    // Only flag if side-by-side (in the same horizontal band)
    const sideBySide = Math.abs(lr.top - ir.top) < 16 && lr.right <= ir.left + 8;
    if (!sideBySide) continue;
    const labelCY = centerY(lbl);
    const inputCY = centerY(inp);
    const drift = Math.abs(labelCY - inputCY);
    if (drift > 4) {
      labelInputFlagged++;
      out.push({
        issueType: 'labelInputBaselineDrift', severity: 'low',
        selector: sel(lbl), bbox: bb(lbl),
        description: `Label "${(lbl.innerText || '').trim().slice(0, 30)}" center-Y is ${drift.toFixed(0)}px off its input's center. Use display:flex + align-items:center.`
      });
    }
  }

  // ── 3. Icon-text baseline drift (buttons / nav items) ──────────────
  let iconTextFlagged = 0;
  const iconContainers = document.querySelectorAll('button, a[href], [role="button"], .nav-item, .menu-item, [class*="nav-link"]');
  for (const c of iconContainers) {
    if (iconTextFlagged >= 4) break;
    if (!visible(c)) continue;
    const icon = c.querySelector('svg, i.fa, i.material-icons, i[class*="icon"], img');
    if (!icon || !visible(icon)) continue;
    const text = (c.innerText || '').trim();
    if (text.length < 2) continue;
    // Find the text node container — usually a span/label child
    const txtChild = [...c.children].find(ch => ch !== icon && visible(ch) && (ch.innerText || '').trim().length > 0);
    const textRef = txtChild || c;
    const iconCY = centerY(icon);
    const textBase = textBaseline(textRef);
    const r = icon.getBoundingClientRect();
    const tr = textRef.getBoundingClientRect();
    // Only meaningful if icon and text are side-by-side
    if (Math.abs(r.top - tr.top) > 24) continue;
    const drift = Math.abs(iconCY - (textBase - parseFloat(getComputedStyle(textRef).fontSize) / 2));
    if (drift > 4 && r.height > 12) {
      iconTextFlagged++;
      out.push({
        issueType: 'iconTextBaselineDrift', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Icon and adjacent text "${text.slice(0, 30)}" misaligned by ${drift.toFixed(0)}px on center-Y. Use display:flex + align-items:center on the parent.`
      });
    }
  }

  // ── 4. Inline group height mismatch ────────────────────────────────
  // Look at parents that contain 2+ inline buttons / inputs in one row
  let inlineGrpFlagged = 0;
  const groupParents = document.querySelectorAll('.button-group, .btn-group, .form-row, .input-group, .filter-bar, .actions, [role="toolbar"], .toolbar');
  for (const grp of groupParents) {
    if (inlineGrpFlagged >= 2) break;
    if (!visible(grp)) continue;
    const items = [...grp.querySelectorAll('button, input:not([type="hidden"]), select, a.btn, [role="button"]')]
      .filter(visible)
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(x => x.r.width > 30 && x.r.height > 16);
    if (items.length < 2) continue;
    // Same row
    const tops = items.map(x => x.r.top);
    const tDelta = Math.max(...tops) - Math.min(...tops);
    if (tDelta > 16) continue;   // wrapping — not same row
    const heights = items.map(x => x.r.height);
    const hDelta = Math.max(...heights) - Math.min(...heights);
    if (hDelta > 6) {
      inlineGrpFlagged++;
      out.push({
        issueType: 'inlineGroupHeightMismatch', severity: 'low',
        selector: sel(grp), bbox: bb(grp),
        description: `Inline group has ${items.length} items in same row with heights ${Math.round(Math.min(...heights))}-${Math.round(Math.max(...heights))}px (${hDelta.toFixed(0)}px variance). Standardize control height.`
      });
    }
  }

  // ── 5. Table cell content baseline mixed ───────────────────────────
  let tableCellFlagged = 0;
  const rows = document.querySelectorAll('tbody tr, [role="rowgroup"]:not(:first-child) [role="row"]');
  for (const row of [...rows].slice(0, 8)) {
    if (tableCellFlagged >= 2) break;
    if (!visible(row)) continue;
    const cells = [...row.querySelectorAll('td, [role="cell"]')].filter(visible);
    if (cells.length < 2) continue;
    // Get content position within each cell
    const positions = cells.map(c => {
      const cr = c.getBoundingClientRect();
      // The "content top" — first visible child's top
      const child = [...c.children].find(visible) || c;
      const chr = child.getBoundingClientRect();
      return chr.top - cr.top;   // offset from cell top
    });
    const pDelta = Math.max(...positions) - Math.min(...positions);
    if (pDelta > 6) {
      tableCellFlagged++;
      out.push({
        issueType: 'tableCellContentBaselineMixed', severity: 'low',
        selector: sel(row), bbox: bb(row),
        description: `Row has cells with content at varying vertical positions (${pDelta.toFixed(0)}px drift between earliest and latest). Use vertical-align: middle on all td.`
      });
    }
  }

  // ── 6. Form action alignment inconsistency across forms ────────────
  const forms = [...document.querySelectorAll('form, [role="form"]')].filter(visible);
  if (forms.length >= 2) {
    const sides = forms.map(f => {
      const actions = [...f.querySelectorAll('.form-actions, .actions, .button-row, .modal-footer')].filter(visible)[0];
      const lastBtn = f.querySelector('button[type="submit"], input[type="submit"], button:not([type])');
      const ref = actions || lastBtn;
      if (!ref) return null;
      const fr = f.getBoundingClientRect();
      const rr = ref.getBoundingClientRect();
      const center = rr.left + rr.width / 2;
      const formCenter = fr.left + fr.width / 2;
      if (center < formCenter - 30) return 'left';
      if (center > formCenter + 30) return 'right';
      return 'center';
    }).filter(Boolean);
    const distinct = new Set(sides);
    if (distinct.size >= 2 && sides.length >= 2) {
      out.push({
        issueType: 'formActionsAlignmentInconsistent', severity: 'low', selector: 'body',
        description: `Page has ${forms.length} forms with action buttons aligned to ${[...distinct].join(' + ')}. Pick one alignment for all forms (right-aligned is most common).`
      });
    }
  }

  // ── 7. Vertical center misaligned (header logo + brand name etc.) ───
  // Check for icon+text combos in header/nav landmarks
  let vcFlagged = 0;
  const hosts = [...document.querySelectorAll('header, [role="banner"], .header, .navbar')].filter(visible);
  for (const host of hosts.slice(0, 2)) {
    if (vcFlagged >= 1) break;
    const children = [...host.children].filter(visible).filter(c => {
      const r = c.getBoundingClientRect();
      return r.width > 30 && r.height > 16;
    });
    if (children.length < 2) continue;
    // Same row only
    const tops = children.map(c => c.getBoundingClientRect().top);
    if (Math.max(...tops) - Math.min(...tops) > 16) continue;
    const cys = children.map(c => centerY(c));
    const delta = Math.max(...cys) - Math.min(...cys);
    if (delta > 8) {
      vcFlagged++;
      out.push({
        issueType: 'verticalCenterMisaligned', severity: 'low',
        selector: sel(host), bbox: bb(host),
        description: `Header row has ${children.length} top-level elements with center-Y drift of ${delta.toFixed(0)}px. Use display:flex + align-items:center on the header.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~14 findings per cell
- Self-skips: page with no breadcrumb / no form / no table / no header returns []
- The `breadcrumbItemsBaselineDrift` catches your "Students > Students" baseline-drift screenshot (title and breadcrumb at different baselines)
- The `labelInputBaselineDrift` and `iconTextBaselineDrift` are companion patterns for inline form/icon alignment
