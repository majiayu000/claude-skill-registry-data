---
name: navigator-editor
description: The internal editor (F4, DN's MICROED.PAS) -- navigator/lib/editor/ (Document, columns, EditBuffer with undo, save), FileEditor and EditWindow, byte-for-byte round-tripping, editor commands named after DN's cm*, closing with must_ask, the Editor menu, and syntax highlighting (navigator/lib/highlight/__init__.py, Pygments, highlight.ini, the ::token part) for the editor and the viewer. Use when changing the editor or highlighting.
---

# The editor

- **Hebrew and Arabic** in a line are painted in reading order (`navkit.bidi.order_cells`); the cursor, block and
  match stay in the line's own columns, mapped by `_visual_column`/`_logical_column`; Left/Right on such a line move
  by painted cell (`_step_visually`) and Ctrl+Left/Right by painted word start (`_word_visually`), and a marked block is what is painted between its ends
  (`_block_runs`), a column block's columns painted columns (`_rect_spans`) -- every block command must use those,
  never `columns.span` or `document.text(*self.block)` directly; departures. `navkit-bidi` skill.
- **F4 is DN's internal editor** (`MICROED.PAS`), all of it, with the departures listed below; what is still not
  there is the reference's last list (*What is still not DN's, or not there*).
  `navigator/lib/editor/` is the model (`Document`, `columns`, `EditBuffer` with undo, `save`); `FileEditor` is `TFileEditor`
  and `EditWindow` is `TEditWindow`, zoomed on the desktop with `TInfoLine` over the bottom frame.
- **A file round-trips byte for byte** -- tabs, each line's own terminator, non-UTF-8 bytes (`surrogateescape`) -- a
  departure from DN's rewriting. Saving renames a new file over the old one.
- **Encodings and line endings** (a departure, asked for: DN's editor knew the screen's code page and `CR+LF`).
  `navigator/lib/editor/encodings.py` is the table (`CODECS`: `UNICODE` -- `utf-8`, `utf-8-bom`, `utf-16-le`/`-be`,
  `utf-32-le`/`-be`, all but the first with a mark -- then every code page of `navigator/lib/codepages.py`, one-byte
  and CJK; `LEGACY` the latter's keys), `sniff` (UTF-32's marks before UTF-16's), `bom`, `decode`/`encode` (surrogateescape for the
  ASCII-compatible ones, so every byte still round-trips; UTF-16 strict) and `first_unencodable`. `Document.encoding`
  is the text's; `LineReader(encoding, fallback)` sniffs the mark from the first bytes and takes it off, decodes
  UTF-16 through an incremental decoder and cuts it as text, and a UTF-16 mark that does not decode is read again as
  UTF-8 (`read_document`, `from_bytes`). `[editor] fallback_encoding` (Editor setup's *Fallback encoding*, default
  `utf-8` = keep the bytes): a sniffed UTF-8 text with a byte that did not decode is re-read in that code page
  (`LineReader.escaped`, `Document.reinterpreted`). Saving writes the mark and the codec (`encode_lines(...,
  encoding=)`); `EditWindow._write` checks `first_unencodable` on a thread first and refuses with an `OSError`
  naming the character and line (`unencodable`), nothing written; ^K W writes the document's encoding, a new file
  with its mark. `Document.counts` tallies the terminators, kept by `insert`/`delete`; `line_ending` is `LF`, `CRLF`,
  `CR`, `Mixed`, or `newline`'s name with none. **A whole-text change is one swap**: `EditBuffer.swap(State, cursor)`
  records `Change("swap", before=, after=)`, undo/redo put one back, listeners hear `"endings"` (lines unchanged:
  nothing moves) or `"replace"` (`FileEditor` unmarks, clamps the cursor, rehighlights). Its uses are `SetLineEnding`
  (every ending made one, and `newline`), `SaveWithEncoding` (only `encoding`, refused with a box and the cursor on
  the first character it cannot write) and `ReopenWithEncoding` (`Document.reinterpreted` on a thread: the text's
  own bytes, mark aside, read as the other; the file is not touched, so an unchanged text stays unchanged --
  `mark_saved` after). All three are ticked through `FileEditor.checks`.
  **The markers**: `FormatMarks#marks` (`StaticText`, `name: "info"`, beside `InfoLine` in `file_editor.py`) a cell
  after the info line shows `FileEditor.format_text`, `[LF]═[UTF-8]` (bracketed as the option strip's items, a frame
  cell between); `ending_indicator()`/`encoding_indicator()` are
  its two zones, brackets included. A left press on the ending makes it the next of LF, CRLF, CR
  (`next_line_ending`: a *Mixed* text first becomes its most common, `newline`) through `SetLineEnding`, one undo
  step a click; a right press, or either on the encoding, emits `ChooseLineEnding`/`ChooseEncoding` (keyless, on
  `EditWindow.keyless_commands`), which `EditWindow._choose_format` answers with a `PopupMenu` whose bottom-left is
  at the marker (`format_menu.choose_line_ending`, opening on the text's ending; `choose_encoding`, two nested boxes
  *Reopen with* / *Save with*). **`behind` is the editor**, not the window: the editor answers the commands, so a box
  behind the window greys them all. `hbar` starts at `max(24, marks end + 1)` and the option strip's `room` is
  measured from the markers' end. Editor > File has *Line en~d~ings* and *En~c~oding* submenus, filled by
  `format_menu.fill_line_endings`/`fill_encodings` (letters chosen so no catalogue clashes).
