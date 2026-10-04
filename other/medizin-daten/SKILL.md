---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Local, private capture of medical data: diagnoses, symptom histories and examination plans. No BACH origin — custom design with its own SQLite store. Strictly local, no cloud transfer."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: de
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---
<img src="banner.png" width="100%" alt="medizin-daten banner">

## Zweck

Medizinische Eigendaten sicher und lokal erfassen: Diagnosen (ICD-10-Code
optional), Symptomverläufe mit Datumsreihen und Untersuchungspläne. Alle
Daten bleiben ausschließlich lokal in `medizin-daten/store.db`.

Der Skill ersetzt keine ärztliche Beratung und trifft keine medizinischen
Aussagen — er ist ein strukturiertes Notizbuch für persönliche Gesundheitsdaten.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Diagnose erfassen" | Neue Diagnose anlegen |
| „Diagnose [Name] hinzufügen" | Benannte Diagnose anlegen |
| „Symptomverlauf" | Symptome für heute erfassen |
| „Symptom [Name] erfassen" | Einzelnes Symptom eintragen |
| „Untersuchungsplan" | Nächste Termine/Untersuchungen anzeigen |
| „Termin hinzufügen" | Untersuchungstermin eintragen |
| „Zeig meine Diagnosen" | Diagnosenliste ausgeben |

---

## Workflow

1. **Modus erkennen**: Diagnose / Symptom / Untersuchungsplan
2. **Eingabe strukturieren**: Datum, Bezeichnung, Notizen, optionaler ICD-10-Code
3. **Speichern**: In `store.db` (lokal, kein Netzwerkzugriff)
4. **Ausgeben**: Lesbare Zusammenfassung für LLM-Kontext

---

## CLI-Einstieg

```bash
# Diagnose anlegen
python medizin_daten_core.py add-diagnosis "Hypertonie" [--icd I10] [--note "Anmerkung"]

# Diagnosen auflisten
python medizin_daten_core.py diagnoses

# Symptom erfassen
python medizin_daten_core.py add-symptom "Kopfschmerzen" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptomverlauf für eine Bezeichnung
python medizin_daten_core.py symptom-history "Kopfschmerzen" [--limit 30]

# Untersuchung planen
python medizin_daten_core.py add-exam "Blutbild" [--date 2026-07-01] [--note "nüchtern"]

# Anstehende Untersuchungen
python medizin_daten_core.py exams [--upcoming]

# Alternativer Store (z.B. für Tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Store

| Eigenschaft | Wert |
|---|---|
| Typ | SQLite |
| Pfad (Standard) | `skills/assist/medizin-daten/store.db` |
| Override | `--store <pfad>` oder Env `MEDIZIN_STORE` |
| Tabellen | `diagnoses`, `symptoms`, `examination_plans` |

### Schema

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (kurz: 8 Hex)
    name        TEXT NOT NULL,        -- Bezeichnung (z.B. "Hypertonie")
    icd_code    TEXT,                 -- ICD-10-Code optional (z.B. "I10")
    onset_date  TEXT,                 -- Beginn (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- Freitext-Notiz
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    name         TEXT NOT NULL,       -- Bezeichnung (z.B. "Kopfschmerzen")
    severity     INTEGER,             -- 1–10 Skala (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 Zeitstempel
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    exam_name    TEXT NOT NULL,       -- Untersuchungsbezeichnung
    planned_date TEXT,                -- Geplantes Datum (ISO-8601)
    done_date    TEXT,                -- Durchgeführt am (NULL = ausstehend)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## Haltung

- Keine medizinischen Empfehlungen, keine Diagnosestellung durch den Skill.
- ICD-10-Codes werden als Freitext gespeichert — keine Validierung gegen eine externe Datenbank.
- Severity-Skala 1–10 ist nutzer-subjektiv.
- Fehlende Werte (Datum, Schweregrad) sind immer erlaubt — das Notizbuch-Prinzip gilt.

---

## Datenschutz (Privacy-Gate)

> **WARNUNG: Medizinische Daten sind besonders schützenswert.**

- `store.db` enthält höchst sensible Gesundheitsdaten — **niemals in Git committen**.
- **Kein Netzwerkzugriff** — alle Operationen laufen vollständig lokal.
- **Keine Weitergabe** an externe Dienste, keine Sync mit Cloud-Backends.
- Backup-Empfehlung: Verschlüsseltes lokales Backup (z.B. `age`/`gpg`).
- Der Skill prüft beim Start, ob `store.db` außerhalb des lokalen Dateisystems liegt,
  und gibt eine Warnung aus wenn der Pfad in einem Sync-Ordner (OneDrive etc.) liegt.
- `~/.gitignore_global` oder lokales `.gitignore` sollte `store.db` ausschließen.

---

## Verwandte Ressourcen

- Skill `assist/gesundheit` — allgemeine Gesundheitsassistenz (nicht medizinische Daten)
- MediPlaner (`tools/module-installer` → `mediplaner`) — Medikamenten-Verwaltung (separates Programm)

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.1.0 | 2026-06-22 | Erstanlage — Eigenentwurf, Privacy-Gate, 3-Tabellen-Schema |
