---
name: pipeline-optimizer
version: 1.2.0
type: protocol
author: Lukas Geiger (method) + Claude (write-up)
created: 2026-05-16
updated: 2026-06-13
aliases: [project-folder-optimizer, pipeline-renovator, project-renovator]
description: Structured 6-step procedure for improving, renovating, or rebuilding existing pipelines, individual project folders, documentation structures, or software stacks. Addressable as "pipeline optimizer" (for whole topic pipelines, e.g. a software, research, or game-dev pipeline) or "project-folder optimizer" (for individual project folders within a pipeline, e.g. a single software tool or paper project). Triggers on tasks like "improve pipeline X", "optimize the stack", "rebuild Y", "renovation", "pipeline refactoring", "clean up project folder", "improve folder structure", "unify conventions", "documentation consolidation", "integrate into existing system", or any substantial intervention in established structures. Delivers building-stock analysis, purpose clarification, ideal sketch, gap plan, empirical pain-point identification, and retests with fresh subagents. Prevents parallel standards, duplication, and pipeline breaks.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [pipeline, renovation, refactoring, stack, workflow, lessons-learned]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/pipeline-optimizer/', 'origin_version': '1.1.1', 'last_sync_from_origin': '2026-05-16', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="pipeline-optimizer banner">

# Pipeline-Optimizer / Projekt-Ordner-Optimizer

**6-Schritte-Renovierung ohne Inkompatibilitäten** — anwendbar auf zwei Größenordnungen:

| Trigger-Name | Anwendungsbereich | Beispiel |
|---|---|---|
| **Pipeline-Optimizer** | Ganze Pipelines, Stacks, Doku-Strukturen | Deine Themen-Pipelines, z.B. `software/`, `research/`, `games/`, ein Agenten-System |
| **Projekt-Ordner-Optimizer** | Einzelne Projektordner innerhalb einer Pipeline | Ein Software-Tool, ein Paper-Projekt, ein Game-Projekt |

Eine **Pipeline** meint hier eine themenbezogene Top-Level-Struktur, in der mehrere Projekte nach gemeinsamen Konventionen leben (z.B. eine Software-Pipeline mit Release-Regeln, eine Forschungs-Pipeline mit Publikationsverfahren).

Beide nutzen denselben 6-Schritte-Workflow — der Unterschied liegt nur im **Scope** (Pipeline-weit vs. Einzelprojekt) und entsprechend in der Tiefe der Bausubstanz-Erfassung in Schritt A.

## Wann dieser Skill greift

Der Skill greift, sobald du eine **bestehende** Struktur verbessern, umbauen oder erweitern sollst — nicht beim Greenfield-Bau. Konkrete Trigger:

**Pipeline-Ebene** (Scope: ganze Pipeline):
- „Pipeline X besser machen"
- „Stack optimieren"
- „Renovierung der Software-Pipeline"
- „Doku-Konsolidierung in der Forschungs-Pipeline"
- Substantieller Eingriff in eine Themen-Pipeline, zentrale `_tools/` oder System-Komponenten

**Projektordner-Ebene** (Scope: einzelner Projektordner):
- „Projektordner X aufräumen/optimieren"
- „Ordnerstruktur in Y verbessern"
- „Einzelnes Tool refactorieren"
- „Paper-Projekt-Setup vereinheitlichen"
- „Game-Projektordner an Pipeline-Standard anpassen"

**Übergreifend:**
- „X umbauen/integrieren in bestehendes Y"
- „Refactoring", „Konsolidierung"
- „Konventionen vereinheitlichen"
- „in bestehendes System integrieren"

## Die Bausubstanz-Metapher

Ein Haus zu renovieren erfordert zuerst zu wissen, **aus was es besteht** (Steine, Holz, Plastik), **wofür es da ist** (Berghütte, Softwareschmiede), und **wo es jetzt schon Funktionen erfüllt**. Dieselbe Disziplin gilt für Pipelines.

---

## Verfahren — 6 Schritte (NICHT überspringen, NICHT umsortieren)

### Schritt A — Bausubstanz erfassen

