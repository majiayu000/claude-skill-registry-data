---
name: gpt-export
description: Generate 21 markdown knowledge files + custom instructions for creating a Custom GPT strategic consultant from the current workspace project.
user-invocable: true
allowed-tools: Read, Write, Grep, Glob, Bash, Edit, Agent
---

# GPT Export — Custom GPT Knowledge Package

Generate a complete Custom GPT knowledge package from the current workspace project. Produces 21 markdown files: 20 documentation files covering every dimension needed for high-level strategic collaboration, plus 1 optimized custom instructions file (≤7,500 characters).

## Purpose

This skill creates everything needed to build a **Custom GPT strategic consultant** for the current project. The GPT is NOT a coding partner — it's a high-level collaborator for **strategy, design, UI architecture, information architecture, user experience, content strategy, and product decisions**. It knows the frameworks and technologies in use but advises at the design and decision layer, not the implementation layer.

## Arguments

`$ARGUMENTS` — Optional output directory path. Defaults to `_docs/custom-gpt/`.

If $ARGUMENTS is provided, use it as the output directory. Otherwise use `_docs/custom-gpt/`.

## Process

### Phase 1 — Deep Project Discovery

Before generating any files, thoroughly explore the workspace to understand:

1. **Project identity** — Read README, CLAUDE.md, package.json, any manifest files
2. **Architecture** — Directory structure, framework, routing, data flow
3. **Design system** — CSS variables, Tailwind config, color tokens, typography, component library
4. **Pages & routes** — All user-facing pages, their purpose, hierarchy
5. **Content model** — Content types, taxonomies, relationships
6. **User flows** — Authentication, onboarding, conversion, engagement loops
7. **Features** — Feature flags, capabilities, integrations
8. **Navigation & IA** — Header, footer, sidebar, breadcrumbs, menus
9. **Brand & voice** — Tone, messaging, copy patterns
10. **Tech stack** — All dependencies and their roles
11. **Tenant/config system** — What's configurable vs hardcoded
12. **AI/agent capabilities** — Any AI features, chatbots, assistants
13. **Conversion architecture** — Pricing, CTAs, subscription tiers, funnels
14. **Animation & motion** — Motion design approach, libraries, patterns
15. **SEO & performance** — Metadata, sitemap, Core Web Vitals approach
16. **Third-party integrations** — APIs, services, webhooks
17. **Conventions & constraints** — Team rules, patterns, anti-patterns
18. **Responsive strategy** — Breakpoints, mobile-first patterns
19. **Accessibility** — A11y approach, ARIA patterns, contrast
20. **Current state** — What's shipped, what's in progress, known gaps

Use the Agent tool with Explore subagents to parallelize discovery. Read key files directly when you know what you're looking for.

### Phase 2 — Generate 20 Documentation Files

