---
name: ui-design-team
description: |
  Multi-specialist UI design and implementation team for cross-platform applications.
  Use when working on: (1) UI/UX design decisions - colors, layout, typography, accessibility,
  (2) Web implementation - HTML5, CSS, responsive design, (3) .NET desktop - WPF, WinUI 3, MAUI with XAML,
  (4) .NET web - Blazor Server/WASM/Hybrid components, (5) Python GUI - PyQt, Tkinter, Kivy, Streamlit.
  Triggers: UI design, color scheme, layout, component styling, accessibility, responsive design,
  XAML styling, Blazor components, CSS architecture, Python GUI, design system, design tokens.
---

# UI Design Team

A coordinated team of specialists for UI design and cross-platform implementation.

## Team Structure

| Specialist | Domain | Reference |
|------------|--------|-----------|
| UX/Visual Design | Design authority - colors, layout, typography, accessibility, visual hierarchy | [ux-visual-design.md](references/ux-visual-design.md) |
| Web Platform | HTML5, CSS3, responsive design, browser compatibility | [web-html-css.md](references/web-html-css.md) |
| XAML Platform | WPF, WinUI 3, .NET MAUI desktop/mobile | [xaml-platform.md](references/xaml-platform.md) |
| Blazor Platform | Blazor Server, WebAssembly, Hybrid, components | [blazor-platform.md](references/blazor-platform.md) |
| Python Platform | PyQt6, PySide6, Tkinter, Kivy, Streamlit, Dear PyGui | [python-ui.md](references/python-ui.md) |

## Specialist Selection

**Design questions** (colors, layout, UX, accessibility) → Load `ux-visual-design.md`

**Implementation by platform:**
- HTML/CSS/Web → Load `web-html-css.md`
- WPF/WinUI/MAUI → Load `xaml-platform.md`
- Blazor → Load `blazor-platform.md`
- Python GUI → Load `python-ui.md`

**Cross-platform tasks:** Load `ux-visual-design.md` first for design specs, then relevant platform file(s).

## Shared Design Token System

All specialists use consistent token naming for cross-platform consistency.

### Color Tokens
```
Naming: {category}-{shade}
Examples: primary-500, neutral-900, success-500, error-500

Semantic: background, surface, text-primary, text-secondary, border
```

### Spacing Scale (8px base)
```
spacing-xs: 4px   (0.25rem)
spacing-sm: 8px   (0.5rem)
spacing-md: 16px  (1rem)
spacing-lg: 24px  (1.5rem)
spacing-xl: 32px  (2rem)
spacing-2xl: 48px (3rem)
```

### Typography Scale
```
font-size-xs: 12px   (0.75rem)
font-size-sm: 14px   (0.875rem)
font-size-base: 16px (1rem)
font-size-lg: 18px   (1.125rem)
font-size-xl: 20px   (1.25rem)
font-size-2xl: 24px  (1.5rem)
font-size-3xl: 30px  (1.875rem)
```

### Border Radius
```
radius-sm: 4px
radius-md: 8px
radius-lg: 12px
radius-full: 9999px
```

## Component State Naming

Standard states across all platforms:
- `default` / `normal` - Base appearance
- `hover` / `pointer-over` - Mouse hover
- `focus` / `focused` - Keyboard focus (REQUIRED for accessibility)
- `active` / `pressed` - During interaction
- `disabled` - Unavailable
- `error` / `invalid` - Validation failure

## Accessibility Requirements (All Platforms)

Every implementation MUST include:
1. **Contrast**: WCAG 2.1 AA minimum (4.5:1 text, 3:1 large text/UI)
2. **Focus indicators**: Visible keyboard focus on all interactive elements
3. **Screen reader**: Proper labels, roles, and announcements
4. **Keyboard**: Full keyboard navigation support
5. **Motion**: Respect reduced-motion preferences

## Collaboration Protocol

### Design → Implementation Flow
1. UX/Visual Design creates platform-agnostic specification
2. Specification includes: colors (hex), spacing (px/rem), typography, states, responsive breakpoints
3. Implementation specialist translates to platform-specific code
4. Review for design fidelity and accessibility compliance

### Platform Constraint Handling
When platform limits prevent exact design implementation:
1. Document the constraint
2. Propose alternative preserving design intent
3. Get design approval before proceeding

### Cross-Platform Consistency Verification
For multi-platform projects, verify:
- [ ] Design tokens match across platforms
- [ ] Component behavior is consistent
- [ ] Accessibility standards met on all platforms
- [ ] Platform-appropriate adaptations documented

## Design Specification Template

When creating designs, use this structure:

```markdown
## Component: [Name]

### Purpose
[User need and problem being solved]

### Visual Specifications
- Colors: [hex values with semantic names]
- Typography: [family, size, weight, line-height]
- Spacing: [margins, padding using token scale]
- Dimensions: [width, height constraints]
- Border/Shadow: [radius, shadow values]

### States
- Default: [base appearance]
- Hover: [changes on mouse-over]
- Focus: [keyboard focus - REQUIRED]
- Active: [during click/tap]
- Disabled: [unavailable state]

### Responsive Behavior
- Mobile (<768px): [adaptations]
- Tablet (768-1024px): [adaptations]
- Desktop (>1024px): [adaptations]

### Accessibility
- [Contrast requirements]
- [Screen reader behavior]
- [Keyboard interaction]
```

## Quick Reference: Platform Translation

| Design Token | CSS | XAML | Blazor | Python (PyQt) |
|--------------|-----|------|--------|---------------|
| primary-500 | `var(--primary-500)` | `{StaticResource Primary500Brush}` | `var(--primary-500)` | `DesignTokens.PRIMARY_500` |
| spacing-md | `var(--spacing-md)` | `{StaticResource SpacingMd}` | `var(--spacing-md)` | `DesignTokens.SPACING_MD` |
| radius-md | `var(--radius-md)` | `{StaticResource RadiusMd}` | `var(--radius-md)` | `DesignTokens.RADIUS_MD` |
