---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "How game development works as a process — roles, subtasks, workflows and role descriptions, especially (but not only) for Roblox. Use this skill when it's about the ORGANIZATION of game dev rather than concrete code: Which roles exist (Creative Director, Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? Who does which subtask? What does a development chain (concept → backend → frontend → polish → test) look like? How do you write a Game Design Document / KONZEPT.md? How do several (AI) agents divide up a game? Also trigger on \"plan a new game\", \"create Game Design Document\", \"which roles do I need for my game\", \"development workflow for a game\", \"who tests the game\", \"structure a game idea\", \"Roblox genre/monetization\"."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---
<img src="banner.png" width="100%" alt="game-design banner">

# Game Design — Rollen, Teilaufgaben & Workflows

## Zweck

Spieleentwicklung ist Teamarbeit aus klar getrennten Disziplinen — auch wenn eine Einzelperson
oder ein KI-Agent mehrere davon übernimmt. Dieser Skill liefert das **Organisationsmodell**:
welche Rollen es gibt, welche Teilaufgaben dazugehören, in welcher Reihenfolge sie zusammenwirken
und wie man ein Spiel als Konzept (GDD) festhält. Für das *technische* Wie siehe `/rojo` (Sync),
`/rbx-studio` (Editor/Assets) und den Metaskill `/rbx-dev` (Architektur).

Nutze diesen Skill beim Planen eines neuen Spiels, beim Aufteilen der Arbeit (auch zwischen
mehreren KI-Agenten) und beim Schreiben/Prüfen eines Game Design Documents.

## Die Rollen (5 Entwicklung + 2 Test)

Eine bewährte, kompakte Rollenaufteilung. Vollständige Beschreibungen mit allen Teilaufgaben:
[`references/roles-and-workflows.md`](references/roles-and-workflows.md).

| Rolle | Fokus | Kern-Teilaufgaben |
| --- | --- | --- |
| **Creative Director** | WAS & WARUM & für WEN | GDD/KONZEPT, Mechaniken entwerfen & balancen, Priorisierung/Sprints, Story, UX-Flow |
| **Engineer** | WIE (technisch) | Server/Client/Shared-Code, Game-Loop, Netzwerk/Remotes, DevOps (Rojo, Build), Bugfixing |
| **Artist** | wie die Welt aussieht | Welt-/Level-Aufbau, Beleuchtung & Atmosphäre, Partikel, Asset-Beschaffung (inkl. Malware-Check) |
| **Polish / Audio** | wie es sich anfühlt & klingt | SFX/Musik/Ambient, Animationen, UI/UX-Feinschliff, "Juice" (Screen-Shake, Hit-Stop), Feedback |
| **Business** | nach außen | Store-Seite, Icon/Thumbnail, Monetarisierung (Gamepass/Products/Pass), Analytics, Community |
| **QA-Tester** | technisch korrekt? | Bug-Scans im Code, Playtests + Console prüfen, reproduzierbare Reports, Regression, Performance |
| **Spielkritiker** | macht es Spaß? | First-/Long-Impression aus Spielersicht, ehrliche Bewertung (Fun, Klarheit, Fairness), Vorschläge |

**Grundregel:** Entwicklung und Test sind **getrennte** Rollen — idealerweise getrennte Personen
oder Agenten. Wer Code schreibt, testet ihn nicht objektiv. Der Spielkritiker darf hart sein.

## Workflows (Entwicklungs-Chains)

Arbeit fließt als Kette von Rolle zu Rolle. Die wichtigsten Muster:

**Standard-Feature-Chain:**
```
Creative Director (plant Feature) → Engineer (Backend) → Artist (Frontend/Assets)
→ Polish/Audio (Sound + Feinschliff) → QA-Tester (technischer Test)
→ Spielkritiker (Spielerperspektive) → Creative Director (Feedback → nächste Iteration)
```

**Quick-Fix-Chain:** QA-Tester (Bug) → Engineer (Fix) → QA-Tester (verifiziert).

**Asset-Chain:** Artist (Store-Suche) → Artist (Malware-Scan) → Artist (einbinden) → QA (visuell).

**Polish-Chain:** Spielkritiker (Schwäche) → Polish/Audio → Artist → Spielkritiker (Re-Check).

**Mensch-im-Loop:** [Agenten-Chain] → menschlicher Tester → Creative Director (Feedback) → [Chain].

Jede Iteration sollte ein kurzes Changelog hinterlassen. Abbruchbedingung: Zeitbudget erreicht
**oder** Qualitätsziel erfüllt.

