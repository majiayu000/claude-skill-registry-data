---
name: e2e-rpc
description: >
  E2E-Steuerung von zid über den RPC-Port 9999 und den Interactive-Modus: RPC-Referenz (key_press, ui_state, editor_state, element_bounds, get_active_tab, explorer_open), Screenshot-Koordinaten, Threading der Handler (gepuffert, onMain, Sperren), Fixtures. Use when writing or debugging scripts/e2e_*.py, adding or changing an RPC in src/e2e_server.zig, drainInputs/serviceScreenshot/onMain, --headless/--interactive, or when a test flakes on timing or thread races.
---

# E2E über RPC

## Headless-Betrieb

- `--headless --ai=off` führt denselben Frame-Loop aus wie das Fenster (Tab-Wechsel,
  Explorer-Klicks, Tab-Schließen, gepufferte Eingaben, Screenshots), nur ohne Fenster-Events,
  Cursor und Präsentation. Tests brauchen deshalb nie `--e2e` mit Fenster; das stört den User.
- Die UI-Uhr (`ui_time_ms`, Tooltips nach 700 ms, Toasts, Hover) läuft mit der echten Zeit
  zwischen zwei Frames (Deckel 250 ms). Ein Headless-Frame mit Layout und RPC dauert ~35 ms;
  Tests, die auf Zeit warten, rechnen deshalb in Echtzeit, nicht in Frames.
- Screenshot: `./tmp/vulkan-screenshot.ppm`, per RPC
  `echo '{"jsonrpc":"2.0","method":"screenshot","id":1}' | nc --send-only localhost 9999`.
- Headless-Screenshot ist 1200x800, Tab-Kopf liegt bei y≈105, Inhalt ab y≈130.
- Der SVG-Atlas rasterisiert max. 4 neue Icons pro Render-Durchgang; neue Icons erscheinen
  erst im zweiten Screenshot (Skripte rendern zweimal).

## Interactive-Modus (stdin/stdout)

`zig build run -- --interactive`, zeilenbasiert; Handler wirken direkt, es gibt keinen Loop.

```bash
open <path>           # Datei in neuem Tab
close-tab <n>         # Tab nach Index schließen
switch-tab <n>        # zu Tab wechseln
click <x> <y>         # Mausklick
key <name> [ctrl]     # Taste (enter, backspace, k, …)
type <text>           # Text tippen
screenshot            # -> ./tmp/vulkan-screenshot.ppm
split <h|v>           # teilen
get-state             # Zustand als JSON
shutdown              # beenden

echo -e "open ./README.md\nget-state\nshutdown" | zig build run -- --interactive
```

## Threading der RPC-Handler

- Handler laufen im Server-Thread. `click`, `right_click`, `move_mouse`, `key_press`,
  `type_text` und `screenshot` werden gepuffert und vom Main-Thread pro Frame angewendet
  (`drainInputs` / `serviceScreenshot`); `close_active_tab` geht über `pending_tab_closes`.
- Ein Handler braucht einen Rückgabewert (etwa `"ok"`): mit `!void` schickt zigjr keine
  Antwort, und der Aufrufer wartet bis zum Zeitlimit.
- `open_file` prüft nur IsDir synchron und legt den Tab gepuffert an, weil ein `tabs.append` aus
  dem Server-Thread `renderTabBar` mitten in der Iteration trifft. Nach `open_file` also
  `settle`, bevor Tabs abgefragt werden. `open_folder` läuft ebenso gepuffert im Main-Thread,
  weil `loadDirectory` sonst Knoten unter einem laufenden Render leert.
- `split_pane` und `show_context_menu` mutieren noch direkt aus dem Server-Thread.
- **`onMain` ist Pflicht für jeden RPC, der veränderlichen UI-Zustand liest** (Buffer, Editoren,
  Listen der UI): der Server-Thread legt den Aufruf ab, `drainInputs` führt ihn im nächsten
  Frame aus, der Server wartet (5 s Zeitlimit). Beispiele: `editor_state`, `file_text`,
  `get_chat_input`, `chatState`, `explorer_entries`. Ohne `onMain` liest der Handler Buffer oder
  Bäume, die der Main-Thread gerade ersetzt: sporadisch fehlende Einträge, Zeiger in freigegebenen
  Speicher, „switch on corrupt value“ in `Buffer.walk_const`. Stresstest:
  `python3 scripts/e2e_rpc_race.py`.
- Übrige Lesezugriffe auf gemeinsame Daten brauchen eine Sperre (Beispiel `git_status_mutex`,
  Skill `explorer`).

## RPC-Referenz

- `agent_tool(name, arguments_json)` führt ein Agent-Werkzeug (`read_file`, `write_file`,
  `replace_text`, …) direkt aus, bestätigt und ohne Modell; Pfade relativ zum Projektordner.
  Ergebnis ist der Text, der ans Modell ginge (`e2e_encoding.py`).
- `explorer_open <path>` simuliert einen Klick im File-Explorer (setzt `file_to_open`),
  `open_file` geht nur über die Tab-Leiste.
- `get_active_tab` liefert pro Tab `modified` sowie `editor_modified` und `editor_file`
  (Buffer, den der Editor gerade zeigt).
- `key_press(name, ctrl)` kennt alle Buchstaben a–z sowie enter, backspace, escape, delete, tab,
  grave, up/down/left/right, home/end, page_up/page_down, f1, f2; `key_press_mods(name, ctrl, shift)`
  zusätzlich Shift (Ctrl+Shift+Tab). Modifier werden nach der Taste wieder gelöscht.
  `key_press_alt` und `click_mods`: Skill `editor`.
- `ui_state` liefert Dialog-Titel, offenes Menü, Explorer-Fokus, Explorer sichtbar,
  Picker/Shortcut-Dialog offen, Tabs (Pfad, Art, geändert) und aktiven Tab, `tooltip` (Text im
  letzten Frame), `last_frame_ms`/`max_frame_ms` (Layout-Zeit; headless rendert nur beim
  Screenshot), die Glyph-Cache-Diagnose `glyph_rasterized`, `glyph_cache_clears`,
  `glyph_cache_entries`, dazu `text_runs_dropped` (nicht gezeichnete Textstücke) und
  `clay_errors` (Clay-Fehler seit Start). Damit prüfen E2E, dass nichts still verloren ging
  (`scripts/e2e_long_runs.py`).
- `editor_state` liefert Zeilen, Cursor, Suchleiste (offen, Begriff, kein Treffer), den Text
  sowie `height`/`visible_rows` (Bounding-Box des Editors aus dem Vorframe, muss über Frames
  konstant bleiben).
- `element_bounds(id)` / `element_bounds_i(id, index)` geben Clay-Bounding-Boxen für Klicks. Für
  „existiert das Element gerade?“ sind sie unzuverlässig (Clay behält Daten verschwundener
  Elemente), dafür `ui_state`.
- Explorer-RPCs (`explorer_entries`, `scroll`): Skill `explorer`. Ordner-Dialog
  (`folder_picker_state`, `get_state.root`): Skill `projektordner`.

## Fixtures

Fixtures unter `tmp/` anlegen (gitignored, im Explorer sichtbar). Keine Suite liest aus
`test_data/`, und zid öffnet beim Start nur eine Datei von der Kommandozeile. Eingecheckte
Vorlagen liegen unter `scripts/fixtures/`; PDF und PNG erzeugt `scripts/e2e_fixtures.py` ohne
Fremdbibliothek (`write_pdf`, `write_png`; Selbsttest per Direktaufruf). Start, Stopp und
Suitenbetrieb (`start_zid`, nie parallel): Skill `grosse-dateien`.
