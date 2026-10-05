---
name: write-art-bible
description: >-
  Sepíše art bible cílového projektu nebo aktualizuje existující — vytěží
  z repozitáře, co už o vzhledu platí (tokeny, písma, komponenty, brand),
  doptá se na záměr, podle povahy projektu vybere moduly šablony a po
  odsouhlasení osnovy dokument zapíše. Hodnotu, pro kterou nemá oporu v kódu
  ani od uživatele, nevymýšlí — nechává ji jako otevřenou otázku s vlastníkem.
  Kontrastní poměry počítá, neodhaduje.
when_to_use: >-
  Použij, když má v projektu vzniknout nebo se aktualizovat závazný popis
  vzhledu — „napiš art bible", „potřebujeme sjednotit vizuál", „doplň do art
  bible ten nový prvek" — i tehdy, když si uživatel stěžuje, že rozhraní vzniká
  pokaždé jinak nebo šedé a bez identity. Nepoužívej pro pravidlo v
  `.claude/rules/`, na to slouží write-rule; pro popis jedné obrazovky nebo flow
  write-ux-spec; pro projektové instrukce čtené v každé session write-claude-md;
  pro rozhodnutí o technologii stylingu i s alternativami write-adr; pro zápis
  hotového dokumentu do paměti agenta train-agent; ani pro implementaci vzhledu
  do kódu, tu vlastní implement-issue.
argument-hint: "[téma nebo cesta k existující art bible]"
# Odchylka od konvence pojmenování: název má tři slova. `art-bible` je ale jeden
# název artefaktu, ne dva předměty — skill dělá jednu věc. Zkrácení na
# `write-style` nebo `write-visuals` by triggering zhoršilo, protože uživatel
# řekne přesně „art bible".
model: opus
effort: high
# Zařazení dle matice: „strategie / koncepční návrh → opus × high" — zadání je
# otevřené (co do dokumentu patří, závisí na povaze projektu), ale exekuce je
# krátká a interaktivní. Nikoli sonnet: skill rozhoduje, které hodnoty smí
# napsat jako fakt a které patří do otevřených otázek, a vymyšlená hodnota
# v dokumentu, který se cituje jako zdroj pravdy, se propíše do celého UI, aniž
# by cokoli spadlo. Nikoli xhigh: skill nikam neběží dlouho sám — těžiště je
# interview a odsouhlasená osnova, ne autonomní průzkum.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - AskUserQuestion
# Bash je tu výhradně kvůli výpočtu kontrastních poměrů (krok 6): poměr
# spočítaný od oka je v dokumentu, který se cituje jako zdroj pravdy, horší
# než žádný. Nic jiného skill přes shell nedělá.
# Vynechaná zvažovaná pole: Agent a Skill — art bible neprochází nezávislým
# reviewem, protože vizuální záměr vlastní uživatel a bránou je jeho odsouhlasená
# osnova (krok 5); navazující skilly (train-agent, write-rule) spouští uživatel;
# disable-model-invocation — skill je užitečný i když si ho model vyvolá sám
# ze stížnosti na nekonzistentní vzhled; context/agent/background — interview
# vyžaduje uživatele v hlavním kontextu, fork ani běh na pozadí nemají komu
# klást otázky; paths — skill se spouští z konverzace o vzhledu, ne prací nad
# konkrétními soubory; shell — awk z kroku 6 se volá přes Bash s výchozím
# shellem, vnucovat cílovému projektu jiný není důvod; disallowed-tools —
# allowed-tools je uzavřený výčet
# a skill se nespouští načtením souboru, není co zakazovat navíc;
# version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Write Art Bible

Cílem je dokument, podle kterého člověk i agent postaví vzhled stejně — a který
se nerozejde s kódem, protože každá jeho hodnota má uvedeno, kde v kódu žije.
Závazným kontraktem je šablona vedle tohoto souboru; při rozporu s čímkoli,
včetně tohoto skillu, má přednost ona.

