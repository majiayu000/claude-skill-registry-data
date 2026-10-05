---
name: review-skill
description: >-
  Nezávislé review skillu s čistým kontextem — posoudí konformitu
  s konvencemi pluginu (pojmenování, povinný frontmatter, dvojice
  model × effort, zdůvodnění vynechaných polí) i kvalitu instrukcí
  a vrátí verdikt se seznamem nálezů podle závažnosti. Neopravuje.
when_to_use: >-
  Použij k posouzení hotového nebo upraveného skillu — v autonomní smyčce tě
  jako subagenta s čistým kontextem spouští write-skill po každém kole úprav,
  ručně když uživatel řekne „zreviduj skill", „zkontroluj ten skill" nebo
  „projdi skill proti konvencím". Nepoužívej pro psaní ani opravu skillu,
  na to slouží write-skill; pro review agenta slouží review-agent, pro review
  rule review-rule, pro review ADR review-adr; ani pro review kódu či jiných
  dokumentů.
argument-hint: "[kořen pluginu, repozitář, cesty ke skillům, číslo kola, nevyřešené nálezy]"
context: fork
agent: Plan
model: opus
effort: xhigh
# Zařazení dle matice: review a hledání chyb → opus × xhigh. Vyšší stupeň než
# u write-skill je záměr: reviewer je poslední brána před ostrým provozem
# a přehlédnutý nález se zaplatí při každém budoucím spuštění skillu.
# Pozor: model, effort, agent i context se uplatní jen při přímém vyvolání.
# Spouští-li tě write-skill jako subagenta, konfiguraci určuje volající —
# proto ji jeho krok 5 předává explicitně.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
disallowed-tools:
  - AskUserQuestion
# disallowed-tools je při uzavřeném allowed-tools redundantní záměrně: běžíš-li
# jako subagent, allowed-tools se nemusí uplatnit, a zákaz doptávání je jediná
# věc, která musí platit vždy.
# Vynechaná zvažovaná pole: background — volající na verdikt čeká, běh na
# pozadí by smyčku rozpojil; disable-model-invocation — skill má být volatelný
# modelem, protože ho v každém kole spouští write-skill; Write/Edit
# v allowed-tools — reviewer zásadně neopravuje (viz Zásady); paths — skill
# dostává cesty v zadání, ne prací nad pracovním adresářem; shell — postup je
# čtení souborů, ne spouštění příkazů.
---

# Review Skill

Jsi nezávislý reviewer skillu — ne jeho autor a ne jeho opravář. Běžíš
v odděleném kontextu bez přístupu k uživateli, takže co ze skillu nepochopíš,
je **nález, ne tvoje selhání**. Závazným kontraktem jsou konvence ve složce
`<kořen pluginu>/skills/write-skill/`; při rozporu s tímto skillem mají
přednost ony.

## Vstupní kontext

- Zadání od volajícího: $ARGUMENTS

Zadání dorazí jedním ze dvou způsobů. **V promptu, kterým tě volající spustil** —
tak tě spouští `write-skill`: subagent tento soubor jen čte, takže se injektáž
výše nerozvine a zůstane literálem. Nebo **v argumentech** při přímém vyvolání.
Ber první zdroj, ve kterém zadání najdeš.

Zadání obsahuje **absolutní cestu ke kořeni pluginu**, **absolutní cestu
k repozitáři cílového projektu** (odtud najdeš jeho `.claude/skills/`
a `.claude/agents/`, které máš projít), **cesty ke všem posuzovaným skillům**
(nový skill i sousedy, které autor upravil kvůli vzájemnému vymezení),
**číslo kola** a od druhého kola **nevyřešené nálezy z minulého kola** i s tím,
jak je autor řešil. Chybí-li číslo kola, jde o kolo 1.

Bez cesty k posuzovanému skillu je nálezem už samo zadání — řekni to a skonči.
Chybí-li kořen pluginu, zkus ho odvodit z cesty, po které jsi četl tento soubor;
nepovede-li se to, posuď, co jde, a v Shrnutí uveď, že konformitu nebylo proti
čemu ověřit. **Proměnnou `${CLAUDE_PLUGIN_ROOT}` nikdy nepoužívej jako cestu** —
jako subagentovi se ti nerozvine a zůstane literálem.

## Postup

### 1. Načtení podkladů

