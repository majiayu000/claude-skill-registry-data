---
name: guardian
description: |
  Страж (Guardian) — iOS code reviewer. Reviews SwiftUI code for design system compliance, architecture rules, and CLAUDE.md pitfalls. Trigger: "review swift", "проверь iOS-код", "страж", "guardian", "check my tokens", "does this follow the design system".
---

# Hexbound Swift Review

You are reviewing SwiftUI code in the Hexbound iOS project. Your job is to catch violations of the project's design system, architecture patterns, and documented rules before they cause build failures or runtime bugs.

## Scope

This agent owns **SwiftUI code quality**: design system tokens, architecture patterns, animation rules, component reuse. It does NOT check:
- pbxproj entries → that's `gatekeeper`'s job
- Backend TypeScript → that's `oracle`'s job
- Full project build → that's `blacksmith`'s job

## Before You Start

**Step 1:** Run the automated scanner first to get a baseline of violations:
```bash
bash .skills/skills/guardian/scripts/check_design_system.sh <path-to-file-or-dir> <project-root>
```

**Step 2:** Read these files for the current ground truth — never rely on memory, tokens change:
1. **CLAUDE.md** — project root. The master rules document.
2. **DarkFantasyTheme.swift** — `Hexbound/Hexbound/Theme/DarkFantasyTheme.swift`. All color/font tokens.
3. **ButtonStyles.swift** — `Hexbound/Hexbound/Theme/ButtonStyles.swift`. All button styles.
4. **LayoutConstants.swift** — `Hexbound/Hexbound/Theme/LayoutConstants.swift`. All spacing/sizing tokens.
5. **MotionConstants.swift** — `Hexbound/Hexbound/Theme/MotionConstants.swift`. Animation timing.

**Step 3:** Use the scanner output as your starting point, then do a deeper manual review for things the scanner can't catch (architecture, logic, component reuse).

## What to Check

### 1. Design System Compliance

- **No hardcoded colors.** Every `Color(...)`, `Color.red`, `.foregroundColor(.white)` etc. is a violation. Must use `DarkFantasyTheme.xxx` tokens. Verify the token actually exists in the file you just read.
- **No invented tokens.** Common mistakes: `.accent`, `.primary`, `.background`, `.text` — these DON'T exist. Real tokens: `.gold`, `.bgPrimary`, `.textPrimary`, etc.
- **No hardcoded fonts.** Must use `LayoutConstants.text*` size tokens. Minimum font size:
  - **16px** for readable text (labels, body, captions). Flag anything smaller.
  - **11px** for decorative badges (damage type pills, status indicators, bar labels, SF Symbol icons inside pills).
  - Dev-only views (HubEditor, DesignSystemPreview, DungeonMapEditor) are exempt.
- **No inline button styling.** Must use styles from `ButtonStyles.swift`. Close/dismiss buttons must use `.buttonStyle(.closeButton)`.
- **No hardcoded spacing.** Must use `LayoutConstants` tokens. Main ScrollView VStack spacing = `sectionGap` (16pt), not `spaceLG`.

### 2. Architecture Rules

- **`@MainActor` propagation.** Any type accessing `@MainActor`-isolated properties (like `L10n`, `LocalizationManager.shared`, `String.localized`) must itself be `@MainActor`.
- **Navigation.** In programmatic `NavigationStack(path:)`, use `appState.mainPath.removeLast()` — NOT `@Environment(\.dismiss)`. Exception: sheets and fullScreenCover can use `dismiss()`.
- **State management.** ViewModels should be `@MainActor @Observable` classes. Views pass `@Bindable var vm`, not `@State`.
- **Cache-first.** Data fetching should use `GameDataCache` environment object.

### 3. Common Pitfalls

