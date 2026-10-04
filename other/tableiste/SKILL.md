---
name: tableiste
description: >
  Die Tab-Leiste in zid: Neu-Menü, Beschriftung, keine Vorschau-Tabs, Ctrl+Tab (MRU), Tab-Picker (Ctrl+E), Scrollen, Drag & Drop, Pinnen, Ctrl+Shift+T. Use when touching src/ui/tab_mru.zig, TabBarState, tabLabel/openFile/mru/cloneFrom, UI.tab_switcher/closed_tabs, or scripts/e2e_tabs.py.
---

## Tab-Leiste

- **„+“ (Neu-Menü) sitzt ganz links** vor dem scrollenden Tab-Streifen. Der Streifen hat `.w = .grow`
  mit Clip; dahinter wandert der Knopf an den Fensterrand und sein Dropdown wird abgeschnitten.
- **Beschriftung** (`tabLabel`): Markdown-Vorschauen heißen „Preview: name“; gleicher Dateiname in
  zwei Tabs derselben Art bekommt den Elternordner davor. Split (`cloneFrom`) kopiert Text-,
  Bild- und Vorschau-Tabs, aber nicht Chat und Terminal (ein Zustand, eine Zeichnung je Frame,
  siehe Skill `clay-layout`).
- **Keine Vorschau-Tabs** (auf Wunsch des Projektinhabers; VS Code und Zed haben
  sie standardmäßig an): Einfachklick, Space und Enter im Explorer öffnen jede Datei in einem
  eigenen Tab, ein Klick auf eine schon offene Datei wechselt nur dorthin (`TabBarState.openFile`).
- **Ctrl+Tab = zuletzt benutzt** (`recent_tab_next`/`recent_tab_prev`, wie VS Code/Zed): Tabs
  tragen eine Seriennummer, `TabBarState.mru` (`src/ui/tab_mru.zig`, unit-getestet) hält die
  Reihenfolge, `setActive` holt nach vorn, `closeTab` entfernt, Split kopiert sie. Der Umschalter
  (`UI.tab_switcher`, Overlay unter der Leiste) wandert bei gehaltenem Ctrl je Tab eine Position
  (`cyclePos`), Loslassen von Ctrl wählt (`commitTabSwitcher` in `setCtrlState(false)`). Ein
  einzelnes Ctrl+Tab springt damit zwischen den zwei jüngsten Tabs. Ctrl+PgUp/PgDn bleiben die
  Reihenfolge der Leiste (`next_tab`/`prev_tab`).
- **Ctrl+E = Tab-Picker** (`open_tab_picker`): der Picker im Modus `tabs` listet die offenen Tabs
  der aktiven Leiste, jüngster zuerst, mit Ordner als Detail; Enter wechselt (`Picker.takeTab`).
- E2E: `key_press_hold(name, ctrl, shift, alt)` lässt die Modifier gedrückt, `mods_release` löst sie;
  `ui_state.tab_switcher` ist die Position (−1 = zu). `key_press_mods` löst Ctrl nach der Taste,
  deshalb wählt dort jedes Ctrl+Tab sofort.
- **Leiste** scrollt den aktiven Tab per `scroll_x` in den Sichtbereich (`tab_strip` mit Clip).
  Klicks auf Tabs zählen nur innerhalb von `tab_strip`: weggescrollte Tabs liegen mit ihrer
  Bounding-Box unter „+“, der Sidebar oder rechts außerhalb des Fensters. E2E aktiviert Tabs
  außerhalb des 1200-px-Fensters per Ctrl+1…9 statt per Klick;
  Namensgleichheit zeigt den Elternordner (`a/mod.zig`), ungespeichert = „• name“. Mittelklick
  schließt, Rechtsklick öffnet das Menü aus `shortcuts.tab_menu_items` (`tab_menu_<command>`,
  gezeichnet über `context_menu.zig`; Markdown Preview nur bei `.md`-Text-Tabs), Kommandos laufen
  mit `tab_cmd_target` durch `executeCommand`. Drag & Drop: `TabBarState.drag`
  (Start beim Klick, ab 6 px Bewegung, Drop auf `tabIndexAt`). Angepinnte Tabs haben kein ×
  und bleiben bei Close Others/All/Saved; geänderte Tabs ebenso (kein Dialog pro Tab).
- Ctrl+Shift+T öffnet aus `UI.closed_tabs` (max. 20, nur noch existierende Dateien), Ctrl+1…9,
  Ctrl+PgUp/PgDn, Ctrl+S ist global. „Don't Save“ lädt den Buffer von der Platte neu, weil Buffer
  das Schließen überleben. Auto-Reveal: Tab-Wechsel auf eine Textdatei markiert sie im Explorer.
- RPCs: `tab_bounds(index)`, `middle_click`, `mouse_down`/`mouse_up` (Drag), `move_mouse` hält die
  gedrückte Taste; Tab-JSON hat `pinned`. `python3 scripts/e2e_tabs.py` deckt alles ab.
- Frame-Zeit: `ui_state.last_frame_ms`/`max_frame_ms` (Maximum seit dem letzten Abholen). Echte
  Frames liegen bei 1–4 ms; Latenz nie über `editor_state` messen, der RPC liefert bei einer
  5-MB-Datei 5 MB JSON je Abfrage. Fehler beim Laden/Speichern zeigt `UI.reportError` als Dialog.
- Markdown-Preview hält je Sprache einen Highlighter (`code_highlighters`-Map), damit nicht jeder
  Sprachwechsel einen neuen Tree-sitter-Parser baut.
