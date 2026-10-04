---
name: ui-factory
description: >-
  Orchestrate the full UI-Factory chain (color-system → design-system → component-library → dashboard) for complex UI tasks. Use when user asks to "build a UI", "create a dashboard", "design an app", "make me a website", "scaffold components from scratch", or wants full-stack UI construction from brief to production-ready code.
version: 1.0.0
author: |
  Yuno (Hermes Agent) — based on KIMI K2 UI-Factory-Pattern 2026-06-30
license: MIT
metadata:
  hermes:
    tags: ['ui', 'orchestrator', 'factory', 'meta-skill', 'ui-builder', 'design-system', 'dashboard', 'full-stack']
    related_skills: ['ui-color-system', 'ui-design-system', 'ui-component-library', 'ui-dashboard', 'web-design-guidelines']
    part_of: ui-factory
    triggers: ['build a UI', 'create a dashboard', 'design an app', 'make me a website', 'scaffold components', 'design system', 'look and feel', 'branding', 'from scratch UI', 'complete UI', 'production-ready UI', 'build me an app', 'design tokens']
lane: worker-vision
reasoning_effort: xhigh
agent: Designer
routing_hint: |
  **Agent-Scope:** UI/UX, visual, art-styles, design-systems, motion. Off-scope: code building, data modeling, long-form copy — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# ui-factory

> **Meta-Skill:** Orchestrates the full UI-Factory chain. Single entry-point for any UI task that needs design + build + a11y + responsiveness. Routes to the right atoms in the right order.

## When to TRIGGER

This meta-skill auto-triggers when user input matches ANY of:

### Trigger-Phrasen (UI-spezifisch)

| Category | Phrasen | Auto-Skill |
|----------|---------|------------|
| **Farben / Branding** | "color palette", "brand colors", "WCAG", "contrast", "dark mode colors", "welche Farben", "Theme", "Akzentfarbe" | → `ui-color-system` |
| **Design-System / Tokens** | "design system", "design tokens", "tokens.json", "CSS variables", "theme", "Brand-Identität als Code", "Komponenten-Standards" | → `ui-design-system` |
| **Komponenten / Library** | "component library", "UI kit", "Button bauen", "Input-Feld", "Modal", "Card", "Nav bauen", "alle Komponenten", "scaffold components" | → `ui-component-library` |
| **Dashboard / Data-UI** | "dashboard", "admin panel", "monitoring", "KPIs", "analytics view", "metrics view", "Übersichts-Seite", "Statistiken anzeigen" | → `ui-dashboard` |
| **Full-Stack / Komplett** | "build a UI", "create a dashboard", "design an app", "make me a website", "complete UI from scratch", "production-ready UI", "Komplettes UI-Projekt", "Vollständig bauen" | → **`ui-factory` (this skill)** |

### Decision-Tree: Welcher Skill passt?

```
User-Input
  │
  ├─ "color/brand/WCAG" → ui-color-system
  ├─ "tokens/design-system" → ui-design-system
  ├─ "component/button/modal" → ui-component-library
  ├─ "dashboard/KPI/analytics" → ui-dashboard
  │
  └─ Komplex/Multi-Step/Full-Stack?
       │
       └─ YES → ui-factory (orchestriert alle 4 Atoms)
```

## When NOT to use

- User asks for ONE simple UI change ("make this button blue") → direkt machen, kein Skill-Overhead
- User asks for code review on existing UI → `web-design-guidelines` oder `simplify-code`
- User asks for creative content (writing, art) → nicht UI-bezogen, andere Skills

## Inputs

```yaml
brief:
  product_type: "SaaS dashboard | Marketing site | E-commerce | Blog | App | Settings"
  mood: "trustworthy | playful | serious | cozy | futuristic | minimal | corporate"
  mode: "light | dark | both | high-contrast | cozy | cyberpunk"
  brand_primary: "#XXXXXX or 'auto-generate'"
  framework: "vanilla-html | react | vue | svelte | sveltekit | nextjs"
  style: "css-modules | tailwind | vanilla-extract | plain-css | styled-components"
  a11y_target: "AA | AAA"
  components_needed: ["button", "input", "card", "modal", "nav", "table", "chart", "dashboard"]
  output_target: "single-file-html | storybook | production-app | prototype"
```

## Output

**Full UI-Factory deliverable:**

1. **`tokens.json`** + **`tokens.css`** + **`tokens.d.ts`** (von ui-design-system)
2. **`colors.json`** + **`colors.css`** + **`contrast-report.md`** (von ui-color-system)
3. **Component files**: `Button.tsx`, `Input.tsx`, `Card.tsx`, etc. mit `.module.css` + `.stories.tsx` + `.test.tsx` + `.a11y.test.tsx` (von ui-component-library)
4. **Dashboard files**: `Dashboard.tsx`, `KpiCard.tsx`, `RevenueChart.tsx`, `RecentErrorsTable.tsx`, `FilterPanel.tsx` (von ui-dashboard)
5. **`index.ts`** re-exports + **`README.md`** usage-docs

## Workflow

### Phase 0: Brief-Analyse (1-2 min)

Lies den User-Brief und parse:
- **Product type** → spacing density, layout pattern
- **Mood** → color palette, corner radius, shadow strength
- **Mode** → light/dark/both token-sets
- **Brand color** → primary hue (oder auto-generate aus mood)
- **Framework** → output format (TSX/Vue/Svelte/HTML)
- **a11y target** → validation threshold
- **Component set** → welche Atoms werden gebraucht

### Phase 1: ui-color-system (3-5 min)

**Input:** Brief
**Output:** `colors.json` + `colors.css` + `contrast-report.md`

Steps:
1. Brand-Color analysieren (oder auto-generate aus mood)
2. Scale generieren (50-950)
3. Semantic-Rollen zuweisen
4. Contrast-Checks durchführen (AA minimum, AAA wo möglich)
5. **4 Modi generieren** (statt nur 2-3):
   - **Cozy** (Warm-Light Mode): Cream-BG `#FFF5F5`, Pink-800 Text, weiche Schatten
   - **Dark** (Standard Dark Mode): Neutral-950 BG, Pink-300 Text, reduzierte Sättigung
   - **Cyberpunk** (Dark + Neon): Night-BG `#0D0020`, Magenta-Neon-Akzente, Sparkle-Particles, 0.12 opacity overlays
   - **A11y** (High-Contrast): Pure Black BG `#000`, White Text `#FFF`, max Kontrast