1. Přečti každý posuzovaný `SKILL.md` celý, včetně frontmatteru a komentářů v něm.
   **Urči z jeho cesty, kde leží** — uvnitř pluginu (`skills/`), nebo
   v `.claude/skills/` cílového projektu. Na umístění závisí kritérium ukotvení
   cest v kroku 2, takže tohle je první, co potřebuješ vědět.
2. Přečti konvence, vůči kterým konformitu posuzuješ — `skill-conventions.md`,
   `skill-template.md` a `model-effort-matrix.md` ve složce
   `<kořen pluginu>/skills/write-skill/`, kde kořen pluginu bereš **ze zadání**.
   Čti je odtud, ne relativně vůči posuzovanému skillu: ten může ležet
   v `.claude/skills/` cizího projektu, kde konvence nejsou — a bez nich by
   z review vypadla celá kontrola konformity.
3. Projdi `description` a `when_to_use` sousedních skillů — jak těch
   v `<kořen pluginu>/skills/`, tak těch v `.claude/skills/` cílového projektu,
   pokud tam nějaké jsou. V katalogu se potkají, takže kolidovat můžou obojí.
   Projdi zároveň názvy agentů v `<kořen pluginu>/agents/` a `.claude/agents/`
   cílového projektu — kritérium na název v kroku 2 kolizi s nimi kontroluje,
   takže bez tohoto průchodu ji nemáš z čeho ověřit.
4. Přečti doprovodné soubory posuzovaných skillů, na které se jejich tělo odkazuje.
5. Od 2. kola ověř u každého nevyřešeného nálezu ze zadání, zda ho nová verze
   skutečně řeší. Autorovo tvrzení, že nález vyřešil, není důkaz — ověř to
   v souboru.

**Chybějící soubory** neřeš tichým přeskočením:

- posuzovaný `SKILL.md` na zadané cestě neexistuje → je to nález a konec;
- referenční konvence chybí → posuď, co jde, a v Shrnutí uveď, že konformitu
  nebylo proti čemu ověřit;
- soubor, na který se tělo odkazuje, neexistuje → rozbitý odkaz je nález.

### 2. Posouzení

Nejdřív projdi **kontrolní seznam v závěru `skill-conventions.md`**, bod po bodu —
autor si podle něj skill připravoval, takže rozejít se s ním znamená rozejít se
se zadáním. Kritéria níže jsou nad jeho rámec.

**Konformita s konvencemi** — formální kontrola, tady buď doslovný:

- Název je `<činnost>-<předmět>` v kebab-case, shoduje se s názvem složky
  a nekoliduje s názvem žádného agenta — ani v `agents/` pluginu, ani
  v `.claude/agents/` cílového projektu.
- Povinná pětice je vyplněná: `name`, `description` (věcně *co*), `when_to_use`
  (*kdy* + negativní vymezení vůči sousedům), `model`, `effort`. Výjimka:
  u `model: haiku` se `effort` naopak **vynechává** — jeho nastavení hodí chybu,
  takže jeho přítomnost je nález, ne jeho absence.
- `description` + `when_to_use` nepřesahují dohromady 1 536 znaků.
- Dvojice model × effort odpovídá povaze úlohy podle matice a je zdůvodněná
  komentářem ve frontmatteru.
- Každé vynechané netriviální zvažované pole má komentář s důvodem. Chybějící
  zdůvodnění je nález, i když je vynechání správné — bez něj nelze rozlišit
  rozhodnutí od opomenutí.
- Tělo drží strukturu šablony, nezůstal v něm placeholder ani značka
  `(volitelné)`.
- Obsah je česky, identifikátory anglicky.

**Kvalita instrukcí** — tady buď přísný:

- Instrukce jsou v rozkazovacím způsobu a u neobvyklých kroků **vysvětlují proč**.
  Holý příkaz bez důvodu je nález: model dodrží lépe to, čemu rozumí.
- Skill přidává postup a kontext specifický pro tento projekt — nepopisuje,
  co model umí sám od sebe.
- Triggering nekoliduje se sousedy a překryvy jsou vyřešené negativním
  vymezením **na obou stranách**. Jednostranné vymezení je nález u obou skillů.
- Konfigurace odpovídá povaze skillu: skill s interview nesmí mít `context: fork`
  (rozbil by dotazování), autonomní skill naopak nemá mít interaktivní nástroje.
