---
name: markdown-preview
description: >
  Markdown-Vorschau in zid: Tabellen, Umbruchbreite, Word Wrap, Balken, Textauswahl, Suche (Ctrl+F), Schriftgröße, abfragbare IDs für E2E. Use when touching src/ui/markdown_view.zig, md_select.zig, md_find.zig, word_wrap.zig, reloadMarkdownPreview, preview rendering or scrolling, zigdown styling limits (strikethrough, bold/italic), or scripts/e2e_md_preview*.py, e2e_find_preview.py.
---

## Markdown-Vorschau

- **Tabellen in der Vorschau:** zigdown liefert eine Tabelle als Container mit flacher
  Zellliste (je `ncol` Paragraphen eine Zeile, erste Zeile = Kopf). `MarkdownView.renderTable`
  baut daraus das Raster. Die Spaltenbreiten kommen
  wie im Browser aus dem Inhalt: `measureCell` liefert je Zelle die Wunschbreite (eine Zeile)
  und die Mindestbreite (breitestes unteilbares Stück), die Tabelle verteilt proportional und
  staucht notfalls die jeweils breiteste Spalte. `relative_width` aus der Trennzeile bleibt
  ungenutzt, die Zahl der Striche sagt nichts über den Inhalt. Die Tabelle steht in zwei
  `grow`-Hüllen (`md_table_row` mit Frame-Nummer für die E2E, darin `md_table_box` mit je Block
  stabiler Nummer zum Messen) und ist selbst `fit` — gemessen wird die Hülle, sonst
  schrumpft die Tabelle Frame für Frame an ihrer eigenen Breite. Die Hüllenbreite ist nach
  oben durch `wrap_width_hint` gedeckelt: `grow` wird nie schmaler als das Kind und hielte
  sonst eine Überbreite aus dem ersten Frame (noch ohne Hint, 800 px) für immer fest.
  **Kein `clip` je Zelle:** Clay hält nur zehn Clip-Container, eine Tabelle sprengt das sofort
  („out of bounds array access"). Zu lange Wörter zerlegt stattdessen `splitWide`; Fließtext und
  Tabellen scrollen nie waagrecht, nur Codeblöcke (siehe unten). Fixture: `libs/zigdown/test/table.md`,
  geprüft in `scripts/e2e_md_preview.py`. Spaltenausrichtung (`alignment`) wird nicht umgesetzt.

- **Listenzeichen:** `renderBlock` setzt vor jeden Eintrag `md_bullet`: „•“ bei `unordered`,
  „N.“ ab `List.start` bei `ordered`, bei `task` (`- [ ]`/`- [x]`, Klammern nimmt zigdown aus
  dem Text) ein Lucide-Kästchen (`square`/`square_check`, angehakt in Akzentfarbe) mit der ID
  `md_check_<n>`, n wie bei `md_li`. Die Breite des Zeichens geht in `indent` ein. Geprüft in
  `e2e_md_preview.check_task` an `libs/zigdown/test/spaced-list.md`.

- **Abfragbare IDs der Vorschau (E2E):** `md_tcell` mit Index Tabelle × 100000 + Zeile × ncol
  + Spalte (Tabellen ab 1), `md_quote`, `md_li`/`md_bullet` und `md_code` mit laufender
  Nummer ab 1. Alle Zähler setzt `resetCounters` zu Beginn jedes Frames zurück.
  **IDs, an denen die Vorschau im nächsten Frame eine Breite abliest** (`md_run_…` in
  `flushPieces`, `md_table_box`), tragen dagegen den Block-Index und einen je Block gezählten
  Lauf (`beginBlock` setzt zurück): frameweite Nummern verrutschen, sobald das virtualisierte
  Fenster oben einen Block verliert, und die Vorschau zappelt beim Rad-Scrollen.
  Zweite Ursache für Springen: Blöcke im Vorlauf über der Oberkante wechseln von Schätzung auf
  Messung, `syncBlockHeights` gleicht das über `scrollbar.anchorShift` im Offset aus.
  `e2e_md_preview.py` prüft, dass ein Rad-Schritt sichtbare Blöcke um genau 60 px bewegt.
  `e2e_md_preview.py` öffnet jede `libs/zigdown/test/*.md` (Glob), legt je Datei
  `tmp/e2e_md_example_<name>.ppm` ab und prüft Zitatrand, Aufzählungszeichen und
  Codeblock-Hintergrund an Pixeln des Screenshots.

- **Umbruchbreite = Hint minus Einrückung, plus Clays Viertelpixel.** `MarkdownView.indent`
  summiert die Einrückungen um den gezeichneten Block (Liste 24 px plus Punkt und Abstand,
  Zitat 16 px, Alert 32 px); `availWidth` zieht sie vom `wrap_width_hint` ab, und `flushPieces`,
  `renderTable`, `renderCodeBlock` brechen daran um; sonst ragt Text in Listen um die
  Einrückung über den Rand und wird stumm abgeschnitten. Zweiter Anteil: Clay schlägt je Textelement 0.25 px auf
  (`measureText` in mod.zig), jedes Wort ist ein eigenes Element — `flushPieces` rechnet den
  Zuschlag wie `measureCell` mit, sonst ist eine Zeile aus 40 Wörtern 10 px zu breit.
  Symptom für beides: `md_content` breiter als `md_viewport` ohne breiten Code. Bei Verdacht
  die Datei in Zeilenbereiche schneiden und je Scheibe headless die Breite messen (Probe im
  Stil von `e2e_md_preview.step_wide_code`), statt am Fenster zu raten.

- **Balken der Vorschau** kommen beide aus `scrollbar.zig` (`vModel`/`hModel`, Pixel als
  Einheiten, `md_scrollbar_*`/`md_hscroll_*`): Klick blättert, Thumb zieht (`vdrag`/`hdrag`),
  `render` meldet Hover → `scrollbar_hovered`, und `UI.getDesiredCursor` fragt zuerst
  `MarkdownView.cursorAt` (Pfeil über Balken und Menü, I-Beam über `md_viewport`).
  **Keine zweite Balken-Implementierung anlegen**, alle Balken laufen über `scrollbar.zig`.
  `ui_state.cursor` (E2E) liefert die Cursorform an der Mausposition;
  `e2e_editor.step_hscrollbar`, `e2e_md_preview.step_wide_code`, `e2e_explorer.step_scrollbar`
  und `e2e_terminal.py` prüfen Pfeil über Balken (Editor und Vorschau auch I-Beam über Text)
  — bei jedem neuen Balken den Test ergänzen. Explorer und Terminal werten den Hover nicht aus (dort gilt ohnehin der
  Pfeil); nur das Ziehen des Explorer-Thumbs hält den Pfeil auch über dem Editor. Zeilen unter
  einem Balken bekommen keinen Klick: Clay-Floating-Elemente fangen den Zeiger (`capture`).

- **Word Wrap in der Vorschau: Alt+Z, ein Schalter für Editor und Vorschau — bewusst anders
  als VS Code.** VS Code bricht in der Vorschau Fließtext immer um, Code nie (`pre { overflow:
  auto }`), und `editor.wordWrap` wirkt dort nicht. Der Projektinhaber will stattdessen den
  Editor-Schalter, und zwar sichtbar am Fließtext, nicht nur an Code. `render` liest
  `getActiveEditor().word_wrap` in `MarkdownView.wrap`. **Ein:** `flushPieces` bricht mit
  `splitWide`/`wrapLines` an `availWidth`, `renderCodeBlock` bricht Codezeilen mit `codeRowEnd`
  an jeder Stelle in Reihen (`Join.none`, kopiert ohne Trenner). **Aus:** `flushPieces` gibt
  jedem Lauf eine Reihe (Limit `floatMax`), Codezeilen laufen hinaus, `md_content` wächst mit
  der längsten Zeile (`grow` wird nie schmaler als das Kind), `md_viewport` verschiebt per
  `child_offset.x`, unten liegt der waagrechte Balken aus `scrollbar.zig`
  (`md_hscroll_track`/`_thumb`; Klick blättert, Thumb zieht, Shift+Rad bzw. Touchpad über
  `UI.handleScrollHorizontal` → `scrollColumns`, 60 px je Schritt). Tabellen passen in beiden
  Fällen in die Breite. Es scrollt der ganze Inhalt, nicht nur der Block: ein Clip je Block
  geht nicht, der Renderer schneidet verschachtelte Clips nicht (Skill `clay-layout`) und Clay hält nur
  zehn. Der Nutzerzustand (`~/.config/zid/state`, `word_wrap=`) gilt beim Start auch für die
  Vorschau. E2E `step_wide_code`: aus → breit mit Balken, ein → Listen, Zitat und 400-Zeichen-
  Code passen; Screenshots `e2e_md_preview_{list_wrapped,wrapped,wide,wide_scrolled}.ppm`.

- **Umbruch nur an Leerzeichen:** `word_wrap.wrapLines` trennt zwischen Wörtern, nie zwischen
  zwei Stücken ohne Leerzeichen dazwischen — zigdown liefert `code`, Satzzeichen und Wortteile
  einzeln, „Nr." kommt als „Nr" und „.". `measureCell` rechnet genauso und schlägt je
  Textelement 0.25 px auf, den Zuschlag aus `measureText` in `mod.zig`.

- **Textauswahl in der Vorschau** (Logik in `src/ui/md_select.zig`, unit-getestet): Ziehen mit
  der Maus markiert wie im Browser, Ctrl+C und Kontextmenü „Copy“ kopieren, Escape oder ein Klick
  ohne Ziehen heben auf. Position = (Block auf oberster Ebene, Zeile im Block, Byte-Offset), damit
  die Auswahl gültig bleibt, während die Virtualisierung andere Blöcke zeichnet. Jede Textreihe
  aus `flushPieces` und jede Codeblock-Zeile trägt die ID `md_line` (laufend je Frame) und landet
  mit Text in `line_texts` (bleibt über Frames, damit ein herausgescrolltes Ende kopierbar ist;
  `endBlock` wirft Zeilen weg, die es nach neuem Umbruch nicht mehr gibt). Hit-Test nimmt die
  Clay-Box der Reihe aus dem Vorframe und misst Codepoints (`offsetAtX`). Hervorhebung: `textSel`
  teilt ein Stück an den Auswahlgrenzen, der markierte Teil steht in einem `md_sel`-Element mit
  Hintergrund — kein Floating, keine Alpha-Überlagerung, Elemente nur für markierte Stücke.
  Kopiertext: weiche Umbrüche werden wieder Leerzeichen, harte Zeilen `\n`, Blockwechsel `\n\n`
  (zigdown macht aus Leerzeilen `Break`-Blöcke, die bleiben stumm), Absatzenden verlieren ihr
  Leerzeichen-Stück; ein nie gezeichneter Block dazwischen kommt als Fließtext aus dem Baum.
  Ändern sich Umbruchbreite oder Schriftgröße, wird die Auswahl aufgehoben (Zeilennummern
  stimmen dann nicht mehr). Andere Tasten und Buchstaben erreichen den unsichtbaren Editor
  hinter Vorschau, Bild, PDF und Binär-Tab nicht (`UI.handleKeyPress`/`handleChar` prüfen
  `activeTabKind() == .text`), sonst schluckt eine unsichtbare Editor-Suchleiste das Getippte.
- **Suche in der Vorschau (Ctrl+F)** nimmt die Bausteine des Editors, nichts nachgebaut:
  Zustand, Leiste und Tasten aus `src/editor/find_bar.zig` (`FindState`, `render`; auch der
  Editor zeichnet damit), Treffer aus `find_ops.Pattern` (Aa/W/.* wie im Editor, Alt+C/W/R).
  Nur die Vorschau-Teile stehen in `src/ui/md_find.zig` (unit-getestet): Weil virtualisiert
  gezeichnet wird, zählt `refreshFind` die Treffer über den Klartext jedes Blocks (`Hit` =
  Block, n-tes Vorkommen), `lineMarks` zählt beim Zeichnen je Zeile in derselben Reihenfolge
  mit; so weiß die Zeile, ob sie den aktuellen Treffer trägt. Sprung: liegt der Block außerhalb
  des gezeichneten Fensters, erst über die Blockhöhe, dann rückt `applyFindReveal` einige Frames
  lang über die gezeichnete Zeile nach (senkrecht, ohne Umbruch auch waagrecht; Boxen gelten
  mit dem Bildlauf des Vorframes, `drawn_scroll_*`). Markierung in `textSel` über
  `md_find.segments` (`md_hit`, `md_hit_cur`, Auswahl `md_sel` hat Vorrang). Grenze: ein
  Begriff über einen weichen Umbruch hinweg zählt im Klartext, wird in den Zeilen aber nicht
  gefunden. Speichern baut die Vorschau neu und übernimmt die Suche (`adoptFind`).
  RPC `md_find_state`, E2E `scripts/e2e_find_preview.py`.
  RPC `md_selection` (`open`, `lines`, `text`), E2E in `scripts/e2e_md_preview.py`
  (`step_selection`).
  **Marp-Decks** zeigt nicht `MarkdownView`, sondern das PDF aus marp-cli (Skill `marp`).
  **Chat-Bubbles:** jede Nachricht hat ihre eigene `MarkdownView`, `AIChatState.handleMouseDown`
  trifft die Bubble (`ai_msg_<idx>`) und startet dort die Auswahl (`sel_msg`, unter `mutex`, weil
  der Worker Nachrichten anhängt); Ctrl+C kopiert markierten Bubble-Text vor dem Eingabefeld,
  Escape hebt auf. Ein Klick ohne Ziehen kopiert die ganze Nachricht, und zwar beim
  Loslassen (`pending_copy_msg`, im Render, dort ist das Fenster).
  Die wachsende Stream-Bubble ist nicht auswählbar (wird je Token neu gebaut). RPC
  `chat_line_bounds(msg, line)`; E2E `select_in_bubble` in `e2e_ai_chat.py`.

- **Vorschau neu laden:** Speichern (Ctrl+S oder Autosave) baut eine offene Vorschau derselben
  Datei neu auf (`UI.reloadMarkdownPreview`, liest die Datei, behält Scroll-Position, Folie und
  Schriftgröße); Split „Editor links, Vorschau rechts“ zieht damit nach.
  E2E: `python3 scripts/e2e_md_preview_reload.py`.

- **Schriftgröße der Vorschau:** `UI.previewFontSize` (Editor minus 4, Standard 24 → 20).
  `setFontSizeAll` setzt sie bei jedem Zoom auf alle offenen `open_markdown_views`, und beide
  Stellen, die eine Vorschau anlegen (`src/main.zig` und der Render-Zweig in `mod.zig`),
  übernehmen sie, sonst bleibt die Vorschau auf ihrer Startgröße stehen.

## Bekannte Grenzen (kein Todo, bewusst so)

- **Durchgestrichen:** `~~text~~` toggelt zigdown zweimal und bleibt ungestylt, `~text~`
  funktioniert. Upstream-Verhalten in zigdown.
- **Fett/Kursiv nur über Farbe:** Es gibt eine einzige Font-Face (JetBrainsMono-Regular).
  Echte Schnitte bräuchten Font-IDs im Text-Renderer und eine zweite geladene Face.
  MarkdownView zeigt Styles deshalb als Theme-Farben (fett=primary, kursiv=accent,
  Code=warning, Link=blau, durchgestrichen=muted).
