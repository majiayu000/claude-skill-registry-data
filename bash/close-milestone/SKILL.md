---
name: close-milestone
description: >-
  Zavře milestone, jehož práce je hotová — ověří, že všechna jeho issues jsou
  zavřená (stránkovaně a proti počtům z trackeru) a že integrační PR je opravdu
  zmergovaný, a teprve pak milestone zavře jedním voláním. Při jakémkoli rozporu
  nezavírá a vypíše, co brání: otevřená issues i s čísly, nezmergované PR, nebo
  anomálii. Prázdný milestone nezavírá tiše.
when_to_use: >-
  Použij, když je práce na milestonu hotová a má se uzavřít — „zavři milestone",
  „ukliď hotový milestone", „je to zmergované, zavři to" — typicky poté, co
  člověk zmergoval integrační PR do výchozí větve. Nepoužívej pro zavírání
  jednotlivých issues, to je jedno volání trackeru, ne úloha pro skill; ani pro
  plánování milestonu, na to slouží plan-milestone; ani pro posouzení plánu, to
  dělá review-milestone; ani pro implementaci jeho issues, tu řídí run-milestone
  — ten milestone záměrně nechává otevřený, protože finální merge patří člověku.
argument-hint: "[název nebo číslo milestonu]"
model: haiku
# Effort tu není a být nesmí: haiku ho nepodporuje a jeho uvedení skončí chybou
# při běhu (model-effort-matrix.md, Tabulka 1 a Časté chyby). Není to opomenutí.
# Zařazení dle matice: inventura a kontrola formátu → haiku, bez effortu.
# Postup je proto vědomě držený mechanický: každé rozhodnutí v krocích 1–3 je
# vyjmenované jako podmínka nad hodnotou z trackeru (počty sedí/nesedí, PR má
# merge/nemá, shoda názvu je/není) a v žádné mezní situaci skill nezavírá podle
# vlastního úsudku — nejednoznačnost vždy končí otázkou na uživatele. Nikoli
# sonnet: nic se tu nenavrhuje ani neposuzuje. Kontextový limit haiku (200K)
# nevadí, skill čte výpisy trackeru, ne dokumentaci projektu. Kdyby reálné běhy
# ukázaly, že haiku některou z větví míjí, správnou opravou je sonnet × medium
# (bod 2 rozhodovacího stromu), ne dopisování dalších podmínek.
user-invocable: true
allowed-tools:
  - Read
  - AskUserQuestion
  - ToolSearch
  - "Bash(bash:*)"
  - mcp__gitea__milestone_read
  - mcp__gitea__milestone_write
  - mcp__gitea__list_issues
  - mcp__gitea__list_pull_requests
  - mcp__gitea__pull_request_read
# Zúžení práv je tu levné a smysluplné: skill má jediný zápis (zavřít milestone)
# a všechno ostatní jen čte. Bash je zúžený na spouštění skriptů; git ani gh se
# nikdy nevolá přímo. Proto volání skriptů piš ve tvaru
# `bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/<skript>.sh"` — v jiném tvaru buď
# nespadne do povolení, nebo se v izolovaném worktree netrefí do kořene pluginu.
# ToolSearch a pětice mcp__gitea__* je tu kvůli Gitea
# větvi: nástroje jsou odložené a bez ToolSearch se nenačtou, bez uvedení v tomto
# výčtu se nezavolají. Názvy odpovídají tvaru z forge-recipes.md; běží-li Gitea
# MCP pod jiným prefixem, ohlas to a výčet neobcházej.
# Vynechaná zvažovaná pole: effort — viz výše, u haiku je to chyba za běhu;
# Glob/Grep — konfigurace má pevnou cestu a zbytek vstupu jsou výpisy trackeru,
# není co hledat v souborech; Write/Edit — skill nezapisuje na disk;
# disable-model-invocation — zavření je vratné jedním voláním a cíl si skill
# nevybírá sám (krok 1), takže samovolné spuštění nemůže zavřít nic cizího;
# context/agent/background — výběr milestonu i potvrzení mezních stavů potřebují
# uživatele v hlavním kontextu, fork ani běh na pozadí nemají komu klást otázky;
# paths — spouští se z konverzace, ne prací nad soubory; shell — skripty se
# spouští explicitním `bash`; disallowed-tools — allowed-tools je uzavřený
# výčet, není co zakazovat navíc; version/license — verzuje se celý plugin.
---

# Close Milestone

