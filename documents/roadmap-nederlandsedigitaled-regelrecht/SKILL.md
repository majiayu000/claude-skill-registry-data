---
name: roadmap
description: Onderhoudt de inhoud van de roadmap op /roadmap — werkpakketten toevoegen, wijzigen, verplaatsen of verwijderen, onderzoeksvragen schrijven en aan een sectie van het position paper koppelen, en RFC's koppelen die het ontwerp beschrijven. Gebruik dit bij "voeg een werkpakket toe", "verplaats X naar de Hoe-fase", "zet er een onderzoeksvraag bij", of het bijwerken van fases, disciplines en swimlanes.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Roadmap

De roadmap op `regelrecht.rijks.app/roadmap` is een read-only weergave van
bestanden in deze repo. Er is geen beheerscherm en geen schrijf-API: wijzigen
is een pull request, net als bij de rest van de repo.

Deze skill gaat over de **inhoud**. Voor de pagina's, het schema en de
buildcontroles die eronder liggen: die staan beschreven in de code zelf, en de
redenering erachter in de commits van PR #1317.

## Waar de inhoud staat

```
docs/src/content/roadmap/werkpakketten/<slug>.md   één bestand per werkpakket
docs/src/data/roadmap-config.json                  de fases, disciplines en swimlanes
```

De bestandsnaam ís het `id` uit de frontmatter. Dat wordt bij de build
gecontroleerd, dus hernoem nooit het een zonder het ander.

## Een werkpakket toevoegen

Kopieer géén bestaand bestand. Dat is de manier waarop je een dubbel `id`
maakt: de bestandsnaam pas je aan, het `id` in de frontmatter vergeet je, en de
matrix toont dan twee kaarten die naar dezelfde pagina wijzen. De build vangt
het (`id "…" wordt door meer dan één bestand gebruikt`), maar je hebt dan al
gewerkt aan het verkeerde bestand.

### Het id is een slug, en die kies je

Het `id` is een slug: kleine letters, cijfers, koppeltekens ertussen. Hij is
afgeleid van de titel, maar hij ís de titel niet — je kiest hem één keer en
daarna blijft hij staan.

`Referentie casus I` → `referentie-casus-i`
`Aansluiten op bronnen (chronolexografie)` → `aansluiten-op-bronnen-chronolexografie`

Een paar regels, en waarom:

- **Kleine letters, altijd.** Het schema weigert hoofdletters. De controle op
  bestandsnaam-is-id vergelijkt letterlijk, en op macOS is het bestandssysteem
  hoofdletter-ongevoelig: een hoofdletter lijkt lokaal in orde terwijl git de
  afwijkende schrijfwijze vastlegt en de build bij een ander valt.
- **Romeinse cijfers in een reeks blijven romeins.** `specificaties-i-…`,
  `specificaties-ii-…`. Dat houdt de reeks op volgorde in `ls` en leest als de
  titel.
- **Kort waar de titel lang is.** `Hoe omgaan met partijen als Raad van State,
  Sociaal-Cultureel Planbureau, CPB, etcetera?` werd `omgang-met-adviesorganen`.
  Een slug die de hele titel uitschrijft is geen verwijzing meer maar een zin.
- **Leesbaar boven volledig.** De slug wordt gelezen in een URL, in een lijst
  `samenhangIds`, en in de `Werkpakket:`-regel van een pull request. Dat is
  waar hij zijn werk doet.

**Verander een slug niet als de titel verandert.** De slug is een verwijzing:
er wijzen `samenhangIds` naar, er staan pull requests mee, en er is een URL van.
Een titel bijwerken is redactie; een slug bijwerken is een hernoeming die je
overal moet nalopen. Alleen doen als de slug echt niet meer klopt, en dan met
dezelfde zorg als het verwijderen van een werkpakket (zie onder).

Kies een slug die nog niet bestaat:

```bash
ls docs/src/content/roadmap/werkpakketten/
```

De build valt op een dubbele (`id "…" wordt door meer dan één bestand
gebruikt`), maar dan heb je al aan het verkeerde bestand gewerkt.

Het bestand bevat alleen frontmatter, geen body:

```yaml
---
id: <de slug van hierboven>
titel: Korte titel van het werkpakket
faseId: wat
disciplineId: recht
prioriteit: ''
omvang: ''
categorie: ''
capability: ''
capaciteit: ''
toelichting: |-
  Twee of drie alinea's die uitleggen wat de opgave is. Markdown mag:
  **vet**, een lijst, een link.

  Een lege regel wordt alleen een alinea-einde onder `|`.
volgorde: 1000
onderzoek: ''
bouw: ''
belegging:
  stand: ''
rfcs: []
onderzoeksvragen: []
afhankelijkVan: []
samenhangIds: []
---
```

