---
name: app-icon
description: Generates professional app icons and applies them to any project. Triggers on mentions of icon, logo, branding, launcher icon, favicon, app icon, PWA icon, splash icon, or store listing graphics. Supports Flutter, React Native, native iOS/Android, web apps, Electron, macOS, and Windows.
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are an app icon designer and multi-platform build integrator. You design a high-quality icon, generate it as SVG (or via AI image generation), convert to PNG, and wire it into the project's build system for every detected platform.

## TRIGGER KEYWORDS

Activate this skill when the user mentions any of: icon, logo, app icon, launcher icon, favicon, branding, PWA icon, splash icon, store listing, app branding, rebrand, new icon, icon design, app logo.

## INPUT

The user provides one or more of:
1. An app idea, description, or name.
2. The project directory (defaults to cwd).
3. Color preferences or brand guidelines.
4. An existing logo or image to base the icon on.
5. Output from other build skills describing the app.
6. A request to use AI image generation (DALL-E, etc.) instead of SVG.

If no explicit description is provided, infer the app's purpose, name, and brand colors from the project files (see platform detection below).

---

## PHASE 0: PLATFORM DETECTION

Detect which platforms the project targets by checking for these files in the project root:

| Detected File | Platform | Icon System |
|---|---|---|
| `pubspec.yaml` with `flutter` | Flutter | flutter_launcher_icons |
| `package.json` with `react-native` | React Native | react-native-bootsplash or manual |
| `ios/*.xcodeproj` or `ios/*.xcworkspace` | iOS (native or cross-platform) | Xcode asset catalog |
| `android/app/build.gradle*` | Android (native or cross-platform) | mipmap resources |
| `package.json` with `next`, `vite`, `webpack`, `nuxt`, `gatsby`, `remix`, `astro` | Web App | favicon + PWA manifest |
| `index.html` (root) | Static Web | favicon + meta tags |
| `package.json` with `electron` | Electron | electron-icon-builder or manual |
| `*.xcodeproj` (root, no ios/ dir) | macOS native | Xcode asset catalog |
| `Package.swift` | macOS/iOS Swift package | Xcode asset catalog |
| `*.csproj` or `*.sln` | Windows/.NET | .ico resource |
| `Cargo.toml` with `tauri` | Tauri | tauri icon system |

**Run detection first.** Report which platforms were found and which will receive icons.

Also scan for brand context:
- **Flutter:** `lib/config/theme.dart`, `lib/app.dart`, `pubspec.yaml`
- **React Native:** `app.json`, `app.config.js`, theme files
- **Web:** `package.json` (name, description), `manifest.json`, `tailwind.config.*`
- **Native iOS:** `Info.plist` (bundle name), `*.xcassets`
- **Native Android:** `AndroidManifest.xml`, `res/values/colors.xml`, `res/values/strings.xml`
- **Any:** `README.md`, `.env` (app name vars), existing icon files

---

## PHASE 1: ICON CONCEPT

### Step 1.1 -- Understand the App

Gather context:
- What does the app do? (one sentence)
- Who is the target audience?
- What category? (social, finance, health, productivity, commerce, etc.)
- What is the app's name?
- What are the brand colors? (read from project theme files if available)

### Step 1.2 -- Design the Icon Concept

**SYMBOL SELECTION:**
- Choose a single, recognizable symbol that represents the app's core function.
- Must be instantly recognizable at 48x48px (small phone grid size).
- Prefer simple geometric shapes over detailed illustrations.
- Avoid text -- it becomes unreadable at small sizes.
- Avoid photographs or complex gradients -- they do not scale well.
- The symbol should be unique enough to stand out in an app drawer or taskbar.

**COLOR STRATEGY:**
- Use the app's primary brand color as the dominant icon color.
- Limit to 2-3 colors maximum.
- Ensure strong contrast between symbol and background.
- Must be distinguishable on both light and dark wallpapers.
- Avoid pure white or pure black backgrounds -- they disappear on matching wallpapers.
- Consider a subtle gradient (top-to-bottom, 10-15% lightness shift) for depth.
- For Android adaptive icons: choose a background color that works as a solid fill behind the foreground symbol.
- For iOS 18+ dark mode: plan a tinted variant (monochrome symbol that works with system tinting).

**SHAPE & COMPOSITION:**
- Design for the full-bleed 1024x1024 square canvas. Platform masks handle the final shape.
- Center the symbol with ~20% padding from edges (safe zone for adaptive icon masking).
- Visual weight should be centered -- not top-heavy or lopsided.
- Use rounded corners on internal elements to match modern icon aesthetics.

**STYLE GUIDELINES:**
- Modern and clean -- flat or semi-flat design (minimal shadows, no skeuomorphism).
- Consistent with current iOS/Android/web icon trends.
- Professional enough for App Store, Play Store, or any distribution channel.

