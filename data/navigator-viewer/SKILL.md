---
name: navigator-viewer
description: The internal file viewer (F3, DN's FVIEWER.PAS) -- navigator/lib/viewer/__init__.py (ViewSource, pread chunks), FileViewer in FileWindow, text/hex/dump modes, wrap, filters, Shift+F6 encodings (DN's XLT) and Shift+F5 Save as, the dBase viewer (dbf.py, DBWindow, As DataBase) and SQLite in it (sqlite.py), CSV in it too (table.py, As Spreadsheet), bytes-regex search on a thread with SearchJob and SearchProgress, go to address, the View menu, Ctrl+Q QuickViewer, and pictures shown on kitty/sixel terminals (image.py). Use when changing the viewer or quick view.
---

# The file viewer

- **Hebrew and Arabic** in a text row are painted in reading order (`navkit.bidi.order_cells`), every cell keeping its
  offset for the hit and the tokens; a combining mark joins its letter's cell. `navkit-bidi` skill.
- **F3 is DN's internal viewer** (`FVIEWER.PAS`). `navigator/lib/viewer/__init__.py` is the model: `ViewSource` uses `pread` into
  cached chunks, **never `mmap`**, so a truncated log cannot `SIGBUS` Navigator. `FileViewer` inside `FileWindow` is
  `TFileViewer` inside `TFileWindow`; it opens zoomed on the desktop with the scroll bar on the frame and `TViewInfo` over
  the bottom edge.
