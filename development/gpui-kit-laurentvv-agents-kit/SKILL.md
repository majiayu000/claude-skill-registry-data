---
name: gpui-kit
description: Build cross-platform Rust desktop apps with GPUI Kit (Longbridge's component library on Zed's GPUI engine) - bootstrap a new app, wire components (Button, Input, Table, Dock, charts, markdown), theme it, and avoid the 0.x pitfalls. Use whenever the user asks for a Rust desktop/GUI app or prototype, mentions gpui, GPUI or gpui-kit, or wants a native-Rust alternative to Slint, egui or Tauri.
---

# gpui-kit - Rust desktop UI on GPUI

GPUI Kit is a component toolkit on top of GPUI, the GPU-accelerated UI
framework extracted from the Zed editor. It ships 75+ styled components
(shadcn/ui-inspired), virtualized data tables, dock layout, charts, markdown
rendering and a tree-sitter/LSP code editor. Production-proven in Longbridge
Pro (a commercial trading app). Apache-2.0, targets macOS / Windows / Linux /
WebAssembly. Version checked here: **0.7.3**.

Verified live on Windows 11 (Git Bash) on 2026-10-18: the bootstrap recipe
compiles clean (`cargo add gpui-kit@0.7.3` + `cargo check`, exit 0, 798
locked packages, ~50 s cold); the rest was checked against the official docs
at gpui-kit.com for v0.7.3.

## The core recipe: bootstrap an app

0. Prerequisites (Windows): Visual Studio 2022 Build Tools with the
   "Desktop development with C++" workload (MSVC + a Windows SDK), the **MSVC**
   Rust toolchain (not GNU), and **CMake on PATH** (`cmake --version`).
1. Scaffold:

```bash
cargo new my-app && cd my-app
cargo add gpui-kit@0.7.3
```

2. Minimal `src/main.rs` (official getting-started, verbatim structure):

```rust
use gpui_kit::component::button::{Button, ButtonVariants};
use gpui_kit::*;

struct HelloWorld;

impl Render for HelloWorld {
    fn render(&mut self, _: &mut Window, _: &mut Context<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .size_full()
            .items_center()
            .justify_center()
            .gap_2()
            .child("Hello, World!")
            .child(
                Button::new("hello")
                    .primary()
                    .label("Click me")
                    .on_click(|_, _, _| println!("Clicked!")),
            )
    }
}

fn main() {
    application()
        .with_assets(assets::Assets)
        .run(|cx| {
            init(cx);

            open_window(WindowOptions::default(), cx, |_, cx| {
                cx.new(|_| HelloWorld)
            })
            .expect("Failed to open window");
        });
}
```

3. `cargo run` - a window opens; clicking the button prints in the terminal.

## Rules that bite

- **Call `init(cx)` once** before opening windows or building components: it
  sets up the Kit layers and component themes. Skip it and components render
  unstyled/broken.
- **Return your content view from `open_window`, not another Root.** The
  window wrapper already provides the Root, which owns the overlay layers
  (dialogs, sheets, notifications). A nested Root breaks overlays.
- **Never add `gpui` or `gpui-pre` as your own dependency.** Depend on
  `gpui-kit` only. `gpui-pre` is the crates.io name for a pinned Zed GPUI
  snapshot used to align Kit releases - not a different framework, and a newer
  snapshot does not mean the Kit supports it. Everything GPUI (`div`,
  `Render`, `Window`, `Context`, `Styled`...) arrives through `use gpui_kit::*`.
- **Imports are two-layer**: GPUI prelude from `gpui_kit::*`, each widget from
  its module (`gpui_kit::component::button::{Button, ButtonVariants}`,
  `gpui_kit::component::{Input, InputState, Form, Checkbox, Switch, ...}`).
  Missing trait imports (ButtonVariants for `.primary()`, ActiveTheme for
  `cx.theme()`) are the usual compile errors.
- **0.x churn**: the API moves between minor versions. Pin the version you
  tested (`cargo add gpui-kit@<exact>`), and re-read the docs page for your
  version before "fixing" compile errors from memory - signatures do drift.
- Optional `features = ["gpui-fast"]` switches the rendering backend; do not
  mix Fast types with a direct GPUI dependency.
- macOS-only: text needs the `font-kit` feature (already enabled by gpui-kit);
  without it a window opens with NoopTextSystem and no text renders.
- WebAssembly builds need a nightly toolchain (see /docs/webassembly).

## What ships in the box

- Forms (Input, Checkbox, Radio, Switch...), navigation, overlays, feedback,
  layout components - full list: https://gpui-kit.com/component
- Data tables: virtual scrolling, fixed/resizable columns, sorting, cell
  selection across hundreds of thousands of rows.
- Dock layout: resizable panels, draggable tabs, nested splits, serializable.
- Rich content: markdown + HTML rendering, charts, syntax highlighting, code
  editor (tree-sitter + LSP), webview, i18n, system notifications.
- Accessibility (AccessKit) built into the interaction layer.
- Headless UI testing: real pointer/keyboard/focus/layout behavior without a
  GPU window - https://gpui-kit.com/docs/test

## Theming

Light, dark and custom themes driven by semantic tokens (`Theme`,
`ThemeColor`, `ActiveTheme` trait - `cx.theme()` in render). Design guidance:
https://gpui-kit.com/docs/design-guides

## When to pick something else

- Slint: native look (Windows Fluent), software rendering, tiny footprint,
  visual DSL/designer. Prefer for small, native-feel utilities.
- egui: immediate mode, quick debug tooling.
- Tauri: you want a web frontend (React/Vue) in a Rust shell.
- gpui-kit: dense, GPU-rendered apps - dashboards, tables, dock-style tools -
  from one Rust codebase, optionally compiled to wasm.

## Sources

- Docs: https://gpui-kit.com/docs (getting-started, installation, test,
  packaging, auto-update). API: https://docs.rs/gpui-kit
- Full-text dump for agents: https://gpui-kit.com/llms-full.txt
- Upstream ships its own agent skills in the repo (`skills/gpui-kit`,
  `skills/gpui-kit-design-guides`; `npx skills add longbridge/gpui-kit`) -
  useful companions to this one.
