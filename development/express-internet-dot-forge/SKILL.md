---
name: express
description: "Collapsed Forge pipeline for medium-complexity tasks. Use when the user says \"forge express\", \"quick build\", or when a task is too complex for a single prompt but doesn't warrant the full 8-phase pipeline."
---

<Purpose>
Express mode collapses the 8-phase pipeline into 3 steps for medium-complexity tasks:
1. PLAN (Discovery + Design compressed into one approval gate)
2. BUILD (Development + QA in a single pass with inline testing)
3. SHIP (Fix + Delivery compressed)

This reduces approval gates from 5 to 2 and turns from ~20 to ~8.
</Purpose>

<Use_When>
- Task is medium complexity (2-5 files, clear requirements)
- User explicitly requests express mode
- KO: "빠르게", "간단하게"  JA: "簡単に", "エクスプレス"  ZH: "快速", "简单"
- Task type is 'feature' or 'refactor' with clear scope
</Use_When>

<Do_Not_Use_When>
- Task requires extensive discovery (unclear requirements)
- Security-sensitive changes (auth, payments, data handling)
- Large-scale architectural changes (use full pipeline)
- Simple bugfix (use light tier instead)
</Do_Not_Use_When>

<Steps>
Step 1 — PLAN:
  1. Initialize .forge/ with tier='medium', mode='express'
  2. PM: Generate compact spec (max 1 page) from user's request
     - Include understanding check: PM summarizes back to user before finalizing
  3. CTO: Define code-rules and key interfaces inline
     - **Lightweight Handoff Interview**: CTO reads spec, flags any gaps in 1 round
     - PM/CEO resolves gaps immediately (no multi-round interview in express mode)
  4. Optional: dispatch Analyst for quick architecture snapshot (skip if trivial task —
     only useful when touching 3+ modules or unfamiliar areas)
  5. Single approval gate: "Plan looks good? (y/n)"

Step 2 — BUILD:
  1. Lead-dev: Split into tasks, assign to developer(s)
  2. Developer: Implement with inline QA checks (test as you go)
     - Recommend native worktree isolation (Agent tool isolation: "worktree") for
       parallel developer lanes
  3. Fact-checker validates key claims
  4. Auto-merge if tests pass, else flag issues

Step 3 — SHIP:
  1. Fix any flagged issues (max 2 iterations)
  2. Tech-writer: Generate minimal README updates
  3. Present delivery summary
  4. Done — no separate QA or security phase (already inline)
</Steps>

<Layer_Classification>
Express uses layer0 only — no Teams overhead. Speed is the priority.
Keep the process compressed: Analyst snapshot is optional, worktree isolation is
recommended but not enforced.
</Layer_Classification>

<Tool_Usage>
- Agent tool: dispatch forge:pm for compact spec generation (PLAN phase)
- Agent tool: dispatch forge:cto for code-rules and interface definition (PLAN phase)
- Agent tool: dispatch forge:developer (layer2_subagent, isolation="worktree") for implementation (BUILD phase)
- Agent tool: dispatch forge:fact-checker for claim validation (BUILD phase)
- Agent tool: dispatch forge:analyst (optional) for architecture snapshot on multi-module tasks
- Bash tool: run tests inline during BUILD, git operations
- Read tool: load .forge/spec.md, .forge/code-rules.md
- Edit tool: update .forge/state.json
</Tool_Usage>

<State_Management>
Express mode uses the same .forge/ directory but with mode='express'.
Phase mapping: plan=discovery, build=develop, ship=delivery
Tier is locked to 'medium' throughout.
</State_Management>
