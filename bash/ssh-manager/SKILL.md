---
name: ssh-manager
description: 'SSH hosts: add, list, exec, exec-all, scp, health-check.'
domain: devops
tags:
  - ssh
  - scp
  - remote
  - multi-host
  - health-check
triggers:
  - "Verwalte meine SSH-Hosts"
  - "Führe Befehl auf Server aus"
  - "Health-Check aller Server"
  - "Dateien per scp übertragen"
  - "Parallel exec auf mehreren Hosts"
---

# SSH Remote Manager

Multi-Host-Verwaltung mit SSH + scp + Ping-Health-Check + paralleler Ausführung.

## Installation

Das Skript liegt unter `~/scripts/ssh-manager.py`. Ein Batch-Wrapper `~/scripts/ssh-manager.bat`
erlaubt den Aufruf von überall (wenn `~/scripts/` im PATH).

```bash
# Alias einrichten (optional)
echo 'alias sshm="python ~/scripts/ssh-manager.py"' >> ~/.bashrc
source ~/.bashrc
```

## CLI-Kommandos

| Kommando | Beschreibung |
|----------|-------------|
| `--add NAME user@host:port` | Host hinzufügen (optional `--key ~/.ssh/id_rsa`) |
| `--list` | Alle Hosts mit Ping-Status auflisten |
| `--exec HOST 'command'` | Befehl auf einem Host via SSH ausführen |
| `--exec-all 'command'` | Befehl auf ALLEN Hosts parallel ausführen |
| `--fetch HOST remote local` | Datei von Host holen (scp) |
| `--push HOST local remote` | Datei zu Host senden (scp) |
| `--check` | Health-Check (Ping aller Hosts) |
| `--check --json` | Health-Check mit JSON-Ausgabe |

## Exit-Codes

- **0**: Alle Hosts OK
- **1**: Teilweise Fehler
- **2**: Alle Hosts offline/tot

## Konfiguration

Hosts werden in `~/.ssh-manager/hosts.json` gespeichert:

```json
[
  {
    "name": "webserver",
    "host": "192.168.1.100",
    "port": 22,
    "user": "root",
    "key_path": "/c/Users/damir/.ssh/id_rsa"
  }
]
```

## Health-Check Cron

Ein Cron-Job läuft alle 30 Minuten und speichert Reports unter `~/.ssh-manager/health_*.json`.
Der aktuelle Report liegt in `~/.ssh-manager/health_latest.json`.

## Sicherheit

- Nur SSH-Key-Authentifizierung (`BatchMode=yes`)
- Keine Passwörter in der Konfiguration
- Host-Key-Verifikation via `StrictHostKeyChecking=accept-new`
- Timeout nach 10s Connect / 120s Exec

## Beispiele

```bash
# Host hinzufügen
python ~/scripts/ssh-manager.py --add web1 root@192.168.1.10:22

# Host mit key hinzufügen
python ~/scripts/ssh-manager.py --add db1 admin@db.internal:2222 --key ~/.ssh/db_key

# Alle Hosts anzeigen
python ~/scripts/ssh-manager.py --list

# Befehl auf einem Host ausführen
python ~/scripts/ssh-manager.py --exec web1 'uptime && free -h'

# Befehl auf allen Hosts parallel
python ~/scripts/ssh-manager.py --exec-all 'df -h /'

# Datei vom Host holen
python ~/scripts/ssh-manager.py --fetch web1 /var/log/nginx/access.log ./access.log

# Datei zum Host senden
python ~/scripts/ssh-manager.py --push web1 ./nginx.conf /etc/nginx/nginx.conf

# Health-Check
python ~/scripts/ssh-manager.py --check
```

## Verwendung in OpenAmer

Lade das Skill und führe die gewünschten Aktionen aus:

```
# Host hinzufügen
Execute python scripts/ssh-manager.py --add web1 root@10.0.0.50

# Status abfragen
Execute python scripts/ssh-manager.py --check

# Parallel Befehl ausführen
Execute python scripts/ssh-manager.py --exec-all 'systemctl status nginx'
```