Referenční soubory čti přes `${CLAUDE_PLUGIN_ROOT}`; plugin běží nad cizím
projektem, kde relativní cesta `skills/…` míří někam jinam.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Příprava

1. Přečti `${CLAUDE_PLUGIN_ROOT}/skills/write-art-bible/art-bible-template.md` —
   kostru, výběr modulů podle povahy projektu a kontrolní seznam, na které se
   budeš celou dobu odvolávat.
2. Najdi existující dokument — hledej `**/art-bible*.md` a projdi dokumentační
   složku projektu (`.docs/`, `docs/`, `wiki/`). Dokument bývá zanořený podle
   domény (`.docs/ui/art-bible.md`), takže samotný kořen nestačí. Hledej i pod
   jinými názvy — `style-guide`, `design-system`, `brand`, `vizualni-styl`:
   dokument popisující vzhled projektu je art bible, i když se tak nejmenuje.
   Takový nález nezakládej podruhé pod novým jménem — předlož ho uživateli
   v interview a nech rozhodnout mezi jeho aktualizací a novým dokumentem
   s křížovým odkazem. Dva zdroje pravdy o vzhledu jsou horší než jeden zastaralý.
3. Podle nálezu urči **režim**:
   - **Nová art bible** — v projektu žádná není.
   - **Aktualizace** — existující dokument se rozšiřuje nebo opravuje.
4. **U aktualizace přečti celý existující dokument, včetně komentářů
   a zapsaných rozhodnutí.** Hodnoty v něm nesou provenienci — někdo je změřil
   nebo o nich rozhodl. Přepsat je bez znalosti důvodu znamená zahodit měření
   a vrátit hodnotu, kterou už jednou někdo opravil.

### 2. Vytěžení projektu

Než se začneš ptát, přečti si, co projekt o svém vzhledu už říká. Hodnota
opsaná z kódu je fakt; hodnota vyslovená v interview je záměr, který se s kódem
teprve srovná.

| Co hledat | Kde typicky |
| --- | --- |
| Barevné tokeny, palety | `@theme`, `:root`, SASS mapy, `tailwind.config`, token JSON, resource dictionary |
| Písma a jejich zavedení | `@font-face`, `next/font`, `package.json`, složka `fonts/` |
| Existující komponenty a jejich třídy | Balíček UI, `components/`, Storybook stories |
| Rozhodnutí o stylingu | ADR projektu, `CLAUDE.md`, rules v `.claude/rules/` |
| Záměr a nálada | Pilíře, design dokument, brand manuál, README |
| Assety a jejich pojmenování | `assets/`, `public/`, `Resources/` |

Zapiš si tři oddělené seznamy — **fakt z kódu**, **rozpor**, **díra**. Rozporem
je i to, když rule v `.claude/rules/` nebo `CLAUDE.md` předepisuje jinou hodnotu,
než jaká má být v dokumentu — ty se načítají v každé session a platí dál a tiše,
takže art bible, která se s nimi rozejde, prohraje. Rozpor nikdy neřeš sám:
předlož ho uživateli v interview jako otázku, protože rozhodnout, která strana
je správně, znamená rozhodnout o vzhledu.

### 3. Povaha projektu a výběr modulů

Z vytěženého urči, co projekt reálně vyrábí — rozhraní z komponent, hru,
tištěný výstup, obsah pro kanály — a podle tabulky v šabloně (§ 1.1) navrhni
sadu modulů. Nezakládej modul, pro který projekt nemá obsah: prázdná kapitola
vyplněná obecnými větami je horší než chybějící, protože vypadá jako
rozhodnutí, kterým není.

Výběr modulů si nech potvrdit v interview spolu se zbytkem.

### 4. Interview

Ptej se **jen na to, co v repozitáři není**. Vytěženou hodnotu předlož jako
fakt k potvrzení, ne jako otázku — jinak nutíš uživatele diktovat něco, co už
napsal do kódu. Veď interview po kolech nástrojem AskUserQuestion, s konkrétními
možnostmi tam, kde dávají smysl.

