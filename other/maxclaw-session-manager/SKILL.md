---
name: maxclaw-session-manager
description: Trackt laufende und abgeschlossene MaxClaw-Sessions (Cron-Jobs, Build-Runs, User-Tasks) in einer lokalen JSONL-DB; erkennt Wiederholungs-Pattern und triggert Cooldown/Caching. Trigger bei jedem cron-driven Workflow und jedem manuellen Task-Start.
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
triggers:
  - cron: jeder registrierte Workflow (pre/post)
  - start: jeder neue User-Task
  - audit: bei "was hat MaxClaw zuletzt getan?"-Fragen
metadata:
  openclaw:
    tags:
      - workflow
      - session
      - tracking
      - meta
---

# maxclaw-session-manager

Lokale Session-Historie als append-only JSONL. MaxClaw kann damit:

1. **laufende Jobs erkennen** (Locking),
2. **Wiederholungs-Pattern** detektieren (gleicher Job < 5 Min = Duplicate),
3. **History** für Audits/Telegram-Reports liefern.

## When to use

- Vor jedem cron-driven Workflow: `session start` → Lock anlegen.
- Nach jedem Job: `session finish` → Dauer + Status loggen.
- Vor manuellem Re-Run: `session last <name>` → Cooldown prüfen.

## Pattern

### 1. Session-Storage (`scripts/session.py`)

```python
#!/usr/bin/env python3
"""session.py — JSONL-basierte Session-Verwaltung"""
import json, os, sys, time, fcntl
from datetime import datetime, timezone
from pathlib import Path

DB = Path(os.environ.get("MAXCLAW_SESSIONS",
                        Path.home() / ".local/share/maxclaw/sessions.jsonl"))
DB.parent.mkdir(parents=True, exist_ok=True)

def now(): return datetime.now(timezone.utc).isoformat(timespec="seconds")

def cmd_start(name: str):
    """Lock + Eintrag"""
    with DB.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        # Duplicate-Check (gleicher Name, letzte <300s)
        try:
            lines = DB.read_text().splitlines()[-20:]
            for line in reversed(lines):
                rec = json.loads(line)
                if rec["name"] == name and rec.get("status") == "running":
                    age = (datetime.now(timezone.utc).timestamp()
                           - datetime.fromisoformat(rec["started"]).timestamp())
                    if age < 300:
                        print(f"DUPLICATE: {name} läuft seit {int(age)}s")
                        sys.exit(3)
        except FileNotFoundError:
            pass
        rec = {"name": name, "started": now(), "status": "running"}
        f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec))

def cmd_finish(name: str, rc: int = 0):
    """Laufenden Eintrag finalisieren"""
    with DB.open("r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        lines = f.readlines()
        for i in range(len(lines) - 1, -1, -1):
            r = json.loads(lines[i])
            if r["name"] == name and r["status"] == "running":
                r["finished"] = now()
                r["status"]  = "ok" if rc == 0 else "fail"
                r["rc"]      = rc
                lines[i] = json.dumps(r) + "\n"
                break
        f.seek(0); f.writelines(lines); f.truncate()
        print(json.dumps(r))

def cmd_last(name: str, limit: int = 5):
    rows = [json.loads(l) for l in DB.read_text().splitlines() if l]
    rows = [r for r in rows if r["name"] == name][-limit:]
    print(json.dumps(rows, indent=2))

if __name__ == "__main__":
    sub = sys.argv[1]; name = sys.argv[2]
    if sub == "start":            cmd_start(name)
    elif sub == "finish":         cmd_finish(name, int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    elif sub == "last":           cmd_last(name)
    else: sys.exit(f"unknown: {sub}")
```

### 2. Watchdog-Wrapper für Cron (`scripts/run-session.sh`)

```bash
#!/usr/bin/env bash
# run-session.sh — wrappt einen Job in start/finish
set -euo pipefail
NAME="${1:?job-name}"; shift
python3 ~/.openclaw/skills/maxclaw-session-manager/scripts/session.py start "$NAME"
rc=0; "$@" || rc=$?
python3 ~/.openclaw/skills/maxclaw-session-manager/scripts/session.py finish "$NAME" "$rc"
exit $rc
```

### 3. Repeat-Pattern-Detection (`scripts/pattern-report.py`)

```python
#!/usr/bin/env python3
"""pattern-report.py — Jobs >5x/Tag = Pattern für Caching/Skip"""
import json, collections
from pathlib import Path
db = Path.home() / ".local/share/maxclaw/sessions.jsonl"
cnt = collections.Counter(json.loads(l)["name"] for l in db.read_text().splitlines() if l)
for name, n in cnt.most_common(10):
    if n >= 5: print(f"⚠  {name}: {n} Runs → Cache/Skip prüfen")
```

## Pitfalls

- ❌ **Lock über ganzes File** → bei vielen parallelen Crons kurze Blöcke. Nur
  während `start`/`finish` flocken, nicht beim Lesen.
- ❌ **JSONL als Single-Writer** — bei Multi-Process via `fcntl.LOCK_EX` (im
  Python-Code oben schon drin).
- ❌ **Duplicate-Check zu kurz** (<60s) → legitime schnelle Retries geblockt.
  300s ist praxistauglich.
- ❌ **Sessions.db ins Git** → Secrets/Code-Snippets können reinrutschen. In
  `~/.local/share/`, **nie** im Repo.
- ✅ History-Aufbewahrung: alle Einträge behalten, aber `tail -1000` für
  Reports → schnell & konstant.
- ✅ Bei Bedarf: `gzip` ältere Wochen und rotieren.

## Cron-Beispiel

```cron
# In jedem registrierten Workflow-Script:
exec /home/bratan/.openclaw/skills/maxclaw-session-manager/scripts/run-session.sh \
    "github-pr-monitor" /home/bratan/.openclaw/skills/github-ops/scripts/gh-pr-monitor.sh
```