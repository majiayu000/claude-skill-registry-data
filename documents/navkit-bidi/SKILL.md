---
name: navkit-bidi
description: Right-to-left text and the mirrored screen -- navkit/bidi.py (layout, order_cells for the viewer's and editor's rows, cells with logical indices, python-bidi's pure-Python UBA run step by step, arabic-reshaper and the lam-alef ligature, marks folded into their letter, caret_column/index_at/text_rtl), Surface.rtl and Surface.draw_runs, ScreenBuffer.mirrored and FLIP, Widget.mirrors (console, command line, viewer, editor, diff view, clock kept left to right) and arrows_mirrored, Application.direction/rtl/_unmirror (mouse and Left/Right), catalogue [meta] direction = "rtl" and i18n.is_rtl, --direction, TerminalInfo.bidi ("app"/"words", NAVKIT_BIDI), VTE's CSI 8 l, kitty's for_words. Use when text in Hebrew or Arabic looks wrong, a widget paints wrong on a mirrored screen, or adding a widget that paints text cell by cell.
---

# Right-to-left text and the mirrored screen

**Navigator lays right-to-left text out itself; no terminal is trusted to.** Measured (Oct 2026): VTE reorders a whole
screen row as one paragraph (columns, frames and overlapping windows trade places), kitty reverses glyphs of some runs
whatever order they arrive in, ghostty reorders nothing and joins no Arabic letter.

**Mirroring is a departure** from DOS Navigator, which never mirrored anything; asked for by the user (a right-to-left
language reads its screen right to left). It is the second standing exception beside the icon gutter.

## Text: `navkit/bidi.py`

- `layout(text, rtl) -> ((logical_index, cell), ...)`, visual order left to right, cached. Pure-LTR text short-cuts.
  Paragraph direction is the first strong letter's, else *rtl* (the surface's) -- so `( )` on a mirrored screen is laid
  out as inside Hebrew. Explicit format characters take part and get no cell.
- Arabic is shaped by `arabic-reshaper` **with ligatures off** (one letter in, one form out, indices kept); lam+alef
  is folded into its ligature by `_shape`, keeping the lam's index. Marks are folded into the letter before them
  before ordering, so a reversed run cannot put niqqud/harakat first. Brackets are mirrored at odd levels (L4).
- python-bidi is **held below 0.5**: 0.5+ is a Rust extension returning only the display string; Navigator needs each
  character's place (style, caret) and the Linux packages are `arch: all`. Its `bidi.algorithm` steps are run one by
  one with an `at` index stamped on each char dict.
