---
name: poc-add
description: Voegt een proof-of-concept toe aan het poc-portaal op poc.regelrecht.rijks.app — register-entry, map-indeling, de subpad-aanpassingen die een losse app nodig heeft om onder /<slug>/ te draaien, en de bedrading in de deploy. Gebruik dit bij "voeg poc X toe", het verhuizen van een losse PoC-repo naar de monorepo, of het aanpassen van status en voorbehoud van een bestaande poc.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Een poc toevoegen

`poc.regelrecht.rijks.app` is één ZAD-component (`poc`) met de pocs erachter,
elk achter een eigen wachtwoord. Dat het één component is, is geen keuze maar
een gevolg: de productie-deployment publiceert op `component.subdomain`, dus
élk component krijgt zijn eigen hostnaam. De routering tussen de pocs gebeurt
daarom binnen één container, in `packages/poc-portal`.

## Waar de inhoud staat

```
pocs/registry.yaml                     het register — de enige bron
corpus-poc/<slug>/                     casus-regelgeving, data, varianten
frontend-poc-<slug>/                   de app (npm-workspace-member)
packages/poc-portal/                   portaal: overzicht, poort, proxy
```

Uit het register volgen de kaarten op het overzicht, de env-var-naam van het
wachtwoord, welke paden geserveerd of doorgestuurd worden, en welke paden het
poc-image raken. Eén regel toevoegen is daarom een echte toevoeging, geen
administratie.

## Kopieer géén bestaande poc-map

Dat is de manier waarop je een halve poc krijgt: je past `slug` en `titel` aan,
vergeet `POC_BASE` in de Dockerfile of het pad in `copy-assets.js`, en de app
laadt zijn wetten uit de map van de buurman. De poort werkt dan gewoon, dus het
valt pas op als iemand de demo geeft. Begin bij het register en werk naar buiten.

## Het register

```yaml
  - slug: mijn-poc                # [a-z0-9-], begint met letter of cijfer
                                  # publiek zichtbaar in de URL
    titel: Wat voor verkenning dit is        # PUBLIEK
    samenvatting: >-                         # PUBLIEK
      Een of twee zinnen: wat voor soort verkenning is dit en waar dient hij
      toe. Geen dossiernaam, geen intern stuk, geen departement.
    titel_intern: Het echte onderwerp        # achter het wachtwoord
    samenvatting_intern: >-                  # achter het wachtwoord
      Waar dit werkelijk over gaat.
    soort: statisch               # statisch | proxy
    bron: poc-mijn-poc            # bij statisch: de npm-workspace
    corpus:
      - corpus-poc/mijn-poc
    assistent: false
    tags: [OCW, bekostiging]      # intern: het departement hoort niet publiek
    status: verkenning            # verkenning | in-ontwikkeling | gevalideerd
    voorbehoud: >-
      Waarom dit nog niet klopt, of waar het overheen loopt.
```

**De overzichtspagina én het inlogscherm zijn publiek.** Het inlogscherm is
bereikbaar door een slug te raden, dus alles wat daarop staat geeft de casus
weg aan wie er langsloopt. Daarom heeft elke poc een publieke helft (`titel`,
`samenvatting`, en de slug in de URL) en een interne helft (`titel_intern`,
`samenvatting_intern`, `tags`, `status`, `voorbehoud`) die pas achter het
wachtwoord te zien is.

Schrijf de publieke tekst zo dat hij klopt zonder te verraden waar het over
gaat: "een verkenning om verschillende regelingen te vergelijken", niet het
dossier, het departement of het stuk waar het uit komt. Laat je de interne
velden weg, dan valt de poc terug op de publieke tekst — dat is goed voor een
casus die niets te verbergen heeft, en fout zodra dat wel zo is. Een test in
`packages/poc-portal/src/pagina.rs` controleert dat geen intern veld op een
publieke pagina belandt, maar die kan niet zien of je de publieke tekst zelf
wel neutraal genoeg hebt geschreven.

`status` en `voorbehoud` zijn **verplicht en hebben geen default**. Een
uitgerekend bedrag ziet er even stellig uit of de regels erachter met juristen
zijn doorgelopen of in een middag zijn geschetst; zonder die twee velden ziet
een nieuwe schets er even betrouwbaar uit als de best nagelopen poc. Schrijf
het voorbehoud in eigen woorden — de vaste huisregel is precies de zin die
iedereen overslaat. Te kort (< 30 tekens) wordt geweigerd bij het opstarten.

Wat de statussen betekenen staat in `pocs/registry.yaml` zelf, boven de lijst.
Kies bij twijfel de lagere: te voorzichtig kost een gesprek, te stellig kost
vertrouwen.

`soort: proxy` is voor een poc met een eigen proces (eigen database, eigen
login). Die draait als eigen ZAD-component zonder `publish-on-web` en is alleen
via het portaal bereikbaar; `upstream` is dan de componentnaam. `assistent: true`
kan alleen bij `statisch` — de assistent draait in het poc-image zelf.

