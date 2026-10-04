---
name: skill-self-review
description: Mandatory post-run self-review for any Northwatch Wardens skill. Analyzes the just-completed run against the skill's definition, surfaces improvement opportunities, and either prompts the user for implementation decisions (interactive) or appends recommendations to the central improvement log (agentic). Every skill must invoke this at completion.
argument-hint: <skill-name> [--agentic]
allowed-tools: Read Write Glob
---

$ARGUMENTS

Read `.claude/skills/<skill-name>/SKILL.md` to compare intent against what actually happened in this run.

## Review — what to look for

Reflect on the just-completed run:

- **Ambiguity:** Did any instruction require re-reading, re-prompting, or guessing?
- **Gaps:** Did the skill omit a step the run needed to add on the fly?
- **Friction:** Did the skill ask for something that wasn't needed, or in the wrong order?
- **Output quality:** Was anything in the output weaker than it should have been given the skill's stated goal?
- **Parallel opportunities:** Were steps run sequentially that could have been parallel?

Generate 1–3 recommendations. Each must be concrete (what exact text changes), evidence-based (tied to something that happened in this run), and not already present in the skill.

---

## Interactive mode (no `--agentic`)

Present each recommendation:

```
Skill: <name>
Recommendation: <what to change>
Why: <what happened this run that motivates it>
Change: <exact replacement or addition>
```

Ask once: "Implement any of these? [1 / 2 / 3 / all / none]"

Apply approved changes directly to the skill file. Confirm what was changed.

---

## Agentic mode (`--agentic`)

Append to `.claude/logs/skill-improvements.md` — create the file if it doesn't exist:

```markdown
### <YYYY-MM-DD> · <skill-name>

**Recommendation:** <what to change>
**Why:** <evidence from this run>
**Proposed change:** <exact text>

---
```

Do not prompt. Do not modify any skill files. One entry per recommendation.
