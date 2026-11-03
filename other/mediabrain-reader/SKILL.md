---
name: mediabrain-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Analysiert bereitgestellte Medienlisten und Metadaten unabhängig von einer bestimmten Medien-App.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [media, catalog, metadata, export]
language: de
status: stable
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---

<img src="banner.png" width="100%" alt="mediabrain-reader banner">

# Medienkatalog-Leser

## Zweck

Medienbestände nach Typ, Status, Thema oder Dubletten auswerten.

**Ergebnis:** Katalogübersicht, Qualitätsprobleme und konkrete Such- oder Bereinigungsvorschläge.

## Arbeitsablauf

1. Ziel, Kontext und gewünschtes Ausgabeformat klären.
2. Nur die im aktuellen Auftrag bereitgestellten Informationen verwenden.
3. Das Ergebnis strukturiert und nachvollziehbar erstellen.
4. Annahmen kennzeichnen und vor externen Änderungen eine Bestätigung einholen.

## Beispiel

**Eingabe:** Fasse diesen JSON-Medienexport nach Typ und Status zusammen.

**Ergebnis:** Katalogübersicht, Qualitätsprobleme und konkrete Such- oder Bereinigungsvorschläge.

## Öffentlicher Kern und private Erweiterungen

Dieser öffentliche Skill enthält ausschließlich die übertragbare Methode. App-spezifische Adapter, Konten, lokale Pfade, Datenbanken und persönliche Voreinstellungen gehören in ein privates Zusatzprofil oder einen privaten Fork und dürfen nicht in dieses Repository übernommen werden.

Ohne privates Profil arbeitet der Skill nur mit Informationen, die im aktuellen Auftrag ausdrücklich bereitgestellt wurden.

## Grenzen und Datenschutz

- Daten werden nicht standardmäßig gespeichert.
- Keine Quelle, Datei oder Schnittstelle wird ohne ausdrückliche Freigabe geöffnet oder verändert.

## Änderungsprotokoll

### 2.0.0 (2026-07-30)

- Nutzerneutraler öffentlicher Kern; private Integrationen und persönliche Profile entfernt.
