---
name: motion
description: Använd när du animerar eller transitionerar något — easing-kurvor (decelerate/accelerate/standard) och duration-tokens (fast/medium/slow) enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Motion – Easing & Duration (ECO Design System)

Animationer förmedlar funktionalitet, intention och samband. Använd dessa tokens för att skapa sammanhängande och realistiska övergångar.

> Principerna gäller som riktlinjer. De kan variera på komponentnivå men ska alltid följas så nära som möjligt för att säkerställa konsekvens.

### Tre grundbegrepp

| Begrepp | Förklaring |
|---|---|
| **Timing** | Hur lång tid en action tar. Välj alltid med omsorg. |
| **Spacing** | Mellanrummet mellan frames i ett rörligt objekt. Varierad spacing ger mjuka övergångar. |
| **Ease** | Kombinationen av timing och spacing. Styr hur en rörelse flödar – objekt ska accelerera och decelerate mjukt. |

---

### Easing-tokens

Välj easing beroende på hur en transition rör sig i relation till skärmen:

- **Liten förändring, kort distans** → snabb fade
- **Medium förändring, medium distans** → medium fade
- **Stor förändring, lång distans** → långsam fade

| Token | Kurva | Typ | Beskrivning | Används för |
|---|---|---|---|---|
| `motion-ease-decelerate-generic` | `cubic-bezier(.16,.38,.58,1)` | Ease Out – Generic | Börjar snabbt, bromsar in gradvis. Mindre betonad variant. | onClick, enter selected states. Form elements, Tabs, Toggled buttons, Tooltip. |
| `motion-ease-decelerate-emphasized` | `cubic-bezier(.16,0,.16,1)` | Ease Out – Emphasized ★ | Tydligare inbromsning. Standardval för att föra in element från utanför skärmen. | Drawers (alla varianter), Main/Account menu, Product menu, Notifications. |
| `motion-ease-accelerate-generic` | `cubic-bezier(.36,.09,1,.58)` | Ease In – Generic | Börjar långsamt, ökar hastighet. Likt ett föremål som faller. | Ta bort element från skärmen (exit-animationer). |
| `motion-ease-standard` | `cubic-bezier(.35,0,.35,1)` | Ease InOut – Standard | Startar långsamt, ökar, bromsar in. Allround-easing. | Hover states (majoriteten). Button, Product Card, Text Link, Breadcrumb, Collapsible, Overflow menu, Form elements, Tab bar, Drawer Link. |

> ★ `motion-ease-decelerate-emphasized` är förstahandsvalet för enter-animationer. `motion-ease-decelerate-generic` används när en mindre betoning önskas.

```css
/* Exempel: Element glider in från utanför skärmen (drawer) */
.drawer {
  transition: transform 350ms cubic-bezier(.16,0,.16,1);
}

/* Exempel: Hover-tillstånd på knapp */
.btn {
  transition: background-color 200ms cubic-bezier(.35,0,.35,1);
}

/* Exempel: Element lämnar skärmen */
.toast-exit {
  transition: opacity 150ms cubic-bezier(.36,.09,1,.58);
}
```

---

### Duration-tokens

Duration delas in i tre grupper — **Fast**, **Medium** och **Slow** — med fyra steg vardera.

> Använd tokens i enlighet med distance- och fade-principerna nedan. Vid vertikala rörelser kan valfri duration inom rätt grupp användas.

#### Fast (50–200ms) – Små, snabba interaktioner

| Token | Värde | Används för |
|---|---|---|
| `motion-duration-fast-1` | 50ms | Mikro-interaktioner, omedelbar feedback |
| `motion-duration-fast-2` | 100ms | Snabba hover-övergångar, focus-indikatorer |
| `motion-duration-fast-3` | 150ms | Standard hover, snabba exit-animationer |
| `motion-duration-fast-4` | 200ms | Lätta enter-animationer, korta state-ändringar |

#### Medium (250–400ms) – Mediumstora interaktioner

| Token | Värde | Används för |
|---|---|---|
| `motion-duration-medium1` | 250ms | Dropdowns, tooltips, kortare slide-ins |
| `motion-duration-medium2` | 300ms | Standard för de flesta UI-övergångar |
| `motion-duration-medium3` | 350ms | Drawers, panels, medelstora ytor |
| `motion-duration-medium4` | 400ms | Komplexa komponent-övergångar |

#### Slow (450–600ms) – Stora, tyngre rörelser

| Token | Värde | Används för |
|---|---|---|
| `motion-duration-slow-1` | 450ms | Stora enter-animationer, sidövergångar |
| `motion-duration-slow-2` | 500ms | Hero-element, fullwidth-animationer |
| `motion-duration-slow-3` | 550ms | Empty states, loading-faser |
| `motion-duration-slow-4` | 600ms | Längsta tillåtna duration – sparsamt |

---

### Distances – distans styr duration

Rörelsens distans avgör vilken duration-grupp som ska användas.

| Distans | Viewport-andel | Duration-grupp | Beskrivning |
|---|---|---|---|
| **Short** | ≤ 25% av vyn | Fast | Täcker liten del av skärmen. Använd fast-tokens. |
| **Medium** | 26–50% av vyn | Medium | Halva skärmen. Använd medium-tokens. |
| **Long** | 51–100% av vyn | Slow | Hela eller större delen av skärmen. Använd slow-tokens. |

---

### Fades – opacitet och färgövergångar

Fades är en sofistikerad metod för att övergå mellan färger och/eller opacitetsnivåer.

| Typ | Duration-grupp | Beskrivning | Komponenter |
|---|---|---|---|
| **Fast fade** | Fast | Standardinteraktioner i liten skala. | Buttons, list items, form elements |
| **Medium fade** | Medium | Medelstora interaktioner. Element som lyfts från ytan. | Cards, elevated surfaces |
| **Slow fade** | Slow | Viktiga tillståndsskiften. | Empty states, loading phases |

---

### Kombinationsregel: distans + fade

| Scenario | Distans | Fade | Easing |
|---|---|---|---|
| Knapp-hover | Short | Fast fade | `motion-ease-standard` |
| Dropdown öppnas | Short–Medium | Fast–Medium fade | `motion-ease-decelerate-generic` |
| Drawer glider in | Medium–Long | Medium fade | `motion-ease-decelerate-emphasized` |
| Modal visas | Medium | Medium fade | `motion-ease-decelerate-emphasized` |
| Element försvinner | Valfri | Fast fade | `motion-ease-accelerate-generic` |
| Loading/empty state | — | Slow fade | `motion-ease-standard` |

```css
/* CSS custom properties för hela projektet */
:root {
  /* Easing */
  --ease-decelerate-generic:    cubic-bezier(.16,.38,.58,1);
  --ease-decelerate-emphasized: cubic-bezier(.16,0,.16,1);
  --ease-accelerate-generic:    cubic-bezier(.36,.09,1,.58);
  --ease-standard:              cubic-bezier(.35,0,.35,1);

  /* Duration */
  --duration-fast-1:   50ms;
  --duration-fast-2:   100ms;
  --duration-fast-3:   150ms;
  --duration-fast-4:   200ms;
  --duration-medium-1: 250ms;
  --duration-medium-2: 300ms;
  --duration-medium-3: 350ms;
  --duration-medium-4: 400ms;
  --duration-slow-1:   450ms;
  --duration-slow-2:   500ms;
  --duration-slow-3:   550ms;
  --duration-slow-4:   600ms;
}
```

---
