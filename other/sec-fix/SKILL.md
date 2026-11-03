---
name: sec-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Erzeugt NUR auf ausdrücklichen Wunsch einen minimalen Sicherheitspatch für einen bestätigten Fund (Status validated oder triaged) - in einer Scratch-Kopie oder einem Worktree, nie im Original, als patches/<id>.diff ohne Anwenden, Commit oder Push. Auslöser: 'fix diesen Fund', 'Patch für SEC-...', 'Sicherheitslücke schließen'. Nicht für gewöhnliche Fehlerbehebung (dafür bugfix-protocol), nicht zum Prüfen eines Patches (sec-verify-fix), nicht zum Auffinden (sec-scan)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, fix, remediation]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-fix banner">

# sec-fix - minimaler Sicherheitspatch

Phase "fix" der ellmos-Security-Familie. Vertrag: `sec-scan/references/contract.md` (Verzeichnis §1, Lebenszyklus §2, Regeln §6). Hier nur die Anwendung.

## Wann (und wann nicht)

- **Nur auf ausdrücklichen Wunsch.** Ein Scan oder eine Validierung löst nie automatisch einen Fix aus.
- **Nur Funde mit Status `validated` oder `triaged`.** `candidate` zuerst durch `sec-validate`; `rejected` bleibt liegen.
- Normaler Bug ohne Sicherheitsbezug: `bugfix-protocol`. Ob ein vorhandener Patch taugt: `sec-verify-fix`. Strukturelle Ursache hinter mehreren Funden: `sec-hardening`.

## Ablauf

1. **Fund und Umfang lesen:** `findings.json` (Fund, `evidence`, `recommendation`), betroffene Datei und die Aufrufer der Stelle. Die Ursache beheben, nicht das Symptom an einer Aufrufstelle; gibt es mehrere Aufrufer derselben unsicheren Funktion, den gemeinsamen Punkt patchen.
2. **Lock prüfen (Vertrag §6 Regel 2):** `lock_scan.py --check-dir <repo> --json`; Exit 0 = frei, 1 = gesperrt, alles andere = unbekannt = stoppen; ohne `lock_scan.py` auf dem Host stattdessen `LOCK*.txt` im Repo und in den Elternordnern suchen (keine = frei, sonst stoppen). `LOCK.user.*` nie anfassen.
3. **Arbeitskopie:** Scratch-Kopie oder `git worktree` in einem Ordner außerhalb des Originals. Im Original wird nichts geschrieben.
4. **Basis messen:** Tests des Projekts einmal vor dem Patch laufen lassen und das Ergebnis festhalten (grün/rot, Anzahl). Gibt es keine Tests: sagen, nicht erfinden.
5. **Minimal patchen:** kleinste Änderung, die den Source-to-Sink-Pfad schließt (Validierung, Parametrisierung, Allowlist, Escaping an der richtigen Stelle). Kein Refactoring, keine Stilkorrekturen, keine neuen Abhängigkeiten ohne Not. Ein Regressionstest für den Fund gehört in den Patch, wenn das Projekt Tests hat.
6. **Nachmessen:** Tests erneut laufen lassen; Vorher/Nachher ehrlich berichten, auch rote Tests und Tests, die nicht liefen.
7. **Patch ablegen:** `git diff` der Arbeitskopie nach `patches/<id>.diff` im Scan-Verzeichnis; mit `git apply --check` gegen den Zielstand prüfen (verändert nichts).
8. **Finding aktualisieren:** `status: fixed`, `fix.patchFile: patches/<id>.diff`; dann `python scripts/secfind.py validate findings.json coverage.json` (Skript liegt in `sec-scan`).

## Grenzen

- **Kein Anwenden, kein Commit, kein Push (Regel 3).** Das braucht einen direkten Nutzerauftrag.
- **Geheimnis-Funde:** Der alte Wert steht zwangsläufig in den `-`-Zeilen des Diffs. Patch nur lokal im Scan-Verzeichnis, nie in Ticket, Chat oder Bericht; das Geheimnis zuerst beim Anbieter rotieren (Regel 4). Offen: ob ein maskierter Diff sinnvoll anwendbar wäre - nicht erfinden.
- Der Autor des Patches prüft ihn nicht selbst: `sec-verify-fix` mit anderem Prüfer (Regel 7).
- Kostenwarnung bei Fixes für viele Funde auf einmal (Regel 5); seriell abarbeiten.

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung.
