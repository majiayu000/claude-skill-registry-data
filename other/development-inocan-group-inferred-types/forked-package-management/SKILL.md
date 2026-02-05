---
name: Forked Package Management
description: Git submodules, VCS path repositories, and custom package development for pcrcard/* namespace packages
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Forked Package Management

Manage forked Laravel/Nova packages using git submodules and VCS path repositories.

## When to Use

- Working with forked packages (pcrcard/nova-*)
- Updating package submodules
- Adding new forked packages
- Modifying package code
- Troubleshooting vendor symlinks
- CI/CD package integration

## Package Architecture

**Strategy**: Git Submodules + VCS Path Repositories

### How It Works

1. **Git Submodules** - Packages stored in `packages/` directory
2. **VCS Path Repositories** - Composer installs from local submodule paths
3. **Vendor Symlinks** - Composer creates symlinks: `vendor/pcrcard/*` → `packages/*`
4. **CI/CD Integration** - GitLab auto-initializes submodules before build

### Benefits

✅ **CI/CD Compatible** - Packages available in GitLab CI environment
✅ **Version Freezing** - Control updates via git commits
✅ **Custom Modifications** - Add features without upstream approval
✅ **Unified Workflow** - All forked packages managed consistently
✅ **Git Independence** - Each package has its own repository

## Current Packages

### 1. nova-menus

- **Repository**: https://github.com/hackur/nova-menus
- **Fork Of**: skylark-team/nova-menus
- **Purpose**: Hierarchical menu management for Nova admin
- **Submodule Path**: `packages/nova-menus/`
- **Vendor Path**: `vendor/pcrcard/nova-menus/` (symlink)
- **Tracked Commit**: b3e0fce

**Features**:
- Database-driven menu hierarchy
- Drag-and-drop reorganization
- Nested set model (kalnoy/nestedset)
- 29 menu items, 3 levels deep

### 2. nova-medialibrary-bounding-box-field

- **Repository**: https://github.com/hackur/nova-medialibrary-bounding-box-field
- **Fork Of**: dmitrybubyakin/nova-medialibrary-field
- **Purpose**: Spatie MediaLibrary + Bounding Box damage assessment
- **Submodule Path**: `packages/nova-medialibrary-bounding-box-field/`
- **Vendor Path**: `vendor/pcrcard/nova-medialibrary-bounding-box-field/` (symlink)
- **Tracked Commit**: 38272e1

**Features**:
- Standard image upload/cropping
- Canvas-based visual editor
- Multi-box damage marking
- 15 damage types, 3 severity levels
- Addressed mode for repair tracking
- Readonly mode for comparisons

## Developer Workflow

### First-Time Setup

```bash
# Clone project
git clone <repo-url>
cd pcrcard

# Initialize all submodules
git submodule update --init --recursive

# Install dependencies (creates vendor symlinks)
./vendor/bin/sail composer install
```

### After Pulling Changes

```bash
# Pull latest code
git pull origin main

# Update submodules to tracked commits
git submodule update --init --recursive

# Reinstall if submodule changed significantly
./vendor/bin/sail composer install
```

### Updating a Package

```bash
# Navigate to package
cd packages/nova-menus

# Pull latest changes
git pull origin main

# Return to project root
cd ../..

# Commit the submodule update
git add packages/nova-menus
git commit -m "Update nova-menus to latest"
git push
```

## Git Submodule Commands

### Essential Commands

```bash
# Initialize all submodules (first time)
git submodule update --init --recursive

# Update all submodules to latest commits
git submodule update --remote --merge

# Check submodule status
git submodule status

# Update specific submodule
git submodule update --remote packages/nova-menus
```

### Troubleshooting

```bash
# Submodule detached HEAD
cd packages/nova-menus
git checkout main
git pull origin main
cd ../..
git add packages/nova-menus
git commit -m "Update submodule to track main branch"

# Submodule missing
git submodule update --init packages/nova-menus

# Reset submodule to tracked commit
git submodule update --force packages/nova-menus
```

## Package Management Scripts

**Helper scripts** in `./scripts/dev.sh`:

```bash
# Show status of all forked packages
./scripts/dev.sh pkg:status

# List available packages
./scripts/dev.sh pkg:list

# Clone all packages (or specific package)
./scripts/dev.sh pkg:clone                    # All packages
./scripts/dev.sh pkg:clone nova-menus         # Specific package

# Update packages from remote
./scripts/dev.sh pkg:update                   # All packages
./scripts/dev.sh pkg:update nova-menus        # Specific package

# Build and reinstall package
./scripts/dev.sh pkg:build nova-menus
```

## Adding New Forked Packages

### 7-Step Checklist

**1. Add Fork as Git Submodule**

```bash
git submodule add https://github.com/hackur/<package-name> packages/<package-name>
```

**2. Update Package composer.json**

Change package name to use `pcrcard/*` namespace:

```json
{
  "name": "pcrcard/<package-name>",
  "version": "1.0.0"
}
```

**3. Add VCS Path Repository**

In main `composer.json`:

```json
{
  "repositories": [
    {
      "type": "path",
      "url": "./packages/<package-name>",
      "options": {
        "symlink": true
      }
    }
  ]
}
```

**4. Add Package Requirement**

In main `composer.json`:

```json
{
  "require": {
    "pcrcard/<package-name>": "@dev"
  }
}
```

**5. Update Package Library**

Edit `scripts/lib/packages.sh` and add to `get_forked_packages()`:

```bash
get_forked_packages() {
    echo "nova-menus nova-medialibrary-bounding-box-field <package-name>"
}
```

**6. Install Package**

```bash
./vendor/bin/sail composer update
```

**7. Commit Changes**

```bash
git add .gitmodules packages/<package-name> composer.json composer.lock scripts/lib/packages.sh
git commit -m "Add <package-name> forked package"
git push
```

## CI/CD Integration

### GitLab CI Configuration

`.gitlab-ci.yml` automatically initializes submodules:

```yaml
build:
  stage: build
  before_script:
    # Initialize git submodules for forked packages
    - git submodule update --init --recursive

  script:
    - composer install --prefer-dist --no-interaction
    - npm ci
```

### How It Works

1. GitLab clones main repository
2. `git submodule update --init --recursive` clones package submodules
3. Composer installs from local `packages/` paths
4. Vendor symlinks created automatically

**No manual package copying required!**

## Common Pitfalls

### ❌ WRONG: Forgetting submodule update after pull

```bash
git pull origin main
# packages/ directories empty!
./vendor/bin/sail composer install
# ERROR: Package not found
```

**✅ CORRECT**: Always update submodules after pull

```bash
git pull origin main
git submodule update --init --recursive
./vendor/bin/sail composer install
```

### ❌ WRONG: Using wrong version constraint

```json
{
  "require": {
    "pcrcard/nova-menus": "^1.0"
  }
}
```

**✅ CORRECT**: Use @dev for path repositories

```json
{
  "require": {
    "pcrcard/nova-menus": "@dev"
  }
}
```

### ❌ WRONG: Modifying vendor/ files directly

```bash
# Editing symlinked file
vim vendor/pcrcard/nova-menus/src/NovaMenus.php
# Changes lost on composer install!
```

**✅ CORRECT**: Edit in packages/ directory

```bash
# Edit source in packages/
vim packages/nova-menus/src/NovaMenus.php
# Changes persist (tracked by git)
```

### ❌ WRONG: Committing without updating submodule

```bash
cd packages/nova-menus
git pull origin main
cd ../..
# Forgot to stage submodule update!
git commit -m "Update dependencies"
# Submodule still points to old commit
```

**✅ CORRECT**: Stage submodule after updating

```bash
cd packages/nova-menus
git pull origin main
cd ../..
git add packages/nova-menus
git commit -m "Update nova-menus to latest"
```

## Composer Commands

### Useful Commands

```bash
# Show installed packages
./vendor/bin/sail composer show pcrcard/*

# Validate composer.json
./vendor/bin/sail composer validate

# Clear composer cache
./vendor/bin/sail composer clear-cache

# Reinstall all packages
./vendor/bin/sail composer install --prefer-source

# Update specific package
./vendor/bin/sail composer update pcrcard/nova-menus
```

## Documentation Links

- **Package Integration Plan**: `docs/development/PACKAGE-FORK-INTEGRATION-PLAN.md`
- **Package Versioning**: `docs/development/PACKAGE-VERSIONING-STRATEGY.md`
- **BoundingBox Quick Reference**: `docs/development/BOUNDING-BOX-QUICK-REFERENCE.md`
- **Nova Menus Guide**: `docs/features/NOVA-MENUS-GUIDE.md`
- **Git Submodules**: https://git-scm.com/book/en/v2/Git-Tools-Submodules
