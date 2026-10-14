---
name: scan
description: '[Documentation] Use when scanning the codebase to (re)generate ONE project-reference doc. Parameterized by `--target=<key>`: project-structure | backend-patterns | frontend-patterns | scss-styling | design-system | code-review-rules | domain-entities | feature-spec | docs-index | e2e-tests | integration-tests | seed-test-data | ui-system. Shared 4-phase scan engine; per-target detail lives in references/targets.md. `ui-system` is an orchestrator meta-target (`kind: orchestrator`) that runs the 3 UI child scans in parallel instead of the 4-phase engine.'
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

## Quick Summary

**Goal:** Scan the codebase for ONE target reference doc and surgically (re)populate it with actual patterns — every example from real project files with `file:line`. The 4-phase engine below is shared; the per-target data (which doc, how many sub-agents, what to detect, what sections to write, what NOT to do) comes from the target's entry in `references/targets.md`.

**Workflow:**

1. **Resolve target** — Read `--target=<key>`; load its entry from `references/targets.md`
2. **Assess** — Read target doc, detect init vs sync (vs force) mode, run the target's Phase-0 detection table(s)
3. **Scan** — Launch the target's sub-agents in parallel; discover patterns with `file:line` evidence
4. **Report** — Write structured findings to report file (incremental, not batched)
5. **Generate** — Surgical update of the reference doc from report (apply target's Target Sections + Content Rules)
6. **Verify** — Multi-round fresh-eyes review validates examples and coverage; then prompt-enhance the doc

**Key Rules:**

**MUST ATTENTION** resolve `--target` FIRST and load its manifest entry — every target-specific behavior (doc path, sub-agent count/roles, Phase-0 tables, Target Sections, Content Rules, special gates, anti-rationalization rows) comes from that entry, NOT from memory
**MUST ATTENTION** detect framework/type FIRST (per the target's Phase-0 table) — scan strategy derives from detection, never hardcoded
**MUST ATTENTION** every code example from actual project files with `file:line` — NEVER fabricate
**MUST ATTENTION** run graph command on key files before concluding — grep finds text, graph finds structure

- Surgical update only — NEVER rewrite entire doc, NEVER remove a section without evidence it's obsolete
- Some targets OVERRIDE shared output rules or add a branch (e.g. `feature-spec` intentionally includes directory trees; `design-system` has an init-mode Authoring branch with a sentinel-removal step). Always honor the target entry's "Content Rules / exceptions" and "Special slivers".

---

# Scan (parameterized reference-doc scanner)

## Phase 0.0: Resolve Target (BLOCKING — do this before anything else)

1. Parse `--target=<key>` from the invocation (e.g. `$scan --target=backend-patterns`). Accept the key with or without the `--target=` prefix.
2. If no target is supplied or the key is unknown → **STOP** and list the valid keys (see frontmatter / `references/targets.md`), ask the user which target to scan.
3. **Read the target's entry in `references/targets.md`.** That entry is the single source of truth for this run and supplies:
    - `doc` — the reference doc path this scan writes
    - `description` — the doc's purpose blurb
    - `sub-agents` — exact count + role of each parallel sub-agent
    - **Phase 0 detection** — the classification table(s) and BLOCKING gates for this target
    - **Sub-agent Think scopes** — each sub-agent's Think question(s) + scan-target bullets
    - **Target Sections** — the output doc's section list
    - **Content Rules / exceptions** — including any override of the shared output-quality rules
    - **Special slivers** — target-unique BLOCKING gates, Authoring branches, sentinel removals, whitelist scopes
    - **Anti-Rationalization rows** — target-specific evasions to refuse
    - **prompt-enhance** — the final `$prompt-enhance <doc>` step
4. **Orchestrator branch (BLOCKING check):** if the loaded entry is marked **`kind: orchestrator`** (e.g. `ui-system`), it does NOT run the 4-phase doc engine. SKIP Phases 0–4 below and instead follow the entry's **Orchestration Procedure** (pre-flight gate → launch the child `--target=` scans in parallel → verify each child doc has real content → summarize). Standard (single-doc scanner) targets ignore this step and continue with the shared engine below.

> Everything below is the SHARED engine (standard single-doc scanner targets). Wherever it says "the target entry," read the loaded manifest entry — do not assume values from another target. **Orchestrator-kind targets do not use this engine** — they run their entry's Orchestration Procedure instead.

## Phase 0: Classify & Assess

**Before any other step**, run in parallel:

1. Read the target's `doc`.
    - Detect mode: **Init** (placeholder — headings only / sentinel present) or **Sync** (populated). Some targets add a **Force** mode (user says "rebuild"/"reset" → treat as Init even if the doc exists) — honor it if the target entry defines it.
    - In Sync mode: list already-documented sections → skip re-scanning those unless staleness suspected.
2. Run the target entry's **Phase 0 detection** table(s) — detect framework / system type / architecture exactly as that table specifies. This is BLOCKING: grep terms and sub-agent scope derive from detection.
3. Load relevant paths from `docs/project-config.json` (e.g. `contextGroups`/`modules`/`designSystem`/`e2eTesting`/`integrationTestVerify`) if the target entry references them.
4. Run a graph command on the primary entry point: `python .claude/scripts/code_graph trace <entry-file> --direction both --json` (when `.code-graph/graph.db` exists).

**Evidence gate:** Confidence <60% on the target's primary detection axis → report uncertainty, DO NOT proceed with detection-specific scanning (or fall back exactly as the target entry's evidence-gate instruction specifies, e.g. "proceed with Agent 1 only").

## Phase 1: Plan Scan Strategy

From the detected framework/type, derive the concrete patterns to search (naming conventions, base classes, config locations). NEVER assume these — derive from actual file evidence.

**Create task tracking entries** for each sub-agent listed in the target entry and for each phase before proceeding.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch the **N general-purpose sub-agents** defined in the target entry (count + roles vary per target — e.g. backend-patterns/domain-entities use 4, project-structure/frontend-patterns/design-system/code-review-rules/e2e-tests use 3, scss-styling/feature-spec/integration-tests use 2, docs-index uses a single main-agent scan + a fresh-eyes verifier). Give each sub-agent its **Think scope** + scan-target bullets verbatim from the entry. Each sub-agent MUST:

- Write findings incrementally after each file/section — NEVER batch at end
- Cite `file:line` for every pattern example
- Confidence: >80% document as pattern; 60-80% document as "observed (unverified)"; <60% omit

Each worker writes a **unique shard** under `plans/reports/scan-{target}-{YYMMDD}-{HHMM}/`; workers never append to the same report. After the barrier, the main agent reads and validates every shard and is the **sole writer** of `plans/reports/scan-{target}-{YYMMDD}-{HHMM}-report.md`.

> Honor any **conditional / ordered** sub-agents from the entry (e.g. an Anti-Pattern agent that runs AFTER the discovery agents; a Cross-Service agent that runs ONLY for microservices; a BDD agent that runs ONLY if a BDD framework is detected). Honor any **CRITICAL security flag** the entry defines (e.g. hardcoded credentials).

## Phase 3: Analyze & Generate

Read the full report. Apply the fresh-eyes protocol:

**Round 1 (main agent):** Build section drafts from report findings, using the target entry's **Target Sections** + **Content Rules / exceptions**.

**Round 2 (fresh sub-agent, zero memory of Round 1):** Sub-agent re-reads report + draft doc independently and checks (apply the target entry's Round-2 verification specifics):

- Does every code example match an actual existing file (Glob verify)?
- Do class/token/variable names in examples match actual declarations (Grep verify)?
- Are required sections (Anti-Patterns / Coverage Report / Gap Analysis / M1-M2 Compliance / etc. as the target mandates) populated?
- Coverage gaps: which Target Sections have no examples?

**Round 3 only if Round 2 finds issues.** Max 3 rounds → escalate to user if unresolved. (Clean Round 1 ends the scan; fresh-eyes is mandatory only after issues are found and fixed.)

> **Authoring branch (init mode):** if the target entry defines one (e.g. `design-system` authors the canonical doc + token `.scss`), follow it exactly — including any **sentinel removal** (e.g. "First: REMOVE `PLACEHOLDER_MARKER_SCSS`") and regen-marker prepend.

## Phase 4: Write & Verify

1. Write the updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top.
2. Surgical update only — preserve sections with no staleness, update only diverged sections; preserve manual annotations.
3. Verify (Glob check): **ALL** code example file paths exist — not just a sample of 5.
4. Verify (Grep check): class/token/variable names in examples match actual declarations.
5. Verify any target-mandated section is real, not hypothetical (Anti-Patterns / Coverage gaps / M1-M2 leaks / ports-from-config / etc.).
6. Run a graph command on 2-3 key files to validate call-chain accuracy.
7. Report: sections updated / unchanged / coverage gaps / violations found.

> **Output-rule overrides:** apply the target entry's "Content Rules / exceptions" — e.g. `feature-spec` intentionally INCLUDES a directory tree (overriding the shared no-trees rule); `docs-index` intentionally OUTPUTS glob-verified counts (its counts are the deliverable); `e2e-tests`/`integration-tests` forbid hardcoded counts and use grep-expression statistics.

<!-- SCAN:prompt-enhance-final-step -->

## Final Step: Enhance Scanned Doc (MANDATORY)

**MUST ATTENTION** after the doc is written and verified, create a REQUIRED final todo task and run `$prompt-enhance <the target entry's doc>` — why: this reference doc is injected into AI context on every downstream session; `$prompt-enhance`'s default `--op=enhance` keeps it as concise as possible while staying valuable enough for AI (caveman compression + attention anchoring — top/bottom Goal, inline READ summaries, token density). A scan is NOT complete until its doc is prompt-enhanced.

**task tracking (required, last task):** `Run $prompt-enhance <target doc> on the scanned doc`

<!-- /SCAN:prompt-enhance-final-step -->

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks per file read. Prevents context loss from long files. Simple tasks: ask user whether to skip.

**Prerequisites:** **MUST ATTENTION READ** before executing:

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:scan-and-update-reference-doc -->

> **Scan & Update Reference Doc** — Surgical updates only, never full rewrite.
>
> 1. **Read existing doc** first — understand current structure and manual annotations
> 2. **Detect mode:** Placeholder (only headings, no content) → Init mode. Has content → Sync mode.
> 3. **Scan codebase** for current state (grep/glob for patterns, counts, file paths)
> 4. **Diff** findings vs doc content — identify stale sections only
> 5. **Update ONLY** sections where code diverged from doc. Preserve manual annotations.
> 6. **Update metadata** (date, counts, version) in frontmatter or header
> 7. **NEVER** rewrite entire doc. NEVER remove sections without evidence they're obsolete.

<!-- /SYNC:scan-and-update-reference-doc -->

<!-- SYNC:output-quality-principles -->

> **Output Quality** — Token efficiency without sacrificing quality.
>
> 1. No inventories/counts — AI can `grep | wc -l`. Counts go stale instantly
> 2. No directory trees — AI can `glob`/`ls`. Use 1-line path conventions
> 3. No TOCs — AI reads linearly. TOC wastes tokens
> 4. No examples that repeat what rules say — one example only if non-obvious
> 5. Lead with answer, not reasoning. Skip filler words and preamble
> 6. Sacrifice grammar for concision in reports
> 7. Unresolved questions at end, if any

<!-- /SYNC:output-quality-principles -->

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

<!-- SYNC:scan-and-update-reference-doc:reminder -->

**IMPORTANT MUST ATTENTION** read existing doc first, scan codebase, diff, surgical update only. Never rewrite entire doc.

<!-- /SYNC:scan-and-update-reference-doc:reminder -->

<!-- SYNC:output-quality-principles:reminder -->

**IMPORTANT MUST ATTENTION** output quality: no counts/trees/TOCs, 1 example per pattern, lead with answer. (Per-target exceptions in the manifest entry override this — e.g. feature-spec trees, docs-index counts.)

<!-- /SYNC:output-quality-principles:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

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

**IMPORTANT MUST ATTENTION** resolve `--target` and load its manifest entry FIRST — never scan from memory of "what a backend/frontend/design scan does"

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Critical Thinking:** traced `file:line` proof per claim; confidence >80% to act.
- **Scan & Update Doc:** read existing doc, diff, surgical update only — never full rewrite.
- **Output Quality:** no counts/trees/TOCs; 1 example per pattern; lead with answer.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**IMPORTANT MUST ATTENTION Final Step:** run `$prompt-enhance <target doc>` as the REQUIRED last todo task — never end the scan without enhancing the doc it just wrote
**IMPORTANT MUST ATTENTION** break work into small task tracking tasks BEFORE starting — one task per sub-agent, one per phase
**IMPORTANT MUST ATTENTION** detect framework/type FIRST in Phase 0 — all grep terms derive from detection, never hardcoded
**IMPORTANT MUST ATTENTION** cite `file:line` for every pattern (confidence >80% to document; <60% omit)
**IMPORTANT MUST ATTENTION** run graph command on key files — grep finds text, graph finds structure (callers, event chains, blast radius)
**IMPORTANT MUST ATTENTION** sub-agents write findings incrementally after each file — NEVER batch at end (context loss)
**IMPORTANT MUST ATTENTION** read existing doc FIRST, diff findings, surgical update only — NEVER rewrite entire doc
**IMPORTANT MUST ATTENTION** multi-round fresh-eyes review — main agent rationalizes its own mistakes; Round 2 sub-agent catches what main agent dismissed
**IMPORTANT MUST ATTENTION** honor the target entry's Content-Rule exceptions, Special slivers, and Anti-Rationalization rows — they encode why this target differs from the others

**Anti-Rationalization (shared — the target entry adds its own rows):**

| Evasion                                                       | Rebuttal                                                                                              |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| "I know what a `<target>` scan does, skip the manifest entry" | The entry holds the BLOCKING gates, sub-agent count, and exceptions — scanning from memory drops them |
| "Framework/type already known, skip Phase 0 detection"        | Phase 0 is BLOCKING — derive grep terms from evidence, not assumption                                 |
| "Doc has content, skip re-read"                               | Show section list extracted from doc as proof of re-read                                              |
| "Examples look right"                                         | Glob-verify ALL file paths + Grep-verify ALL names — looking right ≠ verified                         |
| "Round 2 review not needed for small scan"                    | Main agent rationalizes own mistakes. Fresh sub-agent is non-negotiable.                              |

**[TASK-PLANNING]** Before acting, analyze task scope and break into small todo tasks and sub-tasks using task tracking.

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
