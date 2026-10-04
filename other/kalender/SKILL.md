---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Calendar skill with user-adaptive backend selection (Flag 3). Default: local SQLite store. Optional: Google Calendar MCP, Routinika or UpToday as backend — controlled via assist/prefs.json. Without preference the LLM asks the user interactively."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: de
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
---
<img src="banner.png" width="100%" alt="kalender banner">

## Zweck

Termine erfassen, abfragen und verwalten — mit wählbarem Backend. Der Core
(`kalender_core.py`) arbeitet immer mit dem **lokalen SQLite-Store** als
Default. Das LLM wählt bei Bedarf ein alternatives Backend anhand von
`assist/prefs.json`.

**Flag 3 — Backend-Wahl:**

| `kalender_backend` in prefs.json | Verhalten |
|---|---|
| `local` (Standard/Default) | SQLite-Store in diesem Skill-Ordner |
| `google` | Google-Calendar-MCP (nur LLM-Pfad, nicht in core.py) |
| `routinika` | Routinika-Kalender via module-installer (nicht impl. v0.1) |
| `uptoday` | UpToday-Kalender via module-installer (nicht impl. v0.1) |
| nicht gesetzt | LLM fragt den Nutzer interaktiv nach bevorzugtem Backend |

> `kalender_core.py` implementiert ausschließlich das `local`-Backend.
> Google-Calendar-MCP und weitere Backends sind LLM-gesteuert und werden
> im SKILL.md dokumentiert, nicht im Core.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Trag Termin ein" | Neuen Termin erfassen |
| „Was steht heute an?" | Heutige Termine abfragen |
| „Was steht diese Woche an?" | 7-Tage-Überblick |
| „Termin [Titel] am [Datum]" | Termin mit Datum anlegen |
| „Alle Termine im [Monat]" | Monatsübersicht |
| „Termin löschen [ID]" | Termin entfernen |
| „Termin exportieren" | ICS-Export aller/einzelner Termine |

---

## Workflow

1. **Backend prüfen**: `assist/prefs.json` → `kalender_backend` lesen.
2. **Ohne Präferenz**: LLM fragt Nutzer: lokaler Kalender, Google Calendar oder anderer?
3. **Local-Backend**: core.py — Termin in SQLite-Store anlegen/abfragen/löschen.
4. **Google-Backend**: LLM ruft Google-Calendar-MCP direkt auf (core.py nicht beteiligt).
5. **Ausgabe**: Lesbare Terminliste oder Bestätigung.

---

## CLI-Einstieg

```bash
# Termin anlegen
python kalender_core.py add "Zahnarzt" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Praxis Dr. X"]

# Heutige Termine
python kalender_core.py today

# Wochenübersicht
python kalender_core.py week [--from 2026-06-22]

# Monatsübersicht
python kalender_core.py month [--month 2026-07]

# Alle Termine (optional mit Suchbegriff)
python kalender_core.py list [--search "Zahnarzt"] [--limit 50]

# Termin löschen
python kalender_core.py delete <id>

# ICS-Export
python kalender_core.py export [--id <id>] [--out kalender.ics]

# Backend-Check
python kalender_core.py check-backend

# Alternativer Store (z.B. für Tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Store

| Eigenschaft | Wert |
|---|---|
| Typ | SQLite (local-Backend) |
| Pfad (Standard) | `skills/assist/kalender/store.db` |
| Override | `--store <pfad>` oder Env `KALENDER_STORE` |
| Tabellen | `events` |

### Schema

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (kurz: 8 Hex)
    title        TEXT NOT NULL,         -- Termin-Bezeichnung
    date         TEXT NOT NULL,         -- ISO-Datum YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- Dauer in Minuten (optional)
    location     TEXT,                  -- Ort (optional)
    description  TEXT,                  -- Notiz/Beschreibung
    recurrence   TEXT,                  -- ICS RRULE (optional, z.B. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID für Import/Export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## Haltung

- Der Core implementiert nur das `local`-Backend — leichtgewichtig, keine externen Deps.
- ICS-Export erzeugt valides RFC 5545-Subset (VCALENDAR + VEVENT), importierbar in alle gängigen Kalender-Apps.
- ICS-Import (Parsing) ist v0.1 noch nicht implementiert — geplant für v0.2.
- Wiederholungsregeln (`recurrence`/RRULE) werden gespeichert aber nicht ausgewertet — Auswertung ist v0.2.

---

## Datenschutz

- Lokale Termine bleiben in `store.db` — kein Netzwerkzugriff im Core.
- Beim Google-Calendar-Backend-Pfad verarbeitet Google-Calendar-MCP die Daten — Google-Datenschutzbestimmungen gelten.
- `store.db` nicht in Git committen (empfohlen: `.gitignore`).

---

## Verwandte Ressourcen

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — alternatives Backend, LLM-gesteuert
- Skill `assist/haushalt-manager` — Routinika-Integration (Presence-Check-Muster)
- `tools/module-installer/module_installer.py` — für zukünftige Routinika/UpToday-Backend-Integration

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.1.0 | 2026-06-22 | Erstanlage — Flag-3-Logik, local-Backend, ICS-Export |
