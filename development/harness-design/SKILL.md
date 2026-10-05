---
name: harness-design
description: >-
  Quality harness for design-dna Phase 3 output with browser-based visual
  verification. After an agent generates a design from a Design DNA JSON +
  user content, this skill acts as a verification and scoring layer —
  collecting all page resources via console/network inspection, performing
  section-by-section screenshot comparison against the reference website,
  frame-by-frame animation sampling, and driving a correction loop until
  the output is ship-ready. Use this skill when: (1) a design has been
  generated from a Design DNA JSON and needs quality verification against
  a reference URL, (2) you want to score how faithfully output matches its
  DNA spec AND the original website visually, (3) you need to review and
  correct design drift using real browser rendering evidence, or (4) you
  are iterating on a design and want structured pass/fail gates with
  screenshot proof before delivery.
  Triggers on "harness", "verify design", "score design", "design QA",
  "check design fidelity", "design review against DNA", "design quality gate",
  "audit design output", "does this match the DNA", "compare with reference",
  "visual comparison", "screenshot comparison".
metadata:
  displayName: design-dna-harness
  icon: "🔬"
  color: '#b6d4e2'
  pinned: true
---

# Design DNA Harness

A browser-based verification-loop skill that scores and corrects agent-generated designs against both the source DNA JSON specification and the original reference website. Instead of guessing from code alone, the harness opens both pages in a real browser, collects resources, takes screenshots, samples animation frames, and produces evidence-backed quality reports.

**Core philosophy**: The agent that generates the design is the horse. This skill is the harness — reins, feedback loops, and quality gates that ensure the output faithfully expresses the DNA intent. The browser is the ground truth.

## When to Activate

- After design-dna Phase 3 produces HTML output
- When a user provides a Design DNA JSON, generated HTML, and a reference URL for review
- When iterating on a design that isn't matching its DNA spec or reference visually
- Whenever the user says "harness", "verify", "score", "QA", "audit", "compare" in the context of design output

## Inputs Required

1. **DNA JSON** — the Design DNA specification (immutable source of truth)
2. **Generated HTML** — the output to verify (file path or URL to a local dev server)
3. **Reference URL** — the original website that Phase 2 extracted DNA from (visual ground truth)
4. *(Optional)* **User intent notes** — additional context about priority areas

## Auxiliary Skills

The harness delegates to domain-specific skills for deep verification of specialized effects. Read them when the corresponding effect type is detected in Pass 0.

| Effect Type | Auxiliary Skill | When to Read |
|---|---|---|
| WebGL / Canvas / Shader effects | `web-shader-extractor` | canvas-info.json shows WebGL context or shader code detected in bundle |
| GSAP ScrollTrigger / scroll animations | `gsap-scrolltrigger` | JS bundle contains `ScrollTrigger` or scroll-linked animations detected |
| Three.js / R3F / 3D scenes | `3d-web-experience` | canvas-info.json `dataEngine` shows Three.js/Babylon/Spline |

The `web-shader-extractor` skill also provides infrastructure scripts used directly in Pass 0:
- `~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs` — Playwright script that extracts rendered DOM, canvas-info, network requests, screenshot, and console log in one pass
- `scan-bundle.sh` — identifies framework signatures in JS bundles

## Verification Loop

Five-pass verification: resource audit first, then mechanical token checks, visual comparison, perceptual review, and finally effects audit. Loop until pass or max iterations.

### Pass 0: Resource Audit

Collect runtime data from both pages to establish a factual baseline before any subjective assessment. This pass answers: "Did everything load correctly?"

**Primary path (Playwright available):**

Run `fetch-rendered-dom.mjs` on both pages. This produces structured output in `/tmp/rendered/`:

```bash
# Reference page
node ~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs '<REFERENCE_URL>'
# Move output to reference directory
mkdir -p /tmp/harness/ref && mv /tmp/rendered/* /tmp/harness/ref/

# Generated page (serve locally first if file path)
node ~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs '<GENERATED_URL>'
mkdir -p /tmp/harness/gen && mv /tmp/rendered/* /tmp/harness/gen/
```

