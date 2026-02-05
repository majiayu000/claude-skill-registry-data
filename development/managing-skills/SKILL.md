---
name: managing-skills
description: Install, update, list, and remove Claude Code and OpenCode skills. Supports GitHub repositories (user/repo), GitHub subdirectory URLs, and .skill zip files. Can set up interoperability between Claude Code and OpenCode via symlinks. Use when user wants to install, add, download, update, sync, list, remove, uninstall, delete skills, or share skills between Claude Code and OpenCode.
---

<objective>
Manage Claude Code and OpenCode skills from multiple source types. Handle installation, updates, listing, and removal of skills at both user and project levels.
</objective>

<quick_start>
**Install a skill from GitHub:**
```bash
# User-level (available everywhere)
git clone https://github.com/user/repo ~/.claude/skills/repo

# Project-level (as submodule)
git submodule add https://github.com/user/repo .claude/skills/repo
```

**Always ask the user which location they want before installing.**
</quick_start>

<install_locations>
Skills can be installed in multiple locations depending on the tool:

**Claude Code:**
- User skills: `~/.claude/skills/<skill-name>/` - available in all projects
- Project skills: `<project>/.claude/skills/<skill-name>/` - available only in that project

**OpenCode:**
- User skills: `~/.config/opencode/skill/<skill-name>/` - available in all projects
- Project skills: `<project>/.opencode/skill/<skill-name>/` - available only in that project

**Important:** Always ask the user which location they want before installing.
</install_locations>

<skill_reference_types>

<type name="github-repository">
A dedicated GitHub repo containing a skill.

**How to recognize:**
- Shorthand: `user/repo`
- Full URL: `https://github.com/user/repo`
- May contain `/tree/<branch>` but NO path after the branch

**Install (User - Claude Code):**
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/user/repo ~/.claude/skills/repo
```

**Install (User - OpenCode):**
```bash
mkdir -p ~/.config/opencode/skill
git clone https://github.com/user/repo ~/.config/opencode/skill/repo
```

**Install (Project - as submodule):**
```bash
mkdir -p .claude/skills
git submodule add https://github.com/user/repo .claude/skills/repo
```

**Update (User):**
```bash
git -C ~/.claude/skills/skill-name pull
```

**Update (Project):**
```bash
git -C .claude/skills/skill-name pull
git add .claude/skills/skill-name
```
</type>

<type name="github-subdirectory">
A skill living as a subdirectory within a larger repository.

**How to recognize:**
- Contains `/tree/<branch>/` followed by a path within the repo
- Example: `https://github.com/org/repo/tree/main/skills/my-skill`
- Differs from Type 1: there's a path AFTER the branch name

**Parse the URL:**
- Repository: `https://github.com/org/repo`
- Subpath: `skills/my-skill`
- Skill name: `my-skill` (last path component)

**Install (User or Project):**
```bash
# Clone to temp directory
git clone --depth 1 https://github.com/org/repo /tmp/skill-clone-$$

# Copy subdirectory to target
mkdir -p ~/.claude/skills
cp -r /tmp/skill-clone-$$/skills/my-skill ~/.claude/skills/my-skill

# Create .skill-manager-ref with source URL
echo "https://github.com/org/repo/tree/main/skills/my-skill" > ~/.claude/skills/my-skill/.skill-manager-ref

# Cleanup
rm -rf /tmp/skill-clone-$$
```

**Update:**
```bash
# Read source URL
SOURCE_URL=$(cat ~/.claude/skills/my-skill/.skill-manager-ref)

# Re-run installation (same steps as above, overwrites existing)
```
</type>

<type name="skill-zip">
A `.skill` zip file hosted at any URL.

**How to recognize:**
- URL ends with `.skill`
- Example: `https://example.com/skills/my-skill.skill`

**Parse the URL:**
- Skill name: filename without `.skill` extension

**Install (User or Project):**
```bash
# Download to temp
curl -L -o /tmp/skill-$$.zip "https://example.com/skills/my-skill.skill"

# Create target and extract
mkdir -p ~/.claude/skills/my-skill
unzip -o /tmp/skill-$$.zip -d ~/.claude/skills/my-skill

# If zip contained a single directory, move contents up
if [ $(ls -1 ~/.claude/skills/my-skill | wc -l) -eq 1 ] && [ -d ~/.claude/skills/my-skill/* ]; then
  mv ~/.claude/skills/my-skill/*/* ~/.claude/skills/my-skill/
  rmdir ~/.claude/skills/my-skill/*/
fi

# Create .skill-manager-ref with source URL
echo "https://example.com/skills/my-skill.skill" > ~/.claude/skills/my-skill/.skill-manager-ref

# Cleanup
rm /tmp/skill-$$.zip
```

