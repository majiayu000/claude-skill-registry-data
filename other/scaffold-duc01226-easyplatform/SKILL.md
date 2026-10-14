---
name: scaffold
version: 1.1.0
description: '[Architecture] Use when scaffolding reusable OOP/SOLID project foundations before feature implementation.'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Generate and validate the project's architecture scaffolding — all base classes, interfaces, infrastructure abstractions, and reusable foundation code — BEFORE any feature story implementation begins, producing a copy-ready, OOP/SOLID-compliant architecture foundation with quality-gate tooling that every feature story reuses before implementation starts.

**Summary:**

- **Gate-first:** check Activation Guards before any work — proceed ONLY in `workflow-greenfield-init` / `workflow-big-feature` AND when grep finds NO existing base/abstract/infrastructure scaffolding; otherwise SKIP and mark the step completed.
- **Main steps (do ALL, in order):** (1) Read Plan — parse tech stack, architecture decisions, domain model; (2) Generate Scaffolding Checklist from the Backend + Frontend/UI categories; (3) Validate Against Plan — every architecture decision has a scaffolding item; (4) Present to User via `AskUserQuestion` to confirm the checklist; (5) Scaffold — create all base classes, interfaces, abstractions, infra code + the 5 production-readiness foundations; (6) Verify — build/compile + OOP/SOLID compliance + Verification Gate. Then invoke `/linter-setup` → `/harness-setup`, then `AskUserQuestion` handoff.
- **Scope:** architecture-infrastructure creation (base classes, interfaces, DI, repos, cross-cutting), NOT feature implementation — checklists are TEMPLATES: adapt naming to the detected tech stack, skip irrelevant items, add plan-specific ones.
- **Production-readiness:** stand up all 5 foundations (code-quality tooling, error handling, loading state, Docker, integration points) and delegate ALL sensor setup to `/linter-setup` then `/harness-setup` — never hand-configure linters/hooks here. — why: a checklist of installs is not a harness.
- **Hard gate:** enforce OOP/SOLID on every base class and HARD-BLOCK the handoff to `/feature-implement` until the Verification Gate passes — all 5 foundations verified plus `/linter-setup` and `/harness-setup` complete.

**Purpose:** Scaffolded project copy-ready as starter template. All base code, utilities, interfaces, infrastructure services created — best-practice setup, generic functions any feature story reuses.

**Key distinction:** Architecture infrastructure creation, NOT feature implementation — the foundation layer all stories build upon.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Activation Guards (MANDATORY — Check Before Executing)

**ALL conditions must be true to proceed:**

1. **Workflow check:** Active workflow is `workflow-greenfield-init` OR `workflow-big-feature`. If not → SKIP this skill entirely, mark step as completed.
2. **Existing scaffolding check:** AI MUST ATTENTION self-investigate for existing base/foundational abstractions:
    - Abstract/base classes: grep `abstract class.*Base|Base[A-Z]\w+|Abstract[A-Z]\w+`
    - Generic interfaces: grep `interface I\w+<|IGeneric|IBase`
    - Infrastructure abstractions: grep `IRepository|IUnitOfWork|IService|IHandler`
    - Utility/extension layers: grep `Extensions|Helpers|Utils|Common` (directories or classes)
    - Frontend foundations: grep `base.*component|base.*service|base.*store|abstract.*component` (case-insensitive)
    - DI/IoC registration: grep `AddScoped|AddSingleton|providers:|NgModule|@Injectable`
3. **If existing scaffolding found → SKIP.** Log: "Existing scaffolding detected at {file:line}. Skipping /scaffold step." Mark step as completed.
4. **If NO foundational abstractions found → PROCEED** with full scaffolding workflow below.

## When to Use

- After the second `/plan` + `/plan-review` in greenfield-init or big-feature workflows
- Before `/feature-implement` begins implementing feature stories
- When a new service/module needs its own base architecture within an existing project
- **NOT** when the project already has established base classes and infrastructure

## Workflow

