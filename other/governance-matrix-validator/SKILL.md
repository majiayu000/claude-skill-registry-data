---
name: governance-matrix-validator
description: Use when auditing CI governance workflows, triaging cross-repo script dependencies across toolforge, sigil, and cic-ingestion, or investigating masked failures from permissive CI job configurations.
compatibility: |
  - Runtime: Node.js 18+ / ESM
  - Dependencies: js-yaml, @toolforge/governance-core
  - Permissions: read:repo, write:artifacts
---

# Governance Matrix Validator Specification

**ID**: `governance-matrix-validator`
**Version**: 0.1.0
**Status**: Active
**Owner**: Toolforge Core

---

## Purpose

Validate CI governance matrix workflows against physical repository states. Unmasks hidden errors suppressed by `continue-on-error: true` and verifies cross-repository script and dependency contracts across `toolforge`, `sigil`, and `cic-ingestion`.

---

## Trigger

Exact prompts that invoke this skill:

```
governance-matrix-validator
/governance-matrix-validator
validate governance gates
check governance matrix for masked failures
```

---

## Input Schema

```typescript
interface GovernanceMatrixValidatorInput {
  workflowPath?: string;       // Optional. Path to workflow file (default: .github/workflows/ci-governance-matrix.yml)
  repoScope?: string[];        // Optional. Subset of repos to audit (default: ['toolforge', 'sigil', 'cic-ingestion'])
  unmaskOnly?: boolean;        // Optional. Flag only continue-on-error masking without checking repo disk targets
}
```

---

## Output Schema

```typescript
interface GovernanceMatrixValidatorOutput {
  status: "HEALTHY" | "DEGRADED" | "ACTION_REQUIRED" | "ERROR";
  maskedFailures: Array<{
    jobName: string;
    stepName: string;
    reason: string;
  }>;
  repoFindings: Array<{
    repo: "toolforge" | "sigil" | "cic-ingestion" | string;
    issueCode: string;
    severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
    missingTarget: string;
    suggestedFix: string;
  }>;
  recommendedActions: string[];
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional error codes:

| Code | Message | Handler |
|---|---|---|
| `GOV_WORKFLOW_NOT_FOUND` | Specified workflow file does not exist | Verify path in `.github/workflows/` |
| `GOV_REPO_NOT_MOUNTED` | Linked sibling repo directory is inaccessible | Confirm checkout paths for `sigil` and `cic-ingestion` |
| `GOV_MASKED_FAILURE_DETECTED` | Job contains continue-on-error hiding critical steps | Remove permissive flag or fix upstream failure |

---

## Core Rationalizations & Red Flags

| Excuse / Rationalization | Reality |
|---|---|
| "The workflow run is green, so all governance gates pass" | `continue-on-error: true` conceals failing steps. Always inspect underlying step outcomes. |
| "A missing script in a sibling repo is an external issue" | Matrix workflows execute across repo boundaries; missing scripts break matrix guarantees. |
| "Temporary masking in CI is harmless during refactors" | Masked checks easily become permanent blind spots. Fix the root cause or skip the job explicitly. |

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Troubleshooting, and Integration:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For workflow examples and deep integration patterns:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
