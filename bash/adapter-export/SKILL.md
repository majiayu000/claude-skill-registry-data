---
name: adapter-export
description: "Export a generated subagent package (subagents/<slug>/) into its installed runtime adapter, rendered deterministically from the package's profile.yaml. Use when a profile changes and the derived adapter must be regenerated and reinstalled — the export step (Step 8) of the authoring pipeline. Re-run after any profile.yaml edit."
---

# Skill: adapter-export

**Purpose:** Export generated subagent package into a Claude Code runtime adapter.

---

## Input

- Subagent slug
- `subagents/<slug>/profile.yaml` (must exist and pass Phase 8)

---

## Steps

### 1. Run export script

```bash
python -m tools.subagent_factory.cli export <slug>
```

This generates:
- `subagents/<slug>/adapters/claude-code/<slug>.md` — canonical adapter
- `.claude/agents/generated/<slug>.md` — installed runtime adapter

### 2. Verify adapter header

Adapter must contain:
- `name: <slug>`
- `description:` with role + triggers + exclusion
- `tools:` list
- `model:` field
- `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->` comment
- Canonical package path reference

### 3. Check for duplicate agent name

Verify no other file in `.claude/agents/` uses the same `name:` field.
If duplicate found, report conflict before installing.

### 4. Verify adapter body completeness

Adapter body must include:
1. Role
2. When to use
3. When NOT to use
4. Required inputs
5. Supported modes
6. Output contract per mode
7. Quality bar
8. Forbidden behaviours
9. Handoff rules
10. Source of truth policy
11. Canonical package path
12. Instruction to read package files

---

## Output

- `subagents/<slug>/adapters/claude-code/<slug>.md` written
- `.claude/agents/generated/<slug>.md` installed