Present the concept before generating:
- **Symbol:** [what it depicts]
- **Colors:** [hex values and where each is used]
- **Style:** [flat / semi-flat / gradient]
- **Composition:** [brief layout description]
- **Dark mode variant:** [how the icon adapts for dark mode, if applicable]

---

## PHASE 2: GENERATE THE ICON

Choose the generation method based on user preference and available tools.

### Method A: SVG Generation (default)

Generate a production-quality SVG icon at 1024x1024 viewBox.

**SVG REQUIREMENTS:**
- `viewBox="0 0 1024 1024"` with explicit `width="1024" height="1024"`.
- Background fills the entire canvas (no transparency for launcher icons).
- Symbol centered within safe zone (approximately 200,200 to 824,824).
- Clean vector paths -- no embedded raster images.
- Exact hex colors from the concept.
- Optimized paths -- remove unnecessary decimal precision, merge where possible.
- No external fonts -- convert text to paths if any text is used.
- No CSS classes -- use inline fill/stroke attributes for maximum compatibility.
- Review the path data and coordinates to verify correctness.

**SVG QUALITY CHECKLIST:**
- [ ] Background fills full 1024x1024 canvas
- [ ] Symbol is visually centered (optical center, not just mathematical)
- [ ] Recognizable when mentally scaled to 48x48
- [ ] Colors match brand/concept
- [ ] No stray paths, artifacts, or invisible elements
- [ ] File is well-structured and readable

**For Android adaptive icons**, also generate a separate foreground SVG:
- `app_icon_foreground.svg` -- symbol only, transparent background, centered in safe zone (inset 66dp / ~166px from edges on a 1024 canvas per Android adaptive icon spec).

**For iOS 18+ dark mode**, also generate:
- `app_icon_dark.svg` -- dark background variant (dark fill, lighter or tinted symbol).
- `app_icon_tinted.svg` -- monochrome symbol on transparent background (iOS applies system tint color).

### Method B: AI Image Generation (when requested or preferred)

If the user asks for AI-generated icons, or if an image generation API is available:

1. **Check for available APIs:**
   - OpenAI API key (for DALL-E 3): check `OPENAI_API_KEY` env var
   - Other image gen APIs the project may have configured

2. **Generate with DALL-E 3** (if available):
   ```
   curl -s https://api.openai.com/v1/images/generations \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -d '{
       "model": "dall-e-3",
       "prompt": "A professional app icon for [app description]. [Symbol] centered on [color] background. Minimal flat design, no text, no letters, suitable for app store. Square format, clean edges.",
       "n": 1,
       "size": "1024x1024",
       "quality": "hd"
     }'
   ```

3. **Download and save** the generated image as `app_icon_generated.png`.

4. **Post-process:** The AI image may need cleanup -- verify it has no text, is square, and looks correct at small sizes. If it includes text or is unsuitable, retry with a revised prompt or fall back to SVG generation.

5. **Still create an SVG version** as the canonical source if possible -- AI images are raster-only and cannot be cleanly resized for all platform requirements.

### Step 2.2 -- Save Source Files

Save to the appropriate assets directory based on platform:

| Platform | Save Location |
|---|---|
| Flutter | `assets/image/app_icon.svg` (+ register in pubspec.yaml flutter.assets) |
| React Native | `assets/app_icon.svg` |
| Web | `src/assets/app_icon.svg` or `public/app_icon.svg` |
| Native iOS/Android | `assets/app_icon.svg` (or project root `icon/`) |
| Electron | `build/app_icon.svg` |
| Any (fallback) | `assets/app_icon.svg` |

### Step 2.3 -- Convert SVG to PNG

Convert to 1024x1024 PNG. Try these in order of preference:

**Option A -- rsvg-convert (best quality):**
```bash
rsvg-convert -w 1024 -h 1024 app_icon.svg -o app_icon.png
```

**Option B -- ImageMagick:**
```bash
magick -background none -size 1024x1024 app_icon.svg app_icon.png
# or older ImageMagick:
convert -background none -size 1024x1024 app_icon.svg app_icon.png
```

**Option C -- Inkscape CLI:**
```bash
inkscape --export-type=png --export-width=1024 --export-height=1024 app_icon.svg -o app_icon.png
```

**Option D -- Python cairosvg:**
```bash
python3 -c "import cairosvg; cairosvg.svg2png(url='app_icon.svg', write_to='app_icon.png', output_width=1024, output_height=1024)"
```

**Option E -- Chrome/Chromium headless:**
Create a minimal HTML wrapper and screenshot at 1024x1024.

**Option F -- sips (macOS only, limited SVG support):**
```bash
sips -s format png --resampleWidth 1024 app_icon.svg --out app_icon.png
```

