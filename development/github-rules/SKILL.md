---
name: github-rules
description: Guide for configuring GitHub repository rules, branch protection, rulesets, CODEOWNERS, and security policies. Use when users need to set up branch protection rules, configure required reviews, enforce status checks, manage merge strategies, or implement repository security policies.
---

# GitHub Rules Configuration

Configure repository rules, branch protection, and security policies for GitHub repositories.

## Decision Tree

```
User request → What type of rules?
    │
    ├─ Branch Protection (legacy) → See references/branch-protection.md
    │   └─ Single branch, simple rules
    │
    ├─ Rulesets (modern) → See assets/rulesets/
    │   ├─ Multiple branches/tags
    │   ├─ Organization-wide rules
    │   └─ More granular control
    │
    ├─ Code Review → See references/codeowners.md
    │   ├─ CODEOWNERS file
    │   └─ Required reviewers
    │
    └─ Security Policies → See references/security.md
        ├─ SECURITY.md
        ├─ Dependabot
        └─ Secret scanning
```

## Quick Start

### Option 1: GitHub CLI (Recommended)

```bash
# View current branch protection
gh api repos/{owner}/{repo}/branches/main/protection

# View rulesets
gh api repos/{owner}/{repo}/rulesets

# Apply ruleset from JSON
gh api repos/{owner}/{repo}/rulesets \
  --method POST \
  --input ruleset.json
```

### Option 2: GitHub UI

1. Go to Settings > Rules > Rulesets (modern)
2. Or Settings > Branches (legacy branch protection)

### Option 3: Terraform/Pulumi

See `references/infrastructure-as-code.md` for IaC approaches.

## Rulesets vs Branch Protection

| Feature | Branch Protection | Rulesets |
|---------|------------------|----------|
| Multiple branches | One rule per branch | Pattern matching |
| Tags | Not supported | Supported |
| Organization-wide | No | Yes |
| Bypass permissions | Limited | Granular |
| Import/Export | No | JSON export |
| API | REST only | REST + GraphQL |

**Recommendation:** Use Rulesets for new projects. Branch Protection for legacy compatibility.

## Common Configurations

### Protect Main Branch

```bash
# Using gh CLI
gh api repos/{owner}/{repo}/rulesets --method POST --input - << 'EOF'
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews_on_push": true,
      "require_last_push_approval": true
    }},
    {"type": "required_status_checks", "parameters": {
      "required_status_checks": [
        {"context": "ci"}
      ],
      "strict_required_status_checks_policy": true
    }}
  ]
}
EOF
```

### Require Signed Commits

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input - << 'EOF'
{
  "name": "Signed commits",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "required_signatures"}
  ]
}
EOF
```

### Protect Release Tags

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input - << 'EOF'
{
  "name": "Protect releases",
  "target": "tag",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/tags/v*"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "creation"},
    {"type": "deletion"}
  ]
}
EOF
```

## Template Selection Guide

| Use Case | Template |
|----------|----------|
| Solo developer | `solo-developer.json` |
| Small team (2-5) | `small-team.json` |
| Standard team | `standard-team.json` |
| Enterprise | `enterprise.json` |
| Open source | `open-source.json` |
| Monorepo | `monorepo.json` |

## Reference Files

- **Branch Protection**: See [references/branch-protection.md](references/branch-protection.md)
- **Rulesets API**: See [references/rulesets-api.md](references/rulesets-api.md)
- **CODEOWNERS**: See [references/codeowners.md](references/codeowners.md)
- **Security Policies**: See [references/security.md](references/security.md)
- **Infrastructure as Code**: See [references/infrastructure-as-code.md](references/infrastructure-as-code.md)

## Best Practices

1. **Start restrictive**: Easier to loosen than tighten
2. **Use rulesets**: More flexible than branch protection
3. **Require reviews**: At least 1 for main branch
4. **Enforce status checks**: CI must pass before merge
5. **Enable signed commits**: For sensitive repositories
6. **Document bypass**: Who can bypass and why
7. **Audit regularly**: Review rules quarterly
