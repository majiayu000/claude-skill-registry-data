---
name: annotating-code-in-nvim
description: nvim keymaps for line annotations (haunt.nvim) and region highlights (vim-highlighter). Use to annotate, note, or highlight code.
---

# Annotating and Highlighting Code in nvim

Two plugins, both storing state **outside** the source file so nothing reaches git.
Configured in `nvim/lua/custom/plugins/haunt.lua` and `nvim/lua/custom/plugins/highlighter.lua`.

- **haunt.nvim** — a text note on a line, rendered as end-of-line virtual text.
- **vim-highlighter** — a highlighter-pen wash over an arbitrary region.

Both ride the text, because both are extmarks: haunt's note is one with
`right_gravity = true`, a wash is one with `end_row`/`end_col`. Inserting above,
below, or inside a marked span moves it.

## Annotations — `<leader>n`

| Task | Keys | Command |
|---|---|---|
| Add a note to this line, washed | `<leader>nn` | — |
| Add without the editor or the wash | — | `:HauntAnnotate the retry loop lives here` |
| Edit this line's note, wash untouched | `<leader>ne` | `:HauntAnnotate` (prefills old text) |
| Fold: inline ⇄ box above the line | `<leader>nz` | — |
| Delete this line's note | `<leader>nd` | `:HauntDelete` |
| Delete all notes in this file | `<leader>nc` | `:HauntClear` |
| Delete all notes, every file | `<leader>nC` | `:HauntClearAll` |
| Hide without deleting | `<leader>nt` / `<leader>nT` (all) | `:HauntToggle` |
| Next / previous note | `<leader>nj` / `<leader>nk` | `:HauntNext` / `:HauntPrev` |
| Picker over all notes | `<leader>nl` | `:HauntList` (`d` delete, `a` edit) |
| Notes to quickfix | `<leader>nq` | `:HauntQf` / `:HauntQfAll` |
| Reload after an external branch switch | — | `:HauntReload` |

Both `<leader>nn` and `<leader>ne` open the same editor — a scratch buffer in a
float, prefilled from whatever note is already on the line. The difference is
the wash: `<leader>nn` is `<leader>na` with the motion fixed at one line, so it
paints the line in the pen color too (`{count}<leader>nn` takes more lines, and
the pair is all-or-nothing the same way — `:q!` removes the wash). `<leader>ne`
only edits the text.

So `<leader>nn` is the key for *making* an annotation stand out, and
`<leader>ne` the one for rewording it — notably on a line whose wash came from
the middle of a `<leader>na` region, where a one-line wash of the current pen
would streak it.

Re-pressing `<leader>nn` on a line that is already washed keeps that wash rather
than stacking a second identical mark on it, which would then take two `f<BS>`
to remove. Only the first line of the span is tested.

Annotations are line-scoped either way; there are no range annotations.

### The editor

haunt's own prompt is `vim.fn.input` (`api.lua:544`), which is cmdline editing
and nothing else — no motions, no undo, no text objects. `custom/annot.lua`
replaces it with an `acwrite` scratch buffer in a float, so every vim key works
while writing a note. `api.annotate(text)` takes the string directly and
updates an existing note rather than duplicating it, so the editor only has to
produce text.

| Task | Keys |
|---|---|
| Keep the note | `:w` (applies, stays open) or `:wq` |
| Discard it | `:q!` |

Contract matches the commit popup in `custom/stage_commit.lua`: writing an empty
buffer is **refused** and leaves `modified` set, so `:wq` blocks rather than
dropping the note silently. `:q!` is the only way to abandon one.

Multiple lines are stored joined by a literal `\n`, which is what haunt's box
renderer splits on. Collapsed, a two-line note shows the escaped form inline;
folded open, it renders as two lines in the box.

### The fold — `<leader>nz`

`<leader>nz` flips the note on the cursor line between its inline form and a box
above the line, one note at a time. The box is `virt_lines` — real rendered rows
*inside* the buffer, so it pushes the code below it down while open, exactly as
an open fold does. It is not a floating window.

Width follows `above_max_width` (80, also clamped to the window), so a long note
wraps instead of running off the edge — which is the point, since eol virtual
text can't be reached by any motion.

### Inline notes are clipped

A collapsed note never crosses the window edge: it is cut to the room left on
its line and marked with `…`, meaning "the fold has the rest". Only the
*displayed* string is clipped — the store always keeps the whole note.

The clip is applied by wrapping `display.show_annotation`, which every render
path funnels through (create, restore, toggle, reload, the fold), so there is no
set of events to keep in step with the plugin. It is re-measured on
`VimResized`, `WinResized`, `WinNew` and `WinClosed`; `M.reclip()` redoes it by
hand.

Two rules worth knowing:

- **Measured in display cells, not characters**, so a note containing
  double-width text still lands inside the budget.
- **Clipped to the narrowest window showing the buffer.** The extmark belongs to
  the buffer, not a window, so one clip serves every split — the narrowest is
  the only choice that cannot overflow in any of them.

