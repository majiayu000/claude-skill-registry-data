---
name: plan-milestone
description: >-
  Naplánuje milestone po vlnách — vyzpovídá hrubý rozsah, pro každou položku
  backlogu ověří, jestli v repozitáři existuje precedent k rozšíření, a jen
  z takových sepíše Zadání s kritérii ukotvenými v konkrétním souboru či
  vzoru v kódu, ne v próze dokumentu. Položky bez precedentu se v tomhle
  běhu nezakládají jako issue — zůstávají v backlogu na příští vlnu, až
  vznikne vzor, který rozšíří. Po potvrzení uživatelem založí chybějící
  labely, milestone (nebo do něj přidá další vlnu) a issues sekvenčně, aby
  odkazy na závislosti mířily na skutečná čísla.
when_to_use: >-
  Použij, když má z tématu vzniknout rozepsaný milestone — „naplánuj
  milestone", „rozepiš to na issues", „uděláme UI kit, připrav k tomu úkoly" —
  i tehdy, když uživatel popisuje větší práci, kterou je potřeba rozdělit
  a založit v trackeru, nebo když se má do existujícího milestonu přidat
  další vlna Zadání. Nepoužívej pro jediný ad hoc issue mimo milestone,
  na to slouží file-issue; ani pro posouzení už hotového plánu, to dělá
  review-milestone; ani pro implementaci naplánovaných issues, tu řídí
  run-milestone; ani pro záznam architektonického rozhodnutí i s alternativami
  a důsledky, na to je write-adr; nemá-li jednotlivé issue kritéria ukotvená
  v kódu mimo běh plánování, to řeší triage-issue samostatně. Bez projektové
  konfigurace workflow skill nezakládá nic a odkáže na init-workflow.
argument-hint: "[téma milestonu, nebo název existujícího milestonu k rozšíření]"
model: opus
effort: high
# Zařazení dle matice: strategie / koncepční návrh → opus × high, bez odchylky.
# Nikoli sonnet: rozsah milestonu a klasifikace backlogu se špatně vrací zpět —
# špatně odhadnutá vlna se projeví až o dvě fáze dál, při implementaci, a test
# precedentu v kroku 3 je úsudek nad kódem, ne mechanické porovnání. Nikoli
# xhigh: skill sám neimplementuje ani neorchestruje víc fází, jen klasifikuje
# backlog a sepisuje draft; exekuci vlastní run-milestone. Těžiště je jeden
# rozmyšlený návrh se dvěma brzdami u uživatele.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - AskUserQuestion
  - ToolSearch
  - "Bash(bash:*)"
  - mcp__gitea__label_read
  - mcp__gitea__label_write
  - mcp__gitea__milestone_read
  - mcp__gitea__milestone_write
  - mcp__gitea__issue_read
  - mcp__gitea__issue_write
  - mcp__gitea__list_issues
# Bash je zúžený na spouštění skriptů; git ani gh se nikdy nevolá přímo.
# Proto každé volání píš ve tvaru `bash <cesta>` — jinak nespadne do povolení.
# Glob/Grep hledají precedent v kódu pro klasifikaci backlogu (krok 3), stejný
# test jako v triage-issue, sdílený přes shared/precedent-test.md.
# ToolSearch a nástroje mcp__gitea__* jsou tu kvůli Gitea větvi: jsou odložené
# a bez ToolSearch se nenačtou, bez uvedení v tomto výčtu se nezavolají. Názvy
# odpovídají tvaru, který předepisuje forge-recipes.md; běží-li v projektu
# Gitea MCP pod jiným prefixem, zápis do trackeru neproběhne — ohlas to a nech
# uživatele rozhodnout, výčet neobcházej. `issue_read` a `list_issues` postup
# potřebuje při dohledávání rozepsaného milestonu po přerušeném běhu a při
# výpisu existujících issues, když tahle vlna rozšiřuje už založený milestone
# (krok 2); ve výčtu jsou proto, že je nese tentýž řádek receptu — je to cena
# za jediné volání ToolSearch místo dvou, a obojí je read-only.
# Write slouží výhradně dočasnému souboru s tělem issue, které GitHub skripty
# berou přes --body-file. Edit chybí záměrně: skill nikdy nedopisuje cizí
# dokumentaci (viz krok 4), a bez Edit to není jen slib v próze.
# Vynechaná zvažovaná pole: disable-model-invocation — skill je užitečný i když
# si ho model vyvolá sám z popisu větší rozdělené práce, a do trackeru nesáhne
# dřív než po potvrzení v kroku 6; context/agent/background — interview
# i potvrzení draftu vyžadují uživatele v hlavním kontextu, fork ani běh
# na pozadí nemají komu klást otázky; paths — spouští se z konverzace nad
# tématem, ne prací nad konkrétními soubory; shell — skripty se spouští
# explicitním `bash`; disallowed-tools — allowed-tools je uzavřený výčet, není
# co zakazovat navíc; version/license — verzuje se celý plugin, ne jednotlivý
# skill.
---

