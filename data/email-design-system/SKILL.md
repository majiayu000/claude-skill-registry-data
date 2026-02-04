---
name: email-design-system
description: Apply sophisticated design system principles to HTML emails including typography hierarchy, color palettes, spacing systems, and layout patterns. Use when creating email templates that need cohesive, intentional design within email HTML constraints. Covers section composition, visual rhythm, and brand application.
---

# Email Design System

Transform emails from functional to beautiful while respecting technical constraints. This skill provides the design thinking layer.

## Typography System

### Hierarchy (Required)

Every email needs clear typographic hierarchy:

| Element | Size | Weight | Use |
|---------|------|--------|-----|
| Hero Headline | 32-42px | 700 | One per email, the main message |
| Section Header | 24-28px | 700 | Section introductions |
| Subheader | 18-20px | 600 | Supporting headlines |
| Body | 15-16px | 400 | Main content |
| Small/Caption | 12-13px | 400 | Footer, legal, metadata |

**Key Rule:** Minimum 2x ratio between headline and body. If body is 16px, headline should be 32px+.

### Font Pairing Strategies

Within email-safe constraints, create character:

**Elegant Business:**
```
Headlines: Georgia, 'Times New Roman', serif (32px, normal weight)
Body: Arial, Helvetica, sans-serif (15px)
```

**Modern Friendly:**
```
Headlines: 'Trebuchet MS', 'Lucida Sans', sans-serif (36px, bold)
Body: Verdana, Geneva, sans-serif (14px)
```

**Tech/Minimal:**
```
Headlines: Arial Black, Arial, sans-serif (28px, bold)
Body: Arial, Helvetica, sans-serif (15px)
Accents: 'Courier New', monospace (for codes)
```

### Typography Tricks

**Letterspacing for elegance:**
```css
letter-spacing: 2px; text-transform: uppercase; font-size: 12px;
/* Great for category labels */
```

**Mixed weight headlines:**
```html
<span style="font-weight: 300;">Your order</span>
<span style="font-weight: 700;">is confirmed</span>
```

## Color System

### Palette Structure

Every email needs exactly:
- 1 Background color
- 1 Surface/card color (if different)
- 1 Primary text color
- 1 Muted/secondary text color
- 1 Accent/CTA color
- Optional: 1 section divider color

### Palette Recipes by Aesthetic

**Dark Elegant (Tech/SaaS):**
```
Background: #0f172a
Surface: #1e293b
Primary text: #f8fafc
Muted text: #94a3b8
Accent: #3b82f6
```

**Warm Minimal (Wellness/Lifestyle):**
```
Background: #fef7ed
Surface: #ffffff
Primary text: #1c1917
Muted text: #78716c
Accent: #ea580c
```

**Bold Editorial (Media/Fashion):**
```
Background: #ffffff
Surface: #f5f5f4
Primary text: #0a0a0a
Muted text: #525252
Accent: #dc2626
```

**Professional Clean (Finance/B2B):**
```
Background: #f8fafc
Surface: #ffffff
Primary text: #0f172a
Muted text: #64748b
Accent: #0d9488
```

**Playful Bright (Consumer/Entertainment):**
```
Background: #fef08a
Surface: #ffffff
Primary text: #1e1e1e
Muted text: #525252
Accent: #7c3aed
```

## Spacing System

### Vertical Rhythm

Use consistent spacing scale (in px):

| Token | Value | Use |
|-------|-------|-----|
| xs | 8px | Inline spacing, tight elements |
| sm | 16px | Paragraph spacing |
| md | 24px | Between related elements |
| lg | 40px | Section internal padding |
| xl | 60px | Between major sections |

**Key Rule:** Either generous (lg/xl) OR tight (xs/sm)—never medium-everything.

### Section Padding Pattern

```html
<!-- Major section with generous spacing -->
<td style="padding: 60px 40px;">

<!-- Compact content block -->
<td style="padding: 24px 20px;">

<!-- Mobile-friendly (less horizontal) -->
<td style="padding: 40px 20px;">
```

