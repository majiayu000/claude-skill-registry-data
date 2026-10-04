---
name: lsp
description: >
  LSP-Anbindung in zid (zls): Protokoll, Client, Sprung zur Definition, Messwerte. Use when touching src/lsp/*, ensureLsp, lspGotoDefinition, or scripts/e2e_lsp.py.
---

## LSP (zls): Sprung zur Definition

- **Aufbau:** `src/lsp/lsp_proto.zig` (reine Logik, unit-getestet: `Content-Length`-Rahmen,
  Request/Notification, `file://`-URIs, `firstLocation` für Location | Location[] | LocationLink[],
  `parseMessage`) und `src/lsp/lsp_client.zig` (Prozess über stdio, Reader-Thread, `id → Methode`,
  Antworten als `TaskResult` `lsp_definition` mit dem Ergebnis-JSON; Server-Requests werden sofort
  mit `result: null` beantwortet).
- **Start:** lazy beim ersten F12/Ctrl+Klick in einer `.zig`-Datei (`UI.ensureLsp`): `ZLS_PATH`,
  sonst `~/.local/bin/zls`, sonst `zls` im PATH; `ZID_LSP=off` schaltet ab. Root ist
  `current_directory`. Solange `initialize` nicht beantwortet ist, springt der Editor per Textmuster
  (`gotoDefinitionLocal`). RPC `ui_state.lsp` = off/starting/ready/failed.
- **Ablauf:** `CodeEditor.definition_hook` (vom UI in `ensureEditorHooks` jedem Editor gesetzt, weil
  der UI-Zeiger erst nach `init` stabil ist) → `lspGotoDefinition`: Dokument per didOpen/didChange
  (Full Sync, nur vor Anfragen, nicht pro Tastendruck) synchronisieren, `textDocument/definition`
  mit Zeichenindex (`charIndexAt`, Codepoints statt Anzeigespalten). Antwort in
  `handleLspDefinition`: gleiche Datei → `jumpTo`; andere Datei → `openFileAs` + `lsp_goto`, das
  `applyLspGoto` in `update()` ausführt, sobald der Tab aktiv und der Buffer geladen ist (max. 240
  Frames); leeres Ergebnis → lokale Suche.
- **Gemessen (zls 0.15.1, Zig 0.15.2):** erste Definition im frischen Projekt ~12 s (zls analysiert
  std), danach sofort. Hover/Completion sind im Client nicht angebunden (Methoden vorgesehen).
- E2E `python3 scripts/e2e_lsp.py` (braucht zls): F12 auf `a.helper()` öffnet `a.zig` mit Cursor auf
  `helper`. Hinweis: der RPC `open_folder` lädt nur den Explorer neu, `current_directory` bleibt das
  Startverzeichnis; zls bekommt im E2E deshalb das Projekt als Root.
