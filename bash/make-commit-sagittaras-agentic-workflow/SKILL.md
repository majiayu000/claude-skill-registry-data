---
name: make-commit
description: >-
  Zapíše rozdělanou práci jako commit podle Conventional Commits — zjistí stav
  repozitáře, rozdělí změny do logických celků, sestaví zprávu z diffu
  a commitne; hotový commit rovnou pushne, a nemá-li větev upstream, publikuje
  ji. Vynechá to jen tehdy, když si to uživatel vymíní. Všechny operace nad
  gitem provádí přes připravené skripty, které neumí přepsat historii.
when_to_use: >-
  Použij, když má uživatel rozdělanou práci k zapsání — „commitni to",
  „udělej commit", „zapiš změny", „commitni a pushni" — nebo jako závěrečný
  krok jiné úlohy, která něco změnila v pracovním stromu. Nepoužívej pro
  operace přepisující historii (amend, rebase, force push), ty skill záměrně
  neumí; ani pro zakládání větve, na to slouží create-branch.
argument-hint: "[rozsah nebo popis změny]"
model: sonnet
effort: medium
# Zařazení dle matice: rutinní tvorba podle jasného zadání → sonnet × medium.
# Matice u medium varuje před rozhodnutími, která se těžko vrací zpět — commit
# a jeho push takové jsou. Zůstáváme přesto na medium, protože nevratnost tu
# nesnižuje kvalita úsudku, ale absence brzdy: proti ní stojí zastavení na
# výchozí větvi (krok 1) a fakt, že publikace míří na vlastní pracovní větev,
# kde nikomu nepřekáží — rozdělení do commitů si skill určuje sám z diffu.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - "Bash(bash:*)"
# Bash je zúžený na spouštění skriptů; git se nikdy nevolá přímo (viz Zásady).
# Proto každé volání píš ve tvaru `bash <cesta>` — jinak nespadne do povolení.
# Užší vzor by musel spoléhat na tvar cesty ke skriptu, což je křehčí.
# Vynechaná zvažovaná pole: disable-model-invocation — automatické dokončení
# úlohy commitem je žádoucí a brzdou je krok 1 (zastavení na výchozí větvi),
# ne zákaz vyvolání;
# Write/Edit — skill nezapisuje soubory, zpráva jde do gitu stdinem;
# context/agent/background — skill pracuje nad sdíleným pracovním stromem
# volajícího a fork by ho rozbil; paths —
# spouští se z konverzace, ne prací nad konkrétními soubory; shell — skripty
# se spouští explicitním `bash`; disallowed-tools — allowed-tools je uzavřený
# výčet, není co zakazovat navíc.
---

# Make Commit

Cílem je jednotná, strojově čitelná historie. Závazný formát zprávy drží
`${CLAUDE_PLUGIN_ROOT}/skills/make-commit/conventional-commits.md`; přečti si ho,
než začneš psát první zprávu.

Veškerá práce s gitem jde přes skripty. Důvod není pohodlí, ale předvídatelnost:
skripty mají ošetřené hraniční stavy (odpojená HEAD, zastaralý lokální ref na
výchozí větev, chybějící upstream) a neumí operace, které přepisují historii.
Příkaz `git` proto nevolej přímo, ani když se to zdá rychlejší.

## Skripty

Cesty ke skriptům **i k doprovodné referenci** jsou ukotvené
k `${CLAUDE_PLUGIN_ROOT}`, protože plugin může běžet nad cizím projektem, kde
relativní `scripts/…` ani `conventional-commits.md` neexistují. Skripty volej
vždy tvarem `bash <cesta>` — bez toho nespadnou do zúžení v `allowed-tools`.

