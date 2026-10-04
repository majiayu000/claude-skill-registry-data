---
name: ask
description: "Die jeweils andere CLI (Codex aus Claude Code, Claude aus Codex) non-interaktiv fragen — read-only; ohne Argument Standard-Review des Projekts"
disable-model-invocation: true
---

Hole eine Zweitmeinung von der jeweils anderen CLI. Modus: **ask** (read-only). Ablauf und
Handover-Format stehen in `references/handover.md` im Plugin-Root — erst lesen, dann handeln.

1. **Plugin-Root ermitteln.** Unter Claude Code ist er `${CLAUDE_PLUGIN_ROOT}`. Beginnt dieser Wert nicht
   mit `/` (Codex ersetzt den Platzhalter nicht), leite den Root aus dem Pfad dieser Skill-Datei ab: das
   Verzeichnis, das `.codex-plugin/` enthält (bei `…/skills/ask/SKILL.md` zwei Ebenen über dem
   Skill-Verzeichnis).

2. **Stufe wählen.** Das Skript wählt Modell und Effort nach Stufe, nicht pauschal das Flaggschiff.
   Schätze die Aufgabe ein und übergib sie mit `--tier`:

   | Stufe | Wofür | Claude | Codex | Effort | `--boost` | `--fast` |
   |---|---|---|---|---|---|---|
   | `advanced` | Zweitmeinung, Review, Fehlersuche, Refactoring (Default) | opus | sol | high | xhigh | – |
   | `strong` | Architektur, widersprüchliche Anforderungen, Planung | fable | astra | medium | high | low |

   Ohne `--tier` gilt `advanced`: eine Zweitmeinung darf nicht schwächer sein als der Fragende. `strong`
   lohnt sich für einen Plan oder ein Urteil; `--fast` liefert das starke Modell als schnelle Einschätzung,
   `--boost` als tiefe. `--model <alias|slug>` und `--effort low|medium|high|xhigh|max` setzen Modell und
   Effort frei (bei `--model` ist der Effort high) — nur, wenn der User es ausdrücklich so verlangt.

3. **Ohne Argument:** Skript ohne Handover starten, es liefert das Standard-Review des Projekts:

   ```bash
   bash "<root>/scripts/ask.sh" --mode ask </dev/null
   ```

   **Mit Argument** (`$ARGUMENTS`): Handover nach dem Format aus `references/handover.md` schreiben und per
   Heredoc auf stdin geben:

   ```bash
   bash "<root>/scripts/ask.sh" --mode ask --tier <stufe> [--boost|--fast] <<'HANDOVER'
   # Handover
   …
   HANDOVER
   ```

4. **Unter Codex** den Aufruf mit `require_escalated` starten: `claude -p` braucht Netz, das die
   Codex-Sandbox standardmäßig sperrt. Unter Claude Code läuft der Aufruf normal per Bash.
   Das Skript ermittelt die Ziel-CLI selbst und wählt das Modell nach der Stufe; der Aufruf dauert je nach
   Umfang mehrere Minuten, Timeout großzügig setzen.

5. **Ergebnis wiedergeben:** stdout ist die Antwort der anderen CLI, stderr der Fortschritt. Die Antwort
   **unverändert** ausgeben, danach in wenigen Sätzen einordnen: wo du zustimmst, wo du widersprichst,
   was du übernimmst. Nicht umschreiben, nicht kürzen.
