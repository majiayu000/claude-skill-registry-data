---
name: editor
description: >
  Der Text-Editor in zid: Bearbeiten/Auto-Indent/Autoclose, Maus, Mehrfach-Cursor, Word-Wrap, Suche/Ersetzen, Statusleiste, Panes, externe Änderungen, Kodierung (Windows-1252 laden/speichern) — und die zwei Sorten Textfelder (CodeEditor vs. line_edit). Use when touching src/editor/*, flow-core Buffer load/store or unicode.zig, file encodings, edit_ops.zig, wrap_ops.zig, find_ops.zig, find_bar.zig, tiny_regex.zig, code_editor.zig (own test root code_editor_tests), keymap.zig, CodeEditor/line_edit/EditBuffer, or scripts/e2e_editor.py, e2e_find_preview.py, e2e_external_change.py, e2e_line_edit.py, e2e_encoding.py.
---

## Unit-Tests in code_editor.zig

Tests in `src/editor/code_editor.zig` laufen nur, weil die Datei eigenes Test-Root ist
(`code_editor_tests` in build.zig, wio-Symbol-Hack unter `is_test` in der Datei). Tests in
importierten Modulen führt der Runner nicht aus; `zig build test --summary all` zeigt die
Zähler pro Modul, ein absichtlich kaputter Test ist der schnellste Beweis.

## Editor: Bearbeiten, Maus, Statusleiste, Panes

- Reine Textlogik in `src/editor/edit_ops.zig` (unit-getestet): Auto-Indent (`newlineInsertion`:
  Einrückung übernehmen, nach `{([` eine Stufe mehr, `{}`-Paar aufspannen), Autoclose-Regeln
  (`autoclosePolicy`: Paar, drüberspringen, neben Wortzeichen normal; `deletesPair` für Backspace),
  Ein-/Ausrücken, Kommentar umschalten (`commentPrefixForPath` je Endung, Markdown/HTML keins),
  `languageNameForPath`, `wordAt`, `looksLikeDefinition`. Der Editor wendet sie in `dispatchAction`
  an (Actions IndentLines/OutdentLines/ToggleComment/MoveLineUp/Down/DuplicateLine/GotoLine/Replace/
  GotoDefinition; Keymap Shift+Tab, Ctrl+/, Alt+↑/↓, Ctrl+Shift+D, Ctrl+G, Ctrl+H, F12; Tab mit
  mehrzeiliger Auswahl rückt ein). Zeilenoperationen laufen über `replaceLineSpan`.
- **Ctrl+X ohne Auswahl schneidet die ganze Zeile aus** (VS Code, Zed): Zeile plus Umbruch in
  die Zwischenablage, dann `DeleteLine`. Mit Auswahl bleibt Cut wie gehabt.
- **Metrik:** `insert_chars` addiert die Chunk-Breite aus `egc_chunk_width` zur Cursor-Spalte;
  die muss die echte Breite liefern, sonst steht der Cursor nach Einfügen/Autoclose falsch.
- **Undo-Schritte und Undo-Cursor:** `snapshotForUndo` legt die Cursor-Position (`zeile:spalte`)
  als Metadaten in den flow-core-Undo-Stand; `afterUndoRedo` setzt den Cursor dorthin (begrenzt)
  statt an den Dateianfang und nimmt den Geändert-Status aus `Buffer.is_dirty()`. Eine Tipp-Gruppe
  endet, wenn der Cursor nicht mehr hinter dem zuletzt getippten Zeichen steht (`typing_end`), und
  beim Speichern (`markSaved`): nur dann ist der root des nächsten Undo-Stands `last_save`, und
  Undo zurück dorthin macht den Tab sauber.
- **Cursor-Spalte nach Tippen kommt aus `insert_chars`** (`result[1]`), nie aus der Byte-Länge: ein
  Umlaut ist 2 Bytes, aber 1 Spalte; mit Byte-Länge landet der Cursor hinter dem Zeilenende und
  jede weitere Eingabe scheitert still (`INSERT FAILED`).
- **Anzeige im Editor** (`renderRowOverlays`, schwebende Elemente über dem Zeilentext, x = Spalte ×
  `charWidth`): Einrück-Guides je 4 Spalten führenden Whitespace, Whitespace-Punkte/Tab-Striche
  (`show_whitespace`, Standard aus), Klammerpaar am Cursor (`findBracketPair`, max. 2000 Zeilen,
  pro Frame; Rahmen um beide Klammern; RPC `editor_state.bracket_pair`). Minimap rechts
  (`renderMinimap`, 2 px je Zeile, Fenster um den Viewport, Klick springt) und horizontale Scrollbar
  unten (`renderHScrollbar`, nur wenn eine sichtbare Zeile breiter als der Ausschnitt ist). View →
  Toggle Minimap / Render Whitespace / Indent Guides (gemerkt in `user_state`).
- **Kodierung:** Dateien ohne gültiges UTF-8 lädt flow-core als Windows-1252
  (`unicode.cp1252_decode`, Flag `Buffer.file_utf8_sanitized`) und speichert sie wieder so
  (`store_to_file_const` → `cp1252_encode`). Jedes Byte ist ein Zeichen, unveränderte Bytes
  bleiben exakt. Ein Zeichen außerhalb von 1252 lässt das Speichern mit
  `error.NotInWindows1252` scheitern; Datei unverändert, Meldung im Editor, Tab-Schließen bleibt
  offen, Autosave wartet auf die nächste Änderung (`save_failed_edit_ms`). Der Watcher vergleicht
  über `Buffer.matches_file_bytes` in der Kodierung der Datei, sonst lüde jeder eigene Save neu
  und verwürfe Undo; er zählt auch den zuletzt gespeicherten Stand als eigen, weil sein
  Ereignis verspätet kommt, wenn schon weitergetippt wurde. Statusleiste „Windows 1252“ wie
  VS Code. Umwandeln nach UTF-8 nur bewusst: Command Palette „Save with Encoding: UTF-8“
  (`save_as_utf8`, `UI.saveAsUtf8`). Alle anderen Schreibwege halten die Kodierung der Datei
  ebenso: Ersetzen im Projekt (`replaceInFile` kodiert den Ersatz, Trefferliste dekodiert zur
  Anzeige) und die Agent-Werkzeuge (`decodeFile`/`encodeFor` in `agent_actions.zig`). E2E
  `python3 scripts/e2e_encoding.py`.
- **Backup vor dem Speichern** löst relative Pfade per `realpathAlloc` auf, weil `accessAbsolute`
  bei relativen Pfaden in `unreachable` läuft.
- **Suchleiste** (`CodeEditor.find` = `find_bar.FindState`, Leiste `find_bar.render`, gemeinsam
  mit der Markdown-Vorschau; Logik in `src/editor/find_ops.zig`): inkrementell beim Tippen,
  Enter/Shift+Enter weiter/zurück mit Umbruch, Escape schließt, markierter Text wird Suchbegriff.
  Ctrl+F bei offener Leiste markiert den Begriff neu. Die Widget-IDs (`find_widget`,
  `find_input`, `replace_*`, `goto_*`) tragen das Editor-Salz (`idi`), sonst melden zwei Panes
  mit offener Leiste duplicate_id. Breitzeichen zählen als eine Spalte.
  E2E: `python3 scripts/e2e_find_preview.py` (Vorschau, Editor-Tab, Split).
- Suchleiste: Ctrl+H zeigt die Ersetzen-Zeile, Tab wechselt das Feld, Enter ersetzt den Treffer,
  Alt+Enter alle (`replaceAll`, ein Undo-Schritt). Ctrl+G öffnet „Go to line“ (nur Ziffern).
- **Suche:** Optionen Alt+C (Groß/Klein), Alt+W (Ganzwort), Alt+R (Regex) in der Suchleiste, Badges
  „Aa W .*“. Regex-Engine `src/editor/tiny_regex.zig` (Backtracking: Literale, `.`, `* + ?`, Klassen,
  `^ $`, `\d \w \s \b`, Gruppen, `|`; keine Rückverweise/Captures, keine lazy Quantoren; unit-getestet).
  `find_ops.findOpts` rechnet Spalten als Anzeigespalten (Tab = 4) und nimmt das Trefferende aus dem
  Treffer, nicht aus der Musterlänge. Der erste Tastendruck nach Ctrl+F ersetzt den alten Begriff
  (`replace_on_type`). Watcher: identische Ereignisse werden nur innerhalb von 100 ms
  zusammengefasst, damit eine zweite externe Änderung derselben Datei nicht verloren geht.
- Maus: Dreifachklick markiert die Zeile (`click_count`), Shift+Klick erweitert vom Anker, Ctrl+Klick/
  F12 springen zur ersten Definitionszeile des Worts im selben Buffer (kein LSP: der Client in
  `src/lsp` wird nirgends gestartet), Ziehen über den Rand scrollt (`autoScrollWhileDragging` im Render).
- Statusleiste (oben, neben dem Branch): `UI.statusText` — Ln/Col, Auswahl, LF/CRLF, Kodierung,
  Sprache, „Spaces: 4“; RPC `ui_state.status_text`.
- Datei außerhalb geändert: Watcher-`file_changed` oder `file_created` (atomares Ersetzen per
  rename meldet IN_MOVED_TO) → `UI.handleExternalChange`: gleicher Inhalt (eigener Save)
  ignoriert, ungeänderter Buffer wird still neu geladen, geänderter fragt („File Changed“:
  Reload / Keep Mine). Symlink-Ordner: der Linux-Watcher steigt auch in Link-Ordner ab (inotify
  folgt dem Link; schon bekannter Watch-Deskriptor = kein zweiter Abstieg), und
  `bufferKeyForPath` findet den Buffer notfalls über realpath, weil Ereignis- und Öffnungspfad
  verschiedene Schreibweisen derselben Datei sein können. E2E:
  `python3 scripts/e2e_external_change.py` (in-place, atomic, Symlink im und außerhalb des
  Projekts). Unter Windows nimmt die Suite ohne Symlink-Recht Junctions und schreibt LF
  (`newline="\n"`; im Textmodus käme CRLF und schon der Ausgangsvergleich schlüge fehl).
- Panes: Ctrl+\ splittet, Ctrl+Alt+Pfeil oder Chord Ctrl+K dann Pfeil wechselt geometrisch
  (`focusPane` über die Pane-Bounds des letzten Frames), Ctrl+Shift+E fokussiert den Explorer,
  Ctrl+J wechselt zum Terminal-Tab und zurück (`terminal_return_index`). Ctrl+K erreicht die Shell
  im Terminal nicht.
- RPCs: `key_press_alt(name, ctrl, shift, alt)`, `click_mods(x, y, ctrl, shift)`, `editor_state.selection`,
  `ui_state.active_pane_index`. `python3 scripts/e2e_editor.py` deckt alles ab.
- **Mehrfach-Cursor:** Ctrl+D markiert das Wort unter dem Cursor, jedes weitere Ctrl+D fügt das
  nächste Vorkommen als `ExtraCursor` (Cursor + Anker) hinzu (`selectNextOccurrence`); Ctrl+Alt+↑/↓
  setzt Cursor in der Nachbarzeile (`addCursorVertical`). `dispatchAction`/`handleChar` sind Wrapper:
  mit Extra-Cursorn läuft `forEachCursor` über alle Cursor von unten nach oben (`dispatchSingle`/
  `handleCharSingle` je Cursor, `in_multi` verhindert Snapshots pro Cursor, ein Undo-Schritt für
  alle). Schon bearbeitete Cursor derselben Zeile werden um die Breitenänderung verschoben, tiefere
  um die Zeilenänderung; sonst zeigte `prevCharBoundary` hinter das Zeilenende. Escape/Klick/Enter
  lösen auf (`multiSafe` listet, was mit mehreren Cursorn erlaubt ist). RPC `editor_state.cursors`.
- **Word-Wrap (Alt+Z, View → Toggle Word Wrap, gemerkt in `user_state`):** Soft-Wrap in
  `src/editor/wrap_ops.zig` (unit-getestet): Segmente von `wrapCols()` Anzeigespalten (sichtbare
  Spalten minus Minimap minus 1; Codepoint = 1, Tab = 4), Bruch hinter dem letzten Whitespace,
  sonst hart. Der Renderer zeichnet je Buffer-Zeile ein Segment pro Reihe (`renderLine` bekommt
  Segment, Startspalte und `is_last`; Cursor/Auswahl/Overlays werden auf das Segment geklemmt),
  Fortsetzungsreihen ohne Zeilennummer und mit eigenen Clay-IDs (`roww/gutterw/codew` je sichtbarer
  Reihe; das erste Segment behält `row/gutter/code` je Buffer-Zeile für `element_bounds_i`).
  Maus: `hitRow` findet Zeile + Segmentanfang, `colFromX` misst ab dort. `ensureCursorVisible`
  setzt `view.col = 0`, `view.cols` riesig und rückt `view.row` vor, bis die Reihen bis zum Cursor
  passen. Bewusst einfach: Cursor ↑/↓ und Scrollen arbeiten in Buffer-Zeilen, nicht in Reihen
  (VS Code bewegt sich reihenweise); horizontale Scrollbar und Shift+Mausrad sind aus. Die
  Obergrenze fürs Scrollen ist `maxViewRow`: sie summiert bei Wrap die Reihen von hinten, bis der
  Schirm voll ist; Zeilen minus sichtbare Zeilen ließe das Dateiende unerreichbar. Rad, Leiste
  (Daumen über `totalVisualRows`) und Ziehen benutzen sie.
  RPC `editor_state.word_wrap`, `editor_state.visual_rows` (Reihen der Cursor-Zeile).
- **Neue Editoren erben Optionen:** `splitActivePane` kopiert Minimap/Whitespace/Guides/Wrap,
  Schriftgröße und Theme vom Ausgangs-Editor (`copyEditorOptions`), weil `loadUserState` nur die
  beim Start vorhandenen Leaves erreicht.
- **Clay `getElementData` vergisst nichts:** IDs, die nicht mehr gerendert werden, bleiben `found`
  mit alter Geometrie. E2E-Prüfungen auf „Element ist weg“ sind wertlos; Zustand per RPC prüfen.
  Für ausgeblendete Kontextmenü-Einträge geht es trotzdem: der Eintrag muss innerhalb des frisch
  gezeichneten `<prefix>_container` liegen (`menu_entry_visible` in `scripts/e2e_marp_pdf.py`).
- **E2E nie mit der echten Konfiguration:** `start_zid` in `scripts/e2e_open_folder.py` setzt ohne
  eigenes `env` frische `XDG_CONFIG_HOME`/`XDG_DATA_HOME` unter `tmp/e2e_env/<log-name>`. Mit
  `~/.config/zid/state` (Word-Wrap, Schriftgröße, Sidebar-Breite) messen Suiten Fremdzustand und
  überschreiben ihn. Neue Suiten starten zid deshalb über `start_zid`, nie per `Popen`.
- **Split behält Chat und Terminal:** `splitActivePane` gibt die bisherige Tab-Leiste an die
  erste Hälfte weiter, nur die neue Hälfte bekommt `cloneFrom` (ohne Chat und Terminal), sonst
  verschwinden Chat-Tabs und Terminal-Instanzen. E2E: `e2e_tabs.py`.
- **setText verwirft den Undo-Verlauf.** `libs/flow-core` gibt in `Buffer.load` die Leaf-Puffer des
  vorherigen Ladevorgangs frei (Leak-Fix gegenüber upstream flow), auf deren Bäume alle
  Undo-/Redo-Knoten zeigen (sonst „switch on corrupt value“ in
  `walk_from_line_begin_const_internal`). `CodeEditor.setText` setzt deshalb
  `undo_head`/`redo_head` auf null, beendet die Tipp-Gruppe und löscht Extra-Cursor; Undo über
  einen Reload hinweg gibt es bewusst nicht.

## Textfelder: zwei Sorten, klar getrennt

- **Mehrzeilig → `CodeEditor`**: Haupteditor, KI-Chat-Eingabe und das Commit-Feld der
  Source-Control-Ansicht. Damit gibt es dort Umbruch, Rückgängig, Mausauswahl,
  Kontextmenü und unbegrenzte Länge.
- **Einzeilig → `line_edit` + `explorer_ops.EditBuffer`**: Umbenennen und Filter im
  Explorer, Schnellöffner, Ordner-Dialog. Klein gehalten, kein Umbruch
  (`wrap_mode = .none`). Rückgängig gibt es dort nur **einen** Schritt
  (`undoEdit`/`redoEdit`): zusammenhängendes Tippen ist eine Gruppe, eine Cursorbewegung
  schliesst sie. Doppelklick markiert das Wort (`selectWordAtCursor`); die Zeit dafür kommt
  aus `std.time.milliTimestamp`, damit die Aufrufer keine Uhr durchreichen müssen.
- **`line_edit` in einem Dialog braucht `Config.z_index` über dem Dialog.** Cursorstrich
  und Markierung sind schwebende Elemente, und Clay sortiert z-Indizes global, nicht relativ
  zum Elternteil. Mit dem Standard 10 liegen sie unter Ordner-Dialog und Picker (z 2000);
  beide Felder stehen deshalb auf 2002. E2E prüft das Pixel am Cursor in `e2e_open_folder.py`.
- **`line_edit` scrollt waagrecht:** `EditBuffer.scroll_x` folgt dem
  Cursor (`explorer_ops.followCaret`, unit-getestet), das Textelement ist selbst ein
  Clip-Container mit `child_offset`, Markierung und Strich ziehen den Versatz selbst ab
  (Clay versetzt schwebende Kinder nicht) und hängen mit `clip_to = .to_attached_parent`
  am Feld; Klick und Ziehen rechnen `scroll_x` ein. Der
  Rahmen um das Feld darf **kein** `.clip` haben: Clay zieht `grow`-Kinder eines
  Clip-Elternteils auf Inhaltsbreite, das Feld wuchs dann mit dem Text mit. E2E: Schritt 2b
  in `e2e_open_folder.py`.
- Jeder eingebettete `CodeEditor` braucht die Modifier: `UI.setCtrlState`/`setAltState`/
  `setShiftState` reichen sie an Chat **und** Commit-Feld weiter. Ohne das greift die
  Keymap des Editors nicht und Ctrl+Z tut nichts.
- Ebenso Uhr und Zwischenablage: `time_ms` bekommt in `UI.update` der aktive Editor, der Chat
  (`updateTimeMs`) und das Commit-Feld; ohne Uhr gilt jeder zweite Klick in dieselbe Zeile als
  Doppelklick. Copy/Cut/Paste laufen über `clipboard_hook` (gesetzt in `ensureEditorHooks` für
  Panes, Chat und Commit-Feld) → `UI.setClipboard`, damit auch headless etwas ankommt. Neuer
  eingebetteter Editor: beides mitverdrahten.
- Die Auswahl eines `CodeEditor` hat kein eigenes Clay-Element (anders als `line_edit`,
  `<feld>_sel`). E2E prüfen den Text: `scm_state.changes.selected_text`, `editor_state.selection`.
