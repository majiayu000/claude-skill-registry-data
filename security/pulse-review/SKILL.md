---
name: pulse-review
description: Unabhängiges Code-Review der Pulse-Änderungen (Branch gegen main oder ein PR) vor dem Zusammenführen – in einem frischen Kontext ohne Wissen des Autors. Verwenden vor Merge, PR-Erstellung oder wenn der Nutzer eine Zweitmeinung zu einem Diff will. Ändert keine Dateien.
argument-hint: [PR-Nummer | Branch | leer = aktueller Branch gegen main]
context: fork
disallowed-tools: Edit, Write, NotebookEdit
disable-model-invocation: true
---

# Pulse-Review (unabhängig, nur lesen)

Du bist **nicht** der Autor dieser Änderung. Übernimm keine Begründungen aus Commit-Texten oder PR-Beschreibungen ungeprüft – prüfe den Code. Ändere nichts: keine Dateien, keine Commits, kein Checkout/Stash, keine Kommentare auf GitHub ohne ausdrücklichen Auftrag. `.env` nicht lesen.

## 1. Diff bestimmen
- `$ARGUMENTS` leer: `git diff main...HEAD` plus `git status --short` (unversionierte Dateien nennen, nicht bewerten).
- PR-Nummer: `gh pr diff <nr>` und `gh pr view <nr>`.
- Branch: `git diff main...<branch>`.
Große Diffs dateiweise lesen (`git diff main...HEAD -- <datei>`), `webserver.py` nur in relevanten Hunks + umgebenden Funktionen.

## 2. Prüfen (je Hunk: Aufrufer und tatsächlichen Kontrollfluss nachvollziehen)
1. **Korrektheit:** Logikfehler, Randfälle (None, leere Listen, ungültige IDs), Zeitzonen (`pulse_time`), Async-Fehler (fehlendes `await`, blockierende Aufrufe im Event-Loop).
2. **Aktive Route:** `pulse_pro` u. a. ersetzen Handler zur Laufzeit (`remove_and_add`, `app.post(...)`). Prüfen, ob der geänderte Handler wirklich aktiv ist.
3. **Rechte:** Jede Dashboard-/Admin-Route ruft `auth(..., perm=…, admin=…)` serverseitig auf; Default = verweigern. Same-Origin-Schutz (`pulse_security.same_origin_ok`) nicht umgangen.
4. **Funktionsverlust:** Wurde vorhandenes Verhalten entfernt/abgeschwächt (Projektregel 1)? Team-Kick ≠ Server-Kick (Regel 5). AutoMod/Anti-Nuke/KI nicht still aktiviert (Regel 6).
5. **Daten:** Schema-/JSON-Änderungen rückwärtskompatibel, Migration mit Backup (`pulse_migrations`), `save_json` statt direktem Schreiben.
6. **Ressourcen:** Unbegrenzte Caches/Queues, neue Scheduler statt vorhandener, Discord-Rate-Limits/403/404/429.
7. **Tests:** Deckt ein Test die Änderung ab, inkl. Negativfall (keine Schreibaktion bei Ablehnung)? Fehlen Tests?
8. **Secrets/Dateien:** Keine Tokens, `.env`, Laufzeitdaten (`*.db`, `team_data.json`, `backups/`) im Diff.

Optional für eine zweite Perspektive: `/code-review` auf denselben Diff und Befunde abgleichen.

## 3. Ergebnis (Deutsch)
- **Urteil:** `freigeben` / `freigeben mit Anmerkungen` / `nicht freigeben`
- **Befunde**, nach Schwere sortiert (blockierend → wichtig → Hinweis), jeweils `datei:zeile`, konkretes Fehlerszenario (Eingabe → falsches Ergebnis) und Vorschlag. Nur belegte Befunde als blockierend; Vermutungen kennzeichnen.
- **Fehlende Tests** (konkret benennen)
- Keine Befunde erfinden, um die Liste zu füllen. „Keine blockierenden Befunde“ ist ein gültiges Ergebnis.