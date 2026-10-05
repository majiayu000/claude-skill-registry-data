---
name: mk:agent-detector
description: Detects task agent and complexity tier at Phase 0 orient. Invoked first in every workflow. Provider adapters select any model/runtime policy. NOT for runtime agent routing inside a single skill (see orchestration-rules.md).
triggers:
  - every message
  - always first
allowed-tools:
  - Read
source: aura-frog
keywords:
  - agent-routing
  - model-tier
  - phase-0-orient
  - auto-detect
  - complexity-classification
when_to_use: Auto-invoked at Phase 0 by orchestrator to assign agent + model tier. Not user-callable directly.
user-invocable: false
owner: lifecycle
criticality: medium
status: active
runtime: claude-code
adapted_for: claude-code
requires_external_service: ["jira"]
default_enabled: true
---

# Agent Detector

**Priority:** HIGHEST - Runs FIRST for every message. Automatically detects the correct agent, task complexity level, and model tier for each user message using a multi-layer scoring system. No manual agent selection needed -- the detector analyzes task content, explicit technology mentions, user intent, project context, and file patterns to route to the right agent with the right model.

## When to Use

**ALWAYS** - Every user message, no exceptions. This skill fires before any other skill or agent action. It determines who handles the task, at what complexity level, and with which model.

## Workflow

0. **Safety baseline precheck (HARD GATE).** Before any other step, scan the context window for the cached-sentinel marker emitted by `safety-sentinel-inject.cjs`:

   ```
   ## Safety baseline: verified (cached, session <id>)
   ```

   If the marker IS present (turns 2..N of the same session): emit
   `Safety baseline: verified (cached)` and SKIP the 5-file Read loop below.
   The 5 rules remain in context from the inner harness's CLAUDE.md auto-load;
   the sentinel only suppresses redundant re-reads.

   If the marker is ABSENT (turn 1 of a new session, OR
   `MEOWKIT_SKIP_SAFETY_SENTINEL=off`): `Read` each of the 5 always-on
   safety/baseline rules:
   - `.claude/rules/security-rules.md`
   - `.claude/rules/injection-rules.md`
   - `.claude/rules/gate-rules.md`
   - `.claude/rules/core-behaviors.md`
   - `.claude/rules/development-rules.md`

   If any `Read` returns "file does not exist" or equivalent, **ABORT IMMEDIATELY** with the exact message:

   ```
   SAFETY BASELINE INCOMPLETE: rule <name> not found at .claude/rules/<name>.md
   Refusing to route any task. Restore the rule (git checkout / the installer) before retrying.
   ```

   Do NOT proceed to detection. Do NOT route to any agent. The 5 rules are the deterministic baseline; their absence indicates either repo corruption or a partial install. Replaces the unverified directory-auto-load assumption with a positive existence check.

0b. **Phase-zero rule load.** After the safety baseline is confirmed, scan context for the cached-sentinel marker:

   ```
   ## Phase-zero rules: verified (cached, session <id>)
   ```

   If the marker IS present: emit `Phase-zero rules: verified (cached)` and SKIP the 6-file Read loop. If ABSENT (turn 1 or env-var override), `Read` each phase-zero file. These govern Phase 0 routing and are read once per agent-detector invocation:
   - `.claude/rules/phase-contracts.md` — what each phase expects/produces
   - `.claude/rules/agent-routing.md` — agent → role → phase table
   - `.claude/rules/model-selection-rules.md` — task-type → model-tier mapping
   - `.claude/rules/scale-adaptive-rules.md` — domain CSV → complexity routing
   - `.claude/rules/risk-checklist.md` — 9 horizontal-risk flags
   - `.claude/skills/agent-detector/references/skill-domain-routing.md` — intent → skill dispatch table (used at hand-off, Step 5)

   If any of the 5 rule `Read`s fails: ABORT with `PHASE-ZERO RULE MISSING: <name>` — same fail-fast semantics as Step 0. These rules drive the routing logic in steps 2–4; without them, detection silently degrades to keyword-only. The skill-domain-routing reference is advisory dispatch guidance (not a routing rule): if it is absent, log `skill-domain-routing reference absent; skill dispatch falls back to inline judgment` and continue — do NOT abort.

   **Agile context detection (additive — Agile-only load).** After the 5 phase-zero `Read`s succeed:

   1. **PRE-FLIGHT.** Check that `.claude/rules-conditional/` directory exists. If absent → log `agile rules: rules-conditional/ not deployed; skipping load` and skip steps 2–4. (Defensive: filesystem may lag pruning-plan status doc.)
   2. **Detect Agile context — OR-logic, any one match triggers load:**
      - Glob `tasks/contracts/sprint-state-*-sprint-*.md` returns ≥1 result
      - Active plan frontmatter has non-empty `jira_tickets:`
      - `MEOW_JIRA_BASE_URL` env var is set
      - Last user message matches `[A-Z]{2,10}-\d+` (Jira-key pattern)
   3. **If Agile context detected, `Read` the 3 conditional rules:**
      - `.claude/rules-conditional/agile-story-gates.md`
      - `.claude/rules-conditional/agile-sprint-commitment.md`
      - `.claude/rules-conditional/agile-feedback-cycle.md`
      Per-file Read failure (file absent inside the directory): log and skip THAT rule; do NOT abort Step 0b. The phase-zero baseline is already loaded.
   4. **Sprint-goal banner.** If a sprint-state contract exists, parse `sprint_goal:` from the newest active sprint-state file (status: active) and surface in the orient banner.

   Non-Agile sessions skip steps 1–4 silently — zero context cost.

