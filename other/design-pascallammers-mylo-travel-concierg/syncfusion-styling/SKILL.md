---
name: syncfusion-styling
description: Use when styling or laying out SyncFusion components. Critical for understanding what CSS classes exist vs don't exist. Prevents using fake utility classes that break layout. Auto-activates when working with SF component styling, layout, spacing, colors, or icons.
allowed-tools: Read, Grep, Bash, WebFetch
---

# SyncFusion Fluent2 - Styling & Layout (Verified)

**Created:** 2025-10-25 after 4h debugging session
**Source:** SF official docs + verified icon list + ProjectDetailView implementation

---

## 🔴 KRITISK UPPTÄCKT - Utility-klasser som INTE finns

**SF HAR INGA Tailwind-liknande utility-klasser!**

### ❌ DESSA KLASSER FINNS INTE (gör ingenting):
```tsx
// Layout
e-flex, e-grid, e-inline, e-block
e-align-center, e-align-start, e-align-end
e-justify-between, e-justify-center, e-justify-start
e-flex-column, e-flex-row, e-flex-wrap

// Spacing
e-gap-4, e-gap-8, e-gap-12, e-gap-16, e-gap-24
e-m-0, e-m-4, e-m-8, e-mb-4, e-mb-8, e-mb-12, e-mb-16, e-mb-24
e-mt-4, e-mt-8, e-mt-16, e-mt-32
e-p-4, e-p-8, e-p-12, e-p-16, e-p-24, e-p-32
e-px-16, e-py-8

// Typography
e-text-xs, e-text-sm, e-text-base, e-text-lg, e-text-xl
e-font-normal, e-font-medium, e-font-semibold, e-font-bold
e-text-center, e-text-left, e-text-right

// Grid
e-grid-cols-2, e-grid-cols-3, e-grid-cols-4
```

**Resultat om du använder dessa:** Layout kollapsar helt, komponenter blir osynliga/felplacerade.

---

## ✅ ÄKTA SF-KLASSER (verifierade)

### **Layout Structure:**
```tsx
e-card                 // Card container
e-card-header          // Card header
e-card-title           // Header title
e-card-content         // Card content area
```

### **Buttons:**
```tsx
e-btn                  // Base button
e-primary              // Primary (blue)
e-success              // Success (green)
e-danger               // Danger (red)
e-warning              // Warning (orange)
e-info                 // Info (blue)
e-outline              // Outline style
e-flat                 // Flat style
e-small                // Small button
```

### **Icons:**
```tsx
e-icons                // Base icon class
e-small                // 8px
e-medium               // 16px
e-large                // 24px

// Verified icon names (517 total in fluent2.scss):
e-check, e-plus, e-close, e-warning, e-refresh
e-arrow-left, e-arrow-right, e-arrow-up, e-arrow-down
e-user, e-edit, e-trash, e-folder
e-clock, e-date-occurring
e-play, e-pause
```

**Verifiera ikoner INNAN användning:**
```bash
grep "e-your-icon" node_modules/@syncfusion/ej2-icons/styles/fluent2.scss
```

---

## 🎯 RÄTT APPROACH - SF Best Practice

### **1. Layout → Inline Styles**
```tsx
// ✅ CORRECT
<div style={{
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  marginBottom: '16px'
}}>
  {/* Content */}
</div>

// ❌ WRONG - Dessa klasser gör INGENTING
<div className="e-flex e-align-center e-gap-8 e-mb-16">
  {/* Content */}
</div>
```

### **2. Card Structure**
```tsx
// ✅ CORRECT - Använd e-card för grupperad content
<div className="e-card">
  <div className="e-card-header">
    <div className="e-card-title">Rubrik</div>
  </div>
  <div className="e-card-content" style={{ padding: '12px' }}>
    {/* Content med inline styles för layout */}
  </div>
</div>

// ❌ WRONG - Custom divs med påhittade klasser
<div className="e-p-16 e-rounded-lg e-border">
  <h3 className="e-mb-12">Rubrik</h3>
  {/* Content */}
</div>
```

### **3. Buttons → ButtonComponent**
```tsx
// ✅ CORRECT - SF ButtonComponent
<ButtonComponent
  cssClass="e-primary"
  iconCss="e-icons e-check"
  content="Spara"
  onClick={handleSave}
/>

// ❌ WRONG - Native button (dålig styling, ingen ripple)
<button className="e-btn e-primary" onClick={handleSave}>
  <span className="e-icons e-check"></span> Spara
</button>
```