Zjisti:

- **Záměr a nálada** — čím projekt je, jak má působit, čemu se vzhled
  podřizuje. Tohle je jediná část dokumentu, která nejde odvodit odjinud.
- **Reference** — konkrétní produkt a co si z něj bereme. Trvej na tom, aby
  bylo řečeno i to, co si z reference *nebereme*, hrozí-li záměna.
- **Opakované selhání** — co v tomhle projektu vzniká špatně pořád dokola.
  Z odpovědi se stane kapitola *Tvrdá pravidla*; bez ní je dokument popisný
  a nic nevymáhá.
- **Rozpory z kroku 2** — která strana platí.
- **Vlastník, stav a cesta uložení** — kdo rozhoduje o změnách a kam soubor
  patří. Cestu navrhni podle struktury dokumentace projektu.
- **Chybějící hodnoty povinných kapitol** — paleta, písma, škály, ale i prahy
  přístupnosti, minimální velikost písma a klikací plocha. U každé nabídni
  konkrétní návrh (u přístupnosti typicky WCAG AA, tedy 4,5 : 1 a 3 : 1)
  a nech ho potvrdit; nepotvrzené se nezapisuje jako fakt. Povinná kapitola
  bez hodnot se nedá odbýt obecnou větou — buď má potvrzený obsah, nebo
  otevřenou otázku s vlastníkem.

**Nemáš-li uživatele, dokument nepiš.** Art bible vymyšlená z domněnek se
cituje jako zdroj pravdy a tím zafixuje vzhled, který nikdo nechtěl. Selže-li
volání AskUserQuestion nebo odpověď nedorazí, shrň, na co potřebuješ odpovědět,
a skonči — nezakládej soubory.

### 5. Osnova ke schválení

Než cokoli zapíšeš, předlož uživateli:

- cestu k souboru a režim (nový / aktualizace),
- seznam kapitol včetně vybraných modulů,
- vytěžené hodnoty roztříděné na **fakt z kódu**, **návrh k potvrzení**
  a **otevřenou otázku**,
- u aktualizace navíc výčet toho, čeho se změna dotkne — a co zůstává.

Teprve po odsouhlasení zapisuj. Oprava osnovy stojí jednu větu, oprava hotového
dokumentu celé kolo.

### 6. Zápis

Piš podle šablony; sekce po výběru modulů očísluj a čísla drž, protože se na ně
uvnitř dokumentu i v issues odkazuje.

Nový dokument zapiš Writem. **Aktualizaci veď cílenými Edity**, nikdy plným
přepisem: hodnoty v existujícím dokumentu nesou provenienci a přepis zahodí to,
co se do nové verze nepřeneslo, aniž by to v diffu bylo poznat jako ztrátu.

Při psaní platí:

- **Nevymýšlej hodnotu.** Co nemá oporu v kódu ani v potvrzené odpovědi, jde do
  *Otevřených otázek* s vlastníkem a termínem — ne do tabulky jako by platilo.
- **Ke každé sadě hodnot napiš, kde v kódu žije**, a u dvou kopií i to, že se
  mění současně. Bez toho se dokument a implementace tiše rozejdou.
