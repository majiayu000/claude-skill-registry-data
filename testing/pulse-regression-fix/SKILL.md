---
name: pulse-regression-fix
description: Einen gemeldeten Pulse-Fehler reproduzierbar machen und dauerhaft absichern – Regressionstest zuerst (muss vor dem Fix fehlschlagen), dann minimaler Fix, dann passende Testsuite. Kennt wiederkehrende Fehlerklassen von Pulse (überschriebene Routen, Discord 403/404/429, Zeitzonen, Rechte, JSON/DB-Altdaten). Verwenden bei Bugmeldungen, Rückfällen bereits behobener Fehler oder vor Merge eines Bugfixes.
argument-hint: <Fehlerbeschreibung | Issue | Logauszug>
---

# Pulse-Regression-Fix

## Ablauf
1. **Fehler eingrenzen:** Symptom, betroffene Route/Command/Job, erwartetes vs. tatsächliches Verhalten. Bereits bekannt? `git log --oneline --grep=<stichwort>`, `tests/test_*regression*`, Abschnitt mit Fehlerbildern in `docs/CLAUDE_CODE_HANDOFF.md` (gezielt suchen, nicht ganz lesen).
2. **Aktiven Code finden:** Bei Dashboard-Routen alle Registrierungen derselben Route prüfen – `pulse_pro` u. a. ersetzen Handler zur Laufzeit. Bei Slash-Commands den Cog in `cogs/`.
3. **Regressionstest schreiben – vor dem Fix:** im passenden `tests/test_<bereich>.py` (oder neu), Docstring mit kurzer Fehlerbeschreibung. Test ausführen und bestätigen, dass er **aus dem richtigen Grund fehlschlägt**. Ohne fehlschlagenden Test kein Fix (Ausnahme begründen).
4. **Minimaler Fix:** nur die Ursache, keine Nebenumbauten, keine Funktion abschwächen (Regel 1).
5. **Prüfen:** Regressionstest grün, dann die Tests des Bereichs, bei Rechten/Daten/mehreren Modulen der volle CI-Satz (`python -m unittest discover -s tests -p "test_*.py"`). UI-Fehler zusätzlich mit `/pulse-e2e`.

## Sicherheitsgrenzen
- Darf Dateien bearbeiten, aber muss vor dem Fix den Regressionstest rot sehen (oder begründen, warum das nicht möglich ist).
- Keine Commits, Pushes, Merges, Releases, VPS-/Produktiv-Deployments oder echten Discord-Aktionen ohne ausdrücklichen Auftrag.
- Niemals Laufzeitdaten, Secrets oder lokale `.env`-Dateien lesen, ändern oder committen.
- Keine bestehenden Funktionen entfernen oder Tests abschwächen, nur um die Suite grün zu bekommen.

## Wiederkehrende Fehlerklassen (Testidee je Klasse)
| Klasse | Typisches Symptom | Test |
|---|---|---|
| Überschriebene Route | Fix in `webserver.py` wirkt nicht | Route über `ws.app` aufrufen, nicht Funktion direkt; `tests/test_route_snapshot.py` |
| Discord 403/404/429/Timeout | Command/Job bricht ab, Spam-Retry | Fake wirft `discord.Forbidden/NotFound/HTTPException(429)`; erwartet: Meldung, kein Crash, kein Endlos-Retry (`tests/fakes.py`) |
| Rechte | Team sieht/ändert Admin-Daten | Nicht-Admin-Request → 403 **und** Daten unverändert |
| Zeitzone/Datum | Schicht/Woche/Ablauf um 1–2 h oder 1 Tag falsch | feste Zeiten um Mitternacht/DST-Wechsel über `pulse_time` |
| Altdaten | KeyError/TypeError nach Update | Datei/DB im alten Format laden |
| Team-Kick | Server-Kick statt Rollenentzug | Fake-Member: `kick` nie aufgerufen (`tests/test_team_kick.py`) |
| Persistente Views/Buttons | Buttons tot nach Neustart | `tests/test_persistent_buttons.py`-Muster |
| Nebenläufige Speicherung | Änderungen verschwinden | zwei Writer, `pulse_store.merge_entry` |
| Import-Seiteneffekte | Start hängt/verbindet beim Import | `tests/test_import_side_effects.py`-Muster |

## Ergebnis (Deutsch)
Ursache (1–2 Sätze, `datei:zeile`), Testname, Nachweis „vor Fix rot / nach Fix grün“, ausgeführte Suiten mit echtem Ergebnis, Restrisiko. Fehlerklasse neu? Dann Tabellenzeile hier ergänzen vorschlagen.