---
name: mdl2-icon-picker
description: Select appropriate Segoe MDL2 Assets icons for WinUI Windows applications. Use when the user needs an icon for their WinUI app UI, asks for icon recommendations, needs a glyph for a button or control, or wants to find icons by visual appearance or use case. Provides Unicode points and icon names with visual descriptions and creative alternatives.
---

# MDL2 Icon Picker

Help users select appropriate Segoe MDL2 Assets icons for WinUI Windows applications.

## Overview

The Segoe MDL2 Assets font provides hundreds of glyphs for Windows UI development. Icons are identified by:
- **Unicode point**: Hex code (e.g., E708) used in XAML as `&#xE708;`
- **Description/Name**: The official name (e.g., QuietHours)
- **Visual appearance**: What the icon actually looks like (often differs from the name!)

## Critical: Visual vs Name Mismatch

Icon names often don't describe what the icon looks like:
- **QuietHours** (E708) = Crescent moon shape (great for dark mode!)
- **Brightness** (E706) = Sun with rays (great for light mode!)
- **GlobalNavigationButton** (E700) = Hamburger menu (three lines)

Always consult `references/icon-catalog.md` for accurate visual descriptions.

## Workflow

1. Understand the user's need (what action/concept the icon represents)
2. Consult the icon catalog for visual matches
3. Think creatively about visual metaphors (moon=dark, sun=light, gear=settings)
4. Present 2-4 options in a table with reasoning
5. Suggest the top recommendation with explanation

## Response Format

Present recommendations in this table format:

| Icon | Unicode | Name | Visual | Why It Works |
|------|---------|------|--------|--------------|
| (glyph) | E708 | QuietHours | Crescent moon | Moon universally represents night/darkness |

Include:
- Primary recommendation with reasoning
- 2-3 alternatives with explanations
- Note any creative interpretations (e.g., "Though named QuietHours, the moon shape works perfectly for dark mode")

## Common Mappings

Quick reference for frequent requests:

| User Wants | Best Icon | Unicode | Visual |
|------------|-----------|---------|--------|
| Dark mode | QuietHours | E708 | Crescent moon |
| Light mode | Brightness | E706 | Sun with rays |
| Settings | Setting | E713 | Gear/cog |
| Menu | GlobalNavigationButton | E700 | Three horizontal lines |
| Search | Search | E721 | Magnifying glass |
| Add/New | Add | E710 | Plus sign |
| Delete | Delete | E74D | Trash can |
| Edit | Edit | E70F | Pencil |
| Save | Save | E74E | Floppy disk |
| Close | Cancel | E711 | X mark |
| Home | Home | E80F | House |
| Favorite | FavoriteStar | E734 | Star outline |
| Like | Heart | EB51 | Heart outline |
| Info | Info | E946 | Circle with "i" |
| Warning | Warning | E7BA | Triangle with "!" |
| Error | Error | E783 | Circle with X |
| Success | Completed | E930 | Circle with checkmark |
| Lock | Lock | E72E | Closed padlock |
| Unlock | Unlock | E785 | Open padlock |
| Refresh | Refresh | E72C | Circular arrows |
| Download | Download | E896 | Down arrow to tray |
| Upload | Upload | E898 | Up arrow from tray |
| Share | Share | E72D | Arrow from dot |
| Copy | Copy | E8C8 | Two rectangles |
| Play | Play | E768 | Right triangle |
| Pause | Pause | E769 | Two vertical bars |
| Volume | Volume | E767 | Speaker |
| Mute | Mute | E74F | Speaker with X |

## Creative Thinking

When no exact match exists, think about visual metaphors:

- **Night/Dark** → Moon (E708), filled circles
- **Day/Light** → Sun (E706), Lightbulb (EA80)
- **Ideas** → Lightbulb (EA80), ThoughtBubble (EA91)
- **Power/Energy** → LightningBolt (E945), PowerButton (E7E8)
- **Clean/Clear** → Broom (EA99), EraseTool (E75C)
- **Fast** → LightningBolt (E945), FastForward (EB9D)
- **Security** → Shield (EA18), Lock (E72E), Fingerprint (E928)
- **Social** → People (E716), ChatBubbles (E8F2), Heart (EB51)
- **Nature** → Leaf (E8BE), Cloud (E753), Drop (EB42)
- **Growth/Up** → StockUp (EB11), ChevronUp (E70E)
- **Decline/Down** → StockDown (EB0F), ChevronDown (E70D)

## XAML Usage (for reference)

```xml
<FontIcon FontFamily="Segoe MDL2 Assets" Glyph="&#xE708;"/>
```

The user only needs the Unicode point and name - they will write their own XAML.
