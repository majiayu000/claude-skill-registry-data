---
name: skillify
version: 0.1.0
license: MIT
description: Use when the user wants to turn a script, repeated workflow, runbook, or hard-won procedure into a reusable agent skill, or asks "make this a skill", "extract this into a skill", or "I keep doing this manually".
---

# skillify

Extract a procedure you keep repeating into a SKILL.md an agent can discover and follow. The input is a script, a shell history pattern, a runbook, or "the thing we just did"; the output is an installable skill.

## Is it worth a skill?

Make a skill when the technique was not obvious the first time, will recur across projects, and involves judgment. Do not make a skill for one-off fixes, things a linter or script can fully enforce (automate those instead), or project-specific conventions (those belong in the project's CLAUDE.md or AGENTS.md).

## Extraction

1. **Find the procedure, not the instance.** Strip session-specific paths, names, and values. What survives is the reusable spine: triggers, steps, decision points, failure modes.
2. **Capture the gotchas.** The non-obvious parts are the whole value: the flag that silently resets state, the step everyone skips, the error that means something different than it says. Interview the user or mine the transcript for "the thing that bit us".
3. **Decide what stays executable.** A script the skill calls beats prose describing the script. Put reusable code in `scripts/` next to SKILL.md and have the skill invoke it; keep judgment in the prose.

## Format

```markdown
---
name: verb-first-hyphenated-name   # or the tool's own name when wrapping a named tool
description: Use when [triggering conditions and symptoms only, third person, under 500 chars]
---

# name

One-paragraph overview: what this achieves and the core principle.

## Steps / Pattern (the procedure)
## Rules (the constraints that protect against known failures)
## Common mistakes (what went wrong historically, and the fix)
```

The description field is load-bearing: agents read it to decide whether to load the skill. Describe WHEN to use it (symptoms, triggers, situations), never summarize the workflow, or agents will follow the one-line summary instead of reading the skill.

## Placement

- Personal, all projects: user skills dir (`~/.claude/skills/` for Claude Code)
- One project, shared with the team: `.claude/skills/` in the repo
- Public: a plugin repo with a marketplace manifest

The same SKILL.md format works across harnesses that support agent skills; only the install location differs.

## Verify before calling it done

Hand the skill to a fresh agent (subagent or new session) with a realistic task that should trigger it. If the agent misapplies a step or asks a question the skill should have answered, the skill has a gap; fix it and re-test. An untested skill is a guess.

## Common mistakes

- Writing a narrative of last session instead of a reusable procedure.
- Description that summarizes the steps. Agents shortcut to it and skip the body.
- Inlining a 200-line script as a code block instead of shipping it as a file.
- Skipping the fresh-agent test because the skill "is obviously clear". Clear to the author is not clear to a cold reader.
