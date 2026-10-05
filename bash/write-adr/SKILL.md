---
name: write-adr
description: >-
  Sepíše architektonické rozhodnutí (ADR) do logu cílového projektu — vede
  interview, které nesmí nechat otázku bez odpovědi ani bez přiznání, sepíše
  dokument podle šablony, vypraví ho jako větev a PR přes sdílené skilly
  a nechá ho nezávisle zrevidovat subagentem s čistým kontextem. Umí i dořešit
  otevřené otázky už přijatého ADR. Merge nechává člověku.
when_to_use: >-
  Použij, když má vzniknout záznam architektonického rozhodnutí, které je
  ohrožené — někdo bez kontextu by ho později mohl vnímat jako zbytečnou
  komplikaci a pokusit se ho „opravit" — „udělej z toho ADR", „zapiš to
  rozhodnutí", „proč tu máme vlastní vrstvu nad knihovnou X", „dořeš otevřené
  otázky v ADR 3". Běžnou, levně vratnou volbu nástroje bez skryté ceny (např.
  „vybrali jsme knihovnu X" bez dalšího kontextu) skill sám odmítne založit —
  nenabízej ho na ni dopředu. Nepoužívej pro posouzení už sepsaného ADR, na to
  slouží review-adr; pro pravidlo vázané na část repozitáře write-rule; pro
  projektové instrukce čtené v každé session write-claude-md; pro zobecněný
  poznatek z review zapsaný do paměti agenta train-agent; pro závazný popis
  vzhledu projektu write-art-bible a pro popis jedné obrazovky nebo flow
  write-ux-spec — ty říkají, jak to má vypadat a fungovat, kdežto ADR proč se
  to tak rozhodlo; ani pro rozepsání práce na issues, na to je plan-milestone.
argument-hint: "[číslo ADR] [téma rozhodnutí]"
model: opus
effort: high
# Zařazení dle matice: orchestrace workflow s autonomní smyčkou — matice na ni
# má řádek opus × xhigh. Snížení na high je odchylka o stupeň se stejným
# důvodem jako u write-skill: nejtěžší část běhu (review) je delegovaná na
# review-adr běžící na opus × xhigh a git mechaniku vlastní create-branch
# a open-pr. Vlastní prací tohoto skillu zůstává interview a text, ne hloubkové
# posuzování. Nikoli sonnet: vést interview, které samo najde chybějící
# alternativu a nepřiznanou cenu, je úsudková práce a chyba se platí rok.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Agent
  - Skill
  - "Bash(git:*)"
  - "Bash(bash:*)"
# `Bash(git:*)` používá skill sám, a jen na čtecí zjištění stavu (rezervovaná
# čísla na remotu, čistota pracovního stromu, diff dokumentu do zadání pro
# reviewera). Všechno, co do repozitáře zapisuje, jde přes delegované skilly.
# `Bash(bash:*)` je tam kvůli nim: `create-branch`, `open-pr` i `make-commit`
# stojí na skriptech pluginu volaných tvarem `bash <cesta>`, a jestli se
# u vnořeného vyvolání uplatní práva volaného, nebo průnik s volajícím, plugin
# nikde nefixuje. Položka je bezriziková — povoluje spouštění skriptů, ne
# libovolný shell — a bez ní by autonomní běh mohl umřít na první delegaci.
# Vynechaná zvažovaná pole: disable-model-invocation — skill má jít vyvolat
# i tím, že uživatel popíše rozhodnutí, aniž by řekl „ADR"; context/agent/
# background — interview vyžaduje uživatele v hlavním kontextu a větev i soubor
# musí vzniknout ve sdíleném pracovním stromu, takže fork ani běh na pozadí
# nepřipadá v úvahu (čistý kontext se používá až pro reviewera v kroku 7);
# ToolSearch a `mcp__gitea__*` — skill sám na tracker nesahá, PR zakládá open-pr
# a komentář k PR píše reviewer; paths — spouští se z konverzace nad tématem
# rozhodnutí, ne prací nad konkrétními soubory; shell — postup nespouští nic,
# co by výchozí shell nezvládl; disallowed-tools — allowed-tools je uzavřený
# výčet a skill se vždy spouští loaderem, takže není co zakazovat navíc;
# version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Write ADR

