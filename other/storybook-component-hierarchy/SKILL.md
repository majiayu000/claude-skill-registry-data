---
name: storybook-component-hierarchy
description: Activeer bij het samenstellen van NLDD Storybook web components tot pagina's en layouts — beschrijft de verplichte component-hiërarchie, nesting-regels en beschikbare layout-patronen
user-invocable: true
argument-hint: <layout-type>
---

Gebruik deze skill wanneer je NLDD Storybook web components gaat samenstellen tot pagina's, views of layouts. Hij beschrijft welke componenten in welke volgorde genest moeten worden.

Context: $ARGUMENTS

## Overzicht

Elke NLDD applicatie volgt een vaste hiërarchie van layout-componenten. De buitenste laag is altijd `nldd-app-view`, de binnenste laag bevat content-componenten.

### Met Split View

```
nldd-app-view                                  ← verplichte root
  └── Split View                               ← layout keuze (kan genest worden)
      └── Split View Pane                      ← paneel binnen split view
          └── nldd-page OF nldd-container      ← page voor scrollbare content, container voor simpele content
              ├── nldd-container slot="header" ← navigatie, titelbalk (altijd in container)
              ├── Page sections                ← content layout
              │   └── Content-componenten      ← tekst, lijsten, formulieren
              └── nldd-container slot="footer" ← footer content (altijd in container)
```

### Zonder Split View

```
nldd-app-view                          ← verplichte root
  └── nldd-page                        ← enkele pagina
      ├── nldd-container slot="header" ← navigatie, titelbalk (altijd in container)
      ├── Page sections                ← content layout
      │   └── Content-componenten      ← tekst, lijsten, formulieren
      └── nldd-container slot="footer" ← footer content (altijd in container)
```

**Let op:** Split views kunnen genest worden. Bijvoorbeeld een `nldd-navigation-split-view` in het main-slot van een `nldd-bar-split-view`.

---

## Laag 1: App View (verplicht)

```html
<nldd-app-view background="default|tinted">
  <!-- Eén split view OF één nldd-page -->
</nldd-app-view>
```

| Attribuut | Waarden | Beschrijving |
|-----------|---------|--------------|
| `background` | `default`, `tinted` | Cascade van `--context-parent-background-color` naar alle afstammelingen |

**Regel:** `nldd-app-view` is altijd de root. Bevat exact één direct child: een split view of een `nldd-page`.

---

## Laag 2: Layout keuze

Kies één layout-type op basis van de applicatie:

### Optie A: Navigation Split View (meest gebruikt)

Vier-koloms layout met sidebar, secundaire sidebar, main content en inspector. Panelen verschijnen automatisch wanneer content geslot wordt. Elk slot bevat een `nldd-split-view-pane`, die op zijn beurt een `nldd-page` of `nldd-container` bevat.

```html
<nldd-navigation-split-view>
  <nldd-split-view-pane slot="sidebar">
    <nldd-page>...</nldd-page>
  </nldd-split-view-pane>
  <nldd-split-view-pane slot="secondary-sidebar">
    <nldd-page>...</nldd-page>
  </nldd-split-view-pane>
  <nldd-split-view-pane slot="main">
    <nldd-page>...</nldd-page>
  </nldd-split-view-pane>
  <nldd-split-view-pane slot="inspector">
    <nldd-page>...</nldd-page>
  </nldd-split-view-pane>
</nldd-navigation-split-view>
```

Split views kunnen genest worden. Bijvoorbeeld een `nldd-bar-split-view` in het main-slot van een `nldd-navigation-split-view`.

| Slot | Beschrijving | Verplicht |
|------|--------------|-----------|
| `sidebar` | Primaire navigatie (links) | Nee, maar typisch aanwezig |
| `secondary-sidebar` | Subnavigatie (tweede kolom) | Nee |
| `main` | Primaire inhoud | Ja |
| `inspector` | Details/eigenschappen (rechts) | Nee |

**Responsief gedrag:** Panelen die niet passen worden automatisch verborgen en beschikbaar als sheet (overlay).

| Attribuut | Beschrijving |
|-----------|--------------|
| `inspector-as-sheet` | Inspector altijd als sheet tonen |
| `sidebar-as-sheet` | Sidebar altijd als sheet, main op volle breedte |
| `inspector-accessible-label` | Toegankelijke naam voor inspector sheet |
| `sidebar-accessible-label` | Toegankelijke naam voor sidebar sheet |

