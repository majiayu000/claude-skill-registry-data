---
name: theming
description: Tokyo Night palette, theme API, no hardcoded colors. Load when touching CSS, xterm theme config, or any color-related code.
triggers:
  - theme
  - color
  - palette
  - "tokyo night"
  - css
  - "ansi colors"
---

# Theming

## Default: Tokyo Night (Night variant)

Canonical palette. Source-of-truth lives in `src-tauri/src/modules/theme/palette.rs` (TBD in Phase 1). Everything else reads from there.

| Token | Hex | Use |
|---|---|---|
| `bg` | `#1a1b26` | window/pane background |
| `bg-alt` | `#16161e` | sidebar, popover |
| `fg` | `#a9b1d6` | default text |
| `fg-dim` | `#787c99` | secondary text, comments |
| `accent` | `#7aa2f7` | primary accent (blue), cursor |
| `cyan` | `#7dcfff` | strings, links |
| `green` | `#9ece6a` | success, additions |
| `red` | `#f7768e` | error, deletions |
| `yellow` | `#e0af68` | warning |
| `purple` | `#bb9af7` | keywords, special |
| `selection` | `#283457` | selection background |

ANSI palette must match Tokyo Night Night (see Ghostty's built-in theme).

## Rules

1. **No hardcoded colors in components.** Always reference theme tokens via CSS custom properties (`var(--nyx-accent)`) or a typed theme object.
2. **Theme is emitted**, not computed. Rust emits the palette to the frontend on theme change; frontend listens and updates CSS vars.
3. **Sister tools read from us.** Theme API exports JSON/TOML fragments for `fzf`, `bat`, `lazygit`, `btop`, `starship` (or our prompt). User picks once, theme propagates everywhere.

## Theme API shape (draft)

```rust
struct Theme {
    name: String,
    palette: Palette,
    ansi: [Color; 16],
}

#[tauri::command] fn theme_get() -> Theme
#[tauri::command] fn theme_set(name: String)
#[tauri::command] fn theme_export(target: ExportTarget) -> String
```

Targets: `fzf`, `bat`, `lazygit`, `btop`, `delta`, `starship`, `kitty-conf` (compat).

## Frontend

```css
:root {
  --nyx-bg: #1a1b26;
  --nyx-fg: #a9b1d6;
  --nyx-accent: #7aa2f7;
  /* ... */
}
```

CSS vars set on `:root` by a `useTheme()` hook listening to the Rust event. Components only use vars.

## xterm.js terminal theme

```ts
term.options.theme = {
  background: cssVar('--nyx-bg'),
  foreground: cssVar('--nyx-fg'),
  cursor: cssVar('--nyx-accent'),
  selectionBackground: cssVar('--nyx-selection'),
  // ... 16 ANSI colors from theme.ansi
};
```

Re-apply on theme change.

## Transparency / aesthetic

Default opacity: `0.95`. Unfocused-split opacity: `0.9` (dim inactive panes, Ghostty pattern). CSS-driven, GPU-accelerated.

## What we do NOT support (yet)

- Live theme reload from the OS (light/dark). Phase 2.
- User-authored themes. Phase 1.5+ via Settings UI.
- Per-pane themes. Probably never — clutter.
