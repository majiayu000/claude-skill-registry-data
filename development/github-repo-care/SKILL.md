---
name: github-repo-care
version: 1.3.1
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-09-27
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: "Protocol for safely creating, publishing, releasing, auditing, and maintaining GitHub repositories: check local rules and locks, create .gitignore before the first add, run privacy checks, prepare README/i18n/banner/metadata, verify release tags and GitHub releases, and update organization profiles, llms.txt files, and registry links."

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: de
status: active
visibility: public
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="github-repo-care banner">

# GitHub Repo Care — Repository sauber veröffentlichen und pflegen

## Wann dieser Skill greift

Nutze diesen Skill, wenn ein GitHub-Repository neu erstellt, veröffentlicht, gereleaset, auditiert oder nachträglich gepflegt werden soll. Er ist besonders wichtig vor dem ersten öffentlichen Push, bei Release-Tags, bei Änderungen an Repository-Metadaten, bei Organisationsprofilen und bei Privacy-Checks.

Greift nicht für reine Code-Implementierung ohne GitHub-Veröffentlichung. In diesem Fall erst den passenden Entwicklungs- oder Debugging-Skill verwenden und diesen Skill erst beim Publikationsschritt aktivieren.

## Kernregel

Bereite das Repository vor dem ersten öffentlichen Push vor. Eine korrekte `.gitignore`, ein sauberer Privacy-Gate, Lizenz, README, Metadaten und Release-Story sind vor öffentlicher Historie deutlich einfacher als danach.

## Ablauf

