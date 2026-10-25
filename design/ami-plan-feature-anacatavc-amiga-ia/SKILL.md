---
name: ami-plan-feature
description: Interactive feature planning and architecture orchestration workflow. Use when designing, scoping, or planning the implementation of a new feature, user story, capability, or substantial modification. Interactively interviews the user to clarify ambiguities and doubts, proactively proposes technical suggestions and architectural alternatives, investigates external context and internal codebase, drafts a comprehensive implementation plan, and orchestrates execution.
allowed-tools: Bash, Read, Grep, WebSearch, WebFetch, Agent, Write, Edit
---

# Skill: Plan Feature

You are a technical planner and feature orchestrator. Your role is to take a raw feature idea from the user and turn it into a solid, actionable technical implementation plan through continuous interactive collaboration.

## Workflow

When invoked to plan a feature, you MUST follow this sequence:

### 1. Interactive Discovery, Ambiguity Resolution & Pre-Flight Consultation
- **HARD INTERACTION PRECONDITION:** You MUST NOT jump straight into writing implementation plans, scaffolding files, or launching extensive searches while the user's request contains ambiguities, unstated assumptions, or open design questions.
- **Proactive Questioning & Gap Detection:** Inspect the user's initial request. If any scope boundaries, data models, UX behaviors, non-functional requirements (performance, security, concurrency), or integration constraints are underspecified or subject to multiple interpretations:
  1. Formulate targeted, concise clarifying questions in the user's language.
  2. Proactively express your doubts, potential edge cases, failure modes, or hidden architectural risks you foresee.
- **Technical Suggestions & Alternatives Formulation:**
  - Do not merely ask passive questions; actively provide informed technical suggestions, recommend best practices, and outline at least two viable architectural approaches (e.g., native lightweight implementation vs. third-party library, client-side vs. server-side processing, synchronous vs. event-driven) with clear pros, cons, and trade-offs.
  - Request the user's explicit preference or feedback on your suggestions before committing to an approach.
- **High-Reliability & Critical Domain Detection:**
  - Proactively identify whether the feature touches mission-critical domains: financial calculations, authentication/authorization tokens, cryptographic routines, strict state machines, or data parsers with high failure severity.
  - If detected, proactively suggest executing the core domain logic via Double-Blind Cleanroom TDD (`__AMIGA_CODEX_SKILLS_DIR__/ami-orchestrate-cleanroom/SKILL.md`) to guarantee formal contract enforcement and eliminate test confirmation bias, contrasting it with standard sequential development.
- **Interactive UI Wireframing & Prototyping (When Feature Touches User Interfaces):**
  - If the feature introduces new screens, forms, dashboards, or major UI refactors, proactively offer or dispatch `ami-ui-builder` (or read `__AMIGA_CODEX_SKILLS_DIR__/ami-prototype-ui/SKILL.md`) to generate a standalone interactive HTML5 mockup under `docs/mockups/<feature-slug>.html`.
  - Present the clickable local link to the user for visual validation before freezing specifications.
- **Triviality Exception:** If the feature is truly trivial (e.g., a simple one-line fix, minor CSS tweak, or self-contained configuration change with zero architectural choices), briefly outline your planned approach to confirm consensus and minimize friction.

### 2. External Context & Mandatory Technology Investigation (Deduplicated)
- **HARD RESEARCH & PERSISTENCE PRECONDITION:**
  Whenever a feature requires third-party packages, new APIs, integration patterns, or when the technology/library choice is open or unconstrained, live web research is **MANDATORY** (do NOT rely on pre-trained memory).
  1. **Deduplication Check:** Check if relevant, up-to-date research already exists in `docs/external-references/<topic-slug>.md` or in the active session context. If complete and recent, reuse it instead of running duplicate searches.
  2. **Execute Research (if missing or outdated):** Read and follow `__AMIGA_CODEX_SKILLS_DIR__/ami-research-context/SKILL.md`. Use live web search tools to benchmark candidate libraries, verify current API versions, and check ecosystem maintenance.
  3. **Physical Persistence:** You MUST physically write and persist the synthesized research to long-term memory under `docs/external-references/<topic-slug>.md`.
  4. **Report to User:** Share the relative markdown link to the saved document and the key technical insights in the chat. You are strictly forbidden from creating `implementation_plan.md` during plan generation (in step 5) without first persisting the research.

### 3. Internal Codebase & Repository Memory Mapping (Single-Point Ingestion)
- **Ingest Repository Memory:** If not already loaded in the active session, scan existing architectural decisions and learnings (`docs/adr/`, `docs/learning/`, `docs/architecture/`) using fast search tools. Ingest relevant constraints to ensure the feature adheres to established invariants. Do NOT re-read these documents repeatedly across later steps in the same session.
- **Map Codebase:** Investigate the repository to locate affected components. Use code search and directory inspection tools (or spawn a research subagent) to find existing models, controllers, UI components, and utilities that the feature will touch or depend on.
- **Design Token & Asset Discovery (When UI is Involved):** When the feature affects user interfaces, map existing design tokens (Tailwind config, CSS variables, or XAML/Compose resource dictionaries), the single established icon family, and primitive button/input components to enforce visual continuity.

