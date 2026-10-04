---
name: llm-local
description: >
  Lokales LLM in zid: KI-Chat über llama-server, Selbsteinrichtung von Engine und
  Modell, Engine- und Modellwahl, gepinnte Engines unter engines/, Messregeln aus
  llm-bench/, Agent-Werkzeuge (Tool-Calling, Bestätigung, Kontextgrenze), Kürzel-Werkzeug
  und Verlauf kopieren.
  Use when working on the AI chat, `src/ai/*`, `src/ui/agent_actions.zig`, agent tools,
  scripts/e2e_ai_*.py, llama-server startup, model or device
  selection, streaming replies, `engines/`, `models/`, `llm-bench/`, or when
  benchmarking or comparing local models.
---

# Lokales LLM in zid

zid spricht ausschliesslich mit llama-server und nutzt nur lokale Backends; Cloud-Anbieter
(Claude, OpenAI) hat der Projektinhaber ausgeschlossen.

## Backend-Wahl beim Start

`UI.init`, sofern nicht `--ai=off`. Standard ist der llama.cpp-Vulkan-Build
`engines/llama.cpp-vulkan/build/bin/llama-server` mit
`models/gemma-4-E2B-it-Q4_0.gguf` (ggml-org, sha256 `8e30dff3…`), beides relativ zur
Repo-Wurzel (`src/ai/paths.zig`, unit-getestet: Wurzel aus `<repo>/zig-out/bin` der
ausführbaren Datei, sonst das Arbeitsverzeichnis; nichts über `$HOME`). Fehlt der Build,
kommen Engine und Modell aus dem Datenverzeichnis, das zid sich selbst einrichtet
(`src/ai/selfsetup.zig`: Knopf im Chat, llama.cpp `b11062` und das Modell von ggml-org
nach `<AppData>/zid` bzw. `~/.local/share/zid`). `LLAMA_SERVER_PATH` und
`LLAMA_MODEL_PATH` überschreiben beides.

**Warum gemma4-E2B Q4_0:** gleiche Werkzeugwahl wie Qwen3-4B-Instruct-2507 (10/10 in
`bench/agent_eval.py`, `e2e_ai_tools` grün), aber auf beiden Referenzmaschinen schneller:
27.6 gegen 19.3 tok/s auf der P1000 des Laptops (i7-8850H, 4 GB VRAM, Modell passt ganz
hinein), 18.2 gegen 11.9 tok/s auf der CPU des i5-13500T. Erstes Delta im Chat 8 s auf der
P1000 (Qwen3: 15 s). Antwortet auf deutsche Fragen deutsch (`bench/probe.py`, Chat-Suite).
Messreihen: `llm-bench/results/windows-i5-13500T-gemma4-vs-qwen3.md`,
`llm-bench/results/linux-p1000-gemma4-vs-qwen3.md`.

## llama-server starten

`agent.zig` prüft Engine- und Modelldatei, fragt `--list-devices` ab und wählt per
`device_select.zig` (unit-getestet) eine diskrete GPU mit mindestens 3 GB, sonst CPU
(`-dev none -t N`). **iGPUs werden übersprungen**, sie liefern laut Bench ein Drittel
der CPU-Leistung.

Argumente: `--jinja -c 8192 --log-disable --chat-template-kwargs {"enable_thinking":false}`,
auf GPU zusätzlich `-dev VulkanN -ngl 99`. Port 8080 (`default_llama_port`).
Ohne `-dev` landet das Modell womöglich auf der iGPU, ohne `--jinja` stimmt das
Qwen3-Chat-Template nicht. `enable_thinking=false` ist für Qwen3-Instruct wirkungslos,
schaltet aber bei gemma4 das Denken ab; `--reasoning-budget 0` tut das nicht (gemma4 denkt
dann im Antwortkanal weiter, 0/10 Werkzeugwahl).

Unter Windows heisst die Engine `llama-server.exe` (`paths.exe_suffix`); ohne Endung schlägt
der Existenztest fehl und zid hält die Engine für nicht vorhanden.

