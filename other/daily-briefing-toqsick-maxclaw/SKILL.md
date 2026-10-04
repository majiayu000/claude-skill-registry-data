---
name: daily-briefing
description: Tägliches Briefing zu Beginn jeder Session — System-Status, letzte Aktivität, offene Punkte, Cron-Status.
version: 1.0.0
author: Yuno
license: MIT
lane: koenigin
reasoning_effort: xhigh
---
# Daily Briefing

Lade diese Skill zu Beginn jeder Session mit dem Benutzer (the user). Führe das Briefing durch, bevor du mit Aufgaben beginnst.

## Ablauf

### 0. Skill-Loading (Duplicate Name Resolution)

**⚠️ Bekanntes Problem:** Es gibt ZWEI `daily-briefing` Skills:
- `~/.hermes/skills/productivity/daily-briefing/SKILL.md`
- `~/.hermes/skills/skills/productivity/daily-briefing/SKILL.md`

`skill_view(name='daily-briefing')` schlägt fehl mit "Ambiguous skill name".
**Fix:** Immer den QUALIFIZIERTEN Pfad nutzen: `skill_view(name='productivity/daily-briefing')`.

### 1. Letzte Session abrufen

Nutze `session_search(limit=2, query="")` (browse-Modus) um die letzten 1-2 Sessions zu finden. Lies die bookend_start + bookend_end der aktuellsten Session um zu sehen was zuletzt gemacht wurde und ob was offen blieb.

#### 1.1. Context-Gap nach Modellwechsel (WICHTIG)

Wenn der User nach einem Modellwechsel einen **spezifischen Begriff/eine Version/ein Feature** nennt (z.B. "V6", "Option 1+2+3", "Phase 4"), das du nicht in der Session-History oder im Briefing findest:

1. **Max 2 gezielte session_search-Queries** — einen Discovery-Call mit dem Begriff, ggf. einen zweiten mit Synonym
2. **Memory/Mnemosyne prüfen** — `memory(action='list', target='memory')` oder `mnemosyne_recall(query='...')`
3. **Schnelle System-Checks** — `grep -ri "V6" ~/relevant/path/` (1-2 max, nicht tief)
4. **Nicht gefunden → FRAGEN.** Sofort `clarify(choices=[...])` mit 2-4 Optionen. Kein weiteres Session-Scrollen.
5. **NIEMALS:** große Session-Transcripts (>50KB) scrollen um einen Begriff zu finden. Das kostet >5000 Tokens pro Scroll-Call und produziert selten Treffer. Lies stattdessen bookend_start + bookend_end der letzten relevanten Session — da stehen Goal + Resolution drin.
6. **NIEMALS:** `session_search(limit=10)` — 5 ist die Obergrenze. Bei 10 kommen Sessions die nichts mit dem Thema zu tun haben.

**Warum:** Diese Session hat 10+ session_search- + 8 terminal-Calls + Hunderttausende Bytes Output verbraucht, nur um einen Begriff ("V6") zu finden den es nicht gab. Ein clarify() nach 2 Minuten hätte das verhindert.

### 2. Cron-Jobs prüfen
Nutze `cronjob(action='list')` um den Status der aktiven Cronjobs zu prüfen. Achte auf:
- Fehlgeschlagene Läufe (last_status)
- Bevorstehende Läufe (next_run_at)
- Ob einer kürzlich gelaufen ist und Ergebnisse hatte
- `delivery_error` Feld — auch wenn `last_status=ok`, kann die Telegram-Delivery fehlschlagen!

**⚠️ WICHTIG:** Die nachfolgende Tabelle ist ein SNAPSHOT — NIE als aktuell behandeln! IMMER live prüfen.

**the user's aktive Cronjobs (Stand 2026-07-03 nach Fix — IMMER live validieren!):**

