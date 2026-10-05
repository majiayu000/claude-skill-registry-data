---
name: write-rule
description: >-
  Vytvoří rule v `.claude/rules/` cílového projektu nebo upraví existující —
  vytěží konvence z repozitáře, provede interview, navrhne `paths` globy
  a ověří je proti reálné struktuře, sepíše soubor podle závazné šablony
  a nechá ho nezávisle zrevidovat subagentem s čistým kontextem. Umí i rozpad
  nabobtnalého CLAUDE.md na path-scoped rules.
when_to_use: >-
  Použij, když má v projektu vzniknout nebo se změnit pravidlo pro Claude —
  „přidej rule na…", „napiš pravidla pro testy", „ať Claude ví, jak psát naše
  API", „uprav rule" — i když uživatel jen popisuje konvenci, kterou má dodržet
  každý, kdo sáhne na určitou část repozitáře. Použij i na rozpad dlouhého
  CLAUDE.md, mají-li se bloky přestěhovat do path-scoped rules. Nepoužívej pro
  sepsání ani zeštíhlení samotného CLAUDE.md škrtáním, na to slouží
  write-claude-md; ani pro zakládání skillů, na to write-skill; ani agentů, na to
  write-agent; ani pro záznam architektonického rozhodnutí i s alternativami
  a důsledky, na to je write-adr; pro posouzení hotové rule slouží review-rule;
  ani pro paměť agenta, tu plní train-agent; ani pro závazný popis vzhledu
  projektu jako celku (paleta, typografie, katalog prvků), na to write-art-bible;
  ani pro popis jedné obrazovky nebo flow, na to write-ux-spec.
argument-hint: "[téma pravidla nebo cesta k existující rule]"
model: opus
effort: high
# Zařazení dle matice: orchestrace workflow s autonomní smyčkou — matice na ni
# má řádek opus × xhigh. Snížení na high je odchylka o stupeň: nejtěžší část
# (review) je delegovaná na review-rule běžící na opus × xhigh, takže vlastní
# práce tohoto skillu je průzkum repozitáře, interview a krátký text. Nikoli
# sonnet: skill navrhuje globy nad cizí strukturou a rozhoduje, co do rule
# patří a co ne — chybný glob znamená rule, která se nikdy nenačte, a nic
# nespadne, takže se to nepozná.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Agent
# Glob není jen na hledání souborů: ověření navržených globů proti reálné
# struktuře repozitáře je povinný krok 5 a bez tohoto nástroje ho nelze udělat.
# Vynechaná zvažovaná pole: disable-model-invocation — skill má být volatelný
# i tehdy, když uživatel popíše konvenci, aniž by slovo rule zmínil;
# context/agent/background — interview vyžaduje uživatele v hlavním kontextu,
# fork ani běh na pozadí nemají komu klást otázky; paths — skill se spouští
# z konverzace o pravidle, ne prací nad konkrétními soubory; shell — postup je
# průzkum, psaní souborů a volání subagenta, ne spouštění příkazů;
# disallowed-tools — allowed-tools je uzavřený výčet, není co zakazovat navíc;
# version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Write Rule

Cílem je rule, která se načte právě tam, kde má, a jejíž pravidla jdou dodržet
i porušit prokazatelně. Závazným kontraktem jsou dva referenční soubory vedle
tohoto — při rozporu s čímkoli, včetně tohoto skillu, mají přednost ony.

Referenční soubory čti přes `${CLAUDE_PLUGIN_ROOT}`; plugin běží nad cizím
projektem, kde relativní cesta `skills/…` míří někam jinam.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Příprava

1. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-rule/rule-conventions.md` — pravidla
   pojmenování, `paths` a těla, na která se budeš celou dobu odvolávat.
2. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-rule/rule-template.md` — kostru,
   do které budeš psát.
3. Urči **režim** podle zadání a konverzace; na něm závisí zbytek postupu:
   - **Nová rule** — vzniká soubor, který zatím není.
   - **Úprava** — mění se existující rule. Přečti ji celou ještě před interview;
     bez znalosti toho, co dnes říká a co matchuje, nejde poznat, co se změnou
     rozbije.
   - **Rozpad `CLAUDE.md`** — z jednoho nabobtnalého souboru vzniká víc rules.
     Tuhle větev řídí krok 4b.
