---
name: tauri-syntax-menu
description: >
  Use when creating application menus, system tray icons, context menus, or handling menu events in Tauri 2.
  Prevents using deprecated v1 menu patterns and missing menu event handler registration on the Builder.
  Covers MenuBuilder, menu item types, PredefinedMenuItem, context menus, TrayIconBuilder, and JavaScript Menu/TrayIcon APIs.
  Keywords: tauri menu, MenuBuilder, TrayIcon, system tray, context menu, PredefinedMenuItem, menu events.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-menu

## Quick Reference

### Menu Item Types (Rust)

| Type | Builder | Purpose |
|------|---------|---------|
| `MenuItem` | `MenuItemBuilder` | Basic clickable text item |
| `CheckMenuItem` | `CheckMenuItemBuilder` | Toggleable checkbox item |
| `IconMenuItem` | `IconMenuItemBuilder` | Item with icon |
| `PredefinedMenuItem` | -- | OS-native standard items |
| `Submenu` | `SubmenuBuilder` | Nested menu container |

### PredefinedMenuItem Types (both Rust and JS)

Platform-standard items: `About`, `Hide`, `HideOthers`, `ShowAll`, `CloseWindow`, `Quit`, `Copy`, `Cut`, `Paste`, `SelectAll`, `Undo`, `Redo`, `Minimize`, `Zoom`, `Separator`, `Fullscreen`, `Services`, `BringAllToFront`.

### SubmenuBuilder Convenience Methods (Rust)

| Method | Creates |
|--------|---------|
| `.text(id, text)` | MenuItem with ID and text |
| `.separator()` | Menu separator line |
| `.quit()` | PredefinedMenuItem::Quit |
| `.undo()` | PredefinedMenuItem::Undo |
| `.redo()` | PredefinedMenuItem::Redo |
| `.cut()` | PredefinedMenuItem::Cut |
| `.copy()` | PredefinedMenuItem::Copy |
| `.paste()` | PredefinedMenuItem::Paste |
| `.select_all()` | PredefinedMenuItem::SelectAll |

### TrayIconBuilder Key Methods (Rust)

| Method | Signature | Description |
|--------|-----------|-------------|
| `new()` | `() -> Self` | Create builder |
| `with_id(id)` | `(impl Into<TrayIconId>) -> Self` | Set custom ID |
| `icon(image)` | `(Image) -> Self` | Set tray icon |
| `tooltip(text)` | `(impl Into<String>) -> Self` | Set tooltip |
| `title(text)` | `(impl Into<String>) -> Self` | Set title |
| `menu(menu)` | `(&Menu) -> Self` | Attach context menu |
| `show_menu_on_left_click(bool)` | `(bool) -> Self` | Show menu on left click (default: true) |
| `icon_as_template(bool)` | `(bool) -> Self` | macOS template icon |
| `on_menu_event(F)` | `(F) -> Self` | Menu click handler |
| `on_tray_icon_event(F)` | `(F) -> Self` | Tray icon click handler |
| `build(manager)` | `(impl Manager) -> Result<TrayIcon>` | Build tray icon |

### JS Menu Classes

| Class | Import | Description |
|-------|--------|-------------|
| `Menu` | `@tauri-apps/api/menu` | Menu container |
| `MenuItem` | `@tauri-apps/api/menu` | Clickable text item |
| `Submenu` | `@tauri-apps/api/menu` | Nested menu |
| `CheckMenuItem` | `@tauri-apps/api/menu` | Toggleable item |
| `PredefinedMenuItem` | `@tauri-apps/api/menu` | OS-standard item |
| `TrayIcon` | `@tauri-apps/api/tray` | System tray icon |

### JS TrayIcon Event Types

| Event Type | Description |
|------------|-------------|
| `Click` | Tray icon clicked |
| `DoubleClick` | Tray icon double-clicked |
| `Enter` | Cursor entered tray icon |
| `Move` | Cursor moved over tray icon |
| `Leave` | Cursor left tray icon |

### JS TrayIcon Mouse Buttons

`Left`, `Right`, `Middle`

### Critical Warnings

**NEVER** call `Builder::on_menu_event()` in Tauri 2 -- it was removed. Use `App::on_menu_event()` or the builder `.on_menu_event()` method instead.

**NEVER** use Tauri v1 menu type names (`CustomMenuItem`, `SystemTray`, `MenuItem` for predefined items) -- they are renamed in v2.

**ALWAYS** call `.build()` on `MenuBuilder` and `SubmenuBuilder` -- forgetting `.build()` produces a builder, not a usable menu.

**ALWAYS** match menu event IDs as strings using `event.id().as_ref()` in Rust -- menu item IDs are compared as string references, not typed enums.

**ALWAYS** use `Menu.new()` (not `new Menu()`) in JavaScript -- menu items are created via async factory methods.

---

## Essential Patterns

### Pattern 1: Application Menu (Rust)

```rust
use tauri::menu::{MenuBuilder, SubmenuBuilder, PredefinedMenuItem};

tauri::Builder::default()
    .menu(|app| {
        let file_menu = SubmenuBuilder::new(app, "File")
            .text("new", "New")
            .text("open", "Open")
            .separator()
            .quit()
            .build()?;

        let edit_menu = SubmenuBuilder::new(app, "Edit")
            .undo()
            .redo()
            .separator()
            .cut()
            .copy()
            .paste()
            .select_all()
            .build()?;

        MenuBuilder::new(app)
            .item(&file_menu)
            .item(&edit_menu)
            .build()
    })
    .on_menu_event(|app, event| {
        match event.id().as_ref() {
            "new" => println!("New file"),
            "open" => println!("Open file"),
            _ => {}
        }
    })
    .run(tauri::generate_context!())
    .expect("error running app");
```

