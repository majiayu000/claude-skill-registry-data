---
name: figma-pixel-perfect
description: >
  Iterative pixel-perfect implementation of Figma designs. Covers the full lifecycle:
  screen decomposition, component extraction, fixture data population, Playwright visual
  regression testing with pixelmatch, and convergence iteration. Use when implementing
  UI from Figma with verified visual fidelity — "pixel perfect", "match the design",
  "visual comparison", "compare to Figma", or iterating on implementation quality against
  Figma source of truth.
when_to_use: >
  Reach for this when implementing UI from a Figma comp and you need verified visual fidelity —
  screen decomposition, component extraction, fixture data, and Playwright + pixelmatch visual
  regression iterated to convergence. This is the visual-fidelity member of the Playwright trio:
  use writing-playwright-tests for functional E2E suites of your own app, and playwright-automation
  for RPA/scraping against external sites. Requires the Figma MCP (main session only).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
compatibility: Requires Figma MCP server (main session only), Figma REST API token, Playwright, @playwright/test
paths:
  - "**/*.{tsx,jsx,vue,html}"
  - "tests/visual/**"
  - "tests/__screenshots__/**"
---

# Figma Pixel-Perfect Implementation

End-to-end workflow for translating Figma designs into production code with verified visual
fidelity. Builds on `figma-implement-design` by adding a closed-loop verification cycle
with measurable convergence targets.

## Architecture: Three Tool Layers

| Layer | Tool | What It Does | Who Can Use It |
|-------|------|-------------|----------------|
| **Design Source** | Figma MCP (`get_design_context`, `get_screenshot`, `get_metadata`) | Read design intent: layout, tokens, screenshots | **Main session ONLY** — subagents cannot access MCP |
| **Design Export** | Figma REST API (`/v1/images/:fileKey`) | Download node PNGs to disk at 2x scale | Main session or subagents (with token) |
| **Verification** | Playwright (`toHaveScreenshot()` with pixelmatch) | Compare browser render against Figma baseline | Main session or subagents |

### Critical Constraint: Subagent MCP Access

**Subagents (dispatched via Agent tool) CANNOT access Figma MCP tools.** Only the main
orchestrating session has MCP access. This means:

1. The **main session** must fetch all Figma data (screenshots, design context, metadata)
   and save it to disk BEFORE dispatching subagents.
2. Subagents work from **committed files** — baseline PNGs, design context JSON, fixture data.
3. If a subagent needs additional Figma data, it must request it and wait for the main
   session to fetch it.

### Figma REST API vs MCP

| | REST API | MCP |
|---|---|---|
| **Auth** | Personal access token (`X-Figma-Token` header) | OAuth via remote server |
| **Rate limit** | ~30 req/min on `/v1/images/` (per account, not per token) | Separate limit, unaffected by REST |
| **Output** | JSON with S3 URLs → download PNGs to disk | Inline images in conversation |
| **Use for** | Batch downloading baselines to commit | Viewing designs inline, getting design context |
| **Subagent access** | Yes (pass token in prompt) | No |

**Rate limit recovery**: `/v1/images/` returns `retry-after` header (can be hours on Pro plan).
Use a secondary account's token if available. The `/v1/files/` and `/v1/me` endpoints have
separate, more generous limits.

---

## Phase 0: Screen Decomposition (Main Session)

**Goal**: Break Figma designs into a hierarchy of testable units.

### Step 1: Identify Target Screens

Start with the container node (section or page) that holds all screens. Use `get_metadata`
to discover the full inventory:

```
get_metadata(fileKey, containerNodeId)
```

Catalog every 1920x1080 frame. For each, note:
- Node ID
- Name (e.g., "Knowledge Base & Playbook - categories - all")
- What state it represents
- Which screens are state variations of the same page

**Key insight**: Most Figma files have many screens that are just DIFFERENT STATES of the
same page component. Group them:
- Browse views (different selections, filters, permissions)
- Reader views (different articles, panel states)
- Editor views (empty, populated, with modals open)
- Error/empty states

### Step 2: Extract Component Hierarchy

For each screen, use `get_metadata` to understand the node tree:

```
get_metadata(fileKey, screenNodeId)
```

Map the visual hierarchy:
```
Screen (1920x1080)
  ├── SideMenu (260px, shared across app — exclude from KB scope)
  ├── Header (64px, shared chrome)
  └── Content Area
      ├── Left Panel (sidebar, 410px)
      │   ├── Search input
      │   ├── Filter pills
      │   └── Category tree
      ├── Center Content (fluid)
      │   ├── Breadcrumb
      │   ├── Section headers
      │   └── Article cards / Reader
      └── Right Panel (390px)
          ├── Table of Contents
          └── Metadata grid
```