**Frage:** Aus was besteht das Haus?

**Pipeline-Scope** (alle Root-Dokus + Tools + Templates):
- [ ] **Alle Root-Dokumente vollständig lesen** (nicht nur Snippets/Insertion-Points)
- [ ] Template-Ordner (`_templates/`, `_TEMPLATES/`) und Tool-Ordner (`_tools/`) durchgehen
- [ ] Policy-Dateien: z.B. GITHUB-POLICY.md, RELEASE-MANAGEMENT.md, QUALITY_RULES.md, NAMING-SYSTEM.md, Publikationsverfahren, …
- [ ] Status-Snapshots: z.B. PROJECT_STATUS.md, Status-Übersichten, releases.json, Registry-Dateien
- [ ] Checklisten: z.B. Release-Checklisten, Build-/PDF-Checklisten
- [ ] Workflows: AGENTS.md, GUIDE.md, SKILL.md
- [ ] Lessons-Learned-Dateien: LESSONS_LEARNED.md, MEMORY.md, Loop-State-Dateien

**Projektordner-Scope** (Einzelprojekt-Substanz + relevante Pipeline-Konventionen):
- [ ] **Alle Markdown- und Steuer-Dateien im Projektordner lesen** (README, CHANGELOG, AUFGABEN/TODO, DONE, KONZEPT, AKTIONSPLAN, Beweisnotizen, …)
- [ ] **Code-Struktur erfassen:** src/, tests/, Build-Konfiguration (pyproject.toml, requirements.txt, Projekt-Manifeste, Toolchain-Dateien, …)
- [ ] **Pipeline-Konventionen aus übergeordneter Pipeline berücksichtigen** (z.B. für ein Software-Projekt: GitHub-Policy, Naming-System, Release-Management, Templates)
- [ ] **Bestehende Tools/Scripts im Projekt** scannen (`_tools/`, `_scripts/`, build_*.bat, START-Skripte)
- [ ] **Konfigurationsdateien:** `.gitignore`, LICENSE, NOTICE, SECURITY.md, CODE_OF_CONDUCT.md

**Anti-Pattern:** Mit `grep -l "<keyword>"` Insertion-Points finden und dort einfügen, ohne den Kontext der Datei zu kennen.

**Output:** Inventar-Notiz mit allen relevanten Konventionen, Tools, Templates auf gewähltem Scope.

### Schritt B — Zweck identifizieren

**Frage:** Wofür existiert das Haus?

Zweck explizit formulieren in 1-2 Sätzen.

**Pipeline-Beispiele:**

| Pipeline | Zweck |
|---|---|
| Software-Pipeline | Desktop-Anwendungen + Browser-Tools entwickeln, testen, in Stores/auf GitHub releasen |
| Forschungs-Pipeline | Wissenschaftliche Papers schreiben, peer-reviewen, auf Repositorien/Preprint-Servern publizieren |
| Game-Pipeline | Games entwickeln und auf der Zielplattform publishen |
| Agenten-System | LLM-System zur Multi-Agent-Orchestrierung |

**Projektordner-Beispiele:**

| Projektordner | Zweck |
|---|---|
| `software/PlannerApp` | Planungs-Desktop-App, kommerziell, privates Repo |
| `research/CosmologyModel` | Modell-Paper-Serie + numerische Berechnungen |
| `games/SortingChaos` | Sortier-Game, Alpha-Stadium, Level-Progression |

Der Zweck **lenkt jeden Eingriff** — Maßnahmen, die nicht dem Zweck dienen, fallen raus.

### Schritt C — Ideales Bild entwerfen

**Frage:** Wie sähe ein perfektes Haus für diesen Zweck aus?

- Aus eigener Sicht skizzieren (kurz, max. 10 Punkte)
- Best-Practice-Vergleich heranziehen (z.B. Vercel-Stack für SaaS, scientific-python-stack für Forschung)
- Nicht in Detail-Optimierung gehen — Top-Level-Skizze reicht

**Output:** 5-10 Punkte „Idealzustand pro Pipeline"

### Schritt D — Lücken-Analyse + Plan

