---
name: favicon
description: Generate a complete favicon set (favicon.ico, favicon.svg, apple-touch-icon.png) from a concept or existing SVG. Use when adding a favicon to a website or refreshing an existing one.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: [project-path-or-concept]
---

# Favicon Generator

Generate a complete multi-format favicon set for a website.

**Argument**: `$ARGUMENTS` is either a project path (e.g., `~/projects/my-app`) or a concept (e.g., "blue B on white background"). If not provided, ask.

## Output files

Every favicon generation produces:
- `favicon.svg` — scalable, preferred by modern browsers
- `favicon.ico` — 32x32, fallback for older browsers
- `apple-touch-icon.png` — 180x180, iOS home screen
- `icon-192.png` — 192x192, Android / PWA
- `icon-512.png` — 512x512, PWA large icon (optional)

## Process

### 1. Check for existing brand assets

Look for existing logos, colors, or SVGs in the project:
- `public/` folder for existing favicon files
- `src/app/layout.tsx` for color references
- `tailwind.config.*` for brand colors
- README or CLAUDE.md for design system notes

If the project has a brand (an accent color, a display font), match it. The template below uses teal `#0d9488` as a placeholder.

### 2. Design the SVG

Create `public/favicon.svg` (or project root if no public folder).

**Design principles for favicons:**
- **Fills the frame** — favicon renders at 16x16 and 32x32, so small details vanish
- **Single focal element** — one letter, one simple shape, or one icon (not three)
- **Bold contrast** — the foreground must pop against the background at 16px
- **Rounded corners** — use `rx="[radius]"` on the background rect (8-12 on 64 viewBox)
- **Keep it square** — the design should work in both rounded and square containers

**SVG template:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <!-- Background -->
  <rect width="64" height="64" rx="12" fill="#0d9488"/>

  <!-- Foreground: letter, shape, or simple icon -->
  <text x="32" y="46" font-family="-apple-system, 'Helvetica Neue', sans-serif"
        font-size="42" font-weight="700" fill="white" text-anchor="middle">B</text>
</svg>
```

**For letter-based favicons:**
- viewBox 0 0 64 64
- Font-size ~42 (fills the height)
- y position ~46 (optical center, not geometric)
- Weight 700 or higher (bold reads better small)

**For icon-based favicons:**
- Design at 48x48 within 64x64 canvas (8px padding)
- Use stroke-width 3-4 for visibility at 16px
- Avoid detailed paths — reduce to essential shapes

### 3. Render the PNGs

From the project directory (adjust paths if favicon.svg is in `public/`):

```bash
# Create a large render first (2400px for quality)
qlmanage -t -s 2400 -o . favicon.svg 2>/dev/null

# Generate each size by resizing
sips -z 180 180 favicon.svg.png --out apple-touch-icon.png
sips -z 192 192 favicon.svg.png --out icon-192.png
sips -z 512 512 favicon.svg.png --out icon-512.png
sips -z 32 32 favicon.svg.png --out favicon-32.png

# Clean up the 2400 render
rm favicon.svg.png

# Move PNGs to public/ if applicable
# mv apple-touch-icon.png icon-192.png icon-512.png favicon-32.png public/
```

### 4. Generate favicon.ico

macOS doesn't have `convert` built-in. Use one of these approaches:

**Option A — If ImageMagick is installed:**
```bash
convert favicon-32.png favicon.ico
```

**Option B — If sips only:**
```bash
# Copy the 32x32 PNG and rename — most browsers accept PNG-in-ICO
cp favicon-32.png favicon.ico
```

**Option C — Offer to install ImageMagick if neither works:**
```bash
brew install imagemagick
```

### 5. Update HTML head

Add the favicon links to the site's HTML head (or Next.js metadata).

**For static HTML sites:**
```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

**For Next.js (App Router):** Place files in `src/app/`:
- `favicon.ico` (auto-detected)
- `icon.svg` (auto-detected)
- `apple-icon.png` (auto-detected, 180x180)

Next.js auto-generates the proper `<link>` tags.

### 6. Generate manifest.webmanifest (optional, for PWA support)

If the project supports PWA or wants Android home-screen icons:

```json
{
  "name": "[Project Name]",
  "short_name": "[Short Name]",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#[brand color]",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

### 7. Verify

Read the generated PNGs visually. Check:
- Is the foreground clearly visible at small sizes?
- Does the background fill the frame (no accidental transparency)?
- Are the corners rounded correctly?
- For letters: is the optical centering right (not geometric)?

### 8. Remind about cache

Favicons are aggressively cached by browsers. After deploying:
- Hard refresh: Cmd+Shift+R
- Chrome: Check `chrome://favicon/` to force reload
- Mention this to the user