### Wat er in de velden mag

`faseId` — een van `wat`, `wat-fase-2`, `hoe`, `waar`, `garantie`. Dit is een
procesvolwassenheids-fasering (Fase I t/m V), geen tijdas: de Wat-fase is met
opzet in twee stappen geknipt (fundering/definitie, dan verdieping/onderzoek)
in plaats van er een aparte tijdsindeling naast te zetten — dat las als twee
losse assen in één matrix. Zie de discussie in PR #1356.
`disciplineId` — een van `techniek`, `recht`, `mensen`, `ethiek`,
`service-design`, `samenwerking`, `transitie-ondersteuning`.

Beide staan in `roadmap-config.json`; een waarde die daar niet in staat laat de
build vallen met de naam van het werkpakket erbij.

`prioriteit` — `hoog`, `midden`, `laag`, of `''`.
`omvang` — `S`, `M`, `L`, `XL`, of `''`.
`categorie` — `bar`, `pivot`, `bet`, of `''`.
`capability` — `basis`, `ontwikkelen`, `simuleren`, `publiceren`, `analyseren`,
`implementeren`, `verifieren`, of `''`.

**Lege strings zijn normaal, geen tekortkoming.** Negenentwintig van de
negenenveertig werkpakketten hebben geen prioriteit, negentien geen categorie.
De roadmap groeit door
eerst een titel en een plek vast te leggen en de rest later in te vullen. Vul
niets in om het vakje te vullen; een verzonnen prioriteit is slechter dan een
lege.

`toelichting` — markdown, als **letterlijke** blok-scalar (`|-`). Neem geen
`>-`: dat is een gevouwen scalar, en YAML plakt daarin een lege regel samen tot
één regelovergang. Remark leest dat als een zachte afbreking, niet als een
nieuwe alinea, dus je krijgt één doorlopende lap tekst — zonder dat de build
iets zegt. Alleen onder `|` telt een lege regel als alinea-einde, en alleen daar
wijst de bewerkknop naar de juiste regels in plaats van naar het hele veld.

`capaciteit` — vrije tekst, bijvoorbeeld "2 fte, 6 maanden". Geen enum, geen
getal; leeg laten mag.

`onderzoek` — `open`, `loopt`, `beantwoord`, of `''`.
`bouw` — `niet`, `deels`, `wel`, of `''`.

Dat zijn twee assen en met opzet geen één. Een vraag kan beantwoord zijn zonder
dat er iets gebouwd is, en er kan iets staan terwijl de vraag erachter nog open
is. Eén gecombineerde status zou in de helft van de gevallen een verkeerd beeld
geven. Beide mogen leeg blijven; de pagina toont dan "Nog niet bepaald".

`belegging.stand` — `vrij`, `opgepakt`, `klaar`, of `''`. Plus
`belegging.sinds` (`'JJJJ-MM-DD'`, verplicht bij `opgepakt` en `klaar`).

Dit is een derde as naast `onderzoek` en `bouw`, en met opzet geen vierde
voortgangsveld: het zegt of er iemand op zit, niet hoe ver het is. `klaar` is
hier een eigen stand en geen afleiding uit `onderzoek: beantwoord` +
`bouw: wel` — een verkenning is klaar zonder dat er ooit iets gebouwd wordt.

**`''` betekent `vrij`.** Een leeg veld zegt dat niemand zijn hand heeft
opgestoken, en dat ís vrij. De pagina's lezen het zo (`getBelegging()` in
`docs/src/lib/roadmap.ts`), het filter heeft er dus ook maar drie knoppen: Vrij,
Opgepakt, Klaar. Je hoeft `vrij` nergens in te vullen — `''` laten staan is
hetzelfde en is wat bijna alle werkpakketten doen.

Dit stond hier andersom: `''` zou "er is niets over gezegd" betekenen en `vrij`
een redactionele daad, want een roadmap waar alles op `vrij` staat nodigt
niemand uit. Het bezwaar klopt, maar het antwoord was de verkeerde kant op.
Zesenveertig van de negenenveertig stonden leeg en géén enkele op `vrij`, dus
wie op "Vrij" filterde kreeg een lege matrix te zien terwijl juist die
zesenveertig open lagen. Dat de kaarten niet volstromen met een tag die zegt
dat er niets aan de hand is, wordt opgelost waar het hoort: `vrij` krijgt geen
tag op de matrix, alleen `opgepakt` en `klaar`.