**ButtonComponent props:**
- `cssClass`: 'e-primary', 'e-success', 'e-danger', 'e-outline', 'e-flat', 'e-small'
- `iconCss`: 'e-icons e-iconname'
- `iconPosition`: 'Left' (default) eller 'Right'
- `content`: Text på knappen
- `onClick`: Event handler

### **4. Icons → Verified Names + Size Classes**
```tsx
// ✅ CORRECT - Verified icon + size class
<span className="e-icons e-medium e-check"></span>
<span className="e-icons e-small e-user"></span>

// ❌ WRONG - Påhittad ikon + inline font-size
<span className="e-icons e-calendar" style={{ fontSize: '12px' }}></span>
```

**Icon sizes:**
- `e-small`: 8px
- `e-medium`: 16px (default om ingen size anges)
- `e-large`: 24px

**Vanliga ikoner (verifierade):**
- Åtgärder: `e-check`, `e-plus`, `e-close`, `e-edit`, `e-trash`
- Navigation: `e-arrow-left`, `e-arrow-right`, `e-arrow-up`, `e-arrow-down`
- Status: `e-warning`, `e-refresh`, `e-play`, `e-pause`
- Övrigt: `e-user`, `e-clock`, `e-date-occurring`, `e-folder`

### **5. Colors → SF CSS Variables**
```tsx
// ✅ CORRECT - SF official variables
color: 'var(--color-sf-primary)'      // Primary blue
color: 'var(--color-sf-black)'        // Black text
color: 'var(--color-sf-success)'      // Green
color: 'var(--color-sf-warning)'      // Orange
color: 'var(--color-sf-danger)'       // Red

// Subtle text (opacity):
color: 'var(--color-sf-black)', opacity: 0.6   // Secondary text
color: 'var(--color-sf-black)', opacity: 0.4   // Tertiary text

// ❌ WRONG - Custom vars som inte finns
color: 'var(--e-text)'
color: 'var(--e-surface-hover)'
color: 'var(--primary-600)'
```

**Tillgängliga SF Fluent2 CSS-variabler:**
- `--color-sf-primary`, `--color-sf-primary-light`, `--color-sf-primary-dark`
- `--color-sf-black`, `--color-sf-white`
- `--color-sf-success`, `--color-sf-warning`, `--color-sf-danger`, `--color-sf-info`
- `--color-sf-border`, `--color-sf-border-light`

### **6. Spacing → Inline Styles**
```tsx
// ✅ CORRECT - Inline styles
style={{
  padding: '12px',
  margin: '16px',
  marginBottom: '12px',
  gap: '8px'
}}

// ❌ WRONG - Påhittade klasser
className="e-p-12 e-m-16 e-mb-12 e-gap-8"
```

**Kompakta värden (från ProjectDetailView):**
- Padding: 6-12px (card content)
- Margins: 12-16px (mellan sektioner)
- Gaps: 4-8px (mellan element)
- Font sizes: 11-16px (labels vs siffror)

### **7. Typography → Inline Styles**
```tsx
// ✅ CORRECT
style={{
  fontSize: '11px',      // Small labels
  fontSize: '14px',      // Normal text
  fontSize: '16px',      // Numbers/emphasis
  fontSize: '20px',      // Headings
  fontSize: '24px',      // Page title
  fontWeight: 'bold',
  fontWeight: '600'
}}

// ❌ WRONG
className="e-text-sm e-font-bold"
```

---

## 📋 COMPLETE EXAMPLE - ProjectDetailView Pattern

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { InPlaceEditorComponent } from '@syncfusion/ej2-react-inplace-editor';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