1. **Read Plan** — Parse the implementation plan for architecture decisions, tech stack, and domain model
2. **Generate Scaffolding Checklist** — Produce a checklist of all required base classes and infrastructure from the Backend + Frontend checklists below
3. **Validate Against Plan** — Ensure every architecture decision in the plan has corresponding scaffolding items
4. **Present to User** — Use `AskUserQuestion` to confirm checklist before generating code
5. **Scaffold** — Create all base classes, interfaces, abstractions, and infrastructure code
6. **Verify** — Compile/build to ensure no syntax errors; validate OOP/SOLID compliance

## Backend Scaffolding Categories

AI must self-investigate chosen tech stack, produce a checklist covering these categories. Names below are illustrative — adapt to the project's language, framework conventions, and actual needs.

### Domain Layer

- [ ] Base entity interface + abstract class (Id, timestamps, audit fields)
- [ ] Value object base (equality by value)
- [ ] Domain event interface

### Application Layer

- [ ] Command/query handler abstractions (CQRS if applicable)
- [ ] Validation result pattern
- [ ] Base DTO with mapping protocol
- [ ] Pagination wrapper
- [ ] Operation result pattern (success/failure)

### Infrastructure Layer

- [ ] Generic repository interface + one concrete implementation
- [ ] Unit of work interface (if applicable)
- [ ] Messaging/event bus abstraction
- [ ] External service abstractions (cache, storage, email — only if plan requires them)
- [ ] Database context / connection setup
- [ ] DI/IoC registration module

### Cross-Cutting

- [ ] Current user context abstraction
- [ ] Testable date/time provider
- [ ] Exception hierarchy (domain, validation, not-found)
- [ ] Error handling middleware
- [ ] Strongly-typed configuration models

## Frontend Scaffolding Categories

### Core Architecture

- [ ] Base component with lifecycle/destroy cleanup
- [ ] Base form component with validation, dirty tracking
- [ ] Base list component with pagination, sorting, filtering

### State & API

- [ ] Base state store with loading/error/data pattern
- [ ] Base API service with interceptors, error handling
- [ ] Auth interceptor + environment config

### Shared Utilities

- [ ] Base model with serialization helpers
- [ ] Common utility functions (date, validation, formatting)

### UI Foundation

> **Skip if:** Backend-only project, no frontend component. **Apply if:** Project has ANY frontend.

#### Design Token Files

- [ ] Create design token file(s) per chosen format (CSS custom properties / SCSS variables / JSON)
- [ ] Define minimum token set: colors (primary, secondary, surface, bg, text, error, success, warning), spacing (xs-xl), typography (heading/body/caption families + sizes), breakpoints, shadows, z-index
- [ ] Create theme file(s) if theming required (light/dark CSS classes or theme provider)

#### Base Layout & Responsive

- [ ] Base layout component (app shell: header, sidebar/nav, main content, footer)
- [ ] Responsive container/grid utility
- [ ] Responsive mixin/utility for breakpoints
- [ ] Mobile-first media query definitions

#### Base UI Components

- [ ] Loading indicator component (spinner or skeleton)
- [ ] Error display component (inline + page-level)
- [ ] Empty state component (message + action)
- [ ] Notification/toast component
- [ ] Base button component with variants (primary, secondary, ghost, danger)
- [ ] Base input component with validation display

#### Design System Documentation

- [ ] Create `docs/project-reference/design-system/README.md` skeleton with: token naming conventions, component tier classification (Common/Domain-Shared/Page), usage examples
- [ ] **Author `docs/project-reference/ui-review-principles.md`** (the project-adopted UI-review PRINCIPLES the later `/ui-review` gate reads — these are design-time decisions, hand-authored, NOT code-derived). Capture, as project-enforced principles, every UI-review dimension: **Overflow & scroll containment** (long-content truncation/wrap) · **Responsive & small-screen** (flex-wrap / row-to-column so it stays usable on small devices) · **Flex-vs-fixed sizing** (flex-grow vs hard-coded dimensions) · **z-index discipline** (a documented layering scale, no ad-hoc values) · **BEM on all elements** · **Async states** (loading indicator, user-visible error surface, empty state, in-flight disable) · **Nesting depth ≤ 3 / no magic numbers**. **Cross-link** to `design-system/README.md` and `scss-styling-guide` so the seeded principle doc and the scan-derived docs form one navigable set. Contains NO real endpoints/keys.
    - **No-UI skip rule:** author this doc ONLY when a frontend/UI stack is scaffolded. Backend-only project → SKIP and log the reason.