**Methoden:** `showInspectorSheet()`, `hideInspectorSheet()`, `showSidebarSheet()`, `hideSidebarSheet()`

### Optie B: Bar Split View

Verticale layout met een main-gebied en onbeperkt aantal bars (toolbars, statusbalken). Bars kunnen per breakpoint geordend worden.

```html
<nldd-bar-split-view>
  <nldd-container slot="toolbar" sm-order="1" md-order="1">...</nldd-container>
  <nldd-page slot="main" sm-order="2" md-order="2">...</nldd-page>
  <nldd-container slot="status-bar" sm-order="3" md-order="3">...</nldd-container>
</nldd-bar-split-view>
```

Bars bevatten typisch een `nldd-container` (voor eenvoudige toolbars/statusbalken), het main-slot bevat een `nldd-page`.

| Attribuut (op children) | Beschrijving |
|-------------------------|--------------|
| `sm-order`, `md-order`, `lg-order` | Volgorde per breakpoint |
| `above="sm\|md\|lg"` | Toon vanaf dit breakpoint en groter |
| `below="sm\|md\|lg"` | Toon tot en met dit breakpoint |
| `only="sm\|md\|lg"` | Toon alleen op dit breakpoint |

**Responsief gedrag:** Op sm-viewports overlappen bars de main area. Bars vóór main stapelen top-to-bottom, bars ná main stapelen bottom-to-top.

### Optie C: Side by Side Split View

Horizontale gelijke panelen naast elkaar. Panelen die niet passen worden automatisch verborgen.

```html
<nldd-side-by-side-split-view panes="3">
  <nldd-page slot="pane-1">...</nldd-page>
  <nldd-page slot="pane-2">...</nldd-page>
  <nldd-page slot="pane-3">...</nldd-page>
</nldd-side-by-side-split-view>
```

### Optie D: Stacked Split View

Verticale gelijke panelen gestapeld. Panelen die niet passen worden automatisch verborgen.

```html
<nldd-stacked-split-view panes="2">
  <nldd-page slot="pane-1">...</nldd-page>
  <nldd-page slot="pane-2">...</nldd-page>
</nldd-stacked-split-view>
```

### Optie E: Enkele pagina (geen split view)

Voor eenvoudige pagina's zonder navigatiepanelen.

```html
<nldd-app-view>
  <nldd-page sticky-header>...</nldd-page>
</nldd-app-view>
```

---

## Laag 3: Pagina (nldd-page)

Elk paneel in een split view bevat een `nldd-page`. Een page biedt scrollgedrag, optionele sticky header en footer.

```html
<nldd-page sticky-header sticky-footer background="inherit|default|tinted">
  <nldd-container slot="header" padding="16">
    <!-- Navigatiebalk of titelbalk — altijd in een container -->
  </nldd-container>

  <!-- Page sections met content -->
  <nldd-simple-section>...</nldd-simple-section>

  <nldd-container slot="footer" padding="16">
    <!-- Footer content — altijd in een container -->
  </nldd-container>
</nldd-page>
```

**Regel:** Header en footer content staan altijd in een `nldd-container` om items de juiste ruimte te geven.

| Attribuut | Beschrijving |
|-----------|--------------|
| `sticky-header` | Header blijft bovenaan bij scrollen |
| `sticky-footer` | Footer blijft onderaan |
| `background` | `inherit` (van parent), `default` (wit), `tinted` (grijs) |

| Slot | Beschrijving |
|------|--------------|
| `header` | Navigatie, titelbalk (optioneel sticky) |
| default | Scrollbare content (secties) |
| `footer` | Footer content (optioneel sticky) |

---

## Laag 4: Header-componenten

### Top Navigation Bar (applicatie-niveau)

De hoofdnavigatiebalk met logo, titel, menu en utility-items. Typisch in de header van de sidebar of bovenste page.

```html
<nldd-top-navigation-bar
  title="Mijn Applicatie"
  container="md"
  logo-has-wordmark
  logo-title="Rijksoverheid"
>
</nldd-top-navigation-bar>
```

