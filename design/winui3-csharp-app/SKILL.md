---
name: winui3-csharp-app
description: "WinUI 3 / Windows App SDK desktop apps in C#/XAML. MVVM, bindings, navigation, Mica/Acrylic, windowing, packaging, performance."
---

# WinUI 3 C# App
read other relevant `winui*` skills also as needed. 
## Workflow
1. Classify: new app, existing app, or specific issue.
2. New app → Quick Start (New). Existing app → Quick Start (Existing).
3. Route via Reference Index.

## Core Rules
- Prefer Windows App SDK / WinUI APIs over custom interop.
- Code-behind = view glue only; state/logic in ViewModels.
- Prefer `x:Bind` (typed); `Binding` for dynamic DataContext.
- Marshal UI work through `DispatcherQueue`.
- System backdrops via `Window.SystemBackdrop` with fallback.
- Keep behavior stable unless explicitly asked to change.
- Architecture/packaging/library choices: present 2–3 options + tradeoffs + recommendation.

## Scope
- In: WinUI 3 / Windows App SDK desktop apps, C#/XAML, MVVM, navigation, windowing, packaging, performance.
- Out: WPF, UWP, WinForms, C++/WinRT unless explicitly requested.

## Reference Index
- `references/foundations.md` → project setup, release channels, MVVM/tooling, threading migration
- `references/ui-ux.md` → navigation, layout, title bar, backdrops, accessibility
- `references/design-fluent.md` → Fluent design principles, UX polish
- `references/windowing.md` → AppWindow, multi-window, dialogs, pickers
- `references/performance.md` → bindings, x:Load, list virtualization, perf basics

## Quick Start (New)
1. Decide packaging + target framework; document constraints.
2. Architecture: code-behind for small apps, MVVM Toolkit for larger.
3. Create ViewModel, expose for `x:Bind`.
4. Layout with `Grid`/`StackPanel`.
5. Commands via `RelayCommand`/`AsyncRelayCommand`.
6. Add navigation if multi-page.

## Quick Start (Existing)
1. Audit binding modes + `DataContext`; fix `x:Bind` vs `Binding` mismatches.
2. Move logic to ViewModels; keep code-behind thin.
3. Threading: UI updates on UI thread via `DispatcherQueue`.
4. Validate system backdrop usage + fallbacks.
5. Check dialogs, pickers, multi-window in `references/windowing.md`.
