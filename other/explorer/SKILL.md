---
name: explorer
description: >
  File-Explorer in zid: Fokus, Tastatur/Navigation, Mehrfachauswahl, Papierkorb, Anlegen/Umbenennen, .gitignore-Anzeige und Tab-Nachführung. Use when touching src/ui/file_explorer*, explorer_ops.zig, dialog_ops.zig, FileExplorerState, isIgnored/folderStatus/statusFor, git_status_mutex, RPC explorer_entries, taskGitStatus/parseStatusOutput, pending_fs_change/applyFsChange, or scripts/e2e_explorer.py, e2e_symlink_dir.py, e2e_line_edit.py.
---

## Explorer: Fokus, Tastatur, Auswahl, Papierkorb

- **Symlink auf einen Ordner ist ein Ordner** (`explorer_ops.isDirectory` folgt dem Link, z. B.
  `wartungsheft/business-plan -> ../business/auto-service`). `TabBar.appendFileTab` lehnt
  Verzeichnisse mit `error.IsDir` ab, egal ob Explorer, Ctrl+P, Agent oder RPC `open_file`.
  Scheitert der Buffer-Load beim Tab-Wechsel trotzdem (z. B. AccessDenied), meldet `main.zig`
  den Fehler einmal, schließt den Tab und nullt `pending_switch_path`; sonst wiederholt sich
  der Fehler in jedem Frame. E2E: `python3 scripts/e2e_symlink_dir.py`.

- **Fokus** (`ui_state.explorer_focused`) setzt jeder Klick in die Sidebar, Escape gibt ihn ab; die
  Sidebar zeigt ihn als linken Rahmen in `border_focus`. Mit Fokus erreicht keine Taste den Editor:
  Explorer-Kürzel aus `shortcuts.zig` (Scope `explorer`, auch ohne markierten Eintrag) → sonst
  `FileExplorerState.handleNavKey` (↑↓ mit Shift-Bereich, ←→ zu-/aufklappen bzw. Eltern/Kind,
  Enter/Space öffnet, Home/End, PageUp/PageDown) → Rest wird geschluckt. Buchstaben wie in
  nvim-tree/yazi: `d` Papierkorb, `r` umbenennen, `a`/`Shift+A` anlegen, `y`/`x`/`p` kopieren/
  ausschneiden/einfügen, `Ctrl+D` duplizieren, `c`/`Shift+C` Pfad, `Shift+R`/F5 neu laden,
  `w` alles zuklappen, `Ctrl+A` alles markieren. Kein Type-ahead: Buchstaben sind Kürzel.
- **Auswahl** ist eine Menge (`selected_nodes`, Ctrl+Klick toggelt, Shift+Klick/Shift+↑↓ Bereich ab
  `anchor_index`), `selected_index` ist der Cursor. Ordner-Klick markiert und toggelt. `selectedPaths`
  lässt Kinder markierter Ordner weg. Ctrl+Klick lässt sich per RPC nicht auslösen (Modifier gelten
  nur für `key_press_mods`), der E2E nimmt Shift+↓.
- **Anzeige:** Namen werden auf die Sidebar-Breite gekürzt („…“, `ellipsize` misst per
  `measureTextWidth`), ein Tooltip mit dem vollen Pfad erscheint nach 700 ms über einer Zeile
  (`hover_index`/`hover_since_ms`, Element `fx_tooltip`). Ordner erben die Git-Farbe ihrer Nachfahren
  (`folderStatus`, C > M > A > ?), Icons nach Endung (`fileIcon`-Tabelle). Versteckte Einträge zeigt
  Taste `.` oder „Toggle Hidden Files" im View-Menü (`show_hidden`, gedämpft, mit Häkchen). Das Filterfeld öffnet `/` (Name enthält Text, Elternordner
  bleiben, Ordner mit Treffern gelten als aufgeklappt; nur geladene Knoten werden durchsucht; Enter
  behält den Filter, Escape leert ihn). Drag & Drop: Ziehen eines Eintrags auf einen Ordner (oder eine
  Datei darin) fragt „Move 'a' into 'b'?“ und ruft `performMove` (`drag`/`pending_move`).
