---
name: tooltip
description: Använd när du lägger till en tooltip på en ikonknapp eller annat element utan synlig text — visas vid hover, aldrig vid tangentbordsfokus.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Tooltip (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=316-14656

Tooltips visas vid hover på ikontextlösa knappar och ger en kort etikett som förklarar knappens funktion. Används för **alla** breakpoints.

---

### Storlekar

| Storlek | Padding | Font | Line-height | Letter-spacing |
|---|---|---|---|---|
| **Small** | `8px 12px` | 14px, Regular | 20px | 0.28px |
| **Large** | `16px 24px` | 18px, Regular | 26px | 0.36px |

> Använd alltid **Small** för ikonknappar i verktygsrader och tabellrader.

---

### Utseende

| Egenskap | Värde |
|---|---|
| Bakgrund | `rgba(0,0,0,0.9)` (`surface-100` 90% opacitet) |
| Textfärg | `#ffffff` (`text-primary-inverted`) |
| Font | `Breuer Condensed Regular` |
| `font-feature-settings` | `'ss02' 1, 'ss03' 1, 'ss06' 1` |
| `white-space` | `nowrap` |
| Shadow | `elevation-b-40`: `0px 2px 4px rgba(0,0,0,0.10), 0px 0px 1px rgba(0,0,0,0.05)` |
| Beak | CSS-triangel, 6px hög, ~12.7px bred |

---

### Positioner

| Typ | Beskrivning | Beak-riktning |
|---|---|---|
| **Top** | Tooltip ovanför elementet | Beak pekar nedåt (under tooltip-blocket) |
| **Bottom** | Tooltip nedanför elementet | Beak pekar uppåt (ovanför tooltip-blocket) |
| **Left** | Tooltip till vänster | Beak pekar höger (höger sida av tooltip) |
| **Right** | Tooltip till höger | Beak pekar vänster (vänster sida av tooltip) |
| **Left side top/bottom** | Tooltip vänsterjusterad med offset | Beak vid topp/botten |
| **Right side top/bottom** | Tooltip högerjusterad med offset | Beak vid topp/botten |

> Välj position baserat på var det finns utrymme. Standardval: **Bottom** för knappar i verktygsrader (utrymme nedanför), **Top** för knappar i tabellrader (utrymme ovanför).

---

### Interaktion

- Tooltip visas vid **hover** (CSS `opacity: 1` via `.tooltip-wrap:hover .tooltip`).
- Easing: `motion-ease-standard` (`cubic-bezier(.35,0,.35,1)`), `duration-fast-2` (`100ms`).
- Aldrig synlig vid tangentbordsnavigering (`:focus`) — enbart hover.
- `pointer-events: none` på tooltip-elementet så det inte stör musinteraktion.

---

### HTML-struktur

```html
<!-- Knapp med Bottom-tooltip -->
<div class="tooltip-wrap">
  <button class="action-btn" aria-label="Lägg till användare">
    <span class="ms">person_add</span>
  </button>
  <span class="tooltip tooltip--bottom">Lägg till användare</span>
</div>

<!-- Knapp med Top-tooltip -->
<div class="tooltip-wrap">
  <button class="btn-row-action" aria-label="Redigera">
    <span class="ms">edit</span>
  </button>
  <span class="tooltip tooltip--top">Redigera</span>
</div>
```

> `aria-label` på knappen är obligatorisk och ska ha samma text som tooltip-innehållet.

---

### CSS-mall

```css
.tooltip-wrap {
  position: relative;
  display: inline-flex;
}

.tooltip {
  position: absolute;
  z-index: 300;
  background: rgba(0,0,0,0.9);
  color: #fff;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-size: 14px;        /* Small */
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.28px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 100ms cubic-bezier(.35,0,.35,1); /* duration-fast-2, ease-standard */
  box-shadow: 0px 2px 4px rgba(0,0,0,0.10), 0px 0px 1px rgba(0,0,0,0.05); /* elevation-b-40 */
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

/* Beak — delad bas för alla positioner */
.tooltip::before {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  border-left: 6.35px solid transparent;
  border-right: 6.35px solid transparent;
}

.tooltip-wrap:hover .tooltip { opacity: 1; }

/* Bottom — tooltip nedanför, beak pekar uppåt */
.tooltip--bottom {
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 12px;
}
.tooltip--bottom::before {
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-bottom: 6px solid rgba(0,0,0,0.9);
}

/* Top — tooltip ovanför, beak pekar nedåt */
.tooltip--top {
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 12px;
}
.tooltip--top::before {
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-top: 6px solid rgba(0,0,0,0.9);
}
```

---