## Example / Golden-Path Reference Scaffolding (copy-me implementations — MANDATORY)

> **MANDATORY when scaffolding a foundation:** beyond the empty base abstractions above, emit **ONE worked, compile-checked example per best-practice pattern** — a copy-me reference implementation per layer. Empty abstractions are unverified skeletons; a worked example built ON TOP turns each base class into demonstrated, reviewable usage. This example set is exactly what Phase-02's `/architecture-review-full` grades, so it must exist before that gate runs.

### Location & lifecycle (isolated, production-excluded)

- Examples live in a DEDICATED, ISOLATED `examples/` tree (project-root `examples/` or `docs/project-reference/examples/`) — **NEVER mixed into the production `src/` tree.**
- Name every file `*.example.*` (e.g. `create-order.command.example.ts`, `Order.entity.example.cs`).
- **CI-compiled/linted but EXCLUDED from the production build** via a project-appropriate mechanism (separate compile target / tsconfig references / test-only project / build-exclude glob).
- Devs COPY an example into `src/` to start a real feature; the whole `examples/` tree is deleted wholesale once no longer needed.

### One worked example per applicable pattern (target ≥ 11)

- **Backend:** command · query · command/query handler · entity-with-invariants · value-object · repository (concrete impl) · domain event + event handler.
- **Frontend (only if a UI stack is present):** form component · list component · state store · API service.
- **Tests:** one example integration test exercising the example command/query on BOTH the happy path AND a failure path.
- **Absent-layer skips:** render fewer ONLY when a layer is genuinely absent (e.g. a backend-only project skips the frontend examples) — LOG each skipped example and WHY.

### Every example MUST

1. Follow the project's detected patterns — read `docs/project-reference/*-patterns-reference.md` and mirror the exact shapes.
2. USE the scaffolded base abstractions (demonstrate them in action; do NOT re-implement them).
3. Compile/lint clean under the CI (non-production) target.
4. Carry this header comment verbatim (adapt the comment syntax to the language): `GOLDEN-PATH EXAMPLE — copy into src/ for real features; the examples/ tree is deleted when unused; NOT compiled into the production build.`
5. Contain **NO secrets, real credentials, or real endpoints** — use obvious placeholders ONLY (`EXAMPLE_API_KEY`, `example.invalid`, `00000000-0000-0000-0000-000000000000`).

### Right-sizing

Examples DEMONSTRATE patterns — NOT a feature. Honor the scale-tier guard: a tiny T0/B0 project gets the minimal applicable set, never speculative extras.

## Code Quality Gate Tooling (MANDATORY MUST ATTENTION — Setup Before Any Feature Code)

**MANDATORY IMPORTANT MUST ATTENTION** scaffold ALL code quality enforcement tools as part of project infrastructure — code that passes without quality gates is technical debt from day one.

### Static Analysis & Linting

- [ ] **MANDATORY MUST ATTENTION** configure language-appropriate linter with strict ruleset (zero warnings policy on new code)
- [ ] **MANDATORY MUST ATTENTION** configure static code analyzer with quality gate thresholds (complexity, duplication) — treat line-coverage as a reported DIAGNOSTIC, NOT a build-failing threshold
- [ ] **MANDATORY MUST ATTENTION** enable compiler/transpiler strict mode and treat warnings as errors on build
- [ ] **MANDATORY MUST ATTENTION** add code style formatter with shared config (enforce consistent formatting across team)

### Build-Time Quality Enforcement

- [ ] **MANDATORY MUST ATTENTION** configure pre-commit hooks to run linter + formatter automatically
- [ ] **MANDATORY MUST ATTENTION** configure CI pipeline to fail on any linter violation, analyzer warning, or test failure
- [ ] **MANDATORY MUST ATTENTION** do NOT gate the build on a line-coverage %; report line-coverage as a diagnostic only (low = useful untested-area signal, high ≠ quality). If a test-strength gate is wanted, gate on mutation score (surviving mutant = missing/weak assertion) with line-coverage as the diagnostic. Keep behavior/change-coverage (each behavior-changing file has a test asserting the changed outcome) as the meaningful coverage notion
- [ ] **MANDATORY MUST ATTENTION** enable security vulnerability scanning in dependency management