| Attribuut | Beschrijving |
|-----------|--------------|
| `title` | Paginatitel |
| `container` | `sm`, `md`, `lg` |
| `no-logo`, `no-title`, `no-menu` | Verberg onderdelen |
| `has-back-button`, `back-href`, `back-text` | Terugknop |
| `logo-has-wordmark`, `logo-title`, `logo-subtitle` | Logo met tekst |
| `utility-no-language-switch`, `utility-no-search`, `utility-no-account` | Verberg utility items |

### Top Title Bar (pagina/paneel-niveau)

Titelbalk voor panelen met optionele terugknop en toolbar. Wanneer er een anchor-titel in de content staat (`collapse-anchor`), schakelt de title bar automatisch van default naar compact zodra dat element de bovenkant van de scroll-container bereikt.

```html
<nldd-top-title-bar
  text="Documenttitel"
  supporting-text="Ondertitel"
  back-text="Terug naar overzicht"
  collapse-anchor="content-heading"
>
  <nldd-icon-button slot="toolbar" icon="edit"></nldd-icon-button>
</nldd-top-title-bar>
```

| Attribuut | Beschrijving |
|-----------|--------------|
| `text` | Titel |
| `supporting-text` | Ondertitel |
| `back-text`, `back-href` | Terugknop |
| `dismiss-text` | Sluitknop |
| `collapse-anchor` | ID van element dat compact-modus triggert bij scrollen |

| Slot | Beschrijving |
|------|--------------|
| `toolbar` | Actieknoppen naast de sluitknop |

### Tab Bar (navigatie binnen paneel)

```html
<nldd-tab-bar navigation responsive accessible-label="Hoofdnavigatie">
  <nldd-tab-bar-item text="Overzicht" href="/overzicht" selected>
    <nldd-icon slot="icon" name="home"></nldd-icon>
  </nldd-tab-bar-item>
  <nldd-tab-bar-item text="Instellingen" href="/instellingen">
    <nldd-icon slot="icon" name="settings"></nldd-icon>
  </nldd-tab-bar-item>
</nldd-tab-bar>
```

| Attribuut | Beschrijving |
|-----------|--------------|
| `navigation` | Rendert als `<nav>` in plaats van tablist (voor route-navigatie) |
| `responsive` | Automatisch compact onder 480px |
| `full-width` | Volle breedte |
| `compact` | Altijd icon boven tekst |
| `variant` | `icon-and-text`, `text`, `icon` |

### Menu Bar (horizontaal menu)

```html
<nldd-menu-bar has-overflow-menu>
  <nldd-menu-bar-item selected>Wetten</nldd-menu-bar-item>
  <nldd-menu-bar-item>Regelingen</nldd-menu-bar-item>
  <nldd-menu-bar-item>Besluiten</nldd-menu-bar-item>
</nldd-menu-bar>
```

| Attribuut | Beschrijving |
|-----------|--------------|
| `has-overflow-menu` | Automatische overflow-knop bij beperkte ruimte |
| `size` | `s`, `m`, `l` |

### Document Tab Bar (document-tabs)

```html
<nldd-document-tab-bar accessible-label="Open documenten">
  <nldd-document-tab-bar-item text="Document 1" selected></nldd-document-tab-bar-item>
  <nldd-document-tab-bar-item text="Document 2"></nldd-document-tab-bar-item>
  <nldd-icon-button slot="end" icon="plus"></nldd-icon-button>
</nldd-document-tab-bar>
```

---

## Laag 5: Page sections (content layout)

Page sections organiseren content binnen een page. Ze bieden responsieve padding en gap via container queries.

### Beschikbare page sections

| Component | Layout | Beschrijving |
|-----------|--------|--------------|
| `nldd-simple-section` | Enkele kolom | Basis sectie met header/footer slots |
| `nldd-full-bleed-section` | Volle breedte | Zonder horizontale padding (achtergrondkleuren, afbeeldingen) |
| `nldd-one-third-two-thirds-section` | 1/3 + 2/3 | Sidebar links, content rechts |
| `nldd-two-thirds-one-third-section` | 2/3 + 1/3 | Content links, sidebar rechts |
| `nldd-one-half-one-half-section` | 1/2 + 1/2 | Twee gelijke kolommen |

### Voorbeeld: Simple Section

```html
<nldd-simple-section>
  <nldd-rich-text slot="header"><h2>Titel</h2></nldd-rich-text>
  <nldd-rich-text>
    <p>Inhoud van de sectie.</p>
  </nldd-rich-text>
  <nldd-rich-text slot="footer"><p>Voetnoot</p></nldd-rich-text>
</nldd-simple-section>
```

