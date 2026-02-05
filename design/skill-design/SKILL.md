---
name: skill-design
description: Best practices for skill structure and types. Use when creating skills.
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
---

# Skill Anatomy

```
skill-name/
├── SKILL.md         # Required: core instructions (<500 words)
├── scripts/         # Optional: executable code
├── references/      # Optional: detailed docs (load on-demand)
└── assets/          # Optional: templates, images
```

---

# Skill Types

| Type | Freedom | Use when | Structure |
|------|---------|----------|-----------|
| Knowledge | High | Multiple approaches, context-dependent | SKILL.md + references/ |
| Hybrid | Medium | Guidance + scripts needed | SKILL.md + scripts/ + references/ |
| Tool | Low | Deterministic, repeatable ops | SKILL.md + scripts/ |
| Expert | Very Low | Complex internals, undocumented APIs | Full + validation/ |

---

# When to Script

- Same code rewritten repeatedly → Script
- File format manipulation → Script
- Reliability critical → Script
- External API/tool integration → Script

---

# When to Hook (Enforcement Logic)

**Rule**: If behavior MUST happen, use hooks. Documentation cannot enforce.

| Requirement Type | Example | Solution |
|------------------|---------|----------|
| **MUST/REQUIRED** | "MUST use Skill tool" | PreToolUse hook to warn/block |
| **Validation** | "Schema must be valid" | PostToolUse hook to validate |
| **Prevention** | "Never commit secrets" | PreToolUse hook to block |
| **Guidance** | "Consider using X" | Documentation only (OK) |

## Hook vs Documentation Decision

```
If keyword in ["MUST", "REQUIRED", "CRITICAL", "강제", "반드시"]:
    → Implement as Hook (documentation alone WILL be ignored)

If keyword in ["should", "consider", "recommend"]:
    → Documentation is sufficient
```

## Hookify Checklist

Before finalizing skill:
1. Search for enforcement keywords (MUST, REQUIRED, CRITICAL)
2. Each enforcement requirement → corresponding hook exists?
3. If no hook → either create hook OR downgrade to "should"

**Example**:
- ❌ "MUST use Skill() tool" in SKILL.md → Agents ignore this
- ✅ PreToolUse hook on Read/Grep/Glob warns when skill files accessed directly

---

# SKILL.md Structure

```yaml
---
name: skill-name
description: What + when to use (triggers skill loading)
allowed-tools: ["Tool1", "Tool2"]
---
```

```markdown
# Skill Name

[2-3 sentence overview]

## Quick Start
[Fastest path]

## Workflow
1. Step 1
2. Step 2

## Scripts
| Script | Purpose | Usage |
|--------|---------|-------|

## Key Principles
- Principle 1
- Principle 2

For advanced: [references/advanced.md]
```

---

# Tool Restrictions

```yaml
# Knowledge (read-only)
allowed-tools: ["Read", "Grep", "Glob"]

# Hybrid (guidance + generation)
allowed-tools: ["Read", "Write", "Grep", "Glob", "Bash"]

# Tool (file manipulation)
allowed-tools: ["Read", "Write", "Bash"]
```

---

# Checklist

- SKILL.md < 500 words
- Description includes trigger phrases
- Scripts tested
- References linked
- allowed-tools matches purpose
- **Hookify check**: Enforcement keywords (MUST/REQUIRED/CRITICAL) → hooks exist
