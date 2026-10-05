---
slug: iret77-smart-memory
version: 1.5.6
displayName: 智能记忆设置（Iret77 Smart Memory）
summary: 为 OpenClaw 代理提供 5 层记忆架构，解决上下文膨胀、48 小时遗忘和规则遗忘问题。
tags: clawhub
---

# Smart Memory — Setup Skill

## Was dieses Skill tut

Standard-OpenClaw-Setups akkumulieren über Wochen unkontrolliert Wissen in MEMORY.md.
Das führt zu Kontextfenster-Überlastung, Widersprüchen und einem Agenten der wichtige
Regeln "vergisst" obwohl sie in MEMORY.md stehen — und zu hartem 48h-Fogging bei Daily Logs.

Dieses Skill richtet eine **5-Schichten-Memory-Architektur** ein die das löst.

---

## AGENT: Setup-Anleitung

Gehe die folgenden Schritte der Reihe nach durch.
`[MULTI-AGENT ONLY]`-Schritte können übersprungen werden wenn nur ein Agent im System ist.

### Schritt 1: Verzeichnisse anlegen

```bash
mkdir -p memory/projects
mkdir -p memory/agents   # [MULTI-AGENT ONLY]
mkdir -p docs
```

### Schritt 2: MEMORY.md auf Kern reduzieren

Lese die bestehende MEMORY.md. Extrahiere:
- User-Profil (max. 3 Zeilen)
- Projekt-Headlines (1 Zeile pro Projekt) → Verweis auf CONTEXT.md
- Kritische Regeln (max. 5 Bullet Points)
- Agent-Routing-Tabelle [MULTI-AGENT ONLY]

Alles andere gehört in active-context.md oder die Projekt-/Agent-Kontext-Dateien (s.u.).
Schreibe das Ergebnis in MEMORY.md — Ziel: max. 35 Zeilen.

Füge am Ende hinzu:
```
## Memory-Architektur
- active-context.md → offene Themen + Kontext (täglich pflegen)
- memory/projects/<name>/CONTEXT.md → Projekthandbücher (on-demand injizieren)
- memory/agents/<typ>.md → Domain-Wissen (on-demand injizieren) [MULTI-AGENT ONLY]
- ⚠️ Schreib-Pflicht: Strukturelle Änderungen → active-context.md SOFORT updaten (Session kann jederzeit enden)
```

### Schritt 3: active-context.md erstellen

Erstelle `memory/active-context.md` mit folgendem Header:

```markdown
# Active Context
# Pflege-Regel: [DONE]-Einträge wöchentlich entfernen (automatisch via Cron/Heartbeat).
# Jeder Eintrag: Status + inhaltlicher Kontext (was der User erklärt hat).
# Nach Erledigung: gesamten Block löschen.
# Größenbremse: > 100 Zeilen = zu viele offene Themen oder zu geschwätzig → kürzen.

---
```

Befülle die Datei mit allem was aktuell offen ist (aus MEMORY.md, Tages-Logs, Kontext).
Format pro Eintrag:
```markdown
## [OPEN] <Thema> — <Kurzbeschreibung>
<Inhaltlicher Kontext: Was wurde erklärt, entschieden, vereinbart?>
<Relevante Regeln oder Hintergründe die der Agent kennen muss>

---
```

Besonders wichtig: Kritische Regeln die oft vergessen werden → als `[OPEN]`-Block aufnehmen
(auch wenn sie "immer" gelten — das ist der Punkt, sie bleiben sichtbar bis sie wirklich verinnerlicht sind).

### Schritt 4: Projekthandbücher anlegen

Für jedes aktive Projekt: `memory/projects/<projektname>/CONTEXT.md`

Extrahiere alle projektspezifischen Details aus MEMORY.md in diese Datei.
Template: `templates/projects/example/CONTEXT.md` in diesem Skill-Ordner.