# Plan Milestone

Cílem je milestone, jehož issues jde implementovat bez doptávání: každé
kritérium je pozorovatelné chování ukotvené v konkrétním souboru nebo vzoru
v kódu, který issue rozšiřuje. Milestone smí legitimně vzniknout s jen částí
zamýšleného backlogu — položky bez precedentu čekají na příští vlnu, ne na
kritérium vymyšlené narychlo. Závazným kontraktem jsou sdílené soubory
pluginu — při rozporu s tímhle postupem platí ony.

| Soubor | Kdy ho otevři |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` | V kroku 1, když projektová konfigurace chybí nebo v ní nenajdeš sekci, kterou potřebuješ |
| `${CLAUDE_PLUGIN_ROOT}/shared/precedent-test.md` | V kroku 3, dřív než začneš klasifikovat backlog |
| `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` | V kroku 4, dřív než napíšeš první název a první kritérium |
| `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` | V kroku 2, rozšiřuješ-li existující milestone, jinak v kroku 5 — než poprvé sáhneš na tracker, včetně sekce s nástrahami |
| `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` | Stejně jako recepty — v kroku 2 nebo v kroku 5, na GitHub projektech dřív než složíš první volání skriptu: nese povinné argumenty i význam návratových kódů |

Obsah sdílených souborů si **přečti, ale nepřepisuj do odpovědi**. Šablona issue se
mění na jednom místě; kopie v konverzaci zastará a milestone pak nese dva různé tvary.

## Vstupní kontext

- Téma milestonu, nebo název existujícího milestonu k rozšíření (může být prázdné): $ARGUMENTS

Prázdné zadání znamená, že téma vytěžíš z konverzace. Nemáš-li ani z čeho vytěžit,
zeptej se na téma dřív, než začneš cokoli číst — interview rozsahu bez tématu nemá
co ověřovat.

**Skill je interaktivní.** Selže-li volání AskUserQuestion nebo odpověď nedorazí,
**nezakládej nic**: vypiš draft do konverzace, řekni, na co potřebuješ odpověď,
a skonči. Rozepsaný milestone se z trackeru uklízí ručně, kdežto neodeslaný draft
nestojí nic.

## Postup

### 1. Načti projektovou konfiguraci

Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni cílového
projektu. Potřebuješ z ní podsekce **Forge** (kterou větev receptů použít),
**Labely** (co smíš nasadit) a **Jazyk issues**. Podsekci **Zdroje pravdy**,
existuje-li, si drž po ruce pro krok 4 — ne k ukotvení kritérií (to teď dělá
kód), ale kvůli chráněným rozhodnutím z ADR, na která si má autor Zadání dát
pozor.

- **`CONTRIBUTING.md` neexistuje nebo sekci nemá** → nepokračuj a nedomýšlej si
  hodnoty. Řekni uživateli, že projekt nemá workflow konfiguraci, a nabídni
  `/sagittaras:init-workflow`.
- **Chybí podsekce, kterou potřebuješ** → řekni která a nabídni doplnění; sám ji
  za pochodu nedoplňuj. Odhadnutá taxonomie labelů rozbije routing v `run-milestone`
  a pozná se to až u review.

### 2. Sestav hrubý rozsah

Nástrojem AskUserQuestion vytyč hranice milestonu: co je uvnitř a co se odkládá.
**Rozsah nedomýšlej** — „jen kostra" a „kostra + první funkce" jsou dva různé plány
a rozdíl mezi nimi je několik issues a týden práce.

U každé varianty uveď **doporučení a vysvětlený kompromis** — co se získá a co se tím
odloží. Varianta bez ceny vypadá jako zadarmo a uživatel pak schválí rozsah, který
odsouhlasit nechtěl.

Ptej se po kolech, dokud neumíš vyjmenovat **backlog** — položky práce v rozsahu —
a podle čeho se pozná, že je milestone jako celek hotový. Backlog je zatím jen
seznam záměrů, ne issues; issue vznikne až těm položkám, které projdou krokem 3.

**Rozšiřuješ existující milestone** (zadání jmenuje jeho název) → backlog dopočítej
proti tomu, co v něm už je. Otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`
— tenhle krok totiž jako první sahá na tracker, ne až krok 5. Na Gitea si
jedním voláním `ToolSearch` načti odložené nástroje podle řádku „Zakládá
issues a milestony". Na GitHubu otevři i `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md`
a volej `bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/issue-list.sh" -R <owner/repo>
--milestone <název> --state all` — `-R` je povinné, bez něj skript skončí
kódem `2`; na kód `7` (chybí/nepřihlášené `gh`) a `127` (chybějící skript)
reaguj stejně jako v kroku 5. Jiný nenulový kód znamená nejčastěji milestone
toho jména, který v repozitáři není (typicky překlep) — nepokračuj s prázdným
výpisem, jako by šlo o první vlnu; zeptej se uživatele, který milestone je
míněný. Z výpisu vezmi existující issues a interviuj jen o novém přírůstku,
ne o celém rozsahu znovu.