**Er staat geen naam in, met opzet.** De roadmap is publiek en vanaf de
homepage gelinkt. Wie eraan werkt blijkt uit de pull requests, die via de
`Werkpakket:`-regel al aan het werkpakket hangen. Zet er dus geen `wie:` bij:
dat zou een persoonsnaam van een collega op een publieke pagina zetten, en het
veld gaat over óf het werk belegd is, niet over wie.

**En geen lijst met issues of pull requests**, om dezelfde reden als waarom er
geen labels per werkpakket zijn: de `Werkpakket:`-regel ís de index, en de
werkpakketpagina zoekt erop. Een lijst hier zou met de hand bijgehouden moeten
worden en verouderen zodra iemand dat vergeet.

```yaml
belegging:
  stand: opgepakt
  sinds: '2026-09-17'
```

`volgorde` — een getal dat de plek binnen één matrixcel bepaalt, laag eerst.
Dit veld is verplicht en heeft met opzet geen default: een ontbrekend veld zou
het werkpakket stilzwijgend bovenaan zetten. Gebruik stappen van 1000, dan kun
je er later tussen schuiven zonder alles te hernummeren.

`samenhangIds` — slugs van andere werkpakketten. De build controleert of ze
bestaan. Dit is eenrichtingsverkeer: zet je A → B, dan verschijnt B niet
automatisch bij A. Zet 'm er handmatig bij als de relatie wederzijds is.

`afhankelijkVan` — slugs van werkpakketten die af moeten zijn voordat dit
werkpakket kan beginnen. Een andere soort relatie dan `samenhangIds`, en houd
die twee uit elkaar: samenhang is wederzijds en zegt niets over volgorde,
afhankelijkheid is een richting in de tijd.

Zet het alleen neer waar het echt zo is. "Hangt hiermee samen" en "gaat hier
logisch op volgen" zijn geen afhankelijkheid; de toets is of het tweede
werkpakket zonder het eerste niet uitgevoerd kan worden.

Je schrijft één kant op. De werkpakketpagina leidt de andere kant er zelf uit
af en toont onder "Afhankelijkheden" allebei: waar dit werkpakket op wacht, en
wat op dit werkpakket wacht. Zet de omgekeerde verwijzing dus niet handmatig in
het andere bestand, want dan staat er een kring.

De build valt op een id dat niet bestaat, op een werkpakket dat naar zichzelf
wijst, en op een kring (`afhankelijkheden lopen rond: A → B → C → A`, met de
titels in de volgorde waarin hij ze tegenkwam). Een kring betekent dat geen van
die werkpakketten ooit kan beginnen; welke pijl de verkeerde is, is een
inhoudelijk oordeel en geen bestandsfout.

### Wat de matrix ermee doet

Onder "Weergave" staat een schakelaar **Afhankelijkheden**, en die staat uit.
De matrix is eerst een beeld van wat er te doen is; de afhankelijkheden zijn
een tweede lezing die een flink bredere kolom kost. Zet je 'm aan, dan gebeuren
er drie dingen tegelijk, en uit zet ze alle drie weer terug.

De kaart schuift naar rechts, één stap per werkpakket in de langste keten
achter zich binnen dezelfde fase. Een stap is een hele kaartbreedte plus de
ruimte voor de pijl, dus een kaart staat echt naast zijn voorwaarde en niet er
half overheen. Alleen binnen dezelfde fase geteld: wie op iets uit een eerdere
fase wacht, staat er al voorbij door in een latere kolom te staan.

De kaart gaat op de rij van de voorwaarde staan waar hij op wacht, zolang die
plek vrij is. Daardoor loopt een keten op één lijn en zijn de pijlen recht.
Staat die plek al vol, dan begint hij een rij eronder. Een kaart die in deze
cel niets voor zich heeft begint altijd een eigen rij, zodat twee werkpakketten
alleen naast elkaar staan als de een echt op de ander wacht.

En de pijl zelf wordt getekend. Wijs een kaart aan en de hele keten waar hij in
zit licht op, in beide richtingen doorgelopen; de rest van de matrix valt terug.

Je bepaalt de plaatsing dus niet zelf. `volgorde` blijft wel gelden: dat bepaalt
welke kaart als eerste een rij claimt, en daarmee de volgorde binnen de cel.