**Vier Fragen pro Pipeline:**

1. **Was hat das Haus schon?** — Auch wenn anders gelöst als im Ideal, aber **funktional gleichwertig**.
   *Beispiel:* Ideal sagt „pip-licenses für Dritt-Lizenzen". Real: ein eigenes Generator-Script ist Wrapper drumherum → funktional gleichwertig, kein Eingriff nötig.

2. **Was behindert die Funktion?** — Bestehende Strukturen, die heute Brüche oder Mehraufwand verursachen.

3. **Was ist nicht funktional?** — Toter Code, veraltete Konventionen, ungenutzte Tools.

4. **Was würde Funktionen messbar verbessern?** — Konkrete Eingriffe mit erwartetem Nutzen.

→ Daraus **konkreter Plan**:
- Was wird **neu gebaut**?
- Was wird **erweitert**?
- Was wird **abgerissen**?
- Was bleibt **unverändert** (wichtig zu benennen!)

**Output:** Plan-Tabelle mit Spalten *Eingriff* / *Bestehendes* / *Maßnahme* / *Begründung*

### Schritt E — Empirisch arbeiten

Nicht nur top-down planen — Schmerzpunkte sammeln:

- [ ] **Bekannte Bugs**: Issue-Tracker, AUFGABEN/TODO/DONE-Dateien
- [ ] **Fehler-Historie**: Lessons-Learned-Dateien, Bugfix-Logs, Prüf-Registries
- [ ] **Automatisierungs-Brüche**: „Was muss ich immer manuell machen?"
- [ ] **User-Interview**: Gezielt fragen — Schmerzpunkte, Wünsche, Workarounds
- [ ] **Selbsttest**: Pipeline durchspielen (neues Projekt anlegen, Build durchlaufen, Release simulieren) — wo bricht es?

Die empirisch gefundenen Schmerzpunkte **priorisieren den Plan** aus Schritt D.

### Schritt F — Retests nach Umsetzung

- [ ] **Frische Subagenten** beauftragen (unbelastet vom Renovierungs-Kontext), den geänderten Workflow durchzuspielen
- [ ] **Messbare Vergleichswerte** vorher/nachher: Setup-Zeit, Fehlerquote, Anzahl manueller Schritte, Build-Zeit
- [ ] **Anti-Regression-Check**: Funktionierten bestehende Workflows nach der Änderung weiterhin?
- [ ] Falls **keine messbare Verbesserung** oder Regression: Renovierung **zurückrollen** oder nachjustieren

## Anti-Patterns (verboten)

| Anti-Pattern | Schaden | Gegenmittel |
|---|---|---|
| Insertion-Points suchen statt Doku lesen | Parallele Standards | Schritt A vollständig |
| „Best Practice von X" 1:1 übertragen | Inkompatibilität | Schritt D vergleicht funktional |
| Neue Datei anlegen ohne Konvention zu prüfen | Duplikation (z.B. NOTICE.md ↔ THIRD_PARTY_LICENSES.txt) | Schritt A + Schritt D |
| Top-down planen ohne Empirie | Lösung passt nicht zum Schmerzpunkt | Schritt E vor Plan-Abschluss |
| Eigene Änderung nicht testen | Regression unentdeckt | Schritt F mit frischem Agenten |
| „Klärung später" mit unklarem Status | User entdeckt Konflikt nachträglich | Bei Unsicherheit lieber Schritt D nochmal mit User durchgehen |

## Lehrbeispiel — NOTICE.md-Vorfall

**Auftrag:** Pipeline-Verbesserungen in mehreren Themen-Pipelines (Software, Forschung, Games) umsetzen.

**Fehler:** Schritt A übersprungen — nur Insertion-Points gesucht statt vollständige Policy-Dateien gelesen.

**Folge:** `NOTICE.md` als „neue Lizenz-Datei" in 7 Dateien eingeführt, obwohl `THIRD_PARTY_LICENSES.txt` + ein eigener Lizenz-Generator (Wrapper um `pip-licenses`) bereits etabliert waren — dokumentiert in der GitHub-Policy der Pipeline (Pflichtdateien + Lizenz-Checkliste). Alle Software-Projekte hatten bereits THIRD_PARTY-Dateien.