### Step 3: Identify Components and Their States

Components aren't always well-named in Figma. Look for:
- **Repeated patterns** — the same frame structure appearing multiple times (e.g., post cards)
- **Instance nodes** — Figma components that are reused
- **State variations** — selected vs default, expanded vs collapsed, admin vs limited role

For each component, extract:
- Figma node ID
- Dimensions (width × height)
- All visual properties via `get_design_context`:
  - Colors (as hex — Figma uses 0-1 RGBA, multiply by 255)
  - Typography (font family, size, weight, line-height, letter-spacing)
  - Spacing (padding, margin, gap)
  - Border (radius, width, color)
  - Icons (SVG assets from MCP asset URLs)
  - Images (embedded screenshots, illustrations)

### Step 4: Download Everything to Disk

Before dispatching any subagents, save:

**Baseline PNGs** (Figma REST API at `scale=2`):
```bash
export FIGMA_TOKEN="your-token"
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images/:fileKey?ids=NODE1,NODE2&format=png&scale=2"
# Returns JSON with S3 URLs, then:
curl -o tests/visual/baselines/<name>/<name>.png "<s3-url>"
```

**Design context JSON** (Figma REST API):
```bash
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/:fileKey/nodes?ids=NODE1,NODE2" \
  > tests/visual/design-context/components.json
```

**Commit both** so subagents can read them.

**Directory structure**:
```
tests/visual/
  baselines/                    ← Figma PNGs (SACRED — never overwrite)
    status-filter-pills/
      status-filter-pills.png
    post-card/
      post-card.png
    kb-page-categories/
      kb-page-categories.png
  design-context/               ← Figma node data as JSON
    screen1-components.json
    screen2-components.json
  specs/                        ← Playwright visual test specs
    atoms/
    components/
    sections/
    screens/
    integration/
  helpers/                      ← Test utilities
    dismissOverlay.ts
    injectMswAuth.ts
  test-results/                 ← Diff artifacts (gitignored)
  report/                       ← HTML report (gitignored)
```

---

## Phase 1: Infrastructure Setup

### Dev Harness

Create a route-based component gallery for isolated rendering:

```
src/pages/__dev/
  DevHarness.tsx              ← Route index with links to all harnesses
  MockStoreProvider.tsx       ← Wraps components with mock MobX/Redux store
  fixtures/
    kbFixtures.ts             ← Article data matching Figma content
    kbSidebarFixtures.ts      ← Tree/nav data matching Figma structure
  harnesses/
    StatusFilterPillsHarness.tsx
    PostCardHarness.tsx
    KBPageCategoriesHarness.tsx  ← Full-page harness with SideMenu stub
    ...
```

Key principles:
- Each harness renders ONE component at a fixed size inside `<Box data-testid="harness-root">`
- `MockStoreProvider` provides store context without API calls
- Fixture data must match Figma content EXACTLY (titles, dates, author names, article text)
- Dev-only routes gated behind `process.env.NODE_ENV === 'development'`
- Use `React.lazy()` for code-splitting

### Playwright Configuration

```typescript
// playwright.visual.config.ts
export default defineConfig({
  testDir: './tests/visual/specs',
  workers: 1,                    // Serial for deterministic rendering
  retries: 0,                    // No retries — diffs are real
  expect: {
    toHaveScreenshot: {
      threshold: 0.2,            // Per-pixel color sensitivity
      maxDiffPixels: 100,        // Override per-spec
      animations: 'disabled',
      caret: 'hide',
      scale: 'device',           // CRITICAL: capture at device DPR
    },
  },
  projects: [{
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      viewport: { width: 1920, height: 1080 },
      deviceScaleFactor: 2,      // CRITICAL: match Figma 2x export
      launchOptions: {
        args: ['--disable-gpu', '--font-render-hinting=none'],
      },
      colorScheme: 'light',
    },
  }],
  webServer: {
    command: 'npm run create',   // or npm run dev
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120_000,
  },
  snapshotDir: './tests/visual/baselines',
  snapshotPathTemplate: '{snapshotDir}/{arg}/{arg}{ext}',
});
```

### DPR Handling — The Biggest Gotcha

Figma exports at `scale=2` produce 3840×2160 images for a 1920×1080 viewport.
Playwright must capture at the same resolution.

