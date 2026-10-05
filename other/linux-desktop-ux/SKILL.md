---
name: linux-desktop-ux
description: This skill should be used when the user asks to "follow GNOME HIG", "create a .desktop file", "install Linux desktop icons", "add AppStream metadata", "implement gettext i18n in Rust", "use XDG base directories", "add system tray to a Linux app", "package for Flathub", "write PKGBUILD", or mentions XDG_CONFIG_HOME, AdwAlertDialog, AdwStatusPage, or Linux desktop standards.
triggers:
  - gnome hig
  - linux desktop
  - xdg base directory
  - desktop file
  - appstream
  - flathub
  - pkgbuild
  - gettext rust
  - system tray linux
  - freedesktop
  - hicolor icons
  - xdg config
---

## Role

Linux desktop UX specialist covering GNOME Human Interface Guidelines (HIG), freedesktop.org standards (XDG, desktop entries, icons), AppStream metadata, gettext internationalization, and system packaging (PKGBUILD, Flatpak). Produces standards-compliant, discoverable, and accessible desktop applications.

## XDG Base Directories

Never hardcode `~/.config`. Use the XDG spec — the `directories` crate handles this in Rust:

```rust
use directories::ProjectDirs;

let dirs = ProjectDirs::from("com", "vendor", "myapp")
    .expect("no valid home directory");

let config_dir = dirs.config_dir();    // ~/.config/myapp/
let data_dir   = dirs.data_local_dir(); // ~/.local/share/myapp/
let cache_dir  = dirs.cache_dir();     // ~/.cache/myapp/
```

Always create directories before writing:

```rust
std::fs::create_dir_all(&config_dir)?;
```

**Atomic write pattern** — protects against corruption on crash:

```rust
fn atomic_write(path: &Path, data: &[u8]) -> std::io::Result<()> {
    let dir = path.parent().unwrap();
    let mut tmp = tempfile::NamedTempFile::new_in(dir)?;
    tmp.write_all(data)?;
    tmp.flush()?;
    tmp.persist(path)?;
    Ok(())
}
```

## .desktop File

Every GUI app needs a `.desktop` file installed to `/usr/share/applications/`. Without it, the app won't appear in launchers.

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=My App
Comment=Brief one-line description shown in tooltips
Exec=/usr/bin/myapp %F
Icon=myapp
Terminal=false
Categories=Network;Utility;
Keywords=proxy;vpn;
StartupNotify=true
StartupWMClass=myapp
```

**`StartupWMClass`** must match the `WM_CLASS` the running window reports (usually the binary name). Without it, taskbar shows a duplicate icon.

**`Exec` field codes**:
- `%F` — list of selected files (for file-handling apps)
- `%U` — list of URLs
- `%u` — single URL
- No code needed for apps that ignore arguments

**Categories** (use semicolons, end with semicolon):

| App type | Categories |
|---|---|
| Network utility | `Network;Utility;` |
| Developer tool | `Development;IDE;` |
| System tool | `System;` |
| Media player | `AudioVideo;Player;` |

## Icon Installation

Follow the [Freedesktop Icon Naming Spec](https://specifications.freedesktop.org/icon-naming-spec/latest/). Install to `hicolor` theme (the universal fallback):

```
/usr/share/icons/hicolor/
├── 48x48/apps/myapp.png        ← minimum required
├── 128x128/apps/myapp.png
├── 256x256/apps/myapp.png
├── scalable/apps/myapp.svg     ← preferred (scales perfectly)
└── symbolic/apps/myapp-symbolic.svg  ← for panel/tray (monochrome)
```

Symbolic icons must be single-color (inherits theme foreground). Name them `appname-symbolic.svg`.

In PKGBUILD:
```bash
install -Dm644 assets/myapp.svg \
    "$pkgdir/usr/share/icons/hicolor/scalable/apps/myapp.svg"
install -Dm644 assets/myapp-symbolic.svg \
    "$pkgdir/usr/share/icons/hicolor/symbolic/apps/myapp-symbolic.svg"
```

## GNOME HIG Principles

### Window Layout

```
┌─ AdwHeaderBar ──────────────────────────────────────┐
│  [Back]  Window Title         [Search]  [⋮ Menu]    │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Primary Content (AdwToolbarView content)          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- Primary/default action → header bar (e.g., "Connect" button)
- Secondary actions → hamburger menu (⋮) in header bar
- Destructive actions → always show `AdwAlertDialog` before executing

