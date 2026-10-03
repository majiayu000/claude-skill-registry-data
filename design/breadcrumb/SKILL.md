---
name: breadcrumb
description: Använd när du bygger brödsmulor för sidhierarki-navigering — placeras direkt under headern som första element i .page.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Breadcrumb (ECO Design System)

**Figma – design:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=1986-64264
**Figma – responsivt utförande per breakpoint:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=9071-123361

Breadcrumb används för att visa användarens position i sidhierarkin och möjliggöra snabb navigering uppåt i strukturen (t.ex. `Hem / Kategori / Undersida`). Placeras direkt under headern, som första element inuti sidans innehållswrapper (`.page`).

### Används när
- Sidan ligger mer än ett steg ner i navigationsträdet (PLP, PDP, landningssidor, kategorisidor).
- Användaren behöver kunna backa till en överliggande nivå utan att använda webbläsarens tillbaka-knapp.

### Används INTE när
- Sidan är startsidan eller ligger direkt under Hem utan meningsfull mellannivå.
- Navigeringen redan täcks av tabbar eller en tydlig tillbaka-länk i samma vy (undvik dubblering).

---

### Anatomi

```
[Hem]  /  [Mellansteg]  /  [Aktuell sida]
```

- Varje brödsmula renderas som en **kantad box** (`border: 1px solid` `border-action-3` = `rgba(0,0,0,0.10)`), aldrig som understruken text/länk.
- Avskiljare mellan brödsmulor är ett `/`-tecken, centrerat i en fast bredd om `4px`.
- Containern har **ingen egen bakgrundsfärg** — den ligger alltid mot sidans `body`-bakgrund. Vilken färg det blir beror på sidtyp (se regel 7).
- Samtliga brödsmulor utom den sista är klickbara länkar (`Enabled`-stil). Den **sista** brödsmulan representerar aktuell sida (`Active`-stil) — fetstil, svart text, ej klickbar.
- Komponenten har inbyggd vertikal spacing (padding) — se regel 1 nedan för hur det påverkar sektionen efter.

---

### Storlekar per breakpoint

| Breakpoint | Höjd (bar) | Crumb-padding | Text | Avskiljare (höjd) | Container: horisontell padding | Container: extra bottom-padding |
|---|---|---|---|---|---|---|
| `xs` Mobil (0–639px) | 56px | `6px 7px` | 12px/12px, 0.24px | 24px | `var(--px-page)` (16px) | 0px |
| `sm` Tablet (640–768px) | 56px | `6px 7px` | 12px/12px, 0.24px | 24px | `var(--px-page)` (32px) | 0px |
| `md` Desktop Small (769–1023px) | 72px | `9px 10px` | 14px/14px, 0.28px | 32px | `var(--px-page)` (32px) | 8px |
| `lg` / `xl` Desktop (1024px+) | 80px | `9px 10px` | 14px/14px, 0.28px | 32px | `var(--px-page)` (40px) | 16px |

> `xs` och `sm` är identiska förutom horisontell sidmarginal. `md`, `lg` och `xl` delar samma crumb-/textstorlek — skillnaden är enbart hur mycket extra bottom-padding containern får utöver barens egna `16px` (top+bottom).
> Använd **alltid** `var(--px-page)` (grid-marginalen per breakpoint) för horisontell padding — aldrig ett hårdkodat pixelvärde eller `var(--px-full)`, eftersom breadcrumben ligger inuti `.page` som redan är bredd-begränsad.

---

### Tillstånd (States)

