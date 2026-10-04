---
name: senternet-site-image-webp
description: Convert site images to WebP and wire up responsive image handling.
---

# Image Optimization: WebP Conversion

Convert all site images to WebP format and use `.webp` everywhere — no PNG fallbacks, no `<picture>` elements.

## Steps

### 1. Install `sharp`

```bash
npm install -D sharp
```

### 2. Create `scripts/convert-images.mjs`

```js
import sharp from 'sharp';
import { readdir, stat } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function convertDir(dir, { lossless = false, quality = 82 } = {}) {
  let files;
  try { files = await readdir(dir); } catch { return; }
  const images = files.filter(f => /\.(png|jpg|jpeg)$/i.test(f));
  for (const file of images) {
    const input = path.join(dir, file);
    const output = path.join(dir, file.replace(/\.(png|jpg|jpeg)$/i, '.webp'));
    await sharp(input).webp(lossless ? { lossless: true } : { quality }).toFile(output);
    const inSize = (await stat(input)).size;
    const outSize = (await stat(output)).size;
    console.log(`${file} → ${path.basename(output)}: ${(inSize/1024).toFixed(0)}KB → ${(outSize/1024).toFixed(0)}KB (${Math.round((1-outSize/inSize)*100)}% smaller)`);
  }
}

// Opaque photos and screenshots — lossy is fine
await convertDir(path.resolve(__dirname, '../src/assets'), { quality: 82 });

// Transparent PNGs (icons, logos with alpha) — lossless to preserve alpha
await convertDir(path.resolve(__dirname, '../public/images'), { lossless: true });

// OG preview image
const ogPng = path.resolve(__dirname, '../public/preview.png');
const ogWebp = path.resolve(__dirname, '../public/preview.webp');
try {
  const { promises: fs } = await import('fs');
  await sharp(ogPng).webp({ quality: 82 }).toFile(ogWebp);
  const inSize = (await fs.stat(ogPng)).size;
  const outSize = (await fs.stat(ogWebp)).size;
  console.log(`preview.png → preview.webp: ${(inSize/1024).toFixed(0)}KB → ${(outSize/1024).toFixed(0)}KB`);
} catch { /* no OG image yet */ }
```

Extend the script by calling `convertDir()` for any additional image directories.

### 3. Add the convert script to `package.json`

```json
{
  "scripts": {
    "convert-images": "node scripts/convert-images.mjs"
  }
}
```

### 4. Run the script

```bash
npm run convert-images
```

Original PNG/JPG files can be deleted after conversion — they are not referenced anywhere once Step 5 updates the markup. The `.webp` outputs are committed in the final step below.

### 5. Reference WebP directly in all image elements

Use a plain `<img>` pointing at the `.webp` file. No format-fallback `<picture>` — WebP is supported by all modern browsers.

```tsx
<img src="/path/to/image.webp" alt="Descriptive alt text" className="..." />
```

For responsive images with multiple sizes (single breakpoint, same image):

```tsx
<img
  srcSet="/images/hero-400.webp 400w, /images/hero-800.webp 800w, /images/hero-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  src="/images/hero-800.webp"
  alt="Hero image"
/>
```

`<picture>` **is allowed** for art direction — serving a different image crop or size per breakpoint:

```tsx
<picture>
  <source srcSet="/hero-sm.webp" media="(max-width: 768px)" type="image/webp" />
  <source srcSet="/hero.webp" media="(min-width: 769px)" type="image/webp" />
  <img src="/hero.webp" alt="Hero image" width="800" height="600" />
</picture>
```

Note: the fallback `<img src>` inside `<picture>` must also point at a `.webp` file — never `.png` or `.jpg`.

`<picture>` **is not allowed** for format fallbacks (WebP + PNG `<source>` pairs). That pattern is unnecessary since WebP is universal.

### 6. Rules

- **Lossy (`quality: 82`)**: opaque photos, screenshots, illustrations without transparency
- **Lossless**: anything with an alpha channel (transparent backgrounds, logos, icons)
- **WebP only**: never reference a `.png` or `.jpg` in markup — convert and update all references
- **`<picture>` for art direction only**: use `<picture>` when you need a different image (different crop or size) per breakpoint. Do not use `<picture>` solely to provide a PNG fallback for WebP.
- **OG image** (`public/preview.webp`) is used for social crawlers; update any `<meta property="og:image">` tags to point at the `.webp`

### 7. LCP image special treatment

The hero image (likely the LCP element) needs a `<link rel="preload">` in `index.html`:

```html
<link rel="preload" as="image" href="/screenshot-app.webp" type="image/webp" fetchpriority="high"
  media="(min-width: 769px)" />
<link rel="preload" as="image" href="/screenshot-app-sm.webp" type="image/webp" fetchpriority="high"
  media="(max-width: 768px)" />
```

The preloaded file must use a **stable public URL** (not a Vite-hashed asset) so the `<link>` URL matches the actual `src`. Place hero images in `public/` not `src/assets/`.

### 8. Commit the generated assets

These files are generated build outputs, so commit them as the final step, never leaving the working tree dirty across sessions. Stage the new `.webp` files, any deleted originals, and the script/markup changes, then commit with a descriptive message:

```bash
git status            # review what changed first
git add -A            # stages new .webp files and removes the converted-away originals
git commit -m "Convert site images to WebP"
```

Confirm `git status` is clean before finishing.

## Framework: Next.js track

Most of this skill is redundant here. `next/image` produces WebP/AVIF and a responsive `srcset` on demand, so the conversion script and the hand-written `<picture>` element are solving a problem the framework already solves — and a hand-rolled `<picture>` bypasses the optimizer entirely.

Do this instead:

- Use `next/image` for every content image, with explicit `width`/`height` (or `fill` plus a `sizes` prop). The explicit dimensions are what prevent layout shift; `fill` without `sizes` makes the browser download the largest candidate.
- Set `priority` on the LCP image only. It preloads that one image; setting it on several defeats the purpose.
- `formats: ['image/avif', 'image/webp']` in `next.config.ts` controls what gets served.
- Keep a conversion script only for images the optimizer never touches: OG/share PNGs, favicons, and anything referenced from CSS.
- Remote images need their host listed under `images.remotePatterns` in `next.config.ts` or they will not render.
- Image optimization runs on the server at request time, so it does not work under `output: 'export'` — another reason that setting is off on this track.

See `/senternet-site-framework` for the full convention map.
