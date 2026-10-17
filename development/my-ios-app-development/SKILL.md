---
name: my-ios-app-development
description: Use as the top-level best-practice guide when designing, implementing, refactoring, or reviewing SwiftUI iOS apps. Covers app architecture, file organization, state ownership, local-first data, theming, import/share flows, reader rendering surfaces, accessibility, performance, testing, concurrency safety, settings, release notes, and Xcode build validation. For deep framework or App Store details, pair with specialized skills such as my-ios-app-swiftui-patterns, my-ios-app-swift-concurrency, my-ios-app-swift-testing, my-ios-app-swiftui-performance, my-ios-app-ios-accessibility, my-ios-app-swiftdata, my-ios-app-pdfkit, my-ios-app-swiftui-webkit, my-ios-app-aso, or my-ios-app-store-changelog.
---

# iOS App Development

Use this as the app-development best-practice skill for SwiftUI iOS work. It is especially useful for product design, feature implementation, UI polish, data modeling, local persistence, import/export flows, settings pages, project cleanup, and code review.

This skill sets the default engineering posture. When the task needs concrete framework APIs, use the relevant companion skill for details rather than expanding this guide with long examples.

## Development Principles

- Build the actual usable app experience first, not a marketing shell.
- Keep changes tightly scoped to the requested behavior.
- Prefer the app's existing patterns, naming, file layout, and helper APIs.
- Follow single-responsibility and easy-extension principles. Each file should usually own one focused concern.
- Reuse shared helper logic instead of duplicating parsing, formatting, persistence, or UI state code.
- Avoid introducing large frameworks, databases, or architecture changes unless the current approach is clearly limiting the feature.
- Make user-owned data durable before optimizing derived caches or visual polish.
- Preserve existing data formats and migration paths unless the task explicitly calls for a storage change.
- Treat build success as part of the task, not a separate optional step.
- When this skill could be improved because guidance is outdated, ambiguous, or missing a recurring rule, propose the improvement to the user and wait for explicit confirmation before editing the skill.

## Version And Availability Strategy

- Before recommending or using modern Apple APIs, inspect the project's minimum deployment target, Swift language version, Xcode/toolchain version, and package platform settings when they are available.
- Match implementation choices to the existing target. Do not introduce iOS 26+, Swift 6.3+, or Xcode 26-era APIs into an older-target project unless the user accepts the target bump or the code includes availability gates and fallbacks.
- When a companion skill documents a newer API, treat its version notes as gates, not defaults that override the app's current compatibility policy.
- If the project has no clear version policy, state the assumed target before using version-sensitive APIs.
- Keep compatibility logic localized: prefer small `#available` branches, focused adapters, or alternate helper methods over scattering version checks through feature views.

## Optimization Discussion Template

When the user wants to review optimizations or bug fixes before implementation, explain one item at a time and wait for confirmation before editing nontrivial code.

When executing optimization, cleanup, or refactoring work, always apply this rule: explain the concrete change first and wait for explicit user confirmation before editing, even if the user has already broadly agreed to continue with the next optimization item.

Use this shape:

1. Name the optimization and point to the relevant file/line when practical.
2. Explain the current behavior in concrete terms.
3. Explain the bug, risk, or maintenance cost it creates.
4. Recommend a specific implementation plan.
5. Call out tradeoffs, behavior changes, or compatibility questions.
6. State the exact next action you will take if the user confirms.

## Optimization Review Order

When scanning a project for optimization or cleanup opportunities, follow an implementation-oriented order: establish constraints first, protect data, fix correctness and user-visible behavior, then improve structure and polish. For each risky item, define validation alongside the change instead of leaving all testing to the end.

