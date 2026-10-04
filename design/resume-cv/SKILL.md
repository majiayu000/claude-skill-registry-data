---
name: resume-cv
description: Optimizes Resume/CV Experience and Skills sections for recruiter impact — action-oriented achievements, measurable results, tech highlights, modern chip layouts, and clean professional hierarchy. Use when improving professional experience, work history, Skills/Habilidades, CV layout, or making the profile competitive for Frontend Developer, React Developer, or Full Stack Developer roles.
---

# Resume / CV Optimization

Elevate the resume/CV for **recruiter scanning, credibility, and hiring impact** across **Experience** and **Skills** — not just shorter copy.

## User Brief (follow verbatim)

> Mejora la sección de experiencia profesional para que sea más atractiva visualmente y tenga mayor impacto para reclutadores. Actualmente aparece un indicador como **"+3 more"**, pero no aporta valor al CV; en su lugar, ocúltalo o reemplázalo por una presentación más elegante de la información.
>
> Optimiza cada experiencia laboral destacando logros, responsabilidades clave y tecnologías utilizadas, utilizando verbos de acción y resultados medibles cuando sea posible.
>
> También mejora la sección de **Skills**, organizándola por categorías (Frontend, Backend, Herramientas, Tecnologías, etc.) y presentándola de forma más moderna y fácil de escanear.
>
> Incrementa la credibilidad y el atractivo profesional del perfil, resaltando experiencia relevante, tecnologías actuales y fortalezas técnicas. El objetivo es que el CV se vea más sólido, moderno y competitivo para posiciones de **Frontend Developer, React Developer o Full Stack Developer**, manteniendo una apariencia limpia, profesional y orientada a la contratación.

## Hard Rules

1. **Never use `+N more` / `+N más` on a CV.** Show all relevant items as compact chips, a scannable grid, or curated content — never lazy overflow labels.
2. **Experience leads with impact.** Each role: action verbs, measurable outcomes, and visible tech stack.
3. **Skills use clear categories** — Frontend, Backend, CMS/Commerce, Tooling — with primary stack hero row above groups.
4. **Hierarchy over inventory.** Recruiter identifies core stack in < 3 seconds; experience differentiators in < 10 seconds.
5. **Curate copy, keep data.** Tighten bullets in JSON; do not delete project records without approval.
6. **Match project conventions:** Tailwind, atomic design, `en.json` / `es.json` i18n, `portfolio.json` + `portfolio-es.json`.

## Project Touchpoints

| Area           | Path                                                                 |
| -------------- | -------------------------------------------------------------------- |
| Resume layout  | `components/templates/ResumeTemplate/page.jsx`                       |
| Experience UI  | `components/molecules/ProjectResume/page.jsx`                        |
| Skills UI      | `components/molecules/SkillsSection/page.jsx`                        |
| Skill chips    | `components/atoms/SkillChip/page.jsx`                                |
| Skill grouping | `lib/utils/buildSkillsDisplay.js`                                    |
| Content (EN)   | `lib/utils/data/portfolio.json` — `resume.experiences`, skill arrays |
| Content (ES)   | `lib/utils/data/portfolio-es.json`                                   |
| Labels         | `components/lib/dictionaries/en.json`, `es.json`                     |

## Workflow

### Phase 1 — Audit (required)

```markdown
## CV audit

### Experience issues

- [flat bullet walls, missing tech visibility, weak verbs, no metrics]

### Skills issues

- [+N more labels, category sprawl, equal visual weight]

### Target roles

Frontend Developer · React Developer · Full Stack Developer
```

### Phase 2 — Experience content

Per role in `portfolio.json` / `portfolio-es.json`:

| Field              | Guidance                                                              |
| ------------------ | --------------------------------------------------------------------- |
| `summary`          | 1 line — scope + sector + stack                                       |
| `bullets`          | 4–5 max — verb-led, metrics where honest (%, count, Lighthouse score) |
| `technologies`     | 4–6 chips — role-level stack (array of strings)                       |
| `featuredProjects` | title + short description + `technologies` string or array            |

**Bullet formula:** `[Action verb] + [what] + [how/tech] + [result/metric]`

Examples:

- ✅ "Delivered **10+** client projects across real estate and e-commerce sectors."
- ✅ "Achieved **100% Lighthouse Performance** on a Next.js landing page."
- ❌ "Worked on various projects using different technologies."

### Phase 3 — Experience UI

Upgrade `ProjectResume` to:

1. **Timeline card** — left accent border, date column, role title prominent
2. **Role tech row** — chips from `experience.technologies`
3. **Achievement bullets** — compact list, improved spacing (`space-y-1.5`, no `py-2` bloat)
4. **Featured projects** — compact cards/grid with per-project tech chips (not plain `list-disc`)

### Phase 4 — Skills UI

Follow [resume-skills/SKILL.md](../resume-skills/SKILL.md) with these overrides:

- **Show all skills** in compact secondary chips — no truncation labels
- **Categories:** Core Stack (hero) → Frontend → Backend & Data → CMS & Commerce → Tooling
- **2-column grid** on desktop, single column mobile

### Phase 5 — Verification

- [ ] No `+N more` / `+N más` anywhere on resume page
- [ ] Each experience shows technologies visibly
- [ ] Bullets use action verbs; ≥ 1 metric per senior role where data exists
- [ ] Skills scannable in < 5 seconds
- [ ] EN + ES parity
- [ ] Build passes

## Anti-patterns

- `+N more`, `show more`, collapsed skill overflow without interaction
- Seven equal-weight bullet categories for skills
- Featured projects as undifferentiated bullet list without tech
- Passive voice ("Responsible for...", "Helped with...")
- Listing every project technology inline in bullets when chips exist

## Invocation variants

- `experience` — Phase 2–3 only
- `skills` — Phase 4 only (delegates to `resume-skills`)
- `full` (default) — all phases

## Related skills

- Skills detail: [resume-skills/SKILL.md](../resume-skills/SKILL.md)
- Checklist: [resume-skills/references/audit-checklist.md](../resume-skills/references/audit-checklist.md)
