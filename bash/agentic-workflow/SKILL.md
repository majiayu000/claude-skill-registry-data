---
name: sagittaras
description: >-
  Rozcestník pluginu sagittaras — řekne, co plugin nabízí, a podle rozdělané
  práce navede na skill, který ji umí dokončit, včetně obvyklého zřetězení.
  Přehled sestavuje z frontmatterů nainstalovaných skillů, ne z pevného výčtu.
  Sám nic nemění a doporučený skill nespouští.
when_to_use: >-
  Použij, když se uživatel ptá, co plugin sagittaras umí nebo kudy do něj —
  „co tady můžu použít", „co ten plugin nabízí", „jak s tímhle začít" —
  typicky přes /sagittaras. Nepoužívej místo konkrétního skillu: patří-li práce
  některému z nich, sáhni rovnou po něm a rozcestník přeskoč. Na aktualizaci
  pluginu je update-plugin, na první instalaci README.md v kořeni pluginu.
argument-hint: "[co potřebuješ udělat]"
model: sonnet
effort: medium
# Zařazení dle matice: ohraničené zadání se známým tvarem výstupu → sonnet ×
# medium (bod 2 rozhodovacího stromu). Nikoli haiku: napárovat rozdělanou práci
# na správný skill je úsudek, ne klasifikace, a chybné nasměrování stojí
# uživatele celé kolo. Nikoli výš: skill přečte pár frontmatterů a odpoví,
# nic nedeleguje ani neřídí.
# Odchylka od konvence pojmenování: název není ve tvaru <činnost>-<předmět>
# a opakuje název pluginu. Obojí je vynucené vstupním bodem — `name` se musí
# shodovat s názvem pluginu, jinak se rozcestník přestane volat `/sagittaras`,
# což si uživatel vymínil. Kostru ze skill-template.md skill drží celou,
# jen bez procedurálního jádra — šablona míří na skilly, které něco vykonávají,
# tenhle končí doporučením. Strukturu proto nerozvolňuj.
user-invocable: true
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
# disable-model-invocation je tu podstatné: root skill s obecným popisem by se
# jinak modelu načítal při každé zmínce o pluginu, aniž by ho kdo volal.
# Vynechaná zvažovaná pole: Grep — postup čte frontmattery všech skillů a na to
# je nepoužitelný, u víceřádkových hodnot vrátí jen první řádek; Write/Edit —
# rozcestník nic nemění; AskUserQuestion — odpovídá do konverzace a uživatel
# reaguje sám, doptávání by přidalo kolo navíc;
# Skill — doporučený skill zásadně nespouští (viz Zásady); Bash — nespouští
# příkazy, stav repozitáře si zjistí až doporučený skill; context/agent/
# background — výstup čte člověk v hlavním kontextu, fork ani běh na pozadí
# nemá komu odpovědět; paths — spouští se z konverzace, ne prací nad soubory;
# shell — nic nespouští; disallowed-tools — allowed-tools je uzavřený výčet,
# není co zakazovat navíc; version/license — verzuje se celý plugin, ne
# jednotlivý skill.
---

# Sagittaras

Cílem je, aby člověk, který plugin nezná nebo si nepamatuje, co v něm je, odešel
s jednou konkrétní odpovědí: který skill jeho situaci řeší a co po něm následuje.
Rozcestník sám nic nevykonává — končí doporučením, ne prací.

Zdrojem pravdy o tom, co plugin umí, jsou **frontmattery skillů na disku**, ne
tento text. Při rozporu platí ony.

## Vstupní kontext

- Zadání od uživatele (může být prázdné): $ARGUMENTS

Prázdné zadání znamená obecné „co tu je" — odpověz přehledem. Konkrétní zadání
ber jako popis rozdělané práce a odpověz doporučením; přehled v takovém případě
nevypisuj, uživatel se ptal na svou situaci, ne na katalog. Výjimkou je zadání,
které nesedí na žádný skill — tam přehled patří, viz Formát výstupu.

## Postup

### 1. Sestav aktuální seznam skillů

Nástrojem Glob najdi `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md` a z každého
souboru si vezmi **jen frontmatter** — Readem s `limit: 60`, což na frontmatter
i s komentáři stačí. Zajímají tě `name`, `description` a `when_to_use`.
Nenajdeš-li do 60 řádků uzavírací `---`, dočti zbytek dalším Readem; useknutý
`when_to_use` by tiše ochudil doporučení o spouštěcí situace.

**Těla skillů nečti.** Mají dvě stě řádků instrukcí, které na doporučení nemají
vliv a jen zaplní kontext.

