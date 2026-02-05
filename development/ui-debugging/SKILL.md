---
name: ui-debugging
description: Standardized protocol for describing UI/layout issues in screenshots. Helps Claude understand visual problems clearly on first look by using a structured format for image communication.
---

# UI Debugging Skill - Clear Visual Communication

## Purpose

This skill establishes a **standardized protocol** for describing UI/layout issues in screenshots. Instead of back-and-forth clarification questions, use this structured format to communicate visual problems clearly and completely on the first try.

## Three Communication Modes

### Mode 1: **Screenshot Protocol** - How to Capture & Describe
When sharing screenshots of UI issues, follow this structured approach.

### Mode 2: **Layout Issue Template** - Standardized Problem Description
Use this template when describing broken layouts, missing content, or visual problems.

### Mode 3: **Visual Inspection Checklist** - Completeness Verification
Before sharing a screenshot, verify you've included all necessary details.

---

## Mode 1: Screenshot Protocol - Best Practices

### When to Take Full-Page Screenshots

**Take a full-page screenshot when:**
- Content extends below the visible viewport
- Layout issues involve stacking or overflow
- You want to show what's visible AND what's cut off
- Multiple sections need to be visible together

**How to take full-page screenshots:**

**Browser (Chrome/Firefox):**
1. Open DevTools (F12 or right-click → Inspect)
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Screenshot" → Select "Capture full page screenshot"
4. File saves automatically to Downloads

**Alternative (using console):**
```javascript
// Scroll to top first
window.scrollTo(0, 0);
// Then take screenshot via DevTools as above
```

**Mobile/Responsive:**
- Use DevTools Device Toolbar (Ctrl+Shift+M)
- Set desired viewport size
- Follow same screenshot process

### When to Take Viewport Screenshots

**Take a viewport-only screenshot when:**
- Issue is fully visible on current screen
- You're showing specific interaction moment
- Fixed/sticky elements are important to context

### What to Include in Screenshot Description

When sharing a screenshot, **always include**:

1. **URL/Page**: Where is this? (e.g., "mobile.gfyag.com/predictor")
2. **What you see**: Describe visible elements (e.g., "Black header bar with PREDICTOR title")
3. **What's missing/wrong**: What should be there? (e.g., "Crop toggle buttons should appear below header")
4. **Expected layout**: What should the page show? (e.g., "Should show: header → crop toggles → prediction card → spotlight indicator")
5. **Cut-off content**: Is content cut off? (e.g., "Gray background extends below, and below that is another white/light colored section that's cut off")
6. **Platform/browser**: What are you using? (e.g., "Chrome on web", "Safari on iPhone 14")
7. **Viewport size**: How wide/tall? (e.g., "1024x768", "mobile viewport")

---

## Mode 2: Layout Issue Template - Standardized Format

When describing a layout problem, use this exact format:

```
### Screenshot Description

**URL:** [full URL or page name]

**Platform:** [Web/iOS/Android, Browser/App, Viewport size if applicable]

**What I See (Currently):**
- [Element 1]: [what color/state it is]
- [Element 2]: [what color/state it is]
- [Background color/pattern]
- [Any visible text or content]

**What I Expected to See:**
- [Element 1]: Should be [where/what]
- [Element 2]: Should be [where/what]
- [Expected layout flow]

**The Problem:**
- [Specific issue - missing content, wrong position, wrong size, etc.]
- [Impact - page unusable, navigation broken, can't see content, etc.]

**Layout Layers (Top to Bottom):**
1. [First visible section] - [color, height]
2. [Second section] - [color, height]
3. [What's cut off below] - [if applicable]
4. [More layers below] - [if applicable]

**Additional Context:**
- [Relevant info: recent changes, works on mobile but not web, etc.]
```

### Example: Using the Template

```
### Screenshot Description

**URL:** mobile.gfyag.com/predictor

**Platform:** Chrome on Web, 1920x1080 viewport

**What I See (Currently):**
- Black header bar with "PREDICTOR" title (centered)
- Chat icon (left) and +33 notification badge (right)
- Below header: Large gray/off-white rectangular area filling entire rest of viewport
- No content visible below the gray area (but something else is below, cut off)

**What I Expected to See:**
- Crop toggle buttons (BEAN, CORN, WHEAT)
- Prediction card with price and arrow
- Spotlight indicator component
- Various text labels and data

**The Problem:**
- All page content is missing/invisible
- The layout is pushing content down below the fold
- A different colored background is visible below the gray area, indicating content exists but is positioned off-screen

**Layout Layers (Top to Bottom):**
1. Black header bar (fixed/sticky)
2. Gray/off-white background section (~70% viewport height)
3. White/light background section below (cut off/not visible)

**Additional Context:**
- Works fine on mobile/native app
- Issue is web-platform specific
- Last working state: [commit hash or date if known]
```

