---
name: obsidian-ingest-wiki
description: Validates staged Obsidian raw sources and generates Claude Code prompts for 8-phase wiki semantic synthesis. Implements Karpathy LLM-wiki pattern with human-in-the-loop workflow.
compatibility: |
  - Runtime: Node.js 18+, TypeScript 5.0+
  - Dependencies: configs/obsidian.yaml (kb-sync project)
  - Permissions: read:repo, read:config
---

# obsidian-ingest-wiki

Validates staged Obsidian raw sources and generates Claude Code prompts for 8-phase wiki semantic synthesis.

## Trigger

```bash
# Validate staging directory
invoke obsidian-ingest-wiki { action: "validate" }

# Generate prompt for wiki synthesis
invoke obsidian-ingest-wiki { action: "prompt" }
```

## Input Schema

```typescript
interface SkillInput {
  action: "validate" | "prompt";
  stagingPath?: string;      // Auto-discovered if omitted
  vaultRoot?: string;        // Read from config if omitted
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "valid" | "invalid" | "success" | "error";
  message: string;
  stagingPath?: string;
  vaultRoot?: string;
  prompt?: string;
  fileCount?: number;
  errors?: string[];
  timestamp: string;
}
```

## Error Handling

| Code | Message | Handler | Escalation |
|------|---------|---------|------------|
| `STAGING_NOT_FOUND` | Staging directory does not exist | Fail | Check vault path in obsidian.yaml |
| `MANIFEST_MISSING` | Manifest file not found in staging | Fail | Re-run kb-sync pipeline |
| `INVALID_ACTION` | Unknown action | Fail | Use "validate" or "prompt" only |
| `CONFIG_MISSING` | Obsidian configuration not found | Fail | See Skill Operator Guide |

---

## Full Reference

For Setup, Requirements, Configuration, Integration, Testing:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For capabilities, examples, and troubleshooting:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