Each directory contains:
- `dom.html` — rendered DOM after JS execution
- `canvas-info.json` — WebGL context details, engine version, component tree
- `network.json` — all network requests with status codes, types, sizes
- `screenshot.png` — initial viewport screenshot
- `console.log` — runtime console messages (errors, warnings, info)

Then run framework identification:
```bash
bash ~/.claude/skills/web-shader-extractor/scripts/scan-bundle.sh /tmp/harness/gen/*.js
bash ~/.claude/skills/web-shader-extractor/scripts/scan-bundle.sh /tmp/harness/ref/*.js
```

**Fallback path (browser MCP only):**

When Playwright is unavailable, use the browser MCP tools instead:

1. `browser_navigate` to the generated page URL (use `newTab: true`)
2. `browser_network_requests` to capture all loaded resources
3. `browser_console_messages` to capture runtime errors
4. `browser_take_screenshot` for initial viewport capture
5. Repeat steps 1-4 for the reference URL in a new tab

**Comparison checklist:**

For each resource category, compare reference vs. generated:
- Fonts: same families loaded? Same CDN source?
- JS libraries: same frameworks? Compatible versions?
- WebGL engine: same type (Three.js / Babylon / PixiJS / Raw WebGL)?
- Console errors: generated page should have zero errors that reference page doesn't have
- Resource completeness: no 404s, no CORS blocks

Record findings using check codes R1–R10. Read [references/verification-checks.md](references/verification-checks.md) for the full checklist.

### Pass 1: Mechanical Checks (Token Fidelity)

Deterministic pass/fail against `design_system` values, now enhanced with real browser rendering data.

**Step 1: DOM structure inspection**
1. `browser_navigate` to the generated page
2. `browser_snapshot` to capture the accessibility tree and DOM structure
3. Verify semantic HTML structure matches DNA expectations

**Step 2: Computed style extraction**

Inject JavaScript via the browser console to extract actual rendered values. Navigate to the generated page and use `browser_console_messages` to read results after injecting extraction code through `browser_click` on the console or via a bookmarklet URL pattern.

Key values to extract and compare against DNA JSON:
- `getComputedStyle` for font-family, font-size, color, background-color, padding, margin, border-radius on representative elements (h1, h2, body p, buttons, cards, nav)
- Actual rendered color values (rgb format) vs DNA hex values
- Actual pixel spacing vs DNA spacing scale

**Step 3: Cross-verification**

For each check in [references/verification-checks.md](references/verification-checks.md):
1. Extract expected value from DNA JSON
2. Extract actual rendered value from browser (Step 2) or source code
3. Extract reference page value from Pass 0 data
4. Three-way compare: DNA vs. generated vs. reference
5. Record: `✅ PASS`, `⚠️ DRIFT (expected X, found Y, ref Z)`, or `❌ MISS`

**Categories**: color palette, typography, spacing, shape, elevation, layout, components, motion, effects presence, tech stack, accessibility.

### Pass 2: Visual Comparison (Section-by-Section Screenshots)

Side-by-side screenshot comparison between generated page and reference page. This pass captures what the user actually sees.

**Procedure:**

1. Open both pages in separate browser tabs:
   ```
   browser_navigate url=<GENERATED_URL> newTab=true
   # Note the viewId for generated page
   browser_navigate url=<REFERENCE_URL> newTab=true
   # Note the viewId for reference page
   ```

2. Take full-page screenshots of both:
   ```
   browser_take_screenshot fullPage=true filename="gen-full.png" viewId=<genViewId>
   browser_take_screenshot fullPage=true filename="ref-full.png" viewId=<refViewId>
   ```

3. Section-by-section comparison — scroll both pages to matching positions and take viewport screenshots at each stop:
   ```
   # For each section N (increment by viewport height):
   browser_scroll direction="down" amount=<viewport_height> viewId=<genViewId>
   browser_take_screenshot filename="gen-section-N.png" viewId=<genViewId>
   
   browser_scroll direction="down" amount=<viewport_height> viewId=<refViewId>
   browser_take_screenshot filename="ref-section-N.png" viewId=<refViewId>
   ```

