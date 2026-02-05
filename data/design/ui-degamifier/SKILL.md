---
name: ui-degamifier
description: Remove gaming aesthetics (glowing effects, neon shadows, cyberpunk styling) from CSS and replace with professional, clean design. Use when code has distracting visual effects or when implementing corporate/professional UI design. Ensures WCAG AA accessibility.
allowed-tools: view_file, replace_file_content, multi_replace_file_content
---

# UI Degamifier

Transform gaming/cyberpunk aesthetics into professional, accessible design.

## When to Use

Use this skill when:

- CSS has glowing text-shadow or box-shadow effects
- UI has neon colors or excessive visual effects
- Need to implement Apple/Stripe-like clean design
- Ensuring WCAG AA accessibility compliance
- Converting cyberpunk theme to corporate styling

## Instructions

### Step 1: Identify Gaming Effects

Scan CSS files for these patterns:

- `text-shadow` with glow effects (e.g., `0 0 20px rgba(0, 243, 255, 0.3)`)
- `box-shadow` with large blur radius (e.g., `0 0 15px cyan`)
- Neon colors (bright cyan, magenta, lime green)
- Heavy animations and transforms
- Excessive gradients

### Step 2: Replace with Professional Styling

#### Text Shadows

**Before** (Gaming):

```css
text-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
```

**After** (Professional):

```css
/* Clean professional design - no glowing effects */
```

#### Box Shadows

**Before** (Gaming):

```css
box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
```

**After** (Professional):

```css
box-shadow: 0 0 0 3px rgba(0, 243, 255, 0.15); /* Subtle border effect */
```

#### Button Hover Effects

**Before** (Gaming):

```css
.button:hover {
  box-shadow: 0 4px 15px rgba(0, 243, 255, 0.4);
}
```

**After** (Professional):

```css
.button:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Step 3: Ensure Light/Dark Mode Compatibility

Keep both themes but make them professional:

**Light Mode**:

- White backgrounds (#fff)
- Black text (#000 or dark gray)
- Subtle shadows (rgba(0,0,0,0.1))
- Professional borders

**Dark Mode**:

- Semi-transparent dark backgrounds
- White text (#fff)
- Minimal glows (only for focus states)
- Readable contrast

### Step 4: Verify Accessibility

Check WCAG AA compliance:

- Text contrast ratio: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements clearly distinguishable
- Focus states visible

## Example Transformation

### Input CSS (Gaming):

```css
.title {
  color: #0ff;
  text-shadow: 0 0 20px rgba(0, 243, 255, 0.3), 0 0 40px rgba(0, 243, 255, 0.2);
  font-family: "Orbitron", monospace;
}

.card {
  background: rgba(10, 11, 30, 0.8);
  border: 2px solid #0ff;
  box-shadow: 0 0 30px rgba(0, 243, 255, 0.5), inset 0 0 20px rgba(0, 243, 255, 0.2);
}
```

### Output CSS (Professional):

```css
.title {
  color: var(--ifm-color-primary);
  /* Clean professional design */
  font-family: "Inter", sans-serif;
}

.card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid var(--ifm-color-emphasis-200);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] .card {
  background: rgba(30, 30, 30, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}
```

## Files Typically Modified

- `*.module.css` - Component-specific styles
- `*.css` - Global styles
- Theme files
- CSS-in-JS styled components

## Professional Color Palettes

Replace neon colors with:

**Neutral Professional**:

- Primary: #2563eb (blue)
- Gray scale: #f9fafb to #111827
- Success: #10b981
- Error: #ef4444

**Corporate**:

- Primary: #1e40af (deep blue)
- Secondary: #64748b (slate)
- Accent: #0891b2 (teal)

**Apple-like**:

- Primary: #007aff
- Gray: #8e8e93
- Background: #f2f2f7 (light), #1c1c1e (dark)

## Quality Checklist

After degamification, verify:

- ✅ No glowing text-shadow effects
- ✅ Box-shadows use subtle, professional values
- ✅ Colors are muted, not neon
- ✅ Light mode has good contrast (dark text on light bg)
- ✅ Dark mode is readable (light text on dark bg)
- ✅ Animations are minimal and purposeful
- ✅ Fonts are professional (Inter, Roboto, SF Pro, not Orbitron)

## Preservation Guidelines

Keep these elements:

- Hover states (but make them subtle)
- Focus indicators (required for accessibility)
- Transition effects (if smooth and professional)
- Border radius (maintains modern feel)

Remove these elements:

- All glowing effects
- Neon colors
- Excessive animations
- Cyberpunk fonts
- Heavy gradients
