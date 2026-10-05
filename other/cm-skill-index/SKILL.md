---
name: cm-skill-index
description: "Progressive Disclosure skill index — efficient skill loading in 3 layers. Layer 1 (index, ~100 tokens) always loaded. Layer 2 (summary, ~300 tokens) loaded on context need. Layer 3 (full SKILL.md) loaded on execution only."
token_budget: 800
compressed: true
deprecated: false
---

# Skill Index — Progressive Disclosure Engine

## TL;DR
- **Use when** searching for a CodyMaster or community skill
- **Layered**: L1 index (always loaded) → L2 summary → L3 full
- **Includes**: discovery, search, mastery (consolidated in v6)

> **Save 90%+ tokens.** Agents scan the index first, load full skills only when executing.
> Inspired by Loki Mode's 3-Layer Progressive Disclosure memory architecture.

## The Problem

Traditional approach: Load every SKILL.md to decide which skill to use.
- 30+ skills × ~3000 tokens each = **90,000+ tokens just for discovery**
- Agent only needs ~500 tokens to make the choice
- **89,500 tokens wasted on reading full skills**

## The Solution: 3-Layer Loading

```
┌────────────────────────────────────────────────┐
│ LAYER 1: INDEX (~100 tokens per skill)          │
│ Always loaded. Quick scan. "What exists?"        │
│ Name + Domain + Triggers + 1-line summary       │
└─────────────────────┬──────────────────────────┘
                      │ (match found?)
                      v
┌────────────────────────────────────────────────┐
│ LAYER 2: SUMMARY (~300 tokens per skill)        │
│ Load when choosing. "Is this the right one?"     │
│ Description + When to use + Integration table   │
└─────────────────────┬──────────────────────────┘
                      │ (confirmed?)
                      v
┌────────────────────────────────────────────────┐
│ LAYER 3: FULL SKILL.md (1500-5000 tokens)       │
│ Load ONLY during execution. "How to use it."     │
│ Complete instructions, examples, red flags       │
└────────────────────────────────────────────────┘
```

## Layer 1: Skill Index

**Always loaded by agents at session start.** Maximum 100 tokens per skill.

### Engineering Swarm 🔧

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-tdd` | test, TDD, red-green-refactor | Red-Green-Refactor cycle before any implementation |
| `cm-debugging` | bug, error, fix, debug, broken | Root cause analysis before fixing. 5-phase investigation |
| `cm-quality-gate` | deploy, ship, verify, quality, gate | 6-gate verification: static analysis → blind review → ship |
| `cm-quality-gate` | test setup, CI, verification | Test + verification gate before claiming completion |
| `cm-code-review` | review, PR, feedback, branch | Request reviews, handle feedback, complete branches |
| `cm-codeintell` | understand codebase, call graph, impact, architecture, what calls X, what breaks | AST knowledge graph + architecture diagrams + smart context (30% fewer tokens) |
| `cm-reactor` | rewrite, pivot, migrate, direction change, architecture wrong, restructure | TRIZ-powered strategic codebase re-direction — 5-phase incremental migration |
| `cm-clean-code` | clean, dead code, refactor, code smell, DRY, SOLID, naming, messy | 7-point hygiene gate: dead code, imports, naming, SRP, DRY, nesting |

### Operations Swarm ⚙️

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-safe-deploy` | deploy, staging, production, release | Multi-gate deploy pipeline with rollback strategy |
| `cm-identity-guard` | git push, deploy, Cloudflare, Supabase, account | Verify identity before any push/deploy to prevent wrong-account |
| `cm-execution` | branch, isolate, worktree, parallel | Execution modes including isolated workspaces and parallel batches |
| `cm-terminal` | command, terminal, run, execute | Safe terminal execution with progress logging |

