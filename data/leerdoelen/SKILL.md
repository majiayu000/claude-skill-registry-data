---
name: leerdoelen
description: Legt voor één hoofdstuk van de cursus DataBeheer de belangrijkste leerdoelen vast in leerdoelen.md, elk toetsbaar en met een code (bv. SQL1.3), een belang (kern of aanvullend) en de plaats in het hoofdstuk. Gebruik bij /leerdoelen <hoofdstuk>, als de leraar vraagt welke leerdoelen een hoofdstuk heeft, of als stap van /overhoring. Het resultaat is de invoer van /rubriek.
---

# /leerdoelen `<hoofdstuk>` [`<uitvoerpad>`]

Legt vast wat een hoofdstuk **echt aanleert en inoefent**, als toetsbare
leerdoelen. /rubriek maakt er een rubriek van, /overhoring (#63) kiest er de
vragen mee.

Argumenten:

- **hoofdstuk**: bv. `SQL 1`, `SQL H1`, `01_Starten_met_sql` of `Starten met SQL`.
- **uitvoerpad** (optioneel): waar `leerdoelen.md` komt.

## Werkwijze

1. **Zoek het hoofdstuk in `book/_toc.yml`.** Een hoofdstuk is de
   hoofdstukpagina (`chapters:`) plus al zijn `sections:`, bv.
   `chapters/SQL/01_Starten_met_sql` + `chapters/SQL/01b_AdventureWorks`.
   Is de invoer dubbelzinnig of onbekend: vraag het (los gebruikt) of stop met
   een melding (vanuit /overhoring).
2. **Lees elke pagina volledig**: uitleg, voorbeelden, tips en waarschuwingen,
   en de oefeningen. In de SQL-hoofdstukken staan de oefeningen als commentaar
   in de `sql-live`-codecellen (`--- 1. Toon ...`): lees die cellen mee.
3. **Maak een inventaris** van wat uitgelegd of voorgedaan wordt, en welke
   oefeningen het vragen. Het blok *Leerdoelen* bovenaan een hoofdstuk is een
   startpunt, geen bron: het is soms onvolledig. SQL H1 leert in §8 ook tekst
   samenvoegen met `||` en aliassen met `AS`; H2 filtert datums met `LIKE` en
   met vergelijkingen.
4. **Filter.**
   - Neem op: wat uitgelegd wordt **en** in een oefening terugkomt, ook op de
     toepassingspagina's (bv. dezelfde query's schrijven op een onbekende
     databank door het schema te lezen).
   - Laat weg: wat alleen terloops of in een uitgecommentarieerd voorbeeld
     opduikt en pas in een later hoofdstuk uitgelegd wordt (bv. foreign keys
     in SQL H1 §2: "daar komen we later op terug"), ook als een oefening het
     al vraagt (zo vroeg H1 §4 oef. 3 tot #65 om `LIKE`, stof van H2), en de
     uitleg over de website zelf (Run, Schema, Reset db, Mijn werk). Noteer
     wat je bewust weglaat bij `Niet opgenomen:`.
   - Toets: kan een leerling het doel halen met alleen dit hoofdstuk en de
     hoofdstukken ervoor? Zo niet, dan hoort het er niet bij.
5. **Formuleer per leerdoel één vaardigheid**: "De leerling kan …" met een
   waarneembaar werkwoord (opvragen, filteren, sorteren, berekenen, uitleggen,
   voorspellen, een fout vinden), niet "kent" of "begrijpt". Eén vraag moet het
   doel kunnen toetsen. Niet per operator opsplitsen, niet drie vaardigheden in
   één doel. Reken op 5 à 10 doelen per hoofdstuk.
6. **Bepaal het belang.**
   - `kern`: waar het hoofdstuk om draait: staat meestal in het blok
     *Leerdoelen*, komt in meerdere oefeningen terug, latere hoofdstukken bouwen
     erop voort.
   - `aanvullend`: wel aangeleerd en ingeoefend, maar bijzaak (bv. commentaar
     in een query, de valkuil `+` bij tekst, een onbekend schema lezen).
     /overhoring laat deze doelen eerst vallen.
   - Minstens de helft is kern.
7. **Noteer waar het staat**: paginanaam zonder extensie, paragraaf en de
   oefeningen, bv. `01_Starten_met_sql §4 Filteren met WHERE, oef. 1–5; 01b_AdventureWorks oef. 3–4`.
8. **Leerplan (optioneel)**: het leerplandoel uit `docs/leerplan.md`. De
   nummering daar is door de omzetting uit Word verhaspeld; tel zo:
   LPD 1 structuur en werking van een relationele databank toelichten ·
   LPD 2 een databank implementeren op basis van een eigen ontwerp (datamodel,
   normalisatie, ERD) · LPD 3 een databank uitbreiden · LPD 4 bevragen met SQL
   (selecteren, groeperen, sorteren, berekenen, filteren) · LPD 5 gegevens
   wijzigen, toevoegen en verwijderen met SQL · LPD 6 kenmerken van big data ·
   LPD 7 een dataset zoeken en een datawarehouse samenstellen (ETL/ELT) ·
   LPD 8 visualisaties maken met een BI-tool.
9. **Geef codes**: `<deel><hoofdstuk>.<n>`, met deel `SQL` (Databases Bevragen
   met SQL), `ERD` (Databases Ontwerpen met ERD's) of `BD` (Big Data), het
   nummer van de hoofdstukpagina (`03_JOIN` → 3) en `n` doorlopend vanaf 1 in
   de volgorde van het hoofdstuk: `SQL3.1`, `SQL3.2`, …

## Formaat van `leerdoelen.md`

Dit formaat is het contract met /rubriek en /overhoring: volg het exact.
Voorbeeld (ingekort; een echt hoofdstuk heeft 5 à 10 doelen):

````markdown
# Leerdoelen — SQL 1

## SQL 1 — Starten met SQL

Bron: `book/chapters/SQL/01_Starten_met_sql.ipynb`, `book/chapters/SQL/01b_AdventureWorks.ipynb`

Niet opgenomen: foreign keys (alleen genoemd in §2, uitgelegd in SQL 3), de uitleg over de editor (Run, Schema, Reset db, Mijn werk).

### SQL1.1 — Kolommen opvragen met SELECT … FROM
- Doel: De leerling kan met `SELECT … FROM` gekozen kolommen of met `*` alle kolommen uit één tabel opvragen.
- Belang: kern
- Waar: 01_Starten_met_sql §3 Je eerste query, oef. 1–5; 01b_AdventureWorks oef. 1–2
- Leerplan: LPD 4

### SQL1.2 — Rijen filteren met één voorwaarde
- Doel: De leerling kan met `WHERE` en een vergelijking (`=`, `<>`, `<`, `>`, `<=`, `>=`) de gevraagde rijen selecteren, met tekst tussen enkele aanhalingstekens.
- Belang: kern
- Waar: 01_Starten_met_sql §4 Filteren met WHERE, oef. 1 en 4; 01b_AdventureWorks oef. 3–4
- Leerplan: LPD 4

### SQL1.8 — Tekst samenvoegen met ||
- Doel: De leerling kan tekstkolommen samenvoegen met `||` en uitleggen waarom `+` dat in SQLite niet doet.
- Belang: aanvullend
- Waar: 01_Starten_met_sql §8 Berekende kolommen + aliassen, oef. 1
- Leerplan: LPD 4
````

Regels:

- `# Leerdoelen — <onderwerp>`: het hoofdstuk (`SQL 1`) of, vanuit /overhoring,
  de overhoring (`SQL 1 en 2`).
- Per hoofdstuk een sectie `## <deel> <nr> — <titel>`, met een regel `Bron:`
  (de bestanden) en eventueel `Niet opgenomen:` (wat bewust wegbleef, en waar
  het wel thuishoort: /overhoring vraagt daar niet naar). Meerdere hoofdstukken
  in één bestand: één sectie per hoofdstuk, in cursusvolgorde.
- Per leerdoel een kop `### <code> — <korte titel>` (streepje `—`, titel
  hoogstens een zestal woorden: /rubriek maakt er de naam van het criterium
  van), direct gevolgd door de velden `- Doel:`, `- Belang:` (`kern` of
  `aanvullend`), `- Waar:` en eventueel `- Leerplan:`, in die volgorde. Geen
  andere regels ertussen.
- Na de hoofdstukken mag /overhoring eigen secties toevoegen (bv. `## Dekking`,
  de tabel vraag × leerdoel). Die bevatten geen `###`-kop met een code.
- Codes zijn de sleutel tussen `leerdoelen.md`, `rubriek.csv` en de
  overhoring: hernummer niet meer zodra een rubriek of overhoring ernaar
  verwijst.
- Geen modeloplossingen: `book/` is publiek.

## Uitvoer

- **Los gebruikt**: toon het resultaat in de chat. Is er een uitvoerpad,
  schrijf het daar (UTF-8, LF); anders vraag of en waar het bewaard moet worden.
- **Vanuit /overhoring**: schrijf naar `book/overhoringen/<naam>/leerdoelen.md`
  zonder vragen te stellen en meld het aantal doelen (kern en aanvullend). Die
  map bouwt geen pagina van `leerdoelen.md` (zie `book/overhoringen/README.md`).

## Controle voor je afrondt

- Elk doel is haalbaar met dit hoofdstuk (en de vorige) en toetsbaar met één vraag.
- Geen oefening vraagt iets waarvoor geen doel bestaat (tenzij het onder
  `Niet opgenomen:` staat), en elk doel komt in een oefening terug.
- Elke `Waar` klopt met de paragrafen en oefeningen in de notebooks.
- Codes uniek en doorlopend; kop en velden precies volgens het formaat.
