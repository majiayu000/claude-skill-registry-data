---
name: menues-kuerzel
description: >
  Tastenkürzel, Menüleiste und Kontextmenüs in zid aus einer Quelle: shortcuts.zig (Command, Taste, Scope, Label, Menüstruktur), Umschalt-Häkchen (toggleState), context_menu.zig mit Hidden-Einträgen, Breite der Aufklappmenüs, Auflösung über handleKeyPress/executeCommand, Editor-Keymap. Use when adding or changing a shortcut, command, menu entry or context menu, when touching src/ui/shortcuts.zig, src/ui/context_menu.zig, src/editor/keymap.zig, toggleState, executeCommand, shortcuts.lookup, menu_dropdown, or scripts/e2e_shortcuts.py.
---

# Tastenkürzel und Menüs: eine Quelle

- `src/ui/shortcuts.zig` (Modul `shortcuts`) ist die einzige Tabelle: Command, Taste, Modifier,
  Scope (global / editor / explorer), Label, Anzeige-Text und die Menüstruktur File/Edit/View/Help.
  Unit-Tests prüfen Eindeutigkeit und Labels. Neue Kürzel nur dort eintragen, dann erscheinen sie
  automatisch in Menüleiste, Kontextmenüs, Help → Keyboard Shortcuts (F1) und als
  Agent-Werkzeug (Skill `llm-local`).
- **Umschalt-Befehle zeigen ihren Zustand:** `toggleState(cmd)` in `src/ui/mod.zig` liefert für
  jeden `toggle_*`-Befehl den aktuellen Wert; das Dropdown zeichnet davor ein Häkchen
  (Clay-ID `menu_check_<command>`, E2E über `element_bounds`). Neuer Toggle: dort eintragen.
  Autosave steht zusätzlich als Feld `status_autosave` in der Statusleiste.
- Globale und Explorer-Kürzel löst `UI.handleKeyPress` über `shortcuts.lookup` auf und führt sie
  mit `executeCommand` aus; Menüklicks gehen denselben Weg. Editor-Kürzel (Scope `editor`) liegen
  in `src/editor/keymap.zig` und müssen zur Tabelle passen (Save, Undo/Redo, Cut/Copy/Paste,
  Select All, Delete Line Ctrl+Shift+K, Find Ctrl+F).
- Globale Kürzel greifen vor Terminal/Chat: Ctrl+W, Ctrl+N, Ctrl+O, Ctrl+B, Ctrl+` und
  Ctrl+Tab kommen im Terminal bewusst nicht an der Shell an (wie in Zed).
- Menü per Tastatur (Alt+F/E/V/H) und Scrollen im Kürzel-Dialog: Skill `theme-zoom`.

## Ein Kontextmenü für alles

- `src/ui/context_menu.zig` (Modul `context_menu`, eigenes Modul wie `shortcuts`, weil
  code_editor.zig ein eigenes Test-Root ist) zeichnet Tab-Kopf, Editor-Text, Markdown-Vorschau,
  Terminal und Explorer im selben Theme-Stil (`Colors.fromTheme`, Zeile 30 px, Label 18 px links,
  Kürzel 14 px rechts).
- Einträge sind Listen in `shortcuts.zig` (`tab_menu_items`, `editor_menu_items`,
  `markdown_menu_items`, `terminal_menu_items`, `file_explorer.context_menu_items`), IDs
  `<prefix>_<command>` mit den Präfixen `tab_menu`, `editor_menu`, `md_menu`, `term_menu`,
  `fx_menu`; `hit(prefix, items, hidden)` liefert den angeklickten Eintrag.
- `Hidden` (EnumSet) blendet Einträge zustandsabhängig aus: Markdown Preview nur bei `.md`
  (Editor und Tab-Kopf), im Chat-Eingabefeld (`compact_menu`) weder Preview noch Split.
  Ausgeblendete Einträge in E2E prüfen: Skill `editor` (`menu_entry_visible`).
- Der Editor hält die Farben in `menu_colors` (gesetzt in `applyTheme`).
- Terminal-Copy/Paste sind eigene Commands `terminal_copy`/`terminal_paste` ohne Kürzel
  (Ctrl+C/V gehen an die Shell).
- `md_preview` aus dem Tab-Menü öffnet die Vorschau des angeklickten Tabs
  (`requestMarkdownPreview`), aus dem Editor die des aktiven Buffers.

## Breite der Aufklappmenüs ist dynamisch

Der Rahmen `menu_dropdown` ist `.w = .fit`, die Einträge sind `.w = .grow` mit
`child_gap = 32`. Clay misst den breitesten Eintrag und zieht alle anderen darauf; die Kürzel
stehen dadurch rechtsbündig, ohne dass jemand selbst misst. Eine feste Eintragsbreite ließ lange
Labels an ihr Kürzel stoßen. Gemessene Breiten: File 523, Edit 687, View 475, Help 507. Wann
`fit`/`grow` reicht und wann Obergrenze plus Kürzen nötig ist: Skill `clay-layout`.

## Prüfen

`python3 scripts/e2e_shortcuts.py` fährt headless alle Kürzel und Menüs durch (Explorer
F2/Entf, Tabs, Ansicht, Menüleiste, Kontextmenü, Shortcut-Dialog, Suchleiste) und legt
Screenshots unter `tmp/e2e_*.ppm` ab.
