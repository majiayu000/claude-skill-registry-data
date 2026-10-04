---
name: pyside6-fluent-ui
description: >
  Build, audit, and incrementally refactor PySide6/Qt Widgets desktop interfaces using Microsoft
  Fluent 2 design principles, semantic light/dark tokens, accessible control states, QPalette,
  generated QSS, and Qt-native behavior. Includes an optional VS Code-inspired workbench shell with
  an Activity Bar, Primary Sidebar, single-row frameless Title Bar with menus and caption controls
  or a native-window fallback, optional panel, and structured Status Bar. Use for existing GUI
  modernization, new screens, dialogs, item views, delegates, theme systems, accessibility reviews,
  and desktop-shell navigation.
  Do not introduce React, WinUI, XAML, or browser dependencies merely to obtain a Fluent appearance;
  do not migrate the application to QML solely for styling.
---

# PySide6 Fluent UI

Use this skill to make a Qt Widgets application feel coherent with Microsoft Fluent 2 while remaining a native PySide6 application. Fluent governs visual hierarchy, semantic tokens, typography, spacing, states, accessibility, and motion. Qt governs widget behavior, window management, model/view behavior, high-DPI handling, and platform integration. The optional workbench profile can reproduce VS Code's single-row shell structure without copying VS Code branding, proprietary icons, or exact theme colors.

## Scope

This skill is for **PySide6 and Qt Widgets**. It covers:

- auditing an existing GUI before changing it;
- introducing a semantic theme and token layer;
- refactoring screens incrementally without changing application behavior;
- styling standard controls, item views, dialogs, menus, toolbars, and custom composites;
- an optional workbench shell with Activity Bar, Sidebar, Title Bar, Panel, and Status Bar;
- light, dark, system-following, and high-contrast-aware themes;
- keyboard, focus, accessibility, scaling, and active/inactive-window behavior.

Do not use this skill as the main implementation guide for Qt Quick/QML. Do not migrate a Widgets application to QML, WinUI, React, or another toolkit merely to obtain a Fluent appearance.

## Authority order

Resolve conflicts in this order:

1. Official Qt/PySide behavior and platform documentation.
2. Official Microsoft Fluent 2 principles and token definitions.
3. Official VS Code UX guidance for workbench-shell semantics.
4. This skill’s Qt translation and recipes.
5. Project-specific UI rules that do not violate accessibility or native behavior.

## Operating modes

Classify the task before editing:

- **Audit:** inspect and report; do not modify files.
- **Infrastructure:** add or repair token, theme, palette, QSS, icon, or gallery infrastructure.
- **Component:** implement or refactor a bounded widget or dialog.
- **Shell:** implement or refactor Activity Bar, Sidebar, Title Bar, Panel, or Status Bar.
- **Migration:** refactor one existing screen or workstream while preserving behavior.
- **Review:** verify a proposed change for Fluent, Qt, accessibility, and regression risks.

When a user asks for a broad GUI refactor, begin with an audit unless they explicitly ask for immediate implementation and the affected scope is already clear.

## Non-negotiable rules

