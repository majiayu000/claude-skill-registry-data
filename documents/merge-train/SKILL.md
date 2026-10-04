---
name: merge-train
description: Mergt één pull request of een reeks achter elkaar op main, met bijwerken zonder handtekeningverlies, wachten op de juiste checks, en controleren dat de uitrol geslaagd is. Gebruik dit bij "merge PR N", "laat de trein rijden" of het wegwerken van een stapel mergebare PR's.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob
---

# Merge train

Mergt pull requests op `main` binnen de regels die deze repo stelt: trunk-based,
`strict: true`, squash-merge, ondertekende commits.

Twee ingangen, dezelfde lus:

- `merge-train <nummer>`: één pull request.
- `merge-train`: alle mergebare PR's, één voor één, met een verse `main` per ronde.

## Waarom dit een lus is en geen lijstje

`strict: true` betekent dat een PR bij moet zijn met `main` voordat hij mag
mergen. Elke merge zet daarmee elke andere openstaande PR op achterstand. Je kunt
dus niet vooraf bepalen welke PR's mergebaar zijn en die lijst afwerken: na
iedere merge is de vraag opnieuw.

Werk daarom altijd één PR tegelijk af en begin elke ronde bij een verse
`origin/main`. Bundel nooit meerdere PR's in één branch om cycli te sparen. Dat
is eerder geprobeerd (PR 1205): één rode test legde de hele bundel stil en de
attributie per PR verdween in de squash.

## Vaste regels

**Handtekeningen.** `required_signatures` staat aan. Zet nooit `user.name`,
`user.email` of een `GIT_AUTHOR_*`/`GIT_COMMITTER_*`-variabele; git haalt die uit
`~/.gitconfig` en een ander adres maakt de handtekening onherleidbaar, waardoor
de merge blokkeert.

**Bijwerken doe je met de merge-variant, niet met rebase.**

```bash
gh api --method PUT repos/MinBZK/regelrecht/pulls/<nr>/update-branch
```

Die zet er een merge-commit bovenop die GitHub zelf tekent, dus de branch blijft
`verified`. `gh pr update-branch --rebase` schrijft de commits opnieuw en tekent
het resultaat níét; een ondertekende branch wordt dan `unsigned` en strandt op
`required_signatures`. Squash-merge platst die merge-commits alsnog, dus `main`
houdt een vlakke historie.

**Wat een mens hoort te beoordelen gaat nooit automatisch mee.** Deze repo kent
nul verplichte reviewers, dus een merge door deze skill is de enige beoordeling
die een wijziging krijgt. Voor drie soorten is dat niet genoeg, en die sla je
over, ook als ze groen zijn:

- `corpus/regulation/**` en `schema/**`. Dit is de machine-leesbare weergave van
  Nederlandse wetgeving en het schema waar die aan hangt. Een fout hier levert
  een verkeerde rechtsuitkomst op, en geen enkele poort in CI ziet dat.
- `.github/workflows/**`. Wie de workflows wijzigt kan de poorten wijzigen
  waarop deze skill zelf afgaat. Dit geldt voor elk bestand onder dat pad, wat
  de workflow ook doet en hoe ver hij ook van de merge-poorten af staat. Zie je
  een uitzondering, dan is die uitzondering geen besluit maar een melding: sla
  de PR over en zeg erbij welke workflow het is en waarom je dacht dat hij
  erbuiten viel. Dat is eerder misgegaan: op 8 augustus 2026 ging PR 1219 mee
  omdat er onder dat pad maar één bestand geraakt werd, `scheduled-cleanup.yml`,
  en dat had voorgelegd moeten worden.
- RFC's, rapporten en substantieel proza onder `docs/src/content/rfcs/`.

Meld ze aan het eind als klaar en wachtend op een oordeel.

**Blijf van andermans werk af.** Fork-PR's en PR's van externe bijdragers merge
je niet; die liggen bij hun auteur.

## Lus

### 1. Verse main en de kandidatenlijst

```bash
git fetch origin main
gh pr list -R MinBZK/regelrecht --state open --limit 200 \
  --json number,title,isDraft,mergeStateStatus,author,headRefName
```

