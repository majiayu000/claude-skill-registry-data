---
name: section
description: Använd när du bygger en ny sektion/fullbreddsblock i en sidlayout, inklusive My Pages sidtitel-spacing (main-content/page-preamble) — padding per brytpunkt, bakgrund (Surface Raised Primary/Secondary), page divider och use case för nollad padding.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Section (ECO Design System)

En section är ett modulärt och återanvändbart fullbreddsblock som representerar en distinkt del av en sidlayout. Den används för att dela upp innehåll i tydliga sektioner med automatiskt justerade padding-värden per breakpoint.

### Anatomi

1. **Section padding – Top**
2. **Section padding – Bottom**
3. **Surface** – bakgrundsfärg: `Surface Raised Primary` (`#ffffff`) eller `Surface Raised Secondary` (`#f6f6f6`)
4. **Content container** – innehållsytan inuti sektionen

### Padding per breakpoint

Padding justeras automatiskt beroende på aktuell breakpoint.

#### Första sektionen (first section)

Den första sektionen på en sida använder lägre top-padding.

| Breakpoint | Top (px) | Bottom (px) |
|---|---|---|
| `breakpoint-xs` | 16 | 40 |
| `breakpoint-sm` | 32 | 48 |
| `breakpoint-md` | 32 | 64 |
| `breakpoint-lg` | 40 | 80 |
| `breakpoint-xl` | 48 | 80 |

#### Övriga sektioner

Dessa värden gäller alla sektioner utom den första.

| Breakpoint | Top (px) | Bottom (px) |
|---|---|---|
| `breakpoint-xs` | 32 | 40 |
| `breakpoint-sm` | 48 | 48 |
| `breakpoint-md` | 56 | 64 |
| `breakpoint-lg` | 72 | 80 |
| `breakpoint-xl` | 72 | 80 |

### CSS-mall

```css
/* Övriga sektioner */
.section {
  padding-top: 32px;    /* xs */
  padding-bottom: 40px; /* xs */
}

/* Första sektionen */
.section:first-of-type,
.section--first {
  padding-top: 16px;    /* xs */
  padding-bottom: 40px; /* xs */
}

@media (min-width: 640px) {  /* sm */
  .section { padding-top: 48px; padding-bottom: 48px; }
  .section--first { padding-top: 32px; padding-bottom: 48px; }
}

@media (min-width: 769px) {  /* md */
  .section { padding-top: 56px; padding-bottom: 64px; }
  .section--first { padding-top: 32px; padding-bottom: 64px; }
}

@media (min-width: 1024px) { /* lg */
  .section { padding-top: 72px; padding-bottom: 80px; }
  .section--first { padding-top: 48px; padding-bottom: 80px; }
}

@media (min-width: 1281px) { /* xl */
  .section { padding-top: 72px; padding-bottom: 80px; }
  .section--first { padding-top: 48px; padding-bottom: 80px; }
}
```

### Bakgrundsfärg

Standardfärgen för sektioner är vit (`surface-raised-primary`, `#ffffff`). En layout eller sida bör som tumregel börja med en vit sektion, eller ha vitt som enda bakgrundsfärg — detta skapar en stabil struktur och god konsekvens.

> Undantag finns, t.ex. PLP-sidan och My Pages.

Genom att etablera `background-primary` som basens färg i UI:t skapas en ren och sober känsla, och det blir tydligare när en grå `surface-raised-secondary`-sektion används.

### Paddinganvändning

Padding-switchen bör normalt alltid vara påslagen. Sektionens inbyggda padding skapar det vita utrymme som behövs för att dela upp innehåll i en sidlayout.

Det går att använda sektioner **utan** inbyggd padding och låta innehållet i sig fungera som avdelare — använd detta med försiktighet och med tydligt syfte.

### Use cases – nollad padding

5 fall där sektionens padding stängs av:

1. **Avdelare inuti sektion** – Använd en divider-komponent inuti en sektion med noll top & bottom-padding i sektioner med samma bakgrundsfärg, när du inte vill markera en tydlig separation men ändå ge innehållet sektionens padding-värden.

2. **Angränsande ämne med mellanliggande sektion** – Använd sektionen med noll bottom & top-padding när innehållet i två sektioner behandlar samma ämne, men du vill placera en stor semi-topic-sektion däremellan för cross-sell eller produktplacering.

