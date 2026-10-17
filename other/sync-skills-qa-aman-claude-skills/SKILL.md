---
name: sync-skills
description: Fetch skills from projects on the current system, genericize them, and add to the claude-skills repository. Use when user says "sync skills", "fetch skills", "import skills from projects", or wants to pull skills from their local projects into this public repo.
---

# Sync Skills from Local Projects

## Overview

This skill scans projects on the current system for Claude Code skills (`.claude/skills/` directories), identifies new or updated skills, genericizes them by stripping project-specific content, and adds them to this repository.

## Workflow

### Step 1: Identify the Claude Skills Repo

The target repo is the `claude-skills` project. Confirm its location - it should be the current working directory or specified by the user.

### Step 2: Scan for Skills

Search for skills across local projects:

```
Find all directories matching: <projects-root>/*/.claude/skills/*/SKILL.md
```

Default projects root: `[your projects root]` (e.g. `~/Documents/Projects/`). The user may override this with a different path.

For each found skill, collect:
- Skill name (directory name)
- Source project name
- SKILL.md content
- Any files in `references/`, `assets/`, `scripts/` subdirectories

### Step 3: Deduplicate

Compare found skills against skills already in `skills/by-role/` and `skills/shared/` directories of this repo:
- **New skill**: not present in repo - proceed to genericize
- **Updated skill**: present but source has newer/different content - show diff, ask user whether to update
- **Identical**: skip silently

### Step 4: Determine the Role

For each new skill, determine which role folder it belongs in:

Valid roles: `pm`, `engineer`, `qa`, `designer`, `content-creator`, `devops`, `shared`, `leadership`, `program-delivery-manager`, `customer-success`, `recruiter`, `consultant`, `sales`, `marketing`, `founder`, `data-scientist`, `data-engineer`, `security`

If the role is unclear, ask the user before proceeding.

### Step 5: Genericize

For each new or updated skill, apply these transformations:

**Replace personal references:**
- Author names, handles, usernames -> remove or replace with `[your name]`
- Newsletter/blog names -> `[your newsletter]`
- Specific domains (e.g., `name.substack.com`) -> `[your-domain]`
- Niche or topic tied to the author -> `[your niche]` or `[your topic]`
- Company names -> `[your company]`
- Team names -> `[your team]`
- Client names -> `[your client]`
- Project-specific program names -> `[your program]`

**Remove project-specific content:**
- File paths referencing the source project
- References to other project-specific skills, configs, or workflows
- Environment variables specific to the source project
- API keys, tokens, or credentials (should never exist, but check)

**Preserve:**
- The skill's core logic, frameworks, and checklists
- Generic examples and templates
- Anti-patterns and quality criteria
- References to general tools or platforms (LinkedIn, Substack, etc.)
- The book or methodology the skill is grounded in

**Verify:**
- YAML frontmatter has `name` and `description` fields
- Description has multiple trigger phrases and is pushy
- Body is under 500 lines
- No personal/project-specific content remains
- Skill is self-contained (no broken references to removed content)

### Step 6: Add to Repo

For each genericized skill, use `init_skill.py` to scaffold and register in `skills.json`:

```bash
python3 scripts/init_skill.py <skill-name> --role <role> --description "<one-liner>" --tags "<tag1,tag2>"
```

This creates `skills/by-role/<role>/<skill-name>/SKILL.md` and adds the entry to `skills.json` automatically.

Then overwrite the scaffolded SKILL.md with the genericized content.

Do **not** manually edit `install.sh` - it reads from `skills.json`. The registry is the source of truth.

### Step 7: Validate

```bash
python3 scripts/validate_skill.py
```

All skills must pass before committing.

### Step 8: Update README

Add a row to the correct role table in `README.md`:

```markdown
| `skill-name` | What it does | Book/methodology source |
```

### Step 9: Report and Commit

Output a summary:
- Skills added (with source project and role assigned)
- Skills updated (with what changed)
- Skills skipped (already identical)
- Skills needing manual review (couldn't fully genericize)

Commit with a clear message:
```bash
git add skills/by-role/<role>/<skill-name>/ skills.json README.md
git commit -m "sync <skill-name> from [source project]"
```

## Anti-Patterns

**Don't blindly copy.** Always read the source skill first. Some skills are deeply project-specific and can't be genericized.

**Don't merge skills.** If two projects have different versions of the same skill, ask the user which to keep.

**Don't strip too much.** The goal is to remove personal references, not gut the content. Frameworks, examples, and checklists should survive intact.

**Don't forget supporting files.** Check for `references/`, `assets/`, `scripts/` subdirectories and copy them too.

**Don't edit install.sh directly.** Use `init_skill.py` to register skills. `install.sh` reads from `skills.json` - the hardcoded array no longer exists.

## Quality Checklist

Before completing sync:

- [ ] Each new skill scaffolded with `init_skill.py` (creates folder + registers in skills.json)
- [ ] Each new skill has valid YAML frontmatter (name + description)
- [ ] Description has multiple trigger phrases
- [ ] No personal names, domains, or project paths remain
- [ ] Placeholder brackets used consistently: `[your niche]`, `[your newsletter]`, `[your-domain]`, `[your name]`, `[your company]`, `[your team]`, `[your client]`
- [ ] README.md skills table updated with new row
- [ ] `python3 scripts/validate_skill.py` passes
- [ ] Each skill is self-contained and works standalone
- [ ] Body under 500 lines per SKILL.md
