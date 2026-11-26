---
name: reviewen
description: >-
  Reviewt een tekst zonder iets te veranderen: taal en spelling, AI-patronen, structuur en opbouw, toon voor de
  lezer, en (als die aan staan) APA en academische stijl, plus de beoordelingscriteria of inlevereisen van een
  vak als die in de werkmap staan. Levert een reviewrapport met bevindingen per regel, prioriteiten en de vijf
  belangrijkste acties; korte teksten (mail, post) krijgen hun review in de chat. Gebruik bij
  /dutchquill:reviewen, of als de gebruiker vraagt een tekst na te kijken, te beoordelen of feedback te geven
  ("kijk mijn rapport na", "review this draft", "is deze mail goed zo", "geef feedback op hoofdstuk 3").
argument-hint: "[tekst of pad] [waar je vooral op wilt letten]"
when_to_use: >-
  Gebruik deze skill ook als de gebruiker DutchQuill niet noemt: bij elke vraag om feedback op of een check van
  een eigen tekst (rapport, hoofdstuk, mail, post), zonder dat de tekst herschreven hoeft te worden.
---

# Reviewen

Opdracht: $ARGUMENTS

Je verandert niets aan de tekst. Je levert een review.

Elk `dq`-commando draai je via Bash met dit voorvoegsel; hieronder staat het als `DQ`:

```bash
CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq"
```

## Stand

!`DQ_NIET_INSTALLEREN=1 CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq" config toon --kort 2>&1 | tail -10 || true`

## Stappen

1. **Lees de werkwijze:** `${CLAUDE_PLUGIN_ROOT}/gidsen/werkwijze/basis.md`.
2. **Tekst en genre.** Lees de tekst: geplakt, een pad, of uit de werkmap. Een .docx of .pdf lees je via
   `DQ extraheer`. Bij een .docx ook de opmaak: kijk of de beelden (in de map `-beelden`) en de koppen kloppen.
   Bepaal het genre en laad de config: `DQ gids voor --genre <genre>`. Een review gaat over de modules die aan
   staan. Vraagt de gebruiker expliciet om iets anders ("let ook op APA"), doe dat dan ook.
3. **Gidsen lezen** (werkwijze 2), plus bij het studentprofiel de criteria van het vak:
   - Draai `DQ vak toon --json`. Heeft de gebruiker één vak, dan kiest het commando dat vanzelf. Geeft het
     `"status": "kies"`, vraag dan welk vak (noem de opties; staat de vakcode op de titelpagina, stel die voor) en
     draai `DQ vak toon --code <CODE> --json`. Bij `"geen"` of `"leeg"` is er geen rubric: ga door zonder.
   - Meld in één regel welke criteria geladen zijn (de `melding`, bijvoorbeeld "Criteria geladen voor ABC1: 8
     inlevereisen; 12 beoordelingscriteria").
   - Het commando geeft alleen de items onder `## Rapportage`; die onder `## Praktijk` gaan niet over de tekst en
     tellen niet mee. Staat er geen sectie Rapportage in het bestand, dan zijn alle items gelezen; zeg dat erbij.
   - De bestanden staan in `<werkmap>/templates/vakken/<VAKCODE>/` (`quick-scan.md` en
     `beoordelingscriteria.md`). Voorbeelden van het formaat: `${CLAUDE_PLUGIN_ROOT}/templates/student/`.
4. **Scripts** (de subagent `dutchquill:tekst-analist` kan ze voor je draaien en samenvatten):
   - `DQ tells --input <tekst> --genre <genre> --json`
   - `DQ leesbaarheid --input <tekst>` (Nederlands)
   - `DQ apa-check --input <tekst>` als APA aan staat
   - de taalronde uit `${CLAUDE_PLUGIN_ROOT}/gidsen/werkwijze/taalronde.md`, altijd: elke fout wordt een
     bevinding in het domein Taal; met `privacy.languagetool` aan ook `DQ taalcheck --input <tekst> --lang <taal>`
5. **Zelf lezen.** De scripts vangen niet alles. Loop deze domeinen na:

   | Domein | Waarop | Geldt |
   |---|---|---|
   | Taal | spelling, d/t, zinsbouw, interpunctie, consistentie (je/u, schrijfwijze van termen) | altijd |
   | Helderheid en structuur | hoofdboodschap vooraan, rode draad, alinea's met één gedachte, koppen die kloppen, aansluiting vraag en conclusie | altijd |
   | Toon en lezer | past de toon bij lezer en genre (`toon.md`), wordt er uitgelegd wat de lezer al weet | altijd |
   | AI-patronen | volgens `humaniseren.md`; sterke tells, clusters, formules, ritme | als humaniseren aan staat |
   | APA | bronvermelding in de tekst en in de lijst, titelpagina, koppen, tabellen en figuren, bijlagen, AI-verantwoording | als apa aan staat |
   | Academische stijl | spreektaal, werkwoordstijden, ik-vorm, onderbouwing | als academische_stijl aan staat |
   | Vakcriteria | per criterium uit de rubric: voldoet de tekst, en waar blijkt dat uit | als er een rubric is |

6. **Het reviewrapport.** Elke bevinding krijgt:
   - een plek (hoofdstuk, alinea of regel, met een citaat van hooguit tien woorden);
   - wat er mis is;
   - een voorstel;
   - een prioriteit: **moet** (fout of eis), **beter** (duidelijke winst), **kan** (smaak).

   Geef per domein een kort oordeel in één zin.

   **Inlevereisen** (als er een quick scan is): loop elk item na en geef het een teken:
   ✓ voldaan, ⚠ deels, ✗ niet voldaan, ? niet te beoordelen uit de tekst (bijvoorbeeld de paginanummers in een
   Markdown-bestand). Een tabel met eis, teken en waar het blijkt. Daaronder de telling "X van Y voldaan" (alleen ✓
   telt) en het oordeel **Voldoet aan de inlevereisen** (geen ✗ en geen ⚠) of **Nog niet klaar voor inlevering**.
   De rubric (beoordelingscriteria) beoordeel je per criterium in het domein Vakcriteria, met dezelfde tekens.

   **Eindoordeel**, bovenaan het rapport en in de chat, een van drie:
   - **Klaar voor inlevering**: geen bevindingen met prioriteit moet, en de inlevereisen voldoen (als die er zijn);
   - **Kleine aanpassingen**: hooguit vijf keer moet, elk snel op te lossen, en geen ✗ bij de inlevereisen die veel
     werk is;
   - **Herschrijven aanbevolen**: meer of zwaardere moet-bevindingen, of de opbouw of de hoofdvraag klopt niet.

   Voor een mail, post of ander niet-academisch stuk heet het eerste oordeel **Klaar om te versturen** (of te
   plaatsen). Eindig met de vijf acties die het meeste opleveren.
   Schrijf het rapport in de taal van de tekst; in het Engels: Ready to submit / Minor changes / Rewrite
   recommended, Meets the submission requirements / Not ready to submit yet.

7. **Uitvoer.**
   - Mail, post of korte tekst: de review in de chat. Hooguit tien bevindingen, de belangrijkste eerst.
   - Document:
     1. `DQ versie volgende --actie reviewen --titel "<titel van de tekst>"`.
     2. Het overzichtsbeeld: `DQ reviewgrafiek --input <tekst> --genre <genre> --titel "<titel>" --oordeel
        "<eindoordeel>" --taalronde <aantal taalfouten> --output <map>/overzicht.png`. De cijfers komen uit
        `dq tells`; vul niets zelf in.
     3. Schrijf het rapport als `<map>/bron.md`, in deze volgorde:

        ```markdown
        # Review: <titel>

        ![Overzicht van de review](overzicht.png)

        ## Eindoordeel
        <het oordeel, en in twee of drie zinnen waarom>

        ## Inlevereisen            (alleen met een quick scan: tabel eis | ✓ ⚠ ✗ ? | waar, plus "X van Y voldaan")
        ## De vijf belangrijkste acties
        ## Bevindingen per domein  (per domein het oordeel in één zin, dan de bevindingen: plek, wat, voorstel, prioriteit)
        ## Cijfers                 (AI-patronen, leesbaarheid, woordvariatie; bij een rapport of het klaar is)
        ```

        In het Engels: Review, Overview of the review, Verdict, Submission requirements, The five most important
        actions, Findings per domain, Figures.
     4. `DQ export --bron <map>/bron.md --naam "Review <titel>" --template review`. De template `review` gebruikt
        nooit de APA-opmaak, ook niet bij het profiel student.
     5. In de chat: het pad, het eindoordeel, bij inlevereisen de telling, en de vijf acties.
   - Historie, ook bij een review in de chat: `DQ historie log --actie reviewen --titel "<titel>" --tekst <de
     review als bestand> --meta '{"genre": "...", "oordeel": "...", "uitvoer": "chat|bestand"}'` (plus
     `--bestand` bij een document).

## Klaar als

- [ ] Er is niets aan de tekst zelf veranderd.
- [ ] De taalronde is gedaan en de fouten staan als bevinding in het domein Taal.
- [ ] Elke bevinding heeft een plek, een voorstel en een prioriteit.
- [ ] Er zijn alleen domeinen beoordeeld die aan staan of waar de gebruiker om vroeg; de rubric is gebruikt als
      die er is.
- [ ] Er is een eindoordeel; bij een quick scan heeft elk item een teken en staat de telling erbij.
- [ ] Bij een document staat het overzichtsbeeld bovenaan het rapport.
- [ ] De vijf belangrijkste acties staan in de chat.
