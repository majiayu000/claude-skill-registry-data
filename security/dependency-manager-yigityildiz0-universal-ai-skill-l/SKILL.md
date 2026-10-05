---
name: dependency-manager
description: Manage and upgrade project dependencies safely. Use when upgrading packages, handling breaking changes, managing lock files, patching vulnerabilities, or.
---

# Dependency Manager

Specialized expertise in managing project dependencies, including safe upgrades, vulnerability patching, breaking change handling, and maintaining healthy dependency trees across different package ecosystems.

## When to Use This Skill

Use this skill for:

- Upgrading project dependencies
- Handling breaking changes in updates
- Patching security vulnerabilities
- Managing lock files effectively
- Auditing dependency health
- Resolving dependency conflicts
- Planning major version upgrades

**Trigger phrases**: "upgrade dependencies", "update packages", "fix vulnerabilities", "dependency audit", "npm update", "pip upgrade", "breaking change"

## What This Skill Does

Provides dependency management capabilities including:

- **Audit**: Analyzing dependency health and risks
- **Upgrade Planning**: Safe upgrade strategies
- **Breaking Change Handling**: Managing major version updates
- **Vulnerability Patching**: Quick security fixes
- **Conflict Resolution**: Resolving version conflicts
- **Lock File Management**: Maintaining reproducible builds

## Instructions

### Step 1: Audit Current Dependencies

**Dependency Audit Commands by Ecosystem**:

| Ecosystem | Audit Command | Output |
|-----------|---------------|--------|
| npm/Node | `npm audit` | Security vulnerabilities |
| npm/Node | `npm outdated` | Available updates |
| Python/pip | `pip-audit` | Security vulnerabilities |
| Python/pip | `pip list --outdated` | Available updates |
| Python/uv | `uv pip list --outdated` | Available updates |
| Go | `go list -m -u all` | Available updates |
| Rust | `cargo audit` | Security vulnerabilities |
| Java/Maven | `mvn versions:display-dependency-updates` | Available updates |
| .NET | `dotnet list package --outdated` | Available updates |

**Audit Report Template**:

```markdown
## Dependency Audit Report: [Project Name]
**Date**: [timestamp]
**Package Manager**: [npm/pip/etc]

### Summary
| Category | Count | Action Required |
|----------|-------|-----------------|
| Critical vulnerabilities | [n] | Immediate |
| High vulnerabilities | [n] | This sprint |
| Outdated (major) | [n] | Plan upgrade |
| Outdated (minor/patch) | [n] | Update freely |
| Deprecated | [n] | Find replacement |

### Critical/High Vulnerabilities
| Package | Version | Vulnerability | Fixed In | CVSS |
|---------|---------|---------------|----------|------|
| [name] | [ver] | [CVE/desc] | [ver] | [score] |

### Major Updates Available
| Package | Current | Latest | Breaking Changes |
|---------|---------|--------|------------------|
| [name] | [ver] | [ver] | [Yes/No - link to changelog] |

### Recommendations
1. **Immediate**: [Critical security patches]
2. **Short-term**: [High-priority updates]
3. **Planned**: [Major version upgrades]
```

### Step 2: Plan Safe Upgrades

**Upgrade Strategy Matrix**:

| Update Type | Risk | Strategy |
|-------------|------|----------|
| Patch (x.x.N) | Very Low | Update immediately, run tests |
| Minor (x.N.x) | Low | Update in batch, run tests |
| Major (N.x.x) | Medium-High | Update individually, review changelog |
| Security fix | Varies | Prioritize regardless of version jump |

