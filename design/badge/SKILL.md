---
name: badge
description: Använd när du bygger en icke-interaktiv status- eller etikett-indikator (Badge) — t.ex. "Ny", "Uppdaterad", "Arkiv", rollnamn. Inte att förväxla med Tag (interaktiv filtrering) eller kundvagns-räknarens .badge-klass.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Badge (ECO Design System)

**Figma – riktlinjer:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=4752-241948
**Figma – alla varianter:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=6098-342317

Badge är en **icke-interaktiv** status- eller etikett-indikator — läsbar men aldrig klickbar. Förväxla inte med **Tag** (interaktiv, används för filtrering/sortering/gruppering) eller med `.breadcrumb-item` (interaktiv navigering).

### Används när
- Statusindikering (t.ex. "Senaste", "Arkiv", "Under uppbyggnad", rollnamn som "Administratör").
- Antal, featured/highlighted content, eller information som kräver omedelbar uppmärksamhet.
- Ska **inte** förlita sig på enbart färg för att förmedla betydelse — kombinera med text och/eller ikon.

### Används INTE när
- Elementet ska vara klickbart/filtrerbart → använd **Tag** istället.
- Det är en räknar-bubbla på en ikon (t.ex. kundvagn) → det är en annan, redan existerande komponent i det här projektet: `.badge`/`.badge--white` (cirkulär räknare, se `site-header__right`). Namnkrock — Badge/Basic nedan har fått klassnamnet `.badge-basic` för att inte kollidera.

---

### Varianter

Badge/Basic finns i **6 States** × **3 Emphasis** × **3 Size** (Large/Medium/Small, Small endast Desktop) × valfri ikon. Utöver Basic finns även Dot (endast prick, ingen text), Number-Icon, samt e-com-specifika Product/Discount/Purchase-badges (används bara i e-handelskontext, inte i det här projektet).

#### States (färg)

| State | Syfte |
|---|---|
| **Neutral Grey** | Neutral status utan alert-betydelse (grå). |
| **Neutral Dark** | Neutral status, hög kontrast (svart). |
| **Alert Info** | Informativ — default alert-färg, mest flexibel. |
| **Alert Success** | Positiv feedback/lyckad status. |
| **Alert Warning** | Varning, kräver uppmärksamhet. |
| **Alert Danger** | Negativ feedback/fel. |

#### Emphasis (färgstyrka) — formel per state

