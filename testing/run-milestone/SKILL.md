---
name: run-milestone
description: >-
  Autonomně provede naplánovaný milestone: sestaví graf závislostí z issues,
  ověří v trackeru, že nad plánem proběhlo review, založí integrační větev
  a v dávkách dispečuje odblokovaná issues paralelním agentům podle labelu
  `area:*`. Přibude-li do milestonu za běhu další vlna z plan-milestone,
  zaregistruje ji a pokračuje. Každé PR nechá zrevidovat dvěma přísně
  ohraničenými rolemi — akceptační kritéria bez čehokoli navíc, kvalita kódu
  podle rules dané cesty — protáhne integrační bránou a mergne do integrační
  větve; na konci předloží jedno PR do výchozí větve, a obsahoval-li prompt,
  kterým byl spuštěn, výslovný souhlas k mergi, nechá ho i rovnou mergnout.
  Sám neimplementuje ani nerecenzuje.
when_to_use: >-
  Použij, když je milestone naplánovaný a zrevidovaný a má se začít
  implementovat — „spusť milestone", „proveď ten milestone", „nech to
  naimplementovat", „rozjeď issues z milestonu" — nebo když se má dokončit
  přerušený běh milestonu. Nepoužívej pro sestavení plánu a založení issues,
  na to slouží plan-milestone; pro posouzení hotového plánu review-milestone;
  pro jediné issue implement-issue, ten si spusť přímo. Zavření milestonu
  po merge dělá close-milestone.
argument-hint: "[milestone — název, číslo nebo slug]"
model: opus
effort: xhigh
# Zařazení dle matice: orchestrace workflow řídící víc fází → opus × xhigh,
# bez odchylky. Rozhodovací strom, bod 3: skill má dojet k cíli sám, přes
# desítky kroků a nástrojů, s retry rozpočtem a ověřováním poctivosti cizích
# dispatchů. Matice sice říká „rozhoduj podle nejtěžší práce, kterou skill dělá
# sám", a implementaci i review tenhle skill deleguje — jenže jeho vlastní práce
# je právě to delegování: udržet graf závislostí, poznat selhaný dispatch od
# selhané implementace a nemergnout nic, co neprošlo. Chyba v tomhle rozhodování
# stojí celý milestone, ne jedno kolo.
# Krok 5 (mandát rolí A/B — role B čte rules automaticky vložené do kontextu
# podle cesty čtených souborů) staví na principech 1.4/2.5, krok 9 (vlnový
# růst milestonu) na principu 2.4 interního `.docs/workflow-vision.md`
# pluginu (existuje jen v tomhle repozitáři, proto se v textu pro cizí
# projekt necituje).
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - ToolSearch
  - Agent
  - Skill
  - AskUserQuestion
  - mcp__gitea__milestone_read
  - mcp__gitea__issue_read
  - mcp__gitea__issue_write
  - mcp__gitea__list_issues
  - mcp__gitea__pull_request_read
  - mcp__gitea__pull_request_write
  - mcp__gitea__pull_request_review_write
  - mcp__gitea__list_pull_requests
# Výčet `mcp__gitea__*` odpovídá řádku „Orchestruje celý milestone" ve sdílených
# receptech; jsou to odložené nástroje, ale vyjmenovat je jde a bez toho by
# gitea větev spadla až uprostřed běhu. `pull_request_review_write` přibyl kvůli
# kroku 5: report role B se na rozdíl od role A (ta si komentář ukládá sama skrz
# `verify-issue`) nikde neukládá, dokud ho neuloží tenhle skill.
# Chybějící Write/Edit je tady hlavní hranice, ne opomenutí: bez zapisovacích
# nástrojů skill fyzicky nemůže začít opravovat cizí PR, což je přesně ta role,
# do které orchestrátor sklouzává nejsnáz. Tělo integračního PR proto skládá
# `open-pr`, který soubor umí zapsat.
# Bash je záměrně nezúžený: `integration-gate.sh` dostává jako argument
# libovolný ověřovací příkaz projektu z konfigurace (`dotnet build`, `pnpm test`,
# …) a vzor `Bash(bash:*)` by ho zablokoval.
# disable-model-invocation: false, přestože běh je dlouhý, drahý (paralelní
# opus agenti) a mění repozitář i tracker — model smí spustit i jen na základě
# fráze v konverzaci („spusť milestone", „rozjeď issues z milestonu"), protože
# brzdou proti omylu nejsou zakázaná vyvolání, ale čtecí ověřovací kroky před
# první zapisovací akcí (readiness check, review report, důkaz review v kroku 2)
# a eskalace při čemkoli nejednoznačném. Sama práce zůstává nevratná stejně jako
# dřív; nevratnost tu ale hlídá průběžná eskalace, ne odepřené vyvolání.
# Vynechaná zvažovaná pole: disallowed-tools — allowed-tools je uzavřený výčet,
# není co zakazovat navíc; context/agent — fork by odřízl uživatele, kterému se
# eskaluje a předkládá závěrečné PR; background — uživatel průběh sleduje
# a odpovídá na eskalace; paths — spouští se z konverzace nad celým repozitářem,
# ne prací nad konkrétními soubory; shell — skripty se spouští explicitním
# `bash`; version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Run Milestone

Jsi engineering manager: přiděluješ tikety, necháváš práci zrevidovat a mergeuješ.
**Kód nepíšeš a známky nedáváš** — implementaci i posouzení dělají agenti, ty držíš
pořadí, rozpočet pokusů a rozhodnutí o merge. Jakmile začneš opravovat cizí PR nebo
sám hodnotit, ztratíš nezávislost, kvůli které je celý řetěz postavený takhle.

Závazné kontrakty (při rozporu mají přednost před tímto textem):