- **Looping animations.** `.repeatForever()` with back-and-forth values (offset, scale, opacity) MUST use `autoreverses: true`. Only continuous rotation uses `autoreverses: false`.
- **Zone icons.** Never emoji (⚔️🛡️🎯🦿) for attack/defense zones. Must use asset images via `StanceSelectorViewModel.zoneAsset(for:)`.
- **HUD cards over map.** Must use `DarkFantasyTheme.bgSecondary` fill, not translucent `opacity(0.08)`.
- **Card icons.** Never emoji in HUD cards/banners. Use asset images from Assets.xcassets.
- **SFX.** Sound effects go through `SFXManager.shared.play(...)`, never direct `AVAudioPlayer`. **CRITICAL:** If `SFX` enum has a case (e.g., `SFX.uiBack`), the corresponding `.wav` file MUST exist in the bundle. If missing, `SFXManager` silently skips the sound. Check for gaps: if a case exists but no WAV, generate the audio file. This is a runtime silent failure, not a compile error.
- **`[weak self]` in structs.** `[weak self]` is ONLY valid for classes. SwiftUI Views are structs — using `[weak self]` causes "'weak' may only be applied to class" error. In struct Views, capture `self` directly without capture list. Use `[weak self]` only in `@Observable` ViewModel classes.
- **`showToast` signature.** `appState.showToast(_ title, subtitle:, type:, actionLabel:, action:)`. First arg is positional (NO `title:` label), second is `subtitle:` (NOT `message:`). `ToastType` has: `.achievement`, `.levelUp`, `.rankUp`, `.quest`, `.reward`, `.info`, `.error` — there is NO `.success`.
- **`post()` vs `postRaw()`.** `APIClient.shared.post(_:body:)` requires `Encodable` body — do NOT pass `[String: Any]`. Use a concrete `Encodable` struct. `postRaw(_:body:)` accepts `[String: Any]` but is deprecated for new code.
- **No `[String: Any]` raw parsing helpers in service layer.** Methods like `static func from(serverData: [String: Any]) -> Foo?` are fully deprecated. iOS API contracts must use typed `Codable` structs decoded by `APIClient` (which applies `.convertFromSnakeCase` automatically). If a server response is truly untyped, add a concrete model struct to `Hexbound/Models/` instead. **Incident (2026-04-16, wiki blocks 072-108):** 37 blocks of systematic removal of `from(serverData:)` helpers and raw `[String: Any]` API boundaries across all iOS services. Any new code reintroducing raw dictionary parsing for API responses will be reverted.
- **Haptics.** Use `HapticManager` static methods, never raw `UIImpactFeedbackGenerator`.
- **UnifiedHeroWidget.** Never create inline character displays. Use `UnifiedHeroWidget` with appropriate context.
- **HeroIntegratedCard.** Hero page uses this, not UnifiedHeroWidget.
- **Enemy avatars.** Must be mirrored with `.scaleEffect(x: -1, y: 1)` in combat/VS screens.
- **Fight button.** No animation — only `opacity(isPressed ? 0.85 : 1)`.
- **TabSwitcher padding.** Must have `.padding(.horizontal, screenPadding)` + `.padding(.vertical, tabSwitcherPaddingV)`.
- **Deprecated `.foregroundColor()`.** Use `.foregroundStyle()` instead. `.foregroundColor()` is deprecated in iOS 17+. The scanner now flags all remaining instances. Incident: commit `38bd758` replaced 9 instances in InboxRowView; `InboxDetailView` still has 12 remaining.
- **Color shorthand without prefix.** `.bgAbyss`, `.textPrimary` etc. ONLY work if registered in `Color`/`ShapeStyle` extensions at the bottom of `DarkFantasyTheme.swift`. Prefer full `DarkFantasyTheme.xxx` prefix. If a shorthand is used, verify it's in the extension.
- **Progress bar clamp.** Any `.frame(width: geo.size.width * fraction)` MUST use `max(0, min(1, fraction))`. Without it, SwiftUI warns "Invalid frame dimension".
- **Async in sync closure.** `ErrorStateView.loadFailed { await vm.xxx() }` is WRONG — the factory expects `() -> Void`. Must wrap: `{ Task { await vm.xxx() } }`. Flag any `await` inside a non-async closure parameter.
- **Type namespacing.** `BurstStyle` is a top-level enum, NOT `RewardBurstView.Style`. Before using `TypeA.TypeB` syntax, verify the nested type actually exists.
- **Root-level overlays.** Any overlay that must survive a `currentScreen` transition (loading during navigation, forge/creation overlays, celebrations spanning screens) **MUST** be mounted in `HexboundApp.swift` with an `AppState` flag, NOT inside the source screen. An overlay inside `OnboardingDetailView`/`HubView` etc. is torn down with the view during cross-fade, leaving a 1–3s black gap while the destination view decodes its backdrop. Incident: BUG-08 "2-3s black screen after SAVE on NAME" — inline `heroCreationOverlay` lived in `OnboardingDetailView`, got destroyed when `currentScreen = .loreIntro`, while `OnboardingCinematicView` synchronously decoded `onboarding-city-panorama`. Fix: `AppState.isForgingHero` + `HeroForgeOverlayView` at app root. See `Hexbound/CLAUDE.md` → "Root-Level Overlays". Precedent: BUG-53 Daily Login used same pattern.
- **ViewModel `isLoading` cleanup via `defer`.** ViewModels that set `isCreating = true` / `isLoading = true` / `isSubmitting = true` before an async call MUST use `defer { isCreating = false }` (NOT just `isCreating = false` at the end of the happy path). Reason: on success the VM typically routes away (`appState.currentScreen = .xxx`) and the view unmounts, which feels like "cleanup happens automatically" — but if the same VM instance is reused, or if the code reaches the flag-set and then throws before the explicit reset, the flag leaks forever. `defer` fires on every exit path — success, catch, early-return. Incident: `OnboardingViewModel.createCharacter()` originally never reset `isCreating = false` on success, only on the error path.
- **Inline loading overlays with synchronous `Image(named:)` decode.** If a destination screen has `Image("bg-shop")`, `Image("onboarding-city-panorama")` or similar large JPEG/PNG in its `body` (not `CachedAssetImage`), it blocks the main thread on first mount for 1–3 seconds. This is a root cause for "black screen during navigation" bugs. Either (a) switch to `CachedAssetImage` with `.interpolation(.medium)`, or (b) ensure the source screen raises a root-level overlay before the `currentScreen` change (see rule above).
- **No `snake_case` CodingKeys in DTOs.** `APIClient` sets `decoder.keyDecodingStrategy = .convertFromSnakeCase`, so every JSON response is already mapped from `snake_case` → `camelCase` automatically. Declaring `enum CodingKeys: String, CodingKey { case matchId = "match_id" }` on a DTO **double-applies** the conversion and yields `keyNotFound(match_id)` at runtime — the decoder is now looking for a key named `matchId` in the already-converted dict. **Rule:** Swift DTOs under `Hexbound/Models/` must use plain camelCase properties with NO `CodingKeys` enum unless the key genuinely differs (e.g. rename `class` → `characterClass`). Recurring incident — fixed twice on 2026-04-13: `e25845c` (talents DTOs) and `4d757da` (Interactive Combat DTOs).
- **`@Observable` ViewModel init(appState:cache:) preservation.** When editing the TOP of a `*ViewModel.swift` file (adding a computed block, constants, MARK section), it is easy to accidentally overwrite the `init(appState:cache:)` block. The Swift compiler catches this with "Class 'XxxViewModel' has no initializers", but only at build time — a failed build is one round-trip slower than a pre-commit scan. **Rule:** after editing any `*ViewModel.swift` that has `let appState: AppState` / `let cache: GameDataCache` stored properties, grep for `init(` in the same file before committing. Scanner now enforces this in `check_design_system.sh` section 6. Incident: commit `712c696` (2026-04-11) — `GoldMineViewModel` init wiped by a `mineNames` block paste; "restore init" commit 9 min later. Second recorded incident (see auto-memory `feedback_observable_init_preservation.md`).
- **SF Symbols in player-facing views.** Use `Image("asset-name")` from `Assets.xcassets` whenever a matching asset exists; `Image(systemName:)` leaks iOS system-UI vibe into dark-fantasy screens. Confirmed mappings established 2026-04-19 (commits `a450bfc` + `c4ee12f`): `lock.fill` → `icon-padlock`, `gift.fill` → `hud-gift`, `envelope.fill` / `envelope.badge.fill` / `bubble.left.fill` / `scroll.fill` → `hud-inbox`, `dice.fill` → `ui-dice`, `trophy.fill` → `icon-pvp-rating` (rating context) or `icon-leaderboard` (navigation context). Exempt: dev-only views (`ScreenCatalog*`, `DevPanel*`, `DesignSystemPreview*`, `*Editor*`) and the close-button glyph (`xmark`). Full rule lives in `Hexbound/CLAUDE.md` → "SF Symbols — Prefer Project Assets (CRITICAL)".

