---
name: grosse-dateien
description: >
  Große und merkwürdige Dateien in zid (Binärdateien, Riesenzeilen, 5-MB-Dateien, Glyph-Batching, Spalten als Codepoints), E2E-Betrieb/Windows-Eigenheiten, plus die Use-after-free-Regel für Render-Commands (Segfault in hashText/renderText). Use when touching glyph_layout.zig, file_types.detectFileKind/looksBinary, ShapedRunCache/visibleSliceOf, renderText/renderExample/text_probe.zig, file_watcher_win.zig, conpty.zig, or scripts/e2e_odd_files.py, e2e_repro_text_uaf.py.
---

## Große und merkwürdige Dateien (Binärdateien, Riesenzeilen)

- `gpu_renderer.renderText` arbeitet mit Stack-Puffern von `glyph_layout.max_batch_glyphs` (256)
  Glyphen. `shapeTextInto` liefert für Runs über 256 Glyphen einen owned Heap-Slice beliebiger
  Länge; die Glyphen werden deshalb blockweise verarbeitet, die Stiftposition läuft über
  Blockgrenzen weiter (`glyph_layout.computeGlyphDevicePositions` gibt sie zurück, unit-getestet).
- Headless rendert keinen GPU-Text (`renderFrameWithText` läuft nur mit Fenster). Glyph-Logik
  nach `src/text/glyph_layout.zig` ziehen und dort unit-testen (`types.zig` importiert
  `platform/mod.zig` (wio), deshalb nimmt das Modul die Glyphen als `anytype`). Ob die
  Text-Strings der Render-Commands überhaupt noch gültig sind, prüft headless die Text-Probe
  (siehe „Use-after-free in Render-Commands“).
- **Binärdateien** öffnen keinen Buffer: `file_types.detectFileKind` (Endung zuerst, dann die ersten
  1024 Bytes durch `looksBinary`, Heuristik wie Zeds `analyze_byte_content`: bekannte Header,
  NUL-Anteil ≥ 1/16, sonst ≥ 8 % nicht textartige Bytes; unit-getestet) liefert `.binary`, der Tab
  zeigt nur `binary_view.zig` (Name, Größe). Bewusst ohne „Trotzdem öffnen“ (VS Code hat das, Zed
  nicht). UTF-16 gilt als binär, es gibt keinen Decoder. Bild/PDF entscheidet weiter die Endung.
  Eingaben auf einem Binär-Tab gehen wie bei Bild-Tabs an den Editor des vorherigen Buffers —
  bekanntes Verhalten (Tastatur-Fokus pro Tab-Art ist nicht umgesetzt).
- Textstücke über `ShapedRunCache.MAX_TEXT_LEN` (2048 Bytes) passen nicht in den Shape-Cache und
  gehen ungecacht über den Heap (`shapeTextInto` → `shapeText`); erst über `max_draw_run_bytes`
  (256 KiB, Schutz gegen kaputte Zeiger) werden sie verworfen, gezählt (`ui_state.text_runs_dropped`)
  und einmal geloggt. Der Editor gibt pro Zeile trotzdem nur den sichtbaren Spaltenausschnitt an Clay (`CodeEditor.visibleSliceOf`: ab
  `view.col`, `view.cols + 2` Spalten; `view.cols` kommt aus `visibleColCount` = Editor-Breite minus
  Gutter durch Zeichenbreite). Highlight-Tags, Auswahl und Cursor rechnen mit dem Byte-Offset des
  Ausschnitts. `View.clamp` (flow-core) zieht `view.col` dem Cursor nach; Shift+Mausrad bzw.
  `scroll_horizontal` scrollt Spalten (`scrollColumns`). RPC `editor_state` liefert `view_col`/`view_cols`.
- **Spalten sind Codepoints** (Tab = 4). `CodeEditor.metrics.egc_length` liefert die Länge der
  UTF-8-Sequenz bei einer Spalte; `cursor.col`, `view.col`, `find_ops`, `wrap_ops`,
  `renderRowOverlays` und die LSP-Positionen rechnen alle so. Bytes bekommt man nur über
  `get_line_width_to_pos` (Spalte → Byte) und `pos_to_width` (Byte → Spalte); tree-sitter-Edits
  (`pushEditForChange`) und die Highlight-Tags sind Byte-Offsets. Wer Bytes als Spalten zählt,
  zerschneidet UTF-8-Sequenzen (Cursor, Tippen, `visibleSliceOf`; Symptom `warning(shaper):
  invalid UTF-8 text`). Wer Metriken schreibt, muss
  `reparseFromBuffer` (flow-core) im Blick behalten: tree-sitter meldet Byte-Spalten, der
  Wrapper dort liest byteweise, unabhängig von der Spaltendefinition.
