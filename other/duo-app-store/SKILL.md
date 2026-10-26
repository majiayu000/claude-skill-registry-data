---
name: duo-app-store
description: "Prepares an app's App Store submission for iPhone Duo, Apple's foldable with a 1398 x 2034 outer display and a 2007 x 2853 inner display: App Store screenshots of both displays at the exact sizes App Store Connect lists, flattened without alpha, captured from the iPhone Duo simulator in each pose with a clean status bar; app previews (886 x 1920); uploading them in App Store Connect or with the App Store Connect API (screenshot display type APP_IPHONE_DUO, not in Apple's API reference yet); the 'optimized for iPhone Duo' product page badge; promotional text and the App Store Connect preview tool; App Review notes for the poses; the privacy manifest; and the April 2027 rules (Duo screenshots required, iOS 27 SDK or later, iOS 15 or later). Use when someone asks for Duo screenshots, store assets, a submission checklist or review notes for iPhone Duo."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, App Store Connect API upload, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-app-store

Get an app onto the App Store as an iPhone Duo app: screenshots of both displays, the metadata that goes with them, notes for App Review, and the rules that start in April 2027.

Load other skills for the work around it: `duo-migrate` (the build must use the iOS 27.1 SDK first), `duo-pose-matrix` (sets each pose from outside the app), `duo-testing` (launch switches that open the app on a given screen with sample data), `duo-design-review` (check the frames before they ship).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 23 October 2026, or saw it in a real App Store Connect API upload on 18 October 2026; details in [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline.

## What Apple asks for

From the [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications), the [app preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications) and Apple's [news of 5 October 2026](https://developer.apple.com/news/?id=kkphp5qo):

| What | iPhone Duo |
|---|---|
| Screenshot sizes, outer display | 1398 × 2034 or 2034 × 1398 px |
| Screenshot sizes, inner display | 2007 × 2853 or 2853 × 2007 px |
| Screenshots per set | 1 to 10 |
| Formats | PNG or JPEG, with no alpha channel |
| App previews (optional) | 886 × 1920 or 1920 × 886 px, 15 to 30 s, up to 3 |
| Product page badge | Shown when the app has iPhone Duo screenshots |
| Required from | April 2027 |

- Apple words the April 2027 rule two ways: the screenshot page says it applies to apps using the iOS 27.1 SDK or later; the news says every app or game submitted. Plan for the stricter one.
- From April 2027, uploads must also be built with the iOS 27 SDK or later and target iOS 15 or later ([Submitting](https://developer.apple.com/app-store/submitting/)).
- The preview page labels Duo previews "19.5:9", which matches 886 × 1920 but not the device's own pixel sizes. Use 886 × 1920 or 1920 × 886.

## Rules

- Real screens only: the app running on the iPhone Duo simulator (or a device), at the display's native size. Never upscale, never stretch an iPhone frame to Duo size, never draw UI that the app doesn't have.
- Capture the display that is on. Closed, the inner display is off; open, the outer one is. *Measured:* a screenshot of the display that is off comes back at full size and pure black.
- No alpha channel. *Measured:* `simctl` screenshots are PNGs with an alpha channel by default, which the spec doesn't allow; `--type=jpeg` saves the same size without one.
- Sample data only, never someone's real account, name or photo.
- Show the open phone as well as the closed one. The badge says "optimized for iPhone Duo"; the inner display is where people see that.
- Use the shared iPhone Duo simulator by UDID. Never create a simulator for screenshots.

## Step 1. Plan the set

Pick 3 to 6 moments that sell the app, then the pose that shows each one best:

| Pose | Display to capture | Good for |
|---|---|---|
| Closed | Outer, 1398 × 2034 | The quick glance: the main screen as people see it first |
| Open, held wide | Inner, 2853 × 2007 | Two panes side by side, the layout that only Duo has |
| Open, held tall | Inner, 2007 × 2853 | Long lists, reading, a feed |
| Book, tabletop | Inner | A video above the fold, controls below; two pages |

Apple's App Store pages ask you to show the app "across orientations" ([news](https://developer.apple.com/news/?id=kkphp5qo)). Put your strongest open-phone frame first.

## Step 2. Put the app in each state

Open the app straight into each screen with launch arguments and sample data, so every capture is repeatable (`duo-testing`, launch switches). A `-screenshots` switch that loads fixed sample data, hides debug UI and fixes dates keeps the frames identical between languages and releases.

Set the pose before each capture: in Device Hub by hand (Closed, Partially Open, Open; tabletop is Partially Open, then Rotate Right), or with `duo-pose set closed|open|book|tabletop` from `duo-pose-matrix`, with the user's Accessibility permission.

## Step 3. Capture both displays

Clean the status bar first, then capture, then put it back:

```bash
UDID=<iPhone Duo simulator UDID>
DEV=/Applications/Xcode-27.1.app/Contents/Developer
DEVELOPER_DIR=$DEV xcrun simctl status_bar "$UDID" override --time "9:41" \
  --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
<skill-folder>/scripts/duo-shots Store/iPhoneDuo 01-home
DEVELOPER_DIR=$DEV xcrun simctl status_bar "$UDID" clear
```

[`scripts/duo-shots`](scripts/duo-shots) saves each display with `simctl io screenshot --type=jpeg` (`--display=primary` is the outer display, `--display=primary-1` the inner one), checks the size against the list above, skips a display that came back black, and writes `<name>-outer.jpg` and `<name>-inner.jpg`. It uses the booted iPhone Duo simulator, or the one in `UDID`. `<skill-folder>` is the folder that holds this `SKILL.md`.

- *Measured:* closed and upright, the outer display saved at 1398 × 2034 and the inner one at 2007 × 2853, both exact App Store sizes. The script wrote the outer frame as a JPEG without alpha and skipped the black inner one.
- The run can only capture the display that is on. Change the pose between captures (Step 2), and if you can't, say which display is still missing rather than filling the gap.
- *Unverified:* that the status bar override shows on both displays of the iPhone Duo simulator: the command succeeded, but the frames we captured didn't show a status bar to check.
- `duo-pose-matrix` can capture every pose in one run when you only need the frames, not the store names.

## Step 4. Frames and captions

Captions and backgrounds are allowed, but keep the exact pixel size of the capture, and keep the app's screen large enough to read on a phone. Apple's [asset best practices](https://developer.apple.com/app-store/asset-best-practices/) have templates for screenshots, previews and the new product page header and search assets. Localize the captions and, where you can, capture the app itself in each language.

## Step 5. Upload

- **App Store Connect**: the version's page, Previews and Screenshots, under iPhone Duo. Check them with the [preview tool](https://developer.apple.com/news/?id=kkphp5qo) that shows the product page on iPhone Duo.
- **App Store Connect API**: create an `appScreenshotSets` record for the version's localization with `screenshotDisplayType` = `APP_IPHONE_DUO`, then reserve, upload and commit each screenshot ([uploading assets](https://developer.apple.com/documentation/appstoreconnectapi/uploading-assets-to-app-store-connect)) and wait for each asset to finish processing.
  - *Measured* (18 October 2026): `APP_IPHONE_DUO` is the value the API accepted, and it named it in its error for an unknown display type. Apple's [ScreenshotDisplayType](https://developer.apple.com/documentation/appstoreconnectapi/screenshotdisplaytype) reference didn't list it when we checked on 23 October 2026.
  - *Measured:* 2007 × 2853 inner-display screenshots were accepted in that set. *Unverified:* whether one set takes inner and outer sizes together, and whether 2853 × 2007 landscape uploads go through; upload one size per set first and check that each asset finishes.

## Step 6. Metadata

- **Badge**: comes from the iPhone Duo screenshots; nothing else to set ([screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)).
- **Promotional text and description**: say what the app does on the open phone in the user's words ("each player gets a whole screen", "the list and the map side by side"). Promotional text can change without a new build.
- **Featuring**: Apple's prepare page invites you to tell Apple your app is optimized for iPhone Duo, including every pose ([prepare page](https://developer.apple.com/iphone-duo/prepare/)).

## Step 7. Notes for App Review

Tell the reviewer where the Duo experience is and how to reach it: which poses the app supports, which feature changes when the phone opens, any switch or sample account needed. A template is in [references/review-notes.md](references/review-notes.md). Keep it short and factual; it goes in App Review Information when you submit ([App Review](https://developer.apple.com/distribute/app-review/)).

## Privacy manifest

Unrelated to the fold, but checked on the same submission: an app or SDK that uses an API with a required reason, or tracks, declares it in `PrivacyInfo.xcprivacy` ([privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)). Generate Xcode's privacy report from the archive (Organizer, Generate Privacy Report) and check each third-party SDK ships its own manifest.

## Checklist

- [ ] The build uses the iOS 27.1 SDK (`duo-migrate`).
- [ ] Screenshots of the inner display and the outer display, each at a listed size, 1 to 10 per set, JPEG or PNG without alpha, none black.
- [ ] Every frame is the real app with sample data and a clean status bar; the open phone comes first.
- [ ] Captions keep the exact pixel size and are localized.
- [ ] App previews, if any, are 886 × 1920 or 1920 × 886 and 15 to 30 s.
- [ ] Uploaded under iPhone Duo (API: `APP_IPHONE_DUO`); every asset finished processing; checked with the preview tool.
- [ ] Promotional text says what the open phone does.
- [ ] App Review notes say which poses to try and how to reach them.
- [ ] Privacy manifest and Xcode's privacy report checked.
- [ ] Ready for April 2027: Duo screenshots, iOS 27 SDK or later, iOS 15 or later.