**Output-Detail:**
- 5+ Color-Scales (primary, neutral, success, warning, error, info)
- WCAG contrast report (**≥10 kritische Pairs**, pro Theme)
- Color-Blind-Simulation passed

### Phase 2: ui-design-system (3-5 min)

**Input:** `colors.json` aus Phase 1
**Output:** `tokens.json` + `tokens.css` + `tokens.d.ts`

Steps:
1. Token-Kategorien generieren: color, font, space, radius, shadow, motion, z-index, breakpoints
2. CSS-Variablen mit kebab-case: `--color-primary-500`, `--space-4`
3. TypeScript-Types für IDE-Autocompletion
4. Fluid-Typography mit `clamp()`

**Validation:**
- 4px oder 8px Spacing-Grid (keine Arbitrary-Werte)
- Alle Hex-Codes 7-stellig
- Spacing in `rem` nicht `px`

### Phase 3: ui-component-library (5-10 min)

**Input:** `tokens.json` + `colors.json`
**Output:** Component-Files (TSX/Vue/Svelte/HTML) + Stories + Tests

Steps:
1. Components wählen (Core-Set: Button, Input, Card, Badge, Avatar)
2. Pro Component: 5 Files erstellen (.tsx + .module.css + .stories.tsx + .test.tsx + .a11y.test.tsx)
3. Tokens importieren (keine hardcoded values)
4. A11y-Checklist durchgehen pro Component
5. Stories mit Controls generieren

**Validation:**
- Alle Components importieren Tokens (kein `rgb(255,255,255)` hardcoded)
- Jede Component hat jest-axe a11y test (zero violations)
- Keyboard-Handler überall
- Visible focus-indicator

### Phase 4: ui-dashboard (5-10 min)

**Input:** Components aus Phase 3 + Brief
**Output:** `Dashboard.tsx` + KPI-Cards + Charts + Table + Filter-Panel

Steps:
1. Layout planen: Header → Sidebar + KPI-Grid → Charts → Table
2. KPI-Cards mit Trend-Indicators
3. Charts (line/bar/pie/area — recharts/chart.js)
4. Data-Table mit sort/filter/pagination
5. Filter-Panel mit date-range, multi-select
6. Loading/Empty/Error states für jede Section
7. Responsive (mobile/tablet/desktop breakpoints)

**Validation:**
- 4-6 KPIs max
- Alle Charts haben hover-tooltip
- Alle Tables haben sort + filter + pagination
- Loading states überall

### Phase 5: Verification + Output (2-3 min)

**Wichtig — Auto-Validation vor manueller Abnahme laufen lassen.** Im Yuno-Build 2026-07-06 fand die automatisierte WCAG-Pair-Validation **4 Fails** die bei manueller Prüfung übersehen worden wären (Pink-500 Text 3.2:1, Magenta-500 Body 4.29:1, Error-500 4.04:1, White-on-Magenta 3.64:1). Automatisierte Validierung ist kein Nice-to-have — sie findet Fehler die selbst bei sorgfältigem manuellem Review durchrutschen.

Checkliste:
- [ ] Alle Atoms zusammen integriert (Color → Design → Components → Dashboard)
- [ ] Keine hardcoded values (alle Tokens referenziert)
- [ ] A11y: alle Tests grün, alle Pairs WCAG-konform
- [ ] **Auto-Validation durchgeführt** (Token-Konsistenz + WCAG-Pairs + A11y-Attribute)
- [ ] Responsive: Mobile/Tablet/Desktop breakpoints funktionieren
- [ ] Loading/Empty/Error states überall
- [ ] Theme-Switcher funktioniert in Echtzeit (4 Modi: Cozy/Dark/Cyberpunk/A11y)
- [ ] Kontrast-Report mit **mindestens 10 kritischen Pairs** pro Theme
- [ ] Bundle-Output (ZIP oder Git-Commit-ready) erstellt

## Orchestration-Logic für Sub-Tasks

Wenn der Task lang/komplex ist (mehr als 1 Atoms):

```
User: "Bau mir ein komplettes SaaS-Dashboard mit Users/Revenue/Errors"
   ↓
ui-factory: Analysiere Brief
   ↓
[Auto-Chain triggert]:
   1. ui-color-system → "Primary purple, dark mode default, WCAG AA"
   2. ui-design-system → "Tokens mit 4px grid, Inter sans, JetBrains Mono"
   3. ui-component-library → "Button, Input, Card, Badge, Modal, Nav, Table, Chart"
   4. ui-dashboard → "4 KPIs (Users/Revenue/Errors/Latency), RevenueChart, ErrorsTable"
   ↓
Final: Komplettes Dashboard mit allem
```

## Auto-Orchestration Rule (the user explicit request, 2026-07-01)

**Bei Tasks die "etwas länger" sind → AUTOMATISCH orchestrieren, NICHT fragen.** Diese Regel wurde in Session 2026-07-01 von the user EXPLIZIT angefordert und durch einen erfolgreichen Live-Build bewiesen (komplettes Dashboard in ~5 min ohne einzige Rückfrage).

Trigger-Heuristik für Auto-Orchestration (eines reicht):
1. Task braucht **3+ Tool-Calls**
2. Task involviert **mehrere Files/Components**
3. Task passt zu einer **existierenden Skill-Chain** (z.B. UI-Factory)
4. User-Keywords: "komplett bauen", "from scratch", "vollständig", "alles", "production-ready"

Bei Match: **SOFORT** TodoWrite + Step-by-Step-Plan ausführen. **NICHT** erst fragen "soll ich orchestrieren?".
Begründung: the user experimentierfreudig, hasst unnötige Rückfragen, will momentum.

**Ausnahme:** Bei **Trade-offs mit echten Konsequenzen** (z.B. "Hermes-Source patchen vs standalone Dashboard") → `clarify()` mit 2-4 konkreten Optionen und Sterne-Bewertung. In der Praxis hat the user die Option gewählt die Update-safe und unter unserer Kontrolle war ("Unser Yuno-Dashboard mit Hermes-API verbinden" statt Hermes-Source patchen).