| Skript | Co dělá |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/preflight.sh` | Stav repozitáře jako `key=value`, výpis změn a zavedené scopy |
| `${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/show-diff.sh` | Staged diff; s `--worktree` vše necommitnuté proti HEAD |
| `${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/commit.sh` | Stagne zadané cesty a commitne se zprávou ze stdinu |
| `${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/push.sh` | Pushne větev; nemá-li upstream, publikuje ji na `origin` |

Každý skript má v hlavičce popis použití a návratových kódů. Nenulový kód vždy
vyhodnoť — `nothing_staged` znamená jiný postup než `detached_head`.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

Zadání ber jako vodítko pro `type`, `scope` a rozdělení do celků. O obsahu
zprávy ale rozhoduje diff, ne zadání.

**Interaktivní, nebo ne?** Nehádej to z toho, kdo tě spustil — automatické
spuštění na konci jiné úlohy ještě neznamená, že uživatel není k dispozici.
Za neinteraktivní běh považuj situaci, kdy **volání AskUserQuestion selže nebo
odpověď nedorazí**; teprve pak platí neinteraktivní varianty níže.

## Postup

### 1. Zjisti stav

Spusť `bash "${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/preflight.sh"`
a vyhodnoť výstup:

- **`error=not_a_git_repository`** (kód 2) → ohlas to a skonči.
- **`detached=true`** → zastav se a ohlas to. Commit na odpojené HEAD se tiše
  ztratí, jakmile se přepne větev.
- **`on_default_branch=true`** → zeptej se **nástrojem AskUserQuestion**, jestli
  má práce opravdu jít přímo do výchozí větve, nebo se má nejdřív založit nová —
  na to slouží skill `create-branch`, sám větve nezakládej. Neinteraktivně **necommituj**
  a jen ohlas, že změny leží na výchozí větvi a čekají na rozhodnutí; zápis
  do sdílené výchozí větve se špatně bere zpět, takže tady opatrnost vítězí
  nad plynulostí.
- **`on_default_branch=unknown`** (offline, `default_branch_source=unavailable`)
  → chovej se, jako bys na výchozí větvi byl.
- **`staged_count=0` i `unstaged_count=0` i `untracked_count=0`** → není co
  commitovat. Přeskoč rovnou na krok 5: větev může mít nepushnuté commity nebo
  vůbec žádný upstream a odejít odsud znamená nechat je ležet lokálně. Má-li
  upstream a předstih nula, je push levný no-op.

Ze sekce `[recent_scopes]` si vezmi slovník scopů, které repozitář už používá.

### 2. Urči rozsah

Je-li něco staged, commituj **výhradně to** — někdo ten výběr udělal vědomě
a rozšířit ho by znamenalo commitnout cizí práci.

Jinak projdi `[status]` z preflightu a rozděl změny do logických celků podle
oblasti a povahy změny. Smíchaný commit znehodnotí `type` i `scope`: změna,
která je zároveň `feat` i `fix` v jiné oblasti, nemá správnou zprávu.

Při přímém vyvolání uživatelem („commitni to") je rozsahem celý pracovní strom,
pokud uživatel sám nezúžil. Při automatickém spuštění na konci jiné úlohy vynech
změny, které s ní zjevně nesouvisejí — a vynechání ohlas.

**Víc celků → víc commitů.** Rozdělení urči a proveď sám podle vlastního návrhu,
bez čekání na potvrzení — a to i v interaktivním běhu. Návrh rozdělení do celků
i tak vypiš prostým textem (v postupu commitování nebo ve shrnutí), ať zůstane
vidět, jak byl diff rozdělen.

### 3. Napiš zprávu

Pro každý celek si nech vypsat diff:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/show-diff.sh" --worktree <cesty>
```

U staged výběru vynech `--worktree`, u většího rozsahu si diff vyžádej po
souborech. **Soubory ze sekce `[untracked]` si přečti nástrojem Read** — u
nesledovaných souborů diff obsah neukáže, a `type` i popis odvozený jen z názvu
souboru bývá vedle.

Zprávu piš **z diffu, ne z paměti konverzace**. Commituješ to, co je skutečně
v repu — včetně změn, o kterých konverzace nemluvila. Formát a pravidla drží
`${CLAUDE_PLUGIN_ROOT}/skills/make-commit/conventional-commits.md`, slovník scopů
`[recent_scopes]` z kroku 1.

### 4. Commitni

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/commit.sh" <cesty> <<'MSG'
<zpráva>
MSG
```

Zprávu předávej vždy takhle — heredocem s ukončovačem v uvozovkách. Bez uvozovek
by shell expandoval `$` a zpětné apostrofy a do historie by dorazilo něco jiného,
než jsi napsal. Je-li výběr už staged z kroku 2, cesty vynech.

Skript vrátí `commit=<hash>` a `subject=<popis>`. Odmítne-li commit hook, **ohlas
příčinu uživateli** — opravit ji sám nemůžeš, skill soubory needituje. Přeformátoval-li
hook soubory sám, stagni je znovu a commit zopakuj.

### 5. Pushni

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/make-commit/scripts/push.sh"
```

Pushni **po každém commitu**, ať už větev upstream má, nebo ne — v druhém
případě ji skript publikuje na `origin`. Čekat na zvláštní pokyn nemá o co
se opřít: commit, který zůstane jen lokálně, je ztracená práce při první ztrátě
pracovní kopie a `open-pr` nad ním nemá z čeho PR založit. Vlastní pracovní
větev na remotu nikomu nepřekáží — dokud není zmergovaná, nic v projektu nemění.

Push vynech **jen** tehdy, když ho uživatel odmítl — v konverzaci, nebo
v zadání od volajícího skillu. Vynechání pak ohlas ve shrnutí, ať se ví, že
commit leží jen lokálně.

Nenulový kód vyhodnoť:

- **`error=no_remote`** (kód 4) → repozitář nemá kam publikovat. Není to chyba
  skillu; ohlas, že commit zůstal lokálně, a remote sám nezakládej.
- **`error=detached_head`** (kód 2) → sem se běh po kroku 1 nedostane; dorazí-li
  přesto, zastav se a ohlas to.
- **Odmítnutý push** (zamítnuto remotem, chybějící oprávnění, mezitím posunutá
  větev) → ohlas příčinu. Nezkoušej ji obejít force pushem ani přepsáním
  historie; commit je zapsaný a push jde zopakovat, až bude příčina odstraněná.

### 6. Shrň výsledek

Pro každý commit uveď hash a popis, kam se pushlo (nebo proč ne), a co jsi
z rozsahu vynechal i s důvodem.

## Zásady

- **Git jen přes skripty.** Přímé volání `git` obchází ošetřené hraniční stavy,
  kvůli kterým skripty vznikly.
- **Historie se jen rozrůstá.** Žádný `--amend`, žádný force push, žádné
  přeskakování hooků. Skripty tyhle operace záměrně neumí — nesnaž se je obejít
  jinou cestou.
- **Zpráva se píše z diffu.** Konverzace je vodítko, diff je pravda.
- **Staged výběr je zadání**, ne návrh k rozšíření.
- **Commit nezůstává lokálně.** Push i publikace nové větve jsou výchozí konec
  práce, ne zvláštní krok na vyžádání. Zdrženlivost tu nic nechrání: pracovní
  větev na remotu do ničeho nezasahuje, kdežto commit jen v pracovní kopii se dá
  ztratit. Vynech push jen tehdy, když ho někdo výslovně odmítl.
