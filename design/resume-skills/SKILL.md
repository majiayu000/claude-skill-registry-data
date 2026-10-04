---
name: resume-skills
description: Optimizes the Resume/CV Skills section for recruiter scanning — categorized chips (Frontend, Backend, Tooling), primary stack hero row, no +N more labels, and mobile-friendly spacing. Use for Skills/Habilidades layout only; for full CV (Experience + Skills) use resume-cv. Triggers on skills redesign, category grouping, or decluttering the resume skills section.
---

# Resume Skills Section Optimization

Optimize the **Skills** section of the resume/CV for **scannability, visual hierarchy, and recruiter impact** — not just shorter text.

## User Brief (follow verbatim)

> Revisa la sección **Skills** del resumen/CV. Actualmente se siente demasiado extensa, visualmente cargada y abrumadora para el lector. Quiero que optimices tanto el contenido como el diseño.
>
> Objetivos:
>
> - Reducir la cantidad de texto visible sin perder información importante.
> - Agrupar habilidades relacionadas en categorías claras y fáciles de escanear.
> - Mejorar la jerarquía visual para que los reclutadores identifiquen rápidamente las tecnologías principales.
> - Evitar bloques de texto largos o listas excesivamente extensas.
> - Priorizar la legibilidad y el diseño limpio sobre mostrar absolutamente todas las tecnologías.
> - Destacar las habilidades más relevantes y actuales.
> - Utilizar una distribución visual más equilibrada (grid, columnas, badges o chips, según corresponda).
> - Mantener una apariencia moderna, profesional y orientada a perfiles de desarrollo Frontend/Full Stack.
> - Asegurar que la sección se vea bien tanto en desktop como en dispositivos móviles.
> - Mejorar espaciados, alineación, tamaños de fuente y densidad visual para que la sección respire mejor.
>
> Antes de implementar cambios, analiza qué elementos generan saturación visual y propone una estructura más clara y profesional. El resultado final debe sentirse más limpio, escaneable y atractivo para reclutadores y clientes.

## Hard Rules

1. **Analyze and propose before coding.** Deliver a short audit + proposed structure; wait for confirmation only if the user explicitly asked for a plan-only pass. Otherwise, include the audit inline and implement in the same turn.
2. **Hierarchy over inventory.** Lead with 4–6 primary technologies; secondary skills support, not compete.
3. **No bullet-list walls.** Replace `list-disc` stacks with chips, compact grids, or tiered groups when item count exceeds ~5 per category.
4. **Curate, don't dump.** Merge synonyms and dedupe in display logic; show all curated skills as compact chips — **never use `+N more` / `+N más`** (see `resume-cv` skill). Do not delete data from JSON without user approval.
5. **Match project conventions:** design tokens (`styles/tokens.css`, `styles/globals.css`), Tailwind utilities, atomic design (`components/atoms`, `molecules`), accessibility (labels, contrast, keyboard focus on interactive chips).
6. **Keep i18n in sync:** update `components/lib/dictionaries/en.json` and `es.json` when category labels change.

## Project Touchpoints

| Area           | Path                                                                                                                                   |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Skills UI      | `components/templates/ResumeTemplate/page.jsx` — `SkillCategory`, skills grid                                                          |
| Skill data     | `lib/utils/data/portfolio.json` — `resume.languages`, `frameworks`, `cmsEcommerce`, `databases`, `toolsPlatforms`, `aiTools`, `others` |
| Labels (EN/ES) | `components/lib/dictionaries/en.json`, `es.json` — `resume.*` keys                                                                     |
| Design tokens  | `styles/tokens.css`, `styles/globals.css`                                                                                              |

## Workflow

### Phase 1 — Visual saturation audit (required)

Inspect the live structure and score each issue. Report in this format:

```markdown
## Skills audit

### Saturation sources

- [e.g. 7 categories × bullet lists = high vertical scroll]
- [e.g. equal visual weight for core stack vs niche tools]
- [e.g. py-2 per list item inflates density]

### Recruiter scan path (current vs target)

- Current: ...
- Target: Primary stack → specialty areas → supporting tools (≤10s scan)

### Proposed structure

1. **Primary stack** (hero chips, largest)
2. **Specializations** (2–4 grouped columns/cards)
3. **Supporting** (smaller chips or collapsed)
```

