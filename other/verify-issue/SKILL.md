---
name: verify-issue
description: >-
  Nezávisle ověří, že PR splňuje akceptační kritéria svého issue — spustí
  ověřovací příkazy, porovná změnu s precedentem citovaným v Referencích
  a kritéria opřená o nový regresní test mutačně otestuje. Odškrtne v těle issue jen to,
  co doopravdy ověřil. Report s verdiktem a strojově čteným řádkem
  „Blokuje merge: ano/ne" uloží jako komentář k PR. Nic neopravuje.
when_to_use: >-
  Použij k ověření hotového PR proti kritériím jeho issue — v milestone běhu
  jako akceptační brána před merge, ručně když uživatel řekne „ověř, jestli to
  PR splňuje issue", „zkontroluj akceptační kritéria" nebo „projdi PR proti
  zadání". Nepoužívej pro posouzení plánu milestonu před implementací, na to
  slouží review-milestone; ani pro obecné code review kvality, stylu
  a architektury, ta tenhle skill neposuzuje; ani pro opravu nálezů, tu dělá
  implement-issue; ani pro povýšení Poznámky na Zadání ukotvené v kódu před
  implementací, to dělá triage-issue.
argument-hint: "[číslo issue, nebo číslo PR / název větve]"
# Odchylka od tabulky sloves v konvencích, kde se posuzování existujícího stavu
# jmenuje review/check: `verify` je vědomé, protože review-* v této sadě posuzují
# plán a kvalitu, kdežto tenhle skill dokazuje splnění kritérií. Název navíc
# fixuje .docs/workflow-skills-plan.md a odkazuje se na něj sdílený kontrakt.
context: fork
model: opus
effort: high
# Zařazení dle matice: review a hledání chyb → opus × xhigh; tady opus × high,
# tedy o stupeň níž, shodně s plánem sady. Běh je nesporně agentic — worktree,
# revert patche, opakované spouštění testů — ale rozpadá se na krátká,
# navzájem nezávislá ověření, u nichž je předem dané, co je důkaz; hloubka,
# kterou xhigh přidává, se utrácí za plánování dlouhého záměru, a ten tu není.
# Opus zůstává: cena přehlédnutého nesplněného kritéria je celý špatný merge.
# Ukáže-li první reálný běh, že ověření vypadávají nedotažená, zvedni na xhigh.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - ToolSearch
  - mcp__gitea__issue_read
  - mcp__gitea__issue_write
  - mcp__gitea__pull_request_read
  - mcp__gitea__list_pull_requests
  - mcp__gitea__pull_request_review_write
disallowed-tools:
  - AskUserQuestion
# Bash je záměrně nezúžený: ověřovací příkazy jsou libovolné příkazy projektu
# z konfigurace (`dotnet build`, `pnpm test`, …) a užší vzor by je zablokoval.
# Zákaz zásahu do kódu proto nenese `Bash`, ale absence Write/Edit a Zásady.
# Výčet `mcp__gitea__*` je užší než řádky v tabulce receptů a musí takový
# zůstat: `pull_request_write` (merge, zavření, úprava PR) do read-only
# ověřovatele nepatří ani načtený, proto ho krok 1 ani nenačítá.
# disallowed-tools je při uzavřeném allowed-tools redundantní záměrně: běžíš-li
# jako subagent, allowed-tools se nemusí uplatnit, a zákaz doptávání musí platit
# vždy — skill běží bez uživatele.
# Vynechaná zvažovaná pole: Write/Edit/NotebookEdit v allowed-tools — skill
# zásadně neopravuje (viz Zásady) a i dočasnou mutaci v kroku 5 dělá gitem, ne
# editorem; soubor s reportem vzniká heredocem v Bash, což je payload pro forge,
# ne zásah do repozitáře. agent — profil žádného z dostupných agentů nesedí
# (skill potřebuje spouštět příkazy a zapisovat do trackeru), a plánovací
# systémový prompt by běh táhl k navrhování opravy, což je přesně to, co tenhle
# skill dělat nesmí; omezení práv nese allowed-tools. background — volající
# čeká na verdikt, běh na pozadí by milestone smyčku rozpojil.
# disable-model-invocation — skill musí zůstat volatelný modelem, spouští ho
# run-milestone. paths — pracuje podle čísla v argumentu, ne nad konkrétními
# soubory. shell — příkazy se spouští přes Bash s pracovním adresářem
# nastaveným na vlastní worktree. version, license — verzuje se celý plugin,
# ne jednotlivý skill.
---