- `python3 scripts/e2e_odd_files.py` legt unter `tmp/` eine 3-KB-Binärdatei ohne Zeilenumbruch,
  eine 5000-Zeichen-Zeile und eine 5-MB-Datei an, öffnet sie headless, tippt und misst die Latenz
  bis das Zeichen in `editor_state` steht (gemessen 0,06 s bei der langen Zeile,
  1,2–2,4 s bei der 5-MB-Datei); die Binärdatei muss als Tab-Art `binary` ohne Buffer erscheinen. Logs mit Binärinhalt nur mit `grep -a` lesen, sonst schweigt grep.
- Der RPC-Socket bindet nur mit SO_REUSEADDR, nie mit SO_REUSEPORT (`Address.listen` mit
  `reuse_address` setzt beides). Sonst lauscht eine verwaiste Instanz weiter, der Kernel
  verteilt die Verbindungen, und ein Teil der RPC-Antworten kommt aus dem alten Prozess mit
  altem Zustand. Ein zweiter Start meldet `Port 9999 ist belegt`.
- E2E-Skripte starten zid nie über `zig build run`, sondern über `start_zid` aus
  `scripts/e2e_open_folder.py`: erst `zig build`, dann das Binary als direktes Kind. Bei `zig build
  run` ist zid ein Enkel, ein `kill` auf zig lässt zid auf dem Port zurück; Prozessgruppen
  (`start_new_session`/`killpg`) als Ausweg gibt es unter Windows nicht. `stop_zid` beendet per RPC,
  notfalls hart.
- **Nicht alle Suiten bauen selbst.** Nur wer `start_zid` nimmt, ruft vorher `zig build` auf.
  `e2e_scm_changes.py`, `e2e_scm_graph.py`, `e2e_timeline.py`, `e2e_git_diff.py`, `e2e_lsp.py`,
  `e2e_editor.py`, `e2e_picker.py` u. a. starten `zig-out/bin/zid` direkt: vor dem Lauf `zig build`,
  sonst testet die Suite still das alte Binary.
- **Suiten nacheinander, nie parallel** — auch nicht als zwei Hintergrund-Tasks. Alle nutzen
  Port 9999; ein zweiter Lauf redet mit der Instanz des ersten, und beide scheitern ohne
  erkennbaren Grund.
- **Zeitfehler erst messen, dann erklären.** Kommt ein Tooltip oder Toast zu spät, zuerst mit
  einem 100-ms-Polling-Probe die echte Dauer bestimmen, nicht am Timeout des Tests schrauben.
- **Fenster nur nach Rückfrage.** Auch Reproduktionen und Messungen laufen `--headless`. Braucht
  ein Befund zwingend ein Fenster (Present, Swapchain, DPI, Maximieren), das begründen und den
  User fragen oder ihn selbst starten lassen und das Log auswerten. Frame-Vergleiche per
  Screenshot-RPC zeigen kein Present-Flackern, das nur am Monitor sichtbar ist.
- **Meldungen aus dem Fenster am echten Dokument nachstellen.** „Funktioniert nicht" hat oft eine
  andere Ursache als vermutet. Die Datei des Users aus dem Log holen (die
  Ausgabe von `zig build run` zeigt geöffnete Pfade), headless öffnen, Zustand per RPC messen,
  notfalls in Zeilenbereiche schneiden, bevor eine Theorie entsteht. Ein Test muss den Effekt an
  dem prüfen, was der User sieht (Fliesstext), nicht nur an einem Sonderfall (Codeblock).
- Verwaiste Headless-Prozesse: Linux `pkill -f '[v]ulkan-ed --headless'` — ohne die Klammer trifft
  das Muster die eigene Shell, die den Befehl enthält. Windows: **nie** `taskkill /IM zid.exe` —
  das beendet auch die Fenster des Users samt ungespeicherter Änderungen.
  Nur Headless-Instanzen gezielt per PID:
  `Get-CimInstance Win32_Process -Filter "Name='zid.exe'" | ? CommandLine -match '--headless' |
  % { Stop-Process -Id $_.ProcessId -Force }`.
