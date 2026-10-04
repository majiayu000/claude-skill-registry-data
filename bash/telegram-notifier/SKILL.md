---
name: telegram-notifier
description: Versendet formatierte Telegram-Messages (Markdown→HTML-Konversion) per Bot-API. Watchdog-Modus (silent on success) für Cron-Jobs, plus strukturierte Alert/Daily-Summary-Templates. Trigger bei jedem Alert, jedem Cron-Job (silent on success), jedem Daily-Summary.
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
  - windows
triggers:
  - cron: jeder registrierte OpenClaw-Cron-Job
  - alert: bei Script-Fehler, Build-Bruch, Health-Alert
  - summary: daily-briefing (07:00)
metadata:
  openclaw:
    tags:
      - comms
      - telegram
      - notification
      - watchdog
---

# telegram-notifier

Einheitliches Telegram-Gateway für MaxClaw. Setzt auf die offizielle
**Bot-API** (kein lokaler CLI-Client nötig) und nutzt HTML-Parse-Mode —
Telegram rendert Markdown-Varianten oft inkonsistent.

## When to use

- **Silent on success**: Cron-Job ruft `notify.sh ok "..."` und schweigt;
  nur bei Fehler kommt die Message.
- **Alert**: `notify.sh alert "<msg>"` → rotes 🔥-Prefix, sofort sichtbar.
- **Summary**: `notify.sh summary "<markdown>"` → HTML-Convert + Auto-Split
  bei >4096 Zeichen.

## Voraussetzungen

```bash
# Einmalig: Bot-Token + Chat-ID als Env oder Datei
export TG_BOT_TOKEN="123456:ABC-DEF..."
export TG_CHAT_ID="7222661188"      # Bastis DM
```

## Pattern

### 1. Core-Notifier (`scripts/notify.sh`)

```bash
#!/usr/bin/env bash
# notify.sh — Telegram-Bot-API Wrapper (HTML-Parse-Mode)
set -euo pipefail
MODE="${1:-info}"   # info | ok | alert | summary
MSG="${2:?usage: notify.sh <mode> <message>}"
SILENT_OK="${SILENT_OK:-0}"

: "${TG_BOT_TOKEN:?TG_BOT_TOKEN not set}"
: "${TG_CHAT_ID:?TG_CHAT_ID not set}"

# Markdown → HTML-Konversion (Subset: *, _, `, ```)
to_html() {
  local s="$1"
  s="${s//&/\&amp;}"; s="${s//</\&lt;}"; s="${s//>/\&gt;}"
  s="${s//\*\*/<b>}"   # bold (zwei Stellen, daher Loop unten)
  # einfacher: sed-Pipeline
  echo "$1" | python3 -c '
import sys, re
t = sys.stdin.read()
t = t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
t = re.sub(r"```(.+?)```", r"<pre>\1</pre>", t, flags=re.S)
t = re.sub(r"`([^`]+)`",  r"<code>\1</code>", t)
t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
print(t)
'
}

case "$MODE" in
  info)    PREFIX="ℹ️";;
  ok)      PREFIX="✅"; SILENT_OK=1;;
  alert)   PREFIX="🔥";;
  summary) PREFIX="📊";;
  *)       PREFIX="•";;
esac

HTML="<b>$PREFIX $(to_html "$MSG")</b>"

# Silent-on-success: skip wenn OK + Flag gesetzt
if [[ "$MODE" == "ok" && "$SILENT_OK" == "1" ]]; then
  echo "silent ok: $MSG" >&2
  exit 0
fi

curl -fsS -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
  -d chat_id="$TG_CHAT_ID" \
  -d parse_mode=HTML \
  -d disable_web_page_preview=true \
  --data-urlencode "text=$HTML"
```

### 2. Watchdog-Wrapper für Cron (`scripts/watchdog.sh`)

```bash
#!/usr/bin/env bash
# watchdog.sh — wrappt einen Cron-Befehl, benachrichtigt nur bei Fail
set -euo pipefail
NAME="${1:?job-name}"
shift
START=$(date +%s)

if "$@"; then
  RC=$?
  DUR=$(( $(date +%s) - START ))
  SILENT_OK=1 notify.sh ok "$NAME in ${DUR}s"
else
  RC=$?
  notify.sh alert "$NAME fehlgeschlagen (rc=$RC): $*"
  exit $RC
fi
```

### 3. Daily-Briefing-Template

```bash
# Daily-Briefing um 07:00
briefing() {
  notify.sh summary "📊 *Daily Briefing $(date +%Y-%m-%d)*

*GreyHack-CI:* $(gh pr list --repo Toqsick/greyhack-tools --state open --json number -q 'length') offene PRs
*GitHub-Monitor:* $(tail -1 ~/.cache/maxclaw/pr-monitor.txt)
*Snapshots:* $(du -sh ~/.local/share/maxclaw/snapshots/ | cut -f1)

Nächste Cron: $(openclaw cron list --json | jq -r '.[0].next_run')"
}
```

## Pitfalls

- ❌ **Markdown statt HTML** → `*italic*` rendert je nach Client anders. HTML
  mit `<b>`/`<i>`/`<pre>` ist deterministisch.
- ❌ **Message >4096 Zeichen** → Telegram API wirft 400. Auto-Split einbauen
  oder Summary kürzen.
- ❌ **Secrets im Klartext** → `TG_BOT_TOKEN` NUR aus Env/`.env`-Datei (nie
  ins Git, nie in Logs).
- ❌ **Network-Failure in Cron** schluckt die ganze Benachrichtigung — `curl -f`
  + expliziter `|| notify.sh alert "notify selbst failed"`.
- ✅ `disable_web_page_preview=true` → weniger Telegram-Spam bei URLs.
- ✅ Watchdog-Wrapper um **alle** Cron-Jobs, sonst wird MaxClaw zur
  Dauer-Nervensäge.

## Cron-Beispiel

```cron
# Daily Briefing
0 7 * * * /home/bratan/.openclaw/skills/telegram-notifier/scripts/watchdog.sh \
    "daily-briefing" \
    /home/bratan/maxclaw/workflows/daily-briefing.sh
```