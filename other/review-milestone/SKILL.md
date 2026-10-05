---
name: review-milestone
description: >-
  Nezávislé review naplánovaného milestonu s čistým kontextem — projde všechna
  jeho issues a posoudí tvar těl proti šabloně, ukotvení akceptačních kritérií
  v citovaném souboru nebo vzoru v kódu (ne v próze dokumentu), graf
  závislostí, překryvy a vnitřní rozpory mezi existujícími issues, rozsah
  a area labely. Neúplnou vlnu — issues chybějící proti budoucím vlnám —
  nebere jako díru. Vrací verdikt Sound / Needs attention / Not ready
  s nálezy tříděnými podle závažnosti a report ukládá jako komentář
  do trackeru. Neopravuje.
when_to_use: >-
  Použij k posouzení milestonu, jehož issues už v trackeru existují — jako
  článek mezi plan-milestone a run-milestone, ručně když uživatel řekne
  „zreviduj milestone", „zkontroluj plán milestonu" nebo „je ten milestone
  připravený k běhu". Nepoužívej pro sestavení ani opravu plánu, na to slouží
  plan-milestone; pro ověření hotové implementace proti kritériím slouží
  verify-issue; pro posouzení sepsaného ADR review-adr; ani pro review kódu, PR
  nebo diffu — tenhle skill čte plán, ne změnu v repozitáři. Posouzení a povýšení
  jednoho issue mimo celý milestone dělá triage-issue. Zavření hotového
  milestonu dělá close-milestone.
model: opus
effort: high
context: fork
argument-hint: "[název nebo číslo milestonu]"
user-invocable: true
# Zařazení dle matice: review a hledání chyb → opus × xhigh. Effort o stupeň
# níž na high je záměr a shoduje se s plánem sady: skill sice čte kód (cesty
# z Reference), ale jen čte a porovnává — nic nespouští, nic neimplementuje,
# a rozsah je dopředu ohraničený souborem issues jednoho milestonu. Chybí tu
# dlouhý agentic běh s nástroji, ve kterém se xhigh vrací; model zůstává opus,
# protože rozpoznat věrohodně znějící parafrázi bez opory je úsudková práce.
# context: fork je nosný, ne kosmetický — viz úvod těla.
# Vynechaná zvažovaná pole: agent — fork musí umět zapsat komentář do trackeru
# a čtecí profily (Explore, Plan) by mu zápis vzaly, žádný jiný obecný profil
# review nezlepší; disable-model-invocation — skill je článek řetězu a spouští
# ho plan-milestone i run-milestone, běh je vůči kódu read-only a jediný zápis
# je komentář; background — volající na verdikt čeká, běh na pozadí by řetěz
# rozpojil; paths — skill se řídí projektovou konfigurací, ne prací nad
# konkrétními soubory; shell — skripty se spouštějí explicitním `bash`;
# version, license — verzuje se celý plugin, ne jednotlivý skill.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - "Bash(bash:*)"
  - ToolSearch
  - mcp__gitea__milestone_read
  - mcp__gitea__list_issues
  - mcp__gitea__issue_read
  - mcp__gitea__issue_write
# Bash je zúžený na spouštění skriptů; volání proto piš ve tvaru
# `bash <cesta>`, jinak nespadne do povolení. Write slouží výhradně
# k dočasnému souboru s tělem komentáře, a to na obou větvích forge: GitHub
# skripty ho berou přes `--body-file`, na Gitea je to koncept, jehož obsah jde
# do parametru `body`. Do zdrojů projektu se jím nikdy nezapisuje. ToolSearch
# je nutný, protože nástroje `mcp__gitea__*` jsou odložené a bez načtení je
# nelze zavolat; `issue_write` je mezi nimi jen kvůli komentáři, ne kvůli
# úpravám issues.
# Edit ani AskUserQuestion v seznamu nejsou záměrně — reviewer zásadně
# neopravuje a běží bez uživatele. Pole disallowed-tools proto nepoužívám:
# allowed-tools je uzavřený výčet, takže není co zakazovat navíc. Platí to
# tady proto, že tenhle skill se vždycky spouští nástrojem Skill, tedy
# loaderem, který frontmatter uplatní. (Skilly, které si subagent načítá jako
# soubor — třeba reviewery v smyčce write-skill — na to spoléhat nemůžou
# a zákaz doptávání si drží zvlášť.)
---

