---
name: toast-system
description: Använd när du bygger en systemgenererad Toast-notifikation — kortlivad, tidsbaserad feedback på en användaråtgärd (spara/skicka/radera) som glider in/ut och auto-stänger.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikation – System Toast (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=13377-29321

### Används när
- Svar på en användaråtgärd (spara, skicka, radera)
- Systemhändelse som kräver användarens uppmärksamhet
- Kortlivat meddelande som inte blockerar gränssnittet

### Används INTE när
- Felmeddelande gäller ett enskilt formulärfält → använd `form-helper--error` istället
- Meddelandet är permanent → använd inline-notifikation eller banner
- Åtgärden kräver bekräftelse → använd Modal

---

### Varianter

#### Emphasis
| Emphasis | Bakgrund | Vänster border |
|---|---|---|
| **System Strong** | Statusfärgens svaga bakgrund (se tabell nedan) | `2px solid [statusfärg]` |
| **System Weak** | `#ffffff` (`surface-raised-primary`) | `2px solid [statusfärg]` |

#### Status + färger

| Status | Border / Ikon-färg | Strong-bakgrund | Material Symbol |
|---|---|---|---|
| **Informational** | `#0066ff` | `#e2f1ff` (`surface-information-weaker`) | `info` |
| **Error** | `#d90000` | `#ffebeb` (`surface-danger-weaker`) | `error` |
| **Success** | `#248616` | `#edffe7` (`surface-success-weaker`) | `check_circle` |
| **Warning** | `#fac000` | `#fff5c2` (`surface-warning-weaker`) | `warning_amber` |

#### Layout-varianter
| Variant | Innehåll |
|---|---|
| **Default** | Statusikon + [Titel (valfri) + Brödtext] + Stäng-knapp |
| **Actionable** | Som Default + en eller flera Blank-knappar under texten |

---

### Anatomi

```
[Statusikon 24px] [Titel (valfri) — title-sm]   [✕ stäng 20px]
                  [Brödtext — body-md           ]
                  [Blank-knapp (endast Actionable)]
```

- **Vänster border**: `2px solid [statusfärg]`, full höjd
- **Padding**: `16px` inuti, `8px` gap mellan ikon och textblock
- **Stäng-knapp**: Blank xs, `close`-ikon 20px, `padding: 2px`
- **Shadow**: `elevation-b-80` = `0px 0px 1px rgba(0,0,0,0.05), 0px 8px 16px rgba(0,0,0,0.10)`

---

### Typografi

| Element | Token | Värde |
|---|---|---|
| Titel (valfri) | `title-sm` | 16px/18px, Bold, 0px tracking, `text-primary` (#000) |
| Brödtext | `body-md` | 16px/24px, Regular, 0.32px tracking, `text-primary` (#000) |

---

### CSS-mall

```css
.toast {
  display: flex;
  flex-direction: column;
  width: 375px;
  box-shadow: 0px 8px 16px rgba(0,0,0,0.10), 0px 0px 1px rgba(0,0,0,0.05); /* elevation-b-80 */
}

.toast__inner {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  gap: 8px;
  border-left: 2px solid var(--status-color);
  position: relative;
}

/* System Strong — färgad bakgrund */
.toast--strong.toast--info    { background: var(--color-surface-information-weaker); --status-color: var(--color-surface-information-default); }
.toast--strong.toast--error   { background: var(--color-surface-danger-weaker);      --status-color: var(--color-surface-danger-default); }
.toast--strong.toast--success { background: var(--color-surface-success-weaker);     --status-color: var(--color-surface-success-default); }
.toast--strong.toast--warning { background: var(--color-surface-warning-weaker);     --status-color: var(--color-surface-warning-default); }

/* System Weak — vit bakgrund */
.toast--weak.toast--info    { background: var(--color-surface-raised-primary); --status-color: var(--color-surface-information-default); }
.toast--weak.toast--error   { background: var(--color-surface-raised-primary); --status-color: var(--color-surface-danger-default); }
.toast--weak.toast--success { background: var(--color-surface-raised-primary); --status-color: var(--color-surface-success-default); }
.toast--weak.toast--warning { background: var(--color-surface-raised-primary); --status-color: var(--color-surface-warning-default); }

.toast__icon {
  font-size: 24px;
  color: var(--status-color);
  flex-shrink: 0;
}

.toast__body { flex: 1; display: flex; flex-direction: column; gap: 2px; }

.toast__title {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;
  font-weight: 700;
  line-height: 18px;
  letter-spacing: 0px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

.toast__text {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.toast__close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 20px;
  color: var(--color-text-primary);
}
```

---

### Position per breakpoint

Toasten är `position: fixed`. Glider alltid in från höger — utom på `xs` där den kommer uppifrån.

| Breakpoint | Top | Höger | Vänster | Bredd |
|---|---|---|---|---|
| `lg` (1024px+) | `40px` | `40px` | auto | `375px` |
| `md` (769–1023px) | `32px` | `32px` | auto | `375px` |
| `sm` (640–768px) | `32px` | `32px` | auto | `375px` |
| `xs` (0–639px) | `0px` | `0px` | `0px` | `100vw` (fyller hela viewport-bredden) |

> På `xs` animeras toasten in uppifrån istället för från höger. Bredden är alltid `375px` på sm och uppåt, och fyller hela viewport-bredden på xs.

```css
.toast-container {
  position: fixed;
  z-index: 9999;
  top: 40px;
  right: 40px;
  width: 375px;
}

@media (max-width: 1023px) {
  .toast-container { top: 32px; right: 32px; }
}

@media (max-width: 639px) {
  .toast-container {
    top: 0;
    right: 0;
    left: 0;
    width: 100vw;
  }
}
```

---

### Animation

| Egenskap | Värde |
|---|---|
| Riktning in | Från höger (`xs`: uppifrån) |
| Easing in | `cubic-bezier(0.16, 0, 0.16, 1)` (`ease-decelerate-emphasized`) |
| Riktning ut | Till höger (`xs`: uppåt) |
| Easing ut | `cubic-bezier(0.36, 0.09, 1, 0.58)` (`ease-accelerate-generic`) |
| Duration | `300ms` |
| Auto-hide | `4000ms` |

**Dismiss-triggers:** stäng-knapp, klick utanför toasten, auto-hide. Alla tre ska köra exit-animationen — anropa aldrig `remove()` direkt utan att animera ut.

> Starta click-outside-lyssnaren med `setTimeout(..., 0)` så att klicket som skapade toasten (t.ex. bekräfta-knapp i modal) inte stänger den omedelbart.

```css
/* Enter — från höger (lg/md/sm), ingen fade */
@keyframes toast-slide-in {
  from { transform: translateX(calc(100% + 40px)); }
  to   { transform: translateX(0); }
}
/* Exit — till höger (lg/md/sm), ingen fade */
@keyframes toast-slide-out {
  from { transform: translateX(0); }
  to   { transform: translateX(calc(100% + 40px)); }
}

/* Enter — uppifrån (xs), ingen fade */
@keyframes toast-slide-in-top {
  from { transform: translateY(-100%); }
  to   { transform: translateY(0); }
}
/* Exit — uppåt (xs), ingen fade */
@keyframes toast-slide-out-top {
  from { transform: translateY(0); }
  to   { transform: translateY(-100%); }
}
```

```js
function showToast(/* ... */) {
  var isXs = window.innerWidth <= 639;
  var dismissed = false;
  var autoTimer = null;

  // Skapa och positionera toast...
  // xs: top:0; left:0; right:0; width:100vw; animation: toast-slide-in-top ...
  // sm+: top:40px; right:40px; width:375px; animation: toast-slide-in ...

  function dismiss() {
    if (dismissed) return;
    dismissed = true;
    clearTimeout(autoTimer);
    document.removeEventListener('click', outsideClick);
    toast.style.animation = isXs
      ? 'toast-slide-out-top 300ms cubic-bezier(.36,.09,1,.58) forwards'
      : 'toast-slide-out 300ms cubic-bezier(.36,.09,1,.58) forwards';
    setTimeout(function(){ toast.remove(); }, 300);
  }

  function outsideClick(e) {
    if (!toast.contains(e.target)) dismiss();
  }

  closeBtn.addEventListener('click', dismiss);
  document.body.appendChild(toast);
  setTimeout(function(){ document.addEventListener('click', outsideClick); }, 0);
  autoTimer = setTimeout(dismiss, 4000);
}
```

---