### 3. Klasifikuj backlog podle dostupnosti vzoru

Pro **každou** položku backlogu z kroku 2 proveď test podle
`${CLAUDE_PLUGIN_ROOT}/shared/precedent-test.md` — otevři ho, dřív než
začneš. Najdeš-li precedent, položka jde do téhle vlny s nalezenou cestou
jako Referencí pro krok 4. Nenajdeš-li, položka do téhle vlny nepatří —
**nezakládej pro ni issue vůbec**, ani jako Poznámku; zůstává položkou
backlogu, kterou reportuješ podle Formátu výstupu. Chce-li ji uživatel mít
v trackeru zapsanou pro příště, doporuč mu `/sagittaras:file-issue` — tenhle
skill jí novou issue sám nezakládá, aby nevznikala Poznámka jako vedlejší
produkt plánování.

Vyjde-li z klasifikace **nulový počet položek pro tuhle vlnu**, řekni to
uživateli a zeptej se, jestli má smysl pokračovat krokem 4 s prázdným draftem,
nebo jestli je na řadě napřed spárovaná implementační session pro některou
z položek. Prázdný draft znamená, že v kroku 7 vznikne jen milestone jako
schránka s definicí „hotovo" a žádné issue — `review-milestone` ani
`run-milestone` nad ním nemají co dělat, dokud první issue nepřibude
v příští vlně.

### 4. Sepiš draft Zadání pro tuhle vlnu

Otevři `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` a piš přesně podle něj —
tvar názvu, sekce těla i pravidla pro psaní kritérií, včetně jeho sekce
„Reference je precedent v kódu". Jazyk textu určuje sekce `Jazyk issues`
z konfigurace.

Nad rámec šablony platí:

- **`Souhrn` nese i hranice** — co položka podle nalezeného precedentu dělá,
  a je-li to nejednoznačné, i co nedělá. Stejné pravidlo jako v kroku 4a
  `triage-issue`, ať je Zadání z plánování a Zadání z triage nerozeznatelné.
- **Pořadí je topologické.** Žádné issue nesmí záviset na issue uvedeném později.
  Vzniklý cyklus rozetni tak, že rozdělíš jedno z issues, ne tak, že závislost
  zamlčíš — `run-milestone` z ní staví graf a zamlčená hrana pošle práci na
  rozpracovaný základ.