- **Windows:** Die Suiten laufen headless genauso (`python scripts/e2e_*.py`, kein Fenster).
  RPC-Antworten mit Pfaden immer über `std.json.fmt`/`Stringify` bauen, nie `"{s}"`: Backslashes
  ergeben sonst ungültiges JSON und jede Suite scheitert beim ersten `ui_state`. Die Text-Probe
  (memfd) und der Test auf unlesbare Dateien (`chmod 0`) greifen nur unter Linux; `e2e_symlink_dir.py`
  nimmt ohne Symlink-Recht eine Junction (`mklink /J`).
- **Explorer sortiert nicht:** Reihenfolge ist die des Dateisystems (ext4 Hash-Reihenfolge, NTFS
  alphabetisch). Tests navigieren deshalb per berechneter Anzahl ↑/↓ (`cursor_to` in
  `e2e_explorer.py`), nie mit fest angenommenen Nachbarn.
- **File-Watcher Windows** (`src/async/file_watcher_win.zig`): `ReadDirectoryChangesW` auf die
  Wurzel mit ganzem Baum, überlappende I/O mit Event (Stop-Flag alle 100 ms). Gleiche Ergebnisse
  und Filter wie Linux (versteckte Pfadteile, `zig-out`, `node_modules`, `.gguf`, 100-ms-Dedupe).
  Atomares Speichern (Rename) meldet `file_created`, nur Überschreiben `file_changed` — wie
  inotify. `src/async/file_watcher.zig` ist ein alter, nicht eingebundener Stub.
  `bWatchSubtree` folgt keinen Reparse-Points: der Watcher-Thread sucht deshalb nach dem Start
  Symlink-/Junction-Ordner mit Ziel außerhalb der Wurzel (`GetFileAttributesW`, denn
  `Dir.iterate` meldet sie als `.directory`) und öffnet je Ziel ein eigenes Handle (höchstens 63),
  Ereignisse kommen unter dem Link-Pfad; gewartet wird mit `WaitForMultipleObjects`. Ziele
  innerhalb braucht es nicht (realpath in `bufferKeyForPath`). Nicht abgedeckt: Links, die nach
  dem Start entstehen, und Links innerhalb eines Link-Ziels. E2E `e2e_external_change.py`.
- Testdaten der Suiten kommen aus `scripts/fixtures/` und `scripts/e2e_fixtures.py` (PDF, PNG
  werden erzeugt), nicht aus dem ignorierten `test_data/`. Git-Fixtures löscht
  `e2e_open_folder.rmtree` (setzt Rechte auf `.git/objects`, sonst bleibt das Fixture unter
  Windows still stehen); die Suiten stellen stdout auf UTF-8 (Pfeile in Meldungen).
- **Zeilenenden:** Git for Windows setzt systemweit `core.autocrlf=true`. Neue Git-Fixtures in
  Zig-Tests und Suiten setzen `core.autocrlf false`, Python-Suiten schreiben Dateien mit
  `newline="\n"`.
- Umgebungsvariablen nur über `src/platform/env.zig` lesen, nie `std.posix.getenv` — das gibt
  es unter Windows nicht, und der Windows-Build bricht still, weil hauptsächlich unter Linux
  entwickelt wird. Bei neuen Windows-Buildfehlern zuerst `zig version` (muss 0.15.x sein) und
  die MuPDF-Archive prüfen, bevor Code angefasst wird (README, Abschnitt Windows).
- Ein langsamer Test lässt sich unter Windows nicht mit `timeout` aus Git Bash begrenzen (dort
  teils gesperrt, `Permission denied`); Runner in Python mit `subprocess.run(timeout=)`.
- **Terminal unter Windows (ConPTY, `src/terminal/conpty.zig`):** die Shell (`cmd.exe` aus
  COMSPEC) startet mit `STARTF_USESTDHANDLES` und leeren Std-Handles. Ohne das erbte sie zids
  stdout, sobald der umgeleitet war (Log-Datei der E2E, Pipe), schrieb Prompt und Ausgabe dorthin
  und der Terminal-Tab blieb leer. `terminal_state.screen` zeigt den Bildschirmtext; Suiten
  nehmen unter Windows cmd-Befehle (`for /L`), kein `seq`.
- Windows-Build der Engine: clang + ninja, `-DGGML_VULKAN=OFF`, dazu
  `-D_WIN32_WINNT=0x0A00` in C- und CXX-Flags (cpp-httplib verlangt Windows 10).
