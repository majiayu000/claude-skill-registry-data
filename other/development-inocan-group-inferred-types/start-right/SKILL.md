---
name: start-right
description: Comprehensive repository initialization and scaffolding for new projects. Use when setting up a new repository from scratch with git, GitHub, CI/CD workflows, branch protection, validation checks (format, lint, type-check, tests, builds), git hooks (husky/lefthook), GitHub Actions for PR and main branch validation, automated versioning and tagging, and project-specific release workflows. Ideal for solo developers who want production-ready repository setup including (1) Git initialization with main branch, (2) GitHub repository creation and configuration, (3) Branch protection rules, (4) PR workflow with squash merging and auto-delete branches, (5) Comprehensive validation checks, (6) Git hooks for pre-commit and pre-push validation, (7) GitHub Actions CI/CD pipelines, (8) Automated releases with GitHub Releases integration.
---

# Start Right

Complete repository initialization and scaffolding for new projects with production-ready CI/CD workflows, validation checks, and automated releases.

## Overview

This skill provides end-to-end repository setup for solo developers, automating everything from git initialization to production deployment workflows. It handles project type detection, appropriate tooling configuration, GitHub repository creation, branch protection, validation checks, git hooks, and comprehensive GitHub Actions workflows.

## Workflow Decision Tree

When a user requests repo initialization/scaffolding:

1. **Determine project type** → Detect or ask user for project type (node/typescript/react/rust/python/go/docker/skill)
2. **Gather preferences** → Ask about:
   - Repository visibility (public/private)
   - Organization (if applicable)
   - Validation checks to enable (format, lint, type-check, test, build, integration-test)
   - Git hooks preference (husky for Node.js projects, lefthook for others)
   - Release strategy (npm, github-pages, vercel, docker, binary, pypi, crates.io, skill)
3. **Execute scaffolding** → Run setup scripts in order
4. **Verify and report** → Confirm all components are configured correctly

## Scaffolding Process

### Step 1: Prerequisites Check

Before starting, verify:
- Git is installed
- GitHub CLI (gh) is installed and authenticated
- Current directory is the intended project location
- Directory is empty or contains minimal files

```bash
# Check prerequisites
git --version
gh --version
gh auth status
```

If prerequisites are missing, provide installation instructions:
- **Git**: `brew install git` (macOS) or system package manager
- **GitHub CLI**: `brew install gh` or from https://cli.github.com
- **Authentication**: `gh auth login`

### Step 2: Git Initialization

Initialize git repository with main as default branch:

```bash
python3 scripts/init_git_repo.py <repo-name> [--private] [--org <org>] [--type <project-type>]
```

**Options**:
- `--private`: Create private repository (default: public)
- `--org <n>`: Create under organization
- `--type <type>`: Project type for appropriate .gitignore (node, python, rust, go)

This script:
- Initializes git with `main` branch
- Creates appropriate `.gitignore` file
- Creates GitHub repository
- Sets up remote connection

### Step 3: Tooling Configuration

Set up linting, formatting, and type checking based on project type:

```bash
python3 scripts/setup_tooling.py [project-type]
```

If project type is not specified, it will be auto-detected.

This creates configuration files like:
- **Node/TypeScript**: `.eslintrc.json`, `.prettierrc.json`, `tsconfig.json`
- **Python**: `.flake8`, `.black.toml`, `mypy.ini`
- **Rust**: `rustfmt.toml`

After running, **install the necessary dependencies**:
- **Node**: `npm install --save-dev eslint prettier typescript @typescript-eslint/parser @typescript-eslint/eslint-plugin`
- **Python**: `pip install black flake8 mypy pytest`
- **Rust**: Tools are built-in to cargo

### Step 4: Git Hooks Setup

Configure pre-commit and pre-push hooks:

```bash
python3 scripts/setup_git_hooks.py [--husky|--lefthook] --checks format,lint,type-check,test,build
```

**Hook tool selection**:
- `--husky`: For Node.js projects (recommended, requires npm)
- `--lefthook`: Universal, works with any project type

