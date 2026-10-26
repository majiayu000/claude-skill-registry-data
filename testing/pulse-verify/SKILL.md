---
name: pulse-verify
description: Manually verify Pulse changes before a commit, release, or deployment. Use only when the user invokes /pulse-verify.
disable-model-invocation: true
argument-hint: [targeted|full]
---

# Pulse-Verifikation

Nur prüfen, nicht committen, pushen, deployen oder Dateien automatisch ändern.

1. Prüfe aktuellen Branch, HEAD, git status --short und git diff --check. Bewahre alle vorhandenen Änderungen.
2. Diff selbst durchsehen (nicht nur `--stat`): keine Secrets/Tokens/.env-Inhalte, keine Laufzeitdaten (`*.db`, `team_data.json`, `config.json`, Backups), kein Debug-Code (`print`-Reste, `breakpoint()`), keine unbeabsichtigt entfernten Funktionen oder abgeschwächten Prüfungen/Tests.
3. Wenn $ARGUMENTS "targeted" ist, bestimme anhand der Diff-Dateien die passenden vorhandenen Regressionstests und führe diese sowie compileall aus. Wenn kein klarer Test zugeordnet werden kann, suche zuerst nach ähnlichen Tests.
4. Standardmäßig oder bei $ARGUMENTS "full" führe die gleichen Qualitätsschritte aus wie .github/workflows/python-syntax.yml:
   - python -m ruff check .
   - python -m compileall -q .
   - python tests/feature_smoke.py
   - python tests/smoke_test.py
   - python -m unittest discover -s tests -p 'test_*.py'
5. E2E nur, wenn nötig: `git diff --name-only HEAD | python tools/ci_e2e_needed.py` (gleiche Regel wie die CI). Bei `true` und installiertem Playwright `PULSE_E2E=1 python -m unittest tests.test_e2e_dashboard -v`, sonst als „nicht ausgeführt + Grund“ melden. Berührt der Diff Rechte, Sessions/OAuth, Uploads, Datenzugriffe oder externe Requests: auf `/pulse-security-audit` hinweisen (nicht selbst starten).
6. Starte keine Tests, die echte Discord-/OAuth-/Produktionsaktionen auslösen. Wenn ein Test das erfordert, überspringe ihn, nenne den Grund und suche eine sichere Alternative.
7. Reporte jeden tatsächlich ausgeführten Check mit bestanden/fehlgeschlagen/übersprungen. Behaupte nie, dass die Tests bestanden sind, wenn sie nicht ausgeführt wurden. Fehler nicht verschweigen und bei fehlgeschlagenen Checks keine Freigabe für Deployment suggerieren.
8. Antworte kompakt auf Deutsch mit Ergebnis und konkreter nächster Aktion.