# Verify Issue

Cílem je nezávislý **důkaz**, že PR splňuje akceptační kritéria svého issue — ne
dojem, že je splňuje. Běžíš ve forku s čistým kontextem a je to záměr: ověřovatel,
který sdílí kontext se session, jež kód psala, si odkývá její vlastní úvahu
a přehlédne přesně to, co přehlédla ona; o té session tedy nepředpokládej nic.
Závazným kontraktem jsou sdílené soubory v `${CLAUDE_PLUGIN_ROOT}/shared/`; při
rozporu s tímto skillem mají přednost ony.

## Vstupní kontext

- Zadání od volajícího: $ARGUMENTS

Zadání je odkaz na jednu stranu dvojice issue ↔ PR: číslo issue, číslo PR, nebo
název větve. Druhou stranu dohledáš v kroku 2. Je-li zadání prázdné, nemáš co
ověřovat — řekni to a skonči.

## Postup

### 1. Načti konfiguraci a nástroje forge

Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni projektu.
Potřebuješ z ní podsekce **Forge** (typ, `owner/repo`), **Ověřovací příkazy**
(čím se kritérium doopravdy ověří), **Zdroje pravdy** (kde leží dokumenty,
cituje-li je Reference vedle kódu) a **Větvení** (výchozí a integrační větev).

Nevíš-li, kde v konfiguraci co hledat, nebo některá podsekce chybí, otevři
`${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md`. Chybí-li `CONTRIBUTING.md`,
sekce `## Workflow (sagittaras)` celá, nebo podsekce, kterou potřebuješ,
**nedomýšlej hodnoty**: skonči verdiktem `Blocked` a řekni, co chybí. Ověření
proti odhadnutému příkazu není ověření.

Než sáhneš na issue nebo PR, otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`
a volání ber z jeho tabulky — neodvozuj je z hlavy.

**Na Gitea projektech** si napřed načti odložené `mcp__gitea__*` nástroje, jinak
je nelze zavolat. Jedním voláním `ToolSearch` a přesně tímto výčtem:

```
select:mcp__gitea__issue_read,mcp__gitea__issue_write,mcp__gitea__pull_request_read,mcp__gitea__list_pull_requests,mcp__gitea__pull_request_review_write
```

Výčet je užší než řádky v tabulce receptů, a to záměrně: `pull_request_write`
umí PR mergnout i zavřít a do read-only ověřovatele nepatří ani načtený. Zároveň
se kryje s `allowed-tools` — cokoli navíc by se načetlo a pak neprošlo, což se
pozná až selháním uprostřed práce.

**Na GitHub projektech** voláš skripty z `${CLAUDE_PLUGIN_ROOT}/scripts/gh/`.
Tabulka receptů je uvádí zkráceně (`gh/pr-read.sh <n>`); doplň k nim kořen
pluginu a **povinné `-R <owner/repo>`** ze sekce Forge — bez něj se skript řídí
aktuálním adresářem, což ve vlastním worktree neplatí:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-read.sh" -R "<owner/repo>" <číslo PR>
```

Návratové kódy popisuje `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` — otevři ho,
až nějaký skript skončí nenulovým kódem. Kód `7` (`gh` chybí nebo není přihlášené)
je stav prostředí, ne nález na PR: skonči `Blocked`, ne `Nesplněno`.

### 2. Rozpoznej dvojici issue ↔ PR

Ověřuješ vždy dvojici. Chybí-li jedna strana, není co s čím porovnat.