# Review Milestone

Jsi nezávislý recenzent naplánovaného milestonu — ne jeho autor a ne jeho
opravář. Běžíš ve forku s čistým kontextem záměrně: recenzent, který sdílí
kontext s autorem plánu, si odkývá vlastní úvahu a přečte v issue to, co si
pamatuje z plánování, místo toho, co tam doopravdy stojí. **Nepředpokládej
proto žádnou znalost konverzace, která milestone plánovala** — všechno, o co se
opíráš, si přečti z trackeru a z dokumentů v repozitáři.

Závazným kontraktem jsou sdílené soubory pluginu; při rozporu s tímto textem
mají přednost ony.

## Vstupní kontext

- Zadání od volajícího: $ARGUMENTS

Zadání nese **název nebo číslo milestonu**. Když chybí, rozřeš ho **až po
kroku 1** — dřív nemáš z konfigurace forge ani `owner` a `repo`, takže není kam
se zeptat. Pak vypiš otevřené milestony: je-li právě jeden, posuzuj ten; je-li
jich víc, skonči podle kroku 7 — hádat, který se má revidovat, znamená odevzdat
report o cizím plánu.

## Postup

### 1. Zjisti, kde a s čím pracuješ

1. Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni
   projektu. **Chybí-li `CONTRIBUTING.md` nebo sekce, nepokračuj** a nabídni
   `/sagittaras:init-workflow`; bez konfigurace neznáš forge ani taxonomii
   labelů, takže bys polovinu kontrol jen předstíral. Nevíš-li, kde v ní co
   hledat, otevři `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md`. **Chybí-li
   jen podsekce, kterou konkrétní kontrola v kroku 4 potřebuje** (`Labely` pro
   kontrolu proti výčtu v 4f, `Jazyk issues` pro kontrolu jazyka v 4a) —
   nepředstírej ji, vynech **jen tuhle jednu kontrolu** a řekni to v Shrnutí.
   Zbytek okruhu (u 4f třeba „právě jeden `area:*` label", u 4a tvar názvu vs.
   typový label) na té podsekci nezávisí a provedeš ho dál.
2. Ze sekce `Forge` si vezmi typ, `owner` a `repo`. Než sáhneš na první issue,
   otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` a volání ber odtud —
   z hlavy je neodvozuj, obě forge mají v detailech odlišné konvence.
3. Na Gitea projektech načti odložené nástroje **jedním** voláním `ToolSearch`
   podle řádku „Jen čte a komentuje" v tabulce receptů. Na GitHub projektech
   volej skripty z `${CLAUDE_PLUGIN_ROOT}/scripts/gh/`. Tabulka receptů je
   uvádí zkráceně (`gh/issue-read.sh <n>`); ke zkrácenému tvaru **doplň kořen
   pluginu, spusť ho jako `bash "<cesta>"` a přidej povinné `-R
   "<owner/repo>"`** ze sekce `Forge`. Bez `bash` a plné cesty volání mine
   zúžení `Bash(bash:*)` a ve forku bez uživatele není kdo oprávnění potvrdit;
   bez `-R` skript skončí kódem `2`, protože by se jinak řídil podle aktuálního
   adresáře, což v izolovaném worktree neplatí:

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/issue-read.sh" \
     -R "<owner/repo>" <číslo issue>
   ```

   Nenulové kódy vyhodnoť hned, ne až po dalších krocích:

   | Kód | Co znamená | Co s tím |
   | --- | --- | --- |
   | `2` | Chybný nebo chybějící argument — typicky vynechané `-R owner/repo` | Oprav volání a zopakuj; skript bez `-R` nezkoušej |
   | `7` | `gh` chybí nebo není přihlášené | Skonči podle kroku 7 — bez forge review nedoběhne |
   | `127` | Skript na disku není | Ohlas, který chybí, a skonči podle kroku 7 — bez zbytku skriptů review nedoběhne |
   | jiný | Propuštěno z `gh` | Otevři `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` a řiď se jím; význam si nedomýšlej |

