---
name: propose-feature-design
description: Create or update feature technical design document with architecture and implementation guidance
---

# Propose Feature Design Skill

Create a technical design document that guides implementation. This provides architecture, patterns, and design decisions without writing the actual code.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, feature files | Decides next action, validates gates |
| Subagent | Phase file (e.g., VERIFY.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## When to Use

- Feature concept and requirements exist
- Ready to plan the implementation approach
- Need to document architecture and design patterns

## Orchestrator Loop

```python
import json

feature_dir = "docs/features/NNNN-feature-name"

while True:
  result = bash(f"python3 skills/propose-feature-design/next-step.py {feature_dir}", on_error="raise")
  action = json.loads(result)
  
  if action["type"] == "done":
    log(f"Design document created at {feature_dir}/design.md")
    break
  
  if action["type"] == "gate_failed":
    log(f"Gate failed: {action['reason']}")
    break
  
  if action["type"] == "spawn":
    r = spawn(
      action["prompt"],
      context_files=action["context_files"],
      context_data=action["context_data"],
      allow_tools=True
    )
    write("create", f"{feature_dir}/{action['output_file']}", file_text=r.response)
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
| Store state in your memory | State lives in .design-progress.json |
| Silently advance past failures | Retry, fail, or document gaps |

## Phases

1. **VERIFY**: Check that concept.md and requirements.md exist
2. **PREPARE**: Copy design template and check for idea-honing context
3. **DESIGN**: Fill in all design sections (overview, constraints, architecture, domain model, etc.)

## Inputs

- Feature directory path: `docs/features/NNNN-feature-name`
- Existing files: `concept.md`, `requirements.md`
- Optional: `planning/NNNN-feature-name/idea-honing.md`

## Outputs

- `docs/features/NNNN-feature-name/design.md`: Complete design document

## Design Document Sections

The DESIGN phase fills in:

- **Overview**: High-level architecture and approach
- **Critical Constraints**: What MUST be done specific ways (most important section)
- **Architecture**: Component relationships, data flow, layer responsibilities
- **Domain Model**: Core types, operations, invariants
- **Module Structure**: Directory layout and organization
- **Design Patterns**: Relevant patterns and why they apply
- **Design Decisions**: Key choices and rationale
- **Implementation Guidance**: References to constraints, performance, testing

## Critical Constraints

The most important section for preventing implementation mistakes. For each key operation:
- What would be WRONG?
- What performance is required?
- What invariants must hold?

Format:
- **ID**: CC-1, CC-2, etc.
- **Constraint**: What MUST be done a specific way
- **Rationale**: Why (performance, correctness, security)
- **Anti-pattern**: The wrong approach to reject

Be specific—vague constraints don't help.

## Validation

The state machine validates:
- Prerequisites exist (concept.md, requirements.md)
- Template copied successfully
- Design document created and has substantial content (>500 chars)

## Next Steps

After creating the design:
1. Review with implementors for feasibility
2. Refine based on feedback
3. Create test plan using `propose-feature-test-plan` skill
4. Create implementation plan using `propose-implementation-plan` skill
