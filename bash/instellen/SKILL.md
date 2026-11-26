---
name: instellen
description: >-
  Stelt DutchQuill AI in en past de instellingen aan. Bij de eerste keer: werkmap kiezen en aanmaken, taal,
  profiel en privacy. Daarna in gewone taal: controles (APA, academische stijl, taal, humaniseren) aan of uit,
  toon (formeel tot luchtig), uitvoerformaten, wat alleen in de chat komt, eigen profielen, eigen templates,
  eigen regels. Gebruik bij /dutchquill:instellen, als DutchQuill nog niet is ingesteld, of als de gebruiker
  iets aan DutchQuill wil veranderen ("zet APA uit", "maak de toon luchtiger", "nieuw profiel voor LinkedIn",
  "voeg mijn huisstijl-template toe", "change my DutchQuill settings").
argument-hint: "[wat je wilt aanpassen]"
---

# DutchQuill instellen

Verzoek van de gebruiker: $ARGUMENTS

Elk `dq`-commando in deze skill draai je via Bash met precies dit voorvoegsel (de plugin-variabelen bestaan
niet als omgevingsvariabele in Bash):

```bash
CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq" <commando>
```

Hieronder staat dat als `DQ <commando>`.

## Huidige stand

!`DQ_NIET_INSTALLEREN=1 CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq" config toon --kort 2>&1 | tail -12 || true`

Staat hierboven een installatiemelding of een fout? Draai dan eerst `DQ doctor` (de eerste keer installeert dq
zijn Python-pakketten, ± 1 minuut) en daarna `DQ config toon --kort`.

## Visueel of in de chat?

Vraagt de gebruiker om "visueel", "de Studio" of "een scherm", of is het de eerste keer en de vraag ligt
open: bied DutchQuill Studio aan (een lokale pagina in de browser, er gaat niets naar internet). In de terminal
werken kan ook. Kiest de gebruiker de Studio:

1. Start hem op de achtergrond (Bash met `run_in_background`): `DQ studio`. De browser opent vanzelf. De eerste
   regel van de uitvoer bevat de URL; noem alleen dat de Studio open staat, niet het token.
2. Zeg dat de gebruiker op "Klaar" klikt als het klaar is. De Studio stopt ook na 15 minuten zonder
   activiteit.
3. Als het achtergrondproces klaar is: lees `${CLAUDE_PLUGIN_DATA}/studio-laatste.json`, draai
   `DQ config toon --kort`, en vat in hooguit vijf regels samen wat er veranderd is.

## A. Eerste keer: werkmap staat op "nog niet ingesteld"

Stel deze vier vragen in één AskUserQuestion. Zet je aanbeveling bovenaan; leg kort uit, geen jargon.

1. **Waar moet je DutchQuill-map komen?** Bureaublad (`~/Desktop/DutchQuill`), Documenten
   (`~/Documents/DutchQuill`), in dit project (`<huidige map>/DutchQuill`). Via "Other" kan de gebruiker een
   eigen pad typen, bijvoorbeeld in een Obsidian-vault of wiki.
2. **Taal:** Nederlands, English, of automatisch (volgt de taal van je materiaal).
3. **Waarvoor gebruik je DutchQuill vooral?** Dat wordt het startprofiel:
   - student: hbo-rapporten, APA, formeel;
   - zakelijk: werkdocumenten en mails;
   - social: posts, informeel;
   - techniek: README's en SOP's.

   Later is alles los aan te passen.
4. **Online taalcheck?** Elke tekst krijgt hoe dan ook een taalronde: Claude leest hem na op d/t, spelling,
   komma's en consistentie. LanguageTool is een extra, automatische controle die meer kleine fouten vangt, maar je
   tekst naar api.languagetool.org stuurt. Nee: alleen de taalronde, en er gaat niets extra naar buiten.
   Aanbeveling: nee voor vertrouwelijk werk (klantstukken, persoonsgegevens); ja als je vooral eigen, openbare
   teksten schrijft en een extra check wilt.

Daarna:

```bash
DQ werkmap init --pad "<pad>" --taal <nl|en|auto> --profiel <profiel> --languagetool <ja|nee>
DQ config toon --kort
```

`init` overschrijft nooit iets. Bestaat de map al, dan vult hij alleen aan.

Vertel de gebruiker in maximaal vijf regels waar de map staat en wat erin hoort:

- materiaal gaat in `1-input` (notities, rapporten, beeld, bronnen);
- een paar eigen teksten in `mijn-stijl`, zodat DutchQuill klinkt als de gebruiker;
- resultaten komen in `2-output`, met versies;
- mails en posts komen gewoon in de chat.

Bij het profiel student: bied aan de titelpaginagegevens nu in te vullen (naam, studentnummer, instelling,
opleiding, docenten). Dat is optioneel. Vul ze in met `DQ config zet student.<veld> "<waarde>"`.

## B. Iets aanpassen

Vertaal het verzoek naar een of meer commando's. Gebruik altijd `DQ config ...`, ook als je de YAML zelf zou
kunnen bewerken: dq bewaart het commentaar en de opmaak van de gebruiker, valideert, en maakt een `.bak`.

