---
name: qa-detect-visual-regression
section: visual
description: "Compares visual snapshots to a stored baseline using a DOM-sampled perceptual hash computed via browser_evaluate + Canvas API. No external npm packages, no scripts/phash.cjs required. First audit establishes baseline; subsequent audits detect visual drift. Catches font fallbacks, color drift, layout shifts."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: false
cacheVersion: "2.0.0"
ownership: "exclusive: any visual regression finding (vs prior run baseline) belongs to this skill."
---

# qa-detect-visual-regression — Browser-Based Perceptual Hash (MCP-native)

Computes a 64-bit visual hash of the current viewport using the Canvas API inside `browser_evaluate`. No `sharp`, no `phash.cjs`, no npm packages needed. Compares to stored baseline at `.claude/visual-baseline/`.

## What it checks (4 issue types)

| Issue type | Severity | What it catches |
|---|---|---|
| `visualRegression` | medium | Full-viewport hash differs from baseline by > 8 bits (significant visual change) |
| `componentRegression` | medium | Key component (nav, hero, footer) region hash differs from baseline |
| `visualBaselineCreated` | info | First-run only — baseline established, no fix needed |
| `visualBaselineCorrupt` | low | Baseline file exists but is malformed — re-creating |

## Self-skip conditions

- If `customize.toml → [visual_regression].enabled = false` → skip
- If baseline directory is missing AND running in `--dry-run` → create baseline silently, emit no findings

## Storage layout

```
{project-root}/.claude/visual-baseline/
├── home-mobile-chromium.json       ← hash + metadata
├── login-desktop-chromium.json
└── ... (one file per route × viewport × browser)
```

`.claude/visual-baseline/` should be gitignored — baselines are environment-specific.

## Orchestrator flow

### Step 1 — Compute full-viewport hash

```
fullHash = browser_evaluate(probe.computeVisualHash, {
  gridW: 16,
  gridH: 16,
  regionSelector: null   // null = full viewport
})
// Returns { hash: "0x4c81abef2c40df88", sampleCount: 256, avgBrightness: 142 }
```

### Step 2 — Compute component hashes

For each well-known component (if visible):

```
components = browser_evaluate(probe.findKeyComponents)
// Returns [{name, selector, rect}] for nav, hero, footer

For each component:
  compHash = browser_evaluate(probe.computeVisualHash, {
    gridW: 8,
    gridH: 8,
    regionSelector: component.selector
  })
  Store as componentHashes[component.name] = compHash
```

### Step 3 — Load baseline

```
baselineKey = slugify(cell.route) + '-' + cell.viewportClass + '-' + cell.browser
baselinePath = '{project-root}/.claude/visual-baseline/' + baselineKey + '.json'

Use Bash: node -e "..." to read the file OR use the Read tool
Try to read baselinePath.
```

### Step 4 — Compare or create baseline

**If baseline does NOT exist:**
```
Write baseline:
{
  "fullHash": fullHash.hash,
  "componentHashes": componentHashes,
  "capturedAt": "<current ISO date>",
  "route": cell.route,
  "viewportClass": cell.viewportClass,
  "browser": cell.browser,
  "avgBrightness": fullHash.avgBrightness
}

→ emit visualBaselineCreated (info)
  description: "Visual baseline created for {cell.route} at {cell.viewportClass}/{cell.browser}"
  (This is an info finding, NOT filed as an ADO bug)
```

**If baseline EXISTS:**
```
Parse baseline JSON.
fullDistance = hammingDistance(baseline.fullHash, fullHash.hash)

If fullDistance > 8:
  → emit visualRegression (medium)
    evidence: {
      hammingDistance: fullDistance,
      threshold: 8,
      baselineCapturedAt: baseline.capturedAt,
      route: cell.route
    }

For each component in componentHashes:
  If baseline.componentHashes[component.name] exists:
    compDistance = hammingDistance(baseline.componentHashes[component.name], componentHashes[component.name])
    threshold = component.name === 'cta' ? 3 : component.name === 'nav' ? 4 : 6
    If compDistance > threshold:
      → emit componentRegression (medium)
        evidence: {
          component: component.name,
          hammingDistance: compDistance,
          threshold
        }
```

### Step 5 — Take screenshot for evidence

```
browser_take_screenshot()
```

## Probes (browser_evaluate)