| Soubor | Kdy ho otevřít |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` | v kroku 1, když potřebuješ vědět, kde v projektové konfiguraci co hledat |
| `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` | **před prvním sáhnutím na tracker** — volání issue, PR ani milestonů neodvozuj z hlavy |
| `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` | než poprvé zavoláš skript ze `scripts/`, kvůli výstupu a návratovým kódům |
| `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` | v kroku 1, nejsi-li si jistý čtením sekce `Závisí na` |

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

Kroky 1, 2 a 10 běží jednou. Kroky 3 až 9 tvoří smyčku, která se opakuje, dokud nejsou
všechna issues milestonu zavřená nebo eskalovaná — a „všechna issues" se v kroku 9
před každým dalším kolem znovu ověřuje proti trackeru, ne jen proti grafu z kroku 1:
milestone může za běhu přibrat další vlnu. Krok 11 je referenční — neběží
v pořadí, ale platí po celou dobu.

### 1. Před startem

**Konfigurace.** Načti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md`
v cílovém projektu. Chybí-li `CONTRIBUTING.md` nebo sekce, **nepokračuj
a nedomýšlej si hodnoty** — řekni to a odkaž na `/sagittaras:init-workflow`.
Potřebuješ z ní podsekce `Forge`, `Větvení` a `Ověřovací příkazy`; chybí-li
některá, řekni která a skonči. **Podsekce `Agenti` je nepovinná** — chybí-li
celá, není to důvod skončit: znamená to, že projekt nemá specializované
agenty, a krok 3 i 5 na to mají fallback.

**Přístup k forge.** Podle sekce `Forge` si otevři `forge-recipes.md` a připrav si
větev, kterou pojedeš:

- **Gitea** — **jedním** voláním `ToolSearch` načti odložené nástroje podle řádku
  „Orchestruje celý milestone". Načítat je po jednom znamená kolo navíc u každé
  operace, a těch je za milestone stovky.
- **GitHub** — ověř předpoklady hned teď:

  ```bash
  bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/milestone-list.sh" -R "<owner/repo>" --state open
  ```

  `-R owner/repo` ze sekce `Forge` patří do **každého** `gh` volání; recepty ho v zápisu
  neuvádějí, ale skripty ho vyžadují a bez něj skončí kódem **2** (chybný argument), ne
  kódem 7. Kód **7** znamená chybějící nebo nepřihlášené `gh` — řekni to rovnou, ne až
  v půlce milestonu, kdy už běží dispatche, které nemají kam otevřít PR.

**Milestone.** Rozpoznej ho ze zadání. Sedí-li zadání na víc otevřených milestonů nebo
na žádný, zeptej se — rozjet nesprávný milestone znamená hromadu PR k zahození.

**Issues.** Vypiš **všechna** issues milestonu, otevřená i zavřená. Pozor na dvě pasti
popsané ve `forge-recipes.md`: výpis stránkuje po 30 a bez omezení na typ vrací i PR.
Počet si zkontroluj proti `open_issues` + `closed_issues` z milestonu; při rozporu
raději eskaluj, než abys rozhodoval nad neúplným seznamem.

**Graf závislostí.** Z každého těla vytáhni sekci `Závisí na`. Sekce buď je, nebo není;
jiné stavy šablona nezná. Odkaz na issue mimo milestone nebo na neexistující číslo a
cyklus v grafu jsou důvod k eskalaci — nad vadným grafem se práce buď nikdy nerozjede,
nebo se rozjede ve špatném pořadí.

**Rozřazení podle rozpracovanosti.** Zjisti, co už k issues existuje, **dvěma průchody**:

1. Vypiš PR se stavem `all` a **bez filtru na milestone**. Filtr by nepomohl: milestone
   nese jen integrační PR, protože issue PR mu ho nikdo nepřiřazuje. Nech si ty, jejichž
   base **začíná `milestone/`** — přesný slug určí až krok 2, tady stačí prefix; PR
   patřící jinému milestonu odpadne v dalším bodu, protože jeho `Closes #N` neodpovídá
   žádnému issue z tohohle milestonu. I tenhle výpis stránkuje po 30 — u PR navíc nemáš
   proti čemu počet zkontrolovat, takže se nespoléhej na první stránku a dober zbytek.
2. Spáruj přes strukturované pole, ne přes text: GitHub vrací u PR `closingIssuesReferences`
   a u issue `closedByPullRequestsReferences`, recepty mají řádek „Najdi PR patřící
   k issue" pro obojí. Nedá-li forge strukturované pole, teprve pak zavolej „Přečti PR"
   a vezmi `Closes #N` z těla. **Nikdy podle názvu větve**: název je konvence, vazba
   forge nebo `Closes` je kontrakt. Nepáruje-li se kandidát s žádným issue z téhle sady,
   zahoď ho — patří jinému milestonu, i když sdílí prefix větve.

Každé otevřené issue pak zařaď do jednoho ze tří stavů:

| Stav | Kam patří |
| --- | --- |
| bez PR | do dispatche, krok 3 |
| s otevřeným PR | rovnou do review, krok 5 — dispatch už proběhl v předchozím běhu |
| se zmergovaným PR | **jen** zavření issue a kontrola podle kroku 8; merge ani mazání větve se neopakuje |

Bez tohohle rozřazení se přerušený běh nedokončí: issue s hotovým PR by se nedispečovalo
(PR má) a jeho PR by se neposuzovalo (neprošlo krokem 4), takže by běh skončil
deadlockem — a issue se zmergovaným PR by se naopak dispečovalo znovu.

**Důkaz review.** Na issue s **nejnižším číslem** v milestonu najdi komentář s doslovným
nadpisem `## Review milestonu <název milestonu>` — je to jediná značka, podle které jde
report `review-milestone` poznat. Ověřuj ho čtením trackeru, **ne z tvrzení uživatele a
ne z vlastní paměti**; durable záznam je jediné, co přežije restart session.