| De gebruiker zegt | Commando |
|---|---|
| APA aan of uit | `DQ config zet controles.apa true\|false` |
| academische stijl aan of uit | `DQ config zet controles.academische_stijl true\|false` |
| taal- en spellingscontrole aan of uit | `DQ config zet controles.taalregels true\|false` |
| humaniseren aan of uit | `DQ config zet controles.humaniseren true\|false` |
| formeler, zakelijker, luchtiger | `DQ config zet toon.niveau <formeel\|zakelijk\|neutraal\|informeel\|luchtig>`. "Luchtiger" is één stap op de schaal, tenzij de gebruiker een niveau noemt |
| je of u | `DQ config zet toon.aanspreekvorm <je\|u\|auto\|geen>` |
| een mix ("zakelijk maar met een grapje") | `DQ config zet toon.mix "<tekst>"` |
| bestandsformaten | `DQ config zet uitvoer.formaten "[docx, pdf]"` (docx, pdf, md, txt, html) |
| wat alleen in de chat komt | `DQ config zet uitvoer.chat_voor "[mail, linkedin, social, kort]"` |
| standaardtemplate | `DQ config zet uitvoer.template <naam>` |
| geen versies | `DQ config zet versies false` |
| online taalcheck | `DQ config zet privacy.languagetool true\|false` (zeg erbij dat de tekst dan naar buiten gaat) |
| taal | `DQ config zet taal <nl\|en\|auto>` |
| herinnering gidsen | `DQ config zet bijwerken.herinnering_dagen <7-365>` |
| ander profiel gebruiken | `DQ config profiel kies <naam>`; zie eerst `DQ config profielen` |
| nieuw profiel | `DQ config profiel nieuw <naam> --basis <profiel> --beschrijving "<tekst>"`, daarna `kies` en de afwijkende instellingen zetten |
| profiel weg | `DQ config profiel verwijder <naam>` (alleen eigen profielen) |
| automatisch profiel per soort tekst | `DQ config zet genre_profielen.<genre> <profiel>`. Genres: rapport, onderzoeksrapport, adviesrapport, zakelijk-rapport, technisch-rapport, sop, research-notitie, mail, linkedin, social, readme, memo, kort |

Regels:

- **Profielinstellingen** (controles, toon, uitvoer) gaan naar het actieve profiel. Is dat een meegeleverd
  profiel, dan maakt dq automatisch een eigen kopie `<naam>-eigen` en zet die actief. Zeg dat erbij.
- **Alleen voor dit project:** schrijf `.dutchquill.yaml` in de projectmap met alleen de afwijkende sleutels.
  Toegestaan zijn `werkmap`, `profiel`, `taal`, `controles`, `toon` en `uitvoer`. Daarna `DQ config valideer`.
- **Eigen woorden of huisstijl** ("gebruik nooit 'synergie'", "bedrijfsnaam altijd in hoofdletters"): bewerk
  `eigen-regels.md` in de werkmap met Edit, onder de juiste kop. Niet in de YAML.
- **Eigen template toevoegen:**
  1. Kopieer het bestand (nooit verplaatsen) naar de map `templates/` in de werkmap.
  2. Registreer het: `DQ config zet templates.<naam> "{bestand: templates/<bestand>, soort: docx, beschrijving: <tekst>}"`.
  3. `DQ template check <naam>`: toont welke stijlen er zijn. Stelt het een mapping voor (bijvoorbeeld kop1 naar
     "Kop 1" in een Nederlandse Word), zet die dan met de commando's uit `advies`.
  4. Vraag of het de standaard moet worden (`uitvoer.template`).
- **Opmaak aanpassen** ("koppen in Arial 14 blauw", "ruimere regelafstand", "smallere marges"):
  `DQ template aanpas --van <huidige template> --naar <nieuwe-naam> --stijl kop1.font=Arial --stijl kop1.grootte=14
  --stijl kop1.kleur=1F4E79 [--marge 2] --beschrijving "<tekst>"`. Dat maakt een kopie in `templates/` en
  registreert die; het origineel blijft. Daarna `DQ config zet uitvoer.template <nieuwe-naam>`.
  Sleutels: titel, ondertitel, kop1 tot kop4, normaal, bijschrift, citaat, code. Eigenschappen: font, grootte,
  kleur, vet, cursief, uitlijning, regelafstand, voor, na. Meer dan dit (kop- en voettekst, logo) doet de
  gebruiker in Word in de gekopieerde template.
- **Templates bekijken:** `DQ template lijst`.
- **Werkmap verplaatsen:** maak de nieuwe map met `DQ werkmap init --pad ...`. Inhoud verhuizen doe je pas na een
  expliciete ja van de gebruiker, en dan kopiëren en niet verwijderen.
- **Onduidelijk verzoek:** stel één gerichte vraag. Is het bij twee opties duidelijk welke past, kies die dan en
  zeg welke het werd.
- **Een commando geeft een fout:** lees de melding. Bij "onbekend profiel" of een ongeldige waarde: laat de
  geldige keuzes zien en vraag opnieuw. Probeer niet om de validatie heen te werken.

## C. Afsluiten

1. `DQ config valideer`: moet "Config is geldig." geven.
2. Meld in één tot drie regels wat er veranderd is. Wijk je van de vraag af, zeg dat dan ook (bijvoorbeeld bij
   een automatisch gemaakt `-eigen`-profiel).
3. Staat er een waarschuwing in `DQ config toon --kort` (bijvoorbeeld APA met een luchtige toon), noem die dan
   kort.
