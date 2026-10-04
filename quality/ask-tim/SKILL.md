---
name: ask-tim
description: Ask which skill or flow fits your situation. A route through AOS's skills for work that travels idea to ship, plus a catalogue of the 185 available options for lookup. Use when unsure where to start, or when picking between overlapping choices.
category: bdb-core
---

<!-- The flow map below is derived from mattpocock/skills' ask-matt (MIT, see
     THIRD_PARTY_NOTICES.md). The route is AOS's own: most stations on
     upstream's main flow have no AOS equivalent, so copying it verbatim would
     have produced a router pointing at skills that do not exist. -->

# `ask-tim`: which way do I go?

You don't remember every skill, so ask. This does no work itself.

Two layers, answering different questions. **The flow map** answers *"which way?"* — the route work travels from an idea to something shipped, and which branch to take at each fork. **The catalogue** below it answers *"which skill?"* — grouped by domain, with overlap guidance for the cases where several look alike. Start with the flow; drop to the catalogue when you already know roughly where you are.

---

## The main flow: idea → ship

The route most work travels.

**1. Sharpen the idea.** `/grill-with-docs` whenever you are in a working directory — the interview *plus* a paper trail, writing settled terminology into `CONTEXT.md` and ADRs as it goes. Without a repo to write to, `/grill-me`. Both run the same `grilling` primitive; the difference is only whether the understanding survives the session.

For a bigger or fuzzier idea, `/bdbrainstorm` runs the same interview inside a multi-agent debate (`/bdbmediastorm` for live show-control and event tech). Don't grill twice — those skills already do this step.

**2. Branch: how much machinery does the build need?** This is the fork that matters, and picking wrong is expensive in both directions.

- **`/startcycle`** — the linear chain, and the right answer for most daily work. Architect → TechLead → Build → Reviewer, hand-offs as plain files, no state machine.
- **`/startcycle-graph`** — when you need the durable `state.json`, a Reviewer repair loop with a no-progress guard, an automated quality gate, and escalation to a human. Mission-critical or multi-session work. Runs headless.
- **`/startcycle-graph-user`** — a throwaway 2–4 node fan-out for one-off parallel work. Nothing persistent left behind.
- **Two-file edit?** No pipeline. Just do it.

**3. Review the plan before it is built.** At the Architect→TechLead gate, `aos-plan-canvas open production_artifacts/00_execution_plan.md` opens the plan in a browser where you point at what should change instead of retyping it. Mandatory at the end of `/bdbrainstorm` and `/bdbmediastorm`; optional in `/startcycle`; deliberately not forced in `/startcycle-graph`, which runs headless.

**4. Build, then review adversarially.** The pipelines invoke their own build and review nodes — you do not call these by hand. Reviewer's pass is a correctness check against the plan's contract; `godmode-shipping`'s gate is mechanical (lint, typecheck, tests). Two different checks, deliberately not merged.

Reach for `test-driven-development` or `tdd-workflow` on their own when you want one behaviour built test-first without a whole pipeline, and `git-pr-review` when reviewing a branch or PR against a fixed point.

**Forcing a specific skill into a run:** `--skill=<name>` on any startcycle variant makes it a hard requirement — for a private skill of your own no node would otherwise reach for. Validated before the run starts; a name that does not resolve halts rather than proceeding without it.

## Outside the core: the ECC store

When no native AOS skill fits, search the markdown-only ECC store before starting a pipeline:

- `aos-store search <query>` finds available fallback skills and agents.
- `aos-store install <name> --net` installs a verified item after explicit user action.
- `aos-store list --type=skills` and `aos-store list --type=agents` show the catalogue.
- The core remains the trusted AOS skill set; the store is a fallback, not a reason to bypass the startcycle validation.
- A missing `--skill` is reported by the dispatcher with the exact install command. It never downloads during a run.

