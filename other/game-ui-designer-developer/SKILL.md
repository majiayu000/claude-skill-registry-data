---
name: game-ui-designer-developer
description: Master Enterprise & AAA Game UI/UX Design, Architecture, Performance, Shaders & Technical Art Suite - Complete framework covering Diegetic/Spatial UI, FSM Canvas Navigation, Spring Juice Buttons, Responsive Layout & Safe Area, UGUI vs UI Toolkit zero-GC optimization, Dynamic HUD & Damage Text Pools, Glassmorphism Shaders, and Localization/Colorblind Accessibility.
user-invocable: true
---

# Game UI/UX Designer & Developer - Master AAA Game Interface Suite

This skill provides a standardized, production-grade Game UI/UX architecture, shader suite, and technical art framework for AAA & Enterprise mobile/3D games. It encapsulates 8 deep-research master documents into modular sub-commands.

---

## ⚡ QUICK COMMAND REFERENCE

| Command | Focus Module | Primary Reference Document |
|---|---|---|
| `/game-ui-paradigm` | AAA UI Paradigms (Diegetic, Spatial), Color Theory & SDF Typography | [`game_ui_ux_paradigms_and_visual_hierarchy.md`](researches/game_ui_ux_paradigms_and_visual_hierarchy.md) |
| `/game-ui-arch` | FSM Layered Canvas & Stack Modal Navigation & Focus Graph | [`game_ui_architecture_and_navigation_fsm.md`](researches/game_ui_architecture_and_navigation_fsm.md) |
| `/game-ui-button` | 7-State Button Lifecycle, Spring Micro-Interactions, Haptics & Audio | [`button_systems_micro_interactions_and_juice.md`](researches/button_systems_micro_interactions_and_juice.md) |
| `/game-ui-responsive` | Device Safe Area Notch Inset, Aspect Ratio Adapters & Layout Math | [`responsive_layout_safearea_and_multi_device.md`](researches/responsive_layout_safearea_and_multi_device.md) |
| `/game-ui-perf` | UGUI vs UI Toolkit, Canvas Splitting, SpriteAtlas & Zero-GC TMP | [`ugui_vs_ui_toolkit_and_performance_optimization.md`](researches/ugui_vs_ui_toolkit_and_performance_optimization.md) |
| `/game-ui-hud` | Speedometer, World-Space Damage Pools, Off-screen Pins & DOTween | [`dynamic_gameplay_hud_and_worldspace_ui.md`](researches/dynamic_gameplay_hud_and_worldspace_ui.md) |
| `/game-ui-shader` | Glassmorphism Blur, Glowing Outline, Procedural Corners & Holograms | [`game_ui_shaders_and_technical_art.md`](researches/game_ui_shaders_and_technical_art.md) |
| `/game-ui-a11y` | Unity Localization, CJK/RTL Layout, Colorblind Shaders & UI Auditors | [`localization_accessibility_and_ui_auditing.md`](researches/localization_accessibility_and_ui_auditing.md) |

---

## 🚀 CARDIV STANDARDIZED UI PRODUCTION SCRIPTS

Cardiv's production-ready, zero-bug UI architecture is implemented across the following C# scripts:
These scripts live in the game project (not in this skill repository) under `Assets/Cardiv/Scripts/UI/`:
- **Layout & Safe Area Engine**: `Layout/SafeAreaPanel.cs`
- **Navigation Stack Router**: `Navigation/UIManager.cs` & `Navigation/IUIScreen.cs`
- **Design Tokens System**: `Styling/UIThemeConfig.cs` & `Styling/UIStyleApplier.cs`
- **Atomic Widgets**: `Widgets/ScoreWidget.cs`, `Widgets/ComboWidget.cs`, `Widgets/PauseFABWidget.cs`, `Widgets/OilHazardWidget.cs`

---

## 1. /game-ui-paradigm - AAA UI Paradigms, Color Theory & SDF Typography

