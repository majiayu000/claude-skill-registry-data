---
name: install-skill
description: Install a Claude skill from a GitHub URL or path.
---

# Install Skill

Installs a skill from GitHub into `~/.claude/skills/` so Claude Code picks it up globally.

## Accepted input formats

- Full GitHub folder URL: `https://github.com/owner/repo/tree/main/path/to/skill`
- Short form: `owner/repo/path/to/skill`
- Repo root (installs all skills found): `owner/repo`

## Workflow

1. Parse the input to extract `owner/repo` (combined, slash-separated) and `skill_path` (the subfolder, if any).

2. **Pre-flight: verify this is a skill repo before doing anything else.**
   WebFetch `https://github.com/<owner>/<repo>` (and `https://github.com/<owner>/<repo>/tree/HEAD/<skill_path>` if a subpath was given). Look for `SKILL.md` in the file listing on the page.
   - If `SKILL.md` is **not** listed: **stop immediately**. Explain to the user that this repo does not appear to be a Claude skill package, describe what it actually looks like (plugin, library, CLI tool, etc.) based on what you can see in the repo, and suggest the correct installation method if apparent. Do not run `install.sh`.
   - If `SKILL.md` is listed: proceed.

3. Run `scripts/install.sh <owner/repo> [skill_path]` — the repo is always passed as a single `owner/repo` argument, with the subpath as an optional second argument.
4. **Vendor-strip the new SKILL.md before promoting.** Open the installed `SKILL.md` and apply the strip list in `~/.claude/references/skills-management.md` § Post-Install: Promote + Vendor-Strip.
5. **Always promote to shared after install.** Run `~/projects/dotfiles/scripts/sync-skills.sh add <skill-name>`, then commit the new skill dir. Full contract (LOCAL state, install-one-question-one) → same reference section.
6. Confirm success and tell the user the skill name and install location.
7. If anything fails, show the error and suggest a fix.

## Edge cases to handle

- If the URL points to a repo root or a folder containing multiple skill subdirectories, ask the user which one they want.
- If a skill with the same name already exists in `~/.claude/skills/`, warn the user before overwriting.
