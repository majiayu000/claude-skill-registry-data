---
name: session-handoff
title: Session Handoff Document
description: Erstelle und pflege ein Handoff-Dokument fuer Modell-Wechsel, damit das naechste Modell sofort weiss was los
  ist.
triggers:
- Nach jeder Session mit relevanten Aenderungen
- Vor Modell-Wechsel
- Wenn der User "handoff" oder "wechsel" sagt
- Nach komplexen Tasks (5+ Tool-Calls)
- Wenn Memory fast voll ist und Kontext wichtig bleibt
version: 1.0.0
author: Hermes Agent
license: MIT
lane: koenigin
reasoning_effort: xhigh
---
# Session Handoff Document

## Ziel
Ein Markdown-Dokument das nach einem Modell-Wechsel gelesen wird. Es enthaelt alles was das neue Modell braucht um nahtlos weiterzumachen.

## Pfad
`~/docs/system/model-handoff.md`

## Wann aktualisieren

| Situation | Aktualisieren? |
|---|---|
| Session hat File-Aenderungen | Ja |
| Session hat Config-Aenderungen | Ja |
| Session hat neue Skills erstellt | Ja |
| Session hat offene Tasks/Blocker | Ja |
| Session war nur Q&A ohne Aenderungen | Optional |
| Vor Modell-Wechsel | Immer |

## Workflow

### 1. Snapshot sammeln (am Ende der Session)

```bash

set -euo pipefail
# System-State
hermes status --deep

# Offene Tasks
todo

# Git-Status (falls im Hermes-Repo)
cd ~/.hermes/hermes-agent && git status --short

# Letzte File-Aenderungen
find ~/docs/system/ ~/.hermes/skills/ ~/.hermes/config.yaml -mtime -1 -type f
```

### 2. Dokument aktualisieren

Sektionen die IMMER aktuell sein muessen:

1. **Aktiver Task** — Was ist gerade offen?
2. **System-State** — Provider, Gateway, Cronjobs, Tools
3. **Blocker** — Worauf warten wir?
4. **File-Aenderungen** — Was wurde neu erstellt/modifiziert?
5. **Wichtige Pfade** — Configs, Secrets, Scripts (Pfade pruefen!)
6. **User-Praeferenzen** — Aktuell relevante Einstellungen
7. **Naechste Tasks** — Was war als naechstes geplant?
8. **Lessons Learned** — Neue Erkenntnisse fuer zukuenftige Modelle
9. **Quick-Start** — 5 Befehle fuer das neue Modell
10. **Kontakt** — Wo Hilfe holen?

**WICHTIG:** Auch updaten wenn ein Blocker offen ist aber neue Erkenntnisse entstehen (z.B. neuer Skill, neue Config). Der naechste Block ist nicht "es gibt kein Handoff", sondern "das Handoff ist veraltet".

### 3. Lessons Learned pflegen

Neue Erkenntnisse die fuer andere Modelle hilfreich sind:

- Tool-Quirks (z.B. "terminal() gibt keinen stderr zurueck")
- Config-Traps (z.B. "approvals.mode = smart verhindert manche Calls")
- User-Workarounds (z.B. "User mag keine offenen Fragen, immer clarify()")
- System-Spezifika (z.B. "sudo deaktiviert, nie versuchen")
- Token-/Kontext-Limits (siehe Abschnitt "Memory-Limits kennen" in diesem Skill)

### 4. Speichern & bestaetigen

```bash

set -euo pipefail
# Schreibe nach ~/docs/system/model-handoff.md
# Pruefe ob Datei existiert und lesbar ist
ls -la ~/docs/system/model-handoff.md
```

## Template

