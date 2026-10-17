---
name: usagecheck
description: Detect which coding CLI is running (Claude Code, Codex, or Grok) and report that agent's usage/rate-limit data through its own mechanism, normalized into one report shape.
compatibility: |
  - Runtime: Node.js 18+ (ESM)
  - Dependencies: None (Node built-ins only)
  - Permissions: read:home-config, write:claude-cache (optional)
---

# Usage Check

**ID**: `usagecheck`
**Version**: 0.1.0
**Status**: Active (Claude Code path confirmed; Codex/Grok paths heuristic — see docs/USAGE.md)
**Owner**: Soren (Cast Iron Forge)

---

## Purpose

Claude Code, Codex, and Grok each expose usage/rate-limit data through incompatible
mechanisms. `/usagecheck` detects which one is running, dispatches to that
agent's adapter, and returns a single normalized report instead of three
different ad hoc scripts.

---

## Trigger

```
/usagecheck
/usagecheck --agent codex
/usagecheck --hook   (Claude Code hook mode — drop-in for the original stdin-JSON script)
```

---

## Input Schema

```typescript
interface SkillInput {
  agent?: "claude-code" | "codex" | "grok";  // Optional. Force detection.
  stdinText?: string;                         // Optional. Raw hook JSON (Claude Code path).
  configPath?: string;                        // Optional. usagecheck.config.json override.
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  agent: "claude-code" | "codex" | "grok" | "unknown";
  detection: { agent: string; method: "forced" | "env" | "path" | "none"; confidence: string };
  available: boolean;
  usage: Record<string, any> | null;
  message: string;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Message | Handler |
|------|---------|---------|
| `AGENT_UNDETECTED` | No agent detected and none forced | Pass `--agent` explicitly |

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Troubleshooting, and Integration:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For workflow examples, adapter internals, and why Codex/Grok are heuristic:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
