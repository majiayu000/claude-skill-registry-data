---
name: import-theme-skills
description: Copy custom Claude Code skills bundled inside a theme into the user's `.claude/skills/` directory. Use when asked to "import theme skills", "copy skills from theme", or similar requests to install skill files that ship with a Baan theme.
---

# Import Theme Skills

Baan themes can bundle custom Claude Code skills at `themes/<name>/prompts/skills/*.md`. This skill copies those files into the user's local `.claude/skills/` directory so they become usable Claude Code commands.

## When to Use

Trigger this skill when the user says any of:

- "import theme skills"
- "import skills from theme X"
- "copy skills from theme X"
- "install the bundled skills from a theme"

## What This Skill Does

1. Take a theme name as input (ask if missing)
2. List skill files at `themes/<name>/prompts/skills/*.md`
3. For each file, show metadata (name, description) for user review
4. Ask the user to confirm before copying — especially if the destination already exists
5. Copy each approved file into `.claude/skills/<skill-name>/SKILL.md`
6. Report what was imported, what was skipped, and what was overwritten

## Workflow

### Step 1: Identify the theme

Ask the user which theme to import from if they didn't specify:

```
Which theme would you like to import skills from?
Available themes: default, geek, news, monograph, slate, terminal, the-publish, <custom>
```

Accept either a built-in name or a custom theme directory name.

### Step 2: Scan the skills directory

Check `themes/<name>/prompts/skills/`:

- **If the directory does not exist**: report "Theme '<name>' does not bundle any custom skills — nothing to import." and exit.
- **If the directory is empty**: same as above.
- **If the theme directory itself does not exist**: report the error and list available themes.

### Step 3: Read each skill file

For every `themes/<name>/prompts/skills/*.md`, read the YAML frontmatter:

```yaml
---
name: my-custom-skill
description: Short description of what the skill does
---
```

**Validation**:
- The file must start with `---` YAML frontmatter
- `name` field is required
- `description` field is required
- If frontmatter is missing or malformed, skip the file and report it as invalid

### Step 4: Present the import plan

Show the user each skill that will be imported:

```
Found 2 skills in theme "sunset":

1. sunset-color-tweaker
   Description: Generate harmonious color palettes for the sunset theme
   Destination: .claude/skills/sunset-color-tweaker/SKILL.md
   Status: NEW

2. sunset-layout-switcher
   Description: Swap between layout variants of the sunset theme
   Destination: .claude/skills/sunset-layout-switcher/SKILL.md
   Status: EXISTS (will overwrite)

Proceed? [yes / skip-existing / cancel]
```

**Statuses**:
- `NEW` — destination does not exist, safe to create
- `EXISTS` — destination already exists, needs explicit confirmation

Require **explicit approval** before writing anything. "yes" imports everything. "skip-existing" imports only the NEW ones. "cancel" does nothing.

### Step 5: Copy approved skills

For each approved skill:

1. Create directory `.claude/skills/<skill-name>/` if it does not exist
2. Copy the source file to `.claude/skills/<skill-name>/SKILL.md`
3. Do not modify the file contents — preserve the bundled skill exactly as the theme author wrote it

### Step 6: Report results

```
Imported 1 skill, skipped 1:

✓ sunset-color-tweaker       → .claude/skills/sunset-color-tweaker/SKILL.md
⊗ sunset-layout-switcher     skipped (user chose skip-existing)

Restart Claude Code to load the new skill.
```

## Safety Rules

- **Never overwrite without confirmation.** If the destination file exists, require explicit user approval.
- **Validate YAML frontmatter before copying.** A file without valid frontmatter is not a valid skill and must be skipped.
- **Never copy files outside `prompts/skills/`.** Only files directly in that directory (no subdirectories) are valid skill sources.
- **Preserve file contents exactly.** This skill does not transform, reformat, or add to bundled skill files.
- **Report what was skipped.** Users need to know which files didn't transfer and why.

## Notes

- Claude Code must be restarted (new session) to pick up newly imported skills
- Imported skills are independent of the theme after import — removing the theme does not remove the imported skill
- If the user wants to remove an imported skill later, they delete `.claude/skills/<skill-name>/` manually