Kandidaat is een PR die niet in draft staat, van `ehotting` of een teamlid is, en
`mergeStateStatus` heeft van `CLEAN`, `BEHIND` of `BLOCKED`. `DIRTY` betekent een
echt conflict: overslaan en melden. Elke andere waarde, `UNKNOWN` voorop, is geen
oordeel maar een nog niet berekende mergeability: vraag hem opnieuw op, en blijft
hij anders dan die vier, sla dan over.

PR's van `dependabot[bot]` horen niet in de trein. Die lopen via de `dependabot`-
skill en `claude-dependabot.yml`, en de reviewpoort staat er groen zonder dat er
een review is geweest, want `claude-review` slaat dependabot over.

Welke bestanden een PR raakt staat niet in die lijst, en zonder die bestanden kun
je de uitsluitingen uit "Vaste regels" niet toepassen. Haal ze per kandidaat op:

```bash
gh pr diff <nr> -R MinBZK/regelrecht --name-only
```

Raakt er ook maar één pad `corpus/regulation/**`, `schema/**`,
`.github/workflows/**` of `docs/src/content/rfcs/**`, dan valt de PR af. Doe die
toets hier, vóór je er tijd in steekt, en niet pas bij het mergen.

Kies er één. Bij gelijke geschiktheid: de kleinste diff eerst, want die is het
snelst door de poort en zet de rest het minst op achterstand.

### 2. Bijwerken als hij achterloopt

Stel eerst vast dát hij achterloopt. `update-branch` op een branch die al bij is
geeft een fout, en die fout lijkt op de fout bij een conflict:

```bash
gh api repos/MinBZK/regelrecht/compare/main...<headRefName> --jq .behind_by
```

Is die `0`, sla deze stap dan over. Anders:

```bash
gh api --method PUT repos/MinBZK/regelrecht/pulls/<nr>/update-branch
```

Wacht daarna tot de nieuwe checks starten. Werkt de aanroep niet terwijl
`behind_by` groter dan nul was, dan is het een `DIRTY`-geval: overslaan en
melden.

### 3. Wachten op de juiste checks

Verplicht op `main` zijn:

```
Pre-commit, WASM Build, Protect schema versions, Security Audit,
Test, Validate PR title, Claude review completed
```

`Test` is een verzamelpoort: daarachter hangen `rust-tests`, `bdd-conformance`,
`frontend-tests`, `e2e`, `cross-law-integrity`, `provenance-checks`,
`docs-a11y`, `rust-image` en `changes`. Je hoeft die niet apart af te wachten;
groen op `Test` dekt ze.

Wacht op precies deze zeven en op niets anders.

```bash
gh pr checks <nr> -R MinBZK/regelrecht
```

Die aanroep rapporteert over de actuele head-SHA, wat na een `update-branch` uit
stap 2 een andere is dan daarvoor. Lees nooit een check-run van een oudere SHA.

`Claude review completed` bewaakt dat de review gedraaid heeft, niet wat eruit
kwam. Groen zegt dus niets over de bevindingen. Die lees je zelf zodra de check
klaar is en vóór je merget, en een 🔴 Critical stopt de trein ook als alles groen
staat; dat staat onder "Reviewbevindingen". Issue #1248 stelt voor de check ook
rood te laten worden op een Critical, als tweede net onder het lezen.

- `Build and Deploy` is `skipped` zonder het `deploy:preview`-label. Dat is geen fout.
- `CodeQL` en `Analyze (…)` rapporteren niet op een PR die alleen docs raakt.
  Nooit op wachten; ze zijn niet verplicht.
- `Mutation Testing (diff)` draait alleen bij een wijziging in
  `packages/engine/**` of `packages/pipeline/**`. Hij is niet verplicht, maar
  rood betekent een ongetest codepad: niet mergen.

Reken op ongeveer zes minuten voor CI en tien voor de review; onder belasting
loopt CI op tot een kwartier. Poll rustig, niet elke tien seconden.

### 4. Mergen

