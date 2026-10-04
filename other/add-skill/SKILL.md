---
name: add-skill
description: Install agent skills from git repositories via npx skills add.
---

# add-skill

Use this skill when you need to install other agent skills from a git repo.

## When to Use
- You want to add skills from a GitHub or GitLab repository.
- You need to list available skills in a repo before installing.

## Steps
1. List skills: `npx skills add <source> --list`
2. Install specific skill(s): `npx skills add <source> --skill <name> [-g] [-a opencode] [-y]`
3. Install all skills: `npx skills add <source> -g -a opencode -y`

## Notes
- OpenCode global path: `~/.config/opencode/skills/`
- Use `-g` to install to global path.
- Supported sources: `owner/repo`, full URL, or direct path to skill dir.
- `npx add-skill ...` is deprecated and should not be used as the default workflow.
