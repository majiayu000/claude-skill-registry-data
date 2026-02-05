---
name: website-replicator
description: Analyze and replicate website UI/animations. Use when asked to clone, replicate, or analyze a website's visual implementation.
---

# Website Replicator

Reconstruct website UI and scroll animations through systematic observation.

## Core Principle

**Observe effects, don't extract code.** We watch what changes and when, then generate equivalent code.

**Screenshots are analysis tools, not just artifacts.** They help Claude understand structure and animation, feeding back into the exploration strategy. The workflow is a continuous feedback loop:
- Take screenshot → analyze with Gemini → digest results → inform next DOM queries
- Multiple screenshots → compare changes → understand animation → guide sampling strategy
- Not a separate pipeline - screenshots inform and adjust the exploration in real-time

---

## WORKFLOW

### Phase 1: Initial Load & Overview

**Goal:** Get oriented, understand what we're working with

```
1. navigate_page(url, waitUntil: 'networkidle')
2. wait_for(3000)  -- let initial animations settle
3. take_screenshot(fullPage: true) → save as capture/overview.png
4. take_snapshot() → get accessibility tree
5. AUTOMATED: Call Gemini API with overview.png
   python scripts/gemini_analyzer.py overview capture/overview.png > data/gemini-overview.json
```

**Output:**
- `capture/overview.png` → Screenshot captured
- `data/gemini-overview.json` → Automated Gemini analysis with:
  - Layout structure (sections, pattern, breakpoints)
  - Likely animated elements (type, location, animation style)
  - Design patterns (colors, typography, spacing)
  - Notable elements (graphics, videos, interactive components)
- Accessibility snapshot → DOM structure reference

**No manual intervention required** - Gemini analysis happens automatically

---

### Phase 2: DOM Reconnaissance

**Goal:** Build watch list of elements likely to animate

**Strategy (try in order, use what works):**

```
ATTEMPT 1: Class/attribute heuristics
  evaluate_script → search for elements with:
    - Classes containing: animate, fade, slide, scroll, reveal, parallax, aos, gsap
    - Data attributes: data-aos, data-scroll, data-animate, data-speed
    - will-change set to anything other than 'auto'
  
ATTEMPT 2: Transform/opacity detection
  evaluate_script → find elements where:
    - transform !== 'none'
    - opacity !== '1'
    - These often indicate "starting state" of animations

ATTEMPT 3: Structural analysis (FLEXIBLE - let Chrome tell us what exists)
  evaluate_script → explore actual DOM structure:
    ```javascript
    () => {
      // Don't assume structure - discover it
      const sections = document.querySelectorAll('section, [class*="section"], .w-section');
      const cards = document.querySelectorAll('[class*="card"], [class*="item"]');
      const animated = document.querySelectorAll('[class*="fade"], [class*="slide"], [class*="animate"]');

      // Get real positions and dimensions
      return Array.from(new Set([...sections, ...cards, ...animated])).map(el => ({
        tag: el.tagName,
        classes: el.className,
        offsetTop: el.offsetTop,
        height: el.offsetHeight,
        // Calculate when this element would be interesting to capture
        viewportTrigger: el.offsetTop - window.innerHeight * 0.5
      }));
    }
    ```

  Claude inspects results → decides screenshot positions based on actual element locations
  - If elements clustered: fewer screenshots
  - If elements sparse: more screenshots
  - Adaptive, not programmatic

ATTEMPT 4: Smart scroll sampling (FLEXIBLE - adapt based on what we see)
  Step 1: Ask Chrome what's on the page
    evaluate_script → get element positions (see ATTEMPT 3)

  Step 2: Claude decides scroll positions
    - Around each major element's trigger point
    - Before/during/after viewport intersection
    - Not fixed intervals - based on actual content

  Step 3: For each position, capture with context
    evaluate_script → scroll to position
    evaluate_script → ask "what's visible now?"
      ```javascript
      () => {
        const visible = Array.from(document.querySelectorAll('section, [class*="card"]'))
          .filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.top < window.innerHeight && rect.bottom > 0;
          })
          .map(el => ({
            tag: el.tagName,
            id: el.id,
            classes: el.className.split(' ').slice(0, 3).join(' ')
          }));

        return {
          scrollY: window.scrollY,
          viewportHeight: window.innerHeight,
          visibleElements: visible
        };
      }
      ```
    take_screenshot → save with semantic name based on what's visible

  Claude can compare consecutive screenshots → skip if too similar

  FALLBACK: If DOM analysis unclear, use visual comparison
    take_screenshot at strategic positions (top, 1/4, 1/2, 3/4, bottom)
    AUTOMATED: Call Gemini API to compare screenshots
    python scripts/gemini_analyzer.py compare capture/scroll-*.png > data/gemini-animation-detection.json
    Parse JSON response → extract changed_elements list

FALLBACK: Manual specification
  Ask user: "I couldn't automatically detect animated elements.
            Can you tell me which sections/elements animate on this page?"
```

