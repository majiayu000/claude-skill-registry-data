---
name: senternet-site-share-images
description: Generate per-page Open Graph share images.
---

# Per-Page OG Share Image Generation

Generate 1200x630 Open Graph / Twitter Card share images for every page using Sharp and SVG composition. No Figma or external tools needed.

Each page's share image is built on top of **that page's own hero image**, with the page title overlaid in the **site's main font**. This makes every share preview look like the page it links to. Pages without a hero fall back to the home page's hero.

## Why generate programmatically

- Consistent branding across all pages
- Each share image previews the actual page (its hero image), not a generic card
- No manual Figma exports when adding new pages
- Images can include dynamic text (page title, stats, etc.)
- Output JPEG (q90 — the format to reference in `og:image`, universal crawler support) plus PNG as a lossless source. Avoid WebP for `og:image` — several social crawlers won't render it.

## Steps

### 1. Detect the site's font

Before writing anything, find what font the site actually uses so the share images match site branding.

Check these locations in order:

1. **`index.html`** — look for a Google Fonts `<link>` tag, e.g. `family=Geist` or `family=Manrope`
2. **`tailwind.config.*`** — look for `fontFamily` in `theme.extend`
3. **`src/index.css` or `src/styles.css`** — look for `@import` of a font or a `@font-face` block
4. **`public/fonts/`** — look for any `.ttf` / `.woff2` files already bundled with the site

Record:
- The font **family name** (e.g. `Geist`, `Manrope`, `Plus Jakarta Sans`)
- Where the font file lives: either a local path (bundled in `public/fonts/`) or a Google Fonts URL

The page **title** in each share image renders in this font. If the site has **no** custom font configured, fall back to `system-ui, sans-serif` and skip the font-file steps (3) below.

### 2. Detect each page's hero image

The share image background should be the page's own hero — the large, prominent image at the top of the page. For each route/page that needs a share image, find its hero:

1. **Open the page component** (e.g. `src/pages/About.tsx`) and look for the first/largest image in the hero section — an `<img src>`, a CSS `background-image`, or a hero image prop. This is usually the same asset the page renders above the fold.
2. **Resolve it to a file in `public/`** (or wherever static assets live). Note the local path so the script can read it — Sharp needs a file, not a runtime URL.
3. **Prefer the highest-resolution / original source** (the `.png`/`.jpg`, not a tiny WebP thumbnail) so the cropped 1200×630 result stays sharp.

Determine the **home page's hero** too — it is the fallback for any page that has no hero or only has small inline images (logos, icons, avatars don't count as heroes).

Record, per page: `{ id, title, heroPath | null }`. Pages with `heroPath: null` will reuse the home hero at render time.

### 3. Ensure Sharp is available

```bash
npm install -D sharp
```

### 4. Prepare the font file for Sharp/SVG rendering

Sharp renders SVG via `librsvg`, which requires fonts as local `.ttf` files — it cannot fetch Google Fonts URLs at render time.

**If the site bundles a font in `public/fonts/`:** use that file directly. No extra step needed.

**If the site loads a Google Font:** download the `.ttf` for use by the script:

```bash
# Replace FONT_NAME with the actual family, e.g. Geist, Manrope, PlusJakartaSans
curl -L "https://fonts.google.com/download?family=FONT_NAME" -o /tmp/font.zip
unzip -j /tmp/font.zip "*.ttf" -d /tmp/site-font/
# Pick the variable or regular-weight .ttf and note its path
```

Alternatively install via Homebrew (macOS) if a cask exists:

```bash
brew install --cask font-FONT_NAME-variable   # e.g. font-geist-variable, font-manrope-variable
# Installs to ~/Library/Fonts/
```

### 5. Create `scripts/generate-share-images.mjs`

Replace `SITE_FONT_FAMILY` with the family name found in Step 1, and `getSiteFontPath()` with the actual path to the `.ttf` file (local project path or OS fonts directory). Fill in each page's `hero` with the path found in Step 2 (or `null` to fall back to the home hero).

The script composites three layers, bottom to top:
1. The page's hero image, cropped to fill 1200×630 (falling back to the home hero when `hero` is null)
2. A dark gradient scrim so overlaid text stays legible over any image
3. An SVG layer with the title (in the site font), subtitle, accent bar, and domain watermark

It writes two formats per page: `.jpg` (quality 90 — reference this in `og:image`) and `.png` (lossless source).