**Checks configuration**:
- **Pre-commit**: format, lint, type-check (fast checks)
- **Pre-push**: test, build (slower checks)
- Customize with `--checks` flag

This script:
- Installs the git hooks tool
- Creates hook configuration files
- Sets up hooks to run appropriate validation checks
- Updates package.json scripts (if Node.js project)

### Step 5: GitHub Actions Workflows

Generate comprehensive CI/CD workflows:

```bash
python3 scripts/generate_workflows.py --checks format,lint,type-check,test,build --release <release-type>
```

**Release types** (choose based on project):
- `npm`: npm package publication
- `github-pages`: Static site to GitHub Pages
- `docker`: Container image to GitHub Container Registry
- `binary`: Compiled binaries for multiple platforms
- `skill`: Claude Code skill (no deployment)
- `pypi`: Python package to PyPI
- `vercel`: Skip (Vercel handles deployment automatically)

This creates:
1. **pr-validation.yml**: Runs validation checks on PRs to main
2. **main-ci-cd.yml**: Runs on merge to main, includes:
   - All validation checks
   - Automatic version bumping
   - Git tagging
   - Calls release workflow
3. **release.yml**: Reusable workflow for deployment (if release type specified)

**Workflow features**:
- PR validation runs subset of fast checks
- Main branch validation runs ALL checks including integration tests
- Automatic semantic versioning
- GitHub Releases with auto-generated notes
- Project-specific optimizations (caching, parallel jobs)

### Step 6: Branch Protection Rules

Configure branch protection to enforce PR workflow:

```bash
python3 scripts/setup_branch_protection.py build,test
```

Pass comma-separated list of required status checks (matching GitHub Actions job names).

This script configures:
- **Direct pushes to main**: Blocked
- **Pull requests**: Required
- **Status checks**: Must pass before merge (if configured)
- **Squash merging**: Enabled (enforced)
- **Merge commits**: Disabled
- **Rebase merging**: Disabled
- **Auto-delete branches**: Enabled after merge

### Step 7: Initial Commit and Verification

Create initial commit and push to main:

```bash
git add .
git commit -m "chore: initial repository scaffolding"
git push -u origin main
```

Verify setup:
- Check GitHub repository exists and is configured correctly
- Verify branch protection rules are active
- Confirm workflows are present in `.github/workflows/`
- Test git hooks by making a small change

## Interactive Setup Flow

For best user experience, guide users through the process interactively:

### Phase 1: Information Gathering

Ask the user:

1. **Repository name**: What should the repository be named?
2. **Visibility**: Public or private repository?
3. **Organization**: Create under an organization? (optional)
4. **Project type**: What type of project is this?
   - Node.js / JavaScript
   - TypeScript
   - React / Next.js
   - Python
   - Rust
   - Go
   - Docker container
   - Claude Code skill
   - Other / Generic
5. **Validation checks**: Which checks should run?
   - Format checking (recommended: pre-commit)
   - Linting (recommended: pre-commit)
   - Type checking (recommended: pre-commit for TypeScript/Python)
   - Unit tests (recommended: pre-push)
   - Build verification (recommended: PR and main)
   - Integration tests (recommended: main branch only)
6. **Git hooks**: Set up pre-commit and pre-push hooks?
   - Yes (recommended)
   - No
