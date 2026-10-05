---
name: init-workflow
description: >-
  Jednorázově nastaví cílový projekt pro milestone workflow — detekcí zjistí
  forge a repozitář, z agentů a souborů projektu odvodí mapu oblastí
  a ověřovací příkazy, na zbytek se doptá a založí sekci „Workflow (sagittaras)"
  v `CONTRIBUTING.md`. Mapu agentů interviewuje jen tam, kde se projektu
  skutečně hodí, a zdroje pravdy, které už nese CLAUDE.md, znovu nezapisuje.
  Chybějící labely doplní v trackeru až po potvrzení. Existující konfiguraci
  nikdy nepřepíše tiše — nabídne aktualizaci po podsekcích.
when_to_use: >-
  Použij, když se má v projektu rozjet milestone workflow a chybí mu
  konfigurace — „nastav workflow", „připrav projekt na milestony", „chybí
  workflow konfigurace" — i tehdy, když jiný skill ohlásí, že konfigurace
  chybí nebo v ní chybí sekce, kterou potřebuje. Nepoužívej pro plánování
  milestonu a zakládání issues, na to slouží plan-milestone; pro zakládání
  a úpravu agentů projektu slouží write-agent; pro stažení novější verze
  pluginu update-plugin.
argument-hint: "[nic, nebo podsekce, kterou chceš změnit]"
model: sonnet
effort: high
# Zařazení dle matice: ohraničené zadání se známým tvarem výstupu → sonnet
# (bod 2 rozhodovacího stromu). Effort high místo medium je posun o stupeň:
# konfigurace je vstup pro všechny ostatní skilly workflow a chybná mapa agentů
# se pozná až u review celého milestonu — matice před medium varuje právě
# u rozhodnutí, která se těžko vrací zpět. Nikoli opus: skill nic neorchestruje
# ani neimplementuje, jen zjišťuje, ptá se a zapisuje jednu sekci souboru.
# Odchylka od konvence pojmenování: `init` je zkratka, před kterými konvence
# varují, a v tabulce doporučených sloves není. Ponecháno vědomě — název fixuje
# .docs/workflow-skills-plan.md, ostatní skilly sady se na něj odkazují a v gitu
# je „init" idiom, kterému rozumí i ten, kdo plugin nezná.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - ToolSearch
  - "Bash(bash:*)"
  - mcp__gitea__label_read
  - mcp__gitea__label_write
# Bash je zúžený na spouštění skriptů; git ani gh se nikdy nevolá přímo.
# Proto každé volání píš ve tvaru `bash <cesta>` — jinak nespadne do povolení.
# ToolSearch a dvojice mcp__gitea__label_* je tu kvůli Gitea větvi: nástroje
# jsou odložené a bez ToolSearch se nenačtou, bez uvedení v tomto výčtu se
# nezavolají. Názvy odpovídají tvaru, který předepisuje forge-recipes.md;
# běží-li v projektu Gitea MCP pod jiným prefixem, labely se nezaloží — ohlas
# to a nech uživatele založit je ručně, výčet neobcházej.
# Vynechaná zvažovaná pole: disable-model-invocation — automatické vyvolání
# ve chvíli, kdy jiný skill ohlásí chybějící konfiguraci, je přesně to, co má
# nastat, a brzdou jsou potvrzení v krocích 2, 6 a 7; context/agent/background —
# celý postup stojí na interview, fork ani běh na pozadí nemá komu klást
# otázky; paths — spouští se z konverzace o projektu, ne prací nad konkrétním
# souborem; shell — skripty se spouští explicitním `bash`; disallowed-tools —
# allowed-tools je uzavřený výčet, není co zakazovat navíc; version/license —
# verzuje se celý plugin, ne jednotlivý skill.
---

# Init Workflow

Cílem je sekce `## Workflow (sagittaras)` v `CONTRIBUTING.md` cílového projektu, ze
které všechny ostatní skilly milestone workflow čtou, aby se neptaly na totéž
pokaždé znovu. Závazný tvar sekce drží
`${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` — **přečti si ho jako první**
a při rozporu s tímto skillem platí on. `CONTRIBUTING.md` je konvenční, lidmi
čitelný dokument — sekce je jediná jeho část, kterou tenhle skill smí zakládat
nebo měnit; zbytek souboru je projektův vlastní obsah a nesahej na něj.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

