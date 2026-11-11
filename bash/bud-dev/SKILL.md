---
name: bud-dev
description: How the bud repo (a Neovim IDE driven by a small Go CLI) is built and extended. Use when working in a bud checkout, or when asked to add a language spec, a tool, a layout or a kit entry to bud.
---

# Working on bud

bud is a Go CLI (`cmd/bud`, `internal/`) that installs, launches, updates and syncs an isolated Neovim config (`NVIM_APPNAME=bud`, the repo's `nvim/`). The binary is the release: `nvim/`, `languages/`, `layouts/`, `tools/`, `migrations/` and `bundles/` are embedded (`embed.go`) and synced into `~/.config/bud`; `kit/kit.json` (also embedded) only lists the plugin marketplace and plugins `bud kit sync` installs into Claude Code, where `core.md` comes from, and the MCP servers `bud doctor` expects (D77, D78).

Read `CLAUDE.md` at the repo root first: it holds the rules and points to `docs/internals/` for how each area works; read the file for the area you are changing. `BASE.md` is the plan plus a numbered decision log (D1, D2, ...); when a decision changes, update it there too.

## Hard rules

- Go standard library only (D1); commands use `flag.FlagSet`. Config and data files are JSON (D2).
- Flags go before positionals (D4). macOS and Linux only (D22).
- Commands return errors; only `cli.ExitCode` prints them.
- Every bud path comes from `internal/paths.Resolve`; files bud rewrites go through `internal/atomicfile`.
- Startup budget: 50 ms to the first screen (D35). Slow editor work goes on `vim.schedule` or lazy loading.
- Editor UI uses the robot `[o.o]` and Nerd Font glyphs from `bud.icons`, never emoji.

## Adding things

- **A language:** copy `languages/_template.lua` (unknown fields are errors), then add a case to `scripts/lang_check.lua` and run `just lang-check <name>`.
- **A tool:** `tools/<name>/manifest.json` + `init.lua` returning `{ setup = function(manifest) end }` (D54). Personal ones go in `~/.local/share/bud/user-tools/<name>/`; `:BudGen` drafts one.
- **A layout:** `layouts/<name>.lua` listing panes by kind (`tree`, `git`, `chat`), side and size (D45).
- **A kit entry:** `bud kit add plugin <name@marketplace>` or `bud kit add marketplace <name> <source>` in a checkout (D58, D77). Skills, agents, commands and output styles go in jgarner9/bud-plugins, MCP servers in clod; bud carries no Claude content or secrets of its own.
- **A command:** one file in `internal/cli/` calling `RegisterCommand` from `init()`.

## Checking

`just check` is what CI runs: gofmt, stylua + selene, go vet, shellcheck, `go test ./...`, the headless Lua tests in `tests/lua/` and the smoke test. Tests swap package-level vars and restore them with `t.Cleanup`. Commits are lowercase conventional (`feat:`, `fix:`, `chore:`, `docs:`) with the Linear issue id.
