---
name: propose-implementation-plan
description: Create an implementation plan with atomic commits that build toward a complete feature
---

# Propose Implementation Plan Skill

Create a detailed implementation plan that breaks a feature into atomic, reviewable commits.
The plan serves as a roadmap for implementation, ensuring each commit is self-contained, tested, and buildable.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., SETUP.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## When to Use

- Feature design document exists and is approved
- Ready to begin implementation
- Need to coordinate work or track progress
- Want to ensure commits are appropriately sized

## Prerequisites

- Feature design exists in `docs/features/NNNN-feature-name/design.md`
- Test plan exists in `docs/features/NNNN-feature-name/test-plan.md`
- Design and test plan have been reviewed and approved
- Implementor understands the technical approach

## Orchestrator Loop

```python
import json

workspace = f"planning/{feature_number}-{feature_name}"
bash(f"mkdir -p {workspace}", on_error="raise")

while True:
    result = bash(f"python3 skills/propose-implementation-plan/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)
    
    if action["type"] == "done":
        final_plan = fs_read("Line", f"{workspace}/implementation-plan.md", 1, -1)
        log(f"Implementation plan created at {workspace}/implementation-plan.md")
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

1. **SETUP**: Verify design exists, create planning directory, copy template
2. **ANALYZE**: Study design/test plan, extract constraints, identify boundaries
3. **PLAN**: Break feature into atomic commits with proper sizing and dependencies
4. **FINALIZE**: Validate plan and write final implementation-plan.md

## Inputs

Before starting, gather:
- Feature number (e.g., `0042`)
- Feature name (e.g., `multi-context-support`)

The workspace will be `planning/{number}-{name}`.

## Outputs

- `planning/NNNN-feature-name/implementation-plan.md` - Final implementation plan
- `planning/NNNN-feature-name/00-setup.md` - Setup phase output
- `planning/NNNN-feature-name/01-analyze.md` - Analysis phase output
- `planning/NNNN-feature-name/02-plan.md` - Planning phase output
- `planning/NNNN-feature-name/progress.json` - State machine progress

## Atomic Commit Rules

The plan ensures each commit follows these rules:

**Each commit MUST be:**

1. **Buildable** - The project compiles after this commit
2. **Tested** - New code has tests; existing tests pass (or are explicitly disabled with TODO)
3. **Focused** - Does one logical thing
4. **Reviewable** - Small enough to review in one sitting (target: <400 lines changed)

**Each commit SHOULD:**

1. **Be independently valuable** - Provides some benefit even if later commits aren't merged
2. **Have a clear purpose** - The commit message explains why, not just what
3. **Minimize risk** - Smaller commits are easier to revert if problems arise

## Handling Test Breakage

When a commit breaks tests in distant modules (e.g., schema changes that break integration tests), the plan will explicitly disable them with a TODO that references when they should be re-enabled.

**Pattern for disabling tests:**

```rust
// TODO: Re-enable in Commit 9a after updating domain types
#[cfg(all(test, feature = "enable_broken_tests"))]
mod tests {
    // ...
}
```

Or for individual tests:

```rust
#[test]
#[ignore] // TODO: Re-enable in Commit 12a after facade integration
fn test_search_returns_results() {
    // ...
}
```

## Commit Sizing Guidelines

**Too Small** (avoid):
- Adding a single import
- Renaming one variable
- Adding an empty module

**Too Large** (avoid):
- Entire feature in one commit
- Multiple unrelated changes
- Changes that take days to review

**Just Right** (target):
- Add a new type with its tests (~50-200 lines)
- Implement a trait for one adapter (~100-300 lines)
- Add a new CLI command with tests (~100-300 lines)
- Refactor a module to prepare for new feature (~100-400 lines)

## Validation

The finalize phase validates that:
- [ ] Each commit is atomic and buildable
- [ ] Commits are appropriately sized (target <400 lines)
- [ ] Dependencies are clearly stated
- [ ] Testing approach is documented for each commit
- [ ] Phases group related work logically
- [ ] Critical constraints are mapped to commits
- [ ] Requirements are mapped to commits

## Next Steps

After creating the implementation plan:
1. Review with team for feasibility and sizing
2. Adjust based on feedback
3. Begin implementation, checking off commits as completed
4. Update plan if implementation reveals needed changes
5. Use the checklist to track progress
