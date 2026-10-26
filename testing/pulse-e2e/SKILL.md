---
name: pulse-e2e
description: Dashboard-Workflows von Pulse im echten Browser (Playwright, headless) testen oder neue E2E-Tests schreiben – Seite öffnen, Formular ausfüllen, speichern, Ergebnis und Persistenz prüfen, Desktop und Mobil. Verwenden bei UI-/Formular-/Routenänderungen im Dashboard oder wenn ein E2E-Test fehlt.
argument-hint: [run | neuer Workflow, z. B. "Teamrollen speichern"]
disable-model-invocation: true
---

# Pulse-E2E (Playwright)

## Umgebung
- Einmalig: `python -m pip install --require-hashes -r requirements-dev.lock` (gepinnt, wie CI) und `python -m playwright install chromium`.
- Server: `tools/preview_server.py` – echte FastAPI-App, Fake-Guild (`tests/fakes.py`), Fake-Login (`--role admin|team`), temporäre Daten, bindet nur 127.0.0.1, **kein Discord, kein OAuth**.
- Referenztest: `tests/test_e2e_dashboard.py` – Basisklasse `_PreviewE2EBase` (Server als Subprozess auf freiem Port mit `--e2e-hooks`, `TMP` auf TemporaryDirectory, Serverausgabe in eine Logdatei statt PIPE, externe Requests per `context.route` blockiert, `PULSE_GITHUB_REPO=""`). Neue Klasse = eigener Server; `ROLE = "team"` für Rechte-Tests. Gespeicherte Werte über `self._config()` direkt prüfen.
- Serverfehler: `POST /__preview/maintenance {"on": true}` (echter Restore-Sperrmodus → 503) und `GET /__preview/fail` (echte 500-Seite). Immer per `addCleanup` zurücksetzen. Client-Fehler (API 500, Netzwerk weg) per `page.route(...).fulfill/abort`.

## Ausführen
```
PULSE_E2E=1 python -m unittest tests.test_e2e_dashboard -v
```
Ohne `PULSE_E2E=1` wird bei fehlendem Playwright übersprungen (normale CI/unittest discovery). Der CI-Job `e2e` in `.github/workflows/python-syntax.yml` setzt `PULSE_E2E=1`.

## Neuen Workflow-Test schreiben
1. **Aktive Route klären:** `pulse_pro.py` überschreibt viele Seiten (z. B. `/settings` → Formular an `/settings/pro-goal`). Im gerenderten HTML prüfen, welches `form action` wirklich ausgeliefert wird – nicht im ersten Treffer in `webserver.py`.
2. **Locator** über `form[action="…"]` + `name`-Attribute oder Rolle/Beschriftung, keine CSS-Klassen (Tailwind ändert sich).
3. **Ablauf:** `goto` → Status 200 → ausfüllen → `with page.expect_navigation(): click()` → Erfolgsmeldung im `#toast[role=status]` (Fehler: `role=alert`). Die URL verliert `?msg=…` per `history.replaceState`, also nicht auf die URL prüfen.
4. **Persistenz:** Seite neu laden und gespeicherten Wert prüfen.
5. **Negativfall:** Browser-Validierung (`min/max/required`) per `evaluate` entfernen und prüfen, dass der Server selbst ablehnt/begrenzt und **nichts Ungültiges gespeichert** wird. Für Rechte: `--role team` auf Admin-Seite → 403, keine Änderung.
6. **Mobil:** `viewport 375×812, is_mobile=True` und `scrollWidth - innerWidth <= 1` (kein horizontaler Überlauf).
7. `page.on("pageerror")` sammeln und am Ende `[]` erwarten.
8. Tests unabhängig von der Reihenfolge halten (alle Tests einer Klasse teilen einen Server).

## Grenzen
Keine Tests gegen den VPS, Produktions-URLs oder echte Discord-Logins. Ergebnis ehrlich berichten (bestanden/fehlgeschlagen/übersprungen + Grund).
- Nicht bei jedem kleinen Backend-Fix laufen lassen – nur bei Dashboard-/Formular-/Routenänderungen; sonst `/pulse-verify targeted`.
- Warten über `expect`/`wait_for_*`, nie feste `sleep`s. Für lange Seiten auch Scrollposition nach Speichern prüfen.
- Der Test-Server muss im `tearDownClass`/`finally` beendet werden; danach keinen laufenden Prozess auf dem Port zurücklassen.
- Das Playwright-MCP-Plugin nur zum Erkunden/Debuggen nutzen; was dauerhaft gelten soll, gehört als Test in `tests/`.
- Fehlschlag dokumentieren: Test-ID, Schritt, erwarteter vs. tatsächlicher Zustand, `pageerror`-Ausgabe; Screenshots nur ins Scratch-/Temp-Verzeichnis.
