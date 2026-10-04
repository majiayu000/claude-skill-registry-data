---
name: openclaw-cli-quirks
description: "OpenClaw CLI Pitfalls + Workarounds für Agent-Writing (Cron add/edit, Provider-Drift-Schutz
  bei unpinned Crons, Live-config-Protection von openclaw.json, gh CLI Token-Scopes).
  Get hard-won Fixes statt Stolperfallen."
version: 2.0.0
author: Yuno (MaxClaw-Betreiberin via Owl Alpha)
license: MIT
triggers:
  - "openclaw cron"
  - "openclaw cron add"
  - "openclaw cron edit"
  - "cron pin"
  - "provider drift"
  - "openclaw config"
  - "openclaw.json protected"
  - "gh createPullRequest"
  - "Pitfall #10"
  - "OpenClaw-CLI"
---

# OpenClaw CLI — Quirks & Workarounds

Hard-won Erfahrungen aus dem MaxClaw-Betrieb. Lade diesen Skill **bevor** du Cron-Jobs
anlegst oder die OpenClaw-Config editierst — spart 5-10 Min Trial-Error.

> Hinweis: OpenClaw entwickelt sich schnell (Anfang 2026: 7 Updates in 2 Wochen). Exakte
> Flags immer mit `openclaw cron --help` / `openclaw config --help` gegen die **installierte
> Version** prüfen. Die Muster unten gelten versionsübergreifend, einzelne Flag-Namen ggf. nicht.

## When to use

- Du willst Cron-Jobs anlegen, updaten oder löschen
- Du arbeitest mit `openclaw config` und willst nicht versehentlich die Live-Config zerschießen
- Ein Cron-Lauf bricht mit „drifted / unpinned"-Fehler ab
- Du willst PRs via gh CLI anlegen und es schlägt fehl
- Du brauchst eine **Liste der bekannten OpenClaw-CLI-Edge-Cases**

## Pitfall-Tabelle (was geht NICHT wie erwartet)

### Pitfall #1: Modell wird nicht beim `cron add` gesetzt

**Symptom:** Ein hingeworfenes `--model heavy` beim Anlegen wird ignoriert oder abgelehnt —
der Cron läuft am Ende auf dem globalen Default-Modell statt auf dem gewünschten.

**Fix:**
1. Cron erst **ohne** Modell-Angabe anlegen (OpenClaw nimmt Default).
2. **Danach** gezielt auf Provider/Modell pinnen (via `openclaw cron edit <id>` bzw. dem
   Session-Modell). Flag-Namen mit `openclaw cron --help` verifizieren.

```bash
openclaw cron add --name "greyhack-quality-chain" \
  --cron "0 7 * * 1-5" --tz "Europe/Berlin" \
  --session "session:greyhack-chain" \
  --message "Führe die Quality-Chain aus. Prüfe Source-Freshness vor Summary." \
  --announce

# Job-ID aus Output notieren, dann Modell pinnen (Syntax gegen --help prüfen).
```

### Pitfall #2: `cron edit` kennt evtl. kein `--model/--provider`

**Symptom:** `openclaw cron edit <job-id> --model heavy` → `unrecognized arguments`.

**Fix:** Wie #1 — Modell-Pin läuft über den Session-/Job-Provider, nicht über ein Ad-hoc-Flag.
Immer erst `--help` lesen.

### Pitfall #3: Provider-Drift — unpinned Cron verweigert Lauf

**Symptom:** Jeder Cron-Lauf endet mit sinngemäß:
```
Skipped to prevent unintended spend: global inference config drifted since this job
was created (provider 'X' -> 'Y'; model 'A' -> 'B'), and this job is unpinned.
```

**Ursache:** Die globale Inference-Config wechselt (z.B. Default-Provider gewechselt), aber
der Cron hat seinen **alten** Pin. OpenClaw weigert sich zu laufen, um ungewollte Spends zu
verhindern — bewusstes Sicherheitsverhalten.

**Fix:** Alle betroffenen Crons auf die **aktuelle** Provider/Modell-Kombination re-pinnen:

```bash
# 1. Aktuelles Default-Routing aus openclaw.json holen
grep -E "primary|model" ~/.openclaw/openclaw.json | head

# 2. Fehlgeschlagene Crons listen und pro Job re-pinnen
openclaw cron list 2>/dev/null | grep -iE "error|drift|skipped"
```

