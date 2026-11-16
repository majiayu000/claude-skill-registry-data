---
name: dn-porting
description: Recreating a DOS Navigator feature faithfully -- finding it in the original Pascal source (~/development/Dos-Navigator, DN.DNR/DN.DNL in CP437), naming commands and widgets after DN's cm*/T* identifiers, transcribing dialogs and menus, and recording a departure from the original. Use before implementing any feature that DOS Navigator had, or deciding whether to diverge from it.
---

# Porting from DOS Navigator

Navigator is a faithful recreation of DOS Navigator for modern POSIX terminals. **Prefer recreating original behaviour
over inventing modern alternatives when the two conflict** -- fidelity is the point of the project.

## Where the original is

- The DN source tree is at `~/development/Dos-Navigator`. `RESOURCE/ENGLISH/DN.DNR` (dialogs, menus, the Colors table)
  and `DN.DNL` are **CP437**: decode before grepping (`iconv -f CP437 -t UTF-8`, or Python `open(..., encoding="cp437")`).
- Useful sources: `FVIEWER.PAS` (viewer), `MICROED.PAS` (editor), `FILECOPY.PAS` (copy/move), `ERASER.PAS` (erase),
  `DBLWND.PAS` (the two-panel window, `SwitchView`), `CMDLINE.PAS` (command line), `DNAPP.PAS` (desktop: Tile, Cascade),
  `dlgMainMenu` / `dlgEditorMenu` / `dlg*` resources in `DN.DNR`.
- Midnight Commander is the tie-breaker for things DN never had (type marks, quick search, `+`/`-`/`*` rules).

## How a port is written

- **DN's Help buttons are back** (`navigator-help` skill, *Giving a dialog its help*): every dialog whose DN
  resource has `cmHelp` shows *Help*, `command: Help`, and names its page with `help_topic`. A newly ported dialog
  gets both with its page; one whose resource has none (Filter) gets the topic alone.
- **Name things after the original.** A command class is named for DN's `cm*` (and its docstring says so); a widget is
  the `T*` it recreates (`FileViewer` is `TFileViewer`, `EditWindow` is `TEditWindow`); a dialog document transcribes
  the `dlg*` resource's layout and captions; key handlers say which DN key constant they took (`kbIns`, `kbBack`).
- **Menus transcribe DN's**: `main_menu.nml` is `dlgMainMenu`, with every entry whose feature does not exist greyed rather
  than removed. **The exception is an entry that can never have a POSIX meaning** (video modes, Format disk, the modem,
  the CD player, FAT undelete, DOS archivers, `descript.ion` -- with it Ctrl+K's descriptions and the information
  panel's per-file one, `ReadInfoBBS`): it is dropped, and the document's `#:` header lists it as
  a departure. The same applies to settings and key-bar commands. An entry with a POSIX reading is kept or relabelled
  instead: *Edit environment*, *Character table*, *Encoding...*, and *Change drive left/right*, which are *Bookmarks left/right* (`navigator-bookmarks`).
- **Colours come from DN's slots** (see `colours-themes-glyphs`); a new colour is a `DERIVED` alias, not an invented value.
- **A departure is recorded, never silent.** Say "a departure" in the code comment or `#:` doc and give the reason; a
  colour departure goes in `palconv.py`'s `DEPARTURES`. Examples already taken: the user's shell prompt on the command
  line, the Owner column, byte-exact editor saves, Gray keys typing while the line has text, *Recursive delete*,
  Linux file attributes, symlinks on Shift+F5, F3 closing the viewer, `navigator.ini` in place of `DN.CFG`, the
  editor's and viewer's option strip on the bottom frame, *Hidden characters*, File > *Compare files* and *Compare
  directories*' *Window, recursive* (`navigator-compare`), Split/combine by size into `.001` parts with a Total Commander `.crc`
  and no key (`navigator-file-ops`).
- **The one standing modern exception is the Nerd Font icon gutter** in `Panel`; don't re-litigate it and don't read it
  as licence for the next flourish.
- When DN defined something but never used it (the tree window), or the 1.51 source lacks a handler (Alt+letter quick
  search), say which choice was made and why.

## Where the notes go

A feature's rules go in its skill's `SKILL.md`; the longer rationale goes in that skill's `reference/`, and its heading
is added to the index in `navml/DESIGN.md` or `navkit/DESIGN.md`.