### Code Rules & Standards

- [ ] **MANDATORY MUST ATTENTION** create shared linter config file at project root (team-wide consistency)
- [ ] **MANDATORY MUST ATTENTION** create shared formatter config file at project root
- [ ] **MANDATORY MUST ATTENTION** create `.editorconfig` for cross-IDE consistency (indentation, encoding, line endings)
- [ ] **MANDATORY MUST ATTENTION** document code quality standards in project README or contributing guide

### Harness Integration (MANDATORY — Do Not Skip)

**MANDATORY MUST ATTENTION** delegate ALL computational sensor setup to `/linter-setup`:

- Do NOT manually configure linters, formatters, or pre-commit hooks in this skill
- `/linter-setup` handles: tool research → install → configure → pre-commit hooks → CI gates
- `/harness-setup` handles: full harness inventory (feedforward guides + all feedback types)

**WHY:** Code quality tooling is part of the project's outer agent harness. A checklist of installs is not a harness — a harness is a system of guides and sensors where each control fires at the right lifecycle stage and produces signals the agent can consume.

**After scaffold, invoke (in order):**

1. `/linter-setup` — computational feedback sensors (deterministic, fast, always-on)
2. `/harness-setup` — full harness inventory (all feedforward guides + all feedback sensors)

**Do NOT proceed to `/feature-implement` until both complete.** (`/scaffold` verification gate enforces this)

## Production Readiness Scaffolding (MANDATORY)

> **Scaffold Production Readiness** — See `<!-- SYNC:scaffold-production-readiness -->` block above for full inline protocol.

Every scaffolded project MUST ATTENTION include these 5 foundations. AI must detect tech stack from the plan/architecture report, present 2-3 options per concern via `AskUserQuestion`.

### 1. Code Quality Tooling

Handled by `/linter-setup` skill — do NOT duplicate here.
Verify completion: check that `.editorconfig`, linter config, and pre-commit hook config files exist.
If missing → block scaffold completion, invoke `/linter-setup`.

### 2. Error Handling Foundation

- Detect frontend framework → select from protocol's framework patterns
- Generate: error types, HTTP interceptor, notification service, global error handler
- Minimum 4 files for frontend, 3 for backend-only
- Run protocol's verification checklist

### 3. Loading State Management

- Detect frontend framework → select from protocol's framework patterns
- Generate: loading service, HTTP loading interceptor, loading indicator component
- Counter-based tracking, 300ms display delay, skip token mechanism
- Run protocol's verification checklist

### 4. Docker Development Environment

- Always scaffold (unless user explicitly opts out)
- Generate: docker-compose.yml (with profiles), Dockerfile (multi-stage), .dockerignore, .env.example
- Use 127.0.0.1 binding, health checks on all services, non-root user in prod
- Run protocol's verification checklist

### 5. Integration Points

- Document each outbound boundary (downstream service, queue, third-party API, shared DB)
- Configure retry + circuit breaker + timeout per outbound dependency
- Generate integration tests for both the happy path and the failure path
- Run protocol's verification checklist

### Scaffold Handoff from Architecture-Design

If an architecture report exists (from `/architecture-design`), read the "Scaffold Handoff — Tool Choices" table and use those selections instead of re-asking the user.

## OOP/SOLID Compliance Rules (ENFORCE)

1. **Single Responsibility** — Each base class handles ONE concern
2. **Open/Closed** — Base classes are extensible via inheritance, closed for modification
3. **Liskov Substitution** — Concrete implementations are substitutable for their base
4. **Interface Segregation** — Small, focused interfaces (not one giant IService)
5. **Dependency Inversion** — All infrastructure behind interfaces, injected via DI

**Anti-patterns to prevent:**

- God classes combining multiple concerns
- Concrete dependencies (always depend on abstractions)
- Base classes with unused methods that subclasses must override
- Missing generic type parameters where applicable

## Adaptation Protocol

The checklists above are **templates**. Before scaffolding:

1. **Read the plan** — What tech stack was chosen?
2. **Adapt naming** — Match target framework and language conventions
3. **Skip irrelevant items** — Not every project needs every item (e.g., skip IFileStorageService if no file uploads)
4. **Add project-specific items** — The plan may require additional base classes not in the template
5. **Use `AskUserQuestion`** — Confirm final checklist with user before generating code

