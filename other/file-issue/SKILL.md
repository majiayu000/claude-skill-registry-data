---
name: file-issue
description: >-
  Založí jeden ad hoc issue mimo plánování milestonu jako Poznámku — z popisu
  uživatele sestaví název i tělo v závazném tvaru pluginu se zachyceným
  záměrem nebo pozorováním, bez vyplněných akceptačních kritérií, nasadí
  právě jeden `area:*` label a typový label shodný s typem v názvu, a po
  potvrzení issue založí v trackeru a vrátí jeho číslo s odkazem. Milestone
  přiřadí jen na výslovné přání.
when_to_use: >-
  Použij, když má vzniknout jediný issue mimo milestone — „založ issue",
  „zaeviduj tenhle bug", „přidej to do trackeru", „ať se to neztratí" —
  i pro nálezy, které vypadnou mimochodem během jiné práce. Nepoužívej,
  když má z tématu vzniknout celá sada issues s milestonem a závislostmi,
  na to slouží plan-milestone; ani pro implementaci už existujícího issue,
  tu vlastní implement-issue a v rámci milestonu ji dispečuje run-milestone;
  ani pro povýšení založené Poznámky na Zadání ukotvené v kódu, to dělá
  triage-issue. Bez projektové konfigurace workflow skill nic nezakládá
  a odkáže na init-workflow.
argument-hint: "[co má issue řešit]"
model: sonnet
effort: medium
# Zařazení dle matice: ohraničené zadání se známým tvarem výstupu → sonnet
# (bod 2 rozhodovacího stromu) × medium, bez odchylky. Tvar výstupu drží
# šablona issue, rozsah je jediný issue a těžiště práce je rozlišení labelů
# a formátu forge, ne formulace kritérií — tu dělá triage-issue. Nikoli high
# jako u init-workflow: chybný jediný issue se opraví editací nebo zavřením,
# kdežto chybná konfigurace mlčky rozbije všechny další běhy. Nikoli opus:
# skill neplánuje rozsah, nestaví graf závislostí ani nic neimplementuje.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - ToolSearch
  - "Bash(bash:*)"
  - mcp__gitea__label_read
  - mcp__gitea__label_write
  - mcp__gitea__milestone_read
  - mcp__gitea__issue_write
# Bash je zúžený na spouštění skriptů; gh ani git se nikdy nevolá přímo, takže
# volání piš ve tvaru `bash <cesta>`, jinak nespadne do povolení. Write slouží
# výhradně k dočasnému souboru s tělem issue — GitHub větev ho předává přes
# `--body-file` — nikdy k zápisu do zdrojů projektu; Edit proto ve výčtu není,
# skill v cílovém projektu nic needituje. ToolSearch je nutný, protože nástroje
# `mcp__gitea__*` jsou odložené a bez načtení je nelze zavolat; jejich názvy
# odpovídají tvaru, který předepisuje forge-recipes.md. Běží-li v projektu Gitea
# MCP pod jiným prefixem, zápis neprojde — ohlas to a nech uživatele issue
# založit ručně, výčet neobcházej.
# Vynechaná zvažovaná pole:
# disable-model-invocation — automatické vyvolání ve chvíli, kdy během jiné
# práce vypadne nález, je přesně to, k čemu skill je, a nic nezakládá dřív
# než po potvrzení; context/agent/background — potvrzení návrhu vyžaduje
# uživatele v hlavním kontextu, fork ani běh na pozadí nemají komu klást
# otázku; paths — spouští se z konverzace o nálezu,
# ne prací nad konkrétním souborem; shell — skripty se spouští explicitním
# `bash`; disallowed-tools — allowed-tools je uzavřený výčet a skill běží
# s uživatelem, takže není co zakazovat navíc; version/license — verzuje se
# celý plugin, ne jednotlivý skill; Glob/Grep — po zúžení na Poznámku skill
# už nehledá zdroj pravdy v repozitáři, jen čte soubory na známých cestách.
# Sloveso `file` není v tabulce doporučených sloves konvencí; ponecháno vědomě —
# je to ustálené „file an issue" a název fixuje .docs/workflow-skills-plan.md,
# na který se odkazují sousední skilly sady.
---

# File Issue

