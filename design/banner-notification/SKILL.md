---
name: banner-notification
description: Använd när du bygger en sidövergripande banner-notifikation längst upp på sidan (drift/underhåll/kampanj), inklusive System Extra Strong (admin-impersonation) och E-Com Action (kampanjbanner).
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikation – System Banner (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=13377-41997

### Används när
- Sidövergripande meddelanden som rör hela sidan eller systemet (underhåll, driftstörning, kampanj)
- Meddelandet ska vara synligt tills användaren stänger det eller tillståndet förändras — försvinner **inte** automatiskt
- Placeras högst upp på sidan, **ovanför** allt sidinnehåll

### Används INTE när
- Feedback på en specifik handling → använd **Toast** (kortlivad) eller **System Inline** (kontextuell)
- Meddelandet gäller ett enskilt formulärfält → använd `form-helper--error`
- Blockerar åtgärden och kräver bekräftelse → använd **Modal**

---

### Storlek och layout

Bannern har **en storlek (1-Size)** och sträcker sig alltid till **full bredd** av sin behållare eller viewport. Ingen fast bredd sätts — bannern är `width: 100%`.

| Egenskap | Desktop (`md:` 769px+) | Mobile/Tablet (`xs`/`sm` ≤768px) |
|---|---|---|
| Padding | `12px` alla sidor | `8px` alla sidor |
| Ikon | 24px | 24px |
| Titel-text | `label-sm` Desktop: 14px, 0.56px, Bold, uppercase | `label-sm` Mobile: 12px, 0.48px, Bold, uppercase |
| Brödtext | `body-sm` Desktop: 14px/20px, 0.28px, Regular | Mobile: 12px/18px, 0.24px, Regular |

---

### Varianter

#### Emphasis — System-varianter

| Emphasis | Bakgrund | Vänster border | Övriga borders | Textfärg | Layout |
|---|---|---|---|---|---|
| **System Strong** | Statusfärgens svaga bakgrund | `2px solid [statusfärg]` | `1px solid [statusfärg-weak]` | `#000` | Vänsterjusterad |
| **System Weak** | `#ffffff` | `2px solid [statusfärg]` | `1px solid [statusfärg-weak]` | `#000` | Vänsterjusterad |
| **System Extra Strong** | Statusfärgen (solid) | — ingen border — | — ingen border — | `#ffffff` | Centrerad |

> **System Extra Strong** används för bannrar med hög prioritet som måste synas direkt — t.ex. adminimpersonation ("Du agerar som [användare]") eller kritiska driftvarningar. Hela bakgrunden fylls med statusfärgen och texten är vit. Innehållet centreras horisontellt. Kan innehålla en textlänk (understruken, vit).
>
> **Type: Banner** (inte System Inline). Höjd: `48px` desktop (`min-height`), `40px` mobil/tablet (`min-height`). Padding: `8px` desktop, `8px` vertikalt / `16px` horisontellt mobil. Ikon: `info` (FILL 1, filled), 24px, vit. Mobil: vänsterjusterat, text radbryts, gap text↔länk `16px`. Desktop: centrerat, `white-space: nowrap`, gap text↔länk `4px`. "LOGGA UT"-länk: `body-sm--bold-underline` (Bold 700, understruken).

#### Status + färger (identiska med System Inline och Toast)

| Status | Solid (Extra Strong) | Svag (Strong bakgrund) | Border-weak | Ikon-färg | Material Symbol |
|---|---|---|---|---|---|
| **Informational** | `#0066ff` | `#e2f1ff` | `#d0e9ff` | `#0066ff` | `info` |
| **Error** | `#d90000` | `#ffebeb` | `#ffbdc0` | `#d90000` | `error` |
| **Success** | `#248616` | `#edffe7` | `#daf6d0` | `#248616` | `check_circle` |
| **Warning** | `#fac000` | `#fff5c2` | `#ffe167` | `#fac000` | `warning_amber` |

---

#### E-Com Action (kampanjbanner)

Används **enbart** för varumärkesdrivna kampanjbanners — inte för systemstatus. Inget statusikon-system, ingen vänsterborder. Innehållet centreras horisontellt med en varumärkesikon (24px), etikett och valfri textlänk.

| Emphasis | Bakgrund | Textfärg | Ikon |
|---|---|---|---|
| **Brand Strong – Tools** | `#cd1125` (brand röd) | `#ffffff` | Varumärkesikon, vit |
| **Brand Strong – Swedol** | `#c7d300` (brand lime) | `#000000` | Varumärkesikon, svart |
| **Brand B/W** | `#000000` | `#ffffff` | Varumärkesikon, vit |
| **Brand W/B** | `#ffffff` | `#000000` | Varumärkesikon, svart |
| **Brand Weak – Tools** | Ljus brand-bakgrund | `#000000` | Varumärkesikon, svart |
| **Brand Weak – Swedol** | Ljus lime-bakgrund | `#000000` | Varumärkesikon, svart |

- **Typografi**: Titel = `label-md` desktop (16px/16px, 0.48px, Bold, uppercase). Textlänk = `body-md` (16px/24px, 0.32px, Regular, underline).
- **Gap** ikon–text: `8px`. Gap titel–länk: `4px`.
- **Padding**: `8px` alla sidor (desktop och mobil).
- **Höjd**: 40px (desktop och mobil).

---

### Anatomi

**System Strong / System Weak:**
```
[2px border] [Statusikon 24px] [TITEL (VALFRI): Brödtext...]   [✕ stäng 20px]
```

**System Extra Strong:**
```
          [Statusikon 24px] [Brödtext...  ETIKETT  Textlänk]   [✕ stäng 20px]
          ← hela bakgrunden är statusfärgen, allt är centrerat →
```

**E-Com Action:**
```
          [Varumärkesikon 24px] [TITEL - Textlänk]             [✕ stäng 20px]
          ← hela bakgrunden är brandfärgen, allt är centrerat →
```

- **System Strong/Weak**: vänster border `2px solid [statusfärg]`, övriga borders `1px solid [statusfärg-weak]`
- **System Extra Strong**: ingen border alls — bakgrundsblocket är hela statusfärgen
- **Gap** ikon–text: `8px`. Gap titel–länk (E-Com/Extra Strong): `4px`
- **Stäng-knapp**: Blank xs, `close`-ikon 20px, `padding: 2px`
- **Shadow**: `elevation-b-20` = `0px 1px 3px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)`

---

### CSS-mall

```css
.banner-notification {
  display: flex;
  align-items: stretch;
  width: 100%;
  box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-20 */
}

.banner-notification__base {
  display: flex;
  align-items: center;
  width: 100%;
  overflow: hidden;
}

.banner-notification__left-border {
  width: 2px;
  align-self: stretch;
  flex-shrink: 0;
}

.banner-notification__container {
  flex: 1;
  border-width: 1px 1px 1px 0;
  border-style: solid;
}

.banner-notification__inner {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 12px;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .banner-notification__inner { padding: 8px; }
}

.banner-notification__content {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  flex: 1;
}

.banner-notification__icon {
  font-size: 24px;
  flex-shrink: 0;
  padding-top: 2px;
}

.banner-notification__text {
  flex: 1;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.28px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.banner-notification__title {
  font-weight: 700;
  font-size: 14px;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .banner-notification__text { font-size: 12px; line-height: 18px; letter-spacing: 0.24px; }
  .banner-notification__title { font-size: 12px; line-height: 12px; letter-spacing: 0.48px; }
}

.banner-notification__close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 20px;
  color: var(--color-text-primary);
}

/* Status — Informational */
.banner-notification--info.banner-notification--strong { background: var(--color-surface-information-weaker); }
.banner-notification--info .banner-notification__left-border { background: var(--color-surface-information-default); }
.banner-notification--info .banner-notification__container { border-color: var(--color-border-information-weak); }
.banner-notification--info .banner-notification__icon { color: var(--color-surface-information-default); }

/* Status — Error */
.banner-notification--error.banner-notification--strong { background: var(--color-surface-danger-weaker); }
.banner-notification--error .banner-notification__left-border { background: var(--color-surface-danger-default); }
.banner-notification--error .banner-notification__container { border-color: var(--color-border-danger-weak); }
.banner-notification--error .banner-notification__icon { color: var(--color-surface-danger-default); }

/* Status — Success */
.banner-notification--success.banner-notification--strong { background: var(--color-surface-success-weaker); }
.banner-notification--success .banner-notification__left-border { background: var(--color-surface-success-default); }
.banner-notification--success .banner-notification__container { border-color: var(--color-border-success-weak); }
.banner-notification--success .banner-notification__icon { color: var(--color-surface-success-default); }

/* Status — Warning */
.banner-notification--warning.banner-notification--strong { background: var(--color-surface-warning-weaker); }
.banner-notification--warning .banner-notification__left-border { background: var(--color-surface-warning-default); }
.banner-notification--warning .banner-notification__container { border-color: var(--color-border-warning-weak); }
.banner-notification--warning .banner-notification__icon { color: var(--color-surface-warning-default); }

/* Weak — vit bakgrund */
.banner-notification--weak { background: var(--color-surface-raised-primary); }

/* Extra Strong — solid statusfärg, vit text, centrerat */
.banner-notification--extra-strong {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 8px;
  gap: 8px;
  box-sizing: border-box;
  box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-20 */
}

.banner-notification--extra-strong .banner-notification__content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.banner-notification--extra-strong .banner-notification__message {
  display: flex;
  align-items: center;
  gap: 4px;
}

.banner-notification--extra-strong .banner-notification__icon,
.banner-notification--extra-strong .banner-notification__text,
.banner-notification--extra-strong .banner-notification__close { color: var(--color-text-primary-inverted); }

.banner-notification--extra-strong .banner-notification__text {
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.28px;
  white-space: nowrap;
}

.banner-notification--extra-strong .banner-notification__title {
  font-weight: 700;
  font-size: 14px;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
}

.banner-notification--extra-strong .banner-notification__link {
  color: var(--color-text-primary-inverted);
  text-decoration: underline;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.28px;
  cursor: pointer;
}

/* Extra Strong — status-bakgrunder */
.banner-notification--extra-strong.banner-notification--info    { background: var(--color-surface-information-default); }
.banner-notification--extra-strong.banner-notification--error   { background: var(--color-surface-danger-default); }
.banner-notification--extra-strong.banner-notification--success { background: var(--color-surface-success-default); }
.banner-notification--extra-strong.banner-notification--warning { background: var(--color-surface-warning-default); }

/* E-Com Action — kampanjbanner, centrerat, ingen border */
.banner-notification--ecom-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 40px;
  padding: 8px;
  gap: 8px;
  box-sizing: border-box;
  box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-20 */
}

.banner-notification--ecom-action .banner-notification__content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex: 1;
}

.banner-notification--ecom-action .banner-notification__message {
  display: flex;
  align-items: center;
  gap: 4px;
}

.banner-notification--ecom-action .banner-notification__title {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;   /* label-md */
  font-weight: 700;
  line-height: 16px;
  letter-spacing: 0.48px;
  text-transform: uppercase;
  white-space: nowrap;
}

.banner-notification--ecom-action .banner-notification__link {
  font-size: 16px;   /* body-md */
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  text-decoration: underline;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

/* Variantfärger (E-Com Action) */
.banner-notification--ecom-tools-strong { background: var(--color-accent-default); color: var(--color-text-primary-inverted); } /* brand-specific: Tools */
.banner-notification--ecom-tools-strong .banner-notification__link { color: var(--color-text-primary-inverted); }
.banner-notification--ecom-swedol-strong { background: var(--color-accent-default); color: var(--color-text-primary); } /* brand-specific: Swedol */
.banner-notification--ecom-bw { background: var(--color-surface-100); color: var(--color-text-primary-inverted); }
.banner-notification--ecom-bw .banner-notification__link { color: var(--color-text-primary-inverted); }
.banner-notification--ecom-wb { background: var(--color-surface-raised-primary); color: var(--color-text-primary); }
```

### HTML-exempel (Informational, System Strong)

```html
<div class="banner-notification banner-notification--info banner-notification--strong">
  <div class="banner-notification__base">
    <div class="banner-notification__left-border"></div>
    <div class="banner-notification__container">
      <div class="banner-notification__inner">
        <div class="banner-notification__content">
          <span class="material-symbols-outlined banner-notification__icon">info</span>
          <p class="banner-notification__text">
            <span class="banner-notification__title">Titel (valfri):</span> Brödtext.
          </p>
        </div>
        <button class="banner-notification__close" aria-label="Stäng">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>
    </div>
  </div>
</div>
```

### HTML-exempel (System Extra Strong — admin-impersonation)

```html
<div class="banner-notification banner-notification--extra-strong banner-notification--info">
  <div class="banner-notification__content">
    <span class="material-symbols-outlined banner-notification__icon">info</span>
    <div class="banner-notification__message">
      <p class="banner-notification__text">
        Din roll är <span class="banner-notification__title">Administratör</span>
        och du agerar tillfälligt som <strong>Alban Beluli</strong>.
      </p>
      <a href="#" class="banner-notification__link">LOGGA UT</a>
    </div>
  </div>
  <button class="banner-notification__close" aria-label="Stäng">
    <span class="material-symbols-outlined">close</span>
  </button>
</div>
```

### HTML-exempel (E-Com Action, Brand Strong – Tools)

```html
<div class="banner-notification banner-notification--ecom-action banner-notification--ecom-tools-strong">
  <div class="banner-notification__content">
    <span class="material-symbols-outlined banner-notification__icon">tools_power_drill</span>
    <div class="banner-notification__message">
      <p class="banner-notification__title">Kampanjtitel -</p>
      <a href="#" class="banner-notification__link">Textlänk</a>
    </div>
  </div>
  <button class="banner-notification__close" aria-label="Stäng">
    <span class="material-symbols-outlined">close</span>
  </button>
</div>
```

---
