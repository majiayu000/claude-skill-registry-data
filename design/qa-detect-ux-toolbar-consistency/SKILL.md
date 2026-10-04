---
name: qa-detect-ux-toolbar-consistency
section: visual
description: "Detects inconsistencies inside button groups / toolbars: some buttons have shadow, others don't (icon-only have shadow, text buttons don't), mixed border-radius, mixed padding, mixed sizes, mixed casing of labels. Catches the 'buttons in the same toolbar look like different design systems' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasToolbar]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `toolbarShadowInconsistent` | medium | Some buttons in same toolbar have `box-shadow`, others don't — visual depth mismatch (your Students page: text buttons flat, icon buttons with shadow) |
| `toolbarButtonSizeMixed` | medium | Buttons in same toolbar have noticeably different heights or paddings (> 6px delta) — visual rhythm broken |
| `toolbarButtonRadiusInconsistent` | low | Buttons in same toolbar use different `border-radius` values (e.g. 4px vs 8px vs 12px) |
| `toolbarTextIconButtonStyleMix` | low | Same toolbar mixes text-only buttons (`Download Template`) with icon-only buttons (`+`) styled differently — pick one or unify |
| `toolbarLabelCasingMixed` | low | Buttons in same toolbar mix label casing: Title Case (`Download Template`), ALL CAPS (`SAVE`), sentence case (`Cancel changes`) |
| `toolbarBorderColorInconsistent` | low | Buttons in same toolbar use different border colors (some bordered, some not) |

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

  // Find toolbar / button-group containers
  const containerSel = '.toolbar, [class*="toolbar"], .actions, [class*="actions-bar"], [class*="button-bar"], [class*="btn-group"], .button-group, [role="toolbar"], [class*="action-buttons"], header, .page-actions';
  const containers = [...document.querySelectorAll(containerSel)].filter(visible);
  // Also detect implicit toolbars: any element with 3+ inline buttons in a row
  const implicit = [];
  for (const el of document.querySelectorAll('div, header, section')) {
    if (!visible(el)) continue;
    const btns = [...el.querySelectorAll(':scope > button, :scope > a.btn, :scope > [role="button"], :scope > .button')]
      .filter(visible);
    if (btns.length >= 3) {
      const tops = btns.map(b => b.getBoundingClientRect().top);
      const range = Math.max(...tops) - Math.min(...tops);
      if (range < 16) implicit.push(el);  // same row
    }
  }
  const allContainers = [...new Set([...containers, ...implicit])].slice(0, 5);

  for (const tb of allContainers) {
    // Get visible buttons in this toolbar (direct or nested)
    const btns = [...tb.querySelectorAll('button, a.btn, [role="button"], input[type="button"], input[type="submit"]')]
      .filter(visible);
    if (btns.length < 2) continue;
    // Filter only the ones on the same horizontal band (toolbar row)
    const tops = btns.map(b => b.getBoundingClientRect().top);
    const dominantTop = tops.sort((a, b) => a - b)[Math.floor(tops.length / 2)];
    const row = btns.filter(b => Math.abs(b.getBoundingClientRect().top - dominantTop) < 12);
    if (row.length < 2) continue;

    // Collect style profile per button
    const profiles = row.map(b => {
      const cs = getComputedStyle(b);
      const r = b.getBoundingClientRect();
      const text = (b.innerText || b.value || '').trim();
      const hasIcon = !!b.querySelector('svg, i, img');
      return {
        el: b,
        text,
        hasIcon,
        height: Math.round(r.height),
        width: Math.round(r.width),
        paddingY: parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom),
        radius: parseFloat(cs.borderTopLeftRadius) || 0,
        shadow: cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : null,
        borderColor: cs.borderTopColor,
        borderWidth: parseFloat(cs.borderTopWidth) || 0
      };
    });

    // ── 1. Shadow inconsistency ─────────────────────────────────────────
    const withShadow = profiles.filter(p => p.shadow).length;
    const withoutShadow = profiles.length - withShadow;
    if (withShadow >= 1 && withoutShadow >= 1) {
      out.push({
        issueType: 'toolbarShadowInconsistent', severity: 'medium',
        selector: sel(tb), bbox: bb(tb),
        description: `Toolbar has ${profiles.length} buttons: ${withShadow} with box-shadow, ${withoutShadow} without. Inconsistent visual depth — apply shadow to ALL or NONE.`
      });
    }

    // ── 2. Button size mixed ────────────────────────────────────────────
    const heights = profiles.map(p => p.height);
    const hDelta = Math.max(...heights) - Math.min(...heights);
    if (hDelta > 6 && heights.length >= 2) {
      out.push({
        issueType: 'toolbarButtonSizeMixed', severity: 'medium',
        selector: sel(tb), bbox: bb(tb),
        description: `Toolbar button heights range ${Math.min(...heights)}-${Math.max(...heights)}px (${hDelta}px variance). Standardize to one button height.`
      });
    }

    // ── 3. Border-radius inconsistent ───────────────────────────────────
    const radii = [...new Set(profiles.map(p => Math.round(p.radius)))];
    if (radii.length >= 2 && Math.max(...radii) - Math.min(...radii) >= 4) {
      out.push({
        issueType: 'toolbarButtonRadiusInconsistent', severity: 'low',
        selector: sel(tb), bbox: bb(tb),
        description: `Toolbar uses ${radii.length} different border-radius values: ${radii.join('px, ')}px. Use one corner radius.`
      });
    }

    // ── 4. Text + icon-only mix with different styles ───────────────────
    const textBtns = profiles.filter(p => p.text.length > 0 && !p.hasIcon);
    const iconBtns = profiles.filter(p => p.text.length === 0 && p.hasIcon);
    const textWithIcon = profiles.filter(p => p.text.length > 0 && p.hasIcon);
    if (textBtns.length >= 1 && iconBtns.length >= 1) {
      // Are they styled differently?
      const textStyle = textBtns[0];
      const iconStyle = iconBtns[0];
      const shadowMismatch = !!textStyle.shadow !== !!iconStyle.shadow;
      const heightMismatch = Math.abs(textStyle.height - iconStyle.height) > 4;
      if (shadowMismatch || heightMismatch) {
        out.push({
          issueType: 'toolbarTextIconButtonStyleMix', severity: 'low',
          selector: sel(tb), bbox: bb(tb),
          description: `Toolbar mixes ${textBtns.length} text-only and ${iconBtns.length} icon-only buttons with different styling${shadowMismatch ? ' (shadow mismatch)' : ''}${heightMismatch ? ' (height mismatch)' : ''}. Unify the visual treatment.`
        });
      }
    }

    // ── 5. Label casing mixed ───────────────────────────────────────────
    const casings = new Set();
    for (const p of profiles) {
      if (!p.text || p.text.length < 2) continue;
      if (/^[A-Z][A-Z\s]+$/.test(p.text)) casings.add('UPPER');
      else if (/^[A-Z][a-z]+(\s[A-Z][a-z]+)+$/.test(p.text)) casings.add('Title');
      else if (/^[A-Z][a-z]/.test(p.text) && /\s[a-z]/.test(p.text)) casings.add('sentence');
      else if (/^[a-z]/.test(p.text)) casings.add('lower');
    }
    if (casings.size >= 2) {
      out.push({
        issueType: 'toolbarLabelCasingMixed', severity: 'low',
        selector: sel(tb), bbox: bb(tb),
        description: `Toolbar button labels mix casings: ${[...casings].join(' + ')}. Pick one (Title Case is most common for action buttons).`
      });
    }

    // ── 6. Border color inconsistent ────────────────────────────────────
    const borders = profiles.map(p => p.borderWidth > 0 ? p.borderColor : 'none');
    const distinctBorders = [...new Set(borders)];
    if (distinctBorders.length >= 3) {
      out.push({
        issueType: 'toolbarBorderColorInconsistent', severity: 'low',
        selector: sel(tb), bbox: bb(tb),
        description: `Toolbar buttons use ${distinctBorders.length} different border treatments (${distinctBorders.slice(0,3).join(' / ')}). Either all bordered with same color or all borderless.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: 6 issue types × up to 5 toolbars = max ~30 findings per cell, but per-toolbar typically 1-3
- Self-skips: page with no toolbars / button groups returns []
- The `toolbarShadowInconsistent` catches your Students page: Download Template + Import Student (flat) vs + and refresh icons (with shadow)
- The `toolbarTextIconButtonStyleMix` catches the same pattern: text buttons styled differently than icon buttons
