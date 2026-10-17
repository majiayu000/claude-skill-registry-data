---
name: webhook-engine
description: 'Use for Webhook Engine on port 8900: rules, actions, API.'
category: system
trigger: webhook webhook-engine event triggered automation port 8900 rule engine
---

# Webhook Engine — Event-Triggered Automation

## Überblick

Event-getriggerter Automatisierungsserver auf Port 8900. Empfängt Webhooks, wertet Regeln aus und führt Aktionen aus (Scripts ausführen, Alarme senden, Dienste neu starten, Loggen).

## Standorte

| Komponente | Pfad |
|---|---|
| **Script** | `C:\Users\damir\scripts\webhook-engine.py` |
| **Regeln** | `C:\Users\damir\.webhook-engine\rules.json` |
| **Zustand** | `C:\Users\damir\.webhook-engine\state.json` |
| **Lock** | `C:\Users\damir\.webhook-engine\server.lock` |

## Verwendung

```bash
# Server starten
python3 /c/Users/damir/scripts/webhook-engine.py --start

# Regel hinzufügen
python3 /c/Users/damir/scripts/webhook-engine.py --add-rule '{"event":"git-push","action":"send-alert"}'

# Regel mit Bedingung + Action-Dict
python3 /c/Users/damir/scripts/webhook-engine.py --add-rule '{"event":"cron-fail","condition":{"job_id":"backup"},"action":{"type":"run-script","path":"notify.py"}}'

# Regeln auflisten
python3 /c/Users/damir/scripts/webhook-engine.py --list-rules

# Log anzeigen (letzte 50 Events)
python3 /c/Users/damir/scripts/webhook-engine.py --log

# Regel entfernen
python3 /c/Users/damir/scripts/webhook-engine.py --remove-rule rule-1

# Log leeren
python3 /c/Users/damir/scripts/webhook-engine.py --clear-log

# Health-Check
python3 /c/Users/damir/scripts/webhook-engine.py --health

# Cron: Restart wenn down
python3 /c/Users/damir/scripts/webhook-engine.py --ensure-running
```

## API Endpoints

| Methode | Pfad | Beschreibung |
|---|---|---|
| `POST` | `/webhook/<name>` | Webhook empfangen (JSON-Body) |
| `POST` | `/webhook` | Generisches Event |
| `GET` | `/health` | Health-Check |
| `GET` | `/rules` | Regeln auflisten |
| `GET` | `/state` | Zustand anzeigen |

## Events

Standard-Event-Typen:

| Event | Beschreibung | Typische Daten |
|---|---|---|
| `git-push` | Git Push | `{"repo":"...","branch":"...","commits":[...]}` |
| `cron-fail` | Cron-Job Fehler | `{"job_id":"...","error":"..."}` |
| `threshold` | Metrik-Schwellwert | `{"metric":"...","value":42}` |

Der Event-Typ wird aus `event` oder `event_type` im JSON-Body gelesen; fällt der auf den Webhook-Namen zurück.

## Actions

| Action | Parameter | Beschreibung |
|---|---|---|
| `run-script` | `path`, `args[]` | Python-Script ausführen |
| `send-alert` | `message` | Alert ausgeben (stdout, für Monitoring) |
| `restart-service` | `name` | Service neustarten (taskkill/systemctl) |
| `log-event` | `data` | Daten loggen |

### Action als String (Kurzform)

```json
{"event":"cron-fail","action":"send-alert"}
```

### Action als Dict (mit Parametern)

```json
{"event":"cron-fail","action":{"type":"run-script","path":"notify.py","args":["cron-fail"]}}
```

## Bedingungen (Conditions)

Bedingungen verwenden Dot-Notation für den Zugriff auf Event-Daten:

```json
{
  "event": "git-push",
  "condition": {"branch": "main"},
  "action": "send-alert"
}
```

```json
{
  "event": "cron-fail",
  "condition": {"job_id": "backup"},
  "action": {"type": "run-script", "path": "alert_admin.py"}
}
```

## Regelformat (rules.json)

```json
[
  {
    "id": "rule-1",
    "event": "git-push",
    "condition": {"branch": "main", "repo": "openamer/openamer"},
    "action": {"type": "send-alert", "message": "Push on main: {branch}"}
  },
  {
    "id": "rule-2",
    "event": "cron-fail",
    "action": {"type": "run-script", "path": "notify.py"}
  }
]
```

## Cron-Job (alle 5 Minuten)

Der Cron-Job `webhook-engine-health` prüft alle 5 Minuten, ob der Server läuft, und startet ihn bei Bedarf neu. Definiert in der OpenAmer `jobs.json`.

## Manuelle Events senden (Test)

```bash
# git-push Event
curl -X POST http://localhost:8900/webhook/git \
  -H "Content-Type: application/json" \
  -d '{"event":"git-push","repo":"openamer/openamer","branch":"main","commits":["abc123"]}'

# cron-fail Event
curl -X POST http://localhost:8900/webhook/monitoring \
  -H "Content-Type: application/json" \
  -d '{"event":"cron-fail","job_id":"backup","error":"Timeout"}'

# threshold Event
curl -X POST http://localhost:8900/webhook/metrics \
  -H "Content-Type: application/json" \
  -d '{"event":"threshold","metric":"cpu","value":95}'

# Health-Check
curl http://localhost:8900/health
```

## Troubleshooting

- **Port 8900 already in use**: `netstat -ano | findstr :8900` → taskkill /PID <id> /F
- **Rules not matching**: Prüfe den Event-Namen im JSON-Body (`event` oder `event_type` Feld)
- **Script not found**: Pfad in `rule["action"]["path"]` muss relativ zu `~/scripts/` oder absolut sein
- **Server hängt**: `taskkill /F /IM python.exe` und Neustart
- **Lock stale**: Lösche `C:\Users\damir\.webhook-engine\server.lock`