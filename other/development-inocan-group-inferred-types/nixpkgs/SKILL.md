---
name: Nixpkgs
description: Contributing to NixOS/nixpkgs repository. USE WHEN in nixpkgs repository (git remote contains NixOS/nixpkgs OR path contains github.com/NixOS/nixpkgs), reviewing PRs, updating packages, or contributing to nixpkgs.
---

# Nixpkgs Contribution Guide

## Purpose
Expert guidance for contributing to the NixOS/nixpkgs repository, reviewing pull requests, and maintaining packages.

## Context Detection

**This skill activates when:**
- Git remote URL contains `NixOS/nixpkgs` or `nixos/nixpkgs`
- Current directory path contains `github.com/NixOS/nixpkgs` or `~/src/nixpkgs`
- User explicitly mentions nixpkgs-review, nix-update, or nixpkgs contribution
- User asks a question about nix packages

## Workflow Routing

When the user's request matches specific nixpkgs operations, route to the appropriate workflow:

| Workflow | Trigger | File |
|----------|---------|------|
| **Review** | "review pr", "nixpkgs-review", "review pull request", "test pr" | `workflows/Review.md` |
| **Add Package** | "add package", "new package", "init package", "create package" | `workflows/AddPackage.md` |
| **Update Package** | "update package", "bump version", "upgrade package", "nix-update" | `workflows/UpdatePackage.md` |
| **Fix Package** | "fix package", "broken package", "build failing", "package doesn't work" | `workflows/FixPackage.md` |
| **Maintainer** | "maintainer", "triage issues", "package maintenance", "become maintainer" | `workflows/Maintainer.md` |

**When to use workflows:**
- Route when the user explicitly asks about one of these operations
- Workflows provide comprehensive, step-by-step guidance for nixpkgs contributions
- For general nixpkgs questions or tool usage, continue with this main skill

## Quick Reference

### Review PR
```bash
# Review pull request
nixpkgs-review pr 12345

# Review and post results
nixpkgs-review pr 12345 --post-result

# Review specific packages only
nixpkgs-review pr 12345 -p firefox
```

### Update Package
```bash
# Update package version
nix-update package-name

# Update and build
nix-update --build package-name

# Update, build, and commit
nix-update --build --commit package-name
```

### Review Local Changes
```bash
# Review uncommitted changes
nixpkgs-review wip

# Review staged changes only
nixpkgs-review wip --staged

# Review specific commit
nixpkgs-review rev HEAD
```

## nixpkgs-review

### Installation
```bash
# Run without installing
nix run nixpkgs#nixpkgs-review

# Install to profile
nix profile install nixpkgs#nixpkgs-review

# In development shell
nix-shell -p nixpkgs-review
```

### Basic PR Review
```bash
# Review PR by number
nixpkgs-review pr 12345

# Review PR by URL
nixpkgs-review pr https://github.com/NixOS/nixpkgs/pull/12345

# This will:
# 1. Fetch the PR
# 2. Determine changed packages
# 3. Build all changed packages
# 4. Drop you into nix-shell with built packages
```

### Post Results to PR
```bash
# Post build report as comment
nixpkgs-review pr 12345 --post-result

# Requires GitHub authentication
# Set up with gh, hub, or GITHUB_TOKEN
```

### GitHub Authentication
```bash
# Method 1: GitHub CLI (recommended)
gh auth login

# Method 2: Environment variable
export GITHUB_TOKEN=ghp_...

# Method 3: hub configuration
# ~/.config/hub:
github.com:
- user: username
  oauth_token: token
  protocol: https
```

### Review Options
```bash
# Build only specific packages
nixpkgs-review pr 12345 -p firefox chromium

# Build packages matching regex
nixpkgs-review pr 12345 --package-regex "python.*"

# Review for multiple systems
nixpkgs-review pr 12345 --system x86_64-linux,aarch64-linux

# Don't enter shell (non-interactive)
nixpkgs-review pr 12345 --no-shell

# Run custom command instead of shell
nixpkgs-review pr 12345 --run "nix-shell -p hello --run hello"

# Print results to stdout
nixpkgs-review pr 12345 --print-result

# Sandbox mode (protect HOME)
nixpkgs-review pr 12345 --sandbox
```

### Interactive Commands
```bash
# After nixpkgs-review pr drops you in shell:

# Approve PR (adds approval comment)
nix-shell> nixpkgs-review approve

# Merge PR (requires maintainer access)
nix-shell> nixpkgs-review merge

# Show PR comments
nix-shell> nixpkgs-review comments

# Exit shell
nix-shell> exit
```

### Review Local Changes
```bash
# Review your uncommitted changes
nixpkgs-review wip

# Review staged changes only
nixpkgs-review wip --staged

# Review specific commit
nixpkgs-review rev HEAD

# Review commit range
nixpkgs-review rev HEAD~3..HEAD

# Review remote branch
nixpkgs-review rev origin/staging
```

## nix-update

### Installation
```bash
# Run without installing
nix run nixpkgs#nix-update

# Install to profile
nix profile install nixpkgs#nix-update

# In development shell
nix-shell -p nix-update
```

