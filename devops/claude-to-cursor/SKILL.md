---
name: claude-to-cursor
description: >
  Convert Claude Code skills to Cursor-compatible rules (.mdc/.md files) for sharing
  or use in Cursor workspaces. Does NOT modify local Claude Code setup — outputs go
  to a separate repo. Trigger on: "convert to cursor", "cursor rules", "port to cursor",
  ".mdc", "cursor format", or any request to export skills for Cursor users.
---

# Claude to Cursor Converter

Export Claude Code skills as Cursor-compatible rule files for sharing. All output
goes to a dedicated repo — never modifies local Claude Code configuration.

## Cursor Rule Format (.mdc)

Cursor uses `.mdc` files (Markdown with frontmatter) in `.cursor/rules/`:

```markdown
---
description: One-line description (used for rule matching)
globs:
  - "**/*.py"          # optional: file patterns this rule applies to
alwaysApply: false      # true = always loaded, false = matched by description
---

# Rule Title

Rule content here. Markdown format.
```

Key differences from Claude SKILL.md:
- Extension: `.mdc` (not `.md` — Cursor's convention for rules)
- No `name:` field — filename is the identifier
- `globs:` for file-pattern matching (Claude uses description triggers)
- `alwaysApply:` replaces Claude's always-loaded behavior
- No `references/` subdirectory convention — inline or split into companion rules

## Conversion Process

### 1. Classify the skill

| Type | Converts? | Notes |
|---|---|---|
| Persona (infosec-architect, cpa-tax-specialist) | Yes | Direct conversion, strong match |
| Workflow (tdd, write-a-prd, prd-to-plan) | Yes | Direct conversion |
| Code quality (code-consistency, code-quality) | Yes | Use globs for language-specific rules |
| Tool-specific (token-miser, budi-analytics) | No | Claude Code-only features |
| Infrastructure (fleet-manager, openclaw-ops) | Partial | Remove Claude-specific tool refs |

### 2. Transform content

1. Strip YAML frontmatter, rewrite as Cursor frontmatter (description, globs, alwaysApply)
2. Remove Claude-specific tool references (Agent tool, Bash tool, Read/Write/Edit, MCP)
3. Inline small reference files (<200 lines) directly
4. Large references → separate `.mdc` companion files
5. Replace "Claude Code" with generic "AI assistant" where contextual
6. Add attribution: `<!-- Converted from Claude Code skill: <name> -->`

### 3. Output structure

```
claude-to-cursor/
├── rules/                    # Converted .mdc files
│   ├── tdd.mdc
│   ├── tdd-tests-ref.mdc    # Large reference companion
│   ├── code-quality.mdc
│   └── ...
├── agents/                   # Converted agent files
│   └── ...
└── scripts/
    └── convert.sh            # Batch conversion script
```

### 4. What to skip

- token-miser (Claude Code subagent routing — no Cursor equivalent)
- budi-analytics (Claude Code hook analytics — Cursor-specific)
- skill-updater (meta-skill for Claude Code skill management)
- inbound-sync (claude.ai ↔ Claude Code sync workflow)
- openclaw-ops (primary-host-specific deployment)
- fleet-manager (SSH/Ansible fleet ops — not IDE-relevant)
- ansible-hardening (infrastructure, not IDE-relevant)

## Rules

- NEVER modify local Claude Code skills or configuration
- All output goes to the claude-to-cursor repo only
- Keep attribution on all converted files
- Test in Cursor before marking as ready
- .mdc extension for rules, .md for agents