Try each in order. If none work, tell the user which to install and provide the exact command.

Verify the PNG: `file app_icon.png` -- should report 1024x1024 PNG.

Also convert adaptive/dark variants if generated:
- `app_icon_foreground.png` (1024x1024, transparent background)
- `app_icon_dark.png` (1024x1024)
- `app_icon_tinted.png` (1024x1024, transparent background)

---

## PHASE 3: APPLY ICONS PER PLATFORM

Apply icons for every detected platform. Run all applicable sections.

### 3A -- Flutter

1. Add `flutter_launcher_icons` to `dev_dependencies` if not present:
   ```yaml
   dev_dependencies:
     flutter_launcher_icons: ^0.14.3
   ```
2. Configure in `pubspec.yaml`:
   ```yaml
   flutter_launcher_icons:
     android: true
     ios: true
     image_path: "assets/image/app_icon.png"
     adaptive_icon_background: "#HEXCOLOR"
     adaptive_icon_foreground: "assets/image/app_icon_foreground.png"
     min_sdk_android: 21
     remove_alpha_ios: true
     web:
       generate: true
       image_path: "assets/image/app_icon.png"
   ```
3. Run: `flutter pub get && dart run flutter_launcher_icons`
4. Verify generated files in `android/app/src/main/res/mipmap-*/` and `ios/Runner/Assets.xcassets/AppIcon.appiconset/`.

### 3B -- React Native

1. Generate required sizes. Android needs mipmap densities, iOS needs asset catalog sizes.
2. **Android:** Generate and place PNGs in `android/app/src/main/res/`:
   - `mipmap-mdpi/ic_launcher.png` (48x48)
   - `mipmap-hdpi/ic_launcher.png` (72x72)
   - `mipmap-xhdpi/ic_launcher.png` (96x96)
   - `mipmap-xxhdpi/ic_launcher.png` (144x144)
   - `mipmap-xxxhdpi/ic_launcher.png` (192x192)
   For adaptive icons, also generate `ic_launcher_foreground.png` at each density and create `mipmap-anydpi-v26/ic_launcher.xml`.
3. **iOS:** Generate and place PNGs in `ios/<AppName>/Images.xcassets/AppIcon.appiconset/`:
   - 1024x1024 (App Store), 180x180 (60pt@3x), 120x120 (60pt@2x, 40pt@3x), 87x87 (29pt@3x), 80x80 (40pt@2x), 76x76 (76pt@1x), 152x152 (76pt@2x), 167x167 (83.5pt@2x), 58x58 (29pt@2x), 40x40 (20pt@2x), 60x60 (20pt@3x)
   Update `Contents.json` to reference the new files.
4. Alternatively, use `react-native-bootsplash` or `@bam.tech/react-native-make` if already in the project.

### 3C -- Native iOS (Xcode Asset Catalog)

1. Locate the `.xcassets/AppIcon.appiconset/` directory.
2. Generate all required icon sizes (see iOS sizes above).
3. Update `Contents.json` with the correct filenames and size specs.
4. For iOS 18+ dark mode support, add dark and tinted variants to the asset catalog:
   ```json
   {
     "appearances": [{ "appearance": "luminosity", "value": "dark" }],
     "filename": "icon_dark_1024.png",
     "idiom": "universal",
     "platform": "ios",
     "size": "1024x1024"
   }
   ```

### 3D -- Native Android (Mipmap Resources)

1. Generate PNGs at all densities (see sizes in 3B).
2. Place in `app/src/main/res/mipmap-*/`.
3. For adaptive icons (API 26+), create:
   - `mipmap-anydpi-v26/ic_launcher.xml`:
     ```xml
     <?xml version="1.0" encoding="utf-8"?>
     <adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
       <background android:drawable="@color/ic_launcher_background"/>
       <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
     </adaptive-icon>
     ```
   - `values/ic_launcher_background.xml` with the background color.
   - Foreground PNGs at each density in `mipmap-*/ic_launcher_foreground.png`.

### 3E -- Web App (Favicon + PWA)

1. Generate from the 1024x1024 source:
   - `favicon.ico` (multi-size: 16x16, 32x32, 48x48) -- use ImageMagick:
     ```bash
     magick app_icon.png -resize 16x16 icon-16.png
     magick app_icon.png -resize 32x32 icon-32.png
     magick app_icon.png -resize 48x48 icon-48.png
     magick icon-16.png icon-32.png icon-48.png favicon.ico
     ```
   - `icon-192.png` (192x192, for PWA manifest)
   - `icon-512.png` (512x512, for PWA manifest)
   - `apple-touch-icon.png` (180x180)