### Core Design Rules:
1. **4 UI Paradigms**:
   - **Diegetic**: In-world UI integrated into geometry (e.g. `MaterialPropertyBlock` mesh health bar).
   - **Non-Diegetic**: Screen-space HUD overlays decoupled from world physics.
   - **Spatial**: 3D world-space markers projected to screen coordinates with frustum and depth check.
   - **Meta**: Fourth-wall interfaces (in-game smartphone, glitching HUD, render texture monitors).
2. **Color Theory & Accessibility**:
   - WCAG 2.1 AAA Contrast ratios ($CR \ge 7:1$ for normal text, $4.5:1$ for large headings).
   - Dynamic adaptive text contrast using sRGB linear luminance:
     $$L = 0.2126R_{\text{lin}} + 0.7152G_{\text{lin}} + 0.0722B_{\text{lin}}$$
   - LMS Cone Transformation matrices for Deuteranopia, Protanopia, Tritanopia support.
3. **SDF & MSDF Typography Engine**:
   - Use TextMeshPro SDF / Multi-channel SDF (MSDF) for crisp corners at extreme zoom levels.
   - Fallback Font Chain: Primary Font $\rightarrow$ CJK Fallback $\rightarrow$ Arabic RTL BiDi shaping.

*Reference Document:* [`game_ui_ux_paradigms_and_visual_hierarchy.md`](researches/game_ui_ux_paradigms_and_visual_hierarchy.md)

---

## 2. /game-ui-arch - Layered Canvas Architecture & FSM Navigation

### Architecture Standards:
1. **4-Layer Canvas Hierarchy**:
   - Layer 0 (BaseScreens): Full-screen screens (`MainMenuScreen`, `GameHUD`).
   - Layer 1 (Modals): Window popups (`PausePopup`, `SettingsPopup`, `ShopWindow`).
   - Layer 2 (Dimmer Overlay): Auto 50% black backdrop with Raycast Blocker.
   - Layer 3 (Toasts): Notification toasts (`OilHazardWidget`, `FloatingText`).
2. **Stack-Based Modal Navigation**:
   - `Stack<IUIScreen>` managed via `UIManager.cs` (`PushScreen`, `PopScreen`, `ClearAll`).
   - Unified Back-Button Handler: Android hardware back, iOS edge swipe, Esc key (`OnBackButtonPressed()`).
3. **Gamepad & Focus Navigation**:
   - Automatic focus highlight traps for modal popups.
   - Auto-scroll `ScrollRect` targeting focused UI element with `Mathf.SmoothDamp`.
   - Minimum Touch Target: Apple 44x44pt / Google 48x48dp with invisible Raycast padding.

*Reference Document:* [`game_ui_architecture_and_navigation_fsm.md`](researches/game_ui_architecture_and_navigation_fsm.md)

---

## 3. /game-ui-button - 7-State Button Lifecycle, Spring Juice & Haptics

### Button Engineering Rules:
1. **7 Button States**: Normal, Hover, Pressed, Selected, Disabled, Cooldown Overlay, Loading Spinner.
2. **Spring Physics Micro-Interactions**:
   - Damped harmonic oscillator scaling ($0.94\times$ on press, spring bounce on release):
     $$m\ddot{x} + c\dot{x} + kx = 0$$
   - Y-translation offset (-4px) and dynamic shadow offset shift.
3. **Audio & Haptics**:
   - iOS `UIImpactFeedbackGenerator` & Android `VibrationEffect` via `MobileHapticBridge.cs`.
   - Audio pitch variation ($\pm 0.05$) to prevent ear fatigue.
4. **Reusable UI Components**:
   - Modal Cards, Virtualized ScrollRect ($O(1)$ pool), Juicy Damage Ghost Progress Bars, Radial Selection Wheels.

*Reference Document:* [`button_systems_micro_interactions_and_juice.md`](researches/button_systems_micro_interactions_and_juice.md)

---

## 4. /game-ui-responsive - Safe Area, Aspect Ratio Adapters & Layout Math