**Seznam nikdy nevypisuj z hlavy.** Plugin se rozrůstá a zastaralý výčet pošle
uživatele za skillem, který neexistuje, nebo zamlčí ten, který zrovna potřebuje.

Nenajdeš-li ani jeden skill, ohlas to jako poškozenou instalaci a odkaž na
`README.md` v kořeni pluginu — dál nepokračuj, doporučovat nemáš z čeho.

### 2. Urči, co uživatel potřebuje

Ze zadání a z konverzace odvoď, v jaké fázi práce uživatel je. Rozhoduj podle
`when_to_use`, ne podle názvu skillu — název je zkratka, spouštěcí situace jsou
právě v tomhle poli.

Nesedí-li zadání na žádný skill, řekni to rovnou. Vnucené doporučení je horší
než žádné: uživatel podle něj spustí skill, který jeho práci neumí, a zjistí to
až uprostřed.

### 3. Odpověz

Drž se Formátu výstupu níže.

**Skilly uváděj s namespace** — `/sagittaras:make-commit`, ne `/make-commit`.
Bez prefixu se uživatel v katalogu, kde je pluginů víc, nemusí trefit do toho
správného. Výjimkou je rozcestník sám: ten je `/sagittaras`.

U doporučení vždy uveď, **proč** zrovna tenhle skill, a co po něm následuje —
plugin je stavěný na zřetězení, takže izolované doporučení zamlčí půlku postupu.
Navazující krok neber z paměti, plyne z `when_to_use` sousedů — jednak z vět
o řetězení („jako závěrečný krok jiné úlohy…", „spouští tě write-skill…"),
jednak z negativního vymezení čteného z druhé strany: „Nepoužívej pro zápis
hotové práce, na to slouží make-commit" u `create-branch` znamená, že nástupcem
je `make-commit`. Dvojice `create-branch` → práce → `make-commit` je ilustrace,
ne úplný seznam.

**Aktualizaci neodbývej odkazem na README** — na tu je `/sagittaras:update-plugin`
a doporuč ho stejně jako kterýkoli jiný skill. Do `README.md` v kořeni pluginu
posílej jen první instalaci a odinstalaci; ty skill neumí.

## Formát výstupu

**Přehled** (prázdné zadání) — skilly seskup podle toho, k čemu slouží, ne
abecedně:

```
Plugin sagittaras nabízí [počet] skillů:

**[Název skupiny — např. Práce s gitem]**
- `/sagittaras:[název]` — [co udělá, jednou větou vlastními slovy, ne citace description]

**[Název další skupiny]**
- `/sagittaras:[název]` — [co udělá, jednou větou vlastními slovy, ne citace description]

[Jedna věta o obvyklém zřetězení.]
[První instalace a odinstalace → odkaz na README.md.]
```

**Doporučení** (konkrétní zadání):

```
Na tohle je `/sagittaras:[název]` — [proč sedí, s odkazem na situaci uživatele].

[Co skill udělá, v jednom až dvou bodech: vstup, výstup, kde se ptá.]

Navazuje: [následující skill v řetězci, nebo „nic, tímhle to končí".]
```

**Žádná shoda** (zadání nesedí na žádný skill) — nekonči konstatováním, uživatel
by zůstal stát:

```
Na [shrnutí zadání] tu skill není. [Co s tím: nejbližší skill a v čem se míjí,
nebo že jde o běžnou práci bez skillu.]

[Přehled podle šablony výše — u této větve ho připoj vždy.]
```

**Poškozená instalace** (krok 1 nenašel žádný skill):

```
V `[cesta]/skills/` nevidím žádný skill — instalace pluginu je nekompletní.
Postup nápravy je v `README.md` v kořeni pluginu.
```

## Zásady

- **Doporučený skill nespouštěj.** Rozhodnutí patří uživateli a mezikrok, kde
  může říct ne, je jediná brzda před skillem, který sahá na repozitář.
- **Seznam skillů vždy z disku.** Výčet z paměti zastará první přidaným skillem
  a pozná se to až selháním.
- **První instalace patří README.** Rozcestník řeší orientaci uvnitř session, ne
  nasazení pluginu; dvojí popis instalace se rozejde. Aktualizace je výjimka —
  tu umí `/sagittaras:update-plugin` a patří do doporučení jako každý jiný skill.
- **Necituj `description` doslova.** Přeformuluj to k situaci uživatele —
  odříkaný katalog mu neřekne víc než výpis skillů, který už vidí.
