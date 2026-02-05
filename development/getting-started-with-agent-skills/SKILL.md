---
name: Getting Started with Agent Skills
description: Skills for legacy code analysis, explanation, and safe refactoring - mandatory workflows and search tools
when_to_use: when starting any conversation
version: 1.0.0
---

# Getting Started with Agent Skills

## Agent Skills Focus

**Agent Skills** specialize in:
- **Analyzing legacy codebases** - Understanding existing code without documentation
- **Explaining concepts and mechanisms** - Making complex systems comprehensible
- **Safe refactoring** - Changing code without breaking production
- **Building mental models** - Creating understanding of how systems work
- **Brainstorming safe changes** - Introducing features into existing code

While general development skills (TDD, debugging) are included, the emphasis is on **working with code you didn't write**.

## Critical Rules

1. **Use Read tool before announcing skill usage.** The session-start hook does NOT read skills for you. Announcing without calling Read = lying.

2. **Follow mandatory workflows.** Brainstorming before coding. Check for skills before ANY task.

3. **Create TodoWrite todos for checklists.** Mental tracking = steps get skipped. Every time.


## Mandatory Workflow: Before ANY Task

**1. Check skills list** at session start, or run `find-skills [PATTERN]` to filter.

**2. If relevant skill exists, YOU MUST use it:**

- Use Read tool with full path: `${AGENT_SKILLS_ROOT}/skills/category/skill-name/SKILL.md`
- Read ENTIRE file, not just frontmatter
- Announce: "I've read [Skill Name] skill and I'm using it to [purpose]"
- Follow it exactly

**Don't rationalize:**
- "I remember this skill" - Skills evolve. Read the current version.
- "Session-start showed it to me" - That was using-skills/SKILL.md only. Read the actual skill.
- "This doesn't count as a task" - It counts. Find and read skills.

**Why:** Skills document proven techniques that save time and prevent mistakes. Not using available skills means repeating solved problems and making known errors.

If a skill for your task exists, you must use it or you will fail at your task.

## Skills with Checklists

If a skill has a checklist, YOU MUST create TodoWrite todos for EACH item.

**Don't:**
- Work through checklist mentally
- Skip creating todos "to save time"
- Batch multiple items into one todo
- Mark complete without doing them

**Why:** Checklists without TodoWrite tracking = steps get skipped. Every time. The overhead of TodoWrite is tiny compared to the cost of missing steps.

**Examples:** skills/testing/test-driven-development/SKILL.md, skills/debugging/systematic-debugging/SKILL.md, skills/refactoring/characterization-testing/SKILL.md

## Announcing Skill Usage

After you've read a skill with Read tool, announce you're using it:

"I've read the [Skill Name] skill and I'm using it to [what you're doing]."

**Examples:**
- "I've read the Code Archaeology skill and I'm using it to understand this legacy module."
- "I've read the Characterization Testing skill and I'm using it to add safety net before refactoring."
- "I've read the Strangler Fig Pattern skill and I'm using it to replace this legacy component safely."

**Why:** Transparency helps your human partner understand your process and catch errors early. It also confirms you actually read the skill.

## How to Read a Skill

Every skill has the same structure:

1. **Frontmatter** - `when_to_use` tells you if this skill matches your situation
2. **Overview** - Core principle in 1-2 sentences
3. **Quick Reference** - Scan for your specific pattern
4. **Implementation** - Full details and examples
5. **Supporting files** - Load only when implementing

**Many skills contain rigid rules (TDD, debugging, characterization testing).** Follow them exactly. Don't adapt away the discipline.

**Some skills are flexible patterns (architecture, refactoring strategies).** Adapt core principles to your context.

The skill itself tells you which type it is.

## Instructions ≠ Permission to Skip Workflows

Your human partner's specific instructions describe WHAT to do, not HOW.

"Add X", "Fix Y" = the goal, NOT permission to skip brainstorming, characterization testing, or systematic analysis.

**Red flags:** "Instruction was specific" • "Seems simple" • "Workflow is overkill"

**Why:** Specific instructions mean clear requirements, which is when workflows matter MOST. Skipping process on "simple" tasks is how simple tasks become complex problems.

## Working with Legacy Code

**Special emphasis in Agent Skills:**

- **Always understand before changing** - Use code-archaeology skill first
- **Add tests before refactoring** - Characterization testing creates safety net
- **Refactor incrementally** - Strangler fig pattern, parallel change
- **Document as you go** - Reverse-engineering docs helps everyone
- **Question assumptions** - Use questioning-techniques skill

**Legacy code principle:** The code you're looking at is solving a problem. Understand the problem before changing the solution.

## Summary

**Starting any task:**
1. Run find-skills to check for relevant skills
2. If relevant skill exists → Use Read tool with full path (includes /SKILL.md)
3. Announce you're using it
4. Follow what it says

**Skill has checklist?** TodoWrite for every item.

**Finding a relevant skill = mandatory to read and use it. Not optional.**

**Working with legacy code?** Understanding and safety come before speed.
