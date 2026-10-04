---
name: memory-system
description: AID Memory System for session feedback, learning cycles, and skill improvement. Manages state, feedback collection, and improvement analysis. Load for /aid-init, /aid-start, /aid-status, /aid-end, /aid-improve, /aid-memory, /aid-reset.
---

# Memory System Skill

## Triggers
Load when the user invokes any of these; otherwise do not load.

| Command | Description |
|---|---|
| `/aid-init` | Initialize AID system / memory system (first time setup) |
| `/aid-start [role] [phase]` | Start a work session |
| `/aid-status` | Show current session state |
| `/aid-end` | Complete phase gate, collect feedback |
| `/aid-improve` | Run improvement analysis (spawns sub-agent) |
| `/aid-memory` | Manage memory entries |
| `/aid-reset` | Reset memory system (clear state & feedback) |

## Enums
Roles: `product-manager` (pm), `developer` (dev), `qa-engineer` (qa), `tech-lead` (lead), `data-scientist` (ds)

Phases: `discovery` (Phase 0), `prd` (Phase 1), `tech-spec` (Phase 2), `breakdown` (Phase 3), `development` (Phase 4), `qa-ship` (Phase 5)

## Sub-Agent: Memory Analysis
On `/aid-improve`, spawn the **memory-analysis-agent**:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: [Read ../../agents/memory-analysis-agent.md],
  description: "Memory system improvement analysis"
)
```

Pass:
```
{{FEEDBACK_DATA}} - Contents of ~/.aid/feedback/pending/*.json
{{CURRENT_SKILLS}} - Section headers from skills/memory-system/references/
{{TREND_DATA}} - Contents of ~/.aid/metrics/trends.json
{{MEMORY_ENTRIES}} - Current AID:* Claude Memory entries
```

Agent returns:
```json
{
  "suggestions": [...],
  "memory_candidates": [...],
  "trends_analysis": {...}
}
```

## Session Start Flow (`/aid-start`)
1. Check AID directory:
```
IF ~/.aid/ does not exist:
  → Run /aid-init flow
  → Create directory structure
  → Initialize with defaults
  → Display: "🚀 AID Memory System initialized!"
```
2. Load state: read `~/.aid/state.json`; check `pending_feedback_count`; check `sessions_since_last_improvement`.
3. Check improvement suggestion:
```
IF pending feedback >= threshold:
  Display:
  "📊 I have {pending} feedback items waiting for analysis.
   Would you like to review insights and improve skills?
   [Yes, let's improve] [No, continue working]"
```
4. Determine role & phase:
```
IF /aid-start <role> <phase> provided:
  → Use provided values
ELIF state.last_session exists:
  → Suggest: "Continue as {last_role} in {last_phase}?"
ELSE:
  → Ask for role and phase
```
5. Load skills from `skills/memory-system/references/`, in order:
```
1. roles/{role}/SKILL.md
2. roles/{role}/cumulative.md
3. phases/{phase}/SKILL.md
4. phases/{phase}/cumulative.md
```
6. Update state & begin:
```
Update ~/.aid/state.json with:
- current_session.active = true
- current_session.role = role
- current_session.phase = phase
- current_session.started_at = now()

Greet user and ask what they're working on.
```

## Session Work Flow
Track revisions (internal counter):
```
revision_triggers = [
  "fix", "change", "update", "wrong", "missing", "add",
  "incorrect", "error", "should be", "not right", "revise"
]

On each user message containing trigger:
  revision_count += 1
  Note what needed fixing for feedback
```

Note patterns (internal):
```
positive_triggers = ["great", "perfect", "exactly", "good", "excellent"]

On positive trigger:
  Note what worked well for feedback
```

## Phase Gate Flow (`/aid-end` or phase completion detected)
1. Display summary:
```
📋 Phase Summary: {phase_display_name}

Completed deliverables:
• {deliverable_1}
• {deliverable_2}

Revisions made: {revision_count}
```
2. Request rating (MANDATORY):
```
📊 Quality Rating (1-5):

1 ⭐ - Poor, needs significant improvement
2 ⭐⭐ - Below average, missing important elements
3 ⭐⭐⭐ - Acceptable, worked but room for improvement
4 ⭐⭐⭐⭐ - Good, almost perfect
5 ⭐⭐⭐⭐⭐ - Excellent, exactly what I needed

MUST get rating before proceeding
```
3. Request qualitative feedback (optional): What worked well? What could be improved? Additional notes?
4. Save feedback file:
```
Save to ~/.aid/feedback/pending/{timestamp}.json:
{
  "context": { "role": "...", "phase": "..." },
  "metrics": { "rating": N, "revisions": N },
  "qualitative": { "what_worked": "...", "what_didnt": "..." }
}
```
5. Update state:
```
Update ~/.aid/state.json:
- statistics.total_sessions += 1
- statistics.pending_feedback_count += 1
- statistics.sessions_since_last_improvement += 1
- current_session.active = false
```

## Improvement Flow (`/aid-improve`)
1. Gather data: all files from `~/.aid/feedback/pending/`; current skills from `skills/memory-system/references/`; trends from `~/.aid/metrics/trends.json`.
2. Spawn analysis agent:
```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: [../../agents/memory-analysis-agent.md with variables],
  description: "Analyze feedback and suggest improvements"
)
```
3. Present suggestions with approval buttons: `[Approve] [Edit] [Reject]` for each skill update; `[Promote to Memory] [Skip]` for each memory candidate.
4. Apply changes: update approved skill files; add approved memory entries; archive processed feedback to `~/.aid/feedback/processed/`.

## Anonymization Rules
NEVER include in feedback:
- ❌ Project name or identifier
- ❌ Company name
- ❌ Domain-specific terms
- ❌ Code snippets
- ❌ User names

ALWAYS include:
- ✅ Role (product-manager, developer, etc.)
- ✅ Phase (discovery, prd, etc.)
- ✅ Rating (1-5)
- ✅ Revision count
- ✅ Generic methodology feedback

## State Files
| File | Purpose |
|---|---|
| `~/.aid/state.json` | Current session state |
| `~/.aid/config.yaml` | User configuration |
| `~/.aid/feedback/pending/` | Unprocessed feedback |
| `~/.aid/feedback/processed/` | Archived feedback |
| `~/.aid/metrics/trends.json` | Historical trends |

## Error Handling
| Error | Action |
|---|---|
| Missing ~/.aid/ | Run /aid-init automatically |
| Missing skill files | Use defaults, log warning |
| Corrupted state.json | Backup and reset |
| User skips rating | Gently insist, then save as null |

## Related
- Agent: `../../agents/memory-analysis-agent.md`
- References: `skills/memory-system/references/`
- Commands: `../../commands/aid-*.md`