Komentáře si vyžádej výslovně, řádek „Přečti issue" v receptech na ně nestačí: na Gitea
použij `issue_read` → **`get_comments`** (metoda `get` vrací jen tělo issue), na GitHubu
je vrátí `gh/issue-read.sh <n>` v poli `comments`. Sáhneš-li vedle, komentář nenajdeš
a brána se tiše vypne — skill nabídne běh bez review nad milestonem, který review má.

**Je-li takových komentářů víc, platí poslední založený.** `review-milestone` starší
komentáře nepřepisuje, takže na issue leží celá historie kol; verdikt čti jen
z nejnovějšího a v hlášení uveď jeho datum. Přečtený starý komentář rozhoduje podle
verdiktu, který už neplatí — v horším směru pustí běh nad plánem, jehož poslední verdikt
je `Not ready`.

V platném komentáři přečti řádek `**Verdikt:**`:

- **`Sound`** → pokračuj.
- **`Needs attention`** → shrň nálezy stupně `should-fix` z reportu a zeptej se, jestli
  spustit běh, nebo nejdřív opravit plán. Blokující nálezy u tohohle verdiktu nehledej —
  `review-milestone` je s nimi vydává jako `Not ready`.
- **`Not ready`** → **nespouštěj běh.** Odkaž na opravu plánu (`/sagittaras:plan-milestone`)
  a na nové review. Milestone s tímhle verdiktem je přesně ten případ, kvůli kterému brána
  existuje.
- **Komentář chybí** → nabídni jako první možnost spustit `sagittaras:review-milestone`
  a teprve jako druhou pokračovat bez review. Autonomní běh nad neověřeným plánem protočí
  celou smyčku implementace a ověření na kritériích, která nikdy nebyla ukotvená v žádném
  dokumentu — review stojí jedno kolo, tohle stojí milestone.

### 2. Integrační větev

Slug odvoď z názvu milestonu **deterministicky**, protože je to jediný klíč k integrační
větvi: převeď na malá písmena, odstraň diakritiku, každý neabecední a nečíselný znak
nahraď pomlčkou, opakované pomlčky sluč a krajní ořízni. Skript slug validuje proti
`^[a-z0-9]+(-[a-z0-9]+)*$` a jiný tvar odmítne — a odvodíš-li ho při navazování jinak než
poprvé, založíš druhou integrační větev a práce prvního běhu se rozdvojí.

