---
name: priorities
version: 0.1.0
type: skill
author: ellmos-ai
created: 2026-10-21
updated: 2026-10-21
description: "Verwenden, wenn Sitzungsprioritäten mit /prios gesetzt, aktuelle Ziele gewichtet oder der wichtigste Fokus über die Sitzung hinweg bewahrt werden sollen. Hält Prioritäten je Sitzung und Anbieter getrennt."
visibility: public potential
category: utilities
language: de
status: beta
tags: [planning, priorities, session]
dependencies: []
standalone: true
anthropic_compatible: true
bach_compatible: true
---

# Sitzungsprioritäten

<!-- FAMILY-ROUTER:planning-priorities START -->
> **Familie planning-priorities — Wegweiser:** Sitzungsgewichte → priorities; gemeinsame befristete Agenda und Planverweise → agenda-setting; Pläne über vorhandene Planungsskills bearbeiten.
<!-- FAMILY-ROUTER:planning-priorities END -->

`/prios TEXT` gewichtet die Arbeit innerhalb der Ziele dieser Sitzung. Ein Ziel behält seinen vollständigen Umfang und seine Abschlusskriterien. Prioritäten bestimmen die Reihenfolge; sie erteilen keine neuen Aufträge oder Rechte.

## Ablauf

1. Übernimm die ausdrücklich genannten Schwerpunkte. Trenne mehrere Punkte mit Semikolon oder Zeilenumbruch. Die Eingabereihenfolge bestimmt absteigende Gewichte; `100::TEXT; 70::TEXT` setzt Gewichte ausdrücklich (1–100).
2. Nutze ausschließlich die vom Laufzeitsystem gelieferte Sitzungs-ID und den Anbieter als Namensraum. Fehlt diese ID, halte Prioritäten nur im Gespräch fest und sage dies kurz. Erfinde keine ID aus Datum, Projekt, Prozess oder Modell.
3. Lies den aktuellen Stand und setze danach mit dessen Revision. Bei einem Konflikt erneut lesen und die Nutzeränderung mit dem neuen Stand abgleichen.
4. Bestätige die geordnete Liste. Wende sie bei der Auswahl der nächsten Schritte auf die bestehenden Ziele an. Ein neuer konkreter Nutzerauftrag bleibt maßgeblich.

```sh
python scripts/priorities.py show --provider PROVIDER --session-id TRUSTED_ID
python scripts/priorities.py set '100::Schwerpunkt eins; 70::Schwerpunkt zwei' --provider PROVIDER --session-id TRUSTED_ID --if-revision 0
python scripts/priorities.py clear --provider PROVIDER --session-id TRUSTED_ID --if-revision REVISION
```

Führe die Befehle mit dem absoluten Pfad dieses Skills aus. Übergib Texte als getrennte Prozessargumente; evaluiere sie nie als Shell-Code. `--root` oder `AGENT_PRIORITIES_ROOT` kann einen privaten Speicherort festlegen. Standard: `~/.local/state/agent-priorities/`. Der Schlüssel besteht aus Anbieter und SHA-256 der Sitzungs-ID. Unterschiedliche Sitzungen teilen keine Prioritäten.

## Abgrenzung und Verbindung

- `/prios` ohne Text zeigt die Sitzungsprioritäten; `/prios clear` entfernt deren Gewichtung.
- `$priorities` ist der native Codex-Skillaufruf. Andere Slash-Aliase hängen vom Anbieter ab; siehe installierte Befehlswrapper.
- `/agenda prios` gehört zu `agenda-setting` und verändert die gemeinsame Agenda. `/prios` verändert diese nicht.
- Agenda → Planübersicht → einzelne Pläne und deren Policy-Register → Projektanweisungen bilden den Planungskontext. Darin setzt die Sitzung ihre Ziele und gewichtet sie mit diesen Prioritäten. Diese Planungshierarchie verändert keine Instruktionsrangfolge und umgeht keine Policy.
- Nutze für die Erstellung oder Bearbeitung eines Plans den vorhandenen Planungsskill. Dupliziere keine Pläne in dieser Prioritätenliste.

Zustand ist private Nutzerdaten. Veröffentliche weder Sitzungsdateien noch private Profile. Details zur Anbieteranbindung: [Integration](references/integration.md).
