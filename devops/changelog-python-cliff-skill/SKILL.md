---
name: changelog-python-cliff-skill
description: Generate automated changelogs for Python projects using git-cliff with PEP 440 versioning support
license: Apache-2.0
compatibility: opencode
category: Language-Specific
---

## What I do

I implement automated changelog generation for Python projects using [git-cliff](https://git-cliff.org):

1. **Detect Python Project**: Identify version source (`pyproject.toml`, `__init__.py`, `setup.py`, `setup.cfg`)
2. **Verify git-cliff**: Check if git-cliff is installed and configured
3. **Configure cliff.toml**: Generate Python-specific configuration with PEP 440 version support
4. **Generate Changelog**: Run `git cliff` to produce changelogs from conventional commits
5. **Integrate with Release Workflow**: Support `bump-my-version`, `semantic-release`, or manual versioning

## When to use me

Use this workflow when:
- You need to generate or update a `CHANGELOG.md` for a Python project
- You are preparing a release and want an automated changelog
- You want to configure git-cliff for a Python project with PEP 440 versioning
- You need CI/CD integration for changelog generation in Python projects
- You are using conventional commits and want structured release notes

## Prerequisites

- Python project with git repository
- [git-cliff](https://git-cliff.org) installed (`cargo install git-cliff` or download from releases)
- Conventional commits in git history (see `civiltekk-git-commits` skill)
- Version defined in `pyproject.toml`, `__init__.py`, `setup.py`, or `setup.cfg`

## Steps

### Step 1: Detect Python Project

Verify this is a Python project and identify the version source:
```bash
[ -f pyproject.toml ] && echo "pyproject.toml found"
[ -f setup.py ] && echo "setup.py found"
[ -f setup.cfg ] && echo "setup.cfg found"
find . -name "__init__.py" -path "*/src/*" -o -name "__init__.py" -path "*/pkg/*" | head -5
```

Extract the current version:
```bash
grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml 2>/dev/null
grep -oP '__version__\s*=\s*"\K[^"]+' src/**/__init__.py 2>/dev/null
```

### Step 2: Verify git-cliff Installation

Check if git-cliff is available:
```bash
git cliff --version
```

If not installed, guide installation:
```bash
cargo install git-cliff
# or download binary from https://github.com/orhun/git-cliff/releases
```

### Step 3: Check for Existing Configuration

Check if `cliff.toml` already exists:
```bash
[ -f cliff.toml ] && echo "cliff.toml exists" || echo "cliff.toml not found"
```

### Step 4: Generate cliff.toml Configuration

If no `cliff.toml` exists, create one using the template below (see Reference section). Customize based on:
- **Version source**: Set `version_pattern` to match the Python version file location
- **PEP 440 support**: Ensure regex handles pre/post/dev releases
- **Commit conventions**: Categories match the project's conventional commit usage

### Step 5: Generate Changelog

Generate the full changelog:
```bash
git cliff -o CHANGELOG.md
```

Generate changelog for a specific version range:
```bash
git cliff v1.0.0..v2.0.0 -o CHANGELOG.md
```

Generate changelog for the latest version only:
```bash
git cliff --latest -o CHANGELOG.md
```

Preview without writing:
```bash
git cliff --unreleased
```

### Step 6: Integrate with Release Workflow

#### With bump-my-version
```bash
# In pyproject.toml [tool.bumpversion] section, add:
# [tool.bumpversion]
# current_version = "1.0.0"

# Generate changelog before bumping:
git cliff --unreleased -o CHANGELOG.md
bump-my-version bump patch
git add CHANGELOG.md
git commit --amend --no-edit
```

#### With python-semantic-release
git-cliff can be used as a custom changelog tool in `.releaserc` configuration.

#### Manual workflow
```bash
# 1. Update version in pyproject.toml
# 2. Generate changelog
git cliff -o CHANGELOG.md
# 3. Commit and tag
git add CHANGELOG.md pyproject.toml
git commit -m "chore(release): v1.0.0"
git tag v1.0.0
```

### Step 7: CI/CD Integration

#### GitHub Actions
```yaml
- name: Generate changelog
  uses: orhun/git-cliff-action@v4
  with:
    config: cliff.toml
    args: --latest
  env:
    OUTPUT: CHANGELOG.md
```

#### GitLab CI
```yaml
changelog:
  stage: release
  image: orhun/git-cliff:latest
  script:
    - git cliff -o CHANGELOG.md
  artifacts:
    paths:
      - CHANGELOG.md
```

## Best Practices

- **Conventional Commits**: Use `feat:`, `fix:`, `docs:`, etc. for proper categorization (see `civiltekk-git-commits` skill)
- **PEP 440 Compliance**: Use proper pre-release identifiers (`a`, `b`, `rc`) not `alpha`, `beta`
- **Tag Format**: Use `v` prefix for git tags (`v1.0.0`) for compatibility with both PEP 440 and semver tools
- **Changelog Placement**: Keep `CHANGELOG.md` in project root
- **Version Source**: Prefer `pyproject.toml` as the single source of truth for version
- **Scoped Commits**: Use scopes to group changes by module (`feat(api):`, `fix(core):`)

## Common Issues

### git-cliff Not Found
**Issue**: `git cliff` command not found

**Solution**: Install git-cliff:
```bash
cargo install git-cliff
# or download from https://github.com/orhun/git-cliff/releases
```

### No Tags Found
**Issue**: `git cliff` reports no tags

**Solution**: Create an initial tag:
```bash
git tag v0.1.0
```

### PEP 440 Version Not Parsed
**Issue**: Pre-release versions like `1.0.0rc1` not recognized

**Solution**: Ensure `cliff.toml` uses the PEP 440 regex pattern from the template below.

### Empty Changelog
**Issue**: Changelog has no entries

**Solution**: Verify commit messages follow conventional commit format:
```bash
git log --oneline -10
```

## When NOT to use me

- Non-Python projects (use git-cliff directly with appropriate config)
- Projects not using git for version control
- Projects without conventional commits in history
- One-off changelogs that don't need automation

## Governance

Changelog generation follows the conventions in `semantic-release-convention`:
- Commit types map to changelog categories (feat → Features, fix → Bug Fixes, etc.)
- Release tags use branch-aware format (`v1.0.0` on prod, `v1.0.0-dev.1` on non-prod)
- Tag format uses `v` prefix for compatibility with both PEP 440 and SemVer

## Dependencies

- **semantic-release-convention**: For release tag format and commit type conventions
- **civiltekk-git-commits**: For conventional commit formatting and budget guidance
- **civiltekk-documentation-sync**: If changelog is part of documentation updates
- **git-cliff**: External tool (not bundled)

## Reference: cliff.toml Template for Python Projects

```toml
# cliff.toml - Python project configuration for git-cliff
# Place in project root alongside pyproject.toml

[changelog]
header = """
# Changelog\n
All notable changes to this project will be documented in this file.\n
"""
body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [Unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | striptags | trim | upper_first }}
    {% for commit in commits %}
        - {% if commit.scope %}**{{ commit.scope }}**: {% endif %}\
            {{ commit.message | upper_first }}\
            {% if commit.breaking %} (**BREAKING**){% endif %}\
    {% endfor %}
{% endfor %}\n
"""
trim = true
footer = """
<!-- generated by git-cliff -->
"""

[git]
conventional_commits = true
filter_unconventional = true
split_commits = false
commit_parsers = [
    { message = "^feat", group = "<!-- 0 -->Features" },
    { message = "^fix", group = "<!-- 1 -->Bug Fixes" },
    { message = "^doc", group = "<!-- 2 -->Documentation" },
    { message = "^perf", group = "<!-- 3 -->Performance" },
    { message = "^refactor", group = "<!-- 4 -->Refactoring" },
    { message = "^style", group = "<!-- 5 -->Style" },
    { message = "^test", group = "<!-- 6 -->Testing" },
    { message = "^build", group = "<!-- 7 -->Build System" },
    { message = "^ci", group = "<!-- 8 -->CI/CD" },
    { message = "^chore\\(release\\)", skip = true },
    { message = "^chore|^ci", group = "<!-- 9 -->Miscellaneous" },
    { body = ".*security", group = "<!-- 10 -->Security" },
    { message = "^revert", group = "<!-- 11 -->Reverted Commits" },
]
protect_breaking_commits = false
filter_commits = false
tag_pattern = "v[0-9].*"

sort_commits = "oldest"
```

### PEP 440 Version Regex

For Python projects using PEP 440 versioning, add this to `cliff.toml`:
```toml
[git]
# Override tag_pattern for PEP 440:
# Supports: 1.0.0, 1.0.0a1, 1.0.0b2, 1.0.0rc1, 1.0.0.post1, 1.0.0.dev1
tag_pattern = "v[0-9]+\\.[0-9]+\\.[0-9]+(a[0-9]+|b[0-9]+|rc[0-9]+|\\.post[0-9]+|\\.dev[0-9]+)?$"
```

## Troubleshooting Checklist

Before generating changelog:
- [ ] Python project identified with version source
- [ ] git-cliff is installed (`git cliff --version`)
- [ ] Git tags exist (`git tag -l`)
- [ ] Commits follow conventional format
- [ ] `cliff.toml` exists or will be created

After generating changelog:
- [ ] `CHANGELOG.md` is non-empty and properly formatted
- [ ] Version numbers match PEP 440 format
- [ ] All categories are populated with correct commits
- [ ] Breaking changes are highlighted
