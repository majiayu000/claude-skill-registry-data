---
name: creo
description: >
  Comprehensive design, UX, content, DevOps, and testing toolkit for web applications.
  Design reviews, UX flow analysis, marketing content, SEO auditing, CI/CD pipelines,
  test orchestration, performance optimization, and marketing site creation.
  Triggers on: /creo, design review, UX analysis, marketing content, SEO, DevOps,
  pipeline, test, performance, benchmark, marketing site.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Creo -- Design & Development Toolkit

Creo is a comprehensive design, UX, content, DevOps, and testing toolkit for web applications. It provides a unified interface for design reviews, UX flow analysis, marketing content generation, SEO auditing, CI/CD pipeline management, test orchestration, and full marketing site creation. Each command routes to a specialized sub-skill or subagent optimized for its domain.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `/creo design-review <url>` | UI/UX review (responsive, WCAG AA, Nielsen's heuristics) |
| `/creo design-implement <report>` | Execute design fixes from review reports |
| `/creo ux-internal <flow>` | Analyze your own app's UX flows |
| `/creo ux-competitor <url>` | Analyze competitor websites |
| `/creo content <page-type>` | Generate marketing copy (JTBD, pain points) |
| `/creo image-prompt <context>` | Generate image prompts for DALL-E/Midjourney/SDXL |
| `/creo seo <url>` | Next.js SEO + GEO audit (7-phase, technical + schema + GEO) |
| `/creo seo onboard <url>` | Full SEO lifecycle: audit, plan, guided GSC setup, monitoring cadence |
| `/creo seo init` | Scan codebase and cache project profile for faster audits |
| `/creo seo autofix` | Closed-loop GSC remediation (allowlisted fixes, ledger, live verification) |
| `/creo seo semantic-core` | Focused query core with noise filtering and P0-P3 priorities |
| `/creo seo weekly` | Weekly rank history + LLM-citability monitoring |
| `/creo seo-content <url>` | Deep content audit (E-E-A-T, AI-pattern detection, citability) |
| `/creo devops <command>` | Infrastructure management (GitHub/Cloudflare/Railway/Stripe) |
| `/creo pipeline <command>` | CI/CD pipeline specialist (GitHub Actions) |
| `/creo test <command>` | Test orchestration (unit + E2E) |
| `/creo marketing-site <command>` | Full marketing site creation (7-stage) |
| `/creo ai-generation <command>` | AI generation pipeline expertise |
| `/creo perf <command>` | Performance optimization: init, baseline, audit, optimize, report (six-layer, measured) |

---

## Orchestration Logic

### Individual Commands

For any single command (e.g., `/creo design-review`, `/creo seo`), the orchestrator loads the relevant sub-skill directly. The sub-skill file contains the full instructions and references needed for that domain.

### Marketing Site Full Build (`/creo marketing-site full`)

This is a multi-stage orchestration that delegates to parallel subagents:

1. **Stage 1-2**: Infrastructure setup and content generation run sequentially.
2. **Stage 3**: Page component assembly.
3. **Stage 4-5**: Parallel delegation to:
   - `creo-content-strategist` -- generates marketing copy for all pages
   - `creo-seo` -- runs codebase audit and optimizes metadata/structured data
   - `creo-design-review` -- validates responsive design and accessibility
   - `creo-ux-competitor` -- analyzes competitor sites for differentiation
4. **Stage 6**: Localization via `creo-i18n-translator`.
5. **Stage 7**: Final QA combining all subagent reports.

### DevOps Routing (`/creo devops`)

Routes to specialized CLI subagents based on the target platform:

| Subcommand | Subagent |
|------------|----------|
| `devops github` | `creo-github-cli` |
| `devops cloudflare` | `creo-cloudflare-cli` |
| `devops railway` | `creo-railway-cli` |
| `devops stripe` | `creo-stripe-cli` |

### Performance Routing (`/creo perf`)

Loads the `creo-perf` sub-skill. `perf audit` spawns the measure-only `creo-perf-audit` subagent; `perf init` scaffolds the project's `.claude/skills/creo-perf/` via the perf-harness extension; `perf optimize` runs the fix loop in the main context (baseline, one concern, re-measure, verify, commit).

### Test Routing (`/creo test`)

Routes to the appropriate testing subagent:

| Subcommand | Subagent |
|------------|----------|
| `test unit` | `creo-unit-test` |
| `test e2e` | `creo-e2e-test` |
| `test all` | Both subagents run in parallel |

---

## Domains

| Domain | Sub-Skills | Primary Focus |
|--------|-----------|---------------|
| **Design & UX** | design-review, design-implement, ux-internal, ux-competitor | Visual quality, accessibility, usability |
| **Content & Marketing** | content, image-prompt | Copy generation, JTBD frameworks, image prompts |
| **SEO** | seo | Technical SEO, structured data, Core Web Vitals |
| **DevOps** | devops (github, cloudflare, railway, stripe) | Infrastructure, deployment, services |
| **Testing** | test (unit, e2e) | Code quality, test coverage, E2E validation |
| **Performance** | perf | Six-layer audit, immutable baselines, before/after proof, fix loop |
| **Orchestration** | marketing-site, ai-generation | Multi-stage workflows, parallel delegation |

---

## Reference Files

On-demand reference files loaded by sub-skills as needed. Located in `creo/references/`:

| File | Used By | Content |
|------|---------|---------|
| `design-principles.md` | design-review, design-implement | S-tier SaaS design checklist |
| `design-style-guide.md` | design-review, design-implement | Viewports, spacing, typography, accessibility |
| `visual-dev-snippets.md` | design-review, design-implement | Quick visual verification workflow |
| `ux-methodologies.md` | ux-internal, ux-competitor | Nielsen's heuristics, JTBD, journey mapping |
| `ux-report-template.md` | ux-internal, ux-competitor | Structured UX analysis report format |
| `pain-points-framework.md` | content, marketing-site | Customer pain analysis by segment |
| `voice-and-tone.md` | content, marketing-site | Brand voice pillars, writing principles |
| `image-style-reference.md` | image-prompt | Prompt patterns, style modifiers, categories |
| `seo-checklist.md` | seo, marketing-site | SEO and i18n implementation checklist |
| `seo-audit-checklists.md` | seo | Phase-based SEO audit (5 phases) |
| `i18n-translation-guide.md` | marketing-site, content | Localization best practices, language list |
| `workflow-stages.md` | marketing-site | 7-stage marketing site creation workflow |

---

## Sub-Skills

Each sub-skill is a standalone SKILL.md that can be invoked directly or through the orchestrator.

| # | Sub-Skill | Path | Trigger |
|---|-----------|------|---------|
| 1 | Design Review | `creo/skills/design-review/SKILL.md` | `/creo design-review` |
| 2 | Design Implementation | `creo/skills/design-implement/SKILL.md` | `/creo design-implement` |
| 3 | UX Internal Analysis | `creo/skills/ux-internal/SKILL.md` | `/creo ux-internal` |
| 4 | UX Competitor Analysis | `creo/skills/ux-competitor/SKILL.md` | `/creo ux-competitor` |
| 5 | Content Strategy | `creo/skills/content/SKILL.md` | `/creo content` |
| 6 | Image Prompt Generation | `creo/skills/image-prompt/SKILL.md` | `/creo image-prompt` |
| 7 | SEO Audit | `creo/skills/seo/SKILL.md` | `/creo seo` |
| 8 | DevOps Management | `creo/skills/devops/SKILL.md` | `/creo devops` |
| 9 | CI/CD Pipeline | `creo/skills/pipeline/SKILL.md` | `/creo pipeline` |
| 10 | Test Orchestration | `creo/skills/test/SKILL.md` | `/creo test` |
| 11 | Marketing Site | `creo/skills/marketing-site/SKILL.md` | `/creo marketing-site` |
| 12 | AI Generation | `creo/skills/ai-generation/SKILL.md` | `/creo ai-generation` |
| 13 | Performance | `skills/creo-perf/SKILL.md` | `/creo perf` |

---

## Subagents

Each subagent is a focused agent definition for parallel delegation.

| # | Subagent | Path | Role |
|---|----------|------|------|
| 1 | creo-design-review | `creo/agents/design-review.md` | Visual review and accessibility |
| 2 | creo-design-implement | `creo/agents/design-implement.md` | Execute design fixes |
| 3 | creo-ux-internal | `creo/agents/ux-internal.md` | Internal UX flow analysis |
| 4 | creo-ux-competitor | `creo/agents/ux-competitor.md` | Competitor UX analysis |
| 5 | creo-content-strategist | `creo/agents/content-strategist.md` | Marketing copy generation |
| 6 | creo-image-prompt | `creo/agents/image-prompt.md` | Image prompt generation |
| 7 | creo-seo | `agents/creo-seo.md` | Next.js SEO + GEO audit (7-phase) |
| 7b | creo-seo-content | `agents/creo-seo-content.md` | Deep content-quality audit (delegate or standalone) |
| 8 | creo-github-cli | `creo/agents/github-cli.md` | GitHub API operations |
| 9 | creo-cloudflare-cli | `creo/agents/cloudflare-cli.md` | Cloudflare management |
| 10 | creo-railway-cli | `creo/agents/railway-cli.md` | Railway deployment |
| 11 | creo-stripe-cli | `creo/agents/stripe-cli.md` | Stripe integration |
| 12 | creo-e2e-test | `creo/agents/e2e-test.md` | End-to-end testing |
| 13 | creo-perf-audit | `agents/creo-perf-audit.md` | Six-layer performance audit (measure-only) |

---

## Optional Extensions

These extensions can be added to the toolkit as needed:

- **image-generation** -- Integration with DALL-E, Midjourney, or SDXL APIs for automated image creation from prompts generated by the image-prompt sub-skill.
- **i18n-translator** -- Automated translation pipeline for marketing site localization across 39+ languages with quality validation.
- **gsc-analyzer** -- Google Search Console analysis, SEO auditing, and operations automation: 17 analyzers, GSC API + Indexing API clients, UI-only surface automation (drilldown exports, Validate Fix), the closed-loop autofix scripts, weekly rank/LLM-citability monitoring, and a full GSC API reference.
- **perf-harness** -- Deterministic benchmark scripts behind `/creo perf`: scenario captures (EXPLAIN medians, p50/p95 loops, wire bytes, ETag replay, Playwright interaction probes), Lighthouse initial-load audit, platform/schema audits, pg_stat_statements workload discovery, auto-built before/after dashboard, and the `/creo perf init` project scaffolder.

---

## Project Configuration

All skills check `.claude/project-config.md` at runtime for project-specific settings. This file should contain:

- **Dev server URL** -- The local development server address (default: `http://localhost:3000`).
- **Framework** -- The frontend framework in use (Next.js, Vite, etc.).
- **CSS framework** -- Tailwind CSS, MUI, shadcn/ui, or custom.
- **Supported locales** -- List of language codes for i18n.
- **Brand guidelines** -- Brand name, colors, fonts, voice attributes.
- **Deployment targets** -- Hosting platform and CI/CD configuration.
- **Test framework** -- Vitest, Jest, Playwright, Cypress, etc.

If `.claude/project-config.md` does not exist, skills use sensible defaults and prompt the user for required configuration.
