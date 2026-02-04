---
name: design-guide-mlp
description: MLP Finanzberatung SE Corporate Design System combined with modern UI principles. Use when creating any UI, presentations, documents, or materials for MLP financial advisors. Ensures brand-compliant colors, typography, accessibility standards, consistent spacing (8px grid), and subbrand guidelines for medical professionals (MLP Med) and education (SOFE).
---

# MLP Finanzberatung SE - Corporate Design System

Official design guidelines combining MLP brand standards with modern UI principles. Version 3.0 (verified by MLP UX Hub, August 2025).

## Core Brand Principles

### Brand Impact
- **Sicherheit** (Safety/Security)
- **Markenkontakt** (Brand Contact)
- **Einheitliches Auftreten** (Consistent Appearance)

### Design Philosophy
- Clean and minimal layouts with abundant white space
- Professional, trust-inspiring aesthetics
- Accessible and barrier-free (WCAG compliant)
- Consistent spacing and visual hierarchy
- Mobile-first, responsive approach

## 1. MLP Color System (VERBINDLICH)

### Primary Brand Colors (Markenfarben)

**MLP Blau Dark (Main Corporate Blue):**
- HEX: `#033D5D`
- RGB: 3, 61, 93
- Usage: Logo, backgrounds, main elements, **ALL primary headings**, primary buttons

**Titanium (Premium Gray):**
- HEX: `#BEB6AA`
- Usage: Logo, decorative elements, **ALL divider lines**, table borders, structural elements, secondary buttons

**Türkis (Accent):**
- HEX: `#47A190`
- Usage: Backgrounds, highlights, tertiary accents

### Gray Tones (Text & Structure)