**Werkzeug-Prompt klein halten.** Das `command`-Werkzeug trägt die 106 Kommandos nur als
Enum; eine Liste mit Label und Kürzel im Text kostete 1000 Token und auf CPU 20 s vor dem
ersten Delta (2392 → 1362 Token, 45 → 22 s auf dem i5-13500T) und liess gemma4
`open_folder` statt `command` wählen. Jeder Stream fordert `stream_options.include_usage`
an und loggt `usage: prompt_tokens=… prompt_ms=…`; vor Prompt-Änderungen vorher/nachher
ablesen. Messreihe: `llm-bench/results/windows-i5-13500T-gemma4-vs-qwen3.md`.

## Streaming und Zustand

`streamChatCompletion` (SSE, `stream: true`) schiebt jedes Delta per
`Scheduler.pushResult` als `ai_chat_delta`; der Chat zeigt die wachsende Antwort
(`stream_text`, Markdown wird bei neuem Text neu gebaut). Die finale Antwort kommt als
`ai_chat_reply`. **Escape** setzt `cancel_flag`, der Worker beendet den Stream
(`ai_chat_cancelled`), der Teiltext bleibt mit „(abgebrochen)".

**Kontextfenster voll:** Prompt und Antwort teilen sich `-c 8192`. Läuft die Antwort ans
Ende, meldet llama-server `finish_reason: "length"` (`agent.finishReason`); `endStream`
liefert dann `error.ReplyTruncated`. Der Worker zeigt den Teiltext mit „*(Antwort
abgeschnitten: Kontextfenster voll.)*“, ein abgeschnittener Werkzeugaufruf wird nie
ausgeführt (unvollständiges JSON), ohne Text erscheint eine Fehlermeldung. Kein
`max_tokens`: das würde lange `write_file`-Inhalte kappen. E2E
`python3 scripts/e2e_ai_truncated.py` (12 KB wiedergeben lassen, ~3 min).

`AgentStatus` (`none`, `initializing`, `ready`, `failed`) ist der echte
Verbindungszustand: Statuspunkt, Kopfzeile (`agentTitle`: Modell · Gerät) und
`sendMessage` hängen daran. Warmup schickt „ping" mit `max_tokens = 1`, ohne Limit
dauert der Start minutenlang.

Fehlen Engine oder Modell, lädt der Chat sie auf Knopfdruck selbst nach; nie synchron,
das blockiert den Start minutenlang (`selfsetup.zig` arbeitet im eigenen
Thread, der Fortschritt kommt aus der Grösse der `.part`-Datei).

## Chat-Eingabe ist der CodeEditor

`AIChatState.input_editor` mit `show_gutter = false`, `show_minimap = false`,
`compact_menu = true` und `word_wrap = true`. Enter sendet, Shift+Enter fügt eine Zeile
ein (`dispatchAction(.InsertNewline)`; die Keymap kennt Enter nur ohne Modifier). Das UI
reicht Shift/Ctrl/Alt an den Chat-Editor weiter, `applyThemeToEditors` färbt ihn mit.
Editor-Neuerungen gelten damit automatisch auch im Chat.

**Keine Unit-Tests für `ai_chat.zig`:** die Datei importiert CodeEditor und UI, also
kein eigenes Test-Root möglich. Logik dort klein halten.