### Layout Standards:
1. **Multi-Aspect Ratio Support**: 16:9, 19.5:9, 21:9, and 4:3 (iPad) dynamic anchor scaling.
2. **Hardware Notch / Safe Area**:
   - Normalize `Screen.safeArea` pixels into $[0, 1]$ RectTransform anchor space and reset `offsetMin/Max` to `Vector2.zero` (`SafeAreaPanel.cs`).
3. **Single Source of Safe Area Truth & Double-Notch Shift Prevention Rule**:
   - **Parent SafeArea Ancestor Check**: Top header widgets (`TopBarWidget.cs`) MUST check if any parent ancestor possesses a `SafeAreaPanel.cs` (`GetComponentInParent<SafeAreaPanel>()`) before applying custom notch pixel offsets (`Screen.height - Screen.safeArea.yMax`).
   - If a parent `SafeAreaPanel.cs` exists, `anchoredPosition.y` MUST remain `0` (or relative to parent's top edge) to prevent **Double Notch Shifting** ($2 \times \text{notch}$).
   - **Unified Header-Card Parent Hierarchy**: Place `TopBar` badges ($Y = -6\text{px}$) and upper `CardsContainer` ($Y = -60\text{px}$) inside the SAME root header panel (`TopBar`) as parent-child siblings. This guarantees that no matter the device notch height or aspect ratio (Foldable 960x2658, Tablet 2048x2732), badges and cards shift in 100% synchronized harmony with zero vertical overlap or background clipping.
4. **UGUI Layout Optimization**:
   - Avoid nested `ContentSizeFitter` + `Horizontal/VerticalLayoutGroup` ($O(N^2)$ Rebuild penalty).
   - Use zero-alloc `ManualLayoutGroup.cs` for 35x faster CPU layout calculation.
5. **Zero-Overlap Typography & Bounding Box Math**:
   - **Vertical Bounding Box Gap Formula**:
     $$\text{Gap} = \left(Y_{\text{center, top}} - \frac{\text{Height}_{\text{top}}}{2}\right) - \left(Y_{\text{center, bottom}} + \frac{\text{Height}_{\text{bottom}}}{2}\right) \ge \text{Margin}_{\text{min}} \, (4\text{--}8\text{px})$$
   - **Explicit Anchor Splitting & Zero Double-Offset Rule**:
     - Top Header Line: `anchorMin = (0, 0.5)`, `anchorMax = (1, 1.0)`, `pivot = (0.5, 0.5)`, `anchoredPosition.y = -2px`
     - Bottom Value Line: `anchorMin = (0, 0.0)`, `anchorMax = (1, 0.5)`, `pivot = (0.5, 0.5)`, `anchoredPosition.y = +2px`
     - Keeps texts perfectly centered in their respective anchor halves, eliminating clipping and double-offsetting outside container bounds.
   - **Unity UI `bestFit` Pitfall Safeguard**:
     - NEVER set `resizeTextForBestFit = true` on status titles or timers—it causes Unity UI to aggressively shrink text down to min font size (`8--10pt`).
     - ALWAYS set `resizeTextForBestFit = false`, `horizontalOverflow = Overflow`, `verticalOverflow = Overflow`, and specify crisp font sizes (`18pt--30pt Bold`).
   - **100% Opaque & Dark Outline Rule for 3D Floating HUD**:
     - Floating 3D HUD badges (`OilStatusUI.cs`) MUST use 100% opaque dark backgrounds (`Color32(10, 12, 18, 255)`) to prevent 3D road/coin bleed-through.
     - ALWAYS attach a dark `Outline` component (`Color32(0, 0, 0, 220)`, `effectDistance = (1.5, -1.5)`) to HUD texts for maximum edge contrast over dynamic game scenes.

*Reference Document:* [`responsive_layout_safearea_and_multi_device.md`](researches/responsive_layout_safearea_and_multi_device.md)

---

## 5. /game-ui-perf - UGUI vs UI Toolkit & Zero-GC Optimization

### Performance Rules:
1. **Canvas Splitting**: Separate static background Canvas from high-frequency dynamic HUD Canvas to prevent global VBO re-batching.
2. **SpriteAtlas v2**: Pack UI sprites with 8px bleed padding to prevent edge bleeding under bilinear filtering.
3. **Masking Performance**: Prefer `RectMask2D` over `Stencil Mask` (Stencil adds extra draw call passes).
4. **Zero-GC Text Updates**:
   - Use `FastStringFormat` or `TMP_Text.SetText()` numeric/StringBuilder overloads. Never concatenate strings (`score.text = "Score: " + val`) in `Update()`.

*Reference Document:* [`ugui_vs_ui_toolkit_and_performance_optimization.md`](researches/ugui_vs_ui_toolkit_and_performance_optimization.md)

---

## 6. /game-ui-hud - Dynamic Gameplay HUD & World-Space Damage Text

### Gameplay HUD Standards:
1. **Radial Speedometer & Gauges**: Non-linear angle mapping $\theta(v)$ with `Mathf.SmoothDamp` jitter reduction.
2. **3D World-Space Floating Damage Numbers**:
   - Bezier curve floating text pool (`DamageNumberPool.cs`) with $Z \le 0$ camera rear frustum filtering.
3. **Off-Screen Objective Pins**: Rectangle edge clamping ($\alpha_{\text{clamp}} = \min(\alpha_x, \alpha_y)$) with dynamic arrow rotation (`WorldToScreenTracker.cs`).
4. **Juice Animations**: DOTween elastic punch scale and low-health vignette pulse.
5. **Capsule Badge & Status Indicator Placement**:
   - Ensure dynamic 3D World-Space floating badges (`OilStatusUI.cs`) hover at an un-obstructed offset (`worldOffset = Vector3(0, 2.6f, 0.2f)`).

*Reference Document:* [`dynamic_gameplay_hud_and_worldspace_ui.md`](researches/dynamic_gameplay_hud_and_worldspace_ui.md)

---

## 7. /game-ui-shader - Glassmorphism, Neon Glow & Technical Art Shaders

### UI Shader Engine:
1. **Glassmorphism Blur Shader**: URP Downsampled Kawase Blur with Chromatic Aberration & Rim Lighting (`UI_Glassmorphism_URP.shader`).
2. **Glowing Outline Shader**: 8-tap alpha dilate with sine pulsefalloff (`UI_GlowingOutline_URP.shader`).
3. **Procedural Rounded Corners**: Independent 4-corner SDF radius calculation with antialiased stroke (`UI_ProceduralRoundedCorners_URP.shader`).
4. **Holographic Shimmer**: Anisotropic specular sweep reflection for rare cards/badges.

*Reference Document:* [`game_ui_shaders_and_technical_art.md`](researches/game_ui_shaders_and_technical_art.md)

---

## 8. /game-ui-a11y - Unity Localization, CJK/RTL & Automated UI Auditors

### Accessibility & Audit Rules:
1. **Unity Localization**: Key-based lookup, Smart Format pluralization, `StringBuilderPool` zero-alloc localizer.
2. **Multilingual Alignment**: RTL layout mirroring (`RTLRectTransformMirror.cs`) and CJK Kinsoku Shori line-breaking rules.
3. **Colorblind Filters**: Real-time Deuteranopia, Protanopia, Tritanopia URP simulation shader filter (`UI/ColorblindFilter`).
4. **Automated UI Quality Auditors**: Editor tools to inspect draw calls (`UIDrawCallAuditor.cs`), unassigned TMP fonts (`TMPFontAndOverflowAuditor.cs`), multi-device aspect ratios (`DeviceAspectRatioSimulator.cs`), and RectTransform element overlaps (`RectTransformOverlapAuditor.cs`).

*Reference Document:* [`localization_accessibility_and_ui_auditing.md`](researches/localization_accessibility_and_ui_auditing.md)