| Tillstånd | Border | Textfärg | Underline | Font-weight | Cursor |
|---|---|---|---|---|---|
| **Enabled** (ej sista) | `1px solid border-action-3` | `text-tertiary` (#737373) | Nej | Regular (400) | pointer |
| **Hover** (ej sista) | `1px solid border-action-3` | `text-action-primary` (#000000) | **Ja** | Regular | pointer |
| **Active** (sista/aktuell sida) | `1px solid border-action-3` | `text-primary` (#000000) | Nej | Bold (700) | default |

> Hover byter **enbart** textfärg (till `text-action-primary`) och lägger till understrykning — boxens border och bakgrund (transparent) ändras inte.
> `Active`-brödsmulan får **aldrig** hover-understrykning — den är inte klickbar och saknar `href`/klickhanterare.

---

### CSS-mall

```css
.breadcrumb { padding: 0 var(--px-page) 0; }
.breadcrumb__bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 16px 0;
}
.breadcrumb-item {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--color-border-action-3);
  padding: 6px 7px;
  background: none;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 12px;
  letter-spacing: 0.24px;
  color: var(--color-text-tertiary);
  font-feature-settings: 'ss02' 1, 'ss03' 1;
  transition: color var(--duration-fast-3) var(--ease-standard);
}
.breadcrumb-item:hover {
  color: var(--color-text-action-primary);
  text-decoration: underline;
}
.breadcrumb-item--active {
  font-weight: 700;
  color: var(--color-text-primary);
  cursor: default;
}
.breadcrumb-item--active:hover { text-decoration: none; }
.breadcrumb-sep {
  flex-shrink: 0;
  width: 4px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.28px;
}

/* md: Desktop Small */
@media (min-width: 769px) {
  .breadcrumb { padding-bottom: 8px; }
  .breadcrumb-item { padding: 9px 10px; font-size: 14px; line-height: 14px; letter-spacing: 0.28px; }
  .breadcrumb-sep { height: 32px; }
}
/* lg + xl: Desktop */
@media (min-width: 1024px) {
  .breadcrumb { padding-bottom: 16px; }
}

/* Komponenten har inbyggd spacing — nollställ top-paddingen på en direkt
   efterföljande sektion/titelblock (se Section-regel 4 nedan). */
.breadcrumb + .main-content,
.breadcrumb + .section,
.breadcrumb + .section--first {
  padding-top: 0;
}
```

### HTML-exempel

```html
<!-- 2 nivåer -->
<nav class="breadcrumb" aria-label="Brödsmulor">
  <div class="breadcrumb__bar">
    <a href="#" class="breadcrumb-item">Hem</a>
    <span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-item breadcrumb-item--active" aria-current="page">Recensioner</span>
  </div>
</nav>

<!-- Flera nivåer (PLP/PDP) -->
<nav class="breadcrumb" aria-label="Brödsmulor">
  <div class="breadcrumb__bar">
    <a href="#" class="breadcrumb-item">Hem</a>
    <span class="breadcrumb-sep">/</span>
    <a href="#" class="breadcrumb-item">Kläder och skydd</a>
    <span class="breadcrumb-sep">/</span>
    <a href="#" class="breadcrumb-item">Arbetsbyxor</a>
    <span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-item breadcrumb-item--active" aria-current="page">Hantverksbyxor</span>
  </div>
</nav>
```

### Regler

1. **IMPORTANT — Placering & spacing:** Breadcrumb placeras alltid direkt under headern, som första element i `.page`, **före** sidans titelblock (`.main-content`) eller första `.section`. Eftersom komponenten har inbyggd vertikal padding ska det direkt efterföljande elementet nollställa sin top-padding (`.breadcrumb + .main-content { padding-top: 0; }`) — enligt Section-komponentens regel om "Första sektionen med angränsande komponent med inbyggd spacing".
2. **IMPORTANT — Horisontell padding:** Använd alltid `var(--px-page)`, aldrig `var(--px-full)` eller hårdkodade pixlar, eftersom breadcrumben ligger inuti den breddbegränsade `.page`-wrappern.
3. Varje brödsmula är en **kantad box** — aldrig understruken länktext, aldrig ikon/chevron mellan stegen. Avskiljaren är alltid tecknet `/`.
4. Endast den **sista** brödsmulan får `.breadcrumb-item--active` (fetstil, svart, `aria-current="page"`, ej klickbar/utan `href`). Alla föregående ska vara riktiga länkar (`<a>`).
5. Storlek (crumb-padding, textstorlek, avskiljarhöjd) styrs enbart av breakpoint enligt tabellen ovan — hårdkoda aldrig en annan storlek för en enskild sida.
6. `aria-label="Brödsmulor"` på `<nav>` samt `aria-current="page"` på den aktiva brödsmulan är obligatoriska för tillgänglighet.
7. **Bakgrund:** `.breadcrumb` sätter **ingen** egen bakgrundsfärg — den ligger mot `body`s bakgrund, som skiljer sig per sidtyp: publika/utloggade sidor (`template.html`) har `background-primary` (vit); sidor under Mina sidor (`mypages-template.html`, samma som övriga my-pages-sidor) har `background-secondary` (grå) som standard — det är avsiktligt, inte ett fel.

---
