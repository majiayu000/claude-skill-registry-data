---
name: overhoring
description: Stelt voor één of meer hoofdstukken van de cursus DataBeheer een volledige overhoring op en publiceert ze op GitHub Pages. Legt de leerdoelen vast (/leerdoelen), kiest hoogstens 10 vragen die elk minstens 2 leerdoelen toetsen, maakt de rubriek voor Teams (/rubriek) en een overhoringpagina met SQL-, open en meerkeuzevragen op gadgetshop.db, in book/overhoringen/<naam>/. Gebruik bij /overhoring <hoofdstukken>, of als de leraar een overhoring of toets over een hoofdstuk vraagt. Geeft de link naar de overhoring en naar rubriek.csv, om in Teams een opdracht te maken.
---

# /overhoring `<hoofdstukken>` [`<naam>`] [`--niet-publiceren`]

Argumenten:

- **hoofdstukken**: één of meer hoofdstukken, zoals /leerdoelen ze aanvaardt,
  bv. `SQL 1 en 2` of `SQL H1-H2`.
- **naam** (optioneel): de slug van de map, bv. `sql-h1-h2`. Anders stel je er
  een voor uit de hoofdstukken (`sql-h1-h2`, `sql-h3`) en gebruik je die.
- **--niet-publiceren** (optioneel): maken, controleren en committen op de
  huidige branch, zonder push, bv. binnen een batch of een PR (stap 7).

Resultaat: een nieuwe map `book/overhoringen/<naam>/` met `overhoring.ipynb`
(de pagina), `leerdoelen.md` (voor de leraar, met de dekkingstabel) en
`rubriek.csv` (voor Teams). Lees eerst `book/overhoringen/README.md`: het
formaat van de pagina, de databank gadgetshop.db en het adres.

Gebruik de Python van .venv (`.venv/Scripts/python` op Windows,
`.venv/bin/python` elders): `check_overhoring.py` gebruikt de parser van de
build, en die importeert Sphinx.

## 0. Voorbereiding

- **Publiceren** (standaard): `git status --porcelain` is leeg, je staat op
  `main`, en `git pull --ff-only` lukt. Zo niet: stop en vraag de leraar
  (eerst opruimen, overschakelen naar `main`, of `--niet-publiceren`).
- `book/overhoringen/<naam>/` bestaat nog niet. Bestaat ze wel: vraag of ze
  vervangen moet worden (met `--niet-publiceren` zonder leraar: stop).

## 1. Leerdoelen

Volg /leerdoelen (`.claude/skills/leerdoelen/SKILL.md`) voor elk gevraagd
hoofdstuk, en schrijf alles in één `book/overhoringen/<naam>/leerdoelen.md`:
`# Leerdoelen — <onderwerp>` (bv. `SQL 1 en 2`), één `##`-sectie per hoofdstuk,
in cursusvolgorde. Meld het aantal doelen, kern en aanvullend.

## 2. Selectie en vraagontwerp

Kies de doelen en de vragen **vóór** de rubriek: de rubriek bevat alleen wat
getoetst wordt.

- **Hoogstens 10 vragen.** Er zijn geen punten per vraag: de leraar beoordeelt
  achteraf per leerdoel met de rubriek. Daarom toetst **elke vraag minstens 2
  leerdoelen**.
- **Elk gekozen leerdoel wordt door minstens één vraag getoetst**; anders kan
  het niet beoordeeld worden en hoort het niet in de rubriek.
- **Passen niet alle doelen, dan vallen eerst de aanvullende doelen weg**, pas
  daarna kerndoelen: geen kerndoel weg zolang een aanvullend doel getoetst
  wordt. Passen zelfs de kerndoelen niet (vooral bij meerdere hoofdstukken):
  meld het en stel voor de overhoring te splitsen.
- **Per doel het passende vraagtype**, en alle drie komen voor:
  - een query schrijven → SQL-vraag (`sql-live`);
  - uitleggen, voorspellen wat een query toont, een fout vinden → open vraag
    (`overhoring-open`) of meerkeuze (`overhoring-mc`).
- **Alleen stof uit de gevraagde hoofdstukken** (en de vorige): niets uit
  `Niet opgenomen:`, niets van later. Voor SQL H1–H2 dus geen JOIN, GROUP BY
  of aggregaatfuncties. Heeft je modelquery meer nodig, dan is de vraag fout.
- **SQL-vragen gaan over gadgetshop.db** (schema en inhoud in
  `book/overhoringen/README.md`), niet over een databank uit de lessen. De
  leerling leest het schema met de knop **Schema**. Formuleer zo dat er één
  juist resultaat is: welke kolommen, welke rijen, welke volgorde.
- **Meerkeuze**: 3 à 4 aannemelijke opties met typische fouten (`= NULL`, `+`
  voor tekst, haakjes vergeten bij AND en OR); het juiste antwoord niet telkens
  op dezelfde plaats.