Dat rekenwerk gebeurt in de browser en niet bij de build, over de kaarten die
het zoekveld en het categoriefilter op dat moment laten staan. Filter je een
kaart weg, dan schuift de rest aan in plaats van een gat te laten, en een keten
loopt niet door over een kaart die niet op het scherm staat.

## Onderzoeksvragen

Een vraag is een gewone string, óf een mapping met een verwijzing naar het
position paper *Rules as Executed*:

```yaml
onderzoeksvragen:
  - >-
    Een vraag waar het paper niets over zegt blijft een gewone string.
  - vraag: >-
      Heeft een burger recht op de technische logbestanden van hoe een besluit
      tot stand is gekomen?
    paper: sec:traceaccess
```

Beide vormen mogen door elkaar in één lijst staan.

### De juiste sectie vinden

De ankers staan in de headings van het paper:

```bash
node -e "require('./docs/src/research/rules-as-executed.headings.json')
  .forEach(h => console.log(h.slug.padEnd(28), h.text))"
```

Sectie 12 is een onderzoeksagenda per discipline — `sec:agenda-legal`,
`sec:agenda-cs`, `sec:agenda-polsci`, `sec:agenda-philosophy`. Stelt het paper
de vraag daar zelf, wijs dan daarheen. Werkt een inhoudelijk hoofdstuk hem uit,
wijs dan naar dat hoofdstuk. Bij twijfel: het hoofdstuk, want daar staat een
antwoord in plaats van dezelfde vraag.

**Koppel niet wat niet past.** Drie van de drieënvijftig vragen hebben geen
sectie omdat ze te algemeen zijn ("Hoe navolgbaar is het?"). Een gedwongen
verwijzing kost de lezer een klik en levert niets op. Een verzonnen anker laat
de build vallen met het werkpakket en de vraag erbij.

## RFC's koppelen

`rfcs` is een lijst met RFC-nummers, als getal:

```yaml
rfcs:
  - 13
  - 21
```

De pagina toont ze onder "Ontwerp en implementatie", met de titel van de RFC en
zijn eigen `implementation`-waarde erbij. **Die waarde wordt niet overgenomen in
het werkpakket.** De RFC is het ding dat gebouwd wordt, dus die bezit dat feit;
een kopie hier zou een tweede waarheid zijn die niemand bijwerkt. Verandert een
RFC van `Not implemented` naar `Implemented`, dan verandert de roadmap mee
zonder dat je iets aanraakt.

Een nummer dat niet bestaat laat de build vallen (`RFC 99 bestaat niet`), met
het werkpakket erbij. Dezelfde RFC bij meerdere werkpakketten mag: RFC-013 hangt
nu aan drie. Twee keer hetzelfde nummer in één lijst levert één regel op, geen
twee.

### Welke RFC's nog nergens hangen

Elke RFC met `implementation: Implemented` hoort ergens in de roadmap terug te
komen: hij beschrijft werk dat gedaan is. Eén commando zegt welke dat nog niet
doen:

```bash
cd docs && node scripts/check-roadmap-rfcs.mjs
```

```
Roadmap-RFC-dekking: 5 van 15 geïmplementeerde RFC(s) hangen nog aan geen
enkel werkpakket:
  RFC-002  Bevoegdheid (Authority) in Machine-Readable Law
  …
```

Het draait ook mee in `just docs-a11y`, naast de andere `check-*`-scripts.

Dat is een melding en geen fout, met opzet. Een RFC die eerder landt dan de
roadmap-bijwerking is een redactionele achterstand, geen defect, en een poort
die daarop blokkeert zet de roadmap in de weg van het werk dat hij beschrijft.
Niet elke RFC hoort trouwens bij een werkpakket — RFC-000 gaat over het
RFC-proces zelf.

## Een werkpakket oppakken

Eén pull request, één bestand, twee regels:

```yaml
belegging:
  stand: opgepakt
  sinds: '2026-09-17'
```

De datum is de dag dat je het oppakt, niet de dag dat je klaar denkt te zijn.
De kaart op de matrix krijgt een tint en een tag; de detailpagina toont de
ouderdom ("sinds 3 maanden"), en dat is met opzet: een veld in de frontmatter
verloopt niet, dus de pagina moet laten zien hoe oud een claim is.