### Security Swarm 🔒

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-safe-deploy` | secret, token, leak, security, scan, pre-commit, gitleaks, rotate | Defense-in-depth: repo scanning, token lifecycle, and release safety |

### Product Swarm 🎨

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-brainstorm-idea` | analyze, enhance, improve, initiative, evaluate, review product | Strategic analysis gate: 9 Windows + Double Diamond → 2-3 qualified options |
| `cm-planning` | plan, design, brainstorm, feature | Brainstorm intent → write implementation plan → then code |
| `cm-ux-master` | UI, UX, design, interface, usability | 48 UX Laws + 37 Design Tests + Figma/Stitch integration |
| `cm-design-system` | preview, visual, mockup, render UI, wireframe | Live UI concept generation via design-token and Stitch/Open Design workflows |
| `cm-dockit` | docs, documentation, knowledge base, SOP | Generate complete knowledge base from codebase |
| `cm-project-bootstrap` | new project, init, bootstrap, setup | Full project setup: design system → staging → CI → deploy |
| `cm-jtbd` | customer discovery, JTBD, jobs to be done, product-market fit, why users churn | JTBD canvas: Switch Interview → Outcome Metrics → Opportunity Scoring |

### Growth Swarm 📈

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-content-factory` | content, blog, article, marketing | AI content engine: research → generate → audit → deploy |
| `cm-ads-tracker` | pixel, tracking, GTM, Meta, TikTok, Google Ads | Complete conversion tracking setup across platforms |
| `cm-cro-methodology` | conversion, A/B test, landing page, funnel | CRO audit: funnel mapping → persuasion → objection handling |

### Orchestration Swarm 🎯

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-execution` | execute, implement, plan, RARV, batch | Execute plans: batch mode, subagent-driven, parallel, or RARV |
| `cm-continuity` | memory, context, CONTINUITY, learnings | Working memory protocol: read at start, update at end |
| `cm-skill-index` | which skill, skill list, discover, help | Meta-skill: when to invoke skills and how to discover the right one |
| `cm-skill-health` | skill broken, skill drift, missing skill, stale skill, health | Audit a skill using docs drift, retro notes, validation, and gates |
| `cm-skill-evolution` | repair skill, evolve skill, fix skill, derive skill | Recover a degraded skill with FIX, DERIVED, or CAPTURED mode |
| `cm-skill-evolution` | repair skill, evolve skill, capture skill | Repair, derive, or capture skills from execution feedback |
| `cm-safe-i18n` | translate, i18n, language, localize | Safe translation with multi-pass batching and audit gates |
| `cm-skill-chain` | chain, pipeline, workflow, multi-step, full process | Compose skills into automated multi-step pipelines |
| `cm-deep-search` | semantic search, find docs, large codebase, qmd | Optional power-up for semantic search across large projects |
| `cm-readit` | audio, TTS, read aloud, voice, speech, SpeechSynthesis, MP3 player | Web audio engine — TTS reader, pre-recorded MP3 player, Voice CRO triggers |
| `cm-how-it-work` | how does X work, explain, architecture overview | Explain how a system, feature, or codebase works |

### Workflow Commands 🖥️

| Skill | Triggers | Summary |
|-------|----------|---------|
| `cm-start` | /cm-start, start workflow, begin objective, new task | Orchestrate full cm-* workflow from objective to production code |
| `cm-status` | /cm-status, quick status, progress, what's next, blocked | Ultra-concise progress summary: done / next / blocked |
| `cm-status` | /cm-status, quick status, progress, what's next, blocked | Ultra-concise progress summary: done / next / blocked |


### Planned (not yet implemented) 🧪

> Skills below do not have SKILL.md files yet.

| Skill | Triggers | Summary |
|-------|----------|---------|
| `mom-test` *(planned)* | customer interview, validate idea, leading questions | Customer interviews without leading questions |
| `release-it` *(planned)* | production, circuit breaker, timeout, chaos | Build production-ready systems with stability patterns |
| `medical-research` *(planned)* | medical, OB/GYN, clinical, evidence-based | Evidence-based medical writing with citation standards |
| `tailwind-mastery` *(planned)* | Tailwind, utility-first, responsive, v4 | Tailwind CSS utilities, responsive, accessibility |
| `pandasai-analytics` *(planned)* | DataFrame, analytics, forecast, time-series | Natural language DataFrame analysis and visual reports |
| `cm-google-form` *(planned)* | Google Form, sheet, App Script | Form-to-sheet integration with auto-retry |

### Community Skills Registry 🌐

> **STOP! Zero-Token Discovery Priority:**
> BEFORE using this registry, check if `.cm/project-skills.md` exists in the local project.
> It contains the pre-compiled, exact community skills needed for the project's tech stack.
> If it doesn't exist, run `npx cm index skills` first to build it.
> 
> **Only use the registry below if tech is not listed** or if you need to search manually: `npx skills find "{keyword}"`

