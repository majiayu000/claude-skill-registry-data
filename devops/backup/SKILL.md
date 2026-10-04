---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: Plant, spiegelt, verifiziert, stellt wieder her oder archiviert Dateien explizit über den fail-closed mac-backup-Kern. Für die eigenen hostübergreifenden Backup-Jobs des Nutzers verwenden; nicht für allgemeine Cloud-Synchronisation oder beiläufiges Dateikopieren.
visibility: public
language: de
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="backup banner">

# Backup

Die installierte `mac-backup`-CLI als einzige Transfer-Implementierung verwenden. Den Ablauf nicht
mit rohem `scp`, `rsync`, SSHFS, Explorer-Aktionen oder Ad-hoc-Löschung nachbauen.

## Anfrage routen

- Eine gewöhnliche "Backup"-Anfrage bedeutet `mirror`; die Quelle bleibt unangetastet.
- `archive` bedeutet Quell-Bereinigung und ist eine eigene, destruktive Absicht. Niemals aus
  "backup", "copy" oder "free some space" ableiten.
- `restore` schreibt an ein neues Ziel und überschreibt nie stillschweigend.
- Existiert kein geprüftes Job-JSON, einen Job-Vorschlag vorbereiten und vor `init-target` oder
  Transfer anhalten.

## Ausführung

1. Den Job lesen und `mac-backup plan <job> --json` ausführen.
2. Prüfen, dass die zurückgegebene Quellklasse, Dateianzahl, Byte-Anzahl, Ziel-Volume-ID,
   Verschlüsselungsstatus und Host-Fingerprint mit der Anfrage und dem aktuellen Geräte-Beleg
   übereinstimmen.
3. Für Mirror `mac-backup mirror <job> --json` ausführen, danach `mac-backup verify <job> --json`.
4. Für Restore ein neues, absolutes Ziel verwenden und die wiederhergestellten Dateien über das
   Manifest-Ergebnis des Befehls verifizieren.
5. Für Archive `--confirm-delete` nur übergeben, wenn der Nutzer die Quell-Entfernung ausdrücklich
   verlangt hat und der geprüfte Plan genau diese Quelle nennt. Eine Policy-Blockade ist das
   korrekte Ergebnis; niemals `target_encryption_required`,
   `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, einen Lock, eine
   Identitätsabweichung oder einen fehlenden Anker umgehen.

`init-target` ist privilegiertes Setup, keine Routine-Ausführung. Es benötigt einen unabhängig
eingeholten Betriebssystem-Beleg für Volume-ID und Verschlüsselung; ein aus dem vorgeschlagenen
Job kopierter Wert ist kein Beleg.

Niemals behaupten, ein Mirror sei ein vollständiges Backup, bevor Ziel-Verify und ein echter
Restore-Test beide bestanden haben. Geheimnisse, echte Job-Dateien, lokale Anker und
Nutzer-Dateinamen aus Tickets, Git und OneDrive heraushalten.

## Changelog

### 1.0.0 (2026-08-24)
- Neutralisierte Kopie des `~/.claude/skills/backup/`-Deployment-Masters, in die kategorisierte
  Bibliothek aufgenommen. Ursache der Sync-Lücke: Der Skill war deployt, hatte aber keinen
  Quell-Eintrag unter `skills/<category>/`, weshalb `skill_sync.py status` ihn als `NUR-ZIEL`
  (nur Ziel) meldete und `catalog.py`/`build_public_registry.py` (die nur `skills/` scannen) ihn
  nie sahen — er konnte die öffentliche Registry oder `SKILLS-MAP.md` deshalb nie erreichen, egal
  wie die Deployment-Kopie bearbeitet wurde.
