---
name: walkthrough
description: Begeleidt het opnemen, nabewerken en publiceren van de opgenomen rondleiding door de demo (/rondleiding) met de `just walkthrough`-commando's. Gebruik dit bij "ik heb een opname gemaakt", "neem hoofdstuk X opnieuw op", "zet de rondleiding op de preview", vragen over knippen, ondertitels, diateksten, de stemkloon of FAQ-antwoorden, en wanneer de replay iets niet goed nadoet (een klik, een scroll).
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# De opgenomen rondleiding

De rondleiding is geen video: het is de stem van de presentator, en terwijl
die speelt doet de echte demo na wat hij deed. Hoe dat werkt staat in
`docs/src/content/docs/components/demo.md` (sectie *The recorded
walkthrough*); dit bestand zegt hoe je ermee werkt.

Wat waar staat:

| Wat | Waar | In git |
|---|---|---|
| ruwe opnames (beeld, stem, camera, eventlog) | `.walkthrough/takes/<take>/` | nee |
| wat de kijker ziet: segmenten, knippen, diateksten, vragen | `corpus/demo/walkthrough/walkthrough.yaml` | ja |
| het resultaat: tijdlijn en ondertitels | `corpus/demo/walkthrough/timeline.json`, `*.vtt` | ja |
| de media (stem, camera) | GitHub-release `walkthrough-<datum>` | release, openbaar |

## De commando's

```bash
just walkthrough record            # dev-server met recorder + Chrome op /presentatie?record
just walkthrough prepare <take>    # ingest, stem schoon, transcript, nakijken, knipvoorstel, gezicht
just walkthrough check <take>      # luidheid, oversturing, ruis, tempo, handelingen: oordeel per regel
just walkthrough transcript <take|main>   # de tekst per dia
just walkthrough build             # walkthrough.yaml -> media, timeline.json, ondertitels
just walkthrough subtitles         # kortere ondertitels voor wat gezegd is (daarna weer build)
just walkthrough verify            # elk hoofdstuk headless terugspelen; meldt gemiste handelingen (ook in CI)
just walkthrough anchors           # scrollankers meten voor opnames van vóór de ankers
just walkthrough states            # de demostand vastleggen bij achteraf toegevoegde hoofdstukken
just walkthrough publish <tag>     # media naar een GitHub-release (openbaar)
just walkthrough test              # de pytest-suite van de pijplijn
```

`verify` start zelf een dev-server en haalt de stem uit de release; het is
hetzelfde commando dat CI draait in de job **Rondleiding speelt terug**, bij
elke wijziging aan de demo, het demo-corpus of de engine. `anchors` heeft de
dev-server nodig op `127.0.0.1:7400` (`just walkthrough record` start hem).
Draai na elke `build` ook `node frontend-demo/scripts/copy-demo-corpus.mjs`
als je in de browser kijkt, anders speelt de dev-server een oude kopie van de
tijdlijn af.

## Na een opname

1. **De nieuwste take**: `ls -t .walkthrough/takes | head -1`. Kijk in
   `meta.json` naar `startSlide` en in `events.json` naar de dia's en het
   aantal scrolls: dan weet je wat er is opgenomen.
2. **`prepare` en `check` meteen.** Een slechte opname doe je opnieuw
   terwijl alles nog klaarstaat. `check` onder -35 LUFS: invoervolume hoger
   (de microfoontest in het paneel). `prepare` met large-v3 duurt bij 12
   minuten opname ongeveer 10 minuten; draai hem op de achtergrond.
3. **Lees het transcript per dia** en beoordeel inhoud, tempo en de
   overgangen tussen dia's. Een verspreking die de presentator zelf
   herstelt ("zorgverzekerden, sorry, verzekerden") wordt een knip.
4. **Knippen** in `takes.<take>.cuts` van `walkthrough.yaml`. Neem de
   stiltes uit `cuts.suggested.yaml` over; voeg zelf toe wat het voorstel
   niet ziet (zoeken, versprekingen, het einde na de laatste zin). Zoek de
   tijden op woordniveau op: knip tussen woorden, nooit erdoor. `build`
   weigert een knip door een typreeks; schuif hem dan tot vóór het typen.
