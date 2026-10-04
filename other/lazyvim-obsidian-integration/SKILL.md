---
name: lazyvim-obsidian-integration
description: This skill should be used when configuring obsidian-nvim/obsidian.nvim navigation keymaps, resolving obsidian.nvim vs render-markdown.nvim UI conflicts, wiring blink.cmp completion for obsidian.nvim, or scoping markdownlint-cli2 rules to a specific directory (e.g. an Obsidian vault) without affecting other markdown files.
---

## obsidian.nvim API surface (obsidian-nvim/obsidian.nvim fork, v3.16.x)

- `smart_action` lives in `require("obsidian.actions")`, NOT `obsidian.api`. It's an
  expr-mapped function (returns a command string), so bind it with `expr = true`.
- Cursor-context detection helpers (`cursor_link`, `cursor_tag`, `cursor_heading`,
  `cursor_checkbox`, `cursor_frontmatter`) live in `require("obsidian.api")`.
- `<CR>` (smart_action) and `]o`/`[o` (nav_link) are already auto-bound on every note
  buffer via the `ObsidianNoteEnter` internal wiring, gated by `vim.g.obsidian_default_keymap`
  (default true — don't assume you need to bind `<CR>` yourself; rebinding is redundant
  but harmless for readability/ownership).
- To scope keymaps to vault notes only (not all markdown buffers), hook the `User`
  autocmd with pattern `"ObsidianNoteEnter"` — it only fires for buffers obsidian.nvim
  recognizes as notes inside a configured workspace:
  ```lua
  vim.api.nvim_create_autocmd("User", {
    pattern = "ObsidianNoteEnter",
    callback = function(ev)
      vim.keymap.set("n", "<leader>ch", "<cmd>Obsidian toggle_checkbox<cr>", { buffer = ev.buf })
    end,
  })
  ```
- For a `gf` passthrough that follows wikilinks but falls back to plain `gf` elsewhere,
  wrap `api.cursor_link()` in `pcall` — defensive against API drift across versions:
  ```lua
  vim.keymap.set("n", "gf", function()
    local ok, link = pcall(require("obsidian.api").cursor_link)
    if ok and link then vim.cmd("Obsidian follow_link") else vim.cmd("normal! gf") end
  end, { buffer = ev.buf })
  ```
- Don't guess API module paths from memory/docs alone — grep the installed plugin
  source under `~/.local/share/nvim/lazy/obsidian.nvim/lua/` to confirm, since this
  fork has moved functions between modules across releases.

## ui.enable = false fully disables the renderer (no render-markdown.nvim conflict)

`ui.enable = false` in obsidian.nvim opts short-circuits its entire concealer module
(confirmed in `lua/obsidian/workspace.lua`, gated by `has_no_renderer and (options.ui.enable or options.ui.enabled)`).
When paired with `render-markdown.nvim` as the sole renderer, there's no double-render
of bullets/checkboxes/headings — no `bullets = vim.NIL` workaround needed. That
workaround only applies when obsidian.nvim's own UI is left enabled alongside another renderer.

## blink.cmp: this obsidian.nvim version uses in-process LSP for completion

Newer obsidian-nvim/obsidian.nvim releases migrated wikilink/tag completion to an
in-process LSP server, not a blink.cmp completion-source injection. Required config:
```lua
{
  "saghen/blink.cmp",
  opts = { sources = { per_filetype = { markdown = { "lsp" } } } },
}
```
Confirm with `require("obsidian.lsp.util").check_completion_availability()` — it returns
a descriptive string if blink.cmp isn't configured for `"lsp"` in markdown, nil if fine.
Older upstream/fork versions instead auto-inject `obsidian`/`obsidian_new`/`obsidian_tags`
sources when `per_filetype.markdown` is present — don't assume which model applies;
check the installed version's `lua/obsidian/completion/` or `lua/obsidian/lsp/` dir.

## markdownlint-cli2: directory-scoped config for partial rule overrides

markdownlint-cli2 walks up from each linted file to find the nearest
`.markdownlint-cli2.jsonc`, so you can override rules for one directory tree (e.g. an
Obsidian vault with long soft-wrapped lines) without touching the global/repo config
used by `conform.nvim`'s format-on-save or other markdown files:

```jsonc
// ~/Documents/MyVault/.markdownlint-cli2.jsonc
{
  "config": {
    "MD013": false
  }
}
```

This is the correct fix for "rule X doesn't make sense for this content" — NOT
`vim.b[buf].autoformat = false` in LazyVim, which disables the *entire* formatter
chain (prettier + markdownlint-cli2 --fix + anything else in `formatters_by_ft`) for
that buffer, including auto-fixes you still want (e.g. MD022 blank-lines-around-headings).

Verify scoping directly with the binary rather than trusting nvim diagnostics alone:
```bash
MDLINT=~/.local/share/nvim/mason/bin/markdownlint-cli2
"$MDLINT" "/path/inside/vault/note.md"   # MD013 should be absent
"$MDLINT" "/path/outside/scratch.md"     # MD013 should still fire
```