This works because haunt reads `virt_text_pos` once per render and bakes the
outcome into the extmark: `above` yields `virt_lines`, `eol` yields `virt_text`.
So one note can be re-rendered in the other mode while the rest stay put, and
the extmark *is* the fold state — nothing to track separately, nothing that can
desync. The global config is flipped and restored around the single re-render.

Not persisted, deliberately: like folds, every note comes back collapsed.

## Highlight a region *and* annotate it — `<leader>na`

One stroke for both, over the same span (`nvim/lua/custom/annot.lua`). The note
lands on the region's first line.

| Task | Keys |
|---|---|
| Region + note | `<leader>na{motion}` — `<leader>na4j`, `<leader>naap`, `<leader>nai{` |
| Just this line | `<leader>na_` |
| From a visual selection | Select, then `<leader>na` |
| From a `:` range | `:12,15HiNote 3` (color is a one-off override) |

`<leader>na` is an **operator**, so it takes a motion the way `d` does. The count
belongs to the motion, as in `4dj` — `<leader>na4j` marks the cursor line plus 4
below.

The pair is **all or nothing**: `:q!` out of the editor removes the wash too and
puts the cursor back. For a wash with no note, use `t<CR>` instead.

### Removing one

The wash and the note are two independent marks, so one keystroke made them and
two remove them. Put the cursor on the region's **first line**, where both are
reachable:

Same two marks for `<leader>nn`, on the one line it covers.

| To remove | Press |
|---|---|
| The note | `<leader>nd` |
| The wash | `f<BS>` (cursor anywhere inside it) |
| Both | `<leader>nd` then `f<BS>` |
| Every wash in the window | `f<C-L>` |
| Every note in the file | `<leader>nc` |

To reword a note, `<leader>ne` (the editor opens prefilled). To recolor a wash,
set the pen and press `<leader>nr` with the cursor inside it — see below.

## Color — one global pen

Nothing picks a color on its own. `vim.g.annot_pen` (default 1) is the pen, and
every highlight uses it: the operator above, and a bare `t<CR>`.

| Task | Keys |
|---|---|
| Set the pen | `<leader>n1` … `<leader>n6` |
| Show the palette as swatches | `<leader>np` |
| Set the pen by count | `3<leader>np`, or `:HiPen 3` |
| Recolor the wash under the cursor | `<leader>nr` |

Pin a default in your config with `vim.g.annot_pen = 3`. The pen is session
state otherwise. Out-of-range values are rejected and leave the pen alone.

`<leader>nr` overwrites the wash's extmark by `id`, so its span is kept and the
note and any neighbouring wash are left alone — `f<BS>` and re-marking would
lose the span and could take an overlapping wash with it. It handles both wash
shapes, `hl_group` over a span and `line_hl_group` over whole lines, and finds a
wash that began on an earlier line (`overlap`). The recolor is persisted at
once.

**A wash keeps your syntax highlighting**, because a pen is an index into
vim-highlighter's *background-only* colors — pen 1 is `HiColor80` — and not into
its default palette. `HiColor1..14` each set a foreground as well, so a wash of
one flattens the span to a single color; `HiColor80..89` set only a background,
so treesitter's colors show through. The plugin calls those its multiline colors
(`s:MultilineColor`) and honors them anywhere.

There are six of them, hence pens 1–6. The count is probed rather than
hardcoded, so a `HiColor86` you define by hand joins the pen automatically.

`f<CR>`, the pattern highlighter, is the plugin's own key and still cycles the
opaque 1–14 palette. It colors every occurrence of a word, which is a different
job from washing a region.

### The note's own color

The pen colors the wash only. The note is washed too, but in one fixed color
that ignores the pen: `HauntAnnotation`, which `custom/annot.lua` links to
`vim.g.annot_note_hl` (default `'HiColor9'`, grey).

That is a highlight **group name**, not a number, precisely so it cannot be
mistaken for a pen index — `annot_pen` counts pens, `annot_note_hl` names a
group. It defaults into the opaque `HiColor1..14` palette rather than the
background-only pack the pens use: a note is virtual text with no code
underneath it, so there is no syntax to preserve and a solid chip reads better
than a tint.

Change it with `vim.g.annot_note_hl = 'HiColor4'` plus
`:lua require('custom.annot').define_note_hl()`, or set it before the plugin
loads. Any group works — `'Comment'` gives faint blame-style ghost text with no
background.

A link, not copied attributes: `:colorscheme` runs `hi clear`, so the group is
re-established from a `ColorScheme` autocmd, and linking means it picks up
vim-highlighter's own dark/light retune of `HiColor*` without having to run
after it. `define_note_hl` calls `ensure_loaded()` first, because a file with
notes but no saved washes never runs a `:Hi` command and the link would
otherwise resolve to an undefined group.

**Per-note colors are not available.** haunt bakes the group name into each
extmark, so setting `virt_text_hl` to the live pen just before annotating does
work — but only `{file, line, note}` is persisted, so every note re-rendered by
a reload or `<leader>nT` comes back in whatever color was configured at that
moment, collapsing them all to one. It would look right until the first
restart.