**Wann updaten:**
> ⚠️ **Kritisch:** "Am Ende des Tasks" ist ein Anti-Pattern — Sessions können jederzeit durch
> Rate-Limits oder Crashes enden. Die korrekte Anweisung ist: **CONTEXT.md SOFORT nach der
> Aktion updaten, in derselben Antwort.** Kein nachgelagerter Schritt.

### Schritt 5: Agent-Domain-Wissen anlegen [MULTI-AGENT ONLY]

Für jeden Sub-Agent-Typ: `memory/agents/<typ>.md`

Enthält cross-project Wissen das für diesen Agent-Typ immer gilt.
Templates: `templates/agents/` in diesem Skill-Ordner.

**Abgrenzung:**
- `memory/agents/coding.md`: "GPT erfindet Swift-Typen → nie GPT für Swift-Code"
- `memory/projects/myapp/CONTEXT.md`: "myapp hat zwei .strings-Dateien die synchron bleiben müssen"

Wenn das Wissen beim nächsten Projekt auch gilt → agents/. Sonst → projects/.

**Task-Summary-Pflicht für Sub-Agents:**
Jeder Sub-Agent sendet nach Abschluss eine Summary an den Orchestrator:
```
sessions_send(sessionKey="agent:main", message="[SUMMARY] Projekt: X | Was: Y | Status: Z")
```
Zweck: Orchestrator-Heartbeat kann als Backup-Bestätigung prüfen ob CONTEXT.md-Update erfolgte.

### Schritt 6: AGENTS.md Startup-Sequenz updaten

Ersetze die "Every Session"-Sektion durch:

```markdown
## Every Session

Before doing anything else:
1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. **If in MAIN SESSION:** Read `MEMORY.md` + `memory/active-context.md`
4. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent raw context

**Sub-Agent Spawns [MULTI-AGENT ONLY]:** Injiziere in den Task-Prompt:
- Immer: Inhalt von `memory/agents/<typ>.md`
- Bei Projektarbeit: Inhalt von `memory/projects/<name>/CONTEXT.md`
```

### Schritt 7: Automatischen Cleanup + Backup einrichten

**Option A — Heartbeat (einfach):**
Füge in `HEARTBEAT.md` ein:
```
# TASK: Memory-Hygiene (wöchentlich, jeden Sonntag)
# Prüfe ob seit letztem Cleanup > 6 Tage vergangen (heartbeat-state.json).
# 1. Entferne alle [DONE]-Blöcke komplett aus memory/active-context.md
# 2. [OPEN]-Blöcke älter 30 Tage ohne Aktivität → in Tages-Log, aus active-context entfernen
# 3. memory/projects/*/CONTEXT.md — erledigte Tasks kürzen
# 4. lastMemoryCleanup Timestamp in memory/heartbeat-state.json schreiben

# TASK: Sub-Agent Memory Backup (bei JEDEM Heartbeat) [MULTI-AGENT ONLY]
# Sicherheitsnetz falls Sub-Agent CONTEXT.md-Sofortschreiben vergessen hat.
# 1. Lese letzten Sub-Agent-Output-Channel auf Abschluss-Posts
# 2. Prüfe ob strukturelle Änderungen in CONTEXT.md reflektiert sind
# 3. Falls NICHT → kompakten Eintrag ergänzen (was, wann, Commit/Status)

# TASK: Daily-Log automatisch schreiben (einmal täglich, abends)
# Prüfe ob memory/YYYY-MM-DD.md für heute existiert.
# Wenn NICHT: Lese memory/chat-YYYY-MM-DD.md → destilliere strukturelle Änderungen.
# Schreibe Ergebnis nach memory/YYYY-MM-DD.md (max. 30 Zeilen).
```

**Option B — Cron-Job (präzise):**
```
Schedule: 0 7 * * 0 (Sonntag 07:00 Ortszeit)
Message: "Wöchentliche Memory-Hygiene: [Cleanup-Anweisungen wie oben]"
```

### Schritt 8: Abschlusskontrolle

