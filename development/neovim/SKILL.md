---
name: neovim
description: Rules for Neovim plugin configuration and Lua code in this dotfiles repo
---

# Neovim Development Rules

Load this skill when working on Neovim configuration or Lua code for Neovim.

## 1. Lua Module Pattern: Avoid the `M` Pattern

**CRITICAL**: Do NOT use the `local M = {}` pattern for Lua modules in this codebase.

**Bad** - Using M pattern:

```lua
local M = {}
function M.foo() end
function M.bar() end
return M
```

**Good** - Direct module return:

```lua
local function foo() end
local function bar() end
return { foo = foo, bar = bar }
```

**Why:**

- More explicit and readable
- Follows the coding style guideline of separating declaration from export
- Makes the public API immediately clear at the bottom of the file

## 2. Ask User to Help Debug

When encountering visual/UI issues you can't diagnose from code alone, ask user to run diagnostic commands:

- Color/highlight issues: Ask user to run `:Inspect` on the affected character
- Syntax issues: Ask for `:TSHighlightCapturesUnderCursor`
- Option issues: Ask for `:set option?`

Don't guess - get data first.

## 3. MANDATORY: Read Local Documentation Before Implementation

**CRITICAL BLOCKING REQUIREMENT**: Before implementing ANY Neovim feature or plugin configuration, you MUST read the relevant local documentation first.

**For Neovim Plugins:**

1. **BEFORE** implementing or configuring ANY plugin feature, read the plugin's local help files
2. **Location**: `~/.local/share/nvim/lazy/<plugin-name>/`
   - Help files: `doc/*.txt`
   - README: `README.md`
   - Source code: `lua/` (for defaults and examples)
3. Use the Read tool to verify options, configuration format, and correct parameter names
4. **Only after** reading local docs should you proceed with implementation

**For Neovim Native Features:**

1. **BEFORE** implementing ANY native Neovim feature (options, keymaps, autocommands, etc.), read Neovim's local documentation
2. **Location**: Neovim runtime documentation
   - Help files: Use `:help <topic>` or read from Neovim's help system
   - Runtime docs: `/opt/homebrew/Cellar/neovim/0.11.5_1/share/nvim/runtime/doc/`
3. Verify correct API usage, option names, and function signatures from local docs

**Why this is mandatory:**

- Prevents using deprecated/wrong options (like `jump_to_single_result` vs `jump1`)
- Ensures version compatibility with installed plugins
- Faster and more accurate than web searches
- Works offline

**Only use web searches after reading local docs if:**

- Local docs don't exist or are incomplete
- You need clarification beyond what local docs provide
- You're researching whether to add a NEW plugin (not yet installed)

## 4. Neovim Documentation Locations

When updating documentation for Neovim changes:

- **Neovim docs**: `~/.dotfiles/config.home.symlink/nvim/*.md`
