---
name: write-agent
description: >-
  Vytvoří nového agenta v cílovém projektu nebo upraví existujícího — zjistí,
  jakým slovníkem projekt mluví o rolích, provede interview, navrhne konfiguraci
  podle matice model × effort × maxTurns, sepíše definici podle závazné šablony
  a nechá ji nezávisle zrevidovat subagentem s čistým kontextem. Kola oprav
  a review řídí autonomně; na uživatele se obrací jen při eskalaci.
when_to_use: >-
  Použij, když chce uživatel založit agenta nebo upravit existujícího —
  „vytvoř agenta", „přidej agenta na…", „potřebuju roli, která…", „uprav
  agenta" — i tehdy, když popisuje obor, který by měl někdo na projektu trvale
  vlastnit, aniž by slovo agent zmínil. Nepoužívej pro zakládání skillů, na to
  slouží write-skill; pro pravidla v `.claude/rules/` write-rule; pro projektové
  instrukce čtené v každé session write-claude-md; pro posouzení hotového agenta
  slouží review-agent; pro naplnění jeho paměti train-agent; ani pro běžné
  spuštění existujícího agenta.
argument-hint: "[role nebo téma agenta]"
model: opus
effort: high
# Zařazení dle matice: orchestrace workflow s autonomní smyčkou — matice na ni
# má řádek opus × xhigh. Snížení na high je odchylka o stupeň: nejtěžší část
# (review) je delegovaná na review-agent běžící na opus × xhigh, takže vlastní
# práce tohoto skillu je průzkum projektu, interview a text, ne hloubkové
# posuzování.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Agent
# Vynechaná zvažovaná pole: disable-model-invocation — skill je užitečný i když
# si ho model vyvolá sám z popisu oboru, který má někdo vlastnit; context/agent/
# background — interview vyžaduje uživatele v hlavním kontextu, fork nebo běh
# na pozadí by neměly komu klást otázky; paths — skill se spouští z konverzace
# o roli, ne prací nad konkrétními soubory; shell — postup je průzkum, psaní
# souborů a volání subagenta, ne spouštění příkazů; disallowed-tools —
# allowed-tools je uzavřený výčet, není co zakazovat navíc.
---

# Write Agent

Cílem je agent, který na cílovém projektu obstojí v ostrém provozu: nese roli,
kterou by tam skutečně někdo měl, běží na správném modelu a jeho definice dává
smysl i tomu, kdo nezná kontext jejího vzniku. Závazným kontraktem jsou tři
referenční soubory vedle tohoto — při rozporu s čímkoli, včetně tohoto skillu,
mají přednost ony.

Referenční soubory čti přes `${CLAUDE_PLUGIN_ROOT}`; plugin může běžet nad cizím
projektem, kde relativní cesta `skills/…` míří někam jinam.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Příprava

1. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-agent/agent-conventions.md` —
   pravidla, na která se budeš celou dobu odvolávat.
2. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-agent/agent-template.md` — kostru,
   do které budeš psát.
3. `agent-model-matrix.md` v téže složce otevři až ve chvíli, kdy budeš zařazovat
   roli; dřív ji nepotřebuješ.
4. **Jde-li o úpravu existujícího agenta, přečti ho celý ještě před interview** —
   včetně komentářů ve frontmatteru. Bez znalosti toho, co agent dnes vlastní
   a proč je nakonfigurovaný takhle, nejde poznat, co se změnou rozbije.
5. Urči, kam agent patří: nad cizím projektem do jeho `.claude/agents/<název>.md`,
   ve vývojovém repu pluginu do `agents/<název>.md`. Není-li to jednoznačné,
   zeptej se v interview — na volbě visí ukotvení cest v kroku 3 a špatná větev
   znamená agenta s nefunkčními odkazy. Konvence i šablona platí pro obě umístění
   stejně; liší se jen ukotvení cest a to, že se agentovi uvnitř pluginu
   `permissionMode`, `mcpServers` ani `hooks` neuplatní.
6. **Zjisti, jakým slovníkem projekt mluví o rolích.** Projdi `README.md`,
   `CONTRIBUTING.md`, `CODEOWNERS`, dokumentaci, ADR a názvy štítků nebo týmů,
   na které v repozitáři narazíš. Název agenta má odpovídat roli, která by na
   projektu reálně existovala — a to nejde vymyslet od stolu.