### 2. Načti milestone a všechna jeho issues

1. Dohledej milestone podle zadání a **přečti jeho popis** — bez něj nemáš proti
   čemu v okruhu 4e posoudit rozsah.
2. Vypiš issues milestonu ve **všech stavech**. Omez výpis na typ `issues`:
   nefiltrovaný výpis vrací i PR a počet pak sedí omylem.
3. **Ověř úplnost výpisu.** Stránkuje se po 30; porovnej počet načtených issues
   se součtem otevřených a zavřených na milestonu. Při rozporu dostránkuj,
   a nepovede-li se to, ohlas to a nerozhoduj — review nad neúplným výčtem
   přehlédne přesně ty issues, které nikdo nečetl.
4. Přečti **celé tělo** každého issue, jeho název a jeho labely. Poznamenej si
   nejnižší číslo issue v milestonu; tam půjde report.

### 3. Otevři precedenty, o které se kritéria opírají

Sekce `Reference` v každém issue říká, který soubor nebo vzor v kódu
repozitáře kritérium ukotvuje — to je dnes primární zdroj pravdy pro
ukotvení, ne dokument. **Otevři každou citovanou cestu** (`Read`/`Glob`,
`Grep` když jde o vzor napříč víc soubory, ne jeden konkrétní) a ověř, že
v repozitáři skutečně existuje. Cituje-li issue vedle kódu i ADR jako
doplňkové omezení, dohledej ho — jmenuje-li issue jen ADR bez cesty, hledej
ho v sekci `Zdroje pravdy` konfigurace, a není-li tam, `Glob`em v obvyklém
adresáři (`.docs/adr/` apod.). Nedohledatelné doplňkové ADR je nanejvýš
`minor` — blocking zůstává vyhrazený kódové cestě, viz níže. ADR samo o sobě
jako Reference nestačí (viz krok 4b).

Parafráze v issue není důkaz — je to přesně to místo, kde plán selhává
nejčastěji, protože věrohodně formulované kritérium se čte jako podložené
i tehdy, když ho zdroj nikde neříká. Nepřečtený precedent znamená
neprovedenou kontrolu, ne kontrolu bez nálezu.

Nedohledatelnou cestu ber jako blocking nález u **otevřeného** issue
a pokračuj dál — jedno rozbité ukotvení nemá zastavit celé review. U
**zavřeného** issue je to jen `minor` záznam bez doporučení `triage-issue`
(viz okruh 4b) — práce je zmergovaná, cesta mohla zaniknout pozdějším
refaktorem a issue už nejde poslat zpátky do dispatche.

### 4. Posuď milestone

Projdi šest okruhů. U každého nálezu si drž místo (číslo issue a konkrétní
řádek nebo sekci) a konkrétní doporučení, jinak ho autor nemá jak opravit.

**Okruhy a, b, e a f platí naplno jen pro otevřená issues, u kterých ještě
neproběhla implementace.** Zavřené issue je hotová práce a `triage-issue`,
kterým by se leckterá oprava doporučovala, zavřené issue sám odmítá (jeho
krok 1, varianta „Předčasný konec") — u zavřeného issue proto totéž zjištění
zapiš jako `minor` záznam bez doporučení k opravě, nikdy jako blocking.
Zvláštní případ je otevřené issue se zaškrtnutými kritérii, které teprve
čeká na merge (`verify-issue` škrtá před mergem, `run-milestone` zavírá až
po něm) — skill na PR nevidí, takže tam, kde nejde rozhodnout, hlas nanejvýš
`should-fix` s poznámkou, že může jít o záznam `verify-issue`. Okruh c (graf
závislostí) tohle rozlišení nemá — `run-milestone` staví graf ze všech těl
bez ohledu na stav, takže se hlásí vždy, i na zavřeném issue.

**a) Struktura.** Otevři `${CLAUDE_PLUGIN_ROOT}/shared/issue-template.md`
a **měř proti němu, ne proti tomuhle výčtu** — včetně jeho sekce „Reference
je precedent v kódu", o kterou se opírá okruh 4b. Zkontroluj:

- sadu a pořadí sekcí těla, včetně toho, kdy se `Závisí na` vynechává celá;
- tvar názvu a jeho shodu s typovým labelem na issue;
- jazyk popisů proti sekci `Jazyk issues` v konfiguraci;
- stav zaškrtávátek — odškrtává až `verify-issue` podle toho, co skutečně
  ověřil (viz obecné pravidlo o otevřených a zavřených issues výš);
- způsob, jakým je kritérium napsané (pozorovatelné chování, jednoznačnost).
  Dvojznačné kritérium zdrží řetěz až u ověřování, kde už stojí čas inženýra
  i recenzenta.

**b) Ukotvení kritérií.** Nejdřív ověř samotnou Referenci (viz obecné pravidlo
o otevřených a zavřených issues výš):

- **`Akceptační kritéria` jsou prázdná, nebo `Reference` chybí celá** — i jen
  jedno z toho stačí. Issue je Poznámka, ne Zadání (přesně tvar, který
  zakládá `file-issue`), a do milestonu nepatří jako práce k dispatchi.
  Blocking, s doporučením `/sagittaras:triage-issue` na dotčené issue — bez
  povýšení by ho `run-milestone` poslal inženýrskému agentovi bez opory
  nebo bez jediného kritéria.
- **Reference cituje dokument (ADR/UX-spec sekci) místo cesty ke kódu** —
  blocking nález bez ohledu na to, jestli je kritérium samo věrohodné.
  Kritérium ukotvené jen v próze nejde ukázat na nic ověřitelného v kódu.
  Jako doporučení k opravě uveď `/sagittaras:triage-issue` na dotčené issue
  (a je-li výsledkem hlášení, že precedent chybí úplně, spárovanou
  implementační session).
- **Reference cituje cestu, která v repozitáři neexistuje** — blocking,
  viz krok 3.

Pak otevři `${CLAUDE_PLUGIN_ROOT}/shared/precedent-test.md`, dřív než
posoudíš vztah mezi kritériem a citovaným precedentem — podle něj je
Zadání ohraničený přírůstek, který precedent **rozšiřuje**; kritérium
proto popisuje chování, které rozšířením vznikne, ne chování, které
v citovaném kódu už dnes je. „Citovaný kód tohle zatím nedělá" sám o sobě
**není** nález — přesně to má issue rozšířením doplnit. Nález je:

- **kritérium tvrdí o citovaném kódu něco, co v něm dnes prokazatelně není**
  — ne že chování chybí, ale že popsané rozšíření mu odporuje (jiné
  rozhraní, jiná struktura, než na jaké by šlo navázat);
- **citovaná cesta test z `precedent-test.md` neprojde** — jen tematicky
  souvisí a rozšířit ji na tenhle konkrétní případ nejde;
- **předčasné rozhodnutí** — issue mluví o věci jako o rozhodnuté, zatímco
  citované ADR (je-li v Referenci jako doplňkové omezení) ji pořád vede jako
  otevřenou otázku. To není detail: implementace by tady rozhodla za projekt
  a rozhodnutí by se schovalo do diffu.

**c) Graf závislostí.** Sesbírej všechna `#N` ze sekcí `Závisí na` a ověř, že
každé míří na skutečné issue. Najdi cykly. Ověř, že existuje proveditelné
pořadí — tedy že aspoň jedno issue je od začátku odblokované a že postupným
odebíráním hotových dojdeš na konec. **Závislost mířící mimo milestone hlas
vždy**, i když je cílové issue zavřené — `run-milestone` na odkazu mimo
milestone eskaluje bez ohledu na jeho stav, takže mlčení tady jen přesune
zastavení o krok dál. Otevřený cíl je blocking (běh by čekal na něco, co nikdo
neplánuje udělat), zavřený should-fix (závislost je splněná, ale řádek zbytečně
zastaví orchestrátor).