## Output

After scaffolding is complete:

1. **Scaffolding Report** — List of all created files with brief descriptions
2. **Build Verification** — Compilation/type-check passes
3. **Architecture Diagram** — Optional: generate diagram showing the base class hierarchy
4. **Production Readiness Verification** — All 5 concern areas verified via protocol checklists
5. **Config Files Generated** — Linter, formatter, pre-commit, Docker configs all created
6. **Golden-Path Examples** — one worked, compile-checked example per applicable pattern emitted under the isolated, production-excluded `examples/` tree; absent-layer skips logged with reason

## Verification Gate (MANDATORY before proceeding to /feature-implement)

Run ALL verification checklists from the production readiness protocol:

- [ ] Code quality tooling verified (Section 1)
- [ ] Error handling foundation verified (Section 2)
- [ ] Loading state management verified (Section 3)
- [ ] Docker development environment verified (Section 4)
- [ ] Integration points verified (Section 5)
- [ ] `/linter-setup` completed (linter + formatter + pre-commit + CI gate configured)
- [ ] `/harness-setup` completed (harness-inventory.md produced, feedforward guides in place)
- [ ] Golden-path examples present — one worked example per applicable pattern under an isolated, production-excluded `examples/` tree; each compiles/lints under the CI (non-production) target; every example carries the `GOLDEN-PATH EXAMPLE` header and NO secrets/real endpoints; absent-layer skips logged with reason

**BLOCK proceeding to `/feature-implement` if ANY verification item fails.** Fix issues first, then re-verify.

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** after completing this skill, MUST ATTENTION use `AskUserQuestion` to present these options. Do NOT skip because the task seems "simple" or "obvious" — the user decides:

- **"/feature-implement (Recommended)"** — Begin implementing feature stories on top of the scaffolding
- **"/workflow-review-changes"** — Review scaffolding code before proceeding
- **"Skip, continue manually"** — user decides

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

<!-- SYNC:nested-task-creation -->

> **Nested Task Expansion Contract** — For workflow-step invocation, the `[Workflow] ...` row is only a parent container; the child skill still creates visible phase tasks.
>
> 1. Call `TaskList` first. If a matching active parent workflow row exists, set `nested=true` and record `parentTaskId`; otherwise run standalone.
> 2. Create one task per declared phase before phase work. When nested, prefix subjects `[N.M] $skill-name — phase`.
> 3. When nested, link the parent with `TaskUpdate(parentTaskId, addBlockedBy: [childIds])`.
> 4. Orchestrators must pre-expand a child skill's phase list and link the workflow row before invoking that child skill or sub-agent.
> 5. Mark exactly one child `in_progress` before work and `completed` immediately after evidence is written.
> 6. Complete the parent only after all child tasks are completed or explicitly cancelled with reason.
>
> **Blocked until:** `TaskList` done, child phases created, parent linked when nested, first child marked `in_progress`.

<!-- /SYNC:nested-task-creation -->

<!-- SYNC:project-reference-docs-guide -->

> **Project Reference Docs Gate** — Run after task-tracking bootstrap and before target/source file reads, grep, edits, or analysis. Project docs override generic framework assumptions.
>
> 1. Identify scope: file types, domain area, and operation.
> 2. **Read `docs/project-config.json` first — the project's machine-readable map.** It is the single source of truth for THIS repo (modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns); ground exact paths, run-commands, and conventions on it **before investigating, planning, or coding** — never assume framework defaults (`CLAUDE.md` + reference docs are derived from it). If it — or the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any required reference doc — is missing or stale, auto-run `/project-init` or the narrow route (`/project-config`, `/docs-init`, `/scan-all`, `/scan --target=<key>`, `/claude-md-init`) first; if Codex mirrors or `AGENTS.md` are stale, ask the user to run `/sync-codex` (never auto-run it).
> 3. Required docs by trigger: always `docs/project-reference/lessons.md`; doc lookup `docs-index-reference.md`; review `code-review-rules.md`; backend/CQRS/API `backend-patterns-reference.md`; domain/entity `domain-entities-reference.md`; frontend/UI `frontend-patterns-reference.md`; styles/design `scss-styling-guide.md` + `design-system/design-system-canonical.md`; integration tests `integration-test-reference.md`; E2E `e2e-test-reference.md`; feature docs/specs `feature-spec-reference.md` + `spec-system-reference.md` + `spec-principles.md`; behavior/public-contract/spec-test-code sync `workflow-spec-test-code-cycle-reference.md`; derived spec index/ERD/reimplementation guides `spec-system-reference.md` + source Feature Specs under `docs/specs/`; architecture/new area `project-structure-reference.md`.
> 4. Read every required doc, then before target work state: `Reference docs read: ... | Not applicable: ...`.
>
> **Ready when:** scope evaluated, `docs/project-config.json` consulted, required docs checked/read or setup route completed, `lessons.md` confirmed, citation emitted.

