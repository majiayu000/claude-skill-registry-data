---
name: openfoodjournal
description: Living project knowledge for OpenFoodJournal — an iOS 26 food journaling app with AI-powered nutrition scanning. Consult this skill FIRST when starting any work on this project. Contains architecture decisions, data models, service contracts, current state, known issues, and conventions. Update this skill whenever requirements, architecture, or project state changes so it stays accurate across sessions.
---

# OpenFoodJournal — Project Knowledge

This is the single source of truth for any LLM agent working on this project. Read this before writing code. Update it when things change.

## Quick Facts

| Key | Value |
|-----|-------|
| Platform | iOS 26.2+ (iPhone) |
| UI Framework | SwiftUI + Liquid Glass (no `#available` gating needed) |
| Data Layer | SwiftData (`@Model`) + CloudKit Private Database (`iCloud.k3vnc.OpenFoodJournal`) |
| State Pattern | `@Observable` + `@Environment` injection (no singletons) |
| Bundle ID | `k3vnc.OpenFoodJournal` |
| Build System | Xcode (xcodebuild), no SPM dependencies |
| AI Backend | Direct Gemini REST API (BYOK — user provides own API key, stored in Keychain) |
| App Entry | `MacrosApp` in `OpenFoodJournalApp.swift` |

## Architecture Overview

```
MacrosApp (creates ModelContainer w/ CloudKit + 4 @Observable services)
  └─ ContentView (4-tab TabView)
       ├─ Journal tab → DailyLogView (WeeklyCalendarStrip, macro summary, meal sections, RadialMenuButton)
       ├─ Food Bank tab → FoodBankView (searchable, sortable saved food list, swipe-to-edit, "+" menu: Scan/Manual/Search OFF)
       ├─ History tab → HistoryView (CalendarGridView with progress rings, MacroChartView, macro cards → NutritionDetailView)
       └─ Settings tab → SettingsView (goals, health, data export)
```

**Radial FAB**: DailyLogView uses `RadialMenuButton` — a "+" icon at bottom center that fans out Scan / Manual / Containers / Food Bank in an upper semicircle (210°–330°). Supports tap-to-toggle and drag-to-action. Containers are accessed from here instead of a separate tab.

**Service injection**: All services (`NutritionStore`, `ScanService`, `HealthKitService`, `UserGoals`, `OpenFoodFactsService`) are created in `MacrosApp.init()` and passed via `.environment()`. Views consume them with `@Environment(ServiceType.self)`. `SyncService` was removed — CloudKit handles sync natively via `ModelConfiguration(cloudKitDatabase:)`.

**Sheet management**: `DailyLogView` uses a single `DailyLogSheet` enum with `.sheet(item:)` — never multiple booleans.

## Data Models

See [references/models.md](references/models.md) for full property lists.

