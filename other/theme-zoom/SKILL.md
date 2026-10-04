---
name: theme-zoom
description: >
  Theme-Umschaltung, Zoom/Schriftgröße, Autosave, Backups, Toasts, Beenden-Dialog bei ungespeicherten Buffern und Menü-Tastatur in zid. Use when touching toggle_theme/UI.theme, zoom_in/out/reset/setFontSizeAll, UI.autosave, src/editor/backup.zig, UI.showToast, UI.requestQuit/markLoaded, GlyphCache, or scripts/e2e_ui_misc.py, e2e_quit_unsaved.py.
---

## Theme, Zoom, Autosave, Toasts, Menü-Tastatur

- **Theme:** `toggle_theme` (View, Palette) schaltet `UI.theme` zwischen `Theme.light()`/`dark()`;
  Editor-Farben kommen aus `CodeEditor.applyTheme` (bg, gutter, Zeilennummern, Cursor, Auswahl,
  `text_color`). `--theme light|dark` gilt einmalig beim Start; das Theme nie pro Frame setzen,
  sonst greift kein Umschalter.
- **Zoom:** Ctrl+=/Ctrl+-/Ctrl+0 (`zoom_in/out/reset`, 10–48, `setFontSizeAll` für alle Panes).
  Klein gezoomt zeichnet der Editor mehr Reihen; das Layout selbst darf dabei nie wachsen
  (Minimap-Rückkopplung, siehe Skill `clay-layout`; `python3 scripts/e2e_layout_stable.py`).
  Der Glyph-Cache (4096 Einträge, je Größe × 4 Subpixel-Varianten) leert sich komplett, wenn er
  voll ist (`GlyphCache.ensureFreeSlot`), statt neue Glyphen jeden Frame neu zu rastern.
- **Fenster schließen fragt nach:** wio `.close` beendet nicht selbst (`platform/mod.zig`), sondern
  ruft `UI.requestQuit`. Ohne ungespeicherte Buffer (`Buffer.is_dirty()` über `open_buffers`)
  setzt es `quit_confirmed`, sonst Dialog „Unsaved Changes“ (Save All / Don't Save / Cancel);
  Save All legt wie `save()` eine Sicherung an und bricht beim ersten Speicherfehler ab, ohne zu
  beenden. Der Main-Loop endet über `quit_confirmed`. RPC `request_quit` stellt den
  Schließen-Knopf nach, E2E `python3 scripts/e2e_quit_unsaved.py`.
  **Nach dem Laden `UI.markLoaded`, nie nur `last_save = root`:** `is_dirty` vergleicht auch
  `last_save_eol_mode` (Vorgabe LF) mit dem erkannten `file_eol_mode`; ohne `markLoaded` gilt
  jede CRLF-Datei ab dem Öffnen als geändert. Das gilt auch für den Fallback- bzw.
  Scratch-Buffer. `main.zig` erkennt ein Ordner-Argument (`zid .`) per `openDir` (`statFile`
  öffnet unter Windows als Datei und meldet bei Ordnern IsDir, nie `.directory`) und nimmt es
  als Projektordner statt der cwd. E2E-Fall 1b in `e2e_quit_unsaved.py`.
- **Autosave:** File → Toggle Autosave (`UI.autosave`), speichert 1 s nach der letzten Änderung
  (`CodeEditor.last_edit_ms`) nur Text-Tabs mit Pfad. Jedes Speichern legt vorher eine Sicherung
  unter `$XDG_DATA_HOME/zid/backup/<name>.<hash>.bak` ab (`src/editor/backup.zig`, eine je
  Datei, wird ersetzt). CRLF-Dateien bleiben CRLF (`file_eol_mode`, Test im Editor).
- **Gemerkt** (`user_state`): `theme`, `font_size`, `autosave` zusätzlich zu Breite/Hidden.
- **Toasts:** `UI.showToast` (3 s, unten rechts, max. 4): „Saved x“ (`CodeEditor.takeSaved`),
  „Moved to trash: x“ (`FileExplorerState.takeInfo`), „Font size n“, „Autosave on/off“.
  RPC `ui_state.toast` liefert den jüngsten Text.
- **Menü per Tastatur:** Alt+F/E/V/H öffnet, ←/→ wechselt, ↑/↓ markiert (`menu_highlight`),
  Enter führt aus, Escape schließt. **Kürzel-Dialog** scrollt (Mausrad, ↑/↓; `shortcuts_scroll_y`,
  Inhalt `sc_content` in einem 520-px-Clip).
- **503 beim Warmup:** `agent.zig` liefert `error.ServerLoading` (debug-Log) statt `Llama Server
  Error: 503` im Fehler-Log; die Warmup-Schleife wiederholt, der Chat zeigt „initializing“.
- `python3 scripts/e2e_ui_misc.py` deckt Theme, Zoom, Autosave, Toast, Backup, Menü-Tastatur und
  Dialog-Scroll ab.