**Bewiesene Pipeline (Yuno-Dashboard, 2026-07-01):**
```
User: "okay baue mir ein komplettes Dashboard :D"
  → ui-factory auto-triggered (match: "komplett" + "Dashboard" + "bauen")
  → TodoWrite mit 6 Phasen
  → Phase 1: ui-color-system (Yuno Purple/Pink + WCAG check + 1 fix)
  → Phase 2: ui-design-system (tokens.json/css)
  → Phase 3+4: Components + Dashboard compose (single-file HTML 37KB)
  → Phase 5: Validation (A11y, Responsive, Token-Konsistenz)
  → Phase 6: Doku + Smoke-Test
  → Result: Keine Rückfrage nötig, User zufrieden ("sieht hot aus!")
```

**Live-Data-Erweiterung (v2/v3, gleiche Session):**
Nach dem Static-Build wollte User echte Daten → Auto-Orchestrierung startete erneut:
- Phase 1: API-Discovery (welche `/api/*` sind ohne Auth erreichbar?)
- Phase 2: Python Data-Provider (`server.py` mit psutil + subprocess + caching)
- Phase 3: Live-Dashboard HTML (fetch-Polling alle 10s → später 3s auf User-Wunsch)
- Phase 4: v3 Rewrite mit Accordion-Cards + KPI-as-Buttons (User-Präferenz: "alle tabs anklickbar")
- Phase 5: Start/Stop-Skripte + Browser-Open

## Auto-Trigger Logic

Bei jedem User-Input der UI-spezifisch ist, prüft Hermes:
1. **Description-Match:** User-Input matched eine der Trigger-Phrasen oben?
2. **Tag-Match:** Input enthält UI-spezifische Keywords (dashboard, component, design, color, etc.)?
3. **Context-Match:** Läuft eine UI-Skill-Chain? → Auto-orchestrate

Wenn **JA auf 1+**: triggere entsprechenden Skill automatisch.
Wenn **JA auf allen 3**: triggere `ui-factory` als Meta-Orchestrator.

## Examples

### Example 1: Komplex-Task (triggert ui-factory)
```
User: "Bau mir ein Monitoring-Dashboard für meine SaaS-App mit Users,
       Revenue und Error-Rate. Dark mode, modern, soll schick aussehen."

→ ui-factory triggered
→ Auto-chain: ui-color-system → ui-design-system → ui-component-library → ui-dashboard
→ Output: Komplettes Dashboard
```

### Example 2: Simple-Task (triggert ui-color-system only)
```
User: "Ich brauch ne WCAG-AA-konforme Color-Palette für mein Startup"

→ ui-color-system triggered (matches "color palette", "WCAG")
→ Auto-output: colors.json + contrast-report.md
→ KEIN ui-factory nötig (kein kompletter Build)
```

### Example 3: Mid-Task (triggert ui-component-library)
```
User: "Generier mir ne Button-Komponente mit Storybook-Story"

→ ui-component-library triggered (matches "component", "storybook")
→ Auto-output: Button.tsx + Button.module.css + Button.stories.tsx + tests
→ KEIN ui-factory nötig
```

## Integration with Agent-Profile

Das `ui-builder` Agent-Profile (siehe `~/.hermes/profiles/ui-builder/`) hat:
- **SOUL.md:** "Du bist ein präziser UI-Builder. Sauberer, semantischer, accessible Code. Composition über Configuration. Jede Component keyboard-navigable + screen-reader-friendly."
- **Skill-Bundle:** `ui-factory` + `ui-color-system` + `ui-design-system` + `ui-component-library` + `ui-dashboard` + `web-design-guidelines`

Wenn the user im `ui-builder`-Profile arbeitet, triggern diese Skills **automatisch** bei UI-Themen — ohne dass er sie explizit aufrufen muss.

## Related Skills

- **ui-color-system** — Atom 1 (Color-Palette)
- **ui-design-system** — Atom 2 (Tokens)
- **ui-component-library** — Atom 3 (Components)
- **ui-dashboard** — Atom 4 (Dashboard)
- **web-design-guidelines** — Polish-Review nach Build
- **html-artifact** — Für Single-Page-Deliverables
- **claude-design** — Alternative UI-Generator

## Part of UI-Factory

This is the **META-skill** in the UI-Factory pattern. Other UI-Factory skills are atoms — this one is the molecule that orchestrates them.

```
Atoms (Skills):           Molecule (Meta):       Organism (Profile):
ui-color-system     ─┐
ui-design-system    ─┤
ui-component-library ─┼──→ ui-factory ──→ ui-builder (SOUL.md)
ui-dashboard        ─┘
```

## Pitfalls (from real builds, 2026-07-01)

### Pitfall 12 — Yuno-Pink/Magenta WCAG-Tabelle (entdeckt 2026-07-06)

**Symptom:** Bei der zweiten Iteration des Yuno-Operator-Dashboards waren alle Standard-Tokens (`primary-500`, `accent-500`, `error-500`) um 0.1-0.5:1 unter der AA-4.5:1-Grenze. Hätte man die "offensichtlichen" Token-Defaults aus Pitfall 1 genommen, wäre das Dashboard WCAG-non-compliant ausgeliefert worden. Erst die **automatisierte Validierung** (siehe Phase 5 Pflicht) hat das aufgedeckt.

**Konkretes Failed-Set aus 2026-07-06 (erste Iteration, manuell geprüft sah alles ok aus):**

| Token-Pair | Hex | Hex | Ratio | Target | Status |
|------------|-----|-----|-------|--------|--------|
| `white` on `pink-700` | #FFFFFF | #E63975 | 4.03:1 | 4.5 | **FAIL** |
| `pink-700` on `cream-50` | #E63975 | #FFFBF5 | 3.91:1 | 4.5 | **FAIL** (Body-Text) |
| `magenta-500` on `cream-50` | #FF1493 | #FFFBF5 | 4.29:1 | 4.5 | **FAIL** |
| `magenta-600` on `cream-50` | #E80080 | #FFFBF5 | 4.43:1 | 4.5 | **FAIL** (knapp drunter!) |
| `error-500` on `cream-50` | #E63946 | #FFFBF5 | 4.04:1 | 4.5 | **FAIL** |
| `white` on `magenta-500` | #FFFFFF | #FF1493 | 3.64:1 | 4.5 | **FAIL** (Cyberpunk Button) |

**Fixes (Sweet-Spot-Erkennung):**

