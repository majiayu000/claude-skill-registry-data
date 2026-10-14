---
name: scout
description: '[Investigation] Use when quickly locating relevant files and affected areas across a large codebase.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Deliver a complete, prioritized map of every file relevant to the task via fast, parallel codebase discovery — grep + graph combined — so downstream work starts with full coverage and zero blind spots.

**Summary:**

- **Main step pipeline (run in order, never merge):** Phase 0 classify scope → Step 1 analyze request (extract entities/keywords/file-types) → Step 2 spawn parallel `scout` subagents (grep/glob) → Step 3 graph-expand 2-3 key files (YOU, main agent) → Step 4 low-result check (<5 files → broader re-pass) → Step 5 synthesize numbered prioritized list → ask the user directly for next step.
- Classify scope FIRST (Phase 0: backend/frontend/full-stack) so you spawn only the agents you need — never the default 3 when the prompt names one layer.
- Sub-agents do the parallel grep/glob; only YOU (main agent) run the graph commands afterward — graph expansion on 2-3 key files is MANDATORY when `.code-graph/graph.db` exists and is the step that finds what grep can't.
- This is discovery, not analysis: return prioritized file paths fast (3-5 min), no content deep-dives — that's `investigate`'s job.
- If <5 files surface, re-examine keywords and run a second pass with broader synonyms before synthesizing; close by asking the user (ask the user directly) which next step to take.

**Workflow:**

1. **Phase 0: Classify** — Detect search scope (backend/frontend/both) + keyword type
2. **Analyze Request** — Extract entity names, feature keywords, file types from prompt
3. **Parallel Search** — Spawn agents searching backend core, backend infra, frontend paths
4. **Graph Expand (MANDATORY — DO NOT SKIP)** — **MUST ATTENTION** run graph commands on 2-3 key files. Graph reveals complete dependency network grep CANNOT find.
5. **Low-Result Check** — If <5 files returned, re-examine keywords and run second pass
6. **Synthesize** — Combine grep + graph into numbered, prioritized file list

**Key Rules:**

- Speed over depth — return file paths only, no content analysis
- Target 3-5 minutes total; 3-minute timeout per agent
- NEVER skip graph expansion when `.code-graph/graph.db` exists
- `--ext` / `--engine=external` switches the search engine to the `scout-external` agent (gemini/opencode CLIs); default is internal subagents

# Scout — Fast Codebase File Discovery

---

## Phase 0: Classify Search Scope

**Before spawning agents**, classify request:

| Scope         | Detection                                              | Agent Strategy           |
| ------------- | ------------------------------------------------------ | ------------------------ |
| Backend-only  | server-side class names, domain entities, API handlers | Agents 1+2, skip Agent 3 |
| Frontend-only | component names, client-side source, UI features       | Agent 3 only             |
| Full-stack    | Feature name spanning both layers                      | All 3 agents             |
| Unknown       | Ambiguous prompt                                       | Default all 3 agents     |

**Think:** Prompt mention specific layer? Entity exist in backend, frontend, or both? Adjust agent count — avoid spawning unnecessary agents.

---

## When to Use

- Quickly locating relevant files across large codebase
- Beginning work on features spanning multiple directories
- Before changes affecting multiple parts
- Mapping file landscape before investigation or implementation

**NOT for:** Deep code analysis (use `investigate`), debugging (use `debug-investigate`), implementation (use `workflow-feature`).

---

## Workflow

### Step 1: Analyze Search Request

Extract from USER_PROMPT:

- Entity names (User, Customer, Order)
- Feature names (authentication, notification)
- File types needed (backend, frontend, or both)

### Step 2: Execute Parallel Search

Spawn SCALE number of `scout` subagents in parallel via `spawn_agent` tool (`agent_type: "scout"`).

**WHY `scout` not `Explore`:** Custom `scout` agents read `.claude/agents/scout.md` — includes graph CLI knowledge + Bash access. Built-in `Explore` agents have NO graph awareness.

#### Engine Selection (`--ext` / `--engine=external`)

Detect the engine flag in args (default: **internal**):

- **Internal (default):** spawn `agent_type: "scout"` — the parallel grep/glob/graph search described below.
- **External (`--ext` or `--engine=external`):** spawn `agent_type: "scout-external"` instead. That agent (`.claude/agents/scout-external.md`) owns the `gemini`/`opencode` CLI dispatch, the Explore fallback, and the install prompt when those CLIs are absent.