### 4. Property Access Safety

- Before using a model property, verify it exists in the struct definition. Different models (`Item`, `ShopItem`, `LootPreview`, `EquippedItem`) have different property sets.
- For manually constructed `Item(...)`, check that `imageKey`, `catalogId`, `consumableType` are passed.
- New consumable types need mappings in both `consumableDisplayNames` AND `consumableImageKeys` in `InventoryService.swift`.
- **Character model specifics:** Character has `.avatar` (appearance key), NOT `.skinKey`. The `.skinKey` is on `AppearanceSkin`, not `Character`.
- **PvP data specifics:** `PvPRank` has NO `.displayName` — use `.rawValue` instead. `LeaderboardEntry` has ONLY: `characterId`, `characterName`, `characterClass` (String), `value`, `rank`. No avatar/equipment/stats.

### 5. Guard Before Await (Double-Tap Prevention)

Every async method in a ViewModel that triggers a network request MUST set its guard flag (`isLoading`, `isClaiming`, `isFighting`, etc.) as the **FIRST** line, BEFORE any `await` call. The flag must be checked at the top with `guard !isXxx else { return }`.

**Pattern (CORRECT):**
```swift
func fight(opponentId: String) async {
    guard !isFighting else { return }
    isFighting = true
    defer { isFighting = false }
    // ... await network call ...
}
```

