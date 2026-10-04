---
name: version-manager
description: Universal version management with smart bump recommendations based on conventional commits. Handles Node.js, Python, Rust, Go, and Claude Code plugins with README badge synchronization. Use when bumping versions, releasing, or managing semantic versioning.
---

# Version Manager

Intelligent version management for any project with semantic versioning. Automatically detects project type, analyzes conventional commits, recommends version bumps, and keeps README badges in sync.

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory.

## When to Use

This skill automatically activates via Stop hook when:

- Committing on `main` or `master` branch
- Working in a project with version file (package.json, plugin.json, pyproject.toml, etc.)

Feature branches are handled silently without prompting.

## Supported Project Types

Detected automatically in priority order:

| Project Type       | Detection File               | Version Field          |
| ------------------ | ---------------------------- | ---------------------- |
| Claude Code Plugin | `.claude-plugin/plugin.json` | `.version`             |
| Node.js/JavaScript | `package.json`               | `.version`             |
| Python (modern)    | `pyproject.toml`             | `[project].version`    |
| Rust               | `Cargo.toml`                 | `[package].version`    |
| Go                 | `go.mod`                     | Module version in file |
| Python (legacy)    | `setup.py`                   | `version=` argument    |

## How It Works

### Phase 1: Validation

1. Check for validators in `.claude/hooks/validators/`
2. Run all validators if present
3. If any fail → block version bump, display errors
4. If pass → continue to analysis

### Phase 2: Commit Analysis

Analyzes commits since last version tag to recommend bump type:

**Conventional Commit Patterns:**

- `feat:` or `feature:` → recommends **minor** bump
- `fix:` or `bugfix:` → recommends **patch** bump
- `BREAKING CHANGE:` or `!` suffix → recommends **major** bump
- `chore:`, `docs:`, `style:` → recommends **patch** bump

**Logic:**

- Multiple types → picks highest severity (major > minor > patch)
- No conventional commits → defaults to **patch**

**Analysis command:**

```bash
git log <last-tag>..HEAD --oneline
```

### Phase 3: User Prompt

Uses AskUserQuestion with recommended option first:

```
Question: "Bump version?"
Options:
- "Patch (1.2.4) - bug fixes (Recommended)" ← based on analysis
- "Minor (1.3.0) - new features"
- "Major (2.0.0) - breaking changes"
- "Skip - no version bump"

Warning: ⚠️ Patch/Minor bumps may auto-update users with auto-update enabled
```

### Phase 4: Version Update

1. Parse current version from project file
2. Calculate new version based on selection
3. Update version in project file
4. Find and update README badges (shields.io pattern)
5. Git operations:
   ```bash
   git add <files>
   git commit -m "chore: bump version to X.Y.Z"
   git tag vX.Y.Z
   git push origin <branch>
   git push --tags
   ```

## README Badge Synchronization

Automatically finds and updates shields.io version badges:

**Patterns matched:**

```markdown
![Version](https://img.shields.io/badge/version-1.2.3-blue.svg)
![Version](https://img.shields.io/badge/v-1.2.3-blue)
[![Version](https://img.shields.io/badge/version-1.2.3-blue.svg)](link)
```

**Regex:** `shields\.io/badge/(version|v)-([0-9]+\.[0-9]+\.[0-9]+)-`

## Branch Behavior

**Main/Master Branch:**

- Stop hook triggers
- Runs validators
- Analyzes commits
- Prompts for version bump

**Feature Branches:**

- Silent operation
- No prompts
- Validators may run (if configured) but don't block

**Detection:**

```bash
git branch --show-current
```

## Stop Hook Configuration

The Stop hook is enabled when version-manager is installed globally. It runs on every commit completion but only prompts on main/master.

**Hook behavior:**

1. Detect current branch
2. If not main/master → exit silently
3. Detect project type
4. Run validation phase
5. Analyze commits
6. Prompt user
7. Execute version bump if selected

## Examples

### Example 1: Feature Branch (Silent)

```bash
cd ~/my-node-project
git checkout feature/new-ui
# Make changes
git commit -m "feat: add new dashboard"
# → version-manager: Silent (feature branch), no prompt
```

### Example 2: Main Branch with Conventional Commits