#### 🖥️ Frontend Frameworks (10)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `react-best-practices` | vercel-labs/agent-skills | react, react performance, RSC |
| `composition-patterns` | vercel-labs/agent-skills | react composition, compound components |
| `react-native-guidelines` | vercel-labs/agent-skills | react native, expo, mobile app |
| `react-native-best-practices` | callstackincubator/agent-skills | react native, expo, mobile |
| `nextjs-app-router-patterns` | wshobson/agents | next.js, app router, RSC |
| `react:components` | google-labs-code/stitch-skills | react components, stitch |
| `cm-ux-master` | UI/UX, design system, frontend | UI/UX design intelligence + Harvester v4 |
| `angular-directives` | analogjs/angular-skills | angular, directives, components |
| `svelte-best-practices` | community | svelte, sveltekit |
| `astro-best-practices` | community | astro, static site, islands |

#### 🎨 CSS & UI Design (8)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `web-design-guidelines` | vercel-labs/agent-skills | UI review, accessibility, UX audit |
| `tailwind-design-system` | wshobson/agents | tailwind, design tokens, utility CSS |
| `tailwind-v4-shadcn` | jezweb/claude-skills | tailwind v4, shadcn/ui |
| `tailwindcss-advanced-layouts` | josiahsiegel/claude-plugin-marketplace | tailwind layouts, responsive |
| `remotion-best-practices` | remotion-dev/skills | remotion, programmatic video |
| `shadcn-ui-patterns` | community | shadcn, radix, component library |
| `css-architecture` | community | CSS modules, BEM, CSS-in-JS |
| `framer-motion` | community | animation, framer motion, gestures |

#### 🗄️ Databases & ORM (9)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `supabase-postgres-best-practices` | supabase/agent-skills | supabase, postgres, RLS, SQL |
| `prisma-database-setup` | prisma/skills | prisma, schema, migration |
| `prisma-client-api` | prisma/skills | prisma client, type-safe queries |
| `prisma-expert` | sickn33/antigravity-awesome-skills | prisma, advanced patterns |
| `drizzle-orm` | community | drizzle, ORM, type-safe SQL |
| `mongodb-patterns` | community | mongodb, mongoose, NoSQL |
| `pinecone-db` | community | pinecone, vector DB, embeddings |
| `turso-database` | community | turso, libSQL, edge database |
| `planetscale` | community | planetscale, MySQL, branching |

#### 🔐 Authentication (6)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `clerk-nextjs-patterns` | clerk/skills | clerk, auth, nextjs auth |
| `clerk-auth-v5` | clerk/skills | clerk v5, middleware, session |
| `better-auth-best-practices` | community | better-auth, auth library |
| `next-auth-v5` | the-misfits/agent-skills | nextauth, auth.js, OAuth |
| `auth-js-v5` | the-misfits/agent-skills | auth.js, session, JWT |
| `supabase-auth` | community | supabase auth, RLS, magic link |

#### 💳 Payments & Commerce (4)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `stripe-client` | community | stripe, payment, checkout |
| `stripe-webhook` | community | stripe webhook, event handling |
| `stripe-checkout` | community | stripe checkout, subscription |
| `stripe-connect` | community | stripe connect, marketplace |

#### 🧪 Testing (5)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `testing-library` | community | testing library, react testing |
| `vitest-best-practices` | the-misfits/agent-skills | vitest, unit test, coverage |
| `playwright-e2e` | the-misfits/agent-skills | playwright, e2e, browser test |
| `cypress-patterns` | community | cypress, e2e, component test |
| `testing-guidelines` | anthropics/skills | test strategy, TDD, test design |

#### ☁️ Cloud & Deployment (7)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `vercel-deploy-claimable` | vercel-labs/agent-skills | vercel deploy, preview URL |
| `vercel-deployment-best-practices` | community | vercel, edge functions, ISR |
| `azure-deployment` | microsoft/skills | azure, cloud, Microsoft |
| `aws-deployment` | microsoft/skills | AWS, Lambda, S3 |
| `docker-expert` | community | docker, container, Dockerfile |
| `docker-compose-orchestration` | community | docker compose, multi-container |
| `multi-stage-dockerfile` | community | docker build, multi-stage, CI |

