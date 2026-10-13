---
name: regelrecht-scenario-traces
description: Maakt regelrecht-scenario's vindbaar en hun norm-ketens leesbaar/geassert. Aan de invoerkant — vertaal een platte lijst leaf-parameters naar benoemde casus-assen + een herbruikbare persona-bibliotheek, met een reverse-lookup casus-matrix. Aan de uitvoerkant — maak de norm-keten zichtbaar via keten-checkpoints (assert elke knoop op het kritieke pad, niet alleen de endpoint) en golden-trace-snapshots + branch-coverage. Gebruik dit bij het schrijven of opschonen van scenario-/feature-files, het terugvinden of ontwerpen van een specifieke casus in een grote variabelenlijst, het reviewen van engine-traces, of het regressie-bestendig maken van cross-law-ketens zodat een ketenfout niet stil achter een correcte endpoint verdwijnt. Dossier-agnostisch; de regelrecht-methode is de vaste taal. Haakt aan op regelrecht-stelselanalyse (engine-tests / meta-check) en regelrecht-audit-products (testcase-scenario's).
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, Agent
---

# Regelrecht scenario's & traces — casus vindbaar, keten leesbaar

Een dossier-agnostische techniek-skill die beide werk-skills delen:
`regelrecht-audit-products` schrijft scenario's (de casus-kant),
`regelrecht-stelselanalyse` reviewt traces (de keten-kant). Deze skill levert de
*methode* om scenario's zó te modelleren dat (A) de casuïstiek terugvindbaar is en
(B) de juridische logica-keten zichtbaar én geassert is.

Geen casus-inhoud in de skill; concrete persona's, assen en norm-namen komen uit het
corpus tijdens toepassing.

## Het probleem dat deze skill oplost

Een scenario dat alleen een handvol leaf-parameters flipt en de **endpoint** assert,
verbergt twee dingen tegelijk:

- **A — casus onvindbaar.** De casus ("welke persoon is dit?") bestaat alleen in je
  hoofd, in de scenario-titel en in comments. Met tientallen platte booleans moet je de
  mapping *persona → leafs* elke keer handmatig reverse-engineeren. Twee scenario's met
  identieke invoer maar een ander bedóeld onderscheid zien er identiek uit.
- **B — keten onzichtbaar.** De engine berekent een keten van tussen-normen tussen de
  leafs en de endpoint. Alleen de endpoint asserten betekent: een *foute keten* die op
  jouw gesamplede casus toevallig dezelfde endpoint geeft, slipt er geluidloos door. En
  lezend is de juridische structuur niet uit het scenario te halen.

## Kernprincipe: de ontbrekende middenlaag

Tussen *menselijke casus* en *engine-output* zit een middenlaag die first-class,
vindbaar én geassert moet zijn:

```
   menselijke casus            ENGINE                 uitkomst
   "wie is deze persoon?"  ─►  leaf-feiten ─► keten ─► endpoint
        │                          │           │          │
   [A] benoemde persona ───────────┘           │          │
       op casus-assen                           │          │
                                   [B] benoemde norm-keten ┘
                                       (keten-checkpoints + golden trace)
```

- **Invoerkant (A):** geef de casus een naam en plaats hem op een paar **casus-assen**;
  bundel de leaf-deltas in een herbruikbare **persona**. → `references/casus-assen.md`,
  `references/persona-bibliotheek.md`.
- **Uitvoerkant (B):** bepaal het **kritieke pad** door de YAML-DAG en assert *elke knoop*
  erop; leg de volledige trace vast als **golden snapshot** met branch-coverage. →
  `references/keten-checkpoints.md`, `references/golden-traces.md`.

## De vier mechanismen

| # | Mechanisme | Lost op | Reference / template |
|---|---|---|---|
| 1 | **Assen-groepering** — platte leaf-lijst → casus-assen (dimensie-reductie) | A | `references/casus-assen.md` |
| 2 | **Persona-bibliotheek** — benoemde, herbruikbare leaf-bundel op de assen; twin-persona's (één-as-verschil) | A | `references/persona-bibliotheek.md` · `templates/persona-bibliotheek.md` · `templates/casus-matrix.md` |
| 3 | **Keten-checkpoints** — assert elke knoop op het kritieke pad, niet alleen de endpoint | B | `references/keten-checkpoints.md` · `templates/keten-kaart.md` |
| 4 | **Golden traces** — volledige trace snapshotten + diffen + branch-coverage | B | `references/golden-traces.md` · `templates/golden-trace-review.md` |