- **Controleer tegen de databank.** Schrijf per SQL-vraag een modelquery, en
  voer ook elke query uit die in een vraag staat (bij "wat toont deze query?"):

  ```
  .venv/Scripts/python .claude/skills/overhoring/check_overhoring.py --query "SELECT ..." --query "SELECT ..."
  ```

  Elke query werkt en geeft een zinvol, niet-leeg resultaat (niet alleen NULL,
  geen duizenden rijen als de vraag er een handvol bedoelt). Het script opent
  de databank alleen lezend en schrijft niets weg.
- **Geen modeloplossingen in de repo**: repo en site zijn publiek. Oplossingen
  alleen in de chat (stap 8), niet in `leerdoelen.md`, niet in de notebook
  (ook niet in een `remove-cell`), niet in een ander bestand in de map.

Schrijf de keuze na de hoofdstukken in `leerdoelen.md`, als sectie
`## Dekking`: de tabel vraag × leerdoel waarmee de leraar per leerdoel
beoordeelt. `check_overhoring.py` leest ze, volg het formaat exact:

````markdown
## Dekking

Beoordeel per leerdoel (een rij) over de aangeduide vragen heen.

| Leerdoel | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| SQL1.1 — Kolommen opvragen met SELECT … FROM | x | | x | | |
| SQL1.2 — Rijen filteren met één voorwaarde | x | x | | | x |
| SQL1.8 — Tekst samenvoegen met \|\| | | | x | x | |
| SQL2.1 — Ontbrekende waarden filteren | | x | | x | x |

Niet getoetst: SQL1.9 (aanvullend), SQL2.6 (aanvullend).
````

- Eén kolom per vraag, `V1` tot `Vn`; één rij per getoetst leerdoel, in de
  volgorde van het bestand: `<code> — <korte titel>` (een `|` in de titel
  schrijf je `\|`), `x` waar de vraag het doel toetst, anders leeg.
- Alleen getoetste doelen in de tabel. Wat wegviel, noem je onder
  `Niet getoetst:`.
- Geen `###`-kop in deze sectie: /rubriek zou er een leerdoel in zien.

## 3. Rubriek

Volg /rubriek (`.claude/skills/rubriek/SKILL.md`) met als codes de rijen van
de dekkingstabel, als titel de titel van de overhoring (`Overhoring
<onderwerp>`) en als uitvoer `book/overhoringen/<naam>/rubriek.csv`.

## 4. De overhoring

Kopieer `book/overhoringen/template/overhoring.ipynb` naar
`book/overhoringen/<naam>/overhoring.ipynb` en pas het aan:

- **Verwijder de notitie voor de auteur** (de cel met `remove-cell`): ze staat
  niet op de site, maar wel in de publieke repo. Geen `remove-cell`-cellen.
- De `sql-db`-cel blijft `/_static/db/gadgetshop.db`.
- **Titelcel**: `# <titel>` (dezelfde als de rubriek), de korte instructie uit
  de template en `## Doelen`: **één punt per getoetst leerdoel**, in de volgorde
  van de rubriek en in leerlingentaal, met de code erachter zodat de leerling
  het criterium in Teams terugvindt: `- Je kan rijen kiezen met WHERE en één
  voorwaarde (SQL1.2)`.
- **Per vraag** een markdowncel `## Vraag n` (doorlopend vanaf 1; een titel
  erachter mag, `## Vraag 2 — NULL`, maar verklap het antwoord niet) met de
  vraagtekst, en daarna precies één antwoordcel:
  - `sql-live`: `-- Schrijf hier je query.`
  - `overhoring-open`: een hulptekst, bv. `Schrijf hier je uitleg.`
  - `overhoring-mc`: de opties, één per regel, zonder aan te duiden welke juist is.

  Een query die bij de vraag hoort, zet je in de markdown als ` ```sql `-blok.
- Elke cel heeft een eigen `id` (8 hexadecimale tekens): hergebruik een id uit
  de template hoogstens één keer.

## 5. Controle

Vanuit de root van de repo. Verbeter tot alles klopt; pas nooit een script aan
om een fout weg te werken.

1. `.venv/Scripts/python .claude/skills/overhoring/check_overhoring.py book/overhoringen/<naam>`
   meldt `OK`. Het controleert het formaat (met `parse_quiz` uit
   `book/_ext/overhoringen.py`), hoogstens 10 vragen, de drie types,
   gadgetshop.db, minstens 2 doelen per vraag, elk doel getoetst, eerst de
   aanvullende doelen weg, de rubriek precies de getoetste doelen, één punt
   per doel onder `## Doelen`, geen `remove-cell` en geen andere bestanden.
2. `.venv/Scripts/python .claude/skills/rubriek/check_rubriek.py book/overhoringen/<naam>/rubriek.csv`
   meldt `OK`.
3. `.venv/Scripts/teachbooks build book`, met de uitvoer in een bestand in je
   scratchpad: geen enkele `WARNING`, en de pagina
   `book/_build/html/overhoringen/<naam>/overhoring.html` bestaat. Een nieuwe
   map verandert `exclude_patterns`, dus de build leest alle pagina's opnieuw;
   de cursus zelf bouwt zonder warnings. Gaat een warning over een
   cursuspagina, dan is dat een regressie buiten de overhoring: noem ze, maar
   los ze hier niet op.
