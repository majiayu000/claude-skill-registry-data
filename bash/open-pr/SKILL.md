---
name: open-pr
description: >-
  Otevře pull request pro práci na aktuální větvi — zjistí forge a základní
  větev z projektové konfigurace, nezapsané změny nechá zapsat a odeslat přes
  make-commit, sestaví název podle Conventional Commits a krátké tělo
  s odkazem na uzavírané issue, založí PR podle sdílených receptů a případně
  mu druhým voláním přiřadí milestone. Obsahoval-li prompt, kterým byl
  aktuální běh spuštěn, výslovný souhlas k mergi, PR i rovnou mergne. Výstupem
  je číslo a odkaz PR, případně i výsledek merge.
when_to_use: >-
  Použij, když má z odvedené práce vzniknout pull request — „otevři PR",
  „udělej z toho pull request", „pošli to na review" — a jako sdílený závěrečný
  krok skillů, které odvedly práci na větvi — implement-issue u jednotlivého
  issue, run-milestone u závěrečného PR celého milestonu.
  Nepoužívej pro pouhé zapsání a odeslání změn bez PR, na to slouží make-commit;
  ani pro založení pracovní větve, na to slouží create-branch; ani pro
  implementaci issue — tu vlastní implement-issue, který řeší obsah práce,
  kdežto tenhle skill jen mechaniku PR. Bez projektové konfigurace workflow
  skill PR nezakládá a odkáže na init-workflow.
argument-hint: "[základní větev, číslo issue, milestone nebo popis práce]"
model: sonnet
effort: medium
# Zařazení dle matice: dobře ohraničené zadání se známým tvarem výstupu →
# sonnet × medium (bod 2 rozhodovacího stromu), bez odchylky. Nikoli opus:
# matice velí rozhodovat podle nejtěžší práce, kterou skill dělá sám — obsah
# změn vlastní volající, commit deleguje na make-commit a skill drží jen
# mechaniku. Nikoli low: postup má osm kroků, dvě forge větve a několik stavů,
# které selhávají tiše (nepushnutá větev, duplicitní PR, nepřiřazený milestone).
# Varování matice u medium („nevol u rozhodnutí, která se těžko vrací zpět")
# tady neplatí naplno: PR se zavírá jedním kliknutím a publikaci větve dělá
# cizí skript. Merge do výchozí větve nevratný je, ale brzdou proti němu je
# prokazatelný výslovný souhlas v promptu (krok 8), ne neschopnost mergovat.
# Odchylka od konvence pojmenování: tabulka sloves zná pro nový artefakt
# `write`/`create`, ale forge i uživatel říkají „otevři PR"; `open-pr` proto
# trefí spouštěcí frázi líp než `create-pr`.
user-invocable: true
# Vynechaná zvažovaná pole: allowed-tools — sada nástrojů se liší podle forge
# a na Gitea jde o odložené `mcp__gitea__*` načítané za běhu přes ToolSearch;
# uzavřený výčet by je nepokryl a gitea větev by tiše spadla při zakládání PR.
# Hranicí je tady podmínka výslovného souhlasu v Zásadách, ne zúžení práv;
# disable-model-invocation — automatické vyvolání na konci implement-issue je
# celý smysl skillu a PR je vratný artefakt (dá se zavřít);
# context/agent/background — název a tělo PR se píšou z kontextu odvedené
# práce a commit se dělá ve sdíleném pracovním stromu volajícího, fork by
# obojí rozbil; paths — spouští se z konverzace nebo z jiného skillu, ne prací
# nad konkrétními soubory; shell — skripty se spouští explicitním `bash`;
# disallowed-tools — bez allowed-tools by šlo o výčet bez protějšku;
# version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Open PR

Cílem je pull request otevřený proti správné základní větvi, s názvem a tělem,
ze kterých je poznat, co se mění a co se tím zavírá. Git mechaniku skill sám
nepíše — commit a push deleguje na `sagittaras:make-commit`, zakládání větve na
`sagittaras:create-branch`. Závazným kontraktem jsou sdílené soubory pluginu;
při rozporu s tímhle postupem platí ony.