4. For each section pair, compare and record:
   - Layout alignment (grid, spacing, element positioning)
   - Color consistency (dominant colors, contrast)
   - Typography (heading sizes, body text, hierarchy)
   - Component fidelity (buttons, cards, nav, footer)
   - Content density and whitespace rhythm

Record findings using check codes VA1–VA8. Read [references/verification-checks.md](references/verification-checks.md) for the full checklist.

### Pass 3: Perceptual Review (Style Fidelity)

Qualitative assessment of `design_style` alignment, now informed by the screenshot evidence from Pass 2 rather than code-level guessing.

For each `design_style` field:
1. State the DNA specification
2. Refer to the Pass 2 screenshots as evidence
3. Assess whether the generated output embodies the intended style
4. Rate: **Strong match** / **Partial match** / **Mismatch**
5. If mismatch — describe deviation with reference to specific screenshot sections + concrete fix

**Categories**: aesthetic mood, visual language, composition, imagery, interaction feel, brand voice.

### Pass 4: Effects Audit (Frame Sampling & Deep Verification)

Deep inspection of `visual_effects` implementation using animation frame capture and auxiliary skill expertise. This pass goes beyond "is the effect present?" to "does the effect look and behave the same?"

**Step 1: Identify effect types from Pass 0 data**

Read `canvas-info.json` and `scan-bundle.sh` output to determine which auxiliary skills to consult:

- WebGL/Shader detected → read `web-shader-extractor` skill for shader parameter extraction
- ScrollTrigger detected → read `gsap-scrolltrigger` skill for scroll position verification
- Three.js/3D detected → read `3d-web-experience` skill for 3D rendering verification

**Step 2: Animation frame sampling**

For pages with animations (particles, shaders, transitions, scroll effects):

1. Navigate to generated page, wait 1-2 seconds for animations to initialize
2. Capture a burst of 5-8 frames at ~400ms intervals:
   ```
   browser_take_screenshot filename="gen-frame-1.png" viewId=<genViewId>
   browser_wait_for time=0.4
   browser_take_screenshot filename="gen-frame-2.png" viewId=<genViewId>
   browser_wait_for time=0.4
   # ... repeat for 5-8 frames
   ```
3. Repeat the same sequence on the reference page
4. Compare frame sequences:
   - Do both pages show animation/motion? (frame-to-frame differences exist)
   - Is the motion intensity similar? (amount of pixel change between frames)
   - Are the visual characteristics similar? (particle density, color shifts, blur amounts)

**Step 3: Scroll-triggered effect verification**

For pages with scroll-driven animations:

1. Identify key scroll trigger positions (from code analysis or gsap-scrolltrigger knowledge)
2. On both pages, scroll to just before each trigger point and take a screenshot
3. Scroll through the trigger zone slowly (small increments) taking screenshots
4. Scroll to just after the trigger zone and take a final screenshot
5. Compare the animation state at matching scroll positions

**Step 4: 3D and shader deep verification**

When 3D or shader effects are present:

1. Compare `canvas-info.json` engine type and version between pages
2. Verify canvas elements are rendering (not blank/black)
3. If `web-shader-extractor` identifies shader parameters, compare uniform values
4. Check for proper fallback (disable WebGL in browser, verify graceful degradation)

**Step 5: Performance profiling**

```
browser_profile_start viewId=<genViewId>
browser_wait_for time=3
browser_profile_stop viewId=<genViewId>
```

Read the profile summary to verify:
- Animation runs at consistent frame rate (no major drops)
- No excessive CPU usage from animation loops
- `requestAnimationFrame` is used (not `setInterval`)

**Step 6: Accessibility check**

Verify `prefers-reduced-motion` is respected:
- Check source code for `@media (prefers-reduced-motion: reduce)` or equivalent JS check
- Verify canvas resize handling (ResizeObserver or window resize listener)
- Verify animation cleanup/destroy paths exist

