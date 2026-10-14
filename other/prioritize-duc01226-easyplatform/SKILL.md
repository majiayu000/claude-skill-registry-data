---
name: prioritize
description: '[Project Management] Use when you need to prioritize backlog items using RICE, MoSCoW, or Value-Effort frameworks.'
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

**Goal:** Produce a defensible ranked ordering of 3+ backlog items using RICE, MoSCoW, or Value-Effort frameworks so the team works highest-value items first — every rank backed by a score and tech-agnostic rationale (value/effort/risk/impact).

**Summary:** PURPOSE — rank 3+ backlog items so the team works highest-value first; every rank = a score + tech-agnostic rationale. The main steps/tasks, in order:

- **Step 1-2 Collect & Select** — require 3+ items FIRST (fewer → discuss directly, NEVER force a framework); pick framework by decision tree — RICE = quantitative data exists, MoSCoW = stakeholder must/should/could alignment, Value-Effort 2x2 = quick call; default RICE when unsure.
- **Step 3 Score** — apply the EXACT framework formula (RICE = Reach×Impact×Confidence ÷ Effort, fixed Impact/Confidence scales, story-point Effort); NEVER invent ad-hoc scores.
- **Step 4-5 Rank & Output** — rank descending (RICE) / by band (MoSCoW) / by quadrant (V-E); emit prioritized table with scores + Do-first/Plan-next/Defer recommendations.
- **Step 6 Propagate (MANDATORY when PBI files exist)** — write rank (1-999, ascending) + priority label back into EACH PBI's frontmatter; `pbi-mockup`/`feature-presentation` read priority from there.
- **Cross-cutting — tech-agnostic (M1):** justify every rank by value/effort/risk/business impact, NEVER by named stack/framework/pattern. **Tie gate:** near-tie (top-2 RICE within 15%, same-band MoSCoW overlap, flagged stakeholder disagreement) → ask the user directly offering `$llm-council`; else end without prompting.

**Workflow:**

1. **Collect Items** — read from files or parse inline list (minimum 3 items)
2. **Select Framework** — RICE (quantitative), MoSCoW (stakeholder alignment), Value-Effort (quick decision)
3. **Score Each Item** — apply framework criteria and calculate scores
4. **Rank & Report** — output prioritized table with rationale and recommendations
5. **Propagate Priority** — IF PBI files exist → MANDATORY: write `rank` + `priority` label back into EACH PBI frontmatter
6. **Tie Gate** — near-tie → ask the user directly (`$llm-council` vs accept); else end without prompting

**Key Rules:**

- Minimum 3 items required; fewer than 3 should be discussed directly
- Default to RICE if unsure; ask user if ambiguous
- Optionally update PBI file priority fields after ranking
- **Tech-agnostic rationale (M1):** See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria. Justify every ranking by value, effort, risk, and business impact — NOT by implementation technology. Rationale prose stays tech-agnostic per `docs/project-reference/spec-principles.md` §3: no framework/product/language/design-pattern names; effort may cite story points and relative complexity, never a named stack.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Backlog Prioritization

Order backlog items using data-driven frameworks → ranked list with scores and rationale.

## When to Use

- Sprint planning needs ordered backlog (3+ items to rank)
- Stakeholders need priority ranking with justification
- Feature roadmap ordering with objective criteria
- Comparing competing features or initiatives

## When NOT to Use

- Fewer than 3 items (discuss directly)
- Creating PBIs or writing stories -- use `product-owner` or `story`
- Full product strategy -- use `product-owner`
- Project status tracking -- use `project-manager`

## Prerequisites

- List of 3+ backlog items (PBIs, features, user stories)
- IF items exist as files: read from `team-artifacts/pbis/` or user-provided path
- IF items provided inline: use provided descriptions

## Workflow

1. **Collect items** to prioritize
    - IF file path provided -> read items from files
    - IF inline list -> parse items from user message
    - IF fewer than 3 items -> ask user for more or suggest direct discussion

2. **Select framework** using decision tree:

    ```
    IF quantitative data available (reach, metrics)  -> RICE
    IF stakeholder alignment needed (must/should/could) -> MoSCoW
    IF quick decision needed (2 axes only)            -> Value-Effort 2x2
    IF user specifies framework                       -> use that framework
    IF unsure                                         -> ask user, default RICE
    ```