**Output:** `watchList[]` - array of CSS selectors to monitor
- Built from DOM heuristics OR Gemini visual analysis OR user input

---

### Phase 3: Animation Capture

**Goal:** Record how watched elements change during scroll

**FLEXIBLE APPROACH - Let Chrome guide the sampling:**

```
1. First, understand the scroll range and element positions
   evaluate_script → get page metrics and element locations:
     ```javascript
     () => {
       const elements = Array.from(document.querySelectorAll('[data-watched]')); // or watchList
       return {
         scrollHeight: document.documentElement.scrollHeight,
         viewportHeight: window.innerHeight,
         elements: elements.map(el => ({
           selector: el.id ? `#${el.id}` : el.className,
           offsetTop: el.offsetTop,
           height: el.offsetHeight
         }))
       };
     }
     ```

2. Claude decides sampling strategy based on results
   - If page is short (< 3000px): sample every 100px
   - If page is long (> 10000px): sample at element trigger points + every 500px
   - Adaptive, not hardcoded

3. For each sample position, ask Chrome what's happening
   evaluate_script → scroll to position
   evaluate_script → sample current state:
     ```javascript
     (selector) => {
       const el = document.querySelector(selector);
       if (!el) return null;
       const cs = getComputedStyle(el);
       const rect = el.getBoundingClientRect();
       return {
         scrollY: window.scrollY,
         transform: cs.transform,
         opacity: cs.opacity,
         rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height },
         // Let Chrome tell us what's actually set
         willChange: cs.willChange,
         filter: cs.filter
       };
     }
     ```

4. Claude inspects results → decides if more samples needed
   - If values changing rapidly: sample more densely in that range
   - If values stable: skip ahead
   - Flexible, responsive to actual animation behavior

ALTERNATIVE: Inject monitoring script (if page allows)
  - Only if CSP permits and page structure is simple
  - Otherwise, use manual sampling above
```

**Output:** Animation data - properties at each scroll position, adaptively sampled

---

### Phase 4: CSS Extraction

**Goal:** Capture static styles for replication

```
1. Extract computed styles (FLEXIBLE - based on what we found)
   For elements Claude identified as important:
     evaluate_script → getComputedStyle(el)
     → Capture: colors, fonts, spacing, borders, shadows, layout

   Claude decides which elements matter based on Phase 2 discovery

2. AUTOMATED: Extract design tokens via Gemini
   python scripts/gemini_analyzer.py tokens capture/overview.png > data/design-tokens.json
   → Provides: color palette, typography scale, spacing system, effects

3. Capture actual stylesheet content (if accessible)
   list_network_requests → filter for .css files
   → Note URLs for reference

4. Responsive behavior (ADAPTIVE)
   Claude asks: "Does this page look responsive?"
   - Check if viewport meta tag exists
   - Check if CSS has media queries

   If responsive:
     Take screenshots at key breakpoints (Claude decides based on media queries found)
     evaluate_script → sample key element styles at each size

   If not responsive:
     Skip responsive testing
```

**Output:**
- `data/styles.json` - Computed styles from DOM
- `data/design-tokens.json` - Design system from Gemini analysis
- `capture/responsive-*.png` - Responsive screenshots

---

### Phase 5: Asset Collection

**Goal:** Identify images, fonts, icons needed

```
1. list_network_requests → filter by type:
   - Images: .png, .jpg, .jpeg, .webp, .svg, .gif
   - Fonts: .woff, .woff2, .ttf, .otf
   - Icons: svg inline, icon fonts

2. Extract inline SVGs
   evaluate_script → find all <svg> elements
   → Capture outerHTML

3. Extract image references
   evaluate_script → find all <img> elements
   → Capture src, alt, dimensions

4. Note external dependencies
   list_network_requests → identify CDN resources
   → Font services (Google Fonts, Adobe Fonts)
   → Icon libraries (FontAwesome, etc.)
```

---

### Phase 6: Analysis & Generation

**Goal:** Transform captured data into usable code

**Animation analysis (FLEXIBLE - Claude interprets the data):**

```
Claude examines animation data for each watched element:
  - Identifies when values start changing (animation start)
  - Identifies when values stabilize (animation end)
  - Determines what properties changed (opacity, translateY, scale, etc.)
  - Infers trigger type by comparing scroll position to element position:
    * Immediate (starts at scroll 0)
    * Viewport-based (starts when element enters view)
    * Fixed position (starts at specific scroll value)
  - Infers easing by examining the curve of value changes

Claude adapts analysis based on what it actually sees in the data
```

**Component structure (AUTOMATED):**

```
OPTIONAL: For detailed component breakdown
  python scripts/gemini_analyzer.py components capture/overview.png main > data/components.json
  → Provides component hierarchy for code generation
```

