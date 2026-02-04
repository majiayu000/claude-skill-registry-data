---
name: email-html-engine
description: Generate bulletproof HTML email code that renders correctly across Gmail, Outlook, Apple Mail, Yahoo, and mobile clients. Use when creating HTML emails, email templates, or any HTML content for email delivery. Handles table-based layouts, inline CSS, MSO conditionals, and cross-client compatibility.
---

# Email HTML Engine

Email HTML is NOT web HTML. Outlook uses Microsoft Word's rendering engine. Gmail strips styles. This skill ensures every email renders correctly everywhere.

## Architecture: Table-Based Layout

ALL layout must use tables. No exceptions.

```html
<!-- Master container -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="min-width: 100%;">
  <tr>
    <td align="center" style="padding: 0;">

      <!-- Content wrapper (600px max) -->
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; width: 100%;">
        <tr>
          <td style="padding: 40px 20px;">
            <!-- Content here -->
          </td>
        </tr>
      </table>

    </td>
  </tr>
</table>
```

## Required Attributes

Every table MUST have:
```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0">
```

Every image MUST have:
```html
<img src="..." alt="Descriptive text" width="300" height="200" style="display: block; border: 0; max-width: 100%; height: auto;">
```

## Safe CSS Properties

ONLY use these—everything else is unreliable:

| Property | Notes |
|----------|-------|
| `background-color` | Use hex codes |
| `color` | Use hex codes |
| `font-family` | Always include fallback stack |
| `font-size` | Use px, not rem/em |
| `font-weight` | 400, 700 most reliable |
| `font-style` | normal, italic |
| `text-align` | left, center, right |
| `text-decoration` | none, underline |
| `line-height` | Use px or unitless number |
| `letter-spacing` | Mostly works, use sparingly |
| `padding` | All forms, use on `<td>` |
| `border` | All forms |
| `width` | Use both attribute and style |
| `height` | Unreliable, prefer natural height |
| `vertical-align` | top, middle, bottom |
| `display` | Only block, inline, none |

## NEVER Use These CSS Properties

| Property | Why |
|----------|-----|
| `margin` | Outlook ignores or breaks |
| `float` | Broken in most clients |
| `position` | Completely unsupported |
| `flexbox` | Not supported in email |
| `CSS Grid` | Not supported in email |
| `border-radius` | Outlook ignores completely |
| `box-shadow` | Most clients ignore |
| `max-width` | Outlook 2007-2016 ignores |
| `calc()` | Limited support |
| `CSS variables` | Not supported |

## Outlook-Specific Fixes (MSO Conditionals)

Outlook requires explicit widths. Wrap fluid content:

```html
<!--[if mso]>
<table role="presentation" width="600" align="center" cellspacing="0" cellpadding="0" border="0">
<tr>
<td width="300">
<![endif]-->

<div style="display: inline-block; max-width: 300px; width: 100%; vertical-align: top;">
  <!-- Fluid column content -->
</div>

<!--[if mso]>
</td>
<td width="300">
<![endif]-->

<div style="display: inline-block; max-width: 300px; width: 100%; vertical-align: top;">
  <!-- Fluid column content -->
</div>

<!--[if mso]>
</td>
</tr>
</table>
<![endif]-->
```

## Responsive Technique: Fluid Hybrid

Works WITHOUT media queries (Gmail app strips them):

```html
<!-- Two-column that stacks on mobile -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
  <tr>
    <td align="center">
      <!--[if mso]>
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0">
      <tr>
      <td width="290" valign="top">
      <![endif]-->

      <div style="display: inline-block; max-width: 290px; width: 100%; vertical-align: top;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
          <tr>
            <td style="padding: 10px;">
              <!-- Column 1 content -->
            </td>
          </tr>
        </table>
      </div>

      <!--[if mso]>
      </td>
      <td width="290" valign="top">
      <![endif]-->

      <div style="display: inline-block; max-width: 290px; width: 100%; vertical-align: top;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
          <tr>
            <td style="padding: 10px;">
              <!-- Column 2 content -->
            </td>
          </tr>
        </table>
      </div>

      <!--[if mso]>
      </td>
      </tr>
      </table>
      <![endif]-->
    </td>
  </tr>
</table>
```

## Email-Safe Font Stacks

```css
/* Elegant/Serif */
font-family: Georgia, 'Times New Roman', serif;

/* Modern/Clean */
font-family: 'Trebuchet MS', 'Lucida Sans', Arial, sans-serif;

/* Professional */
font-family: Verdana, Geneva, sans-serif;

/* Fallback-safe */
font-family: Arial, Helvetica, sans-serif;

/* Monospace (for codes/receipts) */
font-family: 'Courier New', Courier, monospace;
```

## Button Pattern (Bulletproof)

Works in ALL clients including Outlook:

```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0">
  <tr>
    <td style="background-color: #2563eb; padding: 14px 28px; text-align: center;">
      <a href="{{cta_url}}" style="color: #ffffff; font-family: 'Trebuchet MS', Arial, sans-serif; font-size: 16px; font-weight: bold; text-decoration: none; display: inline-block;">
        Call to Action
      </a>
    </td>
  </tr>
</table>
```