- **Gemerkter Zustand** (`src/ui/user_state.zig`, unit-getestet): `$XDG_CONFIG_HOME/zid/state`
  bzw. `~/.config/zid/state` mit `sidebar_width` und `show_hidden`; geschrieben nach dem
  Splitter-Ziehen und beim Umschalten, gelesen in `UI.loadUserState` nach `setupClay`. E2E setzt
  `XDG_CONFIG_HOME=tmp/xdg-config`.
- **Kontextmenü** ist datengetrieben (`context_menu_items`, Labels/Kürzel aus der Tabelle, IDs
  `fx_menu_<command>`, gezeichnet über `context_menu.zig`); der Klick landet in `pending_command`,
  die UI führt `executeCommand` aus.
- **Kleine Editierfelder** (Umbenennen, Anlegen, Filter, Picker-Suche, Pfad im Ordner-Dialog,
  Commit-Nachricht) teilen `explorer_ops.EditBuffer` und `line_edit.zig`. Auswahl: `anchor` im Puffer, Shift+Pfeile/Pos1/Ende/↑↓ erweitern, Ctrl+←/→ wortweise
  (`moveWordLeft/Right`, Klassen Wort/Satzzeichen/Leerraum), Ctrl+A/C/X/V über
  `line_edit.Clipboard` (`UI.editClipboard`: Fenster oder headless `last_clipboard_text`),
  Shift+Klick und Ziehen (`handleClick(extend)`, `handleDrag`, `handleRelease`; `mouse_selecting`
  im Puffer). Tippen/Backspace/Entf/Einfügen ersetzen die Auswahl im `EditBuffer`, einzeilige
  Felder machen beim Einfügen aus Umbrüchen Leerzeichen (`insertText(multiline)`). Markierung:
  Element `<feld-id>_sel` (Commit-Feld `sc_input_sel` je Zeile). Die Feld-Handler bekommen
  `line_edit.Mods` und `?Clipboard` von `mod.zig` (`editMods`). Unit-Tests in `explorer_ops.zig`,
  E2E `python3 scripts/e2e_line_edit.py`.
  Anlegen zeigt eine Eingabezeile unter dem Zielordner (`startCreate`, `targetFolder`: markierter
  Ordner, sonst Elternordner, sonst Root); Enter legt an (Dateien werden geöffnet), Escape bricht ab.
- **Löschen = Papierkorb** (`explorer_ops.trashPath`: `$XDG_DATA_HOME/Trash` bzw. `~/.local/share/Trash`,
  `files/` + `info/*.trashinfo`, DeletionDate in UTC), Fallback `gio trash`, nie endgültig.
  Über Laufwerksgrenzen (USB-Stick, Netz, andere Partition) geht das Rename nicht; dann kopiert
  `explorer_ops.moveByCopy` in den Home-Papierkorb und löscht danach das Original (scheitert ein
  Schritt, bleibt das Original). Kein eigener Ablageort: der Home-Papierkorb ist der, den die
  Oberfläche zeigt, und „Wiederherstellen“ folgt dem Pfad in der `.trashinfo`.
  E2E-Skripte setzen `XDG_DATA_HOME=tmp/xdg`, damit der echte Papierkorb leer bleibt. Fehler von
  Explorer-Aktionen landen in `takeError` → Dialog „Error“ statt nur im Log.
- **Windows** (`src/platform/recycle_bin.zig`): Recycle Bin über
  `SHFileOperationW` mit `FOF_ALLOWUNDO`, aber nur auf festen Laufwerken (`GetDriveTypeW ==
  DRIVE_FIXED`). Netz- und Wechsellaufwerke haben keinen Papierkorb, Windows würde dort mit
  `FOF_NOCONFIRMATION` still endgültig löschen; deshalb `FileExplorer.recycleViaStaging`: Kopie
  nach `%LOCALAPPDATA%\zid\recycled` (`copyPath`), die Kopie in den Recycle Bin, dann das
  Original entfernen. Die Datei liegt so im normalen Papierkorb; „Wiederherstellen“ legt sie in
  den Zwischenordner, nicht aufs Netzlaufwerk zurück (die API kennt keinen fremden
  Ursprungsort; das `$I`-Format selbst zu schreiben wäre undokumentiert). Die Statusmeldung nennt
  den Ordner. Ein gesetztes `XDG_DATA_HOME` erzwingt auch unter Windows die freedesktop-Ablage (E2E).
  `build.zig` linkt dafür `shell32`.