- **What F3 opens is DN's `ViewFile`** (`Manager.view_file`). A directory (or `..`), F3 or Alt+F3, is Alt+G's
  `CountLen` (tagged ones too; nothing in an archive, DN's `dtArc`). F3 with *Internal viewer* on: a dBase, SQLite or
  CSV file its window (`_has_window_of_its_own`, `XT = '.DBF'`), an archive into the panel (`Panel.archive_on_f3`,
  `ArcViewer`: whatever *Enter opens an archive* says, never one inside an archive, and one that is no archive goes
  on), then `viewers.ini` (`DN.VWR`), then the viewer. Alt+F3 is `InternalView`: `view(plain=True)`, the viewer on
  the file, never the sheet, database or structured tree, nor `viewers.ini`. *Internal viewer* off: F3 is
  `viewers.ini`, then `$PAGER` (a departure: DN fell back to its own viewer).
- **Shift+F4 is DN's *Edit...*** (`cmXEditFile`, on every DN status line) in the F3 window, the sheet/database
  window and the data tree: `EditNamed` bubbles to `Shell.on_edit_named`, which hands it to the manager in front
  (`Manager.edit_named`; none open, nothing). The quick view binds no Shift+F4, so the panels' table has it. **The
  view switches are Shift+F3** (*Markup view*, the tree's and the sheet's way back to text), a departure: Shift+F3
  was DN's *Phone Book*, dropped. `RETIRED_DEFAULTS` moves an old `keybindings.ini`'s `shift+f4` lines over.
- **Positions are byte offsets and nothing counts lines**, so a gigabyte opens at once. Text is UTF-8; an undecodable byte
  or a control is its CP437 glyph.
- **A scroll bar on the bottom frame** (`FileWindow.hbar`), a departure, asked for: DN's viewer had the right
  frame's bar alone. It sits between the info line (and its `{Markdown}`/`{Tree}` mark) and the option strip, and is
  shown while a row on screen is wider than the view. Its value is `x_delta`, and its range is
  `FileViewer.row_span`, the widest row showing. Nothing measures the whole file, so this is End's `CM_END`
  measure, decoded only to `SPAN_LOOK` (4096) columns or two views past the scroll, so a minified line is not
  decoded whole on every move. It is 0, and the bar hidden, while wrapped, rendered, in hex or dump, or narrower than
  4 cells. *Filter lines*' rows are measured with their gutter. `on_hbar_scroll` sets `x_delta`.
  **The right bar likewise shows only while there is more than the view holds** (`FileViewer.overflows`, a
  departure, asked for: DN's `TViewScroll` was always there). In text that means the top is past the start or the
  last row on screen is not the file's last, since nothing counts lines. For the markup view and *Filter lines* it
  means more rows than the view; for hex and dump, more bytes than the rows show; a picture never overflows. The
  frame shows where the bar would be.
  Ctrl+Q's quick view has the same bar (`QuickViewer.hbar`) across its bottom frame. Like its right bar, after
  DN's `TFileViewer.SetState`, it is shown only while the keyboard is in the quick view.
- Keys: F4 cycles text/hex/dump, F2 wraps, F6 filters, F7/Shift+F7/Ctrl+F7 search (a bytes regex, on a thread), F5 goes
  to a hex address. Esc closes, and so does F3, uncaptioned (mc's key, a departure). File > View > As Text / As Hex open
  it in either mode.
- **`last_search`** is shared by every viewer (DN's `SearchString`); Alt+F7 with plain text sets it too (`filefind.hand_on`).
- **Search as DN's `ContinueSearch`** (`FVIEWER.PAS:1160-1195`): Shift+F7, Ctrl+L and Ctrl+Enter (`kbCtrlEnter`)
  continue, Ctrl+F7 the other way. A hit's row goes to the top (hex and dump: the row holding it, the byte phase
  kept; hex's cursor onto it), as far as the last screenful; under *Filter lines* the lines cursor goes to it. A
  continue goes on from the hit while it shows (`FileViewer.hit_showing`), else from the view: text's `top`, dump's
  `top`, hex's cursor (drawn, so kept over DN's view top). *Showing*, not DN's *on the first row*, is a departure: a
  hit in the last screenful cannot go to the top, and DN's rule would find it again on every Shift+F7. Not found is
  DN's `mfError` box, titled *Error*.
- **The *Find* box's *He~x~* line** (`StartSearch`'s `THexLine`, two rows under *Search for*; navml's `HexLine`): the
  text's bytes in the viewer's encoding (`ViewerFindDialog(encoding=)`), edited as hex. Bytes hex made that are no text
  in it go in `ViewSearch.data` (only when they differ from the text encoded) and are searched as they are in any
  viewer, an ASCII letter either case with *Case sensitive* off (`compile_search(data=)`); F7 reopens on them, the
  history keeps the text shown. The structured view and *Filter lines* search text and ignore `data`.
- **Dump has no cursor** (DN's `ViewMode = 2`, `FVIEWER.PAS:1425-1530`; `FileViewer._dump_key`): Up/Down/PgUp/PgDn
  scroll as in text, Ctrl+Home/Ctrl+End go to the file's start and last screenful (`Goto 1/2`), Ctrl+Left/Right shift
  the rows a byte as in hex (`_shift_rows`, shared). Home/End/Left/Right/Tab do nothing but are still the viewer's.
  `cursor` is kept on `top`, so F7 and *As Spreadsheet* start where the view does (DN's `FilePos+BufPos`); hex keeps
  its own cursor.
- **Hex editing** is DN's `HexEdit` (`FVIEWER.PAS`, `ViewMode = 1` only; never dump, text or the Ctrl+Q quick
  view, `FileViewer.hex_editing` set by `FileWindow`). In the pairs 0-9/A-F replace the cursor's nibble
  (`FileViewer.nibble`) and Left/Right/Home/End step nibbles; Tab moves to the characters (`in_chars`), where a
  character replaces the byte. That works only for a character in File > Encoding's code page, or ASCII under
  UTF-8. Each key moves on, as DN's `Message(kbRight)` did. **Shift+F2, View > *Store*** is `WriteModify` (DN's
  `cmSave`), greyed until something is typed. Closing (Esc, F3, Alt+X) with bytes typed asks DN's
  `dlViewQuery` *Information was modified. Save changes?*, through `must_ask`/`ask_to_close`.
  - **The bytes are an overlay** on `ViewSource` (`edits`, `originals`, `patch`/`revert`/`undo`/`stored`). They
    are laid over each chunk as it is read (`_patched`) and over one already cached as it is typed (`_show`),
    so everything reading through the cache shows them.
  - **A thread reading on its own does not see them.** Search gets a copy (`find(edits=)`); the lexer and the
    markup renderer read the disk until Store, which re-lexes. DN asked on every buffer `Seek`; with no buffer
    here it asks only on Store and close (a departure).
  - **`viewer.store_edits`** writes on a thread. A file on the disk is written in place, one `pwrite` per run of
    neighbouring bytes (`edit_runs`), so inode, owner and links are kept. A drive with `patch_file` (the root
    helper's, and `root:///`) is written in place too. Any other drive gets the whole file rewritten beside it
    with the bytes laid over (`_save_elsewhere(edits=)`). An archive member's copy goes back by `put_back`.
  - **A file no longer the size it was opened at** raises `FileChanged`, and nothing is written.
  - **A refusal on the disk offers *As root***, which writes through `RootDrive.patch_file`.
  - **Departures**, asked for: bytes typed and not stored are marked (`FileViewer::changed`, Compare files'
    `$diff-changed-*`), and the info line starts with `*`. Ctrl+Z takes back the last byte typed, and
    Backspace steps back and puts the file's own byte there; Store clears what can be undone. A click on a
    pair or a character puts the cursor there.
- **The mouse in F3 and Ctrl+Q is DN's quarters** (`FileViewer._quarter`). The outer quarters are Left and Right, and
  the middle is Up above half-way and Down below it. Held, they repeat on every tick and every move, with the quarter
  under the pointer then and nothing while it is off the view (`FVIEWER.PAS:1569`, `Application.hold_mouse`
  `moves=True`). The scroll bars repeat as every `ScrollBar` does.
- **Shift+F6, File > Encoding** is DN's `cmLoadXlatTable`: instead of an `XLT\*.XLT` table, a `PopupMenu` of one-byte
  code pages (`viewer.ENCODINGS`: *UTF-8* first and meaning none, then every one-byte page of
  `navigator/lib/codepages.py` -- DN's dozen and the rest, a departure, asked for -- in a submenu a group through
  `encoding_menu.fill`, the box opening on the group of the page in use). Multi-byte code pages are the editor's
  only: the viewer draws a file byte by byte. `FileViewer.set_encoding` puts `byte_table(codec)` on
  `ViewSource.table`, which `line()` (and so wrapping and scrolling), the hex and dump rows and `compile_search(...,
  encoding=)` all go through; the info line ends `{CP866}`. Controls stay the VGA's glyphs. Not kept in the view record.
- **Shift+F5, File > Save as** is `cmSaveAll`: DN's *Save File As* file dialog (history `edit_save`, the editor's), and
  `viewer.save_as` writes the file through a temporary beside it -- as it is, or read in the chosen code page and
  written in UTF-8, as DN wrote through its `Xlat`; `FileSaved` then re-reads the panels. DN's `SaveFile` questions:
  a code page in use asks *Save the file translated from CP866 to UTF-8?* first (`dlViewSaveXlat`): Yes recodes, No
  writes the bytes as they are, and Esc saves nothing (a departure: DN's Esc was No). A file already there is
  `dlED_OverQuery` with Yes / *Append* / Cancel; Append writes onto its end with no temporary. `limit` (the
  viewer's `size` when the save began, DN's `Sz`) stops a file appended to itself reading its own tail forever. The
  three write paths (disk, another drive, as root) share `_blocks`, one incremental decoder across the blocks.
- **Syntax highlight**, a departure (DN's viewer had none): the editor's highlighting (`navigator-editor` has the
  rules, `highlight.ini` and the `::token` part) in text mode only, `FileViewer::token` taking the editor's highlight
  foregrounds over the viewer's own background -- the quick view's too. `viewer.syntax_highlight` (on), View >
  *Syntax highlight* (the editor's `SwitchHighLight`, handled by `FileWindow`, ticked), `ViewRecord.highlight`.
  Nothing counts lines, so a thread reads and lexes a byte window, from the first whole line after `top - LEX_BACK`
  to `top + LEX_AHEAD` (256 KiB each way, `_lex_window`, its own `open` -- `ViewSource`'s chunk cache is not for
  threads). A file read across a network (`ChunkedSource`) is lexed too, a window of `REMOTE_LEX_BACK`/`AHEAD`
  (128 KiB, two chunks) each way, read on the thread through `ChunkedSource.read_blocking` (one read at a time
  with the fetchers, under the source's `_reader_lock`) and keyed on the origin's URL; cells carry byte offsets, so a row finds its spans by `bisect` and wrapped rows need nothing more.
  View > *File type* picks the lexer by hand (`SetFileType`, `FileViewer.file_type`, `ViewRecord.file_type`; the
  editor skill has the rules), text mode only. A file of 256 KiB or less is lexed whole and exactly; deeper into a bigger one, a comment or string opened more than
  `LEX_BACK` above is not known to be open -- the documented limit. The window is keyed on path, encoding, size and file type
  (Shift+F6 re-lexes) and never asked for twice, so a line longer than it cannot loop.
- **Markup view: Markdown, reStructuredText, HTML and PDF rendered**, a departure (DN's viewer had none): Shift+F3, View > *Markup view*
  (`SwitchRendered`, handled by `FileWindow` and by `QuickViewer`, ticked; the strip's last item,
  `MD`, `RST` or `HTML` (`M↓`, `rST`, `</>` as symbols), dropped first from a short frame) renders the file rather than showing its source, in text mode only.
  `FileViewer.rendered` is the switch; `format_by_name` says `html` (`[viewer] render_html` + `html_masks`), `rst`
  (`render_rst` + `rst_masks`) or `markdown` (`render_markdown` + `markdown_masks`) or "", which seeds it in `open()`; `render_format` is that, else
  `markdown` (a `.txt` switched on reads as Markdown). `{Markdown}`/`{reST}`/`{HTML}` follows the info line (`md_mark`,
  `render_mark`): plain while on, struck through (`Style.strike`, SGR 9) while off for a file the masks name, absent
  otherwise; a press on it switches (`FileWindow.on_mouse_click`). Styled by class (`StaticText.rendered`, `.off`
  struck), in the info line's (`name: "info"`) frame colours. No checkboxes (the Editor/Viewer page has no rows for
  them). Kept as `ViewRecord.rendered` (`on`/`off`, empty for the masks' say).
  **The model is five modules.** `navigator/lib/viewer/layout.py` is the format-free part: `Row`/`Layout`, `_wrap`,
  and `Builder`, whose block methods (`heading`, `paragraph`, `code`, `table`, `rule`, `quote`, `push`/`pop`) make
  the rows. `markdown.py` walks markdown-it-py's tokens into it (CommonMark plus GFM tables and strikethrough).
  `rst.py` walks docutils' document tree into it: sections as headings by depth (a
  title's `line` is its underline's, so one back), lists of every enumerator kind, admonitions as a quote under their
  name, definition and field lists indented, grid and simple tables, `code-block`s lexed here (`syntax_highlight:
  none`) -- docutils puts a directive's `line` after it, so `code_line` finds the first line's text near it.
  `include` and `raw` are off and every warning is quiet (`report_level`/`halt_level` 5): nothing outside the file is
  read, and a document with errors renders what it can. `html.py` walks the stdlib `html.parser` into it, as `lynx -dump` reads a page: `<title>` first,
  `head`/`script`/`style` hidden (`head` ends at the first body element, closed or not), blanks run together, lists
  with unclosed `<li>`, `pre` coloured by its `language-*` class, tables gathered then drawn, `a href` as links, `img`
  as `[alt]`; an end tag closes its own element wherever it is open, so broken HTML degrades. `pdf.py` reads a PDF
  with pypdf (`[viewer] render_pdf` + `pdf_masks`, `{PDF}`): each page a `Page N of M` heading, its `extract_text()`
  in paragraphs (lines joined between blank lines, reflowed), a rule between pages; pictures are not shown, a
  password other than the empty one raises (source shown). Its rows' `src` are **synthetic** -- each page an even
  share of the file, its paragraphs spread across it -- since the text sits in compressed streams; so F7, which
  searches the source bytes, does not find rendered PDF text. Its limit is `PDF_LIMIT` (64 MiB), not
  `RENDER_LIMIT`. Every reader reads the
  **whole** file, so one over `RENDER_LIMIT` (4 MiB) stays source. The layout is made on a thread (`_RENDERER`,
  `_lay_out` dispatching through `RENDERERS`, reading across a network through `read_blocking`), keyed on where,
  encoding, size, width, glyph tier and format, never asked for twice; until one lands the source (first time) or the
  last layout is painted. **Rendered rows are not byte ranges**: each carries `src`, the offset of its block's source
  line (a code or table row, its own line; in HTML, the line of the tag the block began at), and `block`.
  `render_row` is the row on top and `top` follows it at that row's `src`, so the scroll bar, the view history and
  switching back (`toggle_rendered`, `seek(top)`) keep their place by block. Paragraphs reflow to the width, so Wrap
  and ¶ are greyed while it renders and nothing scrolls sideways. A search still runs over the source bytes;
  `show_hit` goes to the block holding the hit, and `_render_marks` marks the hit's text found again (blanks run
  together, case aside) among that block's rows -- unmarked if the markup split it. Cells are classes on
  `FileViewer::md` (`heading h1..h6`, `strong`, `emph`, `strike`, `code`, `code block`, `link` with an OSC 8 URL,
  `image`, `bullet`, `quote`, `rule`, `table`, `th`, `html`), styled in `navigator.nss` from existing theme
  variables only so every theme has them; a code block's tokens are `token` classes, the highlight's foreground
  over `md.code`.
- **The option strip and Hidden characters** -- see `navigator-editor`, which has both; the viewer's strip is
  `option_items.viewer_items`: the mode (`HexMode`, cycles), Wrap (`Unwrap`), Hi, ¶ (`SwitchHiddenChars`, handled
  and ticked by `FileWindow`), the encoding (`ChooseEncoding`), the file type and MD/HTML (`SwitchRendered`); Wrap, Hi, ¶ and the type are text
  mode only, greyed in hex/dump. *Hidden characters* (View > *Sh~o~w hidden characters*, the editor's caption, its `o` the one letter free; Ctrl+Shift+8) marks text mode only:
  `FileViewer._hidden_row` reads each row's shown bytes and its last two (the ending) at paint time; the decoders
  are untouched, and the filter's `·` is told from a blank's by being faint. `[viewer] show_options`/`show_hidden`.
- **While a viewer window is active the bar has a *View* menu after *File*** (modes, filters and wrap ticked, search, go
  to, close) -- see `navml-windows-menus` for how a window's menu joins the bar.
- A search still running after two ticks shows DN's *Search Progress* box (`TWhileView`: gauge, percentage, Stop), fed
  through a `SearchJob` the thread writes and the loop reads. It uses the library's `ProgressBar`. It runs through
  `navigator.lib.system.progress.run_with_progress`, which **stops the job whenever the task ends with the work unfinished** --
  a viewer closed or Navigator quitting mid-search used to leave the thread reading to EOF, and `asyncio.run` waited.
- **Opening is on a thread too**: `open_viewer` is async, building the `ViewSource` (stat, open, `/proc`'s
  read-whole) through `run_with_progress` and handing it to `FileWindow(source=...)`/`FileViewer.open(source=...)`;
  *Reading file* after `SLOW_PROGRESS_DELAY`, Cancel opens nothing. The quick view opens its file through
  `navml.background.Background` and shows only what the cursor is still on when it lands.
- **Ctrl+Q is DN's quick view** (`QuickViewer`, a framed `FileViewer`), standing in the passive panel's place through
  `Manager.switch_view`; it follows the active panel's cursor, and Tab moves the keyboard in and out. Its right-click
  menu is its own (`QuickViewer.context_menu`, set over the viewer's; a departure, asked for): *~V~iew* (the panel's
  F3, on the same file), *~M~arkup view*, *~C~lose quick view* (Ctrl+Q) -- the F3 window's greyed nearly all of itself
  here, and its *Close* closed the file manager. `context_focus` is off, so the keyboard stays with the panel: closing
  the view while it holds the keyboard gives it to the panel put back (DN's `SwitchView`), and the next Ctrl+Q then
  stands on the other side.
- **With the keyboard in it, the quick view's keys are the viewer's**, `StatusDef hcView`'s, since DN's was a
  `THFileViewer`:
  - **Bound:** F2 wrap, F4 hex/dump, F5 go to, F6 filter, F7, Ctrl+F7, Shift+F7, Ctrl+L and Ctrl+Enter search,
    Shift+F5 *Save as* and Shift+F6 *Encoding* (`quick_viewer.nml`).
  - **Shared code:** both hosts handle them through `navigator/widgets/viewer/viewer_host.py`: functions taking the
    host (`goto_address`, `choose_encoding`, `save_as`, `search_for`, `search_again`, `find`, `checks`, `refusal`,
    `COMMANDS`). Their thin `on_*` handlers are written out in `FileWindow` and `QuickViewer`, because a
    component's hand-written half has one base and cannot take a mixin.
  - **Refused** (`QuickViewer.refusal`): any of them with nothing shown (*Nothing is open*), and *Save as* of a file
    from another drive, of which only the head was fetched (*Only the start of the file was read*).
  - **Not bound:** Shift+F2 *Store*, since the quick view never types a byte, and Ctrl+F4, which would close the file
    manager.
  - **A departure:** a key hcView didn't list (F3, F8, the panels' Alt/Ctrl keys) did nothing in DN's quick view.
    Here it still reaches the panels, and the key bar shows it.
  - **While the panel has the keyboard**, every key is the panel's.
- **Alt+Z with the keyboard in the quick view** hides the panel it follows and zooms, so the view fills the screen.
  Alt+Z again puts both back (`navigator-panels`, `Manager.on_zoom_window`).
- **Each Ctrl+Q opens the view as Viewer setup says** (`QuickViewer.fresh`, called from `Manager.switch_view`):
  - DN's `ViewInsert` made a new `THFileViewer` with `ViOpt` each time, and `SwitchView` freed it.
  - The view opens in hex if *Hex mode* is set and wrapped if *Wrap lines* is, with filter 0 and UTF-8.
  - Moving the cursor keeps the mode the user chose, as `cmLoadViewFile` kept `ViewMode`. Markup view is each file's,
    as it opens.
- **File View History (Alt+PgDn)**: DN's `TViewRecord`. Each file's window rectangle (scaled to the desktop, as
  `AdjustToDesktopSize` did), mode, wrap, filter, `top`, `x_delta` and hex `cursor` are written to the `ViewRecord`
  model. That happens when a viewer opens on a file with no record, and when it closes by any route, Alt+X included
  (`Navigator.on_stop`). The record is restored by `FileWindow.recall_history()` once the window is on its desktop.
  **Open viewers through `navigator.lib.config.file_history.open_viewer`**, never `desktop.open(FileWindow(...))`, or nothing is
  restored. As Text / As Hex pass a mode, which wins over the record's. Gated on Interface's *Track viewing history*; the rectangle, `top`, `x_delta` and `cursor` come
  back only under *Store viewer position* as well.
  The dialog and the list are `FileHistoryDialog`/`FileRecordList` (`shell/`). The key bar names the list's own keys,
  *Space Pin*, *Shift+↑↓ Move*, *←→ Pinned* (`FileHistoryDialog.key_hints`; a departure, asked for). The Ctrl+Q quick viewer records nothing.
- **The dBase viewer** (File > View > As DataBase, `ViewAsDataBase`; F3 on a `.dbf`, DN's `ViewFile` `XT = '.DBF'`):
  `navigator/lib/viewer/dbf.py` is `TDBFile` -- header, fields, records by `pread` through a cache, memos from
  `memo_files` (DN's names: a four-letter extension other than `.dbf` with its last letter `T`, so `.scx`→`.sct`,
  else `.fpt`, then `.dbt`; the table's own case first) as bytes (`memo_data`; `memo` decodes them),
  text in the table's own code page (`DBFile.codec`, `code_page_of`: a `.cpg` beside it -- a shapefile's, a
  departure; `cpg_codec` reads `UTF-8`, `1251`, `ANSI 1251` -- else the language-driver byte at offset 29 through
  `LANGUAGE_DRIVERS`, one-byte pages only, else CP437, DN's English screen; DN drew the screen's page). Shift+F6
  (`TableFormat`, the CSV's *Format*; captioned *Encoding...* by the `code_page` property) opens the text viewer's
  box (`viewer_host.pick_encoding`) and `set_codec` reads the cells and field names (`Field.raw_name`) again; F4
  writes in that page, never cutting a character; SQLite refuses it. A copy fetched from another drive or as root
  brings `dbf.companions` (memo files, `.cpg`) along. A file whose fields do not add up is refused (`DBFError`; F3 then falls back to the text viewer, As
  DataBase says so). `DBWindow`/`DBViewer` (`viewer/db_window/`) are `TDBWindow`/`TDBViewer`: field names over the
  records, the delete flag first, a cell the cursor (`Delta`), whole fields scrolled across (`Pos`), dates
  `DD-MM-YYYY` as the panels', a memo column `max(name, Len)` wide, `record/records` over the bottom frame (both plain,
  `ItoS`; in the passive frame colour while another window is active, `GetColor(1 + Byte(sfActive))`);
  Enter/arrows/Home/End/PgUp/PgDn/Ctrl+PgUp/PgDn, mouse quadrants (held, they repeat, `DBVIEW.PAS`'s
  `evMouseAuto` loop). F2 *Structure of*
  (`DBListDialog`), F3 *Memo view* (`MemoDialog`, DN's 69×19 `ViewMemo` box: a `FileViewer` on a `MemorySource`
  of the memo's bytes, a scroll bar, and OK). It reads the bytes on a thread, in the table's code page (UTF-8 for a
  SQLite or CSV cell). It is wrapped as *Wrap lines* says, and the viewer's keys work (F2/F4-F7 and the searches
  again, Shift+F6) through `viewer_host`, with no Save as and no Store. F4 edits the cell in place (`EditLineDialog`, history `edit_dbf`, its line held to the field's
  length and a date's 10 as `InputBox`'s `Limit`; L flips T/F; refused write-protected). A value that will not go in
  says *Not a number*, *The number does not fit the field* or *Not a date* and leaves the cell (a departure: DN's
  `Val` stored 0, losing the cell). F7 *Search* (`DBSearchDialog`, `dlgDbFind`; DN looked
  at one field a record by a slip, every one in scope is looked at here), Shift+F7/Ctrl+L again. A file with no
  records shows *Empty database* and opens nothing; a SQLite table or query or a CSV with no rows opens on its field
  names reading `0/0` (a departure: an empty answer is an answer), F3 and F4 doing nothing there. Colours are the dBase group [166]-[171]. Kept with the desktop, SQLite and CSV too (`navigator-desktop`).
  Its own *View* menu joins the bar after *File* while it is active (a departure, asked for: DN's had the key bar
  alone), twelve items, what does not apply to the source greyed through `DBWindow.refusal`, never removed:
  *Fields...* F2, *Memo view* F3 (greyed off a memo field), *Edit field...* F4 (greyed on SQLite and CSV, read-only),
  *Tables...* F5 and *Query...* F6 (SQLite alone); a line; *Sort by column* F8, *Column width...*, Shift+F6 --
  *Format...* on a CSV, *Encoding...* on a dBase table (the `code_page` property), greyed on SQLite -- and *As text*
  Shift+F3 (CSV alone); a line; *Search...* F7, *Search again* Shift+F7; a line; *Close*. The grid's right-click
  menu (`DBViewer.context_menu`) has seven of them: *Fields*, *Memo view*, *Edit field*, *Sort by column*, *Search*,
  *Search again*, *Close* -- the cell's own and every source's; the SQLite and CSV ones and *Column width* are the
  bar's alone. A right click on a cell first makes it the cursor's (`cell_at`, `prepare_context`).
- **SQLite in the dBase window**, a departure (DN read dBase alone). It opens with F3 on a name in
  `[viewer] database_masks` (`*.sqlite;*.sqlite3;*.db;*.db3`) whose file starts with SQLite's header
  (`is_sqlite`; any other `.db` stays text), or with *As DataBase*, which tells the format by that header
  (`open_database` → `open_sqlite`). A file that is neither raises `DBFError`, so F3 falls back to text and
  *As DataBase* says *not a dBase or SQLite file*.
  - **The model** is `navigator/lib/viewer/sqlite.py`, **read-only always**: `mode=ro` (else `immutable=1`)
    plus `PRAGMA query_only`.
  - **`SQLiteFile`** holds one connection under an `RLock`. It answers `objects` (tables, then views;
    `sqlite_%` left out), `columns` (`table_xinfo`, affinity → `N`/`F`/`C`/`B`), `table`, `query` and
    `schema`.
  - **`SQLTable`** answers what the window asks of a `DBFile`: `fields`, `count`, `record`, `shown`,
    `raw`, `memo`, `flag`, `memo_kinds`, `editable`, `path`, `close`. `DBViewer` paints `db.flag(record)`,
    and `DBWindow` reads `memo_kinds`/`editable`, so the dBase code stays as it was.
  - **Reading an ordinary table**: its rowids are listed on a thread, and a `BLOCK` of rows is fetched by
    `WHERE rowid >= ?`, an indexed seek done on the loop as the dBase `pread` is. A view, a `WITHOUT ROWID`
    table or a query is read whole on the thread, up to `ROW_LIMIT` (`truncated`, shown as `+` after the
    count).
  - **Cells**: NULL is blank, a blob is `‹blob N bytes›` (Memo view shows it as hex rows), and line breaks
    show as blanks.
  - **Keys**: F4 is refused (*The database is opened read-only*). **F5 *Tables*** (`ChooseTable`,
    `choose_object`, a `PopupMenu`) also opens first when a file has more than one table; none gives
    *Empty database*. **F6 *Query*** (`RunQuery`, `QueryDialog`, history `sql_query`) runs one statement
    under an authorizer allowing SELECT/READ/FUNCTION/RECURSIVE only. INSERT, ATTACH, a write `PRAGMA` and a
    second statement are refused, and SQLite's message shows in *Error*. **F2** (`DBWindow.show_schema`)
    lists the columns with declared type and `PK`/`NOT NULL`, then the rows, the indexes and the `CREATE`.
    **F7** runs `dbf.find` (any source with `raw`) on a thread with a stop flag, for dBase too.
  - **The title** is the place and the table (or *Query*). `DBWindow.place` is the original's path for a
    copy. The window list says *SQLite View -*.
  - **A copy fetched** from another drive or as root brings its `-wal` too (`database_elsewhere`,
    `fetch_database`), and a read-only connection reads it.
- **CSV and TSV in the dBase window**, a departure (asked for: one style for the three table viewers). F3 on a
  name in `[viewer] table_masks` (`*.csv;*.tsv;*.tab`, `render_tables` on) or File > View > *As
  Spreadsheet* (`ViewAsSpreadsheet`, any file) opens `DBWindow` through `db_window.open_csv`, read-only.
  DN's F3 on a `.WKZ` opened a spreadsheet window of its own (`TCalcWindow`, CALC.PAS); that look was built
  first and then dropped (`reference/spreadsheet.md`).
  - **The model** is `navigator/lib/viewer/table.py`. `guess` picks the dialect: the delimiter by
    `csv.Sniffer` among `, ; tab |` (tab for `.tsv`/`.tab`), the header by `has_header`, a BOM as
    `utf-8-sig`, and non-UTF-8 as `cp1252`.
  - **`TableSource`** walks the file once on its own thread (`start`): a regex over quotes and line
    endings notes each record's start, so a quoted field may hold delimiters and line breaks. A record is
    `pread` and parsed by `csv` when shown, with an LRU.
  - **`CSVTable`** is the source the window reads (`fields` named by the header or `A`, `B`..; kind `N`
    when every sampled value is a number, right-aligned). Its `count` grows until `complete`, which
    `DBWindow` follows with a `call_every` tick (`row/rows+ 42%`).
  - **For any source** (dBase, SQLite, CSV):
    - **F8 sorts** the rows shown: `table.sort_order` on a thread, `SortedView` reading through the order,
      even for a dBase F4 write. It cycles ascending, descending, then the file's order, and the
      indicator shows `name↑`.
    - ***Column width*** is DN spreadsheet's `cmChangeWidth` mode (`DBViewer.resizing`), and
      Ctrl+Left/Right resize directly (`DBViewer.widths`, `width_of`).
  - **CSV only**:
    - F2 lists the columns, then the delimiter, header, encoding and rows (`show_columns`).
    - F3 shows a cell whole and F4 is refused.
    - **Shift+F6 *Format*** (`TableFormatDialog`) reads the file again.
    - **Shift+F3** goes to F3's text view at the record's offset; Shift+F3 there (`FileWindow.as_table`)
      comes back to the row the top is in, in the same place (`db_window.take_place`).
  - **A file on another drive** is fetched by `Manager._view_sheet` (`materialize`, `use_set`, `place`). A
    file that cannot be opened so falls through to the text viewer.
- **Pictures, shown as pictures**, a departure (DN's viewer had none; asked for): on a terminal that draws them
  (`TerminalInfo.graphics`, kitty's graphics protocol or sixel -- `navkit-terminal`), a file `[viewer] image_masks`
  names (`render_images`) is *Markup view*'s fifth format, `image` (`{Image}`, `Img` on the strip). Shift+F3 gives the
  source, hex and dump work as ever; a terminal that draws nothing, tmux/screen, or `--graphics none` shows the bytes
  as before (`can_render` false). `navigator/lib/viewer/image.py`'s `decode` runs on `_RENDERER` (`_picture`, the
  whole file through `read_blocking` when remote, `IMAGE_LIMIT` 64 MiB) and makes a `navkit.graphics.Picture` fitted to
  the viewer less a caption row (`fit`: aspect kept by `cell_px`, else 2:1, never enlarged), keyed on where, size,
  cols, rows, protocol and `cell_px`; `picture` holds it (`image.Shown`, with format and pixel size), `showing_picture`
  paints it centred with `place_image` and `PNG 1280×320` under it, `picture_pending` says *Reading...*, a failure
  shows the source. **Pillow is optional** (`navigator-fm[images]`, compiled): without it only a PNG on kitty is shown
  (sent as it is; a PNG over `KITTY_AS_IS` is re-encoded smaller when Pillow is there), everything else is the source.
  Sixel is quantised to 255 colours plus a transparent one and encoded by `navkit.graphics.sixel_encode`. An animation
  shows its first frame. **A picture anything paints over is hidden whole** (a menu, a dialog, a window -- the
  `navkit-widgets-input` skill's *Pictures*), and one under a dimmed modal stays bright. Ctrl+Q's quick view has it
  through its `FileViewer`; a new file's picture has a new id, so the last one is freed.
- Commands: `navigator/widgets/viewer/commands.py`.

- **Every bound key is on the View menu** (a departure, asked for): F4 and F6, which cycle, are *He~x~/Text/Dump*
  (`HexMode`) and *Fi~l~ter* (`AddFilter`) above the entries that pick one mode or filter, on the context menu too.
  Only Ctrl+L (`SearchAgain`, *Search again*'s second key) and F3 (`CloseViewer`) stay uncaptioned, as DN and MC had them.

- **Follow end (Ctrl+T, View > *Follow e~n~d*)**, a departure, asked for (`tail -f`): `FileViewer.follow`,
  `{Follow}` on the info line. `FileWindow._follow_tick` runs every `FOLLOW_TICK` (0.5 s): `ViewSource.refresh()`
  `fstat`s the open fd (one syscall, so on the loop), and a `ChunkedSource` takes the size its drive gives on a
  thread (`stat_size`). It answers grew, shrank or same, drops the chunk cached short (all of them on a shrink),
  and `viewer.resized` shows the end. **Any move back up lets go**, as `less`'s F does; Ctrl+T again resumes.
  Refused (`follow_refusal`) for a fetched copy (`use_set`), unstored hex bytes, a rendered view and a `/proc` file.
  Never kept in the view record.
- **Filter lines (Ctrl+G, View > *Fil~t~er lines...*)**, a departure, asked for (`grep`); it is named so it is not
  taken for F6's character filters. `FilterLinesDialog` takes the text plus *Regular expression*, *Case sensitive*
  and *Invert*; a bad regex is refused in the box, and an empty line with OK takes the filter off. `lines.LineScan`
  counts and matches lines on a thread through `run_with_progress` and *Search Progress*, up to `HIT_LIMIT`, and
  continues from `scanned_to`, which is how a followed log stays filtered. `FileViewer.lines` with `filtering`
  paints the number gutter and the text itself (`_paint_lines`, `::lines.number/cursor/match`). Enter goes to the
  line in the whole file and Esc goes back. Text mode only; Wrap, ¶ and Markup view are greyed while it filters.
- **The structured view (Shift+F3 on `[viewer] structured_masks`)**, a departure, asked for: `StructWindow` with
  `DataTree(TreeView)` in the viewer's place (`FileWindow.as_tree`/`shows_tree`, `{Tree}` struck after the info
  line, a click on it opens the tree). The model is `navigator/lib/viewer/structured.py`: lazy `Node`s over
  `json` (order and repeated keys kept), `tomllib`, `xml.etree`, `plistlib`, and PyYAML's **composer** (no
  constructor runs; tags are shown, never acted on; marks give YAML nodes an offset). Rows are `key: value` (a long value **wraps**: `ValueRow`s after its row, hung under the
  value or under the key when that is narrow, rails carried down, `WRAP_ROWS` at most; the cursor passes over
  them, `DataTree.move_cursor`, and lands back on the node's row from a click), coloured by kind (`DataTree::string/number/bool/null/date/tagged/count`), with the cursor's path on the last row
  (jq-style, or XPath-style for XML). Ctrl+Ins copies the path, Ctrl+Shift+C the value (a branch as JSON, YAML or the
  element), F7/Shift+F7/Ctrl+L search every key and value on a thread (`structured.find`), `*` and *Expand all* open
  up to `EXPAND_LIMIT` nodes, Shift+F3 goes back to the text (at a YAML node's line), and Esc closes. A parse error
  says *Line N, column M* and puts the text at that line. Local files and fetched copies only; `STRUCT_LIMIT`
  32 MiB. `[viewer] render_structured` (off, no checkbox) makes F3 open the tree. **View > *D~a~ta tree*** (`ViewAsTree`, no key) opens it for any file on the disk, read as
  `structured.kind_for` says: the masks, else the extension, else the first bytes. That includes **HTML**, whose
  Shift+F3 stays the Markup view: `_read_html` builds `ElementTree` elements through `html.parser` the way a
  browser forgives a page. Unclosed `li`/`p`/`td`/`tr`/`dt`/`dd`/`option` are closed by the next one (`_CLOSED_BY`, and
  a block closes a `p`), empty elements (`_VOID`) hold nothing, and a stray end tag is ignored. The XML tree shows
  the result, with text after a child (a tail) as `#text` in its place. Its own *Data* menu joins the
  bar, and `[struct_window]` is its key table.

## Tooltips

- In hex and dump, `FileViewer.tooltip_at` names the byte under the pointer (`byte_at`): offset, hex, decimal,
  octal, binary, the character in the current table -- read with `ViewSource.peek`, which answers from the chunk
  cache only and never reads on the loop (`None` on a miss; a byte on screen was just read).
- The info line's tooltip is the whole path and exact size (`info_tooltip`).
- A greyed View command says why (`FileWindow.refusal`).

## Read when

| Reference | Read when |
|---|---|
| `reference/file-viewer.md` | the full design and what is deferred |
| `reference/sqlite.md` | SQLite in the dBase window: why read-only, the rowid paging, the query's authorizer |
| `reference/spreadsheet.md` | why a CSV opens in the dBase window and not DN's spreadsheet look |
| `reference/follow-lines-tree.md` | Follow end, Filter lines and the structured view: why polling, what a new size invalidates, why the composer, laziness and aliases |