**Codeblock-Antworten und zigdown:** endet der Text genau mit ``` ohne Zeilenumbruch,
erzeugt `handleLineCode` einen leeren Tag und greift auf `tag[0]` zu (Absturz, Submodul
nicht gepatcht). `chat_markdown.finishForParser` hängt deshalb immer einen Zeilenumbruch
an und schließt einen offenen Zaun.

## Prüfen

```bash
python3 scripts/e2e_ai_chat.py              # Warmup, erstes Delta, Escape, kurze Antwort
python3 scripts/e2e_ai_chat.py --only-off   # nur der --ai=off-Pfad
python3 scripts/e2e_ai_read_limits.py       # read_file 4–40 KB: richtig?, Dauer, Prompt-Token (JSON in tmp/)
python3 scripts/e2e_ai_read_limits.py 12000:last 12000:last   # einzelne Fälle wiederholen
```

Antworten streuen (Temperatur 0.7): Vorher/Nachher nie an einem Lauf entscheiden, sondern
denselben Fall mehrmals wiederholen und die Prompt-Token vergleichen. Gleiche Token heißen
gleiche Eingabe, dann ist ein anderer Ausgang Zufall.

RPC `chat_state`: Status, Detail, Titel, loading/initializing,
`streaming_len`, alle Nachrichten.

## Engines und Modelle

**Layout:** `engines/` ist ignoriert, kein Submodul. Ein lokaler
Build unter `engines/llama.cpp-vulkan/build/` (b10524 = `9ee9fc0`, `GGML_VULKAN=ON`,
derselbe Build für GPU und CPU) hat Vorrang; fehlt er, lädt die Selbsteinrichtung das
Release `b11062`. Wer lokal baut, klont llama.cpp selbst dorthin. `models/` hält alle GGUFs flach
(per `*.gguf` ignoriert, **nie committen**).

**BitNet ist nicht im Repo.** zid nutzt es nicht (braucht eine eigene gepinnte Engine ohne
Vulkan und einen Tokenizer-Override). Für Nachmessungen holt `llm-bench/setup/linux.sh`
die Engine gepinnt auf `01eb415` (Submodul `3rdparty/llama.cpp` auf `1f86f05` = b3962)
nach `engines/BitNet`, spielt `llm-bench/patches/bitnet-mad-const-y_col.patch` ein und lädt
`models/bitnet-b1.58-2B-4T/`.

**cmake brennt absolute Pfade ein.** Nach einem Umzug finden `llama-server` und
`llama-bench` ihre `libllama.so` nicht. `llm-bench/setup/fix-rpath.sh` schreibt die
RUNPATHs der Builds per patchelf auf `$ORIGIN`-relative Pfade um (Kopie patchen und
darüberschieben, weil ein laufender llama-server die Datei gemappt hält: „Text file
busy"). Nach jedem Neubau oder Verschieben erneut ausführen. Die Build-Verzeichnisse
selbst kann cmake nach einem Umzug nicht neu konfigurieren, ein Neubau muss von vorn
beginnen.

**`llm-bench/`** ist das Repo `bitnet-colibri-bench` als `git subtree`.
`results/*.md` sind Messprotokolle und werden nicht angefasst.

## Messregeln

Die drei BitNet-Regeln gelten nur, wenn BitNet per `llm-bench/setup/linux.sh` wieder
aufgebaut ist.

- **Die BitNet-Engine ist gepinnt, und das ist keine Vorsicht.** Der aktuelle Stand von
  microsoft/BitNet zeigt auf einen Fork-Branch, mit dem BitNet-b1.58-2B-4T unbrauchbar
  ist (Endlosschleife, Perplexity ×3,7, Werkzeugwahl 0/10) — bei unauffälligem
  Durchsatz. Vor jeder Messung:
  ```bash
  ./engines/BitNet/build/bin/llama-bench -m <i2_s.gguf> -p 8 -n 8 -r 1
  ```
  `I2_S - 2 bpw ternary` in der Modellspalte heißt brauchbar, `Q1_0` heißt nicht messen.
- **BitNet braucht `--override-kv tokenizer.ggml.pre=str:llama-bpe`** (dem GGUF fehlt
  das Feld; ohne Override zerfallen Werkzeugnamen, 8–9/10 wird zu 4/10). Nur für BitNet.
- **Feste Engine-Zuordnung:** BitNet i2_s nur auf der gepinnten BitNet-Engine (auf
  b10524 ist i2_s kaputt); Qwen3, Phi-4 und Gemma-3 nur auf b10524 (b3962 kennt die
  Architekturen nicht und hat kein taugliches Vulkan); Llama-3.2-3B läuft auf beiden und
  ist die Brücke. Zahlen nie ohne diese Verschiebung über die Engine-Grenze vergleichen.
- **Jede Zahl braucht drei Kennungen:** Engine-Commit, Submodul-Commit, Modell-sha256.
  Perplexity nur mit `llm-bench/bench/ppl-corpus.txt` bei `-c 512`.
- Entscheidungen des Projektinhabers und die Liste „nicht erneut aufrollen" stehen in
  `llm-bench/CLAUDE.md`.
- **`models/` hält nur das Standardmodell** gemma-4-E2B-it Q4_0 (ggml-org). Ein erneuter
  Vergleich mit anderen Modellen braucht den Download, Quelle und
  sha256 stehen in `llm-bench/results/` (Qwen3-4B-Instruct-2507: unsloth,
  `3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597`).

## Chat: Kürzel-Werkzeug und Verlauf kopieren

- Die Tastenkürzel stehen **nicht** im Prompt (das kostete 1000 Token). Der Agent holt sie
  über das Werkzeug `list_shortcuts` (`agent_actions.zig`), optional mit `filter`. Gemessen:
  gemma-4-E2B ruft es von selbst auf und beantwortet „Which key opens quick_open?" mit
  `Ctrl+P`; bei einer umschreibenden Frage („Datei-Schnellsuche") rät es trotz Liste
  gelegentlich daneben — das Werkzeug liefert `command`, `label` und `key`, das Übersetzen
  bleibt Sache des Modells.
- Markieren geht über Bubble-Grenzen: jede Nachricht ist eine eigene `MarkdownView`, beim
  Ziehen markiert `handleMouseMove` die Startnachricht ab dem Anker (`selectFromAnchorToEnd`),
  die dazwischen ganz (`selectAllContent`) und die zuletzt erreichte bis zur Maus
  (`selectFromStartTo`). `selectedText` verkettet alle markierten Nachrichten.
- Werkzeugergebnisse stehen als `✅ ok` bzw. `❌ Fehler` vor dem Namen. Das Zeichen allein
  genügt nicht: unter Windows greift die Emoji-Rückfall-Kette nicht, dort bliebe ein leeres
  Kästchen ohne Wort daneben.
- Ganzen Verlauf kopieren: Knopf `ai_copy_all` in der Kopfzeile oder Ctrl+Shift+C
  (`AIChatState.conversationText` als Markdown, `## Du` / `## AI` je Nachricht). Ctrl+C
  bleibt die markierte Bubble. Der Weg läuft über `UI.setClipboard`, damit `ui_state`
  ihn headless prüfen kann.

## Selbsteinrichtung der KI (`src/ai/setup.zig`, `download.zig`, `install.zig`, `selfsetup.zig`)

- Ein installiertes zid hat kein `engines/` und `models/` neben sich. Fehlt beides, lädt der
  Chat auf Knopfdruck llama-server (gepinnt auf `b11062`, Vulkan-Build) und
  `gemma-4-E2B-it-Q4_0.gguf` von ggml-org in `<AppData>/zid` bzw. `~/.local/share/zid`.
- Geladen wird in `<ziel>.part`, umbenannt erst am Schluss; eine abgebrochene Übertragung
  setzt per Range-Header auf. **`File.Writer` schreibt positional ab 0**: ohne `fw.pos = have`
  überschreibt die Fortsetzung die schon geladenen Bytes und die Datei wächst nie.
- Kein eigener zählender Writer: der müsste Zigs Pufferprotokoll bedienen (erst
  `w.buffer[0..w.end]`, dann `data`, Rückgabe = aus `data` verbrauchte Bytes). Ein Writer, der
  das nicht tut, meldet nie Fortschritt und `fetch` dreht sich endlos. Der Fortschritt kommt
  deshalb aus der Grösse der `.part`-Datei.
- Die Release-Archive sind unterschiedlich gebaut: Windows-ZIP flach, Linux-Tar mit
  `llama-<tag>/` davor (`install.stripComponents`).

## Agent-Werkzeuge: der Agent kann, was der Editor kann

- **Natives Tool-Calling** (OpenAI `tools`-Feld, `tool_calls` in der Antwort, `role: tool` zurück).
  Geprüft mit llama-server b10524 + Qwen3-4B + `--jinja`: funktioniert nicht-streamend
  und streamend (`delta.tool_calls` je Index zusammensetzen), das Modell nutzt Tool-Ergebnisse.
  Kein MCP, kein RPC:
  Agent und Editor sind derselbe Prozess; MCP wäre nur für externe Agenten interessant.
- **Definitionen** in `src/ai/tools.zig` (Modul `ai_tools`, unit-getestet): `command` (Enum aus
  `shortcuts.Command`, Beschreibung mit Label + Kürzel jedes Kommandos → jedes Menü/Kürzel ist
  automatisch Agent-Werkzeug), `open_file`, `read_file` (≤ 200 KB), `write_file`, `replace_text`,
  `list_files` (≤ 200 Einträge), `open_folder`, `find_in_editor`. `toolsJson` liefert das Schema,
  `parseEnvelope` die Aufrufe aus dem Worker-Ergebnis `{"content","tool_calls"}`.
- **Ausführung** auf dem Main-Thread in `src/ui/agent_actions.zig` (`UI.driveAgentTools` in
  `update()`): `command` → `executeCommand`; Dateien nur innerhalb von `current_directory`
  (`ai_tools.resolveInProject`, `..` und fremde absolute Pfade → `{"error": "outside the project"}`).
  Ergebnisse gehen als JSON in `tool`-Nachrichten. Ruft ein Modell einen Enum-Wert als
  Werkzeugnamen (`toggle_explorer` statt `command{name}`, kleine Modelle tun das), führt
  `agent_actions` ihn als Kommando aus (`ai_tools.commandFromToolName`) statt „unknown tool"
  zu melden.
- **Regeln in Code, nicht im Prompt** (Qwen3-4B hält Prompt-Regeln unzuverlässig ein, siehe
  replace_text-Umweg). Der Systemprompt nennt nur Rolle und "Pfade relativ zum Projekt".
  `ai_tools.choosePaneForFile` (unit-getestet) entscheidet für `open_file`: Chat nicht im
  aktiven Pane → dort öffnen; Chat aktiv und zweites Pane vorhanden → dort; sonst vertikal
  splitten (Chat oben, Datei unten). Danach geht der Fokus zurück zum Chat-Pane, man kann
  weiterschreiben. Dafür lädt main.zig Tab-Wechsel für **alle** Leaves
  (`UI.leavesWithPendingSwitch`; der Block biegt `active_pane` pro Leaf kurz um).
- `write_file`/`replace_text` auf eine offene Datei laden den Buffer und alle Editoren darauf
  neu (`UI.reloadFileFromDisk`: `setText`, `setLanguageFromPath`, `last_save = root`, Tabs
  gelten als gespeichert). Zed/VS Code lösen das Sichtbarkeitsproblem mit einem Chat-Dock
  neben den Editor-Panes; das bleibt eine Option, der Split reicht vorerst.
- **Bestätigung** über den normalen Dialog ("AI agent", Allow/Deny): `write_file` auf bestehende
  Datei; `replace_text`, wenn `old` ≥ halbe Datei ist (`replaceCountsAsRewrite`; Qwen umging so
  die write_file-Regel). Antwort wird in `update()` verarbeitet, nie im Dialog-Callback. Deny →
  `{"error":"the user denied this action"}` ans Modell. `close_tab`/`delete_entry` fragen über
  ihre bestehenden Dialoge. Max. 8 Werkzeugrunden pro Frage (`max_tool_rounds`).
- Anzeige: Assistant-Aufrufe als `🔧 name(args)`, Ergebnisse als `✅/⚠️ name → JSON…`.
- Kein `run_shell` (bewusst, erst mit Sandbox). Kein Diff-Review vor dem Schreiben (Zed zeigt
  Agent-Änderungen erst als Vorschlag); wäre der nächste Schritt nach dem Dock.
- **Kontextgrenze:** llama-server (`-c 8192`) kürzt nicht still, sondern antwortet HTTP 400
  `exceed_context_size_error` (gemessen: 24 017 Tokens abgelehnt; ein 8014-Token-Prompt
  brauchte auf der P1000 123 s). `agent.zig` macht daraus `error.ContextTooLong`, der Chat zeigt
  einen verständlichen Hinweis. Vorbeugend schickt `submitCompletion` nur das jüngste Stück der
  Historie, das in `history_budget_chars` (12 000 Zeichen) passt: `src/ai/history.zig` (`keepFrom`,
  unit-getestet) behält die laufende Runde (letzte Frage, Aufrufe, Ergebnisse) immer ganz, auch über
  dem Budget, und beginnt nie mit einem verwaisten `tool`-Ergebnis. Ein Ergebnis ohne Frage und
  Aufruf verwirft das Chat-Template, das Modell antwortet dann ohne jeden Kontext („What would you
  like to do?"). Die Anzeige im Chat bleibt vollständig.
- **`read_file` liefert den rohen Dateiinhalt, ohne JSON und ohne Kopf.** Als JSON-String sah das
  Modell `\n` und `\"` statt echter Zeilen (das gemma4-Template reicht den String unverändert
  durch); ein Kopf wie `path: …` galt ihm als erste Dateizeile (erste Zeile 0/3 statt 3/3). Roh
  spart 6–7 % Prompt-Token beim Ergebnis. Fehler bleiben `{"error":…}`, daran erkennt
  `pushToolResult` sie (Präfix, nicht Teilstring: Dateien dürfen `"error"` enthalten).
- **Zu große Werkzeugergebnisse werden erst nach der Ablehnung gekürzt:** `handleError` kürzt bei
  `ContextTooLong` das größte `tool`-Ergebnis der Runde (`ai_tools.shrinkToolResult`: Anfang auf
  zwei Drittel, höchstens 24 000 Bytes, an einer Zeilengrenze; am Ende die Zeile
  `[zid: file truncated: N bytes total, first M shown]`; JSON mit `content`-Feld wird im Feld
  gekürzt) und sendet neu, bis es passt. Was passt, geht ungekürzt raus; eine feste Grenze in
  `read_file` hätte Dateien gekappt, die ganz ins Fenster passen. Die Ablehnung kostet kaum Zeit.
  Messwerte P1000 (`python3 scripts/e2e_ai_read_limits.py`, erste/letzte Zeile aus N Bytes Zig-Code):
  Grundlast 1 366 Prompt-Token, 4 KB 2 628 Token und 20 s, 12 KB 4 974 Token und 47 s, 28 KB nach
  dem Kürzen 75 s (20 KB passte noch ungekürzt: 7 511 Token, 87 s, gemessen mit JSON-Ergebnis). Die „letzte Zeile" streut ab 12 KB bei gleichem
  Prompt (Temperatur 0.7); Fälle wiederholen.
- **Gemessene Grenzen (Bench `~/projects/bitnet-colibri-bench`, Engine b10524 Commit 9ee9fc0,
  Qwen3-4B-Instruct-2507-Q4_K_M sha256 3605803b982cb64a…):** Ein-Datei-Fix gelingt; Ursachen über
  einen Import hinweg scheitern (Qwen3 bricht gefahrlos ab, Llama-3.2-3B schrieb destruktiv). Der
  Agent soll nur in Git-Repos ändern: nur die Bestätigungsdialoge sichern, eine Warnung außerhalb
  eines Repos ist eine offene Produktentscheidung. Prompt-Verarbeitung auf der P1000 ~96 tok/s.
- **Temperatur bleibt 0.7, auch mit Tools** (negatives Ergebnis): `bench/agent_eval.py`
  Werkzeugwahl bei 0.7 dreimal 10/10, bei 0.0 ebenfalls 10/10 — kein Unterschied, keine Sonderregel.
- **CPU ohne `-tb`** (negatives Ergebnis, `-dev none -ngl 0`, Prompt 6×-Absatz):
  `-t 8` prompt 52,9 tok/s / gen 10,8 tok/s; `-t 8 -tb 12` prompt 50,6 / gen 11,5 — im Rauschen,
  `agent.zig` bleibt bei `-t min(Kerne, 8)`.
- Nach jeder Änderung an `agent.zig` muss `python3 scripts/e2e_ai_tools.py` grün bleiben; Messzahlen
  immer mit Engine-Commit und Modell-sha256 notieren, Referenz
  `bitnet-colibri-bench/results/linux-i7-8850H-gpu-und-neue-modelle.md`.
- RPCs: `focus_chat` (Chat-Tab in irgendeinem Pane aktivieren), `file_text(path)` (Inhalt des
  offenen Buffers), `ui_state.pane_count`,
  `ui_state.all_tabs`, `ui_state.agent_confirm_pending`, `chat_state.tool_rounds/pending_tools`,
  Nachrichten mit `tool_calls`/`tool_call_id`.
- E2E `python3 scripts/e2e_ai_tools.py`: Explorer per Chat aus/ein, Datei anlegen+öffnen ohne
  zweites Pane → Split, Fokus bleibt im Chat, Buffer im Nachbar-Pane geladen; lesen; kleine
  replace_text-Änderung ohne Dialog mit Tab-Reload; Überschreiben → Dialog → Deny → unverändert;
  `/etc/hostname` abgelehnt. Messung: erste Runde nach Warmup 13–14 s, danach 3–9 s je Frage.
