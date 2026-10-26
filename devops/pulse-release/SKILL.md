---
name: pulse-release
description: Read-only Release- und Merge-Vorbereitung für Pulse. Prüft Version, Changelog, CI, Branch-Diff, Daten-/Konfigurationsrisiken und manuelle Betriebsschritte; führt selbst keinen Release, Merge oder Deployment aus.
argument-hint: [PR-Nummer | Branch | Version]
disable-model-invocation: true
disallowed-tools: Edit, Write, NotebookEdit
---

# Pulse-Release (nur Vorbereitung)

Dieser Skill erstellt eine Prüfliste und ändert nichts. Kein Commit, Push, Merge, Tag, GitHub-Release, VPS-Deployment oder echte Discord-Aktion ohne ausdrücklichen Auftrag. `.env`, Tokens und Laufzeitdaten nicht lesen.

## Prüfschritte
1. **Branch / Diff:** `git status --short`, Branch und HEAD prüfen; Diff gegen das Ziel vergleichen. Lokale, uncommittete Änderungen gesondert nennen und nicht überschreiben.
2. **Version:** `pulse_version.py` als maßgebliche Versionsquelle verwenden. Prüfen, ob Changelog-Eintrag und Dokumentation zur Änderung passen; Version nicht automatisch erhöhen.
3. **Qualität:** passende Tests und CI-Status für den exakten HEAD prüfen. Test-Skips, nicht ausgeführte Tests und bekannte Warnungen transparent nennen.
4. **Sicherheit / Daten:** Rechte, Secrets, Runtime-Dateien, Migrationen, Backup-/Restore-Pfade und mögliche irreversible Schritte prüfen.
5. **Betrieb:** nötige Variablen, Host-Agent-Konfiguration, Healthchecks und manuelle VPS-Schritte aus der vorhandenen Betriebsdokumentation zusammenstellen. Keine Secrets ausgeben und nichts auf dem VPS ändern.
6. **Risiken:** bekannte offene Punkte, Rückweg/Rollback und Abhängigkeiten benennen. Code-Rollback nicht mit Datenbank-/Runtime-Rollback verwechseln.

## Ausgabe
- Release-/Merge-Empfehlung mit belegten Gründen.
- Checkliste: bestanden / fehlgeschlagen / offen.
- Exakter geprüfter Commit und CI-Status, sofern verfügbar.
- Konkrete manuelle Schritte nach dem Merge.
- Klarer Hinweis: Dieser Skill führt selbst keine Veröffentlichungsaktion aus.