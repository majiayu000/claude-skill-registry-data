---
name: wiki-governance-sync
description: Use when synchronizing knowledge base and Obsidian vault structures across multiple repositories, enforcing wiki schema conventions, checking topic tag consistency, or archiving stale sync runs.
compatibility: |
  - Runtime: Node.js 18+, TypeScript 5.0+
  - Dependencies: Obsidian vault at C:\dev\kb-sync\obsidian\vault\wiki, wiki-schema definitions
  - Permissions: read:repo, write:repo
---

# wiki-governance-sync

Multi-repository knowledge base synchronization and schema governance engine. Validates entity definitions, aligns wikilinks across workspaces, enforces topic and metadata schemas, and archives superseded sync runs.

## When to Use

- Weekly scheduled wiki governance audit passes
- Cross-repository knowledge base synchronization triggers
- Resolving documentation drift and unaligned wikilinks across repos
- Enforcing Obsidian schema conventions and tag taxonomies

## Trigger & Usage

```bash
# Perform dry-run governance check across all target repos
invoke wiki-governance-sync { "action": "audit", "dryRun": true }

# Execute full synchronization and schema enforcement
invoke wiki-governance-sync { "action": "sync", "autoRemediate": true }
```

## Input Schema

```typescript
interface SkillInput {
  action: "audit" | "sync" | "archive";
  vaultRoot?: string;         // Default: C:\dev\kb-sync\obsidian\vault\wiki
  targetRepos?: string[];     // Optional list of repo paths
  autoRemediate?: boolean;    // Automatically correct fixable schema issues
  dryRun?: boolean;           // Run in non-modifying preview mode
  verbose?: boolean;          // Enable detailed log emission
}
```

## Output Schema

```typescript
interface SchemaFinding {
  type: "NAMING_VIOLATION" | "TAG_INCONSISTENCY" | "BROKEN_LINK" | "ORPHANED_PAGE";
  file: string;
  message: string;
  remediated: boolean;
}

interface SkillOutput {
  status: "success" | "warning" | "error";
  syncedRepos: string[];
  findingsCount: number;
  remediatedCount: number;
  findings: SchemaFinding[];
  archivedRunsCount?: number;
  timestamp: string;
}
```

## Error Handling

| Code | Message | Handler | Escalation |
|------|---------|---------|------------|
| `VAULT_NOT_FOUND` | Canonical vault root not accessible | Fail | Check `obsidian/vault/wiki` path |
| `SCHEMA_ERROR` | Schema definitions corrupt or unreadable | Fail | Inspect `wiki-schema` definitions |
| `WRITE_LOCKED` | Vault is locked by another process | Retry | Wait for concurrent sync to release |

---

## Quick Reference

| Action | Purpose | Safe in Production |
|--------|---------|-------------------|
| `audit` | Read-only scan of naming, tags, and link integrity | Yes |
| `sync` | Cross-repo push/pull and schema alignment | Yes (when dryRun=false) |
| `archive` | Prune or archive previous sync runs older than threshold | Yes |