### Empty States

Show `AdwStatusPage` instead of an empty list:

```rust
adw::StatusPage {
    set_icon_name: Some("document-open-symbolic"),
    set_title: "No Subscriptions",
    set_description: Some("Add a subscription URL to get started"),
    // optional call-to-action button as child
}
```

### Destructive Actions

Never delete without confirmation:

```rust
let dialog = adw::AlertDialog::builder()
    .heading("Remove subscription?")
    .body("This cannot be undone.")
    .build();
dialog.add_responses(&[("cancel", "Cancel"), ("remove", "Remove")]);
dialog.set_response_appearance("remove", adw::ResponseAppearance::Destructive);
dialog.set_default_response("cancel");
dialog.present(Some(&window));
```

### Loading States

Show a spinner in the header bar; disable action buttons during loading:

```rust
adw::HeaderBar {
    pack_end = &gtk::Spinner {
        #[watch]
        set_spinning: model.loading,
        #[watch]
        set_visible: model.loading,
    }
}
```

## Internationalization (gettext)

```toml
[dependencies]
gettextrs = "0.17"
```

```rust
use gettextrs::{gettext, ngettext, TextDomain};

fn setup_i18n() {
    TextDomain::new("myapp")
        .locale_dir("/usr/share/locale")  // or from env for dev
        .init()
        .ok();
}

// Mark strings for extraction
let msg = gettext("Connect");
let msg = ngettext("{n} server", "{n} servers", count as u32);
```

Extract strings with `xgettext`, translate in `.po` files, compile to `.mo` with `msgfmt`.

## AppStream Metadata (Flathub / GNOME Software)

Install to `/usr/share/metainfo/com.vendor.appname.metainfo.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.vendor.myapp</id>
  <name>My App</name>
  <summary>One-line summary (max 60 chars)</summary>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>GPL-3.0-or-later</project_license>

  <description>
    <p>First paragraph describing what the app does.</p>
    <p>Second paragraph with more detail.</p>
  </description>

  <url type="homepage">https://github.com/vendor/myapp</url>
  <url type="bugtracker">https://github.com/vendor/myapp/issues</url>

  <releases>
    <release version="1.0.0" date="2025-02-01">
      <description><p>Initial release.</p></description>
    </release>
  </releases>

  <content_rating type="oars-1.1"/>
</component>
```

## PKGBUILD Pattern (Arch Linux)

```bash
pkgname=myapp
pkgver=1.0.0
pkgrel=1
pkgdesc="Brief description"
arch=('x86_64')
url="https://github.com/vendor/myapp"
license=('GPL-3.0-or-later')
depends=('gtk4' 'libadwaita' 'dbus')
makedepends=('rust' 'cargo')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")

prepare() {
    cd "$pkgname-$pkgver"
    cargo fetch --locked --target "$(rustc -vV | sed -n 's/host: //p')"
}

build() {
    cd "$pkgname-$pkgver"
    cargo build --frozen --release
}

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 target/release/myapp          "$pkgdir/usr/bin/myapp"
    install -Dm644 assets/myapp.desktop          "$pkgdir/usr/share/applications/myapp.desktop"
    install -Dm644 assets/myapp.svg              "$pkgdir/usr/share/icons/hicolor/scalable/apps/myapp.svg"
    install -Dm644 assets/myapp.metainfo.xml     "$pkgdir/usr/share/metainfo/myapp.metainfo.xml"
    install -Dm644 LICENSE                       "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
```

## Edge Cases

If icon doesn't appear after install: run `gtk-update-icon-cache /usr/share/icons/hicolor` or relogin.

If `.desktop` file doesn't appear in launcher: validate with `desktop-file-validate myapp.desktop`.

If gettext translations don't load: check `LANGUAGE`/`LANG` env vars and that `.mo` files are compiled and placed in the correct locale directory.

If AppStream validation fails: use `appstreamcli validate myapp.metainfo.xml` to check required fields.

## References

- [Desktop Integration Standards](references/freedesktop-standards.md)
- [PKGBUILD & Packaging Patterns](references/packaging-patterns.md)