Een proxy-poc draagt zijn voorvoegsel zelf: het portaal stuurt `/napp/...`
ongewijzigd door, dus de app moet zichzelf onder datzelfde pad serveren. Bouw de
frontend met die `base` én laat de backend hem kennen (bij napp
`NAPP_BASE_PATH`). Zet dat voorvoegsel in de **router**, niet in een
middleware-layer die de URI herschrijft: axum matcht het pad vóór de layer
draait, dus zo'n herschrijving komt te laat om nog een andere route te kiezen.
`Router::nest` is het gereedschap; let dan op dat `nest` de kale wortel (`/napp/`)
niet naar de fallback van de genestelde router stuurt.

## Een statische poc onder /<slug>/ krijgen

Een losse app gaat er bijna altijd van uit dat hij op `/` staat. Vier dingen,
in deze volgorde:

1. **`vite.config.js`**: `base: process.env.POC_BASE ?? '/'`. Dat herschrijft
   wat de bundler uitgeeft, en laat `npm run dev` op `/` staan.
2. **De router**: `createWebHistory(import.meta.env.BASE_URL)`.
3. **Elke `fetch()` die de app zelf doet.** Dit is het echte werk en `base`
   dekt het níet: een string in een `fetch()` gaat niet door de bundler. Neem
   `src/basePad.js` over uit frontend-poc-terugbetaalregimes en haal alles op
   met `b('/pad')`. Zoek ze met:

   ```bash
   grep -rn "'/wasm\|'/laws\|'/data/\|'/api/\|location.origin" src/
   ```

   Zit er een web worker in, let dan op `self.location.origin`: dat gooit het
   pad weg. `self.location` is wat je wilt.

   Zit er een centrale fetch-helper in, zet de basis dán daar en niet bij de
   aanroepers — één vergeten aanroeper is een wet die niet laadt, en dat blijkt
   pas in de browser.
4. **De manifesten die de build schrijft.** Staan er wortel-absolute paden in
   de JSON die de app leest, dan herstelt geen enkele config-vlag dat; die
   moeten relatief worden. Let op velden die als *sleutel* worden gebruikt in
   plaats van als URL (in terugbetaalregimes is dat `base` in `variants.json`):
   die moeten bij hun tegenhanger in de index blijven passen.

## Varianten en andere git-afhankelijkheden

Bouwde de app iets op uit git (branches, tags, commit-berichten), dan werkt dat
hier niet: CI heeft die branches niet. Exporteer het één keer naar bestanden
onder `corpus-poc/<slug>/` en laat de build die lezen. Laat de build **hard
vallen** als een genoemd bestand ontbreekt; stil overslaan haalt een kolom of
een scenario weg en dat merkt niemand tot de demo.

## Testpaden

Wijzen de tests naar `../../corpus` of `../../data`, dan wezen die in de losse
repo naar de casus en hier naar het échte regelrecht-corpus. Dat faalt luid
(scenario's over de zorgtoeslag tegen een engine die die wet niet kent), maar
alleen als je de tests draait. Neem `tests/helpers/casusPaden.js` over.

## De bedrading

```bash
just poc-build      # wasm + portaal-assets + elke poc, naar .poc-static/
just poc            # dat plus het portaal op :8611, wachtwoorden 'demo'
npm test -w frontend-poc-<slug>
just check          # deploy-filters-test en dockerfile-consistency-test zitten hierin
```

Met de hand bij te werken, en de reden dat dit een skill is:

- `package.json` (workspaces) en de twee Dockerfiles die de workspace-`npm ci`
  draaien (`frontend/Dockerfile`, `frontend-lawmaking/Dockerfile`): elk
  workspace-member moet daar zijn `package.json` hebben, anders faalt `npm ci`.
- `packages/poc-portal/Dockerfile`: een `COPY` en een `RUN POC_BASE=/<slug>/ npm
  run build -w <workspace>`, plus een `COPY --from=frontend-builder … /app/static/<slug>`.
- `script/deploy-filters.mjs`: de paden van de nieuwe poc bij `poc.paths`.
- `.github/workflows/ci.yml`: het pad in de `ci`-filter, en de testregel in de
  e2e-baan (daar staat de WASM-engine; bij de gewone frontend-tests niet).

Een nieuw ZAD-component is alleen nodig bij `soort: proxy`. Voor een statische
poc verandert er buiten de repo niets.

## Wat Anne zelf draait

Wachtwoorden komen nooit uit een skill en niet uit een transcript. Geef de
regel, laat hem hem draaien:

```bash
zad env add -c poc POC_PW_<SLUG>       # vraagt de waarde interactief
```

`<SLUG>` is de slug in hoofdletters met streepjes als liggende streepjes. Het
portaal weigert te starten als er één ontbreekt — een poc in het register
zonder wachtwoord zou anders voor iedereen open staan, en dat is de verkeerde
kant om die vergissing op te laten vallen.
