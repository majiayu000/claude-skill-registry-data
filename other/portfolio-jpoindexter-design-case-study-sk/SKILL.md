---
name: portfolio
description: "Plan, build, critique, update, or ship a professional design portfolio as one evidence-backed system. Use when the user invokes /portfolio; needs portfolio positioning, project inventory and selection, personal brand, case studies, homepage/about/contact copy, information architecture, visual direction, website implementation, accessibility, review, or publishing; or wants to turn scattered work into a coherent portfolio for a specific role, client, or audience."
---

# Portfolio Dispatcher

Build a portfolio around what the intended audience must understand and believe. Do not begin with a visual theme or force every project into the same story.

## Resolve the mode

Interpret the first argument as a mode when present:

| Call | Outcome |
|---|---|
| `/portfolio build` | Run the full workflow from evidence inventory to validated portfolio |
| `/portfolio position` | Define target audience, promise, differentiators, and proof requirements |
| `/portfolio inventory` | Find and classify usable projects, artifacts, metrics, and testimonials |
| `/portfolio select` | Score projects and choose the smallest credible set |
| `/portfolio architecture` | Create the sitemap, page hierarchy, labels, and content model |
| `/portfolio case-study` | Route one project through `/case-study` |
| `/portfolio write` | Draft or edit homepage, work-index, about, resume, and contact copy |
| `/portfolio design` | Define or implement the portfolio’s visual and interaction system |
| `/portfolio audit` | Test positioning, evidence, findability, writing, accessibility, and execution |
| `/portfolio ship` | Validate, commit, push, and deploy only with explicit publishing authority |
| `/portfolio update` | Re-run inventory and replace stale or weak evidence without rebuilding everything |

No mode means `build`. If a portfolio or project already exists, inspect it before asking for information that can be recovered from the files.

## Route the installed library

Load only the routes required for the active mode. If the `use` dispatcher is installed, run its inventory sweep against the active phase so new relevant skills can join later.

| Need | Route |
|---|---|
| Career/studio positioning, niche, expertise signals | `designbiz` |
| Personal brand, identity, positioning, touchpoints | `brand` |
| Product, system, or AI project story | `case-study` |
| Brand-identity project story or precedent | `brand-case-studies` with `case-study` |
| Sitemap, labels, project taxonomy, findability | `information-architecture-and-navigation` |
| Interface direction, design system, layout, polish | `design` |
| Section-level image direction or generated visuals | `imagegen-frontend-web` |
| Voice and removal of AI writing patterns | `humanizer`, after evidence and structure are stable |
| Accessibility and inclusive implementation | `accessibility-and-inclusive-design` |
| GitHub publication | `github:yeet`, only after an explicit ship request |

Treat these as delegated capabilities, not separate reports. The portfolio owns the audience, project set, cross-page hierarchy, and proof system; companion skills own their specialized decisions.

## Mode plans

Use these sequences as required routes, not suggestions:

| Mode | Ordered plan |
|---|---|
| `build` | `position` → `inventory` → `select` → `architecture` → `case-study` for each selected project → `write` → `design` → `audit` → local handoff |
| `position` | `designbiz` for audience/expertise strategy → `brand` for personal-brand expression → proof requirements |
| `inventory` | Inspect authorized files and sources → evidence/permission ledger → gap list |
| `select` | Permission gate → PROOF scoring → coverage/redundancy/depth check |
| `architecture` | `information-architecture-and-navigation` → content model → sitemap → page briefs |
| `case-study` | `case-study`; add `brand-case-studies` for identity work |
| `write` | Portfolio page copy → evidence check → `humanizer` voice pass |
| `design` | `design`; add `imagegen-frontend-web` only when meaningful new imagery is needed |
| `audit` | Positioning/evidence gate → rendered findability test → `accessibility-and-inclusive-design` → execution checks |
| `ship` | `audit` must pass → `github:yeet` → configured deployment path |
| `update` | Inventory delta → replace or repair weak proof → rerun affected case-study/page/audit stages |

Do not append `ship` to `build`. Run `ship` only when the user explicitly requests publishing.

## Full workflow

1. **Target and position** — name the role, client, or audience; their decision; desired next action; constraints; and proof requirements.
2. **Inventory** — inspect projects, artifacts, metrics, research, screenshots, source files, testimonials, and permissions.
3. **Select** — apply `references/project-selection.md`; choose the smallest set that proves the positioning without repetition.
4. **Architect** — apply `references/page-system.md`; design the content model and sitemap before visual styling.
5. **Build stories** — route each selected project through `case-study`; do not duplicate its internal framework here.
6. **Write connective copy** — draft the homepage, work index, about page, project cards, resume bridge, and contact path.
7. **Design and implement** — route the interface through `design`; generate new imagery only when it carries meaning.
8. **Validate** — apply `references/portfolio-quality-gate.md` against the actual rendered portfolio.
9. **Hand off** — leave a verified local artifact and one re-entry step.
10. **Ship only on request** — publish only when the user explicitly invokes or requests the ship phase.

Use `assets/portfolio-workbook.md` when the user needs a persistent artifact across sessions.

## Evidence contract

For every project and portfolio-level claim:

- name the user, organization, or system affected;
- state the designer’s actual ownership and collaborators;
- connect artifacts to decisions, not decoration;
- distinguish shipped outcomes from observations, reports, and proposals;
- mark confidential, redacted, reconstructed, or unavailable evidence;
- never invent research, metrics, testimonials, awards, employers, responsibilities, or impact.

Use `[evidence needed: …]` for material gaps. A visually strong page does not compensate for unsupported claims.

## Output by default

Return or create:

1. target-audience and positioning statement;
2. evidence inventory;
3. scored project shortlist;
4. portfolio sitemap and page briefs;
5. case-study production queue;
6. portfolio-level copy;
7. design/build direction;
8. validation results and unresolved gaps;
9. one next action when work remains.

## Example

```text
/portfolio build Inspect my project folders and build a portfolio for senior
AI product design roles. Prioritize systems thinking, agent control, and shipped work.
```

Expected outcome: the skill inventories evidence, selects non-redundant projects, defines positioning and sitemap, routes each selected project through `/case-study`, builds or directs the site through `/design`, and reports the executed validation path before calling it ready.

## Done

The portfolio is ready only when the actual rendered artifact lets the target audience answer:

- Who is this person, what kind of work do they do, and for whom?
- Which projects best prove that claim?
- What did they own, decide, and change?
- What evidence supports the result?
- Can I find the right depth quickly on desktop, mobile, keyboard, and assistive technology?
- What should I do next, and does that action work?
