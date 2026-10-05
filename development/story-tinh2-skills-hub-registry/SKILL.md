---
name: story
description: "Full story lifecycle — review, implement, and PR. Takes a story from architecture review through implementation to pull request creation."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous story implementation agent. Do NOT ask the user questions.

This skill chains three skills in sequence:
1. `/arch-review` — review the story's design and flag gaps
2. `/story-implementer` — implement the story with tests
3. `/pr` — create a convention-compliant pull request

INPUT: $ARGUMENTS
A story description — text, image, URL, ticket reference, or plain description of what to build.

============================================================
PHASE 1: ARCHITECTURE REVIEW
============================================================

Follow the instructions defined in the `/arch-review` skill in Design Review mode.

Pass the input story to the arch-review skill. It will:
- Analyze the story's scope and design
- Check for missing acceptance criteria
- Validate the proposed approach against codebase conventions
- Flag any design gaps or concerns

If the review finds CRITICAL gaps:
- Attempt to resolve them autonomously (adjust the approach, add missing criteria).
- If unresolvable, document them and proceed — the implementation will address them.

Record the review verdict and any adjustments for the implementation phase.

============================================================
PHASE 2: IMPLEMENT
============================================================

Follow the instructions defined in the `/story-implementer` skill.

Pass the original story PLUS any adjustments from the architecture review.

The story-implementer skill will:
- Implement the story following repository conventions
- Write unit tests with full coverage
- Follow the codebase's established patterns and architecture
- Commit with conventional commit format per project conventions
- Push after committing

============================================================
PHASE 3: CREATE PR
============================================================

Follow the instructions defined in the `/pr` skill.

The pr skill will:
- Extract the story/ticket reference from the branch name if available
- Generate a summary from the commits and changes
- Create a PR with a test plan and relevant links
- Enforce all CLAUDE.md conventions


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Story Complete

### Architecture Review
- **Verdict:** {approved / approved with adjustments}
- **Adjustments:** {list any changes made to the approach, or "none"}

### Implementation
- **Files changed:** {count}
- **Tests written:** {count}
- **Commits:** {count}

### Pull Request
- **PR:** {URL}
- **Story:** {story/ticket reference if available}
- **Title:** {PR title}

NEXT STEPS:
- "Review the PR and merge when ready."
- "Run `/preflight` for pre-deploy verification."
- "Run `/qa` for full QA verification before merging."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /story — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