| Emphasis | Bakgrund | Border | Textfärg |
|---|---|---|---|
| **Strong** | `surface-{state}-default` (Neutral Grey: `surface-50` #737373 · Neutral Dark: `surface-100` svart) | ingen | `text-primary-inverted` (vit) |
| **Weak** | `surface-{state}-weak` (Neutral Grey: `surface-20` #ccc · Neutral Dark: `surface-100` svart — identisk med Strong) | ingen | `text-{state}-default` (Neutral Grey: `text-primary` svart · Neutral Dark: `text-primary-inverted` vit) |
| **Weaker** | `surface-{state}-weaker` (Neutral Grey: `surface-05` #f6f6f6 · Neutral Dark: `surface-100` svart — identisk med Strong/Weak) | `1px solid border-{state}-weak` (Neutral Grey: `border-primary` #e5e5e5 · Neutral Dark: `border-dark` #333) | Samma som Weak |

> Neutral Dark har alltid svart bakgrund oavsett emphasis — enda skillnaden är att Weaker får en `border-dark`-kant. `{state}` i formeln ovan avser alert-namnet i gemener (`information`, `success`, `warning`, `danger`) för de fyra Alert-varianterna.

**Verifierade exempel (Alert Info, Medium, Desktop):**

| Emphasis | Bakgrund | Border | Text |
|---|---|---|---|
| Strong | `surface-information-default` `#0066ff` | – | `text-primary-inverted` vit |
| Weak | `surface-information-weak` `#d0e9ff` | – | `text-information-default` |
| Weaker | `surface-information-weaker` `#e2f1ff` | `1px solid border-information-weak` `#d0e9ff` | `text-information-default` |

`Alert Success`/`Warning`/`Danger` följer exakt samma formel med respektive statusfärgs `-default`/`-weak`/`-weaker`-tokens (se Färger-sektionen ovan).

---

### Storlekar

| Storlek | Padding (Desktop) | Padding (Mobil) | Font (Desktop) | Font (Mobil) | Tillgänglighet |
|---|---|---|---|---|---|
| **Large** | `6px 8px` | `5px 6px` | `label-lg--badge`: 14px/14px, 0.56px | 14px/14px, 0.48px | Desktop + Mobil |
| **Medium** | `4px 5px` | `4px 5px` | `label-lg--badge`: 14px/14px, 0.56px | samma | Desktop + Mobil |
| **Small** | `3px 5px` | – | `label-sm--badge`: 12px/12px, 0.48px | – | **Endast Desktop** |

- Ikon (valfri): `14px`, `gap: 4px` mellan ikon och text.
- Font-weight: **Medium (500)** — avviker medvetet från projektets vanliga 700, då detta är den faktiska Figma-specen för Badge/Basic.
- `font-feature-settings`: `'ss02' 1, 'ss03' 1` (Large/Small) — Medium-storleken har även `'ss06' 1`.

---

### Letter Case (parameter)

Badge-textens skiftläge är en egen, valbar parameter — inte hårdkodad. Två lägen:

| Letter Case | Font-weight | `text-transform` | Använd när |
|---|---|---|---|
| **Sentence Case** (default) | 500 (Medium) | Inget (`Ny`, `Uppdaterad`) | Statusetiketter — de flesta fall. |
| **Upper Case** | 700 (Bold) | `uppercase` (`NY`, `INLOGGAD`) | Fasta klassificerings-/kategorietiketter där versaler ger extra visuell tyngd — matchar knapparnas/label-komponenternas versal-konvention. |

> Välj Sentence Case som standard. Upper Case är inte "fel" bara för att Sentence Case råkar passa innehållet — det är en medveten stilväxel, inte en bugg-fix.

---

### CSS-mall

```css
/* Badge/Basic — döpt .badge-basic för att inte krocka med den befintliga
   räknar-bubblan `.badge` (kundvagn/jämför-ikoner i headern). */
.badge-basic {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 5px;                 /* Medium, default */
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 500;
  font-size: 14px;
  line-height: 14px;
  letter-spacing: 0.56px;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}
.badge-basic__icon { width: 14px; height: 14px; flex-shrink: 0; }

/* Letter Case — Sentence Case är default (redan satt ovan). Upper Case: */
.badge-basic--uppercase {
  font-weight: 700;
  text-transform: uppercase;
}

/* Storlekar */
.badge-basic--large  { padding: 6px 8px; font-feature-settings: 'ss02' 1, 'ss03' 1; }
.badge-basic--small  { padding: 3px 5px; font-size: 12px; line-height: 12px; letter-spacing: 0.48px; font-feature-settings: 'ss02' 1, 'ss03' 1; }
@media (max-width: 768px) {
  .badge-basic--large { padding: 5px 6px; letter-spacing: 0.48px; }
  .badge-basic--small { display: none; } /* Small är endast Desktop */
}

/* Neutral */
.badge-basic--neutral-grey.badge-basic--strong  { background: var(--color-surface-50); color: var(--color-text-primary-inverted); }
.badge-basic--neutral-grey.badge-basic--weak    { background: var(--color-surface-20); color: var(--color-text-primary); }
.badge-basic--neutral-grey.badge-basic--weaker  { background: var(--color-surface-05); border: 1px solid var(--color-border-primary); color: var(--color-text-primary); }
.badge-basic--neutral-dark.badge-basic--strong,
.badge-basic--neutral-dark.badge-basic--weak    { background: var(--color-surface-100); color: var(--color-text-primary-inverted); }
.badge-basic--neutral-dark.badge-basic--weaker  { background: var(--color-surface-100); border: 1px solid var(--color-border-dark); color: var(--color-text-primary-inverted); }

/* Alert Info / Success (mall för Danger — byt bara statusnamnet) */
.badge-basic--info.badge-basic--strong    { background: var(--color-surface-information-default); color: var(--color-text-primary-inverted); }
.badge-basic--info.badge-basic--weak      { background: var(--color-surface-information-weak); color: var(--color-text-information-default); }
.badge-basic--info.badge-basic--weaker    { background: var(--color-surface-information-weaker); border: 1px solid var(--color-border-information-weak); color: var(--color-text-information-default); }
.badge-basic--success.badge-basic--strong { background: var(--color-surface-success-default); color: var(--color-text-primary-inverted); }
.badge-basic--success.badge-basic--weak   { background: var(--color-surface-success-weak); color: var(--color-text-success); }
.badge-basic--success.badge-basic--weaker { background: var(--color-surface-success-weaker); border: 1px solid var(--color-border-success-weak); color: var(--color-text-success); }

/* Alert Warning — CLAUDE.md saknar en text-warning-default-token (gul text har
   dålig kontrast); använd text-primary (svart) på samtliga emphasis-nivåer. */
.badge-basic--warning.badge-basic--strong { background: var(--color-surface-warning-default); color: var(--color-text-primary); }
.badge-basic--warning.badge-basic--weak   { background: var(--color-surface-warning-weak); color: var(--color-text-primary); }
.badge-basic--warning.badge-basic--weaker { background: var(--color-surface-warning-weaker); border: 1px solid var(--color-border-warning-weak); color: var(--color-text-primary); }
```

### Färgval — vanliga betydelser

Badge har inget fast facit för vilken status som får vilken färg, men håll det konsekvent inom ett projekt. Rekommenderad mappning för statusetiketter av typen "var i sitt livscykel-läge är den här sidan/komponenten":

| Betydelse | State | Emphasis | Exempel |
|---|---|---|---|
| Nyskapad | Alert Success | Weak | `Ny` |
| Nyligen redigerad (befintlig sida) | Alert Info | Weak | `Uppdaterad` |
| Pågående/ofärdigt arbete | Alert Warning | Weak | `Pågående` |
| Lägre prioritet / inaktuellt | Neutral Grey | Weaker | `Arkiv`, `Utkast`, `Test` |
| Redo att lämnas över till utveckling | Neutral Dark | Weaker | `Klar för utveckling` |
| Fast kategori (inte en status) | Neutral Grey eller Neutral Dark | Weaker/Strong | `Inloggad`, `Utloggad` — överväg `--uppercase` här för att visuellt skilja kategori från status. |

### HTML-exempel

```html
<!-- Neutral Grey, Weaker, Medium — standardval för status-etiketter -->
<span class="badge-basic badge-basic--neutral-grey badge-basic--weaker">Senaste</span>

<!-- Alert Success, Strong, med ikon -->
<span class="badge-basic badge-basic--info badge-basic--strong">
  <img class="badge-basic__icon" src="..." alt="" />
  Info
</span>
```

### Regler

1. **Badge ≠ Tag ≠ räknar-bubbla.** Badge är alltid icke-interaktiv (ingen `<button>`/`<a>`, inget `cursor: pointer`, ingen hover-state). Blanda inte ihop med den befintliga `.badge`-klassen (kundvagns-/jämför-räknaren i headern) — de är olika komponenter som råkar dela namn i ECO:s Figma-fil.
2. **Färg ska aldrig vara enda bäraren av betydelse** — kombinera med text och/eller reserverad ikon (t.ex. `info`/`check_circle`/`warning`/`error` för respektive Alert-state, samma ikonlogik som Notifikationer).
3. **Neutral Dark har alltid svart bakgrund** oavsett emphasis-val — använd den bara när hög kontrast/vikt är avsedd, annars Neutral Grey.
4. **Small storlek är endast avsedd för Desktop** — använd Medium eller Large på mobil/tablet.
5. Ikon (om använd) är alltid `14px` med `4px` gap till texten — hårdkoda aldrig en annan ikonstorlek i en badge.
6. **Letter Case är en medveten parameter, inte ett misstag.** Sentence Case (default, vikt 500) och Upper Case (vikt 700 + `text-transform: uppercase`) är båda giltiga — välj utifrån om etiketten är en status (Sentence Case) eller en fast kategori (Upper Case ger extra visuell tyngd).
7. **Färg ska spegla betydelse, inte vara slumpvis.** Håll mappningen konsekvent inom samma sida/vy (se "Färgval — vanliga betydelser" ovan) — blanda inte t.ex. grön för "Ny" på ett ställe och blå för samma betydelse på ett annat.

---
