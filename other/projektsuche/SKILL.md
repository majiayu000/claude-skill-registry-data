---
name: projektsuche
description: Suche und Ersetzen im ganzen Projekt (Ctrl+Shift+F / Ctrl+Shift+H) in zid — ripgrep als Unterprozess, Treffer je Datei in der Sidebar im VS-Code-Stil, Ersetzen auf Byte-Ebene, ungespeicherte Buffer, Auslieferung von rg. Use when touching src/ui/project_search.zig, src/ui/search_view.zig, sidebar_mode .search, startProjectSearch/replaceInFile/openSearchMatch in src/ui/mod.zig, RPC search_state, scripts/e2e_project_search.py, or the ripgrep bundling in packaging/.
---

# Suche im Projekt

## Aufbau

- `src/ui/project_search.zig` (eigenes Test-Root, `zig build test-search`): rg-Argumente
  (`buildArgs`), JSON-Zeilen (`parseMatch`), Ergebnisbaum (`Results`, eine Zeile je Treffer
  wie VS Code, Dateien nach Pfad sortiert), Vorschau (`preview`), Ersetzen auf Byte-Ebene
  (`applyEdits`, `error.Stale` bei geänderter Datei) und der Hintergrund-Lauf (`Runner`).
- `src/ui/search_view.zig`: Panel in der Sidebar (`sidebar_mode = .search`,
  `sidebar_focus = .search`), Felder über `line_edit`, Umschalter über `tooltip.iconButton`,
  virtualisierte Liste mit `scrollbar.zig`. Gibt `Action`s zurück; Dateizugriffe macht
  `UI` (`runSearchAction`, `replaceInFile`, `openSearchMatch`).
- **Windows-1252-Dateien** (kein gültiges UTF-8, wie der Editor sie liest): `replaceInFile`
  kodiert den Ersatztext nach 1252, sonst stünden UTF-8-Bytes mitten in der Datei; kennt 1252
  ein Zeichen nicht, bleibt die Datei unberührt (`ReplaceOutcome.unencodable`, eigener Toast).
  Die Trefferliste dekodiert solche Zeilen nur zur Anzeige, Offsets bleiben an den rohen Bytes.
  Ein UTF-8-Suchbegriff mit Umlauten findet in 1252-Dateien nichts (rg sucht Bytes). E2E
  `python3 scripts/e2e_encoding.py`.
- Sprung zum Treffer über `lsp_goto` mit `select_to` → `CodeEditor.jumpToSelect`. Spalten
  aus `find_ops.colOfByte` (Tab = 4), wie die Ctrl+F-Suche.

## Warum rg und nicht selbst suchen

VS Code, Neovim/telescope und flow rufen `rg --json` auf, Helix bindet ripgreps Crates ein.
rg durchsucht das zid-Repo (23 000 Dateien) in 0,04 s, mit einem Kern in 0,32 s: eine eigene
Suche müsste parallel laufen, SIMD nutzen und `.gitignore` vollständig auswerten. Schalter
wie VS Code: `--hidden --glob=!.git --no-require-git --crlf`, Groß/Klein Unicode-fähig
(„äpfel“ findet „Äpfel“, `find_ops` im Editor kann das nicht).

## Regeln

- **`-r` liefert den Ersatz je Treffer.** Mit Ersetzen-Text sucht rg mit `-r` und schreibt
  pro Teiltreffer `replacement` samt Gruppen (`$1`). Ohne Regex ist der Ersatz wörtlich, `$`
  wird deshalb zu `$$`. Lief die Suche noch ohne `-r` und Regex ist an, sucht
  `replaceReady` erst neu, statt den Rohtext einzusetzen.
- **Nach jedem Ersetzen neu suchen.** Die Byte-Offsets der übrigen Treffer derselben Datei
  stimmen nach dem Schreiben nicht mehr. Die alte Liste bleibt stehen, bis der neue Lauf
  etwas liefert (`pending_clear`, `Runner.hasOutput`), sonst flackert sie.
- **Ungespeicherte Buffer:** rg durchsucht sie über stdin statt der Datei (eigener
  Schreib-Thread, sonst blockieren volle Pipes). Ersetzen lässt sie aus und meldet das per
  Toast; offene, unveränderte Tabs laden den neuen Inhalt über `reloadFileFromDisk`.
- **rg fehlt:** unter POSIX gelingt `spawn` schon nach dem fork, erst `waitForSpawn`
  meldet `FileNotFound`, und `wait` räumt danach nicht auf (`spawnChecked`). Die Meldung
  steht dann im Panel.
- Trefferlimit 20 000 (VS Code `DEFAULT_MAX_SEARCH_RESULTS`), danach wird rg beendet.
  Suche beim Tippen nach 300 ms Pause. `wantsFrameSoon` hält den Fenster-Loop wach, solange
  gesucht wird.
- Dateien werden erst in `rebuildRows` sortiert und neu indiziert; beim Einfügen sortiert
  zu halten war bei tausenden Dateien quadratisch.

## Auslieferung von rg

- Suchreihenfolge (`UI.rgPath`, im Log `search: rg = …`): `ZID_RG_PATH`, neben dem Binary
  (Windows-Zip), `../libexec/zid/rg` (Linux-Tarball), sonst PATH.
- Tarball (`packaging/build-release.sh`) und Windows-Zip (`windows-release.yml`) laden
  ripgrep 15.2.0 mit fester Prüfsumme und legen `ripgrep-LICENSE-MIT` dazu; `.deb`, `.rpm` und
  Arch-Paket übernehmen es nach `/usr/libexec/zid/rg`. Nur COPR hängt an `ripgrep` von Fedora (aktuell).
- **rg ≥ 14 für Regex-Ersetzen:** rg 13 (Debian 12, Ubuntu 22.04, Leap 15.6) schreibt kein
  `replacement` ins JSON. `replaceReady` lehnt Regex-Ersetzen dann mit Toast ab
  (`Results.missingReplacement`), statt `$1` wörtlich einzusetzen.

## Testen

- `zig build test-search` (rg-Tests überspringen sich ohne rg).
- `python3 scripts/e2e_project_search.py`: Fixture unter `tmp/e2e_project_search`, RPC
  `search_state` (Felder, Optionen, Meldung, erste 300 Zeilen mit Vorschau und Ersatz).
  Zeilenaktionen `IDI("ps_act", zeile * 4 + aktion)`, Aktion 0 = Replace, 1 = Dismiss.
  Der letzte Schritt sucht im zid-Repo nach „e“: Limit, keine Clay-Fehler, Layout < 50 ms.
