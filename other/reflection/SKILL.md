---
name: reflection
description: Automatic quality check on significant outputs via isolated sub-agent. Spawns reflection-agent for objective evaluation without conversation context bias.
---

# Reflection Skill

Apply (spawn agent): code, architecture, PRD, specs, tests, plans, APIs, schemas.
Skip: simple questions, status checks, file reading, clarifying questions, help.

The sub-agent gets NO conversation context. It evaluates purely on merit — inline evaluation shares your context, agrees with your reasoning, and trends to 10/10. The agent sees only output + request + WHY, and can verify claims in source files.

## Process

1. Extract isolation variables (below).
2. Spawn reflection-agent with isolated inputs.
3. Parse JSON response.
4. If pass=false and revisions<3: apply guidance, re-evaluate.
5. Display Quality Check box.

## Context Extraction (CRITICAL)

Extract these for the agent. Do NOT summarize or add context.

| Variable | How to Extract |
|---|---|
| `{{ORIGINAL_REQUEST}}` | First user message that initiated this task - **VERBATIM** |
| `{{STATED_WHY}}` | The WHY established at conversation start - **EXACT TEXT** |
| `{{PHASE_NUMBER}}` | Read from `.aid/state.json` → `current_phase` |
| `{{PHASE_NAME}}` | Read from `.aid/state.json` → `phase_name` |
| `{{OUTPUT_TO_EVALUATE}}` | Your draft output (code, spec, etc.) |
| `{{FILES_TO_VERIFY}}` | Read content of all files your output references/modifies |
| `{{PHASE_CRITERIA}}` | Read from `criteria/phase-{N}-{name}.yaml` |

DO: copy original request exactly as user wrote it; copy stated WHY exactly as established; include ALL files the output references (not just some); load criteria from the YAML file.

DO NOT: ❌ summarize the request; ❌ explain your decisions; ❌ include conversation history; ❌ mention previous attempts; ❌ add "helpful context".

## Spawn Command

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: [Load ../../agents/reflection-agent.md, replace variables],
  description: "Objective quality evaluation"
)
```

## Quality Check Display Format

After receiving agent response, display:

```
╭─────────────────────────────────────────────────────────────╮
│ 🔍 Quality Check                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [icon] WHY Alignment     X/10   [agent's note]             │
│  [icon] Phase Compliance  X/10   [agent's note]             │
│  [icon] Correctness       X/10   [agent's note]             │
│  [icon] Security          X/10   [agent's note]             │
│  [icon] Completeness      X/10   [agent's note]             │
│                                                             │
│  ══════════════════════════════════════════════════════     │
│  📊 Overall: X.X/10                                         │
│  STATUS: [agent's status]                                   │
│                                                             │
│  [If revised: 📝 Improvements: ...]                         │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
```

## Score Icons

| Score | Icon |
|---|---|
| 8-10 | ✅ |
| 6-7.9 | ⚠️ |
| 0-5.9 | ❌ |

## Revision Handling

If agent returns `pass: false`:

1. Read `revision_guidance.required_changes`
2. Apply changes to your output
3. Re-spawn agent with updated output (max 3 attempts)
4. Track improvements: `"Security 5→8/10 Fixed: Added input validation"`

## Session Review Mode

On project load or `/good-morning`, spawn session review instead:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: [Load ../../agents/reflection-agent.md],
  description: "Session review - outside perspective"
)
```

Session review variables:
- `{{STATE_JSON}}` - Content of `.aid/state.json`
- `{{CONTEXT_JSON}}` - Content of `.aid/context.json`
- `{{RECENT_CHANGES}}` - Output of `git log --oneline -10`
- `{{RECENT_FILES}}` - Output of `git diff --stat HEAD~5`
- `{{PHASE_CRITERIA}}` - Current phase criteria YAML

## Commands

| Command | Action |
|---|---|
| `/reflect` | Show detailed breakdown of last evaluation |
| `/reflect --session` | Run session review |
| `/reflect --strict` | Run evaluation with threshold 8.0 |
