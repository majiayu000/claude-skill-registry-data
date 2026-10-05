---
name: rubriek
description: Maakt voor een reeks leerdoelen een beoordelingsrubriek als rubriek.csv die in Microsoft Teams geladen kan worden, met één criterium per leerdoel, drie niveaus (Volledig behaald 100, Deels behaald 50, Niet behaald 0) en gewichten die samen 100 zijn. Gebruik bij /rubriek <leerdoelen>, als de leraar een rubriek voor Teams vraagt, of als stap van /overhoring. Controleert het bestand met check_rubriek.py.
---

# /rubriek `<leerdoelen>` [`<codes>`] [`<uitvoerpad>`]

Maakt een rubriek die de leraar in Teams bij een opdracht laadt en waarmee hij
**per leerdoel** beoordeelt.

Argumenten:

- **leerdoelen**: een `leerdoelen.md` van /leerdoelen (zie het formaat in
  `.claude/skills/leerdoelen/SKILL.md`), of een lijst leerdoelen in de chat.
  Heeft een doel geen code, nummer dan `D1`, `D2`, … en geef het een korte titel.
- **codes** (optioneel): alleen deze doelen, bv. `SQL1.1,SQL1.2,SQL2.4`.
  /overhoring geeft zo de doelen door die de overhoring echt toetst.
- **uitvoerpad** (optioneel): standaard `rubriek.csv` naast het
  leerdoelenbestand. Bij een lijst in de chat: vraag waar het bestand moet komen.

## Werkwijze

1. **Lees de doelen**: per `### <code> — <korte titel>` het `Doel` en het
   `Belang`. Beperk tot de gevraagde codes.
2. **Eén criterium per doel**, in de volgorde van het bestand. Naam:
   `<code> – <korte titel>`, bv. `SQL1.2 – Rijen filteren met één voorwaarde`.
3. **Drie niveaus**, altijd dezelfde, het hoogste eerst:
   `,"Volledig behaald","100","Deels behaald","50","Niet behaald","0"`.
4. **Beschrijf elk niveau voor dát doel**, concreet en zichtbaar in wat de
   leerling indient:
   - *Volledig behaald*: wat een juist antwoord voor dit doel toont.
   - *Deels behaald*: de typische halve fout bij dit doel, één of twee met
     naam (bv. "vergeet de haakjes bij AND en OR", "tekst zonder aanhalingstekens").
   - *Niet behaald*: wat ontbreekt of fundamenteel fout is.
   - Kort (één of twee zinnen), zonder onderwerp of in de derde persoon, zoals
     in het voorbeeld van de leraar. Niet drie keer dezelfde zin met
     "goed/matig/slecht".
   - Beoordeeld wordt over alle vragen heen die het doel toetsen: *volledig*
     betekent juist in al die vragen.
   - Geen modeloplossing van een vraag: leerlingen zien de rubriek in Teams, en
     de repo is publiek. Beschrijf het doel, niet het antwoord op vraag 3.
5. **Gewichten**: gehele getallen, samen precies 100. Kern weegt dubbel zo
   zwaar als aanvullend, tenzij de leraar iets anders vraagt. Verdeel 100 in
   die verhouding, rond af op gehele getallen en werk het verschil met 100 weg
   bij de kerndoelen, 1 per doel: te veel → de laatste kerndoelen −1, te weinig
   → de eerste +1. Bv. 7 kern + 3 aanvullend = 17 delen: 100 × 2/17 = 11,8 → 12
   en 100/17 = 5,9 → 6; 7 × 12 + 3 × 6 = 102, dus
   12, 12, 12, 12, 12, 11, 11, 6, 6, 6.
6. **Titel en beschrijving**: de titel die de leraar of /overhoring opgeeft,
   anders `Overhoring <onderwerp>` (uit `# Leerdoelen — <onderwerp>`). De
   beschrijving in één zin, bv. "Beoordeling per leerdoel, over alle vragen
   heen. Kerndoelen wegen dubbel."