1. **Preserve behavior during visual work.** Keep models, signals, slots, controllers, shortcuts, persistence, validation, object names, automation IDs, and test-visible behavior unless a separate change is explicitly requested.
2. **Use semantic aliases.** Application code consumes names such as `text_primary`, `surface_background`, and `brand_background`; it does not scatter hex values or raw Fluent token numbers.
3. **Use Qt-native mechanisms.** Prefer layouts, size policies, standard widgets, model/view, `QPalette`, generated application QSS, delegates, and narrowly scoped `QProxyStyle` overrides.
4. **Do not scatter `setStyleSheet()`.** Apply one generated application style sheet. A local style sheet requires a documented exception and complete state coverage.
5. **Do not use fixed geometry for ordinary layout.** Prefer layouts, constraints, minimum/preferred sizes, stretch, and splitters. Fixed dimensions are allowed for deliberate shell metrics or icon targets.
6. **Define every applicable state.** Cover rest, hover, pressed, focus, selected/checked, disabled, invalid, read-only, and busy states where relevant.
7. **Focus is independent of hover.** Every keyboard-interactive control needs a visible focus treatment that remains visible without mouse hover.
8. **Do not convey status only by color.** Pair severity colors with text, icons, patterns, or accessible descriptions.
9. **Use one icon family.** Prefer Fluent System Icons or another approved SVG family. Do not use emoji or text glyphs as production UI icons.
10. **Keep native window behavior.** Every title-bar profile must preserve system move, resize, snapping/tiling where supported, maximize/restore, active/inactive state, a visible active/inactive outer boundary, safe areas, and accessibility.
11. **Choose the title profile from the requested outcome.** Use the frameless template when the user asks for one VS Code-style row. Use expanded client area only when retaining native caption content is acceptable. Always retain a tested native-title fallback.
12. **Respect system preferences.** Follow system light/dark when configured, inspect contrast preferences where available, and provide a reduced-motion application option.
13. **Use custom painting last.** First exhaust standard widgets, QSS, delegates, icon assets, and small composite widgets.
14. **No decorative card inflation.** Use spacing and hierarchy before wrapping every section in a bordered or elevated card.
15. **Validate both themes and multiple scales.** A screen is not complete after looking correct in one light-theme screenshot.

## Required workflow

### 1. Inventory the affected UI

Identify:

- top-level window/dialog and owning controller;
- widget hierarchy and layouts;
- `.ui`, QSS, palette, icon, delegate, and custom-painting sources;
- existing inline style sheets and hardcoded values;
- model/view and selection-model ownership;
- focus order, shortcuts, validation, and persistent state;
- existing screenshots and tests.

For audit tasks, report findings before proposing code.

### 2. Establish behavioral constraints

Write down what must remain unchanged. At minimum, check:

- public signals and slots;
- model identity and selection behavior;
- command routing and keyboard shortcuts;
- `objectName`, accessible identity, and automation hooks;
- persistent splitter/window state;
- validation, error, loading, and empty states.

Do not combine a visual migration with unrelated domain or architecture rewrites.

### 3. Load only the references needed

| Work type | Read |
|---|---|
| Principles and visual judgment | `references/fluent-principles.md` |
| Tokens, aliases, density, typography | `references/token-architecture.md` |
| Palette/QSS/proxy-style architecture | `references/qt-styling-architecture.md` |
| Standard control mapping | `references/component-mappings.md` |
| Required states | `references/interaction-states.md` |
| Keyboard, contrast, screen readers | `references/accessibility.md` |
| Overall shell | `references/workbench-shell.md` |
| Activity Bar | `references/activity-bar.md` |
| Status Bar | `references/status-bar.md` |
| Integrated/native Title Bar | `references/title-bar.md` |
| Existing-GUI migration | `references/refactor-playbook.md` |
| Completion checks | `references/validation-checklist.md` |
| Prohibited patterns | `references/anti-patterns.md` |

### 4. Introduce or reuse theme infrastructure

Use the existing project theme system if it already provides semantic aliases and complete states. Otherwise:

1. load the versioned official token snapshot;
2. resolve the Qt-facing aliases in `resources/qt-token-map.json`;
3. layer `resources/shell-token-map.json` when using the workbench profile;
4. build an application `QPalette` for broad roles;
5. render and apply a single application QSS;
6. expose theme changes through a `FluentThemeManager` signal;
7. repolish only widgets whose dynamic properties changed.

Do not require application widgets to know whether a value originated from a light, dark, or high-contrast theme.

### 5. Map intent to Qt controls

Prefer a standard Qt widget or a small composite. Examples:

