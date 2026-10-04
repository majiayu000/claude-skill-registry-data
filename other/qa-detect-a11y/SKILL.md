---
name: qa-detect-a11y
section: accessibility
description: "Detects unnamed buttons, missing lang attribute, absent skip-to-content link, and missing/disabled viewport meta."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it checks
- Button or `[role=button]` with no accessible name (text/aria-label/title/aria-labelledby)
- `<html>` missing `lang` attribute
- No skip-to-content link (`<a href="#...">` with skip/jump/content text)
- Icon-sized `<img>` (<48px or src matches icon pattern) without alt
- **`viewportMetaMissing`** — `<meta name="viewport">` missing, OR has `user-scalable=no`, OR `maximum-scale=1` (zoom disabled). Catastrophic — breaks all mobile rendering.

## Probe (browser_evaluate)
```js
() => {
  const sel = el => {
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/)[0] : '';
    return (el.id ? `#${el.id}` : el.tagName.toLowerCase() + cls).slice(0,120);
  };
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // viewportMetaMissing
  const vp = document.querySelector('meta[name="viewport"]');
  if (!vp) {
    out.push({ issueType:'viewportMetaMissing', severity:'high', selector:'head',
      description:'No <meta name="viewport"> tag — page will not scale correctly on mobile devices. Add <meta name="viewport" content="width=device-width, initial-scale=1">' });
  } else {
    const content = (vp.getAttribute('content') || '').toLowerCase();
    if (content.includes('user-scalable=no') || content.includes('user-scalable=0')) {
      out.push({ issueType:'viewportMetaMissing', severity:'high', selector:'meta[name="viewport"]',
        description:`Viewport meta has user-scalable=no — users cannot zoom (accessibility violation). content="${content}"` });
    } else if (/maximum-scale\s*=\s*1(?![\d.])/.test(content)) {
      out.push({ issueType:'viewportMetaMissing', severity:'high', selector:'meta[name="viewport"]',
        description:`Viewport meta has maximum-scale=1 — restricts pinch zoom (accessibility violation). content="${content}"` });
    }
  }

  if (!document.documentElement.hasAttribute('lang')) {
    out.push({ issueType:'missingLang', severity:'high', selector:'html',
      description:"<html> element is missing the lang attribute — add lang='en' (or appropriate language code)" });
  }
  let skipFound = false;
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    if (/skip|jump|main.?content|content/i.test(a.innerText)) { skipFound = true; break; }
  }
  if (!skipFound) {
    out.push({ issueType:'noSkipLink', severity:'medium', selector:null,
      description:"Page has no skip-to-content link — add <a href='#main' class='sr-only focus:not-sr-only'>Skip to content</a> as the first focusable element" });
  }
  for (const el of document.querySelectorAll('button, [role="button"]')) {
    if (out.length >= 20) break;
    // Skip buttons that are not rendered — inside collapsed sidebars, hidden panels,
    // or framework-internal ghost elements (BBox 0×0 = user never sees or interacts with it)
    const br = el.getBoundingClientRect();
    if (br.width === 0 && br.height === 0) continue;
    // Also skip if any ancestor is display:none / visibility:hidden
    let hidden = false;
    let node = el.parentElement;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.display === 'none' || s.visibility === 'hidden') { hidden = true; break; }
      node = node.parentElement;
    }
    if (hidden) continue;
    // Skip elements positioned ENTIRELY OUTSIDE the viewport — off-screen drawers / settings
    // panels that overflow past the edge (their toggles sit at e.g. x=1465 on a 1280 viewport).
    // The user can't see or reach them, so flagging them as "no accessible name" is noise and
    // the annotation lands off-screen. (The off-screen panel itself is a separate layout finding.)
    const vw = window.innerWidth, vh = window.innerHeight;
    if (br.right <= 0 || br.bottom <= 0 || br.left >= vw || br.top >= vh) continue;
    // Skip password show/hide toggle buttons — qa-form-a11y owns password field accessibility.
    // Pattern: small button (≤40px) inside a container that also holds input[type="password"].
    const isSmall = br.width <= 40 && br.height <= 40;
    if (isSmall) {
      const pwdParent = el.closest('div, fieldset, form, .input-group, .input-wrapper, .p-input-icon-right, .p-password');
      if (pwdParent && pwdParent.querySelector('input[type="password"]')) continue;
    }
    // Skip chart library interactive elements — ApexCharts, Chart.js, Recharts, Highcharts, and
    // similar libraries attach role="button" to chart segments, slices, and legend items for
    // keyboard interactivity. These are NOT real buttons and have no innerText by design.
    // Flagging them produces false positives (e.g. "BUTTON NO NAME" on a donut chart slice).
    const inChartContainer = el.closest(
      '[class*="apexchart"], [class*="ApexChart"], [class*="recharts"], [class*="Recharts"],' +
      '[class*="highchart"], [class*="Highchart"], [class*="chartjs"], [class*="ChartJs"],' +
      '[class*="chart-container"], [class*="chart-wrap"], [class*="chart-widget"],' +
      'svg, canvas'
    );
    if (inChartContainer) continue;
    // Also skip any element whose tag is an SVG element (path, circle, g, rect — chart segments)
    if (el.ownerSVGElement || el.tagName === 'path' || el.tagName === 'circle' ||
        el.tagName === 'g' || el.tagName === 'rect' || el.tagName === 'polygon') continue;

    const text = (el.innerText || el.value || '').trim();
    const aria = (el.getAttribute('aria-label') || '').trim();
    const title = (el.getAttribute('title') || '').trim();
    // aria-labelledby may be a SPACE-SEPARATED list of IDs (Material slide-toggle, etc.) — resolve ALL.
    const labelledBy = el.getAttribute('aria-labelledby');
    const labelText = labelledBy ? labelledBy.split(/\s+/).map(id => ((document.getElementById(id) || {}).innerText || '').trim()).join(' ').trim() : '';
    // A wrapping labeled component (mat-slide-toggle, a <label>, an .mdc-form-field) names the control too.
    const wrap = el.closest('label, mat-slide-toggle, mat-checkbox, mat-radio-button, .mdc-form-field, [class*="slide-toggle"], [class*="form-field"]');
    const wrapText = wrap && wrap !== el ? (wrap.innerText || '').trim() : '';

    // --- Icon detection (all flavors) ---
    // Many icon-only buttons (edit/delete table actions, toolbar icons) contain only an icon
    // element with no visible text. innerText returns '' for all of these, so without this
    // detection they all incorrectly fall into buttonNoName (high severity).
    //
    // Covered:
    //  • SVG icons  — <button><svg>…</svg></button>  (SVG <title> or aria-label names it)
    //  • Icon fonts — <button><i class="pi pi-pencil"></i></button>  (PrimeNG, FontAwesome,
    //                 Bootstrap Icons, Material Design Icons, Ionicons, Phosphor, etc.)
    //  • Image icons — <button><img src="edit.png"></button>  (img alt names it)

    // SVG child
    const svgChild = el.querySelector('svg');
    const svgTitle = svgChild ? ((svgChild.querySelector('title') || {}).textContent || '').trim() : '';
    const svgAriaLabel = svgChild ? (svgChild.getAttribute('aria-label') || '').trim() : '';
    const svgAriaHidden = svgChild ? svgChild.getAttribute('aria-hidden') === 'true' : false;
    const svgNamed = svgChild && !svgAriaHidden && (svgTitle || svgAriaLabel);

    // Icon-font child — <i> or <span> carrying an icon class from any major icon library
    // innerText returns '' for these even though they render a visible glyph.
    const iconFontChild = el.querySelector(
      'i[class*="pi "], i[class*="pi-"],' +          // PrimeNG  (pi pi-pencil)
      'i[class*="fa "], i[class*="fa-"],' +           // FontAwesome 4/5/6 (fa fa-edit, fas fa-trash)
      'i[class*="bi "], i[class*="bi-"],' +           // Bootstrap Icons
      'i[class*="mdi "], i[class*="mdi-"],' +         // Material Design Icons
      'i[class*="ion-"],' +                           // Ionicons
      'i[class*="ti "], i[class*="ti-"],' +           // Tabler Icons
      'span[class*="material-icon"],' +               // Material Icons (but these DO have innerText)
      'span[class*="p-button-icon"],' +               // PrimeNG button icon span
      'span[class*="anticon"],' +                     // Ant Design Icons
      'span[class*="iconfont"]'                       // Generic iconfont pattern
    );

    // Image icon child — <button><img src="edit.png"></button>
    const imgChild = !svgChild && !iconFontChild ? el.querySelector('img') : null;
    const imgAlt = imgChild ? (imgChild.getAttribute('alt') || '').trim() : '';
    const imgNamed = imgChild && imgAlt;

    // Determine if this is an icon-only button (visual icon, no text)
    const isIconOnly = (svgChild || iconFontChild || imgChild) && !text;

    if (!text && !aria && !title && !labelText && !wrapText && !svgNamed && !imgNamed) {
      if (isIconOnly) {
        // Icon-only button — the icon renders visually but screen readers get nothing.
        // Severity: medium (not high) because sighted users CAN see and use it;
        // the fix is straightforward: add aria-label describing the action.
        let hint = '';
        if (iconFontChild) {
          // Extract action hint from icon class (pi-pencil → "Edit", pi-trash → "Delete", etc.)
          const cls = (iconFontChild.className || '').toLowerCase();
          if (/pencil|edit|pen/.test(cls))        hint = 'e.g. aria-label="Edit"';
          else if (/trash|delete|remove/.test(cls)) hint = 'e.g. aria-label="Delete"';
          else if (/eye|view|show/.test(cls))       hint = 'e.g. aria-label="View"';
          else if (/plus|add|create/.test(cls))     hint = 'e.g. aria-label="Add"';
          else if (/download|export/.test(cls))     hint = 'e.g. aria-label="Download"';
          else if (/upload|import/.test(cls))       hint = 'e.g. aria-label="Upload"';
          else if (/refresh|reload|sync/.test(cls)) hint = 'e.g. aria-label="Refresh"';
          else if (/close|times|x/.test(cls))       hint = 'e.g. aria-label="Close"';
          else if (/search|magnif/.test(cls))       hint = 'e.g. aria-label="Search"';
          else                                       hint = 'add aria-label describing the action';
        } else if (svgChild) {
          hint = svgAriaHidden
            ? 'SVG is aria-hidden — add aria-label to the <button> element'
            : 'add <title> inside the <svg> or aria-label on the <button>';
        } else if (imgChild) {
          hint = 'add alt="[action]" to the <img> inside the button';
        }
        out.push({ issueType:'iconOnlyButtonNoName', severity:'medium', selector:sel(el),
          description:`Icon-only button ${sel(el)} has no accessible name — screen readers cannot identify what it does. Fix: ${hint}`, bbox: bb(el) });
      } else {
        // Truly unnamed button — no icon, no text, nothing
        out.push({ issueType:'buttonNoName', severity:'high', selector:sel(el),
          description:`Button ${sel(el)} has no accessible name (no text, no aria-label, no title) — add visible text content or aria-label="[action name]"`, bbox: bb(el) });
      }
    }
  }
  for (const img of document.querySelectorAll('img')) {
    if (out.length >= 20) break;
    const src = img.src || '';
    const isIcon = /icon|ico|sprite|glyph/i.test(src) || (img.width < 48 && img.height < 48);
    if (isIcon && !img.hasAttribute('alt') && !img.getAttribute('aria-hidden')) {
      out.push({ issueType:'iconNoAlt', severity:'medium', selector:sel(img),
        description:`Icon image ${src.slice(0,80)} has no alt text`, bbox: bb(img) });
    }
  }
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| buttonNoName | high | "Button {sel} has no accessible name — add text, aria-label, or title" |
| iconOnlyButtonNoName | medium | "Icon-only button with unnamed SVG — add aria-label to button or <title> to SVG" |
| missingLang | high | "<html> missing lang attribute" |
| noSkipLink | medium | "No skip-to-content link" |
| iconNoAlt | medium | "Icon image missing alt" |
| viewportMetaMissing | high | "Viewport meta missing OR scaling disabled (user-scalable=no / maximum-scale=1)" |

## False-positive guards
- **Chart library elements** — `role="button"` on ApexCharts/Recharts/Highcharts/Chart.js segments and legend items are skipped entirely (chart interactivity handles, not real buttons)
- **SVG descendants** — `<path>`, `<circle>`, `<g>`, `<rect>` with `role="button"` inside SVG/canvas are skipped
- **SVG-named icon buttons** — `<button><svg><title>Edit</title>…</svg></button>` passes (SVG title names the button)
- **Icon-font buttons** — `<button><i class="pi pi-pencil"></i></button>` → `iconOnlyButtonNoName` (medium), NOT `buttonNoName` (high); action hint inferred from class name (pi-pencil → "Edit", pi-trash → "Delete", etc.)
- **Image icon buttons** — `<button><img alt="Edit"></button>` passes (img alt names the button)
- **Severity split** — `buttonNoName` (high) = truly unnamed with no icon at all; `iconOnlyButtonNoName` (medium) = has a visual icon but screen readers still get nothing
