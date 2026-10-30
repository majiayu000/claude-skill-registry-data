---
name: app-store-assets
description: Make App Store screenshots, app previews, the app icon, and the new product page Header and Search Results creative assets to Apple's 2026 specs and asset best practices. Use when the user asks for "App Store screenshots", "screenshot sizes", "app preview video", "product page header", "search results asset", "creative assets", "Asset Library", "In-App Event images", or wants store art checked before submission. Covers exact pixel sizes, safe areas, what Apple rejects, a scripted pipeline from real simulator captures, a validator, and uploading with the asc CLI.
---

# App Store assets

Make every image and video on an App Store product page: screenshots, app previews, the icon, the product page **Header**, the **Search Results** asset and In-App Event media. They should be correct to the pixel, honest, and in a style that sells.

Read the reference that fits the task before producing anything:

| Task | Read |
|---|---|
| Any size, format, length or count | `references/specs.md` |
| What to show, what Apple rejects, tone and copy | `references/best-practices.md` |
| Designing and building screenshots and creative assets | `references/screenshot-playbook.md` |
| Uploading, review, Asset Library, `asc` commands | `references/upload.md` |

Specs change. Before you produce final files, re-check the live Apple pages linked in `specs.md` (or run `asc asset-library specs`). If they disagree with this skill, Apple wins; tell the user what changed.

## Workflow

1. **Inventory.** Which devices does the app support (iPhone only, or iPad too)? Which languages? Is the app already approved, or is this the first version? Header and Search Results assets need iOS 27 or iPadOS 27 viewers. They can be published without a new version only after a version has been approved.
2. **Capture real screens.** Seed realistic sample data. Capture from the simulator at the largest size you'll ship (iPhone 6.9": 1320×2868), with a clean status bar:
   `xcrun simctl status_bar <udid> override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3`
   Never mock up UI that doesn't exist.
3. **Write the story.** Up to 10 screenshots. The first 3 carry search results, so they must explain the app on their own. One idea per screenshot, with a short headline that adds to the image instead of describing it.
4. **Build with a script, not by hand.** Use `scripts/build-screenshots.mjs` and `scripts/build-creative.mjs`: an HTML template is rendered by headless Chrome and flattened to RGB PNG with no alpha. You can then rebuild everything after a UI or copy change in seconds.
5. **Validate.** Run `scripts/check-assets.sh <dir>` on every file. It must pass exact size, no alpha channel, sRGB and an allowed format.
6. **Review like App Review.** Go through the "never" list in `best-practices.md`: prices, ratings, awards, other platforms' logos, unverifiable claims, made-up data.
7. **Preview, then upload.** Check the Header and Search Results crops in App Store Connect's Preview tool. Upload with `asc` (see `references/upload.md`) and confirm with `asc screenshots list`.

## Rules that cause rejections or broken uploads

- Exact pixel sizes only, and **no alpha channel**. Transparent PNGs are rejected, so flatten onto a solid colour.
- The 16:9 universal creative asset (5244×2950) must be **PNG**.
- Screenshots and previews show the real app. Anything that isn't the user's own data is clearly sample data.
- Assets must suit a **4+ audience**, even if the app is rated higher.
- No prices or discounts, no URLs, no © symbols, no "Editor's Choice" or "App of the Day", no awards or user counts you can't prove, and no Android, Google Play or other platform logos.
- Text must be localized for every language the app supports, or left off.

## Output

Deliver the PNG and video files, the build script and its config (so the user can rebuild), a contact sheet, and a short note listing each asset, its size and what it shows. Point out anything you couldn't verify, for example a safe area you couldn't check in the Preview tool.