<!-- /SYNC:project-reference-docs-guide -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:understand-code-first -->

> **Understand Code First** — HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
>
> 1. Search 3+ similar patterns (`grep`/`glob`) — cite `file:line` evidence
> 2. Read existing files in target area — understand structure, base classes, conventions
> 3. Run `python .claude/scripts/code_graph trace <file> --direction both --json` when `.code-graph/graph.db` exists
> 4. Map dependencies via `connections` or `callers_of` — know what depends on your target
> 5. Write investigation to `.ai/workspace/analysis/` for non-trivial tasks (3+ files)
> 6. Re-read analysis file before implementing — never work from memory alone. — why: long context drifts from the file; the file is ground truth
> 7. NEVER invent new patterns when existing ones work — match exactly or document deviation. — why: divergent patterns fragment the codebase and slow every future reader
>
> **BLOCKED until:** `- [ ]` Read target files `- [ ]` Grep 3+ patterns `- [ ]` Graph trace (if graph.db exists) `- [ ]` Assumptions verified with evidence

<!-- /SYNC:understand-code-first -->

<!-- SYNC:scaffold-production-readiness -->

> **Scaffold Production Readiness** — Every scaffolded project MUST ATTENTION include 5 foundations:
>
> 1. **Code Quality Tooling** — linting, formatting, pre-commit hooks, CI gates. Specific tool choices → `docs/project-reference/` or `project-config.json`.
> 2. **Error Handling Foundation** — HTTP interceptor, error classification (4xx/5xx taxonomy), user notification, global uncaught handler.
> 3. **Loading State Management** — counter-based tracker (not boolean toggle), skip-token for background requests, 300ms flicker guard.
> 4. **Docker Development Environment** — compose profiles (`dev`/`test`/`infra`), multi-stage Dockerfile, health checks on all services, non-root production user.
> 5. **Integration Points** — document each outbound boundary; configure retry + circuit breaker + timeout; integration tests for happy path and failure path.
>
> **BLOCK `/feature-implement` if any foundation is unchecked.** Present 2-3 options per concern via `AskUserQuestion` before implementing.

<!-- /SYNC:scaffold-production-readiness -->

<!-- SYNC:harness-setup -->