- **`DailyLog`** — `@Model`, keyed by `date` normalized to midnight (no `@Attribute(.unique)` — CloudKit can't enforce uniqueness; app-level dedup in `fetchOrCreateLog(for:)`). Owns `[NutritionEntry]?` (optional for CloudKit) via cascade delete. Uses `safeEntries` computed property for reads.
- **`NutritionEntry`** — `@Model`, stores core macros (cal/protein/carbs/fat) + dynamic `micronutrients: [String: MicronutrientValue]` + brand/serving/servingCount/servingQuantity/servingUnit/servingMappings. `@Attribute(.externalStorage)` on `sourceImage`.
- **`SavedFood`** — `@Model`, reusable food template in Food Bank. Same fields as NutritionEntry minus meal/log context. Includes `lastUsedAt: Date` (defaults to `createdAt`) for "Last Used" sorting. Created from entries, manual input, or directly from ManualEntryView's "Add to Journal & Food Bank" action.
- **`TrackedContainer`** — `@Model`, weight-based container tracking. Snapshots food nutrition at creation time. Start weight → final weight → derived consumption via `consumedServings` math.
- **`UserGoals`** — `@Observable @MainActor`, uses `@ObservationIgnored @AppStorage` for each goal property to avoid property-wrapper conflicts.
- **`Preferences`** — `@Model`, singleton row for UI customization. Stores `ringSlot1..5` (nutrient IDs for MacroSummaryBar configurable rings). `Preferences.current(in:)` static factory fetches-or-creates the singleton. Synced to Turso via `GET/PUT /api/preferences`. Added to `ModelContainer` in app init. Sheets use `@Bindable var prefs: Preferences` for direct binding.
- **`MealType`** — enum: `.breakfast`, `.lunch`, `.dinner`, `.snack`
- **`ScanMode`** — enum: `.label`, `.foodPhoto`, `.barcode`, `.manual`
- **`ServingSize`** — enum: `.mass(grams:)`, `.volume(ml:)`, `.both(grams:ml:)`. Stores canonical SI values. Has `availableUnits: [String]` (dimension-appropriate unit list), `convert(_:from:to:) -> Double?` (handles same-dimension and cross-dimension via density for `.both`). Static tables: `massConversions` (g/oz/kg/lb), `volumeConversions` (mL/cup/tbsp/tsp/fl oz/L). `type: String` returns "mass"/"volume"/"both" for JSON serialization.
- **`ServingMapping`** — Codable struct with `from: ServingAmount` / `to: ServingAmount` for per-food unit conversions (e.g. 1 cup = 244g). Legacy field kept alongside `ServingSize`.
- **`MicronutrientValue`** — Codable struct with `value: Double` / `unit: String` for dynamic micronutrient storage

## Services

See [references/services.md](references/services.md) for full API contracts.

- **`NutritionStore`** — SwiftData CRUD. `log()`, `fetchLog()`, `fetchLogs()`, `delete()`, `saveEntry()`, `exportCSV()`. Pure local operations — CloudKit sync is handled automatically by SwiftData's `ModelConfiguration(cloudKitDatabase:)`. No sync service reference, no fire-and-forget Tasks.
- **`ScanService`** — Resizes images to max 2000px (UIGraphicsImageRenderer) then JPEG 0.90 before direct Gemini REST API call (`generativelanguage.googleapis.com`) → `NutritionEntry` (not yet inserted). Uses `GeminiModelConfig` static configs: `.labelScan` (gemini-3.1-flash-lite-preview, MINIMAL thinking) and `.foodPhotoScan` (gemini-3.1-pro-preview, HIGH thinking). Includes automatic fallback to gemini-2.5-flash/pro on 500/503 errors. Loads API key from `KeychainService`. User reviews in `ScanResultCard` before committing. Logs scan duration via `ContinuousClock` and stores it on `NutritionEntry.scanDurationMs`.
- **`KeychainService`** — Static helper for secure Keychain storage (Security framework). Stores Gemini API key under service `k3vnc.OpenFoodJournal`, account `gemini-api-key`. Methods: `save(_:for:)`, `load(for:)`, `delete(for:)`, `hasGeminiAPIKey`, `geminiAPIKey`.
- **`ServingConverter`** — Pure-value struct encapsulating all serving-unit conversion math. 4-strategy `factorFor(_:)` (ServingSize tables → direct mapping → chain → SI bridge), `availableUnits`, and `scaledCalories/Protein/Carbs/Fat`. Used by both `EditEntryView` and `LogFoodSheet` to eliminate duplicate conversion logic.
- **`HealthKitService`** — Opt-in Apple Health writes (one `HKQuantitySample` per macro). Reads `activeEnergyBurned`.- **`OpenFoodFactsService`** — Text search and barcode lookup against the Open Food Facts REST API. Search uses `search.openfoodfacts.org` (Elasticsearch-backed, the v1 CGI endpoint returns 503). Barcode lookup uses `world.openfoodfacts.org/api/v2/product/{code}`. Batch-fetches full product details after search using `withTaskGroup`. `OFFProduct` model stores full nutrition. `lookupBarcode()` manages UI state (isLoading/errorMessage); internal `fetchProductByBarcode()` is stateless for batch use. Used by both `OpenFoodFactsSearchView` (text search) and `ScanCaptureView` (barcode camera scan).- **`UserGoals`** — Daily targets for cal/protein/carbs/fat, persisted in UserDefaults.

## View Map

See [references/views.md](references/views.md) for detailed view hierarchy and notable patterns.

## Scan Flow (Core Value Prop)

```
User taps Scan → CameraController (AVCaptureSession) → JPEG
  → Prompt overlay: food photo shows text input, label scan skips prompt
  → ScanService.scan(image, mode) → loads API key from KeychainService
  → Builds JSON request with base64-encoded image + prompt
  → POST to https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}
  → ContinuousClock measures full round-trip duration
  → Label mode: gemini-3.1-flash-lite-preview (fast, MINIMAL thinking)
  → Food photo mode: gemini-3.1-pro-preview (HIGH thinking for estimation)
  → Fallback on 500/503: gemini-2.5-flash (labels) / gemini-2.5-pro (food photos)
  → Parses last text part (skips thinking parts) → JSON → GeminiNutritionResponse
  → GeminiNutritionResponse → NutritionEntry (NOT inserted yet)
  → Entry gets scanDurationMs set from ContinuousClock measurement
  → ScanResultCard (editable, shows duration badge) → User taps "Add to Journal"
  → NutritionStore.log(entry, to: date) → SwiftData insert (CloudKit syncs automatically)
  → Auto-creates SavedFood in Food Bank
  → HealthKitService.write(entry) if enabled
```

## Barcode Scan Flow

```
User taps "Scan Barcode" card → CameraController (AVCaptureSession) → JPEG
  → promptOverlay: "Look Up" button (no text prompt for barcode mode)
  → Vision VNDetectBarcodesRequest detects barcode from photo
  → OpenFoodFactsService.lookupBarcode(barcodeValue)
  → GET https://world.openfoodfacts.org/api/v2/product/{code}?fields=...
  → OFFProduct → ManualEntryView(defaultDate:, prefillProduct:)
  → User reviews/edits pre-filled nutrition data → saves to journal
```

## Open Food Facts Search Flow

```
User taps "Search Open Food Facts" in Food Bank "+" menu
  → OpenFoodFactsSearchView (searchable, Enter-only via .onSubmit)
  → GET https://search.openfoodfacts.org/search?q={query}&fields=...&page_size=25
  → Returns barcodes → batch-fetch full products via withTaskGroup
  → OFFProductRow (styled like SavedFoodRowView — macros, calories, serving)
  → Tap row → ManualEntryView(defaultDate:, prefillProduct: product)
  → User reviews/edits pre-filled data → saves to journal
```

## CloudKit Sync Architecture (app-store branch)

```
iOS App (SwiftData + CloudKit)
  ←→ iCloud Private Database (automatic, free, multi-device)

  → ScanService → Direct Gemini REST API (BYOK, zero server dependency)
  → API key stored in iOS Keychain via KeychainService
```

**Strategy**: SwiftData's `ModelConfiguration(cloudKitDatabase: .private("iCloud.k3vnc.OpenFoodJournal"))` handles all sync automatically. No sync code in the iOS app. Zero server maintenance for data operations.

**CloudKit requirements enforced on all models**:
- All stored properties have defaults (including fully qualified enum defaults: `MealType.snack` not `.snack`)
- No `@Attribute(.unique)` (CloudKit can't enforce uniqueness)
- Relationships are optional (`var entries: [NutritionEntry]? = []`)
- No `.deny` delete rules

**Entitlements**: `OpenFoodJournal.entitlements` includes iCloud (CloudKit), Push Notifications (aps-environment), background mode (remote-notification).

**Data migration**: TursoMigrationView was deleted — CloudKit replaced Turso and the migration tool is dead code. All data now syncs via CloudKit Private Database automatically.

**Server**: Express.js on Render — exists in repo for `main` branch usage but is NOT used by the `app-store` branch at all. The iOS app calls Gemini REST API directly (BYOK). No server dependency.

**Turso migration pattern** (`server/db.js`): Use `PRAGMA table_info(table_name)` to check existing columns before running `ALTER TABLE ... ADD COLUMN`. Idempotent on re-deploy. Example:
```javascript
const info = await db.execute("PRAGMA table_info(nutrition_entries)");
const cols = info.rows.map(r => r.name);
if (!cols.includes("serving_type")) {
  await db.execute("ALTER TABLE nutrition_entries ADD COLUMN serving_type TEXT");
  // ...
}
```

**Server tables**: `daily_logs`, `nutrition_entries`, `saved_foods`, `tracked_containers`, `user_goals` — schema in `server/db.js`.

**API endpoints** (mounted at `/api`):
- `GET /api/sync?since=ISO_TIMESTAMP` — Full or incremental data pull
- `POST/GET/PUT/DELETE /api/entries`, `/api/foods`, `/api/containers`
- `GET/PUT /api/goals`
- Entries auto-create their parent `daily_log` on POST

**Sync integration points** — CloudKit sync is fully automatic. No per-view sync calls needed. All SwiftData mutations are automatically pushed to CloudKit.

**Environment vars** (Render): `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN` (falls back to `file:local.db` for dev)

## Known Gotchas

1. **`xcodebuild` is stricter than Xcode IDE** — missing `import SwiftData` may compile in previews but fail in CLI builds. Always verify with `xcodebuild`.
2. **`.easeInOut` is a static property** — don't write `.easeInOut(value:)`. The `value:` belongs to `.animation(_:value:)`.
3. **Ternary type mismatch** — `.primary` is `HierarchicalShapeStyle`, `.orange` is `Color`. Use `Color.primary` to unify.
4. **`@ObservationIgnored` on `@AppStorage`** — required in `UserGoals` to avoid double-wrapper conflict. Every new `@AppStorage` property needs it.
5. **`private` enum across structs** — `private` scopes to the type, not the file. Use `fileprivate` for shared-file enums.
6. **`ModelContainer(for:configurations:)`** — not `schema:`. The `Schema` wrapper is only for migrations.
7. **Swift named parameters must be in declaration order** — adding a new `init` parameter doesn't let you put it anywhere in call sites. Reorder both the declaration *and* all call sites to match. Build will catch mismatches.
8. **`PRAGMA table_info()` not `IF NOT EXISTS` for ALTER TABLE** — SQLite doesn't support `ALTER TABLE ADD COLUMN IF NOT EXISTS`. Use PRAGMA to check first.
9. **`servingQuantity`/`servingUnit` must be set after scaling in LogFoodSheet** — `toNutritionEntry()` copies the food template's serving values; after scaling macros in logButton, write `entry.servingQuantity = quantity` and `entry.servingUnit = selectedUnit` so EditEntryView opens with the correct baseline.
10. **`.swipeActions` is silently ignored outside a `List`** — it does nothing in `LazyVStack`, `ScrollView`, or `VStack`. If swipe actions don't fire, check that the `ForEach` is inside a `List`. The modifier compiles without error regardless of container.
11. **Smooth tappable List rows with swipeActions: use `Button + .buttonStyle(.plain)`** — Default `Button` style causes ~150ms tap disambiguation delay. `onTapGesture + contentShape(Rectangle())` eliminates tap delay but makes swipes choppy (TapGesture blocks swipe tracking). The correct pattern is `Button { } label: { YourRowView() }.buttonStyle(.plain)` — UIKit-optimized for List swipe coexistence, smooth on both taps and swipes.
12. **ZStack gesture priority** — in a `ZStack`, the **last** (top) view receives gestures first. Put a `Color.clear.contentShape(Rectangle()).onTapGesture { dismiss() }` layer **before** the overlay content to create an outside-tap dismiss. Views on top intercept taps; the clear layer catches everything that falls through.
13. **`Color.clear` needs `.contentShape(Rectangle())`** — transparent views have no hit-test area by default. Without `contentShape`, taps pass through as if the view doesn't exist.
14. **`@Model` enum defaults must be fully qualified** — `var mealType: MealType = .snack` fails during macro expansion. Use `MealType.snack`. The error message is unhelpful (just says macro expansion failed).
15. **CloudKit optional relationships need `safeEntries` pattern** — `var entries: [NutritionEntry]? = []` requires unwrapping everywhere. Add `var safeEntries: [NutritionEntry] { entries ?? [] }` and use that for reads. Use `log.entries?.append(entry)` for writes.
16. **`KnownMicronutrient.Category` cases are `.vitamin`/`.mineral`** — not `.vitamins`/`.minerals`. The enum raw values are plural ("Vitamins"/"Minerals") but the Swift case names are singular.

## What's New Sheet Pattern

`WhatsNewSheet` is version-gated via `@AppStorage("lastSeenVersion")` in `ContentView`. On appear, if `lastSeenVersion != currentVersion` (from `CFBundleShortVersionString`), the sheet is presented. On dismiss, `lastSeenVersion` is updated. To add features for a new version, edit `WhatsNewSheet.swift` and bump the version header text. Each feature is a `FeatureRow(icon:, color:, title:, description:)`.

**v1.1 features**: Open Food Facts search, barcode scanning, faster food photo scans (lite model default), reorderable nutrient rings, nutrition history navigation (day/week/month with date picker).

## Entitlements (app-store branch)

Already configured in `OpenFoodJournal.entitlements`:
- `com.apple.developer.icloud-services`: CloudKit
- `com.apple.developer.icloud-container-identifiers`: iCloud.k3vnc.OpenFoodJournal
- `aps-environment`: development (auto-switches to production on Archive)
- `UIBackgroundModes`: remote-notification

**Still needed** (must add to entitlements):
- `com.apple.developer.healthkit` (HealthKit usage compiles but entitlement missing)

**Still needed** (provisioning profile):
- Enable iCloud + Push Notifications capabilities in Apple Developer portal
- Regenerate provisioning profile

## Branches

- **`main`** — Original Turso sync architecture. `SyncService.swift` present, all views have fire-and-forget sync Tasks. Used for developer's personal Turso instance.
- **`app-store`** — CloudKit sync, no Turso dependency. `SyncService.swift` deleted, all sync Tasks removed. `TursoMigrationView` for one-time data import. This is the App Store submission branch.

## Conventions

- **Comments**: Explain *why*, not *what*. Entry-level devs should understand each function's purpose.
- **File creation**: Build large files in small chunks to avoid network errors.
- **Retrospectives**: Live in `docs/`. Update when later fixes change the story.
- **Skills**: This file is the project skill. Update it when architecture or requirements change.
- **Commits**: Descriptive messages. Push after every significant change.

**DailyLogView container**: Uses a `List` (not ScrollView+LazyVStack) with `.listStyle(.plain)` + `.scrollContentBackground(.hidden)`. `WeeklyCalendarStrip` and `MacroSummaryBar` are plain List rows with `listRowBackground(Color.clear)` + `listRowSeparator(.hidden)`. Meal sections use `MealSectionView` which returns a `Section{}` that becomes a proper sticky List section header in a List context. All swipe actions are on the `MealSectionView` Button wrapper (not on `EntryRowView`).

**RadialMenuButton**: Option bubbles support direct `.onTapGesture` (as well as drag-to-select). A `Color.clear.contentShape(Rectangle()).ignoresSafeArea()` layer behind `GlassEffectContainer` dismisses the menu when tapping outside. The layer is only inserted into the ZStack when `isOpen == true`. Option label text has a subtle drop shadow for legibility over light/glass backgrounds.

**Swipe mappings**:
- `FoodBankView` row: trailing (swipe left) = Edit (blue) + Delete (red, no full-swipe); leading (swipe right) = Add to journal (green)
- `MealSectionView` row: trailing (swipe left) = Delete; leading (swipe right) = Edit — both on the outer Button wrapper (never on `EntryRowView` to avoid double-registration gesture lag)

**FoodNutrientBreakdownView**: Inverse of `NutrientBreakdownView` — shows all nutrients (macros + micros) for a specific food across the selected period. Accessed by tapping a food row in NutrientBreakdownView's "By Food" section.

**EditEntryView**: Has full serving-mappings section (same as LogFoodSheet). Uses shared `AddServingMappingSheet` (defined in LogFoodSheet.swift, internal not private). `addMapping()` calls `nutritionStore.saveEntry(entry)`.

## Current State (Last Updated: 2026-04-02)

- **Branch: `app-store`** — CloudKit migration complete, all Turso sync code removed
- App structure complete: all models, services, and views implemented
- 4-tab layout: Journal, Food Bank, History, Settings (Containers accessed via RadialMenuButton)
- Builds successfully with `xcodebuild` (generic/platform=iOS, signing disabled)
- SwiftData + CloudKit Private Database for data persistence and sync
- Render proxy deployed at `openfoodjournal.onrender.com` (Gemini scan proxy only)
- Food Bank: save foods from scan/manual entry, browse/search/sort, log to journal
- **Open Food Facts integration**: search 4M+ products, add to journal/food bank, debounced search, per-serving nutrition
- **Food Bank "+" toolbar menu**: Search Open Food Facts, Manual Entry (replaces empty-state-only guidance)
- **Settings: OFF contribute toggle** (`off.contributeEnabled`, default off) in Integrations section
- Container Tracking: create from Food Bank food, enter start weight, complete with final weight
- Serving Mappings: per-food unit conversions, editable in EditEntryView
- **NutritionDetailView macro cards**: circular progress rings (not linear ProgressView), showing value inside ring + percentage below
- **FoodNutrientBreakdownView**: inverse of NutrientBreakdownView — food → all nutrients. NavigationLink from NutrientBreakdownView "By Food" rows
- **LogFoodSheet editable micronutrients**: collapsible DisclosureGroup with editable text fields for each micronutrient, values applied at log time
- **Radial menu text shadow**: option labels have `.shadow()` for legibility over glass
- **Swipe gesture lag fix**: swipe actions consolidated on MealSectionView Button wrapper (removed from EntryRowView), SavedFoodRowView has `.contentShape(Rectangle())`, EntryRowView uses static DateFormatter
- WeeklyCalendarStrip: horizontally scrollable week strip with momentum snapping
- Comprehensive micronutrient tracking: 30 FDA nutrients with daily values
- Entitlements configured: iCloud (CloudKit), Push Notifications, Camera, HealthKit descriptions
- BYOK Gemini integration: direct REST API calls, no server proxy needed
- KeychainService for secure API key storage
- Onboarding flow: 6 pages (Welcome → API Key → Goals → Camera → Radial Menu Tutorial → HealthKit)
- RadialMenuDemo: pure SwiftUI phase-based animation teaching press-and-drag gesture (in onboarding page 4)
- Settings: API key management section (save/delete/change key), "Show Onboarding" replay button, "Sources & Disclaimers" link
- **App Store Guideline 1.4.1 compliance**: HealthDisclaimerView with FDA citations (21 CFR §101.9), AI estimation disclaimers, Atwater system citation, and general medical disclaimer. Inline citations on NutritionDetailView, ScanResultCard, and GoalsEditorView.
- App Store audit complete: HealthKit entitlement, Privacy Policy, PrivacyInfo.xcprivacy, AGPL→MIT licensing
- sourceImage removed from NutritionEntry and SavedFood (was stored but never displayed)
- TursoMigrationView deleted — CloudKit replaced Turso, migration tool is dead code
- No unit tests beyond Xcode template stubs

## App Store Submission Notes

**First submission rejected (Guideline 1.4.1 — Physical Harm)**: App provided health/nutrition data without citations. Fixed by adding `HealthDisclaimerView` (Settings → Sources & Disclaimers) with FDA Daily Values links, Atwater system reference, AI estimation disclaimer, and general medical disclaimer. Inline citations added to NutritionDetailView, ScanResultCard, and GoalsEditorView.

**Other audit findings to address before next submission:**
- README.md describes `main` branch architecture (Turso/Express), not `app-store` branch. Update README or add branch-specific note.
- Reviewer notes previously contained false HealthKit claim ("data is never read") — corrected to list all read/write types.
- `server/` directory and `render.yaml` are dead code on `app-store` branch — reviewers clicking the GitHub link may be confused.
- AGPL-3.0 license has App Store exception in LICENSE_NOTICE.md — Apple may or may not flag this.
- Privacy policy is web-only (GitHub link) — fails offline. Consider embedding a copy in-app.

## Planned Work (Backlog)

### UX / Feature Improvements

- **Weekly/monthly view should display daily averages** — In `NutritionDetailView`, when `selectedPeriod` is `.weekly` or `.monthly`, `macroTotals` currently accumulates totals. For multi-day periods, display the **daily average** (total ÷ days in period) so "14,000 kcal this week" becomes "2,000 kcal/day avg". The period picker label should reflect this ("Weekly Avg", "Monthly Avg"). Same applies to the `comparisonCard` values in `HistoryView.weekComparisonSection` (already divides by 7 — verify `.monthly` path does the same).

### Open Food Facts Integration

- **Open Food Facts (OFF)** is a free, open database of 4M+ food products. Integrated into the Food Bank for searching and adding foods without scanning.
- **Service**: `OpenFoodFactsService` — `@Observable @MainActor` service for OFF REST API calls (text search + barcode lookup). Injected via `.environment()` from `MacrosApp`.
- **API endpoints used**:
  - **Text search**: `GET https://search.openfoodfacts.org/search?q={query}&fields=product_name,brands,code&page_size=25` — dedicated Elasticsearch-backed search service (the legacy v1 CGI endpoint returns 503)
  - **Barcode/product lookup (v2)**: `GET https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=...` — full nutrition data
  - **Two-step flow**: Search returns lightweight hits (name, brand, code via `OFFSearchHit`); tapping a result fetches full nutrition via barcode lookup → `OFFProduct`
  - **Fields requested** (for product detail): `product_name,brands,nutriments,serving_size,serving_quantity,code`
  - **Nutriments mapping**: `energy-kcal_100g` → calories, `proteins_100g` → protein, `carbohydrates_100g` → carbs, `fat_100g` → fat, plus micronutrients (fiber, sugar, sodium, etc.)
  - **User-Agent**: `OpenFoodJournal/1.0 (openfoodjournal@example.com)` — required by OFF API policy
  - **Rate limits**: 10 req/min for search, 100 req/min for product reads
  - **No auth required** for reads; writes (contribute) require OFF account credentials
- **UI access points**:
  - **FoodBankView toolbar**: "+" button (leading of sort button) → Menu with 3 options: Scan, Manual Entry, Search Open Food Facts
  - **Scan** and **Manual Entry** reuse existing sheets (`ScanView` via DailyLogSheet, `ManualEntryView`)
  - **Search Open Food Facts** opens `OpenFoodFactsSearchView` — debounced text input, paginated results, tap to review details
  - **Result action**: Same pattern as ManualEntryView — "Add to Journal" or "Add to Journal & Food Bank" via toolbar Menu
- **Settings**: `@AppStorage("off.contributeEnabled")` toggle (default: `false`) in SettingsView. When enabled, scanned nutrition data is submitted back to OFF after the user logs it. Write API uses `POST /cgi/product_jqm2.pl` with user credentials.
- **Data flow**: OFF search result → `OFFProduct` struct (Codable) → converted to `NutritionEntry` / `SavedFood` with `scanMode: .manual` and brand preserved. Nutrition values from OFF are per-100g; conversion to serving-based values uses `serving_size` field when available.
- **No SPM dependency**: Direct `URLSession` calls, no OFF Swift SDK imported (keeps zero-dependency architecture).
