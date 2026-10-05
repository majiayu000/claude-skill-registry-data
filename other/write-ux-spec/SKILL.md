---
name: write-ux-spec
description: >-
  Sepíše UX spec jedné obrazovky nebo flow v cílovém projektu, nebo aktualizuje
  existující — vytěží standardy z art bible, ADR a sousedních speců, doptá se
  na kompozici obrazovky a na rozsah dokumentu, podle povahy obrazovky
  vybere moduly šablony, hotový dokument předloží ke schválení a nechá ho
  nezávisle zrevidovat subagentem s čistým kontextem. Kola oprav a review řídí
  autonomně.
when_to_use: >-
  Použij, když má vzniknout nebo se změnit závazný popis jedné obrazovky nebo
  flow — „napiš UX spec pro…", „zdokumentuj obrazovku X", „pojďme rozepsat to
  flow", „doplň otevřené otázky ve specu N" — i tehdy, když uživatel popisuje
  rozvržení obrazovky, kterou má někdo postavit. Nepoužívej pro popis vzhledu
  projektu jako celku (paleta, typografie, katalog prvků), na to slouží
  write-art-bible; pro pravidlo v `.claude/rules/` write-rule; pro záznam
  architektonického rozhodnutí i s alternativami a důsledky write-adr;
  pro posouzení hotového specu review-ux-spec; pro implementaci obrazovky
  implement-issue;
  ani pro neformální rozmýšlení návrhu, které sepsání dokumentu předchází.
argument-hint: "[obrazovka nebo flow, případně číslo existujícího specu]"
# Odchylka od konvence pojmenování: název má tři slova. `ux-spec` je ale jeden
# název artefaktu, ne dva předměty — skill dělá jednu věc. Zkrácení na
# `write-screen` nebo `write-ui` by triggering zhoršilo, protože uživatel řekne
# přesně „UX spec".
model: opus
effort: high
# Zařazení dle matice: orchestrace workflow s autonomní smyčkou — matice na ni
# má řádek opus × xhigh. Snížení na high je odchylka o stupeň, shodně s
# write-rule a write-agent: nejtěžší část (review) je delegovaná na
# review-ux-spec běžící na opus × xhigh, takže vlastní práce tohoto skillu je
# vytěžení dokumentace, interview a text. Nikoli sonnet: skill rozhoduje, co je
# převzatý invariant a co původní návrh, a spletení obou směrů je hlavní způsob,
# jak vznikne spec, který tiše přerozhodne projektový standard.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Agent
# Vynechaná zvažovaná pole: Bash — postup je čtení dokumentace, psaní souboru
# a volání subagenta, ne spouštění příkazů; Skill — navazující kroky (make-commit,
# open-pr, train-agent) spouští uživatel, viz krok 10;
# disable-model-invocation — skill je užitečný i když si ho model vyvolá sám
# z popisu obrazovky, kterou má někdo postavit; context/agent/background —
# interview a schválení vyžadují uživatele v hlavním kontextu, fork ani běh na
# pozadí nemají komu klást otázky; paths — skill se spouští z konverzace
# o obrazovce, ne prací nad konkrétními soubory; shell — viz Bash;
# disallowed-tools — allowed-tools je uzavřený výčet a skill se nespouští
# načtením souboru, není co zakazovat navíc; version/license — verzuje se celý
# plugin, ne jednotlivý skill.
---

# Write UX Spec

Cílem je dokument, podle kterého jde obrazovku postavit bez doptávání — a který
nikde tiše nepřerozhodne to, co už projekt rozhodl jinde. Závazným kontraktem je
šablona vedle tohoto souboru; při rozporu s čímkoli, včetně tohoto skillu, má
přednost ona.

Referenční soubory čti přes `${CLAUDE_PLUGIN_ROOT}`; plugin běží nad cizím
projektem, kde relativní cesta `skills/…` míří někam jinam.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Příprava

1. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-ux-spec/ux-spec-template.md` — kostru,
   výběr modulů a kontrolní seznam, na které se budeš celou dobu odvolávat.
2. Najdi, kde v projektu UX specy leží, a jak se pojmenovávají. Hledej dokumentační
   složku (`.docs/`, `docs/`) a v ní podsložku pro rozhraní; všimni si, jestli
   projekt dokumenty čísluje (`NNNN-kebab-case.md`) a jestli má nečíslované kořenové
   dokumenty, které do číslování nepatří — art bible je typicky jeden z nich.
   Umístění a číslo nového dokumentu si nech potvrdit v kroku 4.
3. Podle nálezu urči **režim**:
   - **Nový spec** — obrazovka zatím dokument nemá; dostane další volné číslo.
   - **Úprava** — existující spec se rozšiřuje nebo se v něm řeší otevřená otázka.
     Nikdy nezakládej druhý dokument o téže obrazovce.
4. **U úpravy přečti celý existující spec dřív, než začneš interview.** Bez znalosti
   toho, co dnes tvrdí a na co se odkazují sousedé, nejde poznat, co se změnou rozbije.

### 2. Vytěžení standardů

Než se začneš ptát, zjisti, co už je rozhodnuté. Cílem kroku je **seznam invariantů**,
které do specu půjdou jako citace a o kterých se v interview nediskutuje.

| Co hledat | Kde |
| --- | --- |
| Barvy, typografie, styl komponent, tempo přechodů, prahy přístupnosti | Art bible projektu |
| Architektonické invarianty — kdo je zdroj pravdy, co se kde nesmí počítat | ADR, `CLAUDE.md`, rules v `.claude/rules/` |
| Data, akce, stavy a fail stavy, které obrazovka obsluhuje | Produktová nebo herní dokumentace |
| Znovupoužitelné komponenty a vztahy rodič–sourozenec | Sousední UX specy |
| Kam se hotový dokument registruje jako zdroj pravdy | `CONTRIBUTING.md`, podsekce Zdroje pravdy sekce „Workflow (sagittaras)" |

**Art bible přečti celou**, ne jen prohledej — je to hlavní zdroj všeho, co spec nesmí
přerozhodovat, a část invariantů z ní plyne nepřímo (vyhrazený vzor, zakázaná kombinace).
Nemá-li projekt art bible, ohlas to a nech uživatele rozhodnout, jestli pokračovat
s vizuálními standardy vytěženými z kódu, nebo nejdřív spustit `write-art-bible`.
Bez ní vzniká spec, který si vizuální rozhodnutí vymyslí per obrazovku — a to je přesně
to selhání, kterému má tenhle postup bránit.

**Sousední specy prohlédni kvůli komponentám.** Prohlásit za novou komponentu něco,
co už jiný spec definoval, znamená postavit ji podruhé a rozejít se s ní ve tvaru.

### 3. Výběr modulů

Z povahy obrazovky urči, které moduly šablony (§ 1.1) přibrat. Modul, pro který
obrazovka nemá obsah, nezakládej — prázdná kapitola vyplněná obecnými větami vypadá
jako rozhodnutí, kterým není. Výběr si nech potvrdit spolu se zbytkem v interview.

### 4. Interview

V obsahových dávkách se ptej **jen na původní návrh téhle obrazovky** — co na ní je, co
je vidět první, jak je rozvržená, jaké má stavy nad rámec obecné trojice. Invariant
z kroku 2 nikdy nedomlouvej; předlož ho jako fakt, ze kterého se vychází.

Veď interview **po dávkách**, ne sekci po sekci:

0. **Rozsah a umístění** — cesta a číslo souboru navržené v kroku 1, vybrané moduly
   z kroku 3, vlastník dokumentu a jeho cílový stav. Tahle dávka není o návrhu obrazovky,
   ale bez ní bys zapisoval na neodsouhlasenou cestu a nechal hlavičku prázdnou.
1. **Účel a kontext** — jakou potřebu obrazovka řeší, odkud na ni uživatel přichází.
   Stačí dvě věty; text sekce z nich napiš sám, to není další otázka.
2. **Navigace a dosažitelnost** — kde obrazovka sedí, jak se otevírá a zavírá, odkud
   všude se na ni dá dostat.
3. **Layout a komponenty** — co je vidět při otevření, jaké zóny a panely, co je nová
   komponenta a co se použije hotové.
4. **Stavy a interakce** — co se stane při prázdných datech a při chybě, co dělá
   klávesnice, co je kdy nedostupné.
5. **Přístupnost specifická pro obrazovku** — pořadí fokusu, co má oznámit čtečka.
   Prahy a obecná pravidla ber z art bible, ty se neřeší znovu.

U skutečného rozcestí s reálným dopadem použij AskUserQuestion, dej **doporučenou
variantu jako první** a u každé možnosti vypiš, co se tím získá a ztratí. Na drobnost
s očividným a vratným výchozím řešením se neptej — rozhodni ji a v dokumentu uveď proč.
Otázka na každý detail vyčerpá uživatele dřív, než dojdete k tomu, na čem záleží.

**Zdá-li se, že obrazovka potřebuje výjimku z invariantu**, není to varianta k zapsání.
Je to buď nedorozumění, nebo skutečná otázka — v obou případech ji pojmenuj a nech
rozhodnout uživatele.

**Nemáš-li uživatele, spec nepiš.** Kompozice obrazovky existuje jen v jeho hlavě;
vymyšlená se pozná až v implementaci, kdy už podle ní někdo staví. Selže-li volání
AskUserQuestion nebo odpověď nedorazí, shrň, na co potřebuješ odpovědět, a skonči.

### 5. Zápis

Piš podle šablony; sekce po výběru modulů očísluj a čísla drž, protože se na ně odkazuje
v review i v issues.

- Nový spec zapiš Writem na potvrzené místo a s dalším volným číslem.
- **Úpravu veď cílenými Edity**, ne plným přepisem — v existujícím dokumentu jsou
  rozhodnutí a odkazy sousedů, které přepis zahodí, aniž by to v diffu vypadalo jako ztráta.
- Hodnotu převzatou z art bible nebo ADR **cituj i s místem**, neopisuj vlastními slovy.
  Opis se s originálem rozejde a nikdo si toho nevšimne.
- Co zůstalo nerozhodnuté, patří do Otevřených otázek s vlastníkem — ne do textu jako
  by to platilo. Vágní věta v layoutu nebo ve stavech je díra, kterou implementace
  vyplní odhadem.
- Do dokumentu nepřenášej vysvětlivky ani příklady ze šablony.
- **Hlavičku vyplň celou** z odpovědí nulté dávky a z vytěžených dokumentů. Cílový stav
  z interview platí jen při nule otevřených otázek: zbývá-li jediná nevyřešená, dokument
  je Draft, i když ho uživatel odsouhlasil. *Poslední ověření* u nového dokumentu je
  datum zápisu.
- **U úpravy posuň *Poslední úprava* na datum zásahu.** *Poslední ověření* nech být,
  pokud někdo výslovně nepotvrdil shodu se skutečným UI — jeho smysl je stáří ověření,
  ne stáří textu, a posunout ho mimochodem znamená tvrdit něco, co nikdo neověřil.

### 6. Vlastní kontrola

Projdi hotový dokument proti kontrolnímu seznamu v závěru šablony, bod po bodu. Zvlášť
ověř, že v souboru nezůstal placeholder, značka `(modul)` ani příklad ze šablony, že
čísla kapitol sedí s odkazy uvnitř dokumentu a že každý citovaný soubor existuje.

Reviewer bude kontrolovat proti témuž seznamu — co si opravíš tady, nemusíš řešit
v dalším kole, a hlavně tím neplýtváš schválením uživatele na dokument, který proti
vlastnímu závaznému seznamu nikdo neprošel.

### 7. Předložení ke schválení

Ukaž uživateli cestu k souboru a shrnutí každé sekce — u kratšího dokumentu rovnou celý
obsah — a vyžádej si výslovné schválení. **Souhlas vyslovený uprostřed interview není
schválením dokumentu**: uživatel tehdy odpovídal na otázku, ne posuzoval výsledek.

Neschválí-li ho, rozliš, čeho se připomínky týkají:

- **formulace nebo doplnění detailu** → zapracuj Edity a předlož znovu;
- **zásah do návrhu obrazovky** → vrať se do interview v kroku 4 a projdi znovu kroky
  5 až 7. Přepsat větu tam, kde se mění rozhodnutí, znamená zapsat něco, co uživatel
  neodsouhlasil.

Bez schválení se review nespouští.

### 8. Nezávislé review

1. Nástrojem Agent spusť subagenta **synchronně** (`run_in_background: false`) — bez
   verdiktu nemáš jak pokračovat. Typ agenta a model vezmi z frontmatteru
   `review-ux-spec` a předej je parametry nástroje: jako subagent si je sám neuplatní.
   Effort parametrem předat nejde, napiš ho do zadání jako pokyn. Zadání sestav podle
   šablony ve Formátu výstupu.

   **Do zadání dosaď rozvinuté absolutní cesty**, nikde nenech proměnnou — reviewer
   běží jako subagent a `${CLAUDE_PLUGIN_ROOT}` se mu nerozvine. Bez cesty ke kořeni
   pluginu si neotevře ani vlastní postup, ani šablonu, a z kola vypadne celá kontrola
   konformity, aniž by to bylo poznat.

2. **Vráceno k dopracování** → zapracuj všechny blokující nálezy, doporučení uvážlivě
   zvaž. Nález, který vyžaduje skutečné rozhodnutí o návrhu, vrať do interview z kroku 4 —
   neopravuj ho přeformulováním věty. Pak spusť další kolo s **novým** subagentem —
   tomu vypotřebovanému nedávej opravu k posouzení, ztratil by odstup. Každý startuje
   s čistým kontextem, takže co mu do zadání nenapíšeš, pro něj neexistuje.

3. **Schváleno** → dokument je hotový; pokračuj krokem 10.

Nálezy neodmítej mlčky. Reviewer nezná interview, takže může napadnout něco, co uživatel
vědomě zvolil — takový nález patří do reportu, ne do koše.

### 9. Eskalace

Přeruš smyčku a obrať se na uživatele, když:

- nález zpochybňuje rozhodnutí o návrhu, které uživatel v interview výslovně potvrdil —
  návrh vlastní uživatel, ne ty ani reviewer;
- stejný blokující nález přetrvává i po tvém pokusu o opravu (dvě kola);
- proběhla tři kola bez schválení;
- narazíš na technickou chybu, kterou opakování nevyřeší.

Při eskalaci shrň stav smyčky, ocituj sporný nález a polož konkrétní otázku.

### 10. Předání

Reportuj podle Formátu výstupu. Na závěr pojmenuj navazující kroky jako věci, které
spustí uživatel — tenhle skill je nespouští:

- zapsání a odeslání dokumentu (`make-commit`, případně `open-pr`);
- registrace specu mezi **Zdroje pravdy** ve workflow konfiguraci projektu, aby se
  o jeho akceptační kritéria mohly opřít `plan-milestone` a `verify-issue`;
- zápis do paměti agentů, kteří obrazovku budou stavět (`train-agent`).

## Formát výstupu

### Zadání pro reviewera

```
Přečti si soubor `<kořen pluginu>/skills/review-ux-spec/SKILL.md`
a proveď přesně jeho postup. Pracuj s effortem <hodnota z frontmatteru
review-ux-spec>.

