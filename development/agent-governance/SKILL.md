---
name: agent-governance
description: |
  Protocol health check skill - ensures AI protocol layer integrity and compliance.
  Supports file validation, naming conventions, and token analysis.
---

# Agent Governance Skill

> Protocol health check - ensures AI protocol layer integrity and compliance.

---

## Overview

| Attribute | Value |
|-----------|-------|
| Name | Agent Governance |
| Version | 2.0.0 |
| Type | Protocol Maintenance |
| Trigger | After protocol changes |

---

## Capabilities

1. **Required Files Check** - Verify all required files exist
2. **Naming Convention Check** - Ensure kebab-case compliance
3. **Engine Pollution Detection** - Check for project-specific info in core/
4. **Token Statistics** - Analyze protocol document token usage
5. **Link Validation** - Check internal links

---

## Usage

```bash
# Full check
python $AGENT_DIR/scripts/lint-protocol.py

# Token statistics
python $AGENT_DIR/scripts/token-counter.py
```

---

## Check Rules

### Required Files

```
$AGENT_DIR/
├── start-here.md
├── index.md
├── core/
│   ├── core-rules.md
│   ├── instructions.md
│   └── conventions.md
├── project/
│   ├── context.md
│   └── tech-stack.md
└── meta/
    └── protocol-adr.md
```

### Naming Convention

```python
NAMING_RULES = {
    "markdown_files": r"^[a-z0-9]+(-[a-z0-9]+)*\.md$",
    "directories": r"^[a-z0-9]+(-[a-z0-9]+)*$",
    "exceptions": ["SKILL.md"],
}
```

---

*This skill is a portable component, reusable across projects*
*Version: 2.0.0*