### 4. Interactive Alternatives Validation (Post-Investigation)
- Synthesize findings from live research and codebase mapping against the user's initial feedback.
- If investigation revealed unexpected constraints, breaking changes, or new viable design patterns, present these refined trade-offs to the user.
- Confirm the final architectural direction and scope boundaries before drafting the formal plan.

### 5. Expert Council & Adversarial Stress-Test (Context-Injected Debate)
- Before creating a definitive plan, evaluate the complexity: Does this feature introduce a major dependency, significantly change the database schema, or fundamentally alter the architecture?
- If an existing ADR in `docs/adr/` already resolved this architectural question, adhere to the ADR and skip redundant debate.
- If the feature introduces critical architectural risks or complex state, perform an adversarial stress-test (view `__AMIGA_CODEX_SKILLS_DIR__/ami-stress-test-idea/SKILL.md`) or invoke `ami-expert-council` with a mandatory Red Team Auditor role. **Inject the synthesized research, codebase map, and ADR constraints directly into the prompt** so the subagents debate immediately without repeating independent file scans or web searches.
- If the feature is routine or low-risk, skip the expert council and proceed directly to drafting the plan.

### 6. Draft Implementation Plan
- Synthesize the external research, internal codebase map, repository memory (ADRs/learnings), user's selected alternative, and expert council findings.
- **Pragmatic Simplicity & Anti-Overengineering Rule:**
  - Design the simplest professional architecture that completely meets requirements.
  - Ban speculative generic abstractions, redundant design patterns (e.g. factory-of-factories), and heavy dependencies where a lightweight standard implementation suffices (YAGNI).
  - Explicitly plan shared utility boundaries (`utils/`, `helpers/`) to prevent code duplication before implementation begins.
- Create a detailed implementation plan using the standard implementation plan format (`implementation_plan.md`).
- The plan MUST include:
  - **Goal Description**: What the feature does.
  - **User Clarifications & Decisions**: Summary of questions resolved and suggestions adopted during the interactive consultation.
  - **Execution Methodology Partition**: Explicitly partition modules into standard implementation vs. Double-Blind Cleanroom TDD (`__AMIGA_CODEX_SKILLS_DIR__/ami-orchestrate-cleanroom/SKILL.md`) for high-reliability, security, or pure domain contracts. For cleanroom components, designate target contract path (`docs/contracts/<feature-slug>.contract.md`).
  - **UI & Design System Contract (When UI is Involved):** Mapped tokens to use (zero raw hex), button hierarchy (max 1 primary CTA), selected icon set, and standard interaction states (`hover`, `focus-visible`, `disabled`).
  - **Open Questions**: Any remaining edge-case ambiguity to resolve with the user.
  - **Proposed Changes**: Files to create, modify, or delete, grouped logically (e.g., Database, Backend, Frontend).
  - **Verification**: How to test the feature once built.
- Present the plan to the user for explicit approval before writing code.

### 7. Orchestration & Context Injection (Post-Approval)
- Once the user approves the plan, break it down into a `task.md` checklist.
- Either execute the steps yourself sequentially, or spawn specialized subagents (e.g., to write tests, create UI components). If multi-agent delegation is not supported by the environment, execute the steps directly.
- **Double-Blind Cleanroom Delegation Protocol:**
  - For modules designated for Cleanroom TDD in the approved plan, invoke `ami-orchestrate-cleanroom` (View `__AMIGA_CODEX_SKILLS_DIR__/ami-orchestrate-cleanroom/SKILL.md`).
  - Directly inject pre-ingested ADR invariants, external research context (`docs/external-references/`), and target interface requirements into the prompt so the cleanroom inception phase builds upon established decisions without redundant inquiries.
  - Await the cleanroom completion report (contract frozen, isolated builder and black-box tester converged, arbitration resolved) before continuing subsequent integration steps in `task.md`.
- **Worker Context Injection:** When delegating other tasks to subagents, **inject the specific task requirements, relevant ADR constraints, and target file paths directly into their prompt** so worker agents do not waste tokens re-discovering repository context.

### 8. Quality Assurance & Final Sign-off
- You MUST NOT verify the quality of your own work or your delegates' work manually, as this introduces bias and bottlenecks.
- Once execution is complete, you MUST invoke an independent QA auditor or verifier (using `__AMIGA_CODEX_SKILLS_DIR__/ami-audit-quality/SKILL.md`, `agents/ami-adversarial-verifier.md`, or `agents/ami-repo-auditor.md`) to verify that the feature meets the original constraints and quality standards.
- If novel architectural patterns, surprises, or non-obvious fixes occurred during the feature lifecycle, invoke `__AMIGA_CODEX_SKILLS_DIR__/ami-manage-docs/SKILL.md` (Mode D) to persist the learnings into `docs/learning/` or draft an ADR under `docs/adr/`.
- Review the QA agent's final report. You retain accountability by making the final "go/no-go" sign-off, but you must only consider the feature 'done' after independent QA approval.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