- Pfade in Git-Status (`/`) und LSP-URIs (`file:///C:/…`) werden auf Windows-Trenner umgesetzt
  (`updateGitStatus`, `lsp_proto.pathToUri`/`uriToPath`). Dasselbe gilt für die Repo-Wurzel aus
  `git rev-parse --show-toplevel`: `git_worker.repoRoot` setzt sie um, bevor sie in Timeline- und
  Graph-Antworten geht — sonst stimmt kein Vergleich gegen einen Editor-Pfad.

## Use-after-free in Render-Commands (Segfault in `hashText`/`renderText`)

- **Frame-Regel:** Die Render-Commands aus `renderExample` zeigen auf fremden Speicher
  (Explorer-Knotennamen, Tab-Namen, Dialog-Nachricht, Frame-Arena). Der GPU-Renderer liest sie
  erst *nach* `renderExample`. Nichts, worauf sie zeigen, darf zwischen `endLayout` und dem
  nächsten `renderExample` freigegeben werden — „nach endLayout“ ist **nicht** sicher.
  Aufräumen gehört vor das nächste Layout: `UI.update`, `processPending`, oder der Anfang
  von `renderExample` (`applyPendingDialogResult`).
- `applyDeferredLayoutActions` läuft am Anfang von `renderExample` und wendet an, was das
  vorige Layout angefordert hat: Dialog-Klick/Enter (`pending_dialog_result`),
  `pending_split`, `pending_tab_closes`, leere Panes. Direkt nach `endLayout` würden
  Dialog-Nachricht, Knotennamen (`loadDirectory`) und Tab-Namen freigegeben, während der Frame
  noch gezeichnet wird → `Segmentation fault` in `text_system.hashText`.
- Kein `clay.text(&.{byte}, …)`: Zeiger auf ein Stack-Temporary, beim Zeichnen längst
  überschrieben. Statische Literale nehmen (Git-Status-Buchstaben in `renderTreeEntry`).
- Dasselbe für `var buf: [N]u8 = undefined` in einer `render`-Funktion mit `bufPrint` → `clay.text`:
  der Puffer gehört in die Frame-Arena (`arena.alloc(u8, N)`) oder das Ergebnis wird `arena.dupe`d.
  Symptom im Fenster (Debug-Build): der Text besteht aus 0xAA-Bytes (Zigs `undefined`-Muster,
  ein späterer Stack-Frame hat den Puffer neu initialisiert), im Log `warning(shaper): invalid
  UTF-8 text … hex=aaaa…`, gezeichnet als lauter U+FFFD. Headless zeigt das nicht (kein
  GPU-Text; der memfd-Probe prüft nur Mapping, nicht Inhalt). `SimpleShaper.shape` dekodiert
  verlustbehaftet, und `renderClayLayout`-Fehler werden als `warning(rendering)` gemeldet, statt
  den Frame abzubrechen.
- `Platform.setCursor` meldet nur Formwechsel an wio: unter Windows macht wio je Aufruf
  `GetCursorPos`+`SetCursorPos`, und bei gedrückter Maustaste erzeugt das ein `WM_MOUSEMOVE`, das
  den nächsten Frame weckt, und der Loop liefe beim Ziehen ohne Pause. Die Debug-Zeilen `mouse:` (main.zig, nur beim Ziehen),
  `splitter:` (Breite vorher/nachher) und `cursor:` (Formwechsel) bleiben für solche Diagnosen.
- **Werkzeug:** Headless fasst jeden Text-Command per `pwrite` in ein memfd an
  (`src/debug/text_probe.zig`; `/dev/null` liest den Puffer nicht, EFAULT bleibt aus). Zeigt ein
  Command auf unmapped Speicher, panict der Loop mit Command-Index, Bounding-Box und dem
  vorigen Text. Mit `--page-alloc` oder `ZID_PAGE_ALLOC=1` läuft alles über
  `src/debug/free_log.zig` (page_allocator: jede Freigabe = munmap, kein In-Place-Remap) und
  die Meldung enthält den Stack-Trace der Freigabe. So laufen lassen:
  `ZID_PAGE_ALLOC=1 python3 scripts/e2e_explorer.py` (jede E2E-Suite geht) oder
  `python3 scripts/e2e_repro_text_uaf.py --page-alloc` (Ordnerwechsel in einen erzeugten Baum
  unter `tmp/e2e_uaf`, Bilder, Tooltip, Picker-Klicks, Tab-Schließen). Der GPA unmappt kleine Buckets erst, wenn sie ganz leer sind,
  darum fällt der Fehler im Fenster nur sporadisch auf.
