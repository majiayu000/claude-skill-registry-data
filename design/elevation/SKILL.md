---
name: elevation
description: Använd när du väljer skugga/elevation för kort, modaler, drawers, tooltips eller andra upphöjda ytor — Shadow Bottom/Top, Designated Level (drawers) och komponentspecifika skuggor.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Elevation & Shadows (ECO Design System)

Shadows uttrycker graden av elevation mellan ytor – ju större och mjukare skugga, desto högre elevation.

### Grundbegrepp

| Begrepp | Definition |
|---|---|
| **Elevation** | Avståndet mellan två element längs z-axeln. |
| **Surface** | Den lägst synliga behållaren som komponenter, text m.m. placeras på. Motsvara `background-primary` (`#ffffff`). |
| **Background** | Applikationens bakgrundsfärg – den yta som allt vilar på under surface-nivån. |

### Välja rätt elevation

- **Öka elevation för prioriterade actions.** Användare uppmärksammar element som verkar ligga närmre – lyft det du vill att de ska fokusera på.
- **Liten och skarp skugga** = ytan ligger nära bakgrunden (låg elevation).
- **Stor och mjuk skugga** = ytan ligger långt från bakgrunden (hög elevation).
- **Efterlikna verkliga ljusförhållanden** – välj den elevationsnivå som känns naturlig för komponentens funktion.
- **Använd sparsamt.** Överdriven elevation distraherar och försämrar användarupplevelsen.

ECO Design System har **4 kategorier** av elevation:

| Kategori | Prefix | Beskrivning |
|---|---|---|
| Shadow Bottom | `elevation-b-*` | Ljuskälla uppifrån. Vanligast förekommande. |
| Shadow Top | `elevation-t-*` | Ljuskälla nedifrån. Används sparsamt. |
| Designated Level | `elevation-drawer-*` | Globala komponenter på separat lager (navigation, drawers). |
| Component Specific | `elevation-*` | Exklusivt för specifika komponenter. |

---

### Shadow Bottom (`elevation-b-*`)

Simulerar ljuskälla uppifrån. Skuggan faller nedåt. **Vanligast förekommande** i hela UI:t.

Varje nivå består av två lager: en mjuk huvudskugga + en skarp konturskugga (`0px 0px 1px 0px rgba(0,0,0,0.05)`).

| Token | CSS `box-shadow` | Nivå | Används för |
|---|---|---|---|
| `elevation-b-20` | `0px 1px 3px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 20% | Variant Tables (PDP/PLP), Data tables |
| `elevation-b-40` | `0px 2px 4px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 40% | Tooltip |
| `elevation-b-60` | `0px 4px 8px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 60% | Overflow menu, Notification |
| `elevation-b-80` | `0px 8px 16px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 80% | Site header, Menu, Dropdowns, Exposed Dropdowns |
| `elevation-b-100` | `0px 16px 24px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 100% | Modaler |

```css
/* Exempel: Kort med elevation-b-20 */
.card {
  box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05);
}

/* Exempel: Modal med elevation-b-100 */
.modal {
  box-shadow: 0px 16px 24px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05);
}
```

---

### Shadow Top (`elevation-t-*`)

Simulerar ljuskälla nedifrån. Skuggan faller uppåt. **Används sparsamt.**

| Token | CSS `box-shadow` | Nivå |
|---|---|---|
| `elevation-t-20` | `0px -1px 3px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 20% |
| `elevation-t-40` | `0px -2px 4px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 40% |
| `elevation-t-60` | `0px -4px 8px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 60% |
| `elevation-t-80` | `0px -8px 16px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 80% |
| `elevation-t-100` | `0px -16px 24px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)` | 100% |

---

### Designated Level – Drawers & Navigation

Avsett för essentiella globala komponenter (navigationsmeny, drawers) som måste ligga på ett separat lager och sällan hindras av andra element.

| Token | CSS `box-shadow` | Beskrivning |
|---|---|---|
| `elevation-drawer-left` | `25px 0px 25px 0px rgba(0,0,0,0.03)` | Drawer från vänster – skugga på höger sida |
| `elevation-drawer-right` | `-25px 0px 25px 0px rgba(0,0,0,0.03)` | Drawer från höger – skugga på vänster sida |
| `elevation-drawer-left-menu-sublevel` | `4px 0px 10px 0px rgba(0,0,0,0.05)` | Inline drawer, sub-menynivåer (nivå 2+) |

```css
/* Drawer från vänster */
.drawer-left {
  box-shadow: 25px 0px 25px 0px rgba(0,0,0,0.03);
}

