---
name: tech-detect
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Erfasst lokale Hardware, Software- und Python-Versionen mit Quellenbelegen als privaten, versionierten Techshot und vergleicht Hoststände ohne fehlende Beobachtungen als Deinstallation auszugeben."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [inventory, hardware, software, python, versions, host-comparison]
language: de
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="tech-detect banner">

# Tech Detect

## Einsatz

Nutze diesen Skill für eine belegte Istaufnahme eines **eigenen, autorisierten Hosts** oder einen Vergleich bereits vorhandener Hostaufnahmen. Eine Inventarliste ist Ausgangspunkt, kein Beweis für eine gerade installierte Version. Lies zuerst die vorhandene Inventarführung und ihre Host-Slot-Regeln. Bei `<inventory>` sind die JSON-Seeds die Eingabe; Datenbank und Tabellenexport sind Projektionen. Aktualisiere den Seed nur über dessen vorhandenen Host-Workflow, niemals beiläufig durch diesen Skill. Fremde Slots bleiben lesend.

Führe die folgenden Befehle im Skillverzeichnis oder mit aufgelöstem Skriptpfad über einen **expliziten Python-Interpreter** aus; eine `.py`-Datei nicht direkt starten.

## Ablauf

1. **Scope festlegen.** Host, eigener Slot, Inventar-Seed, private Ausgabe, Erhebungszeit in UTC, Dateisperren und Rechte prüfen. Keine Geheimnisse, vollständigen PATH-String oder Konfigurationsinhalte in Berichte kopieren.
2. **Lokale Evidenz messen.** `python -X utf8 scripts/techshot.py capture --seed <inventar>/systems/<eigener-slot>.json --slot <eigener-slot> --output <privat>/techshot-<UTC>.json` liest den Seed, lokale Plattform und installierte Pakete. Windows: Uninstall-Registry (Benutzer/Maschine, 32/64 Bit); Linux: vorhandenes `dpkg-query` oder `rpm`; macOS: vorhandenes Homebrew. Diese Quellen sind niemals eine garantierte Gesamtliste. `Win32_Product` **nicht** abfragen: Microsoft dokumentiert dabei Konsistenzprüfung und mögliche MSI-Reparatur. Andere Paketmanager und manuell kopierte Apps bleiben als Erfassungslücke sichtbar.
3. **Python getrennt belegen.** Laufender Interpreter erhält die genaue Laufzeitversion. Alle im PATH beobachteten Python-Dateien und ausdrücklich über `--python-path` benannten Installationen/Venvs erscheinen als getrennte Installationen. Ihre Version bleibt `unknown`, solange sie nicht ausdrücklich als vertrauenswürdiger Pfad mit `--probe-python <pfad>` und `-I -S --version` geprüft wurde. Effektives `sys.executable`, Venv-Kontext und PATH-Kandidaten nie zu einer einzigen Python-Version zusammenziehen.
4. **Qualität erhalten.** Jeder Komponentenbefund enthält stabile Produktidentität, Installationskennung, Version, Quelle und Qualitätsstatus `observed`, `reported`, `uncertain` oder `unknown`. Ein Seedwert wie `3.x` ist keine exakte Version. Hardware aus dem Seed bleibt mit Seedstand als gemeldet getrennt. `hardware_observations` misst OS, Architektur, CPU-Modell und logische Kerne, RAM und Kapazität des System-Dateisystems lesend; die GPU bleibt mangels portablem Sammler ausdrücklich `unknown`. Keine Seriennummern, MAC-Adressen oder vollständigen PATH-Werte erfassen. Fehlt eine Quelle, das Feld als `unknown` ausweisen.
5. **Hosts oder Zeitstände vergleichen.** `python -X utf8 scripts/techshot.py compare --left <privat>/alt-oder-host-a.json --right <privat>/neu-oder-host-b.json --output <privat>/vergleich.json` nutzt den inventargebundenen Slot als Assetkennung. Verschiedene Slots ergeben `axis=cross-host`, auch bei gleichem Hostnamen; `identity_note` nennt diese Mehrdeutigkeit. Derselbe Slot mit demselben Hostnamen und verschiedenen `captured_at_utc` ergibt `axis=same-host-time`. Eine Hostnamenänderung bei gleichem Slot erfordert einen externen Kontinuitätsbeleg und wird hier gestoppt. Die Reihenfolge steht in `chronology`. Einseitig nicht beobachtete Pakete beweisen weder Deinstallation noch fehlende Installation. Gleiche bekannte Versionen mit weiteren unbekannten Installationen erscheinen als `version-uncertain` samt Installationskennungen, statt zu verschwinden. Abweichende oder unbekannte Hardwarefelder separat lesen. Unterschiedliche Paketökosysteme oder Produktaliasse nur mit zusätzlicher Herstellerkennung zusammenführen.
6. **Rhythmus einrichten.** Nur nach Hostfreigabe den vorhandenen Scheduler/Sync-Workflow mit eigenem Slot und neuem Zeitstempel-Ausgabepfad verbinden. Ein Testlauf und der spätere Scheduler-Receipt sind getrennte Belege; aus einem Skill-Commit folgt kein aktiver Zeitplan. Techshots privat und begrenzt aufbewahren.

## Ausgabe und Übergabe

JSON-Vertrag: `ellmos.techshot.v1` mit `captured_at_utc`, `host`, Seed-SHA256, `hardware_observations`, `python_context`, `coverage` und `components[].installations[]`; Vergleich: `ellmos.techshot-comparison.v1` mit `axis`, `chronology`, `inputs.left/right`, `changes` und `hardware_changes`. Der CLI-Vergleich bindet beide Eingabedateien per SHA256 über ihre tatsächlichen Bytes und bewahrt Erfassungszeiten, Hostidentität, Seedbindung und Abdeckung. Die direkte Python-API kennzeichnet stattdessen `hash_basis=canonical-json`. Fehlende oder typdefekte Pflichtprovenienz stoppt den Vergleich; **alte vollständige Aufnahmen bleiben ausdrücklich zulässig**. `compared_at_utc` ist nur der Vergleichszeitpunkt und belegt keine frische Erhebung. Die Aufnahmen sind Beobachtungen neben der bestehenden Inventarquelle, keine konkurrierende Inventardatenbank. An `security-tech-stack-check` nur die nötigen Komponenten, exakten Versionen, Abdeckung und Hashes geben. `unknown` oder `uncertain` niemals als „verwundbar“ oder „sicher“ ausgeben.

Primärquelle zur Windows-Erfassungsgrenze: [Microsoft Learn, Working with software installations](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations?view=powershell-7.6), am 2026-10-25 geprüft.

## Changelog

### 1.0.0 (2026-10-25)

- Lokaler Techshot-/Vergleichsvertrag und quellgebundene Versionsqualität.