## Region highlights alone — `t<CR>`

`t<CR>` is positional (the exact span selected). `f<CR>` is the *other* feature —
pattern highlighting, which colors every occurrence of a word.

| Task | Keys |
|---|---|
| Highlight a region | Select with `v`/`V`/motion, then `t<CR>` |
| Highlight this line | `t<CR>` in normal mode |
| Pick a color | Set the pen (`<leader>n3`); `t<CR>` ignores counts |
| Erase one highlight | Cursor inside it, `f<BS>` (works on a selection too) |
| Erase all in the window | `f<C-L>` |
| Jump between highlights | `:Hi {` / `:Hi }` (any color), `:Hi [` / `:Hi ]` (same color) |
| Highlight every occurrence of a word | `f<CR>` on the word |
| Save this file's highlights | automatic — `<leader>Hs` to force |
| Load by hand | `<leader>Hl` (automatic on `BufWinEnter`) |

Multiline selections become positional automatically. `f<CR> f<BS> f<Tab> t<CR>`
all have visual-mode variants; `f<C-L>` is normal mode only. Plain `f{char}` and
`t{char}` motions are unaffected.

## Storage

- Annotations: `~/.local/share/nvim/haunt/<project-hash>.json`, project-relative
  paths, one file **per git branch**. Saved on every change.
- Highlights: `~/.local/share/nvim/highlighter/<slugified-path>.hl`.

## Traps

- **Both kinds now persist themselves.** Highlights autosave on add and on
  delete (the mutating keys `t<CR>`/`f<BS>`/`f<C-L>` are this config's wrappers,
  which write through), plus `BufWinLeave`, `BufWritePost` and `VimLeavePre`.
- **Deleting the last highlight deletes the store**, including the `.hl.o`
  backup vim-highlighter renames the old file to on every save — otherwise a
  copy of the just-deleted highlights would survive on disk.
- **Pruning is gated on `b:hi_load_ok`.** An empty buffer only means "no
  highlights" if a load actually ran for it; without that flag autosave leaves
  the store alone rather than discarding it.
- **An empty note is refused, not treated as a delete.** Writing an empty editor
  buffer errors and leaves it open; `:q!` discards. Use `<leader>nd` to delete.
  (For `<leader>na`, `:q!` aborts the whole gesture — see above.)
- **The editor's callbacks must not touch buffer `0`.** During `BufWipeout` the
  editor is still the current buffer, so the wash rollback and the highlight
  autosave — both of which reach for buffer `0` — would act on the editor and
  silently do nothing. `edit_note` defers them and runs them inside
  `nvim_win_call` on the annotated window.
- **`win_findbuf` does not take nvim's buffer-0 convention.** The render paths
  do pass `0` for "current buffer", and `win_findbuf(0)` finds no window at all
  — which silently disabled clipping on every path except the first render.
  `clip` resolves `0` to the current buffer before asking.
- **`WinResized` does not fire for a split.** Opening one halves the width but
  emits only `WinNew`, so the re-clip listens for all four geometry events.
- **`<leader>na` is asynchronous now.** The wash is placed and persisted before
  the note exists, and is rolled back later if you `:q!`. A `kill -9` with the
  editor open leaves the wash, which is a legal state — a wash needs no note.
- **Rollback deletes extmarks by identity, not position.** `custom/annot.lua`
  snapshots vim-highlighter's `HiColor` namespace before highlighting and removes
  only marks that appeared, so aborting over an existing wash never eats it.
  Deleting the extmark is sufficient cleanup because the plugin's save routine
  enumerates live marks rather than keeping a side table.
- **Never use bare `:Hi save` / `:Hi load`.** They share one `_.hl`, and a saved
  positional highlight stores only `line,col` with no file path — stock load
  replays one file's coordinates into whatever buffer is current. The
  `<leader>Hs`/`<leader>Hl` wrappers key the file per buffer path; use them.
- **Neither re-anchors after an external edit.** Only `{file, line, note}` is
  persisted, so a `git pull` or a formatter run while nvim is closed brings marks
  back on stale line numbers. Drift is exact only while the buffer is open.
- **Never pass color `0`/nil through to `highlighter#Command`.** Its optional
  second argument overrides the color, but falling back to `0` makes it read
  `v:count` instead — a line count of 4 would silently mean color 4. The wrapper
  in `custom/annot.lua` always passes an explicit color for this reason.
- **`t<CR>` is this config's mapping, not the plugin's.** `vim.g.HiSetSL = ''`
  suppresses vim-highlighter's own version so the pen applies. `f<CR>` is left
  as-is on purpose: an explicit color argument disables its toggle-off, which
  vim-highlighter only honors when no color was given.
- **`HiColor*` groups are defined lazily**, inside vim-highlighter's `s:Load()`
  on first command. Anything counting them before that sees zero.
- `<leader>h` is *not* the annotation prefix (it is window-left and gitsigns'
  hunk group); upstream haunt docs suggest it, this config uses `<leader>n`.