### Basic Package Update
```bash
# Update package to latest version
nix-update package-name

# Update will:
# 1. Fetch latest version from upstream
# 2. Update version in package expression
# 3. Update source hash
# 4. Update cargo/npm hashes if applicable
```

### Update Options
```bash
# Update and build
nix-update --build package-name

# Update and run tests
nix-update --test package-name

# Update and enter nix-shell
nix-update --shell package-name

# Update and review with nixpkgs-review
nix-update --review package-name

# Update and format file
nix-update --format package-name

# Update and commit
nix-update --commit package-name

# Combine options
nix-update --build --test --commit package-name
```

### Update to Specific Version
```bash
# Update to specific version
nix-update --version=1.2.3 package-name

# Update to unstable/latest
nix-update --version=unstable package-name

# Update to branch
nix-update --version=branch=main package-name
```

### Update Source Types
```bash
# PyPI package
nix-update python3Packages.package-name

# GitHub release
nix-update github-package

# Git repository
nix-update --version=branch=main git-package

# Cargo.lock update
nix-update --build rust-package
```

## Contributing to nixpkgs

### ⚠️ CRITICAL: Always Run nixpkgs-review wip Before Submitting

**Before submitting ANY pull request to nixpkgs, you MUST run `nixpkgs-review wip`:**

```bash
# This is NOT optional - always run before pushing:
nixpkgs-review wip

# This ensures:
# ✓ Your changes build successfully
# ✓ Dependent packages aren't broken
# ✓ You catch issues before CI does
# ✓ You don't waste reviewer time with broken PRs
```

**Why this matters:**
- CI takes time and resources - broken PRs waste both
- Reviewers won't look at PRs that fail basic builds
- You'll find and fix issues faster locally than through CI
- It's respectful to the nixpkgs community

**When to run it:**
- After making any changes (run `nixpkgs-review wip`)
- After updating a package (run `nixpkgs-review wip`)
- After fixing a bug (run `nixpkgs-review wip`)
- Before committing (run `nixpkgs-review wip`)
- Before pushing (run `nixpkgs-review wip`)

### Setup nixpkgs Repository
```bash
# Clone nixpkgs
cd ~/src/github.com/NixOS
git clone https://github.com/NixOS/nixpkgs.git
cd nixpkgs

# Add upstream remote
git remote add upstream https://github.com/NixOS/nixpkgs.git

# Create development environment
nix-shell -p nix-update nixpkgs-review nixfmt-rfc-style
```

### Update Package Workflow
```bash
# 1. Create branch
git checkout -b update/package-name

# 2. Update package
nix-update --build --commit package-name

# 3. Review changes
nixpkgs-review wip

# 4. Push and create PR
git push -u origin update/package-name
gh pr create
```

### Add New Package Workflow
```bash
# 1. Create branch
git checkout -b pkg/new-package

# 2. Create package file
mkdir -p pkgs/by-name/ne/new-package
vim pkgs/by-name/ne/new-package/package.nix

# 3. Test build
nix-build -A new-package

# 4. Review
nixpkgs-review wip

# 5. Format
nixfmt pkgs/by-name/ne/new-package/package.nix

# 6. Commit and push
git add .
git commit -s -m "new-package: init at 1.0.0"
git push -u origin pkg/new-package
gh pr create
```

### Fix Package Workflow
```bash
# 1. Create branch
git checkout -b fix/package-name-issue

# 2. Make changes
vim pkgs/path/to/package/default.nix

# 3. Test build
nix-build -A package-name

# 4. Review all affected packages
nixpkgs-review wip

# 5. Commit and push
git add .
git commit -s -m "package-name: fix issue description"
git push -u origin fix/package-name-issue
gh pr create
```

## Review Best Practices

### Review Workflow
```bash
# 1. Review PR
nixpkgs-review pr 12345

# 2. In the nix-shell, test packages
nix-shell> package-name --version
nix-shell> package-name --help

# 3. Check for issues
nix-shell> ls -la $(which package-name)

# 4. If good, approve
nix-shell> nixpkgs-review approve

# 5. Exit
nix-shell> exit
```

### What to Check
1. **Package builds successfully**: No build errors
2. **Tests pass**: If package has tests
3. **Binary works**: Can execute and shows help
4. **Dependencies correct**: No missing runtime dependencies
5. **License correct**: Matches upstream
6. **Meta attributes**: Description, homepage accurate
7. **No regressions**: Dependent packages still build

### Common Review Scenarios

#### Version Update PR
```bash
# Review version bump
nixpkgs-review pr 12345

# Check:
# - Version number correct
# - Hash updated correctly
# - Tests still pass
# - No breaking changes
```

#### New Package PR
```bash
# Review new package
nixpkgs-review pr 12345 -p new-package

# Check:
# - Package name follows conventions
# - In correct category (pkgs/by-name/)
# - Meta attributes complete
# - License specified
# - Maintainers added
# - Tests included
```

#### Security Update PR
```bash
# Review security update
nixpkgs-review pr 12345

# Check:
# - CVE mentioned in description
# - Version fixes vulnerability
# - All variants updated (if multiple)
# - Consider backport to stable
```

