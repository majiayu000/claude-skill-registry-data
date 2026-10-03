---
name: add-gallery-images
description: Add before/after images to the Model Gallery for any quality tier. Handles resize, WebP conversion, directory setup, and config update.
---

# Add Gallery Images

Add before/after preview images to the Model Gallery for a quality tier.

## When to Use

When the user provides before/after images (any format: PNG, JPG, WebP) to add to the model selection gallery.

## Quick Reference

### Helper Script

```bash
.claude/skills/add-gallery-images/scripts/add-gallery-images.sh <tier-slug> <before-image> <after-image> [--object-position "center 25%"]
```

### Manual Steps (if script unavailable)

1. **Convert & resize** source images to 512px wide WebP:

   ```bash
   convert <source.png> -resize 512x -quality 80 public/before-after/<tier>/before.webp
   convert <source.png> -resize 512x -quality 80 public/before-after/<tier>/after.webp
   ```

2. **Update config** in `shared/types/coreflow.types.ts` — set `previewImages` for the tier:
   ```typescript
   previewImages: {
     before: '/before-after/<tier>/before.webp',
     after: '/before-after/<tier>/after.webp',
     // objectPosition: 'center 25%',  // optional CSS crop focus
   },
   ```

## Full Procedure

### 1. Identify the tier slug

Valid tier slugs are defined in `QualityTier` type in `shared/types/coreflow.types.ts`:

- `auto`, `quick`, `face-restore`, `fast-edit`, `budget-edit`, `budget-old-photo`
- `seedream-edit`, `anime-upscale`, `hd-upscale`, `face-pro`, `ultra`, `bg-removal`

### 2. Run the helper script

```bash
bash .claude/skills/add-gallery-images/scripts/add-gallery-images.sh \
  budget-old-photo \
  ./budget-old-photo-before.png \
  ./budget-old-photo-after.png
```

The script:

- Validates inputs and dependencies (ImageMagick `convert`)
- Creates `public/before-after/{tier}/` directory
- Resizes to **512px wide** (maintains aspect ratio)
- Converts to **WebP at quality 80**
- Prints dimensions and file sizes for verification

### 3. Update QUALITY_TIER_CONFIG

In `shared/types/coreflow.types.ts`, find the tier entry and set `previewImages`:

```typescript
'budget-old-photo': {
  // ... existing fields ...
  previewImages: {
    before: '/before-after/budget-old-photo/before.webp',
    after: '/before-after/budget-old-photo/after.webp',
  },
},
```

If the subject is positioned off-center (e.g., face at top of frame), add `objectPosition`:

```typescript
previewImages: {
  before: '/before-after/face-pro/before.webp',
  after: '/before-after/face-pro/after.webp',
  objectPosition: 'center 25%', // focuses on upper portion
},
```

### 4. Verify

- Check the images visually: `open public/before-after/{tier}/before.webp`
- Run `yarn dev` and open the model gallery to confirm the card shows the before/after slider
- Tiers with `previewImages: null` show a placeholder gradient; once set, the images load automatically

## Image Conventions

| Property     | Value                              |
| ------------ | ---------------------------------- |
| Format       | WebP                               |
| Max width    | 512px                              |
| Quality      | 80                                 |
| Aspect ratio | Preserved from source              |
| Naming       | `before.webp`, `after.webp`        |
| Location     | `public/before-after/{tier-slug}/` |

## Tiers Missing Images

Check which tiers still have `previewImages: null` in `QUALITY_TIER_CONFIG` — those need images added.

## Related Files

| File                                                         | Purpose                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| `shared/types/coreflow.types.ts`                             | `QUALITY_TIER_CONFIG` — tier metadata + `previewImages` |
| `client/components/features/workspace/ModelCard.tsx`         | Renders before/after thumbnails with slider             |
| `client/components/features/workspace/ModelGalleryModal.tsx` | Gallery modal layout                                    |
| `public/before-after/`                                       | Image storage                                           |
| `.claude/skills/replicate-before-after/`                     | Alternative: scrape images from Replicate model pages   |