Zadání pro tvůj běh:
- Kořen pluginu: <absolutní cesta, rozvinutá — ne proměnná>
- Repozitář: <absolutní cesta k repozitáři cílového projektu>
- Posuzovaný spec: <absolutní cesta>
- Art bible: <absolutní cesta, nebo „projekt ji nemá — vizuální standardy
  vytěženy z kódu">
- Vybrané moduly: <výčet, nebo „jen jádro">
- Číslo kola: <N>
- Nevyřešené nálezy z minulého kola: <žádné, jde o první kolo | seznam nálezů
  i s tím, jak jsi je řešil>

Vrať verdikt přesně ve struktuře, kterou review-ux-spec předepisuje v sekci
„Formát výstupu".
```

### Závěrečný report uživateli

```
UX spec: <cesta> (<nový | úprava>)
Moduly: <vybrané moduly — nebo „jen jádro">
Invarianty převzaté: <kolik a odkud>
Otevřené otázky: <počet> — <čeho se týkají>
Kol review: <N>
Odmítnuté nálezy: <nález → důvod odmítnutí, nebo „žádné">
```

## Zásady

- Šablona má přednost před tímto skillem. Když si odporují, platí šablona.
- **Dva zdroje obsahu se nesmí splést.** Standard rozhodnutý napříč projektem se cituje;
  kompozice téhle obrazovky se vydoluje z uživatele. Vymyslet první nebo se ptát na druhé
  je stejná chyba z opačných stran.
- **Spec nikdy nemění projektový standard.** Potřebuje-li obrazovka výjimku, je to
  otevřená otázka, nebo úloha pro `write-art-bible` — ne řádek v tomhle dokumentu.
- **Vágnost je díra, ne stručnost.** Věta, u které by se implementátor musel doptat,
  patří mezi otevřené otázky.
- Bez schválení uživatelem se nespouští review a bez schváleného review není dokument
  hotový.
- Skill nesahá do kódu a nezakládá issues. Píše dokument, o který se ostatní opřou.