- Fluent Button → `QPushButton`;
- icon command → `QToolButton`;
- Input → `QLineEdit`;
- Navigation/Activity item → checkable `QToolButton` or item view;
- DataGrid → `QTableView` plus model, selection model, and delegate;
- Message Bar → reusable `QFrame` composite;
- Drawer → side panel, splitter pane, or `QDockWidget` according to behavior;
- Dialog → `QDialog` with explicit default/cancel/destructive actions.

Read `references/component-mappings.md` before inventing a custom control.

### 6. Express appearances through properties

Use stable semantic dynamic properties rather than widget-specific QSS fragments:

```python
set_fluent_property(button, "fluentAppearance", "primary")
set_fluent_property(button, "fluentSize", "medium")
set_fluent_property(frame, "fluentRole", "card")
set_fluent_property(field, "fluentInvalid", True)
```

Approved property vocabulary:

```text
fluentRole        card, messageBar, sidebar, panel, titleBar, activityBar,
                  activityItem, statusBar, statusItem, commandCenter, titleBarMenu,
                  windowFrame, divider
fluentAppearance  primary, secondary, outline, subtle, transparent, danger
fluentSize        small, medium, large, compact
fluentSeverity    info, success, warning, danger
fluentSelected    true/false when :checked is not available
fluentInvalid     true/false
fluentBusy        true/false
windowActive      true/false for custom title surfaces and window frames
windowFrameMode   native/client for a frameless outer boundary
windowFrameVisible true/false for restored versus maximized/full-screen state
```

Keep project-specific properties separate from this vocabulary.

### 7. Implement all applicable states

Use `resources/component-state-matrix.json`. For each interactive component, verify:

- mouse and keyboard paths reach the same action;
- focus is visible;
- selected/check state is unambiguous;
- disabled controls cannot mutate state;
- invalid controls expose a message;
- busy actions prevent duplicate execution;
- hover effects are not required where the platform disables them.

### 8. Apply workbench-shell rules only when appropriate

The optional shell profile is:

```text
Single-row custom Title Bar or native Title Bar plus command strip
└─ Body
   ├─ Activity Bar
   └─ Splitter
      ├─ optional Primary Sidebar
      └─ main content / optional panel
└─ Status Bar
```

- Activity Bar items switch primary view containers; they are not arbitrary commands.
- Status Bar left side is global/workspace state; right side is contextual state.
- A VS Code-style one-row request requires the frameless profile; expanded/native modes retain OS chrome.
- Every Title Bar profile is capability-gated and must preserve the documented window behavior.
- Do not copy VS Code logos, product names, exact theme colors, or proprietary branding.

### 9. Validate before removing legacy styling

Run the applicable checks from `references/validation-checklist.md`. Keep old styling until the migrated scope passes behavior, focus, theme, scaling, and screenshot checks. Then remove obsolete constants, QSS, icons, and compatibility code in the same bounded workstream.

## Theme architecture

Use this division of responsibility:

| Mechanism | Responsibility |
|---|---|
| `QPalette` | broad Active, Inactive, and Disabled colors; selection; links; tooltips |
| Generated app QSS | component borders, padding, radii, states, subcontrols, shell surfaces |
| Dynamic properties | semantic variants, roles, severity, and state |
| Item delegates | data-row visuals and content that QSS cannot express correctly |
| `QProxyStyle` | narrow pixel metrics, style hints, focus/indicator behavior |
| Composite widgets | Message Bar, Activity item badge, Status item, command center |
| Custom painting | exceptional cases only |

Qt style sheets can replace parts of native rendering. After a control is styled, explicitly define the states and subcontrols you rely on; do not assume every native state remains visible.

## Activity Bar contract

- Use a small set of clear, persistent view destinations.
- Use exclusive selection where one view container is active.
- Provide tooltip, accessible name, and stable ID for every item.
- Put global/account/settings destinations at the bottom only when they are true shell destinations.
- Use a compact badge only for a count or urgent state; do not place arbitrary text in the icon area.
- Reference density: 48 px bar/items with 24 px icons; compact 36/32/16 px. Treat these as adaptable reference tokens, not universal mandates.

