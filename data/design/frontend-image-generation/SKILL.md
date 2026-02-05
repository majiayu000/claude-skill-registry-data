---
name: frontend-image-generation
description: Image sourcing for UI. Free first (DiceBear avatars, Unsplash photos, unDraw illustrations). AI generation only for custom needs.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Image Assets

Strategy: **FREE RESOURCES FIRST**, AI generation for custom needs.

## Decision Tree

```yaml
AVATARS:
  → DiceBear, Boring Avatars (FREE)

PLACEHOLDER PHOTOS:
  → Unsplash, Picsum (FREE)

ILLUSTRATIONS:
  → unDraw, Storyset (FREE SVG)

BACKGROUNDS:
  → Haikei, CSS patterns (FREE)

CUSTOM/BRANDED:
  → AI generation (PAID) — only if needed
```

## Free Avatar APIs

```bash
# DiceBear (many styles)
https://api.dicebear.com/7.x/lorelei/svg?seed=John
https://api.dicebear.com/7.x/avataaars/svg?seed=Jane
https://api.dicebear.com/7.x/initials/svg?seed=JD

# Boring Avatars
https://source.boringavatars.com/beam/120/John

# UI Avatars (initials)
https://ui-avatars.com/api/?name=John+Doe&background=6366f1&color=fff
```

```tsx
// Avatar with fallback
function Avatar({ src, name }) {
  const fallback = `https://api.dicebear.com/7.x/lorelei/svg?seed=${name}`;
  return <img src={src || fallback} alt={name} onError={e => e.target.src = fallback} />;
}
```

## Placeholder Photos

```bash
# Unsplash (by keyword)
https://source.unsplash.com/800x600/?technology
https://source.unsplash.com/1200x600/?office,workspace

# Picsum (random)
https://picsum.photos/800/600
https://picsum.photos/seed/hero/1200/600  # consistent
```

## Free Illustrations

```yaml
unDraw:        https://undraw.co/illustrations
Storyset:      https://storyset.com
Humaaans:      https://humaaans.com
Open Peeps:    https://openpeeps.com

HOW:
  1. Go to site
  2. Set brand color
  3. Search (e.g., "empty", "error")
  4. Download SVG
  5. Place in public/illustrations/
```

## Backgrounds

```yaml
Haikei:           https://haikei.app (blobs, waves, grids)
Hero Patterns:    https://heropatterns.com (subtle patterns)
Cool Backgrounds: https://coolbackgrounds.io (gradients)
```

## AI Generation (When Needed)

Only use when:
- Custom branded illustration required
- No suitable free resource exists
- User explicitly requests

```tsx
// DALL-E 3
const response = await fetch('https://api.openai.com/v1/images/generations', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${OPENAI_API_KEY}` },
  body: JSON.stringify({
    model: 'dall-e-3',
    prompt: 'Minimal 3D illustration of [concept], soft gradient background, no text',
    size: '1792x1024',
    quality: 'hd',
  }),
});
```

## Next.js Image Config

```js
// next.config.js
images: {
  remotePatterns: [
    { hostname: 'source.unsplash.com' },
    { hostname: 'picsum.photos' },
    { hostname: 'api.dicebear.com' },
    { hostname: 'ui-avatars.com' },
  ],
}
```

## Quick Reference

```yaml
ALWAYS FREE FIRST:
  avatars:       DiceBear, Boring Avatars
  photos:        Unsplash, Picsum
  illustrations: unDraw, Storyset
  backgrounds:   Haikei, CSS

AI ONLY WHEN:
  - Custom branded needed
  - No free alternative
  - User requests
```
