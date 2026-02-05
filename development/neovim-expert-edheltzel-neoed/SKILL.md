---
name: neovim-expert
description: "Expert Neovim/Lua configuration assistant for NOE.ED (LazyVim-based setup). Covers plugin configuration, LSP setup, keymaps, Mason, TreeSitter, and troubleshooting. Trigger with: neovim skill, lua skill, nvim skill, neoed skill, lazy skill (or plurals). Use for: LSP config help, error troubleshooting, keymap creation, plugin setup, theme customization."
---

# NOE.ED Neovim Expert

Expert assistance for the NOE.ED Neovim configuration - a LazyVim-based setup with extensive customizations.

## Configuration Location

```
/Users/ed/.dotfiles/nvim/.config/nvim/
```

## Architecture Overview

NOE.ED uses a three-level plugin loading system (`lua/config/lazy.lua`):

1. **Core LazyVim** - `lazyvim.plugins`
2. **Custom plugins** - `lua/plugins/` (organized by category)
3. **Language configs** - `lua/plugins/languages/`

### Directory Structure

```
lua/
├── config/
│   ├── lazy.lua      # Plugin manager bootstrap
│   ├── options.lua   # Vim options
│   ├── keymaps.lua   # Custom keybindings
│   ├── autocmds.lua  # Autocommands
│   └── filetypes.lua # Custom filetype associations
└── plugins/
    ├── disabled.lua  # Disabled plugins
    ├── ai/           # Claude Code, Codeium
    ├── coding/       # surround, emmet
    ├── editor/       # git, multicursor
    ├── formatting/   # conform, prettier
    ├── languages/    # LSP configs per language
    ├── linting/      # biome
    ├── ui/           # themes, lualine
    ├── utils/        # snacks
    └── dap/          # debugger configs
```

## Key Files

| File | Purpose |
|------|---------|
| `lazyvim.json` | Enabled LazyVim extras (32 extras) |
| `lazy-lock.json` | Plugin version lockfile |
| `lua/config/keymaps.lua` | Custom keybindings |
| `lua/plugins/ui/lualine.lua` | Custom statusline (253 lines) |
| `lua/plugins/ui/lualine/neoed.lua` | Theme adapter |

## Quick Reference

### Adding a New Plugin

Create file in appropriate category under `lua/plugins/`:

```lua
return {
  "author/plugin-name",
  event = "VeryLazy",
  opts = {
    -- options
  },
}
```

### Extending LSP Server Config

Create/edit file in `lua/plugins/languages/`:

```lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        servername = {
          settings = { servername = { option = value } },
        },
      },
    },
  },
}
```

### Adding a Keymap

Edit `lua/config/keymaps.lua`:

```lua
local set = vim.keymap.set
set("n", "<leader>xx", "<cmd>Command<cr>", { desc = "Description" })

-- For which-key groups:
local wk = require("which-key")
wk.add({ { "<leader>x", group = "Group Name", icon = { icon = "X", color = "blue" } } })
```

### Disabling a Plugin

Add to `lua/plugins/disabled.lua`:

```lua
return {
  { "plugin/name", enabled = false },
}
```

## References

- **[lazyvim-structure.md](references/lazyvim-structure.md)** - File organization, plugin loading, extras system
- **[plugin-patterns.md](references/plugin-patterns.md)** - lazy.nvim spec patterns, overrides, dependencies
- **[lsp-config.md](references/lsp-config.md)** - LSP server configuration, Mason, formatters
- **[keymaps.md](references/keymaps.md)** - Keymap conventions, existing bindings, which-key
- **[troubleshooting.md](references/troubleshooting.md)** - Common errors and solutions

## Active Theme

**Eldritch** - Dark purple theme with custom Lualine statusline.

Theme colors defined in `lua/plugins/ui/lualine/neoed.lua`.

## Leader Key

`<Space>` is the leader key. Key groups:

- `<leader>a` - AI/Claude Code
- `<leader>f` - File operations
- `<leader>g` - Git
- `<leader>j` - Jump/Flash
- `<leader>w` - Window navigation
