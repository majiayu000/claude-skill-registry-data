---
name: continue
description: "Continue an existing Forge project after a pause, restart, or interruption. Triggers: \"forge continue\", \"pick up where we left off\", \"resume\"."
---

<Purpose>
Reads .forge/ state and resumes from the most actionable point. The goal is zero re-explanation —
the user should be able to type "forge continue" and immediately be back in context.
</Purpose>

<Use_When>
- User returns after a session break
- SessionStart detects existing .forge/state.json
- User says "forge continue", "resume", "pick up where we left off"
- KO: "이어서 해줘", "계속해줘", "포지 계속"  JA: "続けて", "フォージ続行"  ZH: "继续", "锻造继续"
</Use_When>

<Steps>

## 1. Detect state

Read `.forge/state.json`. If missing → "No active Forge project. Use `forge` to start one."

## 2. Load context (minimal per phase)

| Phase   | Files to load                                              |
|---------|------------------------------------------------------------|
| 0–1     | state.json only                                            |
| 2       | + spec.md                                                  |
| 3       | + spec.md, code-rules.md, design/, contracts/, runtime.json |
| 4–6     | + spec.md, holes/, runtime.json                            |
| 7       | + spec.md, holes/, delivery-report/                        |

If `.forge/runtime.json` exists, always load it — it has lane ownership, blockers, and handoff notes.

## 3. Show continuation summary

Keep it short. The user needs three things:

```
Forge: {{project_name}}
Phase {{N}}/{{8 for build, 7 for repair}} — {{phase_name}}
{{one-line summary of where things stand}}

Next: {{what to do now}}
{{if blockers: list them}}
```

Examples:

```
Forge: my-saas-app
Phase 3/8 — develop
3 lanes active, 1 blocked (auth waiting on DB schema)

Next: Continue auth-api lane after resolving DB contract
```

```
Forge: my-saas-app
Phase 6/8 — fix
2 blockers remaining (login redirect loop, rate limit bypass)

Next: Diagnose login redirect — attempt 1/3
```

Do NOT dump every runtime field. Surface only what's actionable.

## 4. Determine continuation target

Evaluate in this exact order. Take the FIRST match — do not skip ahead.

| Priority | Condition                                      | Action                                              |
|----------|-------------------------------------------------|-----------------------------------------------------|
| 1        | Customer blocker exists                         | Surface the question. Don't pretend work can continue without user input. |
| 2        | Internal blocker exists                         | Route to the owning team's phase skill with the blocker context. |
| 3        | Saved analysis is stale, or repair flow has no analysis yet | Route to `forge:analyze` first. Refresh analysis before phase work continues. |
| 4        | Lane has handoff notes and is `in_progress`     | Load that lane's task file, worktree, and latest handoff note. Continue in-lane. |
| 5        | Runtime has a designated next lane (`next_lane`) | Load that lane's context. This is the lead dev's recommendation for where to pick up. |
| 6        | None of the above                               | Fall back to the current phase skill. |

The goal: the user types `forge continue` and lands on the single most useful thing to work on, with full context loaded and zero re-explanation needed.

## 4a. AgentRecommendation routing

On resume, `recommendedAgentsFor()` provides layer-classified agent recommendations.
Dispatch agents according to their layer classification (layer0, layer2_subagent, etc.).

Apply staleness-aware dispatch (from state-restore.mjs):
- **Fresh (<1hr)**: full context available — dispatch per layer recommendation immediately
- **Warm (1-24hr)**: abbreviated context — confirm direction with user before dispatching agents
- **Stale (>24hr)**: minimal context — suggest `forge cancel` or require explicit `forge continue` confirmation before proceeding

## 5. Phase → skill mapping

Standard mode (build, N/8):
- 0 → forge:intake
- 1 → forge:discovery
- 2 → forge:design
- 3 → forge:develop
- 4 → forge:qa
- 5 → forge:security
- 6 → forge:fix
- 7 → forge:deliver

Repair mode (N/7):
- 0 → forge:intake
- 1 → forge:troubleshoot  # focus on reproduction (guidance hint, not a sub-mode parameter)
- 2 → forge:troubleshoot  # focus on isolation and root cause (guidance hint, not a sub-mode parameter)
- 3 → forge:fix
- 4 → forge:qa (regress)
- 5 → forge:security (verify)
- 6 → forge:deliver

Express mode:
- plan → forge:discovery (compressed)
- build → forge:develop (inline QA)
- ship → forge:deliver (compressed)

## 6. Hand off

Invoke the target skill with loaded context. The skill takes over from here.

</Steps>

<Tool_Usage>
- Read: .forge/state.json, .forge/runtime.json, phase-specific files per table above
- Skill: invoke mapped phase skill
</Tool_Usage>
