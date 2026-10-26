---
name: recipe-shop
description: "Creates a complete SwiftUI shop for iPhone Duo, Apple's foldable, that sells digital packs and a subscription with StoreKit 2: a product grid with even columns that reflows from 2 per row on the closed outer display to 4 on the open inner display with the fold as its middle gutter, product detail beside the grid when open, a basket that checks out one App Store purchase at a time, and a two-pane paywall and checkout (what you get on one side, price and button on the other; one column with the button pinned when closed). Use when someone wants to start a new shop, catalog, in-app purchase or paywall app from scratch, or runs /duo-new recipe-shop. For an existing app, use duo-patterns (feed reflow, list-detail) instead. Covers a local StoreKit configuration file (no network, no real products), PurchaseAction, Transaction.updates and currentEntitlements, restore, Ask to Buy, SKTestSession in UI tests, a Foundation-only model tested on the Mac, and UI tests that pass in any pose on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# recipe-shop

This recipe makes a new Xcode project: a shop that sells sound packs for one iPhone Duo. Closed, the packs sit two per row under a Plus card and a new pack; a pack opens on its own screen. Open, the grid spans the window, four per row, two on each side of the fold. Pick a pack and it opens beside the grid. The basket and the Plus subscription screen split on the fold too: the packs or what Plus gives on one side, the price and the button on the other.

The packs are a placeholder. The value is the frame: a grid that never puts a tile in the fold, list-detail that survives opening and closing the phone, StoreKit 2 code that buys, restores and handles Ask to Buy, checkout rules you can test on the Mac in seconds, and UI tests that buy, fail and wait for approval on the Duo simulator.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1). *Unverified* means we could not check it. Everything else links to Apple. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

Use a different skill when:

- the app already exists: use `duo-patterns` (feed reflow, list-detail) and `duo-design-system` (the grid);
- the shop sells physical goods or services used outside the app. StoreKit is only for what people use in the app; for the rest, App Review asks for Apple Pay or another payment method ([guideline 3.1.3(e)](https://developer.apple.com/app-store/review/guidelines/)). Keep this recipe's layouts and replace `Store`.

## 1. Create the project

`/duo-new recipe-shop` runs steps 1 to 4, then installs and launches the app with no StoreKit session, so every price reads "–". Run steps 5 and 6 yourself. Run every step yourself when there is no command.

1. Get three values from the user, or propose them:
   - `AppName`: letters and digits, starting with a letter (it becomes a Swift type, `<AppName>App`). Not `Tools` or `StoreKit` (folders in the template), and not an Apple module name such as `SwiftUI` or `Foundation`;
   - a bundle id such as `com.example.soundshop`;
   - a new, empty folder.
2. Run the script from this skill's folder (in the plugin: `${CLAUDE_PLUGIN_ROOT}/skills/recipe-shop/scripts/new-project.sh`):

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/recipe-shop/scripts/new-project.sh" \
     SoundShop com.example.soundshop ~/Developer/SoundShop
   ```

   It copies `template/`, replaces `__APP_NAME__` and `__BUNDLE_ID__` in file contents and paths, checks none are left, and prints the next steps. It refuses a folder that exists and is not empty (exit 73), and bad or clashing names (exit 65) before it creates anything.
3. Test the rules on the Mac. Expect `0 failed`: `cd ~/Developer/SoundShop && Tools/run-model-tests.sh`. Among them: every product in the catalog matches `StoreKit/Shop.storekit`.
4. Build for the Duo simulator (find its UDID with `xcrun simctl list devices available | grep "iPhone Duo"`):

   ```bash
   DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
   xcodebuild -quiet -project SoundShop.xcodeproj -scheme SoundShop \
     -destination "platform=iOS Simulator,id=<UDID>" \
     -derivedDataPath build/DerivedData build
   ```

5. Run the UI tests: `DESTINATION="id=<UDID>" Tools/run-ui-tests.sh`. With no setting it uses the simulator named `iPhone Duo`. They open a StoreKit test session on `StoreKit/Shop.storekit`, and the simulator keeps it for this app afterwards, purchases included: after the subscribe test, the shop shows Plus as on. Run `-only-testing:<AppName>UITests/<AppName>UITests/testPricesComeFromTheStoreKitConfiguration` to leave a clean state.
6. Launch on a pack and screenshot the display in use. Use the UDID, not `booted`. The tests installed the app.

   ```bash
   DEV=/Applications/Xcode-27.1.app/Contents/Developer
   DEVELOPER_DIR=$DEV xcrun simctl launch --terminate-running-process <UDID> com.example.soundshop -select pack.harbor
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary build/outer.png     # closed
   DEVELOPER_DIR=$DEV xcrun simctl io <UDID> screenshot --display=primary-1 build/inner.png   # open
   ```

   *Measured:* launched with `simctl` before any test session, StoreKit returned no products and every price read "–"; after one, prices showed. Only the display in use has content. Look at the PNG before you report. In Xcode, Product > Run uses the scheme's StoreKit configuration directly.
7. Tell the user what passed, and that poses change only in Device Hub (`duo-pose-matrix` can press its buttons).

Set `DEVELOPER_DIR` for every `xcrun` and `xcodebuild` call when the Mac has more than one Xcode. Never run `xcode-select` for this.

## 2. What you get

| Path | What it holds |
|---|---|
| `<App>/Model/Catalog.swift`, `SampleCatalog.swift` | Packs, tracks, categories and the two Plus plans, with StoreKit product IDs. |
| `<App>/Model/Cart.swift` | The basket: add once, toggle, remove packs the person already has, exact `Decimal` totals, "Plus costs less". |
| `<App>/Model/CheckoutRun.swift` | Checkout, one purchase at a time: cancel or error stops it, pending moves on, resume carries on. |
| `<App>/Model/Ownership.swift`, `PlanMath.swift` | What the person owns (packs, Plus) from entitlements; the yearly saving. |
| `<App>/Model/DuoColumns.swift` | `DuoFold`, `DuoColumns`, `PaneFrames`: the grid and pane math from `duo-design-system`. Foundation only. |
| `<App>/Store/Store.swift` | The only StoreKit code: products, purchases, `Transaction.updates`, entitlements, restore. |
| `<App>/Shop/` | The grid, the Plus card, the new pack card, the price slot. |
| `<App>/Detail/PackDetail.swift` | One pack: price, basket button, sounds. |
| `<App>/Basket/BasketScreen.swift` | Basket and checkout. |
| `<App>/Plus/PlusScreen.swift` | The paywall: benefits, plans, subscribe, terms, restore, manage. |
| `<App>/Shared/` | Tokens, `FoldPanes`, `ActionPanes` (two panes, or one column with a pinned button), pack artwork. |
| `StoreKit/Shop.storekit` | The local StoreKit configuration: 12 non-consumables, two subscriptions in one group, a free week on the yearly plan. |
| `<App>UITests/` | Eleven UI tests, pose-agnostic, with a StoreKit test session. |
| `Tools/` | `run-model-tests.sh`, `ModelTests/main.swift`, `run-ui-tests.sh`. |

Project settings match the other recipes: iOS 26.0 deployment, Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, approachable concurrency, file-system synchronized groups, a privacy manifest that declares nothing collected, and a scheme with parallel testing off and the StoreKit configuration on Run.

Architecture and test details: [references/architecture.md](references/architecture.md). StoreKit, testing and going live: [references/storekit.md](references/storekit.md).

## 3. How it behaves in each pose

| Pose | Width class | Shop | Basket and Plus |
|---|---|---|---|
| Closed (outer display) | compact | 4 columns: packs span 2 (2 per row), cards span 4. A pack is pushed. | One column; Buy or Subscribe pinned at the bottom. |
| Open, flat, held wide | regular | 8 columns, the gutter between the halves centred on the fold line: 4 packs per row, one card per side. A picked pack opens in the trailing pane; the grid keeps 2 per row in the leading pane. | Two panes: packs or benefits leading; total or plans, the button and the terms trailing. |
| Partly folded like a book | regular | The same columns; only the gap at the fold grows, to the fold's frame. With a pack open, the grid's pane ends at 455.7 pt and the pack's starts at 495.7 pt (*measured*; flat: 467.7 and 483.7). | Same panes; the fold is the gap between them. |
| Open, held tall, or set on a table like a laptop | regular | The fold runs across, between rows; 8 equal columns (unverified on this recipe). | Two equal panes (unverified). |

The pack, the basket, a checkout in progress and the store live in `ShopModel` and `Store`, above the stack. *Measured:* closed on a pack, then opened, then closed: the pack moved to the trailing pane and back to its own screen.

## 4. Where each Duo technique lives

| Technique | Where | Why |
|---|---|---|
| Even columns, the fold as the middle gutter | `ShopColumn` in `Shop/ShopScreen.swift`: `DuoColumns` grouped by `tokens.span(2)` for packs, `span(4)` for cards | Apple asks for an even column count whenever a division region exists, active or not, and for the gap at the hinge to widen while the outer margins stay ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)). `duo-patterns` calls this feed reflow. |
| Tiles line up across the fold | Fixed art height and line counts in `PackTile` | The halves differ in width next to the vertical bar, so an aspect-ratio image made the two halves' rows different heights (*measured*). |
| Grid alone or beside a pack | `ShopScreen`: `PaneFrames` only when a pack is picked and the width is regular | Open with nothing picked, the grid spans the fold; with a pack, it moves to the leading pane. |
| Text stays on one side | The "All packs" header is capped at the first card's width | A heading or button across the fold is hard to read and to tap. |
| Two-pane paywall and checkout | `Shared/ActionPanes.swift` | Regular: `FoldPanes` with the button in the trailing pane. Compact: one scroll view with `.safeAreaInset(edge: .bottom)` holding the button. |
| Unfolding on a pushed pack | `RootView` waits 600 ms before switching to two panes | *Measured:* popped during the unfold animation, the shop came back with the closed phone's insets and no margins (x −2 pt, right inset 42 pt instead of 84 pt) and stayed so; popped after it, it matched a fresh launch. Same as `recipe-finance-dashboard`. |
| Buy from the right display | `@Environment(\.purchase)` ([`PurchaseAction`](https://developer.apple.com/documentation/storekit/purchaseaction)) in the basket and paywall | Apple's SwiftUI purchase action carries the view's scene, so StoreKit's confirmation shows next to it, on whichever display the app is on. |
| Purchases that arrive later | `Store.start()` listens to [`Transaction.updates`](https://developer.apple.com/documentation/storekit/transaction/updates) at launch | Ask to Buy approvals, other devices, renewals and unfinished transactions arrive there. |
| Width class, never the device | `RootView` | Same rule as every Duology skill. |

## 5. Customise

Change the catalog and the rules first, in `Model/` and `StoreKit/Shop.storekit`, and test them on the Mac.

- **Your products:** edit `SampleCatalog.swift` and `Shop.storekit` together, with the same IDs you will create in App Store Connect. `Tools/run-model-tests.sh` fails when an ID, a price, a name, a period or a trial differs.
- **Artwork:** replace `PackArt` with images. Keep a fixed height in the grid tile.
- **One-tap buy:** call `model.store.buy(id, with: purchase)` from `PackDetail` instead of the basket button. Keep the basket for several packs.
- **Physical goods:** keep `Cart` and the screens; replace `Store` with Apple Pay or your provider, and drop `Ownership`.
- **Paywall copy:** say clearly what people get for the price ([guideline 3.1.2(c)](https://developer.apple.com/app-store/review/guidelines/)). That guideline also points to Schedule 2 of the Apple Developer Program License Agreement: read both before you submit. The template shows the billed price first, a renewal line, Terms of Use, Privacy Policy and Restore. Replace the sample Privacy Policy link.

Keep these, whatever the app:

1. Prices, periods and trials from StoreKit (`displayPrice`, `priceFormatStyle`, `subscription`), never typed in a view.
2. Only verified, unrevoked transactions unlock anything; finish them after you deliver.
3. Restore only from a button: `AppStore.sync()` asks the person to sign in ([doc](https://developer.apple.com/documentation/storekit/appstore/sync())).
4. Even columns with `.includeInactive`, a fixed tile height, and buttons inside one pane.
5. The 600 ms wait before popping on unfold, until a device run says otherwise.

## 6. Test it

**On the Mac:** `Tools/run-model-tests.sh` builds `Model/*.swift` with the test program using `swiftc -swift-version 6 -default-isolation MainActor`. *Measured:* 67 checks pass in a few seconds, including the catalog against `Shop.storekit`; removing `nonisolated` from any of the 13 model types stops the build.

**On the simulator:** `Tools/run-ui-tests.sh`. Eleven tests: prices from StoreKit, even columns, list-detail, the basket total and removal, a full checkout, a failed purchase that stops checkout until resumed, Ask to Buy, both plans, subscribing, and a layout check per pose. *Measured:* all eleven pass closed and open, and `testLayoutInThisPose` passes partly folded (iPhone Duo simulator, iOS 27.1, 20 Oct 2026).

The scheme's StoreKit configuration reaches the app only when Xcode runs it. *Measured:* under `xcodebuild test`, prices stayed unavailable, even with the file also set on the test action. So the tests open an [`SKTestSession`](https://developer.apple.com/documentation/storekittest/sktestsession) on `StoreKit/Shop.storekit` themselves, found through `#filePath`, clear past purchases and turn off the confirmation sheets. Details and the Duo UI test notes: [references/storekit.md](references/storekit.md#testing).

## Checklist

- [ ] Project created with `scripts/new-project.sh`; no `__APP_NAME__` or `__BUNDLE_ID__` left.
- [ ] `Tools/run-model-tests.sh` prints `0 failed`, including the StoreKit file checks.
- [ ] `xcodebuild … build` succeeds for the iPhone Duo simulator with no warnings from your code.
- [ ] `python3 duo-lint.py --strict <project>` reports no findings.
- [ ] `Tools/run-ui-tests.sh` passes closed and open.
- [ ] Screenshots of the display in use, after a test run: prices show; closed 2 packs per row; open 4 per row with no tile in the fold.
- [ ] In Device Hub, Partially Open: the gap between the halves is the fold; no button, price or tile in it.
- [ ] Pick a pack, close the phone, open it: the pack stays on screen, beside the grid when open, and the grid keeps its margins.
- [ ] Paywall shows the billed price, period, trial, renewal line, Terms, Privacy and Restore.
- [ ] Products created in App Store Connect with the same IDs before release; tested once with a Sandbox account on a device.
