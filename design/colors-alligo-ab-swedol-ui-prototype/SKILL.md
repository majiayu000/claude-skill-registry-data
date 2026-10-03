---
name: colors
description: Använd när du väljer eller granskar färger/design-tokens — text-, ikon-, bakgrunds-, surface-, border- och statusfärger enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Färger – Semantiska Tokens (ECO Design System)

Alla tokens har prefixet `color/` i Figma. I CSS används de som hex-värden eller CSS-variabler (`--color-[token]`).

### Accent

| Token | Hex | Beskrivning |
|---|---|---|
| `accent-default` | `#c7d300` | Primär accentfärg (limegul). Används i Accent-knappar. |
| `accent-light` | `#f4f6cc` | Ljus accentfärg. Bakgrund för accentmarkeringar. |
| `accent-dark` | `#8b9400` | Mörk accentfärg. Hover-tillstånd för accent. |

```html
<!-- Exempel: Accent-knapp -->
<button style="background:#c7d300; color:#000;">Köp nu</button>
```

### Text

| Token | Hex | Beskrivning |
|---|---|---|
| `text-primary` | `#000000` | Primär text. Rubriker och huvudinnehåll. |
| `text-primary-inverted` | `#ffffff` | Primär text på mörk/svart bakgrund. |
| `text-secondary` | `#4f4f4f` | Hög betoning på ljus bakgrund. Sekundärt innehåll – minskar kognitiv belastning bredvid text-primary. |
| `text-secondary-inverted` | `#ffffffc7` | Sekundär text på mörk bakgrund. |
| `text-tertiary` | `#737373` | Medium betoning och hinttexter på vit bakgrund. |
| `text-tertiary-inverted` | `#999999` | Tertiär text på mörk bakgrund. |
| `text-disabled` | `#939595` | Inaktiverad text. |
| `text-price-customer` | `#00838f` | Kundpris (inloggad). |
| `text-price-guest` | `#d90000` | Gästpris (ej inloggad). |
| `text-price-on-black` | `#eb0000` | Pris visad på svart bakgrund. |
| `text-action-primary` | `#000000` | Primär länk/klickbar text (på ljus bakgrund). |
| `text-action-primary-hover` | `#737373` | Hover för primär länk (på ljus bakgrund). |
| `text-action-primary-inverted` | `#ffffff` | Primär länk på mörk bakgrund. |
| `text-action-primary-inverted-hover` | `rgba(255,255,255,0.78)` | Hover för primär länk på mörk bakgrund. |
| `text-action-secondary` | `#4f4f4f` | Sekundär länkfärg. Används tillsammans med text-secondary. |
| `text-action-secondary-hover` | `#737373` | Hover för sekundär länk. |
| `text-action-tertiary` | `#737373` | Tertiär länkfärg. Används tillsammans med text-tertiary. |
| `text-action-tertiary-hover` | `#939595` | Hover för tertiär länk. |
| `text-action-accent` | `#000000` | Text på accentfärgad yta. |
| `text-success` | `#248616` | Statustext – lyckat resultat. |
| `text-danger-default` | `#d90000` | Statustext – fel/fara. |
| `text-information-default` | `#0066ff` | Statustext – information. |

```html
<!-- Exempel: Textfärger -->
<p style="color:#000000;">Primär text</p>
<p style="color:#4f4f4f;">Sekundär text</p>
<span style="color:#d90000;">Felmeddelande</span>
<a href="#" style="color:#000000;">Länk</a>
```

### Ikon

| Token | Hex | Beskrivning |
|---|---|---|
| `icon-primary` | `#000000` | Primär ikonfärg. Standard för ikoner på ljus bakgrund. |
| `icon-inverted` | `#ffffff` | Ikon på mörk bakgrund. |

### Bakgrund

| Token | Hex | Beskrivning |
|---|---|---|
| `background-primary` | `#ffffff` | Primär sidbakgrund. |
| `background-secondary` | `#f6f6f6` | Sekundär bakgrund. Paneler, kort, sidofält. |

### Surface – Neutrala nivåer

Används för att bygga upp kontrast i gråskalan. Siffran anger ungefärlig opacitet/mörkhet (02 = ljusast, 100 = svart).

| Token | Hex | Beskrivning |
|---|---|---|
| `surface-02` | `#fafafa` | Mycket ljus yta. Navigations-hover. |
| `surface-05` | `#f6f6f6` | Lätt grå yta. |
| `surface-10` | `#e5e5e5` | Disabled-bakgrund, borders. |
| `surface-15` | `#dad9d7` | Mjuk separator. |
| `surface-20` | `#cccccc` | Svagare border-selected. |
| `surface-40` | `#939595` | Inaktiverad text/ikon. |
| `surface-50` | `#737373` | Mediumgrå yta. |
| `surface-60` | `#595959` | Mörk yta. |
| `surface-80` | `#333333` | Mörkare yta. |
| `surface-90` | `#222222` | Nästan svart yta. |
| `surface-100` | `#000000` | Svart yta. |
| `surface-raised-primary` | `#ffffff` | Upphöjd yta, primär (kort, modaler). |
| `surface-raised-secondary` | `#f6f6f6` | Upphöjd yta, sekundär. |
| `surface-disabled` | `#e5e5e5` | Bakgrund för inaktiverade element. |
| `surface-navigation-hover` | `#fafafa` | Navigations-hover bakgrund. |