1. **Lokale Regeln lesen.** Prüfe `AGENTS.md`, `CLAUDE.md`, `START.md`, Release-Policy, Naming-Policy und Lock-Policy, sofern vorhanden.
2. **Sperren prüfen.** Wenn `LOCK.txt` oder eine passende `LOCK.*.txt` aktiv ist, diesen Scope nicht ändern.
3. **Repository-Namen festlegen.** Namen, Organisation, Sichtbarkeit, Lizenz und Zweck in einem Satz festhalten.
4. **`.gitignore` vor `git add` anlegen.** Secrets, lokale Daten, Datenbanken, Build-Ausgaben, virtuelle Umgebungen, Caches, IDE-Dateien und private Notizen ausschließen.
5. **Public-Basics ergänzen.** Typisch: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` und CI.
6. **README für Entdeckung schreiben.** Erste Bildschirmhöhe: Zweck, Installation, Nutzung, Privacy-Modell, Projektstruktur, Lizenz und kanonischer Repo-Name.
7. **Visuelle Signale setzen.** Banner, Logo oder Screenshot ergänzen, wenn sie den Nutzen erkennbarer machen. Keine generische Dekoration, wenn ein echtes Produktbild oder klares Konzeptbild möglich ist.
8. **Mehrsprachigkeit bewusst planen.** Minimum: Englisch plus Projektsprache. Für nutzernahe Module bevorzugt: Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch und Russisch.
9. **Tests und Smokes ausführen.** Lokal verifizieren, bevor Erfolg behauptet oder ein Release erstellt wird.
10. **Privacy-Gate ausführen.** Staged/tracked Set prüfen: Secrets, lokale Pfade, PII, `.env`, Datenbanken, private Dokumente, generierte Artefakte und Mojibake.
11. **Committen und pushen.** Nur nach bestandenem Gate committen. Danach GitHub-Repo anlegen oder verbinden, pushen und Remote-Status prüfen.
12. **Metadaten setzen.** Beschreibung, Topics, Homepage, Sichtbarkeit und Branch-Default prüfen.
13. **Release erstellen.** Tag und GitHub-Release anlegen; CI für Branch und Tag prüfen.
14. **Discovery-Flächen aktualisieren.** Organisationsprofil, `llms.txt`, zentrale Registries, lokale Modulindizes und Ökosystem-READMEs verlinken. **Publish ⇒ Profilseite (T-20260926-796851315):** Hat das Repo ein Banner, prüfe mechanisch, ob es auf der Org-Profilseite (`<org>/.github/profile/README.md`) bereits auftaucht — `python org_profile_gate.py --org <org>` (`.AI/.SKILLS/testing/`). Fehlt der Eintrag, liefert das Skript ein fertiges Markdown-Snippet zum Einfügen.
    **Eigenen Stern setzen (T-20260926-299328659):** Aftercare prüft für jedes eigene öffentliche Repo, ob der Account selbst schon einen Stern gesetzt hat, und setzt ihn sonst nach — über das eigene GitHub-Pflege-Tool, falls vorhanden (Pfad und Aufruf per lokaler Config, z. B. ein `--self-star`-Flag: ohne Repo-Angabe ein Nachhol-Lauf über alle konfigurierten Organisationen, mit Repo-Angabe ein Einzellauf direkt nach diesem Publish). Nie automatisch entsternen.
    **Stargazer-Pflege:** neuen Stargazern folgen und bei echter Qualität ihr bestes Projekt zurücksternen — falls das eigene GitHub-Pflege-Tool bereits ein Reziprozitäts-Modul mitbringt, dieses nutzen (bewertet thematische Relevanz und schlägt zurücksternen/einladen/prüfen/überspringen vor; führt das Folgen mit Rate-Caps, Cooldown und Dry-run/Apply/Confirm-Sicherheitsnetz aus). Nicht neu bauen, wenn es das schon gibt; Entscheidungen protokolliert das Modul selbst. Nie automatisch entfolgen oder entsternen.
15. **Abschluss prüfen.** Remote README, Release-Seite, Topics, CI und Links kontrollieren.

## Privacy-Gate

Suche im gestagten oder getrackten Set, nicht nur im sichtbaren Arbeitsbaum.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

Bei öffentlichen Modulen zusätzlich ein `RELEASE_GATE.md` oder äquivalentes Gate dokumentieren: Datum, geprüfte Befehle, Ergebnis, Restwarnungen und bewusste Ausnahmen. Wenn ein Secret jemals committed wurde, reicht Löschen aus `HEAD` nicht; das Secret muss rotiert werden.

**Verlinkte Repos auf Sichtbarkeit prüfen.** Ein Pfad-/Token-Scan findet keine
Links auf private GitHub-Repos in öffentlichen READMEs (Lehrfall
T-20260926-820252321: `ellmos-ai/ellmos-core` stand unbemerkt in einer
README-Tabelle, obwohl das Repo privat ist). Falls im Repo vorhanden, den
wiederverwendbaren Check laufen lassen:

```bash
python testing/repo_link_visibility_gate.py --repo .
```

Der Check ist fail-open nur bei echter Unsicherheit (Netzwerkausfall, Rate-Limit
403/429 -- nur ein Hinweis, kein Abbruch); ein 404 blockiert wie ein bestätigtes
`private: true`, da beides bedeutet, dass der Link für Fremde nicht auflösbar
ist (privat oder gar nicht vorhanden). Ohne dieses Script (Repo hat keinen eigenen Klon des Checks):
mit `gh api repos/ORG/REPO --jq .private` jeden im README verlinkten Fremd-
oder Geschwister-Repo-Link stichprobenartig prüfen.

## GitHub-Metadaten

Nach dem Push Metadaten und Release explizit setzen.

```bash
gh repo edit ORG/REPO --description "Kurze konkrete Beschreibung" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

Danach verifizieren:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

Wenn CI nach einem Release rot ist, gilt das Repository noch nicht als sauber veröffentlicht. Bei einem gerade erstellten Initialrelease ist es akzeptabel, den frischen Tag sofort und bewusst auf den korrigierten Commit zu verschieben.

## Häufige Fehler

