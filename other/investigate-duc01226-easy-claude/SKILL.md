---
name: investigate
description: '[Fix & Debug] Use when a workflow step or the user asks for how an existing feature works (read-only code-flow trace) or --mode=debug: a bug''s root cause (reproduce, trace end-to-start). --mode=explain. Plans or decisions: understand.'
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
> **[BLOCKING] Mode routing — detect FIRST.** Explicit `--mode=debug` or `--mode=explain` selects that mode; no mode is the default read-only code-flow investigation (everything below, unchanged). `$investigate --mode=debug <bug>` is the former `/debug-investigate` (root-cause investigation of a bug).

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->
> **[BLOCKING]** Execute phases in declared order. NEVER skip, reorder, or merge without explicit user approval.
> **[BLOCKING]** Before each phase or skill call, update task tracking; mark `in_progress` at start and `completed` after evidence.
> **[BLOCKING]** Record evidence for each completed/skipped phase; if task tools are unavailable, maintain an equivalent tracker.
> **[BLOCKING]** Investigation stays READ-ONLY; report findings, never patch source.
<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Explain existing code through READ-ONLY, evidence-backed exploration so every finding maps to `file:line` (or "inferred"), system flow is verified, and follow-up decisions rest on evidence without changing source.

**Summary:**

- **Purpose:** map behavior from trigger to exit, including transformations, side effects, validation, authz, errors, and cross-service paths; stop at findings.
- **Ordered work:** (0) classify `quick|deep|debug|recommendation|explain` → (1) discover `Entities → Commands/Queries → EventHandlers → Controllers → Consumers → Components` → (2) optional graph hint on high-risk key files (a stale-able hint, never required) → (3) document the per-file knowledge graph → (4) map entry→exit flow → (5) analyze rules/validation/authz/errors/edge cases → (6) synthesize (deep writes/re-reads analysis file; explain writes ledger) → (7) present cited findings.
- **Gates:** stay READ-ONLY; cite `file:line` and mark unknowns `inferred`; recommendation scope requires the full validation chain and confidence; cross-service scope scans producers, consumers, sagas, and contracts.

**Workflow:**

1. **Phase 0: Classify** — MUST ATTENTION determine scope (quick / deep / debug / recommendation / explain) before acting
2. **Discovery** — MUST ATTENTION search codebase for related files (Entities > Commands/Queries > EventHandlers > Controllers > Consumers > Components)
3. **Graph Hint (optional)** — when the blast radius looks high-risk and grep alone may miss it, run graph queries on 2-3 key files (main agent only); a hint that may be stale, verified by reading
4. **Knowledge Graph** — MUST ATTENTION read + document purpose, symbols, dependencies per file
5. **Flow Mapping** — MUST ATTENTION trace entry points through pipeline to exit points
6. **Analysis** — MUST ATTENTION extract business rules, validation, authorization, error handling
7. **Synthesis** — MUST ATTENTION for deep scope, write and re-read `tmp/analysis/[feature]-investigation.md`; explain scope writes its ledger; quick scope skips the analysis file
8. **Present** — MUST ATTENTION deliver structured findings, offer deeper dives

**Modes:**