---

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Issues piling up** → `/triage`. For work you did *not* create: bug reports, incoming requests, anything raw. Tickets a pipeline already produced are agent-ready — **do not triage them**.
- **Something is broken** → `systematic-debugging` for a structured hunt, `debugger` for a plain error. Both refuse to theorise before there is a reproduction.
- **You need a runnable answer, not an argument** → `/prototype`. Throwaway code to settle a question that conversation cannot, then bring what you learned back to the idea thread.
- **Deploying or shipping infrastructure** → `godmode-shipping` gates a release; `bdb-deploy`, `vercel-deployment` and `cloudflare-workers-expert` do the actual shipping.

---

## What this flow does not cover

Named so you don't go looking: AOS has no equivalent of a cross-session `handoff` file, and no `wayfinder`-style skill for charting a months-long effort as decision tickets. For work too large for one session, `/startcycle-graph`'s durable `state.json` is the closest thing — it is resumable, but it does not chart the fog for you.

---

## 🧭 Intent Index (Table of Contents)

If the user's intent matches one of these, jump to the corresponding section:

* **"I need to choose a build pipeline (startcycle vs startcycle-graph)"** ➔ [Agent Orchestration & Pipelines](#agent-orchestration--pipelines)
* **"I need multi-agent brainstorming or ideation"** ➔ [Agent Orchestration & Pipelines](#agent-orchestration--pipelines)
* **"I want to build a new UI component or page"** ➔ [Frontend, UI & Motion](#frontend-ui--motion)
* **"I want Tailwind, shadcn, or design-system UI work"** ➔ [Frontend, UI & Motion](#frontend-ui--motion)
* **"I'm optimizing React or Next.js performance"** ➔ [Frontend, UI & Motion](#frontend-ui--motion)
* **"I'm designing an API (REST/GraphQL)"** ➔ [Backend, APIs & Databases](#backend-apis--databases)
* **"I need Prisma, Drizzle, or Postgres schema help"** ➔ [Backend, APIs & Databases](#backend-apis--databases)
* **"I'm working with n8n workflows"** ➔ [Backend, APIs & Databases](#backend-apis--databases)
* **"I want to deploy to Vercel, Cloudflare, or a VPS"** ➔ [DevOps, Git & Deployment](#devops-git--deployment)
* **"I'm managing GitHub PRs, issues, or monorepos"** ➔ [DevOps, Git & Deployment](#devops-git--deployment)
* **"I want to scrape or extract data from a website"** ➔ [Web Scraping & Browser Automation](#web-scraping--browser-automation)
* **"I need to run browser automation or web testing"** ➔ [Web Scraping & Browser Automation](#web-scraping--browser-automation)
* **"I'm building an AI agent, RAG pipeline, or working with LLMs"** ➔ [AI, LLMs & Agents](#ai-llms--agents)
* **"I need an SEO, GEO, or accessibility audit"** ➔ [Content, SEO & Docs](#content-seo--docs)
* **"I need to write a README or documentation"** ➔ [Content, SEO & Docs](#content-seo--docs)
* **"I need to debug a failing test or weird bug"** ➔ [Core Programming & Debugging](#core-programming--debugging)
* **"I want to ship a feature safely to production"** ➔ [Core Programming & Debugging](#core-programming--debugging)
* **"I'm managing the BDB SaaS multi-cloud fleet"** ➔ [BDB Ecosystem & SaaS Ops](#bdb-ecosystem--saas-ops)
* **"I need Three.js, 3D, or motion work"** ➔ [Media & EventTech](#media--eventtech)
* **"I need live event tech, TouchDesigner, or Resolume help"** ➔ [Media & EventTech](#media--eventtech)
* **"I need PCB layout, schematic capture, or electrical/hardware design"** ➔ [Electrical & Hardware Design](#electrical--hardware-design)

---

## 🏗️ Agent Orchestration & Pipelines

Use these skills to orchestrate complex multi-agent workflows.

* **Top Picks:** `startcycle-graph`, `bdbrainstorm`

### Overlap: The 3 Build Pipelines
Don't guess which pipeline to use. Follow these rules (source of truth: `CLAUDE.md` and `skills/basic/*/SKILL.md`):
* **`startcycle`**: Use for a straight-line, predictable run through the agents with file hand-offs and no state machine. Cheapest of the three.
* **`startcycle-graph`**: Use when you need the full dispatcher graph: durable `state.json`, a Reviewer repair loop, a quality gate, and human escalation.
* **`startcycle-graph-user`**: Use for a small throwaway fan-out (2-4 nodes) in any project without persistent artifacts.

### Overlap: Brainstorming
* **`bdbrainstorm`**: For multi-agent software engineering ideation, UI/UX design, and architecture planning. Handoffs to `/startcycle-graph`.
* **`bdbmediastorm`**: For creative-tech, live event technology, and show-control systems (TouchDesigner, Resolume, grandMA3).
* **`brainstorming`**: Lighter-weight than `bdbrainstorm` — use before any creative or constructive work to turn a vague idea into a validated design through disciplined reasoning, without spinning up a multi-agent cycle.

### Overlap: Planning Before Code
* **`concise-planning`**: A coding task needs a plan. Produces a clear, atomic checklist.
* **`writing-plans`**: You already have a spec/requirements for a multi-step task — write the plan before touching code.
* **`executing-plans`**: You already have a written plan and need to execute it in a separate session with review checkpoints.
* **`planning-with-files`**: Work like Manus — persistent markdown files as working memory on disk, for long-running or resumable tasks.
* **`deep-research`**: The task is autonomous research (plan → search → read → synthesize into a report), not implementation.

### Overlap: Multi-Agent Session &amp; Tool Management
* **`agent-manager-skill`**: Managing multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling.
* **`agent-orchestrator`**: Meta-skill that scans available skills, matches them to task capabilities, and coordinates multi-skill workflows — one level above picking a single skill by hand.
* **`agent-tool-builder`**: You're building a *new* tool for an agent to use (not picking an existing skill) — schema design through error handling.
* **`agent-memory-mcp`**: A hybrid persistent/searchable memory system for agents (architecture, patterns, decisions) — distinct from `memb-skill`/`memb-ingest`, which are BDB's own memB engine specifically.
* **`triage`**: Moving issues/external PRs through a categorize → verify → brief state machine, not general planning.
* **`prototype`**: A throwaway prototype to sanity-check a state model or UI direction before committing to real work.

*Also see:* `agent-pipeline`, `subagent-driven-development`.

---

## 🎨 Frontend, UI & Motion

Use these skills for UI development, component architecture, and design taste.

* **Top Picks:** `godmode-ui-ux`, `ui-component`, `senior-frontend`

### Overlap: The UI Cluster vs Senior Frontend
* **`ui-component` / `ui-page` / `ui-pattern`**: Use these strictly when scaffolding new pieces in the **StyleSeed Toss** design system convention (enforcing tokens, spacing, and rhythm).
* **`ui-review` / `ui-tokens`**: Use for reviewing code against StyleSeed or syncing its design tokens.
* **`senior-frontend`**: Use for general React/Next.js/Tailwind development outside of strict StyleSeed scaffolding, or for reviewing general frontend code quality.
* **`shadcn`**: Use specifically when adding or customizing shadcn/ui components.
* **`tailwind-patterns`**: Use when managing CSS-first configurations, container queries, or Tailwind CSS v4 design token architectures.

### Overlap: React & Next.js Performance
* **`react-best-practices`**: The Vercel-maintained guide for broad performance optimization and App Router data fetching.
* **`react-patterns`**: Use for core hooks, composition, and TypeScript best practices.
* **`nextjs-app-router-patterns` / `nextjs-best-practices`**: Use specifically for Next.js App Router architecture and routing.
* **`react-component-performance`**: Use for targeted diagnosis of slow React components (e.g., render bottlenecks).
* **`tanstack-query-expert`**: Async state/data-fetching specifically — TanStack Query mutations, stale time, optimistic updates.
* **`zustand-store-ts`**: Client-side state stores with Zustand, typed and with middleware.
* **`web-performance-optimization`**: Broader than component-level — Core Web Vitals, bundle size, caching across the whole app.
* **`wcag-audit-patterns`**: Accessibility compliance auditing against WCAG 2.2, not general UX review.
* **`frontend-dev-guidelines`**: General-purpose frontend engineering standards when the task doesn't need a narrower skill above. For the backend half, `godmode-engineering` and `software-architecture`.
* **`landing-page-generator`**: Specifically a high-converting marketing landing page (PAS/AIDA/BAB copy frameworks), not a general app page.

### Overlap: The UX Cluster
* **`ux-flow`**: Designing user flows, progressive disclosure, hub-and-spoke navigation (StyleSeed patterns).
* **`ux-audit`**: Auditing existing screens against Nielsen's heuristics and mobile UX best practices.
* **`ux-feedback`**: Adding loading/empty/error/success feedback states to components.
* **`ux-persuasion-engineer`**: Conversion/onboarding/checkout flows specifically — choice architecture, friction audits, commitment design.
* **`ui-ux-pro-max`**: Broader design guide (color, typography, general UI review) when the task doesn't fit one of the narrower UX skills above.

*Also see:* `bdbdesignpro`, `design-spells`.

---

## 🗄️ Backend, APIs & Databases

Use these for server-side architecture, APIs, workflows, and database schema design.

* **Top Picks:** `godmode-engineering`, `api-design-principles`, `drizzle-orm-expert`

### Overlap: Database & ORM Choices
* **`database-design`**: Use for overarching schema design, indexing strategy, and general database principles.
* **`postgres-best-practices`**: Use for raw performance optimization, queries, and Supabase-specific patterns.
* **`postgresql`**: Use for raw schema design, indexing, and Postgres constraints.
* **`using-neon` / `neon-postgres`**: Use specifically when working with Neon's serverless Postgres (branching, connection pooling).
* **`prisma-expert`**: Use for Prisma ORM schema design, migrations, and relational modeling.
* **`drizzle-orm-expert`**: Use for Drizzle ORM type-safe queries and serverless integrations.

### Overlap: The n8n Cluster
* **`n8n-workflow-patterns`**: Use for architectural patterns of whole workflows.
* **`n8n-code-javascript` / `n8n-code-python`**: Use when writing custom code inside n8n Code nodes (handles `$input`/`$json` nuances for JS/Python).
* **`n8n-expression-syntax`**: Use for debugging `{{}}` expressions.
* **`n8n-mcp-tools-expert`**: Use for integrating n8n-mcp tools effectively.

### Overlap: Architecture Level
* **`software-architecture`**: General quality-focused architecture guidance — the default when the task is "design/analyze architecture" without a more specific fit below.
* **`microservices-patterns`**: Specifically service boundaries, inter-service communication, and distributed-systems resilience.
* **`architect-review`**: Reviewing an existing architecture against modern practice, not designing a new one from scratch.

*Also see:* `api-patterns`, `openapi-spec-generation`, `golang-pro`, `python-pro`.

---

## 🕷️ Web Scraping & Browser Automation

Use these skills to extract data or control browsers.

* **Top Picks:** `apify-ultimate-scraper`, `playwright-skill`

### Overlap: Scraping and Extraction
* **`apify-ultimate-scraper`**: The top-level choice. Automatically selects from 55+ Apify Actors for the task.
* **`apify-lead-generation`**: Narrow use case: scraping leads from multiple platforms.
* **`web-scraper`**: Multi-strategy data extraction (tables, prices) with pagination and CSV/JSON export.
* **`browser-automation`**: General principles for selectors, waiting, and anti-detection.
* **`playwright-skill`**: Universal executor for custom Playwright code (e2e testing, interactive scraping).
* **`go-playwright`**: Use when writing browser automation in Go.
* **`webapp-testing`**: Use when writing native Python Playwright scripts for local testing.

---

## 🚀 DevOps, Git & Deployment

Use these to ship code, manage infrastructure, and handle source control.

* **Top Picks:** `godmode-shipping`, `github`, `vercel-deployment`

* **Godmode Shipping**: `godmode-shipping` is the ultimate pre-launch gatekeeper (lint, tests, rollbacks).
* **Deployments**: `vercel-deployment` (Next.js/React), `cloudflare-workers-expert` (Edge/KV/D1), `bdb-deploy` (rsync over SSH to VPS), `docker-expert` (Containers).
* **Git/GitHub**: `git-advanced-workflows`, `git-pr-review`, `github-workflow-automation`, `github-repo`, `github-actions-templates` (CI/CD workflow patterns specifically).
* **Monorepos**: `turborepo-caching`, `monorepo-management`.

---

## 🧠 AI, LLMs & Agents

Use these when building AI products or optimizing models.

* **Top Picks:** `prompt-engineer`, `llm-structured-output`, `rag-engineer`

* **Agent Dev**: `ai-agent-development`, `crewai`.
* **LLM Integration**: `gemini-api-integration`, `gemini-api-dev` (Gemini API model capabilities specifically), `local-llm-expert`, `llm-app-patterns`.
* **Conversational AI Products**: `llm-application-dev-ai-assistant` — building a chatbot/assistant product end-to-end, not just integrating one API.
* **Prompting**: `prompt-engineering-patterns`, `llm-prompt-optimizer`.
* **RAG**: `rag-implementation`, `rag-engineer` (broader — embedding models, vector DB selection), `vector-database-engineer` (specifically Pinecone/Weaviate/Qdrant/Milvus/pgvector selection and tuning).
* **Vercel AI SDK**: `vercel-ai-sdk-expert` — `generateText`/`streamText`, UI hooks, tool calling specifically on Vercel's SDK.

---

## 📝 Content, SEO & Documentation

Use these for docs, markdown, and search engine optimization.

* **Top Picks:** `readme`, `seo`, `documentation`

* **Docs**: `openwiki-skill`, `readme`, `copywriting`.
* **SEO**: `seo` (broad audit), `seo-technical` (crawlability, CWV), `seo-audit` (rankings), `geo-fundamentals` (AI search), `programmatic-seo`, `schema-markup`.

---

## 🔧 Core Programming & Debugging

Use these for raw problem solving and code hygiene.

* **Top Picks:** `systematic-debugging`, `clean-code`, `test-driven-development`

* **Debugging**: `debugger` (general errors), `systematic-debugging` (structured triage before fixing).
* **Hygiene**: `simplify-code` (diff review for clarity).
* **TDD**: `tdd-workflow`.

### Overlap: Language Expertise
* **`typescript-pro`**: Advanced types, generics, strict type safety, enterprise patterns.
* **`modern-javascript-patterns`**: ES6+ features and functional patterns (no TypeScript-specific typing concerns).
* **`python-patterns`**: Framework selection, async patterns, project structure — decision-making, not a specific bug.
* **`python-performance-optimization`**: An existing Python app is slow — profiling and bottleneck fixes specifically.
* **`go-concurrency-patterns`**: Goroutines, channels, sync primitives, race-condition debugging.
* **`bash-linux`**: General Bash/Linux scripting patterns, macOS or Linux.
* **`posix-shell-pro`**: The script must run on any POSIX shell (dash/ash/sh), not just bash.
* **`tmux`**: Terminal multiplexing and persistent remote session management specifically.

---

## 🌀 BDB Ecosystem & SaaS Ops

Specific utilities for the BDB environment.

* **Top Pick:** `memb-skill`

*Also see:* `memb-ingest`, `synapse-integration-skill`.

---

## 🧊 Media & EventTech

Use these for 3D, motion, video and live show control.

* **Top Picks:** `godmode-media-creation` (video and montage), `godmode-eventtech` (live shows), `godmode-3d-creation` (meshes and scenes)

* **Godmodes**: Determine the overarching flow (3D, Media, EventTech).
* **Implementations**: `mcp-manage` drives the creative applications over MCP, `spline-3d-integration` (web 3D), `threejs-skills` (WebGL), `remotion` (React → MP4, deterministic frame counts).

* **Per-application MCP guides**: once `mcp-manage` has told you *which* server to use, these document the tool surface of one application each — `bdb-touchdesigner-mcp`, `bdb-resolume-mcp`, `bdb-grandma3-mcp`, `bdb-davinci-mcp`, `bdb-adobe-suite-mcp`, `bdb-after-effects-mcp`, `bdb-blender-mcp`, `bdb-unreal-mcp`, `bdb-rhino-mcp`, `bdb-vectorworks-mcp`. Reach for one only when you already know the application; `mcp-manage` is the way in.

### Which video route?

The choice is driven by where the pixels come from, not by the output format — all four end in a video file.

| Source material | Route |
|---|---|
| Code-generated motion graphics, text, brand animation | `remotion` — React components rendered to MP4, deterministic and exactly frame-accurate |
| Existing footage: cutting, colour, beat-sync | `godmode-media-creation` + `mcp-manage` → **DaVinci Resolve** (`davinci-resolve-mcp`) or **Adobe Premiere** (`adobe_uxp_mcp`) |
| Compositing, motion design over footage | `mcp-manage` → **After Effects** (`ae-mcp`, `after-effects-mcp`), or **Photoshop** for stills (`adobe_uxp_mcp`) |
| Generative visuals: audio-reactive, shaders, real-time | `godmode-eventtech` → TouchDesigner MCP, then `record_movie` |
| Generative *assets*: text→3D, image→3D, AI video | The **Creator Extension** engines — TRELLIS and TripoSR (3D), Text-to-CAD, OpenMontage (multimodal montage), Video-Shotcraft (shot direction), Palmier-Pro (timeline and grading), driven through `comfyui-mcp`. Installed as a separate power-up module, not a skill in this catalogue. |
| Concept not settled yet | `bdbmediastorm` first — it runs the grilling interview for show-control and media work |

Resolve and Premiere are interchangeable at this level: pick whichever is actually installed. Both have a working MCP under `mcps/`.

---

## 🔩 Electrical & Hardware Design

Use these for schematic capture, PCB layout, and physical hardware design (KiCad, OpenSCAD).

* **Top Picks:** `godmode-hardware-pcb`, `code-first-hardware-design`, `pcb-constraint-definition`

* **Architectural authority**: `godmode-hardware-pcb` — enforces IPC-standard trace/impedance/stackup math and the headless ERC/DRC/DFM sign-off gate across the skills below; load it before starting schematic or layout work.
* **Circuit synthesis & enclosures**: `code-first-hardware-design` — programmatic schematic capture (SKiDL, netlists, S-expressions) and parametric 3D CAD enclosure co-design (OpenSCAD/BOSL2).
* **Constraints & stackup**: `pcb-constraint-definition` — translates hardware requirements into layer stackup, netclasses, impedance matching, and custom DRC rules before layout starts.
* **Layout & routing**: `pcb-layout-routing-automation` — floorplanning, component placement, high-speed differential pair routing, thermal via arrays, and keepout enforcement.
* **Validation & sign-off**: `pcb-validation-dfm-signoff` — automated DRC/ERC, SI/PI screening, fab house DFM/DFA compliance, and production release sign-off (Gerbers/BOM/CPL).
* **Schematic & datasheet auditing**: `schematic-datasheet-analysis` — electrical rule auditing, datasheet grounding, pinout validation, and power tree tracing.

These ship in the separate `@hybridlabor-api/bdb-hardware-pcb` power-up module (KiCad + OpenSCAD MCP servers), not in this base skills package — install it as an optional AOS module when hardware work comes up.

---

## 🛡️ Overlap: The Supreme Godmodes

When do you use a `godmode-*` skill versus a narrower skill?
* **`godmode-ui-ux`, `godmode-engineering`, `godmode-shipping`, `godmode-3d-creation`, `godmode-media-creation`, `godmode-eventtech`** are orchestrator/enforcer skills. They hold the "supreme rulebook" for a domain. Use them when starting a major feature or defining the overarching architecture of a task.
* Use narrower skills (e.g., `shadcn`, `drizzle-orm-expert`, `threejs-skills`) for the tactical implementation inside those domains.

---

## 🛑 Fallback Note

If none of the intents above match your task, look for the closest general library skill in the catalog. 

**Remember:** This file helps discover skills, but **`CLAUDE.md`** is the canonical source of truth for the primary Skill Routing by Domain table and the exact rules for Agent Counts (subagents vs teams vs solo). Do not rely on `ask-tim` to dictate pipeline definitions—always defer to `CLAUDE.md`.