```js
import sharp from 'sharp';
import path from 'path';
import { fileURLToPath } from 'url';
import { mkdir } from 'fs/promises';
import os from 'os';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const shareDir = path.resolve(projectRoot, 'public/share');
await mkdir(shareDir, { recursive: true });

const WIDTH = 1200;
const HEIGHT = 630;

// Font — use the same font the site uses for brand consistency.
// Update SITE_FONT_FAMILY and getSiteFontPath() to match the actual font.
// If the site has no custom font, set SITE_FONT_FAMILY = null and the title
// falls back to system-ui.
const SITE_FONT_FAMILY = 'SITE_FONT_FAMILY'; // e.g. 'Geist', 'Manrope', or null

function getSiteFontPath() {
  const home = os.homedir();
  // Option A: font is bundled in the project (preferred — works on all OSes)
  const bundled = path.resolve(projectRoot, 'public/fonts/FONT_FILE.ttf');
  // Option B: font installed to OS fonts directory
  switch (os.platform()) {
    case 'darwin': return path.join(home, 'Library/Fonts/FONT_FILE.ttf');
    case 'linux':  return path.join(home, '.local/share/fonts/FONT_FILE.ttf');
    case 'win32':  return path.join(process.env.LOCALAPPDATA ?? home, 'Microsoft/Windows/Fonts/FONT_FILE.ttf');
    default:       return bundled;
  }
}

const titleFontStack = SITE_FONT_FAMILY
  ? `${SITE_FONT_FAMILY}, system-ui, sans-serif`
  : 'system-ui, sans-serif';
const FONT_FACE = SITE_FONT_FAMILY
  ? `@font-face{font-family:'${SITE_FONT_FAMILY}';src:url('file://${getSiteFontPath()}')format('truetype');font-weight:100 900;}`
  : '';

// Pages to generate share images for.
// `hero` is a path (relative to the project root) to the page's hero image,
// or null to fall back to the home page's hero.
const PAGES = [
  {
    id: 'home',
    title: 'APPNAME',
    subtitle: 'Your tagline here',
    color: '#00d4ff',
    hero: 'public/hero.png', // the home hero — also the fallback for other pages
  },
  // Add one entry per page that needs a unique share image, e.g.:
  // { id: 'about', title: 'About APPNAME', subtitle: '...', color: '#00d4ff', hero: 'public/about-hero.png' },
  // { id: 'pricing', title: 'Pricing', subtitle: '...', color: '#00d4ff', hero: null }, // uses home hero
];

// The home hero is the fallback background for pages with no hero of their own.
const homeHero = PAGES.find((p) => p.id === 'home')?.hero ?? null;

// Build the cropped hero background as a Sharp pipeline.
// `cover` fills the whole 1200x630 frame, cropping overflow — no letterboxing.
function heroBackground(heroRelPath) {
  const rel = heroRelPath ?? homeHero;
  if (rel) {
    return sharp(path.resolve(projectRoot, rel)).resize(WIDTH, HEIGHT, {
      fit: 'cover',
      position: 'attention', // crop toward the most salient region
    });
  }
  // No hero anywhere — fall back to a solid brand gradient.
  const gradient = `<svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0a0f"/><stop offset="100%" stop-color="#0f1520"/>
    </linearGradient></defs>
    <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#bg)"/></svg>`;
  return sharp(Buffer.from(gradient));
}

// Dark scrim + text, composited on top of the hero so the title stays legible
// over any image. The scrim is heaviest at the bottom-left where the text sits.
function buildOverlaySvg(page) {
  return `<svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>${FONT_FACE}</style>
    <linearGradient id="scrim" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.85"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.15"/>
    </linearGradient>
  </defs>

  <!-- Legibility scrim over the hero -->
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#scrim)"/>

  <!-- Accent bar -->
  <rect x="60" y="380" width="6" height="80" rx="3" fill="${page.color}"/>

  <!-- Title — rendered in the site's main font -->
  <text x="90" y="445"
    font-family="${titleFontStack}"
    font-size="64" font-weight="700"
    fill="white">${page.title}</text>

  <!-- Subtitle -->
  <text x="90" y="500"
    font-family="${titleFontStack}"
    font-size="32" font-weight="400"
    fill="#e5e7eb">${page.subtitle}</text>

  <!-- Domain watermark -->
  <text x="90" y="575"
    font-family="${titleFontStack}"
    font-size="24" font-weight="500"
    fill="${page.color}">www.DOMAIN.com</text>
</svg>`;
}

