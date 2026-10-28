---
name: theme-brand-styling
description: Apply professional themes and brand guidelines to artifacts. Use when styling slides, documents, reports, landing pages, or any content that needs consistent visual identity. Includes 10 preset themes plus custom theme creation.
license: MIT
---

# Theme & Brand Styling

Apply consistent, professional styling to any artifact with curated themes and brand guidelines.

## When to Use This Skill

**Trigger conditions:**
- User asks to style a presentation, document, or artifact
- User mentions: theme, colors, fonts, branding, styling
- User wants to apply brand guidelines to content
- User says: "make it look professional", "apply theme", "brand colors"

## Quick Decision

| If... | Use... |
|-------|--------|
| User wants Anthropic brand colors | Brand Guidelines |
| User wants a professional theme | Theme Factory |
| User wants custom styling | Custom Theme |

## Theme Factory

**Purpose:** Apply curated professional themes to artifacts.

**When:**
- User wants to style slides, docs, reports, HTML pages
- User mentions: "apply a theme", "make it look good", "professional styling"

**Available Themes:**
1. **Ocean Depths** - Professional maritime theme
2. **Sunset Boulevard** - Warm sunset colors
3. **Forest Canopy** - Natural earth tones
4. **Modern Minimalist** - Clean grayscale
5. **Golden Hour** - Rich autumnal palette
6. **Arctic Frost** - Cool winter tones
7. **Desert Rose** - Soft dusty tones
8. **Tech Innovation** - Bold tech aesthetic
9. **Botanical Garden** - Fresh organic colors
10. **Midnight Galaxy** - Dramatic cosmic tones

**Usage:**
1. Show theme showcase (`references/theme-showcase.pdf`)
2. Ask user to choose a theme
3. Apply selected theme's colors and fonts

**Read:** `references/theme-factory.md`

## Brand Guidelines

**Purpose:** Apply Anthropic's official brand identity.

**When:**
- User wants Anthropic brand colors/style
- User mentions: "Anthropic brand", "brand colors", "corporate identity"

**Brand Colors:**
- **Dark:** `#141413` - Primary text/dark backgrounds
- **Light:** `#faf9f5` - Light backgrounds
- **Mid Gray:** `#b0aea5` - Secondary elements
- **Light Gray:** `#e8e6dc` - Subtle backgrounds
- **Orange:** `#d97757` - Primary accent
- **Blue:** `#6a9bcc` - Secondary accent
- **Green:** `#788c5d` - Tertiary accent

**Typography:**
- **Headings:** Poppins (24pt+)
- **Body:** Lora
- **Fallback:** Arial/Georgia

**Read:** `references/brand-guidelines.md`

## Custom Theme

**Purpose:** Create a new theme when existing ones don't fit.

**When:**
- User wants unique styling not in preset themes
- User provides specific color/font preferences

**Process:**
1. Ask user for preferences (colors, mood, audience)
2. Generate theme with name, colors, fonts
3. Show for review
4. Apply to artifact

## Application Process

1. **Identify need** - User wants styling
2. **Choose approach** - Theme / Brand / Custom
3. **Apply styling** - Colors, fonts, layout
4. **Verify** - Ensure readability and consistency

## Key Principles

- **Consistency** - Apply theme uniformly
- **Readability** - Ensure proper contrast
- **Professional** - Clean, polished look
- **Brand-aligned** - Match brand identity when applicable