---
name: write-skill
description: >-
  Vytvoří nový skill v pluginu nebo upraví existující — provede interview,
  navrhne název a konfiguraci frontmatteru podle matice model × effort,
  sepíše SKILL.md podle závazné šablony a nechá výsledek nezávisle zrevidovat
  subagentem s čistým kontextem. Kola oprav a review řídí autonomně;
  na uživatele se obrací jen při eskalaci.
when_to_use: >-
  Použij, když chce uživatel založit nový skill nebo upravit existující —
  „vytvoř skill", „přidej skill na…", „napiš mi skill", „uprav frontmatter
  skillu" — ale i tehdy, když popisuje opakovaný postup, který by stálo za to
  zachytit jako skill, aniž by slovo skill zmínil. Nepoužívej pro zakládání
  agentů, na to slouží write-agent; pro pravidla v `.claude/rules/` write-rule;
  pro CLAUDE.md cílového projektu write-claude-md; ani pro commandy, ty mají
  vlastní pravidla; pro samotné posouzení
  hotového skillu slouží review-skill; ani pro běžné použití existujícího skillu.
argument-hint: "[název nebo téma skillu]"
model: opus
effort: high
# Zařazení dle matice: orchestrace workflow s autonomní smyčkou — matice na ni
# má řádek opus × xhigh. Snížení na high je odchylka o stupeň: nejtěžší část
# (review) je delegovaná na review-skill běžící na opus × xhigh, takže vlastní
# práce tohoto skillu je návrh, interview a text, ne hloubkové posuzování.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Agent
# Vynechaná zvažovaná pole: disable-model-invocation — skill je užitečný
# i když si ho model vyvolá sám z popisu opakovaného postupu; context/agent/
# background — interview vyžaduje uživatele v hlavním kontextu, fork nebo
# běh na pozadí by neměly komu klást otázky; paths — skill se spouští
# z konverzace nad tématem, ne prací nad konkrétními soubory; shell — postup
# je psaní souborů a volání subagenta, ne spouštění příkazů;
# disallowed-tools — allowed-tools je uzavřený výčet, není co zakazovat navíc.
---

# Write Skill

Cílem je skill, který obstojí v automatickém provozu: spouští se ve správných
situacích, běží na správném modelu a jeho instrukce dávají smysl i tomu, kdo
nezná kontext jeho vzniku. Závazným kontraktem jsou tři referenční soubory
vedle tohoto — při rozporu s čímkoli, včetně tohoto skillu, mají přednost ony.

Referenční soubory čti přes `${CLAUDE_PLUGIN_ROOT}`; plugin může běžet nad cizím
projektem, kde relativní cesta `skills/…` míří někam jinam.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Příprava

1. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-skill/skill-conventions.md` —
   pravidla pojmenování a frontmatteru, na která se budeš celou dobu odvolávat.
2. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-skill/skill-template.md` — kostru,
   do které budeš psát.
3. `model-effort-matrix.md` v téže složce otevři až ve chvíli, kdy budeš
   zařazovat úlohu; dřív ji nepotřebuješ.
4. **Jde-li o úpravu existujícího skillu, přečti ho celý ještě před interview** —
   včetně komentářů ve frontmatteru. Bez znalosti toho, co skill dnes dělá a proč
   je nakonfigurovaný takhle, nejde poznat, co se změnou rozbije.
5. Urči, kam skill patří: ve vývojovém repu pluginu do `skills/<název>/`,
   nad cizím projektem do jeho `.claude/skills/<název>/`. Není-li to jednoznačné,
   zeptej se v interview.
6. Projdi existující skilly — jak ty v `.claude/skills/` cílového projektu, tak ty,
   které dodává plugin; v katalogu se potkají, takže kolidovat můžou obojí. Stačí
   `description` a `when_to_use` z jejich frontmatterů. Ověř zároveň, že název
   nekoliduje s žádným agentem — skilly a agenti sdílejí jmenný prostor v hlavě
   toho, kdo je volá. Nový skill nesmí triggeringem kolidovat se sousedy; hranici je
   potřeba vytyčit negativním vymezením **na obou stranách**, takže pokud úprava
   souseda k zadání patří, udělej ji zároveň — a v kroku 5 ji pošli do review
   spolu s novým skillem.

### 2. Interview