Read `references/activity-bar.md` before implementing it.

## Status Bar contract

- Left: global/workspace status and primary state.
- Right: current page, document, selection, or mode context.
- Use short text; use icons only for clear metaphors.
- Each entry has a stable ID, alignment, priority, visibility, tooltip, accessible name, and optional action.
- Use brand/neutral background consistently. Reserve warning/danger surfaces for exceptional states.
- Reference height: 22 px compact; effective Qt minimum must fit the active font and focus treatment.

Read `references/status-bar.md` before implementing it.

## Title Bar contract

Select one explicit profile:

1. **Single-row frameless:** use `Qt.FramelessWindowHint`, the template's menus/caption controls, `QWindow.startSystemMove()`, and eight `startSystemResize()` edge/corner handles. Wrap the client shell in a `windowFrame` surface and attach `FluentWindowFrameController` so the lost native boundary is replaced. This is the profile that structurally matches current VS Code on Windows. On Windows 11, inherit `WindowsSnapLayoutWindowMixin` and attach `WindowsSnapLayoutAdapter`; it returns `HTMAXBUTTON` only for the custom maximize/restore region and defers native press/release back to the Qt caption control. The frame controller uses `DWMWA_BORDER_COLOR` when supported and the generated-QSS semantic client border otherwise.
2. **Qt 6.9+ expanded client area:** request `ExpandedClientAreaHint` and `NoTitleBarBackgroundHint`, retain native caption content, and respect `QWindow.safeAreaMargins()`. Do not claim this removes the OS caption row.
3. **Native fallback:** keep the OS title bar and place the same Fluent title/menu/command strip beneath it.

Expose the native fallback in configuration or command-line startup. Never silently substitute expanded mode for an explicitly requested one-row title bar.

For Windows Snap Layout compatibility, keep the supported minimum width at or below 500 effective pixels (330 or below is preferred when the application can remain usable), collapse low-priority center/trailing title content first, and manually verify the maximize-button hover flyout on a supported Windows 11 build. Keep client-side resize handles; do not broaden `WM_NCHITTEST` ownership to the window edges merely to add the maximize hit result.

Read `references/title-bar.md` before changing window flags.

## Accessibility baseline

- Icon-only actions have accessible names and tooltips.
- Custom composites expose meaningful name, description, role/state through standard widgets or Qt accessibility interfaces.
- Keyboard focus follows visual reading order.
- Focus returns to the triggering control when dialogs or transient surfaces close.
- Normal text targets 4.5:1 contrast; large text and essential non-text UI target 3:1.
- High-contrast mode derives core colors from the effective system palette.
- Invalid and status states include text or accessible descriptions.
- Do not disable focus rectangles or remove native shortcuts without a replacement.

## Output expectations

### Audit output

Return:

- inventory and current styling architecture;
- visual inconsistencies and hardcoded values;
- state/accessibility gaps;
- behavior that must be preserved;
- migration risks;
- recommended order of work;
- files likely to change;
- no code changes unless requested.

### Implementation output

State:

- which semantic aliases and Qt mechanisms were used;
- which behavior was intentionally preserved;
- which states were implemented;
- what was validated;
- any platform or Qt-version limitation;
- remaining legacy styling in the affected scope.

## Completion gate

A refactored scope is complete only when:

- visual values flow through semantic aliases;
- applicable interaction states are present;
- light and dark themes work;
- high-contrast behavior has a defined path;
- keyboard and focus behavior pass;
- scaling and minimum-size behavior pass;
- existing functional tests pass;
- obsolete local styling in the migrated scope is removed;
- title-bar work preserves native window behavior on supported targets.
- frameless work exposes a semantic active/inactive outer boundary, suppresses it when maximized/full-screen, and retains the client fallback when native border integration is unavailable.
- Windows 11 frameless work returns `HTMAXBUTTON` for the maximize region, preserves maximize/restore activation, and passes the target-platform Snap Layout hover check when that profile is claimed.
