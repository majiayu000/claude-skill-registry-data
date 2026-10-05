---
name: rust-gtk4
description: This skill should be used when the user asks to "build a GTK4 app in Rust", "create a libadwaita UI", "use relm4", "build a Linux desktop app with Rust", "implement a GTK4 widget", "create a preferences dialog", "add system tray", or mentions relm4 components, AdwApplicationWindow, AdwPreferencesPage, or message-driven GTK4 UI patterns.
triggers:
  - gtk4
  - libadwaita
  - relm4
  - linux desktop app
  - gtk rust
  - adwaita
  - desktop gui rust
---

## Role

Expert Rust/GTK4 developer specializing in libadwaita HIG-compliant desktop applications using the relm4 Elm-style architecture. Produces structured, composable, message-driven UIs with clean separation between model state and view rendering.

## Core Architecture: relm4 Elm Pattern

relm4 implements an Elm-like model-update-view loop:

- **`Component::init()`** — construct initial model state + build widget tree
- **`Component::update()`** — receive a typed message, mutate model
- **`view!` macro** — declarative widget tree; auto-syncs to model on `#[watch]` fields

The `#[relm4::component]` macro generates the boilerplate; the `view!` macro is the widget DSL.

## Key Concepts

### Sync vs Async Components

| Trait | When to use |
|---|---|
| `SimpleComponent` | No async work; instant model updates |
| `Component` | Background commands needed (`type CommandOutput`) |
| `AsyncComponent` | `update()` is async; background tasks via `update_cmd()` |

### Message Flow

```
User action (signal) → sender.input(Msg::X) → update() → model mutates → view re-renders
Background task      → sender.command(...)  → update_cmd() → sender.input(...)
```

### Background Work Pattern

Never block `update()`. Use `sender.command()` to dispatch a `CommandOutput` message, then handle the result in `update_cmd()`:

```rust
async fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>) {
    match msg {
        Msg::FetchData => {
            self.loading = true;
            sender.command(|_, _| CmdOut::DoFetch);
        }
    }
}

async fn update_cmd(&mut self, cmd: Self::CommandOutput, sender: ComponentSender<Self>) {
    match cmd {
        CmdOut::DoFetch => match fetch().await {
            Ok(data) => sender.input(Msg::SetData(data)),
            Err(e)   => sender.input(Msg::SetError(e.to_string())),
        }
    }
}
```

## libadwaita Widget Hierarchy

```
AdwApplicationWindow
└── AdwToolbarView
    ├── add_top_bar: AdwHeaderBar
    └── content: [primary content]
```

### Preferences Dialog Structure

```
AdwPreferencesWindow
└── AdwPreferencesPage (tab)
    └── AdwPreferencesGroup (section)
        ├── AdwActionRow (entry, switch suffix)
        └── AdwSwitchRow
```

### Empty + Loading States

```rust
// Empty state
adw::StatusPage {
    set_icon_name: Some("document-open-symbolic"),
    set_title: "No Items",
    set_description: Some("Add an item to get started"),
}

// Inline alert
adw::Banner {
    set_title: "Connection failed",
    set_revealed: model.has_error,
    set_button_label: Some("Retry"),
    connect_button_clicked[sender] => move |_| sender.input(Msg::Retry),
}
```

### Toast Notifications

```rust
adw::ToastOverlay {
    // wraps main content; show toasts programmatically:
}

// In update():
self.toast_overlay.add_toast(
    adw::Toast::new("Settings saved")
);
```

## Signal → Message Pattern

All signals close over `sender` and call `sender.input()`:

```rust
gtk::Button {
    set_label: "Connect",
    connect_clicked[sender] => move |_| {
        sender.input(AppMsg::Connect);
    }
}

gtk::Entry {
    connect_changed[sender] => move |entry| {
        sender.input(AppMsg::SetUrl(entry.text().to_string()));
    }
}

adw::SwitchRow {
    set_title: "Auto-restart",
    set_active: model.auto_restart,
    connect_active_notify[sender] => move |row| {
        sender.input(AppMsg::SetAutoRestart(row.is_active()));
    }
}
```

## System Tray Integration

Use `libayatana-appindicator` (or `ksni`) for system tray. Build a dedicated `TrayModel` component, spawn it alongside the main app:

```rust
let mut indicator = AppIndicator::new("myapp", "myapp-symbolic");
indicator.set_status(AppIndicatorStatus::Active);

let menu = gio::Menu::new();
menu.append(Some("Show"), Some("app.show-window"));
menu.append(Some("Quit"), Some("app.quit"));
indicator.set_menu_model(Some(&menu));
```

## Cargo.toml Dependencies

```toml
[dependencies]
relm4    = { version = "0.10", features = ["libadwaita"] }
gtk4     = { version = "0.9",  features = ["v4_10"] }
libadwaita = { version = "0.7", features = ["v1_4"] }
glib     = "0.20"
gio      = { version = "0.20", features = ["v2_76"] }
tokio    = { version = "1", features = ["full"] }
```

## Edge Cases

If a component needs to talk to a sibling: use `ComponentSender::output()` to emit upward; parent routes messages downward.

If the view needs to reference a named widget outside the macro: use `#[name = "my_widget"]` annotation inside `view!`.

If GTK panics with "assertion failed: is_main_thread": ensure all GTK calls happen on the GLib main thread — never from `tokio::spawn`.

If libadwaita features are version-gated: add the feature flag to the `libadwaita` dep (e.g., `features = ["v1_4"]`).

For deep widget patterns, component composition, and real-world relm4 structure: see the reference files below.

## References

- [Component Patterns](references/component-patterns.md)
- [libadwaita Widget Catalog](references/adwaita-widgets.md)
