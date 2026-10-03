---
name: modal-ecom
description: Använd när du bygger en modal (E-Com Modal) som kräver bekräftelse eller ett aktivt val innan användaren kan fortsätta — inte för kortlivad feedback eller statusinformation i sidkontext.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikation – E-Com Modal (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=13377-48335

### Används när
- Åtgärden kräver bekräftelse eller ett aktivt val innan användaren kan fortsätta
- Viktig information måste presenteras utan att användaren kan missa den
- Innehållet kräver fokus och inte kan visas inline utan risk för missförstånd

### Används INTE när
- Kortlivad feedback på en handling → använd **Toast**
- Statusinformation i sidkontext → använd **System Inline**
- Sidövergripande meddelande → använd **System Banner**
- Felmeddelande gäller ett enskilt formulärfält → använd `form-helper--error`

---

### Storlekar och bredder per breakpoint

Desktop och Tablet: Modalen centreras i viewporten. Bakgrundsöverlagringen är `rgba(0,0,0,0.2)`.

| Storlek | Desktop (`md:` 769px+) | Tablet (`sm:` 640–768px) | Mobile (`xs:` 0–639px) |
|---|---|---|---|
| **Small** | `440px` | `440px` | Fyller hela viewporten |
| **Medium** | `600px` | `576px` | Fyller hela viewporten |
| **Large** | `705px` | `576px` | Fyller hela viewporten |

> Välj storlek utifrån mängden innehåll. Small för enkla bekräftelser, Medium/Large för mer komplex information.

> **xs (Mobile):** Modalen är **inte** centrerad. Den fyller hela viewporten: `position: fixed; top: 0; left: 0; width: 100%; height: 100dvh; padding: 16px`. Header+body-sektionen har `flex: 1` så knappar pinnas i botten. Stäng-knapp (`×`) visas i överkant.

---

### Anatomi

```
[LABEL (VALFRI)]                          [✕ stäng]
Title

Body text

[Avbryt]   [Primär åtgärd               ]
```

- **Overlay**: `position: fixed; inset: 0; background: rgba(0,0,0,0.2); z-index: 9998`
- **Modal-panel**: `position: fixed; z-index: 9999`, centrerad med `transform: translate(-50%, -50%); top: 50%; left: 50%`
- **Bakgrund**: `#ffffff` (`surface-raised-primary`)
- **Shadow**: `elevation-b-100` = `0px 16px 24px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)`
- **Gap** header-sektion: `8px` vertikalt
- **Header**: `gap: 12px` mellan Label+Title och stäng-knapp
- **Stäng-knapp**: Blank xs, `close`-ikon 20px, `padding: 2px`
- **Knappar i footer**: `gap: 8px`, Avbryt (Secondary xs, fast bredd) + Primär (Primary xs, `flex: 1`)

---

### Typografi per breakpoint

| Element | Desktop (`md:` 769px+) | Tablet + Mobile (`sm-xs` ≤768px) |
|---|---|---|
| **Label** (valfri) | `alt-label-sm`: 14px/14px, 0.56px, Medium(500), uppercase, `text-secondary` #4f4f4f | 12px/12px, 0.48px |
| **Title** | `title-md`: 20px/24px, 0px, Bold | `title-md`: 18px/22px, 0px, Bold |
| **Body text** | `body-md`: 16px/24px, 0.32px, Regular, `text-secondary` #4f4f4f | 16px/22px, 0.32px |
| **Knapp-text** | `label-sm`: 14px/14px, 0.56px, Bold, uppercase | `label-md`: 14px/14px, 0.48px, Bold, uppercase |

---

### Knappar per breakpoint

Knapparna i modalen följer **alltid** ECO Design Systems knappstorlekar:
- **Desktop (lg-md, ≥769px):** knappstorlek **xs** → `height: 32px`, `padding: 6px`, `label-sm` 14px, 0.56px
- **Tablet + Mobile (sm-xs, ≤768px):** knappstorlek **sm** → `height: 32px`, `padding: 6px`, `label-md` 14px, 0.48px

Båda varianter (Avbryt och Primär) är **alltid 32px höga** — oavsett breakpoint och knappvariant.

| | Desktop (`md:` 769px+) | Tablet + Mobile (`sm-xs` ≤768px) |
|---|---|---|
| Modal padding | `24px` | Tablet: `24px` / Mobile xs: `16px` |
| Button group top-gap | `pt-32px` | `pt-24px` |
| Knapp höjd (båda) | `32px` (xs-knapp) | `32px` (sm-knapp) |
| Knapp padding (båda) | `6px` | `6px` |
| Knapp letter-spacing | `0.56px` (label-sm) | `0.48px` (label-md) |

---

### CSS-mall

```css
/* Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.2);
  z-index: 9998;
}

/* Modal-panel */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  background: #ffffff;
  padding: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 16px 24px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-100 */
  width: 440px;       /* Small — default */
  max-width: 800px;
  min-width: 440px;
  box-sizing: border-box;
}

/* Storlekar */
.modal--medium { width: 600px; }
.modal--large  { width: 705px; }

/* Tablet */
@media (min-width: 640px) and (max-width: 768px) {
  .modal--medium,
  .modal--large { width: 576px; }
  .modal { padding: 24px; }
}

/* Mobile */
@media (max-width: 639px) {
  .modal,
  .modal--medium,
  .modal--large {
    width: 375px;
    min-width: 375px;
    max-width: calc(100vw - 32px);
    padding: 16px;
  }
}

/* Header */
.modal__header {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  width: 100%;
}

.modal__header-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  padding-top: 2px;
}

/* Label (valfri) */
.modal__label {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;          /* alt-label-sm Desktop */
  font-weight: 500;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  color: #4f4f4f;           /* text-secondary */
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .modal__label { font-size: 12px; line-height: 12px; letter-spacing: 0.48px; }
}

/* Title */
.modal__title {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 20px;          /* title-md Desktop */
  font-weight: 700;
  line-height: 24px;
  letter-spacing: 0px;
  color: #000;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .modal__title { font-size: 18px; line-height: 22px; }
}

/* Stäng-knapp */
.modal__close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 20px;
  color: #000;
}

/* Body */
.modal__body {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;          /* body-md */
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: #4f4f4f;           /* text-secondary */
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .modal__body { line-height: 22px; }
}

/* Button group */
.modal__footer {
  display: flex;
  gap: 8px;
  align-items: center;
  padding-top: 32px;
  width: 100%;
}

@media (max-width: 768px) {
  .modal__footer { padding-top: 24px; }
}

/* Avbryt — Secondary xs */
.modal__btn-cancel {
  flex-shrink: 0;
  background: transparent;
  border: 1px solid #000;
  cursor: pointer;
  padding: 6px;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  color: #000;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .modal__btn-cancel { padding: 8px; font-size: 16px; line-height: 16px; letter-spacing: 0.32px; }
}

@media (max-width: 639px) {
  .modal__btn-cancel { padding: 4px; font-size: 14px; line-height: 14px; letter-spacing: 0.42px; }
}

/* Primär åtgärd — Primary xs, flex: 1 */
.modal__btn-primary {
  flex: 1;
  background: #000;
  border: none;
  cursor: pointer;
  padding: 6px;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .modal__btn-primary { padding: 4px; font-size: 14px; line-height: 14px; letter-spacing: 0.42px; }
}
```

### HTML-exempel (Small, Desktop)

```html
<!-- Overlay -->
<div class="modal-overlay" onclick="closeModal()"></div>

<!-- Modal -->
<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal__header">
    <div class="modal__header-text">
      <p class="modal__label">Label (valfri)</p>
      <h2 class="modal__title" id="modal-title">Title</h2>
    </div>
    <button class="modal__close" aria-label="Stäng" onclick="closeModal()">
      <span class="material-symbols-outlined">close</span>
    </button>
  </div>
  <p class="modal__body">Body text.</p>
  <div class="modal__footer">
    <button class="modal__btn-cancel" onclick="closeModal()">Avbryt</button>
    <button class="modal__btn-primary">Bekräfta</button>
  </div>
</div>
```

---