**WRONG** (resets DPR to 1):
```typescript
test.beforeEach(async ({ page }) => {
  await page.setViewportSize({ width: 1920, height: 1080 }); // RESETS DPR!
});
```

**RIGHT** (preserves DPR):
```typescript
test.use({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 2,
});
```

**ALSO REQUIRED** in `toHaveScreenshot()`:
```typescript
await expect(locator).toHaveScreenshot('name.png', {
  maxDiffPixels: 415000,
  threshold: 0.3,
  scale: 'device',  // Without this, screenshot is at CSS pixels, not device pixels
});
```

### Fixture Data from Figma

Use MCP to extract actual content from Figma for fixture data:
```
get_design_context(fileKey, nodeId)
```

This returns the actual text content, colors, and structure. Use it to populate:
- Article titles, body text, excerpts
- Category/navigation tree names
- Author names, dates
- Tag labels
- Any embedded images (download asset URLs)

**The fixture data must match Figma exactly** — different text content accounts for
the largest portion of pixel diff in visual regression tests.

---

## Phase 2: Bottom-Up Component Iteration

Work bottom-up: atoms → components → sections → screens.

### Why Bottom-Up?

If a component is wrong, every screen containing it will have that error multiplied.
Fix components first, then screens automatically improve.

### Hierarchy

| Level | Example | Figma Source | Playwright Target |
|-------|---------|-------------|-------------------|
| Atom | StatusFilterPills, BreadcrumbNav | Crop/sub-node | `page.locator('[data-testid="..."]')` |
| Component | PostCard, CategoryTree, ArticleReader | Component frame | `page.locator('[data-testid="..."]')` |
| Section | KB Sidebar (search + pills + tree) | Region of screen | `page.locator('[data-testid="..."]')` |
| Screen | Full KB categories page | Full artboard | `page.locator('[data-testid="harness-root"]')` |

### Convergence Loop (Per Component)

```
ITERATION 1 — Structural alignment (target: 10% pixel diff)
  1. Read Figma baseline PNG
  2. Read design context JSON for exact values
  3. Take Playwright screenshot
  4. Compare — identify layout/structural differences
  5. Fix: wrong widths, missing elements, incorrect flex layout
  6. Re-screenshot and verify

ITERATION 2 — Visual refinement (target: 5% pixel diff)
  7. Read diff image — focus on colors, typography, spacing
  8. Fix: wrong font sizes, colors, padding, border radius
  9. Re-screenshot and verify

ITERATION 3 — Polish (target: 3% if achievable)
  10. Read diff image — remaining differences
  11. Fix: fine spacing, icon alignment, text content
  12. If remaining diff is anti-aliasing noise (text rendering), STOP
  13. Set maxDiffPixels to measured value + 10% margin

DONE when diff is under 5% (415K pixels for 3840×2160).
```

### Anti-Aliasing Reality

Chromium and Figma use different text rendering engines. At `threshold: 0.2`, every
text pixel registers as "different" because sub-pixel anti-aliasing produces slightly
different RGB values.

**The fix is threshold tuning, not code changes:**
- Text-heavy screens: `threshold: 0.75` filters out anti-aliasing while catching layout issues
- Icon/graphic-heavy screens: `threshold: 0.3` is tighter
- The `#3A3A46` dark text on white has ~75% LAB distance — that's the boundary

**Structural regressions are STILL caught** at high thresholds because:
- A missing 1250×40px section header = 100K+ pixels of wrong color
- A removed card = 200K+ pixels of exposed background
- A shifted panel = massive contiguous diff block

Set tight `maxDiffPixels` budgets per screen to catch these.

---

## Phase 3: Screen-Level Convergence

After components pass individually, verify full screens.

### Full-Screen Harnesses

For each Figma screen, create a harness that composes all components:
- SideMenu stub (260px dark rectangle — exclude real SideMenu from KB scope)
- KB page header (title + search + action icons)
- All content panels with fixture data matching Figma

### TinyMCE / Third-Party Component Masking

Components like TinyMCE render in iframes with their own CSS — they'll never
pixel-match Figma's static mockup. Options:

1. **Use the real component** (preferred) — render live TinyMCE with the API key.
   The toolbar/chrome will be close to Figma. Accept higher diff tolerance.
2. **Mask the region** — apply CSS to cover the iframe with a solid color before
   screenshot, so only the surrounding layout is compared.
3. **Exclude from comparison** — take element-level screenshots of non-iframe regions.

### Embedded Images in Articles