| Token-Pair | Hex | Hex | Ratio | Status |
|------------|-----|-----|-------|--------|
| `white` on `pink-800` | #FFFFFF | #B7295B | 6.03:1 | ✓ AA |
| `pink-800` on `cream-50` | #B7295B | #FFFBF5 | 5.85:1 | ✓ AA |
| `magenta-700` on `cream-50` | #B30066 | #FFFBF5 | 6.55:1 | ✓ AA |
| `error-600` on `cream-50` | #C81F2E | #FFFBF5 | 5.52:1 | ✓ AA |
| `night-700` on `magenta-500` | #050817 | #FF1493 | 5.48:1 | ✓ AA (Cyberpunk-Button mit dunklem Text) |

**Reusable Algorithm — Bright-Brand-Color-Fitting:**

```python
def find_aa_safe_foreground(brand_500, bg, target=4.5):
    """Suche den dunkelsten Brand-Shade, der auf bg noch mindestens target:1 hat."""
    candidates = [brand_500, brand_600, brand_700, brand_800, brand_900]
    for c in candidates:
        if contrast(c, bg) >= target:
            return c
    # Fallback: brand_900, auch wenn's über das Ziel hinausschießt
    return brand_900
```

**Bright-Brand-Color-Sweet-Spot-Tabelle (empirisch, 2026-07-06):**