Flag only switches **which subagent runs**. Orchestration identical for both engines: Phase 0 classify, Step 3 graph-expand (run by you, main agent), low-result check, synthesize. Output contract (numbered, prioritized file list) same.

#### Agent Distribution

- **Agent 1 - Backend Core**: `{module-source-root}/` domain folder + command folder + query folder (per the project's structure reference)
- **Agent 2 - Backend Infra**: `{module-source-root}/` event-handler folder + controllers + background-jobs folder (per the project's structure reference)
- **Agent 3 - Frontend**: `{frontend-apps-dir}/`, `{frontend-libs-dir}/{domain-lib}/`, `{frontend-libs-dir}/{common-lib}/`

Per agent: 3-minute timeout. Return file paths only — no content analysis. Use Glob (patterns), Grep (content), Bash (graph CLI).

#### Search-Axis Fan-Out (ONE wave — each axis is blind to the others)

Partitioning by path still searches ONE way. Each axis below finds files the others structurally CANNOT see — that blindness is exactly why a single search angle misses files. Select the axes the prompt warrants (they compose with the path split above: an agent gets one path scope + one axis) and spawn the whole set TOGETHER in one message:

| Axis                      | The agent searches by                                                                                     | Finds what the other axes miss                                           |
| ------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Filename / glob**       | Glob on entity + feature names and the project's path conventions                                         | files NAMED for the feature that never mention the keyword inside        |
| **Symbol / content grep** | Grep for class, command, query, handler, endpoint, message names                                          | files that USE the concept without carrying it in their path             |
| **Convention / naming**   | the project's suffix/prefix conventions (`*Handler`, `*Consumer`, `*-store`, per the structure reference) | siblings that convention says must change together                       |
| **Test coverage**         | test directories for the same keywords, plus fixtures/builders/mocks                                      | the tests pinning the behavior — usually the fastest statement of intent |
| **Config / registration** | DI wiring, routes, feature flags, config keys, resource/i18n files                                        | registrations and string-literal references a symbol grep skips          |

**Graph is the sixth axis and it stays with YOU** — Step 3, after the barrier; sub-agents do not run it here.

Wave rules: precompute the full path × triggered-axis assignment set, then dispatch it in consecutive **capacity-bounded waves** with one unique exact artifact path per assignment. Never drop an axis to fit host capacity; queue overflow assignments into the next wave. Each wave is read-only with zero write overlap, launches in one message, and reaches its barrier before Step 3. An axis the prompt gives no trigger for is not an assignment and counts as returned. Both engines take identical axis briefs — `--ext` only swaps `scout` for `scout-external`.

### Step 3: Graph Expand (MANDATORY — DO NOT SKIP)

**YOU (main agent) MUST ATTENTION run graph commands YOURSELF after sub-agents return.** NOT optional — without graph, results are incomplete. Sub-agents cannot use graph — only main agent can.

```bash
# Check graph exists
ls .code-graph/graph.db 2>/dev/null && echo "GRAPH_AVAILABLE" || echo "NO_GRAPH"
```

If GRAPH_AVAILABLE, pick 2-3 key files from sub-agent results (entities, commands, bus messages):

```bash
# Full dependency network of key file
python .claude/scripts/code_graph connections <key_file> --json

# All callers of key command/handler
python .claude/scripts/code_graph query callers_of <FunctionName> --json

# All importers of bus message class
python .claude/scripts/code_graph query importers_of <file_path> --json

# Batch query multiple files (most efficient)
python .claude/scripts/code_graph batch-query <file1> <file2> <file3> --json

# If graph returns "ambiguous" — disambiguate first
python .claude/scripts/code_graph search <keyword> --kind Function --json

# Trace shortest path between two nodes
python .claude/scripts/code_graph find-path <source_qn> <target_qn> --json

# Filter by service, limit results
python .claude/scripts/code_graph query callers_of <name> --limit 5 --filter "ServiceName" --json
```

**Grep-First Discovery (semantic queries):** When prompt describes behavior/flow (not specific file), grep key terms FIRST to discover entry files, then use those as graph input:

1. Grep class names, commands, handlers, endpoints
2. Use discovered files as input to `connections`, `batch-query`, or `trace`
3. Use `trace --direction both` on middle files (controllers, commands) for full upstream + downstream

Graph results get HIGHER priority than grep — structural relationships > text matches. After graph expansion, grep again to verify content in discovered files.

**Post-Grep Trace Trigger:** whenever a grep/glob surfaces an important entry-point file — an entity, command, query, event/command handler, controller, bus message/consumer, component, store, or api-service — immediately run a graph trace on it before concluding. The trace reveals callers, consumers, bus messages, event chains, and tests that grep CANNOT find: `python .claude/scripts/code_graph trace <key-entry-file> --direction both --json`. **Pattern: grep finds files → graph trace reveals full system flow → grep verifies specific details.**

### Step 4: Low-Result Check

If total files found <5 after Steps 2-3:

1. Re-examine keywords — too specific? Try broader synonyms
2. Spawn second scout agent with alternate search terms
3. Try `python .claude/scripts/code_graph search <keyword> --json` to find nodes by name

### Step 5: Synthesize Results

**De-duplicate the union FIRST.** The axes overlap by design, so the same file legitimately arrives from several agents. Normalize each path (separators, casing) and merge to exactly ONE entry, recording which axes surfaced it — multi-axis hits rank higher (independent confirmation), while a HIGH-priority file surfaced by a single axis is the coverage risk worth one verifying grep before it ships in the list.

Then combine grep + graph into a numbered, prioritized file list (see Results Format).

---

## Search Patterns by Priority

> Substitute folder names + file globs from the project's structure reference / `docs/project-config.json`. `{backend-source-glob}` / `{frontend-source-glob}` are the per-stack source extensions.

```
# HIGH PRIORITY - Core Logic
**/{entity-folder}/**/*{keyword}*.{backend-source-glob}
**/{command-folder}/**/*{keyword}*.{backend-source-glob}
**/{query-folder}/**/*{keyword}*.{backend-source-glob}
**/{event-handler-folder}/**/*{keyword}*.{backend-source-glob}
**/*{keyword}*{component-suffix}.{frontend-source-glob}
**/*{keyword}*{store-suffix}.{frontend-source-glob}

# MEDIUM PRIORITY - Infrastructure
**/{controllers-folder}/**/*{keyword}*.{backend-source-glob}
**/{background-jobs-folder}/**/*{keyword}*.{backend-source-glob}
**/*Consumer*{keyword}*.{backend-source-glob}
**/*{keyword}*{api-service-suffix}.{frontend-source-glob}

# LOW PRIORITY - Supporting
**/*{keyword}*Helper*.{backend-source-glob}
**/*{keyword}*Service*.{backend-source-glob}
**/*{keyword}*{markup-glob}
```

---

## Graph Intelligence (MANDATORY when graph.db exists)

---

## Results Format

```markdown
## Scout Results: {USER_PROMPT}

### High Priority - Core Logic

1. `{module-source-root}/{entity-folder}/{Entity}` — domain entity
2. `{module-source-root}/{command-folder}/{Feature}/Save{Entity}Command` — mutating command
   ...

### Medium Priority - Infrastructure

10. `{module-source-root}/{controllers-folder}/{Entity}Controller` — endpoint
11. `{module-source-root}/{event-handler-folder}/{Feature}/SendNotificationOn{Entity}CreatedEventHandler` — event handler
    ...

### Low Priority - Supporting

20. `{module-source-root}/{helpers-folder}/{Entity}Helper` — supporting helper
    ...

### Frontend Files

30. `{frontend-libs-dir}/{domain-lib}/{configured-feature-path}/{feature}-list.component`
    ...

**Total Files Found:** {count}
**Search Completed In:** {time}

### Suggested Starting Points

1. `{most relevant file}` - {reason}
2. `{second most relevant}` - {reason}

### End-to-Start Trace Candidates

| Role                           | Candidate files | Why relevant                                           | Evidence                         |
| ------------------------------ | --------------- | ------------------------------------------------------ | -------------------------------- |
| Observed final output / reader | `{files}`       | `{reader, renderer, assertion, query, aggregate, log}` | `{file:line or search evidence}` |
| Storage / projection / cache   | `{files}`       | `{state consumed by reader}`                           | `{file:line or search evidence}` |
| Writer / updater               | `{files}`       | `{writes final state}`                                 | `{file:line or search evidence}` |
| Consumer / handler / job       | `{files}`       | `{transforms or schedules writes}`                     | `{file:line or search evidence}` |
| Producer / origin trigger      | `{files}`       | `{upstream source of input}`                           | `{file:line or search evidence}` |

**Feeder-path scan:** list every producer/caller/event/job candidate that may write the same final state. Mark unknown paths explicitly instead of hiding them.

### Unresolved Questions

- {any questions that need clarification}
```

---

## Quality Standards

| Standard       | Expectation                            |
| -------------- | -------------------------------------- |
| **Speed**      | Complete in 3-5 minutes                |
| **Accuracy**   | Return only relevant files             |
| **Coverage**   | Search all likely directories          |
| **Efficiency** | Minimize tool calls                    |
| **Structure**  | Always use numbered, prioritized lists |

---

## Workflow Recommendation

> **MANDATORY MUST ATTENTION — NO EXCEPTIONS:** If NOT already in workflow, MUST ATTENTION use ask the user directly to ask user:
>
> 1. **Activate `investigation` workflow** (Recommended) — scout → investigate
> 2. **Execute `$scout` directly** — run this skill standalone

---

## Next Steps

**MANDATORY MUST ATTENTION — NO EXCEPTIONS** after completing, MUST ATTENTION use ask the user directly to present:

- **"$investigate (Recommended)"** — Deep-dive into discovered files
- **"$plan"** — If scouted files sufficient to start planning
- **"Skip, continue manually"** — user decides

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **External Memory:** Complex/lengthy work → write findings incrementally to `plans/reports/`. Prevents context loss.

> **Evidence Gate:** MANDATORY MUST ATTENTION — every claim, finding, recommendation requires `file:line` proof with confidence % (>80% act, <80% verify first).

<!-- SYNC:graph-assisted-investigation -->

> **Graph-Assisted Investigation** — MANDATORY when `.code-graph/graph.db` exists.
>
> **HARD-GATE:** MUST ATTENTION run at least ONE graph command on key files before concluding any investigation.
>
> **Pattern:** Grep finds files → `trace --direction both` reveals full system flow → Grep verifies details
>
> | Task                | Minimum Graph Action                         |
> | ------------------- | -------------------------------------------- |
> | Investigation/Scout | `trace --direction both` on 2-3 entry files  |
> | Fix/Debug           | `callers_of` on buggy function + `tests_for` |
> | Feature/Enhancement | `connections` on files to be modified        |
> | Code Review         | `tests_for` on changed functions             |
> | Blast Radius        | `trace --direction downstream`               |
>
> **CLI:** `python .claude/scripts/code_graph {command} --json`. Use `--node-mode file` first (10-30x less noise), then `--node-mode function` for detail.

<!-- /SYNC:graph-assisted-investigation -->

<!-- SYNC:incremental-persistence -->

> **Incremental Result Persistence** — MANDATORY for all sub-agents or heavy inline steps processing >3 files.
>
> 1. **Before starting:** Create report file `plans/reports/{skill}-{date}-{slug}.md`
> 2. **After each file/section reviewed:** Append findings to report immediately — never hold in memory
> 3. **Return to main agent:** Summary only (per SYNC:subagent-return-contract) with `Full report:` path
> 4. **Main agent:** Reads report file only when resolving specific blockers
>
> **Why:** Context cutoff mid-execution loses ALL in-memory findings. Each disk write survives compaction. Partial results are better than no results.
>
> **Report naming:** `plans/reports/{skill-name}-{YYMMDD}-{HHmm}-{slug}.md`

<!-- /SYNC:incremental-persistence -->

<!-- SYNC:subagent-return-contract -->

> **Sub-Agent Return Contract** — When this skill spawns a sub-agent, the sub-agent MUST return ONLY this structure. Main agent reads only this summary — NEVER requests full sub-agent output inline.
>
> ```markdown
> ## Sub-Agent Result: [skill-name]
>
> Status: ✅ PASS | ⚠️ PARTIAL | ❌ FAIL
> Confidence: [0-100]%
>
> ### Findings (Critical/High only — max 10 bullets)
>
> - [severity] [file:line] [finding]
>
> ### Actions Taken
>
> - [file changed] [what changed]
>
> ### Blockers (if any)
>
> - [blocker description]
>
> Full report: plans/reports/[skill-name]-[date]-[slug].md
> ```
>
> Main agent reads `Full report` file ONLY when: (a) resolving a specific blocker, or (b) building a fix plan.
> Sub-agent writes full report incrementally (per SYNC:incremental-persistence) — not held in memory.
>
> **Context budget** — the return payload is a SUMMARY, not a transcript: ≤10 finding bullets, no raw file contents / full diffs / verbatim logs inline, no re-pasted source. Everything beyond the summary lives in the `Full report` on disk. A sub-agent that would exceed the summary shape MUST write the detail to its report and return only the pointer — the orchestrator's context is the scarce resource the whole map-reduce protects.

<!-- /SYNC:subagent-return-contract -->

<!-- SYNC:nested-task-creation -->

> **Nested Task Expansion Contract** — For workflow-step invocation, the `[Workflow] ...` row is only a parent container; the child skill still creates visible phase tasks.
>
> 1. Call the current task list first. If a matching active parent workflow row exists, set `nested=true` and record `parentTaskId`; otherwise run standalone.
> 2. Create one task per declared phase before phase work. When nested, prefix subjects `[N.M] $skill-name — phase`.
> 3. When nested, link the parent with `TaskUpdate(parentTaskId, addBlockedBy: [childIds])`.
> 4. Orchestrators must pre-expand a child skill's phase list and link the workflow row before invoking that child skill or sub-agent.
> 5. Mark exactly one child `in_progress` before work and `completed` immediately after evidence is written.
> 6. Complete the parent only after all child tasks are completed or explicitly cancelled with reason.
>
> **Blocked until:** the current task list done, child phases created, parent linked when nested, first child marked `in_progress`.

<!-- /SYNC:nested-task-creation -->

<!-- SYNC:project-reference-docs-guide -->

> **Project Reference Docs Gate** — Run after task-tracking bootstrap and before target/source file reads, grep, edits, or analysis. Project docs override generic framework assumptions.
>
> 1. Identify scope: file types, domain area, and operation.
> 2. **Read `docs/project-config.json` first — the project's machine-readable map.** It is the single source of truth for THIS repo (modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns); ground exact paths, run-commands, and conventions on it **before investigating, planning, or coding** — never assume framework defaults (`CLAUDE.md` + reference docs are derived from it). If it — or the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any required reference doc — is missing or stale, auto-run `$project-init` or the narrow route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) first; if Codex mirrors or `AGENTS.md` are stale, ask the user to run `$sync-codex` (never auto-run it).
> 3. Required docs by trigger: always `docs/project-reference/lessons.md`; doc lookup `docs-index-reference.md`; review `code-review-rules.md`; backend/CQRS/API `backend-patterns-reference.md`; domain/entity `domain-entities-reference.md`; frontend/UI `frontend-patterns-reference.md`; styles/design `scss-styling-guide.md` + `design-system/design-system-canonical.md`; integration tests `integration-test-reference.md`; E2E `e2e-test-reference.md`; feature docs/specs `feature-spec-reference.md` + `spec-system-reference.md` + `spec-principles.md`; behavior/public-contract/spec-test-code sync `workflow-spec-test-code-cycle-reference.md`; derived spec index/ERD/reimplementation guides `spec-system-reference.md` + source Feature Specs under `docs/specs/`; architecture/new area `project-structure-reference.md`.
> 4. Read every required doc, then before target work state: `Reference docs read: ... | Not applicable: ...`.
>
> **Ready when:** scope evaluated, `docs/project-config.json` consulted, required docs checked/read or setup route completed, `lessons.md` confirmed, citation emitted.

<!-- /SYNC:project-reference-docs-guide -->

<!-- SYNC:task-tracking-external-report -->

> **Task Tracking & External Report Persistence** — Bootstrap this before execution; then run project-reference doc prefetch before target/source work.
>
> 1. Create a small task breakdown before target file reads, grep, edits, or analysis. On context loss, inspect the current task list first.
> 2. Mark one task `in_progress` before work and `completed` immediately after evidence; never batch transitions.
> 3. For plan/review work, create `plans/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: plans/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:cross-service-check -->

> **Cross-Service Check** — Microservices/event-driven: MANDATORY before concluding investigation, plan, spec, or feature doc. Missing downstream consumer = silent regression.
>
> | Boundary            | Grep terms                                                                      |
> | ------------------- | ------------------------------------------------------------------------------- |
> | Event producers     | `Publish`, `Dispatch`, `Send`, `emit`, `EventBus`, `outbox`, `IntegrationEvent` |
> | Event consumers     | `Consumer`, `EventHandler`, `Subscribe`, `@EventListener`, `inbox`              |
> | Sagas/orchestration | `Saga`, `ProcessManager`, `Choreography`, `Workflow`, `Orchestrator`            |
> | Sync service calls  | HTTP/gRPC calls to/from other services                                          |
> | Shared contracts    | OpenAPI spec, proto, shared DTO — flag breaking changes                         |
> | Data ownership      | Other service reads/writes same table/collection → Shared-DB anti-pattern       |
>
> **Per touchpoint:** owner service · message name · consumers · risk (NONE / ADDITIVE / BREAKING).
>
> **BLOCKED until:** Producers scanned · Consumers scanned · Sagas checked · Contracts reviewed · Breaking-change risk flagged

<!-- /SYNC:cross-service-check -->

<!-- SYNC:rationalization-prevention -->

> **Rationalization Prevention** — AI skips steps via these evasions. Recognize and reject:
>
> | Evasion                      | Rebuttal                                                      |
> | ---------------------------- | ------------------------------------------------------------- |
> | "Too simple for a plan"      | Simple + wrong assumptions = wasted time. Plan anyway.        |
> | "I'll test after"            | RED before GREEN. Write/verify test first.                    |
> | "Already searched"           | Show grep evidence with `file:line`. No proof = no search.    |
> | "Just do it"                 | Still need task tracking. Skip depth, never skip tracking.    |
> | "Just a small fix"           | Small fix in wrong location cascades. Verify file:line first. |
> | "Code is self-explanatory"   | Future readers need evidence trail. Document anyway.          |
> | "Combine steps to save time" | Combined steps dilute focus. Each step has distinct purpose.  |

<!-- /SYNC:rationalization-prevention -->

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

<!-- SYNC:evidence-based-reasoning:reminder -->

**MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:rationalization-prevention:reminder -->

**MUST ATTENTION** never skip steps via evasions. Plan anyway. Test first. Show grep evidence with `file:line`.

<!-- /SYNC:rationalization-prevention:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**MUST ATTENTION** run at least ONE graph command on key files before concluding when `.code-graph/graph.db` exists.

<!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `plans/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:project-reference-docs-guide:reminder -->

- **MANDATORY** Before investigating, planning, or coding, read `docs/project-config.json` (the project map: modules/paths, run-commands, conventions, architecture/workflow rules) + the required project-reference docs, and cite `Reference docs read: ...`.
- **MANDATORY** Always include `lessons.md`; project config + conventions override generic framework defaults.
- **MANDATORY** If project config, root instruction files, or any required reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.

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

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `spawn_agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Deliver a complete, prioritized map of every file relevant to the task — grep + graph combined — so downstream work starts with full coverage and zero blind spots.

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries; each is a signpost to its canonical body above):**

- **Graph-Assisted Investigation:** Run one graph command on key files before concluding.
- **Incremental Persistence:** Append findings to a report file, never hold in memory.
- **Subagent Return Contract:** Sub-agents return summary only, full report on disk.
- **Nested Task Creation:** Expand child phases and link parent when nested.
- **Project Reference Docs:** Read required project docs before target work; cite them.
- **Task Tracking External Report:** Bootstrap task tracking, persist plan findings incrementally.
- **Critical Thinking:** Traced proof per claim, confidence >80% to act.
- **Evidence:** Cite `file:line`; speculation forbidden, <60% do not recommend.
- **Cross-Service Check:** Scan producers, consumers, sagas, contracts for silent regressions.
- **Rationalization Prevention:** Reject step-skipping evasions; show grep evidence.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**MUST ATTENTION** every protocol above is in force for this scout — honor its canonical body, not just the digest line.

**IMPORTANT MUST ATTENTION** execute the FULL step pipeline in declared order — Phase 0 classify scope → Step 1 analyze request (entities/keywords/file-types) → Step 2 spawn parallel `scout` subagents → Step 3 graph-expand 2-3 key files (YOU) → Step 4 low-result check → Step 5 synthesize numbered prioritized list → ask the user directly next step; NEVER skip or merge a step — why: AI forgets the skill's own steps and ships a partial, under-searched map.

**IMPORTANT MUST ATTENTION** run Phase 0 classification BEFORE spawning agents — scope (backend/frontend/full-stack) determines agent count; never spawn the default 3 when the prompt names one layer — why: extra agents waste budget and dilute focus
**IMPORTANT MUST ATTENTION** graph expand is the MANDATORY step that finds what grep cannot — run at least ONE graph command (`connections`/`callers_of`/`trace --direction both`) on 2-3 key files when `.code-graph/graph.db` exists; NEVER skip it — why: structural relationships > text matches, and sub-agents cannot run graph — only you can
**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = DO NOT recommend — why: speculation seeds blind spots downstream work inherits
**MUST ATTENTION** stay in DISCOVERY lane — return prioritized file paths fast (3-5 min), no content deep-dives; that is `investigate`'s job — why: scope creep into analysis breaks the 3-5 min budget and duplicates the next step
**MUST ATTENTION** if <5 files found, re-examine keywords and run a second pass with broader synonyms BEFORE synthesizing — why: a thin result is an under-searched result, not a small surface
**MUST ATTENTION** run a post-grep graph trace whenever grep surfaces an entry-point file (entity, command, query, handler, controller, bus message, component, store, api-service) — trace reveals callers/consumers/event chains/tests grep cannot find — why: missing a downstream consumer = silent regression for the next step
**MUST ATTENTION** spawn `scout`/`scout-external` subagents — NOT built-in `Explore` — why: only the custom agents carry graph CLI knowledge + Bash access
**MUST ATTENTION** sub-agents return a SUMMARY only (≤10 finding bullets + `Full report:` path), writing full findings incrementally to `plans/reports/` — NEVER hold all results in memory or request full sub-agent output inline — why: context cutoff mid-run loses every in-memory finding; disk writes survive compaction
**MUST ATTENTION** bootstrap task tracking BEFORE target work — the current task list first on context loss, one task `in_progress` at a time, expand child phases when nested under a workflow row — why: compaction wipes prior-work memory; resume from state, never duplicate
**MUST ATTENTION** read required project-reference docs (always `lessons.md`; `domain-entities-reference.md` for business entities) BEFORE searching — project conventions override generic framework assumptions
**MUST ATTENTION** use ask the user directly after completing (investigation workflow vs standalone, then $investigate vs $plan vs skip) — NEVER auto-proceed to the next step — why: the user owns scope; assuming standalone skips the workflow they wanted
**MUST ATTENTION** for non-trivial bug/regression scouts, surface End-to-Start trace candidates (reader → storage → writer → consumer → producer) and enumerate every feeder path — why: starting at the first suspicious file collapses multiple producers into one false "flow"

**Anti-Rationalization:**

| Evasion                                | Rebuttal                                                                    |
| -------------------------------------- | --------------------------------------------------------------------------- |
| "Graph step too slow, skip it"         | Graph finds what 50 greps miss. NEVER skip when `graph.db` exists.          |
| "Only 2 files, no need for report"     | Incremental write costs nothing. Skip = context loss risk.                  |
| "Scope obvious, skip Phase 0"          | Wrong agent set = missed files. Classify scope first, every time.           |
| "Already searched, results complete"   | Show grep + graph evidence with `file:line`. No proof = incomplete.         |
| "Use Explore, it's a built-in"         | Explore has NO graph awareness. Spawn `scout`/`scout-external` only.        |
| "<5 files, surface is just small"      | Thin result = under-searched. Broaden synonyms and re-pass before synth.    |
| "I'll deep-dive these files now"       | Discovery only — paths fast, no analysis. Deep-dive is `investigate`'s job. |
| "Simple scout, skip workflow question" | User decides scope. NEVER assume standalone is acceptable.                  |

**IMPORTANT MUST ATTENTION** Phase 0 classify first · graph expand is MANDATORY (never skip when `graph.db` exists) · cite `file:line` with confidence >80% — these three survive any long context, anchored top and bottom.

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
