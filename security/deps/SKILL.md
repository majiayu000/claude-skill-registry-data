---
name: deps
description: Manage dependencies and fix CVEs — check outdated packages, update a specific package, run security audit, explain why a package is installed, or deduplicate. Read claude/cve-policy.md for the decision tree.
---

# Deps Skill

Manage project dependencies following the CVE decision tree.

## Usage

```
/deps check              # Show outdated packages
/deps update lodash      # Update specific package
/deps audit              # Run security audit
/deps why express        # Explain why a package is installed
/deps dedupe             # Deduplicate dependency tree
```

## Instructions

**First:** Read `claude/cve-policy.md` for the CVE decision tree.

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `check` | Show outdated packages |
| `update <package>` | Update specific package |
| `audit` | `npm audit` / `pip audit` / `cargo audit` / `bundle audit` |
| `why <package>` | `npm why <package>` / `pip show <package>` |
| `dedupe` | `npm dedupe` / `pnpm dedupe` |
| (empty) | Run `check` + `audit` |

### By Package Manager:

**npm / pnpm / yarn:**
```bash
pnpm outdated 2>&1 | head -40
pnpm audit --audit-level moderate 2>&1 | head -40
```

**pip / uv / poetry:**
```bash
pip list --outdated 2>&1 | head -30
pip-audit 2>&1 | head -40
```

**cargo:**
```bash
cargo outdated 2>&1 | head -30
cargo audit 2>&1 | head -40
```

### CVE Response Rules (from claude/cve-policy.md):
- Critical/High severity → upgrade immediately, test, PR same day
- Medium severity → schedule within current sprint
- Low severity → batch with next dependency update cycle
- NEVER blindly upgrade majors — check breaking changes first
