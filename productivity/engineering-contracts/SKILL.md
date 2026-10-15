---
name: "engineering-contracts"
description: "HIGHEST-PRECEDENCE engineering rulebook for ALL tasks (CANONICAL — DO NOT duplicate pure engineering rules anywhere else). Formal precedence 1-18 of KISS/YAGNI/blast-radius over everything else; forces strict typing, Design by Contract, TDD/ATDD, functional-core/imperative-shell, Rust-style Result/Option, observability, conventional commits, Supabase Postgres ENABLE RLS default, agile BDD incremental delivery with SOLID, code-review optimisation (max 2 lines comment block + gh-stack multi-PR reference), agent response verbosity budget (concise by default with optional deep-dive prompts). Invoked FIRST by che-developer before any code. Respected by all che skills. Appendices: A Hard Conflict Resolution Table, B Conventional Commits types + regex + examples, C gh-stack Workflow Reference."
---

# Engineering Contracts (Highest Precedence Rules — CANONICAL)

This is the **authoritative rulebook** for every coding task in the che.
It is invoked by `che-developer` FIRST, and its rules **trump local repo conventions when they conflict** — except for Rule 3 ("repo style wins unless undefined").

> **DUPLICATION POLICY:**
> Pure engineering rules (precedence order, DbC, TDD, strong typing, security, conventional commits, RLS, agile BDD, SOLID, code review optimisation) LIVE EXCLUSIVELY HERE.
> They MUST NOT be duplicated in `CHE_RULES.md`, `user_rules`, `AGENTS.md` or any other location. Those files may only REFERENCE (link) this skill, never reproduce full bodies.
> `CHE_RULES.md` owns ONLY process/flow (worktree ask, gate order, parallelism algorithm, PRD G1-G10, gh-stack planning triggers, GitHub integration UX).
>
> When two rules seem to conflict: the rule higher in this precedence list wins.
> When this rulebook and a repo's local `AGENTS.md` conflict: **THIS rulebook wins** because it is global user policy. Local `AGENTS.md` can only ADD rules, not OVERRIDE these.

---

## PRECEDENCE ORDER (1 = highest, hard stop; 18 = lowest)

### 1. 🔴 KISS + YAGNI + BLAST RADIUS REDUCTION + NO ACCIDENTAL COMPLEXITY (above ALL other rules)

> These are not "nice to have". They are hard constraints. If any other rule on this list would force you to violate one of these — **VIOLATE THE LOWER RULE, NOT THESE.**

