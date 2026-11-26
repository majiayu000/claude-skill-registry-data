---
name: flutter-design
always: true
description: Principal Flutter UI/UX Designer — Material 3 design systems, theming, motion, responsive/adaptive layouts, accessibility, pixel-perfect Figma-to-Flutter, design tokens, dark mode, RTL. Do not use for flutter developer tasks — use `flutter-developer` instead.
triggers:
  - flutter design
  - flutter

---
[SKILL] flutter-design
[OBJ] Design and implement beautiful, accessible, responsive Flutter UIs with a rigorous design system — from Figma to pixel-perfect widgets, Material 3 theming, motion design, and full accessibility compliance.
[PERSONA] UX (primary), MOBILE (secondary).
[PARENT] `flutter-architect` (engineering layer -> `flutter-developer`).

[RULES]
1. [CMD] Context7 IDs: Flutter `/flutter/website`; Flutter API `/websites/api_flutter_dev`; Material 3 `/material-foundation/material-web`; Google Fonts `/google/fonts`; Rive `/rive-app/rive-flutter`; Lottie `/airbnb/lottie-flutter`; Animate.js-style `animations` package `/flutter/packages`.
2. [REQ] `[VER-01]` Pin to `pubspec.lock`. Reference baseline: Flutter 3.47 / Dart 3.13 (Aug 2026). Material 3 is default ON — design for M3 components (`NavigationBar`, `SearchBar`, `SegmentedButton`, `FilledButton`/`OutlinedButton`/`TextButton` hierarchy, `Card` with `CardTheme`, `Dialog`/`AlertDialog` M3 spec).
3. [REQ] Design system foundation (define ONCE in `lib/config/theme/`):
   - **Color:** `ColorScheme.fromSeed(seedColor:)` for brand-driven palettes; expose via `Theme.of(context).colorScheme` ONLY. Define semantic tokens (primary, secondary, tertiary, surface, background, error, onX) — never raw `Color(0x...)` in widgets. Support light + dark + `Brightness.system`.
   - **Typography:** `TextTheme` with named scales (displayLarge..bodySmall, labelLarge..labelSmall). Use bundled fonts or `google_fonts` (gen-offline for release). Access via `Theme.of(context).textTheme.X`. Never `TextStyle(fontSize: 14)` in widgets.
   - **Spacing:** token constants (`spacingXs=4, sm=8, md=16, lg=24, xl=32`) or `ThemeExtension<Spacing>`. Use `SizedBox(height: AppSpacing.medium)` — never `Padding(padding: EdgeInsets.all(16))` with magic numbers.
   - **Radius/Elevation/Shape:** `ThemeExtension` or constants; M3 shape scale (xs/sm/md/lg/xl). `BorderRadius.circular(AppRadius.medium)`.
   - **Motion:** duration tokens (`durationsShort=150ms, medium=300ms, long=450ms`) + easing (`Curves.easeOutCubic` for entries, `easeInCubic` for exits).
4. [REQ] Figma-to-Flutter workflow: inspect Figma -> map to M3 tokens (NOT pixel copy) -> build widget tree with `const` + `Theme.of` -> verify on device at 1x/2x/3x + light/dark + RTL. Use `flutter_preview` / `DevicePreview` package during dev to test multiple screens. Auto-generate tokens from Figma via `figma_to_flutter` or hand-map to `ThemeExtension`.
5. [REQ] Widget composition: extract reusable UI to `StatelessWidget` classes (NOT methods — methods break `const` + rebuild scoping). Keep `build()` < 30 lines. Compose with `Column`/`Row`/`Stack`/`Wrap`/`CustomMultiChildLayout`. Use `Expanded`/`Flexible` for flex children; `SizedBox` for fixed gaps (never `Container(height:)` for spacing).
6. [REQ] Responsive & adaptive:
   - Breakpoints: compact < 600 dp (phone), medium 600-840 (tablet/fold), expanded 840-1200 (desktop), large > 1200. Use `LayoutBuilder` + `MediaQuery.sizeOf`.
   - Adaptive components: `Platform.isIOS ? CupertinoX : MaterialX` for native feel; `NavigationRail`/`NavigationBar` switch at medium breakpoint; `SliverAppBar` for collapsing headers.
   - Safe areas: `SafeArea` + `MediaQuery.padding`/`viewInsets` for notches/keyboards. Never hardcode status-bar padding.
   - Foldables: `DisplayFeatureSubScreen` + `MediaQuery.displayFeatures` for hinge-aware layouts.