- **The code pages** are `navigator/lib/codepages.py`'s `CODEPAGES` (`CodePage(key, label, caption, group,
  one_byte)`, grouped by `GROUPS`), shared by the editor, Convert text and the viewer (which takes `ONE_BYTE` only:
  it draws byte by byte). One is let in only if `tests/test_editor_encodings.py` holds: ASCII bytes are ASCII, no
  character encodes to a CR or LF byte (the reader cuts at breaks before decoding -- so no ISO-2022, HZ, UTF-7 or
  EBCDIC), and any bytes round-trip through surrogateescape (so no CP932, CP950, Big5-HKSCS, Johab, CP864,
  Shift_JIS-2004). A failing one is left out, never special-cased. Menus are `navigator/widgets/encoding_menu.fill`:
  the top entries, a line, a submenu a group, every box under 24 rows (tested); `Filled.places` gives the viewer's
  Shift+F6 the submenu to open on.
- **Reading and writing run on a thread, behind DN's `WriteMsg`** (`ReadBlock`, `SaveFile`). `read_document`
  (`navigator/lib/editor/document.py`) reads 4 MiB chunks through `LineReader`, which splits exactly as `from_bytes` does
  however the bytes are cut (a CR ending a chunk waits for the next -- DN's `ReadBlock` stepped back for it), in a few
  C calls per chunk so the loop keeps painting. `navigator/widgets/editor/loading.py` runs it through
  `navigator.lib.system.progress.run_with_progress`: `open_editor` is **async** and returns None when cancelled; F3 (`load_text`),
  ^K R and SmartPad go the same way. Saving snapshots the lists (`FileEditor.snapshot`), writes them as chunks on a
  thread (`encode_lines`, `write_file(path, chunks, job)`) under one `EditWindow._saving` lock, and marks the
  snapshot's save point (`EditBuffer.save_point`/`mark_saved(point)`) -- what is typed meanwhile leaves the text
  changed. **A file marked read-only** -- its owner's write bit clear (`save.marked_read_only`, DOS's attribute
  read on POSIX) -- asks `dlED_ModifyRO` first, *Confirm* / *Modify it anyway?* OK/Cancel, as `SaveFile` did
  (`EditWindow._modify_read_only`, shared by F2, Ctrl+F2, the close query's Yes, Save as and ^K W): OK lifts the
  bit and the mode is put back after; Cancel leaves the text unsaved and a closing window open. Somebody else's
  `0644` file is not asked about: its write is refused and offers *As root*. A copy from another drive is not asked
  about (its mode is not the original's). **Too large is refused** with DN's `erNotEnoughMemory` (`navigator/lib/system/memory.py`; no line cap -- DN's
  `LCount > 25000`, `MICROED.PAS:3480`, a limit of its 64 KB collections, is a departure dropped): against 75% of
  `MemAvailable` before reading, then after every chunk projected from the lines so far (DN's
  `4*(LCount+50)+FFSize`). Departures: the box (`WriteWin`, `file_ops/write_win`) waits `SLOW_PROGRESS_DELAY` (1 s)
  before it appears, has a spinner, a gauge with a percentage and *Cancel* (DN's was a still message read past by Esc);
  a cancelled save removes its temporary and leaves the file as it was, except a write in place (hard links), which
  cannot stop half way and hides *Cancel* (`job.cancellable`).
- **The cursor stays within the line's text** (a departure, asked for; DN's stood anywhere): movements go through
  `_move_to`, which clamps the column unless `_free` (line drawing, or extending a column block -- Shift+movement, Shift+click, a
  drag, flagged by `_extending`; a plain click or move clamps in column mode too, *Vertical blocks* being per file).
  A column block's corner takes `_goal` during Up/Down so Shift+Down across a short line keeps its width; Right/Left cross line ends;
  vertical moves keep a goal column (`_move_vertically`, `_goal`), Ctrl+PgUp/PgDn too: first and last line, the column kept, as DN's scroll bar set only `Min`/`Max` (`VIEWS.PAS:2350`). `_go_column` itself still places anywhere -- edits
  that leave the cursor on an indent rely on it.
- **Every key is a command named after DN's `cm*`** in `FileEditor.keys` (`navigator/widgets/editor/commands.py`).
  `Widget.edits_text` makes the command line's Enter/Home/End/Tab and pastes step aside.
- **Stream blocks and the clipboard.** Shift with any movement marks (`_marking` wraps the movement handlers; the
  block grows from the cursor, or from its other end when the cursor stood on one). `FileEditor.block` is
  `(start, end)` in `Pos`, start first, or None; it persists while the cursor moves under *Persistent blocks* (DN's
  default). Off, it goes (`_block_off`, DN's `BlockOff`) on a movement without Shift, typing, Enter, Backspace and Del.
  *Overwrite blocks* only counts with *Persistent blocks* off (DN's `(ebfPbl + ebfObl) = ebfObl`, both read live from
  the setup): then typing and pastes replace the block in one undo group (`_begin_typed`, `InputChar`'s and
  `PasteBlock`'s `DeleteBlock`), and Del deletes it alone (`_deleting_block`); Backspace never takes it, and Tab,
  ^Q D/T and ^K R leave it be. **A departure, asked for: with the cursor in the block** (`_cursor_in_block`, either
  end included, a column block's rectangle with the column past its right edge) typing and pastes replace it, Del
  and Backspace delete it alone, and Enter (inserting) replaces it with the break, one undo group each, whatever the
  two settings say (`_takes_block`). Outside it DN's rules above stand. Likewise Tab with the cursor in the block is
  ^K I by a tab stop (`on_tab_key`, `IndentBlock(stop=True)`), and Shift+Tab is bound to ^K U by up to a tab stop
  (`UnindentBlock(stop=True)`, `unindent_block_stop` in `keybindings.ini`, always enabled): with the cursor in the
  block it unindents the block, otherwise the cursor's line alone, the cursor moving left with its text; nothing indented, no edit at all
  (the typing run before it goes on, `_blank_at`) --
  departures too, and only Tab and Shift+Tab work at a column block's left edge (painted, `_painted_insert`); ^K I/U keep DN's one blank at column 0. Either way it follows every edit, undo's included, through
  `EditBuffer.listeners` and `document.shifted` -- text inserted at the block's end stays outside it. Painted with
  `FileEditor::selected`. Ctrl+Ins/Ctrl+C/Ctrl+Alt+C (`ClipboardCopy`, `cmCopy`), Shift+Del/Ctrl+X/Ctrl+Alt+X (`ClipboardCut`),
  Shift+Ins/Ctrl+V/Ctrl+Alt+V (`ClipboardPaste`, which asks the application and types the `PasteEvent` that comes back; the cursor ends after it with nothing marked -- a departure, asked for: DN's `InsertBlock` marked the paste, cursor at its start -- and it is greyed, *The clipboard is empty*, only with the system clipboard off and no copy made, since the desktop's cannot be looked at without a process: DN greyed `cmPaste` on an empty clipboard), Ctrl+Del (`Clear`,
  `cmClear`); also at the top of the Editor menu itself (DN's *Edit* submenu, flattened: a departure, asked for -- *Paragraph*, *Options* and *File type* gave up P, O and T for it). Copies hand out plain `\n` breaks, pastes take the file's own. Not `Cut`/`Copy`/`Paste`:
  F5's `Copy` and `on_paste` (the paste event) already own those handler names. **Departure:** Ctrl+X/C/V are the clipboard's, not WordStar's cursor down/PgDn/insert toggle as in DN (the user asked for
  the keys every other editor uses; ^X still draws down in drawing mode). Ctrl+Alt+X/C/V exist because VTE keeps Ctrl+Ins
  and Shift+Ins for itself.
  The ^K/^Q commands are named after their `cm*` in `DN.DNR`'s `EDITOR COMMANDS` table (`BlockStart`, `Clear`,
  `UpcaseBlock`, `MoveBlockStart`, `BlockRead`...); the clipboard four keep their own names (above). Every ^K/^Q
  command in the table is here -- ^K^[ ^K^] ^K^\ in their Ctrl forms (`_wordstar` gives `[ ] \` one, `^Q'['` alone
  excepted; the plain forms stay too, Ctrl+[ being Esc's byte without the kitty protocol, and `ctrl+k escape` is not
  bound) and ^K^Q `OpenMenu` -- but two, dropped: `cmMenu`'s double Alt (only a kitty-protocol terminal reports a
  bare Alt) and ^Q^O/^Q^I/^Q^P/^Q^C, the Windows clipboard's (the clipboard here is the system's). Alt+Shift+/
  (`alt+?`, `alt+shift+/`) is `CapString`, `kbAltSlash` with Shift.
- **The defaults are modern, WordStar is a preset (departure, asked for).** `FileEditor.keys` binds no WordStar key:
  not the Ctrl+E/S/D/A/F/R/W/Z diamond, not Ctrl+G/T, not the ^K/^Q/^B chords. The freed keys do what every editor
  since does: Ctrl+F the Find bar, Ctrl+R the Replace bar (F7/Ctrl+F7 keep DN's dialogs), Ctrl+G go to line, Ctrl+Z undo, Ctrl+Up/Down scroll, and Ctrl+S save
  (`EditWindow`'s, so the editor must not bind Ctrl+S). `WORDSTAR` (module level in `file_editor/helpers.py`) keeps DN's
  keys as they were, `keyless_commands = tuple(WORDSTAR.values())` keeps every command listed (and named as before)
  in Key bindings, and `navigator/assets/keymaps/keybindings_wordstar.ini` / `keybindings_dn151.ini` bind them back
  -- `test_the_wordstar_sets_bind_dn_s_table` holds the files to `WORDSTAR`. A test that presses a WordStar key
  takes conftest's `wordstar` fixture (`@pytest.mark.usefixtures("wordstar")`).
- **WordStar's ^K and ^Q** (with the preset) are navkit chords, each letter bound plain and with Ctrl (`_wordstar`): ^K B/K mark the
  start/end (with no block, the first waits for the other -- `_half_mark`, dropped by any edit), H (and Alt+H) hides the block or shows it again, C copies
  the block to the cursor and marks the copy, V moves it (refused with the cursor inside it), Y deletes it, I/U
  indent/unindent its lines by one blank at column 0, whatever the block's kind (`IndentBlock`/`UnIndentBlock`, `EDITOR.PAS:280-313`): I gives empty lines a blank too, U does nothing at all unless every line with text starts with a blank, a leading tab giving way to spaces; a column block's corners stay put. `[`
  `]` `\` upper/lower/capitalise it, widened to whole words (`ChangeBlockCase`, `_word_span`): a stream block keeps the widened extent, a column block its corners; a reordered Hebrew/Arabic line's lit runs are not widened, T marks the word (`cmMarkWord`, `_dn_word`: on a word's first character that word, else the start of this word or the one before it on the line -- a blank gives the word before it -- else the next word, on a later line too; the cursor at the word's start; a double-click is the same command where it was pressed), L the line; ^Q B/K go to its ends, ^Q Y deletes to the line's
  end, ^Q L undoes.
- **^K R / ^K W are DN's `BlockRead`/`BlockWrite`** (`MICROED.PAS`), also the Editor menu's *Paste from...*/*Copy
  to...*, handled by `EditWindow` (dialogs and I/O; `FileEditor.block_file_text`/`read_block` are the text). The name
  comes from navml's `FileDialog` (`GetFileNameDialog`: titles *Copy block to*/*Paste from File*, labels *File
  ~N~ame*/*~P~aste from*, the shared `hsEditPasteFrom` history `edit_paste_from`), listing the active panel's
  directory. Writing joins lines with the Editor setup's *Line divisor* and ends without one; a column block, or a
  one-line block, writes its columns unpadded. An existing file is `CheckForOver`'s Yes/A~p~pend/Cancel (`Dialog`
  `yes-no-cancel` with `no` relabelled), a read-only one asks *Modify it anyway?* and gets its mode back afterwards;
  the write emits `FileSaved` (`cmRereadDir`). Reading turns column blocks off (`VertBlock := Off`) and marks what it
  put in.
- **Sort, ^K S / Alt+T** (`SortBlock`, DN's `SortBlock` in `EDITOR.PAS`, also Block > Sort): the lines a *column*
  block spans, ordered by its columns' text as plain strings (case-sensitive, as Pascal's `<`); a stream block gets
  `dlED_VertNeed`, "Vertical blocks need for this operation", word for word. Each line keeps the ending of the place it
  lands in. Departures: stable (DN's quicksort was not) and one undo step (DN dropped its undo record).
- **Calculate sum, Alt+Ins** (`CalcBlock`, DN's `CalcBlock`, also Block > *Calculate sum*): the numbers in a column
  block's columns, each with its blanks removed (`DelSpaces`) and read as `Val` would (a non-number counts 0),
  added up and put on the clipboard (`cmPutInClipboard`); the text is untouched and nothing is shown. Written as
  `Str(R:0:20)` less trailing zeros, but summed with `Decimal` (a departure: DN's `Real` printed binary error).
  DN's table also gave ^K^U to it, but `cmUnindentBlock` had ^K^U first and the menu shows Unindent there, so ^K U
  stays Unindent. A stream block gets `dlED_VertNeed`.
- **Print block, ^K P / Shift+F8** (`PrintBlock`, DN's `Print(On)` in `EDITOR.PAS`, also Editor > File > *Print
  block*): *Print N lines?* (`dlED_PrintQuery`, titled *Confirm*, DN's `mfYesNoConfirm`), then the block's lines
  (`FileEditor.block_lines`, DN's `GetSelection`) to `navigator/lib/system/printing.py`, which hands them to `lp`
  (else `lpr`) in an executor -- the system spooler standing for DN's `.PRN` file and print manager -- as UTF-8: the
  text is Unicode already, whatever the file's encoding, so a CP1251 file prints its letters. Departures, for the
  spooler: LF line ends (DN's CR LF), no closing form feed (it ejects the page), no *Printing* box with a gauge and
  Cancel (one `lp` takes the text at once). A refusal (no printer, no default destination) is shown as the
  spooler's own words.
- **Print file, F8** (`PrintFile`, DN's `Print(Off)`, also Editor > File > *Print*): the whole text the editor holds,
  saved or not (DN printed `FileLines`), less the empty line after a final break; same question and spooler as
  Print block (`EditWindow.print_lines`). `PrintFile` is one command, as `cmPrintFile` was: it lives in
  `navigator/commands.py` (re-exported by `manager/commands.py`) because the file manager's Ctrl+F9 answers it too
  (`navigator-file-ops`).
- **Bracket pair, Alt+Left / Alt+Right / ^Q[ / ^Q^]** (`BracketPair`, DN's `cmBracketPair`, `SearchFwd`/`SearchBwd`
  in `EDITOR.PAS`): on `(` `[` `{` the cursor goes forward to the matching close, on `)` `]` `}` back to the opener,
  across lines, counting only brackets of the same kind and blind to strings and comments, as DN was; no bracket under
  the cursor or no pair, and it stays. ^Q[ and ^Q^] are bound only in the forms the table gives.
- **The info line is `InfoLine`** (DN's `TInfoLine`, a `StaticText` beside `FileEditor`, styled by
  `EditWindow StaticText#info`): a left click on its block indicator runs `SwitchBlock` and one on its line:column
  `GotoLineNumber`, as `TInfoLine.HandleEvent` turned them into `cmSwitchBlock`/`cmGotoLineNumber`.
  With the option strip on, `info_text` leaves the block's kind out (the strip has it; `block_indicator()` is then
  empty). Under *Vertical blocks* the `(↕)` is painted as `InfoLine::column_block` (the info line reversed, a departure:
  the mode is kept per file and DN's plain arrow was missed). `FileEditor.block_indicator()`/`place_indicator()` say where they stand, worked out from the text since the code
  may outgrow three digits; `code_indicator()` is its third place, `[nnn]` (`cmSpecChar`), which opens the
  character table. Every press on the line is the line's, so none reaches the frame.
- **The option strip** (a departure, asked for: DN showed options only as menu `On`/`Off`): navml's `OptionStrip#options`
  on the bottom frame of `EditWindow` (and `FileWindow`), right-aligned before the corner, shown while active and
  `[editor] show_options` (default on, the dialog's last checkbox). Items are `option_items.editor_items`:
  Insert/Overwrite, then the block's kind (`SwitchBlock`, `[↔]`/`[↕]`, lit under *Vertical blocks* -- moved off the info line, which shows
  DN's `(↔)`/`(↕)` and takes its click only while the strip is off; the line-drawing pen stays on the info line);
  Insert/Overwrite is `SwitchInsert`, which `checks` now ticks in overwrite; then Autoindent, Auto wrap (`SwitchSave`),
  AutoBrackets, Syntax highlight, Hidden characters, and the file type (`ChooseFileType`, never lit). Switches are
  spelled per glyph tier -- words (`tr`), `⌶ ⇥ ↩ () § ¶`, or Font Awesome 4 (`icons.OPTION_*`); `⎀`/`↵` were dropped,
  JetBrainsMono Nerd Font lacking them. The type is `highlight.file_type_label(file_type, lexer_name)`: the chosen
  type, else `lexer_name` (the lexing thread returns `(lexer_label, spans)`; kept while Hi is off), else `auto`.
  Priority on a short frame: info line, then strip (`room`), then hbar, which ends a cell before the strip and hides
  under 4 cells. Styled `EditWindow OptionStrip::item:checked { reverse }`, `:disabled { dim }`.
  **Both scroll bars show only while there is more than the edit area holds** (a departure, asked for, as the
  viewer's: DN's were always there). The right one (`vbar`) shows while `FileEditor.overflows`, meaning more lines
  than rows or scrolled down. The bottom one (`hbar`) shows while `overflows_across`, meaning a line on screen, or the
  cursor's column, is wider than the area, or the area is scrolled sideways. Its range is `row_span - 1`, the widest
  of them, not DN's 0 to 255. The frame shows where a bar would be.
- **Hidden characters** (`SwitchHiddenChars`, a departure: Editor > Options > *Show hidden characters*, View >
  *Hidden characters*, the strip's ¶; `show_hidden`, seeded from `[editor]`/`[viewer] show_hidden`, not kept in the
  history): `navigator.lib.viewer.HIDDEN_MARKS` -- `·` blank, `→` a tab's first column, and each line's own ending a cell
  past its text, `↓` LF, `⏎` CRLF, `←` CR (ascii `. > $ $ <`), none on a last line without one. Painted in `render`
  over the cell's own colours (`derive(dim=True)`), so blocks and the current line show through; columns, cursor and
  bytes do not change. **Ctrl+Shift+8** on both windows' `keys` (Word's key for its ¶; kitty protocol only), so it is
  in `keybindings.ini` and the menus show it.
- **The character table, Ctrl+P** (`AsciiTable`, DN's `cmASCIITable`/`cmSpecChar`, also Editor > Misc > *Character
  table* and the info line's code): `AsciiChart` (`shell/ascii_chart`, DN's `TASCIIChart`, 34 by 12) around
  `CharTable` (`shell/char_table`, `TTable`: 32 by 8 CP437 glyphs from `viewer.cp437`, block caret) and a report line
  (`TReport`). Arrows/Home/End move, a press or drag picks, Esc cancels, Enter/Ctrl+B/Ctrl+P or a double click take;
  a character typed that code page 437 has is taken at once. It reopens on the code last taken (`p` at first). The
  editor types what the chart shows -- the glyph, `│` for 179, the text being Unicode -- and a NUL for 0. Departure:
  centred, where DN reopened it where it was left. `AsciiTable` lives in `navigator/commands.py`: the shell answers
  it too (`console-command-line`), and an editor's ^B^V chord keeps Ctrl+B in the editor, as DN's table did.
  **That chart is the ASCII glyph tier's only.** Both callers go through `pick_character(app, glyphs)`
  (`shell/unicode_chart`), which in the Unicode and Nerd tiers opens `UnicodeChart`, *Character Table* (a departure,
  by request): sized to the screen (at least 76×22); a search line (history `charsearch`); radio *Blocks* /
  *Categories* / *Nerd Fonts* (Nerd tier only) over a list of groups, *Recent* always and *Search results* first
  while a query is set; `UnicodeGrid` (`shell/unicode_grid`, a `ListViewer` whose items are rows of codes, three
  columns a cell so wide glyphs fit; `column` + `cursor` → `index`/`code`; `show(codes, at)`); a two-row info line
  (U+, glyph, name; category, decimal, UTF-8, block); *Insert* (default), *Copy*, *Cancel*. The model is
  `navigator/lib/utilities/unicode_table.py`: blocks from the shipped `assets/unicode/Blocks.txt`, at once (pinned to
  `tools/unicode_tables.py`'s `UNICODE`, the newest any supported Python has; a block this Python's `unicodedata`
  has nothing in is left out, which is what lets one file pass `--check` on 3.12 and 3.13 alike); the
  general categories, Nerd sets (`nerdfont.txt`) and name search need `build_index`, run once per process on a
  `Background` thread (≈0.3 s), the grid saying *Reading the character names...* meanwhile; searches run there too,
  a stale answer dropped (`searched` is the query the shown results are for -- tests wait on it). Unassigned codes,
  surrogates and private use outside the Nerd sets are never listed; `display()` draws controls as control pictures,
  marks on `◌`, format characters as `⬚`. Typing anywhere goes to the search line (departure: DN took a typed key at
  once); Enter/Ctrl+B/Ctrl+P/double click take, Ctrl+C/Ctrl+Ins or *Copy* copy (`copy_to_clipboard`) and take
  nothing; both move the code to the front of *Recent* (`RecentChar` model, `recent_chars`, newest 64). It reopens on
  the grouping, group and character last left (`_last`, `p` in Basic Latin at first). Block, category and Nerd set
  names are the standards' and stay English.
- **Open, F3, and Save as, Shift+F2** (`LoadText`/`SaveTextAs`, DN's `cmLoadText`/`cmSaveTextAs`, `OpenFile` and
  `SaveFileAs`; also Editor > File): the name from navml's `FileDialog` via `EditWindow._ask_file` -- *Open a File*,
  *~N~ame*, an *~O~pen* button (`fdOpenButton`), history `edit_open` (Shift+F4's too, as `hsEditOpen` was); *Save File As*, *~S~ave File As*, OK,
  `edit_save` -- listing the active panel's directory. Open offers a changed text a save first (Cancel keeps all),
  records the file being left, loads the new one into the same window -- insert mode, line drawing off, as `LoadFile`
  reset them (`use_document`) -- and brings its record back (a departure: DN's `OpenFile` neither stored nor restored
  the history); a file that will
  not open is said and the text stays (DN closed the window). Save as asks `_check_for_over`'s question without
  *Append* (a departure: appending the whole text elsewhere and then editing that file under its name lost what was on
  disk at the next F2), puts a read-only file's mode back, and the window takes the new name; `FileSaved` re-reads
  panels. `_check_for_over` is shared with ^K W, which keeps *Append*.
- **A changed text shows in the title** (a departure, asked for: DN showed it on the info line alone): `_title()` puts
  the info line's mark in front (`☼ `, `* ` in ascii), which Window > List shows too, and `_follow_modified` (an
  effect from `mounted()`) tags the window `.modified`, so `EditWindow.modified::title { fg: yellow }` writes the title
  in yellow.
- **Confirm file save** (a departure, asked for: DN's F2 wrote at once): F2 and Ctrl+S (`SaveText`) ask *Save file
  NAME?* (Yes/No, `EditWindow._confirm_save`) under Options > Confirmations' *Editor file save*
  (`[confirmations] save`, on by default). Save all and the Yes of closing's *Save?* do not ask again. conftest turns
  it off so F2 writes at once in tests; a test of the box sets it back on.
- **Save all, Ctrl+F2** (`SaveAll`, DN's `cmSaveAll`, a `GlobalMessage` of `cmSaveText`; also Editor > File): every
  editor window, this one first and the rest front to back, saved as F2 saves, each failure said and the rest going
  on. A departure: only changed texts are written, where DN's `SaveFile` rewrote every one. The application's Ctrl+F2
  (Hide right) is disabled with no console showing a file manager, so the key reaches the editor window.
- **SmartPad, Alt+Q** (`OpenSmartpad`, DN's `cmOpenSmartpad`, ≡ > *SmartPad (TM)*; `navigator/lib/utilities/smartpad.py`): one
  editor window on `settings.smartpad_path()` -- `SmartPad.DN` in `$SMARTPAD`, else beside the database (DN's fell
  back to its own directory). Each opening stamps the end (not a restored desktop's, `open_smartpad(stamp=False)`, as `Awaken` only loaded), `InsertInfo`'s `──────< date time >──…` (`FileEditor.stamp`)
  with the cursor on an empty line under it; a stamp alone is not a change (a text already changed stays so). A second
  Alt+Q brings the one pad up and stamps again. The window is the desktop less two cells all round (not zoomed),
  titled *SmartPad(TM) - path*; `EditWindow(smartpad=True)` keeps no edit history, saves unasked on closing (Esc,
  Close all, Alt+X) and sends no `FileSaved`. Alt+Q is on `Navigator.keys`; the Shell answers it, putting the console
  away first.
  **Open (F3) and Save as (Shift+F2) end SmartPad** (`EditWindow._leave_smartpad`; a departure -- DN's window stayed
  SmartPad with the other file in it, and its F3 asked `AskSave` where here the pad is saved unasked): the window takes the other file
  and is an ordinary editor from then on -- its title, history, *Save?* on closing and `FileSaved` -- and the next
  Alt+Q opens a fresh pad, which `open_smartpad` finds by the `smartpad` flag (else it brought up that file and
  stamped it). Open saves the pad unasked first, as closing does; Save as leaves the pad's file as it was on disk.
- **Find and Replace** (`StartSearch` F7 / ^Q F, `Replace` Ctrl+F7 / ^Q A, `ContSearch` Shift+F7, `ReverseSearch`
  Alt+F7 / ^Q R; DN's `StartSearch` in `EDITOR.PAS` and `TFileEditor.Search` in `MICROED.PAS`). The model is
  `navigator/lib/editor/search.py` (`SearchData`, the record `SEARCH` kept between searches as DN's typed constant was --
  look it up as `search.SEARCH` at call time; Alt+F7 with text fills it too, `filefind.hand_on`, as DN's `FindFiles` did; `find`/`find_in_line`; `BREAK_CHARS` now lives there). Line by line:
  forward from a place, backward a match ending at or before it; *Case sensitive* off ignores case, *Whole words only*
  wants `BREAK_CHARS` or a line's edge round it, *Selected text* searches only the block's part of each line
  (`FileEditor._search_bounds`, stream or column; a departure: a stream block's first line is clipped at the block's start, where DN clipped only a one-line or column block and searched a longer block's first line whole). `FindDialog` (`editor/find_dialog`) is both `dlgEditorFind` and
  `dlgEditorReplace` (property `replace`, every rectangle the resource's), opening on a one-line block's text, else the word at the cursor
  (`StartSearch`'s guess; the block a departure, asked for), history `find_text` for both lines; *Change all* answers `"all"`. Help is shown disabled, and Goto Line has none, until F1 Help exists. *Entire scope* starts at
  the text's start (its end, backward); nothing found says *Search string not found* and puts the cursor back. A
  match puts the cursor after it (before it, backward) and is lit while the cursor and text stay
  (`show_found`/`found_on_display`); a reversed search with it lit starts from its far side (`SearchOnDisplay`).
  Replacing asks `ReplaceQuery` (`dlQueryReplace`, titled *Query* as `mfQuery`, Yes/No/All/Cancel in the flags' order; *All* stops the asking) while *Prompt on
  replace* is ticked, each replacement its own undo step (`udReplace`); only *Change all* goes on past the first;
  *N replaces made* comes only when the loop runs out (*Change all*, or after *All*) and counts the matches found without asking -- not the one *All* was pressed on (`Inc(NumRep)`); one replacement or Cancel says nothing. Shift+F7 repeats the last search, replacement included, from
  the cursor. Departure: the query box is centred, where DN put it clear of the line found.
- **The Find bar, Ctrl+F / Ctrl+R** (`ShowFindBar`/`ShowReplaceBar`, also Editor > Search > *Find bar*/*Replace
  bar*; a departure, asked for, after IntelliJ IDEA's -- DN had the dialogs alone, which F7/Ctrl+F7 keep):
  `FindBar` (`editor/find_bar`), a child of `EditWindow` declared after the editor so it paints over its top-right
  corner a cell short of the scroll bar, 50 wide (none under a 36-cell edit area; `ShowFindBar` is then disabled),
  dialog-coloured (`EditWindow FindBar`). Row 1: the text (`Field#query`, history `find_text` shared with the
  dialogs), `Aa W .*` (*Match case* Alt+C, *Whole words* Alt+W, *Regular expression* Alt+R -- not IDEA's Alt+X,
  Navigator's quit; `::switch:checked` reversed), the count (`3/12`, `?/12` with the cursor off a match, `…`
  while counting, *No matches* / *Bad pattern* in `::error`), `↑ ↓ ×` (`^ v x` in ascii). Row 2 (Replace): the new
  text (`Field#new`), *Replace* and *All*. Everything after the lines is painted by `render` and clicked through
  `_hits`; tooltips name the keys. Keys are its own table (`[find_bar]` in `keybindings.ini`): Enter/F3 next,
  Shift+Enter/Shift+F3 previous, both wrapping round with no box; Enter in the new text replaces (`FindNext`
  checks the focus); Alt+A / Ctrl+Alt+Enter all; Tab/Shift+Tab between the lines (`on_key`); Esc closes and gives
  the editor the keyboard. Esc in the *editor* closes the bar too while its matches are lit -- in
  `FileEditor.on_key`, not its table, which would shadow the window's Esc (a test forbids that).
  **Incremental**: `open` seeds from `FileEditor.search_seed()` (a one-line block, else the word at the cursor, from
  its start, which is the origin) and an effect searches from the origin on every change of the text or a switch
  (`untracked()` round the search, or the cursor it moves would re-run it); nothing found puts the cursor back at the
  origin (`place_cursor`). Matches are shown with `show_found`, so `found_on_display` is what the count and the
  arrows go on from. **Every match on screen is lit**: `FileEditor.highlight_query` (a `SearchData`, replaced) and
  `render` painting `search.line_matches` per visible line as `FileEditor::match` -- the line's own colours reversed
  and underlined, so no theme needed a slot -- under the block and the match found. **The count
  runs on a thread** (`Background("find-count")`, `search.all_matches` over a copy of the lines, at most
  `MATCH_LIMIT` = 10 000, shown `10000+`), an effect on the search and `editor.revision`, a stale answer dropped by
  generation; the place among them is `bisect` on the loop. *Replace* replaces the match lit (else finds one first),
  one undo step, and finds the next; *All* is `FileEditor.replace_all`, last first, **one** undo step, and says
  *N replaced* in the count's place. The bar writes text and switches to `search.SEARCH` (whole text, forward,
  `new` None), so Shift+F7/Alt+F7 go on from it; the dialogs set `regex` back off (`FindDialog._store`). **Regular
  expressions** are the bar's: `SearchData.regex`, `search.pattern_of` (cached), `valid`, an empty match never one;
  within one line unless the pattern **crosses** -- a `\n`/`\r` in it or the `s` flag (`search.crosses`; `\s+` and
  `[^x]*` alone never do, so old searches find the same) -- when the text is searched whole, joined by `"\n"`
  whatever its endings, under `re.MULTILINE` (`^`/`$` still a line's ends). `all_matches` is
  `(line, start, end_line, end)` for every pattern; painting a crossing pattern's matches searches only the lines
  shown and `WINDOW_MARGIN` either side (`window_matches`, cached by `FileEditor._window_marks`); the found match
  paints over its lines as a stream block (`_found_columns`); a column-block scope refuses a crossing pattern.
  `replacement()` (through `FileEditor.replacement`) expands `\1`/`\g<name>` from the match at the place found and
  writes every line break in what goes in as the text's own ending, the dialog path's replacing too. F3's *Open* closes the bar. Known limit: the bar can cover a match on the top
  two or three rows, which is not scrolled clear.
- **Paragraph formatting, Alt+J/R/L/C** (`FJustify`/`FRight`/`FLeft`/`FCenter`, DN's `cmF*` and `FormatBlock`; also
  ^B^J/R/L/C and Editor > Paragraph): `navigator/lib/editor/paragraph.py`. The stream block's whole lines (one ending at a
  line's start leaves that line out) are one paragraph -- blank lines are no break, runs of blanks one -- laid out
  between `FileEditor.margins` (`LeftSide`, `RightSide`, `InSide`): a line takes a word while `length + word`
  stays under its room (the blank not counted, DN's `+ J`, so a line may reach it); right ends against the right margin, center sits midway, justify widens every line but the
  last gap by gap from the left and indents the first. One undo step; the block then covers the new lines, the cursor
  at its start. Disabled for a column block. **The cursor's line alone**: `LJustify`/`LRight`/`LLeft`/`LCenter`
  (DN's `cmL*`, `EDITOR.PAS:823`: the line made the block, shown, then `FormatBlock`; `format_line`), DN's for macros
  with no key in the English resource -- keyless here too (`keyless_commands`, bound by no preset) and on Paragraph > *Current line* (a
  departure, as item 4's entries are); refused under column blocks ("Line format works on line blocks") where DN
  did nothing. *Margins...* (`SetMargins`, `MarginsDialog`, `dlgEditorFormat` 39 by 11)
  changes this editor's margins only, seeded from the Editor setup, a number that does not read kept, then
  `fix_margins` (`SetFormat`'s corrections).
- **Auto wrap and Justify on wrap** (`FileEditor.autowrap`/`justify_on_wrap`, DN's `AutoWrap`/`AutoJustify`, seeded from
  the Editor setup, switched per editor by Editor > Options -- `SwitchSave` is DN's own name, `cmSwitchSave`, for
  *Auto wrap*, `SwitchWrap` (`cmSwitchWrap`) for *Justify on wrap* -- and ticked through `checks`): a character typed
  at or past the right margin (`type_text`, `InputChar`'s `LastX >= RightSide`) wraps the line, its own undo step
  after the typing's (`_wrap`, `paragraph.wrap_line`, DN's `SplitString`). Trailing blanks go; a line still past the
  margin is cut after its last blank or `,:.?!+;` at or before it -- so a word ending on the margin with no break
  there moves too, as in DN -- the rest put under the left margin; *Justify on wrap* widens what stays to the margin.
  The cursor follows its text. Departure: a line with no break before the margin is cut at the margin, where DN's
  search stopped at the first character. Pastes do not wrap, as DN's `InputChar` alone did.
- **AutoBrackets** (`FileEditor.auto_brackets`, DN's `AutoBrackets`, seeded from the Editor setup, switched per editor
  by Editor > Options > *AutoBrackets* -- `SwitchBrackets`, `cmSwitchBrackets` -- and ticked): `(`, `{` or `[` typed
  at a line's end or before a blank goes in with its partner, the cursor between (`_bracket_pair`, `InputChar`'s
  `LastX >= WL or WorkString[LastX+1] = ' '`); before anything else -- its own closing bracket included -- and in
  overwrite, the character alone. One undo step with the typing.
- **Autoindent and Backspace indents** are DN's `MakeEnter` and `MakeBack`, per editor (`auto_indent`/`back_indent`,
  seeded from the setup's *Auto indent* and *Backspace unindents*, switched by Editor > Options *Autoindent*
  (`SwitchIndent`, `cmSwitchIndent`) and *Backspace indents* (`SwitchBack`, `cmSwitchBack`), ticked). **Enter**
  (`on_new_line`): in overwrite only to the next line's start (a line added past the last). **Overwrite reaches four
  more places, as DN's `InsertMode = Off` did:** Backspace (`_overwrite_back`, `MakeBack`) makes the character
  before the cursor blanks as wide as it and never joins at column 0 (*BackIndent* still first); Tab blanks what it
  crosses and past the end only moves (`_overwrite_tab`); deleting a column block -- Del, Cut, typing over it --
  fills the rectangle with blanks and leaves the cursor (`_take_block`, `udClearBlock`); and with *Vertical blocks*
  any paste goes in as a rectangle (`insert_text`), replacing its width of each line in overwrite
  (`_put_rectangle(replace=True)`). **Ctrl+N** (`on_insert_line`, `cmInsLine`) is `MakeEnter` with the cursor put
  back: Enter's split (`_split_line`) inserting, in overwrite a line added only after the last; a block is let go,
  never taken. Inserting, the part kept
  loses its trailing blanks (tabs too, DN having had only spaces) and the part moved the line's last ones; with
  Autoindent the moved part's leading blanks give way to the indent of the part kept -- the whole line's if that part
  is blank -- the cursor at it, and a new line with nothing after the indent is left empty with the cursor waiting
  there; without, it moves as it is, the cursor at column 0. A departure, part of Autoindent rather than a switch of
  its own: a line of nothing but blanks gives the cursor's column -- its blanks up to the cursor plus `_index()`'s
  virtual `past` -- so Enter after Enter stays at the indent, where DN's went back to column 0; the new line is still
  left empty, the column living in the cursor alone. Edits go right to left so a block's ends follow. **Backspace** (`_unindent`): only on a line's first
  character (blanks before, none under) or anywhere on an all-blank line, never on the first line; back to the indent
  of the nearest line above with text and a narrower indent, the blanks before the cursor becoming that many spaces;
  no such line, a plain Backspace. Departure from DN, which expanded tabs: a leading tab is indentation by its width.
- **Line drawing, F4 / ^Q^M** (`SwitchDrawMode`, DN's `cmSwitchDrawMode` and `DrawLine`; also Editor > Misc > *Line
  Drawing*; `navigator/lib/editor/linedraw.py`): F4 cycles `FileEditor.draw_mode` off, single, double; the info line shows
  `{┼}`/`{╬}` where the block's kind was, and the pen is lifted. While on, the arrows (and ^E ^D ^X ^S) are
  `DrawLine`'s before any key table -- `FileEditor._run_key` looks at the raw key, since a command does not carry the
  modifier that decides: Shift draws, Ctrl erases, neither only moves a cell. Drawing picks the cell's character from
  a 15-entry mask table (up 1, right 2, down 4, left 8) of the arms its neighbours reach it with, the way the pen came
  and the way it goes, in DN's four tables (`Line00/01/10/11`, so a line crossing one of the other weight gets the
  mixed junction); going straight back the way it came draws nothing. Erasing blanks the cell and takes the arm into it
  off any neighbouring junction (three or four arms; a plain line beside is left). Down off the last line adds one.
  Each stroke is one undo step. ^Q^M is bound as `ctrl+q enter` too, Ctrl+M arriving as Enter.
- **Duplicate line, F6** (`DuplicateLine`, DN's `cmDuplicateLine`, also Editor > Misc): a copy of the cursor's line
  under it, put after the line's own text so the line keeps its ending and the copy takes the file's usual break; the
  cursor stays; one undo step.
- **Line and word deletes are DN's** (`MICROED.PAS`): Ctrl+Y (`DeleteLine`, `DeleteLine`) takes the line and its
  break, the cursor to column 0; on the last line it only empties it. Presses on one line merge into one undo step
  (`merge="delline:N"`, `udDelLine`); a move between seals. ^T at a line's end (`DeleteWordRight`) joins the next line
  and eats its leading blanks, joining on through empty lines (`_join_next`). Ctrl+Backspace (`DeleteWordLeft`) stays
  on its line: blanks, then the word before them; at column 0, on an empty line, or after punctuation it is Backspace
  (`foo. |` keeps `foo.`). `_word_left` is Ctrl+Left's alone.
- **Word and line case** (`UpWord`/`LowWord`/`CapWord`, DN's `cmUpWord`.., and `UpString`/`LowString`/`CapString`;
  Editor > Misc > Uppercase/Lowercase/Capitalize > *Word*/*Line*): Ctrl+[ / Ctrl+] / Ctrl+\ (and Alt+/ for Capitalize)
  change the word the cursor is in or just after -- back to a `BREAK_CHARS` character and on to the next -- and with
  Shift the whole line (`_recase_here`). A blank line is left alone; the line loses its trailing blanks either way; the
  cursor stays; one undo step. `capitalize` is `CapCaseStr`, shared with ^K \. Ctrl+[ is Esc's byte and the Ctrl+Shift
  forms need the kitty protocol; Ctrl+], Ctrl+\ and Alt+/ arrive from any terminal, and the menu works everywhere.
- **Optimal fill** (`FileEditor.optimal_fill`, DN's `OptimalFill`, seeded from the setup, switched by Editor > Options >
  *Optimal fill* -- `SwitchFill`, `cmSwitchFill` -- and ticked): what is written goes through `columns.optimal_fill`,
  DN's `CompressString` -- chunk by chunk of the tab size from the line's start, a chunk ending in two blanks or more
  has that run made one tab; a lone blank and a last partial chunk stay. Applied in `FileEditor.snapshot` (every save
  path) and `block_file_text` (^K W); the text in the editor keeps its blanks. With it on, saving rewrites blanks in
  lines nobody touched -- the option's point, and the one exception to byte-for-byte, off by default. Departure: chunks
  are measured in columns, keeping a tab already there, where DN met only spaces (tabs expanded on loading); and a chunk is the tab size wide, where DN's were 8 whatever the tab size (a tab is shown at the tab size, so a saved file must reopen the same; at 8 the two are one).
- **Current line and column highlight** (`FileEditor.highlight_line`/`highlight_column`, DN's `HiliteLine`/
  `HiliteColumn`, seeded from the setup, switched by Editor > Options -- `SwitchHiLine`/`SwitchHiColumn`,
  `cmSwitchHiLine`/`cmSwitchHiColumn` -- and ticked): `render` paints the cursor's row in `FileEditor::current_line`
  ([182]), a block or match on it in `::current_line_selected` ([183]), and the cursor's column on every row of the
  window, text or not, in `::current_column` ([185]), laid last as DN's `Draw` set `CC[7]` over all else.
- **Syntax highlight** (`FileEditor.syntax_highlight`, DN's `HiLite`; `editor.syntax_highlight` in `navigator.ini`,
  on by default, no checkbox since `dlgEditorDefaults` had none; switched by Editor > Options > *Syntax highlight*,
  `SwitchHighLight`/`cmSwitchHighLight`, ticked; kept in `EditRecord.highlight`). **Pygments lexes**, in token mode
  (`navigator/lib/highlight/__init__.py`), where DN had `DoHighlite` and `DN.HGL` -- a departure: multi-line comments and strings
  come out whole. **`highlight.ini`** beside `navigator.ini` is `DN.HGL` (seeded through `associations.TEMPLATES`,
  Options > *Highlight file edit...*, `EditHGL`/`cmEditHGL`): mask sections with `lexer = <Pygments alias>`, `none`,
  or `auto` (Pygments' guess by name and first line, even under `[*] lexer = none`), first match wins. **A section
  also carries DN.HGL's editor modes** (`InitEditorHighLight`, `MACRO.PAS:655`; `highlight.EDITOR_KEYS`) under
  `navigator.ini`'s `[editor]` names: `syntax_highlight`, `auto_indent`, `auto_brackets`, `backspace_unindents`,
  `highlight_line`, `highlight_column`, `autowrap`, `justify_on_wrap`, the three margins, and `line_ending =
  crlf|cr|lf` (DN's `FORCE*`, `ForcedCRLF`: every line *written* with it in `snapshot()`, new lines take it,
  opening changes nothing; choosing Line endings by hand clears it). `[*]` is DN's `DEFAULT`. Each key comes from the
  first section that takes the file and sets it (`Rules.editor_defaults`; a departure: DN stopped at the first
  matching `FILES`); a bad value or unknown key is ignored. Departure: DN's `AUTOWRAP`/`WRAPJUSTIFY` set each
  other's flag; here each does what it says. Read on the loading thread (`load_document` →
  `Document.defaults`) and applied by `FileEditor.apply_defaults` in `use_document`, on every load (open, Load
  text, SmartPad, a new file), only the keys named. Order: Editor setup, then masks, then the edit history.
  **Its template
  lists every language Pygments knows** -- `navigator/assets/highlight.ini`, written by `tools/highlight_ini.py`
  (`--check`; rerun after upgrading Pygments): Navigator's own head (`*.nml` -> `nml`, `*.nss` -> `nss`, `*.log` none), then a pattern
  two lexers can claim (case folded: `*.c`/`*.C`) in an `auto` section naming the candidates, then one section per
  lexer, and a hand-kept `[#!]` of ~35 interpreters. `test_the_template_lexes_every_pattern_as_pygments_would` holds
  it to Pygments' own choice for each pattern. `default_rules()` parses it lazily (~70 ms). **`navigator/lib/highlight/lexers.py` is Navigator's own two lexers**:
  `NssLexer` (a `RegexLexer`; colour names and `Style` fields read from `navkit.stylesheet`, so they cannot drift) and
  `NmlLexer` (line by line, since indentation decides what a line is: heads, directives, `id`, `on_*` handlers,
  properties whose values go to Pygments' `PythonLexer` and run on while a bracket is open, `keys:` lines, and
  `style:` lines whose values go to `NssLexer.value_tokens`; `#` a comment only before a blank, an end or `:`). They
  keep no state on the instance -- `_lexer_named` shares one across threads -- and live in `navigator` because it is
  the layer that depends on Pygments. `_lexer_named` finds them by alias before asking Pygments; installed, the
  `pygments.lexers` entry points in `pyproject.toml` make them Pygments' too. A test lexes every `.nml`/`.nss` in the
  tree and refuses an `Error` token or a gap; `[#!]` maps interpreters (`env` and its options looked through, a
  trailing version optional); `[*] lexer = auto` falls to Pygments' guess by name, `none` stops there. Missing or
  broken, the template's rules (`DEFAULT_RULES`); re-read when its mtime changes, and saving it (`FileSaved`) makes
  every editor and viewer `rehighlight()`. **A token is painted as `FileEditor::token` with its Pygments type's pieces
  as classes** (`String.Double` -> `.literal.string.double`), and `:current_line` on the highlighted line;
  `navigator.nss` maps comments [164] ([184] on the current line), operators/punctuation [189], strings [190] and
  numbers [191], the last three foreground only as DN's `Draw` did. Keywords (and `Operator.Word`: `and`, `not`,
  `in`) are `$keyword`, a `DERIVED` alias of Normal text [76] -- plain, as DN left them -- which `default` gives
  yellow. Headings (`Generic.Heading`/`Subheading`: Markdown's `#`, reST's, a diff's file and hunk lines) are bold in
  `$heading` (the editor, the quick view) and `$viewer-heading` (the viewer's plain and Markdown views): `DERIVED`
  entries the keywords' colour in every DOS theme, and each modern theme's own (solarized-light's olive keywords were
  too faint on cream). A test holds them to 3:1 on their ground in every theme. A block or found
  match paints over tokens, the current column over everything. **Lexing runs on a thread** (`_LEXER`, from `render`
  as `DirectoryTree` asks for counts): the whole text from line 0 to `LEX_AHEAD` lines past the screen, the lexer
  chosen there each time from the name and first line. Edits shift the spans (`highlight.shift_spans`, typing inside a
  span widens it) and drop `_lexed` to the edited line; an answer keeps only the lines before any edit made while it
  ran, and `render` asks again. Over `LEX_LIMIT` (2 M characters; Pygments lexes about 0.5 M a second) a text stays plain. Use `lex_lines` and the
  `get_tokens_unprocessed` it walks -- never `get_tokens`, which strips and expands and so moves indices.
- **A few lines in memory** are lexed with `highlight.lex_text(name, lines)`, synchronously on the caller's thread,
  and come back plain when there is no such lexer or it fails. It lexes with a line break after the last line, because
  `pytb`'s rules each end in one and would otherwise leave the exception line plain. Its one user is the error box's
  traceback (`ErrorDialog`, `pytb`). `TraceList`, a `ListViewer` with a parallel `spans` list, paints the spans through
  `ErrorDialog TraceList::token`. `navigator.nss` gives it the editor's text, current line and highlight colours,
  because a dialog list's cyan swallows them. It also styles `name.builtin` (the frame's file) as a string,
  `generic.traceback` as a comment and `generic.error` (the exception) as a keyword. `error_dialog.fold` wraps by
  offsets, so each row takes its piece of its line's spans.
- **File type** (Editor > *File ~t~ype* -- on the *Editor* menu itself, not under *Options*, so it is one step away
  as on the viewer's *View* -- and View > *File type* in the viewer; `SetFileType(file_type)`, a
  departure -- DN chose a `DN.HGL` section by mask alone): *Automatic* (`""`, `highlight.ini`'s choice), a submenu
  each for *Programming*, *Scripting* and *Markup languages* and *Miscellaneous*, and *None* (`none`). The languages
  are `highlight.FILE_TYPES` (group name, then caption and Pygments/own lexer name), short enough that each box fits
  24 rows; the menus are empty `SubMenu`s in the markup filled by `file_type_menu.fill_file_types` (hotkeys picked
  by `_marked`, the first character not yet taken; group captions bound live through `tr`; at the Nerd tier each
  language's caption starts with its icon, `icons.icon_for_masks(highlight.file_type_masks(lexer))` -- the masks read
  from Pygments' table, never the lexers, so filling the menu imports none -- and the option strip's *File type*
  item shows the chosen type's icon the same way, the file's own while it is *Automatic*). `FileEditor.file_type`/
  `FileViewer.file_type` go to `lexer_for(..., file_type=)`, which then decides alone, and are part of what the tokens
  were lexed for. Choosing switches highlighting on (*None* leaves it), is ticked through the window's `checks`, and
  is written to the record at once (`remember_history`); kept as `EditRecord.file_type`/`ViewRecord.file_type`. F3's
  *Open* into the same editor resets it before the new file's record is read. **Ctrl+Shift+H** (`ChooseFileType`, on `EditWindow.keys` and
  `FileWindow.keys`, so in `keybindings.ini`) opens the same menu as a `PopupMenu` centred on the window
  (`file_type_menu.choose_file_type`), and both *File type* submenus show it through `key_command`; it needs the kitty keyboard protocol, Ctrl+H being Backspace's byte.
- **Go to line, Alt+G** (`GotoLineNumber`, DN's `GotoLine`, also Editor > Search > *Go to line number...* and the
  info line): `GotoLineDialog` (`dlgGotoLine`'s *Goto Line*, a row taller like the viewer's *Goto Address*, history
  `goto_line`) opens with the number last typed, as `GotoLine`'s `const S` kept it; a number above 0 puts the cursor
  on that line at the same column (`FileEditor.go_to_line`, `ScrollTo(Delta.X, I-1)`), past the end on the last;
  anything else does nothing. DN shared its history with *Goto Address* (`hsdbSearch`); here each has its own.
- **A hidden block** (`block_hidden`, DN's `not BlockVisible`; ^K H / Alt+H toggle it): still marked (`marked`) and
  still following edits, but not painted and not acted on -- `has_block`, which the block commands' `enables` read,
  is DN's `BlockVisible and ValidBlock`. Marking anew shows it (`_set_block`/`_set_ordered`, `read_block`, `_unmark`).
- **Editor macros, Ctrl+J 0** (`SelectMacro`, DN's `cmSelectMacro`, empty there): `macros.ini`'s `MACRO` blocks
  for the file's type in a `PopupMenu`, the one chosen played by `macros.play_steps` -- the
  `navigator-macros` skill has the file's syntax and how lines run.
- **Markers, ^K1-9 / ^Q1-9** (`PlaceMarker(n)`/`GotoMarker(n)`, DN's `cmPlaceMarker`/`cmGotoMarker` over `MarkPos`):
  `FileEditor.markers`, nine fixed `(line, col)` -- not moved by edits, as DN's were not. Going to one centres it
  (`Pos := Delta - Size div 2`) and, being a movement, unmarks under *Persistent blocks* off; an unset one does
  nothing. Kept in the edit history as `EditRecord.marks` (`fMarks`), `line:col` nine times comma-separated, and
  brought back whatever *Store editor position* says. The digit is bound alone, as the table has it.
- **^Q D/T** insert the date/time in Country support's format (`country.format_date`/`format_time` with seconds), as
  DN's `GetDateTime` (`ADVANCE.PAS:371-409`) followed the country's order and 12/24 hours; inserted even in overwrite;
  `_now` is the test hook. A departure: DN's `MakeDate` took the year `mod 100` and wrote am/pm straight after the
  seconds; here year and am/pm are as Country support writes them everywhere else. Column blocks take all the ^K commands.
  A pending chord shows as `^K` at the info line's end (a departure).
- **Column blocks** under `vertical_blocks` (Editor setup's *Vertical blocks*, seeded per editor and kept in the edit
  history; `SwitchBlock`, DN's `cmSwitchBlock`, switches it -- ^B^V and Editor > Options > *Vertical blocks*,
  ticked through `FileEditor.checks`. DN's block was two points either way, so the switch keeps it and reads it the
  other way: a stream block becomes the rectangle between its ends, a rectangle the stream from top-left to
  bottom-right; one enclosing nothing goes).
  `FileEditor.column_block` is two corner *cells* `(line, col)` -- columns, not indices, since a rectangle runs past
  short lines and across tabs -- and `rectangle` is `(top, left, bottom, right)`, right exclusive. Only one of
  `block`/`column_block` is ever set; marking code speaks of "ends" (`_here`, `_block_ends`, `_set_block`) so keys,
  Shift+click, drags and double-clicks serve both. A character belongs to the column it starts in
  (`columns.span`), so a tab straddling the left edge stays out. A copy hands out each line's piece without padding
  blanks, and remembers the padded pieces in `_COLUMN_CLIP` (newest only): pasting exactly that text back inserts a
  rectangle (`_insert_rectangle`: short lines padded to the column, lines added past the end, the cursor left at the
  top-left). A column block keeps its columns through edits and moves only by whole lines.
- **The mouse marks too.** A left press puts the cursor there and unmarks; a drag (captured, and only once the
  pointer leaves the pressed cell -- terminals report motion inside it, `_press_cell`) marks from the press,
  scrolling a line at a time past the top or bottom row; Shift+click (or Ctrl+click, for VTE terminals that keep Shift+click, as in panels) extends the block as Shift+movement does (a departure: DN's press always began afresh); a Ctrl+drag instead marks whole lines from the pressed one to the pointer's, the break included (DN's `LineMarking`, `_line_from`/`_mark_lines`; not under *Vertical blocks*); a
  double-click marks the word as ^K T does (`cmMarkWord`, DN's `Event.Double`; on a blank, the word before it), the cursor at its start, and a drag with the button still down after it marks whole
  words (`_drag_word`; the press before the double-click already captured the mouse, so `on_double_click` must not
  end the drag). A block marked by the mouse becomes the primary selection on
  release (`copy_to_clipboard(primary=True)`), and a middle click pastes the primary selection (a departure: DN's other buttons showed the ruler) -- what the console and
  the input lines do. Ctrl+Ins still copies the block to the clipboard. Checked on a pty with SGR mouse bytes and
  `xclip -o`, not only with posted events.
- **The right button: a click is the context menu, a drag DN's column ruler** (`RulerVisible`, `MICROED.PAS`;
  `FileEditor._right_button`). The press captures the mouse, so navkit offers no `ContextMenuEvent`; the first move
  to another cell sets `ruler` and the cursor follows the pointer (scrolling past the top/bottom as the left drag
  does); a release after a drag hides it and leaves the cursor, and a release that never moved opens the menu
  through `open_on_click(self, ContextMenuEvent.of(press))`, so `prepare_context` still decides about the block.
  Painted on the cursor's row from its column in one `draw_runs`: `columns.ruler()`, `n mod 10` with every tenth
  the tens digit in `::ruler_tens`; `::ruler`/`::ruler_tens` are DN's `GetColor($4240)`, slots [64]/[66]
  (`$editor-menu-normal`/`-shortcut`). Departures (asked): the menu opens on release and the ruler on the first
  move, and the block is kept (DN's `BlockOff` hid it). `unmounting` and any other press clear a ruler whose
  release was lost.
- **Redo, Shift+Alt+Backspace / Ctrl+Shift+Z** (`Redo`, a departure: DN had none; Borland's IDE had these keys;
  also Editor > *Redo* and the context menu): `EditBuffer.redo_stack` holds the groups undone, any new change
  (`_record`) empties it. `redo()` replays a group forward through the listeners and returns where its last change
  ended, where `on_redo` puts the cursor. Undoing the saved group no longer loses the save point: redoing back to it
  leaves the text unmodified, and `mark_saved` accepts a point redo still holds. Both keys need the kitty protocol.
- **Every bound key is on a menu** (departures, asked for): Editor > Delete > *Delete line* (Ctrl+Y, also the context menu),
  *Delete word left* (Ctrl+Backspace, also the context menu), Editor > *Insert line* (Ctrl+N), Search > *Matching bracket*
  (Alt+Left/Right), Block > *Hide/show block* (Alt+H). And the commands DN reached by ^K/^Q chords alone have modern
  defaults, so their menu items show a key that works: Alt+Shift+V move, K copy, I indent, O unindent (one blank, ^K U;
  Shift+Tab is the tab-stop `UnindentBlock(stop=True)`, a different command), U/L/C upper/lower/
  capitalise block, D/T insert date/time (Alt+Shift+letter arrives from any terminal; the WordStar presets replace
  them with the chords). Ctrl+A is *Select all* (WordStar's *word left* in DN; the WordStar, DN 1.51 and Emacs presets
  take it back with an empty `select_all =`). `menu_box.key_caption` shows the live binding and falls back to the `.nml`'s static `key:`,
  so a static key must be one the default set binds. Left off the menus on purpose: movement, Enter/Tab/Backspace/
  Del, Ctrl+Up/Down scrolling, Insert (the option strip shows it).
- **An external editor asks first** (DN's `Valid(cmQuit)` in `ExecExtFile`, `RUNCMD.INC:273`):
  `navigator/widgets/editor/external.py`'s `save_before_external(app, paths)` -- each changed editor window on one of
  the files (`must_ask`, once per text) asks `EditWindow.ask_save`'s *File X was modified. Save?*: Yes saves (a failed
  save runs nothing), No runs the program on the bytes on disk, Cancel runs nothing. Called by F4/Alt+F4's
  `editors.ini` entry (`run_associated(before=)`, once an entry is found) and `$EDITOR`, the console editors' box,
  Shift+F4's `$EDITOR`, the Options edits' outside branch and `--edit`'s. A departure: only windows on those files,
  where DN asked every changed one; a file on another drive is not asked about (its window edits a copy of its own).
- **The questions name the file by its path cut to 30** (`cut_path`, DN's `Cut(Name, 30)`: two characters, `...`,
  the end): *was modified. Save?*, *already exists. OK to overwrite it?*, *is marked as Read-Only*.
- **Closing asks** through `Window.must_ask`/`ask_to_close` (`Valid(cmClose)`), which `request_close`, Close all and
  Alt+X all go through; `Dialog.buttons` has `yes-no-cancel`.
- **Shift+F4, *Edit new file*** (`cmXEditFile`, `EditNamed`, also File > Edit > Edit new file): DN's `OpenEditor`
  (`MICROED.PAS:1284`): navml's `FileDialog`, *Open a File* with *~O~pen*, history `edit_open` shared with the
  editor's F3, listing the active panel's directory if it is on the disk (`Manager._disk_directory`); a directory
  typed is listed, a missing parent is *Invalid file name.*, a URL or `#/` archive place is taken as typed (`raw`) and
  reaches its drive. `Manager.edit_named` opens it with `open_editor(..., new=True)`, so a name that does not exist is
  an empty text saving creates. With the active panel on another drive the box lists nothing (`FileDialog(unlisted=...)`) and a
  name typed is that panel's. Departures: with *Internal editor* off it goes to `$EDITOR` (DN always used its own),
  and the file's edit record comes back (DN opened on the whole desktop at the top). The save that creates the file says so (`FileSaved.land`, from
  `os.path.lexists` on the write's thread just before it writes), and `Shell.on_file_saved` re-reads each panel
  showing the directory with its cursor on the new file, as F7 does a directory; a save over an existing file leaves
  the cursor alone. Every save also re-reads each information panel (`Manager.reread_info`, `cmRereadInfo`) and
  drops every tree's file count for that directory (`DirectoryTree.file_changed`, `cmRereadTree`), as `FileChanged` did.
- **`nav --edit FILE`** (`-e`, repeatable; DN's files named on its command line, each `EditFile(On, ...)`,
  `DNUTIL.PAS:733`): checked in `main()` before anything starts (a directory, a missing parent or a URL is an argparse
  error), then `Navigator._edit_files` from `on_start`, after the desktop is restored: an editor window each, in order,
  a new name an empty text saving creates. With *Internal editor* off, one `$EDITOR` on the console with them all (a
  departure: `editors.ini` is not asked). The positionals stay the panels' directories.
- **File Edit History (Alt+PgUp)**: DN's `TEditRecord`, the `EditRecord` model, every field `StoreEditInfo` wrote.
  It holds the window rectangle, cursor (`line`, `col`), scroll (`top`, `left`), `overwrite`, `vertical_blocks`,
  `highlight`, `file_type`, the markers, the block (`block`, as `line:col-line:col`, `|` before a column block's
  corners; `block_hidden`), Current line/column, Autoindent, Justify on wrap, Auto brackets and the three margins.
  It comes back whole -- the rectangle, cursor and scroll with the rest -- whenever *Track editing* is on, as
  `EditFile` put it back (`DNUTIL.PAS:1337`). *Store editor position* is DN's other rule: a **new** editor opens at
  the last editor window's rectangle (`TempBounds`, `file_history.LAST_EDIT`, written by `EditWindow._follow_bounds`
  as any editor but SmartPad moves, kept between runs in the `window_bounds` table, `WindowBounds`), scaled to the
  desktop; off, or before any, the whole desktop (zoomed). The record then wins over it. `open_editor` takes
  `LAST_EDIT` before `desktop.open`, since the new window's own effect writes it on mounting. (The viewer still keeps
  its place only under *Store viewer position*; see `navigator-viewer`.) The eight modes and
  margins are nullable: None, a record from before they were kept, leaves the Editor setup's value; margins go
  through `fix_margins`. A block the text no longer holds, or of the other kind, is dropped (a departure: DN put
  `Mark.A`/`Mark.B` back blindly). Auto wrap, Backspace unindents, Optimal fill, Hidden characters and the draw mode
  were not in DN's record and are seeded from the setup each time. **Open editors through
  `navigator.lib.config.file_history.open_editor`**, awaited from a spawned task.
- **Views** (Window > *New view*, a departure): a second `EditWindow` on the same `EditBuffer`, one undo history
  and one save, a cursor, block and modes of its own; only the text's first view asks *Save?* when all close at
  once. Every edit path must call `_edit_here()` before it changes the buffer, or the other views' cursors drift --
  `reference/editor.md`, *Views*, has the rules.
- **Three opt-in modes, departures (not DN's), each off by default** and switched alike -- an `[editor]` setting,
  Editor > Options, a `highlight.ini` mask key, a nullable `EditRecord` field: *Tab characters* (`insert_tabs`,
  `columns.fill`), *Line numbers* (`line_numbers`, the `LineGutter` widget beside the editor) and *Soft wrap*
  (`soft_wrap`, `navigator/lib/editor/softwrap.py`; the text never changes, rows are only painting and Up/Down,
  Home/End stay the line's, never with column blocks). None is on the option strip: its width is the horizontal
  scroll bar's room. `reference/editor.md` has each one's rules -- read soft wrap's before touching `render`,
  `_follow` or vertical movement.
- **While an editor window is active the bar has an *Editor* menu after *File***: DN's `dlgEditorMenu`, its seven menus
  nested as submenus; every entry is a live command, and an option's is ticked while it is on (`checks`). **F10 and
  ^K^Q drop it** (`EditWindow.f10_menu`, read by `Shell.on_open_menu`), as `cmMenu` reached DN's in-window bar first,
  and *File > Main menu* (`MainMenu`, `cmMainMenu`, F10 in its key column) highlights the bar's first entry. **What the
  modern default keys leave unbound is on the menu** (a departure: in DN these were keys alone): Editor > Delete > *Delete word
  right* / *Delete to end of line* (the four deletes are a submenu because on the Editor menu itself the box would be
  25 rows, which `test_every_menu_box_fits_an_80_by_25_screen` refuses), Block's first group *Mark start/end/word/
  line* and *Go to block start/end*, Search's *Place marker* / *Go to marker* submenus (*Marker 1*-*9*; an unplaced one
  greyed, "Marker N is not placed"). The key column shows a WordStar set's ^K/^Q chord when it is in use. The default
  set itself stays modern (asked, twice). `test_every_editor_command_the_default_keys_leave_unbound_is_on_the_menu`
  holds it: a new command with no default key needs an entry, or a reason in its allow list.

## Tooltips

- `InfoLine.tooltip_at` says what a click on each place does, with its key: line:column (Go to line), the
  character's code (the table), the block indicator (stream/vertical); elsewhere the whole path.
- Greyed block, clipboard and undo commands say why (`FileEditor.refusal`, `EditWindow.refusal`).

## Read when

| Reference | Read when |
|---|---|
| `reference/editor.md` | the full design, and what is still not there |

## Closing hook

`EditWindow.after_close`, a plain callable (not an `on_*` handler), runs once after `close()`; Services uses it to
remove the empty drop-in directory F4 made for an override never saved (`navigator-services`).