Piš jen to, co víš od uživatele. Nejdřív vytěž konverzaci, pak se doptej po
kolech — nástrojem AskUserQuestion a s konkrétními možnostmi tam, kde dávají
smysl. Zjisti:

- **Účel** — jaký opakovaný problém skill řeší a jak často poběží.
- **Triggering** — kdy se má spouštět (situace i fráze, které uživatel reálně
  řekne) a kdy naopak ne. Negativní vymezení vůči sousedním skillům je povinná
  část `when_to_use`, ne ozdoba.
- **Vstupy a výstup** — jestli přijímá argumenty, co je výsledkem a kam se ukládá.
- **Nástroje** — co postup skutečně potřebuje. Užší `allowed-tools` je lepší
  než široký, ale skill, kterému chybí nástroj, se zasekne uprostřed práce.
- **Název** — navrhni `<činnost>-<předmět>` a nech si ho potvrdit.
- **Zařazení do matice** — navrhni dvojici model × effort i s odůvodněním
  a nech si ji potvrdit.

**U úpravy existujícího skillu interview zúž** na to, co se mění. Nepřejmenovávej
skill, který jméno má, a neptej se znovu na rozhodnutí, která už nesou komentáře
ve frontmatteru — jen ověř, jestli změna některé z nich neruší.

Interview končí, až umíš vyplnit všechna povinná pole frontmatteru a rozhodnout
o každém zvažovaném poli. Než začneš psát, shrň uživateli, co skill bude dělat
a jak bude nakonfigurovaný, a nech si shrnutí potvrdit — oprava návrhu stojí
jednu větu, oprava hotového skillu celé kolo.

**Nemáš-li uživatele, skill nepiš.** Skill napsaný z domněnek se spouští ve
špatných situacích a na špatném modelu, což je horší než žádný skill. Selže-li
volání AskUserQuestion nebo odpověď nedorazí, shrň, na co potřebuješ odpovědět,
a skonči — nezakládej soubory.

### 3. Sepsání

**Nový skill** napiš tak, že okopíruješ kostru ze `skill-template.md` a vyplníš
ji. Šablona je kostra k vyplnění, ne text k opsání: placeholdery nahraď, závorky
i značky `(volitelné)` odstraň, nepoužité volitelné sekce smaž celé.

**Úpravu existujícího skillu** veď ze stávajícího souboru — měň jen to, co se
mění. Šablona ti tu slouží jako kontrola struktury, ne jako předloha k přepsání;
přepsat fungující skill ze šablony znamená zahodit rozhodnutí, která v něm někdo
udělal a zdůvodnil.

Ve frontmatteru:

- povinná pětice `name`, `description` (co), `when_to_use` (kdy + negativní
  vymezení), `model`, `effort` — a součet `description` + `when_to_use`
  do 1 536 znaků;
- komentář se zařazením do matice a s odůvodněním, pokud ses odchýlil;
- komentář vypisující každé vynechané netriviální zvažované pole i s důvodem.
  Bez něj review nerozliší uvážené vynechání od opomenutí.

V těle piš rozkazovacím způsobem a u instrukcí, které nejsou samozřejmé,
**vysvětli proč** — instrukci s důvodem model dodrží spolehlivěji než holý
příkaz. Nepopisuj, co model umí sám od sebe. Objemný materiál (referenční
tabulky, šablony, skripty) odsuň do vedlejších souborů a u každého odkazu řekni,
**kdy** se má otevřít.

Cesty k vlastním skriptům a doprovodným souborům ukotvi **podle cílového
umístění z kroku 1**: skill uvnitř pluginu k `${CLAUDE_PLUGIN_ROOT}`, skill
v `.claude/skills/` projektu k jeho kořeni (`.claude/skills/<název>/…`). Mimo
plugin se `${CLAUDE_PLUGIN_ROOT}` nenastaví a skill by spadl na prvním volání.
Tvar volání srovnej se zúžením v `allowed-tools`.

**Výjimka: skill, který se spouští tím, že si ho subagent přečte jako soubor**
(tak běží reviewery v této smyčce), bere kořen pluginu ze zadání a proměnnou
nepoužívá vůbec — subagentovi se nerozvine a zůstane literálem. Píšeš-li takový
skill, řekni mu ve Vstupním kontextu, odkud si kořen vzít a co dělat, když chybí.