3. **Fluid hero banner** – Använd sektionen med noll top & bottom-padding som behållare för en fluid hero banner som marknadsför nya produkter eller relaterade kampanjer.

4. **Första sektionen med angränsande komponent med inbyggd spacing** – Använd den första sektionen med noll top-padding när innehållet börjar med en bild, rubrik eller textblock intill en komponent med inbyggd spacing, t.ex. en brödsmulerad sektion (breadcrumb).

5. **Första sektionen med fluid banner som förstaelement** – Använd den första sektionen med noll top & bottom-padding när layouten börjar med en fluid banner eller fullbreddsbild som första komponent.

### Regler

1. **Mobile-first** – skriv xs-padding utan prefix, bygg sedan upp med `sm:` → `md:` → `lg:` → `xl:`.
2. **Första sektionen** – använd klassen `.section--first` (eller `:first-of-type`) för reducerad top-padding.
3. **Surface** – välj alltid antingen `Surface Raised Primary` (`#ffffff`) eller `Surface Raised Secondary` (`#f6f6f6`) som bakgrund. Blanda aldrig andra bakgrundsfärger utan designgodkännande.
4. **Horisontell padding** – sektionens sidmarginaler följer breakpoint-marginalen definierad i grid-systemet (`16px` xs, `32px` sm/md, `40px` lg+). Använd `--px-full` eller `px-[16px] sm:px-[32px] lg:px-[40px]`.
5. **Nollad padding** – stäng av inbyggd padding enbart i de 5 definierade use-casen ovan. Använd aldrig nollad padding utan tydligt syfte.

### Page Divider

En tunn horisontell linje som skiljer två `.section`-block åt utan att markera en tydlig färgförändring — används **mellan** två sektioner (inte inuti en, se use case 1 ovan), typiskt när båda har samma bakgrundsfärg och en full sektionsgräns skulle kännas för kraftig. Egen `<div>`, inte en `<section>`.

```css
.page-divider { padding: 48px var(--px-full); }
.page-divider__line { height: 1px; background: var(--color-border-primary); }
```

```html
<div class="page-divider"><div class="page-divider__line"></div></div>
```

> `48px` toppadding/bottenpadding är standard när dividern ersätter en sektionsgräns rakt av (som i `mypages/users.html`, mellan `.fav-store-section` och `.contact-section`). Om dividern istället placeras **mellan två `.section`-block som redan har egen top-/bottom-padding** (t.ex. `.section.section--first` följt av nästa `.section`), nollställ `.page-divider`s egen padding (`padding: 0 var(--px-full);`) — annars staplas två luftmängder ovanpå varandra och det blir onödigt mycket tomrum.
>
> **Använd alltid `--px-full`, aldrig `--px-page`.** `--px-page` är enbart marginalvärdet (16/32/40px) och saknar `xl`-brytpunktens centrering mot `max-w: 1200px` — en divider byggd på `--px-page` fortsätter ut mot skärmkanten på breda skärmar istället för att sluta där sektionsinnehållet ovanför/under gör det. `--px-full` (`max(var(--px-page), calc((100vw - var(--max-w)) / 2))`) är samma token som `.section` redan använder, så linjen respekterar samma marginal och samma brytpunktsgräns som resten av sidan.

---

## My Pages – Page Title-sektion

Regler för spacing i page title-sektionen som **alltid** ska användas på My Pages-sidor.

### main-content – top padding

| Breakpoint | padding-top |
|---|---|
| `breakpoint-xs` | 24px |
| `breakpoint-sm` | 24px |
| `breakpoint-md`+ | 40px |

### page-preamble – margin-bottom

| Breakpoint | margin-bottom |
|---|---|
| `breakpoint-xs` | 24px |
| `breakpoint-sm` | 32px |
| `breakpoint-md`+ | 40px |

### CSS-mall

```css
.main-content {
  padding-top: 24px; /* xs + sm */
}

.page-preamble {
  margin-bottom: 24px; /* xs */
}

@media (min-width: 640px) { /* sm */
  .page-preamble { margin-bottom: 32px; }
}

@media (min-width: 769px) { /* md+ */
  .main-content { padding-top: 40px; }
  .page-preamble { margin-bottom: 40px; }
}
```

---