| Job | Zeit | Modus | Deliver | Status |
|-----|------|-------|---------|--------|
| `yuno-morning-briefing` | 08:00 täglich | LLM (daily-briefing) | origin | ✅ |
| `yuno-mittags-check` | 12:00 täglich | LLM (daily-briefing) | **local** | ⚠️ error → fixed |
| `yuno-abend-wrapup` | 18:00 täglich | LLM (daily-briefing) | **local** | ⚠️ error → fixed |
| `gateway-watchdog` | stündlich | Script | local | ✅ |
| `hermes-network-monitor` | alle 15 Min | Script | local | ✅ |
| `mnemosyne-sleep` | 04:00 täglich | Script | local | ✅ |
| `mnemosyne-backup` | stündlich | Script | local | ✅ |
| `gmail-organizer` | 08:00 sonntags | Script | telegram | ✅ |
| `orch-hourly-audit` | stündlich | Script | telegram | ✅ |
| `orch-weekly-improve` | 04:00 sonntags | Script | telegram | ✅ |
| `orch-weekly-pipeline` | 05:00 sonntags | Script | **local** | ✅ |
| `greyhack-ci-watch` (MaxClaw) | stündlich | LLM (greyhack) | telegram:7222661188 | ⚠️ Model-Error #44585 |
| `greyhack-tool-builder` (MaxClaw) | alle 2h | LLM (greyhack) | telegram:7222661188 | ✅ |
| `github-pr-monitor` (MaxClaw) | 09:00 + 17:00 täglich | LLM | telegram:7222661188 | ✅ |
| `greyhack-mobil-watchdog` (NEU 2026-07-04) | alle 2h | LLM (skill-navigator) | telegram:7222661188 | ✅ |
| Todoist Weekly Review | Mo 09:00 | LLM (daily-briefing) | **local** | ⚠️ error → fixed |

### 2.2. Cron Delivery "Chat not found" Detection

Wenn `last_status=ok` UND `last_delivery_error="Telegram send failed: Chat not found"` (oder ähnlich):
- **Bedeutung:** Cron lief durch, Inhalt wurde generiert, aber Gateway konnte nicht in den Home-Channel senden.
- **Häufigste Ursache:** `~/.hermes/.env` (`TELEGRAM_HOME_CHANNEL=@username`) überschreibt `config.yaml` (`home_channel: <numerische_id>`). **.env gewinnt immer.** Bei Username-Versand via Bot kann das Home-Channel-Mapping fehlschlagen, selbst wenn `allowed_chats` korrekt gesetzt ist.
- **Diagnose-Schritte (read-only zuerst):**
  1. `grep -E "TELEGRAM_HOME_CHANNEL|home_channel|TELEGRAM_ALLOWED_USERS|allowed_chats" ~/.hermes/.env ~/.hermes/config.yaml` — vergleichen, Mismatch suchen
  2. **Direkttest mit curl** (entscheidet, ob Token + Chat-ID überhaupt ok sind):
     ```bash

set -euo pipefail
     TOKEN=$(grep ^TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2-)
     curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
       -d "chat_id=<numerische_id>" -d "text=test"
     ```
     → `{"ok":true,...}` heißt: Token + Chat-ID funktionieren direkt. Dann liegt's an der Hermes-Gateway-Home-Channel-Logik (= meist .env-Override).
  3. **Gateway-Log checken**: `journalctl --user -u hermes-gateway --no-pager -n 50 | grep -A1 "home-channel\|Chat not found"` — bestätigt, ob Gateway selbst die .env-Einstellung nutzt.
- **Fix (nur nach Bestätigung des Mismatch):**
  ```bash

set -euo pipefail
  # Numerische Chat-ID in .env setzen (BEIDE Felder, nicht nur home_channel!)
  sed -i 's/^TELEGRAM_HOME_CHANNEL=@.*/TELEGRAM_HOME_CHANNEL=<numerische_id>/' ~/.hermes/.env
  sed -i 's/^TELEGRAM_ALLOWED_USERS=@.*/TELEGRAM_ALLOWED_USERS=<numerische_id>/' ~/.hermes/.env
  systemctl --user restart hermes-gateway.service
  ```