- **Compatibility and platform rules**: deployment target, deprecated APIs, permission strings, Info.plist requirements, StoreKit behavior, App Store review risks, accessibility expectations, and privacy/security-sensitive surfaces.
- **Data and persistence safety**: durable storage for user-owned data, migration compatibility, stable IDs, duplicate writes, stale caches, `UserDefaults` key ownership, and cleanup that might delete canonical data.
- **Hidden bugs and edge cases**: array bounds, optional handling, missing resources, permission denial, failed network/file operations, entitlement drift, stale UI state, and inconsistent success/failure flows.
- **User-visible behavior**: taps that do nothing, missing loading or error feedback, stuck UI, duplicated prompts, confusing alerts, inconsistent purchase/restore/rating behavior, and broken external links.
- **Lifecycle and concurrency**: uncancelled tasks, timers, delayed callbacks after a view disappears, broad catch blocks that swallow cancellation, missing `@MainActor`, duplicated requests, and state updates after navigation.
- **Error handling and observability**: actionable user-facing errors, narrow error cases, fallback paths, avoiding silent failure, and keeping debug logging useful but not noisy.
- **Performance**: heavy work in SwiftUI `body`, repeated filtering/decoding, image loading without caching/downsampling, identity churn, layout thrash, unnecessary animations, and leaks from long-lived timers or tasks.
- **Architecture and file responsibilities**: oversized files, mixed UI/business/storage/network concerns, unclear ownership boundaries, global state used where injection would be cleaner, and duplicated logic that should live in one helper/store/service.
- **Dead code and resource cleanup**: unused types, methods, state, imports, previews, debug prints, commented-out blocks, obsolete assets, scripts, test data, and unused project references.
- **Naming and API shape**: names that reveal behavior and ownership, old names that no longer match behavior, loose strings that should be enums, and public methods that expose implementation details.
- **File organization**: domain-based grouping, app bundle hygiene, separation of source/resources/tools/docs, focused helper files, and file-level comments when a file's role is not obvious.
- **Formatting and consistency**: indentation, import cleanup, comment quality, method ordering, line length, and consistency with local style. Keep this lower priority unless it blocks readability or review.
- **Testing and validation**: add focused tests for risky pure logic when the project supports it, pair behavioral changes with manual checks, and finish with targeted builds/tests that match the changed surface.

Default priority order: platform constraints, data safety, correctness, user-visible behavior, lifecycle/concurrency, error handling, performance, architecture, cleanup, naming, file organization, formatting, and targeted validation.

## Architecture And State

Default to a lightweight Model-View style for SwiftUI apps unless the project already uses another architecture.

- Views should be lightweight state expressions. Models, stores, importers, parsers, renderers, and services own behavior.
- Do not add view models by habit. Add a separate controller/store only when it owns real state, side effects, persistence, parsing, or coordination.
- Prefer `@State` for view-owned values and observable objects, `let` for read-only injected observable models, `@Bindable` when a child needs two-way bindings, and `@Environment` for app-wide shared services or stores.
- Mark UI-bound observable stores/classes as `@MainActor`.
- Keep navigation, sheets, selection, and transient UI state near the screen that owns them.
- Inject services through initializers or environment instead of reaching into global state from feature views.
- Use explicit enums for loading, error, render mode, sort order, import state, and reader mode instead of loose strings or parallel booleans.

Use `my-ios-app-swiftui-patterns` for detailed `@Observable`, environment, composition, async loading, and state-ownership guidance.

## File Organization

Use an MVC-style separation unless the existing project clearly uses another convention:

- **Model files** define base data objects and value types, such as `Book`, `User`, `ReadingHistoryEntry`, or app settings structs.
- **View files** define SwiftUI UI only. Keep them declarative and avoid file, parser, or persistence details inside views.
- **Control/helper files** contain observable stores, importers, parsers, formatters, cache managers, and other controller-style logic.

Practical rules:

- Keep `ContentView.swift` small. Use it mainly for top-level composition, navigation, sheets, and environment wiring.
- Split views by feature when a file grows: headers, grids, tiles, settings rows, reader controls, dialogs, and sheets can live in separate files.
- When the source folder around `ContentView.swift` becomes crowded, introduce responsibility-based subdirectories instead of leaving every feature file in one flat directory. Prefer domain/ownership groupings such as `Reader/Reflowable`, `Reader/Selection`, `Reader/Web`, `Library/Grid`, or `Library/Sheets` over arbitrary type buckets when that makes navigation clearer.
- When refactoring or adding features, prefer directory-based isolation for each feature or responsibility instead of appending unrelated types to existing large files. Put reusable app-wide utilities, models, modifiers, and sheets under a `Shared` directory when the project has one, or introduce `Shared/<Concern>` for new cross-feature behavior.
- Keep reusable non-UI behavior in focused helper files, for example `LocalFileImporter`, `BookParser`, `CacheManager`, or `ShareExporter`.
- Add a brief file-level comment only when the file's role, ownership boundary, lifecycle assumptions, or interaction with persistence/rendering/import flows is not obvious from its name and top-level types.
- Keep UI independent from storage paths. Views should render model values and call store/controller methods.
- Avoid mixing app-wide theme tokens directly into feature logic.

## Data And Persistence