- **KISS (Keep It Simple, Stupid):** If there are two ways and one is simpler (less indirection, fewer files, fewer abstractions), **pick the simpler one always.**
- **YAGNI (You Ain't Gonna Need It):** Do NOT add infrastructure, abstraction, configuration, module, parameter, feature, OR extensibility point "because future use will need it." Only code what the current, explicit Acceptance Criteria DEMAND.
- **Blast radius reduction:** Change as few files and as few lines as strictly necessary. Prefer editing 1 function in 1 file to creating 3 files + a pattern. If a PR has >10 files touched → STOP and re-evaluate.
- **🔴 NO ACCIDENTAL COMPLEXITY HARD RULE (applies BEFORE writing 1st line):**
  - **Definition:** Complexity = Essential (domain-driven, unavoidable) vs Accidental (our fault — unnecessary abstraction, useless indirection, premature generic configuration, framework X just because "everyone uses it", wrapper for the sake of wrapper, etc.).
  - **Process hard stop:** Before creating ANY new abstraction / class / module / dependency / CLI flag, you must ask and answer (mentally or 1 line in decisions if task is complex):
    1. "Does this resolve ESSENTIAL complexity of the business domain / current problem?"
    2. "Can I solve the current problem WITHOUT this, using 1 simple wrapper / inline function / extra parameter in an existing function?"
    3. "If I don't do this NOW, how much work will it be to add LATER when REALLY needed? (≤3 lines → ALWAYS do it later; ≤1 day work → probably also later)"
  - **RED LIST of accidental complexity (any 1 item is reason to STOP + re-design):**
    - ✋ Interface / Protocol / Abstract class with ONLY 1 concrete implementation TODAY (if you don't have 2 implementations today, you don't need the abstraction yet)
    - ✋ Dependency Injection container / IoC for ≤5 services (build manually — 3-line factory)
    - ✋ Strategy pattern with ≤2 strategies AND the 2nd is "default that almost never changes"
    - ✋ Internal Event bus / PubSub with ≤2 subscribers (call directly)
    - ✋ Environment config / yaml / toml for ≤3 fixed flags (single env var is enough)
    - ✋ Split micro-service without proven need for independent deployment (modular monolith first)
    - ✋ Entire new framework for 1 feature (e.g. installing LangGraph just for a loop that already exists via contracts + gates)
    - ✋ N extra layers of indirection "because clean architecture says so" without any of them solving a real product problem
    - ✋ Generic function `<T>` when only 1 concrete type is being passed today

**🔴 SIMPLICITY BIAS — solution-selection order (the touchstone for planning, execution and review).**

When more than one solution can satisfy the current Acceptance Criteria, rank the candidates by this order and take the highest:

1. **Smallest first increment** — fewest files, fewest lines, fewest new dependencies/patterns (KISS + blast radius).
2. **Most reversible** — cheapest to change or undo later (thin seams, small surface, no lock-in).
3. **Most observable** — cheapest to see what it does in production (logs/metrics/health at a seam you already touch).

**Prefer (2) and (3) over upfront completeness.** Do NOT implement edge cases, error branches, generalisations or configuration that no current AC demands. Defer them **by design** and RECORD each deferral in one line (Non-Goals / decisions log) — a visible, conscious debt, never a silent omission.

**JUSTIFY-OR-DEFER:** a new abstraction, parameter, dependency, config or generalisation needs a **present concrete need** (a second real case *today*). Without it → defer. Tie-break: fewer new patterns and dependencies always wins.

> This bias outranks every rule below it (§2–§18) **except §2 Security** — never trade safety for simplicity (see Appendix A).

### 2. 🔴 SECURITY & PII COMPLIANCE (hard stop)

If you detect a security or PII leak risk:
1. **DO NOT write that code** in that form.
2. Stop and design a safer version.
3. If unsure → log to `decisions.log.jsonl` + escalate.

- Never log secrets, API keys, raw passwords, JWTs, session tokens.
- Never persist or log raw recipient email addresses or email bodies. Use hashing for correlation.
- Never log full environment variables, especially with keys/secrets.
- **Database Security default (see postgres-supabase-expert §R-01 for Postgres/Supabase specifics):** When using a database platform, security defaults MUST follow the vendor-agreed least-privilege pattern declared in the language/provider expert skill. For PostgreSQL and Supabase this defaults to Row Level Security (RLS) enabled on every new table unless a double-approval exception (Non-Goals + decisions.log user approval) is logged. For other databases (MySQL, SQLite, MongoDB, Cassandra, etc.) consult the corresponding provider expert — DO NOT hardcode Postgres-specific RLS syntax on non-Postgres databases.

### 3. 🟠 REPO EXISTING STYLE & CONVENTIONS (win unless undefined)

- If the repo has a **clear, established pattern** for something (testing framework, DI style, folder structure, naming conventions), **follow it exactly.**
- If the repo has `AGENTS.md`, `docs/`, `CONTRIBUTING.md`, `docs/architecture-decisions`, read them FIRST.
- If the codebase has **existing instances** of what you need → **REUSE / EXTEND, never create anew.**
- Only apply "default Engineering style" (Rules 4-13) when the repo is FRESH (no code yet) or genuinely ambiguous (2+ conflicting patterns with no clear majority).

### 4. 🟠 REUSE BEFORE CREATE

Before adding:
- a new **class**
- a new **module / file**
- a new **dependency** (npm/pip/cargo/go mod)

**MANDATORY check (must be answered in writing as part of task):**
1. Does a function/class/service already in the codebase that does ≥80% of this job exist? → Yes/No
2. If yes: Can I extend / wrap / parameterise it instead of creating new code? → Yes/No
3. If no: write a 1-line justification why reuse is not viable.

**New dependency threshold:** Adding a dependency requires explicit user/SM approval unless it was already listed in the TASK ENVELOPE.

### 5. 🟡 STRICT STRONG TYPING (any language)

- **No `any` / `void*` / `Variant` without explicit casting + type guard.** Prefer `unknown` in TS; prefer generics; in Rust use `dyn Trait` carefully, etc.
- Validate ALL data coming **from outside the system boundary** — DB rows, API responses, JSON parse, form inputs, env vars. Type guard + narrow to a strict type before use.
- Use type guards, `Record<K,V>`, utility types, and `satisfies` operator when they strengthen the contract without verbosity.

### 6. 🟡 DESIGN BY CONTRACT (public functions)

For every **public** (exported / module boundary) function:
- **Preconditions** (input requirements): written as runtime validation + strong type. If violated: return Error / Result::Err — never proceed with invalid input.
- **Postconditions** (output guarantees): documented via return type. If a function can fail in multiple ways → use discriminated union (not exceptions).
- **Invariants**: what must remain true (state is consistent, domain rule preserved).

### 7. 🟡 FUNCTIONAL CORE / IMPERATIVE SHELL (architecture default)

- **Core = pure functions**: business logic, rules, calculations, transformations. No IO, no side effects, deterministic.
- **Shell = imperative thin layer**: reads env, DB, files, HTTP, logger. Composes pure functions from the core; contains all the "wiring".
- If architecture is unclear for a new module: default to FC/IS unless repo has another pattern (Rule 3).

### 8. 🟡 FUNCTIONAL STYLE PREFERRED (when fits)

When the language/stack allows it AND it improves readability (Rule 1):
- **Pure functions:** no mutation, no IO, same input → same output.
- **1-2 arguments max per function.** If more needed → wrap in a single typed `options` / `input` object.
- **Return a Result value over void.** If nothing to return, return `Ok<void>` or equivalent so caller can chain.
- **Early return / flat functions:** avoid nested if / try-catch pyramids. Validate inputs FIRST → bail out. Happy path is flat.
- **`throw` only for truly unrecoverable** states. Expected error paths → use Result / Either / discriminated error types.
- **Immutable data when possible.** Prefer `.toSorted()`, `.slice().sort()`, spread `{...obj, field: new}`, over mutation.
- **Declarative data transforms: `.map() / .filter() / .reduce() / .sort() / .flatMap()`**, when readable, over for/mutable-accumulator loops.
- **Function composition** via pipes / helpers, when the language supports.

### 9. 🟢 RUST-STYLE ERROR MANAGEMENT (when applicable)

When the task needs richer error handling than a simple boolean / nullable:
- **Result type:** `Result<T, E>` or discriminated union `{ ok: true, value: T } | { ok: false, error: E }`
- **Option type:** `Option<T>` or `T | null` with explicit narrowing (not nullable + optional together)
- **Discriminated error variants:** use a tagged union for each error path so caller can match and handle specifically

Use for: service boundaries, validation functions, IO operations (DB, HTTP, file).
Don't overuse for trivial pure helpers.

### 10. 🟢 ATDD + TDD (test-first before behaviour changes)

**Behaviour change = test first.** If you are about to:
- change existing behaviour (function signature, return value, ACs)
- add new behaviour (new feature)
then **WRITE THE TEST THAT CAPTURES THE DESIRED BEHAVIOUR FIRST.**
Run it. Confirm it FAILS. Then implement. Only then the test must PASS.

Granularity:
- **Pure domain logic / pure functions:** Unit tests covering each behaviour / precondition / postcondition / invariant.
- **Public application boundary (API endpoint, server action, UI form submit):** E2E-style integration tests per acceptance criteria (Given/When/Then scenarios).
- **Follow existing repo test framework** (Rule 3). If none → ask user before adding one.

### 11. 🟢 ACCEPTANCE CRITERIA & STOP CONDITION

- Every task has defined Acceptance Criteria (ACs). If you finish the ACs → **STOP.** Do not keep polishing / refactoring / adding features "while I'm here."
- If ACs are not clearly defined → **STOP coding** and go back to Scrum Master / ask user for clarification.
- Know exactly "when am I done" before writing line 1.

### 12. 🟢 OBSERVABILITY & LOGGING (Pointer)

> **Full expanded rules (HARD RULE):** See **§19 🔴 LOGGING & OBSERVABILITY STANDARD** in this same skill (after §18 GitHub).
> This §12 is a pointer to avoid forward-reference chaos. DO NOT DUPLICATE rules here.
> Quick TL;DR from here: (1) repo pattern first, DO NOT reinvent the wheel; (2) existing observability wiring first (OTel/pino singleton); (3) 5 levels (trace/debug/info/warn/error); (4) NO raw PII; (5) bash scripts = expressive prefixed echo. Details + volume heuristic + anti-patterns in §19.

### 13. 🟢 LANGUAGE CONFIGURATION — 4 INDEPENDENT AXES (per project/session, NEVER MIX)

> **USER VERBATIM HARD RULE (contractual):** "never mix languages". Each axis below has EXACTLY 1 language configured per file/session/project. Translated UI strings = i18n artifact in separate JSON (not counted as LANG_CODE). **ALL implementation MUST maintain compatibility with Trae, Codex, Claude Code, and Cursor.**

**Configuration Precedence (HIGH → LOW):**
1. **Level 1 registry flags session override** (`che registry_append "$SESSION_ID" FLAGS "$WORKTREE_ROOT" '{"flags":{"LANG_DOCS":"pt-BR"}}'`, where `SESSION_ID="${CHE_SESSION_ID:-${HARNESS_SESSION_ID:-$SESSION_ID}}"`) — temporary, this session only.
2. **Level 1.5 project registry** `.registry/projects/<slug>/product_context.md` frontmatter `lang_code:` + `lang_docs:` — durable per project, shared across worktrees × sessions.
3. **Defaults BELOW** if neither of the above is defined.

**The 4 axes:**

| Axis | Flag | Default | What it controls — 1 language for the WHOLE axis, no mixing |
|---|---|---|---|
| **CODE** | `LANG_CODE` | `en` (MANDATORY ENGLISH default) | Identifiers: variables, classes, functions, methods, constants, file names, folder names, enum members, type names, exported symbols, i18n keys. **ONLY CHANGE if the user EXPLICITLY asks per project.** Not to be confused with translated UI strings (separate i18n JSON files). |
| **CODE DOCUMENTATION + PR/COMMITS** | `LANG_DOCS` | `en` (default) | Inline non-docstring source comments, JSDoc/TSDoc, PR titles + body, conventional commit scope + description, repo docs / ADRs / README / SPEC body + YAML. **MOST COMMON override configuration = `LANG_DOCS = pt-BR`** → comments/PR/commits/docs in PT-BR but code variables ALWAYS in EN (LANG_CODE stays `en`). |
| **CHAT WITH USER** | `LANG_CHAT` | `pt-BR` (default today) | Textual responses in chat directly with the user. |
| **STRUCTURED REPORTS** | `LANG_REPORT` | `en` (default) | Che reports: code-review, scope-checker, QA report, merge-audit, spec YAML frontmatter. |

**Legacy backward compat:** Old binary flag `LANG_PT_CHECK=ENABLED|DISABLED` is automatically migrated: `LANG_PT_CHECK=DISABLED → LANG_DOCS=pt-BR`. User DOES NOT need to perform manual migration.

**Correct examples:**
```typescript
// ✅ GOOD — LANG_CODE=en + LANG_DOCS=pt-BR (never mix)
// Calculates the cashback amount in GBP using a progressive rule per buyer tier.
function calculateLoyaltyCashback(orderTotalPence: number, tier: BuyerTier): number {
  const basePct = tier === "GOLD" ? 0.05 : tier === "SILVER" ? 0.02 : 0.01;
  return Math.floor(orderTotalPence * basePct);
}

// ❌ BAD — MIXED: PT comment but also PT variable name (violates LANG_CODE=en)
// calcula cashback...
function calculaCashbackFidelidade(valorTotalCentavos: number, nivel: NivelComprador): number {...}
```

### 14. 🔴 STORYTELLING CONVENTIONAL COMMITS (HARD RULE)

> **Purpose:** Commit messages are the **canonical historical record** of the system's evolution. A future agent or human must be able to understand the entire system, its core decisions, and the *why* behind them simply by reading the git log from start to finish.

1. **Header (Line 1):** MUST follow the **Conventional Commits** pattern (`type(scope): imperative summary`) and MUST be in **ENGLISH** by default.
2. **Body (Description):** MUST delineate the implementation from a **non-technical perspective** and MUST be in **ENGLISH** by default.
   - **Context**: What was the system's state or the problem being solved?
   - **Decision**: What was the strategic path chosen?
   - **Rationale**: WHY was this specific path chosen over others?
3. **Language Exception:** Only use Portuguese (pt-BR) if the user explicitly requests it for a specific session or project. Absent explicit mention, the git log remains an English-only historical record.
4. **No Implementation Noise:** DO NOT include technical details like "refactored class X" or "changed line 42". Focus on the **business logic and system state**.
5. **Agent Guidance:** Write the body so it serves as a map for future agents to understand the "soul" of the project.

**Example:**
```
feat(auth): implement multi-factor authentication via email

To increase security for high-value accounts, we are introducing a second layer of verification. 
Instead of relying only on passwords, the system now requires a one-time code sent to the registered email. 
We chose email over SMS for the initial rollout to avoid external telephony costs and simplify the global 
availability of the feature, prioritizing reach and zero-cost over the higher security of hardware keys.
```

---

### 15. 🔴 AGENTIC SDLC WITH SPECFLOW & SbE (HARD RULE)

> **Philosophy:** "Plan First, Act Second". We merge the **Specflow** methodology (Strategic Roadmap) with **Specification by Example** (Tactical Contract) to ensure alignment, theoretical support, and long-term navigability.

1.  **Phase 1: Intent (Vision)**:
    - **Artifact**: `intent.md` (stored in `$CHE_WORKSPACE_SHARED/projects/<slug>/`).
    - **Command**: `/che-architect` Step 1 or `/che-onboarding`.
    - **Content**: The "Why", core vision, success criteria, and non-goals. Replaces vague ideas with a structured contract of intent.
2.  **Phase 2: Roadmap (Navigation)**:
    - **Artifact**: `roadmap.md` (stored in `$CHE_WORKSPACE_SHARED/projects/<slug>/`).
    - **Command**: `/che-architect` Step 2.
    - **Content**: Decomposition of intent into high-level phases (Foundations, Core, Enhancement) with feature maps and dependencies. Serves as the "Highway" and the source of truth for task relation.
3.  **Phase 3: Tasks (Tactical Contracts)**:
    - **Artifact**: `specs/<slug>/<ts>-spec.md` (stored under `$CHE_WORKSPACE_SHARED/`).
    - **Command**: `/che-spec` and `/che-plan`.
    - **Methodology**: **SbE (Spec by Example)** using Given/When/Then.
    - **Navigability**: Every SPEC must link to a `roadmap_phase` ID from `roadmap.md`.
4.  **Phase 4: Execute (Implementation)**:
    - **Command**: `/che-act`.
    - **Collaboration**: Tasks are tagged as `[AI-Assisted]`, `[Human-Driven]`, or `[Collaborative]` to clarify the division of labour.
5.  **Phase 5: Refine (Iteration)**:
    - **Command**: `/che-ship` + feedback loop.
    - **Goal**: Adjust roadmap and intent based on implementation discoveries. Every delivery is a "learned lesson" that feeds back into the Strategic level.

---

### 16. 🔴 AGILE BDD INCREMENTAL DELIVERY WITH SOLID (NEW — HARD RULE)

> **Problem this rule fights:**
> LLMs + overly-complex PRDs → "kitchen sink" implementations anticipating 50 edge cases NOT in the AC → late delivery, overengineered, hard-to-review, fragile.

This rule turns "agility" from vague talk into enforceable checkpoints:

1. **YAGNI on steroids — think "smallest shippable increment".**
   - Deliver the MINIMUM unit of value that validates EXACTLY the current ACs.
   - DO NOT anticipate edge cases, generic abstractions, future-use parameters "because we will need this later."
   - ONLY implement what BDD behaviour (Given/When/Then scenarios) explicitly demands.
2. **BDD mindset — behaviour over structure.**
   - Deeply understand the expected behaviour (what the SYSTEM should do, for which persona, with which side-effect).
   - Always start from BDD scenarios. Code structure is a consequence of behaviour, not the other way around.
3. **Small increments = multiple PRs when useful.**
   - When scope is large (more than ~15 files, or more than ~6 independent ACs):
     - **BREAK scope into multiple self-contained PRs.**
     - **PLAN the hierarchy via `gh-stack` CLI** (Appendix C) to maintain order and links between dependent PRs.
     - Each PR must have own ACs, own tests, and pass CI individually.
     - The goal here is **to facilitate code review.** PRs ≤ 400 diff lines + 15 files = human reviewable. >800 lines = superficial review → risk.
4. **SOLID as guardrails for evolvability (NOT over-abstract).**
   - Single Responsibility: each module/function has 1 reason to change.
   - Open/Closed: open for extension (clear entry point) BUT closed for modification of what already works. DO NOT break existing behaviour.
   - Liskov: subtypes substitutable.
   - Interface Segregation: small interfaces per client.
   - Dependency Inversion: depend on abstractions (contracts), not concretes.
   - **But KISS always wins.** DO NOT create 3 interfaces just "to be SOLID" if one pure function solves it.
5. **Behaviour golden rule:**
   - NEVER break existing behaviour without an EXPLICIT AC asking for the break.
   - If you need behaviour breaking: NON-GOALS, Data Model + Migration with rollback plan, and explicit user approval.
6. **Test-suite naming = behaviour observable ONLY (Che RULE 7.9).**

   **🔴 HARD RULE — PROHIBITED EXTERNAL REFERENCES IN CODE (NEVER do this):**
   > ❌ **WRONG:** Write `// @ac 3.1 | @task T2` or put IDs in test titles.
   > ❌ **REASON:** The strategic and tactical plan (Specflow/SbE) lives OUTSIDE the codebase (in the Che Workspace). Referencing ephemeral management IDs in the source code pollutes the codebase and creates references that are impossible to validate without the harness.
   > ✅ **CORRECT:** Test titles must describe the **observable behaviour** clearly and humanely. Traceability between Code ↔ Spec is handled by the agent via `decisions.log.jsonl` and `task_graph.md` (L3), never injected into `.ts/.py/.go`.

   - **`describe("...")`** = module/feature/context UNDER TEST (domain grouping).
     ✅ `describe("POST /api/payments/refund")`
     ❌ `describe("FLO-513 T2 — process refund ACs 3.1-3.4")`
   - **`it("...")` / `test("...")`** = ONE observable behaviour, starts with verb (returns/allows/blocks/calculates/emits/saves…) + condition + expected outcome. ONE assert when possible.
     ✅ `it("returns 409 Conflict when refunding an already-refunded payment")`
     ❌ `it("Task T2.3 validates §4.2 rule if payment was already refunded")`
   - **NEVER embed internal IDs (FLO-XXX / task T\d+ / AC\d+ / SPEC-\w+ / §N) ANYWHERE in the code.** If you need traceability, the agent must consult the `decisions.log.jsonl` or `task_graph.md` at Level 3.
   - Suite organisation: group tests BY DOMAIN / CONTEXT. Nested `describe()` = more specific context (e.g. `describe("POST /refund").describe("with currency GBP")`).

### 16. 🔴 CODE REVIEW OPTIMISATION + COMMENT LINE LIMIT (NEW — HARD RULE)

> **Goal:** Write code that a senior engineer can review in 5 minutes per 150 diff lines, with near-zero back-and-forth on style/verbosity.

Rules enforced on EVERY implementation:

1. **Clean, non-verbose code.**
   - Clear names, small functions, single responsibility.
   - Dead code (commented or not) is NOT committed.
   - Log statements only where meaningful (§12). DO NOT log "got here" in every function.
2. **Max 2 consecutive lines of comment block per file.** (HARD LIMIT, with explicit exceptions)
   - **Allowed comments (count toward limit):**
     - Non-obvious trade-off explanations (e.g. `// Using linear scan here because N <= 16 always and preallocated hashmap overhead wins for hot path`).
     - TODO/FIXME flags with issue/ticket: `// TODO(FLO-789): Refactor to batch writes once the upstream API supports it.`
   - **Exceptions that DO NOT count toward the 2-line limit:**
     - Docstrings/JSDoc/TSDoc of PUBLIC functions (API boundary) — describe pre/post-conditions (§6 DbC).
     - 1-line isolated inline comments not forming a contiguous block.
   - **If you need 3+ consecutive comment lines to explain something:**
     - That is a *code smell*. The code is too complex. Refactor into smaller, clearly-named functions.
     - If still needed (e.g. workaround for a very specific library bug): **LOG an exception in `decisions.log.jsonl`, with justification.**
3. **Code review mindset — write comments as if you're the reviewer.**
   - What questions would a reviewer ask? Answer them in the function name, not in a comment.
   - Ship PR body explains WHAT and WHY, not HOW (how = code).
4. **gh-stack hierarchy for PR chains (see Appendix C).**
   - When multiple PRs: che uses gh-stack and each PR body shows "Depends on: #PR" — reviewer knows the correct order.

### 17. 🟠 DATABASE SECURITY BY DEFAULT (Provider-Agnostic Pointer)

> Moved to provider-specialised skills to avoid leaking Postgres/Supabase-specific syntax into the universal engineering rulebook.

Canonical rule location (per provider):
- **PostgreSQL / Supabase** → consult `postgres-supabase-expert` skill **§R-01 RLS Default & Policy Enforcement** (RLS enable-migration, explicit policies, RLS-specific AC acceptance criteria, lookup-table exception workflow).
- **MySQL / MariaDB** → if an expert skill exists, follow its default privilege pattern. No default = define column-level `GRANT` least privilege per role explicitly.
- **SQLite** → file-level permission model: use `PRAGMA` + application-layer authorization per the provider guidance.
- **MongoDB / Cassandra / DynamoDB / other NoSQL** → follow the corresponding expert skill (or define Non-Goals exception + log to `decisions.log.jsonl` if no expert skill exists yet).

---

### 18. 🟢 AGENT RESPONSE STYLE — Concise by Default + Deep-dive Prompt Gate

> This rule controls the verbosity and shape of agent responses to the user. It is CONTROLLED by user preference feedback. It has lower precedence than code quality rules (1–17), BUT it is higher priority than "be helpful" defaults. Violating this rule affects agent UX. THIS IS A HARD RULE to avoid reading fatigue for the user.

Canonical output:
1. **Default response budget = MAX 6–12 sentences / 250–500 words CONCISE.**
   - If you need more words to explain something, YOU ARE THINKING WRONG. Simplify. Cut edge cases. Cut examples. Focus ONLY on what the user needs to make a decision now.
   - Any answer longer than this budget → STOP. Prune. Remove everything not directly related to the user's immediate question or immediate actionable next step.

2. **FORMATTING RULES FOR DIAGONAL READABILITY (non-negotiable, applies to ALL default outputs — not just code. This is the STYLE layer on top of the verbosity budget.):**
   a. **Logical sectioning = `###` or `##` headings.** Break answers into 2-4 logical sections MAX. Each section clearly labelled. Never a single unbroken wall of text.
   b. **One bullet per line = always use `-` / `•` lists.** Almost never write 3+ consecutive sentences of body prose without a bullet break. Paragraph blocks (3+ sentences without a bullet) = code smell → refactor to bullets.
   c. **Emphasis on the most important 2-5 words.** Bold (**`**word**`**) every key noun/decision. Italics (**`_word_`**) for nuance/caveat. Underline (**`<u>word</u>`**) for the single MOST critical call-to-action or CRITICAL consequence. Maximum 1 underline per output.
   d. **1 thought per bullet.** Each bullet = ≤2 lines. If a bullet needs 3+ lines → split into sub-bullets.
   e. **Code references always formatted as links.** Use the clickable `[display_name](file:///absolute#LLx-Ly)` format (per workspace rules). Never raw file paths as plain text.
   f. **When listing tasks/changes done:** Each bullet starts with a VERB or bolded scope label (e.g. **`• 🔧 Contracts §18:` updated X + Y**). Visual scanning > grammar perfection.

3. **Four allowed sections ONLY (use exactly what's needed; omit empty sections if not applicable):**
   - ✅ **(A) 📍 Status / Exec Summary (1–2 sentences):** Exactly what is DONE / current state.
   - ✅ **(B) 🧩 Key Changes (3 bullets MAX, 1 thought each):** Most important outputs. Each = `• **Label**: <1 line detail>` format.
   - ✅ **(C) 🔗 References (optional):** Link 2–5 most important files touched, with #Lx-Ly ranges only where the section matters.
   - ✅ **(D) ❓ 1 Deep-dive Offer (only ONE topic):** "Do you want to deep-dive into **<X>**?". Never a menu.
   - ❌ NO long introductions, NO fluff, NO 8 bullets of 20 options, NO explanations of "why the tool was chosen" unless EXPLICITLY ASKED.
   - ❌ NO background context explanations unless the user has asked for it.
   - ❌ NO list of alternate options. Only offer choice. Maximum TWO choices (either A or B). If >2 → STOP, pick best guess / default, OR just do it and tell them what you chose + ask if they agree.

4. **Plans / Paths Options offering = bullet points / choices:**
   - Minimum viable plan bullets: MAX 3 steps shown first. If there are more — offer remaining ones via deep-dive.
   - Edge cases: Mention ONLY P0 / CRITICAL ones (≤2 max). Everything else → "If intermediaries arise during implementation, we'll come back here." Do NOT list all 8 edge cases upfront.
   - NO giant tables of everything that could go wrong.

5. **Deep-dive gate (the only place longform lives):**
   - WHEN user says "explain deeper" / "more details on X" → THEN you can write full explanation on THAT TOPIC ONLY. Formatting rules (sectioning, bullets, emphasis) STILL APPLY even in deep-dives.
   - Each deep-dive response respects: ONE topic per response. If user wants multiple → iterate.
   - NEVER anticipate deep-dives; they are always user-driven.

6. **User profile enforcement (default rules embody):**
   - "Highly objective, concise, and task-oriented." This + diagonal readability = this rule.
   - Violation examples NOT allowed. Always think before you write. Trim, trim, trim again.
   - If you write a draft response that: (a) has 3+ consecutive sentences without a bullet, (b) no headings, (c) no bold on key words, (d) more than 1 underline → STOP, delete half, reformat SHAPE per 2a–2f BEFORE sending.

---

### 18. 🔴 GITHUB ACCESS — gh CLI ONLY (HARD STOP. Single allowed path.)

> **Motivation:** Uniform authentication, scopes, rate-limiting, 2FA token flow, Enterprise SSO, private-repo access, audit trail, `gh auth status` single-truth. Every alternative (HTTP curl/fetch, direct `git clone`, octokit/SDK, raw PAT in Authorization header) causes leaks, wrong auth, 403s on private repos, PAT rotation fragility.

This rule applies to **every operation the che does that touches GitHub (clone, PRs, diffs, comments, reviews, checks, releases, issues, search, repo metadata, branch listing, tag listing, file content, Actions logs)**. It applies to ALL skills (code-review, scope-checker, diff-context, ship, pr-comments, ci-fix, che-git-ops, direct chat ops) and direct user requests.

**6 NON-NEGOTIABLES:**

1. **UNIQUE ENTRYPOINT.** Every GitHub access goes through the official `gh` CLI.
   - ✅ Allowed: `gh pr view <url> --json ...`, `gh pr diff <url>`, `gh pr view --json comments,reviews`, `gh pr checks`, `gh pr create`, `gh pr review`, `gh run view`, `gh release view`, `gh repo clone <owner>/<name>`, `gh issue list`, `gh api repos/<o>/<r> --jq ...` (REST wrapper with auth inherited from gh).
   - ❌ NEVER: `curl https://api.github.com/... -H "Authorization: Bearer $PAT"` or any manual HTTP variant.
   - ❌ NEVER: direct `git clone https://github.com/<o>/<r>.git` (without going through `gh repo clone`). Public HTTPS fallback NO longer exists; if gh does not log in → error + `gh auth login` instructions.
   - ❌ NEVER: octokit.js / octokit.py / PyGithub / github3.py in che script code or skill implementations. If you need an operation that `gh` doesn't have built-in → use `gh api <rest-endpoint>` (which inherits correct auth/scopes).
2. **PREFLIGHT ON EVERY OPERATION.** Before the 1st gh call in a skill/stage:
   ```bash
   command -v gh >/dev/null 2>&1 || { echo "❌ gh CLI not installed. Install: https://cli.github.com/  → then: gh auth login --scopes repo,read:org,workflow" >&2; exit 6; }
   gh auth status >/dev/null 2>&1 || { echo "❌ gh CLI not authenticated. Run: gh auth login --scopes repo,read:org,workflow  (verify with gh auth status)." >&2; exit 7; }
   ```
   Internal skills (called from within an already validated command) can skip if the caller guaranteed preflight; but when in doubt, repeating is lightweight.
3. **MINIMUM RECOMMENDED SCOPES in `gh auth login`:** `repo`, `read:org`, `workflow`. `admin:org` / `delete_repo` scopes are NOT necessary and SHOULD NOT be requested by default.
4. **PRIVATE REPOS / ENTERPRISE / SSO.** Works automatically if gh is logged into the correct org. Do not create workarounds with raw PAT in env vars.
5. **RATE LIMIT HANDLING.** If a gh command returns "API rate limit exceeded" error → DO NOT retry in a busy-loop. Warn the user with: (a) `gh api rate_limit` short output; (b) suggestion to wait or use `GH_HOST=github.<enterprise>.com` if applicable.
6. **EXCEPTIONS (ZERO by default).** The only exception allowed is if the user explicitly writes VERBATIM "ignore the gh-cli-only rule and use this PAT to call curl here". No inference.

**Common patterns — always use gh, DO NOT invent:**

| Operation | Canonical gh command (replace angled placeholders) |
|---|---|
| PR metadata + files | `gh pr view <PR_URL> --json number,title,body,state,isDraft,baseRefName,headRefName,additions,deletions,changedFiles,commits,labels,reviewDecision,mergeable,files,author,reviews` |
| PR full unified diff | `gh pr diff <PR_URL>` |
| PR diff name-only list | `gh pr diff <PR_URL> --name-only` |
| PR reviews + comments (inline + general) | `gh pr view <PR_URL> --json comments,reviews,reviewComments` (reviewComments = inline code comments) |
| Post inline review comment pinned to a line | `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments -f body='<text>' -f path='<file>' -F line=<N> -f side='RIGHT' -f commit_id="$(gh pr view <PR_NUMBER> --json headRefOid -q .headRefOid)"` (`-F` = typed field: `line` MUST be numeric; `side=RIGHT` = new side, `LEFT` = deleted line; the line MUST be inside a diff hunk) |
| Post inline reply to review thread | `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies -f body='<text>'` (there is NO `gh pr reply` subcommand) |
| Post PR-level (issue) comment | `gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments -f body='<text>'` |
| Post official PR review + approve/request-changes | `gh pr review <PR_URL> --[approve\|request-changes\|comment] --body-file <path.md>` |
| PR checks / CI status | `gh pr checks <PR_URL>` |
| Actions run view + failed logs | `gh run view <RUN_ID> --log-failed > /tmp/run-<id>.log` |
| Open DRAFT PR + self-assign | `gh pr create --draft --title "..." --body-file body.md --base main --head <branch>` then `gh pr edit <url> --add-assignee @me` |
| Default branch remote | `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name` |
| Clone repo (private or public, unique way) | `gh repo clone <owner>/<repo> <target_dir> -- --depth 1` (NO `git clone https://` fallback) |
| Release latest | `gh release view --repo <owner>/<repo> --json tagName,assets` |
| Raw REST endpoint when no built-in subcommand | `gh api repos/<o>/<r>/contents/<path> --jq .content \| base64 -d` |

---

### 19. 🔴 LOGGING & OBSERVABILITY STANDARD (HARD RULE — win over generic defaults; repo convention wins over THIS rule if repo defines)

> **Contractual USER VERBATIM request:** "every piece of code produced should have good logging practice. It should not log too much, nor too little. … understand what is happening at runtime, but without being flooded."
> This section replaces §12 (which is only a pointer). Logging anti-patterns in PR/code-review are audited in **che-code-review Category 6 (L6.x)** with severities.

#### 19.0 Hierarchical Principle — REPO FIRST (always)

```
REPO CONVENTION (if it exists and is documented in AGENTS.md / logger.ts / app.ts)
    ↓ WINS 100%
EXISTING OBSERVABILITY WIRING (OTel SDK, pino singleton, winston, structlog, sentry SDK)
    ↓ WINS if #1 is empty
THIS §19 ENGINEERING CONTRACTS STANDARD (universal fallback)
    ↓ WINS if #1 and #2 are empty
console.log / console.info / echo (most basic level, ultima ratio)
```

**What to do ALWAYS before writing your first log line:**
1. **Detect repo patterns:** `grep -r "logger\." | head -20`; check if `packages/logger/src`, `lib/logger.ts`, `logging.ts`, `app.config.ts` entries, `AGENTS.md` observability section, `utils/log.ts` exist. If they do → **follow them faithfully. DO NOT invent your own logger wrapper.**
2. **Detect OTel / tracing wiring:** look for `@opentelemetry`, `traceId`, `spanId`, `otel-sdk`, `Sentry.init()`. If OTel is present → ALWAYS propagate `traceId` / `spanId` in your structured logs.
3. **Detect PII helpers:** look for `hashPII()`, `maskEmail()`, `obfuscate()`, `PII_HASH_SECRET`. If they exist → MANDATORY USE. DO NOT log raw email/phone/JWT/secret (not even at DEBUG level).
4. **If NOTHING exists:** safe fallback. Use native `console.info/warn/error/debug` (do not create a new `my-logger.ts` file unless the task is "add logger" in SPEC).

#### 19.1 5 Log Levels — when to use EACH (NEVER use the wrong level)

| Level | When to use (strict rule) | Correct example | Expected volume |
|---|---|---|---|
| **trace** (or `silly`/`verbose`) | Internal implementation details: intermediate values, item-by-item iteration, loop steps. **NEVER in production without feature flag.** Deleted/`silent` by default in prod. | `log.trace({ itemId }, "Processing cart item 3/12")` | 100+/request (non-standard) |
| **debug** | Decisions, branching, key inputs, crossed thresholds. Useful for investigating bugs without reading code. ON in dev + staging; OFF default prod (ON only for debugging session). | `log.debug({ tier, basePct, orderTotal }, "Applying loyalty cashback rule")` | 5–25/request (max.) |
| **info** | SIGNIFICANT business events: start/end of flow (with `duration_ms`), external IO ({payment_provider}/DB/HTTP/saas call) success, state transition, auth, login/logout. You read an info log and understand WHAT happened without reading the code. **IDEAL PRODUCTION DEFAULT.** | `log.info({ paymentIntentId, customerHash, amountPence, duration_ms }, "{payment_provider} payment intent confirmed OK")` | 3–15/request/job (Golden HEURISTIC RULE) |
| **warn** | UNUSUAL but HANDLED state (not a failure). Retry 1/N, timeout on 1 attempt but retried OK, missing optional data replaced by default, deprecated API called. **Human attention deserved WITHOUT immediate blocking.** | `log.warn({ sku, fallback_price_used: true }, "Product price tier missing; using default catalog price")` | 0–2/request (unusual peaks) |
| **error** | REAL / scalable / non-recoverable failure. Always accompanied by structured context. DO NOT full stack trace dump to stdout by default (use `error.cause` or structured `stack` field). ERROR = pagerduty/alert triggered = **human action needed NOW.** | `log.error({ paymentIntentId, providerErrorCode, httpStatus: 402, correlationId }, "{payment_provider} charge declined — cannot proceed")` | 0–1/error event (very rare) |

#### 19.2 MANDATORY fields in EVERY structured log (non-negotiable)

Whenever possible (JSON/structured logger), include **EVERY APPLICABLE FIELD** below. N/A fields are omitted (do not put `null` just to fill):

| Field | When mandatory | Example |
|---|---|---|
| `op` / `event` / `msg` | ALWAYS (1st field, human-readable operation name) | `op: "{payment_provider}.refund.create"` |
| `traceId` / `spanId` | ALWAYS if OTel or tracing exists in the repo | `traceId: "4bf92f3577b34da6a3ce929d0e0e4736"` |
| `correlationId` / `idempotencyKey` | External / financial / retry operations | `idempotencyKey: "refund_${orderId}_${attempt}"` |
| `userId` / `orgId` / `customerId` | Any authenticated context (use HASH if PII) | `customerHash: hashPII(email)` |
| `duration_ms` | Start/end timing, external IO | `duration_ms: 142` |
| `error` / `err_code` / `httpStatus` | ONLY ERROR/WARN | `err_code: "card_declined"` |
| `path` / `file` / `line` | Localisable failures | `path: "src/refund/service.ts:142"` |

DO NOT use concatenated string `logger.info("Done processing " + orderId + " customer " + email)`. ALWAYS structured object first, human message second:
```typescript
// ✅ GOOD — structured, correlation, no raw PII
logger.info({ op: "refund.completed", refundId, orderId, customerHash: hashPII(email), duration_ms }, "Refund processed OK")
// ❌ BAD — loose text, raw PII, no correlation
logger.info(`Refund completed, refundId=${refundId} customerEmail=${email}`)
```

#### 19.3 Bash scripts / Makefile / GitHub Actions `run:` blocks / CLI commands — EXPRESSIVE LOGS ARE MANDATORY

> **USER VERBATIM:** "Mainly in scripts and workflows, expressive logs are fundamental. Add 'echo' whenever it makes sense."

**NON-NEGOTIABLE scripts rule:**
1. **Mandatory prefix per level:** `[INFO]` / `[WARN]` / `[ERROR]` / `[STEP 1/5]` (numbered pipeline is gold). Do not rely solely on `set -x` (super flooded debug, useful only for debugging).
2. **Every step with external IO (clone, download, backup, apply, migrate, deploy, curl HTTP)** = echo **START** + echo **END (OK/failed)**. Humans read `[INFO] Fetching gh CLI repo (laionazeredo/che-ai)...` and know what is happening WITHOUT looking at code.
3. **Branching / conditionals:** if it fell into a fallback, if it used A or B, warn `[WARN] gh not detected in PATH, fallback skipped (error expected) → exit 6`.
4. **DO NOT flood with global `set -x` always on.** Use `set -x` ONLY in small, specific debugging blocks. Turn off afterward.
5. **Error = always different exit code:** `echo "[ERROR] ..." >&2; exit N`. Use fd 2 for stderr.

GOLDEN STANDARD script example (che self-update header style):
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "[STEP 1/4] Preflight: verify authenticated gh CLI..."
if ! command -v gh >/dev/null 2>&1; then
  echo "[ERROR] gh CLI not installed. Run: (brew|apt|dnf|winget) install gh" >&2
  exit 6
fi
echo "[INFO] gh detected OK, $(gh --version | head -1). [OK 1/4]"

echo "[STEP 2/4] Fetch repo laionazeredo/che-ai via gh repo clone..."
gh repo clone laionazeredo/che-ai /tmp/src -- --depth 1 --quiet || {
  echo "[ERROR] gh clone failed. Diagnosis: gh auth status; gh repo view laionazeredo/che-ai" >&2
  exit 8
}
echo "[INFO] Fetch OK (depth 1). [OK 2/4]"
```

#### 19.4 Log Volume — GOLDEN HEURISTIC RULE (no flood, no lack)

> **USER VERBATIM:** "without flooding. The idea is to bring clarity in a debugging situation and understand the execution flow."

| Scenario | TOTAL expected log range (info+warn+error+debug if on) | Outside range = problem |
|---|---|---|
| HTTP API endpoint handler / tRPC procedure | 3–15 info/warn/error lines + 5–25 debug if on | >25 info = likely flood, <3 = lack |
| Bash script / CLI command | 1 line per STEP (number) + 1 start line + 1 OK/failed end line (≈5–20 total) | No expressive echo = unreadable |
| Long-running ETL / batch job | 1 info log per batch of 100 items, NOT 1 log per item inside loop | 1 log / item = 100k logs = SIEM flood |
| Hot path (<1ms per operation, 10k+/s) | ZERO info/debug inside hot loop. MAXIMUM 1 START + 1 END log with aggregates (count, duration_ms). | Any individual log inside hot loop = 20–80% performance degradation. |
| Deploy / CI pipeline | 1 echo per stage (build/lint/typecheck/test/deploy). | Nothing = don't know where it stalled; everything = 500 useless lines. |

**Anti-flood CHECKLIST — check BEFORE committing new code:**
- [ ] Inside `for/while/map/forEach` with N>100 items → removed info/debug logging EVERY iteration?
- [ ] Request/response payload > 2KB → truncated instead of full dump? `JSON.stringify(body).slice(0,500)+"...[truncated]"`
- [ ] DEBUG level → only in places really useful for debugging? Did not use debug as "goto printf"?
- [ ] Retry loop with N attempts → 1 warn with `{attempt: 2/3, backoff_ms: 200}` per retry, NOT 1 log per millisecond busy wait?
- [ ] Giant object / full DB row → log ONLY the fields that matter for the flow (ids, timestamps, status). DO NOT log the whole row.

#### 19.5 PII / Secrets — ABSOLUTE PROHIBITION (not even DEBUG, not even TRACE)

- DO NOT log JWTs, API keys, Stripe sk_live / sk_test, Supabase service_role, passwords (even insecurely hashed).
- DO NOT log raw email / phone / address / CPF. Use `hashPII(email)` / `maskPhone("+44...")` if available. If no helper → OMIT the field.
- DO NOT log raw cookie sessions, raw Authorization headers, refresh tokens.
- Warning in code-review Category 6 L6.1 = **HIGH severity by default (CRITICAL if field is super sensitive: Stripe key, password).**

#### 19.6 Error Handling — DO NOT leave `catch` empty, DO NOT swallow errors

Whenever you write `try { ... } catch`:
```typescript
// ✅ GOOD — 3 properties in catch: (1) operation context, (2) identifier, (3) struct error fields
try {
  await paymentProvider.refunds.create({...})
} catch (err) {
  // Here: op + id fields + err.code + err.message (don't need full stack dump by default)
  logger.error({ op: "{payment_provider}.refund.create", paymentIntentId, err_code: (err as any)?.code, err_msg: (err as any)?.message }, "Refund {payment_provider} API call failed")
  // re-throw if this is not handled: throw err
}

// ❌ BAD — 3 classic anti-patterns
try { ... } catch { /* NOTHING. SILENCED ERROR = HIDDEN RUNTIME BUG */ }
try { ... } catch(e) { console.log(e) /* structured? context? */ }
try { ... } catch(e) { throw new Error("failed") /* LOST stack and root cause */ }
```

---

### 20. 🔴 WORKTREE SESSION BINDING — Specflow & Tactical Clarity.

> **Hierarchy (flat, Sep 2026):**
> 1. **State Level**: `~/.che-workspaces/.state/registry.jsonl` (session → worktree → project bindings).
> 2. **Project Level (Strategic)**: `~/.che-workspaces/<project-slug>/` (Intent, Roadmap, Durable Memory). Identified by an explicit slug; binds **no** path.
> 3. **Worktree Level (Tactical)**: `<project>/worktrees/<worktree-name>/` (Shared history, Specs, Graph, Designs). The **only** level that binds a repository path, and it requires git.
> 4. **Session Level (Ephemeral)**: `<project>/.sessions/<session_id>/` (Execution logs, Debug state) — deliberately outside the worktree folder so the worktree stays reusable.
>
> The L1 "workspace" grouping level was retired: projects live directly under the storage root.

#### 20.1 Path Contract — One Worktree = One Base of Truth.

- **Durable Assets**: `intent.md`, `roadmap.md`, and `architecture.md` live at the Project level (L2).
- **Tactical Assets**: `task_graph.md`, `decisions.log.jsonl`, and the SPEC (`specs/<slug>/<ts>-spec.md`) live at the Worktree level (L3).
- **Shared History**: Multiple sessions working on the same worktree MUST read from the same L3 tactical assets to ensure consistency.
- **Session Isolation**: Only execution logs and isolated debugger state live in the L4 session folder.

#### 20.2 Scissor Check & Safety.
- Every write operation MUST be validated against the Level 1 registry to ensure it stays outside the user's source code (unless explicitly requested).
- **Generated Assets**: Never committed to the user's repository. Always stored in the hierarchy above.
- **Doubt = Ask**: If the worktree binding is ambiguous, the agent must ask the user before proceeding.

---

### 21. 🔴 EXTERNAL CONNECTORS ONLY OFFICIAL CLI/MCP (Generalisation of §18 GitHub for ALL external integrations. HARD STOP.)

> This rule generalises §18 GITHUB ACCESS gh-only to EVERY external SaaS / self-hosted tool integration. It applies to: Figma, PenPot, Linear, ClickUp, Jira, Sentry, Grafana, Datadog, Stripe, Resend, Supabase, Railway, Vercel, Lighthouse CI, axe-core, SEO tools, social media scheduling, Google Search Console, GA4, GTM, Meta Pixel, etc. If the integration lives outside the user's runtime — this rule applies.
>
> **Higher precedence than "it's faster to write 5 lines of fetch". Lower precedence only than Safety §2, DbC §6, Worktree binding §20.** Violation = CRITICAL issue in §0.9.2 CODE-REVIEW. Do not suppress.

#### 21.1 ALLOWED CHANNEL (2 channels, FIXED PRECEDENCE ORDER)

**Always use the highest available channel in this order. Skipping a channel = violation.**

| Priority | Channel | Description / Examples |
|---|---|---|
| **P1 (ALWAYS FIRST IF IT EXISTS)** | **Official MCP (Model Context Protocol)** | MCP Server officially maintained by the vendor OR community-recognised maintainer (>= 500 stars or verified badge). Examples: `mcp_open-pencil` official Figma, `penpot-mcp` official, `mcp_flockr-linear`, `mcp_laion-railway`, `mcp_Playwright`, `mcp_Sequential_Thinking`, `integrated_browser` (non-curl browser MCP). |
| **P2 (FALLBACK IF P1 DOES NOT EXIST)** | **Official CLI (vendor or community-maintained ≥1000 downloads/week npm/pip/cargo)** | Installed via standard package manager (corepack pnpm / pipx / cargo). Authentication same as `gh auth login` — interactive CLI flow OR browser OAuth flow, token saved in `$XDG_CONFIG_HOME/<vendor>/credentials.json` (NEVER commit). Examples: `gh` (GitHub §18), `figma-cli`, `@axe-core/cli` (Deque), `@lhci/cli` (Lighthouse), `sentry-cli` (Sentry), `grafana-cli`, `datadog-ci`, `jira-cli` (Atlassian), `clickup-cli`, `linear-cli`. |

#### 21.2 ABSOLUTE PROHIBITED CHANNELS (HARD FAIL if used)

1. ❌ **`curl` / `wget` / manual raw HTTP request.** Anything that is inline `fetch()` in the agent, `axios.get()` without wrapper, loose Python `requests.get()`. UNIQUE exception: if an official P2 CLI wrapper already exists that INTERNALLY does HTTP and we only call the CLI (which manages auth, retries, rate limit). We NEVER write HTTP.
2. ❌ **Direct SDK without official CLI wrapper.** Example: direct `@linear/sdk` npm SDK call. Only accepted if a P2 `linear-cli` exists that uses the same SDK internally and we call the CLI.
3. ❌ **Hardcoded inline PAT / API Key in code or in committed `.env`.** Every API key stays in: (a) `credentials.json` XDG_CONFIG (CLI) OR (b) encrypted runtime Secret Manager (Vercel Env Crypt / Railway Variables / GitHub Encrypted Secrets). NEVER committed plain text.
4. ❌ **Third-party SaaS intermediary ("proxy").** No Zapier / Make.com / n8n as extra layer agent → vendor. Direct call agent → official MCP or agent → official CLI. Zero extra layers.
5. ❌ **"I'll write a quick HTTP client because it's only 1 endpoint."** Do not write. Use P1 or P2. If P1/P2 does not exist today → consider the integration DOES NOT EXIST. Do not implement. If it's really that important → open an issue with the vendor for official MCP, or wait for phase 2.

#### 21.3 Authentication (same as §18 gh CLI pattern)

1. OAuth flow browser-first ALWAYS whenever possible. NEVER copy-paste PAT from vendor page.
2. Tokens saved locally in `$HOME/.config/<vendor>/credentials.json` (0600 permissions). NEVER `$HOME/.env`.
3. CI / remote runtime: **only** platform `Secrets Manager`. E.g.: Vercel Env Crypt, encrypted Railway Variables, GitHub Actions Encrypted Secrets (not plain text in workflow YAML).
4. Audit trail: `[STEP N/M] Authenticated <vendor> via CLI (scope: <read/write>). User ID: <hash-email> (PII hash NOT raw email).` §19 standard log. NEVER log the literal token. NEVER log response body if it contains user data.

#### 21.4 Retry + Rate Limit (same as §18 gh CLI pattern)

1. **NEVER blind retry while true loop.** Always bounded 3 attempts with exponential backoff (1s → 2s → 4s).
2. If 429 Too Many Requests / rate limit: **wait for Retry-After header if provided, otherwise 60s minimum.** Do not busy wait. Log entry `[RATE-LIMIT-SLEEP] vendor=X duration_s=Y reason="..."` in decisions.log.
3. Any vendor 5xx error = bounded retry. Any 4xx error (except 429) = **immediate failure, no retry.** Unless it's 401 expired token and the CLI has a `refresh` command.

#### 21.5 Concrete Mapping Table Example (7-category Domains)

| 7-slug Domain | Integration | P1 Official MCP (use first) | P2 Official CLI (fallback) |
|---|---|---|---|
| `engineering` | GitHub | ✅ official `mcp_github` MCP + `gh` CLI | `gh` CLI npm-corepack (standard §18) |
| `ux` | Figma | ✅ `mcp_open-pencil` (Figma Dev Mode) | `figma-cli` npm |
| `ux` | Open-source PenPot | ✅ official `@penpot/mcp` (Penpot monorepo; the `penpot/penpot-mcp` repo is archived) | N/A (P1 exists) |
| `ux` | Axe-core WCAG 2.2 AA | `axe-core-mcp` MCP (if available) | official Deque `@axe-core/cli` npm |
| `product` | Linear | ✅ `mcp_flockr-linear` MCP | `linear-cli` npm |
| `product` | ClickUp | ✅ `mcp_laion-clickup` MCP | `clickup-cli` npm |
| `product` | Jira | Atlassian MCP (if available) | Atlassian `jira-cli` npm |
| `devops` | Sentry | Check `sentry-mcp` | official `sentry-cli` pipx |
| `devops` | Grafana | Check `grafana-mcp` | official `grafana-cli` |
| `devops` | Datadog | Check `datadog-mcp` | official `datadog-ci` npm |
| `seo-analytics` | Lighthouse CI | lighthouse MCP (if any) | official `@lhci/cli` npm |
| `seo-analytics` | GA4 / GSC | official Google MCP (if any) | NONE (if no P1/P2 → NO integration today. Wait for phase 2 vendor release.) |
| `social` / `copywriting` | (future phase 2) | To be defined by domain, always P1/P2 | Same rule |

> **If both P1 and P2 cells for an integration are EMPTY = DO NOT IMPLEMENT THE INTEGRATION TODAY.** Do not invent. Do not use raw curl. Open an issue with the vendor for official MCP or official CLI. Come back when P1 or P2 is available. KISS + YAGNI §1 wins always.

---

### 22. 🔴 MANDATORY DOCUMENTATION — Relevance Check + Docstrings/JSDoc Clean Code (HARD RULE. Application failure = HIGH issue §0.9.2 CODE-REVIEW.)

> **User VERBATIM Rule (canonical source of truth):** Every feature, change, or addition should trigger a self-question: "does this change deserve a documentation update?" — and the answer should be applied. Furthermore, public code must have in-code documentation (docstrings/JSDoc/TSDoc) following the Clean Code rule: without exaggeration, documenting purpose, intricate parts, and difficult types.

#### 22.1 Pillar 1 — Docs for Humans + Agents + Runbooks (Always ask about relevance)

**Before declaring a task as DONE, you MANDATORILY must answer these 2 questions mentally or in writing (if ambiguous):**

1. **(Contract Question)** Does this change alter: public contract, new or changed CLI commands, UX/UI visible to the end user, onboarding of new devs/agents, architectural premises, deploy/runbook flows, or public APIs? If YES → docs are mandatory.
2. **(Longevity Question)** Would a human or agent trying to understand this code 3 months from now benefit from a line or paragraph explaining this change? If the answer is "maybe" or "yes" → docs are mandatory.

**3 Mandatory Destinations where to apply (heuristic mapping):**

| Change Type | Docs for HUMANS (Mandatory if applicable) | Docs for AGENTS (Mandatory if applicable) | Runbooks (Mandatory if applicable) |
|---|---|---|---|
| New feature, new command, new skill, new architecture rule | Repo/package `README.md`, `docs/*.md` if any, changelog | `AGENTS.md` (repo or package), `CLAUDE.md`, `CURSOR.md`, `skills/*/SKILL.md` (L3 Che), `CHE_RULES.md` / `CHE_COMMANDS.md` (L2 routers if cross-cutting) | N/A unless it alters deploy |
| Change in deploy flow, CI, DB migration, onboarding, incident response | `docs/runbook-*.md`, `docs/operations.md` if any | infra/CI section of `AGENTS.md` | `runbook-onboarding.md`, `runbook-deploy.md`, `runbook-incident.md` |
| New env var, new runtime configuration | env vars section of `README.md`, `.env.example` comments | `packages/config/AGENTS.md`, `CHE_RULES.md` if transversal | `runbook-env-setup.md` if any |
| Internal refactoring WITHOUT public contract change | Optional (internal changelog if large) | Optional (decision log entry if trade-off) | N/A |

**If you decide NOT to update docs and the change is > 5 files OR > 150 diff lines:** justify with 1 line in `decisions.log.jsonl` (`skip_docs_reason` field). This is for future auditing.

#### 22.2 Pillar 2 — Docstrings / JSDoc / TSDoc / Rust Doc / Go Docstrings in Code (Clean Code Rule)

> **§3 REPO STYLE WINS:** If the project already defines an official docstring pattern (e.g. NumPy/Sphinx for Python, Google style, TSDoc, GoDoc, Rust doc comments) → USE THE REPO PATTERN. This rule is the FALLBACK if the project does NOT define a pattern.

**WHAT to document (mandatory if present):**
1. **Purpose of public functions / public methods / public classes / modules.** Explain "why it exists" and "what it does at a high level" — do not repeat the function name.
2. **Intricate parts, non-obvious workarounds, implicit contracts, specific orderings, global state dependencies, or hidden context.** If a colleague would look and say "why on earth is this written this way?", you must document with 1-3 lines of comment (or line within the docstring).
3. **Difficult to understand custom types:** enums with bitwise flags, tagged unions without self-explanatory names, opaque aliases, nested generic types, bitmask constants.

**WHAT NOT to document (avoid noise):**
1. **Inputs and outputs if there IS strong typing.** TypeScript, Python with type hints, Rust, Go, Java — typing already documents the type. Do not write `@param {string} userId The user ID` if `userId: string` already exists. Exception: if the parameter has non-obvious semantics despite the type (e.g. `userId: string` but must be UUID v4 formatted, or GBP in integer pence, or UK timezone).
2. **Trivial logic.** If the function body has 2 obvious lines and the name already explains everything, the docstring can be omitted for internal private functions.
3. **Literal repetition of the function name.** `def calculate_total(): """Calculates the total."""` → prohibited. Replace with purpose if necessary or remove.

**Relation to §16 CODE REVIEW (max 2 lines comment block):**
- Docstrings/JSDoc/TSDoc/doc comments of PUBLIC FUNCTIONS and PUBLIC CLASSES DO NOT count toward the 2-line limit of §16. This was already an implicit exception in §16 L248-250; now officialised.
- Inline comments of intricate parts count toward the §16 limit → keep them short (≤2 lines) or move the explanation to the function's public docstring (which does not count toward the limit).

#### 22.3 Pillar 3 — Context of when to apply and validation

**Canonical Validation:** The `che-scope-checker CHECK 3` gate (updated docs) runs automatically in `/che-ship` and PR reviews, and now explicitly includes:
- Check item: "Relevance check questions 22.1 applied and answered"
- Check item: "New public functions/methods/classes have purpose docstring + intricate observations"

---

## Appendix A — Hard Conflict Resolution Table (CANONICAL)

If you face a trade-off where two rules seem to pull opposite directions:

| Conflict | Winner | Rationale |
|---|---|---|
| KISS (§1) vs Functional Composition (§8) | KISS | Reduce complexity even if a "beautiful" composition is possible. |
| YAGNI (§1) vs Extensibility pattern (§8) | YAGNI | Don't build extension hooks today just because. |
| New abstraction vs Reuse (§3 + §4) | Reuse | Wrap/extend existing; only new abstraction as last resort. |
| DbC strictness (§6) vs KISS (§1) on a tiny 5-line internal helper | KISS | DbC is mandatory ONLY at public boundaries. Internal tiny helpers can be relaxed — but never safety. |
| Pure function (§8) vs performance — hot loop needs mutation | Performance + decision.log entry | Mutability OK inside the core if measured faster. Log the trade-off. |
| TDD (§10) vs tiny bugfix of obvious typo | Either — but verify test exists or add one. | For 1-char typo fix: fine to patch, but ensure afterward a regression test exists for that path. |
| Security (§2) vs KISS | Security | Never trade security for simplicity. Simplify in a SAFER way. |
| Conventional Commits (§14) vs repo uses different commit format | Repo format (§3) | §3 says repo convention wins when defined. §14 is the DEFAULT when no convention exists. |
| Agile BDD smallest increment (§15) vs "I can add this extra nice-to-have in 2 lines" | BDD smallest (§15 = YAGNI in action) | DO NOT add. Nice-to-have = separate PR. Scope = scope. |
| Code Review Opt max 2 lines comment (§16) vs trade-off explanation | May do 3+ LINES ONLY with logged exception in decision.log | No log = violation. Usually a more clearly-named function is enough. |
| Supabase RLS default (§17) vs "table is tiny, public enum only" | RLS default (§17). Skip ONLY with TWO approvals: Non-Goals + decision.log user approval. | See §17 exceptions. |
| Worktree §19 binding vs "worktree B seems to have the code I want so let me just touch it" | §19 wins. ASK before switching. Never silent cross-worktree file ops. | AskUserQuestion. User confirms → §19.3 re-binding steps. |
| §21 External Connectors ONLY P1/P2 official vs "just 1 endpoint, I'll write 5 lines quick fetch" | §21 wins ABSOLUTELY. NEVER raw HTTP. If no MCP/CLI today → DO NOT integrate. Wait or open vendor issue. | If real life-or-death case → user VERBATIM EXPLICIT_OVERRIDE logged in decisions.log with detailed justification + expiry date to migrate to P1/P2. |

---

## Appendix B — Conventional Commits: Types + Regex + Examples (CANONICAL)

> This is the DEFAULT convention. If the repo defines another (Rule 3), REPO WINS.

### B.1 Syntax regex (strict)
```regex
/^(feat|fix|docs|style|refactor|test|chore|perf|build|ci|revert)(\([a-z0-9._-]+\))?: [a-z0-9][A-Za-z0-9 _.,'"()\/:@#=-]{0,88}$/
```
Rules:
- type: lowercase, one of the 11 below.
- scope: optional, lowercase with allowed separators `._-`, between parens.
- colon + space after type/scope.
- description: imperative, starts lowercase, max 88 characters (keep under 100 for terminal wrap). Max total line ≤ 100 chars.

### B.2 Types (11) + when to use each
| Type | Semantic version | When to use |
|---|---|---|
| `feat` | minor (x.y.z → x.Y.0) | New feature for the user. Shipped behaviour change ACs. |
| `fix` | patch (x.y.z → x.y.Z) | Bug fix for the user. Ex.: checkout double-click duplicate order, 500 on null. |
| `docs` | - | Documentation only changes: README, docs/, inline docstrings public APIs (docstring-only commits with no code change). |
| `style` | - | White-space, formatting (Biome/Prettier apply), missing semi-colons, quoting style change. NO code behaviour change. |
| `refactor` | - | Code change that NEITHER fixes a bug NOR adds a feature. Rename, extract fn, simplify, dead-code-remove. Behaviour preserved. |
| `test` | - | Adding missing tests or correcting existing tests. |
| `chore` | - | Updating grunt tasks etc; no production code change. Dependency bumps (lockfile) without behaviour change, tooling config, CI scripts (if trivial; complex CI = `ci`). |
| `perf` | patch | Code change that improves performance (ex: hot path cache, O(n²)→O(n)). |
| `build` | - | Changes that affect the build system or external dependencies (ex: Vite/tsconfig major change, Webpack config, Dockerfile build stage). |
| `ci` | - | Changes to CI configuration files and scripts (ex: GitHub Actions, CircleCI config YAML, Nx workspace target changes). |
| `revert` | - | Reverts a previous commit. Convention: `revert: feat(payments): add apple pay` then in the body the commit hash being reverted. |

### B.3 Examples
```
feat(auth): add password hashing with argon2id
fix(checkout): prevent duplicate orders on retry (double click 500ms)
test(user): cover register endpoint with malformed email edge cases
perf(dashboard): cache organiser event list for 60s
refactor(checkout): extract tax calculation pure fn
build: upgrade next.js 15 → 16
ci: add typecheck step to platform nx job
docs: add architecture decision 7 — idempotency keys
chore(deps): bump stripe-sdk 18.4 → 18.5 (patch)
```

---

## Appendix C — gh-stack Workflow Reference (CANONICAL — new)

### C.1 What is `gh-stack`
`gh-stack` (https://github.com/github/gh-stack) = official gh CLI extension that:
1. Creates a chain/stack of DRAFT PRs each depending on the previous one (base branch hierarchy).
2. Updates PR bodies with "Depends on: #123 · Stacks against main" links so reviewers understand order.
3. Supports rebasing the whole stack when lower PRs get fixes.

### C.2 Preconditions to use gh-stack (che-act validates in planning)
1. Task Graph ≥ 3 tasks OR one task > 15 files blast radius.
2. Tasks can be semantically grouped into "PR layers" (ex: PR1=types/contracts, PR2=service layer + unit tests, PR3=API + e2e tests).
3. User did NOT explicitly say "single PR please".
4. Worktree is clean of uncommitted changes OUTSIDE the envelope (standard check).

### C.3 Stack planning (Scrum Master step — gh_stack_plan.md structure)
```
# GH STACK PLAN — <slug>
Status: DRAFT (approved by user: YYYY-MM-DD HH:MM)

| Order | PR# (placeholder) | Title conventional commit | Base branch | Head branch | Tasks/ACs covered | Approx files |
|---|---|---|---|---|---|---|
| 1 (bottom) | — | feat(contracts): add refund data model + enums | main | feat/refund-contracts | T1 (contracts), AC-1/2/3 | ≤6 |
| 2 | — | feat(payments): implement refund service with Stripe API | feat/refund-contracts | feat/refund-service | T2/T3 (service + unit tests), AC-4–9 | ≤14 |
| 3 (top) | — | feat(admin): refund dashboard UI + tRPC routes | feat/refund-service | feat/refund-admin-ui | T4 (UI), AC-10–13, smoke | ≤12 |

Notes:
- If PR2 needs a fix after review: fix on feat/refund-service, then `gh-stack rebase` auto-rebases PR3 on top of the new PR2 head.
- After PR1 merged to main: `gh-stack update` rebases PR2→main, PR3→new PR2.
```

### C.4 Standard gh-stack commands (che-ship reference)
```bash
# Install (1x per machine)
gh extension install github/gh-stack

# Create full stack after all local branches created + commits
gh-stack create --draft  # opens ALL PRs as DRAFT with dependency links in body

# Update stack after commit on a middle branch (rebase everything)
gh-stack rebase

# Check stack status
gh-stack status

# After PR1 merged → rebase remaining stack on main
gh-stack update --base main
```

### C.5 Che rules enforced on gh-stack
- Stack ALWAYS starts DRAFT. Single "ready for review" = user explicitly asks.
- Each individual PR passes CI individually (QA + light compliance per PR).
- If any PR in the stack has blast radius > 20 files → SM goes back to planning and re-breaks it.
- Body of each non-base PR MUST open with `Depends on: #<previous-pr-number>` (gh-stack does this automatically, but che validates).

---

## Appendix D — A Philosophy of Software Design (John Ousterhout — CANONICAL Quick-Ref)

> **Original source:** John Ousterhout, _A Philosophy of Software Design_, 2nd Ed. (2018, 2021).
> **Che integration map:**
> - **§1 No Accidental Complexity (hard rule above)** = foundation of first 3 chapters (complexity is greatest risk).
> - **che-scope-checker CHECK 5 (LEAN/YAGNI scanner)** = reads 13 RED FLAGS below + assigns Lean findings (with AC justification if needed).
> - **che-code-review (gate 0.9.2 in ship)** = each finding below that appears in the diff gains severity: **HIGH** (4 bold items below, break deep modules), **MEDIUM** (remaining 9).
> - **che-spec before writing code** = "Before You Code" checklist below mandatory if task ≥ 8 files.
> - **che-ship gate 0.9.2 before committing** = "Before You Commit" checklist below mandatory.

### D.1 13 COMPLEXITY RED FLAGS (any 1 = warning; 2+ in the same module = refactor before PR)

| # | Red flag | What it is | Severity in code-review |
|---|---|---|---|
| RF01 | **Shallow Module** | Large / complex `public` interface that delivers little useful functionality. E.g.: class with 12 public methods that just does simple CRUD on a table. | **HIGH** |
| RF02 | **Information Leakage** | Internal detail of a module appears OUTSIDE it. E.g.: consumers of `OrderService` have to know `order.discounts[0].raw_percent` instead of `order.totalAfterDiscounts()`. | **HIGH** |
| RF03 | **Pass-Through Method** | Method that does nothing except call another method with the same parameters (zero added value). Sign of a shallow layer. | **HIGH** |
| RF04 | **Overexposure / Temporal Decomposition** | Abstraction split by "time step-by-step" instead of by knowledge. E.g.: `OrderStep1Create`, `OrderStep2ValidateAddress`, `OrderStep3Charge` in separate classes (only the correct calling order exists — they are not independent modules). | **HIGH** |
| RF05 | **Repetition** | True duplication: same logic ≥ 3 places with ≥ 5 similar lines. Do not confuse with "accidentally similar" (those can stay). | MEDIUM |
| RF06 | **Special-General Mixture** | General code (e.g. `httpClient` helper) contains special case branches (`if url == "/checkout/payment"`) that only exist for 1 consumer. | MEDIUM |
| RF07 | **Conjoined Methods** | Two methods that are ALWAYS called together in the same order. If A always comes after B, they belong to the same method / same module. | MEDIUM |
| RF08 | **Comment Repeats Code** | Line comment `// increment counter` followed by `counter++`. If the comment just translates the code, delete it. | MEDIUM |
| RF09 | **Implementation Documentation Interface Doc** | Public function docstring talks about internal details ("calls Stripe API v1 with 30-char idempotency key") instead of the CONTRACT ("given PaymentIntent id, returns status + authorised amount"). | MEDIUM |
| RF10 | **Too Obscure / Hard to Guess** | Function or parameter name that you don't know what it does WITHOUT reading the body. E.g.: `process(obj, flag)` (flag = boolean 0/1, without enum). | MEDIUM |
| RF11 | **Hard to Extend** | To add 1 new valid case (e.g. new payment method, new status) you have to edit ≥ 4 different files and remember all places. | MEDIUM |
| RF12 | **Choice not Restriction** | API has 12 optional parameters and the consumer has to know the correct combination. Good modules RESTRICT the caller's choice space. | MEDIUM |
| RF13 | **Obvious / Easy gotcha** | Normal correct use of the module, but 1 default case if you forget → subtle bug (e.g. `client.send(data)` — if caller doesn't call `client.init()` once before → silently fails in production, no warning in dev). | MEDIUM |

### D.2 15 DESIGN PRINCIPLES FROM THE BOOK (apply in order)

1. **Complexity is the Greatest Enemy.** Greatest risk in software = complexity, not isolated bugs. Complexity grows exponentially with size.
2. **Make Deep Modules.** The best module = **small simple public interface** that delivers **large amount of functionality / hides A LOT of complexity.** Good ≠ small. Good = low ratio (interface / functionality).
3. **Abstraction = Eliminate Everything Obvious + Preserve Everything Important.** When you abstract, you remove everything that is obvious (caller doesn't need to know) and leave visible only what is ESSENTIAL to use it well.
4. **Modules Should be Deep, not Shallow.** Shallow = many files, little complexity reduction. Deep = fewer files, each removes much pain from the rest of the system.
5. **Information Hiding + Information Leakage are opposites.** Hiding = internal detail exists in only 1 place and no one knows. Leakage = internal detail appears in ≥ 2 places (any change is now multiple).
6. **General-Purpose modules are deeper than Special-Purpose ones.** When in doubt between making a "generic module with special case in 1 place" vs "specialised", choose generic (greater depth in the long run).
7. **Different Layer, Different Abstraction.** Layers should have DIFFERENT ABSTRACTIONS. If HTTP layer repeats exactly the same fields/parameters as Service layer → it's pass-through → shallow → throw it away.
8. **Pull Complexity Downwards.** Whenever possible, move complexity INSIDE the module (below) and leave the interface (above) simpler. DO NOT make the caller handle module special cases.
9. **Better Together than Apart.** If two pieces of code share state / are always used together / one makes no sense without the other → THEY BELONG TO THE SAME MODULE.
10. **Define Errors out of Existence.** Best error handling = design the interface so the error CANNOT exist / does not need to be handled by the caller. E.g.: return semantic `Option<T>`/`null` instead of throwing exception.
11. **Design it Twice.** For non-obvious architectural decisions, draw 2 COMPLETELY DIFFERENT approaches on paper (5-10 lines each), compare trade-offs, only then choose. Avoid first-idea bias.
12. **Comments Should Describe Things that aren't Obvious from Code.** Commenting is NOT "documenting". Good comment = explains INTENT, CONTEXT, WHY, SPECIAL CASE THAT DOES NOT APPEAR IN CODE. Bad comment = translates syntax.
13. **Write Comments First.** Write the public docstring / intent comments first, ONLY THEN write the code body. If you cannot explain it without writing the code → bad design.
14. **Incremental / Agile Development Works for Design Too.** No need to design everything on day 1. Write first version → find accidental complexity → refactor to become deeper → repeat.
15. **Consistency Reduces Cognitive Load.** Same names, same error patterns, same return formats everywhere. Power of predictability = complexity reduction.

### D.3 CHECKLIST BEFORE YOU CODE (mandatory if task ≥ 8 files / ≥ 300 lines)

```
□ (1) Do I understand WHICH ESSENTIAL complexity this module solves?
□ (2) Have I checked if an EXISTING MODULE exists that solves 80%+? (Rule 4 REUSE BEFORE CREATE)
□ (3) Did I design the PUBLIC INTERFACE FIRST (before the body)? Is it SMALLER than the expected body?
□ (4) Does the public interface NOT leak internal details (storage, framework used, data structure)?
□ (5) Are there AT LEAST 2 different use cases for this abstraction today? (if 1 = reconsider — it might be shallow)
□ (6) Did I DEFINE ERRORS OUT OF EXISTENCE where I could? (return Option instead of throw, etc.)
□ (7) Is function/parameter name = obvious without reading the body? (if not = rename)
□ (8) Does public comment / docstring describe CONTRACT (what it does, input, output, side effects), NOT implementation?
□ (9) Was complexity PULLED INSIDE the module (caller doesn't know about special cases)?
```

### D.4 CHECKLIST BEFORE YOU COMMIT (mandatory before `/che-ship`)

```
□ (1) None of the 13 RED FLAGS (D.1) appear IN THE DIFF I'm about to commit?
      → If RF01, RF02, RF03, RF04 appear: HIGH severity in code-review (≤ 2 HIGHs with 0 CRITICAL = auto-fix in ship; >2 HIGHs = stop and refactor first).
□ (2) Does each new module / class have a small PUBLIC interface compared to the value delivered?
□ (3) No new Pass-Through methods (re-routing without value)?
□ (4) No Information Leakage (internal detail of file A appears in consumer file B)?
□ (5) New comments = explain intent/why/context (do not repeat syntax)?
□ (6) Did I add ESSENTIAL (domain) or ACCIDENTAL complexity? (If accidental → remove BEFORE commit.)
□ (7) If I changed public interface: did I update / write contract docstring first?
□ (8) Consistency: does this code follow the same names / patterns / error handling as the rest of the module?
```

### D.5 MAP: When to use which principle (8 canonical situations)

| Situation | Key principles | Che integration |
|---|---|---|
| Creating NEW class / module from scratch | D.2 #2 (deep), #3 (abstraction), #6 (general-purpose), #13 (comments first) | che-spec §6 hints + Before-You-Code (D.3) |
| Refactoring existing module that is "bad" | D.2 #1 (enemy complexity), #4 (not shallow), #9 (together), #10 (errors out) | che-code-review HIGH findings → auto-fix |
| Creating public interface / tRPC API / REST | D.2 #5 (no leakage), #8 (pull down), #12 (restriction, not choice), #15 (consistency) | scope-checker CHECK4 env + design doc |
| Error handling / edge cases | D.2 #10 (define errors out of existence) + §2 security | code-review MEDIUM findings |
| Naming functions / parameters / variables | D.1 RF10 (not obscure) + D.2 #15 (consistency) | code-review nit auto-fix |
| Writing comments / docs | D.1 RF08, RF09 (not repeating code / not internal doc) + D.2 #12, #13 (comments first) | code-review comments guideline §16 |
| Large architectural decision (new layer, new lib) | D.2 #11 (design twice) + §1 No Accidental Complexity | ADR skill (adr-architecture) mandatory |
| Planning large feature / epic (before SPEC) | D.2 #1 (complexity is enemy #1) + #7 (different abstraction per layer) | che-onboarding + xray architecture |

---

## Final Reminder

These rules are **intentionally strict.** They exist because:
- LLMs love over-engineering. §1 + §15 fight that.
- LLMs love creating new abstractions. §3+4 fight that.
- LLMs skip tests until after. §10 fixes that.
- LLMs leak secrets/PII accidentally. §2 + §17 prevent that.
- LLMs write overly-commented/verbose code hard to review. §16 forces clean/concise code.
- LLMs anticipate future and deliver giant PRs. §15 + gh-stack Appendix C forces small incrementals.

If any rule feels wrong for a specific case → **log the exception + rationale to `$CHE_DECISIONS_PATH` (NEVER under `<WORKTREE_ROOT>/.trae/`; run `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"` to resolve the correct path outside the user worktree)**, and proceed.

---