### 4. Vlastní kontrola

Projdi hotový skill proti kontrolnímu seznamu v závěru `skill-conventions.md`,
bod po bodu. Zvlášť ověř, že:

- v souboru nezůstal žádný placeholder ani značka `(volitelné)`;
- `when_to_use` obsahuje negativní vymezení a sedí i z druhé strany — u souseda,
  vůči kterému se vymezuješ;
- `model` a `effort` odpovídají zařazení, které uživatel potvrdil.

Reviewer bude kontrolovat proti témuž seznamu — co si opravíš tady, nemusíš
řešit v dalším kole.

### 5. Nezávislé review

1. Nástrojem Agent spusť subagenta **synchronně** (`run_in_background: false`) —
   bez verdiktu nemáš jak pokračovat. Typ agenta a model vezmi z frontmatteru
   `review-skill` a předej je parametry nástroje: jako subagent si je sám
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

3. **Schváleno** → skill je hotový. Reportuj uživateli podle šablony ve Formátu
   výstupu.

Nálezy neodmítej mlčky. Reviewer nezná interview, takže může napadnout něco,
co uživatel vědomě chtěl — takový nález patří do reportu, ne do koše.

### 6. Eskalace

Přeruš smyčku a obrať se na uživatele, když:

- nález zpochybňuje účel nebo podobu skillu, kterou uživatel v interview
  výslovně potvrdil — záměr vlastní uživatel, ne ty ani reviewer;
- stejný blokující nález přetrvává i po tvém pokusu o opravu (dvě kola);
- proběhla tři kola bez schválení;
- narazíš na technickou chybu, kterou opakování nevyřeší.

Při eskalaci shrň stav smyčky, ocituj sporný nález a polož konkrétní otázku.
Mlhavá eskalace uživatele jen zdrží.

## Formát výstupu

### Struktura složky

```
<cílová složka skillů>/<název-skillu>/
  SKILL.md              ← postup a rozhodování
  <reference>.md        ← volitelně: objemný materiál odsunutý z těla
  scripts/              ← volitelně: skripty, na které skill spoléhá
```

Název složky se musí shodovat s hodnotou `name` ve frontmatteru.

### Zadání pro reviewera

Reviewer ho parsuje a nekompletní zadání označí za nález, kterým kolo skončí —
proto ho posílej v této struktuře:

```
Přečti si soubor `<kořen pluginu>/skills/review-skill/SKILL.md`
a proveď přesně jeho postup. Pracuj s effortem <hodnota z frontmatteru
review-skill>.

Zadání pro tvůj běh:
- Kořen pluginu: <absolutní cesta, rozvinutá — ne proměnná>
- Repozitář: <absolutní cesta k repozitáři cílového projektu, do kterého skill míří>
- Posuzované skilly: <cesta k novému skillu; cesty ke všem upraveným sousedům>
- Číslo kola: <N>
- Nevyřešené nálezy z minulého kola: <žádné, jde o první kolo | seznam nálezů
  i s tím, jak jsi je řešil>

Vrať verdikt přesně ve struktuře, kterou review-skill předepisuje v sekci
„Formát výstupu".
```

### Závěrečný report uživateli

```
Skill: <název> (<cesta>)
Konfigurace: <model> × <effort> — <důvod zařazení>
Vynechaná zvažovaná pole: <výčet>
Kol review: <N>
Odmítnuté nálezy: <nález → důvod odmítnutí, nebo „žádné">
```

## Zásady

- Referenční soubory mají přednost před tímto skillem. Když si odporují,
  platí konvence a šablona, ne tento postup.
- Interview a eskalace jsou jediné fáze, které vyžadují uživatele — bez interview
  skill nevzniká. Mezi nimi běží smyčka psaní a review autonomně; nepřerušuj ji
  kvůli průběžnému hlášení.
- Review si neděláš sám. Vlastní kontrola v kroku 4 ho nenahrazuje: autor
  nevidí, co do skillu podvědomě doplnil z hlavy.
- Do review jde **všechno, čeho ses dotkl** — nový skill i upravení sousedé.
  Úprava, která projde mimo bránu, mění triggering cizího skillu bez kontroly.
- Úprava existujícího skillu jde stejným postupem jako vznik nového, včetně
  review — drobnost není výmluva.