- Start with the minimum model fields that support current behavior.
- Store stable identifiers separately from display names. Display names can change; IDs should not.
- Use explicit enums for states, formats, modes, and sort orders instead of loose strings.
- Persist user-owned data under `Application Support` unless the file should be user-visible in `Documents`.
- Keep generated caches, thumbnails, temporary share files, and derived render data separate from canonical user data.
- Prefer JSON persistence for small MVP datasets. Move to SwiftData/CoreData only when querying, migration, relationships, or scale justify it.
- For imported files, store metadata separately from the original managed file so the UI can load quickly.
- For large imported files, store the managed file and lightweight metadata separately. Do not load full document data just to render lists.
- Compute content hashes when duplicate detection matters.
- Treat migrations as product behavior: preserve existing libraries, reading progress, bookmarks, and settings.
- If adopting SwiftData, define schema ownership, migration strategy, preview/test containers, and CloudKit implications before changing persistence.

Use `my-ios-app-swiftdata` when implementing or reviewing `@Model`, `ModelContainer`, `@Query`, migrations, CloudKit sync, or Core Data coexistence.

## Theming

- Define theme modes and component color tokens in a dedicated theme file.
- Keep raw colors out of feature views.
- Add semantic tokens such as `background`, `primaryText`, `secondaryText`, `controlBackground`, `divider`, and `accent`.
- If a screen has a distinct visual language, give it a focused theme type instead of overloading the main app theme.
- Check both light and dark modes for contrast, readability, and white-on-white or black-on-black control failures.

## App Icon And Logo Prompting

When the user asks for an app logo, app icon, or image-generation prompt for an Apple-platform app, produce a prompt that creates the app icon artwork itself, not a mockup of an icon.

Default prompt rules:

- Ask for a square `1024x1024` image suitable for an Apple app icon source asset.
- Ask for the complete image to be the icon artwork, not a logo drawn inside another rounded square, device mockup, app-store card, or presentation scene.
- Use a transparent background when the user wants raw artwork, or a simple neutral background only when the image model cannot output transparency.
- Explicitly say `no text, no letters, no app name` unless the user specifically wants typography.
- Describe one or two core metaphors from the app's actual function, then add visual style, material, lighting, color, and small-size recognizability.
- For macOS menu bar or utility apps, prefer simple, high-contrast silhouettes with one memorable object and one subtle functional detail.
- Avoid decorative complexity that will disappear at small sizes.
- If the project uses Xcode Asset Catalog, tell the user the generated `1024x1024` PNG can be imported as the AppIcon source; do not manually create many icon sizes unless the project requires legacy icon files.

Reusable prompt shape:

```text
Create a polished Apple app icon for “[App Name]”, an app that [one-sentence purpose].

The icon should be a clean, premium [2D/3D/vector] symbol combining [primary metaphor] and [secondary functional detail]. The design should feel native to modern iOS/macOS, professional, readable at small sizes, and directly connected to the app's core use case.

Use a transparent background. The entire image should be the app icon artwork itself, not placed inside a rounded square, not inside a mockup, and not shown on a device. No text, no letters, no app name.

Visual direction:
- central object: [main object]
- subtle detail: [waveform/time marker/document/checkmark/etc.]
- colors: [2-4 color/material notes]
- high-quality render, soft lighting, crisp edges
- centered composition, enough padding around the object
- recognizable at small Dock, Home Screen, Spotlight, and Settings sizes

Output: square 1024x1024 image, transparent background, no rounded-corner background.
```

## SwiftUI UI Guidance

- Prefer SwiftUI-native components such as `Menu`, `Sheet`, `NavigationStack`, `ShareLink`, or `UIActivityViewController` wrappers before building custom controls.
- Use small view structs with clear inputs and callbacks.
- Keep gestures predictable. If tap, long press, drag, and pinch coexist, isolate gesture state and test conflict cases.
- For dynamic grids, compute spacing from the container width and keep fixed item counts stable when the design requires it.
- Use `zIndex`/`ZStack` for overlay controls that should occupy the same visual layer, and hide mutually exclusive overlays instead of stacking them vertically.
- Add animation where layout changes would otherwise feel abrupt, such as deletion, menu appearance, or mode transitions.
- Keep text legible under Dynamic Type, dark mode, and narrow device widths.
- Prefer system controls for settings, menus, pickers, toggles, sharing, and document import unless custom UI materially improves the workflow.
- Keep overlays mutually exclusive and predictable. Reader controls, menus, selection handles, and transient toasts should not fight for the same tap zone.
- Use system symbols and platform conventions before inventing custom controls.

## SwiftUI View Refactoring