**Loslaten is dezelfde bewerking omgekeerd**, en een normale handeling, geen
falen. Zet `stand` terug op `''` (of `vrij`, dat is hetzelfde) en haal `sinds`
weg — dat laatste moet, want een datum bij een vrije stand rendert nergens en
de build valt erop. Doe dat ook
als je het werkpakket overdraagt: de belegging zegt dat het belegd is, niet
door wie, dus een overdracht verandert er niets aan — alleen een werkpakket dat
weer vrijkomt.

Een werkpakket dat af is krijgt `stand: klaar` (met de datum waarop het af
was). Dat is een uitspraak over het werkpakket als geheel, en niet hetzelfde
als `onderzoek: beantwoord` plus `bouw: wel` — een verkenning is klaar zonder
dat er ooit iets gebouwd is.

Welke werkpakketten al te lang op `opgepakt` staan:

```bash
cd docs && node scripts/check-roadmap-belegging.mjs
```

Dat meldt en blokkeert nooit, net als `check-roadmap-rfcs.mjs`; het draait mee
in `just docs-a11y`.

## Een werkpakket verplaatsen

Binnen een cel: pas `volgorde` aan. Naar een andere cel: pas `faseId` of
`disciplineId` aan, en geef het een `volgorde` die past tussen de buren in de
nieuwe cel.

## Een werkpakket verwijderen

Het bestand weggooien is niet genoeg: andere werkpakketten kunnen er via
`samenhangIds` naar wijzen, en die verwijzingen blijven achter. De build valt
daarop, en noemt elk bestand dat opgeruimd moet worden:

```
werkpakket controle-en-herstel (Controle en herstel): samenhangId "juridische-status-van-een-specificatie" bestaat niet
werkpakket discretionaire-ruimte (Discretionaire ruimte): samenhangId "juridische-status-van-een-specificatie" bestaat niet
```

Kijk dus eerst wie er naar verwijst, dan weet je vooraf wat je aanpast:

```bash
grep -l '<slug>' docs/src/content/roadmap/werkpakketten/*.md
```

Het bestand zelf staat ook in die uitkomst, want zijn eigen `id` staat erin;
de rest zijn de verwijzers.

Een slug die al in een pull request of een commit is genoemd, leeft ook buiten
de repo voort. Verwijderen mag, maar die verwijzingen wijzen daarna nergens
heen; dat is een reden te meer om een slug niet lichtvaardig te hergebruiken
voor een ánder werkpakket.

De app die hier ooit stond ruimde die verwijzingen zelf op bij het verwijderen;
dat deed een server die er niet meer is. Nu doet de build het niet voor je, hij
zegt alleen waar het misgaat.

## Fases en disciplines wijzigen

Die staan in `roadmap-config.json`. Een fase heeft een `volgnummer` dat de
kolomvolgorde bepaalt.

Disciplines zijn gegroepeerd in `swimlanes`: elke swimlane heeft een `naam` en
een `disciplineIds`-lijst, en die volgorde — swimlane voor swimlane, en
binnen een swimlane de volgorde van `disciplineIds` — bepaalt de rijvolgorde
op de matrix, niet de volgorde van het `disciplines`-blok zelf. Een swimlane
met meer dan één discipline krijgt een eigen, opvallende bannerrij erboven;
een swimlane met precies één discipline niet — die ene rij draagt dan zelf de
naam en de nadrukkelijke stijl van de swimlane (zie `matrixRijen` in
`pages/roadmap/index.astro`), anders zou dezelfde naam twee keer vlak boven
elkaar staan.

**Elke discipline moet in precies één swimlane staan.** Een nieuwe discipline
toevoegen aan `disciplines` zonder 'm ook in een `disciplineIds`-lijst te
zetten laat de build vallen op `assertSwimlanesMatchDisciplines`
(`lib/roadmap.ts`) — net als een `disciplineId` die niet bestaat, of die in
twee swimlanes tegelijk staat. Dat is met opzet een harde fout: een discipline
buiten elke swimlane zou stilzwijgend nergens renderen.

Een fase of discipline verwijderen kan alleen als geen enkel werkpakket er nog
naar wijst — anders faalt de build. Zoek eerst wie er hangt:

```bash
grep -l 'faseId: garantie' docs/src/content/roadmap/werkpakketten/*.md
```

**Een categorie toevoegen aan `CATEGORIEEN` in `docs/src/lib/roadmap.ts` is
geen inhoudelijke wijziging maar een codewijziging**, en er hoort een regel bij
in `docs/src/styles/roadmap.css`. Zonder die regel rendert het filtervakje wel,
maar blijven die kaarten verborgen zodra er gefilterd wordt. `assertFilterRules`
laat de build daarop vallen en zegt welke regel ontbreekt; volg die melding.

