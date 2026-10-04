---
name: fleet-code-exploration
description: How engineers systematically examine a codebase — not just reading files, but understanding patterns, dependencies, and the implications for their task. Maps to code-explorer sub-agent.
---

# Code Exploration — Engineer's Analysis Skill

Before you implement, you must understand what exists. Code exploration isn't "read some files" — it's systematic examination of patterns, dependencies, boundaries, and the implications for your task.

## When to Explore

- **Analysis stage:** Your primary activity. Produce analysis_document artifact.
- **Before implementing:** Even in work stage, read the codebase area first.
- **Before contributing:** When architect/QA asks about feasibility.
- **When debugging:** Trace execution paths to find the actual behavior.

## Systematic Exploration Framework

### Step 1: Identify the Scope

Read your task's verbatim requirement. What codebase area does it touch?

```
Task: "Add stage-aware effort to model selection"
Scope: fleet/core/model_selection.py + fleet/cli/dispatch.py + config/methodology.yaml
```

Don't explore everything. Identify the 3-5 files that matter most.

### Step 2: Understand the Pattern

For each file in scope, identify:
- **What pattern does it use?** (adapter, repository, builder, strategy, etc.)
- **What does it depend on?** (imports from which modules)
- **What depends on it?** (who imports this module)
- **What's the module's single responsibility?**

Use the `code-explorer` sub-agent for isolated exploration that won't bloat your context:
```
Agent: code-explorer
Prompt: "Trace the execution path of select_model_for_task() in 
        fleet/core/model_selection.py. Map all functions it calls,
        what config it reads, and what it returns."
```

### Step 3: Map the Cross-System Implications

Every module participates in the 20-system web. When you modify something, trace the impact:

| Question | How to Find Out |
|----------|----------------|
| What events does this emit? | Search for `_emit_event` in the module |
| What does the ChainRunner propagate? | Search for `build_*_chain` calls |
| Does this affect Plane? | Search for `plane` references |
| Does this affect the trail? | Search for `post_memory` with trail tags |
| Does the Doctor watch this? | Check methodology.yaml tools_blocked |

### Step 4: Document Findings

In analysis stage, build your artifact progressively:
```
fleet_artifact_create("analysis_document", "Codebase Analysis: {scope}")
fleet_artifact_update("analysis_document", "scope", "fleet/core/model_selection.py + dispatch.py")
fleet_artifact_update("analysis_document", "current_state", "Model selection uses SP + complexity for routing...")
fleet_artifact_update("analysis_document", "findings", append=True, value={"pattern": "strategy", "issue": "no stage awareness"})
```

### Step 5: Reference Specific Locations

Never say "the module handles routing." Say:
- [model_selection.py:42](fleet/core/model_selection.py#L42) — `select_model_for_task()` uses SP + complexity
- [dispatch.py:118](fleet/cli/dispatch.py#L118) — dispatch record uses `routing.effort` (not stage-aware)

Specific references let the architect validate your findings and the engineer implement precisely.

## What Code Exploration is NOT

- NOT skimming file names and guessing what's inside
- NOT reading one file and assuming you understand the system
- NOT grep for a keyword and calling it analysis
- NOT asking the architect "how does this work?" (you should be able to find out)

## Context Management

Code exploration can consume a lot of context. Strategies:
- Use `code-explorer` sub-agent for broad surveys (isolated context)
- Read only the functions you need, not entire files
- Build artifacts progressively so findings persist across cycles
- If approaching context limits: extract findings to artifact, compact
