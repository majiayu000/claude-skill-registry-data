---
name: git-views
description: >
  Git-Ansichten in zid im VS-Code-Stil: Diff-Editor, Timeline, Source Control Graph, Multi-File-Diff, Changes mit Commit/Sync/Publish. Use when touching src/git/*, git_diff_view.zig, git_commit_view.zig, scm_*_view.zig, timeline_view.zig, taskGit* in git_worker, or scripts/e2e_git_diff.py, e2e_timeline.py, e2e_scm_*.py.
---

## Git-Ansichten: gemeinsame Bausteine

- Repo-Verlauf zeigt der Source Control Graph, Datei-Verlauf die Timeline im Explorer; es gibt
  keinen eigenen History-Tab.
- `git_worker.frame`/`unframe`/`splitKey`: Worker-Ergebnisse als `<schlüssel>\n<text>`, bei
  Commit-Anfragen `\x1f<hash>` im Schlüssel, damit veraltete Antworten erkannt werden. Fehler von
  git kommen als `*_error`-Tag mit stderr als Text, nie als Task-Fehler (`framedResult`).
- `src/git/git_list.zig` (Modul `git_list`, unit-getestet): `visibleRange`, `scrollToShow`,
  `clampScroll` für virtualisierte Listen mit fester Zeilenhöhe (Timeline, Graph).
- Alle git-Aufrufe laufen mit `core.quotepath=off`.
- **Beenden bricht laufende git-Prozesse ab** (`git_worker.killRunning`, in main.zig vor
  `scheduler.deinit`), sonst hält ein langsamer `git log` einen Worker über die 2 s Wartezeit
  des Schedulers hinaus fest. Unter Windows laufen die Prozesse in einem Job-Objekt, weil
  `bin\git.exe` nur ein Launcher für `mingw64\bin\git.exe` ist und `TerminateProcess` auf den
  Launcher den echten git weiterlaufen lässt. Unter Linux startet git mit
  eigener Prozessgruppe (`pgid = 0`), `kill(-pid)` trifft auch Hooks, die sonst die
  stderr-Pipe offen hielten. E2E `python3 scripts/e2e_git_shutdown.py`: ein
  `core.fsmonitor = sleep 30` im Fixture lässt `git status` hängen, zid muss sich in unter
  2 s ohne zurückgelassenen Worker beenden. Ein so abgebrochener Aufruf ist kein Fehler:
  `taskGitStatus`/`runGitCwd` geben bei `isStopping()` `error.Canceled` zurück, das der
  Scheduler nicht loggt; der Test verlangt ein Log ohne `error(`-Zeilen.
- Branch über `symbolic-ref --short -q HEAD` (geht auch ohne ersten Commit), nur bei
  losgelöstem HEAD `rev-parse --abbrev-ref HEAD`.
- **Fremde Repos („detected dubious ownership“):** Gehört das Repo einem anderen Benutzer
  (Netzlaufwerk, anderes Konto), verweigert git jeden Befehl. `taskGitStatus` meldet dann
  `git_unsafe_repo` mit dem Wert, den git selbst für `safe.directory` vorschlägt
  (`unsafeRepoDirectory`, wörtlich übernommen: auf Windows-Netzlaufwerken ist das
  `%(prefix)///host/…`, aus dem Projektpfad nicht sicher ableitbar). `UI.handleUnsafeRepo`
  fragt wie VS Code „Manage Unsafe Repositories“ nach, je Wert einmal pro Sitzung
  (`unsafe_repo`), sonst käme die Rückfrage nach jeder Dateiänderung. Ja führt die Aktion
  `trust_repo` aus (`config --global --add safe.directory`), danach laden Status und Branch
  (`git_branch_wanted`) neu. Bewusst nicht still per `-c safe.directory`: die Prüfung
  verhindert, dass die `.git/config` eines fremden Repos (`core.fsmonitor`) beim automatischen
  `git status` Programme startet. Die übrigen Tasks loggen nur eine Zeile (`error.GitUnsafeRepo`).
  E2E `python3 scripts/e2e_unsafe_repo.py`: `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` stellt den
  fremden Besitzer nach, `GIT_CONFIG_GLOBAL` hält die Benutzer-Config heraus.
- E2E: RPC `git_diff_state` liefert den Diff-Editor des aktiven Tabs (`view: "diff"`), JSON vom
  Main-Thread pro Frame gespiegelt (`snapshotGitViews`, mit `timeline_state` und `scm_state`).

## Diff-Editor im VS-Code-Stil (Tab `git-diff://…`)

- Vorbild ist VS Codes Diff-Editor, Standardwerte aus `src/vs/editor/common/config/diffEditor.ts`:
  Automatic-Layout (nebeneinander ab 900 px, sonst untereinander), `+`/`−`-Markierung, unveränderte
  Bereiche standardmäßig sichtbar, eingeklappt mit Kontext 3 / Minimum 3. Titel wie
  `resolveTimelineOpenDiffCommand`: `name (eltern) ↔ name (commit)`, Wurzel-Commit gegen den leeren
  Baum `4b825dc`. Kürzel wie VS Code: Alt+F5 / Shift+Alt+F5 (`diff_next_change`/`diff_prev_change`),
  Umschalter „Toggle Collapse Unchanged Regions“ und „Toggle Inline View“ in der Werkzeugleiste.
- Aufbau: `src/git/git_diff.zig` (Modul `git_diff`, unit-getestet: Tab-Pfad mit 0x1f-Feldern
  Commit/Eltern/Repo/Pfad/alter Pfad, Hunks aus `git show -U0 -M`, Ausrichtung je Layout,
  `collapse`, `innerChange`, `columnSlice`, `DiffState`), Worker `taskGitFileDiff` (alter Inhalt
  `<eltern>:<alter pfad>`, neuer `<commit>:<pfad>`, fehlende Seite leer), Ansicht
  `src/ui/git_diff_view.zig`. Die Zeilen-Ausrichtung übernimmt git (Hunks), zid berechnet keinen Diff.
- Beide Seiten nutzen den Tree-sitter-Highlighter wie die Markdown-Codeblöcke; Hälften sind
  `.percent(0.5)`, weil feste Breiten aus dem Vorframe im neuen Pane den Container aufziehen.
- Binär und UTF-16 (`file_types.looksBinary` auf einer der Seiten, `GitDiffView.binary`): nur
  der Hinweis wie VS Code, keine Zeilen, kein Highlighter — sonst ginge je Zeile ungültiges
  UTF-8 an den Shaper. Im Multi-File-Diff eine Hinweiszeile je Abschnitt. RPC
  `git_diff_state.binary`.
- Kein gültiges UTF-8 (ASP-Dateien in Windows-1252): `taskGitFileDiff` wandelt beide Seiten
  mit `git_diff.toUtf8` als ganze Datei aus Windows-1252 um. Ein Byte ergibt ein Zeichen, die
  Zeilen und damit die Hunk-Nummern bleiben gleich. RPC `git_diff_state.new_head` zeigt die ersten
  drei neuen Zeilen.
- Tab-Pfade enthalten 0x1f: RPC-JSON immer über `std.json.Stringify` schreiben (`ui_state.tabs`).
- E2E `python3 scripts/e2e_git_diff.py` (öffnet den Tab per `open_file` mit gebautem Pfad), Zustand
  über `git_diff_state`.

## Timeline im Explorer (VS-Code-Stil)

- Abschnitt „TIMELINE“ unter dem Dateibaum (`sidebar` = Explorer + `timeline_view.zig`), anfangs
  eingeklappt wie VS Code, Auf-Zustand in `user_state` (`timeline_expanded`). Quellen:
  `timelinePane.ts` (Zeitspalte, ausgeblendete gleiche Zeit, Meldungen, Pin/Refresh nur beim
  Überfahren), `timelineProvider.ts` (Label = erste Nachrichtenzeile, Autor als Beschreibung,
  `previousRef` = nächstälterer Commit **der Datei**, beim ältesten der leere Baum), `hover.ts`,
  `base/common/date.ts` (`fromNow`-Kurzformen), `git.timeline.date` = committed.
- Logik in `src/git/git_timeline.zig` (Modul `git_timeline`, unit-getestet), Worker `taskGitTimeline`
  (`git log --follow --numstat`; `--shortstat` mit `--name-only` liefert keine Zahlen, `%p` ist in
  deutscher Locale leer → 24 h). Klick öffnet den Diff-Editor (`openGitDiff`), Rechtsklick
  `timeline_menu_items`. Die Hunks kommen dafür aus `git diff <voriger Datei-Commit> <commit>`.
- Folgt dem aktiven Tab (Text, Bild, PDF, Binär, Vorschau-Quelle); Diff-Tabs lassen die Timeline
  stehen, weil ihr Pfad der historische Name ist. Geladen wird nur aufgeklappt; Dateiereignisse (git-status-Debounce) laden neu.
- „File History“ im Explorer-, Tab- und Editor-Kontextmenü (`file_history`, `file_history_entry`)
  stellt die Timeline wie VS Code `files.openTimeline` auf diese Datei: aufgeklappt, angepinnt,
  ohne Tab zu öffnen (`Timeline.show`). Aus dem Editor-Menü läuft das über `pending_file_history`
  in `update()`, nie im Render-Pfad: `show` gibt den Log frei, auf den Clay-Texte des Frames zeigen.
  Pin lösen folgt sofort dem aktiven Tab (`resetTimelineFollow`).
- Tastatur nach Klick in Kopf oder Liste (`sidebar_focus = .timeline`): ↑↓/PgUp/PgDn/Home/End
  wählen, Enter öffnet den Diff wie ein Klick, F5 lädt neu, Escape gibt den Fokus ab.
- E2E `python3 scripts/e2e_timeline.py` (Fixture-Repo mit festen Commit-Zeiten), RPC `timeline_state`.

## Source Control Graph und Multi-File-Diff (VS-Code-Stil)

- Ctrl+Shift+G schaltet die Sidebar auf Source Control (`UI.sidebar_mode`), Ctrl+Shift+E zurück.
  Kopf „SOURCE CONTROL GRAPH“ mit Filter „Auto“ und Refresh; Commit-Zeile = Graph, Betreff, Autor,
  Badges der gefilterten Referenzen; Klick klappt die Dateien auf, Klick auf eine Datei öffnet den
  Diff-Editor, Rechtsklick `graph_menu_items`, Inline-Aktion und Menü „Open Changes“ öffnen den
  Multi-File-Diff (`git-commit://…`, Titel „kurz - betreff“ wie `git.viewCommit`). Am Listenende
  lädt die nächste Seite automatisch (`scm.graph.pageOnScroll`, 50 je Seite).
- **Tastatur:** Klick in die Sidebar oder Ctrl+Shift+G setzt `UI.sidebar_focus = .scm`; dann wählen
  ↑↓/PgUp/PgDn/Home/End Zeilen (`View.moveSelection`), Enter/Leertaste klappt Commits auf bzw.
  öffnet die Datei im Diff-Editor (`activateSelected`), ←/→ klappen zu/auf, F5 lädt neu. Keine
  Taste und kein Zeichen erreicht den Editor; Escape, Klick anderswo, Tab-Öffnen oder Pane-Wechsel
  geben den Fokus ab. Gleiches Modell für die Timeline (`.timeline`, `Timeline.moveSelection`).
- Quellen: `scmHistory.ts` (Bahnen und Zeichnen, 1:1 portiert in `src/git/git_graph.zig`),
  `scmHistoryViewPane.ts` (Zeilen, Badges `scm.graph.badges = filter`), `historyProvider.ts`
  (Referenzen, Filter Auto = Branch + Upstream + Basis), `git.ts` (`--topo-order --decorate=full
  --shortstat --diff-merges=first-parent`), `diffEditorItemTemplate.ts` (Multi-Diff: unveränderte
  Bereiche eingeklappt, Status R/D/A, Klappknopf je Datei).
- Daten in `src/git/git_scm.zig` (Modul `git_scm`, unit-getestet: Referenzen, Filter, Log, Dateien,
  Zeilen, Load More), Worker `taskGitGraphLog`/`taskGitCommitChanges`, Ansichten
  `src/ui/scm_graph_view.zig` und `src/ui/git_commit_view.zig` (jede Datei ein `GitDiffView`,
  Inhalt lädt erst, wenn der Abschnitt sichtbar wird).
- **Graph zeichnen ohne Rundungen im Renderer:** gerade Linien sind Rechtecke, Bögen und Kreise je
  ein kleines SVG mit eigenem Pfad. Das ist Absicht: Der Rasterizer füllt nach Even-Odd (mehrere
  Formen in einem Pfad schneiden Löcher) und der Atlas rastert höchstens vier neue Formen pro
  Durchgang — als eigene Formen je Radius und Quadrant werden sie wiederverwendet.
- **Graph-Log ohne `--shortstat`**: auf einem Netzlaufwerk mit losen Objekten kostet es je Seite
  35–50 s statt 2–6 s. `Commit.stat` ist ein `StatState` (unknown/loading/failed/loaded); das Überfahren
  einer Zeile fordert die Zahlen dieses einen Commits an (`View.requestStat`, Worker
  `taskGitCommitStat` mit `git_scm.statArgs`), die Hover-Karte zeigt bis dahin „Loading
  changes…“. E2E in `e2e_scm_graph.py` (`scm_state.commits[].stat`). Der Rest der Wartezeit ist
  `--topo-order`: git liest dafür den ganzen Verlauf, bevor es die erste Zeile ausgibt.
- `git_worker.FieldsParam` trennt Felder mit 0x1e, weil Schlüssel selbst 0x1f enthalten
  (`graph<generation>\x1f<hash>`); `generation` verwirft Ergebnisse von vor einem Refresh.
- E2E `python3 scripts/e2e_scm_graph.py` (Fixture mit Remote, Merge, Tag und 55 Commits Vorlauf),
  RPC `scm_state`.

### Changes-Bereich mit Commit (über dem Graphen)

- Kopf „SOURCE CONTROL“ (Commit, Sync Changes bzw. Publish Branch, Refresh beim Überfahren;
  VS Code hat statt Sync ein „…“-Menü mit Pull/Push/Fetch/Sync), mehrzeiliges Eingabefeld
  (`EditBuffer` mit Zeilenfunktionen `moveUp/moveDown/moveLineHome/moveLineEnd/setCursorAtLine`,
  Enter = neue Zeile, Ctrl+Enter = Commit, wächst bis `INPUT_MAX_LINES` = 6 wie
  `scm.inputMaxLineCount`, danach scrollt es zur Cursorzeile; Platzhalter `Message (Ctrl+Enter to
  commit on "<branch>")`), großer Knopf wie `scm.showActionButton`: „Commit“ solange Änderungen da
  sind, sauber ohne Upstream „Publish Branch“ (`push -u origin <branch>`), sauber und voraus oder
  zurück „Sync Changes M↓ N↑“ (Zähler nur wenn > 0, wie `actionButton.ts`; Aktion `sync` = `pull`,
  dann `push`, VS Code `git.sync`; Upstream/Vorsprung/Rückstand aus `# branch.upstream` und
  `# branch.ab`). Kein `git.rebaseWhenSync`, kein Autofetch: `behind` ist erst nach einem Fetch
  bekannt. Einzelne Push-/Pull-Knöpfe gibt es wie in VS Code nicht. Gruppen „Merge
  Changes“ (nur bei Konflikten), „Staged Changes“ (nur wenn nicht leer), „Changes“ (immer,
  untracked darin = `git.untrackedChanges: mixed`). Zeile: Name, Ordner gedimmt, rechts Buchstabe
  in `theme.git_*` (VS Code `gitDecoration.*`), gelöscht durchgestrichen. Aktionen nur beim
  Überfahren (Reihenfolge wie `package.json`): Datei öffnen, Stage/Unstage, Discard; Köpfe:
  Stage All / Unstage All / Discard All. IDs `sc_act` mit Index `zeile * 8 + RowAction`.
- Das Eingabefeld ist ein `CodeEditor` mit `font_size = 16` und `line_pad = 6` (Zeilenhöhe
  `lineHeight()` = `INPUT_LINE_HEIGHT` 22); mit den Editor-Vorgaben (24 + 16) schneidet das Feld
  die untere Hälfte der Buchstaben ab.
- Daten `src/git/git_changes.zig` (Modul `git_changes`, unit-getestet): Gruppen aus der rohen
  porcelain-v2-Ausgabe, die `taskGitStatus` hinter 0x1c mitliefert (`splitStatusPayload`), Buchstabe/
  Farbe/Hover-Text/Durchstreichen wie `Resource` in `repository.ts`, Diff-Spec je Zeile
  (Staged = HEAD↔Index `index_ref`, Changes = Index↔Arbeitskopie `git_diff.worktree_ref`,
  Untracked = leerer Baum↔Arbeitskopie mit `syntheticAddHunk`), Auswahl, Discard-Rückfragen.
  Ansicht `src/ui/scm_changes_view.zig`, Aktionen laufen in `UI.runScmAction`.
- Worker `taskGitAction` (`FieldsParam`: Aktion, Repo, Pfade bzw. Nachricht): `stage` = `add -A --`,
  `unstage` = `reset -q HEAD --`, `discard_tracked` = `checkout -q --`, `discard_untracked` =
  `clean -f -q --`, `commit` = `commit --quiet --file - --allow-empty-message` (Nachricht über
  stdin, `runGitCaptureStdin`), `commit_all` = vorher `add -A` (VS Code smartCommit), `push` =
  `push --quiet` plus weitere Felder als Argumente (Publish Branch), `sync` = `pull --quiet`,
  bei Erfolg `push --quiet` (scheitert der Pull, etwa Konflikt oder divergiert ohne
  `pull.rebase`, kommt gits Meldung und kein Push). Fehler kommen
  als `git_action_error` mit stderr → Toast. Ergebnis setzt `git_status_wanted`, main.zig lädt
  den Status über den Debounce; nach Commit und Sync auch Graph und Timeline.
- **Generate Commit Message** (Sparkle rechts oben im Feld, wie VS Code Copilot / Zed): Worker-
  Aktion `commit_diff` liefert den gestagten Diff, sonst Arbeitskopie plus untracked Dateien;
  `git_changes.commitPrompt` (Conventional Commits, 72 Zeichen, Body, nur die Nachricht; Diff auf
  24 KiB gekappt) geht blockierend über `ai_worker.taskChatCompletion` mit eigenen Tags
  `ai_commit_message`/`_error` (`ChatParams.reply_tag`), damit die Antwort nicht im Chat landet;
  `cleanGeneratedMessage` entfernt Zäune, Anführungszeichen und Label. Ohne KI (`--ai=off`,
  Agent nicht `ready`) nur ein Toast. Kein Streaming, kein eigener Systemprompt-Schalter.
- Commit-Verhalten wie `smartCommit`: leere Nachricht → Hinweis unter dem Feld; keine Staged
  Changes → Rückfrage „stage all and commit“; nichts geändert → Toast. Discard fragt immer
  (Texte und Knöpfe aus `commands.ts`: Discard File / Restore File / Delete File / Discard All n
  Files). Rückfragen laufen über `active_dialog` mit `scm_pending`.
- Fokus: Ctrl+Shift+G setzt `sidebar_focus = .commit_input`; Tab wandert Feld → Changes-Liste →
  Graph → Feld. In der Liste ↑↓/PgUp/PgDn/Home/End, Enter öffnet den Diff bzw. klappt den Kopf,
  Entf = Discard mit Rückfrage, Escape gibt ab. Buchstaben gehen nur ins Feld.
- E2E `python3 scripts/e2e_scm_changes.py` (Fixture: geändert, gelöscht, untracked; stage, Diffs,
  unstage, discard mit Dialog, commit mit Rückfrage, Publish, Sync mit Vorsprung, Sync holt fremde
  Commits aus einem zweiten Klon über den großen Knopf nach Fetch und über den Kopf-Knopf ohne
  Fetch, Tastatur), Zustand in `scm_state.changes`. Das Skript baut **nicht** selbst, sondern
  startet `zig-out/bin/zid` direkt — vorher `zig build`, sonst testet es den alten Stand.
  Der RPC `open_project` wechselt den Projektordner wie der Dialog (Explorer, Watcher, Branch,
  git status), `open_folder` lädt nur den Explorer.