Prázdné zadání znamená plné nastavení. Konkrétní zadání („uprav ověřovací
příkazy") ber jako zúžení na jednu podsekci — projdi krok 1, pak rovnou příslušný
krok a krok 7.

**Zúžení platí jen v režimu aktualizace.** Zjistíš-li v kroku 1, že konfigurace
neexistuje, proveď plné nastavení bez ohledu na zadání a řekni to nahlas: nová
sekce musí mít vyplněné všechny podsekce (kromě nepovinné Agenti) a přeskočené
kroky nemají čím. Mění-li zúžení **výčet oblastí**, projdi vždy i kroky 4 a 6 —
oblasti se opakují ve třech podsekcích a rozejít se smí jen jednou.

**Bez uživatele konfiguraci nezakládej.** Selže-li volání AskUserQuestion nebo
odpověď nedorazí, shrň, co jsi zjistil a na co potřebuješ odpovědět, a skonči
bez zápisu. Konfigurace odhadnutá z domněnek pošle práci špatnému specialistovi
a pozná se to až u review hotového PR.

## Postup

### 1. Detekce a stav konfigurace

1. Spusť `bash "${CLAUDE_PLUGIN_ROOT}/scripts/forge-detect.sh"`. Kontrakt
   skriptu — výstupní klíče a návratové kódy — popisuje
   `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md`; otevři ho, jen když si
   nejsi jistý výkladem kódu.
   - **kód 2** (není git repozitář) → ohlas a skonči. Workflow stojí na větvích
     a PR, bez repozitáře není co konfigurovat.
   - **kód 3** (chybí remote nebo z něj nejde odvodit `owner/repo`) → ohlas
     a zeptej se na `owner/repo`, host **i výchozí větev**; bez remotu nemá
     skript odkud vzít ani ji, takže ji v kroku 2 nemáš co předkládat
     k potvrzení. Zbytek postupu běží dál.
   - **kód 0, ale `default_branch` je prázdná** → remote neodpověděl. Je to
     jediný neúplný výsledek, který nenese návratový kód, takže ho snadno
     přehlédneš: doptej se na výchozí větev a **neber ji z lokálního refu**.
   - **`forge=unknown`** → nech uživatele vybrat mezi `gitea` a `github`.
     Neurčenou hodnotu do konfigurace nezapisuj — podle ní se vybírá celá
     větev volání v `forge-recipes.md`.
   - **skript neexistuje nebo není spustitelný** (typicky kód 127) → **detekci
     neobcházej vlastními `git` příkazy**. Ohlas, že instalace pluginu nemá
     `scripts/forge-detect.sh`, a zeptej se na forge, host, `owner/repo`
     a výchozí větev jako u kódu 3. Ručně poskládaná detekce vrátí věrohodně
     vypadající nesmysl — třeba zastaralou výchozí větev z lokálního refu,
     před čímž `git-scripts.md` výslovně varuje.

2. Zjisti, jestli `CONTRIBUTING.md` už existuje a jestli v něm je sekce
   `## Workflow (sagittaras)`.
   - **Sekce existuje** → **přečti ji celou** a přepni se do režimu
     aktualizace: v každém dalším kroku nejdřív ukaž současnou hodnotu, pak
     navrhovanou, a nech vybrat. Podsekce, které uživatel nechce měnit, přenes
     do výsledku **doslova** — včetně poznámek, které si projekt dopsal sám.
     Zbytek `CONTRIBUTING.md` mimo tuhle sekci nečti kvůli konfiguraci vůbec —
     není to tvůj obsah.
   - **Sekce neexistuje** (ať `CONTRIBUTING.md` existuje, nebo ne) → podívej se
     na starší umístění, kam tenhle plugin dřív zapisoval konfiguraci:
     `.claude/workflow.md`, a ještě starší `.claude/sagittaras/workflow.md`.
     Najdeš-li některé, přečti ho, řekni uživateli, že se konfigurace stěhuje
     do `CONTRIBUTING.md`, a pokračuj režimem aktualizace s jeho obsahem —
     zapíšeš ho na nové místo. Starý soubor **nemaž sám**: `allowed-tools` na
     to nemá nástroj a smazání patří do commitu, který dělá uživatel. Připomeň
     mu ho ve shrnutí. Nenajdeš-li nic, plné nastavení: existuje-li
     `CONTRIBUTING.md` už teď, sekce se na konec souboru **přidá**, ne vloží do
     existujícího obsahu; jinak se `CONTRIBUTING.md` založí nově s jedinou
     sekcí.

3. Cesta k souboru se ukotvuje ke **kořeni cílového projektu**, ne
   k `${CLAUDE_PLUGIN_ROOT}`. Zapsat konfiguraci do souboru pluginu je tichá
   chyba: soubor vznikne, projekt ho ale nikdy neuvidí.

### 2. Forge, repozitář a větvení

Rozliš, co detekce vrátila, a co ne. **Zjištěné hodnoty** (forge, host,
`owner/repo`, výchozí větev) předlož **k potvrzení jedním dotazem**; na to,
co má uživatel před sebou, se neptej otevřenou otázkou. **Nezjištěné hodnoty**
si vyžádej jmenovitě a řekni, proč chybí — potvrzování prázdné položky vypadá
jako otázka na formalitu a odpovídá se na ni „ano" i tehdy, když tam nic není.

Z podsekce **Větvení** je proměnná jedině výchozí větev. Ostatní řádky drží
kontrakt a v šabloně nemají hranaté závorky: tvar issue větve `<type>/<popis>`,
integrační větev `milestone/<slug>`, squash merge a věta, že do výchozí větve
mergeuje jen člověk, ledaže prompt, kterým byl aktuální běh spuštěn, obsahoval
výslovný souhlas k mergi. Opiš je doslova a neptej se na ně — `run-milestone`
i `implement-issue` s nimi počítají jako s daností, takže projektová odchylka
by se projevila až selháním za běhu.

### 3. Mapa oblastí a agentů

Podsekce `Agenti` je nejcennější část konfigurace, když se projektu hodí —
je to jediná podsekce, kterou detekce za běhu nenahradí, protože podle ní se
práce posílá specialistovi. **Výčet `area:*` ale vzniká vždycky**, bez ohledu
na to, jestli podsekce `Agenti` nakonec vznikne — potřebují ho i podsekce
Ověřovací příkazy (krok 4) a Labely (krok 6), obě povinné.

1. Odvoď výčet `area:*` — z oborů, které vlastní existující agenti (bod 2),
   z existujících `area:*` labelů v trackeru, ze struktury repozitáře
   (monorepo balíčky, vrstvy), nebo doptáním. Tenhle výčet vznikne vždy,
   nezávisle na tom, kolik projekt má agentů.
2. Nástrojem Glob najdi `.claude/agents/**/*.md` v cílovém projektu a z každého
   souboru si přečti **jen frontmatter** (Read s `limit: 60`). Zajímá tě `name`
   a `description`. Hvězdičky jsou dvě záměrně: některé projekty agenty třídí
   do podsložek a plochý vzor by je minul, což se pozná až selhaným dispatchem.
3. Ke každé oblasti z bodu 1, kterou vlastní agent, ho přiřaď. Do tabulky
   patří **hodnota `name`** přesně tak, jak stojí ve frontmatteru —
   `run-milestone` ji předá nástroji Agent a neexistující název znamená
   selhaný dispatch, ne chybu, kterou by šlo dohledat.
4. Role recenzentů (kvalita kódu, akceptační kritéria) urči **podle
   `description`, ne podle názvu**. Projekt může mít `principal-engineer`
   místo `tech-lead`; hledáš roli, která posuzuje, ne konkrétní slovo.
5. Návrh mapy nech potvrdit a doplnit. Oblast, kterou žádný agent nepokrývá,
   je legitimní zjištění — buď ji z výčtu vypusť, nebo ji nech s poznámkou,
   že agent chybí.

**Podsekce `Agenti` vzniká, právě když z bodů 3–5 vzejde aspoň jeden řádek
`oblast → agent`, nebo aspoň jedna obsazená role recenzenta — jinak ji do
`CONTRIBUTING.md` vůbec nezakládej**, ani prázdnou tabulku, ani placeholder
pomlčky. Tohle je jediné kritérium; žádné jiné (třeba „má projekt víc než
jednoho agenta") vedle něj neplatí. Nevznikne-li podsekce, řekni uživateli,
že `run-milestone` poběží na fallbacku (dispatch na obecného subagenta),
a že mapu může kdykoli doplnit přes `/sagittaras:write-agent` a opakovaný
běh tohohle skillu.

**Migruješ-li starší konfiguraci** (krok 1 bod 2): tohle kritérium se
vyhodnocuje **znovu**, ne přenáší doslova jako ostatní podsekce, které
uživatel nechce měnit. Starší soubor mohl nést vynucenou tabulku s jedinou
pomlčkou přesně proto, že tohle kritérium v něm ještě neexistovalo. Skládá-li
se stará podsekce `Agenti` jen z `—`, zahoď ji a řekni uživateli, že se proti
staré konfiguraci mění.

Výčet oblastí z bodu 1 **musí do znaku sedět** na oblasti v podsekci Labely
(krok 6) i v ověřovacích příkazech (krok 4), bez ohledu na to, jestli podsekce
`Agenti` vznikla. Rozpor znamená issue, které `run-milestone` neumí přiřadit.

### 4. Ověřovací příkazy

Odvoď je z **reálných souborů projektu**, ne z toho, co bývá obvyklé. Prohledej
podle typu projektu: `package.json` (sekce `scripts`), `*.sln` a `*.csproj`,
`Makefile`, `Taskfile.yml`, `justfile`, `pyproject.toml`, `composer.json`,
`Cargo.toml` a workflow soubory v `.github/workflows/`. Vytěžený příkaz opiš
přesně, včetně správce balíčků (`pnpm`, ne `npm`, když projekt používá `pnpm`).

Ke každé oblasti z kroku 3 přiřaď jeden příkaz. Má-li projekt jediný příkaz pro
všechno, zopakuj ho u každé oblasti — tabulku čte `verify-issue` po řádcích
a chybějící řádek pro něj znamená chybějící podsekci, ne „použij ten druhý".

**Příkazy nespouštěj.** Build cizího projektu může trvat minuty a sahat na
závislosti; potvrzení od uživatele je levnější a spolehlivější. Nenajdeš-li
oporu v žádném souboru, příkaz **nevymýšlej** a zeptej se — vymyšlený příkaz
projde konfigurací i review a selže až u integrační brány.

### 5. Zdroje pravdy a jazyk issues

- **Zdroje pravdy** — dokumenty, o které se opírají akceptační kritéria (ADR,
  specifikace, konvence). Nejdřív přečti `CLAUDE.md` cílového projektu (existuje-li):
  nese-li už **konkrétní cesty** k takovým dokumentům (ne jen zmínku, že
  dokumentace „někde je"), **do `CONTRIBUTING.md` je znovu nevypisuj** — zapiš
  jedinou odrážku `— viz CLAUDE.md`. Dvě kopie stejného výčtu driftují, přesně
  jako u zásad 1.5 tohohle pluginu. Nenese-li `CLAUDE.md` konkrétní cesty,
  zjisti to dotazem — z repozitáře to
  spolehlivě neplyne. Jako možnosti nabídni, co jsi v repozitáři našel (`docs/`,
  `adr/`, existující `CONTRIBUTING.md`), ale výběr nech na uživateli: existence
  složky s dokumentací neříká, že jsou v ní kritéria ukotvitelná. Bez tohoto
  vstupu nemá `plan-milestone` co citovat, takže prázdný seznam pojmenuj jako
  mezeru, ne jako platnou odpověď. Trvá-li uživatel na prázdnu, zapiš do
  podsekce jedinou odrážku `—` a **podsekci nevynechávej**: chybějící podsekce
  pro ostatní skilly znamená rozbitou konfiguraci k doplnění, kdežto pomlčka
  znamená vědomé rozhodnutí, se kterým se dá pracovat.
- **Jazyk issues** — čeština, nebo angličtina, jedna hodnota pro celý projekt.
  Jako vodítko můžeš uvést jazyk existujících issues nebo `README.md`, ale
  rozhodnutí patří uživateli.

### 6. Labely

Než sáhneš na tracker, otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`
a volání vezmi z tabulky — neodvozuj je z hlavy. Na Gitea si nástroje načti
**jedním** voláním ToolSearch podle řádku „Zakládá issues a milestony"; je to
jediný řádek, který nese `label_read` i `label_write`, a načtený nástroj navíc
nevadí, zatímco kolo navíc ano.

Na GitHubu předávej skriptům repozitář jako `-R <owner/repo>` **ze zjištění
kroku 1**. Tabulka receptů argument neuvádí a ostatní skilly ho berou ze sekce
`Forge` konfigurace — jenže ta v tuhle chvíli ještě neexistuje, tenhle skill ji
teprve zakládá. Bez `-R` skončí volání kódem 2 a `gh` by se jinak řídilo podle
aktuálního adresáře, což v izolovaném worktree ukazuje jinam.

1. **Načti existující labely** z forge. Bez toho bys navrhoval duplicity
   k něčemu, co v projektu roky funguje.
2. Sestav cílový výčet: **typové** labely podle Conventional Commits (`feat`,
   `fix`, `docs`, `refactor`, `test`, `chore` jako výchozí návrh) a **oblastní**
   `area:*` z kroku 3. Typový label se musí shodovat s `<type>` v názvu issue —
   proč, vysvětluje `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md`; otevři ho,
   jen když návrh typové sady s uživatelem rozporuješ.
3. **Navrhni jen chybějící** labely a nech je potvrdit nástrojem
   AskUserQuestion. Barvu předávej hexem bez `#`; typové a oblastní drž
   v odlišných barevných rodinách, ať je routing čitelný na první pohled.
4. Zakládej teprve po potvrzení. **Existující labely nepřejmenovávej ani
   nemaž** — visí na nich staré issues i uložené filtry lidí, kteří o tomhle
   běhu nevědí.

Selhání, na která reaguj jinak než opakováním:

- **404 na zápisu objektu, který zjevně existuje** → skoro vždy oprávnění účtu;
  nález i s postupem má `forge-recipes.md` v sekci nástrah. Ohlas to a nech
  přístup doplnit; nezkoušej jiný repozitář.
- **`gh` skript skončí kódem 2** → chybný nebo chybějící argument, nejčastěji
  vynechané `-R owner/repo`. Oprav volání a zopakuj; nezkoušej skript bez `-R`.
- **`gh` skript skončí kódem 7** → chybí `gh`, nebo není přihlášené. Řekni to
  rovnou a nech uživatele přihlásit se; obejít to jiným nástrojem nejde.
- **`gh` skript neexistuje** (kód 127), nebo Gitea MCP běží pod jiným prefixem,
  než na jaký je zúžený `allowed-tools` → labely tímhle během **nezaložíš**.
  Vypiš chybějící labely i s barvami, ať je uživatel založí ručně, a pokračuj
  krokem 7. Konfiguraci to neblokuje: chybějící label je vada trackeru,
  kterou `plan-milestone` uvidí a ohlásí, kdežto chybějící konfigurace zastaví
  celý řetěz.

### 7. Zápis konfigurace

Zapiš sekci `## Workflow (sagittaras)` přesně ve tvaru z
`${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` — **nadpisy a jejich pořadí
jsou závazné**, protože se podle nich podsekce vyhledávají bez parsování prózy.
Podsekci **Agenti** vynech úplně, nesplnila-li kritérium z konce kroku 3 —
nezakládej ji ani prázdnou. Komentářové anotace šablony v hranatých závorkách
ani kurzívou (jako `*(nepovinná — viz níž)*` u vzoru podsekce Agenti) do
zapsané sekce nepatří — jsou to poznámky pro tebe, ne pro projekt.

- **`CONTRIBUTING.md` neexistuje** → Write celého souboru s jedinou sekcí
  `## Workflow (sagittaras)`.
- **`CONTRIBUTING.md` existuje, sekci nemá** → Edit: soubor si **přečti jen
  kvůli kotvě** pro připojení (Edit potřebuje existující text, na který
  naváže) — z jeho obsahu do konfigurace nic nevytěžuj a žádný jeho řádek
  neměň. Sekci **připoj na konec** souboru, za všechno, co tam už je.
- **Sekce existuje, plné nastavení nebo zúžení** → Edit jen sekce
  `## Workflow (sagittaras)` po podsekcích, jen tam, kde uživatel změnu
  odsouhlasil. Přepsat celý soubor Writem je tichá ztráta zbytku
  `CONTRIBUTING.md`, který projekt nese.

Hranaté závorky ze šablony jsou pokyn, co do místa patří — v hotové sekci
žádná nesmí zůstat. Výjimkou je `—` u nevyplněné role recenzenta nebo
zdrojů pravdy, což je platná hodnota.

### 8. Shrň a navaž

Vypiš shrnutí podle Formátu výstupu a doporuč další krok:
`/sagittaras:plan-milestone`. Chybí-li v projektu agenti (podsekce Agenti se
nezaložila), doporuč před ním `/sagittaras:write-agent` — bez agentů poběží
milestone na fallbacku, což je funkční, ale slabší než dispatch na specialistu.

## Formát výstupu

```
Konfigurace: CONTRIBUTING.md, sekce „Workflow (sagittaras)" (<založena |
  aktualizována | přenesena ze staršího umístění — smaž `<stará cesta>`>)

Forge: <typ> · <host> · <owner/repo> · výchozí větev <branch>
Oblasti: <area:*, po řádcích — s přiřazeným agentem, je-li podsekce Agenti
  založená; jinak jen výčet oblastí>
Recenzenti: <kvalita <role | —> · kritéria <role | —>, je-li podsekce Agenti
  založená; jinak „netýká se, bez podsekce Agenti">
Ověřovací příkazy: <oblast → příkaz, po řádcích>
Zdroje pravdy: <výčet | „— viz CLAUDE.md" | „nezadány — plan-milestone nebude mít co citovat">
Jazyk issues: <hodnota>
Labely: <založené názvy | „žádné, všechny už existovaly" | „nezaloženy —
  <důvod>, k ručnímu založení: <názvy a barvy>">

Navazuje: /sagittaras:plan-milestone
```

## Zásady

- **Kontrakt má přednost.** Při rozporu mezi tímto skillem a
  `shared/workflow-config.md` platí kontrakt; tvar sekce čtou všechny ostatní
  skilly workflow a odchylka se projeví až jejich selháním.
- **Existující konfiguraci nikdy nepřepisuj tiše — a nikdy nesahej na zbytek
  `CONTRIBUTING.md`.** Ani při plném běhu, ani když se zdá zastaralá.
  Aktualizace je vždy po podsekcích a vždy s potvrzením; obsah mimo sekci
  `## Workflow (sagittaras)` patří projektu, ne tomuhle skillu.
- **Neptej se na to, co jde zjistit — a nedomýšlej, co zjistit nejde.** Obě
  chyby vypadají opačně, ale končí stejně: konfigurací, které uživatel nevěří.
  Interview o dvaceti otázkách se navíc nedodělá, a nedodělaná konfigurace je
  horší než žádná: ostatní skilly se pak spustí proti polovičním hodnotám.
- **Podsekce Agenti a prázdná role recenzenta jsou platné stavy, ne mezery.**
  Nevznikne-li aspoň jeden řádek `oblast → agent` nebo jedna obsazená role,
  podsekce se vůbec nezakládá; chybějící agenti nejsou důvod běh odmítnout
  ani roli vymyslet.
- **Zdroje pravdy se nezdvojují s CLAUDE.md.** Nese-li je už, `CONTRIBUTING.md`
  na něj jen odkáže — dvě kopie téhož výčtu driftují.
- **Trackeru se dotýkej jen skripty a recepty, jen kvůli labelům a jen po
  potvrzení.** Milestony, issues ani větve tenhle skill netvoří — na to jsou
  `plan-milestone` a `run-milestone`. A chybí-li skript nebo nástroj, ohlas to
  a doptej se: ručně poskládaný `git` nebo `gh` příkaz vrátí věrohodně
  vypadající nesmysl, který se zapíše do konfigurace natrvalo.
- **Jeden běh = jeden projekt.** Konfiguraci nekopíruj z jiného repozitáře;
  mapa agentů ani ověřovací příkazy se mezi projekty nepřenášejí.
