---
name: system-snapshot
description: 'Use for full system-state snapshot + diff + HTTP:8898.'
version: 1.0.0
author: OpenAmer Agent
platforms: [windows]
tags:
  - system
  - snapshot
  - monitoring
  - health
  - diff
metadata:
  openamer:
    tags: [system, snapshot, monitoring, health, diff]
---
# System Snapshot

Vollständiger Systemzustand auf einen Blick: OS, Skripte, Skills, Cron, Health, Security, Backup, Sessions.

## Overview

Erfasst den kompletten Zustand des OpenAmer-Systems als strukturiertes JSON und stellt Diff-Funktionen und einen HTTP-Server bereit.

## When to Use

- `--now` für einmaligen Snapshot
- `--diff` um Änderungen zum letzten Snapshot zu sehen
- `--serve` für Live-API auf Port 8898
- `--list` um alle Snapshots anzuzeigen

## Usage

```bash
python scripts/system-snapshot.py --now
python scripts/system-snapshot.py --diff
python scripts/system-snapshot.py --serve
python scripts/system-snapshot.py --compare A.json B.json
python scripts/system-snapshot.py --list
```

## Verification

```bash
python scripts/system-snapshot.py --now && echo "Snapshot OK"
```

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Kein vorheriger Snapshot | `--diff` zeigt Fehler, einfach `--now` zuerst |
| Port 8898 belegt | Anderen Port verwenden oder Prozess beenden |