Cílem je rozhodnutí zapsané tak, aby obstálo za rok: čtenář z něj pozná, co se
rozhodlo, proč, co se zvažovalo a co to stálo. Kvalita ADR se láme v interview —
dokument se nezačíná psát, dokud zbývá otázka, která není ani zodpovězená, ani
vědomě přiznaná jako otevřená.

Závazným kontraktem jsou dva referenční soubory vedle tohoto; při rozporu
s tímhle postupem platí ony. Čti je přes `${CLAUDE_PLUGIN_ROOT}` — plugin běží
nad cizím projektem, kde relativní cesta míří jinam.

| Soubor | Kdy ho otevři |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/skills/write-adr/adr-conventions.md` | V kroku 1, dřív než hledáš log — umístění, číslování, stavy, otevřené otázky |
| `${CLAUDE_PLUGIN_ROOT}/skills/write-adr/adr-template.md` | V kroku 1; struktura šablony určuje, na co se musíš v interview doptat |

Git mechaniku skill nepíše: větev zakládá `sagittaras:create-branch`, commit
a PR obstará `sagittaras:open-pr` (ten uvnitř volá `sagittaras:make-commit`).

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

Zadání může nést **číslo ADR** — buď předem rezervované pro nový dokument, nebo
číslo existujícího ADR, jehož otevřené otázky se mají dořešit — a **téma
rozhodnutí**. Co v zadání není, vytěž z konverzace a zbytek zjisti postupem níže.

## Postup

### 1. Příprava a orientace

1. Přečti `adr-conventions.md` a `adr-template.md`.
2. **Najdi log ADR** postupem z kapitoly 1 konvencí. Z nalezených dokumentů
   zjisti zároveň **jazyk logu**, **slovník stavů** a **tvar, který log drží** —
   podle kapitoly 2 má existující tvar přednost před šablonou.
3. **Prolétni existující ADR** (stačí nadpisy a souhrny; ta, kterých se téma
   dotýká, přečti celá). Nové rozhodnutí může na některé navazovat, nahrazovat
   ho, nebo s ním být v rozporu — a všechny tři případy mění, na co se budeš ptát.
4. **Načti zázemí projektu**: `CLAUDE.md`, `.claude/rules/`, a pokud projekt má
   v `CONTRIBUTING.md` sekci `## Workflow (sagittaras)`, i její podsekci
   `Zdroje pravdy` (hodnota „— viz CLAUDE.md" znamená, že jsi je už četl v `CLAUDE.md`
   výše). Bez konfigurace workflow skill běží dál — ADR se píše i v projektu,
   který milestone workflow nepoužívá; chybí ti pak jen ukazatel na
   dokumentaci, kterou musíš najít sám.
5. **Urči režim.** Rozliší se podle toho, co se s rozhodnutím děje — hranici
   popisuje kapitola 5 konvencí:

   | Režim | Kdy | Co vznikne |
   | --- | --- | --- |
   | **Nový ADR** | Rozhoduje se něco, co dosud rozhodnuté nebylo | Nový dokument ve stavu `Navrženo` |
   | **Dořešení** | Téma je položka v „Otevřených otázkách" existujícího ADR | Editace téhož dokumentu, Stav zůstává `Přijato` |
   | **Nahrazení** | Mění se odpověď, kterou už nějaké ADR dalo | Nový dokument + překlopení Stavu původního na `Nahrazeno ADR-NNNN` |

   Nejsi-li si režimem jistý, **zeptej se** a nabídni, co jsi našel. Rozdíl mezi
   dořešením a nahrazením je rozdíl mezi editací a novým dokumentem, a špatná
   volba se opravuje hůř než jakákoli věta uvnitř.
6. **Urči číslo** podle kapitoly 3 konvencí, včetně kontroly čísel rezervovaných
   souběžnou prací na remotu.

