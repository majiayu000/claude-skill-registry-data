---
name: app-icon-generation
description: Generate iOS and watchOS app icons and image assets from SVG sources using Inkscape and sips
---

# App Icon Generation Skill

Use this skill when generating, resizing, or managing app icons and image assets for iOS/watchOS apps from SVG or PNG sources.

## When to activate this skill

- User asks to add or update app icons
- User provides new logo/icon assets (SVG or PNG)
- User wants to add images to the asset catalog
- User asks about icon sizes or requirements

## Required tools

Check for these tools before proceeding:

```bash
# Prefer Inkscape for SVG → PNG (high quality)
which inkscape

# sips is built into macOS for resizing PNGs
which sips
```

If Inkscape is not installed:
```bash
brew install --cask inkscape
```

## Icon size requirements

### iOS App Icon (AppIcon.appiconset)

| Size (px) | Usage |
|-----------|-------|
| 20 | iPad Notification @1x |
| 29 | iPad Settings @1x |
| 40 | iPhone/iPad Notification @2x, Spotlight @1x |
| 58 | iPhone/iPad Settings @2x |
| 60 | iPhone Notification @3x |
| 76 | iPad Home @1x |
| 80 | iPhone Spotlight @2x, iPad Spotlight @2x |
| 87 | iPhone Settings @3x |
| 120 | iPhone Home @2x, Spotlight @3x |
| 152 | iPad Home @2x |
| 167 | iPad Pro Home @2x |
| 180 | iPhone Home @3x |
| 1024 | App Store |

### watchOS App Icon (AppIcon.appiconset)

| Size (px) | Usage |
|-----------|-------|
| 80 | 38mm @2x |
| 88 | 40mm @2x |
| 92 | 41mm @2x |
| 100 | 44mm @2x |
| 102 | 45mm @2x |
| 108 | 49mm @2x |
| 1024 | App Store |

### Image Assets (*.imageset)

Standard @1x, @2x, @3x scales. Base sizes depend on usage:
- Small icons: 24–32px @1x
- Medium icons: 48–64px @1x
- Logos: 128–256px @1x

## Workflow: Generate app icons from SVG

### Step 1: Create 1024px source from SVG

```bash
inkscape icon/source.svg \
  --export-type=png \
  --export-filename=icon/source-1024.png \
  --export-width=1024 \
  --export-height=1024
```

### Step 2: Generate all iOS sizes

```bash
SOURCE="icon/source-1024.png"
DEST="path/to/Assets.xcassets/AppIcon.appiconset"  # Update for your project

for size in 20 29 40 58 60 76 80 87 120 152 167 180 1024; do
  sips -z $size $size "$SOURCE" --out "$DEST/AppIcon-$size.png"
done
```

### Step 3: Generate all watchOS sizes

```bash
SOURCE="icon/source-1024.png"
DEST="path/to/WatchAssets.xcassets/AppIcon.appiconset"  # Update for your project

for size in 80 88 92 100 102 108 1024; do
  sips -z $size $size "$SOURCE" --out "$DEST/AppIcon-watch-$size.png"
done
```

## Workflow: Create image asset (imageset)

### Step 1: Create directory and generate PNGs

```bash
ASSETS="path/to/Assets.xcassets"  # Update for your project
NAME="MyImage"

mkdir -p "$ASSETS/$NAME.imageset"

# From SVG (adjust base width as needed)
inkscape source.svg --export-type=png --export-filename="$ASSETS/$NAME.imageset/$NAME.png" --export-width=128
inkscape source.svg --export-type=png --export-filename="$ASSETS/$NAME.imageset/$NAME@2x.png" --export-width=256
inkscape source.svg --export-type=png --export-filename="$ASSETS/$NAME.imageset/$NAME@3x.png" --export-width=384
```

### Step 2: Create Contents.json

```json
{
  "images" : [
    {
      "filename" : "MyImage.png",
      "idiom" : "universal",
      "scale" : "1x"
    },
    {
      "filename" : "MyImage@2x.png",
      "idiom" : "universal",
      "scale" : "2x"
    },
    {
      "filename" : "MyImage@3x.png",
      "idiom" : "universal",
      "scale" : "3x"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

## Project asset locations

Locate asset catalogs in your project. Common patterns:

| Type | Typical Path |
|------|------|
| iOS App Icon | `<App>/Assets.xcassets/AppIcon.appiconset/` |
| watchOS App Icon | `<WatchApp>/Assets.xcassets/AppIcon.appiconset/` |
| Image Assets | `<App>/Assets.xcassets/*.imageset/` |
| Source Icons | `icon/`, `logo/`, or `assets/` at project root |

Find your project's asset catalog:
```bash
find . -name "*.xcassets" -type d
```

## Naming convention for source files

Follow this structure when exporting from Figma:

```
icon/
  combo/
    primary.svg
    primary.png
  lettermark/
    primary.svg
    primary.png
logo/
  lockup/
    primary.svg
  stacked/
    light.svg
    dark.svg
```

## Usage in SwiftUI

```swift
// App icon is automatic (set via asset catalog)

// Image assets
Image("Logo")
    .resizable()
    .scaledToFit()
    .frame(height: 60)

// Adapt to color scheme
Image(colorScheme == .dark ? "LogoStacked" : "LogoStackedDark")
```

## Troubleshooting

### Inkscape command not found
```bash
# Use full path if installed via Homebrew Cask
/opt/homebrew/bin/inkscape --version

# Or add to PATH
export PATH="/opt/homebrew/bin:$PATH"
```

### sips produces blurry icons
- Always start from a 1024px source
- sips uses simple interpolation; for better quality, generate each size directly from SVG:
```bash
inkscape source.svg --export-type=png --export-filename=out.png --export-width=180
```

### Asset catalog not picking up new icons
1. Clean build folder: Cmd+Shift+K in Xcode
2. Delete derived data: `rm -rf ~/Library/Developer/Xcode/DerivedData`
3. Verify Contents.json has correct filenames

## Checklist

Before finishing icon generation:

- [ ] 1024px source PNG created from SVG
- [ ] All iOS sizes generated (13 files)
- [ ] All watchOS sizes generated (7 files if applicable)
- [ ] Contents.json matches generated filenames
- [ ] Build project to verify icons appear correctly