#### 🤖 AI & ML (5)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `vercel-ai-sdk-best-practices` | community | AI SDK, streaming, LLM |
| `langchain-skills` | community | langchain, agents, RAG |
| `openai-skills` | community | openai, GPT, embeddings |
| `tavily-search` | community | tavily, web search, research |
| `ai-sdk-patterns` | community | AI SDK, tool calling, generative UI |

#### 📡 APIs & Integrations (3)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `nextjs-supabase-auth` | sickn33/antigravity-awesome-skills | next.js + supabase, full-stack |
| `supabase-edge-functions` | nice-wolf-studio/claude-code-supabase-skills | edge functions, Deno |
| `nextjs-seo` | laguagu/claude-code-nextjs-skills | SEO, meta tags, sitemap |

#### 📱 Mobile & Cross-Platform (2)

| Skill | Source | Install Keywords |
|-------|--------|-----------------|
| `expo-patterns` | community | expo, EAS, mobile deploy |
| `capacitor-patterns` | community | capacitor, ionic, hybrid app |

---

**Discovery Protocol:**
```
1. Check THIS index first (62 skills above)
   → Match found? → npx skills add {source} --skill {name} -a antigravity
2. No match? → npx skills find "{keyword}" on skills.sh
3. Still nothing? → Proceed without skill, note gap in .cm-skills-log.json

Trigger points:
  - cm-start Step 0.5 (before planning)
  - cm-planning Phase A Step 4 (scope analysis)
  - cm-execution Pre-flight (before dispatch)
  - cm-execution RARV (after 2 failed retries)
```

## Layer 2: Skill Summary

**Loaded when an agent has matched a skill from Layer 1 and needs more context.**

To access Layer 2, read the first 20 lines of the corresponding SKILL.md (frontmatter + first section).

```
Example: cm-tdd Layer 2
  - Full name: "TDD — Test Before Write"
  - When to Use: ALWAYS before implementing any feature or bugfix
  - Process: Red (write failing test) → Green (minimal code) → Refactor (clean up)
  - Integration: Works with cm-execution (subagent TDD), cm-quality-gate (coverage check)
  - Token cost: ~4200 tokens for full skill
```

## Layer 3: Full SKILL.md

**Loaded ONLY when executing.** Read the complete SKILL.md file.

```bash
# Agent loads full skill only when ready to execute
view_file /path/to/skills/cm-tdd/SKILL.md
```

## Usage Protocol

```
1. AT SESSION START:
   - Load this skill index (Layer 1) — costs ~2500 tokens total
   - Now you know what 34 skills do without reading any of them

2. WHEN MATCHING A TASK:
   - Scan Layer 1 triggers to find matching skill(s)
   - If unsure, read Layer 2 (first 20 lines of SKILL.md)
   - Choose the best skill

3. WHEN EXECUTING:
   - Load Layer 3 (full SKILL.md) for the chosen skill
   - Follow the skill's instructions completely

4. SAVINGS:
    - Without index: 34 × 3000 = 102,000 tokens
    - With index: 2800 + 300 + 3000 = 6,100 tokens
    - Saved: ~95,900 tokens (~94%)
```

## Skill Domain Mapping

For dynamic agent selection (Phase 3), skills map to domains:

```yaml
engineering: [cm-tdd, cm-debugging, cm-quality-gate, cm-code-review, cm-codeintell, cm-reactor, cm-clean-code]
operations: [cm-safe-deploy, cm-identity-guard, cm-terminal, cm-safe-i18n]
security: [cm-safe-deploy]
product: [cm-brainstorm-idea, cm-planning, cm-ux-master, cm-design-system, cm-dockit, cm-project-bootstrap, cm-jtbd]
growth: [cm-content-factory, cm-ads-tracker, cm-cro-methodology]
orchestration: [cm-execution, cm-continuity, cm-skill-index, cm-skill-health, cm-skill-evolution, cm-skill-chain, cm-deep-search, cm-readit, cm-how-it-work]
commands: [cm-start, cm-status]
# planned (no SKILL.md yet): mom-test, release-it, medical-research, tailwind-mastery, pandasai-analytics, cm-google-form
```

## The Bottom Line

**Know everything. Load nothing. Execute precisely. Save 90%+ tokens.**