```js
// probe.computeVisualHash — args: { gridW, gridH, regionSelector }
// Samples DOM element colors at a grid of points using elementFromPoint + getComputedStyle.
// Computes a perceptual brightness-based hash. No external packages, no Canvas drawImage limitations.
({gridW, gridH, regionSelector}) => {
  let region = { left: 0, top: 0, width: window.innerWidth, height: window.innerHeight };

  if (regionSelector) {
    const el = document.querySelector(regionSelector);
    if (!el) return { hash: null, sampleCount: 0, reason: 'region element not found' };
    const r = el.getBoundingClientRect();
    region = { left: r.left, top: r.top, width: r.width, height: r.height };
    if (region.width < 10 || region.height < 10) return { hash: null, sampleCount: 0, reason: 'region too small' };
  }

  const W = gridW || 16;
  const H = gridH || 16;
  const samples = [];

  for (let row = 0; row < H; row++) {
    for (let col = 0; col < W; col++) {
      const x = region.left + (col / W) * region.width + region.width / (W * 2);
      const y = region.top + (row / H) * region.height + region.height / (H * 2);

      const el = document.elementFromPoint(x, y);
      let brightness = 255; // default white

      if (el) {
        // Walk up to find a meaningful background color
        let cur = el;
        while (cur && cur !== document.documentElement) {
          const style = getComputedStyle(cur);
          const bg = style.backgroundColor;
          if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
            const m = bg.match(/[\d.]+/g);
            if (m && m.length >= 3) {
              // Weighted luminance (ITU-R BT.601)
              brightness = (parseFloat(m[0]) * 0.299 + parseFloat(m[1]) * 0.587 + parseFloat(m[2]) * 0.114);
              break;
            }
          }
          // Also consider text color if no background
          const color = style.color;
          if (color && cur === el) {
            const cm = color.match(/[\d.]+/g);
            if (cm && cm.length >= 3) {
              brightness = (parseFloat(cm[0]) * 0.299 + parseFloat(cm[1]) * 0.587 + parseFloat(cm[2]) * 0.114);
            }
          }
          cur = cur.parentElement;
        }
      }

      samples.push(brightness);
    }
  }

  // Compute average brightness
  const avg = samples.reduce((a, b) => a + b, 0) / samples.length;

  // Build 64-bit hash: bit = 1 if sample >= avg, 0 otherwise (first 64 samples)
  const hashSamples = samples.slice(0, 64);
  let hexHash = '0x';
  for (let i = 0; i < 64; i += 4) {
    const nibble = hashSamples.slice(i, i + 4).reduce((acc, val, j) => {
      return acc | ((val >= avg ? 1 : 0) << (3 - j));
    }, 0);
    hexHash += nibble.toString(16);
  }

  return {
    hash: hexHash,
    sampleCount: samples.length,
    avgBrightness: Math.round(avg)
  };
}
```

```js
// probe.findKeyComponents
() => {
  const componentDefs = [
    { name: 'nav',    selector: 'nav, header[role="banner"], mat-toolbar' },
    { name: 'hero',   selector: 'main > section:first-child, [class*="hero"], mat-card:first-of-type' },
    { name: 'footer', selector: 'footer, [role="contentinfo"]' },
    { name: 'cta',    selector: 'button[type="submit"], button[mat-raised-button], .btn-primary' }
  ];
  const result = [];
  for (const def of componentDefs) {
    const el = document.querySelector(def.selector);
    if (!el) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 10 || r.height < 10) continue;
    result.push({
      name: def.name,
      selector: def.selector,
      rect: { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }
    });
  }
  return result;
}
```

## Hamming distance (computed by orchestrator in JS, not a probe)

```js
// Inline in orchestrator — no Bash needed
function hammingDistance(hexA, hexB) {
  if (!hexA || !hexB) return 999; // treat missing hash as max distance
  const a = BigInt(hexA);
  const b = BigInt(hexB);
  let xor = a ^ b;
  let count = 0;
  while (xor > 0n) { count += Number(xor & 1n); xor >>= 1n; }
  return count;
}
```

## Baseline file I/O

The orchestrator uses the **Read tool** to read existing baselines and the **Write tool** to create new ones — no Bash, no Node script required.

Baseline file format:
```json
{
  "fullHash": "0x4c81abef2c40df88",
  "componentHashes": {
    "nav": "0xabcdef1234567890",
    "hero": "0x1234567890abcdef",
    "footer": "0x9876543210fedcba"
  },
  "capturedAt": "2026-06-08T10:00:00.000Z",
  "route": "/dashboard",
  "viewportClass": "desktop",
  "browser": "chromium",
  "avgBrightness": 142
}
```

## Configuration (customize.toml)

```toml
[visual_regression]
enabled                  = true
full_page_threshold      = 8     # hamming distance > this triggers finding
component_threshold      = 4     # tighter for components (override per-component below)
nav_threshold            = 4
hero_threshold           = 6
footer_threshold         = 4
cta_threshold            = 3
auto_update_baseline     = false
critical_routes          = []    # if non-empty, only run on these routes
```

## Hard rules

1. **NO `scripts/phash.cjs`** — hash computed entirely via `browser_evaluate` + `probe.computeVisualHash`. No `sharp`, no npm packages.
2. **NO Bash for image processing** — use the Read/Write tools for baseline I/O.
3. **`.claude/visual-baseline/` MUST be gitignored** — baselines are local.
4. **First audit always creates baseline, never emits regression** — `visualBaselineCreated` is info, not a bug.
5. **Threshold MUST be configurable** — different apps have different visual stability.
6. **NEVER overwrite baseline without `auto_update_baseline = true`**.

## Why this approach works without sharp

Instead of decoding a PNG image and computing DCT-based pHash (which requires `sharp`), this skill:
1. Samples the **rendered DOM color** at a 16×16 grid of viewport points using `elementFromPoint` + `getComputedStyle`
2. This captures the ACTUAL rendered pixel colors (including CSS, shadows, gradients, web fonts)
3. Computes brightness-based hash — same structure as standard dHash/pHash
4. The hash captures: background color changes, text color shifts, missing elements (point returns white), layout shifts (element at point changes type)

**Limitations vs sharp-based pHash:**
- Does not capture image content inside `<img>` tags or `<canvas>`
- Does not capture CSS `background-image` content
- These are acceptable trade-offs for a zero-dependency approach
