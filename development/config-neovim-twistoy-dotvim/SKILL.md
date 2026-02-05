---
name: config-neovim
description: Use this skill when working with neovim configurations, Lua scripting for Neovim, plugin management, LSP setup, or any Neovim-related development tasks.
---

# config-neovim

## When To Use

Use this skill when working with neovim configurations, Lua scripting for Neovim, plugin management, LSP setup, or any Neovim-related development tasks.

## What Can Do

- Manage plugins
- Manage keymaps
- Manage LSP setup

## Quick Reference

### Add a new plugin

Create file in appropriate caregory under `lua/dotvim/plugins`.

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

Create or update file under `lsp/`.

```lua
---@type vim.lsp.Config
return {
  cmd = { ... },
  init_options = { ... }
  capabilities = { ... },
}
```

### Adding a Keymap

If the keymap is highly plugin-related, config the keymap in that plugin's spec.

```lua
return {
  "author/plugin-name",
  keys = { ... } -- config keymaps here
}
```

Others, config the keymap in `lua/dotvim/configs/keymaps.lua`.

```lua
vim.keymap.set("n", "<M-n>", "<cmd>nohl<CR>", { desc = "nohl" })
```

If the new keymap also creates a new which-key group, add the group in `lua/dotvim/plugins/base/which-key.lua`.