Cílem je jeden issue jako **Poznámka** — zachycuje záměr nebo pozorování ze
vstupu uživatele, ne hotové zadání. Tvar těla je stejný jako u issues
z plánování, ale bez vyplněných akceptačních kritérií; povýšení na Zadání
ukotvené v kódu dělá `triage-issue`, ne tenhle skill. Závazným kontraktem
jsou sdílené soubory pluginu; při rozporu s tímhle postupem platí ony,
**s výjimkou tvaru Poznámky popsaného v kroku 2**.

| Soubor | Kdy ho otevři |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` | V kroku 1, když projektová konfigurace chybí nebo v ní nenajdeš sekci, kterou potřebuješ |
| `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` | V kroku 2, dřív než napíšeš název a tělo |
| `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` | V kroku 3, dřív než poprvé sáhneš na tracker — včetně sekce s nástrahami |
| `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` | V kroku 3, je-li forge GitHub — než spustíš první `gh/*.sh`, kvůli argumentům a návratovým kódům |

Obsah sdílených souborů si **přečti, ale nepřepisuj do odpovědi**. Šablona issue
se mění na jednom místě; kopie v konverzaci zastará a projekt pak nese dva různé
tvary těla.

## Vstupní kontext

- Popis od uživatele (může být prázdný): $ARGUMENTS

Prázdné zadání znamená, že popis vytěžíš z konverzace — typicky z nálezu, který
vypadl během jiné práce. Nemáš-li z čeho vytěžit, zeptej se, co má issue řešit,
dřív než začneš cokoli číst.

**Skill je interaktivní.** Selže-li volání AskUserQuestion nebo odpověď nedorazí,
**nezakládej nic**: vypiš návrh do konverzace, řekni, co potřebuješ doplnit,
a skonči. Nepovedený issue někdo ručně zavírá, kdežto neodeslaný návrh nestojí nic.

## Postup

### 1. Načti projektovou konfiguraci

Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni cílového
projektu. Potřebuješ z ní podsekce **Forge** (kterou větev receptů použít
a jaké `owner/repo` každému volání předat), **Labely** (co smíš nasadit)
a **Jazyk issues**.

- **`CONTRIBUTING.md` neexistuje nebo sekci nemá** → nepokračuj a nedomýšlej si
  hodnoty. Řekni uživateli, že projekt nemá workflow konfiguraci, a nabídni
  `/sagittaras:init-workflow`.
- **Chybí podsekce, kterou potřebuješ** → řekni která a nabídni doplnění; sám ji za
  pochodu nedoplňuj. Odhadnutý výčet oblastí vyrobí `area:*` label, který v projektu
  neexistuje, a s ním issue, jaké `run-milestone` neumí přiřadit.

### 2. Sestav issue jako Poznámku

Otevři `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md` kvůli tvaru názvu
a sekcí těla. Jazyk textu určuje sekce `Jazyk issues` z konfigurace. Pro
Poznámku se ale od šablony vědomě odchyluješ **ve třech bodech** — v nich
platí tenhle postup, ne obecná věta o přednosti sdíleného kontraktu výše:

- **`Souhrn` nese záměr nebo pozorování tak, jak ho dal uživatel** — ne
  závazné tvrzení, co issue dodá. Přenes do něj i kontext, který se jinam
  nevejde (reprodukční kroky, odkaz, útržek logu); Poznámka nemá jinou
  sekci, kam by ho uložila, a zahodit ho znamená ztratit informaci, kterou
  bude `triage-issue` nebo člověk později potřebovat.
- **`Akceptační kritéria` založ jako holý nadpis, bez jediného řádku pod
  ním** — žádná odrážka, žádná pomlčka, žádný placeholder typu „doplní
  triage-issue". Placeholder je text, který nikdo nepsal jako skutečné
  kritérium — `triage-issue` ho stejně přepíše, ale člověk i
  `review-milestone` by ho mezitím mohli číst jako pokus o zadání.
  Nevymýšlej kritérium, ani přibližné — to je přesně ta vada, kterou má
  `triage-issue` eliminovat, ne aby ji nejdřív vyrobil tenhle skill.
- **Sekci `Reference` vynech celou.** Poznámka žádný precedent ještě nemá;
  najde ho až `triage-issue`.

Nad rámec těchhle odchylek dál platí i pro Poznámku: **sekci `Závisí na`
vynech celou**, pokud issue vzniká mimo plán a na ničem nezávisí — uvést ji
smíš jen tehdy, když jde o **skutečné číslo** existujícího issue, které
uživatel jmenoval. Vymyšlené číslo si `run-milestone` přečte jako hranu grafu
a pošle práci na základ, který neexistuje.

### 3. Urči labely

Otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md`, vyber sloupec podle sekce
`Forge` a **volání neodvozuj z hlavy**. Podle větve forge platí:

- **Gitea** → nejdřív **jedním** voláním ToolSearch načti odložené nástroje podle
  řádku „Zakládá issues a milestony"; nese `label_read`, `label_write`,
  `milestone_read` i `issue_write`, takže pokryje celý zbytek postupu a druhé kolo
  načítání odpadne. Každému volání předej `owner` a `repo` ze sekce `Forge`.
  Neexistuje-li nástroj daného názvu (projekt může mít Gitea MCP pod jiným
  prefixem), **výčet neobcházej**: ohlas to a nech uživatele issue založit ručně.
- **GitHub** → skripty `gh/*.sh` volej `bash`em a **vždy jim předej
  `-R owner/repo`** ze sekce `Forge`; bez toho se řídí aktuálním adresářem, což
  v izolovaném worktree neplatí. Skončí-li kterýkoli kódem `7`, chybí `gh` nebo
  není přihlášené — řekni to uživateli hned a skonči, ne až u zápisu v kroku 6.
  Kód `2` znamená chybný argument, typicky vadnou barvu labelu.

Pak urči labely:

1. **Načti existující labely z forge**, ne z konfigurace. Konfigurace říká, jaká
   taxonomie platí; forge říká, co v ní opravdu je. Bez načtení bys navrhoval
   duplicitu k labelu, který se jen jinak píše.
2. Nasaď **právě jeden `area:*` label** podle kódu, kterého se Poznámka týká —
   ne podle tématu, ze kterého nález vypadl. Podle tohohle labelu vybírá
   `run-milestone` inženýra, až issue někdo do milestonu zařadí.
3. Nasaď **typový label shodný s typem v názvu** issue. `implement-issue` z něj
   odvozuje typ větve i commitu a rozpor mezi názvem a labelem je nález pro
   `review-milestone`.
4. Label, který v projektu chybí, teď **jen navrhni** — zakládá se až v kroku 6 po
   potvrzení. Barvu převezmi od existujícího labelu téže rodiny z výpisu z forge
   (hex bez `#`, šest číslic); nemáš-li od čeho, zeptej se. Vymyšlená barva projde
   návrhem a skript ji odmítne kódem `2` až při zápisu.

Nástrahu s číselnými ID labelů u Gitea má `forge-recipes.md` v sekci nástrah —
předané názvy se tiše nepřipnou, takže volání vypadá jako úspěšné a issue je bez
labelu. Sekci si přečti dřív, než uděláš první zápis.

### 4. Milestone jen na vyžádání

Milestone **nepřiřazuj sám od sebe**, ani když je v projektu zrovna jeden otevřený.
Tenhle skill je pro práci mimo milestone a nasazený milestone mění, co s issue udělá
`run-milestone` i `close-milestone` — zařazení je rozhodnutí uživatele, ne úklid.

Vyžádá-li si ho uživatel, **napřed si milestone dohledej** receptem „Vypiš milestony"
se stavem `all` a z výpisu si vezmi jak název, tak číslo. Uživatel milestone jmenuje
názvem, ale každá větev forge chce v poli `milestone` jinou hodnotu — jakou, si ověř
v receptu „Založ issue" a v sekci nástrah, kde je táž záměna popsaná u labelů
a u `list_pull_requests`. Špatný tvar hodnoty se chová stejně tiše: volání projde,
milestone se nepřipne a nikdo si toho nevšimne, protože souhrn ho vypíše jako
přiřazený. Proto se v kroku 6 přiřazení ověřuje z odpovědi forge.

**Milestone daného názvu nenajdeš** → nezakládej ho a zeptej se. Nový milestone
zakládá `plan-milestone` spolu s celou sadou issues a jeho popis definuje, co pro
něj znamená „hotovo"; prázdný milestone založený kvůli jednomu ad hoc issue tuhle
definici nemá a `review-milestone` pak nemá proti čemu posoudit rozsah.

**Poznámka zařazená do milestonu na Zadání sama nepřejde.** `run-milestone`
ji podle `area:*` labelu dispečuje, ale bez kritérií nemá inženýr proti
čemu implementovat a `review-milestone` milestone vrátí jako `Not ready` —
`triage-issue` je tu předpoklad, ne alternativa k zařazení. Řekni to
v souhrnu řádkem `Stav` podle Formátu výstupu, ať se ví, že milestone samo
o sobě nestačí.

### 5. Předlož návrh a počkej na potvrzení

Vypiš návrh podle Formátu výstupu a **potvrzení si vyžádej nástrojem
AskUserQuestion**. Je to jediná brzda celého postupu: název, souhrn a labely se
přečtou za půl minuty, kdežto issue se špatným `area:*` labelem projde až
k dispatchi na špatného specialistu.

Připomínky zapracuj a návrh předlož znovu. Do kroku 6 jdi až s potvrzeným návrhem.

### 6. Založ issue a vypiš výsledek

Zakládej podle receptů — nejdřív potvrzené chybějící labely („Založ label"), pak
issue („Založ issue"). Opačné pořadí znamená issue bez labelu.

Na GitHub větvi tělo **zapiš do dočasného souboru mimo pracovní strom repozitáře**
a předej ho přes `--body-file`; víceřádkový markdown se v argumentu shellu rozpadne.
Soubor leží mimo strom, takže ho není nutné po sobě mazat.

Selže-li zápis, **neopakuj celé volání naslepo**: vypiš, co už vzniklo, a řekni,
co selhalo. U chyby 404 na Gitea ověř oprávnění účtu podle nástrah v receptech
a jiný repozitář nezkoušej; u `gh` skriptu vyhodnoť návratový kód podle
`git-scripts.md`.

Nakonec vypiš **číslo issue a odkaz** podle Formátu výstupu. Bez čísla a odkazu je
výsledek pro uživatele nedohledatelný a pro navazující skilly nepoužitelný. Labely
a milestone do souhrnu opiš **z odpovědi forge, ne ze svého záměru** — právě tichý
rozdíl mezi tím, co jsi poslal, a tím, co se připnulo, je nejčastější chyba
v celém postupu.

Založil-li se nový `area:*` label, řekni to v souhrnu a doporuč
`/sagittaras:init-workflow` k doplnění sekcí `Labely` a `Agenti`. Jinak zůstane
konfigurace zastaralá a `run-milestone` pro tuhle oblast nenajde agenta.

## Formát výstupu

**Návrh k potvrzení** (krok 5):

```
Název: <type>(<scope>): <popis>
Labely: area:<oblast> · <typový label>
Milestone: <název | „žádný — issue vzniká mimo milestone">

Souhrn: <záměr/pozorování ze vstupu uživatele, včetně repro kroků, odkazu nebo útržku logu>
Akceptační kritéria: prázdná — holý nadpis, doplní triage-issue

Chybějící labely k založení: <název (barva hex)>, … | „žádné"
```

Vypiš i sekci `Závisí na`, pokud ji issue výjimečně má. Uživatel má před sebou
všechno, co se chystáš založit — potvrzení návrhu, ze kterého půlka těla vypadla,
je brzda jen naoko.

**Souhrn po založení** (krok 6):

```
Issue #<číslo>: <název> — <url>
Labely: area:<oblast> · <typový label>
Milestone: <název | „žádný">
Založené labely: <výčet, nebo „žádné">
Stav: Poznámka — k dispatchi potřebuje triage-issue
Poznámka ke konfiguraci: <doporučení init-workflow po založení nového area:* labelu, nebo „žádná">
```

## Zásady

- **Jeden běh = jeden issue.** Rozpadá-li se popis na víc kusů práce, řekni to
  a nabídni `/sagittaras:plan-milestone`; sadu issues tenhle skill nezakládá.
- **Tvar těla je stejný jako u plánovaných issues, kritéria ale zůstávají
  prázdná.** Právě proto se dá issue později zařadit do milestonu a povýšit
  přes `triage-issue` — zkratka v těle („však je to jen drobnost") ho z řetězu
  vyřadí. Zařazení do milestonu bez `triage-issue` samo o sobě k dispatchi
  nestačí.
- **Kritérium ani Reference se nevymýšlí.** To je práce `triage-issue`, ne
  tady — issue založené tímhle skillem je vždy Poznámka.
- **Právě jeden `area:*` label, podle kódu, ne podle tématu.**
- **Do trackeru se zapisuje až po potvrzení návrhu.** Před krokem 6 skill tracker
  jen čte — existující labely a případný milestone — a nic v něm nemění.
- **Sdílený kontrakt má přednost**, mimo výjimku u tvaru Poznámky popsanou
  v kroku 2. Odporuje-li tenhle postup šabloně issue **jinde**, konfiguraci
  nebo receptům, platí ony.