> **Harness Engineering** — An outer agent harness has two jobs: raise first-attempt quality + provide self-correction feedback loops before human review.
>
> **Controls split:**
>
> | Axis        | Type          | Examples                                                                                           | Frequency        |
> | ----------- | ------------- | -------------------------------------------------------------------------------------------------- | ---------------- |
> | Feedforward | Computational | `.editorconfig`, strict compiler flags, enforced module boundaries                                 | Always-on        |
> | Feedforward | Inferential   | `CLAUDE.md` conventions, skill prompts, architecture notes, pattern catalogs                       | Always-on        |
> | Feedback    | Computational | Linters, type checks, pre-commit hooks, ArchUnit/arch-fitness tests, mutation-score gate, CI gates | Pre-commit → CI  |
> | Feedback    | Inferential   | `/code-review` skill, `/production-readiness-review`, `/security-review`, LLM-as-judge passes      | Post-commit → CI |
>
> **Test-strength sensor — gate on mutation score, NOT line coverage.** Line coverage is a DIAGNOSTIC only: low coverage is a useful NEGATIVE signal (something is untested); high coverage is NOT evidence of quality (tests can execute lines without asserting intent) — NEVER fail a build on a line-coverage %. The real test-strength metric is **mutation score** (inject faults into changed code; surviving mutant = a missing/weak assertion = write the killing test); gate the build on it where a mutation tool exists. Add **property coverage** as a second sensor — each [HARD] §4 rule / §5 invariant guarded by ≥1 property/metamorphic test. The property tests themselves are REQUIRED for invariant-owning behaviors (`spec [mode=tests]` + `integration-test` force them, not opt-in); what is optional is only wiring property coverage as an _automated CI sensor_ on top. Keep **behavior/change-coverage** (does each behavior-changing file have a test that asserts the changed outcome) — that notion is meaningful and stays.
>
> **Three harness types:**
>
> 1. **Maintainability** — Complexity, duplication, line-coverage (diagnostic only — never a gate), style. Easiest: rich deterministic tooling.
> 2. **Architecture fitness** — Module boundaries, dependency direction, performance budgets, observability conventions.
> 3. **Behaviour** — Functional correctness. Hardest: gate on mutation score + property coverage; line coverage stays a diagnostic.
>
> **Keep quality left:** pre-commit sensors fire first (cheap), CI sensors fire second, post-review last (expensive).
>
> **Research-driven:** Never hardcode tool choices. Detect tech stack → research ecosystem → present top 2-3 options → user decides. Enforce strictest defaults; loosen only with explicit approval.
>
> **Harnessability signals:** Strong typing, explicit module boundaries, opinionated frameworks = easier to harness. Treat these as greenfield architectural choices, not just style preferences.

<!-- /SYNC:harness-setup -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any modification. Run graph trace when graph.db exists.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.
  <!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:scaffold-production-readiness:reminder -->

**IMPORTANT MUST ATTENTION** verify all 5 production-readiness foundations (code quality, error handling, loading state, Docker, integration points) before marking scaffold complete.

<!-- /SYNC:scaffold-production-readiness:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:project-reference-docs-guide:reminder -->

- **MANDATORY** Before investigating, planning, or coding, read `docs/project-config.json` (the project map: modules/paths, run-commands, conventions, architecture/workflow rules) + the required project-reference docs, and cite `Reference docs read: ...`.
- **MANDATORY** Always include `lessons.md`; project config + conventions override generic framework defaults.
- **MANDATORY** If project config, root instruction files, or any required reference doc is missing or stale, auto-run `/project-init` or the narrow lower-level route before ordinary project-specific work.

<!-- /SYNC:project-reference-docs-guide:reminder -->

<!-- SYNC:nested-task-creation:reminder -->

- **MANDATORY** Parent workflow rows do not replace child phase tracking; expand phases and link the parent when nested.
- **MANDATORY** Orchestrators pre-expand child skill phases before invocation; use `[N.M] $skill-name — phase` prefixes and one-`in_progress` discipline.

<!-- /SYNC:nested-task-creation:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Produce a copy-ready, OOP/SOLID-compliant architecture foundation — base classes, infrastructure abstractions, and quality-gate tooling — that every feature story reuses before implementation starts.

**MUST ATTENTION — Main steps (execute ALL, in order; AI keeps forgetting these):** (1) Read Plan → (2) Generate Scaffolding Checklist (Backend + Frontend/UI categories) → (3) Validate Against Plan → (4) Present to User via `AskUserQuestion` → (5) Scaffold base classes/interfaces/infra + 5 production-readiness foundations → (6) Verify (build + OOP/SOLID + Verification Gate) → invoke `/linter-setup` → `/harness-setup` → `AskUserQuestion` handoff. NEVER skip, reorder, or merge a step without explicit user approval.

**MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Nested Task Creation:** Expand child phases; link parent when nested.
- **Project Reference Docs Guide:** Read required project docs; ALWAYS include `lessons.md`.
- **Critical Thinking Mindset:** Traced proof per claim; confidence >80% to act.
- **Understand Code First:** Grep 3+ patterns, read code before modifying.
- **Scaffold Production Readiness:** Verify 5 foundations before scaffold complete.
- **Harness Setup:** Gate on mutation score; NEVER gate on line coverage.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