Prüfe jedes Kriterium:
- [ ] MEMORY.md < 40 Zeilen
- [ ] active-context.md erstellt, mindestens ein [OPEN]-Eintrag
- [ ] Jeder [OPEN]-Eintrag hat inhaltlichen Kontext, nicht nur Statuszeile
- [ ] Keine projektspezifischen Details mehr in MEMORY.md
- [ ] Wöchentlicher Cleanup aktiv (Heartbeat oder Cron)
- [ ] AGENTS.md Startup-Sequenz updated
- [ ] Für jedes aktive Projekt: CONTEXT.md angelegt [MULTI-AGENT ONLY]
- [ ] Für jeden Sub-Agent-Typ: agents/<typ>.md angelegt [MULTI-AGENT ONLY]

Berichte dem User kurz: Was wurde eingerichtet, wie viele Zeilen hat MEMORY.md jetzt,
wie viele offene Themen sind in active-context.md.

---

## Session-Lifecycle: Graceful Termination (v1.3+)

> **Das Session-Bloat-Problem:** Channel-Sessions (Slack, Discord etc.) wachsen unbegrenzt.
> Ab ~500 Zeilen wird jede Antwort spürbar langsamer — die gesamte History wird bei jeder
> Nachricht in den Kontext geladen. Ein harter Trim mitten im Gespräch löscht aber Kontext,
> Sprache und Persona sofort. Beides ist lösbar — ohne Script, ohne sichtbaren Output im Chat.

**Goldene Regel 1 — Immer Memory schreiben lassen, bevor du trimmst oder killst:**
Bevor eine Session getrimmt oder gelöscht wird, muss der Agent die Möglichkeit haben,
seinen Kontext in das Memory-System zu schreiben. Das gilt für manuelle Aktionen genauso
wie für automatische Heartbeat-Tasks. Der Hash-Handshake-Flow (s.u.) ist die technische
Umsetzung dieser Regel.

**Goldene Regel 2:** Niemals eine Channel-Session direkt trimmen oder löschen.
Immer den Hash-Handshake-Flow verwenden. Kein separates Script nötig — der Heartbeat-LLM
führt den Flow direkt aus.

### Warum der Flow unsichtbar ist

Channel-Sessions (z.B. Slack) leiten jede Antwort an den Chat weiter. Sobald man aber
`NO_REPLY` als einzigen Inhalt der Antwort vorgibt, unterdrückt OpenClaw den Output
vollständig — nichts landet im Kanal. Der Hash in `active-context.md` dient als
Out-of-Band-Bestätigung ohne Chat-Output.

### Der Hash-Handshake-Flow

1. Heartbeat prüft `sessions.json` → alle Keys mit `:channel:` **ohne** `:thread:`
2. Für jede Session **> 500 Zeilen** UND **> 2h inaktiv** (`updatedAt`):
   - Generiere einmaligen Hash: `TRIM_READY_<4 random chars>` (z.B. `TRIM_READY_a3f8`)
   - `sessions_send(sessionKey=<key>, timeoutSeconds=90, message="[WARTUNG] Schreibe jetzt alle offenen Themen und wichtigen Kontext in memory/active-context.md. Füge danach exakt diese Zeile am Ende ein: TRIM_HASH: <hash>. Antworte ausschließlich mit NO_REPLY.")`
   - Lese `memory/active-context.md` → suche nach `TRIM_HASH: <hash>`
   - **Hash gefunden:** Sicher trimmen (s.u.) + `TRIM_HASH:`-Zeile entfernen + Log: `TRIMMED`
   - **Hash nicht gefunden (Timeout):** Trotzdem trimmen + Log: `FORCE-TRIM`

> **Warum Force-Trim nach Timeout OK ist:** Eine Session die 90s nicht reagiert, ist
> faktisch eingefroren. Wichtige Infos stehen bereits in active-context.md aus
> früheren Saves. Der Schaden durch dauerhaft aufgeblähte Sessions überwiegt.

**⚠️ Thread-Sessions niemals trimmen:** Keys mit `:thread:` enthalten laufende
Unterhaltungs-Threads und müssen von der Trim-Logik ausgeschlossen werden.