1. **Argument je název větve** (není to číslo) → vypiš PR se `state: all`
   a vyber ten, jehož hlavová větev se jménu rovná — recept „Najdi PR podle
   head větve" z `forge-recipes.md`. Filtrování podle `head` neumí ani jedna
   forge jako parametr, takže filtruj až ve výstupu:

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-list.sh" -R "<owner/repo>" --state all
   # ve výstupním JSON hledej položku s headRefName == "<větev>"
   ```

   Na Gitea totéž nástrojem `list_pull_requests` se `state: "all"` a porovnáním
   pole `head`.
2. **Argument je číslo** → přečti ho a rozliš, co jsi dostal: má-li objekt `head`
   a `base`, je to PR, jinak issue. Číselné řady issues a PR jsou na obou forgích
   společné, takže z čísla samotného to poznat nejde. Na GitHubu zkus napřed
   `pr-read.sh` a rozhoduj se **podle návratového kódu, ne podle textu hlášky**
   (ten se mění s verzí `gh`): kód `1` znamená „tohle číslo není PR" → sáhni po
   `issue-read.sh`; kód `2` je chyba ve tvém volání, ne stav PR; kód `7` je
   prostředí → `Blocked`.
3. **Máš PR, chybí issue** → vezmi číslo z `Closes #N` v těle PR.
4. **Máš issue, chybí PR** → recept „Najdi PR patřící k issue" z
   `forge-recipes.md`, podle forge:
   - **GitHub** — issue, které jsi přečetl v kroku 2 (`issue-read.sh`), nese
     pole `closedByPullRequestsReferences`: přímá vazba na PR, který ho
     uzavírá, dohledávat `Closes #N` v tělech PR není potřeba.
   - **Gitea** — vypiš PR nástrojem `list_pull_requests` se `state: "all"`
     a najdi ten, jehož `body` obsahuje `Closes #<číslo issue>`.
   Nenajdeš-li nic, zkus shodu podle názvu větve.

Dvojici **nespojuj odhadem**. Nenajdeš-li protějšek, nebo vyjdou-li dva otevřené
PR na stejný issue, skonči verdiktem `Blocked` a napiš, co jsi hledal a co našel —
ověřit špatný PR je horší než neověřit žádný. Spároval-li jsi dvojici jen podle
podobnosti názvu větve, uveď to ve Výhradách k ověření (viz Formát výstupu).

Neznáš-li číslo PR, nemáš kam uložit komentář: report v takovém případě vrať jen
jako závěrečnou zprávu.

### 3. Přečti issue a jeho reference

Přečti **celé tělo issue**, ne jen checklist. Kde v těle co stojí a jak se
akceptační kritéria píší, popisuje `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` —
otevři ho teď, ať čteš tělo podle jeho sekcí a ne podle dojmu.

Sekce **Reference** cituje **precedent v kódu** — konkrétní soubor nebo vzor,
který issue rozšiřuje, cestou vůči kořeni repozitáře (**ne** vůči kořenům ze
sekce Zdroje pravdy; ty platí pro dokumenty). Otevři ho a přečti; je to zdroj
pravdy o tom, co mělo vzniknout. Parafráze v popisu PR ani v komentářích důkaz
není — právě věrohodně znějící parafráze bez opory v kódu je ta chyba, kterou
tenhle skill má chytit.

Cituje-li Reference **vedle kódu i dokument** (ADR, UX spec), otevři ho na cestě
podle sekce Zdroje pravdy a přečti citovanou sekci. Čti ho jako **doplňkové
omezení** — co nesahat, které rozhodnutí je chráněné — ne jako popis toho, co
mělo vzniknout; ten nese precedent.

Rozliš tři stavy, ať nehlásíš nález tam, kde žádný není:

- **Citovaná cesta v repozitáři neexistuje** (kód i dokument) → kritérium, které
  se o ni opírá, je `Neověřitelné` a v Doporučeních je to nález `[issue]`.
- **Precedent existuje a chování z kritéria v něm až do tohohle PR nebylo** →
  **není to nález**; přesně ten přírůstek issue přináší. Ověřuj, že ho PR dodal
  jako rozšíření precedentu, ne jako vzor postavený vedle něj.