7. Projdi existující agenty — jak ty v `.claude/agents/` cílového projektu, tak ty,
   které dodává plugin; v katalogu se potkají, takže kolidovat můžou obojí. Stačí
   `description` z jejich frontmatterů. Nový agent nesmí triggeringem kolidovat
   se sousedy; hranici je potřeba vytyčit negativním vymezením **na obou
   stranách**, takže pokud úprava souseda k zadání patří, udělej ji zároveň —
   a v kroku 5 ji pošli do review spolu s novým agentem.
8. Projdi i dostupné skilly. Postup, který už jako skill existuje, bude agent
   volat, ne opisovat — a najdeš-li skill, který pokrývá celé zadání, je to
   signál, že agent vůbec nemá vzniknout (viz Zásady).

### 2. Interview

Piš jen to, co víš od uživatele. Nejdřív vytěž konverzaci, pak se doptej po
kolech — nástrojem AskUserQuestion a s konkrétními možnostmi tam, kde dávají
smysl. Zjisti:

- **Mandát** — jaký obor má agent vlastnit, za co nese odpovědnost a čí slovo
  platí, když se rozejde s někým jiným.
- **Úsudek, nebo postup** — co má agent dělat v situacích, které nikdo předem
  nesepsal. Nedokáže-li uživatel takovou situaci pojmenovat, patří práce
  do skillu, ne do agenta.
- **Triggering** — kdy se má delegovat a kdy naopak ne. `description` nese
  obojí ve třech dílech; negativní vymezení vůči sousedům je povinná část.
- **Vstupní kontrakt** — co agent dostane v promptu a co udělá, když to nedostane.
- **Nástroje a hranice** — co role skutečně potřebuje a co naopak zásadně dělat
  nemá. Práva musí sedět na mandát: agent, který má delegovat, nesmí mít `Write`.
- **Frekvence spouštění** — poběží jednou za sprint, po každé změně, nebo
  automaticky? Do zařazení vstupuje stejně jako náročnost.
- **Paměť a znalost projektu** — má se role učit vzorce projektu napříč sezeními?
  Zjisti zároveň, které dokumenty nebo poznatky bude role potřebovat znát. **Do definice
  je nepiš** — patří do paměti a naplní je `train-agent`; ty si je jen poznamenej
  a vypiš je v závěrečném reportu jako navazující krok.
- **Název** — navrhni ho ze slovníku rolí zjištěného v kroku 1 a nech si ho
  potvrdit.
- **Zařazení do matice** — navrhni model × effort × maxTurns i s odůvodněním
  a nech si je potvrdit.

**U úpravy existujícího agenta interview zúž** na to, co se mění. Nepřejmenovávej
agenta, který jméno má, a neptej se znovu na rozhodnutí, která už nesou komentáře
ve frontmatteru — jen ověř, jestli změna některé z nich neruší.

Interview končí, až umíš vyplnit všechna povinná pole frontmatteru a rozhodnout
o každém zvažovaném poli. Než začneš psát, shrň uživateli, co agent bude vlastnit
a jak bude nakonfigurovaný, a nech si shrnutí potvrdit — oprava návrhu stojí
jednu větu, oprava hotového agenta celé kolo.

**Nemáš-li uživatele, agenta nepiš.** Agent napsaný z domněnek drží roli, kterou
na projektu nikdo nemá, a deleguje se na něj náhodně. Selže-li volání
AskUserQuestion nebo odpověď nedorazí, shrň, na co potřebuješ odpovědět,
a skonči — nezakládej soubory.

### 3. Sepsání

**Nového agenta** napiš tak, že okopíruješ kostru z `agent-template.md` a vyplníš
ji. Šablona je kostra k vyplnění, ne text k opsání: placeholdery nahraď, závorky
i značky `(volitelné)` odstraň, nepoužité volitelné sekce smaž celé.

**Úpravu existujícího agenta** veď ze stávajícího souboru — měň jen to, co se
mění. Šablona ti tu slouží jako kontrola struktury, ne jako předloha k přepsání.

Ve frontmatteru:

- povinná pětice `name`, `description` (trojdílně: co vlastní, kdy zavolat,
  kdy ne), `model`, `effort`, `tools` — u `model: haiku` se `effort` naopak
  vynechává;
- komentář se zařazením do matice, včetně frekvence spouštění a odůvodnění
  odchylky;