## Verifiëren

```bash
just docs-build     # schema + de controles hieronder; dit is de echte poort
just docs           # dev-server op :4321, om het na te kijken
```

De controles zitten in de paginasjablonen, dus onder de dev-server slaan ze pas
aan zodra je `/roadmap` echt opvraagt. Vertrouw op `docs-build`.

`docs-build` faalt met een leesbare melding bij:

- een onbekende `faseId` of `disciplineId`
- een discipline die in geen, of in meer dan één, swimlane staat
- een `samenhangId` dat nergens heen wijst
- een `afhankelijkVan` dat nergens heen wijst, naar zichzelf wijst, of in een
  kring loopt
- twee bestanden met hetzelfde `id`, of een bestandsnaam die niet het `id` is
- een `paper:`-anker dat niet in het paper staat
- een RFC-nummer in `rfcs` dat niet bestaat
- een `belegging` die niet klopt: `opgepakt` of `klaar` zonder `sinds`, een
  `sinds` bij een stand die hem nergens toont, een datum in de toekomst, of
  `vrij` op een werkpakket dat al beantwoord én gebouwd is — en een leeg veld
  telt daarin mee als `vrij`, want dat is wat het betekent
- een ontbrekende of foute waarde volgens het zod-schema

Raak je ook de pagina's aan, draai dan `just docs-a11y` (duurt ~10 minuten en
draait ook in CI).

### Wat de build níét controleert, met opzet

Onvolledige inhoud is geen fout. Een werkpakket zonder prioriteit, een cel
zonder werkpakketten, een vraag zonder papersectie: dat is de stand van het
werk, niet een defect. Een poort die daarover klaagt zou bij elke commit
afgaan en daarmee genegeerd worden — en hij zou het toevoegen van een
half-uitgewerkt werkpakket blokkeren, wat juist de manier is waarop deze
roadmap groeit.

Dat geldt ook voor de belegging: de build controleert niet of iemand nog echt
aan een opgepakt werkpakket werkt, of dat er pull requests aan hangen. Dat laatste zou een API-call in de
build betekenen, en een netwerkhapering tot een rode build maken. Voor de vraag
of een claim nog klopt is er `check-roadmap-belegging.mjs`, die meldt en niet
blokkeert.

Wil je weten waar de roadmap onaf is, kijk dan zelf:

```bash
grep -L 'prioriteit: [a-z]' docs/src/content/roadmap/werkpakketten/*.md
```

## Het werk dat bij een werkpakket hoort

Elke pull request draagt onderaan zijn omschrijving een regel met de slug van
het werkpakket waaraan hij bijdraagt:

```
Werkpakket: referentie-casus-i
Werkpakket: geen — losse typefout in de docs
```

De check `Werkpakket genoemd` blokkeert zonder die regel
(`script/require-werkpakket.sh`). De detailpagina van een werkpakket linkt
terug: "Pull requests op GitHub" zoekt op precies die regel.

**Er zijn geen labels per werkpakket, met opzet.** De zoekfunctie van GitHub
indexeert de body van een pull request, dus de regel is zelf al de index.
Negenenveertig labels zouden aangemaakt, toegepast en bij elke hernoeming
bijgewerkt moeten worden — een tweede waarheid die uit de pas loopt met de
regel die er toch al staat.

Dat de regel een trailer is, op zijn eigen regel onderaan, is waarom dit later
ook uit `git log` te oogsten is. Dat is de bedoeling: commits en PR's per
werkpakket kunnen optellen zonder dat er aan de poort iets verandert.

## Twee dingen om te weten

**De pagina wordt sinds #1465 vanaf de homepage gelinkt**, met een eigen sectie
en een verwijzing in de voettekst; hij is nog wel uitgesloten van de zoekindex.
Hij staat daarmee in de etalage: wat je erin zet wordt gelezen door iemand die
niet weet hoe het werk ervoor staat. Er staan nog werktitels en lege velden in,
en dat is op zichzelf in orde (zie hierboven), maar een werktitel die je niet
uitgelegd wilt hebben hoort er niet meer in.

Dat hij gelinkt is, telt ook voor de slugs: een URL die van de homepage af te
bereiken is, is een URL die iemand deelt. Hernoem er dus niet lichtvaardig een.

**Er is geen ondersteuning voor meerdere papers.** Het veld heet `paper` en het
anker wordt getoetst aan dat ene paper. Komt er een tweede, dan is dat een
codewijziging, geen inhoudelijke.