**Safe Upgrade Process**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFE UPGRADE WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Audit          2. Review           3. Update                │
│  ┌──────────┐     ┌──────────┐        ┌──────────┐             │
│  │ List all │────►│ Check    │───────►│ Update   │             │
│  │ outdated │     │ changelogs│        │ lock file│             │
│  └──────────┘     └──────────┘        └──────────┘             │
│       │                │                    │                   │
│       ▼                ▼                    ▼                   │
│  [Prioritize]    [Note breaking      [Commit lock              │
│                   changes]            file separately]          │
│                                                                 │
│  4. Test          5. Verify           6. Deploy                │
│  ┌──────────┐     ┌──────────┐        ┌──────────┐             │
│  │ Run full │────►│ Manual   │───────►│ Monitor  │             │
│  │ test suite│    │ smoke test│       │ in prod  │             │
│  └──────────┘     └──────────┘        └──────────┘             │
│       │                │                    │                   │
│       ▼                ▼                    ▼                   │
│  [If fail,        [If issues,         [Rollback if             │
│   rollback]        investigate]        needed]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Handle Breaking Changes

**Breaking Change Assessment Template**:

```markdown
## Breaking Change Analysis: [Package] v[old] → v[new]

### Changelog Summary
[Key changes from release notes]

### Breaking Changes Identified
| Change | Impact | Files Affected | Migration |
|--------|--------|----------------|-----------|
| [API change] | [High/Med/Low] | [list] | [steps] |

### Migration Steps
1. [ ] [Step 1]
2. [ ] [Step 2]
3. [ ] [Step 3]

### Code Changes Required
```diff
- old_function(arg1, arg2)
+ new_function(arg1, options={arg2: value})
```

### Testing Plan
- [ ] Update affected tests
- [ ] Run full test suite
- [ ] Manual testing of [specific features]

### Rollback Plan
If issues found:
1. Revert to previous lock file
2. Deploy previous version
```

**Common Breaking Changes by Framework**:

| Framework | Common Breaking Changes |
|-----------|------------------------|
| React | Hook changes, prop deprecations |
| Vue | Composition API, lifecycle changes |
| Express | Middleware signature changes |
| Django | Settings changes, URL patterns |
| Flask | Blueprint changes, configuration |
| Spring | Annotation changes, bean scoping |

### Step 4: Execute Upgrades by Ecosystem

#### Node.js/npm

```bash
# Check outdated packages
npm outdated

# Update all patch/minor versions (safe)
npm update

# Update specific package to latest
npm install package@latest

# Update with breaking changes (interactive)
npx npm-check-updates -i

# Fix vulnerabilities automatically
npm audit fix

# Fix with breaking changes (careful!)
npm audit fix --force

# Clean install from lock file
rm -rf node_modules
npm ci
```

**package.json Version Strategies**:

```json
{
  "dependencies": {
    "exact-version": "1.2.3",        // Exact version (most safe)
    "patch-updates": "~1.2.3",       // Allow 1.2.x (safe)
    "minor-updates": "^1.2.3",       // Allow 1.x.x (default, usually safe)
    "any-version": "*",              // Any version (dangerous)
    "range": ">=1.2.3 <2.0.0"        // Explicit range
  }
}
```

#### Python/pip

```bash
# Check outdated packages
pip list --outdated

# Upgrade specific package
pip install --upgrade package

# Upgrade all packages (careful!)
pip list --outdated --format=json | \
  python -c "import json,sys;print('\n'.join([p['name'] for p in json.load(sys.stdin)]))" | \
  xargs -n1 pip install -U

# Security audit
pip-audit

# Generate requirements with pinned versions
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

**requirements.txt Version Strategies**:

```
# Exact version (most reproducible)
package==1.2.3

# Minimum version
package>=1.2.3

# Compatible release (1.2.x)
package~=1.2.3

# Version range
package>=1.2.3,<2.0.0
```

#### Python/uv (Modern)

```bash
# Update all dependencies
uv pip compile pyproject.toml -o requirements.txt --upgrade

# Update specific package
uv pip compile pyproject.toml -o requirements.txt --upgrade-package package

# Sync environment to lock file
uv pip sync requirements.txt
```

#### Go Modules

```bash
# Check for updates
go list -m -u all

# Update all dependencies
go get -u ./...

# Update specific package
go get -u package@latest

# Tidy up go.mod
go mod tidy

