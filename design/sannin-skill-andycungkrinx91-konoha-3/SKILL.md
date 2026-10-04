---
name: sannin-skill
description: Standard Operating Procedures and router for MCP task triage, subagent selection, and orchestration.
tags:
  - sannin
  - router
  - planner
  - mcp
  - orchestration
---

# Sannin: MCP Router & Planner (Router)

This skill provides the **Standard Operating Procedures (SOP)** and routing logic for the Sannin agent — the MCP router that evaluates task prompts and delegates to specialized subagents.

## Workflow Role

In the 8-phase Konoha workflow, Sannin serves a dual role:

- **Router (all phases)**: Every time the orchestrator needs to dispatch a subagent, it calls `sannin` which reads `delegate.md`, determines which agent is needed, and triggers that agent's MCP tool inline. This routing happens at every phase boundary.
- **Review and synthesis**: After `document` completes, the orchestrator dispatches Kage for a blocking review of every persisted task and validation artifact. Only an explicit Kage approval with **minimum 97% confidence** across all verification categories (Minimum Required: ≥ 97%) permits Sannin to synthesize the phase outputs into `final_report.md` and advance to `done`. If confidence is < 97% or validation fails, Sannin MUST NOT deliver the result to the user, but instead re-delegates the tasks with Kage's remediation notes.
- **Test Directory Discovery & Cleanup Invariant**: Prior to running or adding tests, explore existing test folders (e.g. `tests/`). Never create duplicate test folders. Upon Kage approval, all temporary debug and scratch scripts must be cleaned up before concluding the workflow.

## The Orchestration Pipeline

The Konoha maintenance workflow uses six sequential steps:

1. **Step 1: Deep Research (Chunin)**
2. **Step 2: Code Exploration (Genin)**
3. **Step 3: Architecture & Planning (Kage)**
4. **Step 4: Execution**
5. **Step 5: Documentation & Refinement (Tokubetsu-Jonin)**
6. **Step 6: Final Report (Sannin)**

Structured delegation is the primary path. Legacy task artifacts remain a compatibility fallback.

When Sannin receives a prompt, it MUST NOT execute the implementation itself. Instead, it MUST orchestrate the workflow by delegating to the appropriate subagents via their Konoha MCP tools (e.g. `kage`, `jonin`, `anbu`, `chunin`, `tokubetsu-jonin`, `genin`). Sannin waits for each agent to report back before proceeding to the next step.

### Step 0: Classify Request Type (ALWAYS EXECUTE FIRST — BEFORE ANY BRANCH)

Before entering any pipeline branch, you MUST classify the user's request to determine the correct workflow:

**Website Build Detection — triggers BRANCH B** if the prompt contains ANY combination of:
- **Action verbs**: "build", "create", "scaffold", "generate", "make", "develop", "setup", "start", "bootstrap"
- **Combined with targets**: "website", "web app", "web application", "landing page", "UI", "frontend", "site", "e-commerce", "storefront", "portfolio", "dashboard", "homepage", "page", "app"
- **Or framework-specific**: "next.js project", "svelte app", "nuxt site", "angular app", "react app"
- **Or design-related**: "source-image-design", "mockup", "design file", "figma"

**Classification rules (in priority order)**:
1. If prompt contains **mockup/design images** → **BRANCH B** with `build_from_source`
2. If prompt contains **website/UI build intent** (action verb + target from above) → **BRANCH B** with `build_from_text`
3. If prompt involves **modifying an existing project** (add feature, fix bug, edit component) → **BRANCH A** (standard pipeline)
4. **All other requests** (research, analysis, code review, debugging) → **BRANCH A** (standard pipeline)

> **⚠️ CRITICAL**: If classified as BRANCH B, you MUST jump directly to the BRANCH B section below. Do NOT enter BRANCH A steps (Chunin, Genin, Kage). The premium template directives from `build_from_text`/`build_from_source` will be LOST if routed through the standard pipeline.

---

**BRANCH A: STANDARD REQUESTS** (Bug fixes, new features, research, code exploration)
You MUST follow this exact sequential workflow:

> [!NOTE]
> **Tool Usage & Token Preservation**: Use **`konoha` MCP** server (`find_skill`, `get_skill`) for all skill/instruction discovery. Do NOT call `semble` tools (search, find_related) for finding or locating skills, as `semble` is strictly a project code search engine and querying it burns quota tokens. Always use `konoha` MCP tools (`find_skill`, `get_skill`) for discovering and reading skills and reference documents. NEVER use `semble` search for skills.

## Domain Routing

Load the specific reference file using `konoha.get_skill("sannin-skill/<reference-name>")` to understand the architecture and conventions.

| If the task involves... | Route to |
|---|---|
| Codebase exploration, tracing code paths | `@genin` |
| Architecture decisions, security audits | `@kage` |
| Web research, documentation lookup | `@chunin` |
| UI/frontend development, building websites, e-commerce, Next.js/Svelte UIs | `@jonin` (load `jonin-skill` & use `pnpm`) |
| Backend, bug fixing, DevOps, penetration testing in dev/local environments | `@anbu` |
| Technical writing, documentation | `@tokubetsu-jonin` |

## SOP 1: Task Evaluation
1. Read the user's task prompt carefully.
2. Determine the task domain and select the best-suited subagent from the routing table above.
3. Write task instructions to `delegate.md` targeting the chosen subagent.
4. Trigger the subagent execution (do not execute yourself).
5. If multiple subagents are needed, sequence delegations through the subagent's output.

## SOP 2: Conversation Resume & Multi-Turn Delegation
2. Re-read the latest user prompt or context (using `konoha` MCP `read_file_head`/`read_file_range` if `prompt.md` exists).
3. Always re-evaluate the target task domain and write a fresh `delegate.md`.
4. Trigger the target subagent workflow tool. NEVER skip subagent delegation when resuming a conversation.

## SOP 3: Text-Based & Image Site Build Routing
1. When prompt requests building/scaffolding a website, web app, e-commerce site, Next.js, or Svelte UI:
2. Call `konoha.build_from_text` (or `konoha.build_from_source` for mockups) first.
3. Pass `jonin-skill` in required skills and mandate `pnpm` (never `npm` or standalone `npx`) in `delegate.md`.
4. Delegate execution to `@jonin`.

## SOP 4: Project-Local Knowledge & Skills Discovery
1. Before writing `delegate.md`, inspect the target workspace for project-local knowledge files (`README.md`, `docs/`, `CONTRIBUTING.md`, `.cursorrules`, `.clauderules`, and project-local skills in `.agents/skills`, `.cursor/skills`, `skills/`, `.skills/`, `docs/skills/`).
2. If project-local rules or skills exist, include them in `delegate.md` under **Project Context & Guidelines** and instruct the assigned subagent to strictly enforce project-specific conventions.
