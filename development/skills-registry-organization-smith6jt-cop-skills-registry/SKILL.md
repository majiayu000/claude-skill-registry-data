---
name: skills-registry-organization
description: "Pattern for organizing Skills Registry as a shared submodule across projects"
author: KINTSUGI Team
date: 2025-12-12
---

# Skills Registry Organization

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-12 |
| **Goal** | Organize skills for cross-project reuse while keeping project-specific skills isolated |
| **Environment** | Git submodule setup |
| **Status** | Success |

## Context
When using a Skills Registry across multiple projects (e.g., image processing pipeline + algo trading), need to determine which skills transfer and how to organize them.

## Verified Structure

```
Skills_Registry/plugins/
├── general/              # Cross-project Python/dev skills
│   ├── pypi-collision-fix/
│   ├── type-checking-pattern/
│   ├── dependency-deprecation/
│   └── conda-multi-account-hipergator/
├── scientific/           # Scientific computing patterns
│   ├── project-data-separation/
│   └── windows-cupy-nvrtc/
├── kintsugi/             # Project-specific skills
│   └── basic-caching-evaluation/
└── templates/            # Examples and templates
    └── example-skill/
```

## Category Guidelines

| Category | Contents | Transfers To |
|----------|----------|--------------|
| `general/` | Python packaging, linting, environments, deprecation patterns | All projects |
| `scientific/` | GPU patterns, data pipelines, scientific computing | Scientific projects |
| `{project}/` | Domain-specific learnings (e.g., microscopy, trading) | Only that project |
| `templates/` | Skill creation examples | All projects |

## Submodule Setup

```bash
# Add Skills_Registry as submodule
git submodule add https://github.com/yourorg/Skills_Registry.git Skills_Registry

# Update .claude/commands/advise.md search paths
## Search Paths
- `Skills_Registry/plugins/general/*/`
- `Skills_Registry/plugins/scientific/*/`
- `Skills_Registry/plugins/{your-project}/*/`
- `Skills_Registry/plugins/templates/*/`
```

## Workflow for Adding Skills

```bash
# After /retrospective creates a new skill
cd Skills_Registry
git add -A
git commit -m "feat: add skill-name from session"
git push origin main

# Update submodule reference in parent repo
cd ..
git add Skills_Registry
git commit -m "chore: update Skills_Registry submodule"
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Single flat plugins/ directory | Hard to know which skills transfer | Categorize by scope (general/scientific/project) |
| Embedding skills directly in each project | Lost cross-project learnings | Use submodule for shared registry |
| All skills in project-specific category | General Python skills didn't transfer | Actively classify skills during /retrospective |
| No category guidelines | Contributors put skills in wrong places | Document category criteria in CLAUDE.md |

## Key Insights

- **Trigger conditions matter more than categories**: `/advise` searches descriptions, so good triggers make skills discoverable regardless of folder
- **General skills are most valuable**: pypi-collision-fix, type-checking-pattern apply to any Python project
- **Project-specific skills don't pollute**: Domain-specific triggers (e.g., "BaSiC illumination") won't match unrelated projects
- **Submodule workflow is simple**: Just commit in submodule, push, then update parent

## Checklist for New Skills

- [ ] Is this skill general Python/dev? → `general/`
- [ ] Is this scientific computing but not project-specific? → `scientific/`
- [ ] Is this domain-specific (microscopy, trading, etc.)? → `{project}/`
- [ ] Does description have specific trigger conditions?
- [ ] Is Failed Attempts table filled in?

## References
- Git submodules documentation
- KINTSUGI Skills Registry reorganization (2025-12-12)
