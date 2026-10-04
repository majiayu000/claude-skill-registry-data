---
name: mytex-latex
description: Reference for writing, compiling, and debugging LaTeX with the myvimtex setup (`~/dotfiles/myvimtex`, a lazy.nvim plugin loaded by the daily driver) and for LaTeX authoring problems generally. Use when editing a `.tex` file in Neovim (plain `nvim` or the `mytex` wrapper), choosing VimTeX motions/text-objects/TOC commands, adding or debugging a LuaSnip snippet in `luasnippets/tex.lua`, diagnosing a tectonic compile error or Skim forward/reverse-sync problem, or explaining a LaTeX error message/syntax question even outside this setup.
---

# mytex — LaTeX authoring in Neovim

## Overview

myvimtex (`~/dotfiles/myvimtex`) is a **lazy.nvim plugin** loaded by the
daily-driver config as a `dir` spec with `import = 'latex.plugins'`; every
spec inside is `ft = 'tex'`, so opening any `.tex` file in plain `nvim`
gives the full LaTeX experience and non-tex sessions never load it.
`mytex <file.tex>` is an optional macOS wrapper that only adds the Skim
reverse-search socket (`--listen /tmp/nvimsocket`). Compiler: **tectonic**.
Viewer: **Skim** (SyncTeX forward/reverse search). Snippets: **LuaSnip**,
defined in `luasnippets/tex.lua`, expand via `blink.cmp`. Localleader is
`space`; the VimTeX mapping prefix is moved to `<localleader>v` (which-key
collision with kickstart's `<leader>l`), so VimTeX docs' `\ll` = `Space vl`
here.

Canonical, evolving docs live in the repo itself — `README.md` (install),
`GUIDE.md` (day-to-day usage + append-only snag log). Read `GUIDE.md` for
anything not covered below or if a fact here seems stale; it accumulates
new snags over time and this skill won't auto-update with it.

## Compile / view / sync

| Keys | Action |
|---|---|
| `Space vl` | Compile (tectonic, single-shot — no watch mode; re-run after edits) |
| `Space ve` | Quickfix with compile errors (spans all chapter files) |
| `Space vo` | Raw compiler output |
| `Space vv` | Forward search — open Skim at current line |
| ⌘-click in Skim | Reverse search — jump nvim to that source line (only the most-recently-launched `mytex` session receives it) |
| `Space vc` | Clean aux files |
| `Space vi` | Session info (shows detected main file) |
| `:VimtexCountWords` | Word count |

Multi-file projects: open **any** file — VimTeX scans for the file that
`\input`s/`\include`s it and treats that as the project root for compile,
TOC, and SyncTeX. To iterate fast on one chapter of an `\include`-based
project, add `\includeonly{chaptername}` to the main file while drafting,
remove it for full builds.

## Navigating and editing structurally

| Keys | Action |
|---|---|
| `Space vt` | TOC window (project-wide outline); `Enter` jump+close, `Space` jump+keep-open, `r` refresh, `L`/`I`/`T`/`C` toggle label/include/todo/content layers, `-`/`+` depth, `f`/`F` filter |
| `]]` / `[[` | Next/prev section start (`][`/`[]` for ends) |
| `]m` / `[m` | Next/prev environment |
| `]n` / `[n` | Next/prev math zone |
| `%` | Bounce `\begin`/`\end`, `$...$`, delimiters |
| `gf` on `\input{}`/`\include{}` | Open that file |
| `K` on a command | Open its package docs |

Text objects (`ie`/`ae` environment, `i$`/`a$` math zone, `ic`/`ac`
command, `id`/`ad` delimiters, `iP`/`aP` section) combine with
`c`/`d`/`v`/`y` — e.g. `cie` rewrites an environment's contents, `daP`
deletes a whole section.

Surround-style: `cse`/`dse` change/delete environment wrapper (edits
`\begin`+`\end` together), `csc`/`dsc` change/delete command
(`\textbf{x}`→`\emph{x}`), `cs$`/`ds$` and `csd`/`dsd` for math/generic
delimiters. Toggles: `tse` starred environment (`equation`↔`equation*`),
`tsc` starred command, `tsd` `(...)`↔`\left(...\right)`, `tsf`
`a/b`↔`\frac{a}{b}`.

## Snippets (`luasnippets/tex.lua`)

| Trigger | Kind | Expands to |
|---|---|---|
| `beg` | completion (accept `Enter`, not `Tab`) | `\begin{env}...\end{env}`, name mirrored via `rep(1)` |
| `fig` | completion | figure block (`includegraphics`, caption, `fig:` label) |
| `item` | completion | empty `itemize` block |
| `itemN` (e.g. `item3`) | regex-trigger, auto-expand | `itemize` block pre-populated with N `\item` lines |
| `it` | completion | `\item ` |
| `;a` / `;b` / `;t` | auto-expand, no accept key | `\alpha` / `\beta` / `\theta` |

`vim.g.vimtex_imaps_enabled = 0` so VimTeX's own insert mappings don't
fight LuaSnip's. Accept completion-menu snippets with `Enter`, not `Tab`
(this config's blink.cmp uses `preset = 'enter'`); if a literal buffer word
matching the trigger already exists, blink.cmp may rank the buffer-word
match above the snippet — arrow down (`<C-j>`/`<Down>`) to the snippet
entry first.

**Adding a new snippet:** a plain templated block goes in `snippets`
(completion, needs an accept key), built with `fmt([[...]], { i(1,
'placeholder'), ... })` — e.g. `fig` itself:

```lua
s('fig', fmt(
  [[
\begin{{figure}}[htbp]
	\centering
	\includegraphics[width=\linewidth]{{{}}}
	\caption{{{}}}
	\label{{fig:{}}}
\end{{figure}}]],
  { i(1, 'path'), i(2, 'caption'), i(3, 'label') }
))
```

A word-shaped trigger like `eq` or `thm` belongs here, not in
`autosnippets` — `autosnippets` fire the instant the trigger is typed,
with no accept step and no chance to back out, so a bare word trigger
there would fire mid-prose the moment you typed it as an ordinary word.
`autosnippets` is only safe for triggers that can't occur as normal text
— either a leading-sigil trigger (`;a`, `;b`, `;t` — the `;` guarantees it
never appears in prose) or a regex trigger distinctive enough not to
collide (`item(%d+)`).

**Regex-triggered snippets whose content depends on the match** (like
`itemN`) can't use blink.cmp's completion menu at all — an unset `name`
falls back to the raw Lua pattern (e.g. `item(%d+)`), which can't
fuzzy-match what you typed. Instead they belong in `autosnippets` with
`regTrig = true`, and build their body with a `dynamic_node` that reads
`snip.captures[1]`:

```lua
local function item_nodes(_, snip)
  local n = tonumber(snip.captures[1]) or 1
  local nodes = {}
  for j = 1, n do
    if j > 1 then table.insert(nodes, t { '', '\t' }) end
    table.insert(nodes, t '\\item ')
    table.insert(nodes, i(j))
  end
  return sn(nil, nodes)
end
-- in autosnippets:
s({ trig = 'item(%d+)', regTrig = true }, fmt(
  [[\begin{{itemize}}\n\t{}\n\end{{itemize}}\n{}]],
  { d(1, item_nodes, {}), i(0) }
))
```

`after/ftplugin/tex.lua` hooks `InsertCharPre` → `luasnip.expand_auto()`
(LuaSnip doesn't call this itself) and guards against double-loading,
since the daily driver's lazy.nvim re-dispatches `FileType` once deferred
plugins finish loading.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `\alpha` doesn't render as α | (1) treesitter highlight overrides `:syntax`'s conceal rules — needs `highlight.disable = { 'latex' }` in the daily driver; (2) `conceallevel` defaults to 0; (3) Greek conceal is **math-mode only** (`texCmdGreek` is contained in `texClusterMath`) | Set `conceallevel=2`, `concealcursor=''` for tex buffers (leaving `n`/`i` out of `concealcursor` keeps the *current* line raw/unconcealed so you can edit it, while other lines stay concealed); write `$\alpha$`, not bare `\alpha` |
| `beg<Tab>` does nothing / buffer-word offered instead of snippet | blink.cmp `preset = 'enter'`; buffer-word source can outrank the snippet | Accept with `Enter`; arrow to the snippet entry first if needed |
| ⌘-click in Skim opens a disconnected new nvim | Skim's reverse search shells out to `nvr` (neovim-remote — a CLI that sends commands to a running nvim's RPC socket), which falls back to `/tmp/nvimsocket` when Skim's subprocess has no `$NVIM`; nothing listening there | `mytex` must launch nvim with `--listen /tmp/nvimsocket` so `nvr`'s fallback address actually has a listener |
| `Space vv` lands consistently a few lines below the cursor, or does nothing | Missing/stale synctex: PDF was compiled without `--synctex` (CLI habit) or the last compile failed and the PDF is frozen — Skim silently falls back to text-matching against the stale PDF | Fix the compile error, recompile via `Space vl`; verify `.synctex.gz` exists next to the PDF. See "How SyncTeX actually connects the pieces" below |
| tectonic halts: "Missing number, treated as zero", log points at an unrelated file | A line right after `\\` starts with a bare `[` — LaTeX parses `\\[` as the optional vertical-space argument | Brace it: `{[}text{]}`. Rule: never start a line after `\\` with a bare `[` |
| TOC shows TODOs/includes but no chapter/section outline | (1) content layer toggled off (`C` in TOC to re-enable); (2) `\begin {document}` has a space — VimTeX's preamble-end regex requires no space, so it never leaves preamble mode | Press `C`; write `\begin{document}` with no space |
| `sh: kpsewhich: command not found` in TOC | VimTeX shells out to `kpsewhich` (TeX Live) for bib paths; tectonic doesn't ship it | Cosmetic only, `.bib` is still found — ignore |
| tectonic halts on an error pdflatex would push through | tectonic stops at potentially-recoverable errors by default instead of emitting a broken PDF | Fix the error rather than forcing past, unless it's a legacy doc you deliberately want to force |
| TeX error message/context looks truncated | default `\errorcontextlines` is too small | Add `\errorcontextlines=200` to surface the real backtrace |

General LaTeX gotchas worth knowing regardless of editor: `Undefined
control sequence` usually means a missing `\usepackage` or a typo in the
command name; `Missing $ inserted` means a math-only command (`\alpha`,
`\frac`, `_`, `^`) was used in text mode — wrap it in `$...$`; prefer
`\includegraphics` + the `graphicx` package and `biblatex`/`natbib` +
`hyperref` (load `hyperref` last) as defaults when a document doesn't
specify its own package choices.

## How SyncTeX actually connects the pieces (debugging theory)

Three layers, three contracts — knowing which one broke saves an hour:

1. **Engine (tectonic):** `--synctex` writes `<pdfname>.synctex.gz` — a
   viewer-agnostic text database: `Input:` records (tag → source path),
   then box records `(tag, line) → (page, x, y)`. Plain CLI
   `tectonic file.tex` does NOT pass `--synctex`; vimtex's `Space vl`
   always does.
2. **Viewer (Skim):** not TeX-agnostic — it embeds the reference synctex
   parser (same library as Zathura/Okular/Sumatra) and exposes TeX-aware
   scripting (`go to TeX line N from file F`). It finds the synctex file
   **by basename next to the PDF**. With synctex data, resolution is
   line-exact (verified: mid-paragraph, lists, later pages). **Without it,
   Skim silently falls back to text-matching heuristics** — no error, just
   wrong-ish positions.
3. **Editor (vimtex):** never reads synctex; it only sends Apple Events
   (JXA `go({to: texLines[l-1], from: Path(file)})`, after `revert()` to
   reload the PDF). Reverse search is the mirror: Skim queries
   `(page,x,y) → (file,line)` and shells out to `nvr` per its
   `SKTeXEditor*` defaults.

**Diagnostic rule:** forward search landing consistently a few lines off
(stale-text heuristic match) or doing nothing (no match) means missing or
stale synctex — check that the last compile *succeeded* and that
`.synctex.gz` exists next to the PDF, before suspecting vimtex/Skim/mytex.
A CLI compile without `--synctex` silently poisons this for the whole
project. See GUIDE.md's 2026-07-22 snag entries for the full case study.

## Setup / architecture gotchas (only relevant when the setup misbehaves)

- myvimtex is a normal lazy.nvim plugin (dotfiles submodule); there is no
  separate config, lockfile, or data dir. The daily driver's
  `lazy-lock.json` pins everything — **vimtex is pinned to `a5949d2`**
  because vimtex master requires nvim 0.12.4+; `:Lazy update` breaks the
  LaTeX layer until nvim is upgraded (`:Lazy restore vimtex` recovers).
- Isolation = `ft = 'tex'` gating, not process isolation: tex plugins are
  in every nvim's spec but never load outside tex buffers. `vim.g.vimtex_*`
  globals ARE set in all sessions (lazy runs `init` hooks eagerly) — that's
  expected and inert.
- Snippets load via LuaSnip's rtp scan (`from_lua.load()` with no paths,
  which finds any `luasnippets/` dir on the runtimepath) — there is no
  hardcoded snippet path anywhere.
