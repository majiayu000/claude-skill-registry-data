---
name: doc-sync-drift-audit
description: Use when validating documentation build integrity, inspecting doc-sync cache refusal or version mismatches, diagnosing broken sidebar references, or auditing documentation drift across toolforge wiki targets.
compatibility: |
  - Runtime: Node.js 18+ / ESM
  - Dependencies: @cic/doc-sync, @toolforge/drift-receipt
  - Permissions: read:repo, write:artifacts
---

# Doc-Sync Drift Audit Specification

**ID**: `doc-sync-drift-audit`
**Version**: 0.1.0
**Status**: Active
**Owner**: Toolforge Core

---

## Purpose

Detect, diagnose, and report documentation drift in the Toolforge unified wiki and documentation build pipeline. Validates cross-product sidebar links, verifies cache schema versioning, and persists machine-readable drift receipts.

---

## Trigger

Exact prompts that invoke this skill:

```
doc-sync-drift-audit
/doc-sync-drift-audit
check doc sync for drift
audit documentation drift
```

---

## Input Schema

```typescript
interface DocSyncDriftAuditInput {
  registryPath?: string;       // Optional. Path to doc-sync registry manifest (default: config/doc-sync.json)
  strictCache?: boolean;       // Optional. Enforce hard failure on cache schema mismatch (default: true)
  targetVault?: string;        // Optional. Specific wiki vault or docs target to scope the audit
  persistReceipt?: boolean;    // Optional. Write receipt to drift receipts/ (default: true)
}
```

---

## Output Schema

```typescript
interface DocSyncDriftAuditOutput {
  status: "PASS" | "DRIFT_DETECTED" | "CACHE_REFUSED" | "ERROR";
  driftStatus: "CLEAN" | "STALE_PAGES" | "BROKEN_LINKS" | "SCHEMA_MISMATCH";
  stalePagesCount: number;
  brokenLinks: Array<{
    sourceFile: string;
    targetLink: string;
    reason: "TARGET_MISSING" | "ANCHOR_NOT_FOUND" | "CROSS_PRODUCT_UNRESOLVED";
  }>;
  cacheValidity: {
    expectedVersion: string;
    foundVersion: string;
    accepted: boolean;
  };
  receiptPath?: string;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional error codes:

| Code | Message | Handler |
|---|---|---|
| `DOC_SYNC_CACHE_REFUSED` | Cache schema version mismatch detected | Invalidate cache index and run clean rebuild |
| `DOC_SYNC_BROKEN_SIDEBAR` | Sidebar contains dead links or missing anchors | Patch sidebar topology or restore missing docs |
| `DOC_SYNC_REGISTRY_NOT_FOUND` | Doc-sync registry file missing or unreadable | Verify path in `config/doc-sync.json` |

---

## Core Rationalizations & Red Flags

| Excuse / Rationalization | Reality |
|---|---|
| "Cache version mismatch is just a warning, proceed anyway" | Mismatched cache serves stale topology and dead anchors. Invalidate immediately. |
| "Sidebar links can point to future planned pages" | Unresolved sidebar links break static site generation and fail CI gates. |
| "Skip persisting drift receipt for quick checks" | Drift receipts provide the audit trail for automated remediation and release gates. |

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Troubleshooting, and Integration:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For workflow examples and deep integration patterns:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