### 2. Interview

Nejdůležitější fáze celého skillu. Cílem je, aby se každá sekce dala vyplnit
z toho, co uživatel řekl nebo potvrdil — ne z tvých domněnek.

**Nejdřív vytěž, teprve pak se ptej.** Než položíš první otázku, musíš vědět, co
už zaznělo v konverzaci a co stojí v podkladech z kroku 1. Otázka na něco, co je
napsané v repozitáři, spálí kolo a uživateli řekne, že jsi nečetl — odpovědi pak
chodí kratší a interview se tím zhorší celé.

**U režimu Nový ADR pak nad tímhle vytěženým kontextem ověř, že rozhodnutí
vůbec patří do ADR — ne každé rozhodnutí, jen ohrožené.** Test: narazí-li na
tuhle konstrukci později někdo, člověk nebo agent, bez kontextu, pokusí se ji
věrohodně „opravit" nebo zjednodušit jako zbytečnou komplikaci?

- **Ano** → rozhodnutí je ohrožené, pokračuj interview dál.
- **Ne** — jde o běžnou, levně vratnou, samovysvětlující volbu (typicky výběr
  nástroje nebo knihovny bez skryté ceny) → **ADR se nezakládá**: řekni to
  uživateli i s důvodem a skonči, nezakládej ani soubor, ani větev.
- **Nejsi si jistý** → nerozhoduj to sám. Zeptej se nástrojem `AskUserQuestion`
  s variantami „založit ADR" / „nezakládat", kompromis každé napiš do popisu.
  Trvá-li uživatel na založení, pokračuj interview dál bez dalšího vymáhání
  testu — obsah rozhodnutí je jeho, ne tvůj.

**Test se neprovádí u režimu Dořešení ani Nahrazení** — z jiného důvodu
u každého: u Dořešení se edituje **týž dokument**, který testem prošel při
svém vzniku; u Nahrazení test smysl nedává, protože se zvrací rozhodnutí, které
už jednou do logu patřilo, a bez nového dokumentu nemá původní ADR na co
překlopit svůj Stav.

**Rozliš, na co se ptát a co rozhodnout sám.** Věc se skutečnými kompromisy a bez
zjevné výchozí volby patří uživateli. Věc s běžnou, levnou a vratnou výchozí
volbou rozhodni sám a **důvod napiš do ADR** — otázka na ni jen ředí ty, na
kterých záleží.

**Ptej se po kolech.** Začni jádrem: jaký problém se řeší, proč teď, jaké je
zamýšlené řešení a co se zvažovalo. Podle odpovědí přitvrď v místech, kde se
odpověď rozjíždí. V jednom kole polož nejvýš čtyři otázky.

**Nástrojem AskUserQuestion a s variantami** všude, kde varianty dávají smysl:
doporučenou uveď jako první a označ ji, a **do popisu každé varianty napiš její
kompromis** — volba pak jde udělat na jedno kolo, bez doptávání, co který
řádek vlastně znamená. Otevřené otázky bez variant polož normálním textem.

Interview končí, teprve když umíš vyplnit všechno tohle:

- **Problém** — co se řeší, proč teď a co stojí nerozhodnout.
- **Současný stav** — jak to funguje dnes a co je na tom špatně.
- **Omezení a požadavky** — technická, časová, provozní; kompatibilita. Vstupují
  do Kontextu; vlastní podsekci dostanou, jen když je čeho vyjmenovat.
- **Rozhodnutí** — konkrétně natolik, aby ho šlo implementovat bez doptávání.
- **Alternativy** — reálné, s věcnými důvody zamítnutí. **Nezmíní-li uživatel
  žádnou, navrhni sám jednu až dvě** realistické a nech si potvrdit, proč
  neobstály. ADR bez zvažovaných variant není rozhodnutí, jen zápis.
- **Cena** — negativní důsledky. Slyšíš-li samé klady, zeptej se ještě jednou
  a přímo: co tím ztrácíme, co si tím zavíráme. Rozhodnutí bez ceny znamená,
  že se cena nehledala, ne že žádná není.