- **Dialoge per Tastatur** (`dialog_ops.zig`, unit-getestet): Enter wählt den fokussierten Button
  (Start: erster = primär), Escape Cancel, Tab/Shift+Tab wandern, Anfangsbuchstabe wählt (`d` Delete,
  `s` Save, `n` Don't Save). Bei offenem Dialog erreicht keine Taste und kein Zeichen den Editor.
  In `renderExample` wird `ad.key_result` erst nach dem Übernehmen in `pending_dialog_result`
  geleert, weil `res = render(...) orelse ad.key_result` auf das Feld verweisen kann.
- **Explorer testen:** `explorer_entries` liefert Viewport-Bounds, `row_height`, `scroll` und die
  sichtbaren Zeilen mit Index; Zeilenmitte = `viewport.y + index*row_height + row_height/2 - scroll`.
  Zeilen außerhalb des Viewports vorher mit `scroll x y lines` (negativ = runter) hereinholen.
  Das ist die UI-Konvention aller `scrollLines` (positiv = hoch). Im Fenster spiegelt
  `platform/wheel.zig` das wio-Delta (positiv = Rad nach unten, auf jeder Plattform gleich)
  ohne OS-Sonderfall; der RPC umgeht diese Stelle, das Vorzeichen deckt nur der Unit-Test ab.
  Beim Prüfen von Hand: das Touchpad hat unter GNOME Natural Scrolling, die Maus nicht.
  Rechtsklick auf eine Zeile öffnet das Menü (Rename/Delete); F2/Entf wirken auf den markierten
  Eintrag, aber nur wenn der letzte Klick im Explorer war (`ui_state.explorer_focused`).
- `python3 scripts/e2e_explorer.py` fährt Fokus, Kürzel, Dialog-Tastatur, Papierkorb, Navigation,
  Anlegen/Umbenennen, Zwischenablage, Mehrfachauswahl und Kontextmenü headless durch.

## Explorer: .gitignore-Einträge

- `taskGitStatus` ruft `git status --porcelain=v2 --branch --null --ignored` (im Projekt ~50 ms
  mehr) und schreibt zusätzlich `root:<toplevel>` (aus `rev-parse --show-toplevel`): porcelain-Pfade
  sind relativ zur Repo-Wurzel, nicht zum Projektordner. Das Parsing steckt in
  `git_worker.parseStatusOutput` (unit-getestet); ignorierte Einträge kommen als `I:<pfad>`, Ordner
  ohne den abschließenden Schrägstrich von `! pfad/`.
- `FileExplorer.isIgnored(path)`: Eintrag selbst oder ein Vorfahr mit `I` → Name in `theme.muted`,
  kein Badge; `folderStatus` überspringt `I`, damit ein ignorierter Ordner keinen Status nach oben
  vererbt. RPC `explorer_entries[].ignored`; E2E-Schritt `step_gitignore` nutzt, dass `tmp/` im
  Projekt ignoriert ist.
- **`file_explorer.git_status` hängt an `git_status_mutex`:** der Main-Thread ersetzt die Map in
  `updateGitStatus` (Keys werden freigegeben), während `explorer_entries` sie gleichzeitig liest.
  Zugriff nur über `statusFor`, `isIgnored`, `folderStatus`, nie direkt auf die Map (sonst
  Segfault in `isIgnored`).

## Explorer: Umbenennen/Löschen und offene Tabs

- Umbenennen zieht Tab-Pfad, Titel, Buffer-Pfad und `open_buffers`-Schlüssel mit, auch für
  alle Tabs unter einem umbenannten Ordner (Preview-Tabs mit `preview://`-Präfix ebenso).
- Klick in den Editor setzt `selection_anchor = cursor`; jede Eingabe hebt den Anker wieder auf
  (`deleteSelection`), sonst ersetzt das zweite getippte Zeichen das erste.
- Löschen schließt Tabs ohne ungespeicherte Änderungen; geänderte Tabs bleiben offen mit
  Stern, Speichern legt die Datei wieder an (Verhalten wie VS Code). Buffer gelöschter
  Dateien wandern nach `orphan_buffers` (bis Programmende), damit ein neu angelegtes File
  mit gleichem Namen nicht den alten Inhalt bekommt.
- Ablauf: Explorer setzt `pending_fs_change`, `UI.update()` holt es per `takeFsChange` ab
  und wendet es vor dem Layout an (`applyFsChange`).
