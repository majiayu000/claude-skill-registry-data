---
name: role-tier-card
description: Använd när du bygger ett rollkort/tier card-par som introducerar två nivåer inom samma kategori (t.ex. Standard/Administratör) sida vid sida och länkar vidare ner till en fullständig jämförelsetabell.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Rollkort / Tier Card (ECO Design System)

Ett kortpar som presenterar två nivåer inom samma kategori (t.ex. en grundnivå och en utökad/administrativ nivå) sida vid sida, och länkar vidare ner till en detaljerad jämförelsetabell längre ner på sidan. Används på `feature-comparison-roles.html` (Standard/Administratör, Företag Standard/Företag Special) och `e-handelspartner.html` (Privatperson/Företag, Litet & medelstort företag/Stort företag & koncern) för att introducera respektive sidas roller/kontotyper innan den fullständiga `.compare-table`-jämförelsen. Innehållet (namn, badge, beskrivning, feature-strippar) anpassas per sida — CSS-klasserna och JS-funktionen (`goToCompareView()`) är identiska och kopieras rakt av.

### Anatomi

```
.role-tier-pair                                  ← grid, 2 kort sida vid sida (md+)
  .role-tier                                      ← ljust kort (grundnivå)
    .role-tier__info                              ← vänster halva
      .role-tier__badge-row                       ← ikon + .compare-badge
      .role-tier__name                            ← title-lg
      .role-tier__desc                             ← body-md
      .role-tier__link                             ← Action Link, "arrow_downward"-ikon
    .role-tier__features                           ← höger halva, staplade strippar
      .role-tier__feature × 4                      ← body-sm, centrerad text
  .role-tier.role-tier--dark                       ← utökat/administrativt kort
    (samma understruktur)
```

Flera `.role-tier-pair` kan staplas under varandra (en per kategori/flik som ska introduceras).

### Färgvarianter

| Del | Ljust kort (grundnivå) | `.role-tier--dark` (utökad nivå) |
|---|---|---|
| Kortbakgrund | `surface-raised-primary` (`#fff`) | `surface-100` (`#000`) |
| Kortborder | `border-primary` (`#e5e5e5`) | `surface-90` (`#222`) |
| Titel/ikon | `text-primary` (`#000`) | `accent-default` (`#c7d300`) |
| Beskrivning | `text-secondary` (`#4f4f4f`) | `text-secondary-inverted` (`rgba(255,255,255,.78)`) |
| Länk | `text-action-primary` → hover `text-action-primary-hover` | `text-action-primary-inverted` → hover `text-action-primary-inverted-hover` |
| Feature-strippar | `surface-05` (`#f6f6f6`) bakgrund, `border-primary` mellan | `surface-90` (`#222`) bakgrund, `rgba(255,255,255,.12)` mellan |

> Detta är samma "light vs. dark tier"-mönster som förekommer i externa SaaS-prissidor, men i ECO Design Systems egna färgtokens, raka hörn (`border-radius: 0`) och typografi — inte pill-formade knappar eller godtyckliga färger.

### Typografi

| Element | Token | Mobil | Desktop |
|---|---|---|---|
| `.role-tiers__eyebrow` | `label-sm` | 12px/12px, 0.48px, weight 600, uppercase | 14px/14px, 0.56px |
| `.role-tiers__title` / `.role-tier__group-title` | — (samma skala som `.fob__title`) | 26px/30px, weight 700 | 36px/40px |
| `.role-tiers__desc` (sektionens ingress) | `body-lg` | 18px/24px, 0px | 20px/28px |
| `.role-tier__name` | `title-lg` | 20px/24px, 0px, weight 600 | 24px/28px |
| `.role-tier__desc` | `body-md` | 16px/22px, 0.32px | 16px/24px |
| `.role-tier__link` | Action Link, Medium, **Bold**-variant | 16px/24px, 0.32px, weight 700, gap 6px, ikon 24px | samma |
| `.role-tier__feature` | `body-sm` | 14px/20px, 0.28px | samma |

### Regler

1. **Länken byter aktiv flik i tabellen INNAN den scrollar** — `.role-tier__link` anropar en liten wrapper-funktion (t.ex. `goToCompareView(event, view)`) som hittar rätt `.compare-view-btn[data-view="…"]` och återanvänder tabellens egen `setCompareView(view, btn)` — inte en egen separat kopia av den logiken — så att segmentpillen och synligheten uppdateras identiskt med ett vanligt flik-klick, innan `scrollIntoView({behavior:'smooth'})` körs. `event.preventDefault()` krävs så att webbläsarens direkta ankarhopp inte "snap:ar" mitt i den mjuka scrollningen.
2. **Feature-strippar ska vara grundade i den faktiska jämförelsetabellens rader** — plocka 3–4 rader som är unika för/relevanta för just den rollen (inte påhittat innehåll) så att kortet stämmer överens med vad tabellen faktiskt visar när användaren scrollar dit.
3. **Kortparets ordning speglar flikarnas ordning** i `.compare-view-toggle` — första kortparet hör till första fliken, osv.
4. **Länken använder Bold-varianten (700) och en 24px-ikon**, inte Regular/20px som `.compare-intro__link` — kortets CTA behöver väga upp mot den omgivande brödtexten och synas tydligt som primärt klickbar, medan `.compare-intro__link` står ensam i ett tommare område och klarar sig med Regular.