## Working with Package Sets

### Python Packages
```bash
# Update Python package
nix-update python3Packages.package-name

# Review Python package PR
nixpkgs-review pr 12345 -p python3Packages.package-name
```

### Haskell Packages
```bash
# Update Haskell package
nix-update haskellPackages.package-name

# Update all Haskell packages
# (This is done by nixpkgs maintainers)
```

### Node Packages
```bash
# Node packages use node2nix
# Manual update required

# Review node package
nixpkgs-review pr 12345 -p nodePackages.package-name
```

## Commit Message Format

### Version Updates
```
package-name: 1.0.0 -> 1.1.0
```

### New Packages
```
package-name: init at 1.0.0
```

### Fixes
```
package-name: fix build on aarch64-linux
```

### Multi-Package Updates
```
pythonPackages: update multiple packages

- package1: 1.0 -> 1.1
- package2: 2.0 -> 2.1
```

### Breaking Changes
```
package-name: 1.0.0 -> 2.0.0

Breaking changes:
- API changed from X to Y
- Configuration format updated
```

## Advanced nixpkgs-review

### Remote Builders
```bash
# Use remote builder
nixpkgs-review pr 12345 \
  --remote user@builder-host \
  --remote-build-host user@builder-host

# Configure in ~/.config/nixpkgs-review/config.toml
[remote]
host = "user@builder-host"
```

### Custom Build Options
```bash
# Use specific nixpkgs checkout
nixpkgs-review pr 12345 --nixpkgs /path/to/nixpkgs

# Extra nix options
nixpkgs-review pr 12345 --extra-nixpkgs-config '{ allowUnfree = true; }'
```

### Batch Review
```bash
# Review multiple PRs
for pr in 12345 12346 12347; do
  nixpkgs-review pr $pr --no-shell --post-result
done
```

## Package Organization

### pkgs/by-name Structure
```
pkgs/by-name/
  he/hello/package.nix       # Packages starting with "he"
  fi/firefox/package.nix     # Packages starting with "fi"
  go/go/package.nix          # Packages starting with "go"
```

**Rules:**
- Package name determines directory (first 2 letters)
- File must be named `package.nix`
- One package per directory
- Automatically included in all-packages.nix

### Traditional Structure
```
pkgs/
  applications/
  development/
  servers/
  tools/
```

Use for packages not yet migrated to `by-name`.

## Troubleshooting

### Build Failures
```bash
# Keep build directory on failure
nixpkgs-review pr 12345 --keep-going

# Show full build logs
nixpkgs-review pr 12345 | tee review.log
```

### Authentication Issues
```bash
# Check GitHub token
gh auth status

# Refresh token
gh auth refresh

# Set token manually
export GITHUB_TOKEN=$(gh auth token)
```

### Evaluation Errors
```bash
# Show evaluation trace
nixpkgs-review pr 12345 --show-trace

# Check for syntax errors
nix-instantiate --parse default.nix
```

## Tips and Tricks

1. **⚠️ ALWAYS run `nixpkgs-review wip` before submitting**: This is the most important step - test your changes locally before pushing
2. **Use --post-result**: Auto-comment on PRs to help maintainers
3. **Review regularly**: Help reduce PR backlog
4. **Test on your system**: Real-world testing is valuable
5. **Be thorough but kind**: Constructive feedback
6. **Check ofborg results**: CI results before reviewing
7. **Use nix-update**: Automate version updates
8. **Review related PRs**: Check for conflicts
9. **Comment on approach**: Not just build success
10. **Approve quickly**: Don't block good PRs
11. **Learn from reviews**: Read other reviewers' comments

## Resources

- [nixpkgs-review](https://github.com/Mic92/nixpkgs-review)
- [nix-update](https://github.com/Mic92/nix-update)
- [nixpkgs Contributing Guide](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md)
- [Reviewing Contributions](https://ryantm.github.io/nixpkgs/contributing/reviewing-contributions/)
- [Nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/)
- [Package Naming Conventions](https://nixos.org/manual/nixpkgs/stable/#sec-package-naming)

## Examples

**Example 1: Updating a package in nixpkgs**
```
User: "Update tektoncd-cli to the latest version"
→ Finds package in nixpkgs repository
→ Updates version and hash in default.nix
→ Runs nix-build to test the update
→ Checks for breaking changes or new dependencies
→ Creates commit following nixpkgs standards
→ Opens pull request to nixpkgs
→ Result: Package updated and PR submitted
```

**Example 2: Reviewing a nixpkgs PR**
```
User: "Review nixpkgs PR #12345"
→ Checks out PR branch locally
→ Reviews code changes for correctness
→ Tests build with nix-build
→ Verifies meta attributes are correct
→ Checks commit message follows standards
→ Leaves review comments or approval
→ Result: Thorough PR review completed
```

**Example 3: Adding a new package**
```
User: "Add this new tool to nixpkgs"
→ Creates package directory structure
→ Writes derivation with proper builder (buildGoModule, etc.)
→ Adds to all-packages.nix
→ Tests on multiple platforms
→ Follows nixpkgs contribution guidelines
→ Result: New package ready for nixpkgs
```