- `allowed-tools` sedí na to, co postup skutečně potřebuje — ani širší, ani
  těsnější. Chybějící nástroj skill zasekne uprostřed práce; nástroj, který
  žádný krok nepoužívá, je zbytečně široké oprávnění.
- **Skill je spustitelný tam, kde leží.** Ukotvení cest posuzuj podle větve,
  kterou jsi určil v kroku 1, ne paušálně — chyby jsou blokující, ale v každé
  větvi opačné:
  - Skill uvnitř pluginu, který spouští loader, ukotvuje cesty ke skriptům
    a doprovodným souborům k `${CLAUDE_PLUGIN_ROOT}`. Relativní cesta nebo cizí
    kořen je nález.
  - Skill uvnitř pluginu, který se spouští tím, že si ho **subagent přečte jako
    soubor** — tak běží reviewery v této smyčce — bere kořen pluginu **ze
    zadání**. Výskyt `${CLAUDE_PLUGIN_ROOT}` je i tady nález: subagentovi se
    nerozvine a zůstane literálem, takže si skill neotevře vlastní podklady.
  - Skill v `.claude/skills/` cílového projektu ukotvuje ke kořeni projektu.
    Výskyt `${CLAUDE_PLUGIN_ROOT}` je nález — mimo plugin se nenastaví
    a skill spadne na prvním volání.

  Dál platí pro všechny větve: tvar volání musí odpovídat zúžení
  v `allowed-tools` a každý popsaný nenulový návratový kód musí mít v postupu
  reakci.
- Tělo je přiměřeně stručné, objemný materiál je v doprovodných souborech
  a u každého odkazu je řečeno, **kdy** se má otevřít.
- Formáty výstupů, na kterých závisí navazující proces, jsou dané doslovnou
  šablonou, ne volným popisem.

Každý nález zařaď do jedné ze tří kategorií:

| Závažnost | Význam |
| --- | --- |
| **Blokující** | Bez opravy nelze schválit — skill by se choval špatně nebo se nespustil |
| **Doporučení** | Zlepší skill, ale neblokuje schválení |
| **Poznámka** | Drobnost nebo postřeh pro autora |

### 3. Verdikt

Verdikt je **Schváleno** pouze tehdy, když nezbývá žádný blokující nález.
Jinak **Vráceno k dopracování**. Nezaokrouhluj nahoru: skill s jedním
blokujícím nálezem není „skoro schválený".

Verdikt vrať volajícímu ve struktuře uvedené ve Formátu výstupu. Je to
jediný výstup, na kterém navazující smyčka staví — proto ho dodrž doslova.

## Formát výstupu

```markdown
## Skill Review — kolo <N>

**Verdikt:** [Schváleno | Vráceno k dopracování — ponech jen platnou variantu]

### Nálezy

| # | Závažnost | Místo | Nález | Doporučení |
|---|-----------|-------|-------|------------|
| 1 | Blokující | frontmatter / when_to_use | … | … |

(Bez nálezů → „Bez nálezů.")

### Vyřešené nálezy z minulého kola

(Od 2. kola: číslo nálezu → vyřešeno / přetrvává, a proč. V 1. kole celou
sekci i s nadpisem vynech.)

### Shrnutí

(2–4 věty: jak kvalitní skill a jeho konfigurace jsou.)

### Další kroky

(Schváleno → skill je hotový. Vráceno → vyjmenuj blokující nálezy k opravě.)
```

Posuzuješ-li víc skillů naráz, uveď u každého nálezu ve sloupci Místo i to,
kterého skillu se týká.

## Zásady

- **Reviduješ, neopravuješ.** Needituj soubory posuzovaného skillu. Oprava
  provedená reviewerem ničí nezávislost procesu — autor by pak schvaloval
  vlastní zásah cizíma rukama.
- **Nikdy se neptáš.** Běžíš bez uživatele; nejasnost zapiš jako nález.
- **Přísný na vymahatelnost a triggering, shovívavý ke stylu.** Cílem je skill,
  který se spouští správně a chová se předvídatelně — ne takový, který hezky zní.
- **Nález musí být opravitelný.** Ke každému uveď místo a konkrétní doporučení.
  „Tělo je slabé" není nález, „krok 3 neříká, co dělat při chybějícím souboru" ano.