## Scoring

Read [references/rubric.md](references/rubric.md) for detailed scoring rules.

| Dimension | Weight | What It Measures |
|---|---|---|
| design_system (tokens) | 25% | DNA JSON field matching + actual rendered values |
| design_style (perception) | 20% | Qualitative style alignment based on screenshot evidence |
| visual_effects (rendering) | 20% | Effect implementation, animation frame similarity |
| resource_integrity | 10% | Resource loading, no errors, engine consistency |
| visual_alignment | 25% | Section-by-section screenshot comparison with reference |
| **Weighted Total** | 100% | 0–100 |

**Grades**: A (90–100) ship-ready · B (75–89) minor drift · C (60–74) significant deviation · D (40–59) major departure · F (0–39) does not represent DNA.

## Correction Loop

If score < 90:

1. **Fix plan** — ordered corrections, highest-impact first, referencing specific screenshot evidence
2. **Apply fixes** — modify HTML/CSS/JS directly, one category at a time
3. **Re-verify** — repeat Pass 0–4 on corrected output (can skip unchanged passes)
4. **Loop** until score ≥ 90 or 3 iterations reached

After 3 iterations without grade A → output final score with remaining issues and screenshot comparison, recommend accept-as-is or re-generate.

## Output Format

Always output a structured harness report with screenshot evidence:

```
## Design DNA Harness Report

### Summary
- Grade: [A/B/C/D/F] ([score]/100)
- design_system: [score]/100
- design_style: [score]/100
- visual_effects: [score]/100
- resource_integrity: [score]/100
- visual_alignment: [score]/100
- Iteration: [n]/3

### Pass 0: Resource Audit
- Reference resources: [count] requests, [errors] errors
- Generated resources: [count] requests, [errors] errors
- Engine match: [yes/no] ([ref engine] vs [gen engine])
- Font match: [yes/no]
- Key differences: [list]

### Pass 1: Mechanical Checks
[table of check results with ✅ ⚠️ ❌ indicators]
[three-way comparison: DNA vs Generated vs Reference]

### Pass 2: Visual Comparison
[section-by-section comparison with screenshot file references]
- Section 1 (hero): gen-section-1.png vs ref-section-1.png — [assessment]
- Section 2 (content): gen-section-2.png vs ref-section-2.png — [assessment]
- ...

### Pass 3: Perceptual Review
[field-by-field assessment referencing screenshot evidence]

### Pass 4: Effects Audit
- Animation presence: [match/mismatch]
- Frame sampling: gen-frame-1..N.png vs ref-frame-1..N.png — [assessment]
- Scroll effects: [verified at N trigger points]
- 3D/Shader: [engine match, rendering verified]
- Performance: [FPS assessment]
- Auxiliary skills consulted: [list]

### Fix Plan (if score < 90)
[ordered corrections with expected score impact, referencing specific screenshots]

### Corrected Output (if fixes applied)
[updated HTML or summary of changes]
```

## Integration with design-dna

Downstream companion workflow:
1. **design-dna Phase 2** → Extract DNA JSON from reference URL
2. **design-dna Phase 3** → Generate design from DNA + content
3. **design-dna-harness** → Verify against both DNA JSON and reference URL, score, correct
4. Loop to step 3 if needed

The harness **never modifies the DNA JSON**. It treats DNA as the immutable source of truth and only adjusts the generated output to conform.

## Reference Files

| When | Read |
|---|---|
| Pass 0-4: Browser operation procedures | [references/browser-verification.md](references/browser-verification.md) |
| Pass 1: Full mechanical check list | [references/verification-checks.md](references/verification-checks.md) |
| Scoring: Detailed rubric and weights | [references/rubric.md](references/rubric.md) |
| Shader/Canvas deep dive | `web-shader-extractor` skill |
| ScrollTrigger verification | `gsap-scrolltrigger` skill |
| 3D element verification | `3d-web-experience` skill |