**Update:**
```bash
# Read source URL
SOURCE_URL=$(cat ~/.claude/skills/my-skill/.skill-manager-ref)

# Re-run installation (same steps as above, overwrites existing)
```
</type>

</skill_reference_types>

<operations>

<operation name="remove">
**User skill:**
```bash
rm -rf ~/.claude/skills/skill-name
```

**Project skill (submodule):**
```bash
git submodule deinit -f .claude/skills/skill-name
git rm -f .claude/skills/skill-name
rm -rf .git/modules/.claude/skills/skill-name
```

**Project skill (not a submodule):**
```bash
rm -rf .claude/skills/skill-name
```
</operation>

<operation name="list">
```bash
# Claude Code
ls ~/.claude/skills/
ls .claude/skills/

# OpenCode
ls ~/.config/opencode/skill/
ls .opencode/skill/
```
</operation>

<operation name="check-source">
**GitHub repo:**
```bash
git -C ~/.claude/skills/skill-name remote get-url origin
git -C ~/.claude/skills/skill-name rev-parse --short HEAD
```

**Subdirectory or Zip (has .skill-manager-ref):**
```bash
cat ~/.claude/skills/skill-name/.skill-manager-ref
```
</operation>

<operation name="post-install">
After installing any skill, check for and install dependencies:

```bash
# Python dependencies
if [ -f ~/.claude/skills/skill-name/requirements.txt ]; then
  pip install -r ~/.claude/skills/skill-name/requirements.txt
fi

# Node dependencies
if [ -f ~/.claude/skills/skill-name/package.json ]; then
  cd ~/.claude/skills/skill-name && npm install
fi
```
</operation>

<operation name="interop">
Make skills available to both Claude Code and OpenCode using symlinks.

**User-level (share skills globally):**

First, check which tool already has skills:
```bash
ls -la ~/.claude/skills 2>/dev/null
ls -la ~/.config/opencode/skill 2>/dev/null
```

If Claude Code has skills, make them available to OpenCode:
```bash
mkdir -p ~/.config/opencode
ln -s ~/.claude/skills ~/.config/opencode/skill
```

If OpenCode has skills, make them available to Claude Code:
```bash
mkdir -p ~/.claude
ln -s ~/.config/opencode/skill ~/.claude/skills
```

**Project-level (share skills in a project):**

If Claude Code has project skills, make them available to OpenCode:
```bash
mkdir -p .opencode
ln -s ../.claude/skills .opencode/skill
```

If OpenCode has project skills, make them available to Claude Code:
```bash
mkdir -p .claude
ln -s ../.opencode/skill .claude/skills
```

**Important considerations:**
- Only ONE directory should contain actual files; the other should be a symlink
- If both directories already exist with different skills, ask user which to keep as primary
- Symlinks should be committed to git for project-level interop (use relative paths)
- After creating symlinks, verify with `ls -la` that the link points correctly
</operation>

</operations>

<error_handling>

<error name="clone-failed">
**Symptom:** `git clone` fails with "repository not found" or network error

**Resolution:**
1. Verify the URL is correct: `curl -I https://github.com/user/repo`
2. Check if repo is private (requires auth): `gh auth status`
3. For private repos, use SSH: `git clone git@github.com:user/repo`
</error>

<error name="skill-exists">
**Symptom:** Target directory already exists

**Resolution:**
1. Ask user: "Skill already exists. Update it or reinstall fresh?"
2. Update: `git -C <path> pull`
3. Reinstall: `rm -rf <path>` then clone again
</error>

<error name="invalid-url">
**Symptom:** Cannot parse GitHub URL

**Resolution:**
1. Check URL format matches expected patterns (user/repo or full GitHub URL)
2. Normalize shorthand `user/repo` to `https://github.com/user/repo`
3. Ask user to verify the URL
</error>

<error name="missing-skill-md">
**Symptom:** Cloned directory has no SKILL.md

**Resolution:**
1. Check if skill uses different structure (look for README or other entry point)
2. Warn user: "This doesn't appear to be a valid skill (no SKILL.md found)"
3. Ask if they want to keep it anyway
</error>

</error_handling>

<success_criteria>
Installation is successful when:
- [ ] Target directory exists
- [ ] SKILL.md file is present in the directory
- [ ] For git repos: `.git` directory exists (or is a submodule)
- [ ] For subdirectory/zip: `.skill-manager-ref` file exists with source URL
- [ ] Any dependencies have been installed

Update is successful when:
- [ ] `git pull` completes without errors (for git repos)
- [ ] New files are present after re-download (for subdirectory/zip)

Removal is successful when:
- [ ] Target directory no longer exists
- [ ] For submodules: no entry in `.gitmodules` or `.git/modules/`

**Important:** After installing, updating, or removing skills, always tell the user they need to restart Claude Code/OpenCode for changes to take effect.
</success_criteria>