- Order view files consistently: environment, immutable inputs, state, non-view computed values, `init`, `body`, view builders, then helper/async methods.
- Extract meaningful dedicated `View` types for non-trivial sections instead of hiding a large screen behind many computed `some View` properties.
- Keep computed `some View` helpers small and local. Move reusable, stateful, or independently meaningful subviews into dedicated types or files.
- Move non-trivial button actions, `.task`, `.onChange`, `.refreshable`, and side effects into named private methods. Keep `body` readable as UI.
- Avoid top-level `if/else` branches that swap the whole root view. Prefer a stable base view with conditional sections, overlays, toolbar items, opacity, or disabled state.
- Do not introduce a view model just to mirror local state or wrap environment dependencies.
- If a SwiftUI view file grows past roughly 300 lines, split it aggressively by user-facing sections or reusable controls.
- Keep behavior intact during refactors unless the user explicitly asks for behavior changes.

## Concurrency Safety

- Preserve behavior while fixing concurrency warnings; prefer the smallest safe isolation change.
- Keep UI state and observable stores on the main actor.
- Do not silence diagnostics with `@unchecked Sendable`, `nonisolated(unsafe)`, or broad `@preconcurrency` imports unless there is a documented reason.
- Move CPU-heavy parsing, thumbnail generation, indexing, and export work off the main actor, then marshal only UI updates back to the main actor.
- Respect task cancellation for imports, network fetches, rendering, search indexing, and export flows.
- Avoid unstructured detached tasks unless the work truly must outlive the calling context.

Use `my-ios-app-swift-concurrency` for strict concurrency diagnostics, `Sendable`, actors, `@MainActor`, task groups, and migration to modern Swift concurrency.

## Performance

- Keep heavy work out of `body`: parsing, sorting, formatting allocation, image decoding, PDF work, HTML generation, and file I/O belong in stores/helpers.
- Stabilize identity in `ForEach`, lists, grids, and reader pages. Never create `UUID()` inside render paths.
- Scope observable state narrowly so unrelated changes do not invalidate large view trees.
- Downsample large images and generated covers before display.
- Cache derived render data separately from canonical user data, with clear invalidation rules.
- Prefer lazy containers for large collections, but make item sizing stable to avoid layout churn.
- Profile release builds on a real device when code review cannot explain jank.

Use `my-ios-app-swiftui-performance` for detailed SwiftUI invalidation, identity, layout, image, and Instruments workflows.

## Accessibility

- Every interactive control needs a useful accessible label; icon-only buttons need explicit labels.
- Prefer real `Button`, `Toggle`, `Slider`, `Picker`, `Menu`, and `TextField` controls so traits and input behavior come for free.
- Custom controls must expose correct traits, values, hints, and adjustable actions where appropriate.
- Tap targets should be at least 44x44 points.
- Support Dynamic Type with adaptive layouts and system fonts where practical.
- Do not convey state by color alone.
- Respect Reduce Motion, Reduce Transparency, Bold Text, and Increase Contrast.
- When sheets, dialogs, or popovers close, restore focus to the triggering control when possible.

Use `my-ios-app-ios-accessibility` for VoiceOver, Voice Control, Switch Control, keyboard access, custom rotors, nutrition labels, and accessibility audits.

## Import, Share, And Files

For local import flows:

1. Let the user choose files with `UIDocumentPickerViewController` or app document-opening support.
2. Copy security-scoped files into app-managed storage before parsing.
3. Compute a content hash and detect duplicates before creating new records.
4. Prefer the source URL filename for the initial display title; fall back to embedded metadata when needed.
5. Detect file type from both extension and content signature when possible.
6. Parse metadata and generate thumbnails/covers in helper/parser files.
7. Save model metadata and refresh the UI through the app store/controller.

For sharing:

- Share a temporary exported copy when iOS APIs or receiving apps require a stable URL/name.
- Put share copies in a dedicated temporary folder so cache cleanup can remove them safely later.
- Do not delete a share file synchronously before the share sheet completes.

## Reader Rendering Surfaces

- Pick the narrowest rendering surface that matches the document format and required interactions.
- Use native SwiftUI for app chrome, library screens, settings, and simple text experiences.
- Use PDFKit for PDF display, navigation, search, selection, thumbnails, and annotations.
- Use WebKit for app-owned HTML, EPUB-style reflowable rendering, JavaScript-backed layout, or custom local URL schemes.
- Keep renderer-specific state behind a focused adapter/helper so feature views do not depend on file paths, raw HTML, or PDF internals.
- Preserve reading progress with stable document identifiers and renderer-specific positions.
- Avoid mixing multiple renderers in one view unless there is a clear abstraction boundary.

