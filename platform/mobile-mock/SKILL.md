---
name: mobile-mock
description: |
  Mobile UI mockups with correct proportions and touch interactions.
  Enforces 44px touch targets, proper status bar height, and safe area
  insets. Use for mobile app screens, responsive mobile layouts, or any
  prototype intended for phone viewports.
triggers:
  - "mobile mock"
  - "phone screen"
  - "iOS mock"
  - "android mock"
  - "mobile UI"
df:
  mode: prototype
  platform: mobile
  scenario: design
  design_system:
    requires: true
---

# Mobile Mock Skill

## Viewport and Frame

Output **only the screen contents** as if filling a 375×812 viewport
(or 390×844 for iPhone 14+). The hosting environment provides the device
frame, status bar, and home indicator.

**Forbidden unless explicitly asked:**
- Phone-shaped wrapper divs (bezel, notch, dynamic island)
- iOS status bar icons
- Home indicator bar
- Any explicit phone chrome

Use:
```css
body { max-width: 390px; margin: 0 auto; min-height: 100vh; }
```

## Touch Targets

Every interactive element must be **44×44px** minimum. Apply padding to
extend small visual elements — don't enlarge the visual itself.

```css
.touch-target {
  min-height: 44px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## Safe Area Insets

- **Top**: reserve 44–50px for status bar.
- **Bottom**: reserve 34px for home indicator on notched iPhones.
- Use `padding-top: env(safe-area-inset-top, 44px)` in real implementations.

## Typography Scale

Mobile type scale (base 16px):
- **Display**: 28–34px, weight 700, tight tracking (−0.02em)
- **Headline**: 20–24px, weight 600
- **Body**: 15–16px, weight 400, line-height 1.5
- **Caption**: 12–13px, weight 400, muted color

Never use type smaller than 12px on mobile.

## Interaction Patterns

- No hover-only states. Mobile has no hover. Use `:active` for press feedback.
- Swipe gestures need visual affordances (drag handles, chevrons).
- Bottom sheets/modals dismissible by swipe-down or background tap.

## Spacing System

8px base grid:
- 16px: screen edges
- 12px: card insets
- 8px: between related elements
- 4px: tight pairs

List item height: 48–56px single-line, 64–72px two-line.

## Navigation

- Bottom tab bar: 49–56px tall, 3–5 items max.
- Top nav bar: 44–56px tall.
- Avoid hamburger menus — they hide navigation on mobile.
