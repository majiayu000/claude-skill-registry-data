---
name: write-claude-md
description: >-
  Sepíše nebo zeštíhlí CLAUDE.md cílového projektu — zmapuje strukturu repa
  a tech stack, záměr projektu si vyžádá od uživatele, předloží osnovu
  a teprve po odsouhlasení soubor zapíše. Míří na ~80 řádků se stropem 200;
  hlubší dokumentaci odkazuje místo opisování a existující soubor bere
  jako vstup, ne jako odpad.
when_to_use: >-
  Použij, když má v projektu vzniknout nebo se zeštíhlit CLAUDE.md — „napiš
  CLAUDE.md", „udělej projektové instrukce", „ten CLAUDE.md je zbytečně
  dlouhý, zkrať ho" — i tehdy, když si uživatel stěžuje, že model neví,
  na čem projekt stojí. Na CLAUDE.md sahej tímhle skillem, ne vestavěným
  /init, jehož výstup bývá rozvláčný. Nepoužívej, mají-li se bloky přestěhovat
  do path-scoped rules místo škrtnutí — to je rozpad a umí ho write-rule;
  ani pro zakládání skillů, na to slouží write-skill; pro agenty write-agent;
  pro závazný popis vzhledu projektu write-art-bible; pro záznam
  architektonického rozhodnutí write-adr; ani pro zápis do trvalé
  paměti agenta, na to je train-agent.
argument-hint: "[co má soubor zdůraznit]"
model: sonnet
effort: high
# Zařazení dle matice: ohraničené zadání se známým tvarem výstupu → sonnet
# (bod 2 rozhodovacího stromu), effort high podle řádku „copywriting podle
# zadaného briefu". Nikoli medium: hodnota skillu je ve škrtání, a matice
# u medium výslovně říká, že model nerozvíjí nic nad rámec zadání — rozhodnout,
# co do souboru nepatří, je přesně ten úsudek navíc. Nikoli opus: průzkum
# a text mají známý tvar a skill poběží často.
# Odchylka od konvence pojmenování: název má tři slova. `claude-md` je ale jeden
# název artefaktu, ne dva předměty — skill dělá jednu věc. Zkrácení na
# `write-instructions` nebo `write-context` by triggering zhoršilo, protože
# uživatel řekne přesně „CLAUDE.md".
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Write
  - Edit
  - AskUserQuestion
# Vynechaná zvažovaná pole: Grep — průzkum hledá soubory a čte manifesty, tedy
# Glob a Read; hledat vzory uvnitř kódu skill zásadně nepotřebuje, protože kód
# nečte (viz krok 2); Bash — průzkum stojí na Glob a Read, a plugin drží
# Bash vyhrazený pro vlastní skripty; `git log` by nabídl obraz rozdělané práce,
# jenže ten do souboru čteného v každé session nepatří (viz zákaz obsahu
# vázaného na období v referenci) — trvalý záměr projektu skill získává
# od uživatele v kroku 3; disable-model-invocation — zápis se potvrzuje osnovou v kroku 4,
# takže brzda existuje a skill má jít zřetězit za práci, která projekt založila;
# Agent — review smyčku skill nemá (viz Zásady), takže není koho spouštět;
# context/agent/background — interview i schválení osnovy vyžadují uživatele
# v hlavním kontextu, fork ani běh na pozadí nemají komu klást otázky; paths —
# skill se spouští z konverzace nad projektem, ne prací nad konkrétními
# soubory; shell — nespouští příkazy; disallowed-tools — allowed-tools je
# uzavřený výčet, není co zakazovat navíc; version/license — verzuje se celý
# plugin, ne jednotlivý skill.
---

# Write CLAUDE.md

Cílem je CLAUDE.md, který modelu bez znalosti projektu řekne, **na čem se pracuje,
proč a kde si dohledá zbytek** — a nic víc. Závazným kontraktem je
`${CLAUDE_PLUGIN_ROOT}/skills/write-claude-md/claude-md-template.md`: nese kostru
souboru, výčet toho, co do něj nepatří, a kontrolní seznam. Při rozporu s tímto
postupem platí on.

Soubor se čte v každé session projektu, takže **každý zbytečný řádek se platí
pořád**. Rozsah proto není estetika, ale rozpočet: cíl ~80 řádků, strop 200.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

Zadání ber jako pokyn, co v souboru zdůraznit, ne jako kompletní brief. Prázdné
zadání je normální stav — obsah stejně vzniká z průzkumu a z kroku 3.

## Postup

### 1. Zjisti, kde soubor žije a čím projekt mluví

