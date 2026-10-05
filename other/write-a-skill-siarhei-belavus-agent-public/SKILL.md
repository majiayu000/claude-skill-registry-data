---
name: write-a-skill
description: Create new agent skills with clear triggers, compact instructions, and optional bundled references or helper scripts. Use when user wants to create, write, design, refine, or package a reusable skill.
---

# Writing Skills

## Process

1. **Gather requirements**
   - Task/domain covered
   - Concrete triggers and example requests
   - Output shape: instructions only vs helper scripts/resources
   - Target scope: personal, project-local, or shareable
   - Any reference material, conventions, or constraints

2. **Design the skill shape**
   - Keep the main path short
   - Put rare/advanced material in linked files
   - Add scripts only for deterministic or repetitive work
   - Prefer one reusable skill over many overlapping ones

3. **Draft the skill package**
   - Create `SKILL.md`
   - Add `REFERENCE.md`, `EXAMPLES.md`, or templates only if they reduce clutter
   - Keep assets beside the skill that uses them

4. **Review with the user**
   - Does it trigger on the right requests?
   - Is the default workflow clear?
   - Anything ambiguous, missing, or too verbose?
   - Should it stay broad or be split into multiple skills?

## Skill Structure

```text
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (optional)
├── EXAMPLES.md        # Example prompts/flows (optional)
├── templates/         # Template files (optional)
└── scripts/           # Helper scripts (optional)
    └── helper.js
```

Rules:
- `SKILL.md` must live inside the skill directory
- Frontmatter `name` must match the skill directory name exactly
- Nested category folders are fine; the immediate parent directory is the skill name
- If tool restrictions matter, add `allowed-tools` in frontmatter

Example:

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
allowed-tools: read bash write
---
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working path]

## Workflow

[Ordered steps for the common case]

## Edge cases

[Constraints, gotchas, escalation rules]

## References

See [REFERENCE.md](REFERENCE.md)
```

## Description Requirements

The description is the routing signal used to decide whether to load the skill.
Write it so the runtime can distinguish this skill from nearby ones.

Include:
1. What capability it provides
2. When to trigger it
3. Concrete keywords, contexts, domains, or file types

Format:
- Keep it short and specific
- Write in third person / neutral imperative
- First clause: what it does
- Second clause: `Use when ...`

Good:

```text
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs, forms, or document extraction.
```

Bad:

```text
Helps with documents.
```

## When to Add Scripts

Add helper scripts when:
- The operation is deterministic
- The same code would otherwise be regenerated often
- Validation or formatting should be exact
- Failure modes need explicit handling

Do not add scripts for one-off reasoning.

## When to Split Files

Split into linked files when:
- `SKILL.md` is getting crowded
- Some content is rare or advanced
- Examples/templates would distract from the common path
- Reference material changes independently from the main workflow

Keep references shallow and intentional.

## Review Checklist

After drafting, verify:
- [ ] Description clearly says `Use when ...`
- [ ] `name` matches directory name
- [ ] Default workflow easy to follow
- [ ] No platform-specific assumptions unless intentional
- [ ] No stale or time-sensitive claims
- [ ] Examples/triggers concrete
- [ ] References only added when they reduce clutter
- [ ] Tool access narrowed when useful

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