```markdown
# Model Handoff Document

> Letzte Aktualisierung: YYYY-MM-DD
> Geschrieben von: Yuno (Modell-Name)
> Fuer: Naechstes Modell nach Wechsel

---

## 1. Aktiver Task & Kontext

**User-Frage die gerade offen ist:**
> "..."

**Status:** ...
**Letzte Aktion:** ...

---

## 2. System-State (Snapshot)

| Komponente | Status | Details |
|---|---|---|
| Hermes Version | ... | ... |
| Provider | ... | ... |
| Token-Expiry | ... | ... |
| Gateway | ... | ... |
| Terminal | ... | ... |
| Cronjobs | ... | ... |

---

## 3. Offene Entscheidungen / Blocker

**BLOCKER:** ...

**NICHT blockierend:** ...

---

## 4. File-Aenderungen seit Session-Start

**Neu erstellt:**
- `pfad/zur/datei` — Beschreibung

**Modifiziert:**
- `pfad/zur/datei` — Was geaendert wurde

---

## 5. Wichtige Pfade & Configs

| Was | Pfad | Hinweis |
|---|---|---|
| Hermes Config | `~/.hermes/config.yaml` | ... |
| Auth/Token | `~/.hermes/auth.json` | ... |
| Secrets | `~/.hermes/.env` | ... |

---

## 6. User-Praeferenzen (aktuell relevant)

- **Sprache:** ...
- **Kommunikation:** ...
- **Doku-Pflicht:** ...

---

## 7. Was als Naechstes geplant war

**P0-Tasks:**
1. ...

**P1-Tasks:**
- ...

---

## 8. Lessons Learned

### 8.1 Kategorie
Beschreibung mit konkretem Beispiel.

---

## 9. Quick-Start fuer neues Modell

```bash

set -euo pipefail
# 1. Status check
hermes status --deep

# 2. Daily Briefing laden
skill_view(name='daily-briefing')

# 3. Offene Tasks checken
todo

# 4. Session-Suche wenn Kontext fehlt
session_search(query="...", limit=3)
```

---

## 10. Kontakt & Escalation

| Was | Wie |
|---|---|
| Entscheidung naechtig | `telegram:Gregor (dm)` |
| Skill-Fragen | `skill_view(name='hermes-agent')` |
| Hermes-Doku | https://hermes-agent.nousresearch.com/docs |
```

## Anti-Patterns

- **NIE** Session-Outcomes, SHAs, PR-Nummern reinschreiben (veralten in 7 Tagen)
- **NIE** temporaere Zustaende wie "Port 1234 wird gerade benutzt" (ausser es ist dauerhaft)
- **NIE** vergessen das Datum zu aktualisieren
- **NIE** vergessen den eigenen Modell-Namen zu schreiben
- **NIE** Handoff auslassen nur weil ein Blocker offen ist — gerade dann ist es wichtig

## Verifikation

Nach dem Schreiben:
1. `read_file(path='~/docs/system/model-handoff.md', limit=20)` — Datei lesbar?
2. Datum aktuell?
3. Modell-Name eingetragen?
4. Aktiver Task beschrieben?
5. Blocker aufgefuehrt?

**Pitfall bei Skill-Erstellung:**
- Frontmatter braucht `name:` Feld, sonst fehlschlaegt `skill_manage(action='create')`
- Falsch: `title:` ohne `name:` — Richtig: `name:` + `title:` + `description:`

## Memory-Limits kennen (Session-spezifisch)

Wenn der User nach "Token-Groesse" oder "Kontext-Limit" fragt, unterscheide:

1. **Modell-Kontext**: `model.context_length` — Hartes Limit des Modells (DeepSeek V4 Flash = 256K Default)
2. **Memory-Limit**: `memory.memory_char_limit` — Wie viel Memory ins System-Prompt passt (Default: 2200 chars)
3. **User-Profile-Limit**: `memory.user_char_limit` — Wie viel User-Profil ins System-Prompt passt (Default: 1375 chars)
4. **Tool-Output**: `tool_output.max_bytes` — Max. Tool-Output (Default: 50000 bytes)
5. **File-Read**: `file_read_max_chars` — Max. `read_file` pro Aufruf (Default: 100000 chars)
6. **Compression-Hygiene**: `compression.hygiene_hard_message_limit` — Wann Chat komprimiert wird (Default: 400 Messages)

**Frag nicht "welches meinst du?" — zeige alle und lass den User waehlen.**

## Siehe auch

- `skill_view(name='daily-briefing')` — Morgendlicher System-Check
- `skill_view(name='telegram-clarification-prompt')` — Input-Flow ueber Telegram
