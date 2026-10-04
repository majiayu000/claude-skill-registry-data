---
name: schnelloeffner
description: >
  Schnellöffner (Ctrl+P) und Command Palette (Ctrl+Shift+P) in zid: der modale Picker, Fuzzy-Matching, Datei-Scan im Hintergrund, Zeilenlayout mit mittigem Kürzen. Use when touching src/ui/picker.zig, src/ui/fuzzy.zig, src/ui/path_display.zig, scanWorker/dirShown/truncateMiddle, RPC picker_state, or scripts/e2e_picker.py.
---

## Schnellöffner (Ctrl+P) und Command Palette (Ctrl+Shift+P)

- `src/ui/picker.zig`: ein modaler Picker für beide Modi, Matching in `src/ui/fuzzy.zig` (unit-getestet:
  Teilfolge in Reihenfolge, Bonus für zusammenhängende Treffer, Wortanfänge, Dateinamen). Die Palette
  listet alle `shortcuts.Command` mit Label und Kürzel; Enter läuft über `executeCommand`.
- Dateiliste: Hintergrund-Thread (`scanWorker`, Breitensuche, versteckte und `zig-out`/`node_modules`/…
  übersprungen, max. 100 000), Ergebnis kommt per Mutex in `poll()` (jeden Frame aus `update`). Labels
  liegen in einer Arena, weil 30 000 einzelne `free()` mit dem Debug-Allocator den Main-Thread
  sekundenlang blockieren. Cache 10 s je Root. Der Picker erscheint sofort, „Scanning…“ im Hinweis.
- `filter()` tauscht die Trefferliste erst nach dem Ranking (der RPC-Thread liest nebenläufig).
- **Zeilenlayout bei Dateien** (`src/ui/path_display.zig`, unit-getestet): Dateiname zuerst in
  Textfarbe, Ordner gedimmt dahinter und mittig gekürzt (`truncateMiddle`, Auslassungszeichen,
  zählt Zeichen statt Bytes), weil rechts abgeschnittene Pfade in tiefen Bäumen genau den
  unterscheidenden Teil verlieren. VS Code und Zed stellen den Namen ebenfalls nach vorn, snacks.picker
  kürzt standardmäßig in der Mitte. `ROW_CHARS` rechnet das Zeichenbudget aus `BOX_WIDTH` — zulässig,
  weil die einzige Schrift eine Monospace ist. `commonPrefix` liegt bereit für Zeds Ansatz
  (gemeinsame Segmente aller Treffer wegkürzen), ist aber noch nicht verdrahtet.
- **Clay: Text ohne Umbruch ist eine Mindestbreite.** `wrap_mode = .none` meldet die volle
  Textbreite als Mindestmaß, und Clay zieht Zeile und Liste darauf auf, über den 720 px breiten
  Kasten hinaus. Abhilfe ist
  `SizingAxis.growMinMax(.{ .min = 0, .max = … })` auf der Zeile, das Gegenstück zu `max-width`;
  in CSS entspricht das `min-width: 0` an einem Flex-Element. **Kein verschachteltes `.clip`** als
  Ersatz: der innere Clip ersetzt im Renderer den äußeren statt sich mit ihm zu schneiden, dann
  läuft die Liste unten aus dem Kasten.
- Breiten werden gemessen, nicht aus Zeichen geschätzt: Name (18 px) und Ordner (14 px) stehen in
  verschiedenen Größen, ein gemeinsames Zeichenbudget liegt daneben. `truncateToWidth` sucht die
  Zeichenzahl binär über `ui.measureTextWidth`.
- `Picker.dirShown` ist die eine Quelle für Render und RPC, damit der E2E prüft, was gezeichnet wird.
  `e2e_picker.py` prüft zusätzlich die Geometrie (Zeile ⊆ Kasten), weil reine Textprüfungen
  Überbreite nicht sehen.
- RPC `picker_state` (open, scanning, mode, query, matches, items, selected, selected_label,
  selected_dir_shown); `python3 scripts/e2e_picker.py`.
