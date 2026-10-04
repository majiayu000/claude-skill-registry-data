---
name: orchestration-skill-creator
description: Creates multi-phase orchestration skills that spawn subagents. Use when you want to build a new workflow that chains multiple phases together, with each phase running in its own context and passing reports to the next. Triggers on "create an orchestration skill", "build a multi-phase workflow", "make a skill that uses subagents", or "orchestration skill for [workflow]".
---

# Orchestration Skill Creator

This meta-skill creates orchestration skills - skills that spawn subagents for multi-phase workflows.

## Why This Pattern Works (The Big Deal)

**The Problem:** Claude has a fixed 200k context window. Complex tasks fill it up, quality degrades after 40%.

**The Solution:** Spawn subagents. Each phase gets fresh 200k context.

| Approach | Total Context | Effective Quality |
|----------|---------------|-------------------|
| Monolithic (1 agent) | 200k, degrading | ~80k usable |
| Orchestrated (7 phases) | 7 × 200k = 1.4M | 7 × 80k = 560k |

**This is context multiplication, not just organization.**

Each phase:
- Gets fresh context (no pollution from previous work)
- Returns only a summary (orchestrator stays clean)
- Has dedicated model selection (expensive only where needed)
- Can be retried independently (errors don't cascade)

## What You'll Get

A complete orchestration skill with:
```
{skill-name}/
├── SKILL.md                    # Orchestrator (coordinates, doesn't DO)
├── agents/
│   ├── phase-1-{name}.md       # Subagent prompts with frontmatter
│   ├── phase-2-{name}.md       # Note: phase-N (with hyphen)
│   └── phase-N-{name}.md
├── references/
│   ├── 00-{general}.md         # Patterns all agents read
│   ├── 01-{phase1-specific}.md # Phase-specific reference
│   └── output-templates.md     # JSON contracts
├── scripts/
│   ├── init-project.sh         # Setup automation
│   └── verify-output.sh        # Validation automation
└── reports/                    # Output: {project}/{timestamp}/
```

**Undocumented but Works:** The `agents/` folder pattern is NOT in Anthropic docs. It works because:
- Skills are folders with SKILL.md (no restriction on contents)
- Task tool accepts any prompt (including from files)
- Claude can read files → pass to Task → subagent executes

## Workflow

### Phase 1: Interview

Ask these questions using AskUserQuestion tool. Gather all answers before generating.

#### Q1: Skill Name
```
"What should this orchestration skill be called?"
Header: "Name"
Options:
- [Let user type - use Other]
Example: "content-pipeline", "document-analyzer", "meeting-prep"
```

#### Q2: Purpose
```
"In one sentence, what does this workflow do?"
Header: "Purpose"
Options:
- [Let user type - use Other]
Example: "Analyzes documents and produces structured summaries"
```

#### Q3: Trigger Phrases
```
"What phrases should trigger this skill?"
Header: "Triggers"
Options:
- [Let user type - use Other]
Example: "analyze document", "summarize this doc", "document analysis"
```

#### Q4: Number of Phases
```
"How many phases does this workflow have?"
Header: "Phases"
Options:
- "3 phases" - Simple workflow
- "4 phases" - Standard workflow
- "5 phases" - Comprehensive workflow
- "6+ phases" - Complex workflow (specify number)
```

#### Q5: Phase Details (repeat for each phase)

For each phase, ask:
```
"Phase {N}: What should this phase be called and what does it do?"
Header: "Phase {N}"
Options:
- [Let user describe - use Other]
Format expected: "{name}: {description}"
Example: "discovery: Find and collect relevant sources"
```

#### Q6: Model Selection per Phase
```
"Which phases need deep reasoning (Opus) vs speed (Sonnet) vs simple execution (Haiku)?"
Header: "Models"
Options:
- "All Sonnet" - Balanced for most workflows
- "All Opus" - Deep reasoning throughout (expensive)
- "Mixed" - Right model per phase (Recommended)
```

If Mixed, default assignment:
| Phase Type | Model | Why |
|------------|-------|-----|
| Architecture/Design | **Opus** | Complex reasoning, strategic decisions |
| Analysis/Synthesis | **Opus** | Deep insight required |
| Creative/Ideation | **Opus** | Novel thinking matters |
| Final Writing | **Opus** | Quality and nuance |
| Search/Extraction | Sonnet | Speed advantage, depth not critical |
| Code Generation | Sonnet | Reliable patterns |
| QA/Verification | Sonnet | Systematic checking |
| Deploy/Format | Haiku | Pure execution |

**Default to Opus** for any phase where quality matters. Cost is irrelevant with Claude Max.

#### Q7: Output Location
```
"Where should reports be saved?"
Header: "Output"
Options:
- "Inside skill folder" - ~/.claude/skills/{skill}/reports/ (Recommended)
- "User's home" - ~/Documents/{skill}-reports/
- "Current project" - ./{skill}-reports/
```

### Phase 2: Generate Files

After gathering all answers, generate these files:

#### 2.1: Create Directory Structure

```bash
SKILL_DIR=~/.claude/skills/{skill-name}
mkdir -p $SKILL_DIR/{agents,references,assets/templates,scripts,reports}
```

#### 2.2: Generate SKILL.md

Use template from: `references/skill-md-template.md`

Fill in:
- `{SKILL_NAME}` - from Q1
- `{DESCRIPTION}` - from Q2, expanded with trigger info
- `{TRIGGER_PHRASES}` - from Q3
- `{PHASE_COUNT}` - from Q4
- `{PHASE_LIST}` - names from Q5
- `{PHASE_FLOW}` - generated diagram
- `{OUTPUT_DIR}` - from Q7

#### 2.3: Generate Agent Files

For each phase, use template from: `references/agent-template.md`

Fill in:
- `{PHASE_NUM}` - 1, 2, 3...
- `{PHASE_NAME}` - from Q5
- `{MODEL}` - from Q6 (sonnet or opus)
- `{TOOLS}` - inferred from phase description:
  - Search/find → WebSearch, WebFetch
  - Analyze/read → Read, WebFetch
  - Synthesize/write → Write, Read
  - Verify → WebSearch, Read
  - All phases get Write for reports
- `{TASK_DESCRIPTION}` - from Q5
- `{PREV_PHASE_READS}` - phases 2+ read previous reports
- `{REPORT_FILENAME}` - 0{N}-{phase-name}.md

#### 2.4: Generate References

**orchestrator-flow.md:**
Generate flow diagram showing:
- Phase sequence
- Data passed between phases
- Session directory structure

**json-response-format.md:**
Generate JSON contracts for each phase based on what they produce.

#### 2.5: Generate Templates

**session-init.json:**
JSON state template with all phases listed.

**init-session.sh:**
Bash script to create timestamped session directories.

### Phase 3: Verify & Present

After generating all files:

1. **List created files:**
```
Created orchestration skill: {skill-name}

Files generated:
- SKILL.md (orchestrator)
- agents/phase1-{name}.md
- agents/phase2-{name}.md
- ...
- references/orchestrator-flow.md
- references/json-response-format.md
- assets/templates/session-init.json
- scripts/init-session.sh
```

2. **Show how to use it:**
```
To use this skill, say:
"{trigger phrase} [your input]"

Example:
"{example trigger} {example input}"
```

3. **Offer refinement:**
```
Want me to adjust any phase or add more detail to the agent instructions?
```

## Generation Rules

### Agent Tool Assignment

| Phase Type | Tools |
|------------|-------|
| Discovery/Search | WebSearch, WebFetch, Write, Read |
| Analysis/Extraction | WebFetch, Write, Read |
| Synthesis/Reasoning | Write, Read |
| Verification | WebSearch, Write, Read |
| Report Generation | Write, Read |

### Model Assignment (Mixed mode)

| Phase Type | Model | Why |
|------------|-------|-----|
| Architecture/Design | **Opus** | Complex reasoning, strategic decisions |
| Analysis/Synthesis | **Opus** | Deep insight required |
| Creative/Ideation | **Opus** | Novel thinking, pushing boundaries |
| Final Report | **Opus** | Quality writing matters |
| Discovery/Search | Sonnet | Speed advantage, depth not critical |
| Extraction | Sonnet | Systematic processing |
| Code Generation | Sonnet | Reliable patterns |
| Verification/QA | Sonnet | Systematic checking |
| Deploy/Format | Haiku | Pure execution |

**Quality principle:** Default to Opus for any phase where output quality matters. Cost is irrelevant with Claude Max.

### Report Naming Convention

```
0{phase_number}-{phase-name}.md
```
Examples: `01-discovery.md`, `02-analysis.md`, `03-synthesis.md`

### JSON Response Contract

Every agent returns:
```json
{
  "status": "complete|partial|error",
  "report_path": "{session_dir}/0N-phase-name.md",
  "{phase_name}_summary": {
    // Phase-specific metrics
  }
}
```

## File References

- `references/skill-md-template.md` - Template for orchestrator SKILL.md
- `references/agent-template.md` - Template for phase agents
- `references/flow-template.md` - Template for flow documentation
- `references/json-template.md` - Template for JSON contracts
- `references/common-patterns.md` - 10 workflow patterns + 6 structural archetypes
- `references/script-templates.md` - Bash script templates for automation
- `assets/templates/session-init-template.json` - Template for state file
- `assets/templates/init-session-template.sh` - Template for init script

## Key Learnings Applied

This skill creator incorporates learnings from building `fullstack-app-builder`:

1. **Context multiplication** - Each phase gets fresh 200k, not shared degrading context
2. **Progressive data flow** - Later phases receive more previous context as needed
3. **Model optimization** - Opus for complex reasoning, Sonnet for code gen, Haiku for simple execution
4. **Reference doc linking** - Agents read `${SKILL_DIR}/references/` at runtime
5. **Scripts for heavy lifting** - Bash does repetitive work, Claude does thinking
6. **TodoWrite ownership** - ONLY orchestrator uses TodoWrite, agents return JSON
7. **SKILL_DIR passing** - Agents need path to find references and scripts