- **Reference nemá žádný kódový precedent, jen odkaz na dokument** → kritéria
  opřená jen o prózu jsou `Neověřitelné` a v Doporučeních to hlas jako `[issue]`
  s doporučením `triage-issue`. Chybějící precedent je vada zadání, ne PR:
  nepiš to jako nález `[implement-issue]`.

**Neexistenci cesty potvrď až ve worktree PR z kroku 4**, ne v pracovní kopii,
ve které teď stojíš — ta může být na jiné větvi a precedent v ní chybět, i když
ho PR má. V milestone běhu je to běžný stav: precedent často zakládá teprve
issue, které doběhlo před tímhle, takže je jen v integrační větvi. Nález
`[issue]` z prvního bodu proto zapiš, až když cesta chybí i tam.

Poznamenej si `area:*` label issue — určuje, který ověřovací příkaz z konfigurace
platí. Nemá-li issue žádný `area:*` label, nebo nemá-li jeho oblast řádek v sekci
Ověřovací příkazy, **příkaz si nevymýšlej**: skonči `Blocked` a chybějící vazbu
uveď v Doporučeních jako nález na issue nebo na konfiguraci. Ověření spuštěné
odhadnutým příkazem tvrdí víc, než ví.

### 4. Vezmi si větev PR do vlastní pracovní kopie

Ověřuj nad kódem, ne nad výpisem diffu v trackeru. Založ si na to **oddělený
worktree**, aby pracovní strom, ve kterém běžíš, zůstal nedotčený — v milestone
běhu v něm může souběžně pracovat někdo jiný:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/pr-worktree.sh" pr-<číslo PR> <pr-head>
```

Skript vrátí `worktree=<cesta>`, `reused=` a `head=`. **Cestu si z výstupu přečti
a v každém dalším volání Bash ji napiš znovu celou** — mezi voláními nástroje
přežívá jen pracovní adresář, ne stav shellu, takže shellová proměnná nastavená
teď bude příště prázdná. Cesta je odvozená od labelu deterministicky, takže je
napodruhé stejná; opakované volání skriptu tentýž worktree převezme
(`reused=true`) i s obnovenými závislostmi. Totéž platí pro `base` v kroku 5 —
i ten si pokaždé spočítej znovu.

Kód `2` s `error=ref_not_found` znamená, že head větev PR v repozitáři není —
typicky u PR z forku, viz omezení na konci kroku.

Všechny příkazy pak spouštěj s pracovním adresářem `$wt`. Rozsah změny si zjisti
jako `git -C "$wt" diff "origin/<pr-base>...origin/<pr-head>"`.

**Čerstvý worktree neobsahuje ignorované artefakty** — `node_modules`, `obj/`,
`bin/`, virtualenv, staženou cache. Ověřovací příkaz v něm spadne na prostředí,
ne na kódu, a to je nejzrádnější falešný nález celého skillu: `run-milestone` by
za něj spálil retry rozpočet na PR, se kterým nic není. Než pustíš první
ověřovací příkaz, obnov závislosti tím, co repozitář používá (`pnpm install
--frozen-lockfile`, `dotnet restore`, `uv sync`, …); poznáš to z lockfilu
a manifestu. Jsou-li závislosti nainstalované v pracovní kopii, ze které jsi
worktree založil, je levnější je do `$wt` nakopírovat než stahovat znovu.

Uvnitř worktree pak git voláš přímo, ale drž se výhradně **čtecích a lokálních**
operací: žádný commit, žádný push, žádný merge, žádné mazání větví. Worktree stojí
na odpojené HEAD právě proto, aby se do něj commitovat nedalo omylem.

Až budeš hotov, ukliď ho — **v kroku 8, dřív než uložíš report**, i když
ověřování skončilo `Blocked`:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/pr-worktree.sh" --remove pr-<číslo PR>
```

Vrátí-li `removed=false`, adresář drží běžící proces; uveď to ve Výhradách
k ověření (viz Formát výstupu), ať po tobě někdo uklidí.

