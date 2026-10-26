---
name: pulse-deploy
description: Safely deploy a tested Pulse commit to the production VPS. Only use when the user explicitly invokes /pulse-deploy and has requested deployment in the current conversation.
disable-model-invocation: true
argument-hint: [optional commit SHA]
---

# Pulse Produktions-Deployment

Dies ist ein produktiver Vorgang. Diese Skill darf nur laufen, wenn der Nutzer in dieser Unterhaltung ausdrücklich ein VPS-Deployment verlangt hat und sie manuell aufruft. Eine erfolgreiche CI oder ein Commit allein ist keine Erlaubnis zum Deployen.

1. Lies die aktuelle VPS_DEPLOYMENT.md und .github/workflows/deploy-vps.yml; prüfe die tatsächliche Konfiguration, statt alte Befehle blind zu übernehmen. Die Repository-Variable `PULSE_AUTO_DEPLOY` und GitHub-Schutzregeln nie selbst setzen oder ändern.
2. Prüfe Git-Branch, HEAD, Arbeitsbaum, Ziel-SHA und CI-Status für genau diesen SHA. Bei ungeklärten versionierten Änderungen, falschem Branch, fehlender CI oder laufender/fehlgeschlagener CI abbrechen und Grund melden.
3. Stelle sicher, dass höchstens die bekannte lokale, nicht versionierte Datei assets/support_wait.mp3 zusätzlich vorhanden ist. Andere lokale Änderungen nicht überschreiben oder wegwerfen.
4. Erzeuge vor dem Update ein nur für root zugängliches Backup außerhalb des Repositorys. Sichere vorhandene Teamdaten, Konfigurationen, .env, alle SQLite-Dateien und lokale Medien insbesondere assets/support_wait.mp3. Nie Geheimnisse ins Terminal, in Git oder die Zusammenfassung ausgeben.
5. Update nur mit sicherem Fast-Forward auf den bestätigten Commit. Verwende Docker Compose für den Build/Start. Nutze niemals git clean, git push --force oder docker compose down -v.
6. Warte auf den tatsächlichen Healthcheck und prüfe JSON-Felder ok, bot_ready, guild_ready und database_ok sowie die installierte pulse_version. Ein kurzzeitiger 503 während des Starts ist nicht allein ein Fehler, aber der finale Zustand muss gesund sein.
7. Bei Build-/Healthcheckfehlern Logs sichern und Ursache berichten. Code-Rollback nur kontrolliert nach Erhalt des Backups und Prüfung, dass keine Nutzeränderungen betroffen sind. Laufzeitdatenbanken nicht automatisch auf eine ältere Kopie zurücksetzen, da dabei neue Daten verloren gehen könnten.
8. Abschluss: Ziel-Commit, Version, Containerstatus, Healthcheck und Backup-Pfad nennen. Klare Warnung statt Erfolgsbehauptung, wenn irgendeine Prüfung fehlt.