Nástrojem Glob najdi `CLAUDE.md` a `.claude/CLAUDE.md` v kořeni projektu. Obě
umístění se načítají a projekty používají obojí — **zapisuj tam, kde soubor už je**.
Založení druhého souboru vedle prvního vyrobí dva zdroje pravdy, které se rozejdou.
Neexistuje-li ani jeden, použij `CLAUDE.md` v kořeni.

**Existují-li oba**, přečti oba a v osnově navrhni, který zůstane a co se z druhého
přenáší. Zrušení toho druhého nech potvrdit uživatelem — načítají se obě umístění,
takže nechat jedno nedotčené znamená zeštíhlit polovinu a stav zhoršit; a sloučit
dva zdroje pravdy je rozhodnutí projektu, ne tvoje. **Odmítne-li uživatel sloučení**,
eskaluj podle kroku 6 — dvě umístění, která mají obě zůstat, potřebují rozdělenou
odpovědnost, a tu ti nikdo nezadal.

Existující soubor přečti **celý**. Je to vstup, ne odpad: obsahuje rozhodnutí,
která z kódu nevyčteš, i když je kolem nich navršený balast. Co je platné, přenes.

Urči jazyk, kterým se soubor napíše: podle existujícího CLAUDE.md, jinak podle
README a projektové dokumentace. Nedá-li se to poznat, piš česky. Identifikátory,
cesty a názvy sekcí struktury nech anglicky.

### 2. Zmapuj repo

Zajímá tě mapa, ne inventura:

- **Struktura** — Globem projdi kořen a první dvě úrovně. Hledej hranice, na kterých
  se láme odpovědnost (`srcs/backend` vs. `srcs/frontend`, `Packages` vs. `Assets`),
  ne všechny složky.
- **Tech stack** — z manifestů (`package.json`, `*.csproj`, `Cargo.toml`,
  `pyproject.toml`, `*.asmdef`, lock soubory). Verze si přečti, ale do souboru dávej
  jen ty, které mění způsob práce.
- **Dokumentace** — najdi `.docs/`, `docs/`, ADR, `CONTRIBUTING.md`, `README.md`.
  **Zaznamenej cesty a k čemu složka slouží; obsah nečti celý.** Cílem je vědět,
  na co odkázat, ne co opsat — a přečtená dokumentace svádí k tomu ji shrnout.

**Kód nečti.** Skill píše rozcestník; implementační detaily do něj nepatří a čtení
kódu tě k nim jen svede.

Na konci kroku si otevři
`${CLAUDE_PLUGIN_ROOT}/skills/write-claude-md/claude-md-template.md` — kostra v něm
určuje, na co se má krok 3 ptát, takže bez ní bys interview vedl z paměti. Vezmi si
z něj i výčet toho, co do souboru nepatří; potřebuješ ho v krocích 4 a 5.

### 3. Doptej se na záměr

Průzkum ti dá strukturu a stack. Nedá ti **proč** — záměr projektu, doménu, důvod
zvolené architektury. Právě tahle část je hlavní přínos souboru a jediná, kterou
nelze odvodit; když ji model odhaduje z kódu, vyrobí obecné fráze.

Zeptej se na to, co jsi v repu nenašel. Typicky:

- co se staví a pro koho, čím se to liší od zřejmého řešení;
- jaký princip drží projekt pohromadě (kdo je zdroj pravdy, co se kde nesmí dít);
- co je v projektu neintuitivní — místo, kde nový člověk nebo model sáhne vedle;
- jazyk kódu vs. jazyk komunikace, pokud to z repa neplyne.

**Na záměr a doménu se ptej otevřeně v konverzaci, ne přes AskUserQuestion.**
Ten nástroj nabízí předpřipravené možnosti, takže bys je musel vymyslet z kódu —
a uživatel odklikne tu nejbližší. Vznikne odpověď, kterou sis napsal sám, tedy
přesně ta obecná fráze, před kterou varuje odstavec výš. AskUserQuestion sáhni
tam, kde možnosti reálně existují: jazyk souboru, výběr mezi nalezenými
umístěními, které volitelné sekce zahrnout.

**Neptej se na to, co už víš z kroku 2.** Otázka na tech stack, který jsi právě
přečetl z manifestu, jen ubere uživateli trpělivost na otázky, které smysl mají.

### 4. Předlož osnovu

Sestav osnovu podle kostry v referenci otevřené na konci kroku 2.

Osnovu předlož podle Formátu výstupu a nech si ji odsouhlasit. Vynechané položky
vypiš **explicitně**: uživatel je jediný, kdo pozná, že jsi škrtl něco, na čem
projektu záleží, a v osnově to opraví jednou větou místo celého kola.

