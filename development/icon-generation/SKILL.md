---
name: icon-generation
description: Generate app icons (SVG/PNG) and launcher icons for Android Flutter apps. Use when creating UI icons, launcher icons, or platform-ready icon assets. Handles sizing, formats, and flutter_launcher_icons integration.
---

# Icon Generation Skill

Concise, reusable skill for generating app icons (SVG / PNG) and launcher icons for Android Flutter apps. Designed to work with LLMs (Copilot Chat) and image generation models (DALL·E, etc.).

## When to Use This Skill

- Creating consistent, accessible, and platform-ready icons
- Producing SVG markup or PNG assets
- Generating image-generation prompts for app icons
- Setting up launcher icons with flutter_launcher_icons

## Important Constraints (Project-Specific)

- Prefer vector first (SVG) whenever possible
- Keep icons simple and legible at small sizes (24x24, 48x48)
- Provide transparent backgrounds for app icons when requested
- Use the project's color palette or provide color recommendations with hex codes

## Flutter Icon Locations

### App Icons (Launcher)
- Android: `android/app/src/main/res/mipmap-*/` (ic_launcher.png)

### UI Icons
- Place in `assets/icons/` and register in `pubspec.yaml`
- Use Flutter's built-in Icons class when possible
- For custom icons, consider using flutter_svg package

## Icon Sizing

### Android Launcher (mipmap)
- mdpi: 48×48 px
- hdpi: 72×72 px
- xhdpi: 96×96 px
- xxhdpi: 144×144 px
- xxxhdpi: 192×192 px

### Master Icon
- 1024×1024 px for Play Store and source

## Example Prompts

### 1) Generate a small UI icon (SVG)

"Create a simple, single-color `search` icon for app UI (24x24). Provide:
- a clean SVG with viewBox 0 0 24 24 and a compact single-path
- recommended filename `assets/icons/ic_search.svg`
- one-line alt text for accessibility
Constraints: single color (use #1F2937 or suggest a high-contrast color)."

### 2) Generate app launcher icon

"Design an app launcher icon for a Notes app — style: flat, minimal, rounded corners, primary accent color #0057D9. Provide:
- a 1024×1024 source image
- export-ready PNG files for all Android mipmap sizes
- alt text and recommended filenames
Constraints: simple silhouette, good contrast at small sizes."

### 3) Image-generation prompt

"Create a clean, flat-style app icon. Requirements:
- Transparent or solid background (specify preference)
- Simple two-tone palette: primary #0EA5E9, secondary #0F172A
- Minimalist symbol, centered, no text
- Provide outputs: PNG 1024x1024 (source), then resize for Android mipmap sizes
Negative prompts: avoid photorealism, gradients, text, heavy shadows."

## Using flutter_launcher_icons

For automated icon generation, use the flutter_launcher_icons package:

1. Add to `pubspec.yaml`:
```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_launcher_icons:
  android: true
  image_path: "assets/icon/app_icon.png"
```

2. Run: `flutter pub run flutter_launcher_icons`

## Tips

- Always include primary color hex code and alternate suggestions
- For UI icons, keep viewBox within 24x24 or 48x48
- Test icons at small sizes to ensure legibility
- Consider dark/light mode variations