for (const page of PAGES) {
  const overlay = Buffer.from(buildOverlaySvg(page));
  const pngPath = path.join(shareDir, `${page.id}.png`);
  const jpgPath = path.join(shareDir, `${page.id}.jpg`);

  // Flatten the hero to raw pixels, then composite the scrim+text on top.
  const basePng = await heroBackground(page.hero).png().toBuffer();
  const composited = await sharp(basePng).composite([{ input: overlay }]).png().toBuffer();
  await sharp(composited).png().toFile(pngPath);
  // .jpg is the file to reference in og:image — universal crawler support.
  await sharp(composited).jpeg({ quality: 90, mozjpeg: true }).toFile(jpgPath);
  console.log(`Generated share/${page.id}.jpg + .png${page.hero ? '' : ' (home-hero fallback)'}`);
}
```

The title always renders in the site's configured font (Step 1); set `SITE_FONT_FAMILY = null` only when the site truly has no custom font. To customize further, layer extra SVG elements, embed a logo PNG via a `data:` URI, or add more `composite()` inputs.

### 6. Run the script

```bash
node scripts/generate-share-images.mjs
```

The generated images land in `public/share/` — they are committed in the final step below.

### 7. Add the script to `package.json`

```json
{
  "scripts": {
    "generate:share-images": "node scripts/generate-share-images.mjs"
  }
}
```

### 8. Reference share images in `<MetaTags>`

Pass the `.jpg` path to `<MetaTags image>` in each page component. **Use `.jpg`, not `.webp`** — several social crawlers (including some Facebook/LinkedIn/iMessage paths) won't render WebP `og:image`, so a WebP card silently shows no preview. JPEG has universal support.

```tsx
<MetaTags
  title="About - APPNAME"
  description="Learn more about what we do."
  image="/share/about.jpg"
/>
```

The `MetaTags` component resolves root-relative paths to absolute URLs using `VITE_BASE_URL`.

### 9. Add all share images to the prerender script's third-party strip list

Share images are static files — no action needed. But ensure the `og:image` meta tag in each prerendered page points to the correct share image URL, not the default home preview.

### 10. Commit the generated assets

These files are generated build outputs, so commit them as the final step, never leaving the working tree dirty across sessions. Stage the generated images together with the generator and any wiring changes and commit with a descriptive message:

```bash
git add public/share                                    # the generated .jpg + .png share images
git add scripts/generate-share-images.mjs package.json  # the generator script + npm script
git add src   # any page components whose og:image now points at the new share image
git commit -m "Add per-page Open Graph share images"
```

Confirm `git status` is clean before finishing.

## Design guidelines

- **Hero first**: The page's hero image is the background; the title sits in the lower-left over a dark scrim. The share preview should look like the page it links to.
- **Size**: 1200x630px minimum; 2400x1260 for retina (scale up the canvas and font sizes together)
- **Text**: Keep title ≤ 60 chars so it doesn't get cut in social previews
- **Legibility**: The bottom-weighted scrim keeps white text readable over any hero. If a hero is very bright at the bottom, deepen the scrim's `stop-opacity` values rather than moving the text onto the image.
- **Title font**: Always the site's main font (Step 1) so shares match the live site's typography.
- **Brand element**: Include your domain name or logo so shares are identifiable without context
- **Safe zone**: Keep important content 60px from edges — some platforms crop share images

## Embedding a PNG logo in the SVG

```js
import { readFileSync } from 'fs';
const logoBase64 = readFileSync(path.resolve(__dirname, '../public/logo.png')).toString('base64');
// In the SVG string:
`<image href="data:image/png;base64,${logoBase64}" x="60" y="480" width="120" height="120" />`
```

## Framework: Next.js track

The generation script is unchanged: Sharp renders SVG to PNG, the files land in `public/share/`, and they get committed. Only the reference changes.

- Point at them from each page's `metadata`, not from `index.html`:
  ```tsx
  openGraph: { images: [{ url: '/share/about.png', width: 1200, height: 630, alt: '...' }] }
  ```
  These resolve against `metadataBase` in `app/layout.tsx`. Without `metadataBase`, they ship as relative URLs and no crawler can fetch them.
- Add the share-image block for a new page in the same change that adds the page and its `config/routes.mjs` entry.
- Next also supports generating OG images at request time (`opengraph-image.tsx` with `ImageResponse`). Prefer the pre-generated static PNGs anyway: crawlers fetch OG images aggressively, and a static file costs nothing to serve while a runtime route costs an invocation per fetch. Reach for `ImageResponse` only when the image genuinely depends on data that is not known at build time.

See `/senternet-site-framework` for the full convention map.
