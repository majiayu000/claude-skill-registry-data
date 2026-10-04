---
name: testing-skills-with-subagents
description: DEPRECATED - Use writing-skills instead. This functionality has been consolidated into writing-skills which now contains both skill creation and testing methodology.
---

# Testing Skills With Subagents

## Migration Notice

All content from this skill has been integrated into the `writing-skills` skill, which now provides:

1. **Skill Structure and Formatting** (original writing-skills content)
2. **Testing Skills: Detailed Methodology** (original testing-skills-with-subagents content)
   - When to test skills
   - Writing pressure scenarios
   - Pressure types
   - Key elements of good scenarios
   - Testing setup
   - VERIFY GREEN process
   - Plugging holes systematically
   - Re-verification
   - Meta-testing
   - When skill is bulletproof
   - Complete worked examples

## Why the Merge?

The two skills described the same TDD process (RED-GREEN-REFACTOR) applied to documentation:
- **writing-skills** focused on skill structure, formatting, and CSO
- **testing-skills-with-subagents** focused on detailed testing methodology

Since skill creation REQUIRES testing (the Iron Law: "No skill without failing test first"), and testing IS part of creation, maintaining separate skills created:
- Content duplication (both explained RED-GREEN-REFACTOR)
- Token waste (loading duplicate content)
- Confusion (which skill to use when?)
- Maintenance burden (update in two places)

## Use `writing-skills` Instead

For all skill creation and testing needs, use the `writing-skills` skill, which now contains:
- Everything from the original writing-skills
- Everything from testing-skills-with-subagents
- Clear section organization
- No duplication
- Single source of truth

## Worked Examples

The complete worked example (`examples/CLAUDE_MD_TESTING.md`) referenced in this skill is still available in the `testing-skills-with-subagents` directory for historical reference.