- **Rozsah** — kterých částí repozitáře se to týká, lokální nebo průřezové.
  Potřebuješ ho na správné formulování Rozhodnutí; do sekce Dotčené součásti
  ho vypisuj, jen když je co vypsat.
- **Vazby** — navazuje na existující ADR, nahrazuje ho, nebo mu odporuje? Sekci
  Závislosti ADR zakládej jen tehdy, když nějaká vazba je.
- **Zbývající volitelné sekce** ze šablony — rizika, dopady na provoz, migrace,
  kritéria validace, související odkazy. Ptej se na ně jen tehdy, když je povaha
  rozhodnutí otevírá; u rozhodnutí, které nic nemigruje, je otázka na migrační
  plán zdržení. **Odpověď sama o sobě není důvod sekci založit** — dohodnuté
  pravidlo je, že volitelná sekce se vynechává celá, dokud nenese obsah.

**Nabídne-li uživatel kód** — rozhraní, typ, kostru — jednej podle kapitoly 6
konvencí: je to znění rozhodnutí, ne materiál k parafrázi.

**U režimu dořešení interview zúž** na položky, které se dořešují. Neptej se
znovu na to, co dokument už rozhodl; jen ověř, jestli odpověď něčím z toho
nehýbe — pak jde totiž o nahrazení, ne o dořešení.

**Ověř si porozumění.** Než začneš psát, shrň rozhodnutí vlastními slovy
(problém → rozhodnutí → hlavní důvod) a vyjmenuj, které volitelné sekce hodláš
vyplnit. Oprava návrhu stojí jednu větu, oprava hotového dokumentu celé kolo.

**Nemáš-li uživatele, ADR nepiš.** Selže-li volání AskUserQuestion nebo odpověď
nedorazí, **nezakládej soubor ani větev** — shrň, na co potřebuješ odpovědět,
a skonči. Architektonické rozhodnutí vymyšlené za uživatele je horší než žádné:
bude se na ně rok někdo odvolávat.

### 3. Otevřené otázky předlož výslovně

Než začneš psát, vypiš uživateli, co ADR nechává nedořešené, a zeptej se, jestli
to má vyřešit teď, nebo to zůstane otevřené. **Tenhle krok je povinný**, ne
zdvořilost: tiše vypravený ADR s otázkami, na které se nikdo neptal, je stejná
chyba jako tiché vynucení odpovědi na všechno.

- **Vyřešit teď** → vrať se do interview pro ty konkrétní položky a odpovědi
  zapracuj do Rozhodnutí a Důsledků; z výčtu zmizí.
- **Nechat otevřené** → zůstávají v sekci „Otevřené otázky". ADR s přiznanými
  otevřenými otázkami je pořád plnohodnotné rozhodnutí, ne rozpracovaný dokument.

Nezůstane-li nic, krok přeskoč a sekci v dokumentu vůbec nezakládej.

### 4. Sepsání

**Nový ADR** napiš do logu jako `NNNN-kratky-nazev.md`. Kostru vezmi ze šablony,
pokud ale log drží vlastní tvar, řiď se jím (kapitola 2 konvencí). Stav nastav na
`Navrženo` — přijetí je výsledkem review, ne sepsání.

**Dořešení** veď jako editaci existujícího souboru: odpověď vlož do Rozhodnutí
a Důsledků, dořešenou položku z „Otevřených otázek" odstraň, Stav nech být.
Byla-li to poslední položka, **vynech celou sekci i s nadpisem** — prázdný nadpis
vypadá jako opomenutí a konvence (kapitola 5) ho zakazují.

