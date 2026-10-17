---
name: toolforge-registry-manager
description: Sole writer of Toolforge registry.json. Append-only semantics with audit logging for all mutations.
compatibility: |
  - Runtime: PowerShell 5.1+
  - Dependencies: None
---

# Toolforge Registry Manager

Manages `docs/toolforge/registry.json` with append-only semantics and audit trail.

## Trigger

```powershell
pwsh src/registry.ps1 -Action <add|get|list|quarantine> [options]
```

## Input Schema

```typescript
interface RegistryInput {
  action: "add" | "get" | "list" | "quarantine";
  pluginId?: string;      // Required for add, get, quarantine
  path?: string;          // Required for add
  checksum?: string;      // Required for add
  category?: string;      // Optional filter for list
  reason?: string;        // Required for quarantine
}
```

## Output Schema

```typescript
interface RegistryOutput {
  status: "success" | "error";
  action: string;
  result: any;           // Entry, array, or confirmation
  auditEntry?: string;   // Audit log line written
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
