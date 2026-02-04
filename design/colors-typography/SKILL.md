---
name: colors-typography
description: Define brand styling for website projects. Updates globals.css with CSS color variables (oklch format), typography (h1-h6, p, a, blockquote), and container styles. Use at the start of a project after sitemap is created. Requires primary, secondary, and accent colors plus font choice.
---

# Website Branding

Define brand styling in globals.css for consistent website appearance.

## Workflow

1. **Gather Input** - Colors (hex/oklch), font family, style preference, border radius
2. **Generate Color Palette** - Create full oklch color system
3. **Update :root Variables** - Replace all CSS variables
4. **Update .dark Variables** - Create dark mode variants
5. **Add Typography** - h1-h6, p, a, blockquote styles, including mb-spacing for headings
6. **Verify Container** - Ensure .container class exists

## CSS Variables to Replace

See references/color-system.md for the complete variable list.

Must replace ALL variables in :root and .dark:

- --background, --foreground
- --primary, --primary-foreground
- --secondary, --secondary-foreground
- --accent, --accent-foreground
- --muted, --muted-foreground
- --destructive
- --card, --popover, --sidebar variants
- --border, --input, --ring
- --chart-1 through --chart-5
- --radius

## Border Radius

Set --radius based on input (e.g., 0.625rem for modern/rounded, 0.25rem for minimal/sharp).
Add ".border" and "img" class in globals.css if not present:

```css
.border, img {
    border-radius: var(--radius);
}
```

## Typography Requirements

See references/typography.md for style guidelines.

Add styles for:

- h1, h2, h3, h4, h5, h6
- p (paragraph)
- blockquote

## Link Styling

**IMPORTANT:** Links should NOT have global underline or primary color styling.

**Do NOT add:**

```css
a {
    @apply text-primary underline-offset-4 hover:underline;
}
```

**Instead:** Remove `<a>` styling from globals.css entirely. Components (navbar, footer, content) handle their own link
styles. This prevents nav/footer links from inheriting unwanted colors or underlines.

## List Styling

Lists should only have bullets in prose/content areas (blog posts, articles, etc.).

**Do:**

```css
.prose ul {
    @apply list-disc pl-6;
}

.prose ol {
    @apply list-decimal pl-6;
}
```

**Do NOT:**

```css
ul {
    @apply list-disc;
    /* This affects nav/footer lists! */
}
```

Scoping list styles to `.prose` prevents bullet points from appearing in navigation menus and footer link lists.

**Font Requirements:**

- Must be free for commercial use
- Recommended: Inter, Geist, DM Sans, Plus Jakarta Sans
- Load via next/font or CDN

## Container Class

Ensure this exists in globals.css:

```css
.container {
    @apply mx-auto px-4 sm:px-6 lg:px-8;
    max-width: 80rem; /* 1280px */
}
```

## Output

- Updated globals.css with brand colors
- Updated globals.css with typography
- Font loaded in layout.tsx if needed
