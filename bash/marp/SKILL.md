---
name: marp
description: >
  Marp-Decks in zid: Vorschau und PDF-Export über marp-cli, das zid selbst einrichtet
  (samt chrome-headless-shell, wenn kein Browser da ist). Use when working on Marp decks,
  deck preview or PDF export, `src/ui/marp.zig`, `src/rendering/marp_cli.zig`,
  `startMarpPreview`/`pollMarpPreview`/`exportMarpPdf` in `src/ui/mod.zig`, the
  `md_preview`/`md_export_pdf` commands on decks, `ZID_TOOLS_DIR`, or
  `scripts/e2e_marp_pdf.py`.
---

# Marp in zid

Ein Deck ist eine Markdown-Datei mit `marp: true` im Front-Matter. zid rendert Decks nicht
selbst: Vorschau und PDF kommen beide aus marp-cli, Marps eigenem Konverter (Marp Core,
gedruckt von einem Browser). Das Ergebnis ist dasselbe wie in VS Code.

| Datei | Modul | Aufgabe |
| --- | --- | --- |
| `src/ui/marp.zig` | `marp` | `isMarpDeck`, `isMarpDeckFile` (Front-Matter lesen) |
| `src/rendering/marp_cli.zig` | `marp_cli` | marp-cli einrichten, aufrufen, Watch-Prozess |
| `src/ui/mod.zig` | — | `exportMarpPdf`, `startMarpPreview`, `poll*` je Frame |

## marp-cli einrichten

- `Exporter` lädt beim ersten Bedarf die eigenständige marp-cli (Node eingebaut, ein
  Programm, gepinnt `marp_tag`) nach `<Datenverzeichnis>/tools/marp-cli-<tag>/`. Download und
  Auspacken über `download` und `ai_selfsetup.install` wie bei der KI.
- **Browser:** marp-cli sucht Chrome, Edge, Firefox. Meldet es „No suitable browser
  found“, lädt zid chrome-headless-shell (Chrome for Testing, gepinnt `chrome_version`,
  rund 121 MB) nach `tools/chrome-headless-shell-<version>/` und ruft erneut mit
  `--browser chrome --browser-path`. `browser_used` merkt sich das für den Watch-Prozess.
  Linux auf ARM hat keine chrome-headless-shell: dort Fehlermeldung. Windows hat immer Edge.
- **Aufruf:** `marp --no-stdin --pdf --allow-local-files deck.md -o ziel.pdf`. `--no-stdin`
  ist Pflicht: ohne Terminal liest marp sonst die Eingabe als Markdown und wartet.
- **Zustand:** eigener Thread, atomar (`loading_marp`, `loading_browser`, `converting`,
  `done`, `failed`), `wake` weckt den Frame-Loop. Kein Ergebnis bei Fehler, kein Rückfall.
- **`ZID_TOOLS_DIR`** ersetzt den Ablageort; die E2E setzt `tmp/tools`, damit nur der erste
  Lauf lädt. Unter Windows wirkt `XDG_DATA_HOME` nicht, ohne die Variable landeten
  E2E-Downloads im echten Profil.
- **Zip-Entpacker:** `install.extractZip` ist eine eigene Schleife über
  `std.zip.Iterator`, `flate.Decompress` im direkten Modus (leerer Puffer). Der indirekte
  Modus, den `std.zip.extract` nutzt, stürzt in Zig 0.15.2 bei manchen Einträgen ab
  („reached unreachable“ in `writeMatch`), beim Zip von chrome-headless-shell zuverlässig.

## Vorschau

`md_preview` auf einem Deck (`requestMarkdownPreview` prüft `isMarpDeckFile`) ruft
`startMarpPreview`:

1. Das erste Rendern läuft über `marp_preview_job` (ein `Exporter`) nach
   `tools/preview/<hash>/<deck>.pdf` (`previewPath`, Hash des Deck-Pfads). Daneben
   `source.txt` mit dem Deck-Pfad. Nichts landet neben dem Deck.
