---
name: visual-ui-tester
description: Visual UI testing expert using Playwright MCP for browser automation. Use when testing responsive layouts, verifying UI changes, checking breakpoints, debugging visual/CSS issues, or validating component rendering. Triggers on "test UI", "check layout", "verify design", "responsive", "breakpoint", "visual test", "screenshot".
---

# Visual UI Tester

## Playwright MCP Quick Reference

### Navigation & Snapshots
```
mcp__playwright__browser_navigate     # Go to URL
mcp__playwright__browser_snapshot     # Get accessibility tree (preferred over screenshot)
mcp__playwright__browser_take_screenshot  # Visual capture
mcp__playwright__browser_wait_for     # Wait for text/element
```

### Interactions
```
mcp__playwright__browser_click        # Click element by ref
mcp__playwright__browser_type         # Type into input
mcp__playwright__browser_press_key    # Keyboard input
mcp__playwright__browser_hover        # Hover for tooltips/menus
mcp__playwright__browser_select_option # Dropdown selection
```

### Window Management
```
mcp__playwright__browser_resize       # Set viewport size
mcp__playwright__browser_tabs         # Manage browser tabs
mcp__playwright__browser_close        # Close browser
```

## Responsive Testing Workflow

### 1. Test at Critical Breakpoints

| Breakpoint | Tailwind | Width |
|------------|----------|-------|
| Mobile | `sm` | 640px |
| Tablet | `md` | 768px |
| Laptop | `lg` | 1024px |
| Desktop | `xl` | 1280px |
| Large | `2xl` | 1536px |

### 2. Test Intermediate Widths
Always check: **1000px, 1100px, 1200px, 1300px, 1400px**

These catch edge cases between breakpoints where overflow/layout breaks occur.

### 3. Resize Pattern
```javascript
// Test specific width
mcp__playwright__browser_resize({ width: 1024, height: 768 })
mcp__playwright__browser_snapshot()  // Check layout

// Common test sequence
const widths = [640, 768, 1000, 1024, 1100, 1200, 1280, 1400, 1536];
for (const w of widths) {
  // resize, snapshot, verify
}
```

## Element Priority for Overflow Prevention

When elements compete for space:

1. **Visibility priority** (what stays visible first):
   - Theme toggle > CTAs > Social icons

2. **Visual order** (left to right):
   - Can differ from visibility priority

3. **Mobile menu**:
   - CTAs at bottom
   - Don't duplicate desktop elements
   - Theme switcher handled by framework (Starlight)

## CSS Debugging Patterns

### Flexbox Alignment Issues
**Try first**: Basic flexbox properties before complex hacks

```css
/* Tab/list alignment - try this first */
[role="tablist"] {
  align-items: end;  /* Often fixes tab alignment */
}

/* General alignment */
.container {
  display: flex;
  align-items: center;     /* Vertical centering */
  justify-content: center; /* Horizontal centering */
}
```

### Common CSS Fixes

| Problem | Solution |
|---------|----------|
| Tab misalignment | `align-items: end` on tablist |
| Overflow/scrolling | Check for fixed widths, use `max-width` |
| Dark mode issues | `[data-theme='dark']` selector |
| Inconsistent colors | `theme('colors.slate.600')` |

### What NOT to Do
- Don't use arbitrary Tailwind selectors `[&>*:first-child]:` (unreliable)
- Don't default to JavaScript for CSS-solvable problems
- Don't add horizontal scrolling for vertical alignment issues
- Don't use `!important` in global.css to override frameworks

## Verification Checklist

### Before Claiming UI Fix Complete

1. **Test actual viewport widths mentioned**, not just breakpoints
2. **Check dark mode**: `[data-theme='dark']`
3. **Verify mobile menu** doesn't duplicate desktop elements
4. **Test intermediate breakpoints** (1000-1400px range)
5. **Check overflow** at each breakpoint
6. **Verify interactions** (hover, click, focus states)

### Using Playwright for Verification

```javascript
// 1. Navigate
mcp__playwright__browser_navigate({ url: "http://localhost:3000/page" })

// 2. Resize to target
mcp__playwright__browser_resize({ width: 1024, height: 768 })

// 3. Get snapshot (preferred - shows accessibility tree)
mcp__playwright__browser_snapshot()

// 4. Or screenshot for visual verification
mcp__playwright__browser_take_screenshot({ filename: "test-1024.png" })

// 5. Test interactions
mcp__playwright__browser_click({ element: "Menu button", ref: "button[0]" })
mcp__playwright__browser_wait_for({ text: "Menu content" })
```

## Component Development Order

1. Simple Tailwind classes (Grid/Flexbox)
2. Check if global CSS can solve the problem
3. For alignment: try basic flexbox first
4. Get feedback before adding complexity
5. JavaScript only if CSS fails
6. Component overrides as last resort

## Debugging Tips

### Stuck Processes
```bash
lsof -i :PORT | grep LISTEN
kill PID
```

### Dev Server Issues
- After file changes, wait 5-10 seconds for rebuild
- Fast Refresh may require full reload for env var changes
- Check build output in background processes for errors

### Ask First
- Don't assume dev server port (4200, 3000, etc.)
- Multiple approaches? Ask preference
- Viewport width user mentions may differ from breakpoints