4. Urči **cílové umístění**:
   - `.claude/rules/` cílového projektu — výchozí volba, pravidlo je týmové
     a patří pod verzi;
   - `~/.claude/rules/` — jen pro osobní preferenci nezávislou na projektu.
     Tuhle volbu si nech **výslovně potvrdit**: user-level rule se načítá
     v každém projektu na stroji, takže projektové pravidlo uložené sem začne
     mluvit do cizích repozitářů. Vlnovku před zápisem nahraď rozvinutou
     domovskou cestou — Write ji sám nerozvine a založil by složku `~`
     v pracovním adresáři.
5. Udělej inventuru toho, co v projektu už platí — `CLAUDE.md` (v kořeni
   i v `.claude/`) a všechny soubory v `.claude/rules/` včetně podsložek. Zajímá
   tě, co už je pokryté a čím. **Rule, která si odporuje se sousedem, je horší
   než žádná**: model si při rozporu vybere jednu z instrukcí a nedá se
   předvídat kterou. Najdeš-li překryv, patří jeho vyřešení do zadání — soused,
   kterého kvůli tomu upravíš, jde v kroku 6 do review spolu s novou rule.
   **Míří-li rule do `~/.claude/rules/`, projdi i ostatní soubory v této
   složce** — to jsou její skuteční sousedé a kolizi s nimi jinde nenajdeš.
   Vlnovku si i tady rozviň na absolutní domovskou cestu: Read ani Glob ji
   nerozvinou, průchod by tiše nevrátil nic a ty bys uzavřel, že rule žádné
   sousedy nemá.

### 2. Průzkum cílového projektu

Než se začneš ptát, přines si podklad. Interview nad prázdným listem vytáhne
z uživatele obecnosti; interview nad konkrétním návrhem vytáhne opravy, a ty
jsou přesně to, co do rule patří.

Podle tématu projdi:

- **konfigurace, které konvenci už nesou** — `.editorconfig`, konfigurace
  linteru a formátovače, `tsconfig.json`, nastavení test runneru. Co je vynucené
  nástrojem, do rule většinou nepatří podruhé; co nástroj nevynutí, je kandidát;
- **reprezentativní soubory z oblasti**, které se rule bude týkat — skutečný
  styl projektu se pozná z kódu, ne z toho, co si o něm kdo myslí;
- **strukturu složek**, ze které odvodíš tvar globů.

Rozejde-li se konvence v kódu s tím, co říká uživatel, **zeptej se na to
v interview**. Obojí bývá pravda: kód ukazuje stav, uživatel záměr — a rule
se píše na záměr, ale s vědomím, kolik souborů ho dnes porušuje.

### 3. Interview

Piš jen to, co víš od uživatele. Nejdřív vytěž konverzaci a průzkum, pak se
doptej po kolech — nástrojem AskUserQuestion a s konkrétními možnostmi tam, kde
dávají smysl. Zjisti:

- **Jestli obsah do rule vůbec patří** — tohle je první otázka, ne poslední.
  Projdi zadání proti kapitole 1 `rule-conventions.md`. Instrukce, která musí
  platit i po `/compact` a bez doteku odpovídajících souborů, patří do
  `CLAUDE.md`, nebo do rule bez `paths` — podle toho, jestli by blok `CLAUDE.md`
  utopil; vícekrokový postup do skillu; co se musí vynutit bez výjimky, do hooku;
  co už hlídá linter, nikam. Závazný popis vzhledu projektu jako celku — paleta,
  typografie, katalog prvků — patří do art bible; navrhni `write-art-bible`
  a v rule nech jen tu část, která je vymahatelná a vázaná na konkrétní soubory.
  Vyjde-li z toho jiné místo než rule, řekni to uživateli a navrhni ho — rule
  napsaná místo hooku vypadá jako řešení, ale nic nevynutí.
- **Téma a hranice** — čeho se pravidla týkají a co už je za hranicí.
- **Rozsah platnosti** — na které soubory rule dopadá. Odtud plynou globy;
  navrhni je a nech si je potvrdit. **Ještě před potvrzením je ověř nástrojem
  Glob** a nulový match uživateli předlož: buď se glob opraví, nebo si uživatel
  potvrdí, že rule píše dopředu pro oblast, která teprve vznikne — a ty to
  vykážeš v zadání pro reviewera. Bez téhle otázky v interview nemáš čím
  výjimku v kroku 5 podložit. Platí-li pravidla pro celý repozitář, je to
  vědomé rozhodnutí napsat rule bez `paths`, ne opomenutí.
