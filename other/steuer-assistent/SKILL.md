---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: "Points to the standalone module steuer-assistent: a local, offline-first receipt worksheet for German employee income-related expenses (Werbungskosten) -- record, sum to the cent, private ZIP export. Use this skill when Werbungskosten receipts should be prepared in a structured way -- with a clear boundary: not tax advice, no deductibility check, no creation or submission of a tax return (that happens via ELSTER or approved software)."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: de
status: active
visibility: public
---

<img src="banner.png" width="100%" alt="steuer-assistent banner">

# steuer-assistent -- Verweis-Skill

Dieser Skill ist ein **schlanker Verweis (Wrapper)** auf das eigenstaendige,
oeffentliche Modul-Repository
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(MIT-Lizenz, public). Der eigentliche Skill lebt dort -- dieses Repository
verlinkt und dokumentiert nur die Installation.

## Was das Modul tut

`steuer-assistent` ist ein kleines, offline-first Python-Modul fuer
selbst-kategorisierte Werbungskosten-Belege (Arbeitnehmer-Werbungskosten):

- Belege erfassen (Kategorie, Betrag, Datum, optionale Notiz).
- Erfasste Werbungskosten centgenau nach Jahr summieren.
- Eine private, nicht-amtliche ZIP-Arbeitsunterlage exportieren (CSV +
  Zusammenfassung + Nicht-Amtlichkeits-Hinweis, ohne Belegdateien).
- Lokaler Store (Standard `%USERPROFILE%\.steuer-assistent\steuer.db`), kein
  Netzwerkzugriff, kein Cloud-Upload, kein Zugriff auf fremde Datenbanken.

## Grenzen (wichtig)

- **Keine Steuerberatung.** Das Modul prueft weder die steuerliche
  Abziehbarkeit einzelner Positionen noch erstellt oder uebermittelt es eine
  Steuererklaerung.
- Die offizielle elektronische Uebermittlung erfolgt ausschliesslich ueber
  ELSTER bzw. dafuer zugelassene Software -- nicht ueber dieses Modul.
- Scope: private Arbeitsunterlage fuer Arbeitnehmer-Werbungskosten; keine
  Gewerbe- oder Betriebsausgaben-Erfassung.

## Installation (generisch, ohne lokale Konkretpfade)

1. Modul klonen:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <klon-pfad>
   ```
2. Modul installieren und pruefen:
   ```bash
   cd <klon-pfad>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. `<klon-pfad>/SKILL.md` in die eigene Skill-Umgebung uebernehmen (z. B.
   `~/.claude/skills/steuer-assistent/`). KEINE realen lokalen Pfade oder
   Hostnamen in eine versionierte Skill-Umgebung committen.
4. Store-Pfad bei Bedarf ueber `STEUER_ASSISTENT_DB=<pfad>` bzw.
   `--store <pfad>` anpassen; Standard ist das Benutzerverzeichnis.
5. Details zu CLI-Befehlen, Datenschutz und Grenzen: siehe README des
   Modul-Repos.

## Herkunft dieses Verweis-Skills

Dieser Wrapper wurde am 2026-07-23 als Showcase-Eintrag fuer das
`ellmos-ai/skills`-Repository vorbereitet. Es findet **keine
Code-Duplikation** statt -- Pflege und Versionierung bleiben allein im
Modul-Repo `ellmos-ai/steuer-assistent`.

## Changelog

### 0.1.0 (2026-07-23)
- Initialer Verweis-Skill auf `ellmos-ai/steuer-assistent`.