Než založíš, podívej se, jestli v repozitáři už větev `milestone/*` k tomuhle milestonu
není; předchozí běh mohl slug odvodit jinak. Existuje-li, použij ji.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/milestone-branch.sh" <slug>
```

- `created=false` → **navazuješ na přerušený běh a větev nezakládáš znovu**;
  znovuzaložení by zahodilo práci, kterou předchozí běh už zmergoval.
- kód **2** → chybný slug nebo to není repozitář; oprav odvození, případně eskaluj.
- kód **3** → remote neodpověděl; eskaluj, integrační větev se bez remotu nezaloží.
- kód **4** → nečistý pracovní strom; eskaluj, není to stav k obejití.

### 3. Dispatch dávky

**Odblokované issue** je otevřené issue ve stavu „bez PR" (krok 1), jehož všechny
závislosti jsou zavřené a pro které zrovna neběží agent.

Každé odblokované issue dispečuj **zvlášť a paralelně**, jedno na issue, nástrojem
**`Agent`** s těmito parametry:

| Parametr | Hodnota |
| --- | --- |
| `subagent_type` | agent z tabulky `Agenti` podle labelu `area:*` na issue |
| `isolation` | `"worktree"` |
| `run_in_background` | `true` |
| `prompt` | podle šablony ve Formátu výstupu |

**Používej `Agent`, ne `Skill`.** Forkovaný skill běží synchronně a serializoval by
práci, která má běžet vedle sebe — z dávky pěti issues by se stalo pět čekání za sebou.

**Model ani nástroje dispečovaného agenta nepřenastavuj.** Plynou z jeho definice; kdo je
nastavoval, věděl, co ten agent dělá. `isolation` je jiný případ a rozpor to není: ta
říká, *kde* agent pracuje, ne *jak* — předáním ji zaručíš i agentovi, který ji ve své
definici nemá, a bez ní by si paralelní dispatche přepisovaly jeden pracovní strom.

**Ověř, že agent dosáhne na nástroj `Skill`.** Zadání mu ukládá postupovat skillem
`sagittaras:implement-issue`; agent, který `Skill` ve svých `tools` nemá, naimplementuje
mimo proces — bez `create-branch`, `make-commit` a `open-pr` — a krok 4 to nepozná,
protože PR vznikne. Jeho definici hledej v `.claude/agents/<jméno>.md` cílového projektu
a v `agents/` pluginů. **Nenajdeš-li ji, ber, že `Skill` nemá**; chybí-li pole `tools`
úplně, agent dědí všechno a podmínka je splněná. Nedosáhne-li, dispatch přesto proveď —
šablona zadání mu ukládá to ohlásit místo obcházení postupu.

**Chybí-li na issue `area:*` label, nedispečuj a eskaluj.** Je to chyba dat na issue,
ne limit konfigurace, a poslat práci náhodnému specialistovi se pozná až u review, kdy
je hotová.

**Chybí-li pro oblast issue řádek v mapě `Agenti`, je hodnota `—`, nebo podsekce
`Agenti` chybí v konfiguraci celá, eskalace to není** — sáhni po stejném fallbacku
jako u recenzentů v kroku 5: dispečuj nástrojem `Agent` s
`subagent_type: "general-purpose"` (`isolation` a `run_in_background` beze změny)
a do zadání ulož, ať agent postupuje skillem `sagittaras:implement-issue`.
Prázdná, chybějící nebo zcela nezaložená mapa je platný stav konfigurace, ne důvod
issue vynechat.

**Odmítne-li nástroj `Agent` dispatch** (neznámý `subagent_type`, chyba volání), issue
neztrácej z přehledu — eskaluj ho i s chybou, kterou nástroj vrátil.

Veď si seznam běžících dispatchů (issue → agent). **Totéž issue nikdy nedispečuj podruhé,
dokud jeho agent běží** — dva agenti nad jedním issue si otevřou dvě PR a jedno z nich je
vždycky práce k zahození.

**Čekej na notifikace, nepolluj.** Nespouštěj kontrolní volání, jestli už je hotovo;
notifikace přijde sama. Do té doby o stavu běžícího agenta nic nevíš a **nevymýšlej si ho**.

### 4. Ověření výsledku dispatche

**Nevěř statusu `completed`.** Dispatch umí ohlásit hotovo, aniž by cokoli udělal —
typicky krátkou odpovědí o nedostupném MCP nebo nástroji, s téměř nulovým použitím
nástrojů.

Výsledek platí, jen když jsou splněné **obě** podmínky:

1. report jmenuje číslo PR,
2. to PR podle forge **skutečně existuje** a míří do integrační větve.

Není-li tomu tak, rozliš dva různé případy — jinak přeposíláš zadání, které selže znovu
ze stejného věcného důvodu, a eskalace přijde o celé kolo později:

- **Věcná překážka** — agent ohlásil `PR: žádné` s konkrétním důvodem (podspecifikované
  kritérium, nedostupná závislost, rozpor v zadání). **Nepřeposílej, eskaluj hned.**
  Druhý běh téhož agenta nad tímtéž zadáním skončí stejně.
- **Selhaný dispatch** — chybí řádek s číslem PR, PR neexistuje, nebo je odpověď krátká
  a bez použití nástrojů. Přepošli zadání **jednou** znovu témuž agentovi; při druhém
  stejném selhání eskaluj.

Selhaný dispatch **nečerpá retry rozpočet issue** — ten je vyhrazený kvalitě implementace,
ne výpadkům infrastruktury, a spotřebovat ho na nedostupný nástroj znamená zahodit issue,
které se ještě ani nezačalo řešit.

### 5. Review PR

Do tohohle kroku vstupují jak PR ověřená v kroku 4, tak PR, která už byla otevřená při
startu (krok 1). Každé nech posoudit **souběžně dvěma přísně ohraničenými rolemi** —
role A (akceptační kritéria) a role B (kvalita kódu). Obě mají **stejně přísný mandát**:
nic nad rámec toho, co jim šablona v Formátu výstupu předepisuje — žádné poznámky
navíc, žádné „když už tu jsem". **Prompt sestav doslova podle šablon** ve Formátu
výstupu — roli A podle „Zadání pro roli A", roli B podle „Zadání pro roli B"; vlastní
formulace mandát rozředí. Recenzenty ber ze sekce `Agenti`:

- **Je-li role obsazená** — dispečuj nástrojem `Agent` s `isolation: "worktree"`
  a `run_in_background: true`; recenzent si musí checkoutnout PR větev, aniž by sáhl na
  tvůj pracovní strom. Agentovi pro roli A řekni, ať postupuje skillem
  `sagittaras:verify-issue`; postup ověřování je týž bez ohledu na to, kdo ho vede. Nemá-li
  ten agent ve svých `tools` nástroj `Skill` (zjišťuje se stejně jako v kroku 3), na skill
  nedosáhne — pak roli A **vůbec nedispečuj** a ověř ji fallbackem níž (skillem
  `sagittaras:verify-issue`); agenta uvedeného u role **B** dispečuj beze změny,
  agenta uvedeného u role **A** v tomhle případě vůbec nespouštěj.
- **Je-li v konfiguraci `—`, nebo podsekce `Agenti` chybí celá** — sáhni po fallbacku:
  roli A ověř skillem `sagittaras:verify-issue` (nástroj `Skill`; ten skill si forkuje
  kontext sám), roli B nech posoudit subagentem `general-purpose`
  (`isolation: "worktree"` a `run_in_background: true` beze změny — stejný důvod jako
  výš, recenzent nesmí sáhnout na tvůj pracovní strom). Prázdná nebo chybějící role je
  platný stav konfigurace, ne důvod běh odmítnout. Generického subagenta pusť na pozadí
  **dřív**, než spustíš forkovaný skill — ten běží synchronně, takže obráceným pořadím
  bys obě posouzení serializoval.

**Role A (akceptační kritéria) nesmí hlásit nic nad shodu nebo neshodu s kritérii
issue** — žádné architektonické poznámky, žádné styling připomínky. To je mandát
`verify-issue` samotného; dispatch mimo něj ho jen zopakuje v zadání.

**Role B (kvalita kódu) čte jako zdroj principů pravidla, která se jí sama vloží do
kontextu podle cesty měněných souborů** — ne obecný univerzální seznam z hlavy.
Nezmiňuj jí konkrétní mechanismus ani umístění: agent, kterému se řekne, kde pravidla
hledat, si je jde načíst ručně a udělá přesně ten univerzální průchod, který má mandát
zakázat — nechá to na automatickém vstupu do kontextu. Nálezy píše jako konkrétní
adresný pokyn („oprav tenhle řádek", „oprav tenhle blok"), bez rozepisování nad rámec
toho, co pravidlo v kontextu skutečně říká.

**Report role B musí nést oba řádky, `Přečtené soubory:` i `Pravidla v kontextu:`.**
Pravidlo se do kontextu vloží, až když se přečte soubor, na jehož cestu je navázané
— dokud recenzent nic nepřečetl, nemůže mít v kontextu nic, a `Pravidla v kontextu:
žádné` bez vyplněného `Přečtené soubory:` neznamená „projekt nemá pravidla", ale
„recenzent se na kód nepodíval". Chybí-li kterýkoli z těch dvou řádků, nebo je
`Přečtené soubory:` prázdné, platí to jako **selhaný dispatch** (krok 4), ne jako
blocking nález. Teprve report, který jmenuje přečtené soubory **a** `Pravidla
v kontextu: žádné`, znamená naprázdno proběhlé review — pro dotčené cesty žádné
pravidlo není. `Blokuje merge: ne` od role B v tomhle stavu platí; ohlas to
v hlášení na předělech stejně jako `check=skipped` v kroku 7 (posouzeno jen to, co
bylo v kontextu, ne úplnost) a doporuč `/sagittaras:write-rule`.

**Report role B ulož jako komentář k PR**, hned jak ho uznáš za platný dispatch
(oba řádky výše i `Blokuje merge:`). Na rozdíl od role A, která si komentář
ukládá sama skrz `verify-issue`, report role B se nikde neukládá, dokud to
neuděláš ty. Použij recept „Komentář k PR (review)" z `forge-recipes.md`: na
Gitea nástrojem `pull_request_review_write` se `state: "COMMENT"` a tělem
z reportu; na GitHubu ulož report do dočasného souboru **mimo** worktree PR
a pošli ho `bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-comment.sh" -R "<owner/repo>"
<číslo PR> --body-file "<soubor>"` (tělo nikdy jako argument — víceřádkový
markdown se v shellu rozpadne). Selže-li uložení, review tím neztrácí
platnost — pokračuj a zmiň to v hlášení na předělech.

**V promptu uveď číslo PR explicitně** — recenzenta nenech dohadovat PR z názvu větve.
Recenzent, který si PR hledá sám, si ho najde jiné, nebo si o něm udělá představu z větve,
která se mezitím posunula.

**Rozhoduje řádek `Blokuje merge: ano/ne`, ne próza kolem něj.** Report kteréhokoli
recenzenta bez tohohle řádku je **selhaný dispatch** (krok 4), ne blokující nález —
přepošli jednou znovu. U role A navíc report bez řádku `**Verdikt:**` (přesně tvar,
kterým `verify-issue` report začíná) platí stejně jako chybějící `Blokuje merge:`.

**Vrátí-li role A `**Verdikt:** Blocked`**, nejde o nález na implementaci —
`verify-issue` ho vydává, když ověření jako celek nešlo provést (chybějící
konfigurace, oblast bez ověřovacího příkazu, nedohledaný protějšek PR, nedostupné
prostředí), ne když kritérium neprošlo. `Blokuje merge` u něj sice bude `ano`, ale
**neposílej to do retry** (krok 6) — retry rozpočet je pro kvalitu implementace, ne
pro výpadek infrastruktury. Eskaluj rovnou podle kroku 11 s tím, co `verify-issue`
označil jako chybějící.

Při neshodě mezi recenzenty **vyhrává přísnější** a neshodu pojmenuj v hlášení: dva
protichůdné verdikty nad jedním PR jsou informace o kvalitě zadání, ne šum k zamlčení.

### 6. Retry

`Blokuje merge: ano` → **jeden** pokus o opravu. Týž agent, táž větev, žádné nové PR.
Do zadání dej **konkrétní nálezy obou recenzentů doslova**, ne jejich shrnutí, a povinné
mutační ověření podle šablony ve Formátu výstupu: dočasně vrátit chybu, potvrdit, že test
spadne, opravit, potvrdit, že projde — a **výslovně to uvést v reportu**. Bez toho se další
kolo review propálí na objevování testu, který neselže na ničem.

**Výjimka: konflikt z integrační brány (krok 7, kód 5).** Nejde o nález na kvalitu
kódu ani na kritéria, mutační ověření tu nemá co ověřovat — místo šablony pro retry
zadej: vmerguj aktuální špičku integrační větve, vyřeš konflikty ve jmenovaných
souborech, nezakládej nové PR. Po opravě jdi rovnou zpátky do kroku 7, ne do review
(krok 5) — recenzenti už PR posoudili, brána jen ověřovala slučitelnost. **I tenhle
retry je nejvýš jeden pokus** — nečerpá sice rozpočet vyhrazený kvalitě implementace
(krok 8), ale bez vlastního stropu by se opakovaný konflikt mohl vracet do kroku 7
donekonečna. Přetrvá-li kód 5 i podruhé, eskaluj podle kroku 11.

Po opravě spusť review znovu (krok 5). Vyjde-li podruhé `ano`, **neopakuj**: PR nech
otevřené, eskaluj a pokračuj v issues, která na něm nezávisí. Issue nezavírej — zavřené
issue by odblokovalo závislé práce nad základem, který neprošel.

### 7. Integrační brána před merge

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/integration-gate.sh" <pr-větev> <integrační-větev> -- <ověřovací příkaz>
```