7. **Schrijf het bestand** met de Write-tool, precies in het formaat hieronder.
8. **Controleer** vanuit de root van de repo:

   ```
   python .claude/skills/rubriek/check_rubriek.py <pad>/rubriek.csv
   ```

   (werkt `python` niet: `.venv/Scripts/python` op Windows,
   `.venv/bin/python` elders). Verbeter tot het script `OK` meldt, en herbereken
   bij een fout in de gewichten; pas nooit het script aan om een fout weg te
   werken.

## Het CSV-formaat van Teams

```csv
"Upload deze .csv in Microsoft Teams als een rubriek voor de beste bewerkingsmogelijkheden."

"<titel>","100"
"<beschrijving>"
""
,"Volledig behaald","100","Deels behaald","50","Niet behaald","0"
"<code> – <korte titel>","<volledig behaald>",,"<deels behaald>",,"<niet behaald>",
"<gewicht>"
"<code> – <korte titel>","<volledig behaald>",,"<deels behaald>",,"<niet behaald>",
"<gewicht>"
v.11p
```

- Regel 1 is die vaste zin, letterlijk; daarna een lege regel. De `100` in de
  titelregel blijft `100`.
- Elk veld tussen dubbele aanhalingstekens; een `"` in de tekst schrijf je als
  `""`. Komma's in de tekst mogen. Zonder aanhalingstekens: de lege eerste
  kolom van de niveauregel, de lege puntenkolom na elke beschrijving (daarom
  eindigt een criteriumregel op een komma) en `v.11p`.
- Per criterium precies twee regels, zonder lege regel ertussen. Een
  beschrijving blijft op één regel.
- `v.11p` is de laatste regel, met een regeleinde erna en niets meer.
- `voorbeeld-teams.csv` in deze map is het voorbeeld van de leraar (een
  rubriek uit een ander vak, met vier niveaus): alleen de vorm telt.
  `check_rubriek.py --alleen-teams voorbeeld-teams.csv` aanvaardt het.

**Codering: UTF-8 zonder BOM, met LF.** Zo exporteert Teams zelf een rubriek:
een ander project dat Teams-rubrieken maakt, vergeleek zijn uitvoer byte voor
byte met een export uit Teams (github.com/agrimuitobom/rubric, `HANDOFF.md`:
zonder BOM, LF, regeleinde op het einde). Teams is een webapp en leest UTF-8;
een BOM zou alleen Excel helpen en komt vóór de instructiezin terecht. LF past
bij de repo (`.gitattributes`, #56). De Write-tool schrijft UTF-8 zonder BOM;
`check_rubriek.py` weigert een BOM, CRLF en ongeldige UTF-8. **Niet in Excel
openen en bewaren**: Excel met Belgische instellingen maakt er puntkomma's en
een andere codering van. Aanpassen doe je na de import, in Teams.

**Nog niet bevestigd**: een echte import in Teams is hier niet getest. Vraag de
leraar bij de eerste rubriek na te gaan of de import lukt en of é, ë en – goed
staan. Lukt het niet, pas dan dit formaat en `check_rubriek.py` samen aan.

## Uitvoer

- **Los gebruikt**: toon het pad, de samenvatting van `check_rubriek.py`
  (titel, niveaus, criteria met gewicht) en hoe de leraar ze laadt: in Teams
  een opdracht maken of openen → **Rubriek toevoegen** → **Rubriek uploaden** →
  het .csv-bestand kiezen.
- **Vanuit /overhoring**: invoer `book/overhoringen/<naam>/leerdoelen.md`, de
  codes van de getoetste doelen en de titel; uitvoer
  `book/overhoringen/<naam>/rubriek.csv`, zonder vragen te stellen. Geef het
  pad en de samenvatting terug. Die map bouwt geen pagina van `rubriek.csv`
  (zie `book/overhoringen/README.md`).
