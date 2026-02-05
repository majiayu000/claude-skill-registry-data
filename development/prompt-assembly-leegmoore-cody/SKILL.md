---
name: prompt-assembly
description: Assembles coder and verifier prompts from templates. Use when user says "build a prompt", "assemble a prompt", "assemble prompts", or "generate a prompt" for dispatching work to coding and verification agents.
---

# Prompt Assembly

Assemble coder and verifier prompts from templates.

## When to Use

When user says "build a prompt", "assemble a prompt", "assemble prompts", or "generate a prompt" for dispatching work to coding and verification agents.

## Gathering Information

Before assembling, gather:

### Required
1. **Project** - Which project? (01-api, 02-ui, etc.)
2. **Job name** - Short name for filenames (e.g., "thinking-support")
3. **Job overview** - What does this work accomplish?
4. **Current state** - Where are we now?
5. **Technical spec** - The work to be done (can be inline or from file)
6. **Key files** - Which files are involved?

### Definition of Done
7. **Job-specific DoD items** - Beyond standard checks (tests/format/lint/typecheck)

### Optional
8. **Project why** - Why we need this work
9. **Known issues** - Bugs or errors to address
10. **Avoidances** - What should the agent NOT do?

## Assembly Process

1. Gather answers using `questions.md`
2. Create config.json with the data
3. Run: `node .claude/skills/prompt-assembly/assemble.js --config config.json`
4. Review generated prompts

## Output Options

Output directory priority:
1. `--output /path` CLI flag
2. `outputDir` field in config.json
3. Default: `projects/{project}/prompts/`

**Examples:**
```bash
# Default output
node .claude/skills/prompt-assembly/assemble.js --config config.json

# Custom output directory
node .claude/skills/prompt-assembly/assemble.js --config config.json --output /path/to/project/dir
```

## Output Files

- `{job-name}-coder.md` - For implementation agent
- `{job-name}-verifier.md` - For verification agent

## Files

- `templates/coder-prompt.hbs` - Coder prompt template
- `templates/verifier-prompt.hbs` - Verifier prompt template
- `assemble.js` - Template assembly script
- `questions.md` - Questions checklist
