---
name: law-letter-fidelity-audit
description: >
  Audits whether a machine-readable regelrecht law model is faithful to the LETTER of
  the wettekst — and strictly separates the wettekst (leading) from the toelichting
  (Nota/Memorie van Toelichting; explanatory, not a norm). Runs in critical passes per
  article/lid and detects four deviation classes: toelichting-bleed (a modeled criterion
  that the letter only states as an open norm, or not at all), missing verbatim elements
  (a word/condition such as a "tenzij" or a qualifier dropped from the model), wrong
  legal_basis anchoring (an endpoint hung on a "kapstok"-article while the operative norm
  lives elsewhere), and verbatim-drift in text: (an ingetrokken/older redaction). Also
  detects positief-lid vs uitsluitings-lid conflicts and checks the chapeau for an explicit
  derogation rule ("zo nodig in afwijking van het eerste lid") before judging precedence.
  Classifies every finding as modelfout (fix), wettekst-gevolg (report, do not fix), or
  letter-vs-toelichting-question (jurist decides what is leading + revision signal). Use
  when the user wants to know if a model is "dicht bij de letter", mentions letter vs
  toelichting/bedoeling, fidelity, "natuurgetrouw", or before trusting feature outcomes.
allowed-tools: Read, Write, Bash, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
user-invocable: true
---

# Law Letter-Fidelity Audit

Audits whether a `machine_readable` model reflects the **letter of the wettekst**, not the
*toelichting* and not the desired outcome. The aim is to separate three very different things:
a genuine **modelfout** (the model deviates from the letter — fix it), a **wettekst-gevolg**
(the model faithfully follows a letter that itself produces an odd or unintended result —
report it, do not "fix" it in the model), and a **letter-vs-toelichting-question** (the letter
and the toelichting diverge — a jurist must decide which is leading).

## Core principle — wettekst leidend, toelichting is uitleg

> De **artikeltekst** (het `text:`-veld, de feitelijk geldende wet) is leidend. De **toelichting**
> (Nota / Memorie van Toelichting) legt de bedoeling uit maar is **geen norm**. Modelleer de open
> norm zoals de wet die stelt; gebruik de toelichting als duiding, nooit als een verkapt criterium.

Soll-normalisatie is verboden: het model spiegelt de wet inclusief haar onvolkomenheden. Modelleer
nooit een "zuiver" (zoals-bedoeld) stelsel als vervanging van het verbatim-model; het verschil tussen
letter en bedoeling is juist de te rapporteren bevinding.

## Werkwijze — kritische passes, fideliteit vóór outcome

Doe de fideliteit-audit **vóór** je het model tegen verwachte uitkomsten/scenario's afzet. Anders ga
je het model reverse-engineeren om een test te laten slagen (outcome-bias). Volgorde: (1) letter ↔
model per artikel/lid; (2) pas daarna toetsing tegen scenario's/uitvoeringsbeleid.

Loop per artikel: lees het verbatim `text:`-veld naast de `machine_readable` (parameters/input/actions/
operations) en zoek de vier afwijkingsklassen.

### Klasse 1 — toelichting-bleed
Een conditie of begrip in het model dat uit de **toelichting** komt terwijl de **letter** het slechts
als open norm stelt (of helemaal niet noemt). Symptoom: een leaf/operatie genoemd naar een
toelichtings-term, terwijl de wet alleen "naar de omstandigheden te beoordelen" o.i.d. zegt.
→ Hernoem/herorden zodat het model de open norm van de letter draagt; verplaats de toelichtings-uitleg
naar de `description`/comment, expliciet gelabeld als toelichting.

### Klasse 2 — ontbrekend verbatim-bestanddeel
Een woord of voorwaarde dat **in de letter staat** maar niet in het model zit: een kwalificatie
("rechtmatig", "uitsluitend", "tijdelijk"), een "tenzij"-clausule, of een hele uitsluiting. Grep de
verbatim `text:` op "tenzij", "behoudens", "voor zover", "niet ... dan wel", en controleer of elke
voorwaarde in de `actions` terugkomt. → Voeg het ontbrekende bestanddeel toe (richting de letter).

### Klasse 3 — verkeerde verankering (legal_basis)
Een endpoint hangt aan een "kapstok"-artikel terwijl de dragende norm in een buurartikel of in een
andere wet staat (bv. de beslislogica zit in art. N+1, of een leeftijds-/statuseis in een ander
wetboek). De beslislogica kan correct zijn; de **herleidbaarheid** klopt niet. → Markeer als
`legal_basis`-/architectuur-kwestie (jurist/architectuur), meestal geen logica-fix.

### Klasse 4 — verbatim-drift in `text:`
Het `text:`-veld draagt een **ingetrokken of oudere redactie** (verwijzing naar een ingetrokken wet,
een oude instantienaam) terwijl de feitelijk geldende tekst anders luidt. Kruis-check verbatim tegen
de bron op de claimed `valid_from` (zie de `law-version-drift-check`-skill). → Actualiseer het
`text:`-veld naar de geldende verbatim redactie; corrigeer nooit een fout die in de geldende wet
zélf staat (die rapporteer je).

## Lid-conflict & afwijkings-precedence

Wanneer een positieve grond (een toekennend lid) en een uitsluiting (een ontzeggend lid) elkaar lijken
te weerspreken, **controleer eerst de chapeau** op een expliciete voorrangsregel vóór je een "conflict"
of "lacune" rapporteert:
- Een chapeau als *"zo nodig **in afwijking van** het [vorige lid], is niet ..."* betekent dat de
  uitsluiting **dérogeert** aan de positieve grond — dan is de uitsluitende uitkomst de letter, geen
  modelkeuze en geen lacune.
- Een tegen-uitsluiting als *"[lid X] is niet van toepassing op ..."* schakelt (een deel van) de
  uitsluiting weer uit; modelleer de exacte reikwijdte (welke onderdelen, welke subgroep).
Modelleer de precedence **zoals de letter die stelt**. Als de letter zo een groep uitsluit die de
bedoeling juist insluit, is dat een wettekst-gevolg (zie classificatie), geen modelfout.

## Classificatie van elke bevinding

| Bucket | Betekenis | Actie |
|---|---|---|
| **MODELFOUT** | het model wijkt af van de letter | aanpassen richting de letter |
| **WETTEKST-GEVOLG** | model = letter, maar de letter zelf produceert een vreemde/onbedoelde uitkomst | **rapporteren**, niet "fixen" in het model |
| **LETTER-vs-TOELICHTING** | letter en toelichting divergeren | jurist bepaalt wat leidend is; tevens **signaal voor herziening** (de bedoeling hoort dan in de wéttekst — primaat van de wetgever) |

Voor elke WETTEKST-GEVOLG- en LETTER-vs-TOELICHTING-bevinding: formuleer een **jurist-vraag** en, waar
toepasselijk, een wetgevings-signaal (de norm hoort kenbaar in de regelgeving, niet in toelichting of
stilzwijgende uitvoeringscorrectie).

## Verificatie (geen hunches)

Toets uitkomsten via de engine (`evaluate`-binary, met `extra_laws` voor cross-law), met alleen
upstream-leaf-feiten en anti-masking (flip een bron-feit, zie de uitkomst omklappen) — niet door de
uitkomst direct te injecteren. Schema-validatie en cross-law-integriteit blijven groen.

## Output

Per artikel/lid: (verbatim passage) → (wat het model doet) → (afwijkingsklasse of "letter-getrouw") →
(classificatie: modelfout/wettekst-gevolg/letter-vs-toelichting) → (jurist-vraag waar van toepassing).
Sluit af met een prioriteitenlijst en, voor letter-vs-toelichting-bevindingen, een aparte paragraaf
"Lezing: toelichting náást de letter" puur op de twee teksten (zonder de implementatie erbij).

## Samenhang met andere skills
- `law-version-drift-check` — dekt klasse 4 (verbatim-drift) in detail; draai die als Step 0.
- `regelrecht-stelselanalyse` — cross-law-integriteit, cyclus-workflow en classificatie-taxonomie.
- `law-generate` — de plaatsings-/bindingsregels (source onder `input:`, niet `parameters:`).