- **Každé kritérium ukotvi v precedentu nalezeném v kroku 3** a tu cestu
  uveď v `Reference` — soubor nebo vzor v kódu, ne sekce dokumentu. Odkaz na
  ADR ze `Zdroje pravdy` smíš přidat jako doplňkové omezení („nesahej na X,
  viz ADR-N"), nikdy místo kódové reference.
- **Labely urči rovnou**, podle pravidel v Zásadách níže. Povolené hodnoty bere výčet
  ze sekce `Labely`; label mimo něj nezakládej bez potvrzení v kroku 6.

### 5. Zjisti stav trackeru

Recepty i odložené nástroje na Gitea už máš otevřené, pokud jsi jimi prošel
v kroku 2 (rozšíření existujícího milestonu). Jinak teď otevři
`${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`, vyber sloupec podle sekce
`Forge` z konfigurace a **volání neodvozuj z hlavy**; na Gitea si jedním
voláním `ToolSearch` načti odložené nástroje podle řádku „Zakládá issues
a milestony". **Sekci s nástrahami přečti hned teď**, ne až před zápisem —
část chyb v trackeru selhává tiše (nepřipnutý label vypadá jako úspěšné
volání) a pozná se až u review.

Vypiš **existující labely a existující milestony**. Jsou to čtecí operace, takže
zásada „do trackeru se zapisuje až po potvrzení" platí dál; jenže bez nich neumíš
uživateli v kroku 6 říct, které labely se skutečně budou zakládat, a kolizi názvu
milestonu bys zjistil až po odkývaném draftu.

Na GitHubu skriptům předávej repozitář jako `-R <owner/repo>` ze sekce `Forge`;
tabulka receptů argument neuvádí, ale bez něj skript skončí kódem `2` a `gh` by se
jinak řídilo podle aktuálního adresáře, který v izolovaném worktree ukazuje jinam.
Doslovný tvar volání:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/label-list.sh" -R <owner/repo>
```

Na nenulový kód reaguj dřív, než cokoli vznikne:

- **`7`** — chybí `gh`, nebo není přihlášené. Ohlas to a skonči; uživatel to má vědět
  dřív, než v trackeru leží půlka milestonu.
- **`127`** — skript na disku není. Ohlas, který chybí, a nezakládej nic; rozepsaný
  milestone bez zbytku skriptů se dokončit nedá.
- **`2`** — chybný nebo chybějící argument, nejčastěji vynechané `-R`. Oprav volání
  a zopakuj.

Zbylé kódy vyhledej v `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md`.

**Milestone stejného názvu už existuje** → tohle je běžný stav pro druhou a další
vlnu, ne kolize. Přečti jeho popis a existující issues a potvrď s uživatelem, že
tahle vlna navazuje na tentýž milestone. **Odmítne-li**, zeptej se na jiný název
a založ ho jako první vlnu, ne jako pokračování. **Potvrdí-li**, vrať se s draftem
z kroku 4 na krok 3: přepočítej ho proti právě zjištěným existujícím issues stejně,
jako to krok 2 dělá při rozšiřování milestonu — draft vznikl bez jejich znalosti
a bez přepočtu by `Závisí na` mohlo minout čísla, která už v milestonu jsou, a
issues by se zbytečně zdvojily. Teprve přepočtený draft jde do kroku 6 a v kroku 7
do milestonu jen přidáváš — nezakládáš ho znovu.

### 6. Předlož draft a počkej na potvrzení

Vypiš draft podle Formátu výstupu a **počkej na potvrzení nástrojem AskUserQuestion**.
Tohle je povinná brzda, ne zdvořilost: tabulka názvů a pořadí závislostí se čte půl
minuty a je to jediné místo, kde uživatel zachytí špatně odhadnutou vlnu dřív, než
z ní bude deset issues v trackeru, které někdo musí ručně zavírat.

Zároveň si nech potvrdit labely — jmenovitě ty, které podle kroku 5 v projektu ještě
nejsou a chystáš se je založit, každý s navrženou barvou. Barvu předávej hexem bez
`#`; typové a oblastní drž v odlišných barevných rodinách, ať je routing čitelný na
první pohled.

Připomínky zapracuj a draft předlož znovu. Do kroku 7 jdi až s potvrzeným draftem.

### 7. Založ nebo rozšiř milestone a issues

Volání skládej stejně jako v kroku 5 — z receptů, na GitHubu vždy s `-R <owner/repo>`.
Zakládej v tomhle pořadí; jiné pořadí vyrobí objekty, na které se další volání nemá
jak odkázat:

1. **Chybějící labely** — bez nich se nasazení labelu na issue tiše mine účinkem.
2. **Milestone**, jde-li o první vlnu. Do popisu napiš, co pro tenhle milestone
   znamená „hotovo" — a pokud backlog z kroku 3 obsahuje nezaložené položky,
   zmiň, že popis pokrývá i budoucí vlny, ne jen tuhle. Podle popisu
   `review-milestone` posuzuje rozsah (okruh 4e); `close-milestone` popis
   nečte, zavření řídí jen počty zavřených issues a zmergované integrační PR.
   **Jedna až dvě věty na jednom řádku**: popis se předává
   argumentem, takže víceřádkový markdown se v shellu tiše rozbije. Co se do
   dvou vět nevejde, patří do issues. Jde-li o další vlnu do existujícího
   milestonu, krok přeskoč — nezakládej ho znovu.
3. **Issues sekvenčně, ne paralelně.** Tělo každého issue musí v sekci `Závisí na`
   odkazovat na **skutečná čísla** těch, na kterých závisí, a ta vzniknou až
   založením; u další vlny smí jít i o čísla založená v předchozí vlně. Paralelní
   běh vyrobí sadu issues odkazujících na čísla, která si model domyslel — a graf
   závislostí v `run-milestone` z toho složí nesmysl. Každé volání nese rovnou
   `milestone` i `labels`: issue mimo milestone je tichá chyba stejného druhu
   jako nepřipnutý label a hledá se pak napříč celým trackerem.

Tělo issue vypiš do **dočasného souboru mimo pracovní strom repozitáře** a předej ho
podle receptu (`--body-file` u `gh` skriptů, obsah souboru v parametru `body`
u Gitea MCP) — nikdy argumentem, víceřádkový markdown se o uvozovky a zpětné
apostrofy rozbije, a rozbije se tiše. Soubor uvnitř stromu by tam zůstal jako
nesledovaná veteš a nečistý strom shodí `milestone-branch.sh` hned na začátku
`run-milestone`, který na tenhle skill navazuje — soubor mimo strom tenhle
problém nemá, takže ho ani není nutné po sobě mazat. **Do dokumentace
projektu nezapisuj nic** — mezery a chybějící precedenty hlásíš, neopravuješ.

Selže-li zápis uprostřed, **nezačínej znovu od začátku**: vypiš, co už vzniklo,
a zeptej se, jak pokračovat. Opakovaný běh nad rozpracovaným milestonem vyrobí
duplikáty. U chyby 404 na zápisu ověř oprávnění účtu podle nástrah v receptech;
jiný repozitář nezkoušej.

### 8. Shrň výsledek

Vypiš souhrnnou tabulku podle Formátu výstupu, backlog položek, které do téhle
vlny nešly (a proč), a jako další krok doporuč `/sagittaras:review-milestone` —
ten neúplnou vlnu jako nález nebere, takže recenzentovi stačí výčet
nezaložených položek backlogu pro kontext, ne omluva. Plán **neposuzuješ sám**: recenzent
sdílející kontext s autorem si odkývá vlastní úvahu, proto review patří
někomu, kdo tvůj kontext nevidí. Sám ho nespouštěj — rozhodnutí patří
uživateli.

## Formát výstupu

**Draft k potvrzení** (krok 6) — čísla ve sloupci `#` jsou pořadí v draftu, ne čísla
issues; ta zatím neexistují:

```
Milestone: <název> — hotovo, když <definice hotového> [nebo: „vlna N do existujícího milestonu #<číslo>"]

| # | Název issue | area | Závisí na | Precedent (Reference) |
| --- | --- | --- | --- | --- |
| 1 | <type>(<scope>): <popis> | area:<oblast> | — | <cesta k souboru/vzoru> |
| 2 | <type>(<scope>): <popis> | area:<oblast> | #1 | <cesta k souboru/vzoru> |

Chybějící labely k založení: <název (barva hexem bez #)>, … nebo „žádné"
Do téhle vlny nešlo (chybí precedent): <výčet s jednou větou proč — obvykle „potřebuje spárovanou session"> nebo „nic"
```

**Souhrn po založení** (krok 8):

```
Milestone: <název> — <odkaz>

| Číslo | Název | Závisí na | Odkaz |
| --- | --- | --- | --- |
| #<n> | <název issue> | #<n>, #<n> | <url> |

Založené labely: <výčet, nebo „žádné">
Backlog na příští vlnu: <výčet s důvodem, nebo „žádný">
Další krok: /sagittaras:review-milestone
```

## Zásady

- **Reference vždy kód, ne próza.** Kritérium ukotvené jen v próze nejde
  ukázat na nic ověřitelného v kódu. Odkaz na ADR smíš přidat jako doplňkové
  omezení, nikdy místo kódové reference — přesně tak to popisuje i sdílená
  `issue-template.md` a stejně to čte `implement-issue` i `verify-issue`.
- **Bez precedentu žádné issue, a neúplná vlna je v pořádku.** Položka bez
  precedentu se sama nezakládá (leda jako Poznámka na explicitní přání
  uživatele přes `file-issue`) a milestone i tak smí legitimně vzniknout
  nedopsaný — je to výchozí stav, dokud se neustanoví další precedenty, ne
  chyba.
- **Právě jeden `area:*` label na issue, podle kódu, kterého se kritéria dotýkají —
  ne podle tématu milestonu.** Podle tohohle labelu vybírá `run-milestone` inženýra,
  takže chyba pošle práci špatnému specialistovi a projeví se až u review PR.
- **Typový label se musí shodovat s typem v názvu issue.** `implement-issue` z něj
  odvozuje typ větve i commitu; rozpor je nález pro `review-milestone`.
- **Do trackeru se zapisuje až po potvrzení draftu.** Před krokem 7 skill jen čte;
  nic nezakládá a nic nemění.
- **Sdílený kontrakt má přednost.** Odporuje-li tenhle postup šabloně issue,
  konfiguraci nebo receptům, platí ony.