De bevindingen uit de review beoordeel je vóór deze stap, niet erna. De afweging
onder "Reviewbevindingen" gaat over de vraag of deze PR wel mag, en terugdraaien
kan daarna alleen met een revert-PR die zelf weer een ronde door de trein moet.

```bash
gh pr merge <nr> -R MinBZK/regelrecht --squash
```

Main mergt via een merge queue, dus dit zet de PR in de rij en mergt hem niet
meteen. `--delete-branch` weigert gh zolang de rij aanstaat. Hoe je nagaat dat
hij in de rij staat, en hoe je een uitval ziet (de PR blijft dan gewoon
`OPEN`), staat in AGENTS.md onder "Een pull request door de rij halen". Wacht
met stap 5 tot hij echt gemerged is.

Squash is de enige toegestane methode in deze repo. De titel is de commit-titel,
dus die moet aan Conventional Commits voldoen; `Validate PR title` bewaakt dat al.

### 5. De deploy controleren, niet de CI-herhaling

Wacht **niet** op de CI-run van de nieuwe `main`-commit. Met `strict: true` is de
boom die op main landt identiek aan wat de PR net getest heeft, dus die run is
een herhaling. Daar kan alleen nog iets flaky of tijdsafhankelijks omvallen, een
nieuwe advisory die `Security Audit` raakt bijvoorbeeld, en dat blokkeert de
volgende PR toch al, want dat is een verplichte check.

Controleer in plaats daarvan de uitrol, want daar bestaat geen PR-check voor.
Zoek de `Build and Deploy`-run van de nieuwe `main`-commit op en lees de banen
eruit:

```bash
git fetch origin main && git rev-parse origin/main
gh run list -R MinBZK/regelrecht --workflow "Build and Deploy" \
  --commit <sha> --json databaseId,status,conclusion
gh api repos/MinBZK/regelrecht/actions/runs/<id>/jobs \
  --jq '.jobs[] | "\(.name)\t\(.conclusion)"'
```

De run bestaat vlak na de merge nog niet, en `Wacht op een groene CI` houdt hem
tot twintig minuten op omdat die baan wacht tot de CI van deze commit groen is.
Een lege runlijst of een `conclusion` van `null` betekent dus "nog bezig", niet
"niets uitgerold". Poll tot `deploy-production` een conclusion heeft.

Beoordeel dan die baan, en niet de run als geheel:

- `success`: uitgerold, ga door.
- `failure` of `cancelled`: **stop de trein** en meld het; de volgende merge zet
  er alleen maar meer bovenop.
- `skipped`: er is niets uitgerold, en dat kan twee dingen betekenen. Staan zowel
  `changes` als `Wacht op een groene CI` op `success` en heeft geen enkele
  build-baan gedraaid, dan raakte deze commit geen deploybaar component en is de
  skip in orde. In elk ander geval is er iets vóór de builds omgevallen, meestal
  de CI op main, en is er niets uitgerold. Dat is een stopgrond, geen groen.

De skip is de gevaarlijke uitkomst: overgeslagen is niet rood, dus een
oppervlakkige blik op de run ziet er niets aan. Kun je de twee gevallen niet uit
elkaar houden, stop dan en meld wat je zag.

`deploy-production` kan ook door ZAD opzij worden gezet voor een nieuwere taak op
hetzelfde deployment; zie "Bekende ruis".

### 6. Terug naar stap 1

Verse `origin/main` ophalen en opnieuw beginnen. Verifieer voor elke volgende
merge dat de gekozen PR bij is met `main`:

```bash
gh api repos/MinBZK/regelrecht/compare/main...<headRefName> --jq .behind_by
```

`behind_by` staat niet in `gh pr list` of `gh pr view`; die kennen alleen
`mergeStateStatus`, en `BEHIND` is daar de grovere variant van hetzelfde. Is de
uitkomst niet `0`, dan eerst stap 2.

## Reviewbevindingen

De review deelt in drie: 🔴 Critical (verkeerde rechtsuitkomst, dataverlies,
crash, beveiligingslek), 🟠 Significant (waarschijnlijke bug, kapotte verwijzing,
gemist randgeval) en 🟡 Minor (codekwaliteit, stijl). De schaal staat in
`REVIEW.md`; de bolletjes komen uit de prompt in `claude-code-review.yml` en niet
uit `REVIEW.md`, dus zoek daar niet naar de markering zelf.

