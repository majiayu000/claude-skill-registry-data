---
name: qa-screenshot-validation
description: Evaluate captured screenshots for layout issues, masked elements, and rendering problems. Use after taking screenshots to validate visual correctness and automatically resize viewport if elements are unexpectedly clipped.
---

# QA Screenshot Validation Skill

Validate captured screenshots for layout correctness and handle masked or clipped elements.

## Validation Process

After capturing each screenshot, evaluate it for:

1. **Element visibility** - Is the target element fully visible?
2. **Layout integrity** - Does the layout appear correct?
3. **Clipping/masking** - Are elements unexpectedly cut off?
4. **Overlapping** - Are elements overlapping incorrectly?
5. **Rendering issues** - Missing images, broken icons, etc.

## Common Issues to Detect

### Masked/Clipped Elements

| Issue | Indicators | Action |
|-------|------------|--------|
| Horizontal clipping | Element cut off on right edge | Resize viewport wider |
| Vertical clipping | Element cut off at bottom | Scroll or resize taller |
| Overflow hidden | Content abruptly ends | Check parent container |
| Modal cutoff | Dialog extends beyond viewport | Resize to fit modal |

### Layout Problems

| Issue | Indicators | Action |
|-------|------------|--------|
| Overlapping elements | Text over images, buttons over content | Document as bug |
| Misaligned elements | Uneven spacing, broken grid | Document as bug |
| Missing elements | Expected element not visible | Verify selector, check visibility |
| Broken responsive | Desktop layout on mobile viewport | Document as bug |

## Automatic Resize Logic

When an element appears clipped on **desktop viewport**:

```
IF element is clipped AND viewport is desktop (>1024px):
    1. Try increasing viewport width by 200px
    2. Retake screenshot
    3. If still clipped, try 1920x1080 (full HD)
    4. If still clipped, document as layout bug
```

### Playwright Resize Commands

```javascript
// Get current viewport
const viewport = page.viewportSize();

// Resize wider
await page.setViewportSize({
  width: viewport.width + 200,
  height: viewport.height
});

// Standard breakpoints
await page.setViewportSize({ width: 1920, height: 1080 }); // Full HD
await page.setViewportSize({ width: 1440, height: 900 });  // Laptop
await page.setViewportSize({ width: 1280, height: 720 });  // HD
```

## Mobile/Tablet Testing Rules

**IMPORTANT:** Do NOT auto-resize for mobile or tablet viewports.

| Viewport | Width Range | Auto-Resize? |
|----------|-------------|--------------|
| Mobile | 320-480px | **NO** - Document as bug |
| Tablet | 768-1024px | **NO** - Document as bug |
| Desktop | >1024px | YES - Try resize first |

### Why No Auto-Resize for Mobile/Tablet?

If an element is clipped on mobile/tablet viewport, it indicates a **real responsive design bug**:
- The design should adapt to smaller screens
- Clipping means the responsive CSS is broken
- Auto-resizing would hide the actual problem

### Mobile/Tablet Clipping Response

```
IF element is clipped AND viewport is mobile/tablet (<1024px):
    1. DO NOT resize viewport
    2. Document as responsive design bug
    3. Capture screenshot as evidence
    4. Note: "Element clipped at {width}px viewport - responsive issue"
```

## Validation Checklist

Run this checklist on each screenshot:

```markdown
## Screenshot Validation: {filename}

### Element Visibility
- [ ] Target element fully visible
- [ ] No unexpected clipping on edges
- [ ] Element not obscured by other elements

### Layout Check
- [ ] Spacing appears consistent
- [ ] Alignment looks correct
- [ ] No overlapping content
- [ ] Text is readable (not truncated)

### Responsive Behavior
- [ ] Layout appropriate for viewport size
- [ ] No horizontal scrollbar (unless expected)
- [ ] Touch targets adequate size (mobile)

### Rendering
- [ ] Images loaded correctly
- [ ] Icons displaying properly
- [ ] Fonts rendered correctly
- [ ] No missing assets (broken image icons)

### Result
- [ ] PASS - Screenshot valid
- [ ] FAIL - Issue detected (describe below)
- [ ] RETRY - Resized viewport and retaking
```

## Detection Heuristics

### Clipping Detection

Look for these visual indicators:

```
Horizontal clipping:
- Element touches right edge of viewport
- Text/content appears cut mid-word
- Button or input field partially visible
- Scrollbar appears unexpectedly

Vertical clipping:
- Element touches bottom edge
- Modal/dropdown extends beyond visible area
- Form fields cut off
- Footer missing or partial
```

### Overlap Detection

```
Overlapping indicators:
- Text appearing over images
- Multiple elements at same position
- Z-index conflicts (wrong element on top)
- Shadow/border appearing over content
```

## Viewport Breakpoints Reference

### Standard Testing Viewports

| Device | Width | Height | Use Case |
|--------|-------|--------|----------|
| iPhone SE | 375 | 667 | Small mobile |
| iPhone 14 | 390 | 844 | Standard mobile |
| iPhone 14 Pro Max | 430 | 932 | Large mobile |
| iPad Mini | 768 | 1024 | Small tablet |
| iPad Pro | 1024 | 1366 | Large tablet |
| Laptop | 1280 | 800 | Small desktop |
| Desktop | 1440 | 900 | Standard desktop |
| Full HD | 1920 | 1080 | Large desktop |

### Breakpoint Classification

```javascript
function getDeviceType(width) {
  if (width <= 480) return 'mobile';
  if (width <= 1024) return 'tablet';
  return 'desktop';
}

function shouldAutoResize(width) {
  return width > 1024; // Only desktop
}
```

## Automated Validation Flow

```
1. CAPTURE screenshot
   ↓
2. ANALYZE for issues
   - Check element boundaries vs viewport
   - Look for clipping indicators
   - Detect overlapping elements
   ↓
3. IF issues detected:
   ↓
   3a. Desktop viewport (>1024px)?
       → Try resize and recapture
       → If still broken, document bug
   ↓
   3b. Mobile/Tablet viewport (≤1024px)?
       → DO NOT resize
       → Document as responsive bug
   ↓
4. LOG validation result
   ↓
5. CONTINUE to next screenshot
```

## Issue Documentation Format

When a validation issue is found:

```markdown
### Screenshot Issue: {filename}

**Viewport:** {width}x{height} ({device_type})
**Element:** {element_description}
**Issue Type:** Clipped | Overlapping | Missing | Rendering

**Description:**
{What appears wrong in the screenshot}

**Expected:**
{What should be visible}

**Actual:**
{What is actually visible}

**Auto-Resize Attempted:** Yes/No/N/A (mobile)
**Result After Resize:** Fixed/Still broken/N/A

**Recommendation:**
- [ ] Responsive CSS fix needed
- [ ] Z-index adjustment required
- [ ] Container overflow setting incorrect
- [ ] Element positioning bug
```

## Integration with QA Test Procedure

Add validation step after each screenshot capture:

```markdown
| Step | Action | Expected Result | Pass/Fail | Notes |
|------|--------|-----------------|-----------|-------|
| 1 | Navigate to page | Page loads | ☐ | |
| 1a | **Validate screenshot** | No clipping/overlap | ☐ | Auto-validated |
| 2 | Click Login button | Modal appears | ☐ | |
| 2a | **Validate screenshot** | Modal fully visible | ☐ | Auto-validated |
```

## Example Validation Output

### Pass Example

```
✅ Screenshot Validation: 01-login-form.png
   Viewport: 1280x800 (desktop)
   Element: Login form
   Status: PASS
   - Element fully visible
   - No clipping detected
   - Layout correct
```

### Fail Example (Mobile)

```
❌ Screenshot Validation: 01-login-form-mobile.png
   Viewport: 375x667 (mobile)
   Element: Login form
   Status: FAIL - Responsive bug

   Issue: Submit button clipped on right edge
   Expected: Full button visible within viewport
   Actual: Button extends 20px beyond viewport edge

   ⚠️  Mobile viewport - NOT auto-resizing
   Action: Document as responsive design bug
   Recommendation: Check button width CSS, may need max-width: 100%
```

### Retry Example (Desktop)

```
⚠️  Screenshot Validation: 01-data-table.png
   Viewport: 1280x800 (desktop)
   Element: Data table
   Status: RETRY

   Issue: Table columns clipped on right
   Action: Resizing viewport to 1440x900...

   ✅ Retry successful at 1440x900
   New screenshot: 01-data-table-retry.png
   Note: Table requires minimum 1400px width
```