# Verify dependencies
go mod verify
```

### Step 5: Manage Lock Files

**Lock File Best Practices**:

| Do | Don't |
|----|-------|
| Commit lock files to version control | Ignore lock files in .gitignore |
| Use `npm ci` / `pip sync` in CI | Use `npm install` in CI |
| Update lock file in dedicated commits | Mix code and lock file changes |
| Review lock file diffs | Blindly approve lock file changes |

**Lock File Hygiene**:

```bash
# Node.js - Regenerate lock file
rm package-lock.json
npm install

# Python - Regenerate requirements
pip-compile --upgrade pyproject.toml

# Go - Regenerate go.sum
rm go.sum
go mod tidy
```

### Step 6: Handle Vulnerability Patches

**Emergency Vulnerability Patching**:

```markdown
## Vulnerability Response: [CVE-XXXX-XXXXX]

### Severity Assessment
- **CVSS Score**: [score]
- **Severity**: Critical/High/Medium/Low
- **Exploitable**: Yes/No/Unknown
- **Affected Package**: [package@version]
- **Fixed In**: [version]

### Immediate Actions
1. [ ] Assess exposure in production
2. [ ] Check if exploitable in our context
3. [ ] Identify patched version
4. [ ] Test upgrade locally
5. [ ] Deploy fix

### Mitigation (if upgrade not immediately possible)
- [ ] WAF rules
- [ ] Input validation
- [ ] Feature disable
- [ ] Network isolation

### Patch Commands
```bash
# npm
npm audit fix
# or for specific package
npm install vulnerable-package@patched-version

# pip
pip install vulnerable-package>=patched-version

# go
go get vulnerable-package@patched-version
```

### Verification
- [ ] `npm audit` / `pip-audit` shows no vulnerabilities
- [ ] Tests pass
- [ ] Application functions correctly
- [ ] Deployed to production
```

## Best Practices

- **Pin versions in production** - Reproducible builds
- **Update regularly** - Small, frequent updates are safer
- **Review changelogs** - Before any major update
- **Test thoroughly** - Full test suite after updates
- **Commit lock files** - Ensure reproducibility
- **Separate dependency commits** - Easy to revert
- **Monitor for vulnerabilities** - Automated scanning
- **Document decisions** - Why versions were chosen

## Common Patterns

### Pattern 1: Dependency Update PR Template

```markdown
## Dependency Updates

### Changes
- `package-a`: 1.0.0 → 1.1.0 (minor)
- `package-b`: 2.3.0 → 3.0.0 (major - see breaking changes)

### Breaking Changes
[Details for package-b upgrade]

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual smoke test

### Rollback
```bash
git revert <this-commit>
npm ci  # or pip sync, etc.
```
```

### Pattern 2: Automated Dependency Updates

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      development-dependencies:
        dependency-type: "development"
      production-dependencies:
        dependency-type: "production"
        update-types:
          - "minor"
          - "patch"
```

### Pattern 3: Version Constraint Strategy

```markdown
## Version Constraint Policy

### Production Dependencies
- Use exact versions: `==1.2.3` or `1.2.3`
- Update via explicit PR

### Development Dependencies
- Allow minor updates: `^1.2.3` or `~=1.2.3`
- Auto-merge patch updates

### Security Exceptions
- Always allow security patches regardless of version jump
- Review within 24 hours of CVE publication
```

## Quality Checklist

- [ ] All dependencies audited for vulnerabilities
- [ ] Outdated packages identified
- [ ] Breaking changes reviewed
- [ ] Lock file committed
- [ ] Full test suite passing
- [ ] Manual smoke test completed
- [ ] Rollback plan documented
- [ ] Deployment monitored

## Related Skills

- `security-review` - Security implications of dependencies
- `cicd-architect` - Automated dependency updates in CI
- `legacy-modernizer` - Major framework upgrades
- `pre-commit-checklist` - Dependency checks before commit

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: awesome-claude-code-subagents patterns, package management best practices


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
