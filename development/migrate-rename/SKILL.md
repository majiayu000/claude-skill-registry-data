---
name: migrate-rename
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-09-06
description: Evolutionary file renaming with wrapper files, plus the terse MOVED-stub standard for whole folder/file moves. Enables renames without hard breaks — references are organically updated through usage.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="migrate-rename banner">

# Datei-Umbenennung mit Wrapper (Evolutionaere Migration)

> Ermoeglicht Datei-Umbenennungen OHNE harte Brueche. Verweise werden organisch durch taegliche Nutzung aktualisiert.

---

## Prinzip: Evolutionaere Migration

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

Wer den alten Pfad aufruft:
1. Landet bei der Wrapper-Datei
2. Traegt sich ins Log ein
3. Korrigiert den Verweis der ihn herschickte
4. Geht zur eigentlichen Datei

---

## Schritt-fuer-Schritt

### 1. Datei umbenennen

```bash
mv alte_datei.md neue_datei.md
```

### 2. Wrapper-Datei erstellen

Erstelle `alte_datei.md` mit folgendem Inhalt:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: `neue_datei.md`

---

**Zieldatei:** `neue_datei.md`
```

### 3. Kritische Verweise sofort korrigieren
- Help-Dateien (primaere Dokumentation)
- System-Prompt Referenzen
- CLI-Code der den Pfad direkt verwendet

### 4. Uebrige Verweise evolutionaer migrieren
Der Rest wird automatisch korrigiert bei Nutzung.

---

## Wann Wrapper-Methode verwenden?

**JA - Wrapper sinnvoll:**
- Viele potenzielle Verweise
- Datei wird von verschiedenen Partnern/Tools referenziert
- Keine kritische System-Datei

**NEIN - Direkt alle aendern:**
- Wenige, bekannte Verweise
- Kritische System-Dateien (config, DB-Schema)
- Performance-kritische Pfade

---

## Ordner-/Datei-Umzug mit MOVED-Stub

> Formalisiert 2026-09-06 (Ticket T-20260906-688261413). Präzedenz spontan entstanden bei
> `.ELLMOS.MIGRATED.md` (2026-08-11) und den `_control-center/_CONTROL`-Stubs (2026-09-06).

Andere Situation als der Wrapper oben: Hier zieht ein **ganzer Ordner** oder eine **Datei ohne
viele aktive Referenzen** komplett an einen neuen Ort um (Konsolidierung, Umbenennung,
Pipeline-Reorganisation). Es gibt keinen Migrations-Log, kein "Verweis korrigieren" — nur einen
terse Pointer, der sagt: hier ist es jetzt.

**Unterschied zum Wrapper-Verfahren oben:**

| | Wrapper (Schritt 1-4 oben) | MOVED-Stub |
|---|---|---|
| Einsatz | Einzeldatei, viele aktive Verweise, sollen organisch nachziehen | Ordner oder Datei, kompletter Umzug |
| Inhalt | Migrations-Log-Tabelle, wächst mit Nutzung | Statische Metadaten, 1-3 Zeilen Klartext |
| Lebensdauer | Bis Log zeigt: keine neuen Einträge mehr | Bis `remove_when` erfüllt ist |

### Name, Ort, Pflichtfelder

Vollständiges Schema, Beispiel und Feld-Semantik stehen im ellmos-Template `MOVED-STUB.md`
(`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`, kein Teil dieses standalone-Repos —
Kurzfassung genügt hier):

- **Name/Ort:** `<alter-Name>.MOVED.md` liegt dort, wo der Ordner/die Datei **vorher** lag.
- **Pflichtfelder** (`key: value`, in dieser Reihenfolge): `moved_to`, `moved_on`, `ticket`,
  `reason`, `moved_by`, `remove_when` (Default: `90 Tage UND 0 lebende Referenzen`).
- **Danach** 1-3 Zeilen Klartext für Menschen. Kein Log, keine Tabelle, keine Historie — die
  steht im referenzierten Ticket.
- **Rückbau:** Stub wird **gelöscht**, nie archiviert.

### Policy

Verbindlich als `.SYNC/_policies/library/P-017_umzugs-stub.md`.

### Prüfskript

`scripts/moved_stub_check.py` (in diesem Skill-Ordner) listet alle `*.MOVED.md`/`*.MIGRATED.md`-
Stubs unter einem Wurzelverzeichnis, meldet fehlende Pflichtfelder und markiert rückbau-fällige
Stubs (älter als `remove_when`-Tage). Aufruf:

```bash
python scripts/moved_stub_check.py <wurzelverzeichnis>
```

---

## Cleanup

Nach ca. 30 Tagen oder wenn Log zeigt dass keine neuen Eintraege:
1. Wrapper-Datei nach `_archive/deprecated/` verschieben
2. Oder komplett loeschen (wenn keine Eintraege mehr)

---

## Changelog

### 1.1.0 (2026-09-06)
- Abschnitt "Ordner-/Datei-Umzug mit MOVED-Stub" ergänzt (Ticket T-20260906-688261413):
  formalisiert den terse Umzugs-Pointer für ganze Ordner/Dateien (Standard `<alter-Name>.MOVED.md`,
  Pflichtfelder moved_to/moved_on/ticket/reason/moved_by/remove_when), abgegrenzt vom
  Wrapper-Verfahren oben. Prüfskript `scripts/moved_stub_check.py` ergänzt.

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