## Size Limits

| Limit | Value | Consequence |
|-------|-------|-------------|
| Total HTML size | < 102 KB | Gmail clips email with "View entire message" link |
| `<style>` block | < 8 KB | Gmail strips entire block if exceeded |
| Content width | 600px | Standard for Outlook 3-column view |
| Image width | 100% max | For responsive scaling |
| Touch target | 44x44px min | Mobile accessibility |
| Body font | 14px min | Mobile readability |

## ICON + FEATURE LAYOUTS (CRITICAL)

**IMPORTANT: Never use emojis as icons** - they hurt email deliverability.

### 🚫 BANNED: Icon-Left, Text-Right Layout

This pattern wastes horizontal space and looks dated:

```
❌ DO NOT USE:
| [icon] | Title here          |
|        | Description text... |
```

### ✅ PREFERRED: Centered Icon Above Text

```html
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="text-align: center; margin-bottom: 32px;">
  <tr>
    <td align="center" style="padding-bottom: 16px;">
      <table role="presentation" cellspacing="0" cellpadding="0" border="0">
        <tr>
          <td width="56" height="56" style="background-color: #6366f1; border-radius: 12px; text-align: center; vertical-align: middle;">
            <img src="https://cdn-icons-png.flaticon.com/128/2989/2989988.png" width="28" height="28" alt="" style="display: block; margin: 0 auto;">
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="center">
      <h3 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 600;">Feature Title</h3>
      <p style="margin: 0; font-size: 15px; color: #666;">Description text here</p>
    </td>
  </tr>
</table>
```

### ✅ PREFERRED: Full-Width Feature Card with Image

```html
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 32px;">
  <tr>
    <td style="padding: 0;">
      <img src="[FEATURE_IMAGE_URL]" width="600" height="250" alt="Feature" style="display: block; width: 100%; height: auto; border-radius: 8px;">
    </td>
  </tr>
  <tr>
    <td style="padding: 24px 0 0 0;">
      <h3 style="margin: 0 0 12px 0; font-size: 24px; font-weight: 700;">Feature Title</h3>
      <p style="margin: 0; font-size: 16px; line-height: 1.6; color: #4a4a4a;">Description here...</p>
    </td>
  </tr>
</table>
```

### VERIFIED WORKING ICON URLS (Flaticon CDN)

Use Flaticon CDN - these URLs are tested and working:

- Checkmark: https://cdn-icons-png.flaticon.com/128/2989/2989988.png
- Star: https://cdn-icons-png.flaticon.com/128/1828/1828884.png
- Lightning: https://cdn-icons-png.flaticon.com/128/3313/3313031.png
- Shield: https://cdn-icons-png.flaticon.com/128/2889/2889676.png
- Chart: https://cdn-icons-png.flaticon.com/128/3135/3135706.png
- Rocket: https://cdn-icons-png.flaticon.com/128/3135/3135715.png
- Target: https://cdn-icons-png.flaticon.com/128/3207/3207586.png
- Clock: https://cdn-icons-png.flaticon.com/128/2784/2784459.png
- Gift: https://cdn-icons-png.flaticon.com/128/3131/3131978.png
- Heart: https://cdn-icons-png.flaticon.com/128/833/833472.png
- Settings: https://cdn-icons-png.flaticon.com/128/3524/3524659.png
- User: https://cdn-icons-png.flaticon.com/128/1077/1077114.png
- Mail: https://cdn-icons-png.flaticon.com/128/561/561127.png

Social Media Icons:
- Twitter/X: https://cdn-icons-png.flaticon.com/128/5968/5968830.png
- LinkedIn: https://cdn-icons-png.flaticon.com/128/3536/3536505.png
- Facebook: https://cdn-icons-png.flaticon.com/128/733/733547.png
- Instagram: https://cdn-icons-png.flaticon.com/128/2111/2111463.png

KEY RULES:
- Use CENTERED icon-above-text OR full-width feature images
- NEVER use icon-left/text-right side-by-side layout
- NEVER use emojis (🏆❤️🏠) - use Flaticon PNG URLs instead
- Use Flaticon CDN URLs (verified working)
- Icons in colored backgrounds: wrap in table with background-color

## Pre-Flight Checklist

Before outputting email HTML:

- All tables have `role="presentation" cellspacing="0" cellpadding="0" border="0"`
- All images have `alt`, `width`, `height`, `style="display:block;"`
- All styles are inline (no external stylesheets)
- No margin, float, position, flexbox, or grid
- MSO conditionals wrap multi-column layouts
- Font stacks include web-safe fallbacks
- Total HTML < 102KB
- `<style>` block < 8KB (if present)
- All links have full URLs (not relative)
- Buttons use table-based bulletproof pattern
- NO icon-left/text-right layouts (use centered icon-above-text instead)
- Icons use Flaticon CDN URLs (NOT Icons8 - they don't load reliably)
- Icons use table cells with background-color, NOT display:flex
- NO emojis anywhere in the email (🏆❤️🏠 etc. hurt deliverability)
- Tasty mode: Each feature has its own full-width image (not just icons)