| Soubor | Kdy ho otevři |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` | V kroku 1, když projektová konfigurace chybí nebo v ní nenajdeš sekci `Forge` či `Větvení` |
| `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` | V kroku 1 před prvním voláním skriptu — pro argumenty a návratové kódy `forge-detect.sh` a `gh/*.sh` |
| `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` | V kroku 6, dřív než sáhneš na tracker — včetně sekce s nástrahami |

Obsah sdílených souborů si **přečti, ale nepřepisuj do odpovědi**. Recepty se
mění na jednom místě; kopie v konverzaci zastará a další běh podle ní založí PR
jinak.

## Vstupní kontext

- Zadání od volajícího (může být prázdné): $ARGUMENTS

Ze zadání vytěž, co v něm je: **základní větev**, **číslo issue**, které PR
uzavírá, **milestone**, do kterého PR patří, a **výslovný souhlas k mergi**
(fráze jako „a mergni", „udělej i merge", „vytvoř PR a slej to", „a rovnou
zmerguj"). Co v zadání není, doplň postupem níže — ale nikdy nepřebíjej to,
co volající předal.

**Souhlas k mergi musí být explicitní a musí pocházet z promptu, kterým byl
aktuální běh spuštěn** — dispečuje-li tě `run-milestone` nebo `implement-issue`,
souhlas hledej v zadání, které ti předaly ony (musí ho samy přenést z původního
promptu uživatele, jinak ho nemáš odkud vzít). Domněnka z kontextu konverzace
nestačí: „otevři PR" bez dalšího slova souhlas k mergi neznamená.

**Skill běží často neinteraktivně**, spuštěný na konci jiné úlohy. Celý postup
je proto napsaný tak, že se uživatele neptá — jediné místo, kde k němu míří
otázka, je Eskalace v kroku 10.

## Postup

### 1. Načti konfiguraci a zjisti stav

Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni cílového
projektu. Potřebuješ podsekci **Forge** (kterou větev receptů použít a jaké
`owner/repo` předat) a **Větvení** (výchozí větev, tvar integrační větve,
a že do výchozí větve mergeuje jen člověk).

- **`CONTRIBUTING.md` neexistuje nebo sekci nemá** → nepokračuj a nedomýšlej si
  hodnoty. Řekni to a nabídni `/sagittaras:init-workflow`.
- **Chybí podsekce, kterou potřebuješ** → řekni která a nabídni doplnění; sám ji
  za pochodu nedoplňuj.

Pak zjisti stav repozitáře:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/forge-detect.sh"
```

Reaguj podle návratového kódu:

- **2 `not_a_git_repository`** → ohlas a skonči.
- **3 chybějící remote nebo neodvoditelné `owner/repo`** → ohlas a skonči. PR
  je operace nad remotem; lokální repozitář bez něj nemá kam PR založit.
- **`forge=unknown`** → typ forge ber ze sekce `Forge` konfigurace, ta je pro
  výběr receptů stejně autoritativní. Chybí-li ale i `owner`/`repo`, zastav se —
  volání by nemělo kam mířit.

Liší-li se `owner/repo` z detekce od konfigurace, **nehádej, který je správný**
a ohlas rozpor: obvykle to znamená, že běžíš nad jiným repozitářem, než pro
který konfigurace platí, a PR by vzniklo jinde.

Nakonec si přečti stav pracovní kopie:

```bash
git branch --show-current
git status -sb --porcelain
```

Z `git status -sb` vyčteš zároveň upstream a předstih větve (`[ahead N]`) —
obojí potřebuješ v krocích 4 a 5 a bez upstreamu nemá `origin` co porovnávat.
Přímé volání `git` je tu v pořádku právě proto, že **nic nemění** — všechno, co
do repozitáře zapisuje, jde přes delegované skilly.

### 2. Urči větev, ze které PR poroste

Volající obvykle už na své větvi stojí. **Pak ji použij a novou nezakládej** —
její commity by na nové větvi nebyly a PR by vzniklo prázdné.

- **Jsi na jiné než výchozí větvi** → to je head PR, jdi dál.
- **Jsi na výchozí větvi a máš nezapsané změny** → není na čem stavět, sáhni
  po `sagittaras:create-branch` (změny přeberou s sebou) a pokračuj na nově
  založené větvi. **Předej mu hotový název** ve tvaru `<type>/<popis>`
  odvozený z rozpracovaných změn — bez něj si ho nechá potvrdit uživatelem
  a v autonomním běhu se zastaví. Skončí-li `create-branch` s `checkout_failed`,
  větev nevznikla a zůstáváš na výchozí; ohlas to a nepokračuj.
- **Jsi na výchozí větvi a všechno je zapsané** → zastav se a ohlas to.
  Přesunout hotové commity z výchozí větve jinam je zásah do historie, který
  tenhle skill záměrně neumí.
- **Odpojená HEAD** → zastav se a ohlas to. Commit i větev by se ztratily při
  prvním přepnutí.

### 3. Urči základní větev

Základ PR je větev, **ze které se práce vyvíjela**:

- **Předal-li ji volající** (typicky integrační větev `milestone/<slug>`
  v milestone běhu), platí jeho hodnota. Výchozí větev z konfigurace si v tom
  případě **nedomýšlej** — PR mířící mimo integrační větev obejde integrační
  bránu `run-milestone` a zamíří rovnou do výchozí větve.
- **Jinak** vezmi výchozí větev ze sekce `Větvení`.

Že má head větev proti základní vůbec nějaký commit, ověřuj **až po kroku 4** —
volající typicky předává práci ještě nezapsanou a v tuhle chvíli by kontrola
zastavila i běh, který je úplně v pořádku.

### 4. Zapiš a odešli rozdělanou práci

Je-li pracovní strom čistý a větev už pushnutá (upstream i nulový předstih
z kroku 1), krok přeskoč. Jinak zavolej nástrojem `Skill` skill
`sagittaras:make-commit`. **Vlastní commit logiku nepiš** — rozdělení do celků,
formát zprávy i push jsou jeho práce a psát je podruhé znamená dvě různá
pravidla pro tutéž věc.

Publikaci větve si vyžadovat nemusíš — `make-commit` pushuje po každém commitu
a větev bez upstreamu sám publikuje. **Push mu proto nezakazuj**: nad nepushnutou
větví PR založit nejde.

Skončí-li `make-commit` přesto s nepublikovanou větví, **zastav se a eskaluj**.
Nedopushovávej ji sám: publikace je jeho výchozí chování, takže její absence
znamená překážku, kterou ohlásil (chybí remote, remote push odmítl) — a obejít
ji vlastním pushem znamená publikovat větev, o které nevíš, proč publikovaná
není.

Ohlásí-li `make-commit`, že **necommitnul** (zastavil se na brzdě, odmítl commit
hook), **zastav se a ohlas příčinu**. Commit kolem něj neobcházej.

Teď ověř, že head větev má proti základní aspoň jeden commit navíc:

```bash
git fetch origin <base> && git rev-list --count "origin/<base>..HEAD"
```

Porovnávej **proti remote refu**, ne proti lokální větvi: základní větev
v milestone běhu často lokálně vůbec není a zastaralý ref vydá věrohodně
vypadající špatné číslo. Vyjde-li `0`, nezakládej nic a ohlas to — prázdné PR
obě forge založí, ale nemá co recenzovat.

### 5. Sestav název a tělo

**Název** je Conventional Commit odpovídající odvedené práci, ve stejném tvaru
jako názvy issues: `<type>(<scope>): <popis>`. Uzavírá-li PR právě jedno issue,
**vezmi jeho název doslova** — tracker pak ukazuje tentýž řetězec dvakrát a nic
se nerozchází. Jinak ho odvoď ze zapsaných commitů, ne ze zadání.

**Tělo** piš podle Formátu výstupu: krátké shrnutí a `Closes #N`, jen když PR
opravdu nějaké issue uzavírá.

Na GitHubu ho zapiš do dočasného souboru **mimo pracovní strom repozitáře** —
soubor uvnitř stromu by skončil jako nesledovaná veteš v příštím commitu. Zapisuj
heredocem s ukončovačem v uvozovkách ve stejném volání, ve kterém soubor vznikne,
jinak shell expanduje `$` a zpětné apostrofy a do PR dorazí něco jiného, než jsi
napsal:

```bash
f="$(mktemp)"; cat >"$f" <<'BODY'
<tělo>
BODY
echo "body_file=$f"
```

Po založení PR soubor smaž. Na Gitea tenhle mezikrok odpadá — tělo se předává
přímo parametrem volání a žádný shell v cestě není.

> `Closes #N` zabírá na obou forge až při merge do **výchozí** větve. V milestone
> běhu, kde PR míří do integrační větve, se tím issue nezavře; odkaz tam má
> smysl jako vazba, zavření vlastní `run-milestone` a `close-milestone`.

### 6. Založ PR

Otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`, vyber sloupec podle
sekce `Forge` z konfigurace a **volání neodvozuj z hlavy**. Na Gitea si nejdřív
**jedním** voláním `ToolSearch` načti odložené nástroje podle řádku „Pracuje
s PR".

**Každý `gh` skript potřebuje `-R <owner/repo>`** ze sekce `Forge` konfigurace.
Bez něj skončí kódem `2` — a řídit se aktuálním adresářem nemůže, protože
v izolovaném worktree `run-milestone` nemusí ukazovat na správný repozitář.

Než PR založíš, vypiš otevřená PR a podívej se, jestli už z téhle head větve
jedno neexistuje — na GitHubu `bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-list.sh"
-R <owner/repo> --state open` a porovnání pole `headRefName` ve vráceném JSON, na
Gitea `list_pull_requests` se `state: "open"` a totéž porovnání. Recepty řádek
„najdi PR podle head větve" nemají, tak je tady doslova.

Existuje-li takové PR, **nezakládej druhé** — vrať to stávající a skonči
úspěchem. Opakované spuštění po přerušeném běhu je normální stav, duplicitní PR
nad jednou větví ne. Liší-li se ale u stávajícího PR `baseRefName` od základní
větve z kroku 3, jde o rozpor, který sám nerozsoudíš: eskaluj.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-create.sh" -R <owner/repo> \
  --base <base> --head <head> --title <název> --body-file <cesta k tělu>
```

Tělo předávej `gh` skriptům **vždy souborem** (`--body-file`), nikdy argumentem:
víceřádkový markdown se v shellu o uvozovky a zpětné apostrofy rozbije, a rozbije
se tiše. Na Gitea shell v cestě není — tam předej `pull_request_write` **obsah**
těla přímo v parametru `body` a dočasný soubor nezakládej vůbec.

Skript vrátí `number=` a `url=`. Kód `2` je chybné volání, ne odmítnutí forge:
oprav argumenty (typicky chybějící `-R`) a teprve pak opakuj — opakování beze
změny selže znovu. Kód `7` znamená chybějící `gh` nebo přihlášení; řekni to
rovnou, ne až po dalších krocích. U chyby 404 na zápisu ověř oprávnění účtu
podle nástrah v receptech; jiný repozitář nezkoušej.

### 7. Přiřaď milestone

Patří-li PR do milestonu, přiřaď mu ho **druhým voláním** hned po založení.
Tvar argumentů vezmi z řádku „Přiřaď PR milestone" v receptech — identifikátor
se mezi forge liší (`gh` skript bere **název** milestonu, Gitea `update` číselné
id) a záměna je jedna z tamních nástrah. `gh` větev nezapomene `-R <owner/repo>`.

Při zakládání to nejde ani na jedné forge a není to kosmetika: `close-milestone`
podle téhle vazby integrační PR dohledává.

Selže-li přiřazení, **PR nerušit** — už existuje a je platné. Ohlas jeho číslo
spolu s tím, že milestone přiřazený není, ať to jde doplnit jedním voláním;
mlčky přejít se to nedá, `close-milestone` by pak milestone nezavřel.

Nepatří-li PR do milestonu, krok přeskoč.

### 8. Proveď merge, obsahoval-li prompt výslovný souhlas

Nenašel-li krok „Vstupní kontext" v promptu, kterým byl aktuální běh spuštěn,
výslovný souhlas k mergi, **krok přeskoč** — PR zůstává otevřené, to je
současné chování beze změny.

Souhlas našel → mergni podle řádku „Mergni PR" v receptech, strategií ze
sekce `Větvení` (squash) a se smazáním zdrojové větve:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-merge.sh" <n> --squash --delete-branch
```

Mergovat smíš **do jakékoli základní větve** — souhlas v promptu je přesně ta
výjimka, kterou řádek `merge do výchozí větve: jen člověk` v sekci `Větvení`
připouští; bez tohohle kroku by řádek platil bez výjimky. Neplyne z toho nic
o integrační bránu `run-milestone` — ta svůj vlastní merge do integrační větve
provádí sama (jeho vlastní krok 8), tenhle krok se týká jen PR, které
zakládáš ty.

`result=conflict` nebo jiné nenulové selhání merge **neobcházej** — PR zůstává
otevřené a nemergnuté, ohlas to v souhrnu a eskaluj podle kroku 10. Nezkoušej
force merge ani jiný recept.

### 9. Shrň výsledek

Vypiš souhrn podle Formátu výstupu: číslo a odkaz PR, base a head větev, co
uzavírá, přiřazený milestone, výsledek merge (proveden, nebo „neprovádí se")
a co jsi cestou přeskočil nebo delegoval. **Merge nenabízej jako svůj další
krok** — bez souhlasu v promptu se tady skill zastavuje.

### 10. Eskalace

Přeruš postup a ohlas stav, nastane-li kterákoli z těchto situací:

- chybí projektová konfigurace nebo v ní chybí sekce `Forge` či `Větvení`;
- `forge-detect.sh` skončí kódem `2` nebo `3`, nebo nezná `owner`/`repo`;
- `owner/repo` z detekce se liší od konfigurace;
- stojíš na výchozí větvi se vším zapsaným, nebo na odpojené HEAD;
- `create-branch` větev nezaložil (`checkout_failed`);
- `make-commit` necommitnul, nebo větev zůstala nepublikovaná;
- head větev nemá ani po kroku 4 proti základní žádný commit navíc;
- z téhle head větve už existuje otevřené PR proti **jiné** základní větvi
  (shodné PR není důvod k eskalaci — vrať ho a skonči);
- PR vzniklo, ale přiřazení milestonu selhalo;
- prompt obsahoval souhlas k mergi, ale merge v kroku 8 selhal (konflikt,
  odmítnutí forge);
- forge vrátí 404 nebo `gh` chybí či není přihlášené.

Eskalace vždy shrne, co už vzniklo (commit, větev, PR), a položí **jednu
konkrétní otázku** nástrojem AskUserQuestion. Selže-li volání nebo odpověď
nedorazí, je uživatel mimo hru: nezakládej nic dalšího a stav jen ohlas —
nezaložený PR se doplní jedním během, kdežto zbloudilý PR proti výchozí větvi
uklízí někdo ručně.

## Formát výstupu

**Tělo PR** (krok 5) — `Closes` řádek vynech, když PR žádné issue neuzavírá:

```markdown
<jedna až tři věty: co PR mění a proč, bez výčtu souborů>

Closes #<n>
```

**Souhrn** (krok 9) — řádek `Merge` má dvě platné podoby:

```
PR #<číslo>: <název> — <url>

| | |
| --- | --- |
| Base | <základní větev> |
| Head | <pracovní větev> |
| Uzavírá | #<n>, nebo „—" |
| Milestone | <název>, nebo „—" |

Commity: <počet, nebo „nic nového k zapsání">
Merge: neprovádí se
```

Obsahoval-li prompt souhlas a merge v kroku 8 prošel, poslední řádek nahraď:

```
Merge: proveden — squash do <základní větev>, zdrojová větev smazána
```

## Zásady

- **Skill mergne jen na výslovný souhlas v promptu, jinak nikdy.** Merge do
  integrační větve vlastní `run-milestone` sám; do výchozí větve mergne
  `open-pr` výhradně tehdy, když prompt, kterým byl aktuální běh spuštěn,
  obsahoval výslovný souhlas k mergi (krok 8). Bez něj je výstupem jen
  otevřené PR, stejně jako dosud.
- **Základní větev se nedomýšlí.** Co předal volající, platí; výchozí větev
  z konfigurace je až fallback.
- **Git mechanika se deleguje bez výjimky.** Commit, push i publikace větve přes
  `sagittaras:make-commit`, větev přes `sagittaras:create-branch`. Napsat je
  potřetí znamená tři různá chování téže operace.
- **Jedna head větev, jedno PR.** Před zakládáním se ověřuje, že už neexistuje.
- **Tělo `gh` skriptům vždy souborem, nikdy argumentem.** Na Gitea, kde shell
  v cestě není, se předává obsah přímo.
- **Repozitář se `gh` skriptům předává `-R owner/repo`.** Aktuální adresář
  v izolovaném worktree nemusí být ten repozitář, o který jde.
- **Sdílený kontrakt má přednost.** Odporuje-li tenhle postup receptům,
  konfiguraci nebo kontraktu skriptů, platí ony.