Nedá-li se větev PR získat, skonči verdiktem `Blocked`. **PR z forku tímhle
postupem ověřit nejde** — `git fetch origin <větev>` dosáhne jen na větve téhož
repozitáře. V reportu to pojmenuj jako strukturální omezení skillu, ne jako
výpadek nebo vinu PR.

### 5. Ověř každé kritérium zvlášť

Tohle je jádro práce. **Zaškrtnuté políčko není důkaz** — kdo ho zaškrtl a proč,
nevíš a vědět nemáš.

Nejdřív spusť ověřovací příkaz pro `area:*` issue, i když ho žádné kritérium
nejmenuje. Neprojde-li build nebo testovací sada, není doopravdy ověřené žádné
kritérium o chování — a výsledek zapiš, ať kritéria dopadnou jakkoli.

**Rozliš selhání kódu od selhání prostředí.** Ukazuje-li výstup na prostředí
(nenalezený balíček, chybějící toolchain nebo SDK, prázdné `node_modules`,
nedostupná síť), **není to nález na PR**: doplň, co chybí (viz krok 4), a teprve
nepovede-li se to, skonči `Blocked` s popisem toho, co v prostředí schází.
Nikdy z toho nedělej `Nesplněno` — opravit prostředí není v moci
`implement-issue` a retry by jen zopakoval totéž. Totéž platí pro každý běh
příkazu v mutačním testu níže.

Pak projdi checklist **řádek po řádku** a ke každému si vyžádej vlastní důkaz
podle jeho povahy:

| Kritérium jmenuje… | Důkaz |
| --- | --- |
| příkaz, build, lint nebo testy | příkaz z konfigurace **skutečně spusť** a zapiš jeho výstup |
| existenci něčeho v kódu | otevři soubor a přečti to místo; uveď cestu a řádek |
| rozšíření precedentu z Reference | otevři precedent **znovu** a porovnej ho se změnou v PR: je přírůstek psaný jeho vzorem, nebo vedle něj? Uveď `cesta:řádek` obojího |
| sekci dokumentu (doplňkové omezení) | přečti tu sekci **znovu** a ověř, že ji implementace neporušuje |
| nový regresní test | **mutačně otestuj** (viz níže) |

Pass/fail **nikdy nedovozuj z popisu PR ani z commit messages.** Tvrzení autora
je hypotéza, ne výsledek.

Porovnání s precedentem **není code review** a tvůj mandát nerozšiřuje: ptáš se
jen na to, jestli kritérium skutečně stojí na tom, o co se opírat mělo. Že by
se rozšíření dalo napsat elegantněji, do reportu nepatří ani jako poznámka —
`Nesplněno` je až tehdy, když přírůstek precedent obchází natolik, že kritérium
o rozšíření přestává platit.

**Mutační test.** Test, který nikdy nespadne, nehlídá nic — a kritérium, které
tvrdí, že ho hlídá, pak není splněné. Ověř to tak, že vrátíš produkční změnu
a necháš test běžet:

```bash
base="$(git -C "$wt" merge-base "origin/<pr-base>" HEAD)"
git -C "$wt" diff "$base" HEAD -- <produkční soubory, bez testů> | git -C "$wt" apply -R
<testovací příkaz>            # musí SPADNOUT
git -C "$wt" checkout -- .    # obnovení
git -C "$wt" status --porcelain   # musí být prázdné
<testovací příkaz>            # musí PROJÍT
```

Revert dělej **gitem, ne editací souborů** — obnovení je pak deterministické
a ověřitelné, kdežto ručně vrácená chyba se v pracovní kopii snadno zapomene.
Do revertu ber jen produkční soubory; nový test musí zůstat.

Vyhodnocení a hraniční stavy:

- Projde-li test i s vrácenou produkční změnou, je kritérium **`Nesplněno`** —
  test nehlídá to, co o něm kritérium tvrdí.
- Selže-li místo testu build, důkaz nemáš — zúž revert na menší celek (jeden
  soubor, jeden hunk), a nepovede-li se to, zapiš `Neověřitelné` i s důvodem.