- **Verify:** `cronjob(action='run', job_id=<id>)` triggert Job manuell, prüft `last_delivery_error`.
- **Cross-Reference:** the user's Memory hält das gleiche Pattern fest: _"Telegram Config: `telegram.allowed_chats` AND `telegram.home_channel` in config.yaml are PRIMARY. .env can override config.yaml — check BOTH."_

**Pitfall:** Nicht nur `home_channel` fixen — auch `allowed_chats` und `TELEGRAM_ALLOWED_USERS` müssen als numerische ID vorliegen, sonst greift der DM-Filter und blockt weiter.

**Letzte Änderungen (chronologisch):**

**2026-07-04:**
- `greyhack-mobil-watchdog` (job_id `6003e431dad7`, alle 2h) NEU
  LLM-watchdog für yuno_mobil-Setup-Bundle: checkt greyhack-tools + hermes-v7
  auf neue Files, meldet nur bei Änderung via Telegram
- `greyhack-ci-watch` (MaxClaw, job_id `6732ae8278ce`) Model-Error → pausiert
  Yuno's Duplikat-Cron `a167de38428d` pausiert um Doppel-Sends zu vermeiden.
  Lesson: **Immer `hermes cron list` VOR `cron create`** — Cron-Namen sind global

**2026-07-03:**
- `yuno-mittags-check` (job_id `14b4ed9fbc42`, 12:00 täglich): `deliver` → `local`
  LLM-generierter Mittags-Check, Output > 10KB → Telegram-Send-Timeout
- `yuno-abend-wrapup` (job_id `e7f24d9bb484`, 18:00 täglich): `deliver` → `local`
  LLM-generierter Wrap-up, gleiches Timeout-Problem
- Todoist Weekly Review (job_id `08ff393b7004`, Mo 09:00): `deliver` → `local`
  LLM-generierter Todoist-Review, Output > 10KB
- **Pattern:** Alle 3 sind **LLM-Cronjobs** (kein `no_agent=true` Script!) mit
  großen Reports. Telegram-Timeout trifft sowohl Skript- als auch Agent-Output.
  → Fix identisch: `deliver='local'`, Output landet in `~/.hermes/cron-output/`

**2026-06-28:**
- `orch-weekly-pipeline`: `deliver` von `telegram:7222661188` → `local`
  Pipeline lieferte ~14KB stdout → Telegram-Send-Timeout (30s).
  Fix: Nur lokales Logging. Logs unter `~/.hermes/orchestrator-*.log`.

**Script-Pfade (Stand 2026-06-28):**
- Live-Skripte: `~/.hermes/scripts/` (NICHT `~/scripts/`)
- Orchestrator: `~/.hermes/scripts/orchestrator-*.sh`
- Mnemosyne-Logs: `~/.hermes/orchestrator-*.log`

**Deprecatete/entfernte Jobs:**
- `esl-tech-news`, `greyscripts-daily-status`, `greyhack-daily-scan`, `greyhack-daily-fix` — existieren nicht mehr

### 2.1. Cron Delivery Error Detection

Wenn `last_status=ok` ABER `last_delivery_error` gesetzt ist — oder ein
Cron-Job schlicht nicht ankommt — immer **drei Patterns** checken:

| Pattern | Error-Stichwort | Diagnose | Detail |
|---|---|---|---|---|
| 1 | `Telegram send failed: Chat not found` | `TELEGRAM_HOME_CHANNEL`/`ALLOWED_USERS` auf `@username` statt numerischer `chat_id` | `references/telegram-delivery-errors.md` |
| 2 | `Telegram send failed: Timed out` | Output (Script ODER LLM-Agent) > ~10KB → Gateway-Send-Timeout (30s) | siehe unten |
| 3 | `Provider authentication failed` / `HTTP 401` | API-Key in `.env` tot | `references/telegram-delivery-errors.md` |

**Volle Diagnostic-Befehle + Fix-Schritte:** `references/telegram-delivery-errors.md`

