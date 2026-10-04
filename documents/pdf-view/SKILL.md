---
name: pdf-view
description: >
  PDF-Vorschau in zid: Blättern, Zoom und Bildlauf in der Seite, Suche (Ctrl+F), Neuladen bei Dateiänderung, mupdf-Abstürze bei halb geschriebenen PDFs, E2E-Zustand. Use when touching src/ui/pdf_view.zig, pdf_nav.zig, pdf_find.zig, src/rendering/pdf_handler.zig, fz_page_text_z, PDF reload, or scripts/e2e_pdf_*.py.
---

## Zoom und Bildlauf

- Zustand je Dokument im `PdfHandler` (`zoom`, `scroll_x/y`), also gemeinsam für beide Panes
  eines Splits, wie `current_page`. Zoom 1.0 = Seitenbreite; Stufen `pdf_nav.zoom_levels`
  (50–400 %). Geometrie rein in `pdf_nav.geometry` (unit-getestet): passt die Seite, steht sie
  mittig, sonst verschiebt der Bildlauf sie über `child_offset` des Clip-Elements `pdf_viewport`.
- Bedienung: Knöpfe −/Prozent/+ in der Leiste (Prozent setzt auf 100 %), Ctrl+Rad um die
  Mausposition (`zoomAround`), Ctrl+Plus/Minus/0 über die Befehle `zoom_in/out/reset`, die im
  PDF-Tab die Seite statt der Schrift zoomen. Rad ohne Ctrl scrollt in einer überstehenden Seite
  und blättert erst am Rand (`pdf_nav.wheel`); zurück landet man am Ende der vorigen Seite. Passt
  die Seite, blättert jede Stufe eine Seite. Shift+Rad scrollt waagrecht.
- **Scharf rendern:** die Ansicht meldet je Frame den nötigen Maßstab (`wanted_scale`, px/pt,
  Maximum aller Panes), die Hauptschleife rendert neu, wenn er um mehr als 10 % von
  `requested_scale` abweicht oder `needs_render` (Seitenwechsel) gesetzt ist. Damit richtet sich
  die Auflösung nach Pane-Größe und Zoom statt fest 1.5/2.0. `renderPage` kappt bei 16 MP bzw.
  8192 px Kante; verglichen wird mit dem angeforderten, nicht dem gekappten Maßstab, sonst
  würde jeden Frame neu gerendert.
- Seiten mit MediaBox-Ursprung ungleich (0,0) werden an die Pixmap-Ecke verschoben
  (`origin_x/y`); Such-Rechtecke ziehen denselben Ursprung ab.

## Suche (Ctrl+F)

- Dieselbe Leiste wie Editor und Markdown-Vorschau (`find_bar.FindState` im Handler), dieselben
  Optionen über `find_ops.Pattern`. Enter/Shift+Enter springen mit Umbruch, Escape schließt,
  Blättern bleibt bei offener Leiste möglich.
- Text je Seite liefert `fz_page_text_z` (C-Wrapper, `fz_try` und Strukturblöcke rekursiv): je
  Zeichen Codepunkt und Box, Zeilenende als Leerzeichen, Blockende als `\n`, beide mit leerer
  Box. Die Strukturen von mupdf werden in C durchlaufen, nicht in Zig: System-mupdf (1.27) und
  gebündeltes (1.26.5) unterscheiden sich, der Wrapper wird je gegen den passenden Header gebaut.
- `pdf_find.zig` (rein, unit-getestet) baut daraus UTF-8 mit Byte-Anfang je Zeichen und macht aus
  einem Treffer-Bytebereich Rechtecke je Zeile. Gesucht wird schrittweise (~8 ms je Frame in der
  Hauptschleife, `searchStep`), der erste Treffer ab der Leseposition wird angesprungen, sobald er
  gefunden ist; spätere Funde ziehen nicht weg. Nach einem Reload läuft die Suche neu, ohne zu
  springen.
- Markierung: schwebende Rechtecke am Bild (`clip_to = .to_attached_parent`, passthrough),
  höchstens 400 je Seite; aktueller Treffer orange, übrige gelb.
- E2E: `python3 scripts/e2e_pdf_zoom_find.py`; `pdf_state` liefert dafür zusätzlich `zoom`,
  `scroll_x/y`, `scale`, `find_active`, `searching`, `hits`, `current`, `hit_page`.

## PDF-Vorschau: Blättern und Neuladen

- **Neu laden bei Dateiänderung:** `handleExternalChange` erkennt offene PDFs (`keyForPath` über
  `open_pdfs`, auch per realpath) und reiht sie in `pending_pdf_reloads` ein; `exportMarpPdf` tut
  das direkt. Der Main-Loop lädt erst, wenn die Datei 150 ms ruht (`takeDuePdfReload`, mtime):
  Das System-mupdf 1.27.2 (Linux linkt `/lib64/libmupdf.so`, nicht fancy-cats mupdf) stürzt beim
  Reparieren mancher halb geschriebener PDFs ab („double free“, `mutool draw` segfaultet auf
  derselben Datei), und der Watcher meldet je Datei nur ein Ereignis pro 100 ms. Neuer Handler,
  Seite geklemmt, Textur ersetzt; scheitert etwas, bleibt der alte Stand. `wantsFrameSoon` hält
  den Loop wach, solange ein Reload wartet. E2E `python3 scripts/e2e_pdf_reload.py`, Marp-Weg in
  `e2e_marp_pdf.py` (letzter Schritt).

- Blätter-Logik als reines Modul `src/ui/pdf_nav.zig` (Tasten, Mausrad, Sättigung an den
  Rändern, Beschriftung). Die Ansicht `src/ui/pdf_view.zig` liefert ein Seiten-Delta, die UI
  setzt die Seite (`PdfHandler.setPage`, markiert `needs_render`), die Hauptschleife rendert
  die Textur neu.
- Bild ab/auf und Pfeil links/rechts blättern; hoch und runter bleiben der Navigation
  zwischen Panes und im Explorer. Mausrad: negative Zeilen heißen nach unten, also vorwärts.
- `clay.pointerOver` meldet in dieser Ansicht nichts, deshalb hat die Leiste eine eigene
  Schaltfläche statt `components.Button`: Hover und Klick rechnen gegen die Bounding-Box aus
  dem letzten Layout (`pdf_nav.hits`, Aufhellung über `pdf_nav.brighten`).
- Die Beschriftung liegt in einem Puffer der UI (`pdf_labels`: Seite, Zoom, Trefferzahl), nicht in der Frame-Arena:
  `beginLayout` setzt die Arena zurück, Clay liest den Text erst beim Zeichnen.
- Zustand für E2E: `pdf_state` liest Felder im `E2EContext`, die der Main-Thread pro Frame
  setzt, weil der Server-Thread über Tabs und `open_pdfs` springende Werte liest.
- E2E: `python3 scripts/e2e_pdf_pager.py`, das siebenseitige PDF erzeugt `write_pdf` nach
  `tmp/e2e_pdf/pager.pdf`. Der Test startet
  mit eigenem, frischem `XDG_CONFIG_HOME` und übergibt das PDF als Startdatei: über eine
  wiederhergestellte Sitzung wechselt der aktive Tab und die Messung trifft Fremdzustand.
  `open_file` öffnet keinen PDF-Tab, das Laden hängt am Explorer-Pfad.
