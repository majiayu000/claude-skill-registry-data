---
name: update-plugin
description: >-
  Stáhne do nainstalovaného pluginu poslední stav větve, na které stojí,
  a vypíše, co se změnilo — které skilly přibyly, změnily se nebo zmizely. Poradí,
  jestli stačí reload, nebo je nutný restart. Reload sám nespouští, je to příkaz
  klienta. Upozorní, když práce ve vývojové kopii do instalace nedorazila.
when_to_use: >-
  Použij, když má uživatel dostat nejnovější verzi pluginu — „aktualizuj
  plugin", „stáhni nové skilly", „updatni sagittaras" — nebo jako závěrečný
  krok práce, která do pluginu něco pushla. Nepoužívej pro první instalaci,
  tu popisuje README.md v kořeni pluginu; ani pro zapsání a odeslání změn
  v pluginu, na to slouží make-commit.
model: sonnet
effort: medium
# Zařazení dle matice: ohraničené zadání se známým výsledkem → sonnet × medium
# (bod 2 rozhodovacího stromu). Nikoli low: skript rozlišuje čtyři stavy
# (poškozená instalace, cizí remote, lokální změny, nic ke stažení) a každý
# vede k jiné radě — to je přesně ta vícekrokovost, před kterou matice u low
# varuje. Nikoli výš: těžkou práci dělá skript, skill jeho výstup čte a překládá.
user-invocable: true
allowed-tools:
  - Read
  - "Bash(bash:*)"
# Bash je zúžený na spouštění skriptů; git se nikdy nevolá přímo (viz Zásady).
# Proto volání piš ve tvaru `bash <cesta>` — jinak nespadne do povolení.
# Vynechaná zvažovaná pole: argument-hint — skill nebere argumenty, aktualizuje
# vždy tu instalaci, ze které běží; disable-model-invocation — stažení je
# vratné (ff-only, bez přepisu historie) a skill má jít zřetězit za práci, která
# do pluginu pushla; AskUserQuestion — skill se nerozhoduje, jen stahuje
# a reportuje, a má běžet i tam, kde uživatel nečeká u klávesnice; Write/Edit —
# nic nezapisuje; Glob/Grep — vstupem je výstup skriptu, ne prohledávání
# souborů; context/agent/background — výsledek čte člověk v hlavním kontextu
# a navazuje na něj příkazem, který musí zadat sám; paths — spouští se
# z konverzace, ne prací nad soubory; shell — skript se spouští explicitním
# `bash`; disallowed-tools — allowed-tools je uzavřený výčet, není co zakazovat
# navíc; version/license — verzuje se celý plugin, ne jednotlivý skill.
---

# Update Plugin

Cílem je dostat instalaci na poslední stav větve, na které stojí, a hlavně
**říct, co se změnilo** — bez toho uživatel neví, jestli mu stačí reload, nebo
musí restartovat. Větev se nikdy nepřepíná; instalace pořízená z jiné větve
zůstane na ní.

Reload skill nespouští a spustit ho nemůže: `/reload-plugins` i `/reload-skills`
jsou příkazy klienta, ne spustitelné programy. Skill končí tím, že řekne, který
z nich zadat.

Závazným kontraktem jsou hlavičky skriptů — `scripts/update.sh` a `install.sh`
v kořeni pluginu. Popisují klíče výstupu i návratové kódy a při rozporu s tímto
textem platí ony. Narazíš-li ve výstupu na klíč nebo návratový kód, který kroky
2 a 3 neuvádějí, otevři hlavičku `scripts/update.sh` a řiď se jí — nedomýšlej
si význam.

## Postup

