---
name: ami-audit-ui-consistency
description: Audits UI code and assets across web, desktop, and mobile platforms for design system token compliance, button hierarchy, interactive states, and zero icon duplication or semantic collisions.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: UI & Design System Consistency Auditor

When invoked, act as a strict Design System and UI Quality Auditor. Your purpose is to verify that user interface code across Web, Desktop, and Mobile platforms adheres strictly to project design tokens, component hierarchies, standardized interactive states, and coherent, accessible iconography without duplicated or conflicting glyphs.

## Workflow

### 1. Scope and Platform Discovery

Inspect modified files (`git diff` or target directories) to detect the active interface technology:
- **Web:** Tailwind CSS, CSS Modules, Styled Components, vanilla HTML5, or UI component libraries (Radix, Shadcn, MUI).
- **Desktop:** WinUI 3, WPF, MAUI, or WinForms (XAML ResourceDictionaries, styles, controls).
- **Mobile:** Jetpack Compose, Flutter, or React Native (MaterialTheme, ThemeData, StyleSheet).

Identify the project's source of truth for design tokens:
- **Web:** `tailwind.config.*`, `globals.css`, CSS root variables (`:root { --... }`).
- **Desktop:** `App.xaml`, `Colors.xaml`, `MergedDictionaries`, or shared `ResourceDictionary`.
- **Mobile:** `Theme.kt`, `Color.kt` (Compose) or `theme.dart` (Flutter).

### 2. Design Tokens and Color Palette Audit

Inspect modified UI code for raw, hardcoded visual values:

1. **Color Invariant (New vs. Legacy Code):**
   - **New Code / Modified Lines:** The presence of hardcoded hexadecimal (`#[0-9a-fA-F]{3,8}`), `rgb(...)`, or `hsl(...)` values outside theme configuration files is a **CRITICAL BLOCKING DEFECT**. All colors must reference declared design tokens or theme resources.
   - **Legacy / Preexisting Code:** If hardcoded colors existed before the current change, report them as a **WARNING** with a concrete suggestion for the nearest matching project token.
2. **Spacing and Typography Consistency:**
   - Detect arbitrary inline measurements (e.g., `margin: 13px`, `p-[17px]`, `FontSize="15"`) that break the established spacing or typographic scale.
   - Enforce using standard scale tokens (e.g., `p-4`, `text-sm`, `StaticResource BaseTextBlockStyle`).
3. **Concentric Border-Radius Invariant (Nested Containers & Avatars):**
   - Inspect nested rounded elements (e.g., image within a padded container, inner card inside an outer outline).
   - Verify that outer and inner radii follow the concentric law: $R_{\text{inner}} = R_{\text{outer}} - \text{padding}$.
   - Flag as a warning any squircle/radius mismatch where $R_{\text{inner}} > R_{\text{outer}} - \text{padding}$ that pinches corner margins or creates optical distortion.
4. **Theme Parity & Scrollbar Styling:**
   - Verify that surfaces and text elements support Light and Dark modes without inverted or unreadable contrast.
   - If custom scrollbar rules are defined (`::-webkit-scrollbar*`), verify that dark mode track and thumb styles (`.dark ::-webkit-scrollbar-*` or standard `scrollbar-color` on `html.dark`) are physically declared to prevent glaring white scroll tracks in dark mode.

### 3. Component Hierarchy and Interactive States Audit

Inspect buttons, inputs, and interactive controls for structural discipline:

1. **Button Hierarchy Discipline:**
   - **Single Primary Action Rule:** In any single screen, modal, dialog, or form context, there must be at most **one** prominent `Primary` or `Accent` call-to-action button. Secondary actions must use `Secondary`, `Outline`, or `Ghost` variants.
   - **Destructive Actions:** Deletion or irreversible actions must use designated `Danger` or `Destructive` visual styling.
2. **Interactive States Completeness:**
   - Verify that buttons and interactive controls declare all three standard interaction states:
     - **Hover / PointerOver:** Subtle visual feedback when hovered.
     - **Focus-Visible:** Accessible keyboard focus ring or boundary highlight for accessibility navigation.
     - **Disabled:** Dimmed opacity and disabled pointer events when inactive (`disabled`, `IsEnabled="False"`, `enabled = false`).

### 4. Iconography and Asset Hygiene Audit

Inspect icon usages, icon libraries, and visual assets:

1. **Single Icon Family Lock:**
   - Verify that the project uses a single established icon library (e.g., Lucide, Heroicons, Segoe Fluent Icons, or Material Symbols).
   - Flag as a defect the introduction of a secondary icon library when an established family already exists in dependencies.
2. **Zero Duplicate Glyphs (Semantic Invariance):**
   - Ensure that the same conceptual action or entity uses the identical glyph throughout the application (e.g., do not mix an outlined trash can in one view with a filled trash can in another).
3. **Semantic Collision Prevention:**
   - Verify that identical icons are not repurposed for opposing or contradictory actions across screens.
4. **Accessibility on Icon-Only Controls:**
   - Any button, link, or clickable element displaying only an icon without visible text MUST include an accessible label (`aria-label`, `title`, `AutomationProperties.Name`, or `contentDescription`).
5. **Asset Cleanup:**
   - Detect orphaned, unused, or duplicate SVG files residing in `assets/`, `public/`, or resource folders.

### 5. Multi-Platform Quick Verification Matrix

| Platform | Tokens Check | Button Hierarchy | Iconography Check |
| :--- | :--- | :--- | :--- |
| **Web** | No raw hex in `.tsx`/`.vue`/`.html`; use Tailwind classes or `var(--...)`. | Max 1 `variant="primary"` per view; verify `:focus-visible` ring. | Single SVG/icon package; require `aria-label` on icon buttons. |
| **Desktop** | Use `StaticResource`/`ThemeResource`; no inline `Background="#..."`. | Use `AccentButtonStyle` for primary; adhere to `desktop_app_stability.md`. | Use `FontIcon Glyph` or `SymbolIcon`; set `AutomationProperties.Name`. |
| **Mobile** | Use `MaterialTheme.colorScheme` or `Theme.of(context).colorScheme`. | Use `FilledButton` (Primary), `OutlinedButton`, `TextButton`. | Use consistent `Icons.Default.*` / `CupertinoIcons`; set `contentDescription`. |

### 6. Reporting and Remediation

Emit a structured audit report:
- **[CRITICAL] Blocking Defects:** Raw hex colors in new code, conflicting primary buttons, missing accessibility labels on icon buttons.
- **[WARNING] Hygiene Advisories:** Hardcoded values in legacy code, duplicate SVGs in asset folders, missing hover states.

CONFIRMATION 1 - Remediation Approval: STOP and present the findings to the user with exact token and icon replacement suggestions. Await explicit approval before modifying any UI files.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