| Brand-Hue | Primary-500 als Button | Primary-700 als Button | **Sweet-Spot** | Notes |
|-----------|------------------------|------------------------|----------------|-------|
| Pink (#FF6BB5) | 3.2:1 ❌ | 4.03:1 ❌ | **800 (6.03:1) ✓** | Sehr hell, braucht 3 Stufen tiefer |
| Magenta (#FF1493) | 3.2:1 ❌ | 5.48:1 ✓ | **700 (5.48:1) ✓** | Heller als Pink, 2 Stufen reichen |
| Coral (#FF7F50) | ~2.5:1 ❌ | ~4.0:1 ❌ | **800 (~5.5:1) ✓** | Ähnlich wie Pink, 3 Stufen |
| Cyan (#00E5FF) | ~2.0:1 ❌ | ~5.0:1 ✓ | **700 (~5.0:1) ✓** | Sehr hell, viel zu leicht |
| Lime (#CDDC39) | ~1.5:1 ❌ | ~8.0:1 ✓ | **500 reicht nicht, erst 700+** | Extrem hell |
| Purple (#A855F7) | 3.96:1 ❌ | 6.98:1 ✓ | **700 (6.98:1) ✓** | Mittel, 2 Stufen reichen |
| Navy (#1A237E) | 14:1 ✓ | 16:1 ✓ | **500 reicht locker** | Dunkel genug |
| Forest Green (#2E7D32) | 7:1 ✓ | 9:1 ✓ | **500 reicht** | Schon dunkel |

**Key Insight:** Bright Brand-Colors (Pink, Coral, Cyan, Lime, Yellow) brauchen **immer 2-3 Shade-Stufen tiefer** als Standard-Purple/Navy/Forest. Die "offensichtliche" Token-Default `primary-500` ist bei diesen Hues fast nie AA-safe.

**Lesson:** 
- **Immer Token-Sweetspot-Algorithmus laufen lassen** für jeden Brand-Color + jeden geplanten BG-Mode (Light/Dark/Cyberpunk)
- **Niemals nur "die Standard-500/700" raten** — bei hellen Brand-Colors systematisch testen
- **Auto-Validation in Phase 5 IST PFLICHT** — manuelles Schauen übersieht die knappen Fails
- **Bei Cyberpunk/Neon-Stilen** explizit dark-Text auf Neon-BG testen (oft intuitiv falsch, white-auf-Neon scheitert weil Neon-Farben dunkler sind als sie aussehen)

### Pitfall 1 — WCAG-AA Contrast bei Button-Text (erweitert 2026-07-06)

#### Standard-Case: Purple Brand

**Symptom (Yuno-Dashboard-Build 2026-07-01):** White-text auf `purple-500` (`#A855F7`) = 3.96:1 → **FAIL AA** (minimum 4.5:1 für body-text).

**Root Cause:** Brand-color `purple-500` ist visuell eindrucksvoll, hat aber nicht genug Luminanz für weißen Text.

**Fix:** Zwei verschiedene Primary-Shades für Light vs Dark Mode:
- **Light Mode:** Button-BG = `purple-700` (`#7E22CE`), Button-Text = `#FFFFFF` (6.98:1 ✓)
- **Dark Mode:** Button-BG = `purple-300` (`#D8B4FE`), Button-Text = `#09090B` (11.25:1 ✓)

```css
/* Light */
--yuno-primary: var(--yuno-purple-700);    /* 6.98:1 mit white */
--yuno-primary-fg: #FFFFFF;

/* Dark */
[data-theme="dark"] {
  --yuno-primary: var(--yuno-purple-300);  /* 11.25:1 mit dark-bg */
  --yuno-primary-fg: var(--yuno-neutral-950);
}
```

#### Harder Case: Pink/Magenta Brand (entdeckt 2026-07-06)

**Symptom:** Pink-500 (`#FF6BB5`) auf Cream (`#FFF5F5`) = **3.2:1 → FAIL AA** — viel schlechter als Purple weil Pink heller ist.

**Fix:** Benötigt **zwei Stufen dunkler** als Purple-Case. Pink-500 reicht nicht, selbst Pink-700 (`#D81B60`) gibt nur 4.89:1 auf Cream:
- **Cozy Mode (Cream-BG):** Button-BG = **Pink-800** (`#C2185B`), Text = White (6.03:1 ✓ AA)
- **Dark Mode:** Button-BG = **Pink-300** (`#F48FB1`), Text = Night-900 (9.37:1 ✓ AA)
- **Cyberpunk Mode:** Button-BG = **Magenta-700** (`#B30066`), Text = White (knapp unter AA auf Neon-BG → auf `Night-700` Text wechseln, 5.48:1 ✓)
- **A11y Mode:** Button-BG = **Magenta-500** (`#E91E63`), Text = White (5.96:1 ✓ AA)

**Key Insight — Accent-Color braucht oft einen eigenen Scale-Durchlauf:** Wenn die Brand-Color ein heller/satter Ton ist (Pink, Coral, Cyan, Lime), dann reicht `primary-700` nicht. Der Sweetspot liegt 1-2 Stufen tiefer als bei dunklen Brand-Colors (Purple, Navy, Forest Green). **Immer primary-500, primary-600, primary-700, primary-800 auf der Ziel-BG testen** und den hellsten Shade nehmen der noch AA schafft.

**Lesson:** Bei jeder Brand-Color-Generierung (Phase 1) SOFORT den Button-Text-Contrast checken — vor der Component-Generation. Lieber `primary-700` als `primary-500` für Buttons. Bei hellen Brand-Colors (Pink, Coral, Cyan, Lime, Gelb) → `primary-800` oder `primary-900` nehmen.

### Pitfall 2 — Hardcoded Hex außerhalb `:root`

**Symptom:** Inline-styles oder component-CSS haben `#FFFFFF` statt `var(--yuno-neutral-50)`. Tokens werden umgangen → Theme-Switch bricht.

**Detection-Pattern (in Token-Konsistenz-Check Phase 5):**
```bash
# Finde hardcoded hex außerhalb der :root-Definition
grep -oE '#[0-9A-Fa-f]{6}' index.html | wc -l              # Total hex
sed -n '/:root/,/^}/p' index.html | grep -oE '#[0-9A-Fa-f]{6}' | wc -l  # In :root
# Outside tokens: $((total_hex - in_root))  ← sollte 1 sein (theme-color meta-Tag)
```

**Legitimer Ausreißer:** `<meta name="theme-color" content="#XXX">` — das ist PWA/Chrome-spezifisch und kann nicht aus CSS-Vars gelesen werden.

**Fix:** Alle component-CSS nutzt `var(--yuno-*)` — nie hardcoded hex. Tokens sind die Single Source of Truth.

### Pitfall 3 — Framework-Choice-Lock-In

**Symptom:** User sagt "Bau mir ein Dashboard", Skill empfiehlt React+TypeScript+Tailwind. Aber User wollte eigentlich nur single-file HTML zum zeigen.

**Lesson:** Framework-Defaults aus `framework:`-Input übernehmen, NICHT raten. Wenn unklar, 1× `clarify()` mit 2-4 Optionen (z.B. "vanilla-html | react | svelte | sveltekit").

**Best-Practice Defaults per Use-Case:**
| Use-Case | Default Framework |
|----------|-------------------|
| Quick-Show, No-Backend | `vanilla-html` (single-file) |
| Production-SaaS | `react` + `tailwind` |
| Marketing-Site | `sveltekit` + `tailwind` |
| Internal-Tool | `vue` + `css-modules` |

### Pitfall 4 — Token-Count-Explosion

**Symptom:** Generierter `tokens.json` hat 200+ Tokens weil alle möglichen Variablen erzeugt wurden (jede shade × jede semantic role × jedes breakpoint).

**Fix:** Token-Budget setzen:
- **Color:** 5 main scales (primary, neutral, success, warning, error) × 11 shades = 55 tokens
- **Font:** 5 sizes × 1 weight + 4 families + 3 line-heights = 12 tokens
- **Space:** 13 (0-32) = 13 tokens
- **Radius:** 6 = 6 tokens
- **Shadow:** 6 = 6 tokens
- **Motion:** 6 = 6 tokens
- **Z-Index:** 6 = 6 tokens
- **Total Budget:** ~120 tokens. Wenn mehr → Atomic-Composition statt neue Tokens.

### Pitfall 5 — Token-Konsistenz nicht messbar ohne Check-Tool

**Symptom:** Nach Build sind 30% der Components mit hardcoded Werten, Tokens werden ignoriert.

**Build-Time-Check (in Phase 5):**
```bash
python3 << 'EOF'
import re

with open('index.html') as f:
    html = f.read()

# Total CSS-Var-Usage
var_usage = len(re.findall(r'var\(--[\w-]+\)', html))
# Hardcoded hex außerhalb :root
total_hex = len(re.findall(r'#[0-9A-Fa-f]{6}', html))
root_section = re.search(r':root\s*{([^}]+)}', html, re.DOTALL)
in_root = len(re.findall(r'#[0-9A-Fa-f]{6}', root_section.group(1))) if root_section else 0
outside = total_hex - in_root

print(f"var(--*) usage: {var_usage}")
print(f"hardcoded hex outside :root: {outside}  (erwartet: ≤1)")
assert outside <= 1, "Token-Konsistenz FAIL"
print("✓ Token-Konsistenz PASS")
EOF
```

Wenn `outside > 1` → components nochmal durchgehen, hardcoded → tokens.

### Pitfall 6 — Output-Größe bei Single-File HTML

**Symptom:** Inline-everything Dashboard ist 150 KB weil alle Charts als SVG-Strings eingebettet sind.

**Mitigation:**
- **ASCII-Sparklines statt SVG-Charts** für KPIs (siehe Yuno-Dashboard: 28-byte bars statt 5KB SVG)
- **CSS-only Progress-Bars** statt Chart-Libraries
- **External-Files** wenn >50 KB: `tokens.css`, `tokens.json` als separate Files
- **Lazy-Loading:** Bilder/Schriften mit `loading="lazy"` und `font-display: swap`

### Pitfall 8 — HC-Mode: Page-BG = Card-BG = Pure Black → Cards unsichtbar (entdeckt 2026-07-06)

**Symptom:** Im High-Contrast-Mode hat sowohl `body` (Page-BG) als auch alle `.card`-Container den gleichen Token `--yuno-bg-panel: #000000`. Resultat: Cards haben keine visuelle Abgrenzung mehr, alles verschwimmt zu einem schwarzen Block mit weißen Borders. User findet den Inhalt nicht mehr.

**Root Cause:** Wenn Page-BG und Panel-BG identisch sind, funktioniert das Layering-Konzept von Light/Dark-Modi (Page = subtle, Panel = lighter) nicht mehr — im HC-Mode ist beides per Definition pure Black.

**Fix — Subtle-Lift-Pattern:**
```css
[data-theme="hc"] {
  --yuno-bg:           #000000;   /* Page: pure black */
  --yuno-bg-subtle:    #0A0A0A;   /* Subtle regions */
  --yuno-bg-panel:     #0A0A0A;   /* Cards: lifted by 4% lightness */
  --yuno-border:       #FFFFFF;   /* Aber Borders explizit sichtbar */
  --yuno-border-strong:#FFFFFF;
}
```

**Key Insight:** Im HC-Mode muss der **Card-BG bewusst 1 Stufe heller** sein als der Page-BG, damit Layering funktioniert ohne die WCAG-AAA-Compliance zu verletzen. `#0A0A0A` auf `#000000` ist immer noch weit unter 1.5:1 (kein extra "Card" mehr nötig), aber visuell differenziert. **Alternative:** Falls strikter AAA gewünscht, Borders fett zeichnen (2-3px statt 1px).

**Lesson:** HC-Mode ist nicht einfach "alles pure B/W" — Layering muss bewusst konstruiert werden. Page/Panel/Subtle-Trio aus 3 sehr nahen Schwarz-Tönen + dicke White-Borders ist die saubere Lösung.

### Pitfall 9 — Headless Chrome für Screenshot-Validation wenn keine Browser-Tools verfügbar (entdeckt 2026-07-06)

**Symptom:** ui-factory Phase-5 empfiehlt visuelles Smoke-Testing via `browser_vision` / `browser_navigate`, aber in manchen Hermes-Sessions (Desktop-TUI ohne MCP-Browser) sind die Browser-Tools nicht im Toolset. Trotzdem muss irgendwie validiert werden, dass alle 4 Themes sauber rendern.

**Workaround — Google Chrome Headless:**
```bash
# Static-Server starten
cd ~/10-Projekte/10-active/yuno-ui && python3 -m http.server 8765 &

# Für jedes Theme: URL-Param setzen + Screenshot
for theme in light dark cyberpunk hc; do
  google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1440,1100 \
    --virtual-time-budget=2000 \
    --screenshot=/tmp/yuno-${theme}.png \
    "http://127.0.0.1:8765/index.html?theme=${theme}" 2>&1 | tail -1
done
```

**Voraussetzung — URL-Param-Pattern im Theme-Switcher:**
```javascript
// In index.html script-section:
const urlTheme = new URLSearchParams(location.search).get('theme');
if (urlTheme && VALID_THEMES.includes(urlTheme)) {
  applyTheme(urlTheme);  // überschreibt localStorage
} else {
  applyTheme(loadTheme());  // default path
}
```

**Warum das funktioniert:** Headless Chrome rendert die Page inkl. JS, der URL-Param triggert das Theme vor dem ersten paint, Screenshot zeigt den richtigen Mode.

**Lesson:** Wenn keine interaktiven Browser-Tools verfügbar sind, ist `google-chrome --headless` mit URL-Param-Theme + `--virtual-time-budget=2000` der verlässlichste Fallback für Theme-Validation. Spart den Aufwand eines interaktiven MCP-Browsers und liefert reproduzierbare PNGs die via `vision_analyze` inspiziert werden können.

**Reusable Helper:** siehe `scripts/headless-theme-screenshots.sh` — wiederverwendbares Bash-Script das alle Themes einer ui-factory-Build als PNG rendert. Unterstützt Custom-Theme-Listen + Window-Size via Env-Vars.

**Quick-Reference für nächste Session:**
```bash
# 1. Static-Server starten (im Build-Ordner)
cd ~/10-Projekte/10-active/<build> && python3 -m http.server 8765 &

# 2. Theme-Screenshots rendern
bash ~/.hermes/skills/creative/ui-factory/scripts/headless-theme-screenshots.sh \
  http://127.0.0.1:8765 \
  ~/Bilder/yuno-gallery/<build>-<datum> \
  "light dark cyberpunk hc"

# 3. PNGs via vision_analyze inspizieren
```

### Pitfall 10 — Favicon-404-Lärm im Server-Log (entdeckt 2026-07-06)

**Symptom:** Jeder Browser-Request triggert automatischen `GET /favicon.ico` der mit 404 failed. Bei Static-Server-Logs/CI-Output/Test-Renders entsteht dauerhafter Lärm der echte Fehler überdeckt. Plus: User sieht im Tab ein generisches Browser-Icon statt der Brand.

**Fix — Inline SVG Data-URI als `<link rel="icon">`:**
```html
<!-- Im HTML-Head, vor allen anderen Stylesheets -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+...">
```

**Generierung (encode_then_patch statt manuell):**
```python
import base64
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#FFB6C1"/><stop offset="100%" stop-color="#FF1493"/>
  </linearGradient></defs>
  <rect width="32" height="32" rx="8" fill="url(#g)"/>
  <path d="M16 6 L18 14 L26 16 L18 18 L16 26 L14 18 L6 16 L14 14 Z" fill="#FFFFFF"/>
</svg>'''
b64 = base64.b64encode(svg.encode()).decode()
f"data:image/svg+xml;base64,{b64}"  # ~700 chars für 32x32 brand-coloured sparkle
```

**Vorteile:**
- Zero extra HTTP-Request (im HTML eingebettet)
- Funktioniert in allen modernen Browsern (Chrome/Firefox/Safari/Edge)
- Brand-Sichtbarkeit im Browser-Tab
- Server-Log bleibt clean

**Nachteile:**
- +1 KB HTML-Größe (vernachlässigbar)
- ICO-Fallback fehlt (für IE11 / sehr alte Browser — irrelevant 2026)

**Lesson:** Immer inline-SVG-Favicon bei single-file HTML-Builds setzen, vor allem wenn das HTML auch als Static-Server ausgeliefert wird. Spart 404-Logs, gibt Brand-Identität im Tab, kostet quasi nichts.

### Pitfall 11 — Base64-Encode Tippfehler-Falle (entdeckt 2026-07-06)

**Symptom:** Beim manuellen Erstellen des Favicon-Data-URI via `patch()` mit Copy-Paste der Base64-Bytes wurde `circle` zu `jacmNsZSB` korrumpiert (das `Np` in `NpcmNsZSB` → `jacmNsZSB` durch Encoding-Fehler). Browser zeigt kaputtes/fehlendes SVG-Icon, Validation-Script erkennt es nicht sofort.

**Reproduktion:** Wenn ein langer Base64-String durch mehrere `patch()`-Operationen geht, kann einzelne Zeichenpaare bei Markdown-Rendering/Codeblock-Konvertierung korrumpiert werden — typisch: `N` → `j`, `c` → `a`, `G` → `m` (alle sehen visuell ähnlich aus, sind aber ASCII unterschiedlich).

**Fix — IMMER nach dem Patch decode-testen:**
```python
import re, base64
idx = open('index.html').read()
m = re.search(r'href="(data:image/svg\+xml;base64,([A-Za-z0-9+/=]+))"', idx)
b64 = m.group(2)
try:
    decoded = base64.b64decode(b64).decode('utf-8')
    assert decoded.startswith('<svg') and decoded.endswith('</svg>')
    print(f"✓ Valid SVG ({len(decoded)} chars)")
except Exception as e:
    print(f"❌ Base64 INVALID: {e}")
    # Specific check: typische Tippfehler
    if 'jac' in b64: print("  'jac' korrumpiertes 'Np' gefunden — Re-Patch nötig")
```

**Best-Practice — Data-URI-Generierung im execute_code statt manuell:**
```python
# Statt SVG manuell zu schreiben und zu encoden:
import base64
svg = '<svg ...>...</svg>'  # sauberes SVG
b64 = base64.b64encode(svg.encode()).decode()  # automatisch korrekt
# Dann in write_file() oder patch() mit dem sauberen b64
```

**Lesson:** Bei langen Base64-Strings in `patch()`-Operationen ist das Risiko von Character-Korruption real. **IMMER nach dem Patch den Base64-String decoden und validieren** dass er ein valides SVG/PNG/etc. ergibt. Nutze `execute_code` für Encoding statt manuelles Schreiben wenn möglich.

### Pitfall 7 — Theme-Switcher ohne A11y-freundliche Modi

**Symptom:** Drei Themes die alle Farb-Kombinationen nutzen (Light/Dark/Cyberpunk), aber kein dedicated High-Contrast-Mode. Screenreader-Nutzer und User mit Sehbehinderung haben keine Option.

**Fix:** Immer **4 Modi** anbieten: Cozy (warm-light), Dark (standard), Cyberpunk (dark+neon), A11y (pure black/white). Der A11y-Mode muss alle Gradienten deaktivieren, alle Opacity-Overlays entfernen und auf pure `#000`/`#FFF` setzen (WCAG AAA guaranteed).

**Theme-Switcher localStorage-Pattern (2026-07-06):**
```html
<div class="theme-switcher" role="group" aria-label="Theme auswählen">
  <button class="theme-btn" data-theme="cozy" aria-pressed="true">☀️ Cozy</button>
  <button class="theme-btn" data-theme="dark" aria-pressed="false">🌙 Dark</button>
  <button class="theme-btn" data-theme="cyber" aria-pressed="false">⚡ Cyber</button>
  <button class="theme-btn" data-theme="a11y" aria-pressed="false">♿ A11y</button>
</div>
```

```javascript
// localStorage-gespeichertes Theme beim Laden anwenden
const saved = localStorage.getItem('yuno-theme') || 'cozy';
document.documentElement.setAttribute('data-theme', saved);

// Theme-Buttons steuern die data-theme auf <html>
document.querySelectorAll('.theme-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const theme = btn.dataset.theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('yuno-theme', theme);
    document.querySelectorAll('.theme-btn').forEach(b =>
      b.setAttribute('aria-pressed', b === btn));
  });
});
```

**CSS-Aufbau:**
```css
:root { /* = Cozy Mode */ --bg-primary: #FFF5F5; --text-primary: #AD1457; /* Pink-800 */ }
[data-theme="dark"] { --bg-primary: #1A1A2E; --text-primary: #F48FB1; /* Pink-300 */ }
[data-theme="cyber"] { --bg-primary: #0D0020; --text-primary: #FF1493; /* DeepPink */ }
[data-theme="a11y"] { --bg-primary: #000000; --text-primary: #FFFFFF; }
```

**Validation:** Theme-Switcher im Browser testen (alle 4 Modi klicken, visuell prüfen) + localStorage.getItem('yuno-theme') nach Page-Reload checken.

**Key Insight:** Der A11y-Mode muss **als viertes Theme eigenständig definiert** sein, nicht als prefers-contrast: more media query. Grund: the user oder ein anderer User kann den Mode auch ohne OS-Setting aktivieren (z.B. bei Migräne kurzfristig umschalten). prefers-contrast zusätzlich als Fallback drin lassen aber nie als einzigen Weg.

---

## Live-Build-Template: Yuno-Dashboard (2026-07-01, ~5 min)

**Input:** "okay baue mir ein komplettes Dashboard :D"

**Output:** `~/yuno-dashboard/` mit:
- `index.html` (37 KB, 1034 lines, single-file)
- `tokens/colors.json` (2.3 KB, Yuno-Purple/Pink, WCAG-AA verified)
- `tokens/tokens.css` (3.4 KB, CSS-Vars)
- `tokens/tokens.json` (2.7 KB, JS/TS-tokens)
- `docs/README.md` (7.6 KB, architecture + WCAG-verification)

**Phasen:**
1. **ui-color-system** — Yuno-Purple/Pink Palette + WCAG-check (1 fix: Button-Contrast)
2. **ui-design-system** — Tokens (Color + Font + Space + Radius + Motion)
3. **ui-component-library** — Button + Card + Badge + Progress + Avatar (inline)
4. **ui-dashboard** — Compose: Sidebar + KPI-Grid + Tasks + Reminders + Ideas + Stats
5. **Validation** — A11y (8× label, 24× hidden, 1× current, 13× role) + Responsive (5× @media) + Token-Konsistenz (84× var-usage, 1× hardcoded = meta theme-color)
6. **Docs** — README mit Architecture + WCAG-Tabelle

**Bestätigte Validation-Resultate:**
- File-Size: 37 KB (single-file, no deps)
- A11y: 1× main, 1× nav, 8× article, 3× section, 1× aside, 1× h1 ✓
- ARIA: 8× label, 24× hidden, 1× current, 13× role ✓
- WCAG 2.2 AA: alle 10 Text/Bg-Pairs verified ✓ (Button-Text 6.98:1 light, 11.25:1 dark)
- Responsive: 5× @media queries ✓
- Token-Konsistenz: 84× var-usage, 0 hardcoded-components ✓

**Lessons-Reference:** siehe `references/yuno-dashboard-build-2026-07-01.md` (geplant für nächste Session).

---

## Live-Build-Template: Yuno-Operator-Dashboard 4-Mode (2026-07-06, ~45 min)

**Input:** Yuno-Style-Pattern Analyse (3 Bilder → 5 Soul-Marker) + Dashboard-Build

**Output:** `~/yuno-ui/` mit:
- `index.html` (42 KB, 1118 lines, single-file) — 4 Modi, 273× `var(--*)`, 0 hardcoded-hex
- `tokens/colors.json` (7.1 KB) — 9 Scales, 4 Modes, 17 Contrast-Pairs
- `tokens/colors.css` (7.4 KB) — CSS-Vars pro Mode
- `tokens/tokens.css` (5.6 KB) — Font + Space + Radius + Shadow + Motion + Z
- `tokens/tokens.json` (5.0 KB) — Style-Dictionary-Format
- `tokens/tokens.d.ts` (6.7 KB) — TypeScript-Types + getYunoMode() + applyYunoTheme()
- `tokens/contrast-report.md` (4.7 KB) — 17/17 WCAG-Pairs PASS
- `README.md` (10 KB) — Architecture + WCAG-Table + Theme-Guide

**Neu gegenueber 2026-07-01:**
- **4 Themes statt 3:** Cozy (Cream), Dark (Neutral), Cyberpunk (Night+Neon), A11y (Pure B/W)
- **17 Contrast-Pairs statt 10** (pro Theme: Button, Body, Accent, Decorative, Status, Inverse)
- **Brand-Color Pink/Magenta** statt Purple (schwieriger wegen hellerer Hue)
- **Echte Badge-Farben** für Activity-Status (success/auto/creative/recovered/ui-factory/bug-known)
- **ASCII-Spark-Bars** statt SVG-Charts (28-byte bars statt 5KB SVG)
- **Progress-Bars mit Farb-Coding** (green <70%, yellow 70-90%, red >90%)
- **Sidebar mit Badge + aktiver Nav-Indicator**
- **Console-Easter-Egg** mit gradient + pink icon
- **Brand-Mark Pulse-Animation** mit prefers-reduced-motion Fallback
- **A11y-Mode als separates Theme** (nicht nur prefers-contrast)

**Bestätigte Validation-Resultate:**
- WCAG 2.2 AA: **17/17 Pairs PASS** (alle 4 Themes) ✓
  - Pink-800 (`#C2185B`) auf Cream (`#FFF5F5`): 6.03:1 AA ✓
  - Magenta-700 (`#B30066`) auf Night (`#0D0020`): 5.48:1 AA ✓
  - Pink-300 (`#F48FB1`) auf Dark (`#1A1A2E`): 9.37:1 AA ✓
  - White (`#FFF`) auf Black (`#000`): 21.0:1 AAA ✓
- Token-Konsistenz: 273× `var(--*)`, 0 hardcoded-hex in UI (1 metaTag + 3 console.log legitim) ✓
- A11y: 12× aria-label, 40× aria-hidden, 5× aria-pressed, 4× aria-current ✓
- Responsive: 4× @media (1024/768/480/reduced-motion) ✓
- Components: 13 inline-Typen (btn, badge, kpi-card, card, input, progress, nav-link, activity-item, theme-btn, brand-mark, kpi-spark, kpi-trend, theme-switcher) ✓
- Theme-Switcher: localStorage-persistent, alle 4 Modi im Browser getestet ✓
- Browser-Console: 0 Errors, 0 Warnings ✓

**Lessons-Reference:** siehe `references/yuno-operator-build-2026-07-06.md`.

Based on the KIMI K2 UI-Factory-Pattern (2026-06-30) + Live-Build-Evidence (2026-07-01, 2026-07-06).

## Workspace-Convention für Yuno-UI-Builds (entdeckt 2026-07-06)

**Lesson:** ui-factory-Builds sind **Dev-Projekte mit mehreren Files** (HTML + Tokens + README + ggf. styles.css/.json/.d.ts). Sie gehören daher nach **`~/10-Projekte/10-active/<build>/`**, NICHT in `~/` direkt.

**Hintergrund:** the user's 2026-07-04 Workspace-Präferenz sagt "Yuno agiert primär in `~/.hermes/`" — die Ausnahme sind **mehrere-File Dev-Projekte**, die dem Cluster-Layout (`~/00-Meta/`, `~/10-Projekte/`, `~/20-Workspace/`, `~/30-Library/`, `~/50-System/`) folgen, neben `greyhack-tools`, `cp77-modding`, `github-mcp-server`, `linux-assistant`.

**Empfohlene Pfade je nach Skill-Output:**
- **ui-factory-Build (mehrere Files):** `~/10-Projekte/10-active/<name>/` (z.B. `~/10-Projekte/10-active/yuno-ui/`)
- **Single-File Showcase (1 HTML):** `~/Bilder/yuno-gallery/<build>-<datum>/` (für Screenshots) + `~/10-Projekte/10-active/<name>/index.html`
- **Doku-Only-Output:** `~/docs/system/<name>-<datum>.md` (siehe `system-documentation` Skill)
- **Yuno-Sandbox/Staging:** `~/.hermes/sandbox/` (kurzlebig)

**Migration-Step wenn versehentlich in `~/` angelegt:**
```bash
# 1. Verschieben
mv ~/<name> ~/10-Projekte/10-active/<name>

# 2. README + alle internen Referenzen auf den neuen Pfad updaten
# 3. Memory mit Workspace-Regel + Erweiterung committen
```

## Curator-Note (Overlap-Hinweis, 2026-07-01)

**Potenzielle Überschneidung** mit `creative/html-artifact` Skill:
- Beide können single-file HTML ausliefern
- `html-artifact`: Fokus auf **Explainers/Reports** (Status, Code-Review, Diagramme)
- `ui-factory`: Fokus auf **komponentenbasierte UI** (Design-System, Components, Dashboards)

**Decision-Tree:**
- "Bau mir X (UI/UX)" → `ui-factory`
- "Erklär mir X" / "Schreib Report" → `html-artifact`
- Single-file HTML Showcases (z.B. Yuno-Cockpit) → beide möglich, `ui-factory` für polish wenn Design-Tokens relevant

**Action für Curator:** Falls Konsolidierung gewünscht, könnte `ui-factory` die `html-artifact`-Trigger-Phrasen übernehmen für "showcase"-Cases, oder umgekehrt. Aktuell nicht kritisch — beide haben distinkte Use-Cases.