### Persona-basiertes Testen

Ein Spiel überlebt nur, wenn ganz unterschiedliche Spieler damit klarkommen. Teste daher (auch
simuliert durch Agenten) aus mehreren **Personas** statt nur aus deiner eigenen Sicht — variiert
nach Alter, Erfahrung, Plattform (PC/Mobile/Tablet/Konsole), Aufmerksamkeitsspanne, Sprache und
Zugänglichkeit. Beispiele: ein 9-jähriges Casual-Kind am Tablet, das nur Knöpfe drücken will; ein
12-jähriger Core-Spieler am PC, der die Meta sucht; ein Anfänger 60+, der große Buttons braucht.
Persona-Tests sollten **blind** laufen (Tester kennt die Design-Absicht nicht).

## Game Design Document (KONZEPT.md)

Halte jedes Spiel in einem knappen GDD fest — Vorlage:
[`assets/KONZEPT_template.md`](assets/KONZEPT_template.md). Mindest-Struktur:

- **Vision** — 1–2 Sätze: Was ist das Spiel?
- **Genre / Vorbild** — Einordnung + Referenztitel.
- **Kern-Mechaniken** — **max. 3–4** (Fokus erzwingt Qualität).
- **Gameplay-Loop** — die Minute-für-Minute-Schleife des Spielers.
- **Spielmodi / Zeitformate** — falls relevant.
- **Monetarisierung** — Gamepasses, Developer Products, Battle Pass, Shop.
- **Technik** — Stack (Rojo/Frameworks), grobe Architektur.
- **Nächste Schritte** — Implementierungs-Checkliste.
- **Bekannte Bugs / offene Punkte**.

## Multi-Agent-Arbeitsteilung

Mehrere KI-Agenten (oder Mensch+KI) können sich ein Spiel aufteilen — zwei Modi:

- **Schwarm** — gleiche Aufgabe, verschiedene Bereiche (z. B. drei Agenten balancen je ein System).
- **Team** — verschiedene Rollen, aufeinander abgestimmt (Engineer + Artist + Polish parallel an
  einem Feature, koordiniert vom Creative Director).

Praxisbewährt: Entwicklung und Test **nie** demselben Agenten geben; Rollen-Prompts pro Rolle
fixieren (System-Prompt = Rollenbeschreibung); jede Chain-Iteration endet mit Changelog +
Testbericht; der Mensch bleibt Qualitäts-Gate.

## Roblox-spezifischer Markt-Kontext (Orientierung)

Plattform-Wissen, das die Konzeptarbeit für Roblox erdet (keine Garantie, nur Faustregeln):

- **Profitable Genres:** Simulator, RPG, Tycoon, Horror, Obby — sehr unterschiedliche Skalierung
  und Aufwand.
- **Unterversorgte Nischen (höheres Risiko, weniger Konkurrenz):** echtes Strategie/RTS-Lite,
  qualitativ hochwertige Sportspiele, Cozy/Life-Sim, Coop-Puzzle/Escape, Auto-Battler.
- **Goldene Monetarisierungs-Regeln:** (1) LiveOps ist Pflicht (Updates alle 2–4 Wochen),
  (2) Monetarisierung soll Gameplay *unterstützen*, nicht blockieren, (3) Social-Design (Trading,
  Coop) ist Infrastruktur, (4) Mobile-First (50 %+ spielen am Handy), (5) Content-Creator-
  Tauglichkeit (YouTube/TikTok) ist Marketing.

> Für aktuelle, belastbare Marktzahlen recherchieren statt schätzen — die obigen Punkte sind
> stabile Heuristiken, keine Live-Daten.

## Weiterführend

- Schwesterskills: `/rojo`, `/rbx-studio`; Metaskill `/rbx-dev` (Architektur-Pattern,
  Projektstruktur, Luau-Lessons).
- Referenz-Pipeline (falls vorhanden): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`,
  `IDEAS.md`, Marktanalysen).

## Changelog

### 1.0.0 (2026-06-17)
- Initiale Version. Generisches Rollen-/Workflow-Framework, destilliert aus `.ROBLOX/AGENT_ROLES.md`
  & `GUIDE.md`, nutzerneutral (ohne projektspezifisches Portfolio).

## Verwandte Skills

- `roblox-team-lock` — Datei-, Studio- und MCP-Claims, sobald mehrere Agenten am selben Projekt arbeiten. Erst lesen, dann claimen, dann arbeiten, dann freigeben.
