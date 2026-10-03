---
name: typography
description: Använd när du väljer eller granskar typografi/textstilar (Body, Alt-Label, Label, Title, Headline, Display) på Desktop respektive Mobil enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Typografi – Desktop Base Styling (ECO Design System)

Gäller för **Desktop Small (`md:`, 769px+) och Desktop (`lg:`, 1024px+)**.
Font: `Breuer Condensed`, sans-serif. `font-feature-settings: 'ss02' 1, 'ss03' 1` gäller alla stilar.

### Body

| Token | Namn | Size | Line-height | Letter-spacing | Weight | Paragraph-spacing |
|---|---|---|---|---|---|---|
| `body-sm` | Body Small | 14px | 20px | 0.28px | 400 | 12px |
| `body-md` | Body Medium | 16px | 24px | 0.32px | 400 | 16px |
| `body-lg` | Body Large | 20px | 28px | 0px | 400 | 20px |
| `body-xl` | Body XLarge | 24px | 32px | 0px | 400 | 24px |

> Body används för längre textpassager. `body-xl` lämpar sig för kortare introtexter.

### Alt-Label (alternativa etiketter, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `alt-label-sm` | Alt-Label Small | 14px | 14px | 0.56px | 500 |
| `alt-label-md` | Alt-Label Medium | 16px | 16px | 0.64px | 500 |
| `alt-label-lg` | Alt-Label Large | 18px | 18px | 0.36px | 500 |

> Alt-Label: `text-transform: uppercase`. Används för etikettering av formulärfält och UI-komponenter.

### Label (fetstil-etiketter, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `label-sm` | Label Small | 14px | 14px | 0.56px | 600 |
| `label-md` | Label Medium | 16px | 16px | 0.48px | 600 |
| `label-lg` | Label Large | 18px | 18px | 0.18px | 600 |

> Label: `text-transform: uppercase`. Fetare version av Alt-Label. Används i knappar, formulär och UI-komponenter.

### Title (rubriker, normal case)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `title-sm` | Title Small | 16px | 18px | 0px | 600 |
| `title-md` | Title Medium | 20px | 24px | 0px | 600 |
| `title-lg` | Title Large | 24px | 28px | 0px | 600 |

> Title: kortare, medelstark text. Används för sekundära rubriker och H-taggar av mindre storlek.

### Headline (primära rubriker, normal case)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `headline-sm` | Headline Small | 28px | 32px | 0px | 600 |
| `headline-md` | Headline Medium | 32px | 36px | 0px | 600 |
| `headline-lg` | Headline Large | 36px | 40px | 0px | 600 |
| `headline-xl` | Headline XLarge | 46px | 52px | 0px | 600 |

> Headline: kort, högbetonad text. Primära textpassager och viktiga innehållsregioner. `headline-xl` lämpar sig för H1-innehåll (ej i kombination med `display-lg`).

### Display (kampanj/hero, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `display-sm` | Display Small | 26px | 26px | 0px | 600 |
| `display-md` | Display Medium | 36px | 36px | 0px | 600 |
| `display-lg` | Display Large | 66px | 60px | 0px | 600 |

> Display: `text-transform: uppercase`. Reserverat för hero-banners, kampanjrubriker och numerärer. Använd sparsamt. `display-lg` = H1 på sida/artikel (aldrig tillsammans med `headline-xl`).

### Modified Styles (modifierade varianter)

| Token | Bas | Ändring | Användning |
|---|---|---|---|
| `label-lg--badge` | `label-sm` | 14px, 0.56px, 600, normal case | Badge-komponent |
| `label-sm--badge` | `label-sm` | 12px, 0.48px, 600, normal case | Liten badge |
| `label-lg--underline` | `label-lg` | + `text-decoration: underline` | Understruken etikett |

### CSS-regel (Desktop Base)