**Pattern 2 (Timed out) — Kurzfassung:**
- **Ursache:** Job lief erfolgreich, aber Output > ~10KB verursacht Gateway-Send-Timeout
- **Fix:** `cronjob(action='update', job_id=..., deliver='local')` — Output bleibt lokal
- **Alternative:** Script/Job umbauen auf "silent on success" Pattern (nur bei Alerts output generieren)
- **Relevante Jobs:** Alle Jobs (Script ODER LLM-Agent) mit `deliver=telegram` die >5KB Output produzieren

### 2.5. Tech/Cybersecurity News (optional)
Wenn aktuell relevant oder the user fragt:
- `curl https://www.bleepingcomputer.com/news/security/` für Security-News
- ODER: `web_search("cybersecurity news today", limit=3)` für aktuelle Incidents
- Nur einfließen lassen, wenn the user explizit nach fragt oder Bedeutendes passiert



### 2.7. Container/Docker-Awareness (NEU V1.1)
Wenn Hermes in einem Docker-Container läuft (Working directory = `/root`, Home = `/root`):
- `sysdoctor check` zeigt CONTAINER-Metriken, nicht Host!
- Cron-Jobs kommen vom HOST (werden via Hermes API injected, nicht via Dateisystem)
- `search_files` im Host-Pfad zeigt nicht die Host-Dateien
- Platten-Check zeigt Container-Overlay, nicht Host-SSD
→ **Bei System-Werten IMMER prüfen: Ist das der Container oder der Host?**
→ **Für System-Status besser:** `df -h /`, `free -h`, `uptime` statt `sysdoctor check`

### 3. System-Schnellcheck
Führe `df -h /`, `free -h`, `uptime` aus und fasse in EINEM Satz zusammen:
- Plattenbelegung (relevanteste Partition)
- RAM-Auslastung
- Load average

**Optional: Service-Status** — Wenn the user kürzlich gezockt hat oder Services auffällig sein könnten, prüf kurz ollama + tokentelemetry via `systemctl --user is-active`. Details und Toleranzen: `references/system-services-check.md`.

Nur erwähnen wenn etwas AUFFÄLLIG ist (Platte >80%, RAM >80%, >10 Updates).

### 4. Briefing ausgeben

Formatiere das Briefing als:

```

set -euo pipefail
╔══════════════════════════════════════╗
║   ☕ YUNO'S DAILY BRIEFING          ║
║   <DATUM>                           ║
╚══════════════════════════════════════╝

📋 LETZTES MAL:
<was wir gemacht haben, 2-3 Zeilen>
<offene Punkte>

⏰ CRONS:
<Status der Cronjobs, wenn auffällig>
(optional: "Nichts auffälliges" wenn alles läuft)

🖥️ SYSTEM:
<ein Satz, nur bei Auffälligkeiten>

───
Bin bereit! Was steht an?
```

### Wichtige Regeln
- Das Briefing muss KURZ sein — max 10-15 Zeilen Text
- Nicht jede Kleinigkeit erwähnen, nur Relevantes
- Den Yuno-Ton wahren (kreativ/humorvoll, (kappa))
- Wenn System unauffällig, den System-Teil ganz weglassen
- Cron-Teil weglassen wenn keine Cronjobs existieren oder alle grün sind
- Bei vielen offenen Punkten aus letzter Session: den wichtigsten nennen, dann fragen ob sie den Faden aufnehmen wollen

### Telegram Morning Briefing (Cron Job, delivery: "origin")

Für das `yuno-morning-briefing` und ähnliche Telegram-Cron-Jobs mit `delivery: "origin"`:
Das Format hat **drei feste Sektionen** (ESL/CS2, Tech & Security, Gaming) mit strikten Constraints
(~2500 Zeichen, Deutsch, Yuno-Ton, keine offenen Fragen, kein `send_message`).

**Volle Spezifikation:** `references/telegram-morning-briefing-format.md`

Quick pattern:
1. Run MorphReader: `python3 ~/scripts/morphreader_summary_v6.py --no-cve-ids --days 1`
2. Fallback-Datei: `~/scripts/morphreader-briefing.md`
3. Web-Recherche wenn MorphReader leer: `curl` zu HLTV RSS + BleepingComputer
**Volle Spezifikation:** `references/telegram-morning-briefing-format.md`