- **Kontrastní poměry počítej, neodhaduj.** Poměr napsaný od oka se v dokumentu
  tváří jako měření. Za `A` a `B` dosaď šest hexadecimálních číslic; zkrácený
  zápis (`#fff`) nejdřív rozviň, jinak příkaz skončí chybou místo výsledku:

  ```bash
  awk -v A=ff8a8a -v B=7a2020 'function hx(s, i,n,d){n=0;for(i=1;i<=length(s);i++){d=index("0123456789abcdef",substr(tolower(s),i,1))-1;n=n*16+d}return n}
  function ch(v){v/=255;return v<=0.03928?v/12.92:((v+0.055)/1.055)^2.4}
  function lum(h){return 0.2126*ch(hx(substr(h,1,2)))+0.7152*ch(hx(substr(h,3,2)))+0.0722*ch(hx(substr(h,5,2)))}
  BEGIN{gsub(/[^0-9a-fA-F]/,"",A);gsub(/[^0-9a-fA-F]/,"",B);if(length(A)!=6||length(B)!=6){print "CHYBA: ocekavam sest hex cislic na kazde strane";exit 1}
  a=lum(A);b=lum(B);hi=(a>b?a:b);lo=(a>b?b:a);printf "%.4f:1\n",(hi+0.05)/(lo+0.05)}'
  ```

  Změř každou dvojici text × podklad, kterou do dokumentu píšeš. Nedosáhne-li
  prahu, neschovávej to — buď hodnotu posuň, nebo zapiš omezení, za jakých se
  smí použít.

  Nejsou-li barvy v hexu (`oklch`, `hsl`, `rgb` — výchozí tvar palety Tailwindu
  v4), převeď je nejdřív na hex a v dokumentu uveď obě podoby. Nejde-li převod
  spolehlivě, zapiš dvojici do *Otevřených otázek* — nezměřené číslo je horší
  než přiznaná mezera.
- **Změněnou hodnotu doprovoď rozhodnutím.** Mění-li se hodnota proti dřívějšímu
  stavu nebo se rozhoduje spor, zapiš k ní blok podle šablony (§ 3.1): co bylo,
  proč to nestačilo, co se mění a kam se to promítá. Bez toho ji za rok někdo
  „opraví" zpátky.
- **Nesahej do kódu.** Skill zapisuje dokument. Zavedení tokenů, úpravu
  komponent ani přebarvení UI nedělá — to je práce, která se zadává issuem.

### 7. Vlastní kontrola

Projdi hotový dokument proti kontrolnímu seznamu v závěru šablony, bod po bodu.
Zvlášť ověř, že:

- v souboru nezůstal žádný placeholder v hranatých závorkách ani značka `(modul)`;
- čísla kapitol sedí s odkazy uvnitř dokumentu;
- každý citovaný soubor a každá cesta v křížových odkazech skutečně existuje —
  odkaz na neexistující dokument je horší než žádný, protože se tváří jako opora;
- žádná hodnota se v dokumentu neobjevuje ve dvou verzích.

### 8. Předání

Reportuj podle Formátu výstupu. Na závěr pojmenuj navazující kroky, které
z hotového dokumentu plynou — zápis do paměti agentů, kteří vzhled vlastní
(`train-agent`), a vytěžení vymahatelné části do rule v `.claude/rules/`
(`write-rule`) — jako další krok, který spustí uživatel. Tenhle skill je
nespouští: jsou to samostatné úlohy s vlastními kontrolami a udělat je
mimochodem znamená ty kontroly obejít. Vyšel-li z kroku 2
rozpor se sousední rule, patří sem i její oprava — rozpor se neřeší přidáním
třetí formulace.

## Formát výstupu

```
Art bible: <cesta> (<nová | aktualizace>)
Moduly: <vybrané moduly — nebo „jen jádro">
Zdroj hodnot: <kolik faktů z kódu / kolik potvrzených návrhů>
Otevřené otázky: <počet> — <čeho se týkají>
Rozpory s kódem: <jak byly rozhodnuté, nebo „žádné">
```

## Zásady

- Šablona má přednost před tímto skillem. Když si odporují, platí šablona.
- Art bible říká **co** vypadá jak. Rozhodnutí **čím** se to staví patří do ADR
  projektu — a skill ho nepřepisuje ani nenahrazuje.
- Nepotvrzená hodnota není fakt. Mezi „vymyslet" a „nechat otevřené" volí skill
  vždy druhé, protože chybějící řádek se doplní, kdežto vymyšlený se cituje.
- Bez odsouhlasené osnovy se nezapisuje.
- Dokument je živý. U aktualizace se zvyšuje verze a datum v hlavičce; přepsat
  zapsané rozhodnutí bez nového rozhodnutí je ztráta informace, ne úklid.
