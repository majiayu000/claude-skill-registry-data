---
name: skill-creator-multi
description: Guide for creating multi-phase skills with orchestrated sequential execution. Use when user wants to create a skill that runs multiple steps in sequence (like gap-finder), needs a start-* orchestrator pattern, or asks about multi-step/multi-phase skill architecture.
---

# Multi-Phase Skill Creator

Create skills that execute multiple phases in sequence, where each phase builds on the previous phase's output.

## When to Use Multi-Phase Skills

Multi-phase skills are appropriate when:
- A task naturally decomposes into distinct sequential stages
- Each stage transforms or filters the previous stage's output
- Separating concerns improves reliability and debuggability
- The same pipeline applies to different inputs

Examples: gap analysis, code review pipelines, document processing chains.

## Multi-Phase Skill Structure

```
skill-name/
├── start-skill-name/SKILL.md   # Orchestrator (invokes phases in order)
├── skill-name-1/SKILL.md       # Phase 1 (raw collection/identification)
├── skill-name-2/SKILL.md       # Phase 2 (analysis/filtering)
└── skill-name-3/SKILL.md       # Phase 3 (refinement/final output)
```

### Orchestrator Pattern (start-*)

The `start-*` skill defines the sequence and ensures all phases run without stopping:

```yaml
---
name: start-skill-name
description: [What it does]. Use when user explicitly asks start-skill-name.
---
```

Body lists procedure steps and includes:
```
**IMPORTANT:** Do NOT stop between steps. Run all steps skill-name-* in a single turn.
```

### Phase Pattern (skill-name-N)

Each phase skill:
- Has description: `Triggered by start-skill-name.`
- Defines specific task, rules, output format, anti-patterns
- References previous step's output in conversation context

## Creation Process

### Step 1: Design the Pipeline

Define phases before creating files:
1. What does each phase do?
2. What is the input/output format for each phase?
3. What rules constrain each phase?

### Step 2: Initialize with Script

```bash
scripts/init_multi_skill.py <skill-name> --path <output-dir> [--phases N]
```

Examples:
```bash
# Default 3 phases
scripts/init_multi_skill.py code-reviewer --path skills/public

# Custom 4 phases
scripts/init_multi_skill.py doc-analyzer --path skills/private --phases 4
```

### Step 3: Edit Each Phase

For each generated SKILL.md, replace TODOs with:

1. **Phase description**: What this phase accomplishes
2. **Rules**: Numbered constraints (keep to 3-5)
3. **Output format**: Exact structure with example
4. **Anti-patterns**: What to avoid

### Step 4: Test the Pipeline

Invoke `start-skill-name` and verify:
- All phases execute without stopping
- Output formats match specifications
- Each phase correctly uses previous output

## Example: Gap Finder Structure

```
gap-finder/
├── start-gap-finder/SKILL.md
│   └── Procedure: invoke gap-finder-1, then -2, then -3
├── gap-finder-1/SKILL.md
│   └── Task: Generate raw list of potential gaps (max 20)
├── gap-finder-2/SKILL.md
│   └── Task: Mark each gap CORE or NOT CORE with verdict table
└── gap-finder-3/SKILL.md
    └── Task: Output only CORE items with clusters summary
```

Each phase has strict output format, enabling reliable handoff between phases.
