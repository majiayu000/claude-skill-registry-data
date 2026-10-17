---
name: task-queue
description: 'Use for persistent task-queue with priorities + daemon.'
version: 1.0.0
author: OpenAmer Agent
platforms: [linux, macos, windows]
tags:
  - queue
  - tasks
  - scheduler
  - daemon
  - automation
metadata:
  openamer:
    tags: [queue, tasks, scheduler, daemon, automation]
---
# Task Queue

Persistente JSON-basierte Task-Queue mit Prioritäten, Daemon-Modus und Retry.

## Overview

Verwaltet asynchrone Tasks mit Priorität 1-5, automatischer Verarbeitung im Daemon-Modus und Retry-Logik.

## When to Use

- `--add` um Tasks in die Queue zu stellen
- `--process` für manuelle Verarbeitung
- `--daemon` für automatische Verarbeitung alle 10s
- `--list` für Queue-Übersicht
- `--stats` für Metriken

## Usage

```bash
python scripts/task-queue.py --add '{"type":"backup","payload":{},"priority":1}'
python scripts/task-queue.py --list --status pending
python scripts/task-queue.py --process
python scripts/task-queue.py --stats
python scripts/task-queue.py --retry <id>
python scripts/task-queue.py --cancel <id>
```

## Verification

```bash
python scripts/task-queue.py --add '{"type":"test","payload":{"cmd":"echo ok"},"priority":3}' && python scripts/task-queue.py --process && python scripts/task-queue.py --stats
```

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Race-Condition im Daemon | Wurde via RLock + atomare Updates gefixt |
| Queue-Korruption | `queue.json` manuell reparieren oder löschen |