Příkaz vezmi ze sekce `Ověřovací příkazy` podle oblasti issue. Bránu spusť **vždy**, i
když obě review dopadla čistě: review běželo nad větví, jak se odštěpila, a dvě nezávisle
zelená PR se umí rozbít sémanticky — přejmenovaný parametr, změněný kontrakt, dvakrát
zaregistrovaná služba — **bez jediného textového konfliktu**.

- `merge=conflict` (kód 5) i `check=fail` (kód 6) pošli do retry smyčky (krok 6), ale
  **ne se stejným rozpočtem**. Nález se bere z jiné sekce podle kódu —
  `integration-gate.sh` je nevypisuje do stejného místa: u kódu **5** je to `conflicts=`
  a obsah sekcí `[conflicts]`/`[merge_output]` (textový konflikt, žádný ověřovací
  příkaz neběžel) a **retry rozpočet issue se tím nečerpá** — je to stav integrace,
  stejné pravidlo jako u konfliktu proti posunuté špičce v kroku 8; u kódu **6** je to
  sekce `[output]` (příkaz proběhl a selhal) a **retry rozpočet se čerpá** jako
  u běžného nálezu review. Vyčerpaný rozpočet u kódu 6 → eskalace.
- `check=skipped` **při kódu 0** znamená, že pro oblast v konfiguraci není příkaz. Ohlas
  to — brána v takovém případě ověřila jen slučitelnost, ne funkčnost. U kódu 5 je
  `skipped` jen vedlejší důsledek abortovaného merge a samostatně se nehlásí.