### Surface – Semantiska statusfärger

| Token | Hex | Beskrivning |
|---|---|---|
| `surface-information-default` | `#0066ff` | Informationsyta, stark. |
| `surface-information-weak` | `#d0e9ff` | Informationsyta, svag. |
| `surface-information-weaker` | `#e2f1ff` | Informationsyta, mycket svag. Bakgrund för info-meddelanden. |
| `surface-success-default` | `#248616` | Framgångsyta, stark. |
| `surface-success-weak` | `#daf6d0` | Framgångsyta, svag. |
| `surface-success-weaker` | `#edffe7` | Framgångsyta, mycket svag. |
| `surface-warning-default` | `#fac000` | Varningsyta, stark. |
| `surface-warning-weak` | `#ffe167` | Varningsyta, svag. |
| `surface-warning-weaker` | `#fff5c2` | Varningsyta, mycket svag. |
| `surface-danger-default` | `#d90000` | Farlighetyta, stark. |
| `surface-danger-weak` | `#ffbdc0` | Farlighetyta, svag. |
| `surface-danger-weaker` | `#ffebeb` | Farlighetyta, mycket svag. Bakgrund för felmeddelanden. |

```html
<!-- Exempel: Statusmeddelanden -->
<div style="background:#edffe7; color:#248616;">Beställningen är bekräftad</div>
<div style="background:#ffebeb; color:#d90000;">Något gick fel</div>
<div style="background:#e2f1ff; color:#0066ff;">Hämtar information...</div>
<div style="background:#fff5c2; color:#000;">Lågt lagersaldo</div>
```

### Surface – Opacitetsnivåer

| Token | Hex | Beskrivning |
|---|---|---|
| `surface-opacity-black-05` | `#0000000d` | Svart 5% opacitet. |
| `surface-opacity-black-10` | `#0000001a` | Svart 10% opacitet. Subtil overlay. |
| `surface-opacity-black-20` | `#00000033` | Svart 20% opacitet. |
| `surface-opacity-black-50` | `#00000080` | Svart 50% opacitet. Modalbakgrund. |
| `surface-opacity-white-0` | `#ffffff00` | Vit, helt transparent. |
| `surface-opacity-white-20` | `#ffffff33` | Vit 20% opacitet. Subtil ljusning på mörk bakgrund. |

### Border

| Token | Hex | Beskrivning |
|---|---|---|
| `border-primary` | `#e5e5e5` | Standard border. Kortseparatorer. |
| `border-secondary` | `#f6f6f6` | Ljus border. Subtila separatorer. |
| `border-tertiary` | `#dad9d7` | Mjuk border. Disabled-element. |
| `border-dark` | `#333333` | Mörk border. Hover-tillstånd. |
| `border-selected` | `#000000` | Vald/aktiv border. |
| `border-selected-hover` | `#737373` | Hover för vald border. |
| `border-selected-weaker` | `#cccccc` | Svagare vald border. |
| `border-hover` | `#333333` | Hover-border. |
| `border-disabled` | `#dad9d7` | Inaktiverad border. |
| `border-input-default` | `#939595` | Inputfält, standard. |
| `border-input_control-default` | `#737373` | Inputkontroller (checkbox, radio), standard. |
| `border-action-1` | `#000000` | Aktionsknapp border, primär. |
| `border-action-2` | `#ffffff` | Aktionsknapp border, inverterad. |
| `border-action-3` | `#0000001a` | Aktionsknapp border, subtil (10% svart). |
| `border-focus` | `#455efb` | Fokusring (blå). Används med `inset: -2px`. |
| `border-information-default` | `#0066ff` | Informationsborder, stark. |
| `border-information-weak` | `#d0e9ff` | Informationsborder, svag. |
| `border-success-default` | `#248616` | Framgångsborder, stark. |
| `border-success-weak` | `#daf6d0` | Framgångsborder, svag. |
| `border-warning-default` | `#fac000` | Varningsborder, stark. |
| `border-warning-weak` | `#ffe167` | Varningsborder, svag. |
| `border-danger-default` | `#d90000` | Farlighetborder, stark. |
| `border-danger-weak` | `#ffbdc0` | Farlighetborder, svag. |

```html
<!-- Exempel: Border-användning -->
<input style="border: 1px solid #939595;">
<input style="border: 2px solid #455efb;"> <!-- focus -->
<div style="border: 1px solid #d90000; background:#ffebeb;">Felmeddelande</div>
```

---