Use the checklist in [references/audit-checklist.md](references/audit-checklist.md).

### Phase 2 — Content curation

Apply these rules to `portfolio.json` arrays:

| Priority        | Keep / promote                                    | Demote / merge / hide                                    |
| --------------- | ------------------------------------------------- | -------------------------------------------------------- |
| P0 — Hero       | React, Next.js, TypeScript, Tailwind CSS, Node.js | —                                                        |
| P1 — Strong     | GraphQL, Shopify, Strapi, MongoDB, Git, Vercel    | Duplicate CSS entries (Sass if Tailwind leads)           |
| P2 — Contextual | GSAP, WordPress, Figma, AI/MCP tools              | Niche animation libs unless role-specific                |
| P3 — Collapse   | —                                                 | Certifications overlap, legacy CMS, redundant SQL labels |

**Grouping target (max 4–5 visible categories):**

1. **Core Frontend** — React, Next.js, TypeScript, Tailwind, HTML/CSS
2. **Backend & Data** — Node.js, REST/GraphQL, MongoDB, MySQL
3. **CMS & Commerce** — Shopify, Strapi, WordPress (merge Liquid into Shopify)
4. **Tooling & Workflow** — Git, Vercel, Figma, Lighthouse, AI dev tools

Fold `databases` into Backend, `aiTools` into Tooling unless the role is AI-forward.

### Phase 3 — Visual hierarchy (implementation)

Replace flat bullet lists with a **tiered layout**:

```
┌─ Skills ─────────────────────────────────────┐
│  [React] [Next.js] [TypeScript] [Tailwind]   │  ← Primary: larger chips, accent border
│                                              │
│  Core Frontend    Backend & Data             │  ← 2-col grid desktop, 1-col mobile
│  [chip][chip]…    [chip][chip]…              │
│                                              │
│  CMS & Commerce   Tooling                    │
│  [chip][chip]…    [chip][chip]…              │
└──────────────────────────────────────────────┘
```

**Typography scale (relative to section `h1` = `text-2xl`):**

| Element         | Classes (starting point)                                   |
| --------------- | ---------------------------------------------------------- |
| Section title   | `text-2xl font-bold` (unchanged)                           |
| Category label  | `text-sm font-semibold uppercase tracking-wide opacity-80` |
| Primary chips   | `text-sm font-medium px-3 py-1.5`                          |
| Secondary chips | `text-xs px-2.5 py-1 opacity-90`                           |

**Spacing:** increase category gap (`gap-y-6` / `gap-y-8`), reduce per-chip padding vs current `py-2` list items, use `gap-2` flex-wrap inside groups.

**Components:** prefer a reusable `SkillChip` atom and `SkillCategoryGroup` molecule; use shadcn `Badge` from `components/ui` if present, else token-based Tailwind chips.

### Phase 4 — Responsive & a11y

- Mobile: single column, primary stack full-width wrap, no horizontal overflow
- Desktop: 2-column category grid (`desktop:grid-cols-2`), primary stack spans full width above
- Chips: `aria-label` on groups (`role="list"`, items `role="listitem"`), sufficient contrast on `bg-slate-800` resume card
- Touch targets ≥ 44px only if chips are interactive; static chips need not be buttons

### Phase 5 — Verification

Before finishing:

- [ ] Primary technologies identifiable in **< 3 seconds**
- [ ] No category exceeds 8 visible items without collapse
- [ ] Section height reduced vs previous bullet layout (estimate or screenshot)
- [ ] EN + ES dictionary keys still resolve
- [ ] No hardcoded hex/px where tokens exist
- [ ] `ReadLints` clean on edited files

## Anti-patterns (reject these)

- Long `list-disc` columns (current `SkillCategory` pattern) for 5+ items
- Same font size/weight for hero stack and minor tools
- Seven same-weight categories in a 2-column grid
- Adding every certification technology into Skills (keep Certifications section separate)
- Removing skills from JSON silently — demote visually, keep data

## Invocation variants

- `audit` — Phase 1 only; no code changes
- `content` — Phase 2 only; JSON curation proposal
- `design` — Phase 3–4; UI refactor with minimal data changes
- `full` (default) — all phases

## Additional resources

- Saturation checklist and chip patterns: [references/audit-checklist.md](references/audit-checklist.md)