### CSS-mall (kärnan)

```css
.role-tier-pair {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
@media (min-width: 769px) {
  .role-tier-pair { grid-template-columns: 1fr 1fr; }
}

.role-tier {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border-primary);
  background: var(--color-surface-raised-primary);
}
@media (min-width: 640px) {
  .role-tier { flex-direction: row; }
}
.role-tier--dark {
  background: var(--color-surface-100);
  border-color: var(--color-surface-90);
}

.role-tier__features {
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--color-border-primary);
}
@media (min-width: 640px) {
  .role-tier__features { border-top: none; border-left: 1px solid var(--color-border-primary); }
}
.role-tier--dark .role-tier__features { border-color: rgba(255,255,255,0.12); }

.role-tier__feature {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 16px;
  min-height: 56px;
  background: var(--color-surface-05);
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.28px;
  color: var(--color-text-primary);
}
.role-tier__feature + .role-tier__feature { border-top: 1px solid var(--color-border-primary); }
.role-tier--dark .role-tier__feature { background: var(--color-surface-90); color: #fff; }
.role-tier--dark .role-tier__feature + .role-tier__feature { border-top-color: rgba(255,255,255,0.12); }
```

```js
// Återanvänder tabellens egen setCompareView() — bygger INTE en parallell
// egen version av flik-logiken.
function goToCompareView(event, view) {
  if (event) event.preventDefault();
  var btn = document.querySelector('.compare-view-btn[data-view="' + view + '"]');
  if (btn) setCompareView(view, btn);
  var target = document.getElementById('jamforelse');
  if (target) {
    // Vanlig scrollIntoView() räknar inte in sajtens sticky header
    // (--header-top-h, samma CSS-variabel som .compare-header-row/
    // .compare-group__header redan använder för sin egen sticky
    // top-offset) — sektionens topp hamnar annars gömd bakom headern.
    var headerTopH = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-top-h')) || 0;
    var targetY = target.getBoundingClientRect().top + window.scrollY - headerTopH;
    window.scrollTo({ top: targetY, behavior: 'smooth' });
  }
}
```

> **Scrolla alltid till en `id`-ankrad sektion med `--header-top-h`-offset, aldrig med ren `scrollIntoView()`** — på sidor med sticky site-header döljer headern annars sektionens översta del. `--header-top-h` sätts redan av headerns egen JS och är samma variabel som `.compare-header-row`/`.compare-group__header` använder för sin sticky-positionering, så återanvänd den istället för att räkna ut ett eget offset.

### Snabblänkar i ingressen (`.role-quicklinks`)

En kompakt rad med EN länk per roll, placerad direkt under `.compare-intro__desc` (innan `.compare-card-grid`) — en snabb "innehållsförteckning" som visar exakt vilka roller/konton sidan jämför, redan innan besökaren scrollat förbi hero:n. Kompletterar (ersätter inte) de fullständiga `.role-tier-pair`-korten längre ner: samma roller, samma `goToCompareView()`-länkning, men utan beskrivning eller feature-lista — bara namn + pil.

```
.role-quicklinks                                 ← flex, wrap, centrerad, gap 8px
  .role-quicklink × 1 per roll                    ← <a>, System-knapp (xs, 32px)
    <span>Rollnamn</span>
    <span class="ms">arrow_downward</span>
```

- **Storlek/variant**: byggd som ECO Design Systems **System**-knappvariant (`border: 1px solid border-action-3`, transparent bakgrund) i **xs**-storlek (32px hög, identisk mobil/desktop) — medvetet den minsta, mest diskreta knapptypen som finns, eftersom detta är en genväg och INTE en primär CTA (de finns redan i `.role-tier-pair` längre ner på sidan).
- **Hover**: `background: var(--color-surface-opacity-black-05)` + `border-color: var(--color-border-dark)` — samma hovermönster som Secondary-knappen.
- **Länklogik**: samma `goToCompareView(event, view)` som `.role-tier__link` — byter aktiv flik i `.compare-view-toggle` och scrollar (med `--header-top-h`-offset) till `#jamforelse`. Bygg ALDRIG en egen kopia av flik-/scroll-logiken här.

```css
.role-quicklinks {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 24px; /* space-24 — avstånd till .compare-intro__desc ovanför */
}
.role-quicklink {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 6px 12px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-action-3);
  background: transparent;
  color: var(--color-text-primary);
  text-decoration: none;
  cursor: pointer;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 700;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  transition: background var(--duration-fast-3) var(--ease-standard), border-color var(--duration-fast-3) var(--ease-standard);
}
.role-quicklink:hover {
  background: var(--color-surface-opacity-black-05);
  border-color: var(--color-border-dark);
}
.role-quicklink .ms { font-size: 16px; color: currentColor; }
```

---
