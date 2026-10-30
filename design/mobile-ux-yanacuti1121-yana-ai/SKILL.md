---
name: mobile-ux
description: >
  Design for mobile — touch targets, thumb zones, gesture patterns, iOS and
  Material 3 platform conventions, mobile form design, and responsive
  breakpoints. Use when building mobile-first UI, reviewing a layout for
  phone/tablet, asked about "touch targets", "thumb zone", "iOS conventions",
  "Android Material", "mobile form", or "responsive design".
  Do NOT use for desktop-only UIs — use `ux-heuristics` for general usability.
origin: adapted:ux-ui-mastery
license: MIT © phazurlabs
version: 1.0.0
compatibility: "Any mobile web, React Native, or responsive frontend."
---

<!-- Adapted from phazurlabs/ux-ui-mastery (MIT) — Mobile UX Design skill.
     Touch targets, thumb zone research (Hoober), iOS/Material conventions,
     form design, responsive breakpoints. YAMTAM structure is original. -->

## When to Use

- Use when: designing or reviewing any mobile or responsive layout
- Use when: form feels hard to fill on mobile
- Use when: navigation elements are unreachable with one thumb
- Use when: checking iOS or Android platform-specific conventions before ship
- Do NOT use for: desktop dashboard layouts — use `ux-heuristics` instead

---

## Touch Targets

| Platform | Minimum size | Recommended | Min spacing |
|---|---|---|---|
| iOS | 44 × 44 pt | 48 × 48 pt | 8 pt |
| Android | 48 × 48 dp | 56 × 56 dp | 8 dp |
| Web | 44 × 44 px | 48 × 48 px | 8 px |

Rules:
- Text links: expand clickable area beyond visible text via padding
- Edge targets (floating buttons): add extra padding — grip interferes with accuracy
- Never rely on visual size alone — use `min-height`/`min-width` + padding

---

## Thumb Zone (Hoober Research)

Based on one-handed phone use patterns:

```
╔═══════════════╗
║  ┌─────────┐  ║  ← AVOID: top corners (hardest reach)
║  │ Tertiary│  ║
║  │  zone   │  ║
║  ├─────────┤  ║
║  │Secondary│  ║  ← OK: middle and sides
║  │  zone   │  ║
║  ├─────────┤  ║
║  │ PRIMARY │  ║  ← BEST: bottom center
║  │  zone   │  ║
╚══╧═════════╧══╝
```

- **Primary (bottom-center)**: main actions, tab bar, primary CTA
- **Secondary (middle/sides)**: secondary content, less frequent actions
- **Tertiary (top corners)**: settings, rarely-used controls only

Large phones (6.5"+): top-left is particularly difficult — avoid placing nav here.

---

## iOS Human Interface Conventions

**Navigation:**
- Bottom tab bar — max 5 items (overflow → "More" tab)
- Top navigation bar with back button + swipe-back gesture on all pushed views
- Large titles collapse on scroll
- Bottom sheet modals replace full-screen overlays for most use cases

**Grid and spacing:**
- Base grid: 8pt
- Standard margins: 16pt left/right
- Safe areas: always respect notch, Dynamic Island, home indicator

**Typography:**
- System font: SF Pro
- Dynamic Type: mandatory — never disable user font size preferences

**Platform expectations:**
- Swipe-back on every pushed view
- Haptic feedback on selections, confirmations, errors
- Bottom sheet for contextual menus (not action sheets for everything)

---

## Android Material 3 Conventions

**Navigation:**
- Bottom navigation bar: 3–5 destinations
- Navigation drawer: 5+ destinations (swipe from left edge)
- Single FAB per screen, bottom-right

**Grid and spacing:**
- Base grid: 4dp
- Standard margins: 16dp
- Edge-to-edge content — respect system bar insets

**Typography:**
- System font: Roboto or Material Type Scale
- Material You: dynamic color from wallpaper — respect `colorScheme` tokens

**Platform expectations:**
- Predictive back gesture support
- Dynamic color adaptation
- FAB elevates above content, not overlapping critical info

---

## Mobile Form Design

**Layout:**
- Single column only — never multi-column on mobile
- Top-aligned labels outperform left-aligned on small screens
- Floating labels save space while maintaining context

**Keyboard optimization — match input type:**
```html
<input type="email">    <!-- email keyboard -->
<input type="tel">      <!-- phone dial pad -->
<input type="number">   <!-- numeric keyboard -->
<input type="search">   <!-- search keyboard with return key -->
```

**Smart inputs:**
- Fixed-length fields auto-advance (OTP, card number segments)
- Input masking for phone, date, card number
- Password visibility toggle — always
- Autofill attributes: `autocomplete="email"`, `autocomplete="new-password"`, etc.

**Validation:**
- Validate on blur, not on keystroke
- Include success state (green checkmark) — not just error
- Inline errors linked to specific field — not a generic summary at top

**Form reduction:**
- Collect minimum needed for current step
- Social login where available
- Replace free-text with picker/toggle/slider when input has known valid values

---

## Responsive Breakpoints

Mobile-first: write base styles for mobile, enhance upward.

```css
/* Mobile first — no media query needed for base */
/* Small phone    */ @media (min-width: 320px) { }
/* Standard phone */ @media (min-width: 375px) { }
/* Large phone    */ @media (min-width: 428px) { }
/* Tablet         */ @media (min-width: 768px) { }
/* Small desktop  */ @media (min-width: 1024px) { }
/* Desktop        */ @media (min-width: 1440px) { }
```

Fluid typography — prevents iOS auto-zoom (never below 16px base):
```css
html { font-size: 16px; }
body { font-size: clamp(1rem, 2.5vw, 1.125rem); }
```

Container queries for component-level responsiveness:
```css
@container (min-width: 400px) { /* component-level breakpoint */ }
```

---

## Anti-Fake-Pass Rules

Before claiming a mobile UI is done, you MUST confirm:
- [ ] All interactive elements meet minimum touch target (44px / 44pt)
- [ ] Primary actions are in the bottom-center thumb zone
- [ ] Forms: single column, keyboard type per field, validation on blur
- [ ] iOS or Android conventions respected (whichever is the target platform)
- [ ] Base font ≥ 16px (prevents iOS auto-zoom)
- [ ] `prefers-reduced-motion` handled if animations are present

Reference: `gates/anti-fake-pass-gate.md` | `gates/ui-quality-gate.md`