Create each file with clear, structured content optimized for GPT retrieval. Each file should:
- Start with a `# Title` and one-line summary
- Use consistent heading levels (##, ###)
- Front-load the most important information
- Use tables for structured data
- Use bullet lists for enumerations
- Avoid code blocks longer than 10 lines (this is for strategy, not implementation)
- Include cross-references to other files where relevant (e.g., "See also: 04-DESIGN-SYSTEM.md")
- Be 300–800 words (sweet spot for GPT retrieval chunking)

#### File Manifest

| # | Filename | Content |
|---|----------|---------|
| 00 | `00-INDEX.md` | Table of contents describing every file in the package. Lists each file with a 1-sentence description. This is the GPT's "map" of its knowledge. |
| 01 | `01-PROJECT-IDENTITY.md` | What the project is, who it serves, mission/vision, the problem it solves, target audience, positioning statement. |
| 02 | `02-ARCHITECTURE-OVERVIEW.md` | High-level system architecture — layers, data flow direction, key boundaries. Diagram-level, not code-level. |
| 03 | `03-TECH-STACK.md` | Every technology/framework and WHY it was chosen. Grouped by concern (framework, styling, data, auth, AI, payments, monitoring). |
| 04 | `04-DESIGN-SYSTEM.md` | Design tokens (colors, typography, spacing, radius, shadows), theming approach, dark/light mode, CSS variable architecture. |
| 05 | `05-COMPONENT-LIBRARY.md` | Available UI components (shadcn/ui + custom), their variants, when to use each. Component hierarchy and composition patterns. |
| 06 | `06-PAGE-INVENTORY.md` | Every page/route, its purpose, key sections, and conversion goal. Grouped by area (content, courses, account, etc.). |
| 07 | `07-CONTENT-MODEL.md` | All content types, their fields, relationships, taxonomies. How content flows from creation to display. |
| 08 | `08-USER-JOURNEYS.md` | Key user personas and their primary journeys through the platform. Conversion funnels, engagement loops, retention hooks. |
| 09 | `09-FEATURE-MAP.md` | Complete feature inventory with status (shipped/planned/flagged). Feature flags and their purpose. Capability matrix by subscription tier. |
| 10 | `10-NAVIGATION-IA.md` | Information architecture — site map, navigation hierarchy, header/footer structure, breadcrumb logic, search. |
| 11 | `11-TENANT-CONFIG.md` | What's configurable per tenant vs hardcoded. Configuration surface area. How theming and branding work. |
| 12 | `12-AI-CAPABILITIES.md` | AI features, agent architecture, chat UX, context system, tool use, guardrails. How AI integrates with the platform. |
| 13 | `13-CONVERSION-ARCHITECTURE.md` | Pricing tiers, CTAs, lead magnets, subscription flows, upgrade paths, payment integration, monetization strategy. |
| 14 | `14-BRAND-VOICE.md` | Tone, voice markers, messaging hierarchy, copy conventions, anti-patterns. How the brand communicates. |
| 15 | `15-RESPONSIVE-STRATEGY.md` | Breakpoint system, mobile-first patterns, touch targets, layout strategies (grid, flex, container queries). |
| 16 | `16-ANIMATION-MOTION.md` | Motion design philosophy, animation libraries (GSAP, CSS), scroll animations, micro-interactions, performance budget. |
| 17 | `17-SEO-PERFORMANCE.md` | SEO architecture (metadata, OG tags, structured data), sitemap strategy, Core Web Vitals approach, image optimization. |
| 18 | `18-INTEGRATIONS.md` | Third-party services (Supabase, Stripe, Sentry, Resend, OpenAI, Vercel), their roles, data flow, webhook patterns. |
| 19 | `19-CONVENTIONS-CONSTRAINTS.md` | Team rules, naming conventions, file organization, anti-patterns, "never do this" list, decision records. |
| 20 | `20-CUSTOM-INSTRUCTIONS.md` | The Custom GPT system instructions (≤7,500 characters). Optimized for GPT-4o. |

### Phase 3 — Generate Custom Instructions (File 20)

The custom instructions file (`20-CUSTOM-INSTRUCTIONS.md`) must be ≤7,500 characters and should:

1. **Open with identity & role** — "You are [Project Name] Strategic Consultant, an expert advisor for..."
2. **Define scope** — Strategy, design, UX, IA, content strategy, product decisions. NOT a code writer.
3. **Reference knowledge files explicitly** — "Consult [filename] when answering questions about X"
4. **Set behavioral rules**:
   - Always ground answers in the uploaded project knowledge
   - Cite which knowledge file informed the answer
   - Ask clarifying questions before making recommendations
   - Consider trade-offs and present options, not just one answer
   - Respect existing conventions and constraints
   - Think in terms of user impact, not technical implementation
5. **Define response format preferences**:
   - Lead with the recommendation
   - Explain the reasoning
   - Note trade-offs or risks
   - Suggest next steps
6. **Include domain expertise framing** — What the GPT should be expert in based on the project's domain
7. **Set guardrails**:
   - Don't write production code (pseudocode/wireframes OK)
   - Don't contradict established conventions without flagging it
   - Don't make assumptions about user research — ask
   - Always consider mobile-first
   - Always consider accessibility
8. **End with persona calibration** — How the GPT should "feel" in conversation (collaborative peer, not lecturer)

### Phase 4 — Write All Files

1. Create the output directory if it doesn't exist
2. Write all 21 files
3. Report completion with a summary of what was generated

## Rules

1. **No code dumps** — This is for strategic collaboration. Short code snippets (≤5 lines) are OK to illustrate a pattern, but never paste full files.
2. **Optimize for retrieval** — GPT knowledge files are chunked. Front-load key info. Use clear headings. Avoid burying important facts in paragraphs.
3. **Be concrete, not generic** — Every file should contain actual project-specific information, not boilerplate advice.
4. **Cross-reference** — Files should reference each other (e.g., "See 04-DESIGN-SYSTEM.md for token details").
5. **Current state** — Document what IS, not what should be. Note gaps or known issues where relevant.
6. **Custom instructions budget** — The 20-CUSTOM-INSTRUCTIONS.md file MUST be ≤7,500 characters. Count carefully. This is a hard limit from OpenAI.
7. **Repo-agnostic skill** — This skill must work on ANY project. Do not hardcode paths, entity names, or project-specific knowledge into this skill file. All project knowledge comes from Phase 1 discovery.
8. **Markdown only** — All output files are `.md`. No other formats.
9. **File naming** — Use the exact filenames from the manifest. Zero-padded numbers for sort order.
10. **No secrets** — Never include API keys, tokens, connection strings, or credentials in any output file.