Use `my-ios-app-pdfkit` for PDF-specific implementation and `my-ios-app-swiftui-webkit` for WebKit or app-owned HTML rendering.

## Testing

- Add tests when changing parsers, persistence, migration, duplicate detection, progress tracking, search, export, or renderer adapters.
- Prefer Swift Testing for new unit tests in modern Swift projects.
- Keep XCTest for UI tests, performance tests, and snapshot test infrastructure when the project already uses it.
- Test model/helper behavior more than view structure.
- Use in-memory stores and temporary directories for persistence tests.
- After adding or modifying a feature, first run the relevant existing tests. If they fail, fix the issue or update obsolete tests before adding new coverage. If they pass, evaluate whether focused tests should be added or updated, and prefer adding them whenever practical; if new tests are skipped, note the reason.
- Include at least one regression test for bug fixes that touch data loss, import, deletion, or reading progress.

Use `my-ios-app-swift-testing` for `@Test`, `#expect`, `#require`, async tests, migration from XCTest assertions, and modern test organization.

## Settings And Maintenance

- Keep settings screens independent from feature views.
- Group settings by user intent, not implementation detail.
- Put cache cleanup behind a clear confirmation sheet/action.
- Cache cleanup should delete derived or temporary data only, not canonical user data.
- When adding external links or app URL schemes, update `Info.plist` only for schemes actually used by `canOpenURL`.
- Make destructive actions explicit, reversible where practical, and scoped to the selected data.
- Keep diagnostics, debug toggles, and maintenance actions out of the main reading flow.

## App Store Metadata And ASO

- Treat App Store metadata as a product surface: app name, subtitle, keywords, promotional text, description, screenshots, previews, and positioning should match the current app behavior.
- Ground ASO recommendations in user intent and competitor evidence when available; call out when a draft is based only on provided context.
- Use `my-ios-app-aso` for App Store metadata generation, competitor analysis, keyword strategy, localized listing copy, screenshot messaging, and ASO review notes.

## Release Notes

- Generate release notes from actual git history, tags, or an explicit ref range.
- Keep App Store copy user-facing: describe visible benefits and fixes, not internal commits, refactors, CI, or dependency churn.
- Every release note bullet should map back to a real change in the selected range.
- Prefer concise bullets grouped by user value when the release has many changes.

Use `my-ios-app-store-changelog` for App Store "What's New", TestFlight notes, and user-facing changelog generation.

## Specialized Skill Routing

- Use this skill first for app-level direction, code organization, and implementation posture.
- Use `my-ios-app-swiftui-patterns` for detailed SwiftUI state, environment, composition, and app structure.
- Use `my-ios-app-swift-concurrency` for strict concurrency diagnostics, actors, `Sendable`, and task behavior.
- Use `my-ios-app-swift-testing` for Swift Testing syntax, XCTest migration, and test design details.
- Use `my-ios-app-swiftui-performance` for SwiftUI jank, invalidation, identity churn, layout thrash, and profiling.
- Use `my-ios-app-ios-accessibility` for accessibility implementation or audits.
- Use `my-ios-app-swiftdata` for SwiftData/Core Data persistence details.
- Use `my-ios-app-pdfkit` for PDF rendering, search, thumbnails, annotations, and SwiftUI wrapping.
- Use `my-ios-app-swiftui-webkit` for WebKit-backed HTML, EPUB-style rendering, JavaScript, local content, or custom URL schemes.
- Use `my-ios-app-aso` for App Store metadata, ASO competitor analysis, keyword strategy, localized listing copy, and screenshot messaging.
- Use `my-ios-app-store-changelog` for App Store "What's New", TestFlight notes, or release changelog copy.

## Validation

Choose the narrowest validation command that matches the project shape and requested change:

```bash
# Swift package
swift test

# Xcode workspace
xcodebuild -workspace <AppName>.xcworkspace -scheme <SchemeName> -destination generic/platform=iOS -derivedDataPath /private/tmp/<SchemeName>_derived CODE_SIGNING_ALLOWED=NO build

# Xcode project
xcodebuild -project <AppName>.xcodeproj -scheme <SchemeName> -destination generic/platform=iOS -derivedDataPath /private/tmp/<SchemeName>_derived CODE_SIGNING_ALLOWED=NO build
```

- Prefer a workspace build when both `.xcworkspace` and `.xcodeproj` exist.
- Use a generic iOS destination to avoid simulator availability issues.
- For test-only changes, run the affected test target or package tests when practical.
- If the sandbox blocks Swift preview macros or Xcode plugin tooling, rerun the same command with approval outside the sandbox.