---

## Mode 3: Visual Inspection Checklist

**Before sharing a screenshot, verify you've answered:**

- [ ] **URL/Page Name** - Exactly where is this?
- [ ] **Platform** - Web/mobile? Browser? Viewport size?
- [ ] **Visible Elements** - What DO you see? (colors, text, structure)
- [ ] **Missing/Wrong Elements** - What SHOULD be there?
- [ ] **Layout Flow** - Describe top-to-bottom or expected hierarchy
- [ ] **Colors/Backgrounds** - Note background colors explicitly (gray, white, transparent, etc.)
- [ ] **Cut-off Content** - Is anything cut off? What's above/below?
- [ ] **Context** - When did this break? What changed?
- [ ] **Expected vs Actual** - Be explicit about the difference
- [ ] **Impact** - Why is this a problem? What's broken?

---

## Usage Scenarios

### Scenario 1: Layout Extends Below Viewport

```
Problem: "Page only shows header, rest is blank"

Better: "The page header (black bar) is visible, but below it is a large
gray background area. At the bottom of the viewport I can see the edge
of a white/light colored section, which means content exists below but
is off-screen. The crop toggle buttons should appear in that gray area
but they're invisible."
```

### Scenario 2: Component Not Rendering

```
Problem: "The form is broken"

Better: "The form container (light gray box) renders correctly, but the
input fields inside are not visible. The labels appear but the actual
input elements are missing. The submit button at the bottom is present
but disabled (grayed out)."
```

### Scenario 3: Responsive Issue

```
Problem: "Looks bad on mobile"

Better: "On iPhone 14 (390x844 viewport), the navigation header is cut off
horizontally. Menu items that fit on desktop are overlapping. The sidebar
that appears on desktop (1920px) is completely hidden, but the main content
area didn't expand to fill that space - it's still the same width, leaving
a blank gray area on the right side."
```

---

## Why This Protocol Matters

### Without the Protocol (Back-and-Forth)
```
You: "The page looks broken"
Me: "What's broken specifically?"
You: "The content doesn't show"
Me: "What content? What do you see instead?"
You: "Gray area"
Me: "Is that the whole page? What's the page URL?"
[... 5 more questions ...]
```

### With the Protocol (Clear First Time)
```
You: [Uses screenshot + template format]
Me: [Understands the problem immediately, can fix it]
```

---

## Integration with Claude Code

When you use this skill, mention it in your request:

```
"Use the ui-debugging skill to describe this screenshot..."
```

Or I'll automatically recognize when you're providing visual feedback and apply the protocol.

---

## Quick Checklist - Before Saying "The Page is Broken"

1. **Take full-page screenshot** (not just viewport if content is cut off)
2. **Use the template** (provide all sections)
3. **Be specific about colors** (gray, white, black, etc. - not just "blank")
4. **Show the layers** (what's visible, what's hidden, what's below)
5. **State expected vs actual** (don't assume I know what should be there)
6. **Add context** (URL, platform, viewport, when it broke)

---

## Reference: Full Screenshot Command Examples

### Chrome Full Page Screenshot
```bash
# DevTools → Ctrl+Shift+P → "Capture full page screenshot"
# Or: Right-click → Inspect → Ctrl+Shift+P → "Capture full page screenshot"
```

### Firefox Full Page Screenshot
```bash
# Right-click → Take Screenshot → "Save full page"
# Or: Hamburger → Tools → Browser Tools → Take Screenshot
```

### Using JavaScript (Any Browser)
```javascript
// In DevTools console:
// Scroll to top first
window.scrollTo(0, 0);

// Then manually take screenshot via DevTools
// OR use headless browser automation (Python/Playwright)
```

### Playwright (for automated screenshots)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    page.screenshot(path='full_page.png', full_page=True)
    browser.close()
```

---

## Remember

The goal is **clarity on first contact**. When you describe a UI issue, assume I haven't seen the page before. Be explicit. Be complete. Use the template.

This saves time and prevents the back-and-forth game of "guess what the problem is."