- **Konkrétní pravidla** — předlož návrh z průzkumu a nech ho opravit. U každého
  pravidla se ptej, jak se pozná porušení; na co se nedá odpovědět, do rule
  nepatří.
- **Důvody** — u pravidel, která nejsou samozřejmá. Bez důvodu je model použije
  doslova a v situaci, kterou autor nepředvídal, sáhne vedle.
- **Ukázky** — u pravidel, jejichž tvar se slovy popisuje hůř než kódem.
- **Název souboru** — navrhni `<téma>.md` a nech si ho potvrdit.

**U úpravy interview zúž** na to, co se mění. Nepřepisuj pravidla, na která se
nikdo neptal.

**U rozpadu interview zúž jinak.** Pravidla už existují a jen se stěhují, takže
se na jejich obsah neptej — potvrzuje se tabulka blok → cíl podle kroku 4b
a k ní název souboru a globy pro **každou** vznikající rule. Ptát se u rozpadu
na vymahatelnost jednotlivých odrážek znamená přepisovat instrukce, které nikdo
měnit nechtěl; co je slabé, si uživatel může říct sám, ale není to úkol tohoto
běhu.

Interview končí, až umíš vyplnit celou kostru ze šablony. Než začneš psát, shrň
uživateli, co v rule bude, kam se uloží a co budou matchovat globy, a nech si
shrnutí potvrdit — oprava návrhu stojí jednu větu, oprava hotové rule celé kolo.

**Nemáš-li uživatele, rule nepiš.** Pravidlo vymyšlené z domněnek se do kontextu
načte stejně spolehlivě jako to správné a tiše ovlivní všechnu další práci
v projektu. Selže-li volání AskUserQuestion nebo odpověď nedorazí, shrň, na co
potřebuješ odpovědět, a skonči — nezakládej soubory.

### 4. Sepsání

**Novou rule** napiš tak, že okopíruješ kostru z `rule-template.md` a vyplníš
ji. Šablona je kostra k vyplnění, ne text k opsání: placeholdery nahraď, závorky
i značky `(volitelné)` odstraň, nepoužité volitelné sekce smaž celé.

**Úpravu** veď ze stávajícího souboru — měň jen to, co se mění. Přepsat fungující
rule ze šablony znamená zahodit pravidla, která tam někdo dal z důvodu, jenž
v konverzaci nezazněl.

Piš normativně a konkrétně, jednu myšlenku na odrážku. Jazyk převezmi ze
stávajících rules projektu, ne z této session.

#### 4b. Větev: rozpad `CLAUDE.md`

Rozpad je přesun instrukcí, ne jejich přepis. Postupuj takto:

Interview k této větvi zužuje krok 3; sem přijď s tabulkou, ne s pravidly.

1. Přečti celý `CLAUDE.md` a rozděl jeho obsah do tří skupin: **zůstává**
   (platí pro celý projekt v každé session — build a test příkazy, architektura,
   rozvržení repozitáře), **přesouvá se do rule** (tematický blok vázaný na část
   repozitáře), **zahodit** (co si model odvodí sám z kódu, nebo co už neplatí).
2. Předlož rozdělení uživateli jako tabulku blok → cíl a **nech si ho potvrdit
   celé, než sáhneš na jediný soubor**. Rozpad mění instrukce, podle kterých
   pracuje každá další session v projektu; provedený rozpad se špatně rozmýšlí
   zpětně. **Potvrzenou tabulku si uschovej** — v kroku 6 ji předáš reviewerovi.
   Je to jediný záznam původního stavu: `CLAUDE.md` už bude přepsaný a reviewer
   nemá čím ověřit, že se cestou žádná instrukce neztratila.
3. Teprve po potvrzení založ jednotlivé rules podle šablony a **až nakonec**
   odeber přesunuté bloky z `CLAUDE.md`. Tímhle pořadím se instrukce nikdy
   neztratí — mezistav, kdy jsou na dvou místech, je neškodný, mezistav, kdy
   nejsou nikde, ne. Po odebrání **přečti `CLAUDE.md` znovu celý a ukliď, co po
   blocích zbylo**: osiřelé nadpisy, odkazy na přesunutý obsah a věty ohlašující
   výčet, který už tam není. Úplnost přesunu sama o sobě nezaručí, že zbytek
   souboru dává smysl.