**Text Dark (Primary Text):**
- HEX: `#2B2B2B`
- Usage: All body text, headings (when not using MLP Blau Dark)
- **NEVER use pure black (#000000)**

**Text Medium (Secondary Text):**
- HEX: `#717171`
- Usage: Captions, metadata, secondary information

**Background White:**
- HEX: `#FFFFFF`
- Usage: Main background

**Background Gray Lightest:**
- HEX: `#F8F8F8`
- Usage: Subtle backgrounds for separated sections, alternating table rows

### Functional UI Colors (Hinweisfarben)

**⚠️ ONLY use these colors for their semantic purpose:**

**Information (Blue):**
- HEX: `#047584`
- Usage: Info messages, informational highlights only

**Success (Green):**
- HEX: `#13853E`
- Usage: Success states, positive confirmations only

**Warning (Orange):**
- HEX: `#E3691E`
- Usage: Warnings, caution messages only
- Format: Bold text with "ACHTUNG" prefix + icon

**Error (Red):**
- HEX: `#C1293D`
- Usage: Error states, critical alerts only

### Subbrand Colors (For Specialized Audiences)

**MLP Med (Medical Professionals - Ärzte & Heilberufler):**
- When to use: Content targeting doctors, medical practice owners
- Primary: `#9ED0B7` (Soft Mint Green)
- Dark: `#82AB96` | Light: `#CAE5D7`
- Usage: Key fact backgrounds, info boxes for medical audience

**SOFE (School of Financial Education):**
- When to use: Internal training, academic content, educational materials
- Primary: `#009880` (Rich Petrol)
- Dark: `#03798B` | Light: `#6AD9EB`
- Usage: Educational highlights, training materials

## 2. Spacing System (8px Grid) - MANDATORY

**Always use multiples of 8 for ALL spacing:**

- **8px** - Tight spacing (icon-to-label, tight groups)
- **16px** - Default spacing between related elements, form field spacing
- **24px** - Spacing between component groups, card padding (minimum)
- **32px** - Section padding, comfortable card padding
- **48px** - Large section gaps, major spacing
- **64px** - Major layout divisions, page sections

**Rules:**
- NEVER use arbitrary spacing values (no 15px, 20px, 37px, etc.)
- Always round to nearest 8px multiple
- Consistent spacing creates visual rhythm
- Exception: 4px allowed for very tight micro-spacing (but prefer 8px)

## 3. Typography

### Font Families
- **Digital/Screen:** Arial (fallback) or Rotis Sans Serif (if licensed)
- **Maximum 2 font families** per interface
- System font stack: Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto

### Typography Hierarchy

**Headings:**
- **H1:** 32-40px (page titles) - MLP Blau Dark (#033D5D)
- **H2:** 24-28px (section headers) - MLP Blau Dark (#033D5D)
- **H3:** 20-24px (subsections) - Text Dark (#2B2B2B)
- **Body:** 16px minimum (NEVER smaller for readability)
- **Small text:** 14px (metadata, captions, fine print)

**Text Rules:**
- Line height: 1.5-1.6 for body text
- Maintain clear visual hierarchy through size AND color
- MLP Blau Dark for main headings (mandatory)
- Text Dark for body content
- Text Medium for secondary information

### Accessibility Requirements (Barrierefreiheit)

**WCAG Compliance - MANDATORY:**
- Text under 18px: minimum **4.5:1** contrast ratio to background
- Larger elements (18px+): minimum **3:1** contrast ratio
- **CRITICAL:** Never communicate information through color alone
  - ✓ Error: Red color + "Fehler:" text + X icon
  - ✗ Error: Just red color
- All interactive elements need visible focus states for keyboard navigation

## 4. Shadows and Depth

**Subtle Shadows (Preferred):**
```css
box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
```

**Rules:**
- Use subtle shadows, avoid dramatic effects
- Prefer borders (Titanium #BEB6AA) over shadows when appropriate
- Reserve stronger shadows for modals and elevated elements
- **NEVER** combine heavy shadow AND border on same element

## 5. Border Radius

**Standard Radii:**
- **4px** - Subtle (inputs, small buttons)
- **8px** - Moderate (cards, larger buttons)
- **12px** - Pronounced (featured elements)

**Rules:**
- Not everything needs to be rounded
- Use consistently within each component type
- Sharp corners (0px) acceptable for cards and containers
- Fully rounded only for avatars, pills, badges

## 6. Interactive States - MANDATORY

Every interactive element MUST have clear states:

**Buttons:**
- Default: Base styling with subtle shadow
- Hover: Background darkens 10-15%, slight shadow increase
- Active: Background darkens 20%, shadow reduces
- Disabled: Opacity 0.5-0.6, cursor: not-allowed, no hover effect
- Focus: Visible outline (2px solid, offset 2px)

**Links:**
- Default: Underline or clear color differentiation
- Hover: Color shift or underline appears
- Visited: Optional subtle color change
- Focus: Visible outline

**Form Inputs:**
- Default: Border with subtle color
- Hover: Border color intensifies
- Focus: Border color change + outline
- Error: Red border + error message below
- Disabled: Gray background, cursor: not-allowed

## 7. Component Guidelines

### Buttons

```
✓ MLP CORRECT:
- Primary: MLP Blau Dark (#033D5D) background, white text
- Secondary: Titanium (#BEB6AA) background, Text Dark
- Tertiary: White background, MLP Blau Dark border + text
- Padding: 12px 24px (using 8px grid)
- Height: Minimum 40px (mobile-friendly)
- Clear hover state (darken background 15%)
- Subtle shadow on default state
- Border radius: 4px or 8px (consistent)

✗ WRONG:
- Gradient backgrounds
- No hover states
- Arbitrary padding (e.g., 13px 19px)
- Tiny click targets (<40px height)
- Using functional colors (green/red) for non-semantic purposes
```

### Cards

```
✓ MLP CORRECT:
- Border: 1px solid Titanium (#BEB6AA) OR subtle shadow
- NEVER both border AND heavy shadow
- Padding: 24px or 32px (8px grid)
- Background: White (#FFFFFF) or Gray Lightest (#F8F8F8)
- Border radius: 8px or 12px (consistent)
- Clear content hierarchy within

✗ WRONG:
- Heavy shadow + border combo
- Cramped content (< 16px padding)
- Inconsistent card styling across interface
- Random padding values
```

### Forms

```
✓ MLP CORRECT:
- Labels: Above inputs, Text Dark (#2B2B2B), 14px or 16px
- Input height: 40-48px minimum (touch-friendly)
- Spacing between fields: 16px
- Error states: Red (#C1293D) border + "Fehler:" text + icon
- Success states: Green (#13853E) border + text + checkmark icon
- Focus: Visible outline (2px, 2px offset)
- Background: White (#FFFFFF)

✗ WRONG:
- Labels beside inputs (hard to scan)
- Tiny inputs (<36px height)
- No error messaging
- Missing focus states
- Color-only error indication
```

### Tables (Financial Data)

```
✓ MLP CORRECT:
- Header row: MLP Blau Dark (#033D5D) background, white text
- Borders/dividers: Titanium (#BEB6AA), 1px solid
- Alternating rows: White (#FFFFFF) / Gray Lightest (#F8F8F8)
- Padding: 12px 16px per cell (8px grid)
- Important figures: Bold text, NOT colored
- Alignment: Numbers right-aligned, text left-aligned

✗ WRONG:
- Rainbow colored rows
- Using functional colors decoratively
- Inconsistent cell padding
- Heavy borders or shadows
- Poor number alignment
```

### Layout Containers

```
✓ MLP CORRECT:
- Max width: 1200px-1400px (readability)
- Responsive padding: 24px mobile, 48px tablet, 64px desktop
- Use CSS Grid or Flexbox for alignment
- Mobile-first approach
- Background: White (#FFFFFF) or Gray Lightest (#F8F8F8)
- Whitespace: Abundant, let content breathe

✗ WRONG:
- Full-width text on ultra-wide screens
- Inconsistent container padding
- Desktop-only considerations
- Cluttered layouts
```

## 8. Implementation Guidelines

### For Presentations (PowerPoint/Keynote)

```
STRUCTURE:
- Title slide: MLP Blau Dark (#033D5D) background, white text
- Content slides: White (#FFFFFF) or Gray Lightest (#F8F8F8) background
- All headings: MLP Blau Dark (#033D5D)
- Body text: Text Dark (#2B2B2B)
- Divider lines: Titanium (#BEB6AA), 1-2px
- Spacing: Use 8px grid (16px, 24px, 32px margins)

MEDICAL AUDIENCE (MLP Med):
- Key takeaways: Box with MLP Med (#9ED0B7) background
- Accent elements: MLP Med for highlighting
- Maintain all other MLP standards

TRAINING MATERIALS (SOFE):
- Learning objectives: Box with SOFE (#009880) background
- Educational highlights: SOFE accent
- Maintain all other MLP standards
```

### For Web/App UI (React/HTML)

```javascript
// Tailwind/CSS Example with MLP colors
const mlpTheme = {
  colors: {
    primary: '#033D5D',      // MLP Blau Dark
    secondary: '#BEB6AA',    // Titanium
    accent: '#47A190',       // Türkis
    textDark: '#2B2B2B',     // Text Dark
    textMedium: '#717171',   // Text Medium
    bgWhite: '#FFFFFF',
    bgGray: '#F8F8F8',
    info: '#047584',
    success: '#13853E',
    warning: '#E3691E',
    error: '#C1293D',
    mlpMed: '#9ED0B7',
    sofe: '#009880'
  },
  spacing: {
    xs: '8px',
    sm: '16px',
    md: '24px',
    lg: '32px',
    xl: '48px',
    xxl: '64px'
  }
}
```

### Mobile-First Approach

**Breakpoints:**
- Mobile: < 640px (base styles)
- Tablet: 640px - 768px (sm)
- Laptop: 768px - 1024px (md)
- Desktop: 1024px - 1280px (lg)
- Wide: > 1280px (xl)

**Mobile Rules:**
- Touch targets: Minimum 44x44px
- Padding: Minimum 24px on mobile
- Font sizes: 16px minimum (prevents zoom on iOS)
- Spacing: Use 8px grid but may tighten on very small screens

## 9. Quality Checklist (Before Delivery)

### MLP Brand Compliance
- [ ] MLP Blau Dark used for all primary headings
- [ ] Titanium used for all divider lines and borders
- [ ] Only approved MLP colors used
- [ ] Subbrand colors only for correct audience (Med or SOFE)
- [ ] No pure black (#000000) used for text

### Accessibility (WCAG)
- [ ] All text meets 4.5:1 contrast ratio (or 3:1 for large)
- [ ] Information not conveyed by color alone
- [ ] Error states include text + icon (not just red)
- [ ] Success states include text + icon (not just green)
- [ ] Warning messages have "ACHTUNG" prefix
- [ ] All interactive elements have focus states

### General Design Standards
- [ ] Spacing follows 8px grid system (8, 16, 24, 32, 48, 64)
- [ ] Typography hierarchy is clear
- [ ] All interactive elements have hover/active/disabled states
- [ ] Minimum 16px body text size
- [ ] Adequate white space throughout
- [ ] Shadows are subtle (if used)
- [ ] Border radius consistent within component types
- [ ] Mobile responsive (tested at 320px, 375px, 768px, 1024px)
- [ ] No arbitrary spacing values

### MLP-Specific
- [ ] Authentic imagery (no artificial stock photos)
- [ ] Professional, trust-inspiring aesthetic
- [ ] Financial tables use Titanium borders
- [ ] Color usage reflects brand hierarchy

## 10. Special Notes for Trainers/Dozenten

As a trainer creating materials for different audiences:

**General Financial Planning:**
- Use standard MLP palette
- MLP Blau Dark + Titanium + Türkis

**Medical Practice Seminars:**
- Add MLP Med (#9ED0B7) as accent
- Use for key takeaways and medical-specific highlights
- Never mix with SOFE colors

**Internal Advisor Training:**
- Add SOFE (#009880) as accent
- Use for learning objectives and educational content
- Never mix with MLP Med colors

**Golden Rules:**
- Always maintain core MLP colors (Blau Dark, Titanium)
- Never mix subbrand colors in same presentation
- Subbrand = accent only, not replacement for core brand
- When in doubt, stick to core MLP palette

## Quick Reference Color Matrix

| Purpose | Color Name | HEX | Usage |
|---------|-----------|-----|-------|
| **Primary** | MLP Blau Dark | `#033D5D` | Logo, headings, primary buttons |
| **Structure** | Titanium | `#BEB6AA` | Dividers, borders, secondary buttons |
| **Accent** | Türkis | `#47A190` | Backgrounds, highlights |
| **Text Primary** | Text Dark | `#2B2B2B` | Body text, dark headings |
| **Text Secondary** | Text Medium | `#717171` | Captions, metadata |
| **Background** | White | `#FFFFFF` | Main background |
| **Background Alt** | Gray Lightest | `#F8F8F8` | Sections, alternating rows |
| **Info** | Information Blue | `#047584` | Info messages ONLY |
| **Success** | Success Green | `#13853E` | Success states ONLY |
| **Warning** | Warning Orange | `#E3691E` | Warnings ONLY |
| **Error** | Error Red | `#C1293D` | Errors ONLY |
| **Medical** | MLP Med | `#9ED0B7` | Medical content accent |
| **Education** | SOFE Petrol | `#009880` | Training materials accent |

## Implementation Priority

When conflicts arise, follow this hierarchy:

1. **MLP Brand Colors** (highest priority) - Use approved colors
2. **Accessibility** (WCAG compliance) - Never compromise
3. **Spacing System** (8px grid) - Maintain consistency
4. **Typography** (hierarchy + readability) - Clear structure
5. **Interactive States** (usability) - Functional clarity
6. **Aesthetics** (shadows, radius) - Professional polish
