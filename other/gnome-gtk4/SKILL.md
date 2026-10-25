---
name: gnome-gtk4"
description: Customizes native Adwaita and adw-gtk3 theme colors for a visually consistent GNOME desktop across GTK3, GTK4/libadwaita, Flatpak, and Qt5/Qt6 applications. Use when editing theme colors, changing the accent color, applying a color scheme to all apps, making Flatpak apps follow the host theme, or matching Qt apps to the GNOME look.
---

# GNOME GTK4 — Adwaita color customization

Goal: change the colors of the **native Adwaita** theme (GTK4/libadwaita) and its GTK3 port **adw-gtk3** so every app — GTK3, GTK4, libadwaita, Flatpak, and Qt5/Qt6 — shares the same palette.

## Mental model (why native theming is special)

- **libadwaita apps ignore `GTK_THEME` and `gtk-theme`** by design. They always render Adwaita. To "theme" them, override colors, not the theme name.
- **GTK3 apps** under GNOME use whatever `org.gnome.desktop.interface gtk-theme` says. Default is `Adwaita` (older look). Install **adw-gtk3** to give GTK3 apps the same look as libadwaita.
- Both toolkits read **user CSS**: `~/.config/gtk-3.0/gtk.css` and `~/.config/gtk-4.0/gtk.css`. GTK4 (including libadwaita) loads `gtk-4.0/gtk.css`; GTK3 loads `gtk-3.0/gtk.css`.
- **Flatpak apps are sandboxed** and cannot see `~/.config/gtk-*` or `~/.local/share/themes` unless permissions are granted (overrides).
- **Qt5/Qt6 apps** need a Qt style/theme bridge to match GTK; nothing is automatic.

## Step 1 — Install and activate adw-gtk3 (GTK3 base)

Arch Linux (`pacman -S adw-gtk-theme`), Fedora (`dnf install adw-gtk3-theme`).

```bash
gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3' && gsettings set org.gnome.desktop.interface color-scheme 'default'   # light
gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3-dark' && gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'   # dark
```

Fallback if some GTK4 apps ignore dark mode — add to `~/.config/gtk-4.0/settings.ini` and relog:

```ini
[Settings]
gtk-application-prefer-dark-theme=1
gtk-theme-name=adw-gtk3-dark
```

GTK3 user settings live in `~/.config/gtk-3.0/settings.ini` (theme, font, icons). On Wayland, keys that exist in the `org.gnome.desktop.interface` GSettings schema are read from GSettings instead of `settings.ini`.

## Step 2 — Change the accent color (GNOME 47+, libadwaita native)

```bash
gsettings set org.gnome.desktop.interface accent-color 'blue'   # blue|teal|green|yellow|orange|red|pink|purple
```

Affects all libadwaita apps system-wide. To also update adw-gtk3 (GTK3) to the same accent, use the `accent-color-change` helper from adw-colors:

```bash
git clone https://github.com/lassekongo83/adw-colors.git && cd adw-colors
bash scripts/accent-color-change/install.sh
# then choose accent; scripts regenerate gtk3/gtk4 CSS with matching named colors
```

## Step 3 — Custom palette (named colors / CSS variables)

The Adwaita stylesheet exposes **named colors** usable in user CSS. Key variables of libadwaita (GTK4):

```css
:root {
  --window-bg-color: #1e1e2e;      /* window background */
  --view-bg-color: #181825;        /* list/view background */
  --accent-bg-color: #cba6f7;      /* accent background */
  --accent-fg-color: #11111b;      /* text on accent */
  --accent-color: #cdd6f4;         /* standalone accent */
}
```

Full lists of default named colors:
- GTK4/libadwaita: https://gitlab.gnome.org/GNOME/libadwaita/-/blob/main/src/stylesheet/_colors.scss
- GTK3 (adw-gtk3): https://github.com/lassekongo83/adw-gtk3/blob/main/src/sass/_defaults.scss

Apply to **both** toolkits — create both files:

```bash
mkdir -p ~/.config/gtk-3.0 ~/.config/gtk-4.0
# write identical :root { ... } override block to each gtk.css
```

Variants differ:
- GTK3 light+dark: adw-gtk3 loads `gtk.css` for the active theme; use `prefers-color-scheme` media query for dark-specific rules.
- GTK4: `@media (prefers-color-scheme: dark) { ... }` and `@media (prefers-contrast: more)` work; libadwaita derives `--accent-color` automatically from `--accent-bg-color` via `--standalone-color-oklab`.

### Ready-made palettes (adw-colors)

```bash
git clone https://github.com/lassekongo83/adw-colors.git && cd adw-colors
sh scripts/install.sh                      # interactive theme picker
sudo flatpak override --filesystem=xdg-config/gtk-3.0 && sudo flatpak override --filesystem=xdg-config/gtk-4.0
```

Manual install (symlinks, e.g. Plano2):

```bash
mkdir -p ~/.config/gtk-3.0 ~/.config/gtk-4.0
ln -s "$PWD/themes/Plano2/gtk3-dark.css" ~/.config/gtk-3.0/gtk.css
ln -s "$PWD/themes/Plano2/gtk4-dark.css" ~/.config/gtk-4.0/gtk.css
ln -s "$PWD/themes/Plano2/assets" ~/.config/gtk-3.0/assets
ln -s "$PWD/themes/Plano2/assets" ~/.config/gtk-4.0/assets
```