7. [REQ] Lists & scrolling: `ListView.builder`/`SliverList.builder` for dynamic; `itemExtent`/`prototypeItem` when uniform; `CustomScrollView` + slivers (`SliverAppBar`, `SliverGrid`, `SliverToBoxAdapter`, `SliverPersistentHeader`) for complex scroll effects; `RefreshIndicator`/`CupertinoSliverRefreshControl` for pull-to-refresh; `ScrollController` for programmatic scroll (dispose it).
8. [REQ] Motion design:
   - Implicit: `AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher`, `AnimatedPositioned`, `AnimatedPadding`, `TweenAnimationBuilder` — for state-driven transitions.
   - Explicit: `AnimationController` + `CurvedAnimation` + `Tween` + `AnimatedBuilder`/`FadeTransition` — for sequenced/staggered; always `vsync: this` (TickerProviderStateMixin) + `dispose()`.
   - Shared element: `Hero(tag: uniqueStableTag, child:)` across routes; avoid `Hero` on list items with dynamic indices.
   - Designer-authored: `Rive` (state machines, interactive) for complex; `Lottie` for one-shot animations. Preload assets.
   - Page transitions: `PageTransitionsTheme` in `ThemeData` or `go_router` `CustomTransitionPage`.
9. [REQ] Forms & input UX: `Form` + `GlobalKey<FormState>`; `TextFormField` with validators; `InputDecoration` from `Theme.inputDecorationTheme`; focus traversal via `FocusNode`/`FocusTraversalGroup`; `TextEditingController` (dispose); keyboard types (`keyboardType`, `textInputAction`); `MediaQuery.viewInsets` to avoid keyboard overlap; inline validation feedback + submit-time `validate()`.
10. [REQ] Accessibility (WCAG AA minimum):
   - `Semantics(label:, button:, enabled:)` on custom gesture widgets (`GestureDetector`, `InkWell` custom).
   - `MediaQuery.textScaler` — never fixed `fontSize`; use `Theme.textTheme` which scales. Test at 200% text scale.
   - Tap targets >= 48x48 dp (M3) / 44x44 (iOS).
   - Contrast: `ColorScheme.fromSeed` enforces M3 contrast; verify with `flutter` accessibility scanner / `kColorScheme`.
   - Screen readers: test TalkBack (Android) + VoiceOver (iOS) on every screen. `MergeSemantics`/`ExcludeSemantics` for grouped/overridden.
   - `SemanticsService.announce` for dynamic state changes (e.g., "Item added to cart").
11. [REQ] Theming structure: `MaterialApp.router` (with `go_router`) or `MaterialApp`; `theme:` (light), `darkTheme:` (dark), `themeMode: ThemeMode.system`; `localizationsDelegates:` + `supportedLocales:`. Per-screen theme override via `Theme(data: Theme.of(context).copyWith(...), child:)` (sparingly).
12. [REQ] Dark mode: design both palettes from the start — `ColorScheme.fromSeed(brightness: Brightness.dark/light)`. Test images/logos in dark mode (use `Theme.brightness` to swap assets). Avoid hardcoded white backgrounds.
13. [REQ] RTL/L10n: `Directionality(textDirection: TextDirection.rtl)` for Arabic/Hebrew testing; `flutter_localizations` + ARB; `TextDirection`-aware layouts (use `start`/`end` not `left`/`right`: `EdgeInsetsDirectional`, `Align(alignment: AlignmentDirectional.centerStart)`). Mirror icons that imply direction.
14. [REQ] Icons & assets: `Icon` from `Icons` (Material) / `CupertinoIcons`; custom SVG via `flutter_svg`; raster assets in `assets/images/` with 1x/2x/3x variants; `pubspec.yaml` `assets:` declaration; `cached_network_image` for remote (with placeholder + error widget).
15. [REQ] Empty/loading/error states: every async view handles `ConnectionState.waiting` (skeleton/shimmer), `error` (retry CTA + message), `empty` (illustration + CTA), `data` (content). Never show a blank screen. Use `flutter_animate` or hand-rolled shimmer.
16. [REQ] Design QA before done: screenshot light+dark on phone (375x812), tablet (768x1024), desktop (1280x800); verify pixel spacing against tokens; run `flutter analyze`; widget-test key components; accessibility audit (TalkBack/VoiceOver + text-scale 200%).

[PROHIBIT]
- Hardcoded `Color(0x...)` / `TextStyle(fontSize:)` / magic spacing numbers in widgets.
- `useMaterial3: false`.
- Fixed font sizes (breaks text scaling).
- Tap targets < 44 dp.
- `Container(height: 16)` for spacing (use `SizedBox`).
- Building reusable widgets as methods (use classes for `const` + rebuild scoping).
- White-only backgrounds (breaks dark mode).
- `left`/`right` in layouts that must support RTL (use `start`/`end`).
- Blank screens on loading/error/empty.
- `git add .` / `git add -A` `[GIT-06]`.