export function MyView() {
  return (
    <div style={{ maxWidth: '896px', margin: '0 auto', padding: '24px' }}>

      {/* Navigation */}
      <div style={{ marginBottom: '12px' }}>
        <ButtonComponent
          cssClass="e-flat e-small"
          iconCss="e-icons e-arrow-left"
          content="Tillbaka"
          onClick={() => navigate(-1)}
        />
      </div>

      {/* Title + Metadata */}
      <div style={{ marginBottom: '16px' }}>
        <h1 style={{
          fontSize: '24px',
          fontWeight: 'bold',
          margin: '0 0 4px 0',
          color: 'var(--color-sf-black)'
        }}>Sidtitel</h1>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span className="e-icons e-small e-user"></span>
            <span style={{ fontSize: '14px', color: 'var(--color-sf-black)', opacity: 0.6 }}>
              Metadata
            </span>
          </div>
        </div>
      </div>

      {/* Card with actions */}
      <div className="e-card" style={{ marginBottom: '16px' }}>
        <div className="e-card-header">
          <div className="e-card-title">Sektion</div>
        </div>
        <div className="e-card-content" style={{ padding: '12px' }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <ButtonComponent
              cssClass="e-primary"
              iconCss="e-icons e-check"
              content="Primär åtgärd"
            />
            <ButtonComponent
              cssClass="e-outline"
              iconCss="e-icons e-close"
              content="Avbryt"
            />
          </div>
        </div>
      </div>

      {/* Compact slider card */}
      <div className="e-card">
        <div className="e-card-content" style={{ padding: '6px 10px 4px 10px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
            <span style={{ fontSize: '11px', color: 'var(--color-sf-black)', opacity: 0.5 }}>
              Label vänster
            </span>
            <span style={{ fontSize: '11px', color: 'var(--color-sf-black)', opacity: 0.5 }}>
              Label höger
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--color-sf-primary)' }}>
              55%
            </span>
            <span style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--color-sf-primary-dark)' }}>
              18h
            </span>
          </div>
          <SliderComponent
            min={0}
            max={100}
            type="MinRange"
            tooltip={{ isVisible: true, placement: 'Before', showOn: 'Hover' }}
          />
        </div>
      </div>

    </div>
  );
}
```

---

## 🚨 VARNINGSSIGNALER - Du gör FEL om:

1. **Du skriver:** `className="e-mb-16"` → STOP! Använd `style={{ marginBottom: '16px' }}`
2. **Du skriver:** `className="e-flex e-gap-8"` → STOP! Använd `style={{ display: 'flex', gap: '8px' }}`
3. **Du skriver:** `e-calendar` eller `e-schedule` → STOP! Verifiera i fluent2.scss FÖRST
4. **Du skriver:** `<button className="e-btn">` → STOP! Använd `<ButtonComponent>`
5. **Du skriver:** `var(--e-text)` → STOP! Använd `var(--color-sf-black)` + opacity
6. **Du gissar** på ikon-namn → STOP! Grep i `node_modules/@syncfusion/ej2-icons/styles/fluent2.scss`

---

## 📚 QUICK REFERENCE

### **Verifiera Ikon:**
```bash
grep "e-your-icon-name" node_modules/@syncfusion/ej2-icons/styles/fluent2.scss
```

### **Lista Alla Ikoner:**
```bash
grep -o "&\.e-[a-z-]*:" node_modules/@syncfusion/ej2-icons/styles/fluent2.scss | \
  sed 's/&\.//' | sed 's/://' | sort -u
```

### **SF CSS Variables:**
```bash
grep -E "^\s*--color-sf-" node_modules/@syncfusion/ej2-base/styles/fluent2.css | head -30
```

---

## 🎨 SPACING GUIDELINES (från ProjectDetailView)

**Card Padding:**
- Kompakt: `6px 10px 4px 10px` (progress slider)
- Normal: `12px` (standard card content)
- Luftig: `16px` (selektivt)

**Margins:**
- Mellan sektioner: `12-16px`
- Mellan cards: `16px`
- Inuti card: `4-8px`

**Gaps:**
- Mellan små element: `4-6px`
- Mellan knappar: `8px`
- Mellan metadata: `12px`

**Font Sizes:**
- Tiny labels: `11px` (opacity 0.5)
- Small text: `12px`
- Normal text: `14px`
- Emphasized: `16px`
- Numbers: `16-20px`
- Headings: `20-24px`

---

## 🔧 COMPONENT-SPECIFIC

### **ButtonComponent (ALLTID använd denna)**
```tsx
<ButtonComponent
  cssClass="e-primary"           // Style
  iconCss="e-icons e-check"      // Icon
  iconPosition="Left"            // Left/Right
  content="Knapptext"            // Text
  onClick={handler}              // Handler
  disabled={false}               // State
/>
```

### **SliderComponent**
```tsx
<SliderComponent
  min={0}
  max={100}
  step={5}
  value={50}
  type="MinRange"                // Visar fylld track!
  tooltip={{
    isVisible: true,
    placement: 'Before',
    showOn: 'Hover'              // Inte 'Always'
  }}
  change={(e: any) => handleChange(e.value)}
/>
```

### **InPlaceEditorComponent**
```tsx
<InPlaceEditorComponent
  mode="Inline"
  type="Date"                    // Text, Numeric, Date
  value={value}
  emptyText="Placeholder"
  actionOnBlur="Submit"
  model={{ min: 0, step: 0.5, format: 'N1' }}  // För Numeric
  change={async (e: any) => {
    await save(e.value);
  }}
/>
```

---

## ⚠️ VANLIGA MISSTAG (från dagens session)

### **1. Utility-klass-fällan**
```tsx
// ❌ FEL - 4 timmar debugging
<div className="e-flex e-gap-8 e-mb-16">
  <span className="e-text-sm e-font-bold">Text</span>
</div>
// Resultat: Ingen layout, text osynlig

// ✅ RÄTT
<div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
  <span style={{ fontSize: '14px', fontWeight: 'bold' }}>Text</span>
</div>
```

### **2. Ikon-gissning**
```tsx
// ❌ FEL - Ikonen finns inte
<span className="e-icons e-calendar"></span>
// Resultat: Tom fyrkant

// ✅ RÄTT - Verifiera FÖRST
<span className="e-icons e-medium e-date-occurring"></span>
```

### **3. Native button**
```tsx
// ❌ FEL - Ingen ripple, dålig styling
<button className="e-btn e-primary">Spara</button>

// ✅ RÄTT
<ButtonComponent cssClass="e-primary" content="Spara" />
```

### **4. Custom CSS-variabler**
```tsx
// ❌ FEL - Variabeln finns inte
color: 'var(--e-text)'
color: 'var(--primary-600)'

// ✅ RÄTT - SF official variables
color: 'var(--color-sf-black)'
opacity: 0.6
```

---

## 🎯 CHECKLIST FÖR NY VY

Innan du börjar koda:

- [ ] Läst SF docs för alla komponenter du ska använda
- [ ] Verifierat att ALLA ikoner finns i fluent2.scss
- [ ] Planerat struktur med e-card (inte custom divs)
- [ ] Planerat att använda ButtonComponent (inte native button)
- [ ] Vet att du ska använda inline styles (inte utility-klasser)
- [ ] Vet vilka SF CSS-variabler som finns

Under kodning:

- [ ] Använder ButtonComponent för ALLA knappar
- [ ] Använder e-card för grupperad content
- [ ] Använder inline styles för ALLA layout/spacing
- [ ] Använder SF CSS-variabler (--color-sf-*)
- [ ] Verifierat ikoner med grep
- [ ] Lagt till icon size-klasser (e-small/medium/large)
- [ ] Inga påhittade klasser (e-flex, e-mb-*, e-text-sm)

Efter implementation:

- [ ] Testat i webbläsare (inte bara build)
- [ ] Layout fungerar (inga kollapsade sektioner)
- [ ] Ikoner syns (inte tomma fyrkanter)
- [ ] Knappar har ripple-effekt
- [ ] Spacing ser kompakt ut (inte för luftigt)

---

## 📖 REFERENCES

**Officiell dokumentation:**
- Icons: https://ej2.syncfusion.com/react/documentation/appearance/icons
- CSS Variables: https://ej2.syncfusion.com/react/documentation/appearance/css-variables
- Button: https://ej2.syncfusion.com/react/documentation/button/getting-started
- Slider: https://ej2.syncfusion.com/react/documentation/range-slider/getting-started

**Projekt-referenser:**
- TestView.tsx - Korrekt referens-implementation
- ProjectDetailView.tsx - Komplett exempel efter 4h fixning

**Verifiera innan användning:**
```bash
# Lista alla ikoner
grep -o "&\.e-[a-z-]*:" node_modules/@syncfusion/ej2-icons/styles/fluent2.scss | \
  sed 's/&\.//' | sed 's/://' | sort -u > /tmp/sf-icons.txt

# Kolla om ikon finns
grep "e-my-icon" /tmp/sf-icons.txt
```

---

**Skill Version:** 1.0 (Verified från 4h debugging-session)
**Skapad:** 2025-10-25
**Källa:** SF official docs + verified implementation + learned mistakes
**Status:** Production-ready
