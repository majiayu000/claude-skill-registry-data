---
name: skill-system
description: Load when you struggled with something docs would have helped, when you're about to move on from a complex area you now understand, or when managing skills
---

## Philosophy

Skills are **crystallized knowledge** - patterns, gotchas, and how-tos that would help future sessions work faster. They emerge organically from actual work, not from planning.

**You have full agency to evolve this system:**
- Create skills when you discover patterns worth preserving
- Update skills when they become stale or incomplete
- Remove skills that are no longer useful
- Merge overlapping skills, split overgrown ones
- Improve this very skill when you find better approaches

## Proactive Triggers

**Load this skill when you notice:**
- "I wish I had known this before starting" - document it for next time
- "A future session would need to figure this out again" - capture it now
- "This pattern isn't obvious from the code" - write it down
- You're about to move on from a complex area you just understood deeply

**Domain signals for this codebase:**
- After understanding flash loan flows, UTXO tracking, or instruction encoding
- After debugging a tricky protocol integration (Aave, Morpho, Compound, Venus)
- After learning Starknet-specific patterns vs EVM patterns
- After discovering why something was built a certain way

## When to Create a Skill

Ask yourself:
1. Did I struggle with something that documentation would have helped?
2. Is this pattern recurring and non-obvious from code alone?
3. Would a future session benefit from this knowledge?
4. Am I about to context-switch away from hard-won understanding?

If yes to any, **pause and create a skill before moving on**.

**Don't create skills for:**
- One-off tasks
- Things obvious from reading the code
- External library docs (just link to them)

## When to Update a Skill

- You changed code that a skill documents
- A skill's file paths or examples are wrong
- You discovered better patterns in a covered area
- A skill gave you outdated or incorrect advice

## When to Remove a Skill

- The skill's content is now obvious from the code itself
- The skill hasn't been useful (loaded but not helpful)
- The area it covers no longer exists

## Skill Registry

The skill index lives at `.opencode/skill/INDEX.md`. **Always update it** when creating or removing skills.

To see current skills:
```bash
cat .opencode/skill/INDEX.md
```

## How to Create a Skill

1. **Create the directory and file:**
   ```bash
   mkdir -p .opencode/skill/<name>
   ```

2. **Create `SKILL.md` with frontmatter:**
   ```yaml
   ---
   name: <name>
   description: Load when <trigger conditions>
   ---
   ```

3. **Write the content:**
   - Focus on "how to", not just "what is"
   - Include real code examples from the codebase
   - Keep it under 1500 words
   - Use file paths like `path/to/file.ts:123` for navigation

4. **Update the index:**
   - Add entry to `.opencode/skill/INDEX.md`

### Naming Convention

- Lowercase, hyphenated: `ui-patterns`, `flash-loans`
- Be specific: `morpho-blue` not `lending`
- Action-oriented when possible: `debugging-evm` not `evm-errors`

### Description Format

Start with "Load when..." to make triggers clear:
- "Load when implementing flash loan operations or debugging flash loan failures"
- "Load when adding a new lending protocol to the dashboard"

## How to Update a Skill

1. Read the current skill content
2. Compare with current implementation
3. Edit to reflect the actual state
4. Keep under 1500 words
5. Update INDEX.md if description changed

## How to Remove a Skill

1. Delete the directory: `rm -rf .opencode/skill/<name>`
2. Remove from `.opencode/skill/INDEX.md`

## Quality Guide

Good skills have:
- Clear trigger conditions in the description
- Actionable content (how to do X, not just what X is)
- Real code examples from this codebase
- Current file paths
- Focused scope (one area, not everything)

## Self-Evolution

This skill should improve over time. If you find:
- The creation process is clunky -> simplify it
- Skills keep going stale -> add freshness heuristics
- Categories naturally emerge -> document them
- Better patterns for skill content -> update the guide

The meta-goal: make knowledge capture effortless and valuable.
