---
name: propose-feature-requirements
description: Create or update feature requirements specification using EARS notation with examples and appendices
---

# Propose Feature Requirements Skill

Create a formal requirements specification for a feature using EARS notation. This translates the concept into testable, specific requirements.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., VERIFY.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```
workspace = "planning/<feature-slug>"
mkdir workspace

while True:
  action = bash("python3 skills/propose-feature-requirements/next-step.py <workspace>")
  parse action as JSON
  
  if action.type == "done":
    read workspace/03-validate.md for final results
    break
  
  if action.type == "gate_failed":
    report failure: action.reason
    break
  
  if action.type == "spawn":
    result = spawn(
      prompt = action.prompt,
      context_files = action.context_files,
      context_data = action.context_data,
      allow_tools = True
    )
    write result to workspace/<action.output_file>
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

1. **VERIFY**: Check that concept exists and identify any idea-honing insights
2. **SETUP**: Copy template and determine requirements prefix
3. **WRITE**: Fill in requirements using EARS notation with examples and appendices
4. **VALIDATE**: Review for completeness, testability, and correct formatting

## Inputs

Before starting, gather:
- Feature number and name (format: NNNN-feature-name)
- Concept document must exist at docs/features/NNNN-feature-name/concept.md

## Outputs

- Requirements specification at docs/features/NNNN-feature-name/requirements.md
- Validation report at workspace/03-validate.md

## When to Use

- Feature concept exists and is approved
- Need to specify exactly what the system must do
- Ready to define functional and non-functional requirements

## Prerequisites

- Feature concept document exists in `docs/features/NNNN-feature-name/concept.md`
- Concept has been reviewed and approved
- User understands the feature scope

## Next Steps

After creating requirements:
1. Review for completeness and testability
2. Get feedback from implementors
3. Once requirements are solid, move to design using `propose-feature-design` skill
