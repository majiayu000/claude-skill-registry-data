---
name: script-driven-skill
description: Build multi-step skills using a state-machine pattern with disciplined orchestrator and smart phases
---

# Script-Driven Skill Pattern

A pattern for building reliable multi-step skills where a state machine controls flow and phases are self-contained instruction files.

## Purpose

Separates concerns in complex skills:
- **Orchestrator**: Follows the prescribed workflow, exercises judgment on exceptions
- **State machine** (`next-step.py`): Controls flow, validates gates, tracks progress
- **Phase files**: Self-contained instructions that travel with subagents

**Context isolation** is a primary motivation: the orchestrator stays lean while subagents do heavy lifting (searching, reading files, analyzing). Search results, file contents, and intermediate work stay in subagent contexts—only distilled outputs return. This keeps the orchestrator's context window clean for coordination, not cluttered with discovery.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, reports results |
| State machine | progress.json, CLI args | Decides next action, tracks phase completion |
| Subagent | Phase file (e.g., SCOUT.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files.

## When to Use

**Use for multi-phase workflows** where you need validation gates between steps or resumability after interruption.

| Skill Type | Use This Pattern? | Why |
|------------|------------------|-----|
| Multi-phase with gates | ✅ Yes | Validate outputs before proceeding |
| Needs resumability | ✅ Yes | progress.json survives interruption |
| Documentation-like | ❌ No | Just explains concepts, no execution |
| Tool-like | ❌ No | Provides scripts/info, agent chooses what to use |

## Directory Structure

```
skills/<skill-name>/
├── SKILL.md              # Human-readable overview (you're reading one)
├── next-step.py          # State machine - returns JSON actions
└── phases/
    ├── SCOUT.md          # Phase 1 instructions (for subagents)
    ├── RESEARCH.md       # Phase 2 instructions (for subagents)
    └── ASSEMBLE.md       # Phase 3 instructions (for subagents)
```

Runtime state lives in the workspace (e.g., `planning/<task>/progress.json`).

## The Orchestrator Loop

The orchestrator is intentionally minimal. It:
1. Gets actions from the state machine
2. Executes them (spawn, run command)
3. **Reports results back** to the state machine
4. Repeats until done

### Key Principle: Explicit Result Reporting

The orchestrator **reports phase results back** to the state machine via CLI argument.
This is how the state machine knows a phase completed (not by checking file existence).

```
next-step.py <workspace>                              # Get next action
next-step.py <workspace> --phase-result success       # Report success
next-step.py <workspace> --phase-result failure       # Report failure
```

### Python Implementation

```python
import json

workspace = f"planning/{slug}"
bash(f"mkdir -p {workspace}", on_error="raise")

while True:
    result = bash(f"python3 skills/{skill}/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)
    
    if action["type"] == "done":
        final = fs_read("Line", f"{workspace}/FINAL.md", 1, -1)
        break
    
    if action["type"] == "blocked":
        log(f"Blocked: {action['reason']}")
        break
    
    if action["type"] == "spawn":
        try:
            r = spawn(
                action["prompt"],
                context_files=action["context_files"],
                context_data=action.get("context_data"),
                allow_tools=True
            )
            write("create", f"{workspace}/{action['output_file']}", file_text=r.response)
            
            # Report success back to state machine
            bash(f"python3 skills/{skill}/next-step.py {workspace} --phase-result success", on_error="raise")
        except Exception as e:
            # Report failure back to state machine
            bash(f"python3 skills/{skill}/next-step.py {workspace} --phase-result failure", on_error="raise")
```

### Pseudocode (any agentic system)

```
workspace = "planning/<task-slug>"
create workspace directory

loop:
    action = run("python3 skills/<skill>/next-step.py <workspace>")
    parse action as JSON
    
    if action.type == "done":
        read workspace/FINAL.md
        break
    
    if action.type == "blocked":
        log "Blocked: " + action.reason
        break
    
    if action.type == "spawn":
        result = spawn_subagent(
            prompt = action.prompt,
            context_files = action.context_files
        )
        write result to workspace/<action.output_file>
        
        # CRITICAL: Report result back
        if spawn succeeded:
            run("python3 skills/<skill>/next-step.py <workspace> --phase-result success")
        else:
            run("python3 skills/<skill>/next-step.py <workspace> --phase-result failure")
```

## Writing next-step.py

The state machine:
1. Parses `--phase-result` to update state
2. Returns the next action as JSON

### Template

```python
#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

PHASES = ["scout", "research", "assemble", "done"]

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("workspace", help="Path to workspace directory")
    p.add_argument("--phase-result", choices=["success", "failure"],
                   help="Result of previous phase")
    return p.parse_args()

def load_state(workspace):
    progress = workspace / "progress.json"
    if progress.exists():
        return json.loads(progress.read_text())
    return {"phase": PHASES[0], "completed": [], "retries": 0}

def save_state(workspace, state):
    (workspace / "progress.json").write_text(json.dumps(state, indent=2))

def next_phase(current):
    idx = PHASES.index(current)
    return PHASES[idx + 1] if idx + 1 < len(PHASES) else "done"

def main():
    args = parse_args()
    workspace = Path(args.workspace)
    state = load_state(workspace)
    
    # Handle phase result if provided
    if args.phase_result == "success":
        state["completed"].append(state["phase"])
        state["phase"] = next_phase(state["phase"])
        state["retries"] = 0
        save_state(workspace, state)
    elif args.phase_result == "failure":
        state["retries"] = state.get("retries", 0) + 1
        if state["retries"] >= 3:
            print(json.dumps({"type": "blocked", "reason": f"Phase {state['phase']} failed 3 times"}))
            return
        save_state(workspace, state)
    
    phase = state["phase"]
    
    # Done
    if phase == "done":
        print(json.dumps({"type": "done"}))
        return
    
    # Scout phase
    if phase == "scout":
        print(json.dumps({
            "type": "spawn",
            "prompt": "Execute the scout phase.",
            "context_files": ["skills/my-skill/phases/SCOUT.md"],
            "context_data": {"workspace": str(workspace)},
            "output_file": "01-scout.md"
        }))
        return
    
    # Research phase
    if phase == "research":
        print(json.dumps({
            "type": "spawn",
            "prompt": "Execute the research phase.",
            "context_files": [
                "skills/my-skill/phases/RESEARCH.md",
                f"{workspace}/01-scout.md"
            ],
            "context_data": {"workspace": str(workspace)},
            "output_file": "02-research.md"
        }))
        return
    
    # Assemble phase
    if phase == "assemble":
        print(json.dumps({
            "type": "spawn",
            "prompt": "Execute the assemble phase.",
            "context_files": [
                "skills/my-skill/phases/ASSEMBLE.md",
                f"{workspace}/01-scout.md",
                f"{workspace}/02-research.md"
            ],
            "context_data": {"workspace": str(workspace)},
            "output_file": "FINAL.md"
        }))
        return

if __name__ == "__main__":
    main()
```

### Action Types

| Type | Fields | Purpose |
|------|--------|---------|
| `spawn` | prompt, context_files, context_data, output_file | Run a subagent |
| `blocked` | reason | Stop execution, unrecoverable failure |
| `done` | - | Skill complete |

## Writing Phase Files

Phase files are self-contained instructions for subagents. They should include:

1. **Goal** - What this phase accomplishes
2. **Inputs** - What files/data are available
3. **Procedure** - Step-by-step instructions
4. **Output** - What to produce

Example `phases/SCOUT.md`:

```markdown
# Scout Phase

## Goal
Identify relevant source files and documentation for the research task.

## Inputs
- Workspace path in context_data
- User question in workspace/question.txt

## Procedure
1. Read the user question
2. Search codebase for relevant files
3. List key files with brief descriptions

## Output
Write a markdown summary listing discovered files and their relevance.
```

## Handling Exceptions

The state machine handles the happy path. When things go wrong, **the orchestrator must exercise judgment**:

| Exception | Orchestrator Response |
|-----------|----------------------|
| Spawn times out | Assess: retry with longer timeout? Report partial progress? Ask user? |
| Spawn returns error | Check if retryable. Report failure to state machine, let it track retries |
| Empty/invalid response | Treat as failure, report to state machine |
| Phase blocked after retries | Decide: skip with justification? Fail workflow? Escalate to user? |

**Key principle**: Don't silently advance past failures. Either retry properly, fail explicitly, or make a reasoned decision to proceed with documented gaps.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Check file existence to determine completion | Report result via `--phase-result` |
| Read phase files yourself | Pass phase files via context_files to subagents |
| Store state in orchestrator memory | State lives in progress.json |
| Skip result reporting | Always report success/failure back |
| Silently advance past failures | Exercise judgment: retry, fail, or document gaps |
| Manually edit progress.json to skip phases | Let state machine control flow |

## Resumability

If interrupted, the orchestrator can resume by calling `next-step.py` again.
The state machine reads `progress.json` and returns the appropriate action.

To resume: just run the orchestrator loop again. It will pick up where it left off.