### ⚠️ Sicheres Trimmen: Nie mitten in einem Tool-Call schneiden

`tail -60` kann mitten in einem Tool-Call-Block landen (toolUse ohne nachfolgendes
toolResult, oder toolResult ohne nachfolgende Assistenten-Antwort). Das hinterlässt
die Session in einem **ungültigen Zustand** — der Agent schweigt danach komplett.

**Pflicht: Immer auf einer vollständigen Assistenten-Antwort abschneiden.**

```python
import json

def safe_trim(session_file, keep_lines=60):
    lines = open(session_file).readlines()
    if len(lines) <= keep_lines:
        return  # Nichts zu tun
    
    # Kandidaten-Startpunkte: nur Zeilen wo role=assistant und kein toolUse
    candidates = []
    for i, line in enumerate(lines):
        try:
            msg = json.loads(line).get('message', {})
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content', [])
            # Nur wenn keine toolCall-Blöcke in der Antwort
            if not any(c.get('type') == 'toolCall' for c in content if isinstance(c, dict)):
                candidates.append(i)
        except:
            continue
    
    # Letzten Kandidaten der noch >= keep_lines vom Ende entfernt ist
    cutpoint = None
    for i in reversed(candidates):
        if len(lines) - i >= keep_lines:
            cutpoint = i
            break
    
    if cutpoint is None:
        cutpoint = max(0, len(lines) - keep_lines)
    
    with open(session_file, 'w') as f:
        f.writelines(lines[cutpoint:])
```

Dieses Skript sicherstellen dass der Trim immer nach einer abgeschlossenen
Assistenten-Antwort beginnt — nie mitten in einem Tool-Austausch.

### Heartbeat-Task-Template (direkt in HEARTBEAT.md einfügen)

```
# TASK: Auto-Trim große Channel-Sessions (bei JEDEM Heartbeat)
# [INSTRUCTION for LLM]:
# 1. Lese <workspace>/.openclaw/agents/main/sessions/sessions.json
# 2. Finde alle Keys die ":channel:" enthalten UND KEIN ":thread:" haben
# 3. Für jeden solchen Key: prüfe Zeilenanzahl der sessionFile (wc -l)
# 4. Wenn > 500 Zeilen UND updatedAt > 2h her:
#    a. Generiere Hash: TRIM_READY_<4 random chars>
#    b. sessions_send(sessionKey=<key>, timeoutSeconds=90,
#       message="[WARTUNG] Schreibe jetzt alle offenen Themen und wichtigen Kontext
#       in memory/active-context.md. Füge danach exakt diese Zeile am Ende ein:
#       TRIM_HASH: <hash>
#       Antworte ausschließlich mit NO_REPLY.")
#    c. Lese memory/active-context.md → suche nach "TRIM_HASH: <hash>"
#    d. Hash gefunden:
#       - tail -60 <sessionFile> > /tmp/trim.jsonl && mv /tmp/trim.jsonl <sessionFile>
#       - Entferne TRIM_HASH-Zeile aus active-context.md
#       - Log: "<ISO> | <key> | TRIMMED" → memory/trim-log.txt
#    e. Hash nicht gefunden (Timeout):
#       - tail -60 <sessionFile> > /tmp/trim.jsonl && mv /tmp/trim.jsonl <sessionFile>
#       - Log: "<ISO> | <key> | FORCE-TRIM" → memory/trim-log.txt
```

### Pflicht-Ergänzung in AGENTS.md

```markdown
## Session-Management (Harte Regel, keine Ausnahmen)

NIEMALS eine Channel-Session direkt löschen oder trimmen.
Immer den Hash-Handshake-Flow via Heartbeat verwenden (siehe smart-memory Skill).
Thread-Sessions (:thread: im Key) sind grundsätzlich ausgenommen.
```

---

## Neue Agents: Memory-System als Standard

**Jeder neue Agent bekommt das Memory-System — mit einer Ausnahme:**