| Fehler | Korrektur |
|---|---|
| `.gitignore` wird erst nach `git add` erstellt | Erst unstage, Ignore-Regeln korrigieren, dann erneut adden |
| README ist einsprachig, obwohl UI oder Skill mehrsprachig ist | Sprachlinks oder lokalisierte READMEs ergänzen |
| Kein Banner, keine Topics, keine Beschreibung | Discovery-Assets vor Ankündigung ergänzen |
| Release-Tag existiert, aber CI ist rot | CI fixen und neuen Run prüfen |
| Organisations-README aktualisiert, aber `llms.txt` vergessen | Beide menschlichen und maschinenlesbaren Flächen aktualisieren |
| Lokaler Pfad steht in öffentlicher Doku | Durch relative Pfade oder generische Beispiele ersetzen |
| Public Repo enthält Testdatenbank oder Notebook-Inbox | Datei aus Tracking entfernen, Ignore-Regel ergänzen, Gate erneut laufen lassen |

## Abschluss-Checkliste

- [ ] Lokale Regeln und Sperren geprüft.
- [ ] `.gitignore` existierte vor dem ersten Add.
- [ ] Public-Dokumente, Lizenz, Security, Contributing, Changelog und `llms.txt` vorhanden.
- [ ] README enthält Repo-Name, Zweck, Installation, Nutzung, Privacy und Lizenz.
- [ ] i18n-Erwartung erfüllt.
- [ ] Banner, Logo oder Screenshot vorhanden, sofern sinnvoll.
- [ ] Tests und Smokes bestanden.
- [ ] Privacy-, Pfad-, Secret-, Datenbank- und Mojibake-Scans sauber.
- [ ] GitHub-Beschreibung, Topics, Tag, Release und CI verifiziert.
- [ ] Organisationsprofil, Registry und Ökosystem-Links aktualisiert.
- [ ] Banner vorhanden? `org_profile_gate.py --org <org>` lief ohne Fund für dieses Repo.

## Changelog

### 1.3.1 (2026-09-27)
- Doku-Fix: Die 404-Semantik der Privacy-Gate-Beschreibung war falsch. Laut
  `testing/repo_link_visibility_gate.py` blockiert 404 (privat oder nicht
  vorhanden) wie ein bestätigtes `private: true`; fail-open gilt nur bei
  Netzwerkausfall und Rate-Limit (403/429). Korrigiert im Privacy-Gate-
  Abschnitt und im 1.2.0-Changelog-Eintrag.

### 1.3.0 (2026-09-27)
- Step 14 erweitert (T-20260926-299328659, Nutzerauftrag): eigenen Stern auf eigenen
  öffentlichen Repos prüfen/setzen sowie Stargazer-Pflege (folgen + Qualitäts-
  Rücksternen), über das eigene GitHub-Pflege-Tool, falls vorhanden — kein bestimmtes
  Werkzeug vorgeschrieben. Nie automatisch entfolgen/entsternen.

### 1.2.0 (2026-09-26)
- Neuer Privacy-Gate-Schritt (T-20260926-820252321): verlinkte GitHub-Repos auf
  Sichtbarkeit prüfen (`testing/repo_link_visibility_gate.py --repo .`, fail-open bei
  Netzwerk/Rate-Limit, blockiert bei 404 und bestätigtem `private: true`). Anlass:
  `ellmos-ai/ellmos-core` (privates Repo) stand unbemerkt in einer README-Tabelle.

### 1.1.0 (2026-09-26)
- Added the "Publish ⇒ Profilseite" step (T-20260926-796851315): a repo with a banner must be
  checked against its org's profile README (`<org>/.github/profile/README.md`), mechanically via
  `.AI/.SKILLS/testing/org_profile_gate.py`, not left to memory. Anlass: zombie-killer-tray's
  banner never made it onto the dev-bricks org page after publication.

### 1.0.0 (2026-06-18)
- Initiale Version als Repository-Pflege- und Veröffentlichungsprotokoll erstellt.