- komentář vypisující každé vynechané netriviální zvažované pole i s důvodem.
  Bez něj review nerozliší uvážené vynechání od opomenutí.

V těle **založ personu ve druhé osobě a zbytek piš rozkazovacím způsobem**.
U instrukcí, které nejsou samozřejmé, vysvětli proč. Hranice zapiš tak, aby
u každé bylo i to, co agent udělá místo zakázané akce — **nikde nesmí stát,
že se má agent zeptat nebo počkat na schválení**, protože agent nemá koho:
takový pokyn skončí předstíraným souhlasem, nebo zaseknutím. Kostru reportu
okopíruj z kapitoly „Report“ v konvenci beze změny a přizpůsob jen volnou část.

**Na dokumenty cílového projektu ani na rules se agent neodkazuje.** Do těla nepiš
cesty k ADR, specifikacím a souborům v `docs/` — dokumenty se přejmenovávají a ruší,
kdežto definice zůstává a agent pak čte neplatnou cestu. Trvalá znalost role patří
do její paměti, kterou plní `train-agent`; v těle stačí pojmenovat druh znalosti
a odkud ji bere. `.claude/rules/` v agentovi nezmiňuj vůbec — rules se do kontextu
načítají samy, takže odkaz na ně načte totéž podruhé a rozbije se při přejmenování.
Podrobně to řeší kapitola „Na co se agent neodkazuje“ v konvencích.

Odkazy, které v agentovi zůstanou — na doprovodné soubory a skilly — ukotvi
**podle cílového umístění z kroku 1**. Agent v `.claude/agents/` cílového
projektu není součástí pluginu, takže se mu
`${CLAUDE_PLUGIN_ROOT}` nerozvine — cesty v něm veď od kořene projektu
a skilly pluginu volej jmenovitě i s namespacem (`sagittaras:<skill>`).
Agent uvnitř pluginu naopak `${CLAUDE_PLUGIN_ROOT}` použít může.

### 4. Vlastní kontrola

Projdi hotového agenta proti kontrolnímu seznamu v závěru `agent-conventions.md`,
bod po bodu. Zvlášť ověř, že:

- v souboru nezůstal žádný placeholder ani značka `(volitelné)`;
- `description` má všechny tři díly a vymezení sedí i z druhé strany;
- `tools` neobsahuje nic nad rámec mandátu a všechny názvy nástrojů existují —
  neexistující položka agenta vůbec nespustí;
- kostra reportu je úplná, včetně sekce „Čeho jsem se nedotkl“;
- v těle nezůstal odkaz na dokument cílového projektu ani zmínka o `.claude/rules/` —
  co z definice takhle vypadlo, patří do reportu jako práce pro `train-agent`.

Reviewer bude kontrolovat proti témuž seznamu — co si opravíš tady, nemusíš
řešit v dalším kole.

### 5. Nezávislé review

1. Nástrojem Agent spusť subagenta **synchronně** (`run_in_background: false`) —
   bez verdiktu nemáš jak pokračovat. Typ agenta a model vezmi z frontmatteru
   `review-agent` a předej je parametry nástroje: jako subagent si je sám
   neuplatní, takže co nepředáš, se nepoužije. Zadání sestav podle šablony
   ve Formátu výstupu.

   **Effort parametrem předat nejde** — nástroj Agent ho nemá, takže ho napiš
   do zadání jako pokyn. Je to slabší záruka než parametr, ale bez něj poběží
   reviewer s effortem tvojí session, který bývá nižší než ten, na kterém má
   poslední brána pracovat.

   **Do zadání dosaď rozvinutou absolutní cestu ke kořeni pluginu**, nikde
   nenech proměnnou. Reviewer čte soubory jako subagent a nemá jak si ji
   dopočítat; bez cesty si neotevře ani vlastní postup, ani konvence —
   a z kola vypadne celá kontrola konformity, aniž by to bylo poznat.

   Subagent startuje s čistým kontextem — právě proto je jeho pohled nezávislý,
   a právě proto si historii kol nepamatuje. Co mu nepředáš, pro něj neexistuje.

2. **Vráceno k dopracování** → zapracuj všechny blokující nálezy, doporučení
   uvážlivě zvaž. Pak spusť další kolo s **novým** subagentem; tomu vypotřebovanému
   nedávej opravu k posouzení, ztratil by odstup.