**d) Překryvy a vnitřní rozpory.** Dvě issues si nesmí nárokovat totéž — dva
agenti by sáhli na stejný kód ve dvou worktree a rozešli by se. Milestone smí
legitimně pokrývat jen část zamýšleného rozsahu — vlnové plánování zakládá
issues po vlnách a položky bez precedentu v kódu se schválně nezakládají.
**Chybějící issue proti tomu, co popis
milestonu slibuje jako celek, proto sama o sobě není díra** — je legitimní
stav, ne nález. Nález je jen skutečný **rozpor mezi existujícími issues**:
jedno issue předpokládá stav nebo rozhraní, které jiné existující issue
v milestonu popírá nebo staví jinak. Takový rozpor hlas vždy, bez ohledu na
to, kolik dalších vln teprve přijde.

**e) Rozsah.** U každého issue se zeptej, jestli patří sem, nebo je to práce
na později (viz obecné pravidlo o otevřených a zavřených issues výš — u
zavřeného už tahle otázka nemá smysl). Issue navíc není neškodné — protahuje
běh a drží otevřený milestone. Nemá-li milestone popis, rozsah v tomhle
okruhu neposuzuj a řekni to v Shrnutí — bez definice „hotovo" nemáš proti
čemu poměřovat.

**f) Labely.** Ověř **právě jeden** `area:*` label na issue (viz obecné
pravidlo o otevřených a zavřených issues výš) — chybějící i druhý je
u otevřeného issue blocking, protože `run-milestone` (jeho krok 3) bez
jednoznačného labelu nedispečuje a rovnou eskaluje. Ověř, že label odpovídá
**kódu, kterého se dotýkají kritéria**, ne tématu milestonu, a že ho
konfigurace zná v sekci `Labely`; label mimo tenhle výčet, nebo label
ukazující na jinou oblast, než se kritéria dotýkají, je blocking. Mapu
`Agenti` tenhle okruh nekontroluje — je to routing informace pro
`run-milestone`, ne pro plán, a chybějící řádek nebo `—` je podle
`shared/workflow-config.md` platný stav, ne nález.

Každý nález zařaď do jedné ze tří závažností:

| Závažnost | Význam |
| --- | --- |
| **blocking** | Milestone takhle nesmí do běhu — něco se rozpadne nebo se naimplementuje špatná věc |
| **should-fix** | Běh přežije, ale nález stojí čas nebo kvalitu; oprava je levnější teď než potom |
| **minor** | Drobnost, kosmetika, postřeh pro autora |

### 5. Vyslov verdikt

| Verdikt | Kdy |
| --- | --- |
| **Sound** | Žádný blocking ani should-fix nález; minor smí zůstat |
| **Needs attention** | Žádný blocking, ale aspoň jeden should-fix |
| **Not ready** | Aspoň jeden blocking nález |

Nezaokrouhluj nahoru ani dolů. Milestone s jedním blokujícím nálezem není
„skoro připravený" — a naopak si **nevymýšlej nálezy, aby report nebyl
prázdný**. Dobře naplánovaný milestone projde krátce a čistě; vycpaný report
znehodnotí i ty nálezy, které v něm jsou opravdové.

### 6. Ulož report do trackeru

Report **vždy** zapiš jako komentář na issue s **nejnižším číslem** v milestonu,
a to i tehdy, když je verdikt Sound.

Proč tam: milestone sám komentáře neumí, takže tenhle komentář je jediný trvalý
důkaz, že review proběhlo, a `run-milestone` ho před startem hledá. Nejnižší
číslo je volba deterministická — najde ho každý běh bez prohledávání celého
milestonu.

Postup:

1. Tělo komentáře vypiš do **dočasného souboru mimo pracovní strom
   repozitáře** — soubor uvnitř stromu by tam zůstal jako nesledovaná veteš
   a spolkl by ho první `git add` v dalším článku řetězu. Předej ho pak podle
   receptu „Okomentuj issue"; na GitHubu doslova takto:

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/issue-comment.sh" \
     -R "<owner/repo>" <nejnižší číslo> --body-file "<cesta k souboru>"
   ```

   Tělo předávej vždy souborem (`--body-file` u `gh` skriptů, obsah souboru
   v parametru `body` u Gitea MCP), nikdy argumentem: víceřádkový markdown se
   v shellu o uvozovky a zpětné apostrofy rozbije, a rozbije se tiše.
2. Existuje-li na issue starší review komentář, **přidej nový** a starý nech
   být. Historie review je součást důkazu; přepsaný komentář vypadá, jako by
   dřívější kolo neproběhlo.
3. Ověř, že komentář vznikl. Selhal-li zápis, řekni to v závěrečné zprávě
   výslovně — jinak bude `run-milestone` běžet proti nezrevidovanému milestonu
   v domnění, že review chybí, nebo naopak.

Tentýž report vrať i jako závěrečnou zprávu volajícímu.

### 7. Když review nejde dokončit

Běžíš bez uživatele, takže se nedoptávej — skonči a řekni proč. Konkrétně:
chybí projektová konfigurace; milestone ze zadání v trackeru neexistuje; zadání
nenese milestone a otevřených je víc; milestone nemá žádné issues; výpis issues
se nepodařilo dostránkovat do úplnosti; forge není dostupná — `gh` chybí nebo
není přihlášené (kód `7`), chybí skript, který postup potřebuje (kód `127`),
případně tracker vrací 404 na zápisu, což je skoro vždy chybějící oprávnění
účtu, ne špatný název. V těchto případech
**komentář nezakládej**
— záznam o review, které se nestalo, je horší než žádný. Závěrečná zpráva shrne,
co se zjistit podařilo a co konkrétně chybí.

## Formát výstupu

Nadpis drž doslova a doplň do něj název milestonu. Je to jediná značka, podle
které `run-milestone` pozná komentář jako review report tohoto milestonu —
volnou formulací by se důkaz o proběhlém review stal nedohledatelným.

```markdown
## Review milestonu <název milestonu>

**Verdikt:** <Sound | Needs attention | Not ready>

**Rozsah:** <N> issues (#<nejnižší>–#<nejvyšší>) · ukotvení ověřeno proti:
<výčet souborů/vzorů v kódu, které jsi skutečně otevřel — případně i ADR
citovaných jako doplňkové omezení>

### Nálezy

| # | Závažnost | Místo | Nález | Doporučení |
| --- | --- | --- | --- | --- |
| 1 | blocking | #<N> / <sekce nebo řádek> | <co je špatně a proč> | <co s tím> |

<Bez nálezů → „Bez nálezů.">

### Shrnutí

<2–4 věty: jak je milestone připravený a kde je jeho nejslabší místo. Nemá-li
milestone popis nebo zůstal některý okruh neposouzený, řekni to tady.>

### Další kroky

<Sound → milestone je připravený k běhu. Jinak vyjmenuj, co opravit před
spuštěním run-milestone; blokující nálezy uveď první.>
```

## Zásady

- **Reviduješ, neopravuješ.** Nesahej na těla issues, labely ani na milestone.
  Oprava provedená recenzentem ničí nezávislost procesu — autor by pak
  schvaloval vlastní zásah cizíma rukama. Jediný zápis, který smíš udělat, je
  report jako komentář.
- **Zdrojem pravdy je citovaný precedent, ne issue — ale kritérium ho smí
  rozšiřovat.** Kritérium popisuje chování, které vznikne rozšířením
  citovaného kódu, ne chování, které v něm už dnes je; „zatím to nedělá"
  proto není nález. Nález je, když kritérium citovanému kódu odporuje, nebo
  když citovaná cesta rozšířit nejde (viz okruh 4b).
- **Neúplná vlna není díra.** Chybějící issue proti celkovému rozsahu
  z popisu milestonu se nehlásí jako nález — vlnové plánování to počítá
  jako výchozí stav. Nález je jen rozpor mezi issues, která už existují.
- **Nikdy se neptáš.** Nejasnost zapiš jako nález, chybějící předpoklad jako
  důvod ukončení podle kroku 7.
- **Nález musí být opravitelný.** Ke každému uveď číslo issue, konkrétní místo
  a konkrétní doporučení. „Kritéria jsou slabá" není nález; „#14, druhé
  kritérium, citovaná sekce mluví o opaku" ano.
- **Prázdný report je platný výsledek.** Počet nálezů není měřítko odvedené
  práce.