3. **Score each item** using selected framework:

    **RICE:**

    ```
    Score = (Reach x Impact x Confidence) / Effort

    Reach:      Users affected per quarter (number)
    Impact:     0.25 (minimal) | 0.5 (low) | 1 (medium) | 2 (high) | 3 (massive)
    Confidence: 0.5 (low) | 0.8 (medium) | 1.0 (high)
    Effort:     Story points (1, 2, 3, 5, 8, 13, 21)
    ```

    **MoSCoW:**

    ```
    Must Have:   Critical for release, non-negotiable
    Should Have: Important but not vital, workarounds exist
    Could Have:  Desirable, include if capacity allows
    Won't Have:  Out of scope for this cycle
    ```

    **Value-Effort 2x2:**

    ```
    High Value + Low Effort  = Quick Wins    (do first)
    High Value + High Effort = Strategic     (plan carefully)
    Low Value  + Low Effort  = Fill-ins      (if time permits)
    Low Value  + High Effort = Time Sinks    (avoid)
    ```

4. **Rank items** by score (descending for RICE, category for MoSCoW, quadrant for V-E)

5. **Output** prioritized list with scores and rationale

6. **IF PBI files exist** -> **MANDATORY priority propagation**: write the resulting priority back into EACH PBI's frontmatter — both the numeric `rank` (1-999, ascending) and the `priority` label (e.g. Must Have / Should Have / Could Have / Won't Have, or the framework's category). Never leave this optional when PBI files exist: a PBI without its priority is incomplete, and downstream consumers (`pbi-mockup` header badge, `feature-presentation` Scope & backlog slide) read priority FROM the PBI frontmatter. Update every ranked PBI, not just the standalone backlog file.

## Output Format

```markdown
## Prioritized Backlog

**Framework:** [RICE | MoSCoW | Value-Effort]
**Date:** [YYMMDD]
**Items scored:** [count]

### Rankings

| Rank | Item      | Score | Rationale                                           |
| ---- | --------- | ----- | --------------------------------------------------- |
| 1    | Feature A | 45.0  | High reach (5000), high impact (3), high confidence |
| 2    | Feature B | 12.0  | Medium reach (2000), medium impact, low effort      |
| 3    | Feature C | 2.5   | Low reach, minimal impact, high effort              |

### Recommendations

- **Do first:** [top items]
- **Plan next:** [medium items]
- **Defer:** [low items with reasoning]
```

## Examples

### Example 1: RICE scoring of 5 features

**Input:** "Prioritize: SSO login, dark mode, export to PDF, email notifications, bulk import"

**Output:**

| Rank | Feature             | Reach | Impact | Conf | Effort | RICE |
| ---- | ------------------- | ----- | ------ | ---- | ------ | ---- |
| 1    | Email notifications | 5000  | 2      | 0.8  | 1      | 8000 |
| 2    | SSO login           | 2000  | 3      | 0.8  | 3      | 1600 |
| 3    | Bulk import         | 500   | 2      | 1.0  | 1      | 1000 |
| 4    | Export to PDF       | 1000  | 1      | 0.8  | 2      | 400  |
| 5    | Dark mode           | 3000  | 0.5    | 0.5  | 2      | 375  |

### Example 2: MoSCoW categorization

**Input:** "Categorize for Q1 release: payment gateway, admin dashboard redesign, API rate limiting, user avatars, audit logs"

**Output:**

- **Must Have:** Payment gateway (revenue-critical), API rate limiting (security)
- **Should Have:** Audit logs (compliance, workaround exists with manual exports)
- **Could Have:** Admin dashboard redesign (improves efficiency but current works)
- **Won't Have:** User avatars (nice-to-have, defer to Q2)

## Optional Escalation: $llm-council on Ties

**Gate evaluation:** After producing prioritized backlog (per `## Workflow` step output), inspect ranking output:

- Top-2 RICE scores within 15% of each other → gate fires
- Explicit MoSCoW tie (≥2 items in same Must/Should/Could band with material scope overlap) → gate fires
- Multi-stakeholder disagreement flagged in input → gate fires
- None of the above → gate does NOT fire; skill ends without prompting

