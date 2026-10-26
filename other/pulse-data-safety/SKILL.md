---
name: pulse-data-safety
description: Sichere Datenänderungen in Pulse – SQLite-Schema, JSON-Dateien (Config, Teamdaten, Schichten, Audit), Migrationen, Backups/Restore, Retention und Bereinigungen. Verwenden, bevor Code geschrieben oder gemergt wird, der gespeicherte Daten liest, umformt, migriert, löscht oder wiederherstellt.
argument-hint: [diff | Datei/Tabelle/JSON-Datei]
---

# Pulse-Data-Safety

Projektregel 2: **keine Laufzeitdaten löschen, zurücksetzen oder inkompatibel migrieren.** Echte Laufzeitdateien im Arbeitsbaum (`*.db`, `team_data.json`, `audit_logs.json`, `backups/`, `transcripts/`, `attachments/`) nie öffnen zum Schreiben, nie committen, nie in Tests verwenden.

## 1. Datenlandkarte
Betroffene Speicher bestimmen: `docs/DATENLANDKARTE.md` (gegen Code prüfen), `pulse_db.DB_PATH`/`PULSE_DB_PATH`, JSON-Konstanten in `webserver.py` (`DATA_FILE`, `CONFIG_FILE`, `LOGS_FILE`, `SHIFTS_FILE`, `MEETINGS_FILE`, `APPS_FILE`, `AUDIT_FILE`), weitere `.db` (Abmeldungen, Activity-Check). Alle Leser und Schreiber suchen – auch in `cogs/` und `pulse_pro.py`.

## 2. Regeln für die Änderung
1. **Schreiben:** JSON nur über `save_json` (atomar: `.tmp` + `os.replace`); parallele Bearbeitung über `pulse_store.merge_entry` statt blindem Überschreiben (`tests/test_concurrent_writes.py`).
2. **Lesen tolerant:** Fehlende Schlüssel mit Default (`setdefault`/`get`), alte Formate weiter lesbar, unbekannte Felder erhalten (nicht beim Speichern verwerfen).
3. **SQLite-Schema:** Nur additiv (neue Tabelle/Spalte mit Default, Index). Über `pulse_migrations` als benannte, idempotente Migration – sie sichert `pulse.db` vorher und läuft in einer Transaktion. Kein `DROP`/`RENAME` ohne Lesefallback und Rückweg.
4. **JSON → SQLite:** Datei für Datei, mit Lesefallback auf die alte Quelle, Original bleibt erhalten, Rückweg dokumentiert.
5. **Löschen/Retention:** Nur ausdrücklich gewollt, begrenzt, protokolliert (`log_audit`), vorher Backup; `pulse_retention`/`pulse_backup.prune_auto_backups` nicht aufweiten ohne Auftrag.
6. **Backup/Restore:** `pulse_backup` – Manifest + SHA-256 + `PRAGMA integrity_check`, `preview_restore` vor `restore_full_backup`, Zip-Einträge über `_safe_member`, Wartungsmodus während Restore. Restore nie blind auf Produktion.
7. **Fehlschlag:** Abbruch mitten in der Änderung darf keinen halben Zustand hinterlassen (Transaktion / temp + replace) und muss beim nächsten Lauf sauber wiederholbar sein.

## 3. Tests (Pflicht bei Datenänderungen)
Mit `tempfile.TemporaryDirectory` und gepatchtem `pulse_db.DB_PATH` / JSON-Pfaden (Muster: `tests/test_healthz.py`, `tests/test_migrations.py`):
- Altdaten (vorheriges Format) → werden korrekt gelesen/migriert
- leere/fehlende Datei, ungültige Werte, kaputtes JSON
- zweimal ausführen → idempotent
- Fehler mitten drin → Originaldaten unverändert, nächster Lauf klappt
- Backup vor Migration existiert und ist wiederherstellbar
Vorhandene: `test_migrations`, `test_full_backup`, `test_json_safety`, `test_concurrent_writes`, `test_db_path`, `test_team_protection_db`, `test_warning_expiry_cleanup`.

## 4. Ergebnis (Deutsch)
Betroffene Speicher, Rückwärtskompatibilität (ja/nein + Begründung), Backup-/Rückweg, ausgeführte Tests mit echtem Ergebnis, Restrisiken. Vor einem Deployment mit Datenänderung: Hinweis auf Sicherung laut `pulse-deploy`.