Bez schválení nezapisuj. U projektu s existujícím CLAUDE.md by šlo o přepsání
obsahu, který nikdo neobhájil.

### 5. Zapiš a ověř rozsah

Zapiš soubor na místo z kroku 1. Přepisuješ-li existující, použij Write —
zeštíhlení mění strukturu celého souboru a řetěz Editů z něj udělá slepenec.

Pak si hotový soubor přečti Readem: číslované řádky ti dají přesný rozsah. Nad 200
řádků **škrtej, neřeď** — hledej sekci, kterou lze nahradit odkazem do dokumentace,
a odstraň ji Editem; cílený škrt je jediné, na co se tu Edit používá. Rozsah snížený
obecnějšími formulacemi je horší výsledek než ten původní, protože ubyla informace,
ne text. Nedostaneš-li se pod strop, aniž bys o něco přišel, eskaluj podle kroku 6 —
zapsaný soubor nad 200 řádků není hotový výsledek.

Sloučil-li krok 1 dvě umístění, **druhý soubor smazat neumíš** — skill nemá nástroj,
který by to udělal. Požádej uživatele, ať ho odstraní sám, a uveď to v reportu jako
otevřený krok; dokud tam soubor je, načítá se a sloučení není hotové. Nepřepisuj ho
na prázdný ani na jednořádkový odkaz — načítal by se dál.

Projdi kontrolní seznam v referenci bod po bodu a nakonec vydej závěrečný report
podle Formátu výstupu.

### 6. Eskalace

Přeruš postup a obrať se na uživatele, když:

- na otázky z kroku 3 nedorazí odpověď — sekci „co se staví a proč" **nevymýšlej**,
  bez ní soubor ztrácí důvod existovat a zbyde z něj právě ta inventura, které se
  skill vyhýbá;
- projekt je natolik rozsáhlý, že se ani po škrtech nevejde do 200 řádků — pak je
  na řadě rozhodnutí, co odsunout do vlastní dokumentace, a to není tvoje volba;
- existující CLAUDE.md obsahuje pokyny, kterým nerozumíš natolik, abys posoudil,
  jestli jsou pořád platné — ocituj je a zeptej se.

Při eskalaci shrň, co už máš hotové, a polož konkrétní otázku.

## Formát výstupu

### Osnova ke schválení (krok 4)

```
CLAUDE.md pro [projekt] → [cesta k souboru] ([nový | přepis stávajícího, N řádků])
Jazyk: [jazyk] — [podle čeho určený]

**[Název sekce]** — [co v ní bude, jednou větou] (~[N] řádků)
**[Název sekce]** — [co v ní bude, jednou větou] (~[N] řádků)

Vynechávám: [položka — proč; položka — proč]
[U přepisu:] Ze stávajícího souboru přenáším: [co]. Vyhazuji: [co — proč].
[Existují-li obě umístění:] Zůstává: [cesta]. Ruší se: [cesta] — přenáším z něj
[co]; smazat ho budeš muset sám, skill to neumí.

Odhad rozsahu: ~[N] řádků.
```

### Závěrečný report

```
Zapsáno: [cesta] — [N] řádků (cíl ~80, strop 200)
Odkázaná dokumentace: [cesty, na které soubor odkazuje místo opisu]
[U přepisu:] Ubylo: [N] → [N] řádků.
[Po sloučení umístění:] Zbývá na tobě: smazat [cesta] — bez toho se načítá dál.
Ke zvážení: [co by si zasloužilo vlastní dokument, nebo „nic"]
```

## Zásady

- **Reference má přednost.** Když si kostra, výčet nepatřičného nebo kontrolní
  seznam odporují s tímto postupem, platí reference.
- **Odkazuj, neopisuj.** Existující dokumentace je aktuálnější než její shrnutí
  a odkaz na ni drží krok; opis se rozejde a začne lhát dřív, než si toho někdo
  všimne.
- **Rozsah se snižuje škrtáním.** Obecnější formulace zkrátí text a zároveň uberou
  informaci — to je čistá ztráta.
- **Existující soubor je vstup.** Nikdy ho nepřepisuj, aniž bys ho přečetl celý
  a vyjmenoval v osnově, co z něj mizí.
- **Review smyčku skill nemá.** Brzdou je schválená osnova a kontrolní seznam
  v kroku 5 — na rozdíl od `write-skill` tu nestojí subagent, takže osnovu
  neodbývej, je to jediné místo, kde se dá rozhodnutí zvrátit levně.