**Generate code:**

```
Output in preferred format:
  - GSAP + ScrollTrigger (default)
  - CSS scroll-driven animations
  - Framer Motion (if React project)
  - Plain CSS transitions + IntersectionObserver

Include:
  - Initial state (CSS)
  - Animation code (JS or CSS)
  - Trigger configuration
```

**Verification (OPTIONAL):**

```
After generating output:
  1. Render generated code locally
  2. take_screenshot → capture/generated-output.png
  3. AUTOMATED: Compare with original
     python scripts/gemini_analyzer.py verify capture/overview.png capture/generated-output.png > data/verification.json
  4. Review priority_fixes from JSON response
  5. Iterate on fixes
```

---

## DECISION POINTS

### When something doesn't work:

| Situation | Action |
|-----------|--------|
| Can't find animated elements | Try structural analysis → Try visual comparison → Ask user |
| Script injection blocked | Use manual sampling approach |
| getComputedStyle returns unexpected values | Take screenshot, send to Gemini for visual analysis |
| Scroll doesn't work | Check for scroll hijacking, try scrollTo on body/documentElement |
| Elements not found by selector | Re-analyze DOM, try different selector strategy |
| Page requires interaction first | Look for modals/cookies, dismiss them, retry |

### When to use Gemini:

**AUTOMATED - No manual intervention:**
- Initial overview understanding (Phase 1)
- Visual comparison between scroll states (Phase 2)
- Design token extraction (Phase 4)
- Component breakdown (Phase 6, optional)
- Output verification (Phase 6, optional)

**How Gemini integrates with the workflow:**
1. Claude takes screenshot(s) at strategic moments
2. Calls Python helper: `python scripts/gemini_analyzer.py <command> <args>`
3. Gemini returns structured analysis (JSON)
4. **Claude digests the response** - extracts key insights
5. **Claude merges insights into current understanding** - adjusts strategy
6. Claude proceeds with informed DOM queries or next steps

Example flow:
- Screenshot overview → Gemini says "3 card sections likely animate"
- Claude searches DOM for cards → finds `.card-item` at specific positions
- Claude takes screenshots at those positions → Gemini confirms "fade + slide up"
- Claude samples opacity/transform at those positions → generates code

**All Gemini calls happen via Python helper:**
```bash
python scripts/gemini_analyzer.py <command> <args>
```

See [docs/gemini-integration.md](../../docs/gemini-integration.md) for implementation details.

---

## TOOLS USAGE

### Chrome DevTools MCP tools used:

```
navigate_page     - Load the target URL
wait_for          - Allow page/animations to settle  
take_screenshot   - Visual capture for Gemini analysis
take_snapshot     - Accessibility tree for structure
evaluate_script   - All DOM inspection and monitoring
resize_page       - Responsive testing
list_network_requests - Find CSS/assets
```

### Key evaluate_script patterns:

```javascript
// Get unique selector for element
function getSelector(el) {
  if (el.id) return '#' + el.id;
  if (el.className) {
    const classes = [...el.classList].join('.');
    const siblings = document.querySelectorAll(el.tagName + '.' + classes);
    if (siblings.length === 1) return el.tagName.toLowerCase() + '.' + classes;
  }
  // Fall back to nth-child
  const parent = el.parentElement;
  const index = [...parent.children].indexOf(el);
  return getSelector(parent) + ' > :nth-child(' + (index + 1) + ')';
}

// Sample element state
function sampleElement(selector) {
  const el = document.querySelector(selector);
  if (!el) return null;
  const cs = getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return {
    transform: cs.transform,
    opacity: cs.opacity,
    top: rect.top,
    left: rect.left,
    width: rect.width,
    height: rect.height
  };
}
```

**Note:** These are starting points. Adapt based on what the actual page structure looks like.

---

## OUTPUT STRUCTURE

```
/output/
├── capture/
│   ├── overview.png
│   ├── responsive-375.png
│   ├── responsive-768.png
│   ├── responsive-1024.png
│   ├── responsive-1440.png
│   └── scroll-samples/
│       └── scroll-{n}.png (if needed)
├── data/
│   ├── dom-structure.json
│   ├── animation-data.json
│   ├── styles.json
│   └── assets.json
├── analysis/
│   └── animation-breakdown.md
└── generated/
    ├── components/
    ├── styles/
    └── animations/
```

---

## ADAPTABILITY

This skill should **adapt, not fail**. When the "standard" approach doesn't work:

1. **Observe more** - Take more screenshots, sample more positions
2. **Try alternatives** - Different selectors, different timing, different tools
3. **Ask for help** - Use Gemini for visual analysis, ask user for hints
4. **Partial success is fine** - Capture what you can, note what you couldn't

The goal is **useful output**, not perfect automation.