### Voorbeeld: Twee-koloms sectie

```html
<nldd-one-third-two-thirds-section>
  <nldd-rich-text slot="header"><h2>Titel</h2></nldd-rich-text>
  <nldd-rich-text slot="left">
    <p>Zijbalk content</p>
  </nldd-rich-text>
  <nldd-rich-text>
    <p>Hoofdinhoud (2/3 breedte)</p>
  </nldd-rich-text>
</nldd-one-third-two-thirds-section>
```

**Responsief:** Kolommen wrappen automatisch wanneer ze smaller worden dan 280px.

---

## Laag 6: Content-componenten

Binnen secties gebruik je content- en interactiecomponenten:

| Categorie | Componenten | Beschrijving |
|-----------|-------------|--------------|
| **Content** | `nldd-rich-text`, `nldd-title`, `nldd-icon`, `nldd-tooltip` | Tekst en visuele content |
| **Actions** | `nldd-button`, `nldd-icon-button`, `nldd-toolbar` | Knoppen en acties |
| **Inputs** | `nldd-text-field`, `nldd-dropdown`, `nldd-checkbox`, `nldd-radio-button`, `nldd-switch` | Formulier-invoer |
| **Forms** | `nldd-form-field` | Formulierveld wrapper met label en foutmelding |
| **Lists** | `nldd-list`, `nldd-menu`, `nldd-cell` | Lijsten en menu's |
| **Feedback** | `nldd-dialog`, `nldd-modal` | Dialogen en modals |
| **Layout** | `nldd-container`, `nldd-box`, `nldd-spacer`, `nldd-divider` | Spacing en groepering |

---

## Hulpcomponenten

### Container (padding wrapper)

```html
<nldd-container padding="16" md-padding="24" lg-padding="32">
  <!-- Content met responsieve padding -->
</nldd-container>
```

Geldige padding-waarden: `0`, `2`, `4`, `6`, `8`, `10`, `12`, `16`, `20`, `24`, `28`, `32`, `40`, `44`, `48`, `56`, `64`, `80`, `96`

### Box (visuele groepering)

```html
<nldd-box>
  <!-- Gerelateerde componenten in een visueel afgebakend gebied -->
</nldd-box>
```

### Sheet (overlay paneel)

```html
<nldd-sheet placement="right|left|bottom" accessible-label="Details">
  <!-- Sheet content -->
</nldd-sheet>
```

Methoden: `show()`, `hide()`

### Spacer

```html
<nldd-spacer size="32"></nldd-spacer>
```

Sizes: `2`, `4`, `6`, `8`, `12`, `16`, `20`, `24`, `32`, `40`, `44`, `48`, `64`, `80`, `96`, `m`, `flexible`

---

## Achtergrondkleur

Achtergrondkleur wordt gecascade via `--context-parent-background-color`:

1. Stel `background` in op `nldd-app-view` voor de hele applicatie
2. Of stel `background` in op individuele `nldd-page` componenten per paneel
3. Kinderen lezen de variabele automatisch

```html
<!-- Hele app tinted -->
<nldd-app-view background="tinted">...</nldd-app-view>

<!-- Per paneel -->
<nldd-app-view>
  <nldd-navigation-split-view>
    <nldd-split-view-pane slot="sidebar">
      <nldd-page background="tinted">...</nldd-page>
    </nldd-split-view-pane>
    <nldd-split-view-pane slot="main">
      <nldd-page background="default">...</nldd-page>
    </nldd-split-view-pane>
  </nldd-navigation-split-view>
</nldd-app-view>
```

---

## Voorbeeldpagina's

### Voorbeeld 1: Applicatie met navigatie