/* Drawer från höger */
.drawer-right {
  box-shadow: -25px 0px 25px 0px rgba(0,0,0,0.03);
}
```

---

### Component Specific

Skuggor som enbart används för specifika komponenter. Specificeras i detalj inom respektive komponentbeskrivning.

| Token | CSS `box-shadow` | Används för |
|---|---|---|
| `elevation-input_control-switch` | `0px 4px 8px 0px rgba(48,49,51,0.10), 0px 1px 1px 0px rgba(48,49,51,0.24), 0px -1px 1px 0px rgba(0,0,0,0.03)` | Toggle switch – indikerar upphöjd nivå |
| `elevation-table-overflow-right` | `-5px 0px 10px 0px rgba(0,0,0,0.05), -1px 0px 5px 0px rgba(0,0,0,0.10)` | Tabell-overflow höger – skugga inuti tabell där innehåll överskrider bredden |
| `elevation-table-overflow-left` | `5px 0px 10px 0px rgba(0,0,0,0.05), 1px 0px 5px 0px rgba(0,0,0,0.10)` | Tabell-overflow vänster – skugga inuti tabell där innehåll överskrider bredden |

---

### Regler för elevation

1. **Välj alltid lägsta möjliga nivå** – använd `elevation-b-20` som default för kortliknande ytor.
2. **Öka elevation för prioriterade actions** – modaler och kritiska overlays ska alltid ligga på `elevation-b-100`.
3. **Blanda inte Bottom och Top** på samma komponent (undantag: `elevation-input_control-switch`).
4. **Drawers och navigation** ska alltid använda `elevation-drawer-*`, aldrig `elevation-b-*`.
5. **Component Specific tokens** används aldrig utanför sin avsedda komponent.
6. **Surface ≠ Background** – Surface (`background-primary: #ffffff`) är den synliga behållaren; Background är underliggande sidbakgrund. Elevation skiljer dessa åt visuellt.
7. **Liten/skarp skugga** signalerar nära yta (låg nivå). **Stor/mjuk skugga** signalerar hög elevation – välj därefter.
8. **Drawer-overlay** – bakgrundsöverlagringen bakom en öppen drawer ska ha `background: rgba(0,0,0,0.2)`. Använd aldrig `surface-opacity-black-50` (50%) för drawers.
9. **Drawer-skugga** – en drawer som öppnas från höger ska alltid ha `box-shadow: var(--elevation-drawer-right)`. En drawer från vänster ska ha `box-shadow: var(--elevation-drawer-left)`. Skuggan appliceras direkt på drawer-panelen, inte på overlay.
10. **Drawer-bredd** – en standard drawer ska alltid ha `width: min(500px, 100%)`. Detta ger fast 500px bredd på större skärmar och fyller hela bredden automatiskt när fönstret/enheten är smalare än 500px. Använd aldrig separata media queries för att sätta `width: 100%` eller `width: 500px` på drawer-panelen.
11. **Drawer-header scroll-skugga** – när drawer-innehållet scrollas nedåt ska headern få en skugga för att visuellt separera den från innehållet. Använd `elevation-b-60` (`0px 4px 8px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)`). Klassen `.drawer-header--elevated` togglas via JS när `content.scrollTop > 0`. Transition: `var(--duration-fast-3) var(--ease-standard)`.

```css
.drawer-header {
  transition: box-shadow var(--duration-fast-3) var(--ease-standard);
}
.drawer-header--elevated {
  box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-60 */
}
```

```js
content.addEventListener('scroll', () => {
  header.classList.toggle('drawer-header--elevated', content.scrollTop > 0);
});
```

12. **Drawer – responsiva komponentstorlekar** – vid `max-width: 768px` (xs + sm breakpoints) ska alla komponenter inuti drawern använda Mobile Base Styling. Applicera följande `@media (max-width: 768px)`-block på varje drawer:

```css
@media (max-width: 768px) {
  /* Header */
  .drawer-header { padding: 16px 24px; }
  .drawer-title {
    font-size: 22px;       /* display-sm Mobile */
    line-height: 22px;
  }

  /* Content & footer */
  .drawer-content { padding: 0 24px 24px; gap: 16px; }
  .drawer-footer { padding: 16px 24px; }

  /* Spara-knapp — mobile lg: padding 12px */
  .drawer-save-btn { padding: 12px 16px; }

  /* Labels — label-md Mobile: 14px/14px, 0.42px */
  .form-label {
    font-size: 14px;
    line-height: 14px;
    letter-spacing: 0.42px;
  }

  /* Inputs & selects — Large Mobile: 40px, 8px padding, body-md mobile 16px/22px */
  .form-input,
  .form-select {
    height: 40px;
    padding: 8px;
    line-height: 22px;
  }
  .form-select { padding-right: 40px; }   /* behåll utrymme för dropdown-pil */

  /* Checkbox-text — body-md Mobile: 16px/22px */
  .form-checkbox-item span {
    font-size: 16px;
    line-height: 22px;
    letter-spacing: 0.32px;
  }

  /* form-row staplas vertikalt på mobil */
  .form-row { flex-direction: column; gap: 16px; }
}
```

**Sammanfattning av Mobile Base Styling för drawer-komponenter:**

| Komponent | Desktop (`769px+`) | Mobile (`≤768px`) |
|---|---|---|
| Drawer-titel | `display-sm` 26px/26px | 22px/22px |
| Header-padding | `24px 32px` | `16px 24px` |
| Content-padding | `0 32px 32px`, gap 24px | `0 24px 24px`, gap 16px |
| Footer-padding | `24px 32px` | `16px 24px` |
| Label (`label-md`) | 16px/16px, 0.48px | 14px/14px, 0.42px |
| Input / Select | 48px, padding `8px 12px`, line-height 24px | 40px, padding `8px`, line-height 22px |
| Checkbox-text | `body-md` 16px/24px, 0.32px | 16px/22px, 0.32px |
| Spara-knapp | `padding: 16px` | `padding: 12px 16px` |
| form-row | `flex-direction: row` | `flex-direction: column`, gap 16px |

---