**Prävention:** Nach jedem globalen Provider/Modell-Wechsel direkt alle Crons re-pinnen.

### Pitfall #4: `~/.openclaw/openclaw.json` ist Agent-write-protected

**Symptom:** Versuch, `openclaw.json` per `patch`/`edit`-Tool zu schreiben →
```
Refusing to write to OpenClaw config file: /home/bratan/.openclaw/openclaw.json
Agent cannot modify security-sensitive configuration. Edit ~/.openclaw/openclaw.json
directly or use 'openclaw config' instead.
```

**Ursache:** OpenClaw-Built-in-Schutz. Der Agent darf Live-Settings nicht versehentlich
zerschießen.

**Fix:** Eine von drei Optionen:
1. **User-Action:** `openclaw config set <key> <value>` oder direkter Edit durch Basti.
2. **Workaround:** Änderung in der Repo-Vorlage `config/openclaw.json` dokumentieren + die
   nötige User-Aktion festhalten (siehe `docs/bastimd/security-remediation-2026-07-04.md`).
3. **Validieren statt raten:** `openclaw config validate && openclaw doctor --fix` nach jedem
   Edit — `doctor --fix` strippt unbekannte Keys und migriert veraltete.

### Pitfall #5: `cron list` zeigt nach Pin manchmal noch alten Provider

**Symptom:** Gerade re-gepinnt, aber `openclaw cron list` zeigt weiter den alten Provider.

**Fix:** Meist nur Anzeige-Lag — die echte Execution nutzt das neue Modell. Verifiziere per
manuellem Lauf statt der Listen-Anzeige zu vertrauen:

```bash
openclaw cron run <job_id>     # Status sollte 'ok' mit neuem Provider/Model sein
openclaw cron list 2>&1 | grep -A 8 "$job_id"
```

### Pitfall #6: gh CLI kann PRs nur mit passenden Token-Scopes anlegen

**Symptom:**
- `gh pr create` → `GraphQL: Resource not accessible by personal access token (createPullRequest)`
- `gh api repos/X/Y/pulls` POST → `401 Bad credentials`

**Ursache:** Das gh-Keyring-Token hat oft nur `gist, read:org, repo, workflow` — PR-Erstellung
braucht ggf. mehr.

**Fix:** Push via `git push origin <branch>`, dann PR im Browser öffnen:
```
https://github.com/<owner>/<repo>/compare/main...<branch>
```

## Pattern (lauffähig)

### Komplett-Workflow „Cron sicher registrieren"

```bash
# 1. register-workflows.sh (idempotent, mehrfach ausführbar)
./workflows/register-workflows.sh --dry-run    # Vorschau
./workflows/register-workflows.sh              # alle
./workflows/register-workflows.sh --add <NAME> # nur einer
./workflows/register-workflows.sh --list       # Workflows anzeigen

# 2. Provider-Drift erkennen (read-only)
openclaw cron list 2>&1 | grep -iE "drift|skipped|error"

# 3. Alle Crons smoke-testen (nicht gleichzeitig -> Rate-Limits)
openclaw cron list 2>/dev/null    # Job-IDs sammeln, dann einzeln:
# openclaw cron run <job_id>; sleep 2
```

## Pitfalls (was schiefgehen kann)

- ❌ Cron-Pin ohne Provider — Modell wird nicht gesetzt, Drift-Fehler bleibt
- ❌ Alle Crons gleichzeitig triggern → Rate-Limits des LLM-Providers
- ❌ `openclaw cron edit --workdir /tmp/Pfad` der nicht existiert → scheitert silent
- ❌ `gh pr create` mit `main` als Quelle ohne Force → fataler Conflict
- ✅ **Immer zuerst** mit `openclaw cron run <job_id>` testen, ob der Pin sitzt
- ✅ **register-workflows.sh --dry-run** vor jedem echten Lauf (Default-Deny-Mentalität)
- ✅ Nach jedem Config-Edit: `openclaw config validate && openclaw doctor --fix`

## Siehe auch

- MaxClaw-Audit-Report mit allen P0/P1-Findings: `docs/reports/security-audit-2026-07-04.md`
- Multi-Agent-Pitfall-Checkliste: `~/.openclaw/skills/orchestration/pitfalls/SKILL.md`
- Workflow-Templates: `workflows/greyhack-*.md`
