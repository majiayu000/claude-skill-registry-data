---
name: macos-app-icons
description:
  Design and build macOS app icons and in-app icon tiles procedurally, with no image generator. Draw flat layers with a
  Swift/AppKit script, assemble them into an Icon Composer .icon (Liquid Glass, light and dark), compile it with actool
  outside Xcode, and verify how macOS renders it next to system icons. Also covers matching SwiftUI tiles for icons
  shown inside the app. Use when creating, redrawing or reviewing a Mac app's icon or its in-app icon style.
---

# macOS app icons, drawn in code

Draw the icon with code, then let the system add the material. A script draws a few flat shapes on transparent 1024 pt
layers. An Icon Composer `.icon` package puts them over a background fill, and macOS 26 renders the Liquid Glass,
specular highlights, shadows and the dark and tinted variants. The result is reproducible, reviewable in a diff, easy to
iterate on with the user, and consistent with the app's in-app icons, because both come from the same shapes and colors.

Don't reach for an image generator for the app icon: generated art bakes in lighting that fights the system glass, can't
be tweaked by a few numbers, and rarely survives 16 pt. Offer generated art only when the user asks for an illustrated
look.

The references are working templates, verified end to end on macOS 26 with Xcode 26:

- [make-icon.swift](references/make-icon.swift) draws the layers (`swift make-icon.swift Resources/AppIcon.icon`).
- [icon.json](references/icon.json) is the `.icon` manifest: gradient fill with a dark specialization, glass layers.
- [preview-icons.swift](references/preview-icons.swift) renders the built app's icon beside system icons at 256–16 pt,
  light or dark, as a PNG.
- [in-app-tiles.md](references/in-app-tiles.md) has the SwiftUI tile that matches the icon inside the app.

## 1. Design the motif

1. Say what the app _is_ in one object or scene: the thing users recognize it by (a deck of tiles and a widget card for
   a launcher, a card with a check for a to-do app). Show the app's content, not a letter or a generic symbol.
2. Sketch it as 1–4 simple shapes on a grid. Each shape becomes one layer and gets its own glass, so separate the parts
   that should read as distinct objects, and keep details inside a shape (bars on a card, a prompt on a tile).
3. Pick a background gradient and 3–5 accent colors. A dark or saturated fill makes light shapes pop and holds up in
   dark mode. Check the fill against the Dock in both appearances.
4. Avoid looking like Apple's own icons: a grid of colored squares reads as Apple's Apps, a blue compass as Safari. Put
   the candidate next to them in the preview and ask the user when it's close.

Present the concept in a sentence or two before drawing. Iterate on the user's reaction to real renders, not on
descriptions.

## 2. Draw the layers

Copy [make-icon.swift](references/make-icon.swift) to `scripts/make-icon.swift` and replace its example layers.

- Canvas 1024 × 1024, transparent, AppKit coordinates (origin bottom-left). One PNG per layer, named as in `icon.json`.
- **Keep the artwork to the middle ~60%** of the canvas. At ~78% the icon looked bigger and more raised than its
  neighbours in the Dock. The system mask, glass edge and shadow need the margin.
- Draw **flat**: solid fills or a gentle two-stop gradient, rounded corners, no drop shadows, glows, bevels or glare.
  The glass supplies depth, and baked effects double up with it.
- Lay shapes out from a few constants (cell size, gap, corner radius as a fraction of the cell) so a redraw changes
  numbers, not code.
- Text and glyphs: draw with `NSFont` (e.g. `monospacedSystemFont` for a `>_` prompt, a heavy system weight for a
  check), or build the glyph from paths. Don't put SF Symbols in the app icon: Apple's symbol license excludes app icons
  and logos (they're fine in in-app tiles). Nudge vertical centering by eye; fonts carry descender space.
- Details thinner than ~24 pt at 1024 disappear at 32 pt. Check small sizes in the preview and drop or thicken them.

## 3. Assemble the `.icon`

The `.icon` package is a folder: `AppIcon.icon/icon.json` plus `AppIcon.icon/Assets/<layer>.png`. Start from
[icon.json](references/icon.json):

- `fill-specializations`: the background. A `linear-gradient` of `extended-srgb:r,g,b,a` stops with `orientation`
  start/stop points (0–1, y down). Add an entry with `"appearance": "dark"`, usually the same hues darker, so the icon
  follows the system's dark icon style.
- `groups[].layers`: **listed front to back: the first layer is drawn on top.** Each has `image-name`, `name` and
  `"glass": true`.
- Group settings that worked: `"lighting": "individual"`, `"specular": true`,
  `"shadow": {"kind": "neutral", "opacity": 0.35}`, `"translucency": {"enabled": true, "value": 0.2}`. More translucency
  washes the shapes into the fill.
- `supported-platforms.squares: ["macOS"]`.

The user can open the same `.icon` in Icon Composer (in Xcode 26's developer tools) to fine-tune glass and colors by
hand. The script only rewrites `Assets/`, so their `icon.json` edits survive a redraw. Commit the `.icon` folder, its
PNGs and the script.

## 4. Compile it without Xcode

`actool` compiles a `.icon` into `Assets.car` (Liquid Glass) plus a flat `AppIcon.icns` fallback for anything that can't
read the catalog, and writes the Info.plist keys (`CFBundleIconName`, `CFBundleIconFile`) to a partial plist:

```bash
ICON_DIR="$(mktemp -d)"
xcrun actool Resources/AppIcon.icon --compile "$APP/Contents/Resources" --app-icon AppIcon \
  --platform macosx --target-device mac --minimum-deployment-target 26.0 \
  --output-partial-info-plist "$ICON_DIR/icon.plist" --errors --warnings >/dev/null
/usr/libexec/PlistBuddy -c "Merge $ICON_DIR/icon.plist" "$APP/Contents/Info.plist"
rm -rf "$ICON_DIR"
```

Run it in the app bundle script before signing. Remove any old hand-made `AppIcon.icns` from the resources you copy, so
the compiled one wins. With an Xcode project, add the `.icon` to the target instead and Xcode runs `actool` for you.

## 5. Verify what macOS renders

Source layers aren't the icon. Check the compiled app:

1. `ls "$APP/Contents/Resources"` shows `Assets.car` and `AppIcon.icns`, and `CFBundleIconName` is in Info.plist.
2. Render it beside system apps, in both appearances:

   ```bash
   swift preview-icons.swift /tmp/icons-light.png "$APP" /System/Library/CoreServices/Finder.app /System/Applications/Notes.app
   swift preview-icons.swift /tmp/icons-dark.png --dark "$APP" /System/Library/CoreServices/Finder.app /System/Applications/Notes.app
   ```

   Compare the outline size and weight with its neighbours, and check that it reads at 32 and 16 pt. A blank document
   icon means the path is wrong or the bundle has no `CFBundleExecutable`.

3. Look at the PNGs yourself, fix, redraw, recompile. Then send the renders to the user and ask them to look at the real
   Dock and Finder too (Finder caches icons; `touch` the app or relaunch the Dock if an old one sticks). Judging the
   design on their screen is their call.

Don't install over, launch or re-register the user's own copy of the app to check an icon; preview a build in the
project's build folder.

## 6. Match the icons inside the app

Icons the app draws for its own content (items, sidebar entries, placeholders) should look like siblings of the app
icon: the same squircle, gradient direction, colors and glyph style, scaled down. See
[in-app-tiles.md](references/in-app-tiles.md) for a SwiftUI tile (continuous squircle, two-stop gradient, a light sheen,
a thin top-lit border and a soft shadow) and the sizes and contrast rules that go with it. Real app icons and favicons
stay as they are; custom tiles fill ~80% of the frame, like the art inside a real app icon.

## Checklist

- [ ] Motif shows what the app is, in 1–4 flat layers, within the middle ~60%.
- [ ] `icon.json` lists layers front to back, has a dark fill specialization, and glass on every layer.
- [ ] The build compiles the `.icon` with `actool` and merges `CFBundleIconName`; no stale `.icns` is copied over it.
- [ ] Preview renders checked at 256–16 pt in light and dark, next to system icons.
- [ ] The user has seen the renders and judged it in their own Dock.
- [ ] In-app tiles share the icon's shape, colors and glyph style.