**Nahrazení** znamená dva soubory v jedné změně: nový ADR (s vazbou „Nahrazuje
ADR-NNNN" a s vysvětlením v Kontextu, proč se původní rozhodnutí mění) a překlopený
Stav u původního. **Text původního ADR jinak nesahej** — je to záznam toho, čemu
se tehdy věřilo.

Piš jen to, co uživatel řekl nebo potvrdil. Prázdná sekce je lepší než vymyšlený
obsah; v dokumentu o rozhodování je smyšlenka nejdražší možná chyba.

### 5. Vlastní kontrola

Projdi hotový dokument proti kontrolnímu seznamu v závěru `adr-conventions.md`,
bod po bodu. Reviewer bude kontrolovat proti témuž seznamu — co si opravíš tady,
nemusíš řešit v dalším kole.

Po kontrole **prezentuj hotový dokument uživateli** (cestu k souboru, režim
a Stav) a nástrojem AskUserQuestion se zeptej, jestli má pokračovat vypravení
jako větev a PR s nezávislým review (kroky 6–8), nebo má ADR zatím zůstat jen
v pracovním stromu k doplnění. **Bez výslovného pokynu k pokračování kroky 6–8
nespouštěj** — write-adr se tady zastavuje stejně jako po interview nebo
v kroku 3: ADR, které chce uživatel ještě něčím doplnit před review, si tenhle
prostor zaslouží stejně jako otevřená otázka. Platí to beze zbytku i pro režim
Dořešení — po editaci dokumentu v kroku 4 se tu zastavíš stejně jako u nového
ADR, ne že by dořešení automaticky pokračovalo do zápisu a review.

Selže-li AskUserQuestion nebo odpověď nedorazí, chovej se, jako by odpověď byla
„zatím ne" — vypiš report podle varianty pro zastavený běh a skonči. Řekl-li
uživatel „zatím ne", udělej totéž. Řekl-li, že se má pokračovat, jdi na krok 6 —
ať už v tomtéž běhu, nebo při novém vyvolání `write-adr` nad týmž ADR.

### 6. Vypravení jako větev a PR

**Do tohohle kroku se běh dostane jen po výslovném pokynu z konce kroku 5** —
bez něj tu ADR čeká nezapsané dál. Jakmile pokyn přijde, platí následující beze
změny bez ohledu na to, ve kterém běhu přišel.

Řekl-li uživatel, že se zatím nic vypravovat nemá, **přeskoč podkroky 2 a 3
a s nimi i zápis v krocích 7.2 a 8.2** — dokument zůstane nezapsaný v pracovním
stromu na větvi, na které uživatel stojí. Uživatel si vypravení nepřál, takže se
nezapisuje nic — commit bez vlastní větve by práci navíc přilepil na cizí větev,
kam nepatří.

**Review v kroku 7 spusť vždycky.** Nepotřebuje PR — `review-adr` s tím, že
žádné být nemusí, výslovně počítá — a je to jediná nezávislá kontrola dokumentu;
vynechat ji kvůli odloženému vypravení znamená odevzdat nezrevidované rozhodnutí.
Do zadání pro reviewera dej `PR: žádné — vypravení odloženo`.

1. **Zjisti stav pracovního stromu:**

   ```bash
   git status --porcelain
   git branch --show-current
   ```

   Vlastní ADR ve výpisu očekávej — ten do větve patří. Jsou-li tam navíc
   **nesouvisející rozpracované změny**, řekni to uživateli a nech ho rozhodnout,
   než budeš pokračovat. Větev je vezme s sebou a commit by je vtáhl do ADR PR,
   kde je nikdo nečeká.

2. **Založ větev** nástrojem `Skill`, skill `sagittaras:create-branch`, a předej
   mu **hotový název**. Bez předaného názvu si ho nechá potvrdit zvlášť, což je
   kolo navíc za něco, co už je dané. Základní větev neurčuj, ledaže ti ji
   předal volající. Odpověď skriptu si nech — klíč `base=` potřebuješ v kroku 7.1.

   | Režim | Název větve |
   | --- | --- |
   | Nový ADR, nahrazení | `docs/adr-NNNN-kratky-nazev` se stejným slugem jako soubor |
   | Dořešení | `docs/adr-NNNN-kratky-nazev-doreseni` |

   Dořešení má vlastní příponu proto, že soubor ani jeho slug se nemění — větev
   pojmenovaná jako ta původní by kolidovala prakticky vždy, protože z prvního
   běhu zůstala v klonu ležet. **U ADR větví má přednost tahle tabulka** před
   pravidlem `create-branch` „nepřipojuj pořadové číslo, vymysli jiný popis":
   popisný náhradní název by rozpojil slug větve od slugu souboru, který se
   u ADR měnit nesmí.

   Skončí-li `checkout_failed`, větev nevznikla — ohlas to a nepokračuj.

   Skončí-li kódem `4` (`branch_exists_locally` nebo `branch_exists_on_remote`),
   reaguj podle režimu:

   - **Nový ADR, nahrazení** → náhradní název nepřijímej. Větev s tímhle číslem
     už existuje, takže číslo je zabrané někým jiným — vrať se na jeho určení
     v kroku 1.6. Náhradní název by rozpojil slug souboru od slugu větve, což
     konvence zakazují.
   - **Dořešení** → číslo zabrané není, jen se dořešuje podruhé. Odliš název
     dál (`…-doreseni-2`) a zopakuj; konvence u dořešení rozchod slugu větve
     a souboru výslovně připouštějí.

3. **Otevři PR** nástrojem `Skill`, skill `sagittaras:open-pr`. Do zadání dej,
   že jde o ADR, jeho číslo a název, a že PR **žádné issue neuzavírá** (pokud
   uživatel nějaké neuvedl). Commit, push i publikaci větve řeší `open-pr` sám
   přes `make-commit`; vlastní commit logiku nepiš.

   Nemá-li projekt konfiguraci workflow, `open-pr` se zastaví hned ve svém prvním
   kroku a odkáže na `init-workflow` — tedy **dřív, než cokoli commitne**.
   Není to důvod cokoli rušit: ADR je sepsaný v pracovním stromu a zápis obstará
   krok 8. Pokračuj krokem 7 s tím, že PR neexistuje, a napiš to do reportu.

### 7. Nezávislé review

ADR musí projít nezávislým review podle `review-adr`. **Nikdy ho neprováděj sám**:
jsi autor a tvůj kontext nese celé interview, takže si přečteš i to, co v dokumentu
není. Nezávislost dělá subagent s čistým kontextem, který o rozhovoru neví nic
a všechno si musí přečíst ze souborů — přesně na to je `review-adr` napsaný.

1. Nástrojem Agent spusť subagenta **synchronně** (`run_in_background: false`) —
   bez verdiktu nemáš jak pokračovat. Typ agenta zvol **`general-purpose`**, model
   vezmi z frontmatteru `review-adr` a předej ho parametrem: subagent si ho sám
   neuplatní. Čtecí profily (`Plan`, `Explore`) nepoužívej — reviewer musí umět
   zapsat komentář k PR a ty by mu zápis vzaly.

   **Effort parametrem předat nejde** — nástroj Agent ho nemá, tak ho napiš do
   zadání jako pokyn. Bez něj poběží reviewer s effortem tvojí session, který
   bývá nižší, než na jakém má pracovat poslední brána.

   **Do zadání dosaď rozvinutou absolutní cestu ke kořeni pluginu**, nikde nenech
   proměnnou: subagent čte skill jako soubor, takže `${CLAUDE_PLUGIN_ROOT}` se mu
   nerozvine a zůstane literálem — a on si pak neotevře ani vlastní postup, ani
   konvence, aniž by to bylo z verdiktu poznat.

   **Sahá-li běh na už přijatý dokument, připoj do zadání jeho diff.** Bez něj
   reviewer nemá jak ověřit, že se v něm nezměnilo nic nad rámec toho, co se
   měnit smělo — a tenhle invariant nikdo jiný v procesu nehlídá:

   | Režim | Diff čeho | Co se smí lišit |
   | --- | --- | --- |
   | Dořešení | posuzovaného ADR | Rozhodnutí, Důsledky, výčet Otevřených otázek |
   | Nahrazení | **původního** ADR, ne nového | jediný řádek se Stavem |
   | Nový ADR | — | řádek do zadání nedávej |

   ```bash
   git diff "<base>...HEAD" -- <cesta k dokumentu>
   ```

   `<base>` je hodnota, kterou vrátil `create-branch` klíčem `base=` (krok 6.2).
   Je to **hotový ref včetně `origin/`**, takže ho dosaď tak, jak přišel —
   dopsaný prefix by z něj udělal `origin/origin/main` a git skončí na neplatné
   revizi. Nevznikla-li větev (odložené vypravení) nebo není-li změna ještě
   zapsaná, platí rovnou `git diff -- <cesta k dokumentu>`; jinou základní větev
   si nedomýšlej.

   Výstup vlož do zadání jako fenced blok — u dořešení spolu s výčtem otázek,
   které se dořešily.

   Zadání sestav podle šablony ve Formátu výstupu.

2. **Vráceno k dopracování** → zapracuj všechny blokující nálezy, doporučení
   uvážlivě zvaž. Změnu zapiš a odešli přes `sagittaras:make-commit` a spusť
   další kolo s **novým** subagentem; tomu vypotřebovanému opravu nedávej,
   ztratil by odstup. Stopa kol zůstává v komentářích reviewera u PR, kde má
   každé další kolo sekci s vypořádáním toho minulého — vlastní komentář k PR
   proto nepiš.

   Zápis se řídí tím, co vzniklo v kroku 6:

   | Stav po kroku 6 | Co udělat |
   | --- | --- |
   | Větev existuje (s PR i bez něj) | zapiš přes `make-commit` a nech ho pracovat — pushuje po každém commitu a větev bez upstreamu sám publikuje |
   | Vypravení odložené, větev není | **nezapisuj vůbec** — oprav jen soubor v pracovním stromu |

   **Push `make-commit` nezakazuj.** Běží-li review nad PR, nepushnutá oprava by
   znamenala verdikt nad jinou verzí, než jakou PR ukazuje. Vyžadovat ho zvlášť
   naopak nemusíš: push i publikace větve jsou jeho výchozí konec práce, ne krok
   na zmocnění.

3. **Schváleno** → pokračuj krokem 8.

Nálezy neodmítej mlčky. Reviewer nezná interview, takže může napadnout něco, co
uživatel vědomě chtěl — takový nález patří do reportu i s důvodem odmítnutí,
ne do koše.

### 8. Uzavření

1. U **nového ADR i u nahrazení** překlop Stav na `Přijato` — review je ta brána,
   která o přijetí rozhoduje. U **dořešení** Stav nech být, ADR je přijaté už dávno.
2. Změnu zapiš přes `sagittaras:make-commit` podle **téže tabulky jako v kroku
   7.2**. Nevzniklo-li PR kvůli chybějící konfiguraci, je tohle jediné místo,
   kde se dokument vůbec zapíše — krok proto nepřeskakuj jen proto, že `open-pr`
   v kroku 6.3 skončil bez PR. Při odloženém vypravení se naopak nezapisuje nic;
   dokument zůstává v pracovním stromu.
3. Reportuj podle Formátu výstupu; do řádku `PR:` uveď i to, v jakém stavu
   vypravení skončilo.

**PR nemerguj.** Merge do výchozí větve patří člověku — je to pravidlo celého
pluginu, ne opatrnost tohoto skillu.

### 9. Eskalace

Přeruš postup a obrať se na uživatele, když:

- nález zpochybňuje podstatu rozhodnutí nebo cokoli, co uživatel v interview
  výslovně potvrdil — obsah rozhodnutí vlastní on, ne ty ani reviewer;
- stejný blokující nález přetrvává i po tvém pokusu o opravu (dvě kola);
- proběhla tři kola bez schválení;
- číslo ADR koliduje s rezervovaným a není zřejmé, které je správné;
- narazíš na technickou chybu, kterou opakování nevyřeší — větev, PR, spuštění
  subagenta.

Při eskalaci shrň stav (kolo, verdikt, sporný nález), odkaž na PR a polož
**jednu konkrétní otázku**. Mlhavá eskalace uživatele jen zdrží.

## Formát výstupu

### Zastavený report (konec kroku 5)

Vypiš ho místo Závěrečného reportu, když se běh po kroku 5 zastavil bez
pokynu k pokračování — bez ohledu na to, jestli šlo o nový ADR, dořešení,
nebo nahrazení:

```
ADR-<NNNN>: <název> (<cesta k souboru>)
Režim: <nový | dořešení | nahrazení ADR-NNNN>
Stav: <Navrženo | Přijato — u dořešení beze změny>
PR: nevzniklo — čeká na pokyn k vypravení

Další krok: potvrď vypravení jako větev a PR s nezávislým review — v týhle
konverzaci, nebo novým vyvoláním /sagittaras:write-adr nad tímhle ADR.
```

### Zadání pro reviewera

Reviewer ho parsuje a nekompletní zadání označí za nález, kterým kolo skončí —
posílej ho v téhle struktuře:

```
Přečti si soubor `<kořen pluginu>/skills/review-adr/SKILL.md` a proveď přesně
jeho postup. Pracuj s effortem <hodnota z frontmatteru review-adr>.

Zadání pro tvůj běh:
- Kořen pluginu: <absolutní cesta, rozvinutá — ne proměnná>
- Repozitář: <absolutní cesta ke kořeni cílového projektu>
- Posuzované ADR: <cesta k dokumentu; u nahrazení i cesta k původnímu ADR>
- Režim: <nový ADR | dořešení otevřených otázek | nahrazení ADR-NNNN>
- Dořešené otevřené otázky: <jen u režimu dořešení: výčet položek, které se
  dořešily; u ostatních režimů řádek vynech>
- Diff dokumentu: <u dořešení diff posuzovaného ADR, u nahrazení diff původního
  ADR — výstup `git diff` jako fenced blok; u nového ADR řádek vynech>
- PR: <číslo | „žádné — PR nevzniklo" | „žádné — vypravení odloženo">
- Číslo kola: <N>
- Nevyřešené nálezy z minulého kola: <žádné, jde o první kolo | seznam nálezů
  i s tím, jak jsi je řešil>

Vrať verdikt přesně ve struktuře, kterou review-adr předepisuje v sekci
„Formát výstupu".
```

### Závěrečný report uživateli

```
ADR-<NNNN>: <název> (<cesta k souboru>)
Režim: <nový | dořešení | nahrazení ADR-NNNN>
Stav: Přijato<, u dořešení připoj „(beze změny, ADR bylo přijaté dřív)">
PR: <„#<číslo> — <url>" | „nevzniklo — chybí konfigurace workflow, ADR zapsaný
    na větvi <název>" | „nevzniklo — vypravení odloženo, ADR leží nezapsaný
    v pracovním stromu">
Kol review: <N>
Otevřené otázky: <počet ponechaných, nebo „žádné">
Odmítnuté nálezy: <nález → důvod odmítnutí, nebo „žádné">

Další krok: merge PR — patří člověku.
```

## Zásady

- **Referenční soubory mají přednost.** Odporuje-li tenhle postup konvencím
  nebo šabloně, platí ony.
- **Bez interview ADR nevzniká, a bez pokynu nejde do vypravení a review.**
  Interview, zastavení po kroku 5, krok 3 a eskalace jsou fáze, které vyžadují
  uživatele; uvnitř nich (psaní, vypravení, review a opravná smyčka) běží práce
  autonomně a nepřerušuje se kvůli průběžnému hlášení.
- **Nepiš nic, co uživatel neřekl nebo nepotvrdil** — a totéž platí ve smyčce:
  oprava nálezu nesmí tiše změnit podstatu rozhodnutí. Od toho je eskalace.
- **Review si neděláš sám.** Vlastní kontrola v kroku 5 ho nenahrazuje: autor
  nevidí, co do dokumentu podvědomě doplnil z hlavy.
- **Přijaté ADR se nepřepisuje.** Dořešit se smí jen to, co si dokument sám
  vyhradil; cokoli dalšího je nový ADR a překlopený Stav u původního.
- **Merge patří člověku.** Skill končí schváleným PR, ne zmergovaným.