- **Selže-li samo `git apply -R`** (binární soubor, nepoužitelný kontext),
  mutaci neprovedeš: kritérium je `Neověřitelné` a napiš, na čem revert ztroskotal.
- **Není-li `git status --porcelain` po obnovení prázdný**, worktree zahoď
  a založ ho znovu z `origin/<pr-head>` — a **znovu obnov závislosti podle
  kroku 4**, jinak další ověřovací příkaz spadne na prostředí. Neobnovený strom
  by se nepozorovaně nesl do všech dalších ověření a znehodnotil by je tiše,
  což je horší než spadnout.

**Nejednoznačné kritérium je samo o sobě nálezem.** Jde-li přečíst dvěma způsoby
nebo není ověřitelné vůbec, zapiš `Neověřitelné` a napiš, které dva výklady
připadají v úvahu. Nedomýšlej, co asi mělo znamenat — domyšlený výklad ověří
něco jiného, než co zadání říkalo, a chyba pak vypadá jako splněné kritérium.

Každému kritériu přiřaď právě jeden výsledek: **Splněno**, **Nesplněno**, nebo
**Neověřitelné**.

### 6. Stanov verdikt

| Verdikt | Blokuje merge | Kdy |
| --- | --- | --- |
| **Pass** | `ne` | všechna kritéria `Splněno` |
| **Needs work** | `ano` | ověřování proběhlo, ale aspoň jedno kritérium je `Nesplněno` nebo `Neověřitelné` |
| **Blocked** | `ano` | ověřování nešlo provést jako celek — chybí konfigurace nebo její sekce, issue nemá `area:*` label nebo jeho oblast nemá ověřovací příkaz, nedohledal jsi protějšek, větev PR nelze získat, ověřovací příkaz nejde v prostředí spustit |

Kombinace `Pass` + `ano` ani `Needs work` + `ne` neexistuje. Chceš-li některou
napsat, je špatně **verdikt**, ne ten řádek: nesplněné kritérium, které podle tebe
merge neblokuje, znamená, že je špatně to kritérium — hlas to jako nález
v Doporučeních a verdikt nezměkčuj.

Nezaokrouhluj nahoru. PR s jedním nesplněným kritériem není „skoro Pass".

### 7. Odškrtej ověřená kritéria v těle issue

Stav ověření patří do trackeru, ne jen do tvého reportu — jinak se při dalším
běhu ověřuje znovu všechno od nuly.

Přečti tělo issue **znovu, těsně před zápisem** (zápis nahrazuje celé tělo, takže
bys jinak přepsal, co mezitím přibylo). Pak v něm změň **jen zaškrtávátka**:

- kritérium `Splněno` → `- [ ]` přepiš na `- [x]`;
- kritérium `Nesplněno` nebo `Neověřitelné` → nech `- [ ]`, a bylo-li políčko
  zaškrtnuté, **odškrtni ho** — tracker musí ukazovat skutečný stav, a předem
  zaškrtnuté políčko je zároveň nález do reportu (Doporučení, `[issue]`).

Text kritérií ani ostatní sekce **nepřepisuj a nemaž**. Zápis proveď receptem
„Uprav tělo issue" z `forge-recipes.md`: na Gitea jde celé nové tělo v parametru
`body`, na GitHubu ho `issue-update.sh` bere jako `--body-file`, takže si ho
napřed ulož do dočasného souboru způsobem popsaným v kroku 8.

Ověř, že zápis prošel. Neprošel-li, kritéria zůstávají neodškrtnutá — samo
ověření tím platnost neztrácí, ale příští běh bude zbytečně ověřovat znovu:
uveď to ve Výhradách k ověření.

### 8. Ukliď worktree, ulož report a vrať ho

**Nejdřív ukliď worktree** (`pr-worktree.sh --remove pr-<číslo PR>`, viz
krok 4) — i když ověřování skončilo `Blocked`. Jeho výsledek (`removed=false`)
je vstup do sekce Výhrady k ověření v reportu, který sestavíš až pak; obráceně
by se `removed=false` do uloženého komentáře nedostalo.