| Agent-Typ | Memory-System? |
|-----------|---------------|
| Haupt-Agent (Orchestrator) | ✅ Pflicht — vollständige 5-Schichten-Architektur |
| Persistente Sub-Agents (eigene Channels, lange Laufzeit) | ✅ Pflicht — mindestens active-context.md |
| Reine Task-Sub-Agents (begrenzte Aufgabe, Kontext aus Prompt) | ❌ Nicht nötig — Kontext kommt vom Orchestrator |

**Erkennungsmerkmal für "reine Task-Sub-Agents":**
- Werden für einen einzelnen, klar begrenzten Task gespawnt
- Erhalten ihren gesamten Kontext im Task-Prompt vom Haupt-Agent
- Haben keinen eigenen persistenten Channel
- Schreiben ihr Ergebnis zurück an den Orchestrator (Summary via sessions_send)

**Erkennungsmerkmal für "persistente Sub-Agents":**
- Haben einen eigenen Slack-/Discord-Channel
- Werden wiederholt für ähnliche Tasks genutzt
- Akkumulieren über Zeit domänenspezifisches Wissen

> Faustregel: Wenn ein Agent Gespräche führt oder wiederholtes Wissen aufbaut → Memory.
> Wenn ein Agent einen einzigen Task abarbeitet und dann fertig ist → kein Memory nötig.

---

## Tägliche Schreib-Regeln (nach Setup)

| Situation | Aktion |
|-----------|--------|
| User erklärt etwas Wichtiges | → `[OPEN]`-Block in active-context.md mit vollem Kontext |
| Strukturelle Änderung (Channel, Projekt, Regel) | → active-context.md **SOFORT in derselben Antwort** |
| Technische Erkenntnis bei Coding | → CONTEXT.md **SOFORT** (nicht am Task-Ende) |
| Cross-project Lesson | → memory/agents/<typ>.md updaten |
| Sub-Agent Task abgeschlossen [MULTI-AGENT] | → CONTEXT.md sofort + Summary an Orchestrator |
| Thema abgeschlossen | → `[DONE]` markieren (Cleanup entfernt Block) |
| MEMORY.md nähert sich 40 Zeilen | → destillieren: Was ist wirklich dauerhaft relevant? |
| active-context.md > 100 Zeilen | → Warnsignal: Einträge kürzen oder klären |

> **Goldene Regel:** Schreiben ist Teil der Aktion, nicht ein nachgelagerter Schritt.
> Sessions enden unvorhersehbar. Was nicht sofort geschrieben wird, ist verloren.

---

## Warum das funktioniert

**Das Fogging-Problem:** In Standard-Setups gibt es nur Daily Logs (heute + gestern).
Was vor 3 Tagen besprochen wurde, ist weg. Der User muss alles neu erklären.

**Die Lösung:** active-context.md schreibt Relevanz, nicht Zeit. Ein offenes Thema
bleibt im Kontext bis es erledigt ist — egal wie lange das dauert. Nach Erledigung
fliegt es raus. Kein unkontrolliertes Aufblähen, weil erledigte Themen aktiv entfernt werden.

**Das Rauschen-Problem:** MEMORY.md wächst über Monate auf hunderte Zeilen.
Der Agent sieht alles gleichzeitig — Swift-Lektionen neben Marketing-Strategie neben Cron-IDs.
Alles konkurriert um Aufmerksamkeit. Regeln werden "vergessen" weil sie im Rauschen untergehen.

**Die Lösung:** Jede Schicht hat einen klar begrenzten Scope. Projektdetails sind nicht
im Orchestrator-Kontext — sie werden on-demand in Sub-Agent-Prompts injiziert wenn
sie gebraucht werden. Kein Rauschen, keine Ablenkung.

**Das Session-Crash-Problem (neu in v1.1):** "Am Ende der Session schreiben" versagt
wenn Sessions durch Rate-Limits oder Crashes enden. Die Lösung: Schreiben ist Teil
der Aktion selbst — sofort, inline, bevor die Antwort gesendet wird. Der Heartbeat
ist das Backup-Netz, nicht der Primary-Trigger.