Figma may show screenshots/illustrations embedded in article body content. These are
`<img>` tags in the HTML body, NOT modal overlays. Extract the image from Figma
(`get_screenshot` on the internal frame node) and save as a static asset:

```
src/assets/images/kb/add-task-form-screenshot.png  ← source
public/assets/images/kb/...                         ← CRA serves from public/
```

Reference in fixture HTML: `<img src="/assets/images/kb/add-task-form-screenshot.png" />`

---

## Phase 4: Real App Verification

Harnesses prove components work in isolation. Real app verification proves they
compose correctly within the actual application shell.

### MSW Integration

Wire fixture data into MSW (Mock Service Worker) handlers so the real app pages
render with the same data as harnesses:

1. **Auth bypass**: Add MSW handler for login endpoint + app settings endpoint
2. **KB data**: Sync MSW fixture data with harness fixtures (same categories, articles, tree)
3. **Playwright auth injection**: Use `page.addInitScript()` to write auth token to
   localStorage BEFORE React mounts (NOT `page.evaluate()` which runs after)

### Integration Tests

Test real app routes (not harnesses):
- Navigate to `/crm/knowledge-base` with auth injected
- Verify page structure (sidebar, content, panels)
- Test interactive behaviors (category selection, panel collapse, navigation)
- Compare real page screenshot against harness screenshot for structural match

---

## Baseline Management — SACRED RULES

1. **Figma baseline PNGs are GROUND TRUTH** — they represent what the designer intended.
2. **NEVER run `--update-snapshots`** on Figma baselines.
3. **NEVER overwrite baselines with browser screenshots** — this creates circular
   comparisons that always pass but prove nothing.
4. **Diff means YOUR CODE is wrong**, not the baseline.
5. **Agents WILL try to regenerate baselines** if not explicitly told not to.
   Every agent prompt must include the rule.
6. **Update baselines only when**: Figma designs change, and you re-export from Figma.

---

## Agent Dispatch Pattern

### Pre-Dispatch Checklist (Main Session)

Before dispatching a subagent for pixel-perfect work:

- [ ] All target Figma screenshots downloaded as PNGs to `tests/visual/baselines/`
- [ ] Design context saved as JSON to `tests/visual/design-context/`
- [ ] Embedded images/assets saved to `src/assets/` or `public/`
- [ ] Fixture data in harness files matches Figma content
- [ ] All files committed (subagents read from git)
- [ ] Agent prompt includes: "NEVER overwrite Figma baseline PNGs"
- [ ] Agent prompt includes: "NEVER run --update-snapshots"
- [ ] Agent prompt includes Figma API token (for additional REST API calls if needed)

### Agent Prompt Template

```
You are running pixel-perfect iteration for [component/screen].
Compare browser renders against FIGMA-EXPORTED baseline PNGs.

## CRITICAL RULES
1. NEVER overwrite baseline PNGs — they are Figma ground truth
2. NEVER run --update-snapshots
3. Diff means YOUR CODE is wrong — fix the code, not the baseline
4. Iterate until pixel diff < [target] — don't do one pass and report

## Baselines
- [list baseline paths]

## Design Context
- [path to JSON]

## Figma API Token (for additional data if needed)
export FIGMA_TOKEN="..."

## Convergence Targets
- Round 1: maxDiffPixels [generous], threshold 0.3 (structural)
- Round 2: maxDiffPixels [medium], threshold 0.5 (refinement)
- Round 3: maxDiffPixels [tight], threshold 0.75 (polish)
```

### Parallelization

Split work by component independence:
- **Agent 1**: Sidebar components (CategoryTree, SearchOverlay, StatusFilterPills)
- **Agent 2**: Content components (PostCard, ArticleListView, ArticleReader)
- **Agent 3**: Panel components (TableOfContents, PrimaryDetailsPanel)
- **Agent 4**: Full screens (after components converge)

Use `isolation: "worktree"` for parallel agents to avoid file conflicts.

---

## Quick Reference: Key Measurements

| Property | Value |
|----------|-------|
| Figma export scale | 2x |
| 1920×1080 at 2x | 3840×2160 pixels |
| Total pixels | ~8.3M |
| 5% target | ~415K pixels |
| 3% target | ~249K pixels |
| Anti-aliasing noise floor | ~1-2% at threshold 0.2 |
| Text-safe threshold | 0.75 (filters font anti-aliasing) |
| Playwright DPR setting | `deviceScaleFactor: 2` |
| Screenshot scale | `scale: 'device'` |
| Snapshot path template | `{snapshotDir}/{arg}/{arg}{ext}` |
