---
name: keybind-audit
description: Analyze keybindings across all dotfiles for conflicts, duplicates, and inconsistencies. Use when modifying keybindings or checking for conflicts.
---

# Keybind Audit

Analyze keybindings across all configuration files in this dotfiles repository.

## When to use

- User wants to add or modify a keybinding
- User asks about keybinding conflicts
- User wants to check consistency across tools

## Target files

| Tool | File | Pattern |
|------|------|---------|
| zsh | `dot_zshrc.tmpl` | `bindkey` |
| tmux | `dot_tmux.conf` | `bind`, `bind-key` |
| vim | `dot_vimrc` | `nnoremap`, `vnoremap`, `inoremap`, `cnoremap` |
| neovim | `dot_config/nvim/lua/keymap.lua` | `vim.keymap.set`, `nvim_set_keymap` |
| neovim plugins | `dot_config/nvim/lua/plugin_configs/*.lua` | `vim.keymap.set`, keymaps in setup() |
| obsidian | `dot_obsidian.vimrc` | `nmap`, `vmap`, `exmap` |
| alacritty | `dot_config/alacritty/alacritty.toml` | `[[keyboard.bindings]]` |

## Analysis checklist

1. **Cross-tool conflicts**: Same key combo, different behavior across tools
   - Focus on: Ctrl+key, Alt+key, leader combinations
   - Example: `<C-g>` in tmux vs zsh

2. **Duplicates**: Same keybinding defined multiple times within one tool
   - Example: `j -> gj` in both dot_vimrc and nvim/lua/keymap.lua

3. **Consistency**: Check vim-style navigation unity
   - Are hjkl mapped consistently?
   - Is `<leader>fj/fk/fl` pattern consistent?

4. **Shadowed defaults**: Overwritten important defaults that may cause confusion

5. **Dead bindings**: Commented-out bindings that might be worth revisiting

## Output format

Group by severity:

### Conflicts (must fix)
- Key: `<C-x>`
- Tools: tmux (kill-pane) vs zsh (execute)
- Recommendation: ...

### Duplicates (should fix)
- Key: `j -> gj`
- Files: dot_vimrc:1, keymap.lua:9
- Recommendation: Keep only in keymap.lua

### Inconsistencies (consider)
- ...

### Info
- ...
