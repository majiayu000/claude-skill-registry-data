---
name: cm-start
description: Start the CM Workflow to execute your objective from idea to production code.
token_budget: 1000
compressed: true
deprecated: false
---

# Command: `/cm-start [your objective]`

## TL;DR
- **Use to** kick off a CM session — entry point
- **Detects**: stack (Phase 2), suggests skills, reads continuity + learnings
- **Autonomy**: selects project level from evidence; clear objectives do not need level confirmation
- **Next**: cm-brainstorm-idea or cm-planning

> **Role: Workflow Orchestrator** — You assess complexity, select the right workflow depth, and drive execution from objective to production code.

Follow [`_shared/autonomy-policy.md`](../_shared/autonomy-policy.md). Its decision table controls confirmations across this workflow.

When this workflow is called, the AI Assistant should execute the following action sequence in the spirit of the **CodyMaster Kit**:

0. **Load Working Memory:**
    Per `_shared/helpers.md#Load-Working-Memory` — **use Smart Spine order:**
    1. Check `.cm/context-bus.json` → any active pipeline? any prior skill output to reuse?
    2. Load L0 indexes: `learnings-index.md` (~100 tok) + `skeleton-index.md` (~500 tok)
    3. Scope-filter learnings via `cm_query` — only load what matches current objective
    4. Read `CONTINUITY.md` → set Active Goal to the new objective
    5. Run token budget check: `cm continuity budget` → confirm no category is over soft limit

    > ⚡ Total context load: ~700 tokens. Full load used to be ~3,200.
    > Only escalate to L2 (full files) if L0 index explicitly flags a match.
0.5. **Skill Coverage Check (Adaptive Discovery):**
    - Scan the objective for technologies, frameworks, or patterns mentioned
    - Cross-reference with `cm-skill-index` Layer 1 triggers
    - If gap detected → trigger Discovery Loop from `cm-skill-index`:
      `npx skills find "{keyword}"` → review → ask user → install if approved
    - Log any discovered skills to `.cm-skills-log.json`

0.6. **Stack & Tier Detection (Phase 2):**
    - `cm stack detect --write` → writes `.cm/project-skills.md` (frameworks + suggested skills)
    - `cm tier classify --write` → writes `.cm/project-tier.md` (LITE/STANDARD/PROFESSIONAL/ENTERPRISE)
    - The tier sets the default Vibecoding mode and **adaptive depth**:
      - LITE/STANDARD → render skill TL;DR only
      - PROFESSIONAL/ENTERPRISE → render full protocol
    - Inject the suggested-skills list into the skill chain shortlist
    - These reports are token-light (~300 tok combined) and skipped if files exist and are <24h old

0.7. **Code Intelligence Setup (cm-codeintell):**
    - **ALWAYS:** Run skeleton indexer → `bash scripts/index-codebase.sh` → `.cm/skeleton.md`
    - Read `.cm/skeleton.md` (~5K tokens) → instant codebase understanding
    - Count source files → determine intelligence level (MINIMAL/LITE/STANDARD/FULL)
    - IF level >= LITE: generate architecture diagram → `.cm/architecture.mmd`
    - IF level >= STANDARD: check CodeGraph → `codegraph status` → index if needed
    - IF level >= STANDARD: also check qmd (cm-deep-search) for existing semantic vector databases and initialize/update if needed.
    - Log intelligence level to `CONTINUITY.md`

1. **Understand Requirements (Planning & JTBD):**
    - Read the objective provided in the `/cm-start` command.
    - Analyze requirements. Ask once only when ambiguity would materially change scope; include a recommendation and default.
    - Consider multi-language support (i18n) from the start if the project requires it.

2. **Detect Project Level:**
    Per `_shared/helpers.md#Project-Level-Detection`
    - Select the L0/L1/L2/L3 project level from objective and repository evidence
    - State the detected level and recommended skill chain, then continue without confirmation when the objective is clear
    - Allow the user to override the level at any time; an override applies from the next safe boundary
    - Do not treat level selection as the plan-to-execution approval boundary

3. **Execute Based on Level:**

    **L0 (Micro):** Code + Test only
    - Skip planning. A clear, reversible micro task may proceed with zero approval.
    - Apply `cm-tdd` directly → `cm-quality-gate`

    **L1 (Small):** Planning lite → Code → Deploy
    - Apply `cm-planning` (lightweight implementation plan)
    - For meaningful code changes, request one plan approval that grants scoped execution authorization
    - Apply `cm-tdd` + `cm-execution` → `cm-quality-gate`

    **L2 (Medium):** Full analysis flow
    - Init OpenSpec (create `openspec/changes/[initiative-name]/` folder and artifacts manually)
    - Apply `cm-brainstorm-idea` if problem is ambiguous
    - Apply `cm-planning` (full implementation plan with OpenSpec `tasks.md`)
    - Request one plan approval that grants scoped execution authorization
    - Create `cm-tasks.json` from `tasks.md` → launch RARV autonomous execution
    - Apply `cm-quality-gate` → `cm-safe-deploy`

    **L3 (Large):** Full + PRD + Architecture + Sprint
    - Init OpenSpec (create `openspec/changes/[initiative-name]/` folder and artifacts manually)
    - Apply `cm-brainstorm-idea` (mandatory)
    - Apply `cm-planning` with FR/NFR requirement tracing
    - Request one plan approval that grants scoped execution authorization
    - Sprint planning → `openspec/changes/[objective]/tasks.md` sync with `cm-tasks.json`
    - Apply `cm-execution` (Mode E: TRIZ-Parallel for speed)
    - Apply `cm-quality-gate` → `cm-safe-deploy`

3. **Track Progress:**
    - Create `openspec/changes/[objective]/tasks.md` (for standardized spec tracking)
    - Create or update `cm-tasks.json` (for autonomous agent execution)
    - Suggest `/cm-dashboard` for visual tracking
    - Suggest `/cm-status` for quick terminal summary

4. **Complete:**
    Per `_shared/helpers.md#Update-Continuity`
    - Record any new learnings or decisions made during this workflow
    - If inside a skill chain: `cm continuity bus` → verify context bus reflects completed step
    - Refresh L0 indexes: `cm continuity index` (auto-runs on `addLearning`, manual refresh here)
> **Note for AI:** If this is a brand new project, suggest running `cm-project-bootstrap` first.
> If the working environment has a risk of accidentally switching accounts/projects, remind about `cm-identity-guard` (Per `_shared/helpers.md#Identity-Check`).