Schaal naar de vraag: een snelle opschoning gebruikt 1+3; een regressie-bestendige
cross-law-keten gebruikt alle vier.

## Werkstroom

1. **Vind de assen.** Reduceer de platte leaf-lijst tot een handvol onafhankelijke
   casus-assen (zie `references/casus-assen.md`). Groepeer de baseline-parameters per as
   — alleen al volgorde + kopjes maken de lijst scanbaar.

2. **Bouw de persona-bibliotheek + casus-matrix.** Druk elke casus uit als benoemde
   bundel leaf-deltas op de assen (`templates/persona-bibliotheek.md`). Leg de
   reverse-lookup vast: persona ↔ scenario ↔ keten-pad ↔ uitkomst
   (`templates/casus-matrix.md`). Voeg twin-persona's toe waar een onderscheid anders
   onzichtbaar blijft.

3. **Bepaal het kritieke pad & leg keten-checkpoints vast.** Leid uit de YAML de DAG van
   tussen-normen naar de endpoint af (`templates/keten-kaart.md`). Laat elk scenario
   *elke knoop op zijn pad* asserten, niet alleen de endpoint
   (`references/keten-checkpoints.md`).

4. **Snapshot golden traces + branch-coverage.** Leg de volledige engine-trace per
   scenario vast en diff bij wijziging; rapporteer welke takken nog ongetest zijn
   (`references/golden-traces.md`, `templates/golden-trace-review.md`).

5. **Voer de meta-check uit.** Maken de scenario's en de YAML dezelfde fout? Dan
   valideert de suite de YAML, niet de wet. Keten-checkpoints + golden-traces zijn het
   concrete wapen hiertegen — zie de hook naar `regelrecht-stelselanalyse`.

6. **Schrijf naar het corpus/dossier, niet in de skill.** Persona's, matrices en
   trace-snapshots horen bij het corpus: feature-files in de `scenarios/`-map
   naast de wet die ze testen, verder `docs/`.
   Wijzig nooit de skill-bestanden met casus-inhoud. Commit/push alleen op verzoek.

## Bestanden in deze skill

**references/**
- `casus-assen.md` — van een platte leaf-lijst naar onafhankelijke casus-assen
  (dimensie-reductie); hoe je assen herkent en de baseline groepeert.
- `persona-bibliotheek.md` — persona = benoemde leaf-bundel op de assen; expressievormen
  (Scenario Outline / custom `Given persona`-step / fixtures); twin-persona's.
- `keten-checkpoints.md` — kritiek pad uit de YAML-DAG; de conventie "assert elke knoop";
  sensitiviteits-/twin-scenario's; band met de features-vs-YAML meta-check.
- `golden-traces.md` — volledige trace vastleggen, diffen, branch-coverage; wanneer wel/niet.

**templates/**
- `persona-bibliotheek.md` — persona | assen-coördinaat | leaf-deltas | keten-checkpoints | endpoint.
- `casus-matrix.md` — reverse-lookup index: persona ↔ scenario ↔ keten-pad ↔ uitkomst.
- `keten-kaart.md` — per endpoint de knoop-DAG met coverage-markering per schakel.
- `golden-trace-review.md` — trace-snapshot-review + branch-coverage-rapport.

## Routing & handoff

Dit is een techniek-laag die beide werk-skills bedienen. Twijfel je waar te beginnen →
`regelrecht-dossier`. Bij het ontwerpen van expert-testcases gebruikt
`regelrecht-audit-products/templates/testcase-scenarios` deze persona-methode; bij
regressie/validatie voert `regelrecht-stelselanalyse` (engine-tests + de
features-vs-YAML meta-check) de keten-checkpoints + golden-traces uit.

## Belangrijke regels

- **Dossier-agnostisch blijven.** Geen vaste wet-namen, norm-namen, bedragen of
  casus-voorbeelden in de skill-bestanden. In *output* (corpus/features) mag casus-inhoud
  uiteraard wel.
- **Assert de keten, niet alleen de endpoint.** Een groene endpoint met een ongeteste
  keten bewijst niets over de tussenstappen.
- **Persona is de bron, scenario is de afgeleide.** Eén persona-definitie, hergebruikt
  over scenario's — niet dezelfde leaf-bundel telkens opnieuw met de hand.
- **Twin-scenario's voor elk onderscheid dat het model niet vanzelf ziet.** Eén-as-verschil
  maakt de keten falsifieerbaar.
- **Stille truncatie loggen.** Cap je coverage (top-N personas, niet alle takken) → meld
  expliciet wat je overslaat.