4. Vzniklé rules i upravený `CLAUDE.md` jdou do review společně.

**Rozpad není zeštíhlení.** Sem patří jen bloky, které se stěhují do rules,
protože jsou vázané na část repozitáře. Je-li `CLAUDE.md` i po přesunu rozvláčný,
je to práce pro `write-claude-md` — ten škrtá a přeformulovává, což tenhle skill
záměrně nedělá: instrukci, kterou má vlastnit `CLAUDE.md`, nepřepisuj cestou
kolem.

### 5. Vlastní kontrola

1. **Ověř každý glob nástrojem Glob** proti reálné struktuře repozitáře a podívej
   se, co vrátil. Vzor, který nematchuje nic, je rule, která se nikdy nenačte —
   a nepozná se to, protože nic nespadne. Vzor, který matchuje půl repozitáře,
   je zase rule tažená do kontextu u práce, které se netýká; obojí oprav teď.

   **Dvě výjimky, u kterých nulový match není důvod glob měnit:** rule
   v `~/.claude/rules/` platí ve všech projektech na stroji, takže se proti
   jednomu repozitáři ověřit nedá — u ní posuď jen tvar a šíři vzoru. A rule
   psaná dopředu pro oblast, která teprve vznikne, je legitimní, pokud to
   uživatel v interview takhle chtěl. Obojí uveď v zadání pro reviewera, jinak
   ti to vrátí jako blokující nález.
2. Projdi rule proti kontrolnímu seznamu v závěru `rule-conventions.md`, bod po
   bodu. Zvlášť ověř, že v souboru nezůstal placeholder ani značka `(volitelné)`
   a že ve frontmatteru není jiné pole než `paths`.

Reviewer bude kontrolovat proti témuž seznamu — co si opravíš tady, nemusíš
řešit v dalším kole.

### 6. Nezávislé review

1. Nástrojem Agent spusť subagenta **synchronně** (`run_in_background: false`) —
   bez verdiktu nemáš jak pokračovat. Typ agenta a model vezmi z frontmatteru
   `review-rule` a předej je parametry nástroje: jako subagent si je sám
   neuplatní, takže co nepředáš, se nepoužije. Zadání sestav podle šablony
   ve Formátu výstupu.

   **Effort parametrem předat nejde** — nástroj Agent ho nemá, takže ho napiš
   do zadání jako pokyn. Je to slabší záruka než parametr, ale bez něj poběží
   reviewer s effortem tvojí session, který bývá nižší než ten, na kterém má
   poslední brána pracovat.

   **Do zadání dosaď rozvinuté absolutní cesty** — ke kořeni pluginu i k cílovému
   repozitáři, nikde nenech proměnnou. Reviewer čte soubory jako subagent a nemá
   jak si je dopočítat; bez cesty ke kořeni pluginu si neotevře ani vlastní
   postup, ani konvence, a z kola vypadne celá kontrola konformity, aniž by to
   bylo poznat. Bez cesty k repozitáři neověří globy.

   Subagent startuje s čistým kontextem — právě proto je jeho pohled nezávislý,
   a právě proto si historii kol nepamatuje. Co mu nepředáš, pro něj neexistuje.

2. **Vráceno k dopracování** → zapracuj všechny blokující nálezy, doporučení
   uvážlivě zvaž. Pak spusť další kolo s **novým** subagentem; tomu vypotřebovanému
   nedávej opravu k posouzení, ztratil by odstup.

3. **Schváleno** → rule je hotová. Reportuj uživateli podle šablony ve Formátu
   výstupu.

Nálezy neodmítej mlčky. Reviewer nezná interview, takže může napadnout pravidlo,
které uživatel vědomě chtěl — takový nález patří do reportu, ne do koše.

### 7. Eskalace

Přeruš smyčku a obrať se na uživatele, když:

- nález zpochybňuje pravidlo nebo rozsah, který uživatel v interview výslovně
  potvrdil — obsah pravidel vlastní uživatel, ne ty ani reviewer;
- stejný blokující nález přetrvává i po tvém pokusu o opravu (dvě kola);
- proběhla tři kola bez schválení;
- narazíš na technickou chybu, kterou opakování nevyřeší.

