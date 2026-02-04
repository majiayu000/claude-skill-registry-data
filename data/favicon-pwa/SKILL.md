---
name: favicon-pwa
description: Set up favicon and PWA manifest for website projects. Creates favicon.ico, apple-touch-icon, and site.webmanifest. Use at project end before release. Triggers on "favicon", "PWA", "manifest", "app icon".
---

# Favicon & PWA Setup

Create favicon set and PWA manifest for professional web presence.

## Workflow

1. Get brand colors from globals.css
2. Create/request favicon source (512x512 PNG or SVG)
3. Generate favicon variants
4. Create site.webmanifest
5. Add to app/layout.tsx

## Required Files

### Favicon Set

| File | Size | Location |
|------|------|----------|
| favicon.ico | 16x16, 32x32, 48x48 | app/favicon.ico |
| apple-touch-icon.png | 180x180 | public/apple-touch-icon.png |
| icon-192.png | 192x192 | public/icon-192.png |
| icon-512.png | 512x512 | public/icon-512.png |

### site.webmanifest

Create at `public/site.webmanifest`:

```json
{
  "name": "[Business Name]",
  "short_name": "[Short Name]",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "[primary color from globals.css]",
  "background_color": "[background color from globals.css]",
  "display": "standalone",
  "start_url": "/"
}
```

## Layout Integration

Add to `app/layout.tsx` metadata:

```typescript
export const metadata: Metadata = {
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
}
```

## Checklist

- [ ] favicon.ico created (multi-size)
- [ ] apple-touch-icon.png created (180x180)
- [ ] icon-192.png and icon-512.png created
- [ ] site.webmanifest created with correct colors
- [ ] Layout metadata updated
- [ ] Favicon displays in browser tab