- **Default (analysis)** — MUST ATTENTION deliver engineer-facing structured findings + analysis file; quick scope may skip the file.
- **`--mode=explain`** (developer narrative) — MUST ATTENTION keep the same READ-ONLY and evidence gates (the graph stays optional advice); deliver a one-way Purpose → How → Why → Impact explanation in a git-ignored ledger. See [Mode: Explain](#mode-explain-developer-narrative). Use `$understand [target]` for the standalone explainer.
- **`--mode=debug`** (root-cause investigation of a bug) — MUST ATTENTION read `references/mode-debug.md` in full FIRST: reproduce → hypothesize → end-to-start trace → confirm → `$why-review` validation → report, then `$fix`. Investigation-ONLY. See [Mode Dispatch](#mode-dispatch).

**Key Rules:**

- Strictly READ-ONLY — NEVER make code, plan, or spec changes
- Every claim/finding needs `file:line` proof — mark unverified as "inferred"
- Optional: the code graph can hint at callers/dependents for a high-risk blast radius grep may miss; it can be stale, so verify by reading — never required
- MUST ATTENTION plan a task to READ `project-structure-reference.md`; if missing, search project documentation, coding standards, and architecture docs

## Mode Dispatch

Detect the mode from the invocation arguments before any other work; do not load a mode file the invocation did not select.

| Mode | Purpose | Read in full FIRST |
| --- | --- | --- |
| _(none)_ | Default read-only code-flow investigation — this file | — |
| `--mode=debug [bug description]` | Root-cause investigation of a bug: reproduce, trace end-to-start, hypothesis matrix, pinpoint the owning layer, `$why-review` validation; never patches code (`$fix` applies the fix). Formerly `/debug-investigate` | `references/mode-debug.md` |
| `--mode=explain [target]` | One-way developer narrative (Purpose → How → Why → Impact) — [Mode: Explain](#mode-explain-developer-narrative) below | _(inline below)_ |

- **[BLOCKING]** When `--mode=debug`, read `references/mode-debug.md` in full FIRST; it replaces the default Phase 0 classification, Workflow and Output Format for the invocation (Phase 0 bug-type routing, reproduce, end-to-start trace, the `$why-review` Root Cause Validation gate, `$fix` hand-off). Workflow invocation (for example `workflow-bugfix`) returns the validated root cause to the parent; standalone ends with the ask user tool next-step choice.
- `--mode=debug` and the default flow are separate invocations; the default flow never chains into the debug gate, and debug mode never relaxes the READ-ONLY or `file:line` evidence rules.

## Phase 0: Scope Classification

**Classify before acting** — MUST ATTENTION route to the required depth:

| Scope              | Signals                                        | Depth                                                    |
| ------------------ | ---------------------------------------------- | -------------------------------------------------------- |
| **Quick**          | Single feature/function, clear entry point     | grep → trace → answer (no analysis file needed)          |
| **Deep**           | Multi-service, cross-boundary, ambiguous scope | Full workflow + knowledge graph template + analysis file |
| **Debug**          | Error/crash/unexpected behavior                | Root-cause-debugging protocol above; a full root-cause hunt is `--mode=debug` (see [Mode Dispatch](#mode-dispatch)) |
| **Recommendation** | Code change suggested (removal, refactor)      | Validation chain protocol below — MANDATORY              |
| **Explain**        | `--mode=explain` flag | Investigation-local developer narrative — see [Mode: Explain](#mode-explain-developer-narrative). Use `$understand` for the standalone prompt-driven explainer. |

Quick scope: MUST ATTENTION run grep → present (optional graph hint for a high-risk blast radius); skip knowledge-graph template + analysis file.
Deep scope: MUST ATTENTION write to `tmp/analysis/[feature]-investigation.md`.
Explain scope: MUST ATTENTION keep the same READ-ONLY evidence gate; deliver in-chat narrative + git-ignored ledger, NOT the analysis file.

## Investigation Mindset (NON-NEGOTIABLE)

**Skeptical. Every claim needs `file:line` proof; confidence >80% to act.**
- NEVER assume names describe behavior — verify actual implementations
- MUST ATTENTION cite `file:line` for every finding; mark unproven claims "inferred"
- ALWAYS grep usages, consumers, and cross-service references — NEVER assume completeness
- ALWAYS trace actual call paths with evidence — NEVER rely on signatures alone

### Logical-ID Extraction & Business-Intent Rule (M3/M5)

> **AI-SDD Artifact Contract** — Shared SDD rules keep reusable guidance in `.claude`, require the `spec → plan → tasks → implement → verify → update spec/docs` cycle, traceability, explicit unknowns, and intent-guarding tests. Project-specific paths and commands come from project docs.
> Extracted rules use logical IDs and separate abstract source anchors; findings state business intent, not only implementation behavior.

MUST ATTENTION READ `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria before extracting operations, business rules, or events into findings:

- Assign each extracted operation/rule/event a logical ID (FR-/BR- for operations/rules) as PRIMARY. Keep `[Source: namespace/service/id]` as a separate abstract-anchor carrier; never use physical coordinates/repository paths in the rule statement (M3).
- For every rule, explain **WHY** it exists (business intent/invariant), not only **WHAT** code does; state it in tech-agnostic terms reusable on any stack (M5).

## Workflow

1. **Discovery** — MUST ATTENTION search all related files. Priority: Entities > Commands/Queries > EventHandlers > Controllers > Consumers > Components.
2. **Graph Hint (OPTIONAL)** — Optional: when grep and reading files alone may not reveal a high-risk blast radius (shared contract, many callers, cross-module/cross-service flow, public API), the code graph (`.code-graph/graph.db`) can add callers, dependents and impacted tests. Treat it as a hint, NOT proof: the graph can be stale or incomplete (it lags uncommitted edits and unindexed paths) — verify anything that matters by reading the files/grep. Skip it for low-risk or local changes; an absent or stale graph is never a finding. The main agent runs it (sub-agents do not). Pick 2-3 key files (entities, commands, bus messages):
    ```bash
    python .claude/scripts/code_graph connections <key_file> --json
    python .claude/scripts/code_graph query callers_of <FunctionName> --json
    python .claude/scripts/code_graph query importers_of <file_path> --json
    # "ambiguous" → search to disambiguate, retry with qualified name
    python .claude/scripts/code_graph search <keyword> --kind Function --json
    # Trace how two nodes connect
    python .claude/scripts/code_graph find-path <source> <target> --json
    # Filter by service, limit results
    python .claude/scripts/code_graph query callers_of <name> --limit 5 --filter "ServiceName" --json
    ```
    The graph may surface callers, importers, tests, inheritance, and other edges grep misses. `$graph-code --mode=connect-api` can hint at frontend-to-backend API mapping.

**Post-Grep Graph Hint (optional):** when discovery surfaces an important high-risk entry file — entity, command/query, handler, controller, bus message/consumer, component, store, or API service — a graph trace (`py -3 .claude/scripts/code_graph trace <key-entry-file> --direction both --json`; macOS/Linux: `python3` instead of `py -3`) can hint at callers, consumers, bus messages, event chains, and tests grep may not reveal. It can be stale or incomplete — verify by reading the files. **Pattern: grep → optional graph hint → grep verify.**
3. **Knowledge Graph** — MUST ATTENTION read + analyze each file from grep + graph results; document purpose, symbols, dependencies, and data flow. Batch in groups of 10 and update progress after each batch. Use the per-file template:
4. **Flow Mapping** — MUST ATTENTION trace entry → exit; map transformations, persistence, side effects, and cross-service boundaries.
5. **Analysis** — MUST ATTENTION extract business rules, validation, authorization, errors, happy path, and edge cases.
6. **Synthesis** — Answer the original question with an executive summary, key files, patterns, and text flow diagrams.
7. **Present** — Use Output Format; offer deeper dives.

**If a prior discovery pass supplies a numbered file list:** use those confirmed paths, skip redundant discovery, and prioritize highest relevance.

### Parallel Investigation Threads (Discovery → ONE wave → optional Graph Hint)

Investigation is strictly READ-ONLY; parallelize independent threads with disjoint write targets. Once Step 1 names the surface, decompose it BEFORE deep reads:

| Decomposition axis | One thread per…                                   | Use when                                                                              |
| ------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Per-module**     | module / bounded context the target spans          | the feature crosses several modules                                                   |
| **Per-layer**      | backend · frontend · data/persistence              | a full-stack flow — each layer reads a disjoint file set                              |
| **Per-question**   | one hypothesis, or one "how does X work?" question | Phase 0 classified `debug`, or the prompt carries several independent questions       |
| **Per-service**    | each service that produces/consumes the flow       | cross-service / event-driven target (pairs with the Cross-Service Check protocol)     |

Dispatch rules specific to this skill:

1. **Declare, then spawn in ONE message** — `Parallel plan: wave 1 = [thread A, thread B, …] · SEQ = [optional Graph Hint, Flow Mapping, Analysis, Synthesis] (each consumes the whole wave)`.
2. **Route per thread** — file/symbol landscape → `researcher`; root-cause/hypothesis → `debugger`; never a generic reviewer. The main `investigate` pass owns any optional graph hint after the read-only barrier.
3. **Own scope + report path** — each brief names exact files/questions and its own target (`tmp/analysis/[feature]-{thread}.md` or `tmp/reports/…`); threads NEVER share files and persist incrementally, not as transcripts.
4. **An optional Graph Hint stays SEQ on YOU** — after the barrier, Step 2's commands can be run on 2–3 surfaced high-risk key files to reconcile the independent threads into one dependency network; skip when the blast radius is low-risk.
5. **Synthesize from reports, not memory** — re-read each thread report, then write Steps 4–6 (Flow Mapping → Analysis → Synthesis) yourself.

**SEQ boundary:** a thread starting from another thread's finding is SEQ, not PAR. Example: consumer tracing waits for the published-event finding, so place it in wave 2 and name that dependency. Threads sharing only a topic (same feature, different layer) remain PAR.

## Investigation Techniques

### Discovery Search Patterns

Grep `{FeatureName}` with: `EventHandler`, `BackgroundJob`, `Consumer`, `Service`, `Component`.

**Priority order (stack-neutral):** (1) Domain model (entities/aggregates) → (2) Use-cases (commands/queries) → (3) Event handlers (side effects) → (4) Entry points (controllers/API/routes) → (5) Cross-service consumers → (6) Background jobs/schedulers → (7) UI components/stores → (8) Services/helpers. _Folder names, globs, and framework markers vary; discover them from the project's structure reference + project config._

### Dependency Tracing

**Backend (stack-specific locators):** method/function callers (grep backend source); dependency injectors (interface/type in constructors or DI wiring); domain-event subscribers (framework handler type); cross-service message handlers (message/event contract); repository/data-access usage (repository/data-access interface).

**Frontend:** component users (grep selector in templates); service importers (grep class in source); store/state chains (`state-effect → API call → response handler → state`); routes (grep component in routing files). _Find globs and framework primitives in the project's frontend reference + config._

### Data Flow Mapping

Document as: `[Entry] → [Validation] → [Processing] → [Persistence] → [Side Effects]`

**MUST ATTENTION trace:** (1) entry points, (2) processing pipeline, (3) transformations, (4) persistence, (5) exits/responses, (6) cross-service message-bus boundaries.

### Common Investigation Scenarios

| Question Type               | Steps                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------- |
| "How does X work?"          | Entry points → command/query handlers → entity changes → side effects                   |
| "Where is logic for Y?"     | Keywords in commands/queries/entities → event handlers → helpers → frontend stores      |
| "What happens when Z?"      | Identify trigger → trace handler chain → document side effects + error handling         |
| "Why does A behave like B?" | Find code path → identify decision points → check config/feature flags → document rules |

### Project Pattern Recognition

**Backend** (search `backend-patterns-reference` in docs/): CQRS commands/queries, entity event handlers, message-bus consumers, repository extensions, fluent validation, authorization attributes.

**Frontend** (search `frontend-patterns-reference` in docs/): component base classes, view-model/state-store base, reactive data-fetch effects with loading/error states, API service base class.

### Graph Intelligence (optional advice)

**When used, orchestrate grep → graph → grep:** (1) Grep key terms to find entry files, (2) `connections`/`batch-query`/`trace --direction both` can expand the dependency network, (3) Grep again to verify content. `trace` follows ALL edge types including MESSAGE_BUS and TRIGGERS_EVENT; results are hints that may be stale.

```bash
python .claude/scripts/code_graph connections <file> --json     # Full picture
python .claude/scripts/code_graph query callers_of <name> --json
python .claude/scripts/code_graph query importers_of <file> --json
python .claude/scripts/code_graph query tests_for <name> --json
python .claude/scripts/code_graph batch-query <f1> <f2> --json
```

## Evidence Collection

**Deep scope — MANDATORY:** Write analysis to `tmp/analysis/[feature-name]-investigation.md`; MUST ATTENTION re-read it ENTIRELY before presenting.

Structure: Metadata (original question) → Progress → File List → Knowledge Graph (per-file entries per SYNC:knowledge-graph-template) → End-to-Start Debugger Trace (bug/fix/behavior-changing) → Data Flow → Findings.

**Rule:** Every 10 files, MUST ATTENTION update progress and re-check alignment with the original question.

### Analysis Phases

**Comprehensive:** Run one focused pass per applicable dimension; for each, ask what it protects, what fails if weak, and what evidence proves the answer:
- **Happy path** — trace expected input → processing → result.
- **Error paths** — trace failures, handling, and observable outputs.
- **Edge cases** — trace boundary, empty, duplicate, retry, and alternate paths found in code.
- **Authorization** — trace actors, permissions, ownership, and denial paths.
- **Validation per layer** — trace where each invariant enters, is enforced, and can be bypassed.

Extract core business rules, state transitions, side effects, and evidence for each dimension.

**Synthesis:** Executive summary (1-para answer, top 5-10 key files, patterns) + step-by-step `file:line` walkthrough + flow diagrams.

### Output Format

MUST ATTENTION include: (1) Direct answer (1-2 paragraphs), (2) Step-by-step "How It Works" with `file:line` refs, (3) Key Files table, (4) Data Flow diagram, (5) "Want to Know More?" subtopics.

For bug, failed-verification, or behavior-changing investigations, MUST ATTENTION also include:

```markdown
### Debugger Trace: End -> Start

- Observed final state:
- Final reader/query/renderer/assertion:
- Backward hops: reader -> storage/projection/cache -> writer -> consumer/handler/job -> producer/origin
- Feeder paths scanned:
- Unknown or unverified paths:

### Hypothesis Matrix

| RC | Hypothesis | Evidence for | Evidence against | Status | Verification |
| --- | --- | --- | --- | --- | --- |
```

### Guidelines

- **Evidence-based** — every claim needs code evidence; MUST ATTENTION mark unverified as "inferred"
- **Question-focused** — ALWAYS tie findings back to the original question
- **Read-only** — NEVER suggest changes unless explicitly asked
- **Layered** — start simple, offer deeper detail on request

## Related Skills

`researcher` (delegated landscape research) | `workflow-feature` (implementation) | `investigate --mode=debug` (bug root cause) | `fix` (applies the fix) | `graph-code --mode=query` (natural language queries)

---

## Mode: Explain (Developer Narrative)

**Trigger:** `$investigate --mode=explain [target]`. Manual-only; never auto-inserted into workflows. Use `$understand [target]` for the standalone explainer.

**Only change:** audience, shape, and write target. The evidence gate stays **identical and NON-NEGOTIABLE**: code/plans remain READ-ONLY; every concrete claim cites `file:line`; confidence >80% to assert (the graph stays optional advice). Explain mode NEVER relaxes these; mark unsupported narrative points "inferred".
**Goal:** make the **developer** understand **WHAT** the work is, its **PURPOSE**, **HOW** it works, and **WHY this way** (trade-offs + rejected alternatives) through a clear, detailed, **one-way** explanation. Derive scope from the prompt; no fixed agenda.

### Contract (read first)

- **DERIVE SCOPE FROM THE PROMPT.** No target → current context: active tasks (the current task list), working-tree changes (`git diff --name-only` + untracked via `git ls-files --others --exclude-standard`), active plan, and latest `$watzup` summary.
- **NEVER ASK THE USER A QUESTION.** Stay one-way: no teach-back, quiz, ask user tool, ambiguity question, or comprehension gate. Infer the likeliest target, state the assumption once, proceed. The explicit-skill workflow-detection exemption still applies.
- **OPT-IN, NEVER BLOCKS.** Explain and end; never loop or gate commit, implementation, or workflow progress.
- **ALWAYS EXPLAIN IN FULL.** Cover purpose + how + why every time.
- **EXPLAIN THE WHOLE SCOPE, LEAD WITH THE NON-OBVIOUS.** Cover all scope, order by blast radius, future-change cost, and surprise; treat boilerplate/CRUD briefly.
- **WRITES ONLY to a project-root temp folder.** Never edit source/plan files or `tmp/analysis/...`; the only write target is `tmp/understand/{branch}.md` (Step E3).

### Step E0 — Resolve scope

1. **Derive scope from the prompt:**

   | Prompt signal | Scope to explain |
   | ------------- | ---------------- |
   | Bare invocation, no target named | **Default: current working context** — active tasks + working-tree changes + active plan / latest `$watzup`. |
   | Names a change set / PR / "what I just did" | The diff and its rationale. |
   | Names a plan / "the approach" / "before we build" | The active plan: problem, approach, rejected alternatives, risks, phase order. |
   | Names a subsystem / file / feature / "how does X work" | That code path — read files (optionally a graph trace for a high-risk flow), explain the flow. |
   | Names a single decision / "why X over Y" | That decision and its trade-offs. |
   | Names a concept / bug / error | That concept or root cause. |
   | Ambiguous / multiple plausible targets | **Do NOT ask.** Infer most likely (default current context), state the assumption in one line, proceed. |

    State resolved scope in one line (e.g. `Explaining: current working changes (3 files) + active task #42`).

### Step E1 — Gather the material (proportional to scope)

- **Current context:** read the current task list, `git diff --name-only` (+ untracked), active plan, and latest `$watzup`; extract work, changes, rationale, behavior.
- **Plan:** read `plan.md` + `phase-*.md`; extract problem, approach, rejected alternatives, decisions, risks, phase order.
- **Subsystem:** read files (optionally `python .claude/scripts/code_graph trace <file> --direction both --json` as a stale-able hint); extract entry points, data flow, invariants.
- **Single decision:** read relevant code + rationale (comments, git blame, plan alternatives).

Do not read the whole repo for one decision.

### Step E2 — Order topics by leverage

Cover the whole scope; use these only to ORDER: **Blast radius** (grep/read; optionally `$graph-code --mode=blast-radius` as a stale-able hint; highest reach first) · **Future-change cost** (schema, public contract, cross-service message, shared/framework layer first) · **Surprise** (call out what a competent engineer would not guess). Give boilerplate/generated/mechanical renames one line.

### Step E3 — Maintain the understanding ledger

> **[HARD RULE]** Write the ledger ONLY to a project-root temp folder — NEVER inside `.claude/`, the source tree, or any tracked path.
>
> Path: `tmp/understand/{branch}.md` (use `temp/understand/{branch}.md` if the project already uses `temp/`); create the subdir if absent, replace branch `/` with `-`, and ensure it is git-ignored.
>
> **[ANNOUNCE — the chat is the deliverable]** The explanation lives in chat, not only in the file. Whenever writing/appending, state `Understanding ledger updated → tmp/understand/{branch}.md`; NEVER leave the explanation only in the ledger.

Append, never overwrite, a checklist with: **Problem** (purpose, prior limitation, branches) · **Solution** (design, business logic, edge cases, alternatives) · **Impact** (what/who changes, blast radius, follow-ups).

### Step E4 — Explain: Purpose → How → Why (the deliverable)

Deliver in chat, in this order, for **every** level; tune depth/vocabulary only. Cite `file:line` for every concrete claim.

1. **WHAT** — one-line orientation: name the thing and location.
2. **PURPOSE (why-it-exists)** — problem solved, prior limitation, and necessary alternative branch; lead here.
3. **HOW (mechanics)** — trace entry points, data flow, invariants, callers, business logic, and handled edge cases using file evidence (graph output, when used, is only a hint).
4. **WHY-this-way (trade-offs)** — explain why this over alternatives, cost/benefit, reversibility, and non-obvious decisions ("we did X instead of Y because Z").
5. **IMPACT (blast radius & follow-ups)** — what/who changes, upstream/downstream reach, open follow-ups.

Offer a simpler restatement/analogy for dense points when useful. Answer `eli5`/`elii` follow-ups; NEVER pose questions to the developer.

### Step E5 — Recap & close (no quiz, no loop)

Mark ledger items `explained`. Close with a 2–3 line recap: purpose, key mechanic, and highest-leverage trade-off/blast-radius note. End there; do NOT quiz, ask for restatement, loop, or block the next step.

**NOT for:** investigation/docs/design/research where nothing was built or planned to understand; comprehension gates; code-quality review (use `$code-quality-review`, `$changes-review`).
**Anti-Rationalization:** "Senior dev, skip it" → NEVER skip by level. · "I'll quiz them" → one-way only. · "Ambiguous — ask which" → infer + state assumption. · "Dump everything" → derive scope, order by leverage. · "Skip trade-offs" → WHY-this-way is mandatory. · "Drop ledger" → only `tmp/understand/{branch}.md`; announce its path because chat is the deliverable.

---

## Investigation & Recommendation Protocol

Applies only when recommending code changes (removal, refactoring, replacement). MUST ATTENTION complete the full validation chain.

### Validation Chain (NEVER skip steps)

**NEVER recommend code changes before completing ALL steps:**

1. Interface/API identified → 2. ALL implementations found → 3. ALL registrations traced → 4. ALL usage sites verified → 5. Cross-service impact (ALL services) → 6. Impact assessment → 7. Confidence declaration → **ONLY THEN** output recommendation.

**If ANY step incomplete → STOP.** State "Insufficient evidence to recommend."

### Breaking Change Risk Matrix

| Risk       | Criteria                                                      | Required Evidence                                              |
| ---------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| **HIGH**   | Removing registrations, deleting classes, changing interfaces | Full usage trace + impact + cross-service check (all services) |
| **MEDIUM** | Refactoring methods, changing signatures                      | Usage trace + test verification + cross-service check          |
| **LOW**    | Renaming variables, formatting, comments                      | Code review only                                               |

### Removal Checklist (ALL MUST ATTENTION pass)

- MUST ATTENTION verify no static references (`rg "ClassName" {configured-source-roots}` returns no live references)
- MUST ATTENTION verify no string literals/dynamic invocations (reflection, factory, message bus)
- MUST ATTENTION verify no DI registrations (`services.Add*<ClassName>`)
- MUST ATTENTION verify no config references (appsettings, env vars)
- MUST ATTENTION verify no test dependencies
- MUST ATTENTION verify cross-service impact (ALL microservices)

**Incomplete checklist → state:** `Confidence: <90% — did not verify [missing items]`.

### Evidence Hierarchy

(1) Code evidence (grep/read) → (2) test evidence → (3) documentation → (4) inference. Recommendations based on inference alone are FORBIDDEN; MUST ATTENTION upgrade to code evidence.

### Confidence Levels

**95-100%** full trace + all services | **80-94%** main paths verified | **60-79%** partially traced | **<60% DO NOT RECOMMEND**

**Format:** `Confidence: 85% — Verified main usage in ServiceC, did not check ServiceA/ServiceB`

### Service Comparison Pattern

Find working reference → compare implementations → identify differences → verify WHY each exists → recommend from proven pattern, NEVER assumptions.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting, including each file read; this prevents long-file context loss. For simple tasks, AI MUST ATTENTION ask the user whether to skip.

- `domain-entities-reference.md` in the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path) — domain entity catalog, relationships, cross-service sync (when task involves business entities/models).

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `cross-service-check` — Scan producers, consumers, sagas and shared contracts for cross-service impact; concluding an investigation, plan or spec in a service-based system → .claude/skills/shared/protocols/cross-service-check.md
- `end-to-start-debugger-trace` — Walk backward from the observed end state through every feeder path before fixing; fixing a non-trivial bug, a regression or unclear code flow → .claude/skills/shared/protocols/end-to-start-debugger-trace.md
- `environment-fault-hypothesis` — Weigh the environment as a competing cause, with a named discriminator; judging a bug report, failing test, error or unexpected output → .claude/skills/shared/protocols/environment-fault-hypothesis.md
- `fix-layer-accountability` — Fix at the component that owns the violated contract, not at the crash site; choosing where to apply a fix → .claude/skills/shared/protocols/fix-layer-accountability.md
- `graph-assisted-investigation` — Optional hint: a code-graph query can add callers and dependents when grep may miss a high-risk blast radius, and it can be stale; a high-risk change where grep and reading alone may miss the blast radius → .claude/skills/shared/protocols/graph-assisted-investigation.md
- `knowledge-graph-template` — Per-file analysis record: type, pattern, symbols, dependencies and evidence; documenting analyzed files during an investigation → .claude/skills/shared/protocols/knowledge-graph-template.md
- `root-cause-debugging` — Systematic root-cause debugging, never guess-and-check; debugging a failure → .claude/skills/shared/protocols/root-cause-debugging.md
- `sequential-thinking-protocol` — Structured multi-step reasoning with revision, branch and hypothesis markers; planning, debugging or reviewing complex or ambiguous work → .claude/skills/shared/protocols/sequential-thinking-protocol.md
- `source-test-drift-check` — When source behavior changes, reconcile the affected tests from evidence; code, fix, test or review work changes behavior → .claude/skills/shared/protocols/source-test-drift-check.md
- `task-tracking-external-report` — Task breakdown before the work and report files written incrementally; starting any multi-step skill, plan or review → .claude/skills/shared/protocols/task-tracking-external-report.md
- `understand-code-first` — Read and trace the target and existing patterns before changing code; planning or editing code → .claude/skills/shared/protocols/understand-code-first.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code/conventions BEFORE any modification or explanation. The code graph is optional advice for high-risk blast radius (a hint that may be stale), never a requirement.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**Optional advice:** the code graph (`.code-graph/graph.db`) can hint at a high-risk blast radius grep misses; it can be stale, so verify by reading files. Never required.

<!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim; never speculate. Confidence >80% to act, <60% = do NOT recommend; "not enough evidence" is valid output.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:knowledge-graph-template:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** document per-file: type, pattern, symbols, dependencies, relevanceScore, evidenceLevel.

<!-- /SYNC:knowledge-graph-template:reminder -->

<!-- SYNC:fix-layer-accountability:reminder -->

**IMPORTANT MUST ATTENTION** trace full data flow and fix at the owning layer, not the crash site. Audit all access sites before adding `?.`.

<!-- /SYNC:fix-layer-accountability:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** use structured reasoning for complex or ambiguous work, implicitly when visible markers would clutter. Verify hypotheses, revise assumptions, and close with confidence, assumptions, open questions and a concrete next action.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `tmp/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing; select the authoritative invariant owner from project architecture and retain validation at untrusted boundaries. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->


<!-- SYNC:environment-fault-hypothesis:reminder -->

**MUST ATTENTION** environment-fault gate: a bug, failed test, error, or odd output is NOT proof of a code defect. Sweep environment preconditions (versions, deps/install state, config & env vars, services, ports/network/clock, permissions, leftover state) and resource/transience suspects (RAM, CPU, disk, handles, network, timeouts) as a competing hypothesis, cite the discriminator you ran, and fix an environment cause in the environment — never by editing code or weakening a test. "Flaky" is a symptom, not a verdict.

<!-- /SYNC:environment-fault-hypothesis:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Explain existing code through READ-ONLY, evidence-backed exploration so every finding maps to `file:line` (or "inferred"), system flow is verified, and follow-up decisions rest on evidence without changing source.

**IMPORTANT MUST ATTENTION — Main steps:** run in order: (0) classify `quick|deep|debug|recommendation|explain` → (1) discover all related files (`Entities → Commands/Queries → EventHandlers → Controllers → Consumers → Components`) → (2) optional graph hint on high-risk key files → (3) build the per-file knowledge graph → (4) map entry→exit flow and side effects → (5) analyze rules, validation, authz, errors, and edge cases → (6) synthesize (deep analysis file; explain ledger) → (7) present cited findings.

**IMPORTANT MUST ATTENTION — Modes/gates:** `--mode=debug` → read `references/mode-debug.md` in full FIRST (root-cause investigation; `$why-review` gate; never patches); Default analysis returns structured findings; quick skips the knowledge-graph template and analysis file; deep writes/re-reads `tmp/analysis/[feature]-investigation.md`; `--mode=explain` writes only `tmp/understand/{branch}.md` and delivers one-way WHAT → PURPOSE → HOW → WHY → IMPACT, never questions or loops. Stay READ-ONLY; cite `file:line` or mark "inferred"; the code graph is optional advice (a stale-able hint; never required); recommendation scope requires the full validation chain; cross-service scope scans producers, consumers, sagas, and contracts; bug/behavior-changing scope runs end-to-start tracing plus a hypothesis matrix.

**Protocols in force (SYNC bodies above are canonical):**

- **End-to-Start + Root Cause:** start at observed end state; reproduce, isolate, trace, hypothesize, verify; fix only at the owning layer.
- **Knowledge Graph + Evidence:** document per-file type/pattern/symbols/dependencies/relevance/evidence level; cite every claim and confidence.
- **Project Docs + Task Tracking:** read required docs first; create/advance tasks one at a time; persist deep findings incrementally.
- **Critical/Sequential Thinking:** use Thought N/M with revisions/branches/hypotheses when needed; never present guesses as facts.
- **Cross-Service + Source/Test Drift:** scan producers, consumers, sagas, contracts; reconcile affected tests when source behavior changes.
- **Parallel Dispatch:** tag PAR/SEQ, use disjoint write-set waves, spawn each wave in one message, honor the all-return barrier.
- **Nested Tasks + Fix Layer:** expand child phases when nested; trace origin → crash and protect all consumers at the lowest invariant-owning layer.

**IMPORTANT MUST ATTENTION** stay READ-ONLY — NEVER edit code, plans, or specs during investigation; deliver findings only — why: mutation corrupts the baseline the next step trusts.
**IMPORTANT MUST ATTENTION** cite `file:line` for every claim; mark unverified statements "inferred"; confidence >80% to act, <60% DO NOT recommend — why: an unmarked guess propagates as fact.
**Optional advice:** for a high-risk blast radius grep may miss, `code_graph` (and `$graph-code --mode=connect-api` for frontend-to-backend mapping) can add hints — they may be stale; verify by reading. Never required.
**MANDATORY IMPORTANT MUST ATTENTION** create tasks before work, keep one `in_progress`, and complete each after evidence; if nested, expand/link child phases.
**MANDATORY IMPORTANT MUST ATTENTION** read required project docs first, including `lessons.md` and `project-structure-reference.md` for architecture; local conventions override generic assumptions.
**MANDATORY IMPORTANT MUST ATTENTION** grep 3+ patterns and read implementations before concluding; evaluate fit before copying a nearby pattern.
**MANDATORY IMPORTANT MUST ATTENTION** deep scope → write/re-read `tmp/analysis/[feature]-investigation.md`; recommendation scope → complete implementations → registrations → usages → cross-service impact → confidence or state "Insufficient evidence to recommend."
**MANDATORY IMPORTANT MUST ATTENTION** bug/behavior-changing scope → trace end-to-start, enumerate feeder paths, build the hypothesis matrix, identify the owning layer, and prove forward convergence before any fix recommendation.

**Anti-Rationalization:**

| Evasion                                            | Rebuttal                                                                       |
| -------------------------------------------------- | ----------------------------------------------------------------------------- |
| "Already grepped, enough evidence"                 | Show `file:line` proof. No citation = no evidence; unverified = mark inferred. |
| "Quick task, skip task tracking"                      | Still need tracking. Create tasks, mark done immediately.                      |
| "Recommendation is obvious, skip validation chain" | Risk matrix applies regardless of confidence. Complete ALL steps or STOP.      |
| "Deep scope wastes time for this"                  | Classify first. If quick, fine — but DECLARE scope before skipping steps.      |
| "Nearby example is close enough, copy it"          | Closest ≠ matching preconditions. Verify base class, scope, lifetime first.    |
| "I'll just fix what I found while here"            | READ-ONLY. Investigation never mutates; hand findings to the fix step.         |

**[TASK-PLANNING]** Before acting, analyze scope and break work into small tasks/subtasks with task tracking.

**IMPORTANT MUST ATTENTION** READ-ONLY always; cite `file:line` or mark "inferred".
**IMPORTANT MUST ATTENTION** classify and run the ordered phases; complete the required validation gates before concluding.
**IMPORTANT MUST ATTENTION** these three rules bind every scope and mode; the code graph is optional advice, never a gate.
