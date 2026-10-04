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
| Data Layer | SwiftData (`@Model`) + CloudKit Private Database (`iCloud.k3vnc.OpenFoodJournal`) + optional push-only Turso mirror |
| State Pattern | `@Observable` + `@Environment` injection (no singletons) |
| Bundle ID | `k3vnc.OpenFoodJournal` |
| Build System | Xcode (xcodebuild), no SPM dependencies |
| Build Verify Command | `xcodebuild -project OpenFoodJournal.xcodeproj -scheme OpenFoodJournal -destination generic/platform=iOS build` |
| Build Notes | No iOS simulators installed. Use `generic/platform=iOS` for compile-only verification. Physical device (iPhone 18,3) available when connected. Device support symbols at `/Volumes/DevDisk/Developer/Xcode/iOS DeviceSupport/`. |
| Release Automation | GitHub `macos-26` cloud CI pinned to stable Xcode 26.6; `testflight` builds once and uploads internally; protected external TestFlight and `app-store` workflows promote the exact tested build without rebuilding |
| AI Backend | BYOK direct AI calls: Gemini, OpenRouter, Azure OpenAI, OpenAI, Anthropic, Muse Spark, or any OpenAI-compatible endpoint (custom base URL + key, e.g. Meta Model API / LiteLLM / self-hosted vLLM) for Assistant; Gemini/OpenRouter/OpenAI-compatible for Scan; food icon images via Gemini or an OpenAI-compatible `/images/generations` endpoint (e.g. Muse Image, selected by `foodBank.iconImageProvider`); native, Tavily, Parallel, or Exa research |
| App Entry | `MacrosApp` in `OpenFoodJournalApp.swift` |

## Architecture Overview

```
MacrosApp (creates ModelContainer w/ CloudKit + @Observable services)
  └─ ContentView (4-tab TabView)
       ├─ Journal tab → DailyLogView (selected month/year title, WeeklyCalendarStrip, macro summary, meal sections, RadialMenuButton)
       ├─ Food Bank tab → FoodBankView (searchable, sortable active saved food list, swipe-to-archive/edit, "+" menu: Composite/Nutrition Calculator/Search OFF/Manual/Archive)
       ├─ History tab → HistoryView (CalendarGridView with progress rings, MacroChartView, macro cards → NutritionDetailView)
       └─ Assistant tab → ChatView (streaming AI chat over nutrition data, persistent CloudKit-synced threads)

Journal's top-right Settings toolbar control pushes `SettingsView` on the Journal
`NavigationStack`. Settings is intentionally not a persistent root tab.
```

**Radial FAB**: DailyLogView uses `RadialMenuButton` — a "+" icon at bottom center that fans out Scan / Manual / Containers / Food Bank in an upper semicircle (210°–330°). Supports tap-to-toggle and drag-to-action. Containers are accessed from here instead of a separate tab.

**Service injection**: All services (`NutritionStore`, `ScanService`, `ChatService`, `TursoMirrorService`, `HealthKitService`, `UserGoals`, `MealTimeSettings`, `OpenFoodFactsService`) are created in `MacrosApp.init()` and passed via `.environment()`. Views consume them with `@Environment(ServiceType.self)`. `SyncService` was removed — CloudKit handles sync natively via `ModelConfiguration(cloudKitDatabase:)`; Turso is an optional push-only mirror, not a source of truth.

**Sheet management**: `DailyLogView` uses a single `DailyLogSheet` enum with `.sheet(item:)` — never multiple booleans.

## Data Models

See [references/models.md](references/models.md) for full property lists.