**MANDATORY ATTENTION** — when the gate fires, you MUST use ask the user directly to present these options (identical preamble pattern to architecture-design's `## Next Steps` MANDATORY ATTENTION block):

- **"Escalate to $llm-council (Recommended)"** — Tie/disagreement detected. Run 11 sub-agent council (5 advisors + 5 reviewers + chairman). Council's Contrarian + Outsider lenses are well-suited to multi-PBI ranking ties. Cheaper alternatives: `$why-review`, `$plan-validate` (use these instead if the tie is narrow but stakes are routine).
- **"Skip — accept current ranking"** — Acknowledge the tie; proceed with current ranking.

If gate does NOT fire, the prioritization decision stands; do NOT prompt.

## Related Skills

| Skill             | When to use instead                |
| ----------------- | ---------------------------------- |
| `product-owner`   | Full product management workflow   |
| `story`           | Breaking PBIs into user stories    |
| `refine`          | Refining ideas into PBIs           |
| `project-manager` | Sprint/project status and tracking |

---

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

- **IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
- **IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
- **IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
- **IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

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

- **IMPORTANT MUST ATTENTION Goal:** produce a defensible ranked ordering of 3+ backlog items via RICE/MoSCoW/Value-Effort so the team works highest-value items first — every rank backed by a score and tech-agnostic rationale (value/effort/risk/impact)

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Critical Thinking:** ALWAYS trace `file:line` proof for every claim, confidence >80% to act, NEVER present guess as fact.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

- **IMPORTANT MUST ATTENTION** require 3+ items BEFORE ranking; fewer than 3 → discuss directly, NEVER force a framework — why: ranking 1-2 items adds ceremony without signal
- **IMPORTANT MUST ATTENTION** select the framework by the decision tree — RICE for quantitative data, MoSCoW for stakeholder must/should/could alignment, Value-Effort 2x2 for a quick call; default RICE when unsure, ask the user when ambiguous — why: matching framework to the decision type is what makes the ranking defensible
- **IMPORTANT MUST ATTENTION** emit the prioritized table (scores + rationale) AND Do-first/Plan-next/Defer recommendations — NEVER stop at raw scores — why: the consumable output is the ranked table plus an action call, not a number column
- **IMPORTANT MUST ATTENTION** keep every rationale tech-agnostic per M1 — justify by value/effort/risk/business impact, NEVER by named stack/framework/product/language/design-pattern; effort may cite story points + relative complexity only — why: spec-principles §3 BLOCKING, a tech-named rationale leaks implementation into a priority call
- **IMPORTANT MUST ATTENTION** score with the EXACT framework formula (RICE = Reach×Impact×Confidence ÷ Effort, fixed Impact/Confidence scales, story-point Effort), then rank descending (RICE) / by band (MoSCoW) / by quadrant (V-E) — NEVER invent ad-hoc scores — why: a defensible rank needs a reproducible number
- **IMPORTANT MUST ATTENTION** on a near-tie (top-2 RICE within 15%, same-band MoSCoW overlap, flagged stakeholder disagreement) the gate FIRES — use ask the user directly to offer `$llm-council` escalation vs. accepting the ranking; if the gate does NOT fire, end WITHOUT prompting — why: tie-breaking is a judgment call the user owns, but a clear winner needs no interruption
- **IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting; mark one `in_progress`, `completed` immediately after evidence
- **IMPORTANT MUST ATTENTION** search codebase/artifacts for 3+ similar patterns before creating new structure; evaluate pattern FIT (same constraints/scope) before copying a nearby example — why: closest example ≠ matching preconditions
- **IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act, <60% DO NOT recommend); NEVER present a guess as fact
- **IMPORTANT MUST ATTENTION** when PBI files exist, propagating the ranking into EACH PBI's frontmatter (numeric `rank` 1-999 + `priority` label) is MANDATORY, not optional — do it after ranking; grep downstream consumers before changing any priority field — why: downstream consumers (`pbi-mockup` header, `feature-presentation` Scope & backlog slide) read priority from PBI frontmatter, and stale/absent priority refs cascade silently
- **IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**Anti-Rationalization:**

| Evasion                                                | Rebuttal                                                                                                                                           |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Only 2 items, just rank them"                         | Below the 3-item floor → discuss directly; a framework adds ceremony, not signal                                                                   |
| "I'll cite the framework in the rationale"             | Tech-agnostic per M1 — justify by value/effort/risk only, never by named stack                                                                     |
| "Scores are close enough, I'll pick"                   | Near-tie fires the gate → ask the user directly for `$llm-council`, never silently break                                                           |
| "RICE feels right, skip the formula"                   | Apply the EXACT formula with fixed scales — a defensible rank needs a number                                                                       |
| "The backlog file has the ranking, PBIs don't need it" | When PBI files exist, priority write-back to each PBI frontmatter is MANDATORY — mockup + presentation read priority from the PBI, not the backlog |
| "Already know the patterns"                            | Show `file:line` evidence — no proof = no search                                                                                                   |

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->
<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

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
