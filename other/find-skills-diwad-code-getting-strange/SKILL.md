---
name: find-skills
description: Helps users discover, search, and install skills from the skills.sh registry using the npx skills CLI. Use this skill when users ask to find skills, browse the skill registry, install a skill, or search for skills by name or functionality.
version: 1.0.0
---

# Find Skills

This skill guides the AI to help users discover and install skills from the [skills.sh](https://skills.sh) registry using the `skills` CLI.

## When to Use

Use this skill when the user:
- Asks to find, search, or browse available skills
- Wants to install a skill by name or GitHub path
- Asks "what skills are available?" or "is there a skill for X?"
- Wants to explore the skills registry

## How to Search for Skills

To search the registry, run:

```bash
npx skills search <query>
```

Example:
```bash
npx skills search pdf
npx skills search invoice
npx skills search github
```

This lists matching skills with their names, descriptions, and GitHub paths.

## How to Install a Skill

To install a skill globally (available to Desktop Commander):

```bash
npx skills add <github-path> --yes --global
```

Example:
```bash
npx skills add desktop-commander/skills/pdf --yes --global
```

The `--yes` flag skips confirmation prompts. The `--global` flag installs into `~/.agents/skills/` so Desktop Commander picks it up automatically.

## Workflow

1. Ask the user what kind of skill they are looking for (or what task they want to automate)
2. Run `npx skills search <query>` with relevant keywords
3. Present the results to the user — name, description, and GitHub path
4. If the user wants to install one, run `npx skills add <github-path> --yes --global`
5. Confirm the skill appears in the sidebar (Desktop Commander auto-detects new skills)
6. Let the user know the skill is ready to use

## Notes

- Skills are installed to `~/.agents/skills/` by default when using `--global`
- The registry is hosted at [skills.sh](https://skills.sh) — browsable in a browser too
- Each installed skill is immediately available to the AI in new conversations
- Re-running `npx skills add` on an existing skill will update it to the latest version