- **0.4 predates Unicode 6.3's isolates and knows no class `""`**: an LRI/RLI/FSI/PDI, an unassigned code point or a
  noncharacter beside an RTL letter failed `resolve_implicit_levels`' assert inside a paint. `_classifiable()` hands
  the algorithm stand-ins of the same length (isolates as LRE/RLE/PDF, FSI by the next strong letter, the classless
  as U+FFFD's ON); the cells still show the real characters, and the isolates, like embeddings, get none.
- `caret_column(text, index, rtl)` / `index_at(text, column, rtl)`: columns as `draw_runs` paints them (reversed on a
  mirrored surface). The caret sits on the character it is before; at the end, past the end the paragraph grows from.
  `painted_cells(text, rtl)` is `(index, column, width)` per painted cell -- how `link_urls` (StaticText) marks an
  address where it was painted.
- `display_width(text)`: the cells `draw_runs` paints (marks on their letter, format characters none, lam-alef one).
  **Centring and right alignment measure with it, never `len()`** (titles, captions, labels, headers, panel names).
- `order_cells(chars, rtl, detect=True)`: *detect* false fixes the paragraph direction to *rtl* -- a console row
  (VTE's left to right), a wrapped viewer row (its whole line's direction, UBA's L1: break first, order each row).
- `char_width`: marks and every `Cf` (marks of direction, joiners, soft hyphen) are 0 wide.
- `reveal(text, mark="⁇", keep="")`: embeddings/overrides (U+202A..202E), isolates (U+2066..2069) and C0/C1 controls
  become *mark*, one character for one (a `len` still holds), so `photo` + U+202E + `gpj.exe` cannot paint as
  `photoexe.jpg`. LRM/RLM/ALM stay hidden (they cannot turn letters round). Applied to what is *shown* only --
  `Panel.shown_name` (rows, list widths, scroll, tooltips, info line; the mark reversed out of the row via
  `REVEALED`/`reveal_runs`), `escape_caption` (every dialog caption naming a file; keeps `\n`/`\t`), Ctrl+L, the quick
  view title, `TreeView` -- never to a name that is used (input values, the command line, file operations).
  `glyphs.hidden_mark(tier)`: `⁇`, `?` in ASCII.

## Painting: `Surface.rtl`, `draw_runs`, the mirror

- `Surface.draw_runs(x, y, [(text, style), ...], max_width)` is the one text primitive; `draw_text` is one run (ASCII
  on an LTR surface keeps a fast path). **A caption with a highlighted letter is one `draw_runs` call**
  (`draw_caption`, `shortcut_runs` in `navml/widgets/dialog/control`), or the letter lands in the wrong cell.
- The application composes the frame left to right with `_back.rtl` set, then `ScreenBuffer.mirrored()` flips it on
  the way out: rows reversed, wide characters kept owner-first, glyphs through `FLIP` (corners, tees, half blocks,
  pointers, arrows, brackets). `draw_runs` on an rtl surface writes reversed and FLIP-swapped, so the mirror puts text
  back the right way and against the right-hand edge of its span. **A glyph that points the layout's way is a
  `set_cell`, not text** (the submenu arrow), so it flips.
- **Text painted cell by cell with `set_cell` comes out reversed on a mirrored screen.** Use `draw_runs`, or keep the
  widget left to right.
- `Widget.mirrors = False` keeps a widget's content left to right inside the mirrored frame: `render_tree` gives it a
  view with `rtl=False` and `mirror()`s its rectangle afterwards, which the screen's mirror cancels. Set on
  `ScreenView` (console), `CommandLine`, `FileViewer`, `FileEditor`, `DiffView`, `Clock` (a blinked colon makes the
  time two numbers, which an RTL line swaps).
- **The console** (`navkit/console.py` `ConsoleScreen`) lays each row out as VTE does a line: `sync()` runs
  `order_cells(row, detect=False)` (paragraph left to right whatever the row starts with, so its blanks stay at the
  end) on the dirty rows only, keeping the written cells (`written`, for `prompt_cells`) and the laid ones (`surface`,
  `blit_into`), plus each row's order. `visual_x`/`logical_x` map columns: `ScreenView.cursor_position` paints the
  child's cursor where its column is shown, a click passed to a mouse-tracking program goes to the written column,
  and `text()` (selection, double-click, copy) takes the painted cells and copies what they cover in written order.
  A child sending `CSI 8 l` (BDSM explicit, `_Screen.implicit_bidi`; seeded on in the constructor *and* `reset()`,
  since pyte's constructor resets its modes after `reset()`) gets its rows unordered.
- **The diff view** (`DiffView._paint_line`) orders each side's line with `order_cells` as the viewer does; a line has
  one look, so only the characters move.
- **A line cut at the screen's edge is decoded whole before it is reordered** when it holds right-to-left text
  (`FileViewer._whole`, `DiffView`, up to `viewer.WHOLE_LINE` columns): its far end can be what is painted at the
  left. The viewer's search hit is scrolled to the column it is painted in (`show_hit`). Wrapped rows take their
  line's direction (`FileViewer._ordered`/`_line_rtl`).
- **The rendered Markdown/reST/HTML view**: a paragraph or heading whose first strong letter is right to left gets
  `Row.rtl` and `Row.lead` (its gutter/bullet cells) from the builder; `file_viewer._laid_row` orders what follows
  the lead right to left and sets it against the right edge (padding columns map to None for the marks).
- **File contents** (viewer, editor) are left to right *widgets* but their lines are still laid out: each painted row's
  cells go through `bidi.order_cells(chars)` -- the row as columns (`""` second halves, tabs already spread), returned
  as `(column, shown)` in visual order, or None when nothing changes (cached). Every per-cell decision keeps using the
  original column/offset: the viewer's search hit and tokens (looked up per cell once reordered, the one-pointer walk
  assumes growing offsets), the rendered view's marks, the editor's block/match (lit per cell by original column; the
  fill covers only what is past the text) and tokens. The viewer keeps lines left-aligned.
- **The editor right-aligns a right-to-left line** (its first strong letter Hebrew or Arabic; a departure, asked
  for): `_laid_line` gives a line's cells, painted order and `shift` = `max(width, painted length + 1) - painted
  length`, so the line ends against the window's right edge and the cell left of it -- where typing at its end
  appears, and where its end-of-line caret sits -- always exists; columns past the end run leftwards, clamped at 0.
  A line holding Hebrew or Arabic is laid out whole, never cut at the screen edge. Latin-first lines stay left.
  **Every mapping goes through `FileEditor._laid`**: `_visual_column`/`_logical_column` (cursor, click; a click right
  of an RTL line is its start), `_painted_here`, `_rect_spans`, `_text_column`, render (line-break cell, block
  fill, line-ending mark), `_follow` (scrolls by painted column), the current-column highlight. The editor's columns
  stay logical. Left/Right move to the neighbouring *painted* cell (`_step_visually`): on a left-to-right line off
  the left end it stays and off the right end goes past the text and on to the next line, as Right always did; on
  an RTL line mirrored -- Right at its right end (its start) stays, Left past its left end goes to the end and then
  on. Ctrl+Left/Right go to the nearest word start that way on screen (`_word_visually`), else on in reading order.
- `_ordered` keeps every column of a line: a lam-alef ligature's spare alef column becomes a `""` cell beside the
  next blank after it in the text (one blank wider, never a gap inside the word), or at the line's end, so tab stops
  after it hold.
- **A block the cursor marked is what is painted between its ends** (Word's visual selection): `FileEditor._painted_block`
  is the very `block` tuple `_set_block`/`_set_ordered` made (kept through `_follow_edit`, and through a recase that
  changes lengths, its ends moved through the recased text); any other block -- ^K C's copy, ^K R's read -- is the
  stretch it is. On an RTL line a caret is its cell's right-hand edge and the line's end the cell left of the text
  (`_painted_spans`). `_block_runs()` turns it into the text
  stretches it holds (`_painted_spans` per reordered line: between the ends on one line; from the start's cell towards
  the end the line reads to on the first; from the line's beginning to the end's cell on the last; whole lines
  between). **Every stream-block command goes through the runs** -- `block_text`, `_take_block`, ^K C/V, `_recase`,
  `block_lines`, `_cursor_in_block`, the right-click test; render lights a reordered line by `_block_picked`. A new
  stream-block command must use `_block_runs()`, never `document.text(*self.block)`. Line-based ones (indent, format) are
  unchanged.
- **A column block's columns are painted columns** (rectangle straight on screen): its corners are made painted --
  `_here` (Shift+movement, `_visual_column`), `_mark_span`/switch block (`_painted_column`), ^K C/V; `_rect_spans`
  gives what a line paints in them (scattered text stretches on a reordered line, `columns.span` elsewhere), used by
  pieces, delete, recase, sort keys, calc, `block_lines`, the cursor-in-block test; render compares the painted
  column for a rectangle (a match stays lit by the text's columns). `_line_spans(number)` is any block's stretches on
  a line; *Selected text* search covers first..last stretch and `find` passes over a match not wholly inside one.
  ^K I/U at a column block's left edge work on what is painted there: `_painted_insert` tries the blanks before
  and after the character painted at the edge, the preferred side first, lays each out, and keeps the one painting
  the blanks nearest the edge; on a right-aligned line they go just left of the edge (what is painted from the edge
  on stays put, the rest grows leftwards), and `_text_column` makes ^K U take the cell left of it, undoing ^K I. A stream block and the lone-line unindent
  still work at the line's start in the text (a Hebrew line's right-hand end). Combining
  marks join their letter's cell in both rows (`viewer.decode_cells`, `editor.columns.cells`).
- `Application._unmirror` runs on every event as it comes off the queue (once, so derived double-clicks are already
  converted; the original event's id is what `_posted` tracks): a mouse x is flipped, and flipped again inside an
  unmirrored widget (`Widget.unmirrored()`); Left/Right swap when the focused widget `arrows_mirrored()` (InputLine
  too: it moves by painted place, so the swap is always right on a mirrored screen). `_cursor` maps the caret through
  `_mirror_x` the same way.
- **InputLine** (so CommandLine and every field) moves by painted place once the value holds right-to-left text or
  sits on a mirrored surface (`_bidi()`): Left/Right to the neighbouring caret column (`_step`), Ctrl to the nearest
  word start that way (`_word_step`), off the painted text on to the end lying that way (the line scrolls). A
  selection is the cells painted between the anchor's caret and the cursor's (`picked()`, the editor's rule): copied
  in text order, deleted wholly, replaced at its first index; `selection` is its first..last for callers that want a
  range. Plain text keeps the index arithmetic.
- Direction: `Application.direction` (`auto`/`ltr`/`rtl`); `auto` is `i18n.is_rtl()`, a catalogue's
  `[meta] direction = "rtl"` (he, ar). Set from `[interface] direction` (Options > Settings > Interface, *Text
  direction*, applied at once by `Shell.settings`), which `--direction` overrides for a session. A change -- of it or
  of the language -- repaints everything (no underlay reuse), mirrored or not on the next frame (tested both ways,
  and dragging and sizing a window on a mirrored screen, `tests/test_windows.py`).
- **Columns in a translated table are laid out a column at a time**, never a translated string spaced to fit (a
  Hebrew one turns round as a whole and sits against the far edge): the attributes grid's headings are a Label per
  column at `Cluster.column_x(i)` (public, measured with `display_width`), the Top Ten's headings and lines a Label per
  column at `tetris.SCORE_COLUMNS`; the dBase structure box, whose field names are ASCII by the format, holds its
  rows left to right with an LRM opening every cell (`db_window._table_row`) -- one LRM at the line's start is not
  enough, two Hebrew cells with blanks between run together into one reversed stretch.

## Terminals: `TerminalInfo.bidi`

- `"app"` (default): cells are sent as laid out; `Terminal` sends `CSI 8 l` (ECMA-48 BDSM reset, explicit) before the
  screen is cleared -- VTE keeps the mode per line from when the line is made -- and `CSI 8 h` when it gives the screen
  back, so the console's programs get VTE's own bidi. Ignored (logged) by kitty/ghostty. `terminal.bidi_switch(info)`
  builds both strings:
  - `TerminalInfo.reorders` names a terminal that reorders and ignores BDSM but has its own switch, sent beside it
    (`BIDI_SWITCHES`): **Konsole** (`KONSOLE_VERSION`) `OSC 50;BidiRenderingEnabled=false/true`, **mlterm** (`MLTERM`
    or `TERM=mlterm*`) `OSC 5379;use_ctl=false/true` (`use_bidi` does nothing). Neither can be asked what it was, so
    leaving turns it back on, both defaults.
  - `TerminalInfo.multiplexer`: inside **screen** (`STY`) each sequence goes out wrapped in `ESC P … ESC \`, which
    screen passes on (works for VTE's BDSM and Konsole's OSC 50). Inside **tmux** (`TMUX`) nothing gets through --
    VTE's BDSM, Konsole's and mlterm's switches all failed with `allow-passthrough on` too, with or without a
    `refresh-client` after -- so the terminal's own bidi has to be switched off by hand there.
  - Probed (Oct 2026, the scratch probe paints `abc לאאך 123 def`: a reordering terminal puts `123` left of the
    Hebrew): VTE (xfce4-terminal) reorders, BDSM stops it; Konsole 23.08 and mlterm 3.9.3 reorder, only their own
    switch stops them (mlterm right-aligns an RTL line too); alacritty and ghostty reorder nothing (ghostty 1.4 also
    dropped two probe rows, a frame and Arabic, unexplained); kitty as below. Untested: WezTerm, foot (Wayland only),
    Windows Terminal.
- `--bidi {app,words}` overrides `NAVKIT_BIDI`, which overrides the detection.
- **No tier hands bidi back to the terminal**, deliberately: every terminal probed that does bidi (VTE, Konsole,
  mlterm) reorders a whole screen row as one paragraph, frames and side-by-side panels included, so text must reach it
  laid out with its own bidi off.
- `"words"` (kitty: `TERM=xterm-kitty` or `KITTY_WINDOW_ID`; `NAVKIT_BIDI` or `--bidi` overrides): `screen.for_words` sends kitty
  glyphs pre-reversed for it to put back, **styles left in place** (kitty moves glyphs, not colours). A run is broken by
  a space, a box/block character or a bold/italic change, not by colour; a run starting with Arabic is reversed to its
  end (Latin after it included); Hebrew is reversed a stretch of Hebrew letters at a time. Found by probing kitty,
  undocumented: re-probe (lamed/final kaf, Latin markers) if kitty changes. Re-probed on kitty 0.32.2 (Oct 2026)
  against VTE, Navigator's viewer on `abc سلام xyz`, `abسلام xyz` (Arabic straight after Latin in one run), lam-alef,
  Hebrew with `ך`, `a1b שלום2 c`: all identical but niqqud, whose marks kitty places imperfectly.

## Checking it

`tests/test_bidi.py`. By eye: `nav --language he` / `--language ar` (or `--direction rtl`) in a VTE terminal, kitty
and ghostty, Konsole, mlterm, alacritty; xdotool + `import` can capture windows (Konsole and mlterm: find the window
by `--class`, Navigator retitles it) (kitty: capture after `windowactivate --sync`, or it comes out
black; find a window by its process, not its title, or the keys go to another Navigator). Reading Hebrew order off a
screenshot is unreliable; use letters with ascenders/descenders (ל, ך) or Latin next to Arabic.
`tools/screenshot.py --language he` paints a mirrored scene to `docs/screenshot-he.svg`;
`NAVIGATOR_PTY_TESTS=1 ./venv/bin/python -m pytest tests/test_pty_end_to_end.py` runs `--language he` on a real pty
(mirrored menu bar, `CSI 8 l`/`8 h`, quitting).

**Cost** (Oct 2026, 300x80, `bench` in the session's scratch): the mirror 1.4 ms a frame, kitty's pass 11.6 ms. A
screen of rows not seen before costs python-bidi's layout: the editor 57 ms (8 ms in Latin), the viewer 27 ms (14);
the same screen again is the Latin cost (10 ms, 15 ms), `layout`/`_ordered_cells` being cached.

## What is left

`reference/backlog.md` lists what is still to do for right-to-left text, by priority. Update it as items are done.