- Kód **2** (chybný argument nebo větev, která neexistuje lokálně ani na remotu) a kód
  **3** (nedostupný remote) **nejsou selhání review** — je to výpadek infrastruktury,
  retry rozpočet issue nečerpá; eskaluj podle kroku 11. Propálit retry na nedostupném
  remotu je totéž selhání jako u dispatche v kroku 4, jen o krok později.
- Brána sama nikdy nepushuje ani nemerguje. Merge je krok 8.

### 8. Merge do integrační větve

Mergni strategií ze sekce `Větvení` (pro integrační větev je to squash). **Neprošel-li
merge** (konflikt, odmítnutí forge, nenulový kód volání) — **issue nezavírej a větev
nemaž.** Rozliš dál:

- **Konflikt proti aktuální špičce integrační větve** — brána v kroku 7 ověřovala
  slučitelnost v okamžiku svého běhu; u dávky víc PR mergovaných po sobě je špička
  u druhého a dalšího PR jinde. Pošli PR zpátky do kroku 7 nad aktuální špičkou; projde-li
  brána znovu čistě, merge opakuj. Retry rozpočet issue tím nečerpáš — je to stav
  integrace, ne kvalita implementace.
- **Odmítnutí forge** (ochrana větve, povinný check, zastaralý stav PR) — eskaluj podle
  kroku 11. Neobcházej ochranu ani nezkoušej force.

Prošel-li merge, smaž zdrojovou větev a ověř, že se issue **skutečně zavřelo**.
`Closes #N` na obou forge zabírá až při merge do **výchozí** větve, takže tady se issue
samo nezavře — zavři ho explicitně. Otevřené issue po merge by smyčku v kroku 3 držela
v přesvědčení, že práce ještě neproběhla; zavřené issue nad prací, která do integrační
větve nedorazila, by naopak odblokovalo závislé issues nad základem, který neexistuje.

**Tenhle merge je autonomní** — uživatel ho autorizoval sekcí `Větvení` v konfiguraci
a ptát se na každé PR by z autonomního běhu udělalo ruční klikání.

**Do výchozí větve sám nikdy nemergeuješ.** Jediné místo, kde se to smí stát, je
`open-pr` v kroku 10.3 — a jen tehdy, když prompt, kterým byl aktuální `run-milestone`
spuštěn, obsahoval výslovný souhlas k mergi (viz krok 10). Bez toho souhlasu zůstává
zákaz stejný jako dosud, i kdyby si merge uživatel vyžádal uprostřed běhu: rozhodnutí
musí stát v promptu, kterým běh začal, ne v průběžné zprávě.

### 9. Sync mezi dávkami

Po zmergování dávky srovnej integrační větev s výchozí:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/sync-branch.sh" <integrační-větev>
```

`result=conflict` (kód 5) **neřeš sám** — skript merge abortuje, takže větev zůstává
použitelná, a rozhodnutí, čí verze platí, patří uživateli. Eskaluj a čekej. Kódy
`2`–`4` (viz `git-scripts.md`) jsou výpadek volání nebo prostředí, ne konflikt —
eskaluj podle kroku 11, retry rozpočet issue tím nečerpáš.

**Před návratem na krok 3 zkontroluj nové issues.** Milestone může za běhu přibrat
další vlnu — `plan-milestone` do něj může přidat další Zadání, zatímco `run-milestone`
už pracuje. Vypiš issues milestonu znovu (stejný recept jako v kroku 1, „Issues").
Nesedí-li počet proti `open_issues` + `closed_issues`, nejde rovnou o důvod k eskalaci
jako v kroku 1 — `plan-milestone` může zakládat issues sekvenčně, souběžně s tímhle
během. **Běží-li ještě nějaký dispatch**, počkej na jeho notifikaci a přečti znovu
tehdy; **neběží-li nic**, přečti znovu hned. Teprve druhá shodná neshoda je důvod
eskalovat.

Porovnej výpis se seznamem, který znáš dosud. Pro každé nové issue:

1. **Ověř, že je to Zadání, ne Poznámka** — kritéria vyplněná a Reference neprázdná
   (volnější filtr než `triage-issue` krok 2, který navíc ověřuje, že Reference cituje
   kód, ne dokument — tuhle přesnost hlídá až brána review níž, tady jde jen o to,
   oddělit Poznámku od Zadání). Nesplňuje-li to, **nedispečuj ho** a eskaluj podle
   kroku 11 s odkazem na `/sagittaras:triage-issue` — Poznámka bez kritérií nemá co
   implementovat.
2. Zařaď ho do grafu závislostí stejně jako v kroku 1 — přečti `Závisí na`, zkontroluj
   cykly a odkazy mimo milestone — a rozřaď podle rozpracovanosti (nová issues budou
   typicky „bez PR").

**Přibylo-li aspoň jedno nové Zadání, ověř znovu důkaz review** (krok 1, „Důkaz
review") — přečti nejnovější komentář `## Review milestonu <název>` a porovnej jeho
datum s datem založení nových issues. Je starší, nebo komentář vůbec není → zachovej
se jako u chybějícího komentáře v kroku 1: nabídni jako první možnost
`/sagittaras:review-milestone`, jako druhou pokračovat bez review. Je novější, přečti
v něm i řádek `**Verdikt:**` a rozhodni **stejnými větvemi jako v kroku 1** — `Sound`
pokračuje, `Needs attention` se ptá, `Not ready` novou vlnu nespouští. Novější datum
samo o sobě nestačí: nová issues by jinak mohla vlnu rozjet i nad plánem, jehož
poslední review skončilo `Not ready`.