2. `pollMarpPreview` startet danach `marp --watch` (`spawnWatch`, Browser bleibt offen,
   rund 1 s je Durchlauf) und öffnet das PDF als gewöhnlichen PDF-Tab. Blättern, Zoom und
   Suche sind die der PDF-Ansicht.
3. Je Frame vergleicht `pollMarpPreview` die mtime des Vorschau-PDFs und stößt bei Änderung
   `requestPdfReload` an (der Reload wartet 150 ms Ruhe ab). Der Datei-Watcher sieht den
   Cache nicht, er liegt außerhalb des Projekts.
4. Zeigt kein Pane mehr das PDF (nach 5 s Anlauf), beendet `stopWatch` den Prozess, unter
   Linux/macOS die ganze Prozessgruppe samt Browser.

Gerendert wird die Datei auf der Platte: die Vorschau folgt dem Speichern, nicht dem Tippen.
Ein zweiter Aufruf für dasselbe Deck zeigt nur den Tab. Ein Vorschau-PDF-Tab aus einer
früheren Sitzung nimmt `resumeMarpPreviews` über `source.txt` wieder auf (ein Versuch je
Tab). Ein alter `preview://deck.md`-Tab übergibt an die neue Vorschau und schließt sich
(`MarkdownView.handed_to_marp`).

## Export

Command `md_export_pdf` („Export to PDF") in `shortcuts.zig`, sichtbar im
Tab-Kontextmenü, im Editor-Kontextmenü, im Kontextmenü der Markdown-Vorschau und im
View-Menü. Die Kontextmenüs zeigen ihn nur bei Decks (`isMarpDeck` auf Buffer bzw.
Dateikopf). `exportMarpPdf` schreibt `deck.pdf` neben das Deck, öffnet es als Tab bzw. lädt
einen offenen Tab neu. Über das View-Menü geht der Befehl auch bei Nicht-Decks; fehlt
`marp: true`, kommt ein Fehlerdialog statt einer Datei.

## Prüfen

```bash
python3 scripts/e2e_marp_pdf.py            # headless, deckt Export und Vorschau ab
```

RPCs `marp_export_state` (`state`, `last`, `message`) und `marp_preview_state` (dazu
`previews` mit `md`, `pdf`, `watching`). Fixture: `scripts/fixtures/marp_test.md` (sieben
Folien, Folie 2 mit `![bg right:40% contain](marp_skizze.svg)`). Die E2E prüft Einrichtung,
Export, Seitenzahl, Skizzentext im PDF, Vorschau im Cache, Neuladen nach dem Speichern, eine
Vorschau je Deck und das Ende des Watch-Prozesses mit dem Tab.

Den Browser-Rückfall deckt die Suite nicht ab (121 MB): von Hand prüfen, indem zid mit
`PROGRAMFILES`, `PROGRAMFILES(X86)` und `LOCALAPPDATA` auf einen leeren Ordner startet
(Windows); dann findet marp-cli keinen Browser. Vorher normal bauen, der Zig-Cache
braucht das echte `LOCALAPPDATA`.

**Beschriftung:** `TabBarState.openFile` erkennt Vorschau-PDFs am Pfad
(`marp_cli.isPreviewPath`: `…/preview/<16 Hex>/<name>.pdf`) und merkt sich das Deck aus
`source.txt` (`Tab.preview_source`). `tabLabel` zeigt dann „Preview: deck.md“ wie bei der
Markdown-Vorschau; bei gleichem Namen steht der Ordner des Decks davor, nicht der
Hash-Ordner. Markdown- und Marp-Vorschau zählen dabei als eine Art (`Tab.isPreview`).
`ui_state` liefert je Tab `label`.

Wie die Markdown-Vorschau folgt auch diese dem Speichern (mit Autosave nach 1 s Ruhe
praktisch dem Tippen); anders als jene zeigt sie beim Öffnen nicht den ungespeicherten
Buffer, sondern die Datei.
