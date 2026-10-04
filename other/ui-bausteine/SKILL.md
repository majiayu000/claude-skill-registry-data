---
name: ui-bausteine
description: >
  Gemeinsame UI-Bausteine in zid: Schaltflächen (components/button.zig), Icon-Schaltflächen mit Tooltip (tooltip.iconButton/attach, hover_delay), Scrollbalken (scrollbar.zig), Lucide-Icons als Kontur (svg.SvgStroke). Use when adding or changing a button, icon button, tooltip, hover element, scrollbar or SVG icon, when touching src/ui/components/button.zig, tooltip.zig, scrollbar.zig, hover_delay, svg.Svg/SvgStroke, or scripts/e2e_terminal.py, e2e_scm_changes.py, e2e_timeline.py.
---

# UI-Bausteine

Scrollbalken, Tooltips, Kontextmenüs und Eingabezeilen gibt es je einmal (`scrollbar.zig`,
`tooltip.zig`, `context_menu.zig`, `line_edit.zig`). Vor einem neuen Bedienelement dort suchen
und das Modul verwenden oder erweitern, nie parallel nachbauen: eine Kopie bekommt Fixes nicht
mit (der I-Beam über dem waagrechten Balken kam so in der Markdown-Vorschau zurück, die einen
eigenen Balken hatte). Kontextmenü: Skill `menues-kuerzel`; Eingabezeilen: Skill `editor`.

## Schaltflächen: `components/button.zig`

- Einheitliches Aussehen über `button(id, text, theme, mouse_x, mouse_y, mouse_pressed, opts)`
  mit den Rollen `primary` (Hauptaktion), `secondary` (Nebenaktion) und `ghost` (unauffällig,
  Fläche erst beim Überfahren). `disabled` dämpft und schluckt Klicks.
- Der Treffer wird gegen die Box aus dem letzten Layout gerechnet, **nicht** über
  `clay.pointerOver`: im Frame eines RPC-Klicks kennt Clay die neue Zeigerposition noch
  nicht, der Klick ginge verloren.
- Wer eine Schaltfläche braucht, nimmt diese Komponente statt selbst zu zeichnen, sonst fehlen
  Hover und Rahmen.
- Eine Aktion ohne sichtbare Folge bestätigt sich per `UI.showToast`.

## Tooltips für Icon-Schaltflächen

- `src/ui/components/tooltip.zig`: `iconButton(arena, theme, id, icon_id, icon, label, opts)` ist
  der gemeinsame Knopf (Hintergrund beim Überfahren, `toggled` in Primärfarbe), `attach(theme,
  id, label)` hängt einen Tooltip an ein selbst gezeichnetes Element. Tooltip erscheint nach
  700 ms über demselben Element unter dem Element (`hover_delay.Hover`, Modul `hover_delay`,
  unit-getestet); `beginFrame`/`endFrame` rahmen `renderExample` ein. Zustand ist modulweit, der
  Text muss den Frame überleben (Literal oder Frame-Arena).
- Neue Icon-Knöpfe immer über `tooltip.iconButton` anlegen.
- Beschriftungen wie VS Code: Timeline (Pin the Current Timeline / Unpin …, Refresh), Graph
  (Refresh, Open Changes), Changes (Commit, Sync Changes / Publish Branch, Refresh, Open File,
  Stage/Unstage/Discard Changes, Stage/Unstage/Discard All Changes), Diff-Editor (Previous/Next
  Change, Toggle Collapse Unchanged Regions, Switch to Inline/Side by Side View),
  Multi-File-Diff (Collapse/Expand All Diffs), Ordner-Dialog (Parent Folder), Statusleiste
  (Current Git Branch, Toggle Autosave).
- **Jedes Hover-Element, das nicht selbst klickbar ist, braucht
  `pointer_capture_mode = .passthrough`** (wie `tooltip.attach`, Cursorstriche, Platzhalter),
  sonst fängt es den Klick auf das Element darunter ab (Explorer-Tooltip `fx_tooltip` über der
  nächsten Zeile).
- E2E: `ui_state.tooltip` = Text des Tooltips im letzten Frame (null ohne), geprüft in
  `e2e_scm_changes.py` und `e2e_timeline.py` (Maus 1 s über dem Knopf halten).

## Scrollbalken: `src/ui/scrollbar.zig`

- Modul `scrollbar`, eigenes Modul, weil code_editor.zig ein eigenes Test-Root ist. Clay hat
  keinen Balken, nur Clip-Container; die virtualisierten Ansichten scrollen über eigene Offsets.
- `Model` (Achse, Track, total, visible, offset, max_offset) → `geometry`, `hitTest` (Thumb
  greifen oder Seite blättern), `dragOffset`, `render`.
- Editor senkrecht und waagrecht (`vscrollModel`/`hscrollModel`, `vscroll_drag`/`hscroll_drag`).
  Die waagrechte Editor-Leiste misst die längste Zeile der ganzen Datei (`maxLineWidth`, gecacht,
  nach einem Edit nur der betroffene Bereich), damit sie beim senkrechten Scrollen stabil bleibt,
  und deckt auch den Gutter ab. E2E: `step_hscrollbar` in `scripts/e2e_editor.py`.
- Explorer: `FileExplorerState.scrollModel` in Pixeln, der Balken hängt an der Hülle
  `file_tree_area` und beginnt so unter der Filterzeile. E2E `e2e_explorer.step_scrollbar`.
- Terminal: `TerminalInstance.scrollModel` in Zeilen, Track über die volle Höhe von
  `terminal_outer` (Lage aus dem Vorframe). E2E `scripts/e2e_terminal.py` (RPC `terminal_state`:
  `view_row`, `total_rows`, `visible_rows`, `pane_index` für
  `element_bounds_i("terminal_scrollbar_track", pane_index)`).
- Markdown-Vorschau: Skill `markdown-preview`. Bei jedem neuen Balken den Cursor-Test ergänzen
  (Pfeil über dem Balken, `ui_state.cursor`).

## Lucide-Icons sind Strichpfade

`svg.Svg` füllt den Pfad (Explorer-Chevrons und Datei-Icons so gewollt); reine Linienpfade wie
`plus`, `minus`, `check`, Pfeile bleiben gefüllt aber unsichtbar, Bögen (`undo_2`,
`refresh_cw`) werden zu Klecksen. Dafür `svg.SvgStroke` (Strichbreite 2 auf viewbox 24,
`SvgRenderInfo.stroke_width`, Atlas-Key unterscheidet Füllung/Strich). `tooltip.iconButton`, die
SCM-Zeilenaktionen, der Commit-Knopf und die Graph-Kopfzeile zeichnen als Kontur. Der
Rasterizer schreibt im Strich-Modus den Alpha auch nach R, weil `text_atlas.wgsl` mit R maskiert.