- **Přibylo nové Zadání, nebo něco zbývá odblokované či rozpracované** → vrať se na
  krok 3 s doplněnou dávkou.
- **Nepřibylo žádné nové Zadání (nová Poznámka eskalovaná v bodu 1 se nepočítá)
  a všechna issues jsou zavřená nebo eskalovaná** → smyčka končí, pokračuj krokem 10.
- **Nepřibylo žádné nové Zadání, něco zbývá otevřené, ale nic není odblokované
  a nic neběží** → **deadlock** — eskaluj s výpisem toho, co na čem čeká.

### 10. Závěr

1. Poslední sync integrační větve s výchozí (krok 9).
2. Sestav název a tělo integračního PR: název jako Conventional Commit shrnující celý
   milestone, tělo podle šablony ve Formátu výstupu.
3. **PR nech založit skillem `sagittaras:open-pr`** (nástroj `Skill`) — předej mu
   základní větev (výchozí větev z konfigurace), milestone, hotový název i tělo, **a
   výslovně řekni, že jsou hotové a nemá je znovu odvozovat** — jeho vlastní krok 5 by
   jinak název i tělo odvodil ze zapsaných commitů podle svojí šablony, protože
   integrační PR žádné issue přímo neuzavírá. Bez tohohle pokynu se výčet zahrnutých
   a eskalovaných issues z tvé šablony ztratí. Obsahoval-li prompt, kterým byl aktuální
   `run-milestone` spuštěn, výslovný souhlas k mergi — i ten, doslova. Bez týhle předávky
   `open-pr` souhlas nemá odkud vzít, protože
   neviděl prompt, kterým byl spuštěn `run-milestone`. Mechaniku PR nepiš podruhé:
   `open-pr` řeší i push nepushnuté větve, kontrolu, že z téhle větve PR ještě neexistuje,
   předání těla souborem a **druhé volání, kterým se přiřazuje milestone** — při zakládání
   to nejde ani na jedné forge a `close-milestone` podle té vazby integrační PR dohledává.
   Ověř v jeho souhrnu, že milestone opravdu přiřadil.
4. Vzniklo-li jen otevřené PR (`open-pr` bez souhlasu, nebo souhlas nebyl), předlož ho
   uživateli a **skonči** — merge do výchozí větve patří jemu. Provedl-li `open-pr` merge
   (souhlas byl a merge prošel), ohlas hotovo bez dalšího čekání — na mergnutou výchozí
   větev už není na co čekat.
5. **Zeptej se, jestli přijde další vlna**, dřív než doporučíš `/sagittaras:close-milestone`
   — vlnové plánování dovoluje milestone legitimně rozšířit i po dnešním merge. Nepřijde-li,
   doporuč `close-milestone`, ale **až po merge** (vlastním, nebo tím, které provedl
   `open-pr`), ne dřív. Přijde-li, řekni, že další vlna se rozjede novým během
   `run-milestone` nad týmž milestonem — jestli si příští běh integrační větev
   z kroku 2 najde (`created=false`), nebo založí novou (`created=true`), záleží na
   tom, jestli dnešní PR do výchozí větve zůstalo otevřené (větev žije dál), nebo
   bylo zmergované a smazané (`open-pr` krok 8: `pr-merge.sh --delete-branch`) —
   v obou případech to `milestone-branch.sh` rozpozná samo, nic se tím nerozbije.

### 11. Eskalace

Eskaluj v těchto konkrétních situacích:

- konfigurace chybí, nebo v ní chybí sekce, kterou potřebuješ;
- `gh` chybí nebo není přihlášené (kód 7), případně forge vrací 404 na zápisu (skoro vždy
  chybějící oprávnění účtu, ne špatný název);
- `integration-gate.sh` skončil kódem 2 nebo 3 — výpadek infrastruktury, ne nález review;
- `area:*` label na issue chybí, nebo nástroj `Agent` dispatch odmítl — chybějící řádek
  v mapě agentů mezi tyhle důvody nepatří, na to je fallback v kroku 3;
- graf závislostí obsahuje cyklus, nebo `Závisí na` odkazuje mimo milestone;
- počet načtených issues nesedí s počty na milestonu (v kroku 9 až při druhé shodné
  neshodě, jinak počkej na notifikaci a přečti znovu);
- nové issue přidané do milestonu za běhu je Poznámka, ne Zadání — chybí kritéria
  nebo `Reference` (krok 9);
- review report v trackeru chybí, nebo má verdikt `Needs attention` (v obou případech
  se ptáš) či `Not ready` (běh nespouštíš); totéž platí, objeví-li se nová vlna Zadání
  bez vlastního review report novějšího, než jsou tahle issues (krok 9);
- dispatch ohlásil věcnou překážku, nebo selhal **dvakrát stejným způsobem** (krok 4);
- role A vrátila přes `verify-issue` verdikt `Blocked` (krok 5) — výpadek infrastruktury,
  ne nález na implementaci, retry rozpočet se nečerpá;
- PR má i po retry `Blokuje merge: ano`, nebo po retry znovu neprojde integrační branou;
- merge PR do integrační větve odmítlo forge (ochrana větve, povinný check, zastaralý
  stav PR) — issue zůstává otevřené, větev nesmazaná;
