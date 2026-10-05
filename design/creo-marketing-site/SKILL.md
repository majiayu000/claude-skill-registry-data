---
name: creo-marketing-site
description: >
  Seven-stage marketing site creation orchestration. Coordinates infrastructure setup,
  content generation, page components, SEO optimization, design review, localization,
  and final QA. Delegates to specialized agents for each stage. Trigger keywords:
  marketing site, marketing website, orchestrate, site creation, landing page site.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Marketing Site Orchestrator

Meta-agent responsible for coordinating the entire process of creating a professional marketing website. Manages the workflow, delegates tasks to specialized skills, and ensures quality at every stage.

## Commands

| Command | Description |
|---------|-------------|
| `/creo marketing-site full` | Execute all 7 stages in sequence |
| `/creo marketing-site content` | Generate content for all page types |
| `/creo marketing-site review` | Run design review and fix issues |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, `project_name`, `project_url`, `locales`
3. Load project extension if it exists at `.claude/skills/creo-marketing-site/creo-marketing-site-{project_id}.md`. This file contains project-specific site structure, page list, stage sequencing, and quality gates. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Role

This skill is NOT a content creator or developer. Its role is to:
1. **Plan** the work sequence
2. **Delegate** to specialized skills
3. **Track** progress across stages
4. **Verify** quality gates are passed
5. **Coordinate** handoffs between skills

### Available Skills for Delegation

| Skill | Capability |
|-------|------------|
| creo-content | Content creation, JTBD, pain points |
| creo-seo | SEO audits, structured data |
| creo-design-review | UI/UX review, accessibility |
| creo-design-implement | Design fixes |
| creo-ux-competitor | Competitor analysis |

### Stage 1: Infrastructure

**Goal:** Create project structure and base components

- Next.js project structure with TypeScript and Tailwind
- i18n infrastructure (langs config, request config, routing, language switcher)
- SEO infrastructure (robots.ts, sitemap.ts, manifest.ts)
- UI component library setup

**Quality Gate:** Build succeeds, no TypeScript errors, home page renders.

### Stage 2: Content Generation

**Goal:** Generate all JSON content files

- Directory structure: `messages/{locale}/core/` and `messages/{locale}/pages/`
- Core content: brand, navigation, common, footer, errors
- Page content: features, use-cases, pricing, resources
- Delegate to creo-content for JTBD-based copywriting

**Quality Gate:** All JSON files created, schema validation passes, no duplicate keys.

### Stage 3: Page Components

**Goal:** Create React components and pages

- Section components: Hero, PainPoints, Features, HowItWorks, Benefits, Comparison, FAQ, CTA
- Unified page component that assembles sections based on content
- Dynamic route pages for features, use-cases, sources, resources

**Quality Gate:** All section components render, dynamic routes work, i18n displays translations.

### Stage 4: SEO Optimization

**Goal:** Add SEO elements to all pages

- Structured data (JSON-LD) per page type
- Meta tags: unique titles (50-60 chars), descriptions (150-160 chars), canonicals
- Open Graph and Twitter Cards
- Sitemap and robots.txt
- AI bot configuration (GPTBot, PerplexityBot, Claude-Web)
- Delegate to creo-seo for audit

**Quality Gate:** All pages have unique titles/descriptions, JSON-LD validates, sitemap includes all pages.

### Stage 5: Design Review

**Goal:** Ensure design quality

- Responsive check at 375px, 768px, 1440px, 1920px
- Accessibility audit (WCAG 2.1 AA): contrast >= 4.5:1, touch targets >= 44px, focus states, alt text, keyboard nav
- Delegate to creo-design-review, then creo-design-implement for fixes

**Quality Gate:** No critical issues, WCAG 2.1 AA compliance, no horizontal scroll on mobile.

### Stage 6: Localization

**Goal:** Add additional languages

- Translate content via creo-content with locale parameter
- Verify key parity between locales
- Test UI fit (no overflow from longer translations)

**Quality Gate:** All JSON files in each locale, key parity verified, text fits UI.

### Stage 7: Final QA

**Goal:** Verify everything works

- Build verification (must pass with no errors)
- Link checking (all internal links work)
- Lighthouse audit (target >= 90 in all categories)
- Final SEO audit via creo-seo

**Quality Gate:** Build succeeds, no broken links, Lighthouse >= 90 all categories.

### Execution Protocol

1. Read project-specific config first
2. Read relevant stage documentation
3. Check prerequisites from previous stages
4. Execute tasks in order
5. Verify quality gates
6. Report status and any blockers

### Coordination Patterns

- **Sequential**: Stage 2 Content must complete before Stage 4 SEO
- **Parallel**: Multiple content types can be generated simultaneously
- **Review Loop**: Design Review -> Fix -> Re-review -> Pass
- **Localization Chain**: EN content first, then localize to other languages

### Error Handling

If a stage fails:
1. Document the error clearly
2. Identify the blocker
3. Propose a fix
4. Ask for user guidance if needed
5. Do NOT proceed to next stage

### Important Rules

1. Never skip stages -- each depends on previous ones
2. Always verify quality gates before proceeding
3. Track everything for visibility
4. Delegate to specialized skills, do not do their work
5. Report blockers immediately
6. Read project extension first for project-specific requirements

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/workflow-stages.md` | Detailed stage checklists |
| `references/agent-coordination.md` | How to call and coordinate skills |

## Quality Gates

- Each stage must pass its quality gate before the next begins
- Build must succeed at stages 1, 3, and 7
- All content must be valid JSON with i18n structure
- All pages must pass WCAG 2.1 AA accessibility
- Lighthouse scores must be >= 90 in all categories
- All locales must have key parity