De bevindingen staan op twee plekken: een sticky comment op de PR en losse
inline comments bij de regels.

```bash
gh pr view <nr> -R MinBZK/regelrecht --json comments --jq '.comments[].body'
gh api repos/MinBZK/regelrecht/pulls/<nr>/comments --jq '.[].body'
```

Lees ze pas als `Claude review completed` klaar is. Elke nieuwe review-run wist
de vorige comments en schrijft ze opnieuw, dus wat je tijdens het draaien leest
is de vorige ronde, en nul comments betekent dan niets.

**Critical.** Merge niet. Stop de trein en meld wat er staat; repareren hoort
niet bij deze skill. Ga hier niet af op de kleur van `Claude review completed`:
die check staat groen zodra de review gedraaid heeft, ook met een 🔴 eronder. Dat
is op 8 augustus 2026 misgegaan bij PR 1234, die drieëntwintig seconden na een
kritieke bevinding gemerged werd.

**Significant.** Die blokkeert niet, en dat is opzet: "waarschijnlijk" zit in de
definitie, dus vals-positieven zijn er genoeg. Doorgeven zonder oordeel is
daarom geen melding maar een beslispunt zonder grond. Beoordeel hem zelf, aan de
code en niet aan de tekst van de review:

- Klopt hij? Lees de regels die hij aanwijst, in het hele bestand en niet alleen
  in de diff, en ga na of het beschreven pad bereikbaar is.
- Welk gedrag verandert erdoor, en wie merkt dat.
- Hoe duur is het als hij blijft staan? Landt er een fout in productie die geen
  poort ziet, of gaat het om een pad dat niemand loopt.

Beslis daarna zelf en voer die beslissing uit: mergen, of overslaan tot de
bevinding gerepareerd is. Kom je er niet uit, neem dan aan dat hij klopt en sla
over; dat is de goedkoopste van de twee vergissingen. Raakt de bevinding
`corpus/regulation/**`, `schema/**`, `.github/workflows/**` of
`docs/src/content/rfcs/**`, dan hoorde die PR sowieso al niet in de trein.

Beide takken laten iets achter, want anders beoordeelt de volgende ronde
dezelfde bevinding opnieuw en misschien anders. Bij mergen maak je een issue aan
met de bevinding en de PR erin; bij overslaan zet je hem als comment op de PR.

Meld per bevinding één alinea: wat hij zegt, of hij klopt, wat het kost, wat jij
gedaan hebt en waarom. Zo bevestigt of draait Eelco jouw beslissing om zonder
zelf in de diff te hoeven duiken.

**Minor** vermeld je niet apart.

## Wanneer je stopt

- De productie-deploy van de vorige merge is mislukt.
- Een PR heeft een echt conflict (`DIRTY`).
- Een required check faalt inhoudelijk. Repareren hoort niet bij deze skill;
  meld welke check op welke PR en wat het log zegt.
- De review meldt een 🔴 Critical. Dat is een zelfstandige stopgrond, ook als
  `Claude review completed` groen staat; die check zegt alleen dat de review
  gedraaid heeft. Zie "Reviewbevindingen".

## Wat je aan het eind meldt

Per PR één regel: nummer, titel, en wat ermee gebeurd is. Daarachter de
overgeslagen PR's met de reden. Geen samenvatting van de inhoud van wat er
gemerged is; dat staat in de PR's zelf.

Uitzondering: een Significant-bevinding krijgt de alinea uit
"Reviewbevindingen", met jouw oordeel en wat je gedaan hebt.

## Bekende ruis

Een gefaalde `deploy-preview` of `deploy-production` met `"status": "superseded"`
in de JSON betekent dat ZAD de taak opzij heeft gezet voor een nieuwere taak op
hetzelfde deployment. Het werk is dan gedaan; alleen die job opnieuw draaien
volstaat.

Twee check-runs met dezelfde naam op één commit kan: twee PR's kunnen dezelfde
head-SHA delen. De nieuwste telt.
