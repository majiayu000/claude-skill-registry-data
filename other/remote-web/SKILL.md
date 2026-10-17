---
name: remote-web
description: 'Use when starting/stopping the Remote Web UI on port 8901.'
author: OpenAmer
tags: [web, dashboard, remote, http, server, monitoring]
---

# Remote Web Platform

## Überblick

Die Remote Web Platform ist ein vollständiges Web-Dashboard für OpenAmer, erreichbar von jedem Gerät im Netzwerk.

- **Port:** 8901
- **Build:** Python stdlib only (http.server, json, threading)
- **Auth:** Bearer-Token (SHA256 geschützt)

## Endpunkte

| Pfad | Methode | Beschreibung |
|---|---|---|
| `/` | GET | HTML-Dashboard mit Chat, Status, Skills, Logs |
| `/health` | GET | Health-Check (gibt "OK" zurück) |
| `/api/status` | GET | JSON System Snapshot |
| `/api/skills` | GET | JSON Alle Skills (nach Kategorie) |
| `/api/chat` | POST | Chat-Kommunikation: `{"prompt": "..."}` |
| `/api/logs` | GET | Letzte 100 Log-Zeilen |

## Starten

```bash
# Standard (Port 8901, alle Interfaces)
python "$OPENAMER_HOME\scripts\remote-web.py"

# Nur lokal (127.0.0.1)
python remote-web.py --local

# Benutzerdefinierter Port
python remote-web.py --port=8901
```

## Auth-Token

- Standard-Token beim ersten Start: `openamer-remote-secret`
- Token-Datei: `~/.remote-web/auth.txt`
- Token in jeder Anfrage als Header: `Authorization: Bearer <token>`
- Der SHA256-Hash des Tokens wird serverseitig geprüft

## Health-Check Cron-Job

Ein Cron-Job läuft alle 5 Minuten:

```bash
openamer cron create "5m" --name "remote-web-health" --script "remote-web-health.py" --no-agent --deliver local
```

1. Ruft `http://127.0.0.1:8901/health` auf
2. Schreibt Ergebnis nach `~/.remote-web/health.json`
3. Exit-Code 0 = OK, 1 = Fehler

## Dateien

| Datei | Zweck |
|---|---|
| `scripts/remote-web.py` | HTTP-Server (Hauptdatei) |
| `scripts/remote-web-health.py` | Health-Check-Script für Cron |
| `~/.remote-web/auth.txt` | Auth-Token (SHA256) |
| `~/.remote-web/health.json` | Letzter Health-Check-Status |

## Fehlerbehebung

- **Port belegt:** `netstat -ano | findstr :8901` → PID ermitteln und killen
- **Auth-Fehler (401):** Prüfe `~/.remote-web/auth.txt` – Token muss im `Authorization: Bearer <token>` Header gesendet werden
- **Server startet nicht:** Prüfe Python 3.11+, kein psutil nötig (Fallback auf wmic)