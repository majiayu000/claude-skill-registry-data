---
name: inline-notification
description: Använd när du bygger en inline-notifikation som ska ligga kvar i sidkontext tills användaren agerar eller tillståndet förändras — inte kortlivad feedback (använd toast-system för det).
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikation – System Inline (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=13377-35659

### Används när
- Feedback eller statusinformation hör direkt till ett specifikt avsnitt, formulär eller innehållsblock på sidan
- Meddelandet ska vara synligt tills användaren agerar eller tillståndet förändras (försvinner **inte** automatiskt)
- Kontextuell information som inte blockerar resten av gränssnittet

### Används INTE när
- Kortlivat svar på en användaråtgärd → använd **Toast** istället
- Åtgärden kräver bekräftelse → använd **Modal**
- Meddelandet gäller ett enskilt formulärfält → använd `form-helper--error`

---

### Storlekar

| Storlek | Höjd | Padding | Ikon |
|---|---|---|---|
| **Medium** | 48px | `12px` alla sidor | 24px |
| **Small** | 32px | `4px` alla sidor | 20px |

---

### Varianter

#### Emphasis
| Emphasis | Bakgrund | Vänster border | Övriga borders |
|---|---|---|---|
| **System Strong** | Statusfärgens svaga bakgrund (se tabell) | `2px solid [statusfärg]` | `1px solid [statusfärg-weak]` |
| **System Weak** | `#ffffff` (`surface-raised-primary`) | `2px solid [statusfärg]` | `1px solid [statusfärg-weak]` |

#### Status + färger

| Status | Vänster border / Ikon | Strong-bakgrund | Höger/topp/botten border | Material Symbol |
|---|---|---|---|---|
| **Informational** | `#0066ff` | `#e2f1ff` (`surface-information-weaker`) | `#d0e9ff` | `info` |
| **Error** | `#d90000` | `#ffebeb` (`surface-danger-weaker`) | `#ffbdc0` | `error` |
| **Success** | `#248616` | `#edffe7` (`surface-success-weaker`) | `#daf6d0` | `check_circle` |
| **Warning** | `#fac000` | `#fff5c2` (`surface-warning-weaker`) | `#ffe167` | `warning` |
| **Informational E-Com** | `#0066ff` | — (alltid Weak, `#ffffff`) | **ingen** | Valfri (ex. `local_shipping`) |

> **Informational E-Com** har alltid vit bakgrund (`surface-raised-primary`, `#ffffff`) och **ingen** höger/topp/botten-border — bara den 2px vänstra blå. Ikonen är ej reserverad och väljs kontextuellt från galleri.

#### Layout-varianter
| Variant | Innehåll |
|---|---|
| **Default** | Statusikon + [Titel (valfri) + Brödtext] + Stäng-knapp |
| **Actionable** | Som Default + knappar och/eller text-länk under texten (indrag `32px`) |

---

### Anatomi

```
[2px border] [Statusikon] [TITEL (VALFRI): Brödtext.]   [✕ stäng 20px]
             [Secondary-knapp] [Primary-knapp]            ← Actionable
             [Text link]                                   ← Actionable
```

- **Vänster border**: `2px solid [statusfärg]`, full höjd
- **Höger/topp/botten border**: `1px solid [statusfärg-weak]`
- **Padding**: `12px` (Medium) / `4px` (Small)
- **Ikon**: Material Symbols Outlined, 24px (Medium) / 20px (Small), färg = statusfärg
- **Gap** mellan ikon och text: `8px`
- **Titel** (valfri): `label-sm` — 14px, Bold, uppercase, `#000`, `letter-spacing: 0.56px`
- **Brödtext**: `body-sm` — 14px/20px, Regular, `#000`, `letter-spacing: 0.28px`
- **Stäng-knapp**: Blank xs, `close`-ikon 20px, `padding: 2px`
- **Shadow**: `elevation-b-20` = `0px 1px 3px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)`

#### Actionable — Action Group
- Indrag: `padding-left: 32px`
- Knappar: `gap: 8px`, `padding-top: 16px` från texten
- Knappstorlek: xs (höjd 32px)
- Text-länk: `body-sm` understruken, `padding-top: 8px` under knapparna

---

### CSS-mall

```css
/* Wrapper */
.inline-notification {
  display: flex;
  align-items: stretch;
  box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-20 */
}

/* Base — vänster border + bakgrund */
.inline-notification__base {
  display: flex;
  align-items: center;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.inline-notification__left-border {
  width: 2px;
  align-self: stretch;
  flex-shrink: 0;
}

/* Container med höger/topp/botten border */
.inline-notification__container {
  flex: 1;
  border-width: 1px 1px 1px 0;
  border-style: solid;
}

.inline-notification__inner {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 12px;        /* Medium */
  width: 100%;
  box-sizing: border-box;
}

/* Small */
.inline-notification--small .inline-notification__inner {
  padding: 4px;
}

/* Header-rad: ikon + text + stäng */
.inline-notification__header {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  width: 100%;
}

.inline-notification__icon {
  font-size: 24px;        /* Medium */
  flex-shrink: 0;
}
.inline-notification--small .inline-notification__icon {
  font-size: 20px;
}

.inline-notification__text {
  flex: 1;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;        /* body-sm */
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.28px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
  padding-top: 2px;
}

.inline-notification__title {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.56px;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

.inline-notification__close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 20px;
  color: var(--color-text-primary);
}

/* Actionable — Action Group */
.inline-notification__actions {
  padding-left: 32px;
  width: 100%;
  box-sizing: border-box;
}

.inline-notification__btn-group {
  display: flex;
  gap: 8px;
  align-items: center;
  padding-top: 16px;
  width: 100%;
}

.inline-notification__link {
  padding-top: 8px;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.28px;
  color: var(--color-text-primary);
  text-decoration: underline;
  cursor: pointer;
}

/* Status — Informational */
.inline-notification--info.inline-notification--strong { background: var(--color-surface-information-weaker); }
.inline-notification--info .inline-notification__left-border { background: var(--color-surface-information-default); }
.inline-notification--info .inline-notification__container { border-color: var(--color-border-information-weak); }
.inline-notification--info .inline-notification__icon { color: var(--color-surface-information-default); }

/* Status — Error */
.inline-notification--error.inline-notification--strong { background: var(--color-surface-danger-weaker); }
.inline-notification--error .inline-notification__left-border { background: var(--color-surface-danger-default); }
.inline-notification--error .inline-notification__container { border-color: var(--color-border-danger-weak); }
.inline-notification--error .inline-notification__icon { color: var(--color-surface-danger-default); }

/* Status — Success */
.inline-notification--success.inline-notification--strong { background: var(--color-surface-success-weaker); }
.inline-notification--success .inline-notification__left-border { background: var(--color-surface-success-default); }
.inline-notification--success .inline-notification__container { border-color: var(--color-border-success-weak); }
.inline-notification--success .inline-notification__icon { color: var(--color-surface-success-default); }

/* Status — Warning */
.inline-notification--warning.inline-notification--strong { background: var(--color-surface-warning-weaker); }
.inline-notification--warning .inline-notification__left-border { background: var(--color-surface-warning-default); }
.inline-notification--warning .inline-notification__container { border-color: var(--color-border-warning-weak); }
.inline-notification--warning .inline-notification__icon { color: var(--color-surface-warning-default); }

/* Weak — vit bakgrund */
.inline-notification--weak { background: var(--color-surface-raised-primary); }

/* Informational E-Com — vit bakgrund, ingen höger/topp/botten-border */
.inline-notification--ecom .inline-notification__container {
  border: none;
}
.inline-notification--ecom .inline-notification__left-border { background: var(--color-surface-information-default); }
.inline-notification--ecom .inline-notification__icon { color: var(--color-surface-information-default); }
```

### HTML-exempel (Default, Informational, System Strong, Medium)

```html
<div class="inline-notification inline-notification--info inline-notification--strong">
  <div class="inline-notification__base">
    <div class="inline-notification__left-border"></div>
    <div class="inline-notification__container">
      <div class="inline-notification__inner">
        <div class="inline-notification__header">
          <span class="material-symbols-outlined inline-notification__icon">info</span>
          <p class="inline-notification__text">
            <span class="inline-notification__title">Titel (valfri):</span> Brödtext.
          </p>
          <button class="inline-notification__close" aria-label="Stäng">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

---
