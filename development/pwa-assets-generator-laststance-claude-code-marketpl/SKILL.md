---
name: pwa-assets-generator
description: Generate all required PWA assets from a single 1024x1024px image. This skill creates app icons, favicons, Apple touch icons, maskable icons, badge icons, and placeholder screenshots for PWAs. Use when developers need to prepare PWA manifest assets, generate multiple icon sizes from a source image, or create a complete set of PWA-compliant images.
allowed-tools: Bash, Read, Write
---

# PWA Assets Generator

Generate complete set of PWA assets from a single 1024x1024px source image.

## Prerequisites

Ensure Node.js and npm are installed. The script will automatically install required dependencies.

## Quick Start

1. Place your 1024x1024px source image in the project directory
2. Run the generation script:
   ```bash
   node scripts/generate-pwa-assets.js <source-image-path> <output-directory>
   ```

## Generated Assets

The script creates the following PWA-compliant assets:

### App Icons (Standard)
- `icon-144x144.png` - Standard PWA icon
- `icon-192x192.png` - Android Chrome icon
- `icon-512x512.png` - High-resolution PWA icon

### Maskable Icons
- `icon-192x192-safe.png` - Maskable variant with safe area padding (20% padding)

### iOS Support
- `apple-touch-icon.png` - 180×180px for iOS devices

### Favicon
- `favicon.ico` - Multi-resolution icon (16×16, 32×32, 48×48)

### Badge Icon
- `badge.png` - 96×96px monochrome white badge

### Screenshot Placeholders
- `screenshots/desktop-wide.png` - 1280×720px desktop placeholder
- `screenshots/mobile-narrow.png` - 375×812px mobile placeholder

### Shortcut Icons
- `shortcuts/start.png` - 96×96px with play overlay
- `shortcuts/settings.png` - 96×96px with gear overlay

## Script Features

- **Automatic dependency installation**: Installs sharp and png-to-ico if not present
- **Smart resizing**: Uses sharp for high-quality image processing
- **Maskable icon generation**: Adds proper padding for maskable icons
- **Multi-resolution favicon**: Creates proper .ico file with multiple sizes
- **Badge creation**: Converts to monochrome white for notification badges
- **Placeholder screenshots**: Generates branded placeholders with instructions
- **Overlay icons**: Adds symbolic overlays for shortcut icons
- **Progress tracking**: Shows real-time generation progress

## Customization

### Maskable Icons
The script adds 20% padding to maskable icons by default. Adjust the `MASKABLE_PADDING` constant in the script if needed.

### Screenshot Placeholders
The generated screenshots include instructional text. Replace these with actual app screenshots before deployment.

### Badge Color
The badge is converted to white monochrome. Edit the script's badge generation section for different color schemes.

## Usage Example

```bash
# Generate all assets from logo.png into public/ directory
node scripts/generate-pwa-assets.js ./logo.png ./public
```

## Output Structure

```
output-directory/
├── icon-144x144.png
├── icon-192x192.png
├── icon-512x512.png
├── icon-192x192-safe.png
├── apple-touch-icon.png
├── favicon.ico
├── badge.png
├── screenshots/
│   ├── desktop-wide.png
│   └── mobile-narrow.png
└── shortcuts/
    ├── start.png
    └── settings.png
```

## Troubleshooting

- **Image too small**: Source image must be at least 1024×1024px
- **Transparency issues**: PNG with alpha channel recommended for best results
- **Favicon not showing**: Clear browser cache after replacing favicon.ico