**Erkennung:** Erst nach Nachfrage des Users („ich bin recht sicher, dass wir schon ein Rechtemanagement hatten").

**Korrektur:** NOTICE.md aus dem Projekt-Template gelöscht, 6 weitere Dateien angepasst, der bestehende Lizenz-Generator statt `pip-licenses` referenziert.

**Lehre:** Wäre Schritt A vollständig ausgeführt worden, wäre der Konflikt vor dem Schreiben erkannt worden.

## Faustregeln

1. **Bei „Pipeline verbessern" zuerst genauso lange lesen wie schreiben.**
2. **Kein neuer Standard ohne Beweis, dass kein bestehender existiert.**
3. **Bestehende Tools/Wrapper nutzen statt neue parallele.**
4. **„Mehr von demselben" ist meist schlechter als „Bestehendes erweitern".**
5. **Bei Konflikt zurückrollen** ist immer besser als zwei parallele Standards laufen lassen.

## Checkliste zum Abschluss

Bevor du eine Pipeline-Renovierung als „erledigt" meldest:

- [ ] Schritt A: Alle relevanten Root-Dokus gelesen?
- [ ] Schritt B: Zweck der Pipeline in 1-2 Sätzen formuliert?
- [ ] Schritt C: Idealbild skizziert (5-10 Punkte)?
- [ ] Schritt D: Lücken-Analyse mit Tabelle (was bleibt / was erweitert / was neu / was weg)?
- [ ] Schritt E: Empirie geprüft (Bugs, Lessons, Selbsttest, User-Interview)?
- [ ] Plan mit User abgestimmt?
- [ ] Schritt F: Mit frischem Subagenten getestet — Verbesserung messbar?
- [ ] Keine parallelen Standards eingeführt?
- [ ] Bei Konflikten zurückgerollt oder ehrlich Rechenschaft abgelegt?

## Optimale Projektordner-Struktur (für Projekt-Ordner-Optimizer)

Wenn der Skill auf **einen einzelnen Projektordner** angewendet wird, hilft als Ideal-Referenz (Schritt C) folgende kombinierte Empfehlung:

### Anthropic-Standard (Claude Code)

| Datei/Ordner | Funktion |
|---|---|
| `CLAUDE.md` (Root) | Auto-loaded von Claude Code, projektspezifische Anweisungen |
| `.claude/settings.json` | Permissions, Env-Vars, Model-Auswahl (committed) |
| `.claude/settings.local.json` | Lokale Overrides (NICHT committen, in `.gitignore`) |
| `.claude/commands/*.md` | Custom Slash-Commands |
| `.claude/agents/*.md` | Custom Subagents |
| `.claude/skills/<name>/SKILL.md` | Projekt-Skills |

### Eigenes Projekt-Doku-Template (empfohlen)

Falls du ein eigenes Projekt-Doku-Template pflegst (z.B. unter `<dein-workspace>/_templates/project-docs/`), lohnen sich **drei Ausbauprofile**. Beispiel-Aufteilung: **MINIMAL** liefert das Session-Kernset mit 7 Root-Files (`AGENTS.md`, `CLAUDE.md`, `README.md`, `START.md`, `STATE.md`, `TODO.md`, `DONE.md`) plus `_tools/`. **STANDARD** ergänzt `CHANGELOG.md`, `DECISIONS.md` und `PATTERNS.md`. **FULL** baut auf 14 Root-Files aus und ergänzt zusätzlich `ARCHITECTURE.md`, `WORKFLOWS.md`, `TOOLS.md`, `GLOSSARY.md` sowie `workflows/` und `.github/`.

→ **Bei neuen Projekten ein solches Template als Basis nutzen** (kopieren statt manuell anlegen).

### Pipeline-spezifische Ergänzungen (Beispiele)

Je nach Pipeline kommen weitere Pflichtdateien hinzu — typische Muster:

- **Software-Projekt:** LICENSE, CODE_OF_CONDUCT.md, SECURITY.md, CONTRIBUTING.md, THIRD_PARTY_LICENSES.txt (generiert), pyproject.toml/requirements.txt, Eintrag in der zentralen Release-Registry der Pipeline. → Falls vorhanden: Cookiecutter-Template der Pipeline nutzen.
- **Forschungs-Projekt:** Konzept-Dokument, Aktionsplan, Publikationsplan, Archiv-/Quellen-/Ergebnis-/Daten-Ordner (`_archive/`, `_sources/`, `_results/`, `_data/`), `paper/` für LaTeX. Bei Beweisprojekten: eine Beweisnotiz-Datei mit Beweiskette und Status.
- **Game-Projekt:** Projekt-Manifest und Toolchain-Dateien der Engine (z.B. bei Roblox/Rojo: default.project.json, rokit.toml, wally.toml, selene.toml), Game-Design-Dokument, `src/{server,client,shared}/` nach Engine-Konvention.

### Vollständige Detail-Referenz

→ Siehe **`references/optimal-project-structure.md`** in diesem Skill-Ordner. Enthält:
- Beispiel-`settings.json` (Anthropic-Schema)
- `.gitignore`-Pflichteinträge
- Anti-Patterns (was NICHT in Projektordner)
- Empfohlene Workflows pro Pipeline-Typ (Software/Forschung/Game)
- YAML-Header-Konvention für Doku-Dateien
- Auto-Check-Skizze

## Verwandte Skills (Wann statt diesem Skill?)

| Skill | Wann nutzen |
|---|---|
| **`project-onboarding`** | EXTERNES bestehendes Repo ins eigene System aufnehmen |
| Projekt-Bootstrapper (falls vorhanden) | NEUES Projekt in bestehender Pipeline anlegen (Greenfield, kein Umbau) |
| Pipeline-Bootstrapper (falls vorhanden) | KOMPLETT NEUE Pipeline anlegen (seltener Fall) |
| System-Onboarding (falls vorhanden) | Neuen Rechner einrichten |

Der **Pipeline-Optimizer** ist für **Renovierung** zuständig, nicht Neubau oder Übernahme. Falls deine Skill-Sammlung einen Skill-Index hat, dort nach passenden Bootstrapping-Skills suchen.

## Querverweise

- Detail-Referenz: `references/optimal-project-structure.md` (in diesem Skill-Ordner)
- Anthropic Claude Code Docs: `https://docs.claude.com/en/docs/claude-code`
- Falls vorhanden: globale User-Regeln (z.B. ein Abschnitt „Umbauten/Renovierungen" in deiner `~/CLAUDE.md`) und pipeline-spezifische Stack-Beschreibungen

## Scope-Wahl: Pipeline vs. Projektordner

Wenn nicht klar ist, welcher Scope gemeint ist, **vor Schritt A klären**:

| Indiz | Scope |
|---|---|
| „Die ganze Software-Pipeline verbessern" | Pipeline |
| „Den Ordner von Tool X aufräumen" | Projektordner |
| „Die zentrale Release-Registry synchronisieren" | Pipeline (zentrales Asset) |
| „Den AssetBuilder im Game Y refactorieren" | Projektordner |
| „Eine Prüf-Konvention pipeline-weit einführen" | Pipeline |
| „Im Projekt Z eine Prüf-Datei anlegen" | Projektordner |

Bei **Projektordner-Scope** zusätzlich immer kurz die übergeordneten Pipeline-Konventionen prüfen (Schritt A erweitert), damit der Eingriff zur Pipeline kompatibel bleibt.

---

## Changelog

### 1.2.0 (2026-06-13)
- Erstveröffentlichung in der Skill-Bibliothek: persönliche Pfade, konkrete Pipeline-/Projektnamen und Verweise auf private Skills durch generische Beispiele ersetzt; Verfahren (6 Schritte, Anti-Patterns, Lehrbeispiel, Checklisten) unverändert

### 1.1.1 (2026-06-01) und früher
- Interne Fassungen (privates Skill-Verzeichnis, vor Veröffentlichung)