```html
<nldd-app-view background="default">
  <nldd-navigation-split-view>
    <!-- Sidebar met navigatie -->
    <nldd-split-view-pane slot="sidebar">
      <nldd-page sticky-header background="tinted">
        <nldd-container slot="header" padding="16">
          <nldd-top-title-bar text="Navigatie"></nldd-top-title-bar>
        </nldd-container>
        <nldd-simple-section>
          <nldd-list>
            <!-- Navigatie-items -->
          </nldd-list>
        </nldd-simple-section>
      </nldd-page>
    </nldd-split-view-pane>

    <!-- Hoofdinhoud -->
    <nldd-split-view-pane slot="main">
      <nldd-page sticky-header>
        <nldd-container slot="header" padding="16">
          <nldd-top-title-bar text="Documenttitel" supporting-text="Laatst bewerkt: vandaag">
            <nldd-icon-button slot="toolbar" icon="edit"></nldd-icon-button>
          </nldd-top-title-bar>
        </nldd-container>
        <nldd-simple-section>
          <nldd-rich-text>
            <h2>Inhoud</h2>
            <p>Primaire content van de pagina.</p>
          </nldd-rich-text>
        </nldd-simple-section>
      </nldd-page>
    </nldd-split-view-pane>

    <!-- Inspector voor details -->
    <nldd-split-view-pane slot="inspector">
      <nldd-page sticky-header>
        <nldd-container slot="header" padding="16">
          <nldd-top-title-bar text="Eigenschappen"></nldd-top-title-bar>
        </nldd-container>
        <nldd-simple-section>
          <nldd-rich-text>
            <p>Details over het geselecteerde item.</p>
          </nldd-rich-text>
        </nldd-simple-section>
      </nldd-page>
    </nldd-split-view-pane>
  </nldd-navigation-split-view>
</nldd-app-view>
```

### Voorbeeld 2: Eenvoudige pagina

```html
<nldd-app-view>
  <nldd-page sticky-header>
    <nldd-top-navigation-bar
      slot="header"
      title="Rijksoverheid"
      logo-has-wordmark
      logo-title="Rijksoverheid"
    >
    </nldd-top-navigation-bar>

    <nldd-simple-section>
      <nldd-rich-text>
        <h1>Welkom</h1>
        <p>Een eenvoudige pagina zonder split view.</p>
      </nldd-rich-text>
    </nldd-simple-section>

    <nldd-two-thirds-one-third-section>
      <nldd-rich-text>
        <h2>Hoofdartikel</h2>
        <p>Content in 2/3 breedte.</p>
      </nldd-rich-text>
      <nldd-rich-text slot="right">
        <h3>Gerelateerd</h3>
        <p>Sidebar content in 1/3 breedte.</p>
      </nldd-rich-text>
    </nldd-two-thirds-one-third-section>

    <nldd-container slot="footer" padding="16">
      <nldd-rich-text>
        <p>Footer informatie</p>
      </nldd-rich-text>
    </nldd-container>
  </nldd-page>
</nldd-app-view>
```

### Voorbeeld 3: Applicatie met toolbar

```html
<nldd-app-view>
  <nldd-bar-split-view>
    <nldd-container slot="toolbar" sm-order="1" md-order="1">
      <nldd-tab-bar navigation responsive>
        <nldd-tab-bar-item text="Start" selected></nldd-tab-bar-item>
        <nldd-tab-bar-item text="Zoeken"></nldd-tab-bar-item>
      </nldd-tab-bar>
    </nldd-container>

    <nldd-page slot="main" sm-order="2" md-order="2" sticky-header>
      <nldd-container slot="header" padding="16">
        <nldd-top-title-bar text="Overzicht"></nldd-top-title-bar>
      </nldd-container>
      <nldd-simple-section>
        <nldd-rich-text>
          <p>Content onder de toolbar.</p>
        </nldd-rich-text>
      </nldd-simple-section>
    </nldd-page>
  </nldd-bar-split-view>
</nldd-app-view>
```

---

## Beslisboom: welke layout?

```
Heeft de app een zijnavigatie?
├── Ja → nldd-navigation-split-view
│   ├── Met details-paneel? → voeg inspector slot toe
│   ├── Met subnavigatie? → voeg secondary-sidebar slot toe
│   └── Met toolbars in main? → nest nldd-bar-split-view in main slot
│
├── Nee, maar wel toolbars/statusbalken?
│   └── nldd-bar-split-view
│
├── Nee, maar meerdere gelijke panelen naast elkaar?
│   └── nldd-side-by-side-split-view
│
├── Nee, maar meerdere gelijke panelen gestapeld?
│   └── nldd-stacked-split-view
│
└── Nee, gewoon één pagina
    └── nldd-page direct in nldd-app-view
```

**Nesting:** Split views kunnen in elkaar genest worden. Plaats een geneste split view in een `nldd-split-view-pane` binnen het gewenste slot.