### Delivery-Probleme (BadRequest, last_delivery_error)

Wenn Crons `last_delivery_error: "Telegram send failed: Chat not found"` oder ähnliches zeigen, ist die Troubleshooting-Tabelle in **`references/cron-delivery-patterns.md`** (Sektion "Troubleshooting") der schnellste Weg zur Lösung. Deckt u.a.:

- `.env` überschreibt `config.yaml` (`.env` wins)
- `@username` vs numerische `chat_id` in `TELEGRAM_HOME_CHANNEL`
- Gateway-Restart-Ordering (erster Restart nach `.env`-Patch kann noch alten Wert laden)
- `cronjob(action='update')` ohne Feld-Updates gibt "No updates provided"

### Esports / Tech News Briefing (Cron Job)

For the dedicated `esports-tech-briefing` cron job, use the resilient multi-source fallback chain. Key principle: **never rely on a single source** — HLTV and Liquipedia are frequently Cloudflare-blocked.

Full fallback recipes and source-specific curl commands: see `references/hltv-liquipedia-esports-research.md` in the `research-tools` skill.

Quick pattern:
1. Try `web_search` + `web_extract` first
2. If blocked → `curl` to **HLTV RSS** (`https://www.hltv.org/rss/news`) for esports titles (works without Cloudflare!)
3. If security news needed → `curl` to **BleepingComputer** (`https://www.bleepingcomputer.com/news/security/`)
4. If all fail → read local cache `~/Schreibtisch/wichtigsten Nachrichten.md` for last known state
5. Always note which sources were unavailable in the output

### Efficiency Notes

- **System check:** `sysdoctor check` is the preferred tool. It does disk/RAM/temp/GPU/cache/kernel/updates in one call. Fallback: manual `df -h`, `free -h`, `sensors`.
- **Gmail check:** Use server-side SEARCH (FROM/BEFORE/SUBJECT via IMAP), NOT one-by-one header fetch. Example:
  ```python
  conn.search(None, '(FROM "noreply")')     # instant
  conn.fetch(msg_id, '(BODY.PEEK[...])')     # slow - avoid for bulk
  ```
  Server-side SEARCH is ~100x faster than fetching headers individually.
- **Cron job check:** Always use `cronjob(action='list')`. Check `last_status` and `last_run_at` to see if jobs ran.
- **⚠️ web_search Firecrawl-Fallback:** `web_search` kann mit `'NoneType' object has no attribute 'status_code'` fehlschlagen (Firecrawl-Backend offline). **Sofort auf `curl` umsteigen** — HLTV RSS und BleepingComputer sind direkt per curl erreichbar und oft zuverlässiger als die Such-API. `web_extract` generiert zudem manchmal kaputte URLs (`/v2/scrape` statt voller URL) — für RSS/HTML immer direkt `curl` nutzen.

### Referenzen
- `references/briefing-template.md` — Vorlage zum Kopieren, Session-Such-Guide, Cron-Checkliste, System-Schwellwerte
- `references/telegram-morning-briefing-format.md` — Telegram Morning Briefing: 3-Sektionen-Format, Datenquellen-Reihenfolge, Parsing-Pitfalls
- `references/telegram-delivery-errors.md` — Drei Diagnostic-Patterns für Cron-Delivery-Fehler (Chat-not-found, Timed-out, Provider-401) + Provider-Switch-Workflow + Ollama-Cloud-vs-Local Klärung
- `references/morphreader-data-source.md` — MorphReader v6 CLI-Optionen, Format-Details, Fallback
- `references/gmail-server-search.md` — IMAP server-side SEARCH patterns
- `references/cron-delivery-patterns.md` — Cron output delivery conventions + Missing-Script Detection
- `references/cron-job-validation.md` — Validierungs-Checkliste nach Merges, Recovery-Flow für fehlende Skripte
- `references/system-services-check.md` — ollama/tokentelemetry service status
- `research-tools/references/hltv-liquipedia-esports-research.md` — Resilient esports/news source fallback chain
