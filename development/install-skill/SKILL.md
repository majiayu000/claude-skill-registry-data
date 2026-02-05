---
name: install-skill
description: Install agent skills from various sources including local paths, GitHub URLs, or the dot-agents repository. Use when adding new skills to a project or user environment.
license: MIT
allowed-tools:
  - Bash
  - Read
---

# Install Skill

Install agent skills from local paths, GitHub repositories, or the dot-agents library.

## When to Use This Skill

Use install-skill when you need to:

- Add a skill from the dot-agents repository to your project
- Install a custom skill from a local directory
- Fetch and install a skill from a GitHub repository
- Set up skills for the first time in a project
- Share skills between projects

## Installation Process

### Step 1: Identify the Skill Source

Determine where the skill is located:

**Shorthand (from dot-agents repository)**:

- `skills/meta/skill-creator`
- `skills/meta/skill-tester`
- `skills/meta/skill-evaluator`
- `skills/examples/get-weather`
- `skills/examples/simple-task`

**Local Path**:

- Absolute: `/path/to/skill-directory`
- Relative: `../skills/my-skill`
- Home: `~/custom-skills/my-skill`

**GitHub URL**:

- Full tree URL: `https://github.com/user/repo/tree/main/path/to/skill`

### Step 2: Determine Target Directory

The installation script automatically discovers the skills directory by searching for existing `SKILL.md` files.

**Discovery Priority**:

1. `.agents/skills/` (project-level, agent-agnostic) - preferred
2. `.claude/skills/` (project-level, Claude-specific)
3. `~/.agents/skills/` (global, agent-agnostic)
4. `~/.claude/skills/` (global, Claude-specific)

If no existing skills are found, the script will prompt you to choose a location.

**Manual Override**:
You can specify the target directory as a second argument:

```bash
bash scripts/install.sh <skill-source> <target-directory>
```

### Step 3: Run the Installation Script

Check available options:

```bash
bash scripts/install.sh --help
```

Install a skill:

```bash
bash scripts/install.sh <skill-source>
```

### Step 4: Verify Installation

Check that the skill was installed correctly:

```bash
ls -la <target-directory>
cat <target-directory>/<skill-name>/SKILL.md
```

Validate the installed skill:

```bash
python /path/to/skill-tester/scripts/test_skill.py <target-directory>/<skill-name>
```

## Script Usage

### Basic Commands

**Show Help**:

```bash
bash scripts/install.sh --help
```

**Show Version**:

```bash
bash scripts/install.sh --version
```

**Install from Shorthand**:

```bash
bash scripts/install.sh skills/meta/skill-creator
bash scripts/install.sh skills/examples/get-weather
```

**Install from Local Path**:

```bash
bash scripts/install.sh /path/to/custom-skill
bash scripts/install.sh ../skills/my-skill
bash scripts/install.sh ~/custom-skills/my-skill
```

**Install from GitHub**:

```bash
bash scripts/install.sh https://github.com/user/repo/tree/main/skills/my-skill
```

**Specify Target Directory**:

```bash
bash scripts/install.sh skills/meta/skill-creator ~/.agents/skills
bash scripts/install.sh skills/examples/get-weather ./.agents/skills
```

## Examples

### Example 1: First-Time Setup

**Scenario**: Setting up skills in a new project

**Steps**:

1. Create skills directory:

   ```bash
   mkdir -p .agents/skills
   ```

2. Install skill-creator:

   ```bash
   bash scripts/install.sh skills/meta/skill-creator
   ```

3. Verify installation:

   ```bash
   ls -la .agents/skills/skill-creator
   ```

**Expected Output**:

```text
ℹ Discovering skills installation directory...
⚠ Found empty skills directory: ./.agents/skills
ℹ Target directory: ./.agents/skills
ℹ Found skill locally: /Users/user/dot-agents/worktrees/main/skills/meta/skill-creator
ℹ Installing skill-creator from /Users/user/dot-agents/worktrees/main/skills/meta/skill-creator
✓ Installed skill: skill-creator → ./.agents/skills/skill-creator
```

### Example 2: Installing Multiple Skills

**Scenario**: Installing several skills from the dot-agents repository

**Steps**:

```bash
bash scripts/install.sh skills/meta/skill-creator
bash scripts/install.sh skills/meta/skill-tester
bash scripts/install.sh skills/meta/skill-evaluator
bash scripts/install.sh skills/examples/get-weather
```

**Result**: All skills installed to the same auto-detected directory

### Example 3: Installing Custom Skill

**Scenario**: Installing a skill you developed locally

**Steps**:

1. Develop skill at `~/my-skills/custom-analyzer/`
2. Ensure it has `SKILL.md` with proper frontmatter
3. Install:

   ```bash
   bash scripts/install.sh ~/my-skills/custom-analyzer
   ```

**Expected Output**:

```text
ℹ Discovering skills installation directory...
ℹ Found skills in: ./.agents/skills
ℹ Target directory: ./.agents/skills
ℹ Installing custom-analyzer from /Users/user/my-skills/custom-analyzer
✓ Installed skill: custom-analyzer → ./.agents/skills/custom-analyzer
```

### Example 4: Installing from GitHub

**Scenario**: Installing a community skill from GitHub

**Steps**:

```bash
bash scripts/install.sh https://github.com/user/repo/tree/main/skills/awesome-skill
```

**Process**:

1. Script clones the repository (sparse checkout)
2. Extracts the skill directory
3. Validates SKILL.md exists
4. Installs to auto-detected location

### Example 5: Overwriting Existing Skill

**Scenario**: Updating a skill that's already installed

**Steps**:

```bash
bash scripts/install.sh skills/meta/skill-creator
```

**Interactive Prompt**:

```text
⚠ Skill already exists: ./.agents/skills/skill-creator
Overwrite? [y/N]:
```

Choose `y` to update, `N` to cancel.

## How Directory Discovery Works

The script searches for existing `SKILL.md` files in common locations to infer where skills should be installed.

**Search Process**:

1. Search `./.agents/skills/*/SKILL.md`
2. Search `./.claude/skills/*/SKILL.md`
3. Search `~/.agents/skills/*/SKILL.md`
4. Search `~/.claude/skills/*/SKILL.md`

**Decision Logic**:

- If skills found in `.agents/skills/` → use that
- If only found in `.claude/skills/` → use that
- If found in multiple locations → use highest priority (agent-agnostic over Claude-specific, local over global)
- If none found but empty directory exists → use that
- If nothing found → prompt user

## Skill Name Extraction

The script extracts the skill name from the `SKILL.md` YAML frontmatter:

```yaml
---
name: skill-name
description: ...
---
```

The skill is installed using this name, **not** the source directory name. This ensures consistency.

## Best Practices

- **Use shorthand for dot-agents library**: Simplest and most reliable
- **Verify after installation**: Check SKILL.md exists and is readable
- **Use `.agents/skills/` for projects**: Agent-agnostic, future-proof
- **Use `~/.agents/skills/` for global skills**: Available across all projects
- **Validate installed skills**: Run skill-tester after installation
- **Version control project skills**: Commit `.agents/skills/` to git for team sharing

## Common Pitfalls

- **Missing SKILL.md**: Source directory must contain valid SKILL.md file
- **Name mismatch**: Skill installed using YAML `name` field, not directory name
- **Permission errors**: Ensure write access to target directory
- **Network issues**: GitHub installations require internet connection
- **Invalid GitHub URL**: Must be full tree URL, not just repo URL

## Error Handling

**Source Not Found**:

```text
✗ Source directory does not exist: /path/to/skill
```

Check path spelling and existence.

**SKILL.md Missing**:

```text
✗ SKILL.md not found in: /path/to/skill
```

Source must be a valid skill directory.

**Clone Failed**:

```text
✗ Failed to clone repository: https://github.com/user/repo
```

Check URL and network connection.

**Name Extraction Failed**:

```text
✗ Could not extract skill name from SKILL.md
```

SKILL.md must have valid YAML frontmatter with `name:` field.

## Dependencies

- `bash` (version 4.0+)
- `git` (for GitHub and dot-agents repository installations)
- `awk` (for YAML parsing)
- `find` (for directory discovery)

Standard utilities available on macOS and Linux.

## Integration with Other Meta-Skills

**After Installation**:

1. **Validate with skill-tester**:

   ```bash
   python skill-tester/scripts/test_skill.py .agents/skills/new-skill
   ```

2. **Evaluate with skill-evaluator**:
   Load skill-evaluator and assess the installed skill's quality.

3. **Use skill-creator for new skills**:
   Install skill-creator first, then use it to scaffold new skills.

## Troubleshooting

### Q: Script can't find dot-agents repository

A: Install from GitHub URL or clone the repository locally first.

### Q: Installation directory not detected

A: Manually specify target directory as second argument or create `.agents/skills/` first.

### Q: Skill name doesn't match directory

A: This is expected. The script uses the `name` field from SKILL.md YAML frontmatter.

### Q: Permission denied

A: Check write permissions on target directory or use a different location.

## Resources

- Installation script: `scripts/install.sh`
- Agent Skills Repository: <https://github.com/tnez/dot-agents>
- Agent Skills Specification: <https://github.com/anthropics/skills/blob/main/agent_skills_spec.md>
