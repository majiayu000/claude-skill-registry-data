---
name: project-doc-sync
description: Synchronisiert System-Dokumentation nach jedem relevanten Task. Nutze diesen Skill, wenn ein Build, Fix oder eine Konfigurationsänderung abgeschlossen ist und in ~/docs/system/ als Markdown festgehalten werden soll.
---

# project-doc-sync

## Wann nutzen
Nach jedem relevanten Task (Build, Fix, Config-Änderung, neues Tool) für Bastis Projekte.
Basti will für alle Builds/Fixes eine Markdown-Doku unter `~/docs/system/`.

## Schritte
1. **Ist-Zustand prüfen:** Existiert schon eine passende Doku-Datei unter `~/docs/system/`?
   - Suche mit `search_files` nach dem Projekt-/Task-Namen.
2. **Struktur wählen:**
   - Neue Doku: `~/docs/system/<projekt>-<thema>-<YYYY-MM-DD>.md`
   - Bestehende: gezielt ergänzen (patch), nicht überschreiben.
3. **Inhalt** (immer auf Deutsch):
   ```markdown
   # <Titel>
   **Datum:** YYYY-MM-DD · **Projekt:** <name>

   ## Was gemacht wurde
   - ...
   ## Wie (Befehle/Code)
   ```bash
   ...
   ```
   ## Ergebnis / Verifikation
   - ...
   ## Offene Punkte / nächste Schritte
   - ...
   ```
4. **Verifizieren:** Datei zurücklesen, prüfen ob Befehle/Ergebnis stimmen.
5. **Basti kurz informieren:** Pfad zur Doku nennen.

## Pitfalls
- ❌ Doku ohne konkrete Befehle/Ergebnis → wertlos. Immer lauffähige Befehle + Verifikation.
- ❌ Bestehende Doku blind überschreiben → gezielt patchen.
- ✅ Deutsch, konkret, mit Datum im Dateinamen.

## Verifikation
Nach dem Schreiben: `read_file` auf die Datei, prüfen dass alle Abschnitte gefüllt sind.