```css
/* Alla typografistilar delar: */
font-family: 'Breuer Condensed', Arial, sans-serif;
font-style: normal;
font-feature-settings: 'ss02' 1, 'ss03' 1;

/* Alt-Label och Label tillägger: */
text-transform: uppercase;

/* Display tillägger: */
text-transform: uppercase;
font-feature-settings: 'ss02' 1, 'ss03' 1; /* ej 'ss06' */
```

---

## Typografi – Mobile Base Styling (ECO Design System)

Gäller för **Mobile (`xs`, 0–639px) och Tablet (`sm`, 640–768px)**.
Font: `Breuer Condensed`, sans-serif. `font-feature-settings: 'ss02' 1, 'ss03' 1` gäller alla stilar.

### Body

| Token | Namn | Size | Line-height | Letter-spacing | Weight | Paragraph-spacing |
|---|---|---|---|---|---|---|
| `body-sm` | Body Small | 14px | 20px | 0.28px | 400 | 12px |
| `body-md` | Body Medium | 16px | 22px | 0.32px | 400 | 16px |
| `body-lg` | Body Large | 18px | 24px | 0px | 400 | 16px |
| `body-xl` | Body XLarge | 20px | 26px | 0px | 400 | — |

> Body används för längre textpassager. `body-xl` lämpar sig för kortare introtexter.

### Alt-Label (alternativa etiketter, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `alt-label-sm` | Alt-Label Small | 12px | 12px | 0.48px | 500 |
| `alt-label-md` | Alt-Label Medium | 14px | 14px | 0.56px | 500 |
| `alt-label-lg` | Alt-Label Large | 16px | 16px | 0.32px | 500 |

> Alt-Label: `text-transform: uppercase`. Används för etikettering av formulärfält och UI-komponenter.

### Label (fetstil-etiketter, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `label-sm` | Label Small | 12px | 12px | 0.48px | 600 |
| `label-md` | Label Medium | 14px | 14px | 0.42px | 600 |
| `label-lg` | Label Large | 16px | 16px | 0.32px | 600 |

> Label: `text-transform: uppercase`. Fetare version av Alt-Label. Används i knappar, formulär och UI-komponenter.

### Title (rubriker, normal case)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `title-sm` | Title Small | 16px | 18px | 0px | 600 |
| `title-md` | Title Medium | 18px | 22px | 0px | 600 |
| `title-lg` | Title Large | 20px | 24px | 0px | 600 |

> Title: kortare, medelstark text. Används för sekundära rubriker och H-taggar av mindre storlek.

### Headline (primära rubriker, normal case)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `headline-sm` | Headline Small | 22px | 24px | 0px | 600 |
| `headline-md` | Headline Medium | 26px | 28px | 0px | 600 |
| `headline-lg` | Headline Large | 28px | 32px | 0px | 600 |
| `headline-xl` | Headline XLarge | 30px | 36px | 0px | 600 |

> Headline: kort, högbetonad text. Primära textpassager och viktiga innehållsregioner. `headline-xl` lämpar sig för H1-innehåll (ej i kombination med `display-lg`).

### Display (kampanj/hero, uppercase)

| Token | Namn | Size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `display-sm` | Display Small | 22px | 22px | 0px | 600 |
| `display-md` | Display Medium | 28px | 28px | 0px | 600 |
| `display-lg` | Display Large | 36px | 34px | 0px | 600 |

> Display: `text-transform: uppercase`. Reserverat för hero-banners, kampanjrubriker och numerärer. Använd sparsamt. `display-lg` = H1 på sida/artikel (aldrig tillsammans med `headline-xl`). OBS: `display-lg` har line-height (34px) som är lägre än font-size (36px) — avsiktligt för tät kampanjtext.

### CSS-regel (Mobile Base)

```css
/* Alla typografistilar delar: */
font-family: 'Breuer Condensed', Arial, sans-serif;
font-style: normal;
font-feature-settings: 'ss02' 1, 'ss03' 1;

/* Alt-Label och Label tillägger: */
text-transform: uppercase;

/* Display tillägger: */
text-transform: uppercase;
font-feature-settings: 'ss02' 1, 'ss03' 1; /* ej 'ss06' */
```

---
