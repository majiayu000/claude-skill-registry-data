---
name: pagination
description: Använd när du bygger ett "visa fler"-mönster för att stegvis ladda in fler resultat i en lista (recensioner, produkter, orderhistorik) — inte numrerad sidnavigering.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Pagination (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=11614-537671

Pagination används för att låta användaren ladda in fler resultat i en lista (recensioner, produkter, orderhistorik m.m.) utan sidladdning — ett "visa fler"-mönster, inte numrerad sidnavigering. Komponenten är smal och centrerad (`190px`, `max-width: 100%`) och placeras som sista element i en `.section`/lista, oavsett hur bred föräldern är.

### Används när
- En lista är för lång för att visa i sin helhet direkt och fler poster ska kunna laddas in stegvis.
- Totalt antal poster är känt i förväg (behövs för räknartext + progressbar).

### Används INTE när
- Alla poster redan visas (dölj hela komponenten, se regel 3).
- Sidan kräver traditionell numrerad sidnavigering (1, 2, 3 …) — det är ett annat mönster.

---

### Anatomi

```
Visar [X] av [Y] [enhet]
[▬▬▬▬▬▬▬▬░░░░░░]              ← progressbar, 2px
[      VISA FLER RESULTAT       ]  ← Secondary-knapp, md, full bredd av komponenten
```

### Mått

| Egenskap | Värde |
|---|---|
| Total bredd | `190px` (`max-width: 100%`, centrerad) |
| Gap: info-block → knapp | `24px` |
| Gap: räknartext → progressbar | `16px` |
| Progressbar höjd | `2px` |
| Top-avstånd till innehållet ovanför | `24px` xs → `32px` sm → `40px` md/lg |
| Bottom-avstånd | **Ingen egen** — se regel 1 |

### Typografi & färger

| Element | Token | Färg |
|---|---|---|
| Räknartext ("Visar X av Y …") | `body-md`: 16px/22px, 0.32px, Regular | `surface-60` (`#595959`) |
| Progressbar — track | — | `surface-10` (`#e5e5e5`) |
| Progressbar — fyllning | — | `surface-100` (`#000000`) |
| Knapp | **Secondary**, storlek **md** (se Knapp-styling ovan) | border/text `border-action-1` / `text-action-primary` |

---

### CSS-mall

```css
.pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  width: 190px;
  max-width: 100%;
  margin: 24px auto 0; /* xs: top 24px */
}
.pagination[hidden] { display: none; }
@media (min-width: 640px) { .pagination { margin-top: 32px; } } /* sm */
@media (min-width: 769px) { .pagination { margin-top: 40px; } } /* md + lg/xl */

.pagination__info { display: flex; flex-direction: column; align-items: center; gap: 16px; width: 100%; }

.pagination__count {
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0.32px;
  color: var(--color-surface-60);
  text-align: center;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.pagination__progress { width: 100%; height: 2px; background: var(--color-surface-10); position: relative; }
.pagination__progress-bar {
  position: absolute;
  inset: 0;
  width: 0%; /* sätts via JS: (synliga / totalt) * 100% */
  background: var(--color-surface-100);
  transition: width var(--duration-medium-2) var(--ease-standard);
}

.pagination__btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--color-border-action-1);
  cursor: pointer;
  padding: 8px;                    /* xs–sm: md-knapp mobil */
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  white-space: nowrap;
  font-size: 16px;
  line-height: 16px;
  letter-spacing: 0.32px;
  color: var(--color-text-action-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1;
  transition: background var(--duration-fast-3) var(--ease-standard);
}
.pagination__btn:hover { background: var(--color-surface-opacity-black-05); }
@media (min-width: 769px) {
  .pagination__btn { padding: 12px; font-size: 18px; line-height: 18px; letter-spacing: 0.18px; } /* md+: md-knapp desktop */
}
```

### HTML-exempel

```html
<div class="pagination" id="pagination-produkter">
  <div class="pagination__info">
    <p class="pagination__count">Visar <span id="produkter-pagination-count">4</span> av 6 recensioner</p>
    <div class="pagination__progress">
      <div class="pagination__progress-bar" id="produkter-pagination-bar" style="width:66.6667%"></div>
    </div>
  </div>
  <button type="button" class="pagination__btn" onclick="showMore('produkter', this)">Visa fler recensioner</button>
</div>
```

```js
function updatePagination(key, visible, total) {
  document.getElementById(key + '-pagination-count').textContent = visible;
  document.getElementById(key + '-pagination-bar').style.width = (total ? (visible / total) * 100 : 0) + '%';
  document.getElementById('pagination-' + key).hidden = visible >= total; // inget mer att ladda
}
```

### Regler

1. **IMPORTANT — Ingen egen bottom-padding:** Komponenten placeras alltid som sista element i en `.section` (se Section-komponenten ovan). Sektionens egen bottom-padding (40/48/64/80px per breakpoint) ger redan rätt luft under — lägg **aldrig** till `padding-bottom`/`margin-bottom` på pagineringskomponenten själv, det skulle dubblera avståndet. Endast top-avståndet (24/32/40/40) hör till komponenten.
2. Progressbarens fyllnadsbredd beräknas alltid dynamiskt som `(synliga / totalt) * 100%` via JS — hårdkoda aldrig ett fast procenttal utöver det initiala serverrenderade värdet.
3. **Dölj hela komponenten** (`hidden`-attribut på ytterwrappern, inte bara knappen) när alla poster redan är laddade. Att bara gömma knappen lämnar en missvisande räknare/progressbar kvar.
4. Knappen är alltid **Secondary, storlek md**, i full bredd av komponentens 190px-container — aldrig Primary eller annan storlek/variant.
5. Komponentens bredd (`190px`, `max-width: 100%`) är fast och centrerad oavsett hur bred föräldersektionen är — sträck aldrig ut den till sektionens fulla bredd.

---