**MANDATORY IMPORTANT MUST ATTENTION** check Activation Guards FIRST — proceed ONLY in `workflow-greenfield-init`/`workflow-big-feature` AND when grep finds NO existing base/abstract/infrastructure scaffolding; otherwise SKIP and mark step completed — why: re-scaffolding an established project duplicates foundations and corrupts existing abstractions.
**MANDATORY IMPORTANT MUST ATTENTION** grep 3+ existing base/abstract/infra patterns (`abstract class.*Base`, `interface I\w+<`, `IRepository`, `base.*component`, DI registration) and cite `file:line` BEFORE generating any scaffolding — existing scaffolding found = SKIP — why: scaffolding over real foundations is the failure the Activation Guards exist to prevent.
**MANDATORY IMPORTANT MUST ATTENTION** BLOCK `/feature-implement` until the Verification Gate passes — all 5 production-readiness foundations verified AND both `/linter-setup` and `/harness-setup` complete — why: code shipped without quality gates is technical debt from day one.
**MANDATORY IMPORTANT MUST ATTENTION** delegate ALL sensor setup to `/linter-setup` then `/harness-setup` — NEVER hand-configure linters/formatters/pre-commit hooks in this skill — why: a checklist of installs is not a harness; the harness skills wire each control to its lifecycle stage.
**MANDATORY IMPORTANT MUST ATTENTION** enforce OOP/SOLID on EVERY base class (SRP per concern, depend on abstractions, small focused interfaces, no unused methods subclasses must override) — why: a god/concrete base class propagates its design flaw into every feature story that inherits it.
**MANDATORY IMPORTANT MUST ATTENTION** the checklists are TEMPLATES — self-investigate the chosen tech stack, adapt naming to framework conventions, skip irrelevant items, and confirm the final checklist via `AskUserQuestion` before generating code — NEVER auto-decide scope — why: scaffolding the wrong stack's idioms forces a costly rewrite before any feature lands.
**MANDATORY IMPORTANT MUST ATTENTION** evaluate fit before copying a nearby pattern — closest example ≠ matching preconditions; verify the new context shares the same base classes, scope, and lifetime — why: a foundation lifted from a mismatched context fails silently.
**MANDATORY IMPORTANT MUST ATTENTION** gate the build on mutation score, NOT a line-coverage % — line coverage is a DIAGNOSTIC only (low = useful untested signal, high ≠ quality) — why: tests can execute lines without asserting intent, so a coverage gate rewards hollow tests.
**MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` proof + confidence % for EVERY claim (>80% to act, <60% DO NOT recommend) — NEVER present a guess as fact — why: speculation without evidence is the root of hallucinated foundations.
**MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting, mark one `in_progress`, mark `completed` immediately after evidence lands, and add a final review todo — why: external task state survives context compaction; memory does not.
**MANDATORY IMPORTANT MUST ATTENTION** after scaffold, present `/feature-implement` vs `/workflow-review-changes` vs skip via `AskUserQuestion` — the user decides; do NOT skip because it "seems obvious" — why: the user owns the handoff decision.

**Anti-Rationalization (Closing — reject these excuses):**

| Excuse the model tells itself                          | Reality                                                                                               |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| "It's a new feature, just scaffold it"                 | Check Activation Guards first — wrong workflow OR existing scaffolding = SKIP and mark completed.     |
| "Already searched for base classes"                    | Show `file:line` grep evidence for all 6 guard patterns. No proof = no search.                        |
| "I'll just configure the linter inline, it's quick"    | NEVER hand-configure sensors — delegate to `/linter-setup` then `/harness-setup`. Installs ≠ harness. |
| "Coverage is high, the foundation is well-tested"      | Line coverage is a diagnostic, not a gate. Gate on mutation score; high coverage ≠ asserted intent.   |
| "The stack is obvious, skip the AskUserQuestion"       | Checklists are templates — confirm the adapted final checklist with the user before generating code.  |
| "Found a nearby base class, just copy it"              | Evaluate fit first — same base classes/scope/lifetime? Closest ≠ matching. Verify before reusing.     |
| "Scaffold's done, jump straight to /feature-implement" | BLOCKED until the Verification Gate passes — all 5 foundations + `/linter-setup` + `/harness-setup`.  |

**IMPORTANT MUST ATTENTION** check Activation Guards FIRST (SKIP if existing scaffolding or wrong workflow) · BLOCK `/feature-implement` until the Verification Gate passes · cite `file:line` + confidence >80% for every claim.

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