1. **Check cache** -- reuse cached result if same workflow and phase > 1. See `references/detection-process.md`
2. **Score agents** -- analyze task content, extract keywords, check project context across all layers (0-4). See `references/multi-layer-detection.md`, `references/scoring-and-thresholds.md`
3. **Select model + mode** -- map complexity to model tier, check team mode eligibility. See `references/model-selection.md`, `references/complexity-detection.md`, `references/team-mode.md`
4. **Evaluate risk flags** -- read `.claude/rules/risk-checklist.md` (loaded in Step 0b). For each of the 9 flags (AUTH, AUTHZ, DATA_MODEL, AUDIT_SEC, EXT_SYSTEM, PUBLIC_CONTRACT, CROSS_PLATFORM, EXISTING_BEHAVIOR, WEAK_PROOF), evaluate whether the task description matches its trigger criteria. Emit `matched_flags: [<ID>, ...]` (default `[]`). If any flag in `{AUTH, AUTHZ, DATA_MODEL, AUDIT_SEC, EXT_SYSTEM}` matches, escalate the tier to COMPLEX per `rules/model-selection-rules.md` Rule 2 — regardless of `mk:scale-routing` outcome.
5. **Output + hand off** -- show detection banner (including `matched_flags` line if non-empty), load agent instructions, invoke skill. See `references/detection-process.md`, `references/after-detection.md`

## References

- `references/lifecycle-routing.md` -- Task signal → phase → skill mapping (advisory, does not change scoring)
- `references/complexity-detection.md` -- Complexity levels, auto-detection criteria, detection logic
- `references/model-selection.md` -- Model mapping tables (complexity, task type, agent defaults)
- `references/multi-layer-detection.md` -- Layers 0-4: task content, tech, intent, project context, file patterns
- `references/scoring-and-thresholds.md` -- Scoring weights, agent thresholds, QA activation rules
- `references/detection-process.md` -- Step-by-step process (cache, Steps 0-5, banner format)
- `references/examples.md` -- Seven worked examples covering common detection scenarios
- `references/team-mode.md` -- Team mode gate, composition rules, output format, handoff
- `references/after-detection.md` -- Post-detection actions, available agents, manual override

## Token Budget

After complexity detection, check user depth signals per `references/token-budget-levels.md` to set response verbosity. Silent by default — do not surface to users.

## Gotchas

- **Misrouting trivial tasks to heavyweight agents**: Short messages that contain domain keywords (e.g., "fix the auth token") score high for complex agents even when the actual work is a one-line change. The detector favors keyword matches over scope signals. → If the banner shows an unexpected agent/model tier, override via `--quick` or use the explicit `/mk:fix --quick` shorthand to force the right complexity level.
- **Cache stale after context switch**: The detection cache reuses the result from the previous workflow phase, but when a conversation pivots mid-session (e.g., "actually, let's do X instead"), the cached detection is wrong for the new task. The detector doesn't invalidate on pivot signals. → Confirm the banner after any explicit task change; if the agent/model is wrong, start a new message explicitly describing the new task so Layer 0 re-detects from scratch.
- **Multi-domain tasks picking the wrong primary agent**: Tasks spanning two domains (e.g., "add a security check to the payment UI") split scores across agents and the highest scorer wins, which may be wrong for the dominant concern. The tiebreaker is the first keyword match, not importance. → For cross-domain tasks, state the primary concern explicitly at the start of the message (e.g., "Security task: ...") so Layer 0 domain detection anchors to the right agent before keyword scoring runs.
