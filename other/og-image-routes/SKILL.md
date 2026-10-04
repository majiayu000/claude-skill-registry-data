---
name: og-image-routes
description: Dorkroom's Open Graph image pipeline — regenerate OG images and metadata after adding or changing a route, page, or API endpoint. Covers ROUTE_TITLES/ROUTE_DESCRIPTIONS, the Lucide icon map in api/og.tsx, dynamic metadata in api/meta.ts, and the local preview script. Use when adding a route, renaming a page, or changing an API endpoint's metadata.
---

# Dorkroom OG images

Dorkroom generates OG images **at runtime** from `api/og.tsx`. There are no
committed PNGs and no dedicated page to screenshot.

## When to run this

Adding a new route/page, modifying an existing route, or changing an API
endpoint that has metadata.

## Procedure

1. **Update `utils/routeMetadata.ts`** — add/update `ROUTE_TITLES` and
   `ROUTE_DESCRIPTIONS` for new routes.
2. **Update `api/og.tsx`** — add a Lucide icon for the new route in
   `getRouteIcon()`. Download the SVG from
   `unpkg.com/lucide-static@latest/icons/<name>.svg` to get exact element data.
3. **Update `api/meta.ts`** if the route needs dynamic metadata (query params
   like `film`, `developer`).
4. **Regenerate previews** — run `bun run scripts/preview-og.tsx` and visually
   verify the output in `og-previews/` (generated; gitignored).

## Notes

- `ROUTE_TITLES` is also consumed elsewhere in the app — keep it in sync with
  the route definitions, not just with the OG output.
- Verify the icon renders: a missing entry in `getRouteIcon()` falls through to
  the default icon rather than failing loudly.
