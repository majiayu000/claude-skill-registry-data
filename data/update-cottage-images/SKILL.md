---
name: update-cottage-images
description: Updates cottage gallery images for Cabañas Bariloche. Use when adding new photos, replacing existing images, converting HEIC to WebP, generating thumbnails, or reordering cottage gallery images.
---

# Update Cottage Images Skill

This skill guides the process of updating gallery images for any cottage in the Cabañas Bariloche website.

## Prerequisites

- **ImageMagick** must be installed (`magick` command)
- New photos should be placed in a subdirectory within the cottage folder

## Directory Structure

Each cottage has images organized as:
```
src/assets/cottages/cottage-{code}/
├── main-images/
│   ├── 01.Descriptive Name.webp
│   ├── 02.Another Name.webp
│   └── ...
└── thumbnails/
    ├── 01.Descriptive Name_thumbnail.webp
    ├── 02.Another Name_thumbnail.webp
    └── ...
```

## Image Specifications

| Property | Value |
|----------|-------|
| Format | WebP |
| Quality | 75 (for ~250KB-800KB file size) |
| Resolution | Keep original (typically 3024x4032) |
| Thumbnail width | 150px (proportional height) |

## Workflow Steps

### Step 1: Create Feature Branch
```bash
git checkout -b feature/update-{cottage-code}-images
```

### Step 2: Convert Source Images to WebP

For HEIC files:
```bash
cd "src/assets/cottages/cottage-{code}/new-photos/"
for f in *.HEIC; do
  magick "$f" -quality 75 "../converted_${f%.HEIC}.webp"
done
```

For other formats (JPG, PNG):
```bash
for f in *.jpg *.png; do
  magick "$f" -quality 75 "../converted_${f%.*}.webp"
done
```

### Step 3: Review and Name Images

1. View each converted image using the Read tool
2. Assign descriptive names based on content:
   - Living areas: "Sala de Estar", "Cocina", "Comedor"
   - Bedrooms: "Dormitorio Principal", "Dormitorio Secundario"
   - Bathroom: "Baño"
   - Exterior: "Exterior Verano", "Exterior Invierno", "Estacionamiento"
   - Other: "Escalera", "Planta Baja", "Terraza"

### Step 4: Rename with Sequential Numbers

Use format: `##.Descriptive Name.webp`

Examples:
- `01.Sala de Estar.webp`
- `02.Dormitorio Principal.webp`
- `03.Cocina.webp`

### Step 5: Handle Reordering (if needed)

To avoid filename conflicts when reordering:
```bash
# First: rename all to temp names
for f in *.webp; do mv "$f" "temp_$f"; done

# Then: rename to final sequential names
mv temp_old07.webp "01.New Name.webp"
# ... continue for all files
```

### Step 6: Update main-images Folder

```bash
# Remove old images (if replacing)
rm src/assets/cottages/cottage-{code}/main-images/*.webp

# Move new images
mv converted_*.webp src/assets/cottages/cottage-{code}/main-images/
```

### Step 7: Generate Thumbnails

```bash
cd src/assets/cottages/cottage-{code}

# Clear old thumbnails
rm -f thumbnails/*.webp

# Generate new thumbnails (150px width)
for f in main-images/*.webp; do
  name=$(basename "$f" .webp)
  magick "$f" -resize 150x "thumbnails/${name}_thumbnail.webp"
done
```

### Step 8: Verify

1. Run `npm run dev` to start the development server
2. Navigate to `http://localhost:5173/cottage/{code}`
3. Verify all images load correctly in the carousel
4. Check that thumbnails display properly

### Step 9: Commit Changes

Use conventional commit format:
```
feat(cottage-{code}): update gallery with new photos

- Brief description of changes
- Number of images added/replaced
- Any reordering done
```

## Common Issues

### Filename Encoding (ñ, accents)
Use single quotes for filenames with special characters:
```bash
rm '08.Baño.webp'
```

### Large File Sizes
If converted files are too large (>1MB), reduce quality:
```bash
magick input.webp -quality 65 output.webp
```

### Missing Thumbnails
Ensure thumbnail naming includes `_thumbnail` suffix:
```
main-images/01.Name.webp → thumbnails/01.Name_thumbnail.webp
```

## Quick Reference

| Task | Command |
|------|---------|
| Convert HEIC | `magick input.HEIC -quality 75 output.webp` |
| Generate thumbnail | `magick input.webp -resize 150x output_thumbnail.webp` |
| Check file sizes | `ls -lh main-images/` |
| Count images | `ls main-images/*.webp \| wc -l` |

## Cottage Codes Reference

| Cottage | Code |
|---------|------|
| Cabaña Mascardi | `mascardi` |
| Cabaña Otto | `otto` |
| Cabaña Frey | `frey` |
| Cabaña Huapi | `huapi` |
| Cabaña Moreno | `moreno` |
| Espacio Común | `espacio-comun-belgrano` |
| Cabaña Catedral | `catedral` |