### Pattern 2: Application Menu (JavaScript)

```typescript
import { Menu, MenuItem, Submenu, PredefinedMenuItem, CheckMenuItem } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    await Submenu.new({
      text: 'File',
      items: [
        await MenuItem.new({
          text: 'Open',
          accelerator: 'CmdOrCtrl+O',
          action: () => { console.log('Open clicked'); },
        }),
        await MenuItem.new({
          text: 'Save',
          accelerator: 'CmdOrCtrl+S',
          action: () => { console.log('Save clicked'); },
        }),
        await PredefinedMenuItem.new({ item: 'Separator' }),
        await PredefinedMenuItem.new({ item: 'Quit' }),
      ],
    }),
    await Submenu.new({
      text: 'View',
      items: [
        await CheckMenuItem.new({
          text: 'Dark Mode',
          checked: false,
          action: (item) => { console.log('Toggled'); },
        }),
      ],
    }),
  ],
});

await menu.setAsAppMenu();
```

### Pattern 3: Context Menu (JavaScript)

```typescript
// Show context menu at cursor position
await menu.popup();

// Show context menu at specific position
await menu.popup({ x: 100, y: 200 });
```

### Pattern 4: System Tray (Rust)

```rust
use tauri::tray::TrayIconBuilder;
use tauri::menu::MenuBuilder;
use tauri::image::Image;

tauri::Builder::default()
    .setup(|app| {
        let menu = MenuBuilder::new(app)
            .text("show", "Show Window")
            .text("hide", "Hide Window")
            .separator()
            .text("quit", "Quit")
            .build()?;

        let _tray = TrayIconBuilder::new()
            .icon(Image::from_path("icons/tray.png")?)
            .tooltip("My Tauri App")
            .menu(&menu)
            .show_menu_on_left_click(true)
            .on_menu_event(|app, event| {
                match event.id().as_ref() {
                    "show" => {
                        if let Some(w) = app.get_webview_window("main") {
                            w.show().unwrap();
                        }
                    }
                    "quit" => app.exit(0),
                    _ => {}
                }
            })
            .on_tray_icon_event(|tray, event| {
                println!("Tray event: {:?}", event);
            })
            .build(app)?;

        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error running app");
```

### Pattern 5: System Tray (JavaScript)

```typescript
import { TrayIcon } from '@tauri-apps/api/tray';
import { Menu, MenuItem } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    await MenuItem.new({ text: 'Show', action: () => showWindow() }),
    await MenuItem.new({ text: 'Quit', action: () => exit(0) }),
  ],
});

const tray = await TrayIcon.new({
  icon: 'icons/tray-icon.png',
  tooltip: 'My App',
  menu,
  action: (event) => {
    if (event.type === 'Click') {
      console.log('Tray clicked with', event.button);
    }
  },
});

// Update at runtime
await tray.setTooltip('Updated tooltip');
await tray.setIcon('icons/new-icon.png');
await tray.setVisible(false);
```

### Pattern 6: Menu Item Management (JavaScript)

```typescript
// Dynamic menu manipulation
await menu.append(await MenuItem.new({ text: 'New Item', action: () => {} }));
await menu.prepend(await MenuItem.new({ text: 'First Item', action: () => {} }));
await menu.insert(1, await MenuItem.new({ text: 'At Index 1', action: () => {} }));
await menu.remove('item-id');
await menu.removeAt(0);

const item = await menu.get('item-id');
const allItems = await menu.items();
```

---

## Menu Event Handling (Rust)

```rust
// On the builder
.on_menu_event(|app, event| {
    match event.id().as_ref() {
        "new" => println!("New file"),
        "open" => println!("Open file"),
        _ => {}
    }
})
```

The `event.id()` returns a `MenuId`. Use `.as_ref()` to get a `&str` for pattern matching.

---

## Tray Configuration in tauri.conf.json

```json
{
  "app": {
    "trayIcon": {
      "iconPath": "icons/icon.png",
      "iconAsTemplate": true
    }
  }
}
```

---

## Permissions

Menu operations require `core:menu:default` and tray operations require `core:tray:default` in the capability file.

```json
{
  "permissions": [
    "core:menu:default",
    "core:tray:default"
  ]
}
```

---

## v1 to v2 Migration Names

| Tauri v1 | Tauri v2 |
|----------|----------|
| `Menu` | `MenuBuilder` |
| `CustomMenuItem` | `MenuItemBuilder` |
| `Submenu` | `SubmenuBuilder` |
| `MenuItem` (predefined) | `PredefinedMenuItem` |
| `SystemTray` | `TrayIconBuilder` |
| `SystemTrayEvent` | `TrayIconEvent` |

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for Menu, Tray, and all item types
- [references/examples.md](references/examples.md) -- Working code examples for menu and tray patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with menus and tray, with WHY explanations

### Official Sources

- https://v2.tauri.app/develop/menu/
- https://v2.tauri.app/develop/system-tray/
- https://v2.tauri.app/reference/javascript/api/namespacemenu/
- https://v2.tauri.app/reference/javascript/api/namespacetray/
