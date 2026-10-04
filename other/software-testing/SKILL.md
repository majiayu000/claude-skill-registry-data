---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: Teststrategie-Berater für Softwareprojekte — wählt die richtigen Teststufen (Unit/Integration/System/Abnahme), Testarten (funktional, nicht-funktional, änderungsbezogen) und Testentwurfsverfahren (Äquivalenzklassen, Grenzwerte, Entscheidungstabellen, explorativ) für die jeweilige Situation und SDLC-/CI-Phase, inkl. Testpyramide, CI/CD-Gates, Shift-Left und Best Practices. Nutze diesen Skill IMMER, wenn Tests geschrieben, geplant, priorisiert oder bewertet werden sollen — bei "schreibe Tests", "Teststrategie", "Testplan", "Testkonzept", "was/wie soll ich testen", "welche Tests fehlen", "Testabdeckung verbessern", "QA aufsetzen", Fragen zu Regression/Smoke/Sanity/Last/Stress/Security-Tests oder beim Einrichten einer Test-Pipeline — auch wenn "Test" nur beiläufig fällt. Abgrenzung — für die TDD-Schleife selbst superpowers:test-driven-development, für Bug-Diagnose bugfix-protocol, für systematische Bug-Suche bugsweep nutzen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide, Agile Testing Quadrants, moderne Verfahren); Quellen siehe testarten-katalog.md'}
---

<img src="banner.png" width="100%" alt="software-testing banner">

# Software-Testing: Teststrategie & Testauswahl

Dieser Skill beantwortet die Frage **„Welche Tests brauche ich hier, jetzt, wofür?"** —
systematisch statt aus dem Bauch. Er liefert die Entscheidungslogik; der vollständige
Katalog aller Testarten, Verfahren und Definitionen liegt in
`testarten-katalog.md` im selben Ordner (bei Detailfragen dort nachschlagen).

---

## 1. Ordnungsrahmen: In drei Dimensionen denken

Bevor du Tests planst oder schreibst, verorte die Aufgabe auf drei Achsen (ISTQB).
Wer nur „eine Liste von Tests" führt, vermischt die Achsen und plant lückenhaft:

| Achse | Frage | Ausprägungen |
|---|---|---|
| **Teststufe** | Auf welcher Ebene? | Unit → Integration → System → Abnahme |
| **Testart** | Welche Eigenschaft? | funktional / nicht-funktional / strukturbezogen / änderungsbezogen |
| **Testverfahren** | Wie entstehen die Testfälle? | Black-Box / White-Box / erfahrungsbasiert |

Quer dazu: **statisch** (Reviews, statische Analyse — ohne Ausführung, früheste und
billigste Fehlerfindung) vs. **dynamisch** (Code wird ausgeführt).

---

## 2. Situations-Router: Was liegt vor?

Wähle den Einstieg nach der konkreten Situation:

| Situation | Vorgehen |
|---|---|
| **Neues Feature bauen** | Abnahmekriterien VOR dem Code klären (ATDD/BDD-Denkweise). Unit-Tests parallel zur Implementierung (Äquivalenzklassen + Grenzwerte). Integrationstest für neue Schnittstellen. Einen E2E-Happy-Path, nicht mehr. |
| **Bug fixen** | Erst Bug reproduzierender Test (rot), dann Fix (grün) = **Re-Test**. Danach **Regression** der Umgebung. Diagnose selbst → `bugfix-protocol`. |
| **Refactoring** | KEINE neuen Feature-Tests — bestehende Suite ist das Sicherheitsnetz. Vorher prüfen, ob die Suite das Verhalten wirklich abdeckt (ggf. Charakterisierungstests nachziehen). Coverage/Mutation als Lückenindikator. |
| **Legacy-Code ohne Tests** | Nicht mit Unit-Tests jeder Funktion beginnen. Erst Charakterisierungstests auf System-/API-Ebene um das Ist-Verhalten legen, dann beim Anfassen einzelner Teile Unit-Tests nachziehen. |
| **API / Microservices** | API-Tests auf Service-Ebene als Schwerpunkt (mittlere Pyramidenebene). Bei getrennten Teams/Deployments: **Contract Testing** (z. B. Pact) statt gemeinsamer Staging-Integrationstests. |
| **Release vorbereiten** | Reihenfolge: Smoke (Build stabil?) → volle Regression → nicht-funktionale Tests (Last, Security) → UAT/Abnahme → Smoke auf dem Release-Kandidaten. |
| **Performance-Sorge** | Erst messbares Ziel definieren (z. B. „P95 < 300 ms bei 1.000 Nutzern"), sonst ist kein Test auswertbar. Lasttest = Normallast, Stresstest = Bruchpunkt + Erholung. Produktionsnahe Umgebung Pflicht. |
| **Test-Pipeline aufsetzen** | CI/CD-Gates aus Abschnitt 4 implementieren; mit Unit + Lint bei jedem Commit beginnen, dann stufenweise ausbauen. |
| **Teststrategie/Testkonzept schreiben** | Struktur entlang der 3 Dimensionen + Phasen-Mapping (Abschnitt 4) + risikobasierte Priorisierung (Abschnitt 6, Punkt 10). |

---

## 3. Teststufen: Prüfobjekt, Ziel, Zeitpunkt

| Stufe | Prüft | Wann | Faustregel |
|---|---|---|---|
| **Unit/Komponente** | Einzelne Funktion/Klasse isoliert (Mocks/Stubs) | Während der Implementierung, jeder Commit | Breite Basis der Pyramide; schnell (< Sekunden), deterministisch |
| **Integration** | Zusammenspiel, Schnittstellen, DB-Anbindung | Nach Unit-Tests, bei jedem Merge | Inkrementell integrieren (Top-Down/Bottom-Up), nie Big Bang bei großen Systemen |
| **System** | Gesamtsystem gegen technische Anforderungen | Sobald integrierter Build existiert | Funktional UND nicht-funktional; unabhängige Tester wertvoll |
| **Abnahme** | Geschäftserwartung, realer Einsatz | Letzte Stufe vor Go-Live | UAT durch Fachbereich; betrieblich (Backup/Deploy/Monitoring) nicht vergessen; ggf. Alpha/Beta |

**Testpyramide** als Mengenverhältnis: viele Unit-, gezielte Integrations-/API-, wenige
E2E-Tests (Daumenregel ~70/20/10 als Startpunkt — nach tatsächlicher Fehlerherkunft
justieren). Umgedrehte Pyramide (viele UI-Tests) = langsam + flaky → vermeiden.

---

## 4. Phasen-Mapping: Wann prüft man was?

### CI/CD-Gates (modernes Standard-Mapping)

| Pipeline-Stufe | Gate |
|---|---|
| Jeder Commit | Unit-Tests, Linter, statische Analyse (Sekunden–Minuten) |
| Pull Request | Code-Review, SAST/SCA, gezielte Komponententests |
| Merge | Integrations-/API-/Contract-Tests, Smoke auf Testumgebung |
| Nightly / Pre-Release | Volle Regression, E2E, Performance-/Lasttests, DAST |
| Release-Kandidat | Smoke auf Staging, UAT, Abnahme |
| Produktion (Shift-Right) | Monitoring/Observability, Canary/Blue-Green, Feature Flags, ggf. Chaos-Experimente |

**Zeitbudgets & Blockier-Regeln (Faustwerte aus der Praxis):**

- **Commit-zu-Feedback < 10 Minuten** für den schnellen Pfad (Lint + Unit + kritische
  Integrationstests); Gesamtpipeline bis Staging **< 30–45 Minuten**; volle Regression
  nightly oder vor Release. Ein Regelkreis, der langsamer taktet, wird umgangen.
- **Blockierend vs. meldend:** Unit-, Integrations- und Smoke-Gates blockieren IMMER
  (bei Rot kein Merge/Deploy). Nightly-Stufen (Regression, Last, DAST) melden per
  Ticket/Fix, blockieren aber nicht jeden Commit. Nach dem Prod-Deploy: Smoke +
  Monitoring — bei Rot Rollback + Incident.
- **Übergabepunkt:** Der Commit (git push) trennt Inner Loop (lokal: TDD, Unit,
  schnelle Iteration) vom Outer Loop (geteilte Pipeline mit Gates). Was sich in den
  Inner Loop verlagern lässt, wird dort am billigsten gefangen (Shift-Left).

### Klassisch (V-Modell): Tests beim Spezifizieren entwerfen

Anforderungen↔Abnahmetest · Systemdesign↔Systemtest · Architektur↔Integrationstest ·
Code↔Unit-Test. Kernidee: Die Tests einer Stufe werden **beim Erstellen der zugehörigen
Spezifikation** entworfen — nicht erst am Ende. Reviews der Anforderungen/Designs
(statisches Testen) sind die früheste Fehlerfindung überhaupt.

### Agile Testing Quadrants (Planungsraster für Sprints)

Q1 Unit/TDD + Q2 Story-Tests/BDD laufen kontinuierlich und **verhindern** Fehler;
Q3 explorativ/Usability/UAT + Q4 Performance/Security **bewerten** das Produkt, sobald
genug Produkt existiert. Details im Katalog.

---

## 5. Testentwurfsverfahren wählen

| Wenn die Testbasis … | … dann Verfahren |
|---|---|
| Eingabebereiche/Wertemengen hat | **Äquivalenzklassen** (ein Repräsentant je Klasse) + **Grenzwertanalyse** (an und direkt jenseits jeder Grenze: bei 5–50 teste 4, 5, 50, 51) — die Grundausstattung für fast jeden Unit-Test |
| komplexe Geschäftsregeln/Bedingungskombinationen hat | **Entscheidungstabellentest** |
| Zustände und Übergänge hat (Workflow, Session, Gerät) | **Zustandsübergangstest** (auch verbotene Übergänge testen) |
| Nutzerabläufe beschreibt | **Use-Case-/Szenariotest** inkl. Fehler- und Ausnahmepfaden |
| Code ist und Abdeckung gemessen werden soll | **Anweisungs-/Zweigüberdeckung** — als Lückenindikator, nicht als Ziel (100 % Coverage ≠ korrekt) |
| unklar/lückenhaft ist oder Zeit knapp | **Exploratives Testen** (zeitboxte Sessions mit Charter) + **Error Guessing** (Null, Leerstring, Sonderzeichen, Zeitzonen, Race Conditions) |

Systematische Verfahren zuerst, erfahrungsbasierte bewusst **ergänzend** — sie finden,
was Skripte übersehen.

---

## 6. Best Practices (Checkliste beim Planen/Reviewen von Tests)

1. **Shift-Left:** Reviews + statische Analyse ab der Anforderungsphase — je später ein
   Fehler gefunden wird, desto teurer (verbreitete Faustregel nach Boehm; Richtung
   unstrittig, exakte Faktoren umstritten).
2. **Testpyramide respektieren** — E2E-Tests sparsam, Unit-Basis breit.
3. **Automatisieren, was wiederholt wird** (Smoke, Regression, API, Unit) und in
   CI/CD-Gates verankern; manuelle Kapazität für explorativ + Usability reservieren.
4. **Testfälle systematisch entwerfen** (Abschnitt 5), nicht ad hoc.
5. **Nicht-funktionale Anforderungen messbar machen** — ohne Zahlenziel kein
   auswertbarer Performanz-/Lasttest.
6. **Re-Test ≠ Regression:** erst Fix bestätigen, dann Seiteneffekte. Reihenfolge
   Smoke → Sanity/Re-Test → Regression.
7. **Flaky Tests sofort behandeln** — quarantänisieren, Ursache fixen oder löschen;
   instabile Suiten zerstören das Vertrauen in die Pipeline.
8. **Testdaten/-umgebungen managen:** reproduzierbar (Container/IaC), produktionsnah,
   anonymisierte oder synthetische Daten.
9. **Testqualität selbst messen:** Coverage als Lückenindikator; **Mutation Testing**
   dort, wo Coverage-Zahlen täuschen könnten.
10. **Risikobasiert priorisieren:** Testtiefe nach Ausfallwirkung ×
    Fehlerwahrscheinlichkeit — nicht gleichverteilt.
11. **Qualität ist Teamaufgabe** (Whole-Team-Approach): Tester früh in Anforderungen
    einbinden; BDD/ATDD als gemeinsames Vehikel mit dem Fachbereich.
12. **Shift-Right nicht vergessen:** Monitoring, Canary, Feature Flags; Chaos
    Engineering erst bei reifer Observability.

---

## 7. Moderne Verfahren — wann zusätzlich einsetzen

| Verfahren | Einsetzen wenn … |
|---|---|
| **Contract Testing** (Pact) | Microservices mit getrennten Deployments/Teams |
| **Mutation Testing** (Stryker, PIT, mutmut) | Güte einer bestehenden Testsuite bewertet werden soll |
| **Property-Based Testing** (Hypothesis, fast-check) | Invarianten existieren („sortiert ist idempotent") und Randfälle gefürchtet sind |
| **Fuzzing** | Parser, Deserialisierung, sicherheitskritische Eingaben |
| **Chaos Engineering** | Verteilte Systeme + reife Observability + saubere Rollbacks |

---

## Nachbar-Skills (nicht duplizieren)

- **`superpowers:test-driven-development`** — die konkrete Red-Green-Refactor-Schleife
  beim Schreiben von Code.
- **`bugfix-protocol`** — 6-Phasen-Diagnose eines konkreten Bugs.
- **`bugsweep`** — systematischer Bug-Suchlauf über eine Codebasis.
- **`dev-cycle`** — 8-Phasen-Gesamtzyklus (ab dessen v1.2.0: Tests werden in den
  Phasen 1/3/5 entworfen, in Phase 6 geschrieben und in Phase 7 ausgeführt; dieser
  Skill füllt aus, WELCHE Tests wo laufen sollen).

## Referenz

Vollständiger Katalog (alle Teststufen, Testarten inkl. nicht-funktionaler Detailtabelle,
alle Entwurfsverfahren, Agile Quadrants, statisch/dynamisch, V-Modell, Quellen):
→ `testarten-katalog.md` (im selben Ordner)

Visuelle Gesamtkarte — Phasen, Regelkreise, Rollen und Test-Gates als „Schaltplan
der Softwareentwicklung" (Blatt BL-5 = Test-Einhängung, BL-2 = Regelkreis-Takte):
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (im Browser öffnen)

---

## Änderungsprotokoll

### 1.0.1 (2026-08-22)
- Zeitbudgets & Blockier-Regeln für CI/CD-Gates ergänzt (< 10 min Fast Path,
  < 30–45 min Pipeline; blockierend vs. meldend; Rollback nach Prod-Rot) sowie
  der Commit als Übergabepunkt Inner/Outer Loop
- Verweis auf die Schaltplan-Beilage im dev-cycle-Skill; dev-cycle-Abgrenzung an
  dessen v1.2.0 (Shift-Left: entwerfen 1/3/5, schreiben 6, ausführen 7) angepasst

### 1.0.0 (2026-08-22)
- Erstversion aus Online-Recherche (ISTQB-Systematik, Testpyramide, Agile Testing
  Quadrants, CI/CD-Gates, moderne Verfahren)