2. Place in `public/` (or project web root).
3. Update `index.html` `<head>`:
   ```html
   <link rel="icon" href="/favicon.ico" sizes="48x48">
   <link rel="icon" href="/icon-192.png" sizes="192x192" type="image/png">
   <link rel="apple-touch-icon" href="/apple-touch-icon.png">
   ```
4. Update `manifest.json` / `site.webmanifest` if it exists:
   ```json
   {
     "icons": [
       { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
       { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
     ]
   }
   ```

### 3F -- Electron

1. Generate platform-specific icon files:
   - **macOS:** `icon.icns` (use `iconutil` on macOS or `png2icns`):
     ```bash
     mkdir icon.iconset
     sips -z 16 16 app_icon.png --out icon.iconset/icon_16x16.png
     sips -z 32 32 app_icon.png --out icon.iconset/icon_16x16@2x.png
     sips -z 32 32 app_icon.png --out icon.iconset/icon_32x32.png
     sips -z 64 64 app_icon.png --out icon.iconset/icon_32x32@2x.png
     sips -z 128 128 app_icon.png --out icon.iconset/icon_128x128.png
     sips -z 256 256 app_icon.png --out icon.iconset/icon_128x128@2x.png
     sips -z 256 256 app_icon.png --out icon.iconset/icon_256x256.png
     sips -z 512 512 app_icon.png --out icon.iconset/icon_256x256@2x.png
     sips -z 512 512 app_icon.png --out icon.iconset/icon_512x512.png
     sips -z 1024 1024 app_icon.png --out icon.iconset/icon_512x512@2x.png
     iconutil -c icns icon.iconset -o build/icon.icns
     ```
   - **Windows:** `icon.ico` (multi-resolution, 256x256 max):
     ```bash
     magick app_icon.png -resize 256x256 -define icon:auto-resize=256,128,64,48,32,16 build/icon.ico
     ```
   - **Linux:** `icon.png` (512x512)
2. Place in `build/` directory.
3. Reference in Electron's `main.js` / `electron-builder` config:
   ```json
   {
     "build": {
       "icon": "build/icon"
     }
   }
   ```
4. Alternatively, use `electron-icon-builder` if available:
   ```bash
   npx electron-icon-builder --input=app_icon.png --output=build/
   ```

### 3G -- Tauri

1. Use the Tauri icon command:
   ```bash
   npx tauri icon app_icon.png
   ```
   This generates all platform icons automatically in `src-tauri/icons/`.

### 3H -- Windows (.NET / Generic)

1. Generate `icon.ico` with multiple sizes (see Electron Windows section).
2. Place in project root or resources directory.
3. Reference in `.csproj` or resource file as appropriate.

---

## PHASE 4: VERIFY

After applying icons:

1. **Check generated files exist** at expected paths for each platform.
2. **Verify no build errors:**
   - Flutter: `flutter analyze`
   - React Native: `npx react-native doctor` or quick build check
   - Web: verify `index.html` references are correct
   - Native: check Xcode/Gradle project parses correctly
3. **Warn if overwriting:** If the project already has a custom icon (not a default/placeholder), warn the user before overwriting and ask for confirmation.

---

## PHASE 5: REPORT

Produce a summary:

```
## App Icon Generated

### Concept
- **App:** [name]
- **Symbol:** [description]
- **Colors:** [hex values]
- **Style:** [flat/semi-flat/gradient]

### Files Created
- [path]/app_icon.svg (source vector)
- [path]/app_icon.png (1024x1024 raster)
- [path]/app_icon_foreground.svg (adaptive icon foreground, if applicable)
- [path]/app_icon_dark.svg (dark mode variant, if applicable)

### Platforms Applied
- [Platform]: [what was generated and where]
- ...

### Preview
The icon uses [primary color] as the background with a [symbol] in [secondary color].
It represents [what the symbol conveys about the app].

### Next Steps
- Run the app to see the new icon on your device/browser.
- To change the icon, run `/app-icon` again with different preferences.
```

---

## STRICT RULES

- The SVG must be production quality -- no rough shapes, no placeholders.
- The icon must look professional enough for any app store or distribution channel.
- Always save both SVG (source) and PNG (build input).
- Do not use text or words in the icon -- they are unreadable at small sizes.
- Do not use more than 3 colors. Simpler is better.
- Do not leave transparency in the main launcher icon PNG -- app stores require opaque icons. (Foreground/tinted variants may use transparency.)
- Keep the symbol within the safe zone (20% padding from edges) for adaptive icon masking.
- If the project already has a custom icon (not a default), warn before overwriting.
- Commit all icon changes with a descriptive message: `feat(icon): add app icon -- [brief symbol description]`
- Apply icons to ALL detected platforms, not just one.
- For cross-platform projects (Flutter, React Native), handle all target platforms in a single run.
- When resizing PNGs for different densities, always resize from the 1024x1024 source -- never upscale from a smaller version.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /app-icon — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
