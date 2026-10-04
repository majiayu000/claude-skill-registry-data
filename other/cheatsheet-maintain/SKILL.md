---
name: cheatsheet-maintain
description: This skill should be used when the user asks to "add to cheatsheet", "update cheatsheet", "add a shortcut", "new tool shortcut", or wants to extend the CLI cheatsheet at dotfiles/cheatsheet.html.
---

# Cheatsheet Maintenance

## File location
`~/Progetti/dotfiles/cheatsheet.html`

Open with: `cheat` alias (calls `open ~/Progetti/dotfiles/cheatsheet.html`)

## Architecture

Sidebar nav + pages model. Each tool = one `.nav-item` in the sidebar + one `.page` div in `.content`. The JS `meta` object drives the toolbar title/subtitle. Search filters `.shortcut` rows inside the active page only.

```
<nav>          → nav items, one per tool
<main>
  .toolbar     → title + search input
  .content
    .page      → one per tool (hidden unless active)
      .columns → CSS grid of .card divs
```

## Adding a new page — 4 touch points

### 1. CSS variable (if new color needed)
Add to `:root` in `<style>`:
```css
--sky: #91d7e3;
```

### 2. Nav item
```html
<div class="nav-item" data-page="toolname" style="--dot-color:var(--COLOR)">
  <div class="nav-dot"></div>tool name
</div>
```

### 3. Page div
```html
<div class="page" id="page-toolname" data-accent="var(--COLOR)">
  <div class="columns">
    <!-- cards here -->
  </div>
</div>
```

### 4. JS meta entry
```js
'toolname': { title: 'Tool Name', sub: 'subtitle text' },
```

## Color table — all variables in use

| Variable    | Hex     | Page        |
|-------------|---------|-------------|
| `--lavender`| #b7bdf8 | vim         |
| `--blue`    | #8aadf4 | tmux        |
| `--teal`    | #8bd5ca | fzf         |
| `--green`   | #a6da95 | fzf-git     |
| `--mauve`   | #c6a0f6 | zoxide      |
| `--peach`   | #f5a97f | atuin       |
| `--yellow`  | #eed49f | eza         |
| `--sapphire`| #7dc4e4 | bat·delta   |
| `--red`     | #ed8796 | lazygit     |
| `--pink`    | #f5bde6 | lazydocker  |
| `--sky`     | #91d7e3 | glove80     |

For new tools add a Catppuccin Macchiato color not yet listed (e.g. `--maroon: #ee99a0`, `--flamingo: #f0c6c6`).

## Standard shortcut card

```html
<div class="card">
  <div class="card-header">section name</div>
  <div class="card-body">
    <div class="shortcut">
      <div class="keys"><kbd>Key</kbd><span class="plus">+</span><kbd>X</kbd></div>
      <span class="desc">what it does</span>
    </div>
  </div>
</div>
```

### `.keys` patterns
- Single key: `<kbd>key</kbd>`
- Combo: `<kbd>A</kbd><span class="plus">+</span><kbd>B</kbd>`
- Sequence: `<kbd>Ctrl+G</kbd><span class="then">then</span><kbd>f</kbd>`
- Command/flag: `<kbd>command text</kbd>` (auto-styled as `.kbd-cmd` by JS)

### kbd auto-styling (JS applies on load)
- Modifier keys (Ctrl, Alt, Shift, Cmd, prefix, Space) → `.kbd-mod` (mauve tint)
- Special keys (Enter, Esc, Tab) → `.kbd-special` (blue tint)
- Text with spaces or `<` → `.kbd-cmd` (teal tint)

## Full-width card

Span all columns with inline style:
```html
<div class="card" style="grid-column: 1 / -1">
```

## Graphical / visual cards

For tools that benefit from a visual layout (keyboard diagrams, layer maps, etc.), use a scoped `<style>` block inside the `.page` div and build custom CSS classes. The JS `colorKbds()` function only touches `<kbd>` elements, so custom markup is safe.

### Pattern: badge rows (layer maps, numbered items)
```html
<style>
  .badge { display:inline-flex; align-items:center; justify-content:center;
    width:1.5rem; height:1.5rem; border-radius:4px;
    font-size:0.65rem; font-weight:700; }
  .badge-row { display:flex; align-items:center; gap:0.5rem;
    padding:0.22rem 0; font-size:0.72rem; }
</style>

<div class="badge-row">
  <span class="badge" style="background:var(--sky);color:var(--crust)">0</span>
  <span>Layer name</span>
  <span style="color:var(--subtext0);font-size:0.68rem">— activation method</span>
</div>
```

### Pattern: key-stack (key + modifier label below)
```html
<div style="display:flex; flex-direction:column; align-items:center; gap:2px">
  <div style="background:var(--surface1); border:1px solid var(--surface2);
    border-bottom:2px solid var(--surface2); border-radius:4px;
    padding:3px 7px; font-size:0.68rem">A</div>
  <div style="font-size:0.58rem; color:var(--green)">⌃ Ctrl</div>
</div>
```

### Pattern: thumb/key grid (tap + hold annotations)
```html
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:4px">
  <div style="border-radius:4px; border:1px solid var(--sapphire);
    border-bottom:2px solid var(--sapphire); padding:4px 6px;
    font-size:0.62rem; text-align:center; background:var(--surface1)">
    <div style="font-weight:600">⌫ Bksp</div>
    <div style="color:var(--sapphire); font-size:0.58rem">▼ Cursor 12</div>
  </div>
</div>
```

### Pattern: grouped sections inside card body
```html
<div class="card-body" style="padding:0.6rem 1rem; display:flex; gap:2rem; flex-wrap:wrap">
  <div style="min-width:210px">
    <div style="font-size:0.6rem; color:var(--subtext0); text-transform:uppercase;
      letter-spacing:0.1em; margin-bottom:0.4rem; border-bottom:1px solid var(--surface0);
      padding-bottom:0.15rem">group label</div>
    <!-- rows -->
  </div>
</div>
```

## Search behavior
The JS filter matches `.textContent` of `.shortcut` rows against the query. Custom graphical markup (badge rows, key-stacks, etc.) is **not** searched — only `.shortcut` divs are. For searchable content in graphical cards, duplicate key info as hidden `.shortcut` rows or accept that graphical sections are unsearchable.

`/` focuses search · `Escape` clears it.
