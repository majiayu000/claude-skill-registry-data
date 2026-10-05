---
name: app-store-screenshots
description: Capture App Store / TestFlight screenshots from the iOS Simulator at native resolution, downscale to every required display size, and upload to App Store Connect via helm-asc. Use when asked to take/produce/refresh App Store screenshots, marketing screenshots, or screenshots for custom product pages.
---

# App Store Screenshots

Capture native-resolution screenshots on the simulator, downscale to the other required sizes, upload via `helm-asc`.

## Sizes (only TWO files per screen are actually needed)

| Display | Pixels | Device |
|---------|--------|--------|
| 6.9" | 1320×2868 | iPhone 16/17 Pro Max (capture native here) |
| 6.7" | 1290×2796 | downscale from 6.9" |
| 6.5" | 1242×2688 | downscale from 6.9" |

Aspect ratios differ <0.4%, so downscaling 6.9"→6.7"/6.5" is visually lossless. If the app's deployment target is iOS 26+, **no real 6.5"-class device can run it** — those sizes MUST be derived from a 6.9" capture, never captured natively.

## Capture pipeline

1. **Boot the largest Pro Max sim** and build/install: `flowdeck simulator boot <udid>`; `flowdeck run -S <udid> -d ios/DerivedData-shots`. Find the UDID with `flowdeck simulator list` (pick an iPhone 17/16 Pro Max).
2. **Clean status bar:** `flowdeck simulator status-bar override -S <udid> --time "9:41" --data-network 5g --wifi-mode active --wifi-bars 3 --cellular-mode active --cellular-bars 4 --battery-state charged --battery-level 100`. Re-assert it before each capture (navigation can reset it).
3. **Capture at NATIVE resolution** — use `flowdeck simulator frames --images -S <udid> -t 1s --fps 2 -o <dir>`, then take `frame-000-*.png` (1320×2868). ⚠️ Do NOT use `flowdeck ui simulator screen --screenshot` for the deliverable — it returns POINT resolution (440×956 @1x), which ASC rejects. `frames --images` is the native-res path.
4. **Navigate** by reading the tree as text — `rocketsim elements --agent-mode nav` or `flowdeck ui simulator screen --tree --json` — then `flowdeck ui simulator tap "<label>"` or `tap --point x,y` (point coords from the tree). Re-assert status bar, then capture each screen with step 3's native-resolution command — the tree read is for finding what to tap, not for the deliverable.
5. **Downscale** to the other sizes: `sips -z 2796 1290 6.7/NN.png` and `sips -z 2688 1242 6.5/NN.png` (note `sips -z` is height-then-width).

## Upload via helm-asc

helm-asc is **sandboxed** — it can't read arbitrary paths. Stage the tree in its inbox:
```
INBOX=$(helm-asc paths --agent | python3 -c "import json,sys;print(json.load(sys.stdin)['uploadsInbox'])")
# Build <path>/<locale>/<deviceType>/NN_name.png  e.g. en-US/APP_IPHONE_67/01_home.png
helm-asc version <version-id> screenshots upload --path "$INBOX/<dir>" --dry-run   # validate first
helm-asc version <version-id> screenshots upload --path "$INBOX/<dir>"
```
- **Device types:** `APP_IPHONE_67` (6.7"), `APP_IPHONE_65` (6.5"). helm-asc does **not** support `APP_IPHONE_69` — the 6.9" native set must be added through the ASC web UI if wanted (the 6.5" tier satisfies Apple's required iPhone size, so 67+65 is a valid submittable set).
- The `NN_` filename prefix sets display order in ASC.
- **Custom Product Pages** can't be created or populated by helm-asc — those are ASC-web-UI only; reuse the same `.shots/` folders there.

## Gotchas

- **You cannot CLI-screenshot a physical device.** Network-connected devices route through CoreDevice; `idevicescreenshot`/libimobiledevice only speak legacy usbmuxd and won't see them, and the RocketSim/flowdeck CLIs are simulator-only. For real-device shots (e.g. a signed-in premium account), have the user take them on-device and AirDrop them (they land in `~/Downloads`, native 1320×2868).
- **Gated screens:** in signed-out "Explore"/guest mode the player shows a premium error and Stats/streaks does nothing. The **paywall** is reachable signed-out via Settings → Subscribe. A clean "playing" player and real Stats need a signed-in account — either sign one into the sim or use AirDropped device shots.
- Real-device shots carry a real status bar (time/battery), not 9:41 — acceptable for App Store, but note the inconsistency vs the sim's 9:41 shots; RocketSim's GUI can overlay a clean status bar on device captures if needed.