- **`DailyLog`** — `@Model`, keyed by `date` normalized to midnight (no `@Attribute(.unique)` — CloudKit can't enforce uniqueness; app-level dedup in `fetchOrCreateLog(for:)`). Owns `[NutritionEntry]?` (optional for CloudKit) via cascade delete. Uses `safeEntries` computed property for reads.
- **`NutritionEntry`** — `@Model`, stores core macros (cal/protein/carbs/fat) + dynamic `micronutrients: [String: MicronutrientValue]` + brand/serving/servingCount/servingQuantity/servingUnit/servingMappings + optional `selectionSummary` for generated calculator builds. Includes HealthKit sync metadata (`healthKitSyncStatus`, `healthKitSyncedAt`, `healthKitSyncVersion`, `healthKitLastError`, `healthKitLastWriteHash`) so Apple Health writes are idempotent.
- **`SavedFood`** — `@Model`, reusable food template in Food Bank. Same fields as NutritionEntry minus meal/log context. Includes optional `emoji: String?` plus optional generated icon image data/mime/update/prompt for the Food Bank icon, `kind: SavedFoodKind` (`.single`/`.composite`/`.calculator`), `compositeIngredients: [CompositeIngredientSnapshot]`, `calculatorIngredients: [CalculatorIngredient]`, `isOnShelf: Bool`, `lastUsedAt: Date` (defaults to `createdAt`) for "Last Used" sorting, and `archivedAt: Date?` for manual cosmetic archive state. Composite ingredients are copied snapshots, never live `SavedFood` references, so editing a composite only affects future logs. Nutrition calculators are also saved-food rows: flat ingredient/portion value snapshots, not SwiftData relationship trees. Foods auto-archive cosmetically when `lastUsedAt` is more than 14 days old unless `isOnShelf` is true; manual archive always wins. Archived foods stay in SwiftData, remain searchable, and can be browsed from Food Bank "+" → Archive.
- **`TrackedContainer`** — `@Model`, weight-based container tracking. Snapshots food nutrition at creation time. Start weight → final weight → derived consumption via `consumedServings` math.
  - `Enter Weight` creates a long-running active container whose later gross-weight delta is logged on completion. `Use Tare` is intentionally different: empty-container plus loaded-container measurements resolve immediately to a gram-based journal entry and do not create an active container.
  - Active tare records created by earlier 1.4 builds remain compatible: optional `tareWeight` persists through CloudKit/backup/Turso, completion rejects weights below the stored tare, and initial/remaining food calculations remain available. New `Use Tare` actions log immediately instead of creating another active tare record.
  - `NewContainerSheet` prefills the editable start-weight field from the last completed `finalWeight` for the same `SavedFood`, so continuing the same physical container does not require re-entering that weight.
  - The container food picker sorts all saved foods by most recent container activity first, then alphabetically for foods that have never been tracked.
  - `NewContainerSheet(preselectedFood:)` is the shared quick-start path. Completed container rows resolve `savedFoodID` and open it directly; missing/deleted Food Bank links show an alert instead of reconstructing a food from the nutrition snapshot.
- **`GeminiScanLog` / `ChatDiagnosticSpan`** — Legacy `@Model` compatibility shells retained so existing CloudKit rows can decode and migrate. New detailed AI diagnostics are never inserted into SwiftData/CloudKit. `AIDiagnosticEvent` normalizes redacted scan, Assistant, and external-research telemetry for append-only Turso writes; it omits prompts, answers, journal/HealthKit values, source URLs/content, attachments, raw provider bodies, and chain-of-thought. Legacy rows upload once and are deleted locally only after Turso acknowledges them.
- **`AIDiagnosticOutboxStore`** — Bounded local-only delivery queue for Turso diagnostic writes (500 events, 2 MiB, 48 hours). It is excluded from backup, uses file protection, removes acknowledged UUIDs immediately, and is not a diagnostic history.
- **`GeminiCostAccumulator`** — `@Model`, singleton-style local running total of estimated Gemini token cost. Accumulates input/output/thinking tokens, request counts, success/failure counts, grounded AI Search prompt count, last model/cost, and total estimated USD. Estimates use Gemini/OpenRouter usage metadata plus local Google Standard paid-tier rates checked 2026-06-30. Food icon image generation uses reported Gemini image output tokens when available, falling back to the documented 1K-image equivalent if usage metadata is absent. Google Search grounding fees are not included because Gemini does not return billable search-query count.
- **`UserGoals`** — `@Observable @MainActor`, uses `@ObservationIgnored @AppStorage` for each goal property to avoid property-wrapper conflicts.
- **`MealTimeSettings`** — `@Observable @MainActor`, uses `@ObservationIgnored @AppStorage` for configurable meal boundaries. Defaults are Breakfast 2:00 AM–12:00 PM, Lunch 12:00 PM–6:00 PM, Dinner 6:00 PM–2:00 AM. Logging flows call `mealTimeSettings.mealType()` using `Calendar.autoupdatingCurrent`, so the default meal is based on the device's local time zone at log time, not UTC. Snack remains a manual override.
- **`Preferences`** — `@Model`, singleton row for UI customization. Stores `ringSlot1..5` (nutrient IDs for MacroSummaryBar configurable rings) plus Shelf enablement, top-N count (clamped 1...5), calorie trigger fraction, incomplete-nutrition policy, separate energy intent (`Cut`/`Maintain`/`Bulk`/`Custom`) and nutrition emphasis (`Balanced`/`Protein Focus`/`Fiber Focus`/`Low Sodium`/`Custom`), rolling-week context, optional calorie/sodium hard caps, and custom per-nutrient policy + strength. Defaults are enabled, top 3, Maintain, Balanced, 50%, rolling context on, hard caps off, and Include Cautiously. Legacy style/flexibility/role fields remain for additive CloudKit/backup compatibility and seed the new nutrition emphasis when a new value is absent. `Preferences.current(in:)` static factory fetches-or-creates the singleton. Included in optional Turso mirroring as the `ofj_preferences` row. Added to `ModelContainer` in app init. Sheets use `@Bindable var prefs: Preferences` for direct binding.
- **Assistant persistence models** — `ChatThread`, `ChatMessage`, and `ChatAttachment` retain the complete CloudKit-safe transcript and user uploads. `ChatToolRecord` preserves provider call IDs, Gemini thought signatures, model-turn grouping, arguments/results, status, and chip summaries. `ChatProviderContinuation` stores provider-specific opaque continuation items (including Azure encrypted reasoning) with their original turn ID and ordinal. `ChatContextCheckpoint` is the validated provider-neutral summary used after compaction; `ChatSourceArtifact` versions durable web/HTML/PDF/image evidence; `ChatAgentRun` and `ChatToolExecution` persist recovery and write-tool idempotency state. Compaction never deletes or rewrites original messages or attachments. Production threads request a short title from the selected Assistant provider after the first completed reply; title requests contain only clipped user/model text, expose no tools or attachments, and enter usage/cost accounting. Threads sort by `updatedAt`.
- **`MealType`** — enum: `.breakfast`, `.lunch`, `.dinner`, `.snack`
- **`ScanMode`** — enum: `.label`, `.foodPhoto`, `.barcode`, `.manual`
- **`ServingSize`** — enum: `.mass(grams:)`, `.volume(ml:)`, `.both(grams:ml:)`. Stores canonical SI values. Has `availableUnits: [String]` (dimension-appropriate unit list), `convert(_:from:to:) -> Double?` (handles same-dimension and cross-dimension via density for `.both`). Static tables: `massConversions` (g/oz/kg/lb), `volumeConversions` (mL/cup/tbsp/tsp/fl oz/L). `type: String` returns "mass"/"volume"/"both" for JSON serialization.
- **`ServingMapping`** — Codable struct with `from: ServingAmount` / `to: ServingAmount` for per-food unit conversions (e.g. 1 cup = 244g). Legacy field kept alongside `ServingSize`.
- **`MicronutrientValue`** — Codable struct with `value: Double` / `unit: String` for dynamic micronutrient storage

## Services

See [references/services.md](references/services.md) for full API contracts.

- **`NutritionStore`** — SwiftData CRUD and the canonical journal-mutation boundary. `log()`, `saveEntry()`, `moveEntry()`, and entry/log deletion persist SwiftData first, then automatically schedule the matching idempotent HealthKit sync/delete through an injected `NutritionEntryHealthSyncing` adapter when Apple Health export is enabled. Views, Assistant tools, and future entry-writing surfaces must not call HealthKit separately. `entriesNeedingHealthSync()` drives launch/foreground reconciliation and Settings backfill so interrupted or older-build writes heal from SwiftData. Also provides `fetchLog()`, `fetchLogs()`, `repairDailyLogEntryRelationships()`, `exportCSV()`, `exportBackup()`, and `importBackup()`. CSV is spreadsheet/analytics only. Restore-grade backup uses versioned JSON DTOs in `OpenFoodJournalBackup.swift` and imports idempotently by UUID. Local/iCloud remain source of truth; successful saves schedule the optional Turso mirror when enabled.
- **`ScanService`** — Accepts 1-4 photos for label and food-photo scans. Resizes each image to max 1200px (UIGraphicsImageRenderer), encodes label JPEGs at 0.50 and food-photo JPEGs at 0.80, then sends each photo to the selected AI provider and returns a reviewable `NutritionEntry` (not yet inserted). Direct Gemini uses streamed Interactions SSE (`generativelanguage.googleapis.com/v1beta/interactions`) with `generation_config.thinking_summaries = "auto"` so `step.delta` events with `delta.type == "thought_summary"` update `thinkingTrace`; `delta.type == "text"` is accumulated as final nutrition JSON. OpenRouter uses streamed OpenAI-compatible chat completions (`openrouter.ai/api/v1/chat/completions`) with base64 image content parts, JSON response format, app attribution headers, optional `plugins: [{"id":"web"}]` for AI Search, and optional provider routing to prefer/require `google-vertex`. OpenRouter does not currently drive the Gemini thought-summary UI; it shows a neutral provider wait state and logs stream timing. Gemini may emit only one late thought-summary event for a request; do not fake streaming by delaying the final nutrition sheet just to display that late summary. Also supports Food Bank AI Search, nutrition-calculator OCR import via `extractCalculatorIngredient(named:from:useProModel:)`, sequential Food Bank emoji backfill via `backfillMissingFoodEmojis()`, and direct Gemini Flash Lite image icon generation via `backfillMissingFoodIconImages()` / `generateFoodIconImage(for:force:)`. Direct Gemini uses `gemini-flash-latest` for label/lite/emoji work and `gemini-pro-latest` for Pro food photo scans/search; do not replace these with concrete preview/versioned model slugs unless Google removes the latest endpoints. The icon image endpoint is the concrete `models/gemini-3.1-flash-lite-image` Interactions image model. Its thinking level is a model-specific typed enum (`minimal`/`high`) and production uses `high`; `low` is invalid for this model and must never be copied from text-model configuration. Image output uses top-level polymorphic `response_format`, not legacy `generation_config.image_config` or `response_modalities`. OpenRouter model slugs are runtime-editable in Settings and default to the analogous Google latest aliases. User reviews in `ScanResultCard`, `ManualEntryView`, or `NutritionCalculatorEditorView` before committing. Logs scan/search/OCR/emoji/icon duration via `ContinuousClock`, stores standard scan durations on `NutritionEntry.scanDurationMs`, emits redacted `AIDiagnosticEvent` telemetry to the configured Turso sink, and keeps `GeminiCostAccumulator` usage/cost totals in SwiftData. Stores `lastSubmittedScan` for scan-page/result-sheet redo without recapturing photos.
- **Food Bank AI Search retirement** — `ScanService.searchNutrition` and `.aiSearch` telemetry remain only as backward-compatible legacy plumbing. There is no `AIFoodSearchView`, sheet case, or Food Bank menu entry; Open Food Facts and Assistant research are the supported user-facing search paths.
- **`RuntimeModelCatalog`** — Runtime metadata cache over `https://models.dev/api.json`. It retains Google, OpenRouter, Azure, OpenAI, Anthropic, and Meta records in the app cache directory, honors ETags, refreshes at launch/foreground no more than once per 24 hours, and falls back to the shipped catalog on any failure. Provider adapters capture the concrete model ID returned by each API; alias changes are persisted immediately and force a background refresh. The concrete model drives limits, capabilities, pricing, per-round/daily accounting, and scan estimates while arbitrary Azure deployment identifiers remain request-only routing values. models.dev is never an inference or authentication dependency, and app-owned overrides remain authoritative for streaming, parallel calls, native search, and compaction.
- **`ChatService`** — `@Observable @MainActor` provider-neutral agent loop and app-level run coordinator for the Assistant tab (max 8 model turns/reply). It builds one `ChatModelRequest` transcript and depends on a configured `ChatModelProxy`, so provider additions must stay at the adapter edge. Gemini replays thought signatures and call IDs; OpenAI and Azure share stateless Responses translation with encrypted reasoning items and `store: false`; Anthropic uses Messages/SSE and replays signed thinking blocks plus matching `tool_use_id`; Muse Spark uses Meta Model API Chat Completions at `https://api.meta.ai/v1` with a runtime-editable model slug. Tavily, Parallel, and Exa implement the independent `ChatWebSearchProviding` contract for any conversation model; Exa uses `/search`, `x-api-key`, source text, citations, request IDs, provider-reported latency, and provider-reported request cost. The existing send gate, persisted run phases, suspension/Continue behavior, retry rules, parallel read groups, context compaction, durable sources, exactly-once writes, diagnostics, and cost accounting remain provider-neutral. Food Bank write tools must persist structured `servingQuantity`, `servingUnit`, `ServingSize`, and `ServingMapping` whenever a serving-to-grams fact is known; a display-only string such as `1 serving = 42 grams` is not a conversion contract and must be parsed at the write boundary for backward compatibility.
- **`TursoMirrorService`** — Optional `@Observable @MainActor` direct SQL-over-HTTP integration with a user-provided Turso database. Journal/configuration/usage tables remain push-only generation-pruned mirrors. Detailed AI diagnostics use a separate append-only `ofj_ai_diagnostic_events` table, UUID upserts, 14-day `expires_at`, a bounded local delivery outbox, and no generation pruning. Credentials are Keychain-only (`turso-database-url`, `turso-auth-token`); non-secret status includes mirror and diagnostic-upload timestamps/counts. It never reads Turso into SwiftData as application state; the only read path is an explicit diagnostic CSV export.
- **`ShelfRecommendationEngine`** — Pure deterministic local scorer for Food Bank Shelf foods. It evaluates 0.5x/1x/1.5x/2x servings using human-readable nutrient policies (`Reach`, `Stay Near`, `Try to Avoid`, `Ignore`) and `Gentle`/`Standard`/`Strong` penalty strength, applies curved sodium/limit pressure, portion-size cost, and cautious missing-data penalties, then uses stable score/name/UUID tie-breaking. Policies are soft by default so tradeoffs remain rankable; only explicitly enabled calorie/sodium hard caps eliminate candidates. A guarded rolling context reads the prior six calendar days, requires at least five non-empty positive-calorie logs, estimates one missing day from covered pace, and clamps today's adjustment to ±min(300 kcal, 15% of the normal goal). The Shelf appearance trigger and hard caps always use the unadjusted selected-day goal. It never calls AI or the network.
- **`KeychainService`** — Static helper for secure Keychain storage (Security framework). Stores Gemini, OpenRouter, Azure OpenAI, OpenAI, Anthropic, Muse Spark, Tavily, Parallel, and Exa API keys under dedicated accounts plus optional Turso mirror credentials. Provider choices, research modes, endpoints/deployments, editable model slugs, and context preset are non-secret UserDefaults/backup settings; API keys are never exported. Azure credentials may be attached only after `AzureOpenAIEndpointValidator` accepts the endpoint.
- **`ServingConverter`** — Pure-value struct encapsulating all serving-unit conversion math. 4-strategy `factorFor(_:)` (ServingSize tables → direct mapping → chain → SI bridge), `availableUnits`, and `scaledCalories/Protein/Carbs/Fat`. Used by both `EditEntryView` and `LogFoodSheet` to eliminate duplicate conversion logic.
- **`HealthKitService`** — Opt-in Apple Health sync. Writes calories/macros and every app-tracked dietary nutrient with an iOS 26.2 `HKQuantityTypeIdentifier` as separate `HKQuantitySample`s using deterministic `HKMetadataKeySyncIdentifier` values (`entry.id + nutrient key`). Supported writes include fiber, sugars, sodium, cholesterol, saturated/mono/polyunsaturated fat, vitamins A/C/D/E/K/B6/B12, thiamin, riboflavin, niacin, pantothenic acid, biotin, folate, calcium, iron, magnesium, phosphorus, potassium, zinc, copper, manganese, selenium, chromium, molybdenum, iodine, chloride, water, and caffeine. HealthKit does not expose separate write types for added sugars or trans fat; those stay in OpenFoodJournal only. Micronutrient lookup accepts both canonical IDs (`sodium`, `fiber`, `saturated_fat`) and legacy display-name keys (`Sodium`, `Fiber`, `Saturated Fat`) because historical entries contain both shapes. `NutritionEntry.healthKitWriteHash` includes a HealthKit export schema version so adding write mappings marks older successful exports stale for "Sync Missing Nutrition to Apple Health". Sync deletes only OpenFoodJournal-owned samples for an entry before saving replacements, so retries/edits are idempotent. Settings includes "Sync Missing Nutrition to Apple Health" for incremental stale rows and "Repair Apple Health Nutrition" for a forced historical rewrite when entries were previously marked synced with macro-only writes; forced repair also purges legacy no-sync samples written by this app by matching the entry food name across the affected local day before writing current samples. Reads `activeEnergyBurned`.
- **`OpenFoodFactsService`** — Text search and barcode lookup against the Open Food Facts REST API. Search uses `search.openfoodfacts.org` (Elasticsearch-backed, the v1 CGI endpoint returns 503). Barcode lookup uses `world.openfoodfacts.org/api/v2/product/{code}`. `OFFProduct` model stores full nutrition and exposes `hasUsableNutrition`; text search and barcode lookup filter out zero-calorie/no-nutrition placeholder rows before showing or prefilling them. `lookupBarcode()` manages UI state (isLoading/errorMessage); internal `fetchProductByBarcode()` is stateless for batch use. Used by both `OpenFoodFactsSearchView` (text search) and `ScanCaptureView` (barcode camera scan). Settings has an Open Food Facts contribution status row backed by `off.contributionSuccessCount` and `off.lastContributionAt`; do not treat the contribution toggle itself as proof that a DB write happened.
- **`UserGoals`** — Daily targets for cal/protein/carbs/fat, persisted in UserDefaults.

## View Map

See [references/views.md](references/views.md) for detailed view hierarchy and notable patterns.

## Scan Flow (Core Value Prop)

```
User taps Scan → CameraController (AVCaptureSession) → 1-4 photos
  → Camera view uses exactly three non-glass zoom steps: 0.5×, 1×, and 2×
  → CameraController starts only the physical wide lens; 0.5× swaps to a single ultra-wide input, while 1×/2× share the wide input and 2× applies a 2.0 device factor; never use a virtual multi-camera input
  → Prompt overlay: review thumbnails, optionally add another angle or library photos
  → Food photo shows text input, label scan skips prompt
  → ScanService.scan(images, mode) → loads the selected provider API key from KeychainService
  → Resizes/JPEG-encodes each image and builds either Gemini Interactions image blocks or OpenRouter chat-completion image_url content parts
  → Direct Gemini: POST to https://generativelanguage.googleapis.com/v1beta/interactions with x-goog-api-key header
  → OpenRouter: POST to https://openrouter.ai/api/v1/chat/completions with Authorization bearer header, app attribution headers, and optional Google Vertex provider routing
  → Loading overlay shows scan stage; direct Gemini also shows recent thought-summary deltas (`step.delta` / `delta.type == "thought_summary"`)
  → ContinuousClock measures full round-trip duration
  → Direct Gemini label/lite mode: gemini-flash-latest; Pro mode: gemini-pro-latest
  → OpenRouter uses Settings-editable lite/pro/emoji model slugs, defaulting to analogous Google latest aliases
  → Fallback on transient server failures uses the configured fallback model
  → Accumulates response text → JSON → GeminiNutritionResponse
  → GeminiNutritionResponse → NutritionEntry (NOT inserted yet)
  → Entry gets scanDurationMs set from ContinuousClock measurement
  → ScanResultCard (editable, shows duration badge, can redo previous photos) → User taps "Add to Journal"
  → NutritionStore.log(entry, to: date) → SwiftData insert (CloudKit syncs automatically)
  → Auto-creates SavedFood in Food Bank
  → NutritionStore automatically schedules HealthKitService.sync(entry) if enabled (replaces OpenFoodJournal-owned HealthKit samples by sync identifier)
```

## Barcode Scan Flow

```
User taps "Scan Barcode" card → CameraController (AVCaptureSession) → JPEG
  → promptOverlay: "Look Up" button (no text prompt for barcode mode)
  → Vision VNDetectBarcodesRequest detects barcode from photo
  → OpenFoodFactsService.lookupBarcode(barcodeValue)
  → GET https://world.openfoodfacts.org/api/v2/product/{code}?fields=...
  → OFFProduct (requires calories > 0 and usable nutrition) → ManualEntryView(defaultDate:, prefillProduct:)
  → User reviews/edits pre-filled nutrition data → saves to journal
```

## Open Food Facts Search Flow

```
User taps "Search Open Food Facts" in Food Bank "+" menu
  → OpenFoodFactsSearchView (searchable, Enter-only via .onSubmit)
  → GET https://search.openfoodfacts.org/search?q={query}&fields=...&page_size=25
  → Converts hits to OFFProduct and filters out zero-calorie/no-usable-nutrition rows
  → OFFProductRow (styled like SavedFoodRowView — macros, calories, serving)
  → Tap row → ManualEntryView(defaultDate:, prefillProduct: product)
  → User reviews/edits pre-filled data → saves to journal
```

## Retired Food Bank AI Search

The user-facing `AIFoodSearchView` and Food Bank `+` menu entry were removed in
August 2026. Do not re-add them without a new owner request. Keep legacy
`.aiSearch` diagnostics, persisted counters, and decoding cases so older data
continues to load. Open Food Facts remains the Food Bank's searchable database;
the Assistant retains its separate provider-neutral research tools.

## Food Bank Emoji Flow

```
Settings → Food Bank → Enable Food Icon Generation
  → @AppStorage("foodBank.autoGenerateEmojis") enables icon generation; when generated-image mode is also selected, each newly persisted Food Bank item is queued automatically
  → Optional @AppStorage("foodBank.useGeneratedIconImages") switches the icon target from text emoji to generated images
  → `NutritionStore.addSavedFood(...)` is the canonical creation boundary. After a successful save it notifies `SavedFoodImageGenerationQueuing`; `ScanService` deduplicates IDs and processes them FIFO so additions made during an active generation are not dropped.
  → Toggling either setting must not queue the whole existing Food Bank. Settings → "Generate Missing ..." remains the explicit backfill action, and Food Bank row context-menu generation remains available.
  → Backup restore preserves restored records without automatically spending BYOK image-generation quota.
  → Emoji mode: ScanService.backfillMissingFoodEmojis() fetches all SavedFood rows with empty emoji
  → Image mode: ScanService.backfillMissingFoodIconImages() fetches all SavedFood rows without generated icon image data
  → Processes foods sequentially. Emoji mode uses the selected provider's emoji model and a JSON-only one-emoji prompt; image mode uses direct Gemini `models/gemini-3.1-flash-lite-image` with the Gemini key.
  → CRITICAL model contract: Nano Banana 2 Lite documents exactly `minimal` and `high` thinking levels. Code represents them as `GeminiFlashLiteImageThinkingLevel`; production uses `.high`. Never send `low`. Official source: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image
  → The production payload and the billable TestFlight live contract share `ScanService.foodIconImageRequest(prompt:)`. The payload uses `response_format: {type: image, mime_type: image/jpeg, aspect_ratio: 1:1, image_size: 1K}`. TestFlight must not upload when that exact request fails or returns no image.
  → Image prompts are JSON such as {"Brand":"Tyson","item":"Crispy Chicken Fries"} and omit the Brand key entirely when no brand exists.
  → The image prompt chooses a flat warm off-white background for dark foods and a flat charcoal background for light foods, with no gradient, props, floor, or shadow. The provider still returns JPEG because the concrete Lite endpoint rejects PNG output.
  → `VisionFoodIconForegroundMasker` runs Apple's semantic foreground-instance mask off the main actor, composites real alpha, and persists a compact 160 px PNG. Implausibly empty/full masks or Vision failures fall back to a compact opaque contrast JPEG without another billable request. Do not restore RGB thresholding or border flood fill.
  → Existing transparent PNGs keep alpha during local size optimization; do not flatten them back to white. Raw 1K Gemini bytes are never stored in SwiftData/CloudKit for row icons.
  → Sets SavedFood.emoji or SavedFood.generatedIconImageData only if that target is still missing; automatic backfill skips existing icons and also skips the same prompt/model for one hour after a failure so bad requests do not churn through the whole Food Bank. Context menus can force-regenerate the active icon mode and bypass that recent-failure cache.
  → Writes GeminiScanLog(operation: .foodEmoji or .foodIconImage), updates GeminiCostAccumulator, and schedules optional Turso mirror
  → DEBUG Xcode logs for food icon image generation print the estimated request cost and token counts on the completion line, using the same pricing metadata persisted to GeminiScanLog.
  → SavedFoodRowView shows a circular generated image above calories when image mode is enabled and image data exists; while image mode is enabled but image data is still missing, it shows a neutral photo placeholder rather than falling back to the old emoji.
  → Newly assigned or regenerated generated images animate from SavedFoodRowView using generatedIconImageUpdatedAt: a short scale pulse, diagonal shine, and tiny sparkles pulse. Ordinary row render/scroll should not replay the effect.
  → LogFoodSheet shows the saved food's icon above brand/name: prefer generated image when image mode is enabled and image data exists, otherwise show the saved emoji, with generated image as fallback when no emoji exists.
  → Settings shows the actual generated-image storage footprint from stored SwiftData bytes.
```

## Food Bank Archive Flow

```
Default Food Bank list
  → Shows active foods only (`!SavedFood.isArchivedInFoodBank`)
  → Empty search filters active foods; non-empty search filters all saved foods so archived matches still appear
  → Trailing swipe: Archive/Unarchive + Edit
  → Leading swipe or tap: LogFoodSheet
  → `NutritionStore.log()` refreshes linked SavedFood usage via `savedFoodID` so logged foods update `lastUsedAt` and leave the archive

Food Bank "+" → Archive
  → FoodBankArchiveView lists foods with `archivedAt != nil` or `lastUsedAt` older than 14 days
  → Users can search archived foods, log them, edit them, or unarchive them
  → Unarchive clears `archivedAt` and refreshes `lastUsedAt` so the item becomes visible in the active list
```

## Food Bank Shelf Recommendation Flow

```
Food Bank row context menu or Edit Food → Add to Shelf
  → `SavedFood.isOnShelf = true`; age-based auto-archive is bypassed, but manual archive still excludes the food
  → After today's calories reach the configured trigger (default 50%), Food Bank shows "Good Fits" above the normal list
  → `ShelfRecommendationEngine` evaluates deterministic serving candidates against separate energy intent and nutrition-emphasis policies for calorie, protein, fiber, carb, fat, and sodium goals
  → When enabled and sufficiently covered, the prior six days can adjust today's calorie-ranking target by at most ±300 kcal or ±15%; the 50% appearance trigger and optional hard cap still use the normal daily goal
  → Top results include a plain-language reason and quantity; incomplete nutrients are labeled and conservatively penalized or excluded per Settings
  → Tapping a result opens `LogFoodSheet` with the recommended quantity/unit prefilled and still editable

Settings → Food Bank → Shelf Recommendations
  → Enable/disable, top 1...5, 25/50/75/100% trigger, incomplete-data policy, Cut/Maintain/Bulk/Custom energy intent, and Balanced/Protein Focus/Fiber Focus/Low Sodium/Custom nutrition emphasis
  → Custom exposes Reach/Stay Near/Try to Avoid/Ignore plus Gentle/Standard/Strong; it never exposes raw scoring weights
  → Rolling-week context is guarded and clamped; calorie and sodium hard caps are explicit advanced toggles and off by default
  → Configuration syncs through CloudKit `Preferences`, versioned JSON backup/import, and optional Turso mirror
```

## Food Bank Brand Flow

```
Food Bank toolbar → Brand filter
  → Lists runtime-derived brand buckets from visible saved foods, plus Unbranded for nil/blank brands
  → Empty search uses active foods only; non-empty search uses all foods so archived search matches remain consistent with existing archive behavior
  → Sort menu includes Brand Name, which groups named brands alphabetically before unbranded foods and sorts foods by name within each brand

Food Bank toolbar or "+" menu → Manage Brands
  → User selects one source brand and one target brand or types a new target
  → Bulk consolidation updates SavedFood.brand snapshots for every matching saved food, including archived foods
  → Existing journal entries remain unchanged because logged entries store copied brand/nutrition snapshots
```

## Composite Food Flow

```
Food Bank "+" → Composite Food
  → CompositeFoodBuilderView
  → User names the composite and adds Food Bank ingredients
  → Each ingredient is stored as CompositeIngredientSnapshot with copied nutrition, serving info, selected quantity, and selected unit
  → SavedFood.refreshCompositeNutrition() sums the selected ingredient portions into a SavedFood(kind: .composite)
  → Editing the composite changes its ingredient snapshots and recalculates future saved-food nutrition only
  → Existing NutritionEntry rows remain unchanged because logging still snapshots SavedFood.toNutritionEntry()
```

## Nutrition Calculator Flow

```
Food Bank "+" → Nutrition Calculator
  → NutritionCalculatorLibraryView lists SavedFood(kind: .calculator) rows by last used
  → New/Edit opens NutritionCalculatorEditorView
  → User defines restaurant/brand identity and a flat list of ingredients with portion names
  → Ingredient editor can call the selected AI provider's OCR/image understanding on images for the user-named ingredient only
  → Image import stays visibly disabled until the ingredient has a name and at least one image is selected
  → OCR fills nutrition first; imported portions keep source labels when available, otherwise default to "normal"
  → Manually added portions also default to "normal" as actual field text instead of opening with a blank placeholder
  → Calculator ingredients are stored as Codable value arrays on SavedFood, not relationships
  → Build opens NutritionCalculatorBuildView
  → User chooses one portion per ingredient, adjusts quantities, and sees live macro totals
  → Add to Journal writes a NutritionEntry with copied macros/micros, savedFoodID, servingUnit "build", and selectionSummary
  → Later calculator edits affect future builds only; previous NutritionEntry rows keep their logged nutrition snapshot
```

## CloudKit Sync Architecture (app-store branch)

```
iOS App (SwiftData + CloudKit)
  ←→ iCloud Private Database (automatic, free, multi-device)

  → ScanService → Direct Gemini REST API or OpenRouter chat completions (BYOK, zero server dependency)
  → Gemini/OpenRouter API keys stored in iOS Keychain via KeychainService
  → Optional TursoMirrorService → user-owned Turso DB via SQL-over-HTTP
      ↳ journal/configuration/usage: generation-pruned snapshot mirror
      ↳ detailed AI diagnostics: append-only events with 14-day retention
```

**Strategy**: SwiftData's `ModelConfiguration(cloudKitDatabase: .private("iCloud.k3vnc.OpenFoodJournal"))` handles Apple-device sync automatically. Optional Turso mirroring is a debuggable external copy for SQL inspection; it does not replace SwiftData/iCloud and does not restore data.

**CloudKit requirements enforced on all models**:
- All stored properties have defaults (including fully qualified enum defaults: `MealType.snack` not `.snack`)
- No `@Attribute(.unique)` (CloudKit can't enforce uniqueness)
- Relationships are optional (`var entries: [NutritionEntry]? = []`)
- No `.deny` delete rules

**Entitlements**: `OpenFoodJournal.entitlements` includes iCloud (CloudKit), Push Notifications (aps-environment), background mode (remote-notification).

**Data migration**: TursoMigrationView was deleted — CloudKit replaced the old Turso source-of-truth path. Current Turso support is optional push-only mirroring through `TursoMirrorService`, with normalized `ofj_*` tables and JSON columns for complex Swift value fields.

## Turso Agent Debugging

When a user has enabled Turso mirroring and provides credentials, use `.agents/skills/openfoodjournal/scripts/turso_debug.py` for read-only SQL inspection. It accepts `TURSO_DATABASE_URL` / `TURSO_AUTH_TOKEN`, common `LIBSQL_*` aliases, `.env` by default, or `--url` / `--token`. It supports: `summary`, `day YYYY-MM-DD`, `entry UUID`, `food-search TEXT`, `healthkit-pending`, `ai-events` with provider/status/operation/run/request filters, legacy `gemini-failures`, `typed-args-smoke-test`, and `raw-sql "SELECT ..."` (SELECT-only unless `--allow-write` is passed). `ai-events` excludes `payload_json` unless `--include-payload` is explicit.

## GitHub Project Board

Use `.agents/skills/openfoodjournal/scripts/github_project_board.py` to inspect
or update the OpenFoodJournal GitHub Projects v2 kanban board. The helper wraps
`gh project` with repo defaults so agents can avoid retyping owner/repo/project
arguments.

**Script maintenance**: Treat the repo-local path above as the stable command
entrypoint, but do not assume it is the canonical source file forever. This
helper may later become a symlink to a shared GitHub Projects utility used by
OpenFoodJournal and CodeGym. Before changing the script, resolve the real file
with `realpath .agents/skills/openfoodjournal/scripts/github_project_board.py`
or `readlink`, then modify the resolved canonical file and update this skill if
the shared location changes. Do not patch a stale copied script while another
project points at the shared target. If this is centralized, prefer a neutral
shared-tools location near the sibling repos instead of making one app repo own
the other app repo's utility.

Requirements:
- `gh auth status` must show `repo` and `project` scopes.
- Default owner/repo: `kvn8888/OpenFoodJournal`.
- Default project title lookup: `OpenFoodJournal`.
- Current Status columns are `Todo`, `In Progress`, and `Done`.
- Current Category options are `Spikes`, `Frontend / UX`, `Backend / API`,
  `AI / Gemini`, `Data / Sync`, `Health / Integrations`, and
  `Project / Process`.
- Current Priority options are `P0`, `P1`, and `P2`; Size options are `XS`,
  `S`, `M`, `L`, and `XL`; `Source` is a text field for the origin of the
  task.
- GitHub labels are used as an agent work router. Every planned issue should
  carry exactly one primary `agency:*` label, exactly one `agent:*` label, and
  optionally an `output:*` label:
  - `agency:ready` — a coding agent can implement or validate from repo context
    with little owner input.
  - `agency:investigate` — a coding agent can independently produce useful
    diagnosis, evidence, or a plan; implementation may or may not follow.
  - `agency:needs-owner-decision` — Kevin needs to decide product scope, risk,
    launch posture, or tradeoffs before implementation.
  - `agency:needs-architecture-decision` — system shape must be decided before
    code should move.
  - `agency:external-blocked` — action depends on Apple, Google, GitHub,
    CloudKit, App Store Connect, or another external setting/access path.
  - `agent:standard` — suitable for scoped UI, docs, tests, scripts, and small
    service changes.
  - `agent:strong` — use a strong coding agent for cross-layer SwiftData,
    HealthKit, Gemini, sync, migration, or tricky validation work.
  - `agent:frontier` — reserve for ambiguous architecture/product/security
    decisions where a frontier model is worth the cost.
  - `output:plan-only` — expected output is a decision memo, issue comment, or
    implementation plan before code.
- After each work session, update relevant GitHub issues and board fields
  (`Status`, `Category`, `Priority`, `Size`, `Source`) so the board reflects
  the latest state.
  At minimum, move actively worked issues to `In Progress`, move verified
  completed issues to `Done`, and add notes/links for blockers or validation.
- New agent-created issues should include context/source, acceptance criteria,
  likely starting files, risk or user impact, `Status`, `Category`, `Priority`,
  `Size`, `Source`, one primary `agency:*` label, one `agent:*` label, and
  `output:plan-only` when the expected next step is a memo rather than code.
- Draft Project cards are inbox items. Convert durable work to real GitHub
  Issues when it needs labels, comments, links, or agent routing; leave rough
  brainstorms as drafts until they are actionable.

Common commands:
```bash
python .agents/skills/openfoodjournal/scripts/github_project_board.py create
python .agents/skills/openfoodjournal/scripts/github_project_board.py projects
python .agents/skills/openfoodjournal/scripts/github_project_board.py columns
python .agents/skills/openfoodjournal/scripts/github_project_board.py list
python .agents/skills/openfoodjournal/scripts/github_project_board.py list --status Todo
python .agents/skills/openfoodjournal/scripts/github_project_board.py add-issue 4 --status Todo --category "AI / Gemini" --priority P0 --size M --source "manual triage"
python .agents/skills/openfoodjournal/scripts/github_project_board.py move 4 "In Progress"
python .agents/skills/openfoodjournal/scripts/github_project_board.py create-issue --title "Bug title" --body-file /tmp/body.md --label area:healthkit,type:bug,priority:p0,agency:ready,agent:strong --status Todo --category "Health / Integrations" --priority P0 --size M --source "conversation import"
python .agents/skills/openfoodjournal/scripts/github_project_board.py edit-issue 10 --body-file /tmp/body.md --add-label area:healthkit --status Todo --category "Health / Integrations" --priority P0
python .agents/skills/openfoodjournal/scripts/github_project_board.py check-criteria 10 --all
python .agents/skills/openfoodjournal/scripts/github_project_board.py check-criteria 10 "AI Search overlay"
python .agents/skills/openfoodjournal/scripts/github_project_board.py set-fields 10 --status "In Progress" --category "Health / Integrations" --priority P0 --size M --source "validated"
```

## Backup / Export Flow

```
Settings → Data → Export Spreadsheet CSV
  → NutritionStore.exportCSV()
  → Human-readable analytics CSV with stable IDs, ISO dates, escaped fields, core macros, serving basics, savedFoodID, scanDurationMs, and dynamic micronutrient columns
  → Not intended for restoring app state

Settings → Data → Export Backup
  → NutritionStore.exportBackup(goals, appSettings)
  → Versioned JSON (`schemaVersion: 1`) with DailyLog, NutritionEntry, SavedFood (including emoji, generated icon image data, composite ingredient snapshots, and calculator ingredient snapshots), TrackedContainer, Preferences, UserGoals, meal schedule, and non-sensitive app settings
  → Does not include Gemini/OpenRouter API keys, HealthKit authorization state, or HealthKit samples

Settings → Data → Import Backup
  → Decodes `OpenFoodJournalBackup`
  → Confirms with the user before import
  → NutritionStore.importBackup(...) upserts by stable UUID and relinks entries to DailyLogs by ID
  → Re-importing the same backup updates existing records instead of duplicating them

Settings → Data → Export AI Logs
  → TursoMirrorService.exportDiagnosticCSV()
  → Flushes pending events, then queries the last 14 days from ofj_ai_diagnostic_events
  → Includes provider/model/deployment, run/turn/call/request IDs, timings, usage/cost, status/errors, and bounded redacted operational metadata
  → Does not include prompts, answers, journal/HealthKit values, source URLs/content, attachments, raw provider bodies, chain-of-thought, API keys, or image bytes
```

**Server**: The current app path has no proxy server. The iOS app calls Gemini or OpenRouter directly, CloudKit handles Apple-device sync, and optional Turso mirroring talks directly to Turso SQL-over-HTTP. The legacy Express/Turso source-of-truth architecture lives only in old branch history.

**Turso mirror schema**: `TursoMirrorService` creates namespaced `ofj_*` tables: `ofj_sync_runs`, `ofj_daily_logs`, `ofj_nutrition_entries`, `ofj_saved_foods`, `ofj_tracked_containers`, `ofj_preferences`, `ofj_user_goals`, `ofj_app_settings`, legacy `ofj_gemini_scan_logs`, `ofj_gemini_cost_accumulators`, and append-only `ofj_ai_diagnostic_events`.

**Turso migration pattern**: Use `CREATE TABLE IF NOT EXISTS` for full table creation. For additive columns, query `PRAGMA table_info(table_name)` and only then run plain `ALTER TABLE table ADD COLUMN column TYPE`. SQLite/libSQL does not support `ALTER TABLE ADD COLUMN IF NOT EXISTS`.

**Turso sync integration points**: SwiftData + CloudKit remain source of truth for conversations, nutrition, run recovery, and usage aggregates. Local application writes call `scheduleMirror(reason:)`; each snapshot mirror upserts current rows with a `mirror_generation` and prunes older generations per table only after that table succeeds. Detailed diagnostics instead call `recordDiagnostic(_:)`, then flush UUID upserts independently; `ofj_ai_diagnostic_events` is deliberately excluded from generation pruning. Turso is not read back into application state.

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
15. **CloudKit optional relationships need `safeEntries` pattern** — `var entries: [NutritionEntry]? = []` requires unwrapping everywhere. Add `var safeEntries: [NutritionEntry] { entries ?? [] }` and use that for reads. Use `NutritionStore.link(_:to:)` for entry/log writes so nil arrays, moved entries, and duplicate references are normalized.
16. **Day UI depends on `DailyLog.entries`; CSV export fetches `NutritionEntry` directly** — if entries export but older days look empty, suspect orphaned or duplicate `DailyLog` relationships, not deleted food data. `repairDailyLogEntryRelationships()` runs on launch and is intentionally idempotent so it can reattach entries after CloudKit sync catches up.
17. **`KnownMicronutrient.Category` cases are `.vitamin`/`.mineral`** — not `.vitamins`/`.minerals`. The enum raw values are plural ("Vitamins"/"Minerals") but the Swift case names are singular.
18. **`@Observable` should only track UI state** — mark framework infrastructure with `@ObservationIgnored` (`ModelContext`, `URLSession`, `HKHealthStore`, `AVCaptureSession`, `AVCaptureDevice/Input`, continuations). Leaving dispatch/AVFoundation/HealthKit internals observable can surface runtime-only Objective-C selector crashes such as `_setContext:` on dispatch-backed objects. For `NSObject` delegate controllers like `CameraController`, prefer `ObservableObject` + `@StateObject` with `@Published` UI state instead of `@Observable`.
19. **Gemini thinking levels are model-specific enums, not interchangeable strings** — `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite) officially supports `minimal` and `high`: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image. The executable enum is `GeminiFlashLiteImageThinkingLevel { case minimal, high }`, and the production image request uses `.high` because it is documented and live-verified. **Never send `low` to this image model.** A hard-coded `low` value was accepted transiently and then began returning HTTP 400 on 2026-07-31. Text-model thinking configuration must not be reused for image models. Unit tests must assert the exact enum and serialized payload; the protected TestFlight workflow must run the exact production builder against Gemini before archive/upload. Separately, streamed text scans must parse `event:` + `data:` lines and route `step.delta` by `delta.type`: `thought_summary` updates the visible trace, `text` accumulates final JSON, and completion/stop usage updates cost. Do not wait for blank SSE separators, invent thought-summary chunks, or place API keys in query strings.
20. **Debugger log triage needs ownership evidence** — use `docs/debug-log-triage.md` and `.agents/skills/openfoodjournal/scripts/triage_debug_log.py` before turning Xcode console noise into app work. Keyboard constraints with `TUIKeyplane`/`TUIPredictionViewCell`, RunningBoard entitlement lines, Network framework UDP/TCP cleanup, and CoreData CloudKit `BGSystemTaskSchedulerErrorDomain Code=3` export scheduling lines are usually framework/debugger noise unless a breakpoint stack enters `OpenFoodJournal`. `unsafeForcedSync` is not actionable from the log line alone; capture a Swift concurrency runtime backtrace. `glassEffect() tried to update multiple times per frame` is the scan-session warning family most likely to be app-owned, so check broad implicit animations around glass-heavy overlays first.
21. **`AVCaptureSession.startRunning()` / `stopRunning()` block** — they take hundreds of milliseconds to a second. `CameraController` runs them on `k3vnc.openfoodjournal.camera.session`, not the main actor. Calling them from `@MainActor setup()` freezes the scan sheet for ~1s.

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

- **`main`** — Original Turso sync architecture. `SyncService.swift` present, all views have fire-and-forget sync Tasks. Treat this as legacy branch history, not the current app-store architecture.
- **`testflight`** — Protected integration/beta branch. Pull requests run cloud compile and non-UI unit/provider-contract tests. Trusted pushes allocate a remote-safe build number, archive once on the GitHub `macos-26` runner pinned to stable Xcode 26.6 (17F113), upload to internal TestFlight, and create an immutable `testflight/<version>-<build>` prerelease manifest.
- **`app-store`** — Protected production-promotion branch for the CloudKit architecture and the repository default branch. It must promote a reachable, manifest-backed TestFlight build without rebuilding the binary. App-affecting changes after the selected TestFlight tag block promotion. Normal pushes stage metadata, attach the exact build, validate, and prepare a private `vX.Y` GitHub release draft; App Review submission requires an explicit manual input plus protected-environment approval. A six-hour public-release sync publishes the draft only after Apple's public storefront reports the same version.

## Cloud CI and release workflow

**Required live-test forwarding (2026-08-30)**: Host `OFJ_*` environment variables
alone do not reach the iOS XCTest process. The protected image gate must set
`TEST_RUNNER_OFJ_RUN_LIVE_GEMINI_IMAGE_TESTS=1` and
`TEST_RUNNER_OFJ_GEMINI_API_KEY` (secret), per Apple's xcodebuild environment
contract: https://developer.apple.com/documentation/xcode/environment-variable-reference.
Always verify the exact required test executed and passed, not just that the job
was green. `verify-live-test-log.sh` rejects missing, skipped, failed, duplicated,
or mixed outcomes. Normal unprivileged tests remain opt-in and skip live calls.

See [`docs/cloud-release-workflow.md`](../../../docs/cloud-release-workflow.md) for the old-versus-new comparison, workflow behavior, security model, secrets, branch protections, rollout checklist, and current blockers.

- `.github/workflows/cloud-ci.yml` runs release-workflow contract tests, compiles all targets, and executes `OpenFoodJournalUnitTests` on a hosted simulator. It never runs UI tests or receives deployment/provider secrets.
- `.github/workflows/screenshots.yml` is optional: manual CLI dispatch on a selected branch (verified after registration by a labeled PR run) or the `ci:screenshots` label on PRs to `testflight`/`app-store`. The web Run Workflow button depends on the default-branch workflow file. It builds `OpenFoodJournalScreenshots` once and exports Journal, Scan, Food Bank, Log Food, History, Assistant, and Settings in light/dark mode as PNGs plus an offline gallery and commit/hash manifest. It is not a release gate and receives no secrets. `ScreenshotFixtures.swift` contains Debug-only sample data; both `OFJ_UI_TEST_MODE=1` and `OFJ_SCREENSHOT_MODE=1` are required for fixed presentation dates and fixture setup. Test stores explicitly disable CloudKit. The Scan capture uses the real `ScanCameraControls` over white, with simulated zoom/torch and inert shutter/library actions; it never creates a camera controller or requests permissions. Ordinary UI tests retain their existing mocked Assistant scenario. Keep real service/persistence clocks on `Date`; `AppPresentationDate.now` only stabilizes visual dates in screenshot mode. See `docs/screenshots.md` for inputs, artifact retention, and extension guidance.
- `.github/workflows/release-credentials-check.yml` is a manual, read-only smoke workflow. It checks App Store Connect app/build access from both deployment environments and independently validates the TestFlight certificate/password and provisioning profile without allocating a build number, archiving, uploading, staging, or submitting.
- `.github/workflows/testflight.yml` is gated by `ENABLE_TESTFLIGHT_AUTOMATION=true` and the `testflight-internal` GitHub environment. It validates the source-controlled marketing version, allocates only the build number automatically, drafts version-specific public notes with GitHub Models plus deterministic fallback, validates the 4,000-character/locale contract, uses ephemeral signing assets, distributes internally, and publishes an immutable schema-2 commit/build/IPA/notes manifest. DerivedData, archives, IPA files, and signing material are not retained.
- `.github/workflows/testflight-external.yml` is manual-only on the default `app-store` branch. It requires an exact immutable TestFlight tag plus explicit confirmation, verifies the manifest before and after the protected `app-store-production` approval gate, assigns the existing binary to the configured public-link external group, and submits Beta App Review without rebuilding or re-uploading. It is idempotent when a build is already assigned, awaiting review, or externally testing.
- `.github/workflows/app-store.yml` is gated by `ENABLE_APP_STORE_AUTOMATION=true`. Its unprivileged prepare job resolves and displays the exact TestFlight binary and hash-bound public notes before the protected `app-store-production` environment asks for approval. The approved job reverifies the artifact, stages the existing `VALID` build without recompiling, copies prior public metadata, applies the reviewed notes, runs strict readiness checks, and prepares a private `vX.Y` draft containing the schema-2 manifest and notes. A normal push never submits; submission requires `workflow_dispatch` with `submit_for_review=true` plus environment approval.
- `.github/workflows/app-store-release-sync.yml` runs every six hours or manually without Apple credentials. It reads Apple's public storefront version, resolves the matching private `vX.Y` draft, verifies its app/version/build/TestFlight tag/commit/target/note hash against the attached schema-2 manifest, and only then publishes it as the immutable Latest GitHub release. An already-published match is an idempotent no-op; a missing or mismatched draft fails closed.
- `ci/release-config.json` owns non-secret Apple identifiers, toolchain pins, and the default GitHub Models release-note model. Credentials stay in protected GitHub environment secrets or an external secrets manager.
- GitHub Models receives only bounded commit-derived release evidence through a short-lived `GITHUB_TOKEN` with `models: read`. AI may draft public copy, but deterministic automation validates and seals the artifact. Build numbers, signing, build identity, upload/promotion, state changes, legal/privacy/export/health declarations, and public submission remain outside AI authority.

## Conventions

- **Container icon provenance and History polish (2026-08-31)**: `TrackedContainer.toNutritionEntry` must copy its existing `savedFoodID` so Journal/History resolve the Food Bank icon by UUID; keep snapshot nutrition unchanged and do not guess old orphan links by name. Immediate tare logging already carries the link. Nutrition's picker/date/card share a single List row with explicit spacing. History date/composite text transitions use the shared numeric helper with full-content triggers. The micronutrient strip is one alphabetic row with no edge arrows. No persistence schema change.

- **Nutrition/History refresh (2026-08-30)**: Both screens use bounded `NutritionLogQuery` and non-persisted `NutritionAnalytics` snapshots; calendar, charts and drill-down share date-aware values and the Journal duplicate-day rule. Keep historical reference dates through food/nutrient navigation. Averages include only recorded days (zero counts; missing does not), with visible coverage; normalize aliases and compatible units, never combine incompatible units. History is calendar → selected-day link → Week/Month → one alphabetical tracked-micro row/chart; no Custom or gaps caption. Day detail exposes all recorded micros and reuses `JournalEntryButton` for tap-to-edit and context menus without swipes. Journal owns swipe modifiers and clear List row backgrounds so the gradient remains visible. No schema change is part of this release. See `docs/nutrition-history-refresh.md`.

- **Journal visual transfer (2026-08-30)**: Production Journal and Food Bank rows share `FoodMacroPill`: one 110×40 neutral glass capsule, three 35pt-spaced number/G columns, lavender/green/amber text (not the playground RGB experiment). Dimensions scale with Dynamic Type; accessibility-size rows place the pill below the title. `MacroSummaryBar` opts into 4.3pt tracks, 16pt fitted values, and D86669 overage; other ring callers keep their prior style. Journal gradient stops are 0/0.25/1 over 16–800pt with separate light/dark opacity arrays. Keep native navigation, scoped day queries, and swipe actions. Settings → Journal → Show Food Images defaults on independently of generation settings, round-trips in backups, and enters optional Turso settings mirroring. `JournalEntryFoodImage` observes exact linked/source-entry Food Bank IDs only, uses the shared 51pt image/58pt column, and shows placeholders when absent or undecodable. Never name-match images or generate them from row appearance. Newly created `SavedFood(from:)` records source-entry provenance without altering logged nutrition. Old unlinked entries may correctly remain placeholders.
- **Journal design playground (Kevin, 2026-08-30)**: `DesignPlaygrounds/Journal/JournalPlayground.xcodeproj` is an intentionally isolated native macOS visual scratchpad, not a port of the app. Edit `JournalDesign.swift` like CSS, preview with `JournalPlayground → My Mac`, then port only explicitly chosen visual changes back. Duplicated presentation and fictional sample meals are intentional; do not introduce app services, SwiftData/CloudKit/Turso, credentials, camera dependencies, or shared production target membership. No iOS simulator/runtime is needed. `build.sh prepare` installs project-local per-user Xcode settings keeping Canvas DerivedData under the playground's ignored `.build` on DevDisk; Xcode 27 ignores a shared DerivedData location alone. CLI build/run also prepare these prefs and explicitly route caches externally. iOS system chrome is approximate; this sandbox does not prove iPhone behavior. See its README for setup/storage caveats. Do not build or install the shipping app to verify this playground.
- **Comments**: Explain *why*, not *what*. Entry-level devs should understand each function's purpose.
- **File creation**: Build large files in small chunks to avoid network errors.
- **Retrospectives**: Live in `docs/`. Update when later fixes change the story.
- **Skills**: This file is the project skill. Update it when architecture or requirements change.
- **Commits (Kevin, 2026-08-30)**: Commit previously completed work before beginning a new change. Prefer frequent local checkpoint commits after each agent-owned file edit, with descriptive messages; intermediate checkpoints may be incomplete until the final verified commit. Stage only the intended file/hunks, never secrets or another session's unapproved work. This preference does not authorize pushing or releasing without an explicit request.

**DailyLogView container**: Uses a `List` (not ScrollView+LazyVStack) with `.listStyle(.plain)` + `.scrollContentBackground(.hidden)`. `WeeklyCalendarStrip` and `MacroSummaryBar` are plain List rows with `listRowBackground(Color.clear)` + `listRowSeparator(.hidden)`. Meal sections use `MealSectionView` which returns a `Section{}` that becomes a proper sticky List section header in a List context. All swipe actions are on the `MealSectionView` Button wrapper (not on `EntryRowView`).

**Journal data reactivity**: `DailyLogView` owns a range-scoped SwiftData `@Query` for calendar history. `JournalDayData` applies the same populated-row/UUID duplicate-day selection as `NutritionStore.fetchLog`; `JournalDayTotals` is a render-time value snapshot, not a new persisted model or `@State` cache. The macro bar, calendar progress dictionary, and selected-day background derive from that one snapshot. Calendar cells must not independently fetch logs or rely only on the local `changeCount`: newly inserted days and incoming persistence changes need query membership observation. Calendar arc/color animation is keyed to progress, scoped away from selection/font-weight transitions, and respects Reduce Motion. Non-UI regression tests cover projection and Observation; actual CloudKit delivery and visual motion still require a manual device smoke check.

**Journal → Food Bank**: Shared `MealSectionView` rows expose Save to Food Bank via context menu and leading swipe, so Journal and History behave consistently. `NutritionStore.saveJournalEntryToFoodBank` copies the logged portion (macros, micros, serving quantities/mappings), queues its image through the canonical saved-food path, and retains `SavedFood.sourceJournalEntryID` to avoid repeated-save duplicates. It does not repoint the journal entry's `savedFoodID`, especially when that ID identifies a source calculator. A repeated save returns the existing snapshot rather than overwriting user edits; archived snapshots are restored.

**Calculator customizations**: `SavedFood.calculatorCustomizations` contains Codable name/selection/summary/last-used snapshots with CloudKit-safe defaults. The Build view lists Saved Customizations immediately below Ingredients. Explicit save creates no journal entry; logging through `NutritionStore.logCalculatorBuild` persists both the nutrition snapshot and the reusable choices in one save. Identical name/ingredient/portion/quantity combinations deduplicate independently of transient selection IDs/order. Loading is opt-in and uses current calculator nutrition; old journal nutrition never changes. Missing portion/ingredient IDs or invalid quantities block reuse rather than silently dropping part of a meal. Old text-only `selectionSummary` records are not parsed into guessed presets. Both customizations and source-journal IDs round-trip through backup DTOs and additive Turso saved-food columns. `NutritionStore.log` now returns a discardable success Bool so callers that own a dismiss action can report persistence failure.

**Repeat logging and scan-to-container UX**: `LogFoodSheet` applies the most recent valid quantity + unit for the linked `SavedFood` on first appearance, falling back to the template when history is missing or its unit is no longer available. Scan results expose an explicit "Save to Food Bank & Track Container" action that saves without journal logging and presents `NewContainerSheet(preselectedFood:)`; dismissing container setup keeps the Food Bank item.

**Appearance and Log Food**: Settings offers Blue, Harvest Orange, Leaf Green, and Berry Purple through `OFJAccentTheme`; the app root owns the tint/environment injection. Harvest Orange uses the reviewed `#E9792B` accent with warm light `#F6F5F3`/`#FFFFFF` and dark `#20201F`/`#2A2A28` Log Food surfaces. `LogFoodSheet` uses compact identity, amount-preserving unit controls, calorie/macronutrient composition, always-visible editable micronutrients when present, factual saved mappings, meal selection, and a sticky Add action. It still logs through `NutritionStore.log(...)` with the linked Food Bank ID and serving-scaled macro/micronutrient values; no view coordinates HealthKit or Turso directly. Accent choice round-trips through JSON backup and the optional Turso settings mirror, with Blue as the backward-compatible fallback.

**RadialMenuButton**: Option bubbles support direct `.onTapGesture` (as well as drag-to-select). A `Color.clear.contentShape(Rectangle()).ignoresSafeArea()` layer behind `GlassEffectContainer` dismisses the menu when tapping outside. The layer is only inserted into the ZStack when `isOpen == true`. Option label text has a subtle drop shadow for legibility over light/glass backgrounds.

**Swipe mappings**:
- `FoodBankView` row: trailing (swipe left) = Archive/Unarchive (gray/green) + Edit (blue); leading (swipe right) = Add to journal (green)
- `MealSectionView` row: trailing (swipe left) = Delete; leading (swipe right) = Edit — both on the outer Button wrapper (never on `EntryRowView` to avoid double-registration gesture lag)

**FoodNutrientBreakdownView**: Inverse of `NutrientBreakdownView` — shows all nutrients (macros + micros) for a specific food across the selected period. Accessed by tapping a food row in NutrientBreakdownView's "By Food" section.

**EditEntryView**: Has full serving-mappings section (same as LogFoodSheet). Uses shared `AddServingMappingSheet` (defined in LogFoodSheet.swift, internal not private). `addMapping()` calls `nutritionStore.saveEntry(entry)`.

**CursorEndModifier**: Applied once at the app root with `.cursorAtEnd()`. It keeps `UITextField` cursors at the end on focus and installs a non-canceling window tap recognizer that dismisses the keyboard when tapping outside text inputs. Keep this centralized instead of adding competing per-view whitespace tap gestures.

**Executable UI foundations**: `Views/Shared/OFJDesignSystem.swift` owns `OFJColor`, `OFJSpace`, `OFJRadius`, `OFJType`, `OFJMotion`, `OFJLayout`, calendar calorie state, and stable content phases. Seed values match the existing Liquid Glass UI; architecture-only migrations must be pixel-equivalent unless a separate reviewed design issue authorizes a visual change. Issue #45 authorizes only the Journal calendar/header treatment: selected month/year title, no outer calendar glass card, rounded selected-day rectangle, larger weekday labels, dashed future rings, calendar-only adaptive black/green/`#D86669` status colors, and a subtle selected-day calorie gradient.

## Current State (Last Updated: 2026-08-31)

- **Branch: `app-store`** — CloudKit is the primary sync path, with optional push-only Turso mirror for user-owned SQL debugging
- **Cloud release foundation** — Both release branches and deployment environments exist. Credentials pass App Store Connect read checks, and TestFlight signing assets pass integrity checks. `testflight-internal` is restricted to `testflight`; `app-store-production` is restricted to `app-store` and requires `kvn8888` approval. Both branches require pull requests, resolved conversations, and cloud CI; force pushes/deletion are blocked. `testflight` stays linear, while `app-store` uses merge commits for promotion so immutable TestFlight tags remain ancestors of production. GitHub release immutability and scheduled public-App-Store release synchronization are enabled, and both deployment variables are enabled.
- **Public App Store: version 1.3 build 3** — live App Store Connect state `READY_FOR_DISTRIBUTION`; GitHub v1.2 and v1.3 releases were reconciled to Apple on 2026-07-30, with v1.3 Latest.
- **Internal TestFlight build identity is CI-owned** — the `testflight` workflow resolves the next version/build at runtime and publishes an immutable manifest; do not infer the deployed source from the stale local project build number.
- App structure complete: all models, services, and views implemented
- 4-tab layout: Journal, Food Bank, History, Assistant. Settings is pushed from the Journal's top-right toolbar; Containers remain accessible via RadialMenuButton.
- **Assistant tab (agent foundations 2026-08-27)**: persistent CloudKit-synced agentic chat with independent Gemini/OpenRouter/Azure/OpenAI/Anthropic/Muse Spark generation and independent model-native/Tavily/Parallel/Exa research. Model-response context menus expose a Response Info sheet containing the former completed-run metadata plus current context-window estimate, limit, reserves, last reported/cached input, compaction state, cost, retries, and request IDs; do not restore the always-visible composer context meter or the separate completed-run boxes.
- App and full unit/UI test targets compile with `xcodebuild ... build-for-testing` against `generic/platform=iOS`; generic unsigned Release and signed App Store archives also succeed. The installed simulator runtime works with an isolated `/private/tmp` device set, but this Mac's default CoreSimulator store is symlinked to an external volume that CoreSimulatorService cannot write, so XCTest execution needs that host configuration repaired or a safe signed device destination.
- SwiftData + CloudKit Private Database for data persistence and sync
- AI scans/searches call the selected BYOK provider directly from the device; Gemini Interactions remains the default, OpenRouter chat completions can be selected in Settings, and no Render proxy is used by the current app path
- Food Bank: save foods from scan/manual entry, build composite foods from snapshot ingredient portions, manually generate missing emojis/images from Settings or per-row context menus with sequential selected-provider calls, optionally show circular Gemini Flash Lite image icons for saved foods, browse/search/sort/filter active foods, filter by runtime-derived brand buckets including Unbranded, bulk-consolidate one brand string into another across all saved foods, auto-hide foods unused for over 14 days, manually archive/unarchive foods, log archived foods from search or Archive
- Shelf recommendations: mark foods actually available at home, surface deterministic nutrition-aware Good Fits after a configurable calorie trigger in an expanded-by-default collapsible Food Bank section, swipe a suggestion to explicitly remove that food from the Shelf, prefill an editable suggested serving, and configure top 1...5, separate energy/nutrition intents, guarded rolling context, soft nutrient policies, and optional hard caps in Settings
- Nutrition Calculator: calculators are `SavedFood(kind: .calculator)` rows with flat ingredient/portion snapshots. OCR import is name-first per ingredient: type an ingredient name, choose an image from the library or camera, the selected AI provider fills nutrients, and portion rows default to visible `normal` field text when no source label exists.
- Keyboard UX: tapping outside a text input dismisses the keyboard app-wide via `CursorEndModifier`, while taps still pass through to buttons/lists.
- Settings Data: spreadsheet CSV export plus versioned JSON backup export/import. JSON import is idempotent by UUID and includes saved-food emojis.
- Apple Health consistency: `NutritionStore` owns entry sync/delete side effects for every journal mutation path, including Assistant tools, instead of requiring each SwiftUI screen to remember a second call. App launch and foreground reconcile persisted `notSynced`/stale entries automatically. Settings can still force-rewrite OpenFoodJournal-owned HealthKit nutrition samples for every entry, using deterministic sync identifiers so historical macro-only or partial micronutrient writes can be replaced without duplicating samples. Incremental "Sync Missing" also picks up new HealthKit dietary export mappings because the write hash includes the export schema version.
- **AI scan UX**: direct Gemini loading overlay shows Interactions API streamed thought-summary trace, OpenRouter shows a neutral provider wait state, and the result sheet/scan page can redo the last submitted photo set. The live camera opens directly with Scan Food/Barcode/Food Label rectangular modes, compact non-glass 0.5×/1×/2× controls above them, circular torch/library controls flanking the shutter, exit at top-left, and conditional retry at top-right. Startup initializes only the physical wide lens. Selecting 0.5× replaces the session's sole input with the ultra-wide lens; 1× and 2× use the wide lens, with 2× applying a device zoom factor. The full-screen aspect-fill preview publishes its normalized visible sensor rectangle and every shutter press snapshots that crop, so review, barcode detection, and AI input contain exactly the framing visible at capture time instead of the wider uncropped still. The remaining camera chrome uses dark Liquid Glass with white labels/icons over the live preview, with no bottom legibility gradient, and deliberately omits logos, real-time ingredient callouts, and instructional caption bubbles.
- **Open Food Facts integration**: Enter-only search, zero-calorie/no-usable-nutrition rows filtered out, add to journal/food bank, per-serving nutrition
- **Food Bank "+" toolbar menu**: Composite Food, Nutrition Calculator, Search Open Food Facts, Manual Entry, Archive, and Manage Brands. AI Search is intentionally removed.
- **Meal Schedule**: Settings lets users configure Breakfast/Lunch/Dinner start times. Manual entry, scan result, saved-food logging, container completion, and nutrition-calculator builds default to the schedule from the device's local clock at log time while still allowing manual meal override.
- **Settings: OFF contribute toggle/status** (`off.contributeEnabled`, default off; `off.contributionSuccessCount` and `off.lastContributionAt` show confirmed on-device upload history)
- Container Tracking: create from Food Bank food, enter start weight, complete with final weight
- Serving Mappings: per-food unit conversions, editable in EditEntryView
- **NutritionDetailView**: `ScrollView` on `JournalCalorieBackground` (same page treatment as History/calendar). Macro summary and vitamin/mineral sections use `NutritionSurface` glass cards. Avoid `insetGrouped` List here — glass on grouped-list chrome creates a double-card halo.
- **External TestFlight**: `ci/release-config.json` carries `externalTestFlightGroupID` (empty by default). When set, `asc publish testflight` distributes to it alongside the internal group and `--submit --confirm` asks for Apple's Beta App Review. asc skips the submission when no external group was added, so an empty value keeps internal-only behaviour.
- **App Store product-page copy**: `app-store.yml` resolves `description`, `keywords` and `promotionalText` before the protected approval gate, in order: committed `metadata/releases/<version>/<locale>/store.json`, the Claude Code agentic harness, the Bifrost router, then keeping the live text. Every tier must pass `.github/scripts/validate-store-metadata.sh`. The proposed copy appears in the approval summary, and generated fields are excluded from `--copy-metadata-from` so they are not overwritten.
- **History micronutrient pins**: long-press chip → context menu Pin/Unpin. Persisted by `PinnedMicronutrientSettings` (`history.pinnedMicronutrientIDs`) and included in `AppSettingsRecord` backups.
- **FoodNutrientBreakdownView**: inverse of NutrientBreakdownView — food → all nutrients. NavigationLink from NutrientBreakdownView "By Food" rows
- **LogFoodSheet refresh**: selected app accent, deterministic amount-preserving unit controls, calorie/macro composition, daily-total preview, always-visible editable micronutrient table, factual saved-unit mappings, and sticky meal-aware Add action. Accent selection persists in app settings, backup, and the optional Turso mirror.
- **Radial menu text shadow**: option labels have `.shadow()` for legibility over glass
- **Swipe gesture lag fix**: swipe actions consolidated on MealSectionView Button wrapper (removed from EntryRowView), SavedFoodRowView has `.contentShape(Rectangle())`, EntryRowView uses static DateFormatter
- WeeklyCalendarStrip: horizontally scrollable week strip with momentum snapping; selected dates use a rounded rectangular material state, future dates use disabled dashed rings, and calendar progress uses a Journal-only adaptive black/green/`#D86669` palette. The strip has no outer glass card or duplicate month header; `DailyLogView` shows the selected month/year as its large title and derives a subtle background gradient from the selected day's calorie state.
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
- TursoMigrationView deleted — old restore/source-of-truth Turso migration path is dead code
- Optional Turso integration in Settings → Data stores URL/token in Keychain, supports `/health`, migrations, generation-pruned journal/usage mirroring, direct append-only AI diagnostics, legacy CloudKit-log migration, remote diagnostic export/clear, and an agent read-only debug script.
- Assistant tests use `ScriptedChatModelProxy`, a separate `ScriptedChatWebSearchProvider`, an injectable monotonic clock, and an in-memory SwiftData harness. Provider wire fixtures cover Gemini signatures/call IDs, Azure/OpenAI encrypted continuation replay, Anthropic signed-thinking/tool IDs, Muse Spark runtime slugs/tool calls, and Tavily/Parallel/Exa research. Food Bank tool tests must prove a generated serving-to-grams statement makes `g` selectable without manual mapping. `OpenFoodJournalUnitTests` is the shared non-UI scheme; live provider contracts are opt-in and skip without environment credentials.

## App Store Submission Notes

**First submission rejected (Guideline 1.4.1 — Physical Harm)**: App provided health/nutrition data without citations. Fixed by adding `HealthDisclaimerView` (Settings → Sources & Disclaimers) with FDA Daily Values links, Atwater system reference, AI estimation disclaimer, and general medical disclaimer. Inline citations added to NutritionDetailView, ScanResultCard, and GoalsEditorView.

**Other audit findings to address before next submission:**
- README.md has been updated for the current app-store architecture, including optional Turso mirroring. Re-check before submission if branch contents change again.
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
  - **Text search**: `GET https://search.openfoodfacts.org/search?q={query}&fields=product_name,brands,code,nutriments,serving_size,serving_quantity&page_size=25` — dedicated Elasticsearch-backed search service (the legacy v1 CGI endpoint returns 503)
  - **Barcode/product lookup (v2)**: `GET https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=...` — full nutrition data
  - **Filtering**: `OFFProduct.hasUsableNutrition` requires calories > 0 plus at least one macro or micronutrient. Text search and barcode lookup reject zero-calorie/no-nutrition placeholder rows before UI prefill.
  - **Fields requested** (for product detail): `product_name,brands,nutriments,serving_size,serving_quantity,code`
  - **Nutriments mapping**: `energy-kcal_100g` → calories, `proteins_100g` → protein, `carbohydrates_100g` → carbs, `fat_100g` → fat, plus micronutrients (fiber, sugar, sodium, etc.)
  - **User-Agent**: `OpenFoodJournal/1.0 (openfoodjournal@example.com)` — required by OFF API policy
  - **Rate limits**: 10 req/min for search, 100 req/min for product reads
  - **No auth required** for reads; writes (contribute) require OFF account credentials
- **UI access points**:
  - **FoodBankView toolbar**: "+" button (leading of sort button) → Menu with 3 options: Scan, Manual Entry, Search Open Food Facts
  - **Scan** and **Manual Entry** reuse existing sheets (`ScanView` via DailyLogSheet, `ManualEntryView`)
  - **Search Open Food Facts** opens `OpenFoodFactsSearchView` — Enter-only search, filtered usable results, tap to review details
  - **Result action**: Same pattern as ManualEntryView — "Add to Journal" or "Add to Journal & Food Bank" via toolbar Menu
- **Settings**: `@AppStorage("off.contributeEnabled")` toggle (default: `false`) plus contribution status backed by `off.contributionSuccessCount` / `off.lastContributionAt`. Current code reports whether this device has recorded confirmed uploads; it does not submit writes just because the toggle is enabled.
- **Data flow**: OFF search result → `OFFProduct` struct (Codable) → converted to `NutritionEntry` / `SavedFood` with `scanMode: .manual` and brand preserved. Nutrition values from OFF are per-100g; conversion to serving-based values uses `serving_size` field when available.
- **No SPM dependency**: Direct `URLSession` calls, no OFF Swift SDK imported (keeps zero-dependency architecture).
