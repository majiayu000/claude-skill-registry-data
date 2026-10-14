---
name: ui-visual-verification
description: Verify UI colors and layout by pixel sampling, not OCR. Preserve chrome when fixing colors.
---

# UI Visual Verification Skill

## Problem it solves

OCR reads text but cannot verify colors, borders, or visual layout. When fixing UI color bugs, developers accidentally remove borders, boxes, and chrome — breaking the visual design. TUI frameworks like tview hard-code color constants (e.g., `ContrastBackgroundColor`, `InverseTextColor`) that override theme settings, producing unexpected blues or wrong accent colors.

## Detection triggers

Activate when:
- Fixing or verifying UI colors in a TUI, terminal UI, or desktop application
- User says "the colors look wrong" or "check the theme"
- Modifying widget styles, borders, or focus states
- Verifying that a color change didn't break surrounding chrome
- Working with frameworks that hard-code color constants (tview, bubbletea, curses)

## Protocol

### 1. Capture baseline before changing anything

Take a screenshot and sample the current colors at key coordinates:
```
get_pixel_color(x, y)   # border of the widget
get_pixel_color(x, y)   # label text area
get_pixel_color(x, y)   # focused element
```
Record what each coordinate represents. This is your before state.

### 2. Make the color change

Remove ONLY the wrong colors. Never touch:
- Border drawing characters or box chrome
- Padding/margin spacing
- Focus ring structure
- Layout positioning

BAD: Rewriting the widget to "fix colors" (removes borders, changes layout)
GOOD: Changing only the color attribute/variable that controls the wrong hue

### 3. Verify by pixel sampling, not OCR

After the change, sample the same coordinates:
```
get_pixel_color(x, y)   # Did the border color change? It shouldn't have.
get_pixel_color(x, y)   # Did the text color change? It should have.
get_pixel_color(x, y)   # Does focus still invert correctly?
```

OCR cannot distinguish red text from blue text — it only reads the characters. Pixel sampling reads the actual rendered color.

### 4. Verify focus/unfocus states

For widgets with focus behavior, check both states:
- Unfocused: label and border in base border color
- Focused: box inverts to accent color

Sample colors in both states. If the focus inversion is broken, the theme override is wrong.

### 5. Check for hard-coded framework colors

TUI frameworks often hard-code colors that override your theme:
- tview: `ContrastBackgroundColor`, `InverseTextColor` (blue by default)
- Fix: override once in theme initialization, not per-widget

```go
// Fix hard-coded tview blue — do this ONCE in theme.go init()
tview.Styles.ContrastBackgroundColor = tcell.ColorMyGreen
tview.Styles.InverseTextColor = tcell.ColorWhite
```

## When NOT to use

- Verifying text content (use OCR for that)
- Non-visual backend logic
- Layout-only changes with no color impact

## Cross-references

- **screenshot** — Capture screenshots for before/after comparison.
- **go-mcp-computer-use** — The `get_pixel_color` and `screenshot` tools live here. Load this skill when using those tools for UI verification.

## Lessons learned

Real bugs caught by this skill:
1. tview hard-codes `ContrastBackgroundColor` to blue — overriding it in `init()` once fixes all widgets
2. "Fix the colors" rewrites that remove borders/boxes break the visual contract — always preserve chrome
3. OCR says text is correct but pixel sampling reveals wrong color — OCR cannot verify color
