---
name: propose-feature-concept
description: Create a new feature concept document to pitch the idea and explain the problem/solution
---

# Propose Feature Concept Skill

Create a feature concept document that pitches the feature idea and explains the problem it solves. This is the first step in the feature proposal process.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., SETUP.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## When to Use

- User wants to propose a new feature for crumbly, forester, or other forest crates
- Starting to document a feature idea
- Need to explain "why" and "what" before diving into requirements

## Prerequisites

- User has described the feature idea

## Optional: Offer Idea Honing First

Before starting the orchestrator loop, ask the user:

> Would you like to use an idea honing process to bring more clarity to the concept? This involves working through questions one at a time to explore ambiguities and design considerations.

If yes, use the `idea-honing` skill following the protocol in `skills/README.md`. Return to this skill after idea honing is complete.

## Orchestrator Loop

```python
import json

workspace = f"planning/{feature_slug}"
bash(f"mkdir -p {workspace}", on_error="raise")

while True:
    result = bash(f"python3 skills/propose-feature-concept/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)
    
    if action["type"] == "done":
        setup = json.loads(fs_read("Line", f"{workspace}/setup.json", 1, -1))
        review = fs_read("Line", f"{workspace}/review.md", 1, -1)
        log(f"Feature concept created at {setup['feature_dir']}/concept.md")
        log(review)
        break
    
    if action["type"] == "gate_failed":
        log(f"Gate failed: {action['reason']}")
        break
    
    if action["type"] == "spawn":
        r = spawn(
            action["prompt"],
            context_files=action["context_files"],
            context_data=action.get("context_data"),
            allow_tools=True
        )
        write("create", f"{workspace}/{action['output_file']}", file_text=r.response)
```

## Handling Exceptions

The state machine handles the happy path. When things go wrong, **exercise judgment**:

| Exception | Response |
|-----------|----------|
| Spawn times out | Assess: retry with longer timeout? Report partial progress? |
| Spawn returns error | Report failure to state machine, let it track retries |
| Empty/invalid response | Treat as failure, report to state machine |

**Don't silently advance past failures.** Either retry, fail explicitly, or document gaps.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Read phase files yourself | Pass phase files via context_files to subagents |
| Decide what phase is next | State machine decides via next-step.py |
| Skip gates "because it looks done" | Always validate gates |
| Store state in your memory | State lives in progress.json |
| Silently advance past failures | Retry, fail, or document gaps |

## Phases

1. **SETUP**: Determine feature number, create feature name, check for idea honing document, create feature directory
2. **DRAFT**: Copy template and work with user to fill in concept document as narrative
3. **REVIEW**: Review for narrative flow, validate creation, provide recommendations

## Inputs

- Feature idea description from user
- Optional: idea-honing.md from prior idea honing session

## Outputs

- `docs/features/NNNN-feature-name/concept.md` - The feature concept document
- `planning/<feature-slug>/review.md` - Review and next steps

## Next Steps

After creating the concept:
1. Review and refine the narrative
2. Get feedback on whether the feature is valuable
3. Once concept is solid, move to requirements using `propose-feature-requirements` skill
