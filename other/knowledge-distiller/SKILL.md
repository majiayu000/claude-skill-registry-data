---
name: knowledge-distiller
description: Liest MaxClaw-Session-Logs, Workflow-Outputs und ~/docs/system/, destilliert wiederkehrende Muster und schlägt gezielte Skill-Updates vor. Trigger weekly (Sonntag-Cron) oder nach größeren Themen-Phasen.
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
triggers:
  - cron: weekly Sonntag 23:00
  - milestone: nach Phase-Abschluss (n Builds erledigt)
  - manual: "distill.sh"
metadata:
  openclaw:
    tags:
      - meta
      - knowledge
      - reflection
      - skills
---

# knowledge-distiller

MaxClaw's "Wochenrückblick": wertet Logs/Docs aus, findet Wiederholungen
und schlägt vor, **welche Skills erweitert oder angelegt werden sollten**.

## When to use

- Sonntag-Abend-Cron → Wochenrückblick an Basti (Telegram).
- Nach jeder größeren Themen-Phase (z. B. "GreyHack-Tool v2 fertig").
- Vor dem Anlegen eines neuen Skills → prüfen, ob's schon Inhalt dafür gibt.

## Pattern

### 1. Distiller-Script (`scripts/distill.sh`)

```bash
#!/usr/bin/env bash
# distill.sh — sammelt Quellen, ruft Python-Analyzer, postet Summary
set -euo pipefail
DOC_DIR="${1:-$HOME/docs/system}"
LOG_DIR="${2:-$HOME/.local/share/maxclaw/logs}"
OUT="${3:-$HOME/.cache/maxclaw/distill-$(date +%Y-W%V).md}"
mkdir -p "$(dirname "$OUT")"

python3 - <<PY > "$OUT"
import os, re, json, collections, datetime
from pathlib import Path

docs  = list(Path("$DOC_DIR").rglob("*.md"))
logs  = list(Path("$LOG_DIR").rglob("*.log"))

# 1) Häufigste Befehle aus Logs (Pattern, nicht Strings)
cmd_re = re.compile(r"\b(greybel build|sqlite3|rsync|openclaw cron|gh pr)\b\S*")
cnt = collections.Counter()
for log in logs[-50:]:                     # letzte 50 Logs
    for m in cmd_re.finditer(log.read_text(errors="ignore")):
        cnt[m.group(0)] += 1

# 2) Themen-Cluster aus Doku-Titeln
titles = [d.stem for d in docs]
clusters = collections.Counter()
for t in titles:
    head = re.split(r"[-_]", t)[0]
    clusters[head] += 1

# 3) Skill-Update-Hinweise: Commands die >3x vorkamen ohne dedizierten Skill
KNOWN_SKILLS = {"greyhack","sqlite","sandbox","telegram","github","bash"}
hints = [c for c, n in cnt.most_common() if n >= 3 and not any(s in c for s in KNOWN_SKILLS)]

print(f"# Wissens-Destillation {datetime.date.today()}\n")
print("## Top-Befehle (Logs, letzte 50)")
for c, n in cnt.most_common(10):
    print(f"- `{c}` ×{n}")
print("\n## Doku-Themen-Cluster")
for c, n in clusters.most_common(10):
    print(f"- **{c}** ({n} Dateien)")
if hints:
    print("\n## 💡 Vorgeschlagene neue Skills")
    for h in hints:
        print(f"- Skill für `{h}` anlegen (kam ≥3x in Logs vor)")
PY

echo "→ $OUT ($(wc -l < "$OUT") Zeilen)"
```

### 2. Skill-Update-Vorschlag-Generator

```python
# scripts/suggest_skill_patch.py — vergleicht bekannte Skill mit aktuellen Patterns
import re, sys, pathlib, collections

SKILL_DIR = pathlib.Path(sys.argv[1])
log = pathlib.Path(sys.argv[2]).read_text(errors="ignore")

# Häufige Fehler/Befehle aus letztem Log-Lauf extrahieren
errors = collections.Counter(re.findall(r"ERROR\s+(.+)", log))
for err, n in errors.most_common(5):
    print(f"FEHLER-PATTERN: {err}  (×{n})")
    print(f"  → in SKILL.md unter 'Pitfalls' ergänzen")
```

### 3. Wochenrückblick an Telegram koppeln

```bash
# In register-workflows.sh ergänzen:
"knowledge-distill|0 23 * * 0|workflows/knowledge-distill.md|knowledge-distiller,telegram-notifier"
```

## Pitfalls

- ❌ **Logs roh pasten** → Telegram-Spam. Immer Clustern + Top-N.
- ❌ **Skill-Vorschläge ohne Evidenz** ("könnte nützlich sein") → nicht
  handelbar. Immer mit Log-Count ≥3 belegen.
- ❌ **Distillation über mehrere Wochen kumulativ** → Output wächst
  unkontrolliert. Pro Woche eigenes File (`distill-YYYY-Www.md`).
- ✅ Output in `~/docs/system/insights/` archivieren — wird zur Historie.
- ✅ **Reflexions-Frage** immer mit rein: "Was hat MaxClaw diese Woche
  NICHT gut gemacht?" → verhindert Selbst-Zufriedenheit.

## Cron-Beispiel

```cron
# So 23:00 — Wochenrückblick
0 23 * * 0 /home/bratan/.openclaw/skills/knowledge-distiller/scripts/distill.sh \
    && SILENT_OK=1 notify.sh ok "knowledge-distill: fertig" \
    || notify.sh alert "knowledge-distill: fehlgeschlagen"
```