4. `TESTS_FAIL_ON_SKIP=1 .venv/Scripts/python -m pytest tests/test_overhoringen.py tests/test_overhoring_skill.py`
   (in PowerShell eerst `$env:TESTS_FAIL_ON_SKIP=1`) is groen: die controleren
   ook de map, de gebouwde pagina en de pagina in Chromium (elke SQL-editor
   draait op gadgetshop.db, elk antwoordvak werkt, **Download mijn antwoorden**
   bevat elke vraag). Zonder `TESTS_FAIL_ON_SKIP` slaan de Chromium-tests
   zichzelf stil over als Playwright of Chromium ontbreekt
   (`playwright install chromium`), en lijkt de controle groen zonder dat de
   pagina ooit geopend werd.

## 6. Publiceren (standaard)

**Bewust rechtstreeks op `main`, zonder PR**: de commit bevat alleen de nieuwe
map (inhoud, geen code), en de deploy (`call-deploy-book`) wachtte nooit op de
tests (`tests.yml` loopt apart en houdt een publicatie niet tegen). Een PR zou
alleen een wachttijd voor de les toevoegen. Wil de leraar toch een PR: vervang
deze stap door een branch en een PR zoals bij /start-work; de rest blijft.

1. `git status --porcelain` toont alleen `book/overhoringen/<naam>/`. Staat er
   iets anders: stop.
2. **Vraag bevestiging.** Toon de bestanden die je commit, de vragen met hun
   leerdoelen (de samenvatting van `check_overhoring.py`) en dat repo en site
   publiek zijn vanaf de push. Geen ja: stop, de bestanden blijven staan.
3. `git add book/overhoringen/<naam>`, dan
   `git commit -m "feat(overhoringen): overhoring <naam>"` en
   `git push origin main`.
4. **Wacht op de deploy.** Zoek de run van je commit:
   `gh run list --workflow call-deploy-book.yml --commit <sha> --json databaseId,status --limit 1`
   (de run verschijnt soms pas na enkele seconden: probeer opnieuw), dan
   `gh run watch <id> --exit-status`. Mislukt: toon
   `gh run view <id> --log-failed` en stop.
5. **Controleer de pagina**: `curl -s -o /dev/null -w "%{http_code}" <url>`
   geeft `200` (soms pas een minuut na de run: probeer een paar keer).

## 7. Niet publiceren (`--niet-publiceren`)

Stap 0 (behalve de nieuwe map) en stap 6 vervallen; niets wordt gepusht. Na
stap 5 commit je alleen de map, op de huidige branch, zonder te vragen:
`git add book/overhoringen/<naam>`, dan
`git commit -m "<boodschap>" -- book/overhoringen/<naam>`, met de boodschap
van de aanroeper (bv. met een issuenummer), anders
`feat(overhoringen): overhoring <naam>`. De links in stap 8 werken pas na de
merge naar `main` en de deploy; zeg dat erbij. Een gepushte branch staat wel
al als voorbeeld op `https://yvanvds.github.io/DataBeheer/<branch>/…`, met
elke `/` in de branchnaam als `-`.

## 8. Resultaat

`check_overhoring.py` drukt de links af. Geef de leraar, om in Teams een
opdracht te maken:

- **De overhoring**:
  `https://yvanvds.github.io/DataBeheer/main/overhoringen/<naam>/overhoring.html`.
  Gebruik het adres met `/main/`: de deploy zet elke branch in een eigen map,
  en zonder `/main/` geeft GitHub Pages een 404 die pas met JavaScript
  doorverwijst.
- **De rubriek**, `rubriek.csv`:
  - downloaden: `https://raw.githubusercontent.com/yvanvds/DataBeheer/main/book/overhoringen/<naam>/rubriek.csv`
    (rechtsklikken, *Opslaan als*);
  - op GitHub: `https://github.com/yvanvds/DataBeheer/blob/main/book/overhoringen/<naam>/rubriek.csv`;
  - lokaal: het volledige pad naar `book/overhoringen/<naam>/rubriek.csv`.

  In Teams: opdracht maken → link naar de overhoring → **Rubriek toevoegen** →
  **Rubriek uploaden** → het .csv-bestand. De leerling dient het bestand van
  **Download mijn antwoorden** in (`<naam>-antwoorden.md`).
- **De vragen**: per vraag het type en de leerdoelen, en wat niet getoetst
  wordt (de samenvatting van `check_overhoring.py`).
- **De modeloplossingen, alleen hier in de chat**: per SQL-vraag de modelquery
  en het aantal rijen dat ze geeft, per meerkeuzevraag de juiste optie, per
  open vraag de kern van een goed antwoord.
- **Twee waarschuwingen**:
  - Repo en site zijn **publiek**: vanaf de push kan wie de repo of het adres
    vindt de overhoring zien. Moet ze geheim blijven tot de toets, publiceer
    dan kort voor de les.
  - Controleer bij de **eerste import** van een rubriek in Teams of die lukt en
    of é, ë en – goed staan (zie /rubriek).
