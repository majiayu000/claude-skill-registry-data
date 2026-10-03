---
name: segment-control
description: Använd när du bygger eller granskar en segmenterad kontroll (pill toggle) för att växla mellan två relaterade vyer/filter i samma yta — storlekar, den glidande pill-interaktionen och states. Ersätter aldrig Tabs eller Radio-knappar.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Segment Control (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=23144-268049

Segment Control (segmenterad kontroll/"pill toggle") används för att växla mellan två relaterade vyer eller filter i samma yta — t.ex. `Användarroller / Företagsplan` eller `Alla funktioner / Nyckelfunktioner`. Ska **inte** användas som ersättning för Tabs (navigering mellan olika sidor/innehåll) eller Radio-knappar (formulärval som skickas in).

> Exempelimplementation: `.compare-view-toggle`/`.compare-view-btn` (Large) och `.compare-filter-toggle`/`.compare-filter-btn` (Small) i `feature-comparison-roles.html`.

### Varianter

| Variant | Bakgrund (spår) | Använd på |
|---|---|---|
| **Primary** | `#dad9d7`→hover, `var(--color-surface-disabled)` `#e5e5e5` enabled | Ljus bakgrund (standard) |
| **Primary Inverted** | Motsvarande mörk variant | Mörk/svart bakgrund |

**Shape:** `Pill` (helt rundade hörn — `border-radius: höjd / 2`, standardval) eller `Square` (raka hörn, `border-radius: 0`, används sparsamt).

### Storlekar

Track-padding skalar med storlek (~1px mindre på mobil än desktop för respektive storlek). `border-radius` på spåret är alltid `höjd / 2`; det aktiva segmentets pill-radie är `spårets radie − track-padding`.

**Bredd:** Kontrollen är **fluid (`width: 100%`) enbart i `breakpoint-xs`** (0–639px) — den fyller sin förälders bredd, och de två segmenten delar utrymmet jämnt (`flex: 1` på varje `.segment-control__btn`). Redan vid `sm:` (640px+) slutar den vara fluid och krymper till sitt innehåll (`width: auto`, `flex: none` på knapparna) — höjd/padding/font byter dock inte förrän vid `md:` (769px+), så sm har fortfarande mobil-storlek fast innehållsbaserad bredd. Ligger kontrollen i en flex-column-förälder med standard `align-items: stretch` (t.ex. `.compare-header-row__right`) krävs även `align-self: flex-start` från `sm:` — annars sträcker föräldern ut den trots `width: auto`. Se `.compare-view-toggle`/`.compare-filter-toggle` i `feature-comparison-roles.html` för den verifierade implementationen.

| Storlek | Höjd Desktop (`md:` 769px+) | Höjd Mobil (≤768px) | Text | Använd för |
|---|---|---|---|---|
| **Large** | 56px, padding `5px`, radius `28px`, pill-radius `23px`, pill-padding `24px`, `label-lg` (18px/18px, 0.18px) | 48px, padding `4px`, radius `24px`, pill-radius `20px`, pill-padding `20px`, `label-lg` mobil (16px/16px, 0.32px) | `label-lg` | Primär vy-växlare (sidnivå) |
| **Medium** | 48px, padding `4px`, radius `24px`, pill-radius `20px`, pill-padding `20px`, `label-lg` (18px/18px, 0.18px) | 40px, padding `4px`, radius `20px`, pill-radius `16px`, pill-padding `16px`, `label-lg` mobil (16px/16px, 0.32px) | `label-lg` | Mellanstor vy-växlare (t.ex. i en drawer) |
| **Small** | 40px, padding `4px`, radius `20px`, pill-radius `16px`, pill-padding `16px`, `label-md` (16px/16px, 0.48px) | 32px, padding `3px`, radius `16px`, pill-radius `13px`, pill-padding `12px`, `label-md` mobil (14px/14px, 0.42px) | `label-md` | Sekundära filter inom en yta (t.ex. "Nyckelfunktioner") |
| **XSmall** | 32px, padding `3px`, radius `16px`, pill-radius `13px`, pill-padding `12px`, `label-sm` (14px/14px, 0.56px) | 32px, padding `3px`, radius `16px`, pill-radius `13px`, pill-padding `10px`, `label-sm` mobil (12px/12px, 0.48px) | `label-sm` | Kompakta filter i tät yta (t.ex. tabellverktygsrad) |

> XSmall har samma höjd (32px) på både desktop och mobil — endast pill-padding (12px/10px) och fontstorlek (14px/12px) skiljer breakpointen åt.

### Tillstånd (States)

| Tillstånd | Visuell regel |
|---|---|
| **Enabled** | Spår: `var(--color-surface-disabled)` `#e5e5e5`. Aktivt segment: svart pill (`var(--color-surface-100)`) med `elevation-input_control-switch`-skugga, vit text. Inaktivt segment: transparent, svart text, ingen understrykning. Pillen är ett **eget, separat `.segment-control__thumb`-element** som glider mellan segmenten — se **Interaktion (glidande pill)** nedan — inte en bakgrund som sätts direkt på den aktiva knappen. |
| **Hover** | Spåret mörknar till `var(--color-border-tertiary)` `#dad9d7`. Det **inaktiva** segmentets text får `text-decoration: underline` (samma hover-princip som Action Link). Det aktiva segmentet ändras inte. |
| **Focus** | **Ingen egen fokusstil på kontrollen.** De enskilda segment-knapparna är vanliga `<button>`-element och ärver projektets globala fokusring (se **Knapp-styling → Tillstånd → Focus**: `body.keyboard-nav button:focus { outline-color: #455efb }`), enbart synlig vid tangentbordsnavigering. Bygg **aldrig** en separat `::after`/border-baserad fokusring för Segment Control — det skulle avvika från den etablerade outline-metoden och dubblera fokusindikeringen. |
| **Disabled** | Används sällan för denna komponent i produkten — om det behövs, hämta exakt spec från Figma-noden (`State=Disabled`) innan implementation. |

### Interaktion (glidande pill)

Det aktiva segmentets pill är **inte** en bakgrund som sätts direkt på knappen — det är ett eget `.segment-control__thumb`-element som ligger absolut positionerat bakom knapparna och **glider** till den aktiva knappens position/bredd. Det behövs eftersom knapparna kan vara olika breda (innehållsbaserad bredd på desktop, `flex: none`) — en fast 50/50-uppdelning av thumben skulle då hamna fel.

1. Thumben mäts/positioneras med JS via aktiv knapps `offsetLeft`/`offsetWidth` (inte CSS `%`, se `moveSegmentThumb()` nedan).
2. Knapparna själva är genomskinliga (`position: relative; z-index: 1`) och ligger ovanpå thumben — bara textfärgen ändras vid `--active`.
3. Thumbens övergång: `transform`/`width` med **`var(--duration-medium-2) var(--ease-standard)`** (300ms, ease-in-out — lugn start, snabb mitt, lugn avslutning). Detta skiljer sig medvetet från hover-övergångarna (`--duration-fast-3`/`--ease-standard`, se Tillstånd-tabellen ovan) eftersom pillen rör sig en synlig sträcka och ska kännas mjuk, inte snabb/hover-artad.
4. Mät om thumbens position vid `resize` (knapparnas bredd ändras vid `md:`-brytpunkten) och vid sidladdning.

### CSS-mall (Large, Primary/Pill — mobile-first)

```css
.segment-control {
  position: relative;
  display: flex;
  width: 100%;                  /* fluid — enbart breakpoint-xs (0–639px) */
  height: 48px;                 /* mobil */
  padding: 4px;
  background: var(--color-surface-disabled);
  border-radius: 24px;
  box-sizing: border-box;
  transition: background-color var(--duration-fast-3) var(--ease-standard);
}
.segment-control:hover { background: var(--color-border-tertiary); }

@media (min-width: 640px) {
  /* sm+ (Tablet och uppåt): kontrollen slutar vara fluid redan här och
     krymper till sitt innehåll — höjd/padding är dock fortfarande
     mobil-storlek tills md: (769px). Om föräldern är en flex-column
     med align-items:stretch (standard) krävs även align-self: flex-start
     här, annars sträcks kontrollen ut trots width:auto. */
  .segment-control { width: auto; }
}
@media (min-width: 769px) {
  .segment-control { height: 56px; padding: 5px; border-radius: 28px; }
}

/* Den glidande pillen — se "Interaktion (glidande pill)" ovan.
   Bredd/position sätts av moveSegmentThumb(), inte av CSS. */
.segment-control__thumb {
  position: absolute;
  top: 4px;
  bottom: 4px;
  left: 0;
  width: 0;
  background: var(--color-surface-100);
  border-radius: 20px;
  box-shadow: 0px 4px 8px 0px rgba(48,49,51,0.10), 0px 1px 1px 0px rgba(48,49,51,0.24), 0px -1px 1px 0px rgba(0,0,0,0.03); /* elevation-input_control-switch */
  transition: transform var(--duration-medium-2) var(--ease-standard), width var(--duration-medium-2) var(--ease-standard);
  pointer-events: none;
}
@media (min-width: 769px) {
  .segment-control__thumb { top: 5px; bottom: 5px; border-radius: 23px; }
}
/* Ligger kontrollen redan på en mörk/grå yta (t.ex. ett filter inuti en
   annan, större segment-control — se .compare-filter-toggle) ska pillen
   vara vit istället för svart: */
.segment-control__thumb--light { background: var(--color-surface-raised-primary); }

.segment-control__btn {
  position: relative;
  z-index: 1;
  flex: 1;                       /* xs: fyller segmenten jämnt */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0 20px;
  background: transparent;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-size: 16px;               /* label-lg Mobil */
  font-weight: 700;
  line-height: 16px;
  letter-spacing: 0.32px;
  text-transform: uppercase;
  color: var(--color-text-action-primary);
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
  transition: color var(--duration-fast-3) var(--ease-standard);
}
@media (min-width: 640px) {
  .segment-control__btn { flex: none; }   /* sm+: innehållsbaserad bredd, matchar kontrollens width:auto */
}
@media (min-width: 769px) {
  .segment-control__btn { padding: 0 24px; border-radius: 23px; font-size: 18px; line-height: 18px; letter-spacing: 0.18px; }
}

/* Inaktivt segment — hover ger understrykning */
.segment-control__btn:not(.segment-control__btn--active):hover { text-decoration: underline; }

/* Aktivt segment — bara textfärgen ändras, pillen ligger redan under
   (svart pill → vit text). Med .segment-control__thumb--light (vit
   pill) ska texten INTE bytas — låt den vara svart hela vägen. */
.segment-control__btn--active { color: var(--color-text-action-primary-inverted); }

/* Medium — mellanstor vy-växlare (t.ex. i en drawer) */
.segment-control--md { height: 40px; padding: 4px; border-radius: 20px; }
.segment-control--md .segment-control__thumb { top: 4px; bottom: 4px; border-radius: 16px; }
.segment-control--md .segment-control__btn { padding: 0 16px; border-radius: 16px; font-size: 16px; line-height: 16px; letter-spacing: 0.32px; }
@media (min-width: 769px) {
  .segment-control--md { height: 48px; padding: 4px; border-radius: 24px; }
  .segment-control--md .segment-control__thumb { top: 4px; bottom: 4px; border-radius: 20px; }
  .segment-control--md .segment-control__btn { padding: 0 20px; border-radius: 20px; font-size: 18px; line-height: 18px; letter-spacing: 0.18px; }
}

/* Small — sekundära filter (t.ex. "Nyckelfunktioner") */
.segment-control--sm { height: 32px; padding: 3px; border-radius: 16px; }
.segment-control--sm .segment-control__thumb { top: 3px; bottom: 3px; border-radius: 13px; }
.segment-control--sm .segment-control__btn { padding: 0 12px; border-radius: 13px; font-size: 14px; line-height: 14px; letter-spacing: 0.42px; }
@media (min-width: 769px) {
  .segment-control--sm { height: 40px; padding: 4px; border-radius: 20px; }
  .segment-control--sm .segment-control__thumb { top: 4px; bottom: 4px; border-radius: 16px; }
  .segment-control--sm .segment-control__btn { padding: 0 16px; border-radius: 16px; font-size: 16px; line-height: 16px; letter-spacing: 0.48px; }
}

/* XSmall — kompakta filter i tät yta (t.ex. tabellverktygsrad).
   Samma höjd på mobil och desktop — endast pill-padding och font ändras. */
.segment-control--xs { height: 32px; padding: 3px; border-radius: 16px; }
.segment-control--xs .segment-control__thumb { top: 3px; bottom: 3px; border-radius: 13px; }
.segment-control--xs .segment-control__btn { padding: 0 10px; border-radius: 13px; font-size: 12px; line-height: 12px; letter-spacing: 0.48px; }
@media (min-width: 769px) {
  .segment-control--xs .segment-control__btn { padding: 0 12px; font-size: 14px; line-height: 14px; letter-spacing: 0.56px; }
}
```

### HTML- och JS-exempel

```html
<div class="segment-control" role="group" aria-label="Välj vy">
  <span class="segment-control__thumb" aria-hidden="true"></span>
  <button type="button" class="segment-control__btn segment-control__btn--active" onclick="setView('roller', this)">Användarroller</button>
  <button type="button" class="segment-control__btn" onclick="setView('foretag', this)">Företagsplan</button>
</div>
```

```js
// Glider pillen till den aktiva knappens position/bredd — se
// "Interaktion (glidande pill)" ovan för varför offsetLeft/offsetWidth
// används istället för en fast CSS %-uppdelning.
function moveSegmentThumb(thumb, activeBtn) {
  if (!thumb || !activeBtn) return;
  thumb.style.width = activeBtn.offsetWidth + 'px';
  thumb.style.transform = 'translateX(' + activeBtn.offsetLeft + 'px)';
}

function setView(view, btn) {
  btn.parentElement.querySelectorAll('.segment-control__btn').forEach(function (b) {
    b.classList.toggle('segment-control__btn--active', b === btn);
  });
  moveSegmentThumb(btn.parentElement.querySelector('.segment-control__thumb'), btn);
  // ... visa/dölj respektive vy ...
}

// Initiera vid sidladdning och mät om vid resize (knapparnas bredd
// ändras vid md:-brytpunkten, 769px).
function initSegmentThumb(control) {
  moveSegmentThumb(control.querySelector('.segment-control__thumb'), control.querySelector('.segment-control__btn--active'));
}
document.querySelectorAll('.segment-control').forEach(initSegmentThumb);
window.addEventListener('resize', function () {
  document.querySelectorAll('.segment-control').forEach(initSegmentThumb);
});
```

---
