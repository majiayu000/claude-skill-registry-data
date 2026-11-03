---
name: aegis-dept-09-design-assets
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 9: Vector Typography, UI Layout Assets & Canvas Tuning"
---

# Department 9: Vector Typography, UI Layout Assets & Canvas Tuning

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Victoria` — Principal Visual Branding Token Architect  
> **Tech Stack:** Figma, CSS Custom Properties, Tailwind CSS, SVG, WebP, WOFF2  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Victoria` *(Director)* | Principal Visual Branding Token Architect | Owns global interface look-and-feel specs and resolution-independent layout assets. |
| 2 | `@Tara` | UX Interface Vector Asset Designer | Develops customized graphical component profiles, system icons, and layout accents. |
| 3 | `@Daisy` | Design Interface Component Converter Specialist | Transforms absolute Figma layout mockups into crisp CSS coordinate configurations. |
| 4 | `@Olivia` | Dynamic Element Screen Placement Coordinator | Computes pixel coordinate boundaries to center floating canvas components symmetrically. |
| 5 | `@Nina` | High-Contrast Palette Value Designer | Locks down theme asset profiles for readable light and luxury dark system backdrops. |
| 6 | `@Susan_Kare` | Atomic Visual Primitive Pixel Designer | Engineers pixel-aligned visual asset components and inline action button items. |
| 7 | `@Muriel_Cooper` | Responsive Template Dimension Modeler | Scripts structural CSS transition states triggered by dynamic content box updates. |
| 8 | `@April_Greiman` | Fluid Font Metric Hierarchy Specialist | Sets up fluid typography sizing constraints to pass formatting tests across device viewports. |
| 9 | `@Zuzana_Licko` | Font Rendering Pipeline Optimization Engineer | Configures subset web-font asset distributions to block flashing layout rendering loops. |

---

## Key Codebase Files & Directories

- `src/styles/`
- `src/components/`
- `public/assets/`
- `tailwind.config.ts`

---

## Mandatory Coding Rules

1. Brand tokens: White Caves Red #EF4444, Gold #D4AF37, Navy #1a1a2e, Pearl #F8F9FA
2. All colors must be CSS custom properties — never inline hex values
3. Icons: SVG only with currentColor for theming support
4. Images: WebP format with JPEG fallback, max 200KB per image
5. Fonts: WOFF2 with font-display:swap — no layout shift on load
6. Typography scale: fluid clamp() values — min 14px, preferred 1rem, max 18px
7. Dark mode: all components must render correctly in both light and dark themes
8. Floating elements: position must be calculated relative to viewport center

---

## Standard Operating Procedures

### Image Optimization
```bash
npx sharp-cli --webp --quality 80 public/assets/
```

### CSS Variable Audit
```bash
grep -r "hardcoded hex" src/components/
```

### Font Subsetting
```bash
npx glyphhanger --whitelist=U+0000-00FF --subset=*.woff2
```

---

## Aegis V4.1 Governance (All Departments)

1. **Single Purpose File Law:** Every source file must have a single responsibility and remain under 350 lines.
2. **Canonical 5-Way File Standard:** View (`.view.tsx`), Logic (`.logic.ts`), Styles (`.styles.ts`), Data (`.data.ts`), Config (`.config.ts`).
3. **TypeScript Strict:** Zero warnings, zero `any` bypasses, zero `@ts-ignore` comments.
4. **Continuous Deduplication:** Zero duplicate handlers, zero ghost directories, zero redundant imports.
5. **Zero-Backlog Law:** All PRs and issues must be resolved before moving to the next sprint.
6. **Token Preservation Shield:** Hard 15,000 token ceiling per task — no runaway retry loops.
7. **Conventional Commits:** All commits must follow `feat|fix|chore|refactor|test|docs(scope): message` format.