```bash
git checkout main
git merge feature/new-ui
# Commits since v1.2.3:
# - feat: add new dashboard
# - fix: correct typo
# → version-manager analyzes: sees "feat:" → recommends minor

# Stop hook triggers:
# Question: "Bump version?"
# Options:
# - "Minor (1.3.0) - new features (Recommended)"
# - "Patch (1.2.4) - bug fixes"
# - "Major (2.0.0) - breaking changes"
# - "Skip"

# User selects "Minor"
# → Updates package.json: "version": "1.3.0"
# → Updates README.md shields.io badge
# → Commits: "chore: bump version to 1.3.0"
# → Tags: v1.3.0
# → Pushes
```

### Example 3: Breaking Change Detection

```bash
# Commits since v2.1.0:
# - feat!: redesign API (breaking change)
# → version-manager analyzes: sees "!" → recommends major

# Question: "Bump version?"
# Options:
# - "Major (3.0.0) - breaking changes (Recommended)"
# - "Minor (2.2.0) - new features"
# - "Patch (2.1.1) - bug fixes"
# - "Skip"
```

### Example 4: No Conventional Commits

```bash
# Commits since v1.5.2:
# - update dependencies
# - refactor code
# → version-manager: no patterns found → defaults to patch

# Question: "Bump version?"
# Options:
# - "Patch (1.5.3) - bug fixes (Recommended)"
# - "Minor (1.6.0) - new features"
# - "Major (2.0.0) - breaking changes"
# - "Skip"
```

## Integration with Validators

If your project has validators in `.claude/hooks/validators/`:

```bash
.claude/
└── hooks/
    └── validators/
        ├── lint-validator.py
        └── test-validator.py
```

version-manager runs them BEFORE prompting:

```
Running validators...
✓ lint-validator.py passed
✓ test-validator.py passed

Analyzing commits...
Recommendation: Minor (1.3.0)

Question: "Bump version?"
```

If validators fail:

```
Running validators...
✗ test-validator.py failed: 3 tests failing

Version bump blocked. Fix validation errors first.
```

## Files in This Skill

- `SKILL.md` (this file) - Skill instructions
- `scripts/detect-project-type.py` - Detects project type and version file
- `scripts/analyze-commits.py` - Parses conventional commits
- `scripts/update-version.py` - Updates version files and badges

## Installation

Install as a project-local skill via symlink:

```bash
ln -sfn "$TOOLKIT_DIR/version-manager" "$WORKSPACE_ROOT/.claude/skills/version-manager"
```

Once installed, it will:

- Detect project type automatically
- Only prompt on main/master branches
- Work silently on feature branches

## Conventional Commits Reference

**Format:** `<type>[optional scope]: <description>`

**Types that affect version recommendations:**

- `feat:` - New feature (minor bump)
- `fix:` - Bug fix (patch bump)
- `feat!:` or `BREAKING CHANGE:` - Breaking change (major bump)
- `chore:`, `docs:`, `style:`, `refactor:`, `test:` - Maintenance (patch bump)

**Examples:**

```bash
git commit -m "feat: add user authentication"        # → minor
git commit -m "fix: correct login validation"        # → patch
git commit -m "feat!: redesign API endpoints"        # → major
git commit -m "chore: update dependencies"           # → patch
```

## Troubleshooting

**Issue: Hook not triggering**

- Verify on main/master branch: `git branch --show-current`
- Check skill is installed: `ls "$(git rev-parse --show-toplevel)/.claude/skills/version-manager"`
- Check project has version file: `ls package.json` (or plugin.json, etc.)

**Issue: Wrong recommendation**

- Check commit messages: `git log <last-tag>..HEAD --oneline`
- Verify conventional commit format
- You can always override the recommendation

**Issue: Badge not updating**

- Verify shields.io format in README.md
- Pattern: `shields.io/badge/version-X.Y.Z-blue`
- Check regex matches your badge format

**Issue: Validators blocking unexpectedly**

- Run validators manually to see output
- Fix validation errors before version bump
- Or remove validators temporarily from `.claude/hooks/validators/`

## Best Practices

1. **Use conventional commits** for accurate recommendations
2. **Test in feature branches** before merging to main
3. **Review commit history** before accepting recommendation
4. **Skip bump if not ready** - you can always bump later manually
5. **Keep validators fast** - they run on every main branch commit

## Future Enhancements

- Changelog generation from conventional commits
- GitHub release creation on version bump
- Configurable commit message templates
- Support for pre-release versions (alpha, beta, rc)
- Monorepo support with independent package versioning