Při eskalaci shrň stav smyčky, ocituj sporný nález a polož konkrétní otázku.
Mlhavá eskalace uživatele jen zdrží.

## Formát výstupu

### Umístění souboru

```
<kořen projektu>/.claude/rules/<téma>.md          ← týmové pravidlo pod verzí
<kořen projektu>/.claude/rules/<oblast>/<téma>.md ← u velkých repozitářů
~/.claude/rules/<téma>.md                         ← osobní preference napříč projekty
```

Poslední tvar je zápis pro člověka. **Při zápisu vlnovku nahraď rozvinutou
domovskou cestou** — Write ji nerozvine a založil by složku `~` v pracovním
adresáři.

### Zadání pro reviewera

Reviewer ho parsuje a nekompletní zadání označí za nález, kterým kolo skončí —
proto ho posílej v této struktuře:

```
Přečti si soubor `<kořen pluginu>/skills/review-rule/SKILL.md`
a proveď přesně jeho postup. Pracuj s effortem <hodnota z frontmatteru
review-rule>.

Zadání pro tvůj běh:
- Kořen pluginu: <absolutní cesta, rozvinutá — ne proměnná>
- Repozitář: <absolutní cesta k repozitáři cílového projektu>
- Posuzované rules: <cesta k nové rule; cesty ke všem upraveným sousedům>
- Umístění: <.claude/rules/ projektu | ~/.claude/rules/, rozvinutá cesta>
- Globy bez shody schválené uživatelem: <vzor a důvod — dopředná rule pro oblast,
  která teprve vznikne; jinak „žádné">
- Upravený CLAUDE.md: <cesta, byl-li v tomto běhu změněn — rozpadem i kvůli
  vyřešení překryvu; jinak „netýká se">
- Rozpad CLAUDE.md: <potvrzená tabulka blok → cíl z kroku 4b; jinak „netýká se">
- Číslo kola: <N>
- Nevyřešené nálezy z minulého kola: <žádné, jde o první kolo | seznam nálezů
  i s tím, jak jsi je řešil>

Vrať verdikt přesně ve struktuře, kterou review-rule předepisuje v sekci
„Formát výstupu".
```

### Závěrečný report uživateli

```
Rule: <název souboru> (<cesta>)
Rozsah: <globy z paths a co matchují — nebo „bez paths, platí vždy">
Pravidel: <počet>
Dotčené sousedící soubory: <výčet upravených rules a CLAUDE.md, nebo „žádné">
Kol review: <N>
Odmítnuté nálezy: <nález → důvod odmítnutí, nebo „žádné">
```

## Zásady

- Referenční soubory mají přednost před tímto skillem. Když si odporují, platí
  konvence a šablona, ne tento postup.
- **Patří-li obsah do `CLAUDE.md`, skillu, hooku nebo art bible, rule nepiš**
  a navrhni správné místo. Rule napsaná místo hooku vypadá jako řešení, ale nic
  nevynutí — a to se pozná, až když na ní někdo postaví postup; paleta
  a typografie zapsané do rule místo do art bible platí jen tam, kam dosáhnou
  `paths`, takže zbytek projektu vypadá jinak.
- **Pravidlo, u kterého nejde poznat porušení, do rule nepatří.** Nevymahatelná
  odrážka zabírá kontext v každé session a nezmění nic.
- **Rule se nesmí rozejít s `CLAUDE.md` ani se sousedy.** Rozpor neřeš přidáním
  třetí formulace — najdi ji a oprav. U user-level rule to platí vůči sousedům
  v `~/.claude/rules/`; rozpor s projektovou vrstvou řeší priorita načítání
  (projektová rule vyhrává) a cizí projekt kvůli osobní preferenci nepřepisuj.
- Uživatele vyžadují tři věci: interview, eskalace a u rozpadu potvrzení tabulky
  blok → cíl (krok 4b) — bez nich rule nevzniká. Jinde běží smyčka psaní
  a review autonomně; nepřerušuj ji kvůli průběžnému hlášení.
- Review si neděláš sám. Vlastní kontrola v kroku 5 ho nenahrazuje: autor nevidí,
  co do pravidel podvědomě doplnil z hlavy.
- Do review jde **všechno, čeho ses dotkl** — nová rule, upravení sousedé
  i `CLAUDE.md`, ať už jsi ho změnil rozpadem, nebo kvůli vyřešení překryvu.