Cílem je zavřít milestone teprve tehdy, když je jeho práce **prokazatelně**
hotová — všechna issues zavřená a integrační PR zmergovaný. Zavřít předčasně je
horší než nezavřít: zavřený milestone vypadá jako hotová práce a nikdo se do něj
už nedívá. Závazným kontraktem jsou sdílené soubory pluginu; při rozporu s tímhle
postupem platí ony.

| Soubor | Kdy ho otevři |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/shared/workflow-config.md` | V kroku 1, když projektová konfigurace chybí nebo v ní nenajdeš sekci, kterou potřebuješ |
| `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` | V kroku 1, dřív než sáhneš na tracker — včetně sekce s nástrahami, na které tenhle skill stojí |
| `${CLAUDE_PLUGIN_ROOT}/shared/git-scripts.md` | V kroku 1, je-li forge GitHub — než spustíš první `gh/*.sh` |

## Vstupní kontext

- Milestone od uživatele (může být prázdné): $ARGUMENTS

## Postup

### 1. Načti konfiguraci a urči milestone

Přečti sekci `## Workflow (sagittaras)` v `CONTRIBUTING.md` v kořeni cílového
projektu. Potřebuješ podsekci **Forge** (kterou větev receptů použít,
`owner/repo`) a **Větvení** (výchozí větev a tvar integrační větve
`milestone/<slug>`).

- **`CONTRIBUTING.md` neexistuje nebo sekci nemá** → nepokračuj a nedomýšlej si
  hodnoty. Řekni uživateli, že projekt nemá workflow konfiguraci, a nabídni
  `/sagittaras:init-workflow`.
- **Chybí podsekce, kterou potřebuješ** → řekni která a nabídni doplnění; sám ji
  za pochodu nedoplňuj.

Pak otevři `${CLAUDE_PLUGIN_ROOT}/shared/forge-recipes.md` a **volání neodvozuj
z hlavy**. Podle sekce `Forge` si připrav větev:

- **Gitea** → **jedním** voláním načti odložené nástroje. Role tohoto skillu
  (čtení + jediný zápis na milestone) nemá v tabulce rolí vlastní řádek, takže
  použij tenhle select:

  ```
  select:mcp__gitea__milestone_read,mcp__gitea__milestone_write,mcp__gitea__list_issues,mcp__gitea__list_pull_requests,mcp__gitea__pull_request_read
  ```

- **GitHub** → skripty spouštěj `bash`em a s cestou ukotvenou ke kořeni pluginu,
  jinak se v izolovaném worktree netrefí. **Vždy jim předej `-R owner/repo`**
  ze sekce `Forge`; bez toho se řídí aktuálním adresářem, což tamtéž neplatí:

  ```bash
  bash "${CLAUDE_PLUGIN_ROOT}/scripts/gh/milestone-list.sh" -R <owner/repo> --state all
  ```

  Skončí-li kterýkoli skript kódem `7`, chybí `gh` nebo není přihlášené — řekni
  to uživateli hned a skonči, ne až v půlce kontrol. Jakýkoli jiný nenulový kód
  (typicky `2` u chybného argumentu) ohlas doslova a skonči bez zavírání.

**Milestony načti receptem „Vypiš milestony" se stavem `all`** — je to jediný
recept, kterým se milestone čte. Řádek receptu ukazuje `--state open`, ale `all`
je podle `git-scripts.md` platná hodnota přepínače a potřebuješ ji, abys poznal
už zavřený milestone. Shodu na argument dělej nad tímhle výpisem, ne dalším
voláním. Z odpovědi si u vybraného milestonu **zapamatuj číslo, název,
`open_issues` a `closed_issues`**: na počtech stojí křížová kontrola v kroku 2
a číslo s názvem potřebuješ jako parametr do kroků 2 až 4, kde se liší podle
forge i podle operace.

Cíl urči takto:

- **Argument je prázdný** → nabídni otevřené milestony z výpisu a nástrojem
  AskUserQuestion **nech uživatele vybrat**. Cíl si nevybírej sám: skill mění
  stav a odhadnutý milestone se zavře potichu a špatně.
- **Argument sedí právě na jeden milestone** (číslo nebo název) → pokračuj s ním.
- **Argument nesedí na žádný** → vypiš, co jsi hledal a co v repozitáři je,
  a skonči. Nic nezavírej.
- **Argument sedí na víc milestonů** (částečná shoda názvu) → předlož nalezené
  přes AskUserQuestion a nech vybrat.
- **Vybraný milestone je už zavřený** → řekni to a skonči. Není to chyba, je to
  no-op.

### 2. Kontrola 1 — všechna issues zavřená

Receptem „Vypiš issues milestonu" načti issues, se stavem `all`. Volání se liší
podle forge víc, než vypadá:

- **Gitea** → `list_issues`, `milestones` jako **pole řetězců** s číslem
  milestonu, a **povinně `type: "issues"`**. Bez filtru typu spadnou do výpisu
  i pull requesty, počet vyjde vyšší a kontrola „všechno zavřené" projde omylem
  — přesně to selhání, kvůli kterému skill existuje. Stránkuje se po 30, takže
  načítej další stránky (`page`), dokud poslední vrátí plných 30.
- **GitHub** → `issue-list.sh --milestone "<název>" --state all`. `--milestone`
  bere **název milestonu, ne číslo**; s číslem filtr vrátí prázdno, kontrola
  níž pak selže na neshodě počtů a vypadá to jako porucha trackeru. Filtr typu
  tu nemá protějšek a nepotřebuje ho — `gh issue list` pull requesty nevrací.
  Nestránkuje se, ale výpis je useknutý na 500 položek; blíží-li se počet téhle
  hranici, ohlas to a nerozhoduj z něj.

Načtený počet porovnej s `open_issues` + `closed_issues` z kroku 1:

- **Souhlasí** → vyhodnoť stavy.
- **Nesouhlasí** → načti výpis znovu (mezitím mohl někdo issue přidat nebo
  zavřít). Nesouhlasí-li ani podruhé, **ohlas rozpor a nezavírej**. Zavírat na
  datech, kterým nevěříš, je horší než nezavřít.

Podle stavů:

- **Nějaké issue je otevřené** → vypiš otevřená issues (číslo + název) a skonči.
  Nezavírej. Tohle je hlavní důvod, proč skill existuje.
- **Milestone nemá jediné issue** → **nezavírej tiše.** Obvykle to znamená, že
  se issues nikdy nezaložily, ne že je práce hotová. Řekni to a nástrojem
  AskUserQuestion si nech potvrdit, že se má i tak zavřít. Potvrdí-li uživatel,
  přeskoč krok 3 — integrační PR nemá pro co vzniknout — a jdi rovnou na krok 4.
- **Všechna zavřená a je jich aspoň jedno** → pokračuj krokem 3.

### 3. Kontrola 2 — integrační PR je zmergovaný

Integrační PR dohledej receptem „Vypiš PR milestonu", stav `all`. `run-milestone`
přiřazuje PR milestone hned po založení právě proto, aby se dal takhle najít.
Parametr milestonu je tu jiný než v kroku 2:

- **Gitea** → `list_pull_requests`, `milestone` jako **jedno číslo** (ne pole
  jako u `list_issues`).
- **GitHub** → `pr-list.sh --milestone "<název>" --state all`, tedy stejně jako
  u issues **název**, protože `gh pr list` filtruje vyhledávacím kvalifikátorem.

Stav `closed` sám o sobě **nerozlišuje** merge od zavření bez merge. Rozhodující
pole se liší podle forge a jiné pole na tohle rozhodnutí nepoužívej:

- **Gitea** → `merged` / `merged_at` z výpisu; nenese-li je, dočti PR receptem
  „Přečti PR".
- **GitHub** → `mergedAt` z výpisu (prázdné = nezmergováno), případně `state`
  `MERGED`. **Nerozhoduj podle `mergeable` ani `mergeStateStatus`** — ta říkají,
  jestli PR *jde* mergnout, ne jestli *byl* zmergovaný, a na otevřeném PR by
  vedla k předčasnému zavření milestonu. `pr-read.sh` merge příznak vůbec
  nevrací, takže na GitHubu ho jako fallback nevolej.

| Stav | Co s tím |
| --- | --- |
| Zmergovaný | Pokračuj krokem 4 |
| Otevřený | Dej odkaz a **nezavírej** — čeká se na člověka, merge do výchozí větve nedělá skill |
| Zavřený bez merge | Anomálie. Popiš, co jsi našel, a vynes to na uživatele; sám nerozhoduj |

**Nenajdeš-li žádné PR s vazbou na milestone, nevyvozuj z toho, že šlo o ad hoc
milestone bez integrace.** Stejně vypadá i milestone dokončený dřív, než tohle
přiřazování vzniklo. Zopakuj tedy tentýž recept **bez filtru na milestone**
(stav dál `all`) a vyber z výpisu PR, jehož cílová větev je výchozí větev
z konfigurace a zároveň platí aspoň jedno:

- jeho zdrojová větev je `milestone/<slug>` daného milestonu, nebo
- jeho název obsahuje název milestonu.

Na GitHubu jsou to pole `baseRefName`, `headRefName` a `title` z výpisu.

Ať už takové PR najdeš, nebo ne, **krok 4 odsud sám nespouštěj**: shoda podle
názvu je silná indicie, ne důkaz, a rozhodnutí nad indicií nepatří skillu.
Ohlas, co jsi našel a podle čeho, a nech potvrdit nástrojem AskUserQuestion —
u nezmergovaného kandidáta se neptej vůbec a zastav se jako u řádku „Otevřený"
nebo „Zavřený bez merge" výše. Nenajdeš-li nic, popiš, kde jsi hledal, a nech
rozhodnout uživatele.

### 4. Zavři milestone

Jedno volání podle receptu „Zavři milestone" — na Gitea `milestone_write` →
`update` s `id`, na GitHubu `milestone-update.sh -R <owner/repo> <číslo>
--state closed`. Pozor, tady se předává **číslo**, kdežto výpisy v krocích 2 a 3
braly na GitHubu název; proto sis v kroku 1 zapamatoval obojí.

**Nepokládej před voláním další potvrzovací otázku:** uživatel skill zavolal
jménem, obě kontroly prošly a zavření se jedním voláním vrací zpátky. Ptát se
znovu jen přidává klikání.

Selže-li volání, nepokoušej se o obchvat:

- **404 na Gitea** → skoro vždy chybějící oprávnění účtu, pod kterým MCP běží.
  Ověř podle sekce s nástrahami v receptech a nezkoušej jiný repozitář.
- **Kód `7` u `gh` skriptu** → chybí nebo není přihlášené `gh`; řekni to
  uživateli doslova.
- **Jiné selhání** → ohlas doslova, co volání vrátilo. Milestone zůstává
  otevřený, což je bezpečný stav.

### 5. Ohlas výsledek

Krátké hlášení podle Formátu výstupu, ne formální dokument. Výpisy z trackeru
do odpovědi nepřepisuj — z otevřených issues stačí čísla a názvy.

## Formát výstupu

Vyber variantu podle toho, jak běh dopadl. Pro konce, které tu nejsou (argument
nesedí na žádný milestone, nejednoznačný argument, selhání volání), napiš jednu
větu ve stejném duchu: co se stalo a že se **nezavíralo**.

```
Milestone <název> zavřen. <N> issues, všechna zavřená; integrační PR #<n> zmergován.
```

```
Milestone <název> zavřen na potvrzení uživatele — nemá jediné issue, integrační
PR se nedohledával.
```

```
Nezavírám: <N> otevřených issues.

- #<číslo> <název>
- #<číslo> <název>
```

```
Nezavírám: integrační PR #<n> <je otevřené | nemá merge> — <url>.
<Jedna věta, co se čeká: merge do výchozí větve dělá člověk. | Popis anomálie.>
```

```
Nezavírám: integrační PR se nepodařilo dohledat. Hledáno podle vazby na milestone
a mezi PR do <výchozí větev> podle větve `milestone/<slug>` a názvu.
<Nalezený kandidát #<n> a podle čeho, nebo „žádný kandidát".>
```

```
Nezavírám: počty nesedí. Ve výpisu <N> issues, milestone hlásí <O> otevřených
a <C> zavřených. Načteno dvakrát se stejným rozporem.
```

```
Milestone <název> je už zavřený. Nic k udělání.
```

## Zásady

- **Při pochybnosti nezavírej.** Nesouhlasící počty, nedohledatelné PR i
  nejednoznačný argument končí hlášením nebo otázkou, ne akcí. Zavřený milestone
  nikdo znovu nekontroluje.
- **Nad indicií rozhoduje uživatel, ne skill.** Jediné, co skill uzavírá sám, je
  případ, kdy obě kontroly prošly na tvrdých datech z trackeru.
- **Do výchozí větve skill nemergeuje a merge nečeká vynutit.** Otevřené
  integrační PR je legitimní stav, ve kterém se čeká na člověka.
- **Skill nezavírá issues.** Otevřené issue je důvod skončit, ne úkol k dodělání.
- **Volání ber z receptů, včetně sekce s nástrahami.** Filtr na typ „issues",
  stránkování a tvar parametru milestonu — na Gitea `milestones` jako pole
  a `milestone` jako číslo, na GitHubu název u výpisů a číslo u zavření — jsou
  přesně ta místa, kde chybný odhad projde bez chybové hlášky a s nesprávným
  výsledkem.
- **Sdílený kontrakt má přednost.** Odporuje-li tenhle postup konfiguraci nebo
  receptům, platí ony.
