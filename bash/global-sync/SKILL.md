---
name: global-sync
description: 'Use for multi-machine HTTP delta sync with peer management.'
tags:
  - global-sync
  - synchronization
  - multi-machine
  - state-sync
  - cron
usage: |
  Führe `python scripts/global-sync.py --start` um Server + Sync-Thread zu starten.
  Nutze `--sync-now` für sofortige Synchronisation zu allen Peers.
  Nutze `--status` für aktuellen Status.
  Nutze `--add-peer NAME HOST:PORT` zum Hinzufügen eines Peers.
  Der Cron-Job führt `--sync-now` alle 60 Minuten aus.
---

# Global State Sync

Multi-Machine State Synchronization für OpenAmer.

## Überblick

Global State Sync synchronisiert OpenAmer-Zustände (Skills, Cron, Scripts, Config, Sessions)
zwischen mehreren Maschinen über HTTP. Nur geänderte Dateien seit dem letzten Sync werden
übertragen (Delta-Only). Bei Timestamp-Konflikten gewinnt die neuere Version; die verlierende
Version wird in `.global-sync/conflicts/` gespeichert.

## Architektur

```
+-------------------+          HTTP POST /sync           +-------------------+
|  Maschine A       |  ──────────────────────────────►   |  Maschine B       |
|  Port 8902        |  JSON-Delta + SHA256-Signatur      |  Port 8902        |
|  Sync-Thread 60m  |  ◄──────────────────────────────   |  Sync-Thread 60m  |
+-------------------+          JSON-Delta + Signatur     +-------------------+
```

## Installation

Das Script liegt unter `scripts/global-sync.py` (OpenAmer Home) und wird via
Config in `.global-sync/config.json` gesteuert.

## Verwendung

```bash
# Status anzeigen
python scripts/global-sync.py --status

# Peer hinzufügen
python scripts/global-sync.py --add-peer mein-server 192.168.1.100:8902

# Sofort syncen
python scripts/global-sync.py --sync-now

# Server starten (Daemon-Modus)
python scripts/global-sync.py --start

# Peer-Liste anzeigen
python scripts/global-sync.py --peers

# Neues Token setzen
python scripts/global-sync.py --token MEIN_NEUES_SICHERES_TOKEN
```

## Konfiguration

`.global-sync/config.json`:

```json
{
  "peers": [
    {"name": "server1", "host": "192.168.1.100", "port": 8902}
  ],
  "sync_interval_minutes": 60,
  "sync_items": ["skills", "cron", "scripts", "config", "sessions"],
  "token": "DEIN_SICHERES_TOKEN",
  "server_port": 8902
}
```

### sync_items
- `skills` — OpenAmer Skills
- `cron` — Cron-Job-Definitionen
- `scripts` — Python-Scripte
- `config` — config.yaml
- `sessions` — Session-Dumps

## Sicherheit

- Jeder Request enthält einen SHA256-HMAC über den Body.
- Der Shared-Token wird in der Config gespeichert.
- Nur der SHA256-Hash des Tokens wird im Header übertragen.
- Port 8902 sollte hinter einer Firewall liegen.

## Konfliktlösung

| Bedingung | Ergebnis |
|-----------|----------|
| Remote neuer als lokal | Remote-Version überschreibt lokale |
| Lokal neuer als remote | Lokale Version bleibt; Remote in `.global-sync/conflicts/` |
| Gleicher Timestamp | Remote gewinnt (idempotent) |

## Dateien

| Pfad | Beschreibung |
|------|-------------|
| `~/.global-sync/config.json` | Sync-Konfiguration |
| `~/.global-sync/conflicts/` | Konflikt-Dateien |
| `~/.global-sync/last_sync.txt` | Timestamp des letzten Syncs |
| `scripts/global-sync.py` | Hauptscript |

## Cron-Job

Ein Cron-Job führt `--sync-now` alle 60 Minuten aus.