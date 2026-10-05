---
name: cm-skill-chain
description: Skill Chain Engine — compose skills into automated pipelines. One task triggers multi-skill workflows with progress tracking, auto-detection, and step management.
---

# Skill Chain Engine

> **TRIZ #40 Composite Materials** — Skills compose into pipelines.
> One command → full workflow → automated step progression.

## When to Use

ALWAYS trigger for: chain, pipeline, workflow, multi-step, end-to-end,
"run the whole thing", "full process", "feature pipeline", "bug fix flow",
"from scratch to deploy", "brainstorm to ship", "skill chain", "full pipeline"

## Quick Reference

| Command | Description |
|---------|-------------|
| `cody chain list` | Show all available chains |
| `cody chain info <id>` | Show chain pipeline details |
| `cody chain auto "task"` | Auto-detect best chain & start |
| `cody chain start <id> "task"` | Start specific chain |
| `cody chain status [exec-id]` | Show progress |
| `cody chain advance <exec-id>` | Complete current step, move to next |
| `cody chain skip <exec-id>` | Skip current step |
| `cody chain abort <exec-id>` | Cancel chain |
| `cody chain history` | View past chain runs |

## Naming Convention

Step names use short-form identifiers — the `cm-` prefix is stripped by convention.
Full skill names: `cm-brainstorm-idea`, `cm-planning`, `cm-tdd`, `cm-execution`, `cm-quality-gate`,
`cm-safe-deploy`, `cm-debugging`, `cm-content-factory`, `cm-ads-tracker`, `cm-project-bootstrap`,
`cm-code-review`. All skills now use the `cm-` prefix convention.

## Built-in Chains

### 🚀 feature-development (up to 3 active steps)
`brainstorm-idea* → planning → tdd → execution → quality-gate → safe-deploy*`
*optional steps — only activated when task context scores them relevant

### 🐛 bug-fix (3 steps)
`debugging → tdd → quality-gate`

### 📝 content-launch (3 steps)
`content-factory → ads-tracker → cm-cro-methodology`

### 🏗️ new-project (up to 3 active steps)
`project-bootstrap → planning → tdd → execution → quality-gate → safe-deploy*`
*optional steps selected by task relevance

### 🔍 cm-code-review (3 steps)
`cm-code-review → quality-gate → safe-deploy`

## Intelligent Skill Selection (v5.1)

Chains no longer execute every step blindly. `selectTopSkills()` dynamically selects the **top 3 most relevant steps** for each task:

```
Task: "fix login timeout bug"
  → Scores each step by keyword overlap with task description
  → Mandatory steps (condition='always', optional=false) always included first
  → Optional steps ranked by relevance score, capped at 3 total
  → Result: debugging (score 105) → tdd (score 101) → quality-gate (score 100)
```

**Why it matters (SkillsBench research):**
- 2-3 focused skills → **+18.6pp** task performance
- 4+ skills → **+5.9pp**
- Monolithic loading → **-2.9pp**

If a chain has more than 3 mandatory steps, all mandatory steps run and a performance advisory is logged.

## Workflow

1. **Start**: Use `chain auto` for auto-detection or `chain start` for specific chains
2. **Execute**: Work through each skill step, using `@[/skill-name]` to invoke
3. **Advance**: When step is done, run `chain advance <id> "summary"`
4. **Repeat**: Continue until all steps complete
5. **Track**: Use `chain status` to monitor progress anytime

## Integration with Other Skills

- **cm-continuity**: Chain progress persists across sessions via CONTINUITY.md working memory
- **cm-execution**: Each chain step delegates to cm-execution for actual implementation
- **cm-quality-gate**: Automatically runs at end of each development chain
- **Context Bus (v5)**: Every chain automatically maintains `.cm/context-bus.json` — shared state across all steps

## Context Bus — Inter-Skill Coordination (v5)

When `chain start` runs, the context bus is initialized automatically:

```
chain start feature-development "add payment flow"
→ Creates .cm/context-bus.json with:
    pipeline: "feature-development"
    session_id: "<uuid>"
    current_step: "brainstorm-idea"
    shared_context: {}
    resource_state: { skeleton_generated: null, learnings_indexed: null, ... }
```

When `chain advance` runs after each skill completes:

```
chain advance <exec-id> "summary of what was done"
→ Updates context-bus.json:
    current_step: "planning"   ← moved forward
    shared_context.brainstorm-idea: { summary, affected_files, output_path }
```

**What downstream skills gain:**
- `cm-planning` can read brainstorm output path → no re-read of full filesystem
- `cm-tdd` can see which files planning created → targeted test generation
- `cm-quality-gate` knows exactly which files changed → focused review

**Reading the bus:**
```bash
cm continuity bus          # terminal pretty-print
cm_bus_read                # MCP tool (Claude Desktop)
cm://pipeline/current      # URI resolver (in skill prompts)
```

**Publishing to the bus (inside a skill):**
```bash
cm_bus_write skill=cm-planning summary="tasks.md created" output_path=openspec/...
```

## For AI Agents

When dispatching tasks that match a chain pattern:

```
1. Check if task matches a chain: suggestChain(taskTitle)
2. If match found, suggest to user: "This task matches the X chain pipeline"
3. If user agrees, start the chain and invoke skills in order
4. At the START of each skill step:
   → Read cm://pipeline/current to see upstream skill outputs
   → Check shared_context to avoid re-doing work
5. After completing each skill, advance the chain:
   → chain advance <id> "summary"
   → This updates context bus + CONTINUITY.md simultaneously
```