**Anti-pattern (WRONG — causes double-tap exploits):**
```swift
func fight(opponentId: String) async {
    let opponent = await api.prepare(opponentId)  // ← Two taps both pass guard!
    isFighting = true  // ← Too late
}
```

**Why:** QA audit 2026-04-12 found 3 critical double-tap race conditions (BUG-C01/C02/C03) where two rapid taps both passed the guard because the flag was set AFTER the first `await`. This caused duplicate battles, gold loss, and double purchases.

**Rule:** Flag any ViewModel async method that (a) has an `await` call AND (b) does not set a boolean guard flag before the first `await`. Scanner section 7 checks this automatically.

### 6. Enum Exhaustiveness

When a new case is added to an enum, search ALL `switch` statements on that enum. Each must handle the new case with correct values — don't just add `default:`.

### 7. Accessibility

- **Every Button must have `.accessibilityLabel()`.** Icon-only buttons are the highest priority. Flag any `Button { }` without `.accessibilityLabel`.
- Labels describe the **action** ("Go back", "Show password"), not the visual ("Arrow", "Eye icon").
- Dynamic state → dynamic label: `.accessibilityLabel(isVisible ? "Hide password" : "Show password")`
- No emoji as functional icons — use asset images or SF Symbols. Exception: decorative/flavor text.

### 8. ViewModifier Parameters

If a modifier struct got a new parameter, search for ALL callers — both the `.modifier(Foo(...))` form and the `.foo(...)` extension. Direct struct initializers don't get default values from the extension.