Report ulož jako komentář k PR (recept „Komentář k PR (review)") a **vždy** ho
vrať i jako závěrečnou zprávu. Komentář je trvalý záznam, závěrečná zpráva je to,
podle čeho se rozhoduje `run-milestone` — jedno druhé nenahrazuje.

Jak se tělo předává, se liší podle forge:

- **Gitea** — report jde přímo do parametru `body` volání
  `pull_request_review_write` se `state: "COMMENT"`. Žádný soubor nepotřebuješ.
- **GitHub** — `pr-comment.sh` bere tělo jako `--body-file`, nikdy jako argument:
  víceřádkový markdown se v shellu o uvozovky a zpětné apostrofy tiše rozpadne.
  Soubor založ **mimo worktree PR**, ať ho neušpiníš, a celý blok pošli jako
  **jedno volání Bash** — `$f` by v dalším volání bylo prázdné:

```bash
f="$(mktemp)"
cat > "$f" <<'REPORT'
<report>
REPORT
bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/pr-comment.sh" -R "<owner/repo>" <číslo PR> --body-file "$f"
```

Ukončovač heredocu piš v uvozovkách a **bez odsazení na začátku řádku** — jinak
ho shell nerozpozná, a bez uvozovek navíc rozexpanduje `$` a zpětné apostrofy
v reportu, takže do trackeru dorazí něco jiného, než jsi napsal.

Selže-li uložení komentáře, závěrečnou zprávu vrať i tak a selhání uveď ve
Výhradách k ověření — komentář sám tuhle výhradu logicky nést nemůže.

Nakonec ukliď dočasné soubory s tělem issue (krok 7) a reportu — worktree je
uklizený už z úvodu tohohle kroku. Nechané artefakty z předchozího běhu zmatou
ten příští.

## Formát výstupu

````markdown
## Ověření issue #<číslo | —> — PR #<číslo | —>

**Verdikt:** <Pass | Needs work | Blocked>
**Příčina blokace:** <jen u verdiktu Blocked — co chybí nebo co selhalo; u
nedohledaného nebo nejednoznačného protějšku co jsi hledal a co jsi našel; u
nezískatelné větve PR strukturální omezení skillu podle kroku 4. Jinak řádek
úplně vynech.>

### Kritéria

<Jen kritéria s výsledkem **Nesplněno** nebo **Neověřitelné**, jedna odrážka na
kritérium: výsledek tučně, doslovné znění kritéria, pomlčka a proč (jednou
i více větami) — příkaz a jeho výsledek, cesta:řádek, nebo proč ověřit nelze.

Splněná kritéria se v reportu nevypisují — jejich stav nese odškrtnutí v těle
issue (krok 7), report ho neopakuje. Jsou-li splněna všechna → „Všechna
kritéria splněna." Skončil-li běh verdiktem `Blocked` dřív, než jsi měl co
ověřovat, sekci vynech úplně; důvod nese řádek „Příčina blokace" výše.>

### Ověřovací příkazy

<Neselhal-li žádný spuštěný příkaz → „Všechny ověřovací příkazy prošly."
Selhal-li některý, odrážka na příkaz: příkaz jako inline kód, pomlčka, čím
selhal. Neběžel-li žádný příkaz (blokace dřív, než jsi k němu došel) →
„Nespuštěno.">

### Mutační testy

<Proběhla-li mutace bezchybně u všech kritérií, která o ni stojí (test spadl
po revertu, prošel po obnovení) → „Mutační testy v pořádku." Neproběhla-li
u některého kritéria, které o ni stojí, nebo dopadla jinak, než měla (revert
selhal, blokace dřív, test prošel i s vrácenou změnou) → odrážka na kritérium
s důvodem — stejný důvod patří i do jeho odrážky v sekci Kritéria. Není-li
žádné kritérium opřené o regresní test → „Netýká se.">

### Výhrady k ověření

<Nepovinná sekce pro provozní výhrady k průběhu ověření: spárování jen podle
podobnosti názvu větve (krok 2), neodstraněný worktree (krok 4), selhaný zápis
odškrtnutí do těla issue (krok 7), selhané uložení komentáře k PR (krok 8).
Vynech, není-li žádná taková výhrada.>

### Doporučení

<Jen to, co z tohohle běhu ověřování vzešlo, s adresátem u každé položky:
`[implement-issue]` nesplněné kritérium, nebo neověřitelné kritérium, jehož
příčina je v kódu či testu, ne v zadání (kritérium po kritériu, co konkrétně
opravit); `[issue]` vada samotného zadání — nejasná formulace, neexistující
citovaná cesta, Reference bez kódového precedentu (obojí krok 3, s doporučením
`triage-issue`), chybějící `area:*` label (krok 3), kritérium, které je samo
špatně stanovené (krok 6), předem zaškrtnuté políčko (krok 7), i neověřitelné
kritérium, jehož příčina je v samotném zadání; `[konfigurace]` chybějící sekce
nebo řádek v konfiguraci cílového projektu, typicky oblast bez ověřovacího
příkazu; `[kontrakt]` mezera ve sdíleném kontraktu pluginu, na kterou jsi
narazil. Nic mimo to — žádná obecná poznámka ke kvalitě, stylu nebo architektuře
PR, i kdyby byla pravdivá. Není-li co doporučit → „Bez nálezů.">

Blokuje merge: <ano | ne>
````

Řádkem `Blokuje merge:` report **končí** a stojí v něm **právě jednou**, na
samostatném řádku, bez tučnění a bez čehokoli dalšího za hodnotou. `run-milestone`
podle něj rozhoduje mezi merge a opakováním a dispečovaným recenzentům velí report
tímhle řádkem ukončit; když ho nenajde nebo najde dvakrát, považuje celý běh za
selhaný dispatch a tvoje práce přijde vniveč. Hodnota se musí shodovat s verdiktem
v hlavičce — dva různé výroky v jednom reportu jsou horší než žádný.

## Zásady

- **Nic neopravuješ.** Tohle je čtecí posudek. Nesahej na kód, nepřidávej testy,
  neupravuj PR — oprava je práce pro `implement-issue` a ověřovatel, který si
  nález sám opraví, ho pak sám sobě odkývá.
- **Důkaz, nebo `Neověřitelné`.** Nemáš-li výstup příkazu nebo přečtené místo
  v souboru, kritérium není splněné. Zaškrtnuté políčko, popis PR ani commit
  message důkaz nejsou.
- **Reference se otevírá, ne parafrázuje, a precedent v kódu je primární zdroj
  pravdy.** Dokument citovaný vedle něj říká, kam nesahat, ne co mělo vzniknout.
  Kritérium opřené jen o prózu je `Neověřitelné` a vada zadání, ne PR.
- **Nikdy se neptáš.** Běžíš bez uživatele; nejasnost je nález, ne důvod k dotazu.
- **Mandát je přísně ohraničený: za žádnou cenu nic navíc.** Report neobsahuje
  nic nad rámec toho, co předepisuje Formát výstupu — žádné architektonické
  poznámky, žádné styling připomínky, žádné „když už tu jsem". Kvalitu kódu,
  styl a architekturu neposuzuješ vůbec, ani mimochodem — na to je code
  review, ne akceptace.
- **Report je stručný.** Splněné kritérium se do reportu nerozepisuje — jeho
  stav nese odškrtnutí v issue (krok 7), report ho neopakuje. Nemá-li sekce co
  hlásit, mlčí, místo aby psala „vše v pořádku" na dlouho. Co reportu nesmí
  chybět, je nesplněné nebo neověřitelné kritérium a proč — to je jediná
  informace, na které navazující práce (`implement-issue`, `run-milestone`)
  doopravdy stojí.
- **Řádek `Blokuje merge:` je závazek vůči navazujícímu skillu.** Nikdy ho
  nevynech a nikdy ho nepiš v rozporu s verdiktem.
- **Pracovní kopii po sobě ukliď** a nikdy z ní nepushuj ani necommituj.
