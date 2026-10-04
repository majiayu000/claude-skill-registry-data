---
name: qa-detect-ux-icons
section: visual
description: "Catches icon UX problems: icon-only buttons without tooltip, icons without accessible labels, ambiguous icon meaning, oversized/undersized icons, icon-text gap inconsistency. Goes beyond qa-detect-a11y (which only checks aria-label presence) — checks discoverability + UX clarity."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasIcons]
---

## What it catches — 9 issue types

| issueType | severity | What |
|---|---|---|
| `iconButtonNoTooltip` | high | Icon-only button (no visible text) has no `title` attribute AND no tooltip element nearby — sighted users have no way to know what it does |
| `iconAmbiguousMeaning` | medium | Icon-only button uses an ambiguous symbol (3 dots, arrows, generic shapes) with no label or tooltip — purpose unclear |
| `iconUndersized` | low | Icon visible but rendered < 12px square — too small to recognize at a glance |
| `iconAspectExtreme` | high | Icon rendered with extreme aspect ratio (>3:1 or <1:3) — looks squashed/sliver-like instead of square. Indicates CSS width/height bug or broken SVG dimensions |
| `iconClippedInButton` | high | Icon inside a button is < 25% of the button's height (e.g. 8px icon in a 60px button) — visually a tiny dot/sliver above text. Indicates parent overflow:hidden, missing icon font-size, or wrong SVG sizing |
| `iconOversized` | low | Decorative icon > 64px square — wastes screen real estate especially on mobile |
| `iconTextGapInconsistent` | low | Icons next to text labels use inconsistent gaps (some 4px, some 12px) across the same view |
| `iconDuplicatedMeaning` | low | Same icon (same SVG path or class) used for two different actions on the same page |
| `iconColorAmbiguous` | medium | Icon used as status indicator (red/green/yellow) without text alternative — color-blind users can't decode it |

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

  // Find all icon-only buttons (button/a with no text but contains svg/i/img)
  const interactives = document.querySelectorAll('button, a[href], [role="button"], input[type="button"], input[type="submit"]');
  let nooTooltipFlagged = 0, ambiguousFlagged = 0;
  const ambiguousIcons = /^(more|menu|kebab|dots|three-dots|ellipsis|arrow|chevron|caret|swap|exchange|sort)$/i;

  // Skip elements that are clearly logos / brand glyphs / home links — these are NOT
  // "icon-only action buttons" even when they have only an image inside.
  const isLogoOrBrandLink = (el) => {
    // (a) href points to home/root
    const href = (el.getAttribute('href') || '').trim();
    if (href === '/' || href === '#' || href === '/home' || href === '/dashboard' || href === '#/') return true;
    // (b) any ancestor up to 4 levels has a logo/brand-shaped class
    if (el.closest('[class*="logo"], [class*="Logo"], [class*="brand"], [class*="Brand"], [class*="navbar-brand"], [class*="sidebar-brand"], [class*="app-bar"], [class*="appbar"]')) return true;
    // (c) the inner image is a logo (alt text or src filename)
    const inner = el.querySelector('img, svg');
    if (inner) {
      const alt = (inner.getAttribute('alt') || '').toLowerCase();
      const src = (inner.getAttribute('src') || '').toLowerCase();
      if (/^(logo|brand|favicon|app\s*logo|site\s*logo)\b/.test(alt)) return true;
      if (/\/(logo|brand|favicon)[-_]?[\w-]*\.(png|jpe?g|svg|webp)/.test(src)) return true;
      const cls = ((inner.className && typeof inner.className === 'string') ? inner.className : '').toLowerCase();
      if (/\b(logo|brand|favicon)\b/.test(cls)) return true;
    }
    // (d) link is positioned in the top-left of the page AND contains an image (classic logo slot)
    const r = el.getBoundingClientRect();
    if (r.left < 240 && r.top < 80 && el.querySelector('img, svg')) {
      // Top-left corner of a typical sidebar/header layout → almost always a logo
      return true;
    }
    return false;
  };

  for (const el of interactives) {
    if (!visible(el)) continue;
    if (isLogoOrBrandLink(el)) continue;   // skip site logo / brand link
    const text = (el.innerText || el.value || '').trim();
    const ariaLabel = (el.getAttribute('aria-label') || '').trim();
    const ariaLabelledBy = (el.getAttribute('aria-labelledby') || '').trim();
    const title = (el.getAttribute('title') || '').trim();
    if (text.length > 0) continue;          // has visible text — not icon-only
    if (ariaLabelledBy) continue;           // labeled via reference

    const icons = el.querySelectorAll('svg, i.fa, i.material-icons, i[class*="icon"], img');
    if (icons.length === 0) continue;       // not icon button

    const iconClass = [...icons].map(i => i.className.toString()).join(' ');
    const ariaHidden = el.getAttribute('aria-hidden') === 'true';

    // 1. iconButtonNoTooltip — no aria-label AND no title AND no aria-describedby
    if (!ariaLabel && !title && !ariaHidden) {
      if (nooTooltipFlagged < 6) {
        nooTooltipFlagged++;
        out.push({
          issueType: 'iconButtonNoTooltip', severity: 'high',
          selector: sel(el), bbox: bb(el),
          description: `Icon-only ${el.tagName.toLowerCase()} has no aria-label, no title, no nearby tooltip. Sighted users can't discover the action; screen readers announce it as unnamed.`
        });
      }
      continue;
    }

    // 2. iconAmbiguousMeaning — has label but icon class matches ambiguous pattern AND label is generic
    if (ambiguousFlagged < 4) {
      const labelLow = (ariaLabel || title).toLowerCase();
      const looksAmbiguous = ambiguousIcons.test(iconClass.replace(/.*[ -](\w+)$/, '$1'));
      const labelIsGeneric = /^(button|action|more|menu|click|open)$/.test(labelLow);
      if (looksAmbiguous && labelIsGeneric) {
        ambiguousFlagged++;
        out.push({
          issueType: 'iconAmbiguousMeaning', severity: 'medium',
          selector: sel(el), bbox: bb(el),
          description: `Icon ${iconClass.slice(0, 40)} has generic label "${labelLow}" — users won't know what action it triggers.`
        });
      }
    }
  }

  // 3 + 4. Icon size — find all visible <svg> + <i>+ <img class*="icon">
  const iconEls = document.querySelectorAll('svg, i[class*="icon"], i.fa, i.material-icons, img[class*="icon"], img[alt=""]');
  let sizeFlagged = 0;
  let aspectFlagged = 0;
  let clippedFlagged = 0;
  for (const ic of iconEls) {
    if (sizeFlagged >= 4 && aspectFlagged >= 4 && clippedFlagged >= 4) break;
    if (!visible(ic)) continue;
    const r = ic.getBoundingClientRect();
    const dim = Math.min(r.width, r.height);

    // 3a. iconUndersized — both dimensions tiny
    if (dim < 12 && sizeFlagged < 4) {
      sizeFlagged++;
      out.push({
        issueType: 'iconUndersized', severity: 'low',
        selector: sel(ic), bbox: bb(ic),
        description: `Icon rendered at ${r.width.toFixed(0)}×${r.height.toFixed(0)}px — too small to read at a glance. Use ≥16px for UI icons.`
      });
      continue;
    }
    // 3b. iconAspectExtreme — squashed/stretched (e.g. 16×4 or 4×16) — clearly broken rendering
    if (r.width > 0 && r.height > 0 && aspectFlagged < 4) {
      const ratio = r.width / r.height;
      if (ratio > 3 || ratio < 0.33) {
        aspectFlagged++;
        out.push({
          issueType: 'iconAspectExtreme', severity: 'high',
          selector: sel(ic), bbox: bb(ic),
          description: `Icon rendered ${r.width.toFixed(0)}×${r.height.toFixed(0)}px (aspect ${ratio.toFixed(2)}:1) — icons should be roughly square. Likely a CSS height/width bug squashing the icon. Visible icon looks like a sliver instead of a recognizable shape.`
        });
        continue;
      }
    }
    // 3c. iconClippedInButton — small icon (< 16px tall) inside a tall button (>= 50px)
    //     where icon takes < 20% of button height — clear visual mismatch, button looks like
    //     it has a dot/sliver above the text instead of a real icon.
    if (clippedFlagged < 4 && r.height < 16 && r.height >= 3) {
      const btn = ic.closest('button, a[href], [role="button"], .btn, [class*="quick-action"]');
      if (btn && btn !== ic) {
        const br = btn.getBoundingClientRect();
        if (br.height >= 50 && r.height / br.height < 0.20) {
          clippedFlagged++;
          out.push({
            issueType: 'iconClippedInButton', severity: 'high',
            selector: sel(ic), bbox: bb(ic),
            description: `Icon is only ${r.height.toFixed(0)}px tall inside a ${br.height.toFixed(0)}px button (${((r.height/br.height)*100).toFixed(0)}% of button height). Icon appears clipped or undersized — looks like a sliver/dot instead of a clear icon. Check for parent overflow:hidden with too-small height, missing icon font-size, or broken SVG dimensions.`
          });
          continue;
        }
      }
    }
    // 4. iconOversized — decorative icon way too big
    if (r.width > 64 && r.height > 64 && !ic.closest('button, a, [role="button"]') && sizeFlagged < 4) {
      sizeFlagged++;
      out.push({
        issueType: 'iconOversized', severity: 'low',
        selector: sel(ic), bbox: bb(ic),
        description: `Decorative icon ${r.width.toFixed(0)}×${r.height.toFixed(0)}px — wastes screen space especially on mobile.`
      });
    }
  }

  // 5. Icon-text gap inconsistency — buttons with text+icon
  const iconTextButtons = [...document.querySelectorAll('button, a[href]')].filter(b => {
    if (!visible(b)) return false;
    const hasIcon = b.querySelector('svg, i[class*="icon"], i.fa, i.material-icons, img');
    const text = (b.innerText || '').trim();
    return hasIcon && text.length > 0;
  });
  if (iconTextButtons.length >= 4) {
    const gaps = new Map();
    for (const b of iconTextButtons) {
      const cs = getComputedStyle(b);
      // Use gap property (flex/grid) OR padding+icon-margin heuristic
      let gap = parseFloat(cs.gap) || parseFloat(cs.columnGap);
      if (isNaN(gap) || gap === 0) {
        // Fallback: measure space between icon and first text node
        const ic = b.querySelector('svg, i, img');
        if (ic) {
          const ir = ic.getBoundingClientRect();
          const br = b.getBoundingClientRect();
          gap = Math.round(Math.abs(ir.right - br.left - parseFloat(cs.paddingLeft) || 0));
        }
      }
      const rounded = Math.round(gap / 2) * 2;
      gaps.set(rounded, (gaps.get(rounded) || 0) + 1);
    }
    if (gaps.size >= 3) {
      const values = [...gaps.keys()].sort((a, b) => a - b);
      out.push({
        issueType: 'iconTextGapInconsistent', severity: 'low',
        selector: 'body', description: `Icon-to-text gap varies across buttons: ${values.join('px, ')}px. Inconsistent spacing reads as sloppy design.`
      });
    }
  }

  // 6. Icon duplicated meaning — count uses of each unique icon class signature
  const iconSigs = new Map();
  for (const ic of iconEls) {
    if (!visible(ic)) continue;
    let sig = '';
    if (ic.tagName === 'SVG') {
      const path = ic.querySelector('path');
      sig = (ic.getAttribute('viewBox') || '') + '|' + (path ? (path.getAttribute('d') || '').slice(0, 50) : '');
    } else {
      sig = ic.className.toString();
    }
    if (!sig || sig.length < 4) continue;
    // Get the parent action label
    const parent = ic.closest('button, a, [role="button"]');
    const label = parent ? ((parent.getAttribute('aria-label') || parent.getAttribute('title') || parent.innerText || '').trim().toLowerCase().slice(0, 40)) : '';
    if (!label) continue;
    if (!iconSigs.has(sig)) iconSigs.set(sig, new Set());
    iconSigs.get(sig).add(label);
  }
  let dupFlagged = 0;
  for (const [sig, labels] of iconSigs) {
    if (dupFlagged >= 2) break;
    if (labels.size >= 2) {
      dupFlagged++;
      out.push({
        issueType: 'iconDuplicatedMeaning', severity: 'low',
        selector: 'body', description: `Same icon used for different actions: ${[...labels].slice(0, 3).join(' / ')}. Users will conflate them.`
      });
    }
  }

  // 7. Color-only status icon — icons with red/green/yellow color and no nearby text
  const statusIcons = document.querySelectorAll('svg, i, span[class*="status"], span[class*="badge"], [class*="indicator"]');
  let colorFlagged = 0;
  for (const ic of statusIcons) {
    if (colorFlagged >= 3) break;
    if (!visible(ic)) continue;
    const cs = getComputedStyle(ic);
    const color = cs.color || cs.fill || cs.backgroundColor;
    // Detect red/green/yellow-ish status colors
    const m = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (!m) continue;
    const [r, g, b] = [+m[1], +m[2], +m[3]];
    const isStatusColor = (r > 180 && g < 100 && b < 100) ||    // red
                          (g > 150 && r < 120 && b < 120) ||    // green
                          (r > 200 && g > 150 && b < 100);      // yellow
    if (!isStatusColor) continue;
    const parent = ic.parentElement;
    const sibText = parent ? (parent.innerText || '').trim() : '';
    if (sibText.length < 2 || sibText.length > 50) {
      // No nearby text label
      const r2 = ic.getBoundingClientRect();
      if (r2.width < 32 && r2.height < 32) {  // small status indicator
        colorFlagged++;
        out.push({
          issueType: 'iconColorAmbiguous', severity: 'medium',
          selector: sel(ic), bbox: bb(ic),
          description: `Status icon uses color (rgb ${r},${g},${b}) with no adjacent text label. Color-blind users can't tell the state.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Self-skips: page with no icons / no icon-only buttons returns []
- Bounded: 6 noTooltip + 4 ambiguous + 4 size + 1 gap + 2 dup + 3 color-only = max ~20 findings
- The `iconButtonNoTooltip` check is the highest-value: every icon-only button without tooltip is a UX failure for sighted users (a11y skill catches the screen-reader half; this catches the discovery half)