3. **Schváleno** → agent je hotový. Reportuj uživateli podle šablony ve Formátu
   výstupu.

Nálezy neodmítej mlčky. Reviewer nezná interview, takže může napadnout něco,
co uživatel vědomě chtěl — takový nález patří do reportu, ne do koše.

### 6. Eskalace

Přeruš smyčku a obrať se na uživatele, když:

- nález zpochybňuje mandát nebo podobu role, kterou uživatel v interview
  výslovně potvrdil — záměr vlastní uživatel, ne ty ani reviewer;
- stejný blokující nález přetrvává i po tvém pokusu o opravu (dvě kola);
- proběhla tři kola bez schválení;
- narazíš na technickou chybu, kterou opakování nevyřeší.

Při eskalaci shrň stav smyčky, ocituj sporný nález a polož konkrétní otázku.
Mlhavá eskalace uživatele jen zdrží.

## Formát výstupu

### Umístění souboru

```
<kořen cílového projektu>/.claude/agents/<název-role>.md    ← nad cizím projektem
<kořen pluginu>/agents/<název-role>.md                      ← ve vývojovém repu pluginu
```

Jeden soubor = jeden agent, bez podsložek. Název souboru se musí shodovat
s hodnotou `name` ve frontmatteru.

### Zadání pro reviewera

Reviewer ho parsuje a nekompletní zadání označí za nález, kterým kolo skončí —
proto ho posílej v této struktuře:

```
Přečti si soubor `<kořen pluginu>/skills/review-agent/SKILL.md`
a proveď přesně jeho postup. Pracuj s effortem <hodnota z frontmatteru
review-agent>.

Zadání pro tvůj běh:
- Kořen pluginu: <absolutní cesta, rozvinutá — ne proměnná>
- Repozitář: <absolutní cesta k repozitáři, do kterého agent míří>
- Posuzovaní agenti: <cesta k novému agentovi; cesty ke všem upraveným sousedům>
- Číslo kola: <N>
- Nevyřešené nálezy z minulého kola: <žádné, jde o první kolo | seznam nálezů
  i s tím, jak jsi je řešil>

Vrať verdikt přesně ve struktuře, kterou review-agent předepisuje v sekci
„Formát výstupu".
```

### Závěrečný report uživateli

```
Agent: <název> (<cesta>)
Mandát: <jednou větou, co role vlastní>
Konfigurace: <model> × <effort> × <maxTurns> — <důvod zařazení včetně frekvence>
Paměť: <hodnota memory: — u nového agenta „zatím prázdná, naplní se skillem
  train-agent", u upraveného „tímto během se neměnila" nebo „doplněna/změněna
  tímto během z <původní> na <nová>" | vynechána>
K naučení přes train-agent: <dokumenty a poznatky z interview, které do definice
  nepatří a mají jít do paměti — konkrétními cestami, ať se dají skillu předat
  | žádné>
Vynechaná zvažovaná pole: <výčet>
Kol review: <N>
Odmítnuté nálezy: <nález → důvod odmítnutí, nebo „žádné">
```

## Zásady

- Referenční soubory mají přednost před tímto skillem. Když si odporují, platí
  konvence, matice a šablona, ne tento postup.
- **Když z interview vyjde, že práce nevyžaduje úsudek, agenta nepiš** a navrhni
  místo něj skill. Agent tam, kde stačil postup, stojí kontext, běh i údržbu
  navíc — a je to nejčastější chyba, které se tenhle skill má vyhnout.
- Jeden běh = jeden **nově vznikající** agent; úprava vymezení u sousedů do téhož
  běhu patří. Potřebuje-li uživatel víc rolí, spusť skill víckrát — každá role
  si zaslouží vlastní interview.
- Interview a eskalace jsou jediné fáze, které vyžadují uživatele — bez interview
  agent nevzniká. Mezi nimi běží smyčka psaní a review autonomně; nepřerušuj ji
  kvůli průběžnému hlášení.
- Review si neděláš sám. Vlastní kontrola v kroku 4 ho nenahrazuje: autor nevidí,
  co do agenta podvědomě doplnil z hlavy.
- Do review jde **všechno, čeho ses dotkl** — nový agent i upravení sousedé,
  a úprava existujícího agenta jde stejným postupem jako vznik nového. Změna,
  která projde mimo bránu, mění triggering bez kontroly; drobnost není výmluva.
