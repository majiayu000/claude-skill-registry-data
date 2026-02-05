---
name: sync-gruvbox-theme
description: Verify and sync gruvbox theme consistency across vim, neovim, tmux, and terminal
---

# Sync Gruvbox Theme

This skill ensures the gruvbox theme is consistently configured across all tools.

## Task

You should:

1. Check gruvbox configuration in:
   - Neovim (`nvim/lua/plugins/gruvbox.lua`)
   - Vim (`vim/vimrc.ln`)
   - Tmux (`tmux/tmux.conf.ln`)
   - Bash/terminal settings (`bash/bashrc.ln`)

2. Verify all use the same variant (dark/light)

3. Check color settings:
   - 256 color support
   - True color (RGB) support
   - Terminal overrides

4. Ensure consistent appearance of:
   - Background colors
   - Foreground text
   - Syntax highlighting
   - Status lines
   - Borders/separators

5. Suggest improvements for better consistency

## Files to Check

### Neovim
- `nvim/lua/plugins/gruvbox.lua` - should use ellisonleao/gruvbox.nvim
- Check contrast setting (hard/soft/default)
- Verify colorscheme is set

### Vim
- `vim/vimrc.ln` - should have gruvbox colorscheme
- Background setting (dark/light)

### Tmux
- `tmux/tmux.conf.ln` - should use egel/tmux-gruvbox plugin
- Verify @tmux-gruvbox setting matches vim/neovim
- Check terminal-overrides for true color

### Bash
- `bash/bashrc.ln` - check TERM variable
- Verify LSCOLORS or LS_COLORS use gruvbox palette

## Validation

Test by:
1. Opening neovim and checking `:colorscheme`
2. Running tmux and verifying status bar colors
3. Listing files with `ls` and checking colors
4. Opening vim and verifying theme

## Common Issues

- Terminal doesn't support 256 colors
- True color not enabled in tmux
- Mismatched dark/light variants
- Missing gruvbox plugins
- Wrong TERM environment variable

## Output

Report:
- Current theme variant in each tool
- Any inconsistencies found
- Color support status (256/true color)
- Recommended fixes
- Commands to apply fixes