7. **Release strategy**: How will this project be released?
   - Provide options based on project type (see [Release Strategies](#release-strategies))

### Phase 2: Execution

Execute the scaffolding scripts in order, showing progress:

```
🚀 Initializing repository...
✅ Git initialized with main branch
✅ Created .gitignore
✅ Created GitHub repository: username/repo-name (public)
✅ Configured remote origin

🔧 Setting up tooling...
✅ Created .eslintrc.json
✅ Created .prettierrc.json
✅ Created tsconfig.json

🪝 Configuring git hooks...
✅ Installed husky
✅ Created pre-commit hook (format, lint)
✅ Created pre-push hook (test, build)

⚙️  Generating GitHub Actions workflows...
✅ Created pr-validation.yml
✅ Created main-ci-cd.yml
✅ Created release.yml (npm)

🔒 Configuring branch protection...
✅ Enabled branch protection for main
✅ Configured squash merge only
✅ Enabled auto-delete branches

📝 Creating initial commit...
✅ Initial commit created and pushed
```

### Phase 3: Post-Setup Instructions

Provide next steps to the user:

```
✅ Repository scaffolding complete!

Your repository is ready at: https://github.com/username/repo-name

Next steps:
1. Install dependencies:
   npm install

2. Install dev dependencies for tooling:
   npm install --save-dev eslint prettier typescript

3. Test the setup:
   - Make a change in a file
   - Commit (hooks should run)
   - Push to trigger branch protection (push will fail - create PR instead)

4. Create your first feature:
   git checkout -b feature/initial-implementation
   # Make changes
   git add .
   git commit -m "feat: add initial implementation"
   git push -u origin feature/initial-implementation

5. Open a pull request:
   gh pr create --fill
   # CI will run automatically
   # After approval (or if no review required), squash and merge

6. Configure secrets (if needed for releases):
   - For npm: Add NPM_TOKEN to repository secrets
   - For PyPI: Add PYPI_TOKEN to repository secrets
   - For Docker: Authentication handled automatically via GITHUB_TOKEN

Validation checks configured:
- Pre-commit: format, lint, type-check
- Pre-push: test, build
- PR workflow: format, lint, type-check, test, build
- Main workflow: ALL checks + integration tests + release

Release strategy: npm
- Merges to main will automatically version, tag, and publish to npm
- Check .github/workflows/release.yml for details

Branch protection active:
- Cannot push directly to main
- PRs required with squash merge
- Feature branches auto-delete after merge

Resources:
- Workflows: .github/workflows/
- Git hooks: .husky/ (or lefthook.yml)
- Tooling config: .eslintrc.json, .prettierrc.json, tsconfig.json
```

## Release Strategies

Based on project type, suggest appropriate release strategies. See `references/release-strategies.md` for comprehensive details on each strategy.

### Quick Selection Guide

**For npm/Node.js projects**:
- **Library**: npm package
- **Web app**: Vercel, Netlify, or GitHub Pages
- **CLI tool**: npm package or standalone binary

**For Python projects**:
- **Library**: PyPI
- **Web app**: Docker container or Platform-as-a-Service
- **CLI tool**: PyPI or standalone binary

**For Rust projects**:
- **Library**: crates.io
- **Binary/CLI**: GitHub Releases with multi-platform binaries
- **Web Assembly**: Build to WASM + GitHub Pages

**For Docker projects**:
- **Any service**: GitHub Container Registry (ghcr.io)

**For Claude Code skills**:
- **Skill package**: GitHub Releases with .skill file

**For static sites**:
- **Documentation/website**: GitHub Pages

## Troubleshooting

### Git hooks not running
- **Husky**: Ensure `npm install` has been run (installs hooks)
- **Lefthook**: Run `lefthook install` to activate hooks
- Check file permissions: `chmod +x .husky/pre-commit`

### GitHub Actions failing
- Verify all required secrets are configured
- Check that validation commands match package.json scripts
- Review workflow logs for specific errors
- Ensure branch protection doesn't block the Actions bot

### Branch protection preventing merge
- Verify required status checks match GitHub Actions job names
- Ensure all checks are passing on the PR
- Check that actor has permission to merge (admin bypass may be needed for first setup)

### Pre-commit hooks too slow
- Move expensive checks (tests, build) to pre-push or CI only
- Use parallel execution in lefthook
- Configure incremental checking (only changed files)

## References

For detailed information:
- **Project Types**: See `references/project-types.md` for validation and build requirements per type
- **Release Strategies**: See `references/release-strategies.md` for comprehensive deployment options

## Scripts Directory

All automation scripts are in `scripts/`:
- `init_git_repo.py`: Git and GitHub initialization
- `setup_tooling.py`: Linting, formatting, type checking configuration
- `setup_git_hooks.py`: Git hooks with husky or lefthook
- `generate_workflows.py`: GitHub Actions workflow generation
- `setup_branch_protection.py`: Branch protection rules configuration

Each script can be run independently or as part of the complete scaffolding flow.