5. **`build`, dan `verify`.** Nul gemist in beide vensterformaten, anders
   is de rondleiding niet af.

## Een hoofdstuk opnieuw

Een hertake begint bij **Beginnen bij dia N** met **Demostaat terugzetten**
aan, en eindigt met `Shift+R` op het moment dat de presentator doorklikt.
In `walkthrough.yaml` wordt het dan:

```yaml
main:
  segments:
    - take: <oud>       # tot vlak vóór het hoofdstuk
      to: 149.6
    - take: <nieuw>     # het nieuwe hoofdstuk
      from: 2.3
      to: 141.6
    - take: <oud>       # verder waar het nieuwe ophoudt
      from: 314.05
```

- **Knip op zinsgrenzen, niet op het dia-moment.** De presentator praat
  vaak door over een diawissel ("En we beginnen deze demo helemaal aan |
  de achterkant"). Kies het einde van de laatste hele zin vóór de wissel,
  en bij terugkeer het begin van een zin die aansluit op wat de hertake
  als laatste zegt.
- Een stuk dat terugkeert naar een opname begint in de staat van die
  opname bij de dia waar het stuk start; de handelingen tussen die dia en
  het knippunt worden snel nagespeeld. Dat gaat vanzelf goed.

## Wat de replay niet nadoet

Faalt **Rondleiding speelt terug** in CI op een PR die de demo wijzigt, dan
heeft die wijziging iets weggehaald of hernoemd waar de opname op klikt. De
annotatie noemt het hoofdstuk. Eerst de vraag of de wijziging de bedoeling
was: zo niet, herstel de demo; zo wel, dan moet dat hoofdstuk opnieuw
worden opgenomen (en tot die tijd kan de PR niet door de poort). Een
waarschuwing "vond alleen losser" faalt niet, maar bekijk het: een knop die
nu "Wetten, 81" heet is onschuldig, een ander element met dezelfde woorden
niet.

- **Een gemiste klik** (`verify` meldt hem): kijk in `events.json` naar
  het `target`. Een id met een uuid erin of een teller wordt al genegeerd
  (`generatedId` in `locator.js`); een tekst die per corpus verschilt
  wordt na de halve wachttijd losser gezocht. Is het iets anders, repareer
  dan de locator, niet de opname.
- **Een scroll die op de verkeerde plek landt**: een scroll draagt een
  `anchor` (de regel die midden in beeld stond). Heeft hij er geen, dan
  is de opname van vóór de ankers: `just walkthrough anchors`, dan
  opnieuw `build`.
- **Een scroll die helemaal ontbreekt** (geen `scroll`-events in dat stuk
  van `events.json`): die is niet opgenomen, en dat is niet te herstellen.
  Dat hoofdstuk moet opnieuw. Opnames van vóór 3 oktober 2026 missen de
  scrolls binnen panelen van het ontwerpsysteem.

## Het dek stond uit, of de opname begon halverwege

- **Geen dia's in een deel van de opname** (`dia's` in `check` houdt eerder
  op dan de opname, of er staan `deck`-events met `active: false` in
  `events.json`): de presentator zette het dek uit en liep via de tabbladen
  verder. Dat is geen reden om opnieuw op te nemen. Leid de overgangen af uit
  het transcript en de tabwissels en geef dat deel achteraf hoofdstukken:
  ```yaml
  takes:
    <take>:
      chapters:
        - at: 842.1            # take-tijd, vlak voor de zin die het onderdeel opent
          overline: De burger
          title: Eén burger, Merijn
          lead: Alles waar Merijn recht op heeft, berekend door de wet zelf.
          bullets: [...]
          route: /portaal      # het tabblad; zonder `route` dat van de laatste tabwissel
        - at: 1270.4
          kind: closing        # een dia zonder tabblad, voor de afsluiting
          title: Van wet naar digitale werking
  ```
  Daarna `build`, dan `just walkthrough states` (dev-server aan; speelt de
  rondleiding één keer in echte tijd af en legt per hoofdstuk de stand van
  de demo vast, zodat een sprong ernaartoe direct is), dan opnieuw `build`.
  `states` opnieuw draaien na elke wijziging aan knippen of hoofdstukken
  vóór dat deel.
- **De opname begint met iets dat al gedaan was** (een scenario dat al
  uitgevoerd was, een paneel dat al openstond; `verify` mist dan de eerste
  klik): de staat van een tabblad zit niet in de demostand. Zet de
  ontbrekende handelingen erbij onder `actions:` van de opname, met `at`,
  `type`, `fx`/`fy` en het `target` zoals `events.json` het voor zo'n klik
  noteert. Kijk in `app.cfr.mp4` hoe het scherm er bij het begin uitzag.

## Pauzes en tussenzinnen

- **Pauzes**: zegt de presentator "kijk gerust even zelf rond", "klik zelf
  even rond", "probeer het zelf" of "ga je gang", dan stopt de speler aan het
  eind van die zin met een coach mark bij de afspeelknop. Dat vindt `build`
  vanzelf (`INVITATIONS` in `timeline.py`). Bijsturen in `walkthrough.yaml`:
  ```yaml
  pauses:
    - {take: <take>, at: 330.2, hint: Klik op een wet in de graaf.}  # erbij
    - {take: <take>, at: 512.0, off: true}                           # weg
  takes:
    <take>:
      auto_pauses: false   # niets automatisch in deze opname
  ```
  Controleer na een build of `main.pauses` in `timeline.json` klopt. Zegt de
  presentator na de uitnodiging nog iets ("dan gaan we zo weer verder"), zet
  de gevonden pauze dan uit en een nieuwe na die zin. Lees ook het hele
  transcript na op uitnodigingen in andere woorden ("voel je vrij om hier
  rond te kijken"); die vindt de build niet.
- **Tussenzinnen** (bumpers): korte stukjes uit een opname in de eigen stem,
  gezegd als de kijker zelf gaat klikken (`wait`) en als hij verder drukt
  (`resume`). Neem ze op in een losse take ("Ga je gang, kijk maar even rond,
  ik wacht." en "Oké, we gaan verder.", 2-3 varianten), zoek de tijden op
  woordniveau en zet ze in:
  ```yaml
  bumpers:
    wait:
      - {take: <take>, from: 1.2, to: 3.9}
    resume:
      - {take: <take>, from: 6.0, to: 7.4}
  ```
  Ze gaan mee in `publish`.

## Transcript en diateksten

- Het transcript wordt bij `prepare` nagekeken door een taalmodel met de
  schermbeelden erbij (`corrected.txt` in de take). Klopt er toch een
  woord niet, verbeter dan `corrected.txt`; geen lijst met vaste fixes.
- **Ondertitels** zijn ingekorte spreektaal: na een `build` maakt
  `just walkthrough subtitles` een korte versie van elke ondertitel die er
  nog geen heeft, in `corpus/demo/walkthrough/subtitles.yaml` (`gezegd` ->
  `ondertitel`); dan opnieuw `build`. Lees de nieuwe na en verbeter met de
  hand wat niet loopt; betekenis, begrippen en getallen moeten kloppen.
- De dia's van de rondleiding zijn die van het moment van opnemen.
  Pas ze aan in `slides:` van `walkthrough.yaml`, per dia-index, **kort**,
  en zo dat ze volgen wat er gezegd wordt. De zaal-deck in
  `corpus/demo/demo-config.yaml` blijft daarbuiten.

## Publiceren

- `publish` zet de media in een **openbare** GitHub-release, met stem en
  gezicht. Vraag het de presentator de eerste keer per tag; daarna voegt
  een publish aan dezelfde tag alleen bestanden toe.
- Commit daarna `walkthrough.yaml`, `subtitles.yaml`, `timeline.json` en de `.vtt`'s;
  stage een verdwenen `.vtt` mee. Nooit committen: lokale testconfiguraties
  en `corpus/demo/walkthrough/script/` met proefscripts.
- Met het label `deploy:preview` op de PR haalt de preview de media uit de
  release.

## Werken met de presentator

- Test in een headless Chrome met `--mute-audio`. Een stem die opeens door
  iemands vergadering klinkt is geen testresultaat.
- Geef bij elke opnamesessie de stappen genummerd, met het spiekbriefje
  voor wat er gezegd wordt, en zeg na elke take binnen een paar minuten of
  hij bruikbaar is.