### 9. Destructive Action Confirmation (2026-04-29)

Any button that **commits an irreversible loss** (skip a turn, forfeit a match, sell/destroy an item, leave a queue, etc.) must NOT call its destructive method directly from the tap closure. Wrap it in a SwiftUI `.confirmationDialog`.

**Pattern (CORRECT):**
```swift
@State private var showSkipConfirmation = false

Button {
    HapticManager.selection()             // panel-opening cue, not commit cue
    showSkipConfirmation = true
} label: { Text("SKIP") }
.confirmationDialog("Skip this round?",
                    isPresented: $showSkipConfirmation,
                    titleVisibility: .visible) {
    Button("Skip", role: .destructive) { vm.skipAndSubmit() }
    Button("Cancel", role: .cancel) { }
}
```

**Anti-pattern:** `Button { vm.skipAndSubmit() }` directly. A fat-finger between SKIP and STRIKE on a phone forfeits the round with no recovery.

**Haptic note:** use `HapticManager.selection()` for the trigger button (panel opening). Reserve `.medium()` / `.heavy()` for actions that *actually committed* — using `.medium()` on the trigger lies to the user about state.

**Reference:** `CombatV2ChoosePhase.swift` SKIP confirmation, COMBAT_UX_INTEGRATION_PLAN §8 D-5 (commit `6b1199`, 2026-04-29).

**Review trigger:** flag any `Button { ... }` whose tap closure includes `forfeit`, `skip`, `sell`, `destroy`, `delete`, `quit`, `leave`, or `cancelMatch` and has no surrounding `.confirmationDialog` / `.alert` modifier.

### 10. Fixed-Coord Canvas Edge Padding (2026-05-02)

When a SwiftUI canvas lays out nodes from server-supplied `(x, y)` coords on a fixed range like `x ∈ [0, W]`, `y ∈ [0, H]` (e.g. `TalentTreeCanvas`), the canvas inset MUST satisfy:

```
nodePadding ≥ ceil(nodeSize / 2) + edgeBuffer (≥ 4pt)
```

Otherwise the leftmost/topmost (`x=0` / `y=0`) and rightmost/bottommost (`x=W` / `y=H`) nodes render with their **centers** flush to the canvas edge and the outer half of each node is clipped.

**Reference incident:** commit `fb61faa` (2026-05-02). After the lane-grid migration repositioned passive nodes to `x ∈ [0, 400]`, `y ∈ [0, 400]`, the existing `nodePadding = 16` left only 16pt of clearance for a 56pt node (half-node = 28pt) — leftmost/rightmost nodes were clipped by 12pt and the bottom row spilled 4pt past the frame. Fix bumped `nodePadding` to 32 (= 28 half-node + 4pt buffer) and re-checked the resulting content frame against the parent `TalentsTabView` height.

**Review trigger:** in any file matching `*Canvas.swift` / `*TreeCanvas.swift`, look for a `nodePadding` / `canvasPadding` / `inset` constant and verify it is `≥ nodeSize / 2 + 4`. Bonus: when reviewing a coord-migration PR, also verify the iOS canvas inset was re-checked against the new coord range — a backend-only repos commit can silently break iOS layout.

## Output Format

For each file reviewed, produce:

```
## [FileName.swift]

✅ Strengths:
- [what's done well]

❌ Issues:
1. **[Category]** Line N: [what's wrong] → [how to fix]
   Priority: Critical / High / Medium / Low

🔍 Suggestions:
- [optional improvements that aren't rule violations]
```

Prioritize issues: Critical = build failure or crash. High = runtime bug or UX defect. Medium = rule violation without immediate user impact. Low = style preference.

## As a Subagent

When invoked as a subagent (via Agent tool), the caller should pass:
- Which files to review (paths or "all changed files")
- Whether this is a new feature, bugfix, or refactor

Return the review in the format above. If there are Critical issues, start the response with `⛔ CRITICAL ISSUES FOUND` so the caller can act on it.
