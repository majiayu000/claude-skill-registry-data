---
name: textproduction
version: 2.0.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-09-27
description: >
  KI-gestuetzte Textproduktion in drei Teilskills: Allgemeine Texte (Blogpost,
  Social, Newsletter, Copy, E-Mail, Bericht), narrative Storys (Skript, Kurzgeschichte,
  RPG, Weltenbau) und PR-Kommunikation (Pressemitteilung, Positionspapier) mit
  lokalem LaTeX-PDF-Compiler. Kein externer Dienst zwingend erforderlich.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: production
tags: [text, blogpost, social-media, newsletter, marketing, email, bericht, copy,
       story, drehbuch, rpg, weltenbau, pressemitteilung, positionspapier, pr, latex]
language: de
status: active
visibility: public

dependencies:
  tools: [pr/press_compiler.py]
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/textproduction/ + system/agents/_experts/press/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  origin_license: "MIT"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="textproduction banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `textproduction`.


# Textproduction — Router (Deutsch)

Dieser Skill deckt alle textlichen Produktionsformen ab. Er leitet an den
passenden Teilskill weiter — lies die Detail-Anleitung im Unterordner.

## Routing-Tabelle

| Teilskill | Trigger-Beispiele | Detail-Anleitung |
|---|---|---|
| **text** | „Schreib einen Blogpost", „5 LinkedIn-Posts", „Newsletter", „Produktbeschreibung", „Formelle E-Mail", „Fasse X zusammen" | `text/WORKFLOW.md` |
| **storys** | „Schreib ein Drehbuch", „Kurzgeschichte", „RPG-Abenteuer erstellen", „Character Sheet", „Weltenbau" | `storys/WORKFLOW.md` |
| **pr** | „Pressemitteilung verfassen", „Positionspapier", „PR-Paket", „PDF generieren" | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## Workflow & Vorgehen

```
1. Nutzerwunsch → Routing-Tabelle oben → passenden Teilskill bestimmen.
2. Detail-Anleitung im Unterordner lesen (WORKFLOW.md).
3. Prompt-Muster auswaehlen, Platzhalter fuellen, Text generieren.
4. Qualitaetspruefung (je Teilskill angegeben).
```

## Hinweise

- **Userneutral:** Keine persoenlichen Daten, API-Keys oder Kontodaten im Skill.
  Konfiguration (Tonalitaet, Zeichenlimits, Kontaktdaten fuer PR) obliegt dem Nutzer.
- **PR-Tool:** `pr/press_compiler.py` kompiliert Pressemitteilungen und Positionspapiere
  zu PDF via LaTeX (pdflatex/xelatex). Setup einmalig: `pr/config.example.json`
  nach `pr/config.json` kopieren und Kontaktdaten eintragen.
- Optionale Stiloptimierung: DeepL Write (kostenlos bis 500.000 Zeichen/Monat).

## Änderungsprotokoll

### 2.0.0 (2026-06-22)
- Umstrukturierung auf Router-Muster: SKILL.md = Einstieg + Routing-Tabelle.
- Drei Teilskills: text/ (6 Texttypen), storys/ (4 narrative Formate),
  pr/ (Pressemitteilung + Positionspapier + LaTeX-PDF-Compiler).
- press_compiler.py + LaTeX-Templates + config.example.json aus
  ai-media-editor/production/pr/ hierher verschoben (SSOT).
- Verwandte-Skills-Verweise auf interne Teilskill-Pfade aktualisiert.

### 1.0.0 (2026-06-22)
- Initiale Version. Herausgeloest aus ai-media-editor/production/text/WORKFLOW.md.
- Provenance: BACH agents/_experts/textproduction/ (MIT).