### 1. Stáhni změny

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-plugin/scripts/update.sh"
```

Skript sám nic nemerguje napřeskáčku — deleguje na `install.sh` v kořeni
pluginu, který ověří remote a udělá `merge --ff-only`. Git proto nevolej přímo
ani tehdy, když se to zdá rychlejší; obejdeš tím kontroly, kvůli kterým skript
vznikl.

Návratové kódy vyhodnoť dřív, než začneš cokoli hlásit:

| Kód | Co znamená | Co s tím |
| --- | --- | --- |
| 0 | Hotovo — i když nebylo co stáhnout | Pokračuj krokem 2 |
| 1 | Poškozená instalace (`error=installer_missing`, `error=not_a_git_installation`, `error=detached_head`) | Přečti `${CLAUDE_PLUGIN_ROOT}/README.md` a nabídni z něj konkrétní krok nápravy. Neodpovídá-li README na to, co se stalo, poraď sám: u `detached_head` stačí přepnout instalaci na větev a spustit skill znovu. Neopravuj to za uživatele |
| 2 | Cíl obsazený cizím obsahem nebo cizím remotem | Ohlas doslova, co skript vypsal na chybový výstup; úklid patří uživateli |
| jiný | Selhání propuštěné z gitu, typicky `128` u nedostupného remotu nebo chybějícího klíče | Ohlas doslova stderr; je to stav prostředí, ne něco, co má skill obcházet |

Rozhoduj **podle návratového kódu, ne podle klíče** — `error=update_failed`
uvozuje každé selhání propuštěné z `install.sh`, tedy i kód 2.

### 2. Přečti výstup

Skript píše `key=value` a sekce uvozené hlavičkou v `[]`. Klíče, na kterých
záleží:

| Klíč | Význam |
| --- | --- |
| `branch=` | Větev, na které instalace stojí a která se stahovala. Uvnitř `[dev_copy]` je jako `dev_branch=` větev vývojové kopie — nezaměň je |
| `install_dirty=true` | Instalace má necommitnuté změny, **stažení se přeskočilo** — ne že nebylo co stáhnout |
| `updated=false` | Instalace už byla na posledním stavu |
| `reason=branch_not_on_remote` | Instalace stojí na čistě lokální větvi — není odkud stahovat, což není chyba |
| `commits=N` | Kolik commitů přibylo |
| `[commits]` | Jejich `--oneline` výpis; čerpej z něj, když `[skills]` mlčí a je potřeba říct, co se tedy změnilo |
| `[skills]` | `added=`, `modified=`, `removed=` podle skillů; `(rozcestník)` je kořenový `SKILL.md` |
| `[files]` | Všechny změněné soubory, i mimo `skills/` |
| `[dev_copy]` | Zda stojíš v odděleném klonu téhož repozitáře, a co v něm zůstalo — `dev_branch`, `dirty`, `unpushed`, `unmerged`. Hodnoty `no_upstream` a `unknown` znamenají „nedalo se určit", ne „nic tam není" |

`install_dirty=true` nikdy nezaměňuj za „nic nového" — jsou to opačné situace
a uživatel v té první přijde o změny, které čeká.

### 3. Poraď, co dál

Větve ber v tomhle pořadí; první dvě se snadno zamění a záměna stojí uživatele
změny, na které čeká.

- **`install_dirty=true`** → řeš jako první, ještě před `updated`. Stažení se
  vůbec nespustilo, protože instalace má lokální změny. Ohlas to a řekni, že je
  potřeba je uložit nebo zahodit; teprve pak má smysl skill spustit znovu.
- **`reason=branch_not_on_remote`** → řekni, na které větvi instalace stojí
  (`branch=`) a že na ní není odkud stahovat. Není to porucha; instalace prostě
  sedí na větvi, která nikdy neodešla na remote.
- **`updated=false`** (a `install_dirty=false`) → neposílej uživatele nic mačkat.
  Reload bez změn na disku nic neudělá a jen ho zdrží.
- **`updated=true`** → doporuč `/reload-plugins`. Instalace běží jako plugin
  (`sagittaras@skills-dir`), takže plugin-level reload je ta správná úroveň;
  `/reload-skills` zmiň jako lehčí variantu.
- **`[skills]` obsahuje `added=` nebo `removed=`** → připoj, že po přibylém nebo
  zaniklém skillu je jistotou restart Claude Code. Reload je stavěný na změny
  na disku, ale u nově vzniklého skillu se na něj nespoléhej.
- **`[dev_copy] detected=true`** → varuj, jakmile platí **cokoli** z `dirty=true`,
  `unpushed` je `no_upstream` nebo větší než nula, `unmerged` je větší než nula
  nebo `unknown`. Instalace táhne jen svou větev z remotu, takže neuložená,
  neodeslaná i odeslaná ale nezamergovaná práce jsou pro ni stejně neviditelné.
  `no_upstream` je z nich ta nejjistější — větev nikdy nikam neodešla.
  **`unknown` ber jako důvod k varování, ne k mlčení**: znamená, že se nedala
  určit základna pro porovnání, a mlčet na nejistotu je tady horší chyba než
  varovat zbytečně. Vždy uveď, ve které větvi ta práce leží (`dev_branch=`).

`/reload-plugins` nefunguje v neinteraktivním běhu. Běžíš-li bez uživatele
u klávesnice, ohlas to jako čekající krok, ne jako hotovo.

## Formát výstupu

**Po úspěšné aktualizaci:**

```
Plugin aktualizován: [before] → [after] ([N] commitů).

Skilly: [výčet z [skills] přeložený do lidské řeči — co přibylo, co se změnilo,
co zmizelo. Když se skilly nezměnily, řekni to a uveď, co se změnilo místo nich.]

Aby se změny projevily: `/reload-plugins`
[Restart, jde-li o přibylý nebo zaniklý skill.]
[Varování o vývojové kopii, je-li na co upozornit.]
```

**Když nebylo co stáhnout:**

```
Instalace je aktuální ([after]). Nic ke stažení, reload není potřeba.
[Varování o vývojové kopii, je-li na co upozornit.]
```

**Když větev nemá protějšek na remotu** (`reason=branch_not_on_remote`):

```
Instalace stojí na větvi `[branch]`, která na remotu není — není odkud stahovat.
Není to porucha; přepni instalaci na sledovanou větev, pokud čekáš novinky.
[Varování o vývojové kopii, je-li na co upozornit.]
```

**Když se stažení přeskočilo nebo selhalo:**

```
Aktualizace neproběhla: [příčina — lokální změny v instalaci, cizí remote,
poškozená instalace].

[Co s tím: konkrétní krok pro uživatele, doslova to, co vypsal skript.]
```

## Zásady

- **Git jen přes skript.** Přímé volání `git` obchází ověření remotu a `ff-only`,
  kvůli kterým skript existuje.
- **Reload nespouštěj a nepředstírej.** Je to příkaz klienta; skill ho může jen
  doporučit. Hlásit „změny jsou aktivní" je nepravda, dokud ho uživatel nezadá.
- **Nic neopravuj.** Lokální změny v instalaci ani cizí remote skill neřeší —
  ohlásí je a skončí. Automatický úklid cizí složky je nevratný.
- **`install_dirty` a `updated=false` drž oddělené.** Splynou-li v reportu,
  uživatel uvěří, že je aktuální, zatímco stažení se vůbec nespustilo.