Authoring a theme: copy a theme dir into `src/sass/`, edit `settings/_palette.scss`, run `sh parse-sass.sh` (needs dart-sass).

## Step 4 — Flatpak compatibility

Flatpak apps cannot see host theme files unless you grant access. Any combination of:

```bash
# 1) Grant filesystem access to theme dirs (covers ~/.config/gtk-3.0, gtk-4.0, ~/.local/share/themes)
sudo flatpak override --filesystem=xdg-config/gtk-3.0
sudo flatpak override --filesystem=xdg-config/gtk-4.0
sudo flatpak override --filesystem=xdg-data/themes

# 2) OR install theme runtimes from Flathub (GTK3 themes only — does not affect non-libadwaita GTK4 apps)
flatpak install org.gtk.Gtk3theme.adw-gtk3 org.gtk.Gtk3theme.adw-gtk3-dark
```

If using both, **mask** the Flathub runtimes so the host adw-gtk3 takes precedence:

```bash
sudo flatpak mask org.gtk.Gtk3theme.adw-gtk3
sudo flatpak mask org.gtk.Gtk3theme.adw-gtk3-dark
```

Confirm per-app overrides win over the global `sudo flatpak override`: `flatpak override` (user) overrides global. Use Flatseal as a GUI alternative.

> Portals: theme set via GSettings needs the XDG Desktop Portal; if colors do not propagate to Flatpak apps, ensure `xdg-desktop-portal-gnome` is installed/running. `ADW_DISABLE_PORTAL=1` forces GSettings theme pickup without a portal (debug only).

## Step 5 — Qt5/Qt6 consistency

Pick one strategy; each needs the matching packages. Do NOT stack Qt bridges (they conflict).

| Strategy | Packages (Arch) | Activation | Result |
|----------|-----------------|------------|--------|
| QGtk3Style (built-in) | none (in qt5-base/qt6-base) | `QT_QPA_PLATFORMTHEME=gtk3` | Qt follows current GTK3 style incl. adw-gtk3 colors |
| adwaita-qt | `adwaita-qt5-git` + `adwaita-qt6-git` (AUR) | `QT_STYLE_OVERRIDE=adwaita` | Native Qt style designed to look like Adwaita |
| Kvantum + KvLibadwaita | `kvantum`, `kvantum-qt5`, optional KvLibadwaita theme | `QT_STYLE_OVERRIDE=kvantum` (or set in qt5ct/qt6ct) | Full control of every Qt color, best for matching custom palettes |

Kvantum config file: `/etc/xdg/Kvantum/kvantum.kvconfig` or `~/.config/Kvantum/kvantum.kvconfig`; manage with `kvantummanager`.

For custom palettes: match your GTK `:root` hex values in **qt5ct/qt6ct** (`qt5ct`/`qt6ct` packages) — set the same `--accent-bg-color` as the Qt accent and same base/alternate view colors. Set `QT_QPA_PLATFORMTHEME` in your session environment (e.g. `~/.config/environment.d/qt.conf` with `QT_QPA_PLATFORMTHEME=gtk3`).

## Step 6 — Firefox (optional)

Firefox ships its own libadwaita colors; force the system palette:

1. Open `about:config`
2. Set `widget.gtk.libadwaita-colors.enabled` to `false`

## Verification loop

After any change:

1. `gsettings get org.gnome.desktop.interface gtk-theme` and `... color-scheme` — confirm active theme.
2. Restart running apps (or log out/in) — GTK caches CSS at startup.
3. Check every toolkit: one GTK3 app (e.g. GIMP), one GTK4 app (e.g. GNOME Files), one libadwaita app (e.g. GNOME Software), one Flatpak app, one Qt app (e.g. Qt Creator) — colors must match.
4. If only Flatpak apps are wrong → check `flatpak override --show` and portal service.
5. If only Qt apps are wrong → verify `QT_QPA_PLATFORMTHEME`/`QT_STYLE_OVERRIDE` is exported for the session (env in `environment.d` applies to new sessions only).

## Anti-patterns

- Do **not** set `GTK_THEME` globally expecting libadwaita to change — it is ignored there (works for plain GTK3/GTK4; per-app: `GTK_THEME=Adwaita:dark app`).
- Do **not** use Gradience for new setups: it is archived (June 2024); prefer gsettings `accent-color` + adw-colors.
- Do **not** edit vendor theme files under `/usr/share/themes` — use user overrides.
- Do **not** stack Qt bridges (gtk3 platformtheme + kvantum simultaneously).

## Sources (verify details online — versions move fast)

- adw-gtk3: https://github.com/lassekongo83/adw-gtk3 (README + gtk4.md)
- adw-colors: https://github.com/lassekongo83/adw-colors (HOWTO_INSTALL.md, HOWTO_CREATE.md, accent-color-change)
- ArchWiki GTK: https://wiki.archlinux.org/title/GTK
- ArchWiki Uniform look for Qt and GTK: https://wiki.archlinux.org/title/Uniform_look_for_Qt_and_GTK_applications
- libadwaita docs: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/styles-and-appearance.html