## Layout Patterns

### Hero Variations

**1. Bold Centered:**
```
[Full-width background color]
     [Centered headline 32-42px]
     [Subtext 16px, muted color]
     [CTA Button]
[End background]
```

**2. Split Asymmetric:**
```
[60% Text] [40% Image]
  Headline   Product/
  Subtext    Visual
  CTA
```

**3. Image-First:**
```
[Full-width hero image]
[Text block below with clear separation]
  Headline
  Subtext
  CTA
```

### Content Section Variations

**1. Feature Grid (2-column):**
```
[Icon/Image] [Icon/Image]
[Title]      [Title]
[Description][Description]
```

**2. Alternating Media:**
```
[Image LEFT] [Text RIGHT]
[Text LEFT]  [Image RIGHT]
```

**3. Feature List (Icon + Text):**
```
[Icon] [Title + Description]
[Icon] [Title + Description]
[Icon] [Title + Description]
```

### Footer Patterns

**Minimal:**
```
[Logo/Name centered]
[Unsubscribe link]
[Address (if required)]
```

**Structured:**
```
[Logo] [Social icons]
[Links row: Help | Privacy | Preferences]
[Unsubscribe | Company address]
```

## Visual Interest Techniques

Within email constraints, create visual interest:

### 1. Background Color Blocking
Alternate section backgrounds:
```html
<td style="background-color: #ffffff; padding: 40px 20px;">
  <!-- White section -->
</td>
...
<td style="background-color: #f8fafc; padding: 40px 20px;">
  <!-- Light gray section -->
</td>
```

### 2. Border Accents
Use borders for definition:
```css
border-left: 4px solid #3b82f6; /* Quote/highlight accent */
border-top: 1px solid #e5e7eb; /* Subtle divider */
```

### 3. Spacer Rows
Create intentional breathing room:
```html
<tr>
  <td height="40" style="font-size: 1px; line-height: 1px;">&nbsp;</td>
</tr>
```

### 4. Image Styling
Make images feel intentional:
```html
<!-- Contained with padding -->
<td style="padding: 20px;">
  <img src="..." style="display: block; max-width: 100%;">
</td>

<!-- Full-bleed -->
<td style="padding: 0;">
  <img src="..." width="600" style="display: block; width: 100%;">
</td>
```

## Section Separation (CRITICAL)

ALWAYS ensure clear visual separation between sections:

1. **Different background colors** - alternate between white and light gray/brand tint
2. **Adequate padding** - minimum 40px padding-top on new sections
3. **Clear content boundaries** - hero content should NOT flow into feature section
4. **Visual breaks** - use spacer rows or border-top between major sections

## Icon + Text Feature Lists

CORRECT pattern (icons aligned with text):
```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
  <tr>
    <td width="64" valign="top" style="padding-right: 16px;">
      <table role="presentation" cellspacing="0" cellpadding="0" border="0">
        <tr>
          <td width="48" height="48" style="background-color: #2563eb; text-align: center; vertical-align: middle;">
            <span style="font-size: 24px;">🏆</span>
          </td>
        </tr>
      </table>
    </td>
    <td valign="top">
      <h4 style="margin: 0 0 8px;">Title</h4>
      <p style="margin: 0;">Description</p>
    </td>
  </tr>
</table>
```

WRONG patterns to AVOID:
- Using `<div style="display: flex;">` for icon containers
- Missing `valign="top"` causing vertical misalignment
- No padding-right on icon cell causing text to touch icon
- Using margin instead of padding for spacing

## Pre-Output Design Checklist

Before generating email:

1. **Choose aesthetic direction** (from palette recipes)
2. **Define typography scale** (hero, section, body sizes)
3. **Plan section flow** (which backgrounds, what padding)
4. **Verify icon patterns** (table-based, valign="top", proper gaps)
5. **Check vertical rhythm** (consistent spacing scale)
6. **Ensure section separation** (no overlapping content)