- `milestone-branch.sh` nebo `sync-branch.sh` skončily konfliktem, nečistým stromem,
  chybným argumentem či neexistující větví (kód 2), nebo nedostupným remotem;
- zbývají otevřená issues, ale žádné není odblokované.

Eskalace **shrne stav** — co je zmergované, co běží, co blokuje — a položí **jednu
konkrétní otázku**. Netýká-li se blokáda celého milestonu, nezastavuj běh: issues, která
na blokovaném nezávisí, běží dál.

## Formát výstupu

### Zadání pro implementujícího agenta

```
Naimplementuj issue #<číslo> (<název>) v repozitáři <owner/repo>.

Použij skill sagittaras:implement-issue. Nemáš-li nástroj Skill, postup
neobcházej — ohlas to a skonči.
Základní větev: <integrační větev> — z ní větvi a proti ní otevři PR.
Akceptační kritéria, reference i závislosti si přečti přímo z těla issue.

Report ukonči řádkem přesně v tomhle tvaru:
PR: #<číslo>

Nevzniklo-li PR, napiš `PR: žádné` a věcný důvod. Bez jednoho z těch dvou
řádků nehlas hotovo.
```

### Zadání pro roli A — akceptační kritéria

```
Posuď pull request #<číslo PR> v repozitáři <owner/repo>
(issue #<číslo issue>, větev <větev>).

Tvoje role: soulad s akceptačními kritérii issue. Postupuj skillem
sagittaras:verify-issue — jeho vlastní Formát výstupu platí beze změny
(řádek **Verdikt:** a report zakončený řádkem Blokuje merge: ano|ne). Tvůj
mandát je přísně ohraničený: posuzuješ jen shodu nebo neshodu s kritérii
issue — žádné architektonické poznámky, žádné styling připomínky, žádné
„když už tu jsem". Neopravuj nic — vracíš verdikt.
```

### Zadání pro roli B — kvalita kódu

```
Posuď pull request #<číslo PR> v repozitáři <owner/repo>
(issue #<číslo issue>, větev <větev>, základní větev <integrační větev>).

Fetchni a vycheckoutuj větev <větev> ve svém worktree. Zjisti soubory, které
PR mění: git diff --name-only origin/<integrační větev>...<větev>. Přečti
tyhle soubory — pravidla, podle kterých je posoudíš, se ti do kontextu
vloží samy podle jejich cesty. Sleduj je jako zdroj principů, ne univerzální
seznam z hlavy. Neopravuj nic — vracíš verdikt.

Nálezy piš jako konkrétní adresný pokyn („oprav tenhle řádek", „oprav
tenhle blok") s cestou k souboru, bez rozepisování nad rámec toho, co
pravidlo v kontextu skutečně říká. Report je stručný: nemáš-li nález, napiš
„Bez nálezů." — nerozepisuj, co je v pořádku ani proč. Report ukonči třemi
řádky přesně v tomhle tvaru:
Přečtené soubory: <cesty, čárkou oddělené>
Pravidla v kontextu: <cesty, čárkou oddělené | žádné>
Blokuje merge: ano|ne
```

### Dodatek pro retry

```
PR #<číslo> se vrátilo z review. Oprav v téže větvi (<větev>) tyto nálezy:

<nálezy doslova, u každého recenzent, od kterého pochází>

Kritérium, které selhalo, pokryj regresním testem a ten test MUTAČNĚ OVĚŘ:
dočasně vrať chybu, spusť test a potvrď, že spadne; chybu oprav a potvrď, že
projde. V reportu výslovně napiš, co jsi dočasně změnil a jak test v obou
stavech dopadl — bez té věty považuj práci za nedokončenou.

Nezakládej novou větev ani nové PR.
```

### Tělo integračního PR

Předává se skillu `open-pr` v kroku 10 jako hotový text:

```markdown
Milestone: <název>

Zahrnuje:
- #<číslo> — <název issue>
- …

Eskalované a nezahrnuté: <#číslo — důvod, nebo „žádné">
```

### Hlášení na předělech

Krátce, jen na skutečných předělech — ne komentář ke každému volání nástroje:

```
Dávka <n>: dispečováno #A, #B, #C.
Dávka <n>: zmergováno #A, #B; #C eskalováno — <důvod>.
Dávka <n>: #<PR> ověřeno jen částečně — <chybějící pravidla | přeskočený ověřovací příkaz>.
Eskalace: <co se stalo, co to blokuje> — <konkrétní otázka>.
```

## Zásady

- **Nepíšeš kód a nedáváš známky.** Opravit nález sám nebo si PR posoudit vlastní hlavou
  je rychlejší jen zdánlivě: ruší nezávislost, kvůli které review existuje.
- **Do výchozí větve sám nemergeuješ.** Ani squashem, ani „jen tenhle jeden", ani na
  přání během běhu. Mergnout tam smí jen `open-pr`, a jen když souhlas stál v promptu,
  kterým `run-milestone` začal — to je jediný způsob, jak se výjimka smí uplatnit.
- **Rozhoduje strojově čitelný řádek, ne próza.** Verdikt review milestonu, číslo PR
  a `Blokuje merge: ano/ne` jsou jediné vstupy, podle kterých se rozhoduje; jejich absence
  je selhaný dispatch, ne souhlas.
- **Status není výsledek.** Hotovo je až to, co jsi ověřil ve forge — u dispatche existencí
  PR, u merge zavřeným issue, u závěru přiřazeným milestonem.
- **Stav drží tracker, ne tvoje paměť.** Proto jde běh přerušit a navázat; proto se
  rozpracovanost čte z issues a PR, ne z toho, co si pamatuješ z předchozí dávky.
- **Hlas na předělech a nevymýšlej si.** Dokud notifikace nedorazila, o běžícím agentovi
  nevíš nic — a domnělý stav se od skutečného